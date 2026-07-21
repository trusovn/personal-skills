#!/usr/bin/env python3
"""Small Stage 1 policy, prompt, attempt, and closure primitives."""

from __future__ import annotations

import fcntl
import hashlib
import importlib.util
import json
import math
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

_verification_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_verification_runner",
    Path(__file__).with_name("verification_runner.py"),
)
_verification_module = importlib.util.module_from_spec(_verification_spec)
assert _verification_spec.loader is not None
_verification_spec.loader.exec_module(_verification_module)

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
            "last_closure_sha256": None,
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


class RunCommandLock:
    """One non-blocking local lock for an existing run."""

    def __init__(self, run_dir: Path):
        self.path = run_dir / "controller.lock"
        self.stream = None

    def acquire(self) -> None:
        if self.stream is not None:
            return
        stream = self.path.open("a+")
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            stream.close()
            raise ValueError(
                "Another controller command owns this run's mutation phase"
            )
        self.stream = stream

    def release(self) -> None:
        if self.stream is None:
            return
        fcntl.flock(self.stream.fileno(), fcntl.LOCK_UN)
        self.stream.close()
        self.stream = None

    def __enter__(self) -> "RunCommandLock":
        self.acquire()
        return self

    def __exit__(self, *_args: object) -> None:
        self.release()


def _update_ledger_locked(
    run_dir: Path, updater: dict[str, Any], *, expected_revision: int,
    closure_decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    ledger = _state_module.apply_ledger_update(
        ledger, updater, _now_iso(), expected_revision=expected_revision,
        closure_decision=closure_decision,
    )
    atomic_write_json(ledger_path, ledger)
    return ledger


def update_ledger(
    run_dir: Path, updater: dict[str, Any], *, expected_revision: int,
    closure_decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Lock, validate the expected revision, and atomically update the ledger."""
    with RunCommandLock(run_dir):
        return _update_ledger_locked(
            run_dir, updater, expected_revision=expected_revision,
            closure_decision=closure_decision,
        )


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


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_record_bytes(record: dict[str, Any]) -> bytes:
    return canonical_json(record).encode()


def _publish_or_reuse_record(
    path: Path,
    record: dict[str, Any],
    validator: Any,
) -> tuple[dict[str, Any], str]:
    validator(record)
    serialized = _canonical_record_bytes(record)
    if path.exists():
        existing_bytes = path.read_bytes()
        try:
            existing = json.loads(existing_bytes)
        except json.JSONDecodeError as error:
            raise ValueError(f"Existing record is invalid: {path.name}") from error
        validator(existing)
        if existing_bytes != serialized:
            raise ValueError(f"Existing record bytes contradict inspection: {path.name}")
        return existing, _sha256_bytes(existing_bytes)
    with path.open("xb") as stream:
        stream.write(serialized)
        stream.flush()
        import os
        os.fsync(stream.fileno())
    return json.loads(serialized), _sha256_bytes(serialized)


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
    if raw != _canonical_record_bytes(record):
        raise ValueError("Existing command-execution record is not canonical")
    _state_module.validate_command_execution_record(
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
            if not artifact.is_file() or _sha256_bytes(artifact.read_bytes()) != outcome[
                f"{stream_name}_sha256"
            ]:
                raise ValueError(f"Existing command-execution {stream_name} artifact mismatch")
    return record, _sha256_bytes(raw)


def _load_inspection_authority(
    run_dir: Path,
) -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any],
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any],
]:
    ledger = json.loads((run_dir / "ledger.json").read_text())
    _validate_ledger(ledger)
    if ledger["state"] != "awaiting_inspection":
        raise ValueError("inspect requires run state 'awaiting_inspection'")

    policy_path = run_dir / "run-policy.json"
    manifest_path = run_dir / "task-manifest.json"
    if ledger["policy_path"] != "run-policy.json" or ledger["manifest_path"] != "task-manifest.json":
        raise ValueError("Persisted authority path mismatch")
    policy = json.loads(policy_path.read_text())
    validate_run_policy(policy)
    if sha256_text(canonical_json(policy)) != ledger["policy_sha256"]:
        raise ValueError("Persisted policy digest mismatch")
    manifest = json.loads(manifest_path.read_text())
    if sha256_text(canonical_json(manifest)) != ledger["manifest_sha256"]:
        raise ValueError("Persisted manifest digest mismatch")
    repo = Path(ledger["repository"]).resolve()
    if repo != Path(policy["repository"]).resolve() or _git_module.repository_top_level(repo) != repo:
        raise ValueError("Persisted repository identity mismatch")
    validated_manifest = validate_task_manifest(policy, manifest, repo)
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
    if set(baseline) != {"head_oid", "index_tree", "status"}:
        raise ValueError("Selected task baseline has an invalid shape")
    baseline_digest = sha256_text(canonical_json(baseline))
    if baseline_digest != ledger.get("selected_task_baseline_digest"):
        raise ValueError("Selected task baseline digest mismatch")

    attempt_dir = run_dir / "attempts" / attempt_id
    attempt = json.loads((attempt_dir / "record.json").read_text())
    validate_attempt_record(attempt)
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
        or attempt["prompt_sha256"] != sha256_text(prompt)
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
        or adapter_state.get("attempt_outcome") != _worker_module.result_status(result_path)
        or adapter_state.get("process_pid") is not None
        or adapter_state.get("cwd") != str(repo)
        or adapter_state.get("prompt_sha256") != attempt["prompt_sha256"]
        or Path(adapter_state.get("result_path", "")).resolve() != result_path.resolve()
    ):
        raise ValueError("Adapter state or structured result identity mismatch")

    closure_path = run_dir / ledger["last_closure_path"]
    closure_bytes = closure_path.read_bytes()
    if _sha256_bytes(closure_bytes) != ledger.get("last_closure_sha256"):
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
    }
    if any(closure.get(field) != value for field, value in expected_top.items()):
        raise ValueError("Closure identity field mismatch")
    claims = closure.get("worker_claims")
    if not isinstance(claims, dict):
        raise ValueError("Closure worker claims are invalid")
    if claims.get("result_sha256") != _sha256_bytes(result_bytes):
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
    adapter_digest = sha256_text(canonical_json(adapter_state))
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
        digest = sha256_text(content)
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
        or closure.get("index_tree_digest") != sha256_text(closure.get("index_tree", ""))
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
    if closure.get("evidence_digest") != sha256_text(canonical_json(evidence_record)):
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
    _state_module.validate_closure_identity(closure_identity, expected_subject=subject)
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

    accepted = not reasons
    if accepted:
        reasons = ["mechanical checks passed"]
        allowed_actions = ["accept", "stop"]
        allowed_transitions = ["accepted", "stopped"]
    else:
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
    _validate_ledger(preliminary_ledger)
    if preliminary_ledger["state"] != "awaiting_inspection":
        raise ValueError("inspect requires run state 'awaiting_inspection'")
    with RunCommandLock(run_dir):
        (
            ledger, policy, selected, baseline, attempt, adapter_state,
            worker_result, closure_data,
        ) = _load_inspection_authority(run_dir)
        closure = closure_data["packet"]
        closure_identity = closure_data["identity"]
        repo = Path(ledger["repository"]).resolve()
        expected_pre_identity = {
            "head_oid": closure_identity["post_worker_head_oid"],
            "index_tree_oid": closure_identity["post_worker_index_tree_oid"],
            "status_sha256": closure_identity["post_worker_status_sha256"],
        }

        plan = _verification_module.build_verification_plan(selected, policy)
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
        if verification_path.exists():
            execution, execution_digest = _validate_execution_artifacts(
                run_dir=run_dir,
                record_path=execution_path,
                closure_identity=closure_identity,
                plan=plan,
                permissions=policy["permissions"],
            )
            post_identity = _git_module.capture_workspace_identity(repo)
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
            post_identity = _git_module.capture_workspace_identity(repo)
        else:
            pre_identity = _git_module.capture_workspace_identity(repo)
            if pre_identity != expected_pre_identity:
                raise ValueError("Workspace identity changed before verification")
            current_status = _git_module.capture_git_status(repo)
            if sha256_text(canonical_json(current_status)) != pre_identity["status_sha256"]:
                raise ValueError("Workspace identity changed during pre-verification inspection")
            _validate_closure_observations(
                closure=closure, baseline=baseline, selected=selected,
                current_status=current_status,
            )
            execution, execution_digest = _verification_module.execute_verification_plan(
                plan=plan,
                repository_cwd=repo,
                permissions=policy["permissions"],
                timeout_seconds=timeout_seconds,
                run_directory=run_dir,
                execution_path=execution_relative,
                closure_identity=closure_identity,
            )
            post_identity = _git_module.capture_workspace_identity(repo)

        drift_findings = []
        if post_identity["head_oid"] != pre_identity["head_oid"]:
            drift_findings.append("verification changed HEAD")
        if post_identity["index_tree_oid"] != pre_identity["index_tree_oid"]:
            drift_findings.append("verification changed the Git index")
        if post_identity["status_sha256"] != pre_identity["status_sha256"]:
            drift_findings.append("verification changed workspace content or paths")
        execution_passed = execution["terminal_reason"] in {"complete", "authorized_gap"}
        verification = {
            "version": 1,
            "closure_identity": closure_identity,
            "execution_path": execution_relative,
            "execution_sha256": execution_digest,
            "pre_verification_git": pre_identity,
            "post_verification_git": post_identity,
            "drift_findings": drift_findings,
            "outcome": "passed" if execution_passed and not drift_findings else "failed",
        }
        verification, verification_digest = _publish_or_reuse_record(
            verification_path,
            verification,
            lambda record: _state_module.validate_verification_record(
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
        )
        decision, _decision_digest = _publish_or_reuse_record(
            decision_path,
            decision,
            lambda record: _state_module.validate_closure_decision(
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
        ):
            _update_ledger_locked(run_dir, {
                "last_verification_path": verification_relative,
                "last_decision_path": decision_relative,
            }, expected_revision=ledger["revision"])
        return {
            "status": "awaiting_inspection",
            "task_id": selected["id"],
            "accepted": decision["accepted"],
            "allowed_actions": decision["allowed_actions"],
            "verification_path": str(verification_path),
            "decision_path": str(decision_path),
        }


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

    inspect_parser = subparsers.add_parser(
        "inspect", help="Independently verify one completed worker attempt"
    )
    inspect_parser.add_argument("--run-dir", required=True)
    inspect_parser.add_argument("--timeout-seconds", type=float, required=True)
    inspect_parser.set_defaults(handler=_cli_inspect)

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
    lock = RunCommandLock(run_dir)
    lock.acquire()
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
    ledger = _update_ledger_locked(run_dir, {
        "state": "running",
        "selected_task_id": task["id"],
        "active_attempt_id": attempt_id,
        "selected_task_baseline_ref": task_baseline_ref,
        "selected_task_baseline_digest": task_baseline_digest,
        "tasks": running_tasks,
    }, expected_revision=ledger["revision"])
    running_revision = ledger["revision"]
    lock.release()

    def stop_active_attempt(reason: str) -> int:
        print(reason, file=sys.stderr)
        stopped_tasks = [dict(entry) for entry in ledger["tasks"]]
        next(entry for entry in stopped_tasks if entry["id"] == task["id"])["state"] = "stopped"
        _update_ledger_locked(run_dir, {
            "state": "stopped",
            "selected_task_id": None,
            "active_attempt_id": None,
            "tasks": stopped_tasks,
        }, expected_revision=ledger["revision"])
        lock.release()
        return 1

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
            "result_sha256": _sha256_bytes(result_path.read_bytes()),
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
    closure_sha256 = _sha256_bytes(closure_json_path.read_bytes())

    awaiting_tasks = [dict(entry) for entry in ledger["tasks"]]
    next(entry for entry in awaiting_tasks if entry["id"] == task["id"])["state"] = "awaiting_inspection"
    _update_ledger_locked(run_dir, {
        "state": "awaiting_inspection",
        "selected_task_id": task["id"],
        "active_attempt_id": None,
        "last_closure_path": str(closure_json_path.relative_to(run_dir)),
        "last_closure_sha256": closure_sha256,
        "tasks": awaiting_tasks,
    }, expected_revision=ledger["revision"])
    lock.release()

    print(json.dumps({
        "status": "awaiting_inspection",
        "task_id": task["id"],
        "closure_path": str(closure_json_path),
    }, sort_keys=True))
    return 0


def _cli_inspect(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    result = inspect_run(Path(args.run_dir).resolve(), args.timeout_seconds)
    print(json.dumps(result, sort_keys=True))
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
