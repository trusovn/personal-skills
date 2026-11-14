"""Inspect retained legacy attempt and closure evidence.

inspect_run owns the lock, independent verification, immutable replay and ledger
references for public inspect. Helpers validate the distinct legacy envelopes.
Candidate checks and actor review admission are separate application workflows.
Dependencies: authority, records, execution contracts, flow policy, manifest and
ledger rules, serialization, Git, storage, verification and transport.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from . import run_records
from . import run_authority
from . import execution_contracts
from . import flow_policy
from . import ledger as ledger_rules
from . import record_serialization
from . import task_manifest
from . import controller_git as git
from . import codex_worker as worker
from . import verification_runner
from . import run_storage as storage


def _validate_execution_artifacts(
    *,
    run_dir: Path,
    record_path: Path,
    closure_identity: dict[str, Any],
    plan: dict[str, Any],
    permissions: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    raw = record_path.read_bytes()
    try:
        record = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("Existing command-execution record is invalid") from error
    if raw != storage.canonical_record_bytes(record):
        raise ValueError("Existing command-execution record is not canonical")
    execution_contracts.validate_command_execution_record(
        record, expected_closure_identity=closure_identity
    )
    expected_plan = [{
        "id": command["id"],
        "argv": command["argv"],
        "sources": [source["source"] for source in command["provenance"]],
        "role": (
            "repository_gate"
            if command["roles"] == ["repository_gate"] else "targeted"
        ),
    } for command in plan["commands"]]
    if record["plan"] != expected_plan:
        raise ValueError("Existing command-execution plan does not match persisted authority")
    expected_permissions = dict(permissions)
    expected_permissions["writable_roots"] = [
        str(Path(path).resolve()) for path in expected_permissions["writable_roots"]
    ]
    if record["effective_envelope"] != expected_permissions:
        raise ValueError("Existing command-execution permission envelope mismatch")
    for outcome in record["outcomes"]:
        for stream_name in ("stdout", "stderr"):
            relative = outcome[f"{stream_name}_path"]
            artifact = run_dir / relative
            if not artifact.is_file() or run_records.sha256_bytes(artifact.read_bytes()) != outcome[
                f"{stream_name}_sha256"
            ]:
                raise ValueError(f"Existing command-execution {stream_name} artifact mismatch")
    return record, run_records.sha256_bytes(raw)


def _load_inspection_authority(
    run_dir: Path,
) -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any],
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any],
]:
    ledger = json.loads((run_dir / "ledger.json").read_text())
    ledger_rules.validate_ledger(ledger)
    if ledger["state"] != "awaiting_inspection":
        raise ValueError("inspect requires run state 'awaiting_inspection'")
    flow, flow_authority, _ = run_authority.load_flow_authority_state(run_dir, ledger)

    policy, manifest, _ = run_authority.load_input_authority(run_dir, ledger)
    repo = Path(ledger["repository"]).resolve()
    if repo != Path(policy["repository"]).resolve() or git.repository_top_level(repo) != repo:
        raise ValueError("Persisted repository identity mismatch")
    validated_manifest = task_manifest.validate_task_manifest(policy, manifest, repo)
    immutable_task_fields = (
        "id", "title", "brief_path", "dependencies", "allowed_paths", "required_checks",
    )
    for persisted, expected in zip(ledger["tasks"], validated_manifest["task_entries"]):
        if any(persisted[field] != expected[field] for field in immutable_task_fields):
            raise ValueError("Persisted selected-task authority mismatch")

    selected = next(
        (task for task in ledger["tasks"] if task["id"] == ledger["selected_task_id"]),
        None,
    )
    if selected is None or selected["state"] != "awaiting_inspection":
        raise ValueError("Selected task is missing or not awaiting inspection")
    attempt_id = selected["attempt_ids"][-1]
    if ledger["last_closure_path"] != f"closure/{attempt_id}.json":
        raise ValueError("Closure reference does not match the selected attempt")
    attempt_number = attempt_id.removeprefix("attempt-")
    if attempt_id != f"attempt-{attempt_number}" or not attempt_number.isdigit():
        raise ValueError("Selected attempt identity is invalid")
    expected_baseline_ref = f"task-{attempt_number}.json"
    if ledger.get("selected_task_baseline_ref") != expected_baseline_ref:
        raise ValueError("Selected task baseline reference mismatch")
    baseline_path = run_dir / "baselines" / expected_baseline_ref
    baseline = json.loads(baseline_path.read_text())
    if set(baseline) not in ({"head_oid", "index_tree", "status"},
                             {"head_oid", "index_tree", "status", "dirty_files"}):
        raise ValueError("Selected task baseline has an invalid shape")
    baseline_digest = record_serialization.sha256_text(record_serialization.canonical_json(baseline))
    if baseline_digest != ledger.get("selected_task_baseline_digest"):
        raise ValueError("Selected task baseline digest mismatch")

    attempt_dir = run_dir / "attempts" / attempt_id
    attempt_record_bytes = (attempt_dir / "record.json").read_bytes()
    attempt = json.loads(attempt_record_bytes)
    execution_contracts.validate_attempt_record(attempt)
    implement = flow_policy.flow_step(flow, "implement")
    assert implement is not None
    actor = flow_policy.ACTOR_LEVELS[implement["mode"]]
    prompt = (attempt_dir / "prompt.txt").read_text()
    durable_prompt = attempt_dir / "turn-001.prompt.txt"
    if not durable_prompt.is_file() or durable_prompt.read_text() != prompt:
        raise ValueError("Durable turn prompt mismatch")
    if "prompt" in attempt and attempt["prompt"] != prompt:
        raise ValueError("Attempt record prompt mismatch")
    if (
        attempt.get("attempt_number") != int(attempt_number)
        or attempt["task_id"] != selected["id"]
        or attempt["brief_path"] != selected["brief_path"]
        or attempt["baseline_ref"] != expected_baseline_ref
        or attempt.get("baseline_digest") != baseline_digest
        or attempt["policy_sha256"] != ledger["policy_sha256"]
        or attempt["flow_revision"] != flow_authority["flow_revision"]
        or attempt["flow_sha256"] != flow_authority["flow_sha256"]
        or attempt["model"] != actor["model"]
        or attempt["effort"] != actor["reasoning"]
        or attempt["prompt_sha256"] != record_serialization.sha256_text(prompt)
        or attempt.get("effective_permission_envelope") != policy["permissions"]
    ):
        raise ValueError("Attempt record identity mismatch")

    state_path = attempt_dir / "state.json"
    result_path = attempt_dir / "turn-001.result.json"
    terminal_path = result_path.with_suffix(".state.json")
    adapter_state = json.loads(state_path.read_text())
    if json.loads(terminal_path.read_text()) != adapter_state:
        raise ValueError("Adapter terminal state mismatch")
    result_bytes = result_path.read_bytes()
    worker_result = json.loads(result_bytes)
    if worker_result.get("task_id") != selected["id"]:
        raise ValueError("worker result task id does not match the selected task")
    if (
        adapter_state.get("version") != 1
        or adapter_state.get("turn") != 1
        or adapter_state.get("status") != "awaiting_inspection"
        or adapter_state.get("attempt_outcome") != worker.result_status(result_path)
        or adapter_state.get("process_pid") is not None
        or adapter_state.get("cwd") != str(repo)
        or adapter_state.get("prompt_sha256") != attempt["prompt_sha256"]
        or Path(adapter_state.get("result_path", "")).resolve() != result_path.resolve()
    ):
        raise ValueError("Adapter state or structured result identity mismatch")
    effective_command = adapter_state.get("effective_command")
    if not isinstance(effective_command, list) or not all(
        isinstance(item, str) for item in effective_command
    ):
        raise ValueError("Adapter effective command is invalid")
    model_values = [
        effective_command[index + 1]
        for index, item in enumerate(effective_command[:-1])
        if item == "--model"
    ]
    effort_values = [
        effective_command[index + 1]
        for index, item in enumerate(effective_command[:-1])
        if item == "--config"
        and effective_command[index + 1].startswith("model_reasoning_effort=")
    ]
    if (
        adapter_state.get("model") != attempt["model"]
        or adapter_state.get("effort") != attempt["effort"]
        or model_values != [attempt["model"]]
        or effort_values != [f'model_reasoning_effort="{attempt["effort"]}"']
    ):
        raise ValueError("Durable adapter command actor mismatch")

    closure_path = run_dir / ledger["last_closure_path"]
    closure_bytes = closure_path.read_bytes()
    if run_records.sha256_bytes(closure_bytes) != ledger.get("last_closure_sha256"):
        raise ValueError("Closure bytes do not match the ledger digest")
    closure = json.loads(closure_bytes)
    expected_top = {
        "run_id": ledger["run_id"],
        "task_id": selected["id"],
        "attempt_id": attempt_id,
        "policy_sha256": ledger["policy_sha256"],
        "manifest_sha256": ledger["manifest_sha256"],
        "baseline_sha256": baseline_digest,
        "prompt_sha256": attempt["prompt_sha256"],
        "attempt_record_sha256": run_records.sha256_bytes(attempt_record_bytes),
    }
    if any(closure.get(field) != value for field, value in expected_top.items()):
        raise ValueError("Closure identity field mismatch")
    claims = closure.get("worker_claims")
    if not isinstance(claims, dict):
        raise ValueError("Closure worker claims are invalid")
    if claims.get("result_sha256") != run_records.sha256_bytes(result_bytes):
        raise ValueError("Worker result bytes do not match the closure digest")
    if (
        claims.get("result") != worker_result
        or Path(claims.get("result_path", "")).resolve() != result_path.resolve()
        or Path(claims.get("state_path", "")).resolve() != state_path.resolve()
        or claims.get("terminal_state") != adapter_state["status"]
        or claims.get("attempt_outcome") != adapter_state["attempt_outcome"]
        or claims.get("thread_id") != adapter_state.get("thread_id")
        or claims.get("exit_code") != adapter_state.get("exit_code")
        or claims.get("effective_command") != adapter_state.get("effective_command")
    ):
        raise ValueError("Closure worker claims mismatch durable adapter evidence")
    adapter_digest = record_serialization.sha256_text(record_serialization.canonical_json(adapter_state))
    if closure.get("adapter_state_digest") != adapter_digest:
        raise ValueError("Closure adapter-state digest mismatch")

    expected_artifacts = {
        "staged_name_status": f"closure/{attempt_id}.staged.name-status.txt",
        "unstaged_name_status": f"closure/{attempt_id}.unstaged.name-status.txt",
        "staged_stat": f"closure/{attempt_id}.staged.stat.txt",
        "unstaged_stat": f"closure/{attempt_id}.unstaged.stat.txt",
        "task_patch": f"closure/{attempt_id}.diff.patch",
    }
    artifacts = closure.get("evidence_artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != set(expected_artifacts):
        raise ValueError("Closure artifact set mismatch")
    artifact_contents: dict[str, str] = {}
    artifact_digests: dict[str, str] = {}
    for name, relative in expected_artifacts.items():
        artifact = artifacts[name]
        if not isinstance(artifact, dict) or artifact.get("path") != relative:
            raise ValueError("Closure artifact path mismatch")
        path = run_dir / relative
        content = path.read_text(errors="surrogateescape")
        digest = record_serialization.sha256_text(content)
        if set(artifact) != {"path", "sha256"} or artifact["sha256"] != digest:
            raise ValueError("Closure artifact digest mismatch")
        artifact_contents[name] = content
        artifact_digests[name] = digest
    for prefix in ("staged", "unstaged"):
        if (
            closure.get(f"{prefix}_changes") != artifact_contents[f"{prefix}_name_status"].strip()
            or closure.get(f"{prefix}_digest") != artifact_digests[f"{prefix}_name_status"]
            or closure.get(f"{prefix}_stat_digest") != artifact_digests[f"{prefix}_stat"]
        ):
            raise ValueError(f"Closure {prefix} artifact binding mismatch")
    if (
        closure.get("task_patch") != artifact_contents["task_patch"]
        or closure.get("task_patch_digest") != artifact_digests["task_patch"]
        or closure.get("head_before") != baseline["head_oid"]
        or closure.get("index_tree_digest") != record_serialization.sha256_text(closure.get("index_tree", ""))
    ):
        raise ValueError("Closure Git evidence binding mismatch")
    status_digest = closure.get("post_worker_status_sha256")
    if not isinstance(status_digest, str):
        raise ValueError("Closure lacks the canonical post-worker status digest")
    evidence_record = {
        "policy_sha256": ledger["policy_sha256"],
        "manifest_sha256": ledger["manifest_sha256"],
        "baseline_sha256": baseline_digest,
        "prompt_sha256": attempt["prompt_sha256"],
        "head_before": closure["head_before"],
        "head_after": closure.get("head_after"),
        "index_tree_before": baseline["index_tree"],
        "index_tree_after": closure.get("index_tree"),
        "artifact_digests": artifact_digests,
        "untracked_paths": closure.get("untracked_paths"),
        "adapter_state_digest": adapter_digest,
        "post_worker_status_sha256": status_digest,
    }
    if closure.get("evidence_digest") != record_serialization.sha256_text(record_serialization.canonical_json(evidence_record)):
        raise ValueError("Closure evidence digest mismatch")
    subject = {
        "run_id": ledger["run_id"],
        "task_id": selected["id"],
        "attempt_id": attempt_id,
        "turn": 1,
        "policy_sha256": ledger["policy_sha256"],
        "manifest_sha256": ledger["manifest_sha256"],
        "prompt_sha256": attempt["prompt_sha256"],
        "selected_task_baseline_sha256": baseline_digest,
    }
    closure_identity = {
        "subject": subject,
        "stage2_git_evidence_sha256": closure["evidence_digest"],
        "post_worker_head_oid": closure.get("head_after"),
        "post_worker_index_tree_oid": closure.get("index_tree"),
        "post_worker_status_sha256": status_digest,
    }
    execution_contracts.validate_closure_identity(closure_identity, expected_subject=subject)
    return ledger, policy, selected, baseline, attempt, adapter_state, worker_result, {
        "packet": closure, "identity": closure_identity,
    }


def _validate_closure_observations(
    *,
    closure: dict[str, Any],
    baseline: dict[str, Any],
    selected: dict[str, Any],
    current_status: dict[str, str],
) -> None:
    observations = closure.get("controller_observations")
    if not isinstance(observations, dict):
        raise ValueError("Closure controller observations are missing")
    baseline_status = baseline["status"]
    current_paths = set(current_status)
    baseline_paths = set(baseline_status)
    allowed = set(selected["allowed_paths"])
    expected = {
        "head_changed": closure["head_after"] != baseline["head_oid"],
        "index_changed": closure["index_tree"] != baseline["index_tree"],
        "allowed_changed_paths": sorted(
            path for path in current_paths
            if path in allowed and (
                path not in baseline_status or current_status[path] != baseline_status[path]
            )
        ),
        "unexpected_paths": sorted(current_paths - baseline_paths - allowed),
        "disappeared_preexisting_paths": sorted(baseline_paths - current_paths),
        "modified_preexisting_paths": sorted(
            path for path in baseline_paths & current_paths
            if baseline_status[path] != current_status[path]
        ),
        "untracked_paths": sorted(
            path for path, value in current_status.items() if value.startswith("??:")
        ),
        "index_tree": closure["index_tree"],
        "index_tree_digest": closure["index_tree_digest"],
        "staged_changes": closure["staged_changes"],
        "staged_digest": closure["staged_digest"],
        "unstaged_changes": closure["unstaged_changes"],
        "unstaged_digest": closure["unstaged_digest"],
    }
    mechanical = []
    if expected["head_changed"]:
        mechanical.append("worker changed HEAD despite commit prohibition")
    if expected["index_changed"]:
        mechanical.append("worker changed the Git index")
    expected["mechanical_violations"] = mechanical
    if any(observations.get(field) != value for field, value in expected.items()):
        raise ValueError("Closure controller observations mismatch exact workspace evidence")
    if closure.get("untracked_paths") != expected["untracked_paths"]:
        raise ValueError("Closure untracked-path evidence mismatch")


def _build_inspection_decision(
    *,
    policy: dict[str, Any],
    selected: dict[str, Any],
    worker_result: dict[str, Any],
    adapter_state: dict[str, Any],
    closure: dict[str, Any],
    closure_identity: dict[str, Any],
    verification_path: str,
    verification_digest: str,
    execution: dict[str, Any],
    plan: dict[str, Any],
    drift_findings: list[str],
    current_step: str,
) -> dict[str, Any]:
    reasons = []
    resume_policies = []
    status = worker_result.get("status")
    if status != "complete":
        reasons.append(f"worker result status is {status!r}, not complete")
        if status == "needs_input":
            resume_policies.append("on_needs_input")
        elif status == "blocked":
            resume_policies.append("on_blocked")
        else:
            resume_policies.append("on_failed")
    if worker_result.get("task_id") != selected["id"]:
        reasons.append("worker result task id does not match the selected task")
    if any(
        isinstance(question, dict) and question.get("blocking")
        for question in worker_result.get("questions", [])
    ):
        reasons.append("worker result contains a blocking question")
        resume_policies.append("on_needs_input")
    if worker_result.get("risks"):
        reasons.append("worker result contains unresolved risks")
        resume_policies.append("on_blocked")

    outcomes = {outcome["id"]: outcome for outcome in execution["outcomes"]}
    for command in plan["commands"]:
        outcome = outcomes.get(command["id"])
        status_value = outcome.get("status") if outcome else "not_run"
        if any(role in {"task_required", "policy_targeted"} for role in command["roles"]):
            if status_value != "passed":
                reasons.append(
                    f"targeted verification {command['id']} did not pass: {status_value}"
                )
                resume_policies.append("on_failed")
        elif status_value not in {"passed", "authorized_gap"}:
            reasons.append(
                f"repository gate {command['id']} did not pass or match its authorized gap: "
                f"{status_value}"
            )
            resume_policies.append("on_failed")
    observations = closure["controller_observations"]
    for field, label in (
        ("unexpected_paths", "unexpected changed paths"),
        ("disappeared_preexisting_paths", "pre-existing dirty paths disappeared"),
        ("modified_preexisting_paths", "pre-existing dirty paths changed"),
        ("mechanical_violations", "worker Git violations"),
    ):
        if observations[field]:
            reasons.append(f"{label}: {', '.join(observations[field])}")
            resume_policies.append("on_unexpected_changes")
    if drift_findings:
        reasons.extend(drift_findings)
        resume_policies.append("on_unexpected_changes")

    mechanically_eligible = not reasons
    accepted = mechanically_eligible and current_step == "accept"
    if accepted:
        reasons = ["mechanical checks passed"]
        allowed_actions = ["accept", "stop"]
        allowed_transitions = ["accepted", "stopped"]
    else:
        if mechanically_eligible:
            reasons = [
                "mechanical checks passed",
                f"{current_step} is pending",
            ]
        allowed_actions = ["stop"]
        allowed_transitions = ["stopped"]
        thread_id = adapter_state.get("thread_id")
        resume_allowed = (
            isinstance(thread_id, str) and bool(thread_id)
            and adapter_state.get("process_pid") is None
            and bool(resume_policies)
            and all(policy["stop_policy"][entry] == "escalate" for entry in resume_policies)
        )
        if resume_allowed:
            allowed_actions.insert(0, "resume")
            allowed_transitions.insert(0, "resumable")
    return {
        "version": 1,
        "closure_identity": closure_identity,
        "verification_path": verification_path,
        "verification_sha256": verification_digest,
        "accepted": accepted,
        "reasons": reasons,
        "allowed_actions": allowed_actions,
        "allowed_transitions": allowed_transitions,
        "gap_details": execution["authorized_gap"],
        "semantic_review": "not_collected",
    }


def inspect_run(run_dir: Path, timeout_seconds: float) -> dict[str, Any]:
    if (
        type(timeout_seconds) not in {int, float}
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        raise ValueError("timeout must be greater than zero")
    run_dir = run_dir.resolve()
    preliminary_ledger = json.loads((run_dir / "ledger.json").read_text())
    if run_records.active_actor(preliminary_ledger):
        return {"status": "refused", "reason": "active_operation", "next_actions": ["observe_operation", "intervene"]}
    if preliminary_ledger.get("actor_operations"):
        run_authority.load_run_context(run_dir)
        return {"status": "pending", "reason": "successor_inspection_pending", "next_actions": ["intervene"]}
    if preliminary_ledger["state"] != "awaiting_inspection":
        raise ValueError("inspect requires run state 'awaiting_inspection'")
    ledger_rules.validate_ledger(preliminary_ledger)
    run_authority.load_flow_authority(run_dir, preliminary_ledger)
    with storage.RunCommandLock(run_dir):
        (
            ledger, policy, selected, baseline, attempt, adapter_state,
            worker_result, closure_data,
        ) = _load_inspection_authority(run_dir)
        if run_records.active_actor(ledger):
            return {"status": "refused", "reason": "active_operation", "next_actions": ["observe_operation", "intervene"]}
        closure = closure_data["packet"]
        closure_identity = closure_data["identity"]
        flow = run_authority.load_flow_authority(run_dir, ledger)
        verify_step = flow_policy.flow_step(flow, "verify")
        verify_enabled = verify_step is not None
        completed_cursor = flow_policy.transition_flow_cursor(
            flow,
            {
                "current_step": "implement",
                "correction_cycle": ledger["correction_cycle"],
            },
            "complete_inspection",
        )
        if ledger["current_step"] not in {
            "implement", completed_cursor["current_step"],
        }:
            raise ValueError("inspect cursor contradicts the current flow")
        if (
            ledger["current_step"] != "implement"
            and (
                ledger["last_verification_path"] is None
                or ledger["last_decision_path"] is None
            )
        ):
            raise ValueError("advanced inspection cursor lacks durable records")
        repo = Path(ledger["repository"]).resolve()
        expected_pre_identity = {
            "head_oid": closure_identity["post_worker_head_oid"],
            "index_tree_oid": closure_identity["post_worker_index_tree_oid"],
            "status_sha256": closure_identity["post_worker_status_sha256"],
        }

        if verify_step is not None:
            effective_policy = json.loads(json.dumps(policy))
            if verify_step["mode"] == "targeted":
                effective_policy["verification"]["repository_gate"] = None
                effective_policy["verification"]["authorized_gap"] = None
            elif effective_policy["verification"]["repository_gate"] is None:
                raise ValueError(
                    "targeted_plus_repository_gate requires a repository gate"
                )
            plan = verification_runner.build_verification_plan(
                selected, effective_policy
            )
        else:
            plan = {"version": 1, "commands": []}
            plan["plan_sha256"] = record_serialization.sha256_text(record_serialization.canonical_json(plan))
        subject = closure_identity["subject"]
        stem = f"{subject['attempt_id']}.turn-{subject['turn']:03d}"
        execution_relative = f"verification/{stem}.execution.json"
        execution_path = run_dir / execution_relative
        verification_relative = f"verification/{stem}.json"
        verification_path = run_dir / verification_relative
        decision_relative = f"decisions/{stem}.json"
        decision_path = run_dir / decision_relative
        if decision_path.exists() and not verification_path.exists():
            raise ValueError(
                "Existing decision record has no prerequisite verification record"
            )
        if not verify_enabled:
            if execution_path.exists():
                raw_execution = execution_path.read_bytes()
                execution = json.loads(raw_execution)
                execution_contracts.validate_command_execution_record(
                    execution, expected_closure_identity=closure_identity
                )
                if execution["terminal_reason"] != "omitted_by_policy":
                    raise ValueError("Verify-off execution record is not omitted by policy")
                execution_digest = run_records.sha256_bytes(raw_execution)
                pre_identity = expected_pre_identity
                post_identity = git.capture_workspace_identity(repo)
            else:
                pre_identity = git.capture_workspace_identity(repo)
                if pre_identity != expected_pre_identity:
                    raise ValueError("Workspace identity changed before inspection")
                current_status = git.capture_git_status(repo)
                if (
                    record_serialization.sha256_text(record_serialization.canonical_json(current_status))
                    != pre_identity["status_sha256"]
                ):
                    raise ValueError("Workspace identity changed during inspection")
                _validate_closure_observations(
                    closure=closure, baseline=baseline, selected=selected,
                    current_status=current_status,
                )
                timestamp = run_records.now_iso()
                execution = {
                    "version": 1,
                    "closure_identity": closure_identity,
                    "plan": [],
                    "outcomes": [],
                    "effective_envelope": policy["permissions"],
                    "started_at": timestamp,
                    "ended_at": timestamp,
                    "terminal_reason": "omitted_by_policy",
                    "authorized_gap": None,
                }
                execution, execution_digest = storage.publish_or_reuse_record(
                    execution_path,
                    execution,
                    lambda record: execution_contracts.validate_command_execution_record(
                        record, expected_closure_identity=closure_identity
                    ),
                )
                post_identity = git.capture_workspace_identity(repo)
            if verification_path.exists():
                existing_verification = json.loads(verification_path.read_text())
                if post_identity != existing_verification.get("post_verification_git"):
                    raise ValueError(
                        "Workspace identity changed after recorded inspection"
                    )
        elif verification_path.exists():
            execution, execution_digest = _validate_execution_artifacts(
                run_dir=run_dir,
                record_path=execution_path,
                closure_identity=closure_identity,
                plan=plan,
                permissions=policy["permissions"],
            )
            post_identity = git.capture_workspace_identity(repo)
            existing_verification = json.loads(verification_path.read_text())
            recorded_post_identity = existing_verification.get("post_verification_git")
            if post_identity != recorded_post_identity:
                raise ValueError(
                    "Workspace identity changed after recorded verification"
                )
            pre_identity = expected_pre_identity
        elif execution_path.exists():
            execution, execution_digest = _validate_execution_artifacts(
                run_dir=run_dir,
                record_path=execution_path,
                closure_identity=closure_identity,
                plan=plan,
                permissions=policy["permissions"],
            )
            pre_identity = expected_pre_identity
            post_identity = git.capture_workspace_identity(repo)
        else:
            pre_identity = git.capture_workspace_identity(repo)
            if pre_identity != expected_pre_identity:
                raise ValueError("Workspace identity changed before verification")
            current_status = git.capture_git_status(repo)
            if record_serialization.sha256_text(record_serialization.canonical_json(current_status)) != pre_identity["status_sha256"]:
                raise ValueError("Workspace identity changed during pre-verification inspection")
            _validate_closure_observations(
                closure=closure, baseline=baseline, selected=selected,
                current_status=current_status,
            )
            execution, execution_digest = verification_runner.execute_verification_plan(
                plan=plan,
                repository_cwd=repo,
                permissions=policy["permissions"],
                timeout_seconds=timeout_seconds,
                run_directory=run_dir,
                execution_path=execution_relative,
                closure_identity=closure_identity,
            )
            post_identity = git.capture_workspace_identity(repo)

        drift_findings = []
        if post_identity["head_oid"] != pre_identity["head_oid"]:
            drift_findings.append("verification changed HEAD")
        if post_identity["index_tree_oid"] != pre_identity["index_tree_oid"]:
            drift_findings.append("verification changed the Git index")
        if post_identity["status_sha256"] != pre_identity["status_sha256"]:
            drift_findings.append("verification changed workspace content or paths")
        execution_passed = execution["terminal_reason"] in {
            "complete", "authorized_gap", "omitted_by_policy",
        }
        verification = {
            "version": 1,
            "closure_identity": closure_identity,
            "execution_path": execution_relative,
            "execution_sha256": execution_digest,
            "pre_verification_git": pre_identity,
            "post_verification_git": post_identity,
            "drift_findings": drift_findings,
            "outcome": (
                "omitted_by_policy"
                if execution["terminal_reason"] == "omitted_by_policy"
                and not drift_findings
                else "passed" if execution_passed and not drift_findings
                else "failed"
            ),
        }
        verification, verification_digest = storage.publish_or_reuse_record(
            verification_path,
            verification,
            lambda record: execution_contracts.validate_verification_record(
                record,
                expected_closure_identity=closure_identity,
                expected_execution_sha256=execution_digest,
            ),
        )
        decision = _build_inspection_decision(
            policy=policy,
            selected=selected,
            worker_result=worker_result,
            adapter_state=adapter_state,
            closure=closure,
            closure_identity=closure_identity,
            verification_path=verification_relative,
            verification_digest=verification_digest,
            execution=execution,
            plan=plan,
            drift_findings=verification["drift_findings"],
            current_step=completed_cursor["current_step"],
        )
        decision, _decision_digest = storage.publish_or_reuse_record(
            decision_path,
            decision,
            lambda record: execution_contracts.validate_closure_decision(
                record,
                expected_closure_identity=closure_identity,
                expected_verification_sha256=verification_digest,
            ),
        )
        for field, expected in (
            ("last_verification_path", verification_relative),
            ("last_decision_path", decision_relative),
        ):
            if ledger[field] not in {None, expected}:
                raise ValueError(f"Ledger {field} contradicts inspection artifacts")
        if (
            ledger["last_verification_path"] != verification_relative
            or ledger["last_decision_path"] != decision_relative
            or ledger["current_step"] == "implement"
        ):
            updater = {
                "last_verification_path": verification_relative,
                "last_decision_path": decision_relative,
            }
            cursor_action = None
            if ledger["current_step"] == "implement":
                updater["current_step"] = completed_cursor["current_step"]
                cursor_action = "complete_inspection"
            run_authority.update_ledger_locked(
                run_dir,
                updater,
                expected_revision=ledger["revision"],
                flow=flow,
                cursor_action=cursor_action,
            )
        return {
            "status": "awaiting_inspection",
            "task_id": selected["id"],
            "accepted": decision["accepted"],
            "allowed_actions": decision["allowed_actions"],
            "verification_path": str(verification_path),
            "decision_path": str(decision_path),
        }

