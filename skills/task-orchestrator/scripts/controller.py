#!/usr/bin/env python3
"""Small Stage 1 policy, prompt, attempt, and closure primitives."""

from __future__ import annotations

import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

# Import atomic_write_json from the worker adapter for ledger persistence
_worker_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_worker",
    Path(__file__).parents[1] / "scripts" / "codex_worker.py",
)
_worker_module = importlib.util.module_from_spec(_worker_spec)
assert _worker_spec.loader is not None
_worker_spec.loader.exec_module(_worker_module)
atomic_write_json = _worker_module.atomic_write_json

_state_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_controller_state",
    Path(__file__).with_name("controller_state.py"),
)
_state_module = importlib.util.module_from_spec(_state_spec)
assert _state_spec.loader is not None
_state_spec.loader.exec_module(_state_module)

_git_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_controller_git",
    Path(__file__).with_name("controller_git.py"),
)
_git_module = importlib.util.module_from_spec(_git_spec)
assert _git_spec.loader is not None
_git_spec.loader.exec_module(_git_module)

# Compatibility imports: pure state rules live in controller_state.py.
ATTEMPT_REQUIRED_FIELDS = _state_module.ATTEMPT_REQUIRED_FIELDS
ALLOWED_TASK_TRANSITIONS = _state_module.ALLOWED_TASK_TRANSITIONS
ALLOWED_RUN_TRANSITIONS = _state_module.ALLOWED_RUN_TRANSITIONS
canonical_json = _state_module.canonical_json
sha256_text = _state_module.sha256_text
validate_run_policy = _state_module.validate_run_policy
transition_task = _state_module.transition_task
transition_run = _state_module.transition_run
validate_attempt_record = _state_module.validate_attempt_record
build_attempt_record = _state_module.build_attempt_record
_validate_task_manifest_schema = _state_module._validate_task_manifest_schema
_detect_dependency_cycles = _state_module._detect_dependency_cycles
_is_valid_repo_relative_path = _state_module._is_valid_repo_relative_path
validate_task_manifest = _state_module.validate_task_manifest
select_task = _state_module.select_task
_validate_ledger = _state_module.validate_ledger

# Compatibility imports: Git observations live in controller_git.py.
capture_git_status = _git_module.capture_git_status
capture_initial_baseline = _git_module.capture_initial_baseline


def persist_run_policy(path: Path, policy: dict[str, Any]) -> str:
    validate_run_policy(policy)
    serialized = json.dumps(policy, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        stream.write(serialized)
    return sha256_text(canonical_json(policy))


def render_worker_prompt(
    *,
    task_id: str,
    brief_path: str,
    task_instructions: str,
    policy: dict[str, Any],
) -> str:
    validate_run_policy(policy)
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
    validate_run_policy(policy)
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
    validate_attempt_record(record)
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


# ── Manifest validation ──────────────────────────────────────────────


# ── Run initialization ────────────────────────────────────────────────


def init_run(
    run_dir: Path,
    policy_path: Path,
    manifest_path: Path,
    repository: Path,
) -> dict[str, Any]:
    """Initialize an immutable run from validated policy and manifest."""
    policy = json.loads(policy_path.read_text())
    validate_run_policy(policy)
    manifest = json.loads(manifest_path.read_text())

    # Resolve and verify repository is Git top-level
    resolved_repo = repository.resolve()
    try:
        actual_top = _git_module.repository_top_level(resolved_repo)
        if actual_top != resolved_repo:
            raise ValueError(
                f"Provided repository {resolved_repo} is not the Git top-level "
                f"(actual: {actual_top})"
            )
    except subprocess.CalledProcessError:
        raise ValueError(
            f"{resolved_repo} is not a Git repository or has no HEAD"
        )

    policy_repo = Path(policy["repository"])
    if resolved_repo != policy_repo.resolve():
        raise ValueError(
            f"Policy repository {policy['repository']} does not match "
            f"provided repository {repository}"
        )

    # Validate manifest cross-policy
    validated = validate_task_manifest(policy, manifest, resolved_repo)

    # Enforce run directory is outside the repository
    if run_dir.resolve().is_relative_to(resolved_repo):
        raise ValueError(
            f"Run directory {run_dir} must be outside the repository {resolved_repo}"
        )

    # Capture baseline
    baseline = capture_initial_baseline(resolved_repo)
    baseline_ref = f"run-initial.json"
    baseline_path = run_dir / "baselines" / baseline_ref

    # Build temporary directory and atomically publish
    temp_dir = run_dir.parent / f".tmp-run-{run_dir.name}-{hashlib.sha256(str(run_dir.name).encode()).hexdigest()[:8]}"
    try:
        # Copy canonical policy and manifest
        policy_digest = persist_run_policy(temp_dir / "run-policy.json", policy)
        manifest_content = manifest_path.read_text()
        manifest_digest = sha256_text(canonical_json(json.loads(manifest_content)))
        (temp_dir / "task-manifest.json").write_text(manifest_content)
        manifest_digest = sha256_text(canonical_json(manifest))

        # Create baselines directory
        (temp_dir / "baselines").mkdir()
        baseline_data = {
            "head_oid": baseline["head_oid"],
            "status": baseline["status"],
        }
        baseline_path = temp_dir / "baselines" / baseline_ref
        baseline_path.write_text(json.dumps(baseline_data, indent=2, sort_keys=True) + "\n")

        # Build ledger
        completed = set(validated["completed_task_ids"])
        for task in validated["task_entries"]:
            if all(dependency in completed for dependency in task["dependencies"]):
                task["state"] = "ready"
        ledger = {
            "version": 1,
            "run_id": policy["run_id"],
            "repository": str(resolved_repo),
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "revision": 1,
            "policy_path": "run-policy.json",
            "policy_sha256": policy_digest,
            "manifest_path": "task-manifest.json",
            "manifest_sha256": manifest_digest,
            "initial_baseline_path": str(baseline_ref),
            "initial_baseline_digest": sha256_text(
                canonical_json(baseline_data)
            ),
            "completed_task_ids": validated["completed_task_ids"],
            "state": "ready",
            "selected_task_id": None,
            "active_attempt_id": None,
            "last_closure_path": None,
            "last_verification_path": None,
            "last_decision_path": None,
            "active_operation_path": None,
            "tasks": validated["task_entries"],
        }
        _validate_ledger(ledger)
        (temp_dir / "ledger.json").write_text(
            json.dumps(ledger, indent=2, sort_keys=True) + "\n"
        )

        # Atomic rename
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        if run_dir.exists():
            raise FileExistsError(f"Run directory already exists: {run_dir}")
        temp_dir.rename(run_dir)

    except BaseException:
        # Clean up temp directory on failure
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    return {
        "run_id": policy["run_id"],
        "state": "ready",
        "ledger_path": str(run_dir / "ledger.json"),
        "baseline_path": str(run_dir / "baselines" / baseline_ref),
    }


# ── Deterministic task selection ──────────────────────────────────────


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


# ── Ledger update helpers ─────────────────────────────────────────────


def update_ledger(
    run_dir: Path, updater: dict[str, Any], *, expected_revision: int,
    closure_decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Read, update, validate, and atomically write the ledger."""
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    ledger = _state_module.apply_ledger_update(
        ledger, updater, _now_iso(), expected_revision=expected_revision,
        closure_decision=closure_decision,
    )
    atomic_write_json(ledger_path, ledger)
    return ledger


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
    validate_attempt_record(attempt)
    if attempt["task_id"] != task["id"]:
        raise ValueError("Accepted attempt task identity mismatch")
    if attempt["baseline_ref"] != ledger["selected_task_baseline_ref"]:
        raise ValueError("Accepted attempt baseline reference mismatch")
    if attempt.get("baseline_digest") != ledger["selected_task_baseline_digest"]:
        raise ValueError("Accepted attempt baseline digest mismatch")
    _git_module.validate_accepted_workspace(
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


# ── CLI entry points ─────────────────────────────────────────────────


def build_parser() -> "argparse.ArgumentParser":  # type: ignore[name-defined]
    import argparse
    parser = argparse.ArgumentParser(
        description="Task orchestrator controller."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize an immutable run")
    init_parser.add_argument("--run-dir", required=True, help="Run directory (outside repo)")
    init_parser.add_argument("--policy", required=True, help="Run policy JSON path")
    init_parser.add_argument("--manifest", required=True, help="Task manifest JSON path")
    init_parser.add_argument("--repository", required=True, help="Repository root")
    init_parser.set_defaults(handler=_cli_init)

    runnext_parser = subparsers.add_parser("run-next", help="Select and launch one task")
    runnext_parser.add_argument("--run-dir", required=True)
    runnext_parser.add_argument("--timeout-seconds", type=float, required=True)
    runnext_parser.add_argument("--codex-bin", default="codex", help=argparse.SUPPRESS)
    runnext_parser.set_defaults(handler=_cli_run_next)

    return parser


def _cli_init(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    import argparse
    result = init_run(
        run_dir=Path(args.run_dir).resolve(),
        policy_path=Path(args.policy).resolve(),
        manifest_path=Path(args.manifest).resolve(),
        repository=Path(args.repository).resolve(),
    )
    print(json.dumps(result, sort_keys=True))
    return 0


def _cli_run_next(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    import argparse
    import codex_worker
    if args.timeout_seconds <= 0:
        raise ValueError("timeout must be greater than zero")
    run_dir = Path(args.run_dir).resolve()
    lock_path = run_dir / "controller.lock"
    lock_stream = lock_path.open("a+")
    try:
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_stream.close()
        raise ValueError("Another controller owns this run's mutation phase")
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    _validate_ledger(ledger)
    policy = json.loads((run_dir / "run-policy.json").read_text())
    manifest = json.loads((run_dir / "task-manifest.json").read_text())

    # Validate persisted digests
    persisted_policy = json.loads((run_dir / "run-policy.json").read_text())
    if sha256_text(canonical_json(persisted_policy)) != ledger["policy_sha256"]:
        raise ValueError("Persisted policy digest mismatch")
    persisted_manifest = json.loads((run_dir / "task-manifest.json").read_text())
    if sha256_text(canonical_json(persisted_manifest)) != ledger["manifest_sha256"]:
        raise ValueError("Persisted manifest digest mismatch")

    # Compare current Git state with the applicable controller-owned evidence.
    repo = Path(ledger["repository"]).resolve()
    initial_baseline = json.loads(
        (run_dir / "baselines" / ledger["initial_baseline_path"]).read_text()
    )
    if any(task["state"] == "accepted" for task in ledger["tasks"]):
        _validate_accepted_workspace(run_dir, ledger)
    else:
        current_head = _git_module.capture_head(repo)
        if current_head != initial_baseline["head_oid"]:
            raise ValueError(
                f"HEAD has changed since initialization: {current_head} != {initial_baseline['head_oid']}"
            )
        current_status = capture_git_status(repo)
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
    computed_baseline_digest = sha256_text(canonical_json(json.loads(persisted_baseline_content)))
    if computed_baseline_digest != ledger["initial_baseline_digest"]:
        raise ValueError(
            f"Initial baseline digest mismatch: persisted={computed_baseline_digest}, "
            f"expected={ledger['initial_baseline_digest']}"
        )

    # Preflight the exact Codex start command shape before any durable mutation.
    worker_script = Path(__file__).parents[1] / "scripts" / "codex_worker.py"
    _worker_module.preflight_codex(
        args.codex_bin,
        repo,
        sandbox=policy["permissions"]["sandbox"],
    )

    # Selection is pure. Durable mutation begins only after exact preflight.
    task = select_task(ledger, policy)

    # Capture task baseline
    attempt_number = 1
    attempts_dir = run_dir / "attempts"
    while (attempts_dir / f"attempt-{attempt_number:03d}").exists():
        attempt_number += 1
    task_baseline_ref = f"task-{attempt_number:03d}.json"
    task_baseline_data = _git_module.capture_task_baseline(repo)
    task_baseline_digest = sha256_text(canonical_json(task_baseline_data))
    atomic_write_json(run_dir / "baselines" / task_baseline_ref, task_baseline_data)

    # Build prompt
    prompt = render_worker_prompt(
        task_id=task["id"],
        brief_path=task["brief_path"],
        task_instructions=f"Implement task {task['id']}: {task['title']}.\n"
                         f"Allowed paths: {task['allowed_paths']}\n"
                         f"Required checks: {task['required_checks']}\n"
                         f"Dependencies satisfied: {task['dependencies']}",
        policy=policy,
    )

    # Allocate attempt
    attempt_record = build_attempt_record(
        task_id=task["id"],
        brief_path=task["brief_path"],
        prompt=prompt,
        policy=policy,
        baseline_ref=task_baseline_ref,
    )
    expected_attempt_dir = run_dir / "attempts" / f"attempt-{attempt_number:03d}"
    adapter_invocation = [
        sys.executable, str(worker_script), "start",
        "--run-dir", str(expected_attempt_dir),
        "--cwd", str(repo),
        "--prompt-file", str(expected_attempt_dir / "prompt.txt"),
        "--codex-bin", args.codex_bin,
        "--timeout-seconds", str(args.timeout_seconds),
        "--sandbox", policy["permissions"]["sandbox"],
    ]
    attempt_record.update({
        "adapter_invocation": adapter_invocation,
        "codex_bin": args.codex_bin,
        "timeout_seconds": args.timeout_seconds,
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
    ledger = update_ledger(run_dir, {
        "state": "running",
        "selected_task_id": task["id"],
        "active_attempt_id": attempt_id,
        "selected_task_baseline_ref": task_baseline_ref,
        "selected_task_baseline_digest": task_baseline_digest,
        "tasks": running_tasks,
    }, expected_revision=ledger["revision"])
    running_revision = ledger["revision"]
    fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)
    lock_stream.close()

    def stop_active_attempt(reason: str) -> int:
        print(reason, file=sys.stderr)
        stopped_tasks = [dict(entry) for entry in ledger["tasks"]]
        next(entry for entry in stopped_tasks if entry["id"] == task["id"])["state"] = "stopped"
        update_ledger(run_dir, {
            "state": "stopped",
            "selected_task_id": None,
            "active_attempt_id": None,
            "tasks": stopped_tasks,
        }, expected_revision=ledger["revision"])
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)
        lock_stream.close()
        return 1

    # Launch through worker adapter
    result = subprocess.run(
        adapter_invocation,
        text=True,
        capture_output=True,
    )

    lock_stream = lock_path.open("a+")
    try:
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_stream.close()
        raise ValueError("Another controller owns this run's mutation phase")
    current_ledger = json.loads(ledger_path.read_text())
    if (
        current_ledger["revision"] != running_revision
        or current_ledger["state"] != "running"
        or current_ledger["selected_task_id"] != task["id"]
        or current_ledger["active_attempt_id"] != attempt_id
    ):
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)
        lock_stream.close()
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
    if sha256_text(canonical_json(task_baseline)) != task_baseline_digest:
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
    validated_outcome = _worker_module.result_status(result_path)
    if (
        terminal_record != adapter_state
        or validated_outcome is None
        or validated_outcome != adapter_state.get("attempt_outcome")
    ):
        return stop_active_attempt("Adapter result and terminal state do not match")

    adapter_state_digest = sha256_text(canonical_json(adapter_state))
    git_evidence = _git_module.capture_closure_evidence(
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
    atomic_write_json(closure_json_path, closure_packet)

    awaiting_tasks = [dict(entry) for entry in ledger["tasks"]]
    next(entry for entry in awaiting_tasks if entry["id"] == task["id"])["state"] = "awaiting_inspection"
    update_ledger(run_dir, {
        "state": "awaiting_inspection",
        "selected_task_id": task["id"],
        "active_attempt_id": None,
        "last_closure_path": str(closure_json_path.relative_to(run_dir)),
        "tasks": awaiting_tasks,
    }, expected_revision=ledger["revision"])
    fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)
    lock_stream.close()

    print(json.dumps({
        "status": "awaiting_inspection",
        "task_id": task["id"],
        "closure_path": str(closure_json_path),
    }, sort_keys=True))
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    sys.exit(main())
