"""Retained legacy attempt execution and closure preparation.

Owns prompt/attempt construction and the private run_next compatibility workflow.
The public run-next command remains reporting-only. No new legacy capability is
introduced; existing inspection fixtures still need real attempt/closure evidence.
Dependencies: authority, records, execution contracts, flow/run policy, manifest
and ledger rules, serialization, Git, storage and worker transport.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from . import run_records
from . import run_authority
from . import execution_contracts
from . import flow_policy
from . import ledger as ledger_rules
from . import record_serialization
from . import run_policy
from . import task_manifest
from . import controller_git as git
from . import codex_worker as worker
from . import run_storage as storage


def render_worker_prompt(
    *,
    task_id: str,
    brief_path: str,
    task_instructions: str,
    policy: dict[str, Any],
) -> str:
    run_policy.validate_run_policy(policy)
    return "\n".join(
        (
            f"Task: {task_id}",
            f"Authoritative brief: {brief_path}",
            "",
            task_instructions.rstrip(),
            "",
            "Worker boundary:",
            "- Work only on the selected task and its allowed paths.",
            "- Do not commit, even if the controller policy permits a later controller-owned commit.",
            "- Do not update the orchestration ledger or select another task.",
            "- Do not change the controller, installed skills, or permission envelope.",
            "- Return the required structured result; it is a claim pending independent inspection.",
            "",
        )
    )


def decide_closure(
    *,
    policy: dict[str, Any],
    task_id: str,
    allowed_paths: set[str],
    baseline_status: dict[str, str],
    current_status: dict[str, str] | None,
    result: dict[str, Any] | None,
    controller_verification: dict[str, str] | None = None,
    run_id: str | None = None,
    attempt_id: str | None = None,
    prompt_sha256: str | None = None,
    evidence_digest: str | None = None,
    stage2_mode: bool = True,
) -> dict[str, Any]:
    """Decide closure with identity/digest binding.

    When stage2_mode is True (default), acceptance is blocked and only
    inspect/stop transitions are allowed. When False, the legacy behavior
    (acceptance based on verification evidence) is restored.
    """
    run_policy.validate_run_policy(policy)
    reasons: list[str] = []
    unexpected_paths: list[str] = []

    if current_status is None:
        reasons.append("independent Git inspection is missing")
    else:
        unexpected_paths = sorted(set(current_status) - set(baseline_status) - allowed_paths)
        if unexpected_paths:
            reasons.append("unexpected changed paths: " + ", ".join(unexpected_paths))
        lost_dirty_paths = sorted(set(baseline_status) - set(current_status))
        if lost_dirty_paths:
            reasons.append("pre-existing dirty paths disappeared: " + ", ".join(lost_dirty_paths))
        changed_dirty_paths = sorted(
            path
            for path in set(baseline_status) & set(current_status)
            if baseline_status[path] != current_status[path]
        )
        if changed_dirty_paths:
            reasons.append("pre-existing dirty paths changed: " + ", ".join(changed_dirty_paths))

    if result is None:
        reasons.append("structured worker result is missing")
    else:
        if result.get("status") != "complete":
            reasons.append("worker result is not complete")
        if result.get("task_id") != task_id:
            reasons.append("worker result task id does not match")
        required = list(policy["verification"]["targeted_checks"])
        repository_gate = policy["verification"].get("repository_gate")
        if repository_gate:
            required.append(repository_gate)
        if controller_verification is None:
            reasons.append(
                "independent controller verification evidence is missing; "
                "worker-claimed verification alone cannot satisfy the verification gate"
            )
        else:
            for command in required:
                if controller_verification.get(command) == "passed":
                    continue
                if command == repository_gate and policy["verification"].get("authorized_gap"):
                    continue
                reasons.append(f"required verification did not pass: {command}")
        if any(question.get("blocking") for question in result.get("questions", [])):
            reasons.append("worker result contains a blocking question")
        if result.get("risks"):
            reasons.append("worker result contains unresolved risks")

    accepted = not reasons
    if stage2_mode:
        accepted = False
        allowed_transitions = ["resumable", "stopped"]
        allowed_actions = ["inspect", "stop"]
    else:
        # Legacy mode: acceptance based on verification evidence
        allowed_transitions = ["accepted"] if accepted else ["resumable", "stopped"]
        allowed_actions = ["record_acceptance"] if accepted else ["inspect", "resume", "stop"]
        if accepted and policy["commit_policy"]["mode"] == "controller_exact_paths":
            allowed_actions.append("commit_exact_paths")
    # Bind the decision to run/task/attempt identity
    identity_fields = {
        "run_id": run_id,
        "task_id": task_id,
        "attempt_id": attempt_id,
    }
    if prompt_sha256:
        identity_fields["prompt_sha256"] = prompt_sha256
    if evidence_digest:
        identity_fields["evidence_digest"] = evidence_digest
    return {
        "accepted": accepted,
        "reasons": reasons,
        "unexpected_paths": unexpected_paths,
        "observed_paths": sorted(current_status or {}),
        "allowed_transitions": allowed_transitions,
        "allowed_actions": allowed_actions,
        "identity": identity_fields,
    }


def create_attempt(run_dir: Path, record: dict[str, Any]) -> Path:
    execution_contracts.validate_attempt_record(record)
    attempts_dir = run_dir / "attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)
    attempt_number = 1
    while (attempts_dir / f"attempt-{attempt_number:03d}").exists():
        attempt_number += 1
    attempt_dir = attempts_dir / f"attempt-{attempt_number:03d}"
    attempt_dir.mkdir()
    persisted = dict(record)
    prompt = persisted.pop("prompt", "")
    persisted["attempt_number"] = attempt_number
    with (attempt_dir / "record.json").open("x") as stream:
        stream.write(json.dumps(persisted, indent=2, sort_keys=True) + "\n")
    with (attempt_dir / "prompt.txt").open("x") as stream:
        stream.write(prompt)
    return attempt_dir


def _validate_accepted_workspace(run_dir: Path, ledger: dict[str, Any]) -> None:
    closure_ref = ledger["last_closure_path"]
    candidates = []
    for task in ledger["tasks"]:
        if task["state"] != "accepted" or not task["attempt_ids"]:
            continue
        attempt_id = task["attempt_ids"][-1]
        if closure_ref == f"closure/{attempt_id}.json":
            candidates.append((task, attempt_id))
    if len(candidates) != 1:
        raise ValueError("Accepted workspace identity is missing or ambiguous")
    task, attempt_id = candidates[0]
    attempt_path = run_dir / "attempts" / attempt_id / "record.json"
    if not attempt_path.is_file():
        raise ValueError("Accepted attempt record is missing")
    attempt = json.loads(attempt_path.read_text())
    execution_contracts.validate_attempt_record(attempt)
    if attempt["task_id"] != task["id"]:
        raise ValueError("Accepted attempt task identity mismatch")
    if attempt["baseline_ref"] != ledger["selected_task_baseline_ref"]:
        raise ValueError("Accepted attempt baseline reference mismatch")
    if attempt.get("baseline_digest") != ledger["selected_task_baseline_digest"]:
        raise ValueError("Accepted attempt baseline digest mismatch")
    git.validate_accepted_workspace(
        repository=Path(ledger["repository"]).resolve(),
        run_dir=run_dir,
        task_baseline_ref=ledger["selected_task_baseline_ref"],
        task_baseline_digest=ledger["selected_task_baseline_digest"],
        closure_ref=closure_ref,
        allowed_paths=task["allowed_paths"],
        expected_identity={
            "run_id": ledger["run_id"],
            "task_id": task["id"],
            "attempt_id": attempt_id,
            "policy_sha256": ledger["policy_sha256"],
            "manifest_sha256": ledger["manifest_sha256"],
            "prompt_sha256": attempt["prompt_sha256"],
        },
    )


def run_next(run_dir: Path, *, timeout_seconds: float, codex_bin: str) -> dict[str, Any]:
    if timeout_seconds <= 0:
        raise ValueError("timeout must be greater than zero")
    run_dir = run_dir.resolve()
    preliminary_ledger = json.loads((run_dir / "ledger.json").read_text())
    ledger_rules.validate_ledger(preliminary_ledger)
    run_authority.load_flow_authority(run_dir, preliminary_ledger)
    lock = storage.RunCommandLock(run_dir)
    lock.acquire()
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    ledger_rules.validate_ledger(ledger)
    if ledger.get("input_revisions"):
        raise ValueError("Revised inputs require successor actor admission; legacy launch is unavailable")
    policy, manifest, _ = run_authority.load_input_authority(run_dir, ledger)
    run_policy.validate_run_policy(policy)

    # Validate persisted digests
    persisted_policy = json.loads((run_dir / "run-policy.json").read_text())
    if record_serialization.sha256_text(record_serialization.canonical_json(persisted_policy)) != ledger["policy_sha256"]:
        raise ValueError("Persisted policy digest mismatch")
    persisted_manifest = json.loads((run_dir / "task-manifest.json").read_text())
    if record_serialization.sha256_text(record_serialization.canonical_json(persisted_manifest)) != ledger["manifest_sha256"]:
        raise ValueError("Persisted manifest digest mismatch")
    flow, flow_authority, _ = run_authority.load_flow_authority_state(run_dir, ledger)
    if ledger["state"] != "ready":
        raise ValueError(f"Cannot select task from state '{ledger['state']}'")

    cursor_action = None
    if ledger["selected_task_id"] is None:
        task = task_manifest.select_task(ledger, policy)
        selected_cursor = flow_policy.transition_flow_cursor(
            flow,
            {"current_step": None, "correction_cycle": 0},
            "select",
        )
        if selected_cursor["current_step"] != "implement":
            pending = run_authority.update_ledger_locked(
                run_dir,
                {
                    "selected_task_id": task["id"],
                    "current_step": selected_cursor["current_step"],
                },
                expected_revision=ledger["revision"],
                flow=flow,
                cursor_action="select",
            )
            lock.release()
            return {
                "status": "pending",
                "task_id": task["id"],
                "current_step": pending["current_step"],
                "reason": "no MVP adapter owns the current flow step",
            }
        cursor_action = "select"
    else:
        task = next(
            (
                entry for entry in ledger["tasks"]
                if entry["id"] == ledger["selected_task_id"]
            ),
            None,
        )
        if task is None:
            raise ValueError("Selected task is missing from the ledger")
        if ledger["current_step"] != "implement":
            lock.release()
            return {
                "status": "pending",
                "task_id": task["id"],
                "current_step": ledger["current_step"],
                "reason": "no MVP adapter owns the current flow step",
            }

    # Compare current Git state with the applicable controller-owned evidence.
    repo = Path(ledger["repository"]).resolve()
    initial_baseline = json.loads(
        (run_dir / "baselines" / ledger["initial_baseline_path"]).read_text()
    )
    if any(task["state"] == "accepted" for task in ledger["tasks"]):
        _validate_accepted_workspace(run_dir, ledger)
    else:
        current_head = git.capture_head(repo)
        if current_head != initial_baseline["head_oid"]:
            raise ValueError(
                f"HEAD has changed since initialization: {current_head} != {initial_baseline['head_oid']}"
            )
        current_status = git.capture_git_status(repo)
        initial_status = initial_baseline["status"]
        if current_status != initial_status:
            changed = sorted(set(current_status) ^ set(initial_status))
            raise ValueError(
                f"Repository state has changed since initialization. "
                f"Changed paths: {', '.join(changed)}"
            )

    # Validate initial-baseline digest before proceeding
    persisted_baseline_path = run_dir / "baselines" / ledger["initial_baseline_path"]
    persisted_baseline_content = persisted_baseline_path.read_text()
    computed_baseline_digest = record_serialization.sha256_text(record_serialization.canonical_json(json.loads(persisted_baseline_content)))
    if computed_baseline_digest != ledger["initial_baseline_digest"]:
        raise ValueError(
            f"Initial baseline digest mismatch: persisted={computed_baseline_digest}, "
            f"expected={ledger['initial_baseline_digest']}"
        )

    # Preflight the exact Codex start command shape before any durable mutation.
    worker_script = Path(__file__).parents[1] / "scripts" / "codex_worker.py"
    worker.preflight_codex(
        codex_bin,
        repo,
        sandbox=policy["permissions"]["sandbox"],
    )

    # Capture task baseline
    attempt_number = 1
    attempts_dir = run_dir / "attempts"
    while (attempts_dir / f"attempt-{attempt_number:03d}").exists():
        attempt_number += 1
    task_baseline_ref = f"task-{attempt_number:03d}.json"
    task_baseline_data = git.capture_task_baseline(repo)
    task_baseline_digest = record_serialization.sha256_text(record_serialization.canonical_json(task_baseline_data))
    storage.atomic_write_json(run_dir / "baselines" / task_baseline_ref, task_baseline_data)

    # Use the approved snapshot, never reload mutable task documents.
    inputs = run_authority.load_frozen_inputs(run_dir, ledger)
    prompt = render_worker_prompt(
        task_id=task["id"],
        brief_path=task["brief_path"],
        task_instructions=f"Implement task {task['id']}: {task['title']}.\n"
                         f"Allowed paths: {task['allowed_paths']}\n"
                         f"Required checks: {task['required_checks']}\n"
                         f"Dependencies satisfied: {task['dependencies']}\n\n"
                         "Use the frozen authority below; source paths are provenance only.\n"
                         f"Frozen brief:\n{inputs['documents']['brief']['content']}\n"
                         f"Frozen verification:\n{inputs['documents']['verification']['content']}",
        policy=policy,
    )

    # Allocate attempt
    attempt_record = execution_contracts.build_attempt_record(
        task_id=task["id"],
        brief_path=task["brief_path"],
        prompt=prompt,
        policy=policy,
        flow=flow,
        flow_revision=flow_authority["flow_revision"],
        flow_sha256=flow_authority["flow_sha256"],
        baseline_ref=task_baseline_ref,
    )
    expected_attempt_dir = run_dir / "attempts" / f"attempt-{attempt_number:03d}"
    adapter_invocation = [
        sys.executable, str(worker_script), "start",
        "--run-dir", str(expected_attempt_dir),
        "--cwd", str(repo),
        "--prompt-file", str(expected_attempt_dir / "prompt.txt"),
        "--codex-bin", codex_bin,
        "--timeout-seconds", str(timeout_seconds),
        "--sandbox", policy["permissions"]["sandbox"],
        "--model", attempt_record["model"],
        "--effort", attempt_record["effort"],
    ]
    attempt_record.update({
        "adapter_invocation": adapter_invocation,
        "codex_bin": codex_bin,
        "timeout_seconds": timeout_seconds,
        "effective_permission_envelope": policy["permissions"],
        "baseline_digest": task_baseline_digest,
    })
    attempt_dir = create_attempt(run_dir, attempt_record)
    attempt_id = attempt_dir.name
    if attempt_dir != expected_attempt_dir:
        raise ValueError("Attempt allocation changed during the owned mutation phase")

    running_tasks = [dict(entry) for entry in ledger["tasks"]]
    selected_task = next(entry for entry in running_tasks if entry["id"] == task["id"])
    selected_task["state"] = "running"
    selected_task["attempt_ids"] = [*selected_task["attempt_ids"], attempt_id]
    ledger = run_authority.update_ledger_locked(run_dir, {
        "state": "running",
        "selected_task_id": task["id"],
        "current_step": "implement",
        "active_attempt_id": attempt_id,
        "selected_task_baseline_ref": task_baseline_ref,
        "selected_task_baseline_digest": task_baseline_digest,
        "tasks": running_tasks,
    }, expected_revision=ledger["revision"], flow=flow, cursor_action=cursor_action)
    running_revision = ledger["revision"]
    lock.release()

    def stop_active_attempt(reason: str) -> dict[str, Any]:
        stopped_tasks = [dict(entry) for entry in ledger["tasks"]]
        next(entry for entry in stopped_tasks if entry["id"] == task["id"])["state"] = "stopped"
        run_authority.update_ledger_locked(run_dir, {
            "state": "stopped",
            "selected_task_id": None,
            "active_attempt_id": None,
            "current_step": None,
            "correction_cycle": 0,
            "tasks": stopped_tasks,
        }, expected_revision=ledger["revision"], cursor_action="task_boundary")
        lock.release()
        return {"status": "stopped", "reason": reason}

    # Launch through worker adapter
    result = subprocess.run(
        adapter_invocation,
        text=True,
        capture_output=True,
    )

    lock.acquire()
    current_ledger = json.loads(ledger_path.read_text())
    if (
        current_ledger["revision"] != running_revision
        or current_ledger["state"] != "running"
        or current_ledger["selected_task_id"] != task["id"]
        or current_ledger["active_attempt_id"] != attempt_id
    ):
        lock.release()
        raise ValueError("Run state changed while the worker was active; refusing stale reconciliation")
    ledger = current_ledger

    if result.returncode != 0:
        return stop_active_attempt(f"Worker error: {result.stderr}")

    # Parse the adapter's terminal output and durable state.
    try:
        output = json.loads(result.stdout)
        state_path = Path(output["state_path"]).resolve()
        expected_state_path = (attempt_dir / "state.json").resolve()
        if state_path != expected_state_path or not state_path.is_file():
            raise ValueError("adapter state path is missing or outside the active attempt")
        adapter_state = json.loads(state_path.read_text())
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        return stop_active_attempt(f"Invalid adapter terminal output: {error}")

    terminal_statuses = {"awaiting_inspection", "resumable", "stopped"}
    if (
        adapter_state.get("status") not in terminal_statuses
        or output.get("status") != adapter_state.get("status")
        or adapter_state.get("process_pid") is not None
        or not isinstance(adapter_state.get("exit_code"), int)
        or not isinstance(adapter_state.get("ended_at"), str)
        or adapter_state.get("prompt_sha256") != attempt_record["prompt_sha256"]
    ):
        return stop_active_attempt("Invalid or non-terminal adapter state")

    # Collect closure evidence
    task_baseline = json.loads(
        (run_dir / "baselines" / task_baseline_ref).read_text()
    )
    if record_serialization.sha256_text(record_serialization.canonical_json(task_baseline)) != task_baseline_digest:
        return stop_active_attempt("Selected task baseline digest mismatch")

    # Read result if it exists
    result_path = Path(output.get("result_path", "")).resolve()
    expected_result_path = (attempt_dir / "turn-001.result.json").resolve()
    recorded_result_path = Path(adapter_state.get("result_path", "")).resolve()
    terminal_record_path = expected_result_path.with_suffix(".state.json")
    if (
        result_path != expected_result_path
        or recorded_result_path != expected_result_path
        or not result_path.is_file()
        or not terminal_record_path.is_file()
    ):
        return stop_active_attempt("Adapter result is missing or outside the active attempt")
    try:
        worker_result = json.loads(result_path.read_text())
        terminal_record = json.loads(terminal_record_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return stop_active_attempt(f"Adapter result is invalid: {error}")
    validated_outcome = worker.result_status(result_path)
    if (
        terminal_record != adapter_state
        or validated_outcome is None
        or validated_outcome != adapter_state.get("attempt_outcome")
    ):
        return stop_active_attempt("Adapter result and terminal state do not match")

    adapter_state_digest = record_serialization.sha256_text(record_serialization.canonical_json(adapter_state))
    git_evidence = git.capture_closure_evidence(
        repository=repo,
        run_dir=run_dir,
        attempt_id=attempt_id,
        task_baseline=task_baseline,
        task_baseline_digest=task_baseline_digest,
        allowed_paths=task["allowed_paths"],
        policy_sha256=ledger["policy_sha256"],
        manifest_sha256=ledger["manifest_sha256"],
        prompt_sha256=attempt_record["prompt_sha256"],
        adapter_state_digest=adapter_state_digest,
    )
    (run_dir / "verification").mkdir(exist_ok=True)
    (run_dir / "decisions").mkdir(exist_ok=True)
    current_status = git_evidence["current_status"]
    closure_git_fields = git_evidence["closure_fields"]
    mechanical_violations = []
    if git_evidence["head_changed"]:
        mechanical_violations.append("worker changed HEAD despite commit prohibition")
    if git_evidence["index_changed"]:
        mechanical_violations.append("worker changed the Git index")
    closure_git_fields["controller_observations"][
        "mechanical_violations"
    ] = mechanical_violations
    evidence_digest = closure_git_fields["evidence_digest"]

    # Build the complete closure packet
    closure_packet = {
        "run_id": policy["run_id"],
        "task_id": task["id"],
        "attempt_id": attempt_id,
        "policy_sha256": ledger["policy_sha256"],
        "manifest_sha256": ledger["manifest_sha256"],
        "baseline_sha256": task_baseline_digest,
        "prompt_sha256": attempt_record.get("prompt_sha256"),
        "attempt_record_sha256": run_records.sha256_bytes(
            (attempt_dir / "record.json").read_bytes()
        ),
        **closure_git_fields,
        "worker_claims": {
            "status": worker_result.get("status") if worker_result else None,
            "result_path": output.get("result_path"),
            "terminal_state": adapter_state.get("status"),
            "attempt_outcome": adapter_state.get("attempt_outcome"),
            "exit_code": adapter_state.get("exit_code"),
            "thread_id": adapter_state.get("thread_id"),
            "state_path": str(state_path),
            "effective_command": adapter_state.get("effective_command"),
            "result_sha256": run_records.sha256_bytes(result_path.read_bytes()),
            "result": worker_result,
        },
        "controller_verification": "not_collected",
    }

    # Decide before publication so the complete packet is written atomically once.
    closure = decide_closure(
        policy=policy,
        task_id=task["id"],
        allowed_paths=set(task["allowed_paths"]),
        baseline_status=task_baseline["status"],
        current_status=current_status,
        result=worker_result,
        controller_verification=None,  # Stage 2: not_collected
        run_id=policy["run_id"],
        attempt_id=attempt_id,
        prompt_sha256=attempt_record.get("prompt_sha256"),
        evidence_digest=evidence_digest,
    )
    if mechanical_violations:
        closure["accepted"] = False
        closure["reasons"].extend(mechanical_violations)

    closure_packet.update(closure)
    closure_json_path = run_dir / "closure" / f"{attempt_id}.json"
    storage.atomic_write_json(closure_json_path, closure_packet)
    closure_sha256 = run_records.sha256_bytes(closure_json_path.read_bytes())

    awaiting_tasks = [dict(entry) for entry in ledger["tasks"]]
    next(entry for entry in awaiting_tasks if entry["id"] == task["id"])["state"] = "awaiting_inspection"
    run_authority.update_ledger_locked(run_dir, {
        "state": "awaiting_inspection",
        "selected_task_id": task["id"],
        "active_attempt_id": None,
        "last_closure_path": str(closure_json_path.relative_to(run_dir)),
        "last_closure_sha256": closure_sha256,
        "tasks": awaiting_tasks,
    }, expected_revision=ledger["revision"])
    lock.release()

    return {
        "status": "awaiting_inspection",
        "task_id": task["id"],
        "closure_path": str(closure_json_path),
    }

