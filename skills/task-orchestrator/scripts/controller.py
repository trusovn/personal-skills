#!/usr/bin/env python3
"""Small Stage 1 policy, prompt, attempt, and closure primitives."""

from __future__ import annotations

import fcntl
import hashlib
import importlib.util
import json
import math
import os
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
validate_flow_profile = _state_module.validate_flow_profile
resolve_flow_profile = _state_module.resolve_flow_profile
validate_flow_cursor = _state_module.validate_flow_cursor
transition_flow_cursor = _state_module.transition_flow_cursor
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


def _canonical_flow_bytes(flow: dict[str, Any]) -> bytes:
    validate_flow_profile(flow)
    return (canonical_json(flow) + "\n").encode()


def _sync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_durable_exclusive(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
        _sync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def load_input_authority(run_dir: Path, ledger: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Resolve all current inputs from one ledger snapshot and immutable bundle."""
    action = "Initialize a new run using reviewed current inputs."
    revisions = ledger.get("input_revisions", [])
    if revisions:
        _state_module.validate_input_revisions(ledger)
        receipt = revisions[-1]
        raw = (run_dir / receipt["path"]).read_bytes()
        if _sha256_bytes(raw) != receipt["sha256"]:
            raise ValueError("Persisted input revision digest mismatch")
        bundle = json.loads(raw)
        if bundle["request"] != receipt["request"]:
            raise ValueError("Persisted input revision request mismatch")
        policy = bundle["request"]["payload"]["policy"]
        manifest = bundle["request"]["payload"]["manifest"]
        inputs = bundle["inputs"]
        inputs_raw = _canonical_record_bytes(inputs)
    else:
        if ledger["policy_path"] != "run-policy.json" or ledger["manifest_path"] != "task-manifest.json":
            raise ValueError("Persisted authority path mismatch")
        policy = json.loads((run_dir / ledger["policy_path"]).read_text())
        manifest = json.loads((run_dir / ledger["manifest_path"]).read_text())
        inputs_raw = (run_dir / "inputs.json").read_bytes()
        inputs = json.loads(inputs_raw)
    try:
        validate_run_policy(policy)
        if "inputs_sha256" not in ledger:
            raise ValueError("missing frozen task inputs")
    except ValueError as error:
        raise ValueError(f"Incompatible frozen run: {error}. {action}") from error
    if sha256_text(canonical_json(policy)) != ledger["policy_sha256"]:
        raise ValueError("Persisted policy digest mismatch")
    if sha256_text(canonical_json(manifest)) != ledger["manifest_sha256"]:
        raise ValueError("Persisted manifest digest mismatch")
    if _sha256_bytes(inputs_raw) != ledger["inputs_sha256"]:
        raise ValueError("Persisted task input digest mismatch")
    if inputs["task_id"] != policy["task_ids"][0]:
        raise ValueError("Frozen task inputs contradict policy")
    if policy["run_id"] != ledger["run_id"] or Path(policy["repository"]).resolve() != Path(ledger["repository"]).resolve():
        raise ValueError("Persisted run/repository identity mismatch")
    return policy, manifest, inputs


def load_frozen_inputs(run_dir: Path, ledger: dict[str, Any]) -> dict[str, Any]:
    """Read approved bytes only; mutable repository sources are not authority."""
    return load_input_authority(run_dir, ledger)[2]


def _load_flow_authority_state(
    run_dir: Path, ledger: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
    policy, _, _ = load_input_authority(run_dir, ledger)
    revision = ledger["flow_revision"]
    if ledger.get("input_revisions"):
        flow = resolve_flow_profile(policy)
        if _sha256_bytes(_canonical_flow_bytes(flow)) != ledger["flow_sha256"]:
            raise ValueError("Persisted revised flow digest mismatch")
        validate_flow_cursor(flow, {field: ledger[field] for field in ("current_step", "correction_cycle")})
        return flow, {field: ledger[field] for field in ("flow_revision", "flow_path", "flow_sha256")}, None
    expected_path = f"flows/flow-{revision:03d}.json"
    if ledger["flow_path"] != expected_path:
        raise ValueError("Persisted current flow path does not match its revision")
    expected_flow_names = [
        f"flow-{history_revision:03d}.json"
        for history_revision in range(1, revision + 1)
    ]
    actual_flow_names = sorted(
        path.name for path in (run_dir / "flows").glob("flow-*.json")
    )
    candidate_flow_name = f"flow-{revision + 1:03d}.json"
    if not set(expected_flow_names).issubset(actual_flow_names):
        raise ValueError("Persisted flow revision history is not exact")
    extra_flows = set(actual_flow_names) - set(expected_flow_names)
    if not extra_flows.issubset({candidate_flow_name}):
        raise ValueError("Persisted flow revision history is not exact")

    flow = None
    flow_digest = None
    for history_revision in range(1, revision + 1):
        flow_relative = f"flows/flow-{history_revision:03d}.json"
        flow_raw = (run_dir / flow_relative).read_bytes()
        revision_flow = json.loads(flow_raw)
        try:
            validate_flow_profile(revision_flow)
        except ValueError as error:
            raise ValueError(
                f"Incompatible frozen flow: {error}. "
                "Initialize a new run using reviewed current inputs."
            ) from error
        if flow_raw != _canonical_flow_bytes(revision_flow):
            raise ValueError("Persisted flow bytes are not canonical")
        flow_digest = _sha256_bytes(flow_raw)
        flow = revision_flow

    if (
        flow is None
        or flow_digest is None
        or ledger["flow_sha256"] != flow_digest
    ):
        raise ValueError("Persisted current flow digest mismatch")

    candidate = None
    if extra_flows:
        candidate_path = run_dir / "flows" / candidate_flow_name
        candidate_raw = candidate_path.read_bytes()
        candidate_flow = json.loads(candidate_raw)
        validate_flow_profile(candidate_flow)
        if candidate_raw != _canonical_flow_bytes(candidate_flow):
            raise ValueError("Uncommitted flow revision bytes are not canonical")
        candidate_digest = _sha256_bytes(candidate_raw)
        candidate = {
            "flow": candidate_flow,
            "flow_bytes": candidate_raw,
            "flow_sha256": candidate_digest,
        }

    current = ledger["current_step"]
    validate_flow_cursor(
        flow,
        {
            "current_step": current,
            "correction_cycle": ledger["correction_cycle"],
        },
    )
    authority = {
        "flow_revision": revision,
        "flow_path": expected_path,
        "flow_sha256": flow_digest,
    }
    return flow, authority, candidate


def _load_flow_authority(run_dir: Path, ledger: dict[str, Any]) -> dict[str, Any]:
    flow, _, _ = _load_flow_authority_state(run_dir, ledger)
    return flow


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
    flow = resolve_flow_profile(policy)
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

    selected = next(task for task in manifest["tasks"] if task["id"] == policy["task_ids"][0])
    brief = resolved_repo / selected["brief_path"]
    verification = brief.with_name("verification.md")
    if not verification.resolve().is_relative_to(resolved_repo) or not verification.is_file():
        raise ValueError("Prepared task requires verification.md beside its brief")
    inputs = {"version": 1, "task_id": selected["id"], "documents": {}}
    for name, path in (("brief", brief), ("verification", verification)):
        raw = path.read_bytes()
        inputs["documents"][name] = {
            "source_path": str(path.relative_to(resolved_repo)),
            "content": raw.decode("utf-8"), "sha256": _sha256_bytes(raw),
        }
    inputs["allowed_paths"] = selected["allowed_paths"]
    inputs["required_checks"] = selected.get("required_checks", [])
    inputs_bytes = _canonical_record_bytes(inputs)

    # Enforce run directory is outside the repository
    if run_dir.resolve().is_relative_to(resolved_repo):
        raise ValueError(
            f"Run directory {run_dir} must be outside the repository {resolved_repo}"
        )

    # Capture baseline
    baseline = _git_module.capture_task_baseline(resolved_repo)
    baseline_ref = f"run-initial.json"
    baseline_path = run_dir / "baselines" / baseline_ref

    # Build temporary directory and atomically publish
    temp_dir = run_dir.parent / f".tmp-run-{run_dir.name}-{hashlib.sha256(str(run_dir.name).encode()).hexdigest()[:8]}"
    try:
        # Copy canonical policy and manifest
        policy_digest = persist_run_policy(temp_dir / "run-policy.json", policy)
        _write_durable_exclusive(temp_dir / "inputs.json", inputs_bytes)
        flow_relative = "flows/flow-001.json"
        flow_bytes = _canonical_flow_bytes(flow)
        flow_path = temp_dir / flow_relative
        flow_path.parent.mkdir()
        with flow_path.open("xb") as stream:
            stream.write(flow_bytes)
        flow_digest = _sha256_bytes(flow_bytes)
        manifest_content = manifest_path.read_text()
        manifest_digest = sha256_text(canonical_json(json.loads(manifest_content)))
        (temp_dir / "task-manifest.json").write_text(manifest_content)
        manifest_digest = sha256_text(canonical_json(manifest))

        # Create baselines directory
        (temp_dir / "baselines").mkdir()
        baseline_data = baseline
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
            "flow_revision": 1,
            "flow_path": flow_relative,
            "flow_sha256": flow_digest,
            "inputs_sha256": _sha256_bytes(inputs_bytes),
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
            "actor_operations": [],
            "readiness": None,
            "correction_request": None,
            "candidate_sha256": None,
            "evidence": {},
            "outstanding_findings": [],
            "current_step": None,
            "correction_cycle": 0,
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
    flow: dict[str, Any] | None = None, cursor_action: str | None = None,
    cursor_result: str | None = None,
) -> dict[str, Any]:
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    _load_flow_authority(run_dir, ledger)
    if _active_actor(ledger):
        raise ValueError("Active actor operation blocks legacy ledger mutation")
    ledger = _state_module.apply_ledger_update(
        ledger, updater, _now_iso(), expected_revision=expected_revision,
        closure_decision=closure_decision,
        flow=flow, cursor_action=cursor_action, cursor_result=cursor_result,
    )
    atomic_write_json(ledger_path, ledger)
    return ledger


def update_ledger(
    run_dir: Path, updater: dict[str, Any], *, expected_revision: int,
    closure_decision: dict[str, Any] | None = None,
    flow: dict[str, Any] | None = None, cursor_action: str | None = None,
    cursor_result: str | None = None,
) -> dict[str, Any]:
    """Lock, validate the expected revision, and atomically update the ledger."""
    ledger = json.loads((run_dir / "ledger.json").read_text())
    _load_flow_authority(run_dir, ledger)
    if _active_actor(ledger):
        raise ValueError("Active actor operation blocks legacy ledger mutation")
    with RunCommandLock(run_dir):
        return _update_ledger_locked(
            run_dir, updater, expected_revision=expected_revision,
            closure_decision=closure_decision,
            flow=flow, cursor_action=cursor_action, cursor_result=cursor_result,
        )


def _write_flow_pointer(
    run_dir: Path,
    ledger: dict[str, Any],
    *,
    flow_revision: int,
    flow_path: str,
    flow_sha256: str,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(ledger))
    updated.update({
        "revision": ledger["revision"] + 1,
        "updated_at": _now_iso(),
        "flow_revision": flow_revision,
        "flow_path": flow_path,
        "flow_sha256": flow_sha256,
    })
    _validate_ledger(updated)
    atomic_write_json(run_dir / "ledger.json", updated)
    return updated


def revise_flow(run_dir: Path, flow_path: Path) -> dict[str, Any]:
    """Publish one immutable flow revision at the exact safe task boundary."""
    requested = json.loads(flow_path.read_text())
    validate_flow_profile(requested)
    requested_bytes = _canonical_flow_bytes(requested)
    requested_digest = _sha256_bytes(requested_bytes)
    preliminary_ledger = json.loads((run_dir / "ledger.json").read_text())
    _load_flow_authority(run_dir, preliminary_ledger)
    with RunCommandLock(run_dir):
        ledger = json.loads((run_dir / "ledger.json").read_text())
        _validate_ledger(ledger)
        _, authority, candidate = _load_flow_authority_state(run_dir, ledger)
        if (
            ledger["state"] != "ready"
            or ledger["selected_task_id"] is not None
            or ledger["active_attempt_id"] is not None
            or ledger["active_operation_path"] is not None
            or ledger["current_step"] is not None
            or ledger["correction_cycle"] != 0
        ):
            raise ValueError("Flow revision requires the exact safe task boundary")
        if requested_digest == authority["flow_sha256"]:
            return {
                "status": "unchanged",
                "flow_revision": authority["flow_revision"],
                "flow_sha256": authority["flow_sha256"],
            }
        revision = authority["flow_revision"] + 1
        relative = f"flows/flow-{revision:03d}.json"
        published = run_dir / relative
        if candidate is not None:
            if candidate["flow_sha256"] != requested_digest:
                raise ValueError(
                    "An interrupted flow revision must be retried with the same flow"
                )
            if candidate["flow_bytes"] != requested_bytes:
                raise ValueError("Uncommitted flow revision digest collision")
        else:
            _write_durable_exclusive(published, requested_bytes)
        try:
            _write_flow_pointer(
                run_dir,
                ledger,
                flow_revision=revision,
                flow_path=relative,
                flow_sha256=requested_digest,
            )
        except Exception:
            try:
                committed = json.loads((run_dir / "ledger.json").read_text())
                _validate_ledger(committed)
            except Exception:
                raise
            if (
                committed["flow_revision"] != revision
                or committed["flow_path"] != relative
                or committed["flow_sha256"] != requested_digest
            ):
                raise
        return {
            "status": "revised",
            "flow_revision": revision,
            "flow_sha256": requested_digest,
        }


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
    flow, flow_authority, _ = _load_flow_authority_state(run_dir, ledger)

    policy, manifest, _ = load_input_authority(run_dir, ledger)
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
    if set(baseline) not in ({"head_oid", "index_tree", "status"},
                             {"head_oid", "index_tree", "status", "dirty_files"}):
        raise ValueError("Selected task baseline has an invalid shape")
    baseline_digest = sha256_text(canonical_json(baseline))
    if baseline_digest != ledger.get("selected_task_baseline_digest"):
        raise ValueError("Selected task baseline digest mismatch")

    attempt_dir = run_dir / "attempts" / attempt_id
    attempt_record_bytes = (attempt_dir / "record.json").read_bytes()
    attempt = json.loads(attempt_record_bytes)
    validate_attempt_record(attempt)
    implement = _state_module.flow_step(flow, "implement")
    assert implement is not None
    actor = _state_module.ACTOR_LEVELS[implement["mode"]]
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
        "attempt_record_sha256": _sha256_bytes(attempt_record_bytes),
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
    if _active_actor(preliminary_ledger):
        return {"status": "refused", "reason": "active_operation", "next_actions": ["observe_operation", "intervene"]}
    if preliminary_ledger.get("actor_operations"):
        _reservation_context(run_dir)
        return {"status": "pending", "reason": "successor_inspection_pending", "next_actions": ["intervene"]}
    if preliminary_ledger["state"] != "awaiting_inspection":
        raise ValueError("inspect requires run state 'awaiting_inspection'")
    _validate_ledger(preliminary_ledger)
    _load_flow_authority(run_dir, preliminary_ledger)
    with RunCommandLock(run_dir):
        (
            ledger, policy, selected, baseline, attempt, adapter_state,
            worker_result, closure_data,
        ) = _load_inspection_authority(run_dir)
        if _active_actor(ledger):
            return {"status": "refused", "reason": "active_operation", "next_actions": ["observe_operation", "intervene"]}
        closure = closure_data["packet"]
        closure_identity = closure_data["identity"]
        flow = _load_flow_authority(run_dir, ledger)
        verify_step = _state_module.flow_step(flow, "verify")
        verify_enabled = verify_step is not None
        completed_cursor = transition_flow_cursor(
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
            plan = _verification_module.build_verification_plan(
                selected, effective_policy
            )
        else:
            plan = {"version": 1, "commands": []}
            plan["plan_sha256"] = sha256_text(canonical_json(plan))
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
                _state_module.validate_command_execution_record(
                    execution, expected_closure_identity=closure_identity
                )
                if execution["terminal_reason"] != "omitted_by_policy":
                    raise ValueError("Verify-off execution record is not omitted by policy")
                execution_digest = _sha256_bytes(raw_execution)
                pre_identity = expected_pre_identity
                post_identity = _git_module.capture_workspace_identity(repo)
            else:
                pre_identity = _git_module.capture_workspace_identity(repo)
                if pre_identity != expected_pre_identity:
                    raise ValueError("Workspace identity changed before inspection")
                current_status = _git_module.capture_git_status(repo)
                if (
                    sha256_text(canonical_json(current_status))
                    != pre_identity["status_sha256"]
                ):
                    raise ValueError("Workspace identity changed during inspection")
                _validate_closure_observations(
                    closure=closure, baseline=baseline, selected=selected,
                    current_status=current_status,
                )
                timestamp = _now_iso()
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
                execution, execution_digest = _publish_or_reuse_record(
                    execution_path,
                    execution,
                    lambda record: _state_module.validate_command_execution_record(
                        record, expected_closure_identity=closure_identity
                    ),
                )
                post_identity = _git_module.capture_workspace_identity(repo)
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
            current_step=completed_cursor["current_step"],
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
            _update_ledger_locked(
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


# ── CLI entry points ─────────────────────────────────────────────────


# Actor assignments are embedded in the ledger: one atomic replace publishes
# ownership, assignment and its charge together. No receipt is a liveness oracle.
def _producer_workspace(ledger, inputs):
    return _git_module.capture_candidate_workspace(Path(ledger['repository']), inputs['allowed_paths'])


def _producer_context(run_dir, operation_id):
    ledger, flow = _reservation_context(run_dir)
    policy, manifest, inputs = load_input_authority(run_dir, ledger)
    operation = _actor_operation(ledger, operation_id)
    assignment = operation['assignment']
    if any(assignment[k] != ledger[k] for k in ('inputs_sha256', 'policy_sha256', 'flow_sha256')):
        raise ValueError('Stale operation authority')
    if assignment['task_id'] != inputs['task_id']:
        raise ValueError('Task identity mismatch')
    return ledger, flow, policy, inputs, operation


def inspect_candidate(run_dir: Path, operation_id: str) -> dict[str, Any]:
    """Inspect an admitted terminal producer, never an actor's content claims."""
    try:
        with RunCommandLock(run_dir):
            ledger, flow, policy, inputs, operation = _producer_context(run_dir, operation_id)
            if _active_actor(ledger):
                raise ValueError('An operation is active or unknown')
            if operation['state'] != 'terminal' or operation['assignment']['stage'] not in {'implement', 'correction'}:
                raise ValueError('Terminal implementation/correction required')
            producers = [item for item in ledger['actor_operations'] if item['assignment']['stage'] in {'implement', 'correction'}]
            if operation is not producers[-1]:
                raise ValueError('Historical producer cannot replace current candidate')
            outcome = operation.get('transport', {}).get('outcome')
            if not outcome or outcome['blocker']:
                raise ValueError('Admitted terminal outcome required')
            raw = _worker_module.read_json(Path(outcome['raw_result_path']))
            _validate_observed_result(operation['assignment'], outcome['observed'], raw)
            if raw['status'] != 'complete':
                raise ValueError('Producer did not complete')
            baseline = _worker_module.read_json(run_dir / 'baselines' / ledger['initial_baseline_path'])
            if sha256_text(canonical_json(baseline)) != ledger['initial_baseline_digest']:
                raise ValueError('Initial baseline identity mismatch')
            if 'index_tree' not in baseline or set(baseline.get('dirty_files', {})) != set(baseline['status']):
                raise ValueError('Frozen baseline lacks owner/index identity; initialize a new reviewed run')
            workspace = _producer_workspace(ledger, inputs)
            status = workspace['status']
            dirty = baseline['status']
            violations = sorted(p for p in set(dirty) | set(status)
                                if (p in dirty and (status.get(p) != dirty[p]
                                                   or workspace['files'].get(p) != baseline['dirty_files'][p]))
                                or (p not in dirty and p not in inputs['allowed_paths']))
            staged_paths = _git_module.capture_index_changed_paths(
                Path(ledger['repository']), baseline['index_tree'], workspace['index_tree_oid'])
            violations = sorted(set(violations) | {p for p in staged_paths if p in dirty or p not in inputs['allowed_paths']})
            if workspace['head_oid'] != baseline['head_oid']:
                violations.append('HEAD changed')
            if violations:
                return {'status': 'blocked', 'reason': 'scope_or_owner_work_violation', 'paths': violations}
            candidate = {'operation_id': operation_id, 'assignment': operation['assignment'],
                         'baseline_sha256': ledger['initial_baseline_digest'], 'workspace': workspace}
            digest = sha256_text(canonical_json(candidate))
            relative = f'candidates/{digest}.json'
            _publish_actor_bytes(run_dir / relative, _canonical_record_bytes(candidate))
            if ledger.get('candidate_sha256') != digest:
                ledger.update(candidate_sha256=digest, candidate_path=relative, current_step='verify')
                ledger.setdefault('evidence', {})['implement'] = {
                    'status': 'passed', 'inputs_sha256': ledger['inputs_sha256'],
                    'candidate_sha256': digest, 'operation_id': operation_id, 'path': relative}
                _save_actor_ledger(run_dir, ledger)
            return {'status': 'passed', 'candidate_sha256': digest, 'path': relative}
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {'status': 'refused', 'reason': str(error)}


def _load_current_candidate(run_dir, ledger, inputs):
    candidate = _worker_module.read_json(run_dir / ledger['candidate_path'])
    if sha256_text(canonical_json(candidate)) != ledger['candidate_sha256']:
        raise ValueError('Candidate artifact identity mismatch')
    if candidate['workspace'] != _producer_workspace(ledger, inputs):
        raise ValueError('Candidate is stale')
    if any(candidate['assignment'][k] != ledger[k] for k in ('inputs_sha256', 'policy_sha256', 'flow_sha256')):
        raise ValueError('Candidate authority is stale')
    return candidate


def _check_closure_identity(ledger, operation, candidate):
    assignment = operation['assignment']
    workspace = candidate['workspace']
    return {
        'subject': {'run_id': ledger['run_id'], 'task_id': assignment['task_id'],
                    'attempt_id': operation['operation_id'], 'turn': 1,
                    'policy_sha256': ledger['policy_sha256'], 'manifest_sha256': ledger['manifest_sha256'],
                    'prompt_sha256': ledger['inputs_sha256'],
                    'selected_task_baseline_sha256': ledger['initial_baseline_digest']},
        'stage2_git_evidence_sha256': ledger['candidate_sha256'],
        'post_worker_head_oid': workspace['head_oid'],
        'post_worker_index_tree_oid': workspace['index_tree_oid'],
        'post_worker_status_sha256': sha256_text(canonical_json(workspace['status']))}


def _publish_check_outcome(run_dir, ledger, operation, result):
    operation['state'] = 'terminal'
    ledger['active_operation_path'] = None
    ledger.setdefault('evidence', {})['verify'] = {
        'status': result['status'], 'inputs_sha256': ledger['inputs_sha256'],
        'candidate_sha256': operation['assignment']['candidate_sha256'],
        'operation_id': operation['operation_id'], 'path': result['path']}
    ledger['actor_blocker'] = result.get('blocker')
    if result['status'] == 'failed':
        ledger.update(correction_request='check_failed')
    elif result['status'] == 'passed':
        ledger['current_step'] = 'semantic_review'
    _save_actor_ledger(run_dir, ledger)


def check_candidate(run_dir: Path, assignment: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    """Run one reserved check once; uncertain interrupted execution never relaunches."""
    if type(timeout_seconds) not in {int, float} or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        return {'status': 'refused', 'reason': 'timeout_seconds must be positive and finite'}
    try:
        with RunCommandLock(run_dir):
            ledger, flow, policy, inputs, operation = _producer_context(run_dir, assignment['operation_id'])
            if not _same_typed_assignment(assignment, operation['assignment']) or assignment['stage'] != 'verify':
                raise ValueError('Exact verifier assignment required')
            if assignment['candidate_sha256'] != ledger.get('candidate_sha256'):
                raise ValueError('Historical candidate cannot become current')
            candidate = _load_current_candidate(run_dir, ledger, inputs)
            relative = f"checks/{operation['operation_id']}.json"
            path = run_dir / relative
            if path.exists():
                result = _worker_module.read_json(path)
                if not _same_typed_assignment(result['assignment'], assignment) or result['timeout_seconds'] != timeout_seconds:
                    raise ValueError('Check identity/configuration conflict')
                if result['status'] == 'blocked' and 'execution_sha256' not in result:
                    return result
                execution_raw = (run_dir / result['execution_path']).read_bytes()
                if _sha256_bytes(execution_raw) != result['execution_sha256']:
                    raise ValueError('Execution record changed')
                execution = json.loads(execution_raw)
                _state_module.validate_command_execution_record(execution, expected_closure_identity=_check_closure_identity(ledger, operation, candidate))
                for outcome in execution['outcomes']:
                    for stream in ('stdout', 'stderr'):
                        if _sha256_bytes((run_dir / outcome[f'{stream}_path']).read_bytes()) != outcome[f'{stream}_sha256']:
                            raise ValueError('Execution log changed')
                if operation['state'] != 'terminal':
                    _publish_check_outcome(run_dir, ledger, operation, result)
                return result
            if operation['state'] != 'reserved':
                return {'status': 'blocked', 'blocker': 'Check execution uncertain; inspect retained evidence and resolve terminality before retry'}
            if _active_actor(ledger) is not operation:
                raise ValueError('Check does not own active operation')
            selected = {'required_checks': inputs['required_checks']}
            check_policy = json.loads(json.dumps(policy))
            check_policy['verification']['authorized_gap'] = None
            omitted = []
            if _state_module.flow_step(flow, 'verify')['mode'] == 'targeted':
                if check_policy['verification']['repository_gate']:
                    omitted.append('repository_gate')
                check_policy['verification']['repository_gate'] = None
            plan = _verification_module.build_verification_plan(selected, check_policy)
            identity = _check_closure_identity(ledger, operation, candidate)
            execution_path = f"verification/{operation['operation_id']}.turn-001.execution.json"
            intent = {'assignment': assignment, 'timeout_seconds': timeout_seconds, 'plan': plan,
                      'candidate_sha256': ledger['candidate_sha256']}
            _publish_actor_bytes(run_dir / f"checks/{operation['operation_id']}.intent.json", _canonical_record_bytes(intent))
            operation['state'] = 'unknown'
            _save_actor_ledger(run_dir, ledger)
            (run_dir / 'verification').mkdir(exist_ok=True)
            result = {'assignment': assignment, 'timeout_seconds': timeout_seconds, 'path': relative,
                      'execution_path': execution_path, 'policy_omissions': omitted, 'plan': plan,
                      'mechanism_limits': 'YOLO does not enforce filesystem or network restrictions',
                      'environment': {'cwd': ledger['repository'], 'platform': sys.platform},
                      'setup': inputs, 'status': 'blocked', 'blocker': None}
            try:
                execution, digest = _verification_module.execute_verification_plan(
                    plan=plan, repository_cwd=ledger['repository'], permissions=policy['permissions'],
                    timeout_seconds=timeout_seconds, run_directory=run_dir.resolve(), execution_path=execution_path,
                    closure_identity=identity, execution_authorization=policy['execution_authorization'])
                result['execution_sha256'] = digest
                result['status'] = ('not_run' if not execution['outcomes'] else
                                    'passed' if execution['terminal_reason'] == 'complete' else 'failed')
                result['post_workspace'] = _producer_workspace(ledger, inputs)
                if result['post_workspace'] != candidate['workspace']:
                    result['status'] = 'stale'
            except (OSError, ValueError, RuntimeError) as error:
                # No completed record means terminality cannot be inferred. Keep
                # the operation unknown, even for a truthful infrastructure error.
                ledger['actor_blocker'] = str(error) + '; inspect retained check evidence before retry'
                result['blocker'] = ledger['actor_blocker']
                _publish_actor_bytes(path, _canonical_record_bytes(result))
                ledger.setdefault('evidence', {})['verify'] = {
                    'status': 'blocked', 'inputs_sha256': ledger['inputs_sha256'],
                    'candidate_sha256': ledger['candidate_sha256'],
                    'operation_id': operation['operation_id'], 'path': relative}
                _save_actor_ledger(run_dir, ledger)
                return result
            _publish_actor_bytes(path, _canonical_record_bytes(result))
            _publish_check_outcome(run_dir, ledger, operation, result)
            return result
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {'status': 'stale' if 'stale' in str(error).lower() else 'refused', 'reason': str(error)}


def _collection_check_paths(operation):
    identity = operation['operation_id'] + '.rerun'
    return identity, f'collection-checks/{identity}.json', f'collection-checks/{identity}.intent.json'


def _collection_check_unresolved(run_dir, operation):
    if operation['assignment']['stage'] != 'semantic_review':
        return False
    _, result, intent = _collection_check_paths(operation)
    if not (run_dir / intent).exists():
        return False
    try:
        return 'execution_sha256' not in _worker_module.read_json(run_dir / result)
    except (OSError, ValueError):
        return True


def _validate_check_artifacts(run_dir, result, identity):
    raw = (run_dir / result['execution_path']).read_bytes()
    if _sha256_bytes(raw) != result['execution_sha256']:
        raise ValueError('Execution record changed')
    execution = json.loads(raw)
    _state_module.validate_command_execution_record(execution, expected_closure_identity=identity)
    for outcome in execution['outcomes']:
        for stream in ('stdout', 'stderr'):
            if _sha256_bytes((run_dir / outcome[f'{stream}_path']).read_bytes()) != outcome[f'{stream}_sha256']:
                raise ValueError('Execution log changed')
    expected = 'not_run' if not execution['outcomes'] else 'passed' if execution['terminal_reason'] == 'complete' else 'failed'
    if result['status'] != expected:
        raise ValueError('Check disposition contradicts execution')
    return execution


def _collection_launch_context(run_dir, ledger, inputs, operation):
    candidate = _load_current_candidate(run_dir, ledger, inputs)
    evidence = _evidence_view(ledger, 'verify')
    if evidence['status'] != 'passed':
        raise ValueError('Current passed checks required for collection')
    check = _worker_module.read_json(run_dir / evidence['path'])
    verifier = _actor_operation(ledger, evidence['operation_id'])
    if check['assignment'] != verifier['assignment']:
        raise ValueError('Check assignment mismatch')
    _validate_check_artifacts(run_dir, check, _check_closure_identity(ledger, verifier, candidate))
    return {'run_dir': str(run_dir.resolve()), 'controller_path': str(Path(__file__).resolve()),
            'candidate': candidate, 'check_evidence': check,
            'prior_findings': ledger.get('outstanding_findings', []),
            'review_requirements': ['requirements', 'behavior', 'code_quality'],
            'review_workflow': {
                'skill_resolution': 'Use matching project-local .agents/skills installations first; source presence is not availability. Never substitute source or refresh installations. Block unavailable mandatory review capabilities.',
                'collection': 'Fresh independent task-review-discovery gathers evidence without deciding acceptance',
                'separate_stages': ['task-maintainability-review when required', 'task-contract-registry-updater when contracts change', 'task-review-discovery', 'separate task-acceptance-review'],
                'authority': 'Frozen brief, verification and repository instructions determine applicability; collection grants no acceptance or deferral authority'},
            'rerun_callable': 'check_collection(run_dir, assignment, timeout_seconds=...)',
            'rerun_cli': 'check-collection --run-dir RUN --request ASSIGNMENT --timeout-seconds N'}


def _collection_check_context(run_dir, assignment):
    ledger, flow, policy, inputs, operation = _producer_context(run_dir, assignment['operation_id'])
    if not _same_typed_assignment(assignment, operation['assignment']) or assignment['stage'] != 'semantic_review':
        raise ValueError('Exact collector assignment required')
    if _active_actor(ledger) is not operation or operation['state'] not in {'running', 'unknown'}:
        raise ValueError('Only the active launched collector can request reruns')
    observed, _ = _read_actor_observation(_actor_directory(run_dir, operation), operation)
    if not observed.get('thread_id'):
        raise ValueError('Observed collector session required')
    candidate = _load_current_candidate(run_dir, ledger, inputs)
    if assignment['candidate_sha256'] != ledger.get('candidate_sha256'):
        raise ValueError('Collector candidate is stale')
    return ledger, flow, policy, inputs, operation, observed, candidate


def check_collection(run_dir: Path, assignment: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    """Execute one collector-owned full-plan rerun; never launch another actor."""
    if type(timeout_seconds) not in {int, float} or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        return {'status': 'refused', 'reason': 'timeout_seconds must be positive and finite'}
    try:
        with RunCommandLock(run_dir):
            ledger, flow, policy, inputs, operation, observed, candidate = _collection_check_context(run_dir, assignment)
            identity, relative, intent_path = _collection_check_paths(operation)
            checker = dict(operation, operation_id=identity)
            closure = _check_closure_identity(ledger, checker, candidate)
            if (run_dir / relative).exists():
                result = _worker_module.read_json(run_dir / relative)
                if not _same_typed_assignment(result['assignment'], assignment) or result['timeout_seconds'] != timeout_seconds or result['session_id'] != observed['thread_id']:
                    raise ValueError('Collector rerun replay conflict')
                if 'execution_sha256' in result and result['status'] != 'stale':
                    _validate_check_artifacts(run_dir, result, closure)
                return result
            if (run_dir / intent_path).exists():
                return {'status': 'blocked', 'blocker': 'Collection rerun terminality unresolved; inspect retained intent and logs; do not relaunch'}
            check_policy = json.loads(json.dumps(policy))
            check_policy['verification']['authorized_gap'] = None
            if _state_module.flow_step(flow, 'verify')['mode'] == 'targeted':
                check_policy['verification']['repository_gate'] = None
            plan = _verification_module.build_verification_plan({'required_checks': inputs['required_checks']}, check_policy)
            result = {'operation_id': identity, 'assignment': assignment, 'session_id': observed['thread_id'],
                      'candidate_sha256': ledger['candidate_sha256'], 'timeout_seconds': timeout_seconds,
                      'path': relative, 'plan': plan, 'setup': inputs,
                      'execution_path': f'verification/{identity}.turn-001.execution.json',
                      'status': 'blocked', 'blocker': None}
            _publish_actor_bytes(run_dir / intent_path, _canonical_record_bytes(result))
            (run_dir / 'verification').mkdir(exist_ok=True)
            try:
                execution, digest = _verification_module.execute_verification_plan(
                    plan=plan, repository_cwd=ledger['repository'], permissions=policy['permissions'],
                    timeout_seconds=timeout_seconds, run_directory=run_dir.resolve(),
                    execution_path=result['execution_path'], closure_identity=closure,
                    execution_authorization=policy['execution_authorization'])
                result['execution_sha256'] = digest
                result['status'] = 'not_run' if not execution['outcomes'] else 'passed' if execution['terminal_reason'] == 'complete' else 'failed'
                if _producer_workspace(ledger, inputs) != candidate['workspace']:
                    result['status'] = 'stale'
            except (OSError, ValueError, RuntimeError) as error:
                result['blocker'] = str(error) + '; rerun terminality unresolved; inspect retained evidence'
            _publish_actor_bytes(run_dir / relative, _canonical_record_bytes(result))
            return result
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {'status': 'stale' if 'stale' in str(error).lower() else 'refused', 'reason': str(error)}


def _collection_evidence(ledger, operation, status, blocker=None, path=None):
    assignment = operation['assignment']
    ledger.setdefault('evidence', {})['semantic_review'] = {
        'status': status, 'inputs_sha256': assignment['inputs_sha256'],
        'candidate_sha256': assignment['candidate_sha256'],
        'operation_id': operation['operation_id'], 'path': path, 'blocker': blocker}


def _validate_current_collection(run_dir, ledger):
    evidence = ledger.get('evidence', {}).get('semantic_review', {})
    if evidence.get('status') != 'passed':
        raise ValueError('Current successful collection required')
    raw = (run_dir / evidence['path']).read_bytes()
    record = json.loads(raw)
    operation = _actor_operation(ledger, evidence['operation_id'])
    if (_sha256_bytes(raw) != evidence.get('sha256')
            or not _same_typed_assignment(record['assignment'], operation['assignment'])
            or record['status'] != 'passed'
            or any(record['assignment'][key] != ledger[key] for key in ('candidate_sha256', 'inputs_sha256', 'policy_sha256', 'flow_sha256'))):
        raise ValueError('Admitted collection identity is stale or changed')


def _merge_collection_findings(previous, findings, assignment):
    merged = {finding['id']: json.loads(json.dumps(finding)) for finding in previous}
    for finding in findings:
        current = merged.get(finding['id'])
        history = current.get('history', []) if current else []
        disposition = current.get('disposition') if current else None
        if disposition and current and (set(current['evidence']) != set(finding['evidence']) or current['exposure'] != finding['exposure']):
            disposition = {'status': 'reopened', 'previous': disposition,
                           'reason': 'new relevant evidence or changed exposure'}
        snapshot = {**finding, 'operation_id': assignment['operation_id'],
                    'candidate_sha256': assignment['candidate_sha256'], 'disposition': disposition}
        merged[finding['id']] = {**finding, 'disposition': disposition, 'history': history + [snapshot]}
    return list(merged.values())


def _admit_collection(run_dir, ledger, operation, observed, result):
    assignment = operation['assignment']
    inputs = load_frozen_inputs(run_dir, ledger)
    if any(assignment[key] != ledger[key] for key in ('inputs_sha256', 'policy_sha256', 'flow_sha256', 'candidate_sha256')):
        raise ValueError('Collection authority or candidate is stale')
    candidate = _load_current_candidate(run_dir, ledger, inputs)
    producer_sessions = {item.get('transport', {}).get('outcome', {}).get('observed', {}).get('thread_id')
                         for item in ledger['actor_operations'] if item['assignment']['stage'] in {'implement', 'correction'} and item.get('transport', {}).get('outcome')}
    if observed['thread_id'] in producer_sessions:
        raise ValueError('Collection session is not independent of implementation/correction')
    if result['session_id'] != observed['thread_id']:
        raise ValueError('Collection must bind the observed session explicitly')
    if result['readiness'] is not None:
        raise ValueError('Collection cannot supply preflight readiness authority')
    report = result['collection']
    _state_module.validate_collection_report(report)
    _, rerun_path, _ = _collection_check_paths(operation)
    status, blocker = 'passed', None
    if report['rerun_path'] is None:
        status, blocker = 'not_run', 'Missing independent rerun evidence; request fresh collection checks'
    else:
        if report['rerun_path'] != rerun_path:
            raise ValueError('Fresh collector-owned rerun required; historical verifier evidence cannot cover collection')
        rerun = _worker_module.read_json(run_dir / rerun_path)
        if not _same_typed_assignment(rerun['assignment'], assignment) or rerun['session_id'] != observed['thread_id'] or rerun['candidate_sha256'] != ledger['candidate_sha256']:
            raise ValueError('Collector rerun binding mismatch')
        checker = dict(operation, operation_id=rerun['operation_id'])
        _validate_check_artifacts(run_dir, rerun, _check_closure_identity(ledger, checker, candidate))
        status = rerun['status']
        if status != 'passed':
            blocker = 'Independent required check failed; bounded check_failed correction required' if status == 'failed' else 'Required independent checks not run; collect missing evidence'
    if result['status'] != 'complete' or any(item['status'] == 'blocked' for item in report['coverage'].values()):
        status, blocker = 'blocked', 'Review capability or authority unresolved; inspect report and relay blocker in active chat'
    elif status == 'passed' and (report['gaps'] or any(item['status'] != 'passed' for item in report['coverage'].values())):
        status, blocker = 'not_run', 'Required collection coverage gaps; rerun or recollect missing evidence'
    record = {'assignment': assignment, 'observed': observed, 'report': report,
              'status': status, 'blocker': blocker}
    relative = f"collections/{operation['operation_id']}.json"
    _publish_actor_bytes(run_dir / relative, _canonical_record_bytes(record))
    findings = _merge_collection_findings(ledger.get('outstanding_findings', []), report['findings'], assignment)
    ledger['outstanding_findings'] = findings
    _collection_evidence(ledger, operation, status, blocker, relative)
    ledger['evidence']['semantic_review']['sha256'] = _sha256_bytes((run_dir / relative).read_bytes())
    if status == 'failed':
        ledger['correction_request'] = 'check_failed'
    ledger['current_step'] = 'acceptance' if status == 'passed' else 'semantic_review'
    return blocker


def _reservation_context(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    ledger = json.loads((run_dir / "ledger.json").read_text())
    _validate_ledger(ledger)
    flow = _load_flow_authority(run_dir, ledger)
    active = _active_actor(ledger)
    if active:
        assignment = active["assignment"]
        stage = "implement" if assignment["stage"] == "correction" else assignment["stage"]
        mode = _state_module.flow_step(flow, stage)["mode"]
        if assignment["actor"] != flow["actor_levels"].get(mode):
            raise ValueError("Active assignment actor contradicts the frozen flow")
    return ledger, flow


def _active_actor(ledger: dict[str, Any]) -> dict[str, Any] | None:
    return next((operation for operation in ledger.get("actor_operations", [])
                 if operation["state"] != "terminal"), None)


def _current_readiness(ledger: dict[str, Any]) -> bool:
    readiness = ledger.get("readiness")
    if not isinstance(readiness, dict) or readiness.get("status") != "ready":
        return False
    operation = next((item for item in ledger.get("actor_operations", [])
                      if item["operation_id"] == readiness.get("operation_id")), None)
    if operation is None or operation["state"] != "terminal":
        return False
    assignment = operation["assignment"]
    return (
        assignment["stage"] == "preflight"
        and assignment["role"] == "preflight"
        and all(readiness.get(field) == ledger[field] == assignment[field]
                for field in ("inputs_sha256", "policy_sha256", "flow_sha256"))
        and readiness.get("task_id") == assignment["task_id"]
        and readiness.get("task_id") == ledger["selected_task_id"]
        and not any(item["assignment"]["can_repair"] for item in
                    ledger.get("actor_operations", [])[ledger.get("actor_operations", []).index(operation) + 1:])
    )


def _evidence_view(ledger: dict[str, Any], stage: str) -> dict[str, Any]:
    item = dict(ledger.get("evidence", {}).get(stage, {"status": "missing"}))
    if item["status"] != "missing":
        if item.get("inputs_sha256") != ledger["inputs_sha256"] or (
            stage != "preflight" and item.get("candidate_sha256") != ledger.get("candidate_sha256")
        ):
            item["status"] = "stale"
        elif item["status"] == "omitted_by_policy":
            # All actor/check stages in this policy are mandatory.
            item["status"] = "blocked"
    return item


def _reservation_options(ledger: dict[str, Any]) -> tuple[list[str], str | None]:
    active = _active_actor(ledger)
    if active and active['assignment']['stage'] == 'verify':
        return ['check_candidate', 'intervene'], f"check_operation_{active['state']}"
    if active:
        actions = ["launch_operation", "stop_operation", "intervene"] if active["state"] == "reserved" else ["observe_operation", "stop_operation", "intervene"]
        return actions, f"operation_{active['state']}"
    if ledger["state"] not in {"ready", "resumable"}:
        return ["intervene"], "successor_admission_pending"
    correction = ledger.get("correction_request")
    if correction and ledger["correction_cycle"] >= 3:
        return ["intervene"], "corrections_exhausted"
    if correction == "environment_repair":
        return ["reserve:correction"], None
    if correction in {"check_failed", "review_findings"}:
        if not _current_readiness(ledger):
            return ["reserve:preflight"], "current_preflight_readiness_required"
        return ["reserve:correction"], None
    if ledger.get('candidate_path') and not ledger.get('correction_request'):
        if ledger['current_step'] == 'preflight' or not _current_readiness(ledger):
            return ['reserve:preflight'], 'current_preflight_readiness_required'
        actions = ['reserve:verify', 'inspect_candidate', 'intervene']
        if _evidence_view(ledger, 'verify')['status'] == 'passed':
            actions.insert(0, 'reserve:semantic_review')
            if _evidence_view(ledger, 'semantic_review')['status'] == 'passed':
                actions.insert(0, 'reserve:acceptance')
        return actions, None
    stage = ledger["current_step"] or "preflight"
    if stage in {"ready", "preflight"}:
        return ["reserve:preflight"], None
    if stage in {"implement", "correction"}:
        if not _current_readiness(ledger):
            return ["reserve:preflight"], "current_preflight_readiness_required"
        if stage == "implement" and any(
            item["assignment"]["stage"] == "implement"
            for item in ledger.get("actor_operations", [])
        ):
            return ["intervene"], "successor_admission_pending"
        if stage == "correction" and correction not in {"check_failed", "review_findings"}:
            return ["intervene"], "correction_authorization_pending"
        return [f"reserve:{stage}"], None
    # Successors admit these records; reservations consume, never manufacture,
    # eligible prerequisites. Semantic validation remains T-004/T-005 work.
    predecessor = {"verify": "implement", "semantic_review": "verify", "acceptance": "semantic_review"}.get(stage)
    if predecessor:
        if not ledger.get("candidate_sha256") or _evidence_view(ledger, predecessor)["status"] != "passed":
            return ["intervene"], "successor_evidence_required"
        return [f"reserve:{stage}"], None
    return ["intervene"], "successor_completion_pending"


def status_run(run_dir: Path) -> dict[str, Any]:
    """Read one atomic ledger snapshot without advancing state or taking a lock."""
    ledger, flow = _reservation_context(run_dir)
    actions, blocker = _reservation_options(ledger)
    task_id = load_frozen_inputs(run_dir, ledger)["task_id"]
    if ledger.get('candidate_path'):
        try:
            _load_current_candidate(run_dir, ledger, load_frozen_inputs(run_dir, ledger))
        except (ValueError, OSError, KeyError):
            ledger = json.loads(json.dumps(ledger))
            for stage in ('implement', 'verify', 'semantic_review', 'acceptance'):
                if stage in ledger.get('evidence', {}):
                    ledger['evidence'][stage]['status'] = 'stale'
            if not _active_actor(ledger) and blocker != 'corrections_exhausted':
                actions, blocker = ['inspect_candidate', 'intervene'], 'candidate_stale'
        if ledger.get('evidence', {}).get('semantic_review', {}).get('status') == 'passed':
            try:
                _validate_current_collection(run_dir, ledger)
            except (OSError, ValueError, KeyError, TypeError):
                ledger = json.loads(json.dumps(ledger))
                ledger['evidence']['semantic_review']['status'] = 'stale'
                if not _active_actor(ledger):
                    actions, blocker = ['reserve:semantic_review', 'intervene'], 'collection_stale'
    return {
        "status": "ok", "run_id": ledger["run_id"], "task_id": task_id,
        "inputs_sha256": ledger["inputs_sha256"],
        "policy_sha256": ledger["policy_sha256"],
        "flow_revision": ledger["flow_revision"], "flow_sha256": ledger["flow_sha256"],
        "state": ledger["state"], "state_version": ledger["revision"],
        "stage": ledger["current_step"] or "ready",
        "attempts": next(task["attempt_ids"] for task in ledger["tasks"] if task["id"] == task_id),
        "correction_count": ledger["correction_cycle"],
        "candidate_sha256": ledger.get("candidate_sha256"),
        "references": {field: ledger.get(field) for field in ("last_closure_path", "last_verification_path", "last_decision_path", "active_operation_path")},
        "evidence": {stage: _evidence_view(ledger, stage) for stage in
                     ("preflight", "implement", "verify", "semantic_review", "acceptance")},
        "policy_omissions": ["repository_gate"] if _state_module.flow_step(flow, "verify")["mode"] == "targeted" else [],
        "required_evidence": ["preflight", "implement", "verify", "semantic_review", "acceptance"],
        "outstanding_findings": ledger.get("outstanding_findings", []),
        "operation": _active_actor(ledger), "operation_history": ledger.get("actor_operations", []),
        "readiness_current": _current_readiness(ledger),
        "input_revision_history": ledger.get("input_revisions", []),
        "next_actions": actions, "blocker": ledger.get("actor_blocker") if blocker == "operation_unknown" and ledger.get("actor_blocker") else blocker or ledger.get("actor_blocker"),
        "interventions": ledger.get("interventions", []),
        "chat_relay_action": "relay precise blocker in active chat; delivery/response unknown unless recorded" if blocker not in {None, "operation_reserved", "operation_running"} or ledger.get("actor_blocker") else None,
    }


def reserve_operation(
    run_dir: Path, *, expected_version: int, task_id: str, stage: str,
    role: str, operation_key: str, reason: str = "initial",
) -> dict[str, Any]:
    """Reserve only current permitted work. T-003 owns launch/outcome admission."""
    def refuse(code: str, ledger: dict[str, Any] | None = None) -> dict[str, Any]:
        actions, _ = _reservation_options(ledger) if ledger else (["intervene"], None)
        return {"status": "refused", "reason": code, "next_actions": actions,
                "state_version": ledger["revision"] if ledger else None}

    try:
        with RunCommandLock(run_dir):
            ledger, flow = _reservation_context(run_dir)
            if (type(expected_version) is not int or expected_version < 1
                    or not isinstance(operation_key, str) or not operation_key
                    or any(not isinstance(value, str) for value in (task_id, stage, role, reason))):
                return refuse("invalid_request", ledger)
            request = dict(expected_version=expected_version, task_id=task_id,
                           stage=stage, role=role, operation_key=operation_key, reason=reason)
            for operation in ledger.get("actor_operations", []):
                if operation["request"]["operation_key"] == operation_key:
                    if operation["request"] != request:
                        return refuse("operation_key_conflict", ledger)
                    return {"status": "replayed", "assignment": operation["assignment"],
                            "state_version": ledger["revision"]}
            if expected_version != ledger["revision"]:
                return refuse("stale_version", ledger)
            inputs = load_frozen_inputs(run_dir, ledger)
            if stage in {'verify', 'semantic_review', 'acceptance'} and ledger.get('candidate_path'):
                _load_current_candidate(run_dir, ledger, inputs)
                if stage == 'acceptance':
                    _validate_current_collection(run_dir, ledger)
            expected_role = "implementer" if stage == "correction" else _state_module.FLOW_STEP_ROLES.get(stage)
            if task_id != inputs["task_id"] or role != expected_role:
                return refuse("task_or_role_mismatch", ledger)
            actions, blocker = _reservation_options(ledger)
            if f"reserve:{stage}" not in actions:
                return refuse(blocker or "stage_mismatch", ledger)
            is_correction = stage == "correction"
            if (is_correction and reason != ledger.get("correction_request")) or (
                not is_correction and reason not in {"initial", "retry"}
            ):
                return refuse("reason_not_authorized", ledger)
            if stage == "implement" and any(item["assignment"]["stage"] == "implement" for item in ledger.get("actor_operations", [])):
                return refuse("initial_implementation_already_reserved", ledger)
            mode = _state_module.flow_step(flow, "implement" if is_correction else stage)["mode"]
            operation_id = f"operation-{len(ledger.get('actor_operations', [])) + 1:03d}"
            count = ledger["correction_cycle"] + int(is_correction)
            assignment = {
                "run_id": ledger["run_id"], "task_id": task_id,
                "operation_id": operation_id, "operation_key": operation_key,
                "stage": stage, "role": role, "reason": reason,
                "inputs_sha256": ledger["inputs_sha256"], "policy_sha256": ledger["policy_sha256"],
                "flow_sha256": ledger["flow_sha256"], "flow_revision": ledger["flow_revision"],
                "candidate_sha256": ledger.get("candidate_sha256"),
                "correction_count": count, "can_repair": is_correction and reason == "environment_repair",
                "can_change_files": stage in {"implement", "correction"},
                "actor": flow["actor_levels"].get(mode),
                "session_policy": "fresh" if is_correction else None,
            }
            operation = {"operation_id": operation_id, "state": "reserved",
                         "request": request, "assignment": assignment}
            updated = json.loads(json.dumps(ledger))
            updated.setdefault("actor_operations", []).append(operation)
            updated.update(revision=ledger["revision"] + 1, updated_at=_now_iso(),
                           selected_task_id=task_id, current_step=stage,
                           correction_cycle=count,
                           active_operation_path=f"actor_operations/{operation_id}")
            if is_correction:
                updated["correction_request"] = None
            if stage == "preflight" or assignment["can_repair"]:
                updated["readiness"] = None
                updated["actor_blocker"] = None
            _validate_ledger(updated)
            atomic_write_json(run_dir / "ledger.json", updated)
            return {"status": "reserved", "assignment": assignment, "state_version": updated["revision"]}
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {**refuse("authority_or_lock_unavailable"), "detail": str(error)}


def _actor_operation(ledger: dict[str, Any], operation_id: str) -> dict[str, Any]:
    operation = next((item for item in ledger.get("actor_operations", [])
                      if item["operation_id"] == operation_id), None)
    if operation is None:
        raise ValueError("Unknown reserved operation")
    return operation


def _save_actor_ledger(run_dir: Path, ledger: dict[str, Any]) -> None:
    ledger.update(revision=ledger["revision"] + 1, updated_at=_now_iso())
    _validate_ledger(ledger)
    atomic_write_json(run_dir / "ledger.json", ledger)


def _publish_actor_bytes(path: Path, content: bytes) -> None:
    if path.exists():
        if path.read_bytes() != content:
            raise ValueError(f"Conflicting prepared actor record: {path.name}")
        return
    _write_durable_exclusive(path, content)


def _actor_directory(run_dir: Path, operation: dict[str, Any]) -> Path:
    return run_dir / "actors" / operation["operation_id"]


def _actor_prompt(assignment: dict[str, Any], inputs: dict[str, Any], policy: dict[str, Any], collection_context=None) -> str:
    return ("Execute only this frozen assignment. Actor output is a claim, never authority. "
            "Respect frozen run_policy permissions and task scope. Do not commit, change policy, select another task, or edit controller records. "
            "Review roles must not edit implementation. Always use a fresh session.\n"
            "For preflight, check every task-required tool, dependency and installed skill in "
            "this execution environment. Report tools/dependencies/skills arrays of "
            "{name, status: passed|blocked, evidence}; use empty arrays only when no such "
            "prerequisite is required. Report requirements_complete only after checking all "
            "frozen task requirements. Missing prerequisites mean blocked, never ready.\n"
            "Return the assigned result schema, echo the exact assignment and observed "
            "thread.started session_id if known, otherwise null; never invent it. "
            "Collection must call check_collection with its exact assignment, rerun every frozen check, "
            "and report collection {coverage: {requirements, behavior, code_quality}, gaps, findings, rerun_path}. "
            "Coverage values are passed|blocked|not_run with evidence; findings contain id, evidence, requirement, context, exposure. "
            "Report evidence only, never acceptance decisions or new disposition/deferral authority.\n"
            + json.dumps({"assignment": assignment, "frozen_inputs": inputs, "run_policy": policy, "collection_context": collection_context}, sort_keys=True))


def _same_typed_assignment(value: Any, expected: Any) -> bool:
    """Compare to validated ledger authority without Python bool/number coercion."""
    if type(value) is not type(expected):
        return False
    if isinstance(expected, dict):
        return (value.keys() == expected.keys()
                and all(_same_typed_assignment(value[key], item)
                        for key, item in expected.items()))
    return value == expected


def launch_operation(run_dir: Path, assignment: dict[str, Any], *,
                     codex_bin: str = "codex", timeout_seconds: float = 300) -> dict[str, Any]:
    """Start one detached transport supervisor, after durable no-relaunch intent."""
    try:
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("Positive finite timeout required")
        with RunCommandLock(run_dir):
            ledger, _ = _reservation_context(run_dir)
            policy, _, inputs = load_input_authority(run_dir, ledger)
            operation = _actor_operation(ledger, assignment["operation_id"])
            if not _same_typed_assignment(assignment, operation["assignment"]):
                raise ValueError("Launch assignment mismatch")
            if any(assignment[field] != ledger[field] for field in ("inputs_sha256", "policy_sha256", "flow_sha256")):
                raise ValueError("Stale launch assignment; use current frozen authority")
            if assignment["actor"] is None:
                raise ValueError("Verifier uses the successor check pipeline")
            directory = _actor_directory(run_dir, operation)
            config = {"assignment": assignment, "execution_authorization": policy["execution_authorization"],
                      "cwd": policy["repository"], "codex_bin": str(codex_bin),
                      "timeout_seconds": timeout_seconds}
            if operation.get("transport"):
                if _worker_module.read_json(directory / "launch.json") != config:
                    raise ValueError("Launch replay configuration conflict")
                return {"status": "replayed", "operation": operation}
            if operation["state"] != "reserved" or _active_actor(ledger) is not operation:
                raise ValueError("Only the active reserved operation can launch")
            directory.mkdir(parents=True, exist_ok=True)
            content = _canonical_record_bytes(config)
            _publish_actor_bytes(directory / "launch.json", content)
            context = _collection_launch_context(run_dir, ledger, inputs, operation) if assignment['stage'] == 'semantic_review' else None
            prompt = _actor_prompt(assignment, inputs, policy, context).encode()
            _publish_actor_bytes(directory / "prompt.txt", prompt)
            operation["transport"] = {"configuration_sha256": _sha256_bytes(content),
                                      "supervisor_pid": None, "outcome": None}
            # From this point uncertainty is durable. Never relaunch, even if
            # the coordinator dies before Popen or identity publication.
            operation["state"] = "unknown"
            _save_actor_ledger(run_dir, ledger)
            with (directory / "supervisor.stdout.log").open("x") as output, (directory / "supervisor.stderr.log").open("x") as errors:
                supervisor = subprocess.Popen(
                    [sys.executable, str(Path(_worker_module.__file__).resolve()), "actor", "--config", str((directory / "launch.json").resolve())],
                    stdin=subprocess.DEVNULL, stdout=output, stderr=errors, start_new_session=True,
                )
            operation["transport"]["supervisor_pid"] = supervisor.pid
            operation["state"] = "running"
            _save_actor_ledger(run_dir, ledger)
            # Keep the handle until a later observation can reap it in this
            # coordinator; other coordinators rely solely on durable receipts.
            _ACTOR_SUPERVISORS[str(directory.resolve())] = supervisor
            return {"status": "launched", "operation": operation}
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {"status": "refused", "reason": "launch_refused", "detail": str(error),
                "next_actions": ["status", "observe_operation", "intervene"]}


_ACTOR_SUPERVISORS: dict[str, subprocess.Popen] = {}


def _validate_observed_result(assignment: dict[str, Any], observed: dict[str, Any], result: dict[str, Any]) -> None:
    expected = {"assignment", "session_id", "status", "summary", "readiness"}
    if assignment["stage"] == "semantic_review":
        expected.add("collection")
    if set(result) != expected:
        raise ValueError("Malformed actor result")
    if not _same_typed_assignment(result["assignment"], assignment):
        raise ValueError("Result assignment mismatch")
    if not observed.get("thread_id") or result["session_id"] not in (None, observed["thread_id"]):
        raise ValueError("Result session mismatch or missing observed session")
    if result["status"] not in {"complete", "blocked", "failed", "needs_input"} or not isinstance(result["summary"], str):
        raise ValueError("Invalid result status/summary")


def _validate_readiness(readiness: dict[str, Any]) -> None:
    if not isinstance(readiness, dict) or set(readiness) != {"status", "requirements_complete", "tools", "dependencies", "skills"}:
        raise ValueError("Incomplete readiness payload")
    if readiness["status"] != "ready" or readiness["requirements_complete"] is not True:
        raise ValueError("Preflight is not complete and ready")
    for category in ("tools", "dependencies", "skills"):
        items = readiness[category]
        if not isinstance(items, list):
            raise ValueError(f"Missing prerequisite inventory: {category}")
        for item in items:
            if not isinstance(item, dict) or set(item) != {"name", "status", "evidence"}:
                raise ValueError(f"Malformed prerequisite: {category}")
            if not isinstance(item["name"], str) or not item["name"] or not isinstance(item["evidence"], str) or not item["evidence"]:
                raise ValueError(f"Missing prerequisite evidence: {category}")
            if item["status"] != "passed":
                raise ValueError(f"Missing {category} prerequisite: {item['name']}; {item['evidence']}")


def _admit_actor_outcome(run_dir: Path, ledger: dict[str, Any], operation: dict[str, Any], observed: dict[str, Any], result: dict[str, Any]) -> str | None:
    """Single admission extension point; T-005 extends acceptance here."""
    assignment = operation["assignment"]
    try:
        if observed.get("exit_code") != 0 or observed.get("stop_requested") or observed.get("attempt_outcome") in {"timed_out", "interrupted"}:
            raise ValueError("Actor failed, stopped or interrupted")
        _validate_observed_result(assignment, observed, result)
        if assignment["stage"] == "semantic_review":
            return _admit_collection(run_dir, ledger, operation, observed, result)
        if assignment["stage"] != "preflight":
            return None  # Implementation and future acceptance remain raw claims.
        if result["status"] != "complete":
            raise ValueError(f"Preflight {result['status']}: {result['summary']}")
        if any(assignment[field] != ledger[field] for field in ("inputs_sha256", "policy_sha256", "flow_sha256")):
            raise ValueError("Stale preflight authority")
        _validate_readiness(result["readiness"])
        ledger["readiness"] = {field: assignment[field] for field in
                               ("task_id", "operation_id", "inputs_sha256", "policy_sha256", "flow_sha256")}
        ledger["readiness"]["status"] = "ready"
        ledger["current_step"] = "implement"
        ledger.setdefault("evidence", {})["preflight"] = {
            "status": "passed", "inputs_sha256": assignment["inputs_sha256"],
            "operation_id": assignment["operation_id"],
        }
        return None
    except (ValueError, KeyError, TypeError) as error:
        return str(error)


def _read_actor_observation(directory: Path, operation: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Only the adapter's exclusive terminal receipt proves a reaped child."""
    terminal = directory / "result.state.json"
    path = terminal if terminal.exists() else directory / "state.json"
    if not path.exists():
        return {}, False
    try:
        observed = _worker_module.read_json(path)
    except json.JSONDecodeError:
        # An exclusive receipt path can be visible before its bytes are complete.
        # Missing terminal proof remains unresolved; never admit or relaunch.
        return {}, False
    transport = operation["transport"]
    if not _same_typed_assignment(observed.get("assignment"), operation["assignment"]) or observed.get("configuration_sha256") != transport["configuration_sha256"]:
        raise ValueError("Transport observation binding mismatch")
    terminality = (terminal.exists() and observed.get("terminal_observed") is True
                   and observed.get("group_absent") is True)
    return observed, terminality


def _open_actor_intervention(ledger: dict[str, Any], operation: dict[str, Any], blocker: str) -> None:
    record = {"key": operation["operation_id"] + ":" + operation["state"],
              "blocker": blocker, "evidence": "actors/" + operation["operation_id"],
              "operation_id": operation["operation_id"],
              "required_action": "Coordinator inspect retained evidence; resolve liveness or obtain explicit repair authority before retry",
              "event": "opened", "text": "Relay and response unknown; relay in active coordinator chat"}
    records = ledger.setdefault("interventions", [])
    if record not in records:
        records.append(record)


def _publish_actor_outcome(run_dir: Path, ledger: dict[str, Any], operation: dict[str, Any],
                           observed: dict[str, Any]) -> dict[str, Any]:
    directory = _actor_directory(run_dir, operation)
    try:
        result = _worker_module.read_json(directory / "result.json")
        blocker = _admit_actor_outcome(run_dir, ledger, operation, observed, result)
    except (OSError, ValueError) as error:
        blocker = f"Missing or malformed actor result: {error}"
    operation["transport"]["outcome"] = {
        "observed": observed, "blocker": blocker,
        "raw_result_path": str(directory / "result.json"),
        "terminal_path": str(directory / "result.state.json"),
    }
    operation["state"] = "terminal"
    ledger["active_operation_path"] = None
    ledger["actor_blocker"] = blocker
    if blocker:
        _open_actor_intervention(ledger, operation, blocker)
        if operation["assignment"]["stage"] == "semantic_review":
            evidence = ledger.setdefault("evidence", {}).get("semantic_review", {})
            if evidence.get("operation_id") != operation["operation_id"]:
                _collection_evidence(ledger, operation, "stale" if "stale" in blocker.lower() else "missing" if not (directory / "result.json").exists() else "blocked", blocker)
        if operation["assignment"]["stage"] == "preflight":
            ledger["readiness"] = None
            ledger.setdefault("evidence", {})["preflight"] = {
                "status": "blocked", "inputs_sha256": operation["assignment"]["inputs_sha256"],
                "operation_id": operation["operation_id"],
            }
    _save_actor_ledger(run_dir, ledger)
    return {"status": "terminal", "operation": operation, "blocker": blocker}


def observe_operation(run_dir: Path, operation_id: str) -> dict[str, Any]:
    """Collect once, retaining invalid raw output without granting eligibility."""
    try:
        with RunCommandLock(run_dir):
            ledger, _ = _reservation_context(run_dir)
            operation = _actor_operation(ledger, operation_id)
            if operation["state"] == "terminal":
                return {"status": "replayed", "operation": operation}
            if not operation.get("transport"):
                return {"status": "reserved", "operation": operation}
            directory = _actor_directory(run_dir, operation)
            handle = _ACTOR_SUPERVISORS.get(str(directory.resolve()))
            if handle is not None and handle.poll() is not None:
                del _ACTOR_SUPERVISORS[str(directory.resolve())]
            observed, terminal = _read_actor_observation(directory, operation)
            if not terminal:
                # Alive is not terminal; absence without a receipt is unknown,
                # and may hide a surviving child. No automatic retry.
                pid = operation["transport"]["supervisor_pid"]
                alive = pid is not None and _worker_module.process_liveness(pid) == "alive"
                state = "running" if alive and operation["state"] == "running" else "unknown"
                changed = operation["state"] != state
                operation["state"] = state
                before = len(ledger.get("interventions", []))
                if state == "unknown":
                    _open_actor_intervention(ledger, operation, "No terminal receipt; actor liveness unresolved; retry and another writer prohibited")
                if changed or len(ledger.get("interventions", [])) != before:
                    _save_actor_ledger(run_dir, ledger)
                return {"status": state, "operation": operation, "observation": observed,
                        "next_actions": ["observe_operation", "intervene"]}
            if _collection_check_unresolved(run_dir, operation):
                operation["state"] = "unknown"
                _, rerun_path, _ = _collection_check_paths(operation)
                blocker = 'Collection rerun terminality unresolved; inspect collection-checks intent and logs before retry'
                try:
                    blocker = _worker_module.read_json(run_dir / rerun_path).get('blocker') or blocker
                except (OSError, ValueError):
                    pass
                ledger['actor_blocker'] = blocker
                _collection_evidence(ledger, operation, 'blocked', blocker, rerun_path)
                _open_actor_intervention(ledger, operation, blocker)
                _save_actor_ledger(run_dir, ledger)
                return {"status": "unknown", "operation": operation, "next_actions": ["intervene"]}
            if handle is not None:
                try:
                    handle.wait(timeout=1)
                    _ACTOR_SUPERVISORS.pop(str(directory.resolve()), None)
                except subprocess.TimeoutExpired:
                    pass
            return _publish_actor_outcome(run_dir, ledger, operation, observed)
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {"status": "refused", "reason": "observation_refused", "detail": str(error)}


def stop_operation(run_dir: Path, operation_id: str) -> dict[str, Any]:
    """Persist a stop request; the adapter, never a reused PID, receives it."""
    try:
        with RunCommandLock(run_dir):
            ledger, _ = _reservation_context(run_dir)
            operation = _actor_operation(ledger, operation_id)
            if operation["state"] == "terminal":
                return {"status": "replayed", "operation": operation}
            directory = _actor_directory(run_dir, operation)
            directory.mkdir(parents=True, exist_ok=True)
            _publish_actor_bytes(directory / "stop.request.json",
                                     _canonical_record_bytes({"operation_id": operation_id, "requested": True}))
            if not operation.get("transport"):
                operation["state"] = "terminal"
                ledger["active_operation_path"] = None
                ledger["actor_blocker"] = "Stopped before launch; reserve fresh preflight or intervene"
                _save_actor_ledger(run_dir, ledger)
                return {"status": "terminal", "operation": operation}
        return observe_operation(run_dir, operation_id)
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {"status": "refused", "reason": "stop_refused", "detail": str(error)}


def record_intervention(run_dir: Path, request: dict[str, Any]) -> dict[str, Any]:
    """Retain active-chat relay/response observations; this grants no authority."""
    try:
        with RunCommandLock(run_dir):
            ledger, _ = _reservation_context(run_dir)
            required = {"key", "blocker", "evidence", "operation_id", "required_action", "event", "text"}
            if set(request) != required or any(not isinstance(request[f], str) for f in required):
                raise ValueError("Incomplete intervention request")
            if any(not request[f] for f in ("key", "blocker", "evidence", "required_action")):
                raise ValueError("Precise blocker/evidence/owner action required")
            if request["event"] not in {"opened", "relayed", "response"}:
                raise ValueError("Unknown chat observation event")
            if request["operation_id"]:
                _actor_operation(ledger, request["operation_id"])
            records = ledger.setdefault("interventions", [])
            if request in records:
                return {"status": "replayed", "interventions": records}
            if any(r["key"] == request["key"] and any(r[f] != request[f] for f in
                   ("blocker", "evidence", "operation_id", "required_action")) for r in records):
                raise ValueError("Intervention key conflict")
            records.append(request)
            _save_actor_ledger(run_dir, ledger)
            return {"status": "recorded", "interventions": records}
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {"status": "refused", "reason": "intervention_refused", "detail": str(error)}


def revise_inputs(run_dir: Path, request: dict[str, Any]) -> dict[str, Any]:
    """Publish explicitly owner-authorized inputs at an idle task boundary.

    The caller is responsible for obtaining the owner response; actor prose is
    not an authorization object. A bundle is immutable preparation. Only the
    atomic ledger replacement makes it current, including its replay receipt.
    """
    ledger = None
    publishing = False

    def refuse(reason: str, detail: str | None = None) -> dict[str, Any]:
        result = {"status": "refused", "reason": reason,
                  "state_version": ledger["revision"] if ledger else None,
                  "next_actions": ["intervene"]}
        if detail is not None:
            result["detail"] = detail
        return result

    try:
        # Detach caller-owned objects before validation, hashing or persistence.
        request = json.loads(json.dumps(request))
        _state_module.validate_input_revision_request(request)
    except (ValueError, KeyError, TypeError) as error:
        return refuse("invalid_revision_request", str(error))
    try:
        with RunCommandLock(run_dir):
            ledger, _ = _reservation_context(run_dir)
            for receipt in ledger.get("input_revisions", []):
                if receipt["request"]["revision_key"] == request["revision_key"]:
                    if receipt["request"] != request:
                        return refuse("revision_key_conflict")
                    return {"status": "replayed", "state_version": ledger["revision"],
                            "revision_state_version": receipt["state_version"],
                            "inputs_sha256": receipt["inputs_sha256"], "revision_path": receipt["path"]}
            if request["expected_version"] != ledger["revision"]:
                return refuse("stale_version")
            task_id = load_frozen_inputs(run_dir, ledger)["task_id"]
            if request["task_id"] != task_id:
                return refuse("task_mismatch")
            if task_id in ledger["completed_task_ids"] or any(task["state"] == "accepted" for task in ledger["tasks"]):
                return refuse("task_completed")
            active = _active_actor(ledger)
            if active:
                return refuse(f"operation_{active['state']}")
            if ledger["active_attempt_id"] or ledger["active_operation_path"] or ledger["state"] in {"running", "finalizing"}:
                return refuse("operation_active_or_unknown")
            # An interrupted legacy flow change must be resolved explicitly.
            _, _, pending_flow = _load_flow_authority_state(run_dir, ledger)
            if pending_flow:
                return refuse("pending_flow_revision")

            payload = request["payload"]
            policy, manifest = payload["policy"], payload["manifest"]
            if (policy["run_id"] != ledger["run_id"] or policy["task_ids"] != [task_id]
                    or Path(policy["repository"]).resolve() != Path(ledger["repository"]).resolve()):
                return refuse("run_task_or_repository_mismatch")
            validated = validate_task_manifest(policy, manifest, Path(ledger["repository"]))
            if validated["completed_task_ids"] != ledger["completed_task_ids"]:
                return refuse("completion_history_mismatch")
            selected = next(task for task in manifest["tasks"] if task["id"] == task_id)
            policy_digest = sha256_text(canonical_json(policy))
            manifest_digest = sha256_text(canonical_json(manifest))
            inputs = {"version": 1, "task_id": task_id, "revision_key": request["revision_key"],
                      "policy_sha256": policy_digest, "manifest_sha256": manifest_digest,
                      "allowed_paths": selected["allowed_paths"],
                      "required_checks": selected.get("required_checks", []), "documents": {}}
            for name, content in payload["documents"].items():
                source = selected["brief_path"] if name == "brief" else str(Path(selected["brief_path"]).with_name("verification.md"))
                inputs["documents"][name] = {"source_path": source, "content": content,
                                             "sha256": _sha256_bytes(content.encode("utf-8"))}
            inputs_digest = _sha256_bytes(_canonical_record_bytes(inputs))
            bundle_bytes = _canonical_record_bytes({"version": 1, "request": request, "inputs": inputs})
            history = ledger.get("input_revisions", [])
            relative = f"input-revisions/revision-{len(history) + 1:03d}.json"
            receipt = {"request": request, "path": relative, "sha256": _sha256_bytes(bundle_bytes),
                       "inputs_sha256": inputs_digest, "state_version": ledger["revision"] + 1,
                       "previous": {key: value for key, value in ledger.items() if key != "input_revisions"}}
            updated = json.loads(json.dumps(ledger))
            flow_digest = _sha256_bytes(_canonical_flow_bytes(resolve_flow_profile(policy)))
            updated.update(revision=receipt["state_version"], updated_at=_now_iso(),
                           inputs_sha256=inputs_digest, policy_sha256=policy_digest,
                           manifest_sha256=manifest_digest, policy_path=relative, manifest_path=relative,
                           flow_path=relative, flow_sha256=flow_digest,
                           flow_revision=ledger["flow_revision"] + int(flow_digest != ledger["flow_sha256"]),
                           input_revisions=[*history, receipt], state="ready", selected_task_id=task_id,
                           active_attempt_id=None, active_operation_path=None, current_step="preflight",
                           readiness=None, candidate_sha256=None, correction_request=None,
                           last_closure_path=None, last_closure_sha256=None,
                           last_verification_path=None, last_decision_path=None)
            # Task projection changes, but implementation history and count do not.
            task = validated["task_entries"][0]
            task.update(state="ready", attempt_ids=ledger["tasks"][0]["attempt_ids"])
            updated["tasks"] = [task]
            _validate_ledger(updated)
            path = run_dir / relative
            if path.exists():
                if path.read_bytes() != bundle_bytes:
                    return refuse("pending_revision_conflict")
            else:
                publishing = True
                _write_durable_exclusive(path, bundle_bytes)
            publishing = True
            atomic_write_json(run_dir / "ledger.json", updated)
            return {"status": "revised", "state_version": updated["revision"],
                    "revision_state_version": updated["revision"],
                    "inputs_sha256": inputs_digest, "revision_path": relative}
    except (ValueError, OSError, KeyError, TypeError) as error:
        if publishing:
            return {"status": "refused", "reason": "revision_publication_uncertain",
                    "state_version": None, "next_actions": ["intervene"],
                    "detail": f"{error}. Read status and retry the exact original revision request."}
        return refuse("authority_or_lock_unavailable", str(error))


def _cli_actor(args: Any) -> int:
    run_dir = Path(args.run_dir).resolve()
    if args.command == "launch":
        result = launch_operation(run_dir, _worker_module.read_json(Path(args.request)),
                                  codex_bin=args.codex_bin, timeout_seconds=args.timeout_seconds)
    elif args.command == "intervene":
        result = record_intervention(run_dir, _worker_module.read_json(Path(args.request)))
    else:
        handler = observe_operation if args.command == "observe" else stop_operation
        result = handler(run_dir, args.operation_id)
    print(json.dumps(result, sort_keys=True))
    return int(result["status"] == "refused")


def _cli_revise_inputs(args: Any) -> int:
    result = revise_inputs(Path(args.run_dir), json.loads(Path(args.request).read_text()))
    print(json.dumps(result, sort_keys=True))
    return 1 if result["status"] == "refused" else 0


def _cli_status(args: Any) -> int:
    print(json.dumps(status_run(Path(args.run_dir).resolve()), sort_keys=True))
    return 0


def _cli_reserve(args: Any) -> int:
    result = reserve_operation(Path(args.run_dir).resolve(), expected_version=args.expected_version,
                               task_id=args.task_id, stage=args.stage, role=args.role,
                               operation_key=args.operation_key, reason=args.reason)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] != "refused" else 1


def _cli_run_next(args: Any) -> int:
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds <= 0:
        raise ValueError("timeout must be greater than zero")
    result = status_run(Path(args.run_dir).resolve())
    print(json.dumps({"status": "pending", "task_id": result["task_id"],
                      "current_step": result["stage"], "reason": result["blocker"] or "successor_launch_pending",
                      "next_actions": result["next_actions"]}, sort_keys=True))
    return 0


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

    runnext_parser = subparsers.add_parser("run-next", help="Report pending successor launch work")
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

    revise_parser = subparsers.add_parser(
        "revise-flow", help="Publish a flow revision at a safe task boundary"
    )
    revise_parser.add_argument("--run-dir", required=True)
    revise_parser.add_argument("--flow", required=True)
    revise_parser.set_defaults(handler=_cli_revise_flow)

    status_parser = subparsers.add_parser("status", help="Read current task and operation status")
    status_parser.add_argument("--run-dir", required=True)
    status_parser.set_defaults(handler=_cli_status)
    reserve_parser = subparsers.add_parser("reserve", help="Reserve one permitted operation")
    reserve_parser.add_argument("--run-dir", required=True)
    reserve_parser.add_argument("--expected-version", type=int, required=True)
    for field in ("task-id", "stage", "role", "operation-key"):
        reserve_parser.add_argument(f"--{field}", required=True)
    reserve_parser.add_argument("--reason", default="initial")
    reserve_parser.set_defaults(handler=_cli_reserve)
    inputs_parser = subparsers.add_parser("revise-inputs", help="Publish an explicit owner-authorized input revision")
    inputs_parser.add_argument("--run-dir", required=True)
    inputs_parser.add_argument("--request", required=True, help="JSON request including bound owner response")
    inputs_parser.set_defaults(handler=_cli_revise_inputs)
    for command in ("launch", "observe", "stop", "intervene"):
        actor_parser = subparsers.add_parser(command)
        actor_parser.add_argument("--run-dir", required=True)
        if command in {"launch", "intervene"}:
            actor_parser.add_argument("--request", required=True)
        else:
            actor_parser.add_argument("--operation-id", required=True)
        if command == "launch":
            actor_parser.add_argument("--codex-bin", default="codex")
            actor_parser.add_argument("--timeout-seconds", type=float, default=300)
        actor_parser.set_defaults(handler=_cli_actor)
    for command in ('inspect-candidate', 'check-candidate', 'check-collection'):
        producer = subparsers.add_parser(command)
        producer.add_argument('--run-dir', required=True)
        if command == 'inspect-candidate':
            producer.add_argument('--operation-id', required=True)
        else:
            producer.add_argument('--request', required=True)
            producer.add_argument('--timeout-seconds', type=float, required=True)
        producer.set_defaults(handler=_cli_producer)
    return parser


def _cli_producer(args):
    run_dir = Path(args.run_dir).resolve()
    if args.command == 'inspect-candidate':
        result = inspect_candidate(run_dir, args.operation_id)
    else:
        runner = check_collection if args.command == 'check-collection' else check_candidate
        result = runner(run_dir, _worker_module.read_json(Path(args.request)), timeout_seconds=args.timeout_seconds)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] in {'passed', 'failed', 'stale'} else 1


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


def _legacy_run_next(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    import argparse
    import codex_worker
    if args.timeout_seconds <= 0:
        raise ValueError("timeout must be greater than zero")
    run_dir = Path(args.run_dir).resolve()
    preliminary_ledger = json.loads((run_dir / "ledger.json").read_text())
    _validate_ledger(preliminary_ledger)
    _load_flow_authority(run_dir, preliminary_ledger)
    lock = RunCommandLock(run_dir)
    lock.acquire()
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    _validate_ledger(ledger)
    if ledger.get("input_revisions"):
        raise ValueError("Revised inputs require successor actor admission; legacy launch is unavailable")
    policy, manifest, _ = load_input_authority(run_dir, ledger)
    validate_run_policy(policy)

    # Validate persisted digests
    persisted_policy = json.loads((run_dir / "run-policy.json").read_text())
    if sha256_text(canonical_json(persisted_policy)) != ledger["policy_sha256"]:
        raise ValueError("Persisted policy digest mismatch")
    persisted_manifest = json.loads((run_dir / "task-manifest.json").read_text())
    if sha256_text(canonical_json(persisted_manifest)) != ledger["manifest_sha256"]:
        raise ValueError("Persisted manifest digest mismatch")
    flow, flow_authority, _ = _load_flow_authority_state(run_dir, ledger)
    if ledger["state"] != "ready":
        raise ValueError(f"Cannot select task from state '{ledger['state']}'")

    cursor_action = None
    if ledger["selected_task_id"] is None:
        task = select_task(ledger, policy)
        selected_cursor = transition_flow_cursor(
            flow,
            {"current_step": None, "correction_cycle": 0},
            "select",
        )
        if selected_cursor["current_step"] != "implement":
            pending = _update_ledger_locked(
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
            print(json.dumps({
                "status": "pending",
                "task_id": task["id"],
                "current_step": pending["current_step"],
                "reason": "no MVP adapter owns the current flow step",
            }, sort_keys=True))
            return 0
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
            print(json.dumps({
                "status": "pending",
                "task_id": task["id"],
                "current_step": ledger["current_step"],
                "reason": "no MVP adapter owns the current flow step",
            }, sort_keys=True))
            return 0

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

    # Capture task baseline
    attempt_number = 1
    attempts_dir = run_dir / "attempts"
    while (attempts_dir / f"attempt-{attempt_number:03d}").exists():
        attempt_number += 1
    task_baseline_ref = f"task-{attempt_number:03d}.json"
    task_baseline_data = _git_module.capture_task_baseline(repo)
    task_baseline_digest = sha256_text(canonical_json(task_baseline_data))
    atomic_write_json(run_dir / "baselines" / task_baseline_ref, task_baseline_data)

    # Use the approved snapshot, never reload mutable task documents.
    inputs = load_frozen_inputs(run_dir, ledger)
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
    attempt_record = build_attempt_record(
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
        "--codex-bin", args.codex_bin,
        "--timeout-seconds", str(args.timeout_seconds),
        "--sandbox", policy["permissions"]["sandbox"],
        "--model", attempt_record["model"],
        "--effort", attempt_record["effort"],
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
        "current_step": "implement",
        "active_attempt_id": attempt_id,
        "selected_task_baseline_ref": task_baseline_ref,
        "selected_task_baseline_digest": task_baseline_digest,
        "tasks": running_tasks,
    }, expected_revision=ledger["revision"], flow=flow, cursor_action=cursor_action)
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
            "current_step": None,
            "correction_cycle": 0,
            "tasks": stopped_tasks,
        }, expected_revision=ledger["revision"], cursor_action="task_boundary")
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
        "attempt_record_sha256": _sha256_bytes(
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


def _cli_revise_flow(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    result = revise_flow(
        Path(args.run_dir).resolve(),
        Path(args.flow).resolve(),
    )
    print(json.dumps(result, sort_keys=True))
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "refused", "reason": str(error), "next_actions": ["intervene"]}, sort_keys=True), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
