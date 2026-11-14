"""Initialize runs and load or revise frozen input and flow authority.

Public operations own initialization, safe-boundary flow revision, validated run
context loading and legacy ledger updates. Mutation commands retain their lock
and publication sequence here. Actor scheduling and input replacement live elsewhere.
Dependencies: flow/run policy, manifest and ledger rules, serialization, Git,
storage and shared run records.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from . import run_records
from . import flow_policy
from . import ledger as ledger_rules
from . import record_serialization
from . import run_policy
from . import task_manifest
from . import controller_git as git
from . import run_storage as storage


def persist_run_policy(path: Path, policy: dict[str, Any]) -> str:
    run_policy.validate_run_policy(policy)
    serialized = json.dumps(policy, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        stream.write(serialized)
    return record_serialization.sha256_text(record_serialization.canonical_json(policy))


def canonical_flow_bytes(flow: dict[str, Any]) -> bytes:
    flow_policy.validate_flow_profile(flow)
    return (record_serialization.canonical_json(flow) + "\n").encode()


def load_input_authority(run_dir: Path, ledger: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Resolve all current inputs from one ledger snapshot and immutable bundle."""
    action = "Initialize a new run using reviewed current inputs."
    revisions = ledger.get("input_revisions", [])
    if revisions:
        ledger_rules.validate_input_revisions(ledger)
        receipt = revisions[-1]
        raw = (run_dir / receipt["path"]).read_bytes()
        if run_records.sha256_bytes(raw) != receipt["sha256"]:
            raise ValueError("Persisted input revision digest mismatch")
        bundle = json.loads(raw)
        if bundle["request"] != receipt["request"]:
            raise ValueError("Persisted input revision request mismatch")
        policy = bundle["request"]["payload"]["policy"]
        manifest = bundle["request"]["payload"]["manifest"]
        inputs = bundle["inputs"]
        inputs_raw = storage.canonical_record_bytes(inputs)
    else:
        if ledger["policy_path"] != "run-policy.json" or ledger["manifest_path"] != "task-manifest.json":
            raise ValueError("Persisted authority path mismatch")
        policy = json.loads((run_dir / ledger["policy_path"]).read_text())
        manifest = json.loads((run_dir / ledger["manifest_path"]).read_text())
        inputs_raw = (run_dir / "inputs.json").read_bytes()
        inputs = json.loads(inputs_raw)
    try:
        run_policy.validate_run_policy(policy)
        if "inputs_sha256" not in ledger:
            raise ValueError("missing frozen task inputs")
    except ValueError as error:
        raise ValueError(f"Incompatible frozen run: {error}. {action}") from error
    if record_serialization.sha256_text(record_serialization.canonical_json(policy)) != ledger["policy_sha256"]:
        raise ValueError("Persisted policy digest mismatch")
    if record_serialization.sha256_text(record_serialization.canonical_json(manifest)) != ledger["manifest_sha256"]:
        raise ValueError("Persisted manifest digest mismatch")
    if run_records.sha256_bytes(inputs_raw) != ledger["inputs_sha256"]:
        raise ValueError("Persisted task input digest mismatch")
    if inputs["task_id"] != policy["task_ids"][0]:
        raise ValueError("Frozen task inputs contradict policy")
    if policy["run_id"] != ledger["run_id"] or Path(policy["repository"]).resolve() != Path(ledger["repository"]).resolve():
        raise ValueError("Persisted run/repository identity mismatch")
    return policy, manifest, inputs


def load_frozen_inputs(run_dir: Path, ledger: dict[str, Any]) -> dict[str, Any]:
    """Read approved bytes only; mutable repository sources are not authority."""
    return load_input_authority(run_dir, ledger)[2]


def load_flow_authority_state(
    run_dir: Path, ledger: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
    policy, _, _ = load_input_authority(run_dir, ledger)
    revision = ledger["flow_revision"]
    if ledger.get("input_revisions"):
        flow = flow_policy.resolve_flow_profile(policy)
        if run_records.sha256_bytes(canonical_flow_bytes(flow)) != ledger["flow_sha256"]:
            raise ValueError("Persisted revised flow digest mismatch")
        flow_policy.validate_flow_cursor(flow, {field: ledger[field] for field in ("current_step", "correction_cycle")})
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
            flow_policy.validate_flow_profile(revision_flow)
        except ValueError as error:
            raise ValueError(
                f"Incompatible frozen flow: {error}. "
                "Initialize a new run using reviewed current inputs."
            ) from error
        if flow_raw != canonical_flow_bytes(revision_flow):
            raise ValueError("Persisted flow bytes are not canonical")
        flow_digest = run_records.sha256_bytes(flow_raw)
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
        flow_policy.validate_flow_profile(candidate_flow)
        if candidate_raw != canonical_flow_bytes(candidate_flow):
            raise ValueError("Uncommitted flow revision bytes are not canonical")
        candidate_digest = run_records.sha256_bytes(candidate_raw)
        candidate = {
            "flow": candidate_flow,
            "flow_bytes": candidate_raw,
            "flow_sha256": candidate_digest,
        }

    current = ledger["current_step"]
    flow_policy.validate_flow_cursor(
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


def load_flow_authority(run_dir: Path, ledger: dict[str, Any]) -> dict[str, Any]:
    flow, _, _ = load_flow_authority_state(run_dir, ledger)
    return flow


def init_run(
    run_dir: Path,
    policy_path: Path,
    manifest_path: Path,
    repository: Path,
) -> dict[str, Any]:
    """Initialize an immutable run from validated policy and manifest."""
    policy = json.loads(policy_path.read_text())
    run_policy.validate_run_policy(policy)
    flow = flow_policy.resolve_flow_profile(policy)
    manifest = json.loads(manifest_path.read_text())

    # Resolve and verify repository is Git top-level
    resolved_repo = repository.resolve()
    try:
        actual_top = git.repository_top_level(resolved_repo)
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
    validated = task_manifest.validate_task_manifest(policy, manifest, resolved_repo)

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
            "content": raw.decode("utf-8"), "sha256": run_records.sha256_bytes(raw),
        }
    inputs["allowed_paths"] = selected["allowed_paths"]
    inputs["required_checks"] = selected.get("required_checks", [])
    inputs["required_reviews"] = selected.get("required_reviews", [])
    inputs_bytes = storage.canonical_record_bytes(inputs)

    # Enforce run directory is outside the repository
    if run_dir.resolve().is_relative_to(resolved_repo):
        raise ValueError(
            f"Run directory {run_dir} must be outside the repository {resolved_repo}"
        )

    # Capture baseline
    baseline = git.capture_task_baseline(resolved_repo)
    baseline_ref = f"run-initial.json"
    baseline_path = run_dir / "baselines" / baseline_ref

    # Build temporary directory and atomically publish
    temp_dir = run_dir.parent / f".tmp-run-{run_dir.name}-{hashlib.sha256(str(run_dir.name).encode()).hexdigest()[:8]}"
    try:
        # Copy canonical policy and manifest
        policy_digest = persist_run_policy(temp_dir / "run-policy.json", policy)
        storage.write_durable_exclusive(temp_dir / "inputs.json", inputs_bytes)
        flow_relative = "flows/flow-001.json"
        flow_bytes = canonical_flow_bytes(flow)
        flow_path = temp_dir / flow_relative
        flow_path.parent.mkdir()
        with flow_path.open("xb") as stream:
            stream.write(flow_bytes)
        flow_digest = run_records.sha256_bytes(flow_bytes)
        manifest_content = manifest_path.read_text()
        manifest_digest = record_serialization.sha256_text(record_serialization.canonical_json(json.loads(manifest_content)))
        (temp_dir / "task-manifest.json").write_text(manifest_content)
        manifest_digest = record_serialization.sha256_text(record_serialization.canonical_json(manifest))

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
            "created_at": run_records.now_iso(),
            "updated_at": run_records.now_iso(),
            "revision": 1,
            "flow_revision": 1,
            "flow_path": flow_relative,
            "flow_sha256": flow_digest,
            "inputs_sha256": run_records.sha256_bytes(inputs_bytes),
            "policy_path": "run-policy.json",
            "policy_sha256": policy_digest,
            "manifest_path": "task-manifest.json",
            "manifest_sha256": manifest_digest,
            "initial_baseline_path": str(baseline_ref),
            "initial_baseline_digest": record_serialization.sha256_text(
                record_serialization.canonical_json(baseline_data)
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
        ledger_rules.validate_ledger(ledger)
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


def update_ledger_locked(
    run_dir: Path, updater: dict[str, Any], *, expected_revision: int,
    closure_decision: dict[str, Any] | None = None,
    flow: dict[str, Any] | None = None, cursor_action: str | None = None,
    cursor_result: str | None = None,
) -> dict[str, Any]:
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    load_flow_authority(run_dir, ledger)
    if run_records.active_actor(ledger):
        raise ValueError("Active actor operation blocks legacy ledger mutation")
    ledger = ledger_rules.apply_ledger_update(
        ledger, updater, run_records.now_iso(), expected_revision=expected_revision,
        closure_decision=closure_decision,
        flow=flow, cursor_action=cursor_action, cursor_result=cursor_result,
    )
    storage.atomic_write_json(ledger_path, ledger)
    return ledger


def update_ledger(
    run_dir: Path, updater: dict[str, Any], *, expected_revision: int,
    closure_decision: dict[str, Any] | None = None,
    flow: dict[str, Any] | None = None, cursor_action: str | None = None,
    cursor_result: str | None = None,
) -> dict[str, Any]:
    """Lock, validate the expected revision, and atomically update the ledger."""
    ledger = json.loads((run_dir / "ledger.json").read_text())
    load_flow_authority(run_dir, ledger)
    if run_records.active_actor(ledger):
        raise ValueError("Active actor operation blocks legacy ledger mutation")
    with storage.RunCommandLock(run_dir):
        return update_ledger_locked(
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
        "updated_at": run_records.now_iso(),
        "flow_revision": flow_revision,
        "flow_path": flow_path,
        "flow_sha256": flow_sha256,
    })
    ledger_rules.validate_ledger(updated)
    storage.atomic_write_json(run_dir / "ledger.json", updated)
    return updated


def revise_flow(run_dir: Path, flow_path: Path) -> dict[str, Any]:
    """Publish one immutable flow revision at the exact safe task boundary."""
    requested = json.loads(flow_path.read_text())
    flow_policy.validate_flow_profile(requested)
    requested_bytes = canonical_flow_bytes(requested)
    requested_digest = run_records.sha256_bytes(requested_bytes)
    preliminary_ledger = json.loads((run_dir / "ledger.json").read_text())
    load_flow_authority(run_dir, preliminary_ledger)
    with storage.RunCommandLock(run_dir):
        ledger = json.loads((run_dir / "ledger.json").read_text())
        ledger_rules.validate_ledger(ledger)
        _, authority, candidate = load_flow_authority_state(run_dir, ledger)
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
            storage.write_durable_exclusive(published, requested_bytes)
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
                ledger_rules.validate_ledger(committed)
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


def load_run_context(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    ledger = json.loads((run_dir / "ledger.json").read_text())
    ledger_rules.validate_ledger(ledger)
    flow = load_flow_authority(run_dir, ledger)
    active = run_records.active_actor(ledger)
    if active:
        assignment = active["assignment"]
        stage = "implement" if assignment["stage"] == "correction" else assignment["stage"]
        mode = flow_policy.flow_step(flow, stage)["mode"]
        if assignment["actor"] != flow["actor_levels"].get(mode):
            raise ValueError("Active assignment actor contradicts the frozen flow")
    return ledger, flow

