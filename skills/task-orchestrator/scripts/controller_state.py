"""Pure controller policy, manifest, transition, and ledger rules."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ATTEMPT_REQUIRED_FIELDS = (
    "task_id", "brief_path", "prompt_sha256", "baseline_ref", "policy_sha256",
    "transport", "model", "sandbox", "approval_policy", "network", "writable_roots",
)

RUN_STATES = (
    "initialized", "ready", "running", "awaiting_inspection", "resumable",
    "finalizing", "stopped",
)
TASK_STATES = (
    "initialized", "ready", "running", "awaiting_inspection", "resumable",
    "accepted", "stopped",
)

ALLOWED_RUN_TRANSITIONS = {
    "initialized": {"ready", "stopped"},
    "ready": {"running", "stopped"},
    "running": {"awaiting_inspection", "resumable", "stopped"},
    "awaiting_inspection": {"resumable", "finalizing", "stopped"},
    "resumable": {"running", "stopped"},
    "finalizing": {"ready", "stopped"},
    "stopped": set(),
}

ALLOWED_TASK_TRANSITIONS = {
    "initialized": {"ready", "stopped"},
    "ready": {"running", "stopped"},
    "running": {"awaiting_inspection", "resumable", "stopped"},
    "awaiting_inspection": {"accepted", "resumable", "stopped"},
    "resumable": {"running", "stopped"},
    "accepted": set(),
    "stopped": set(),
}


def transition_run(current: str, requested: str) -> str:
    if current not in ALLOWED_RUN_TRANSITIONS:
        raise ValueError(f"Unknown run state: {current}")
    if requested not in ALLOWED_RUN_TRANSITIONS[current]:
        raise ValueError(f"Run transition {current} -> {requested} is not allowed")
    return requested


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _validate_str(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")


def _validate_str_array(value: Any, field: str, *, allow_empty: bool = False) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    if not allow_empty and len(value) < 1:
        raise ValueError(f"{field} must have at least one item")
    for item in value:
        _validate_str(item, f"{field} item")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} items must be unique")


def _validate_bool(value: Any, field: str) -> None:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be a boolean")


def _validate_non_empty_object_keys(obj: dict[str, Any], prefix: str) -> None:
    for key in obj:
        _validate_str(key, f"{prefix}.{key}")


def _validate_verification(verification: dict[str, Any]) -> None:
    if not isinstance(verification, dict):
        raise ValueError("verification must be an object")
    required = ("targeted_checks", "repository_gate", "authorized_gap")
    missing = [field for field in required if field not in verification]
    if missing:
        raise ValueError(f"verification is missing: {', '.join(missing)}")
    _validate_str_array(verification["targeted_checks"], "verification.targeted_checks")
    if verification["repository_gate"] is not None:
        _validate_str(verification["repository_gate"], "verification.repository_gate")
    authorized_gap = verification["authorized_gap"]
    if authorized_gap is not None:
        if not isinstance(authorized_gap, dict):
            raise ValueError("verification.authorized_gap must be an object or null")
        required_gap = ("reason", "owner", "follow_up")
        missing_gap = [field for field in required_gap if field not in authorized_gap]
        if missing_gap:
            raise ValueError(
                f"verification.authorized_gap is missing: {', '.join(missing_gap)}"
            )
        for field in required_gap:
            _validate_str(authorized_gap[field], f"verification.authorized_gap.{field}")
        unknown = set(authorized_gap) - set(required_gap)
        if unknown:
            raise ValueError(
                "verification.authorized_gap contains unknown fields: "
                f"{', '.join(sorted(unknown))}"
            )
    unknown = set(verification) - set(required)
    if unknown:
        raise ValueError(f"verification contains unknown fields: {', '.join(sorted(unknown))}")


def _validate_permissions(permissions: dict[str, Any]) -> None:
    if not isinstance(permissions, dict):
        raise ValueError("permissions must be an object")
    required = (
        "sandbox", "approval_policy", "network", "dependency_install", "writable_roots",
        "danger_full_access_authorized",
    )
    missing = [field for field in required if field not in permissions]
    if missing:
        raise ValueError(f"permissions is missing: {', '.join(missing)}")
    if permissions["sandbox"] not in {"read-only", "workspace-write", "danger-full-access"}:
        raise ValueError(f"Unsupported sandbox: {permissions['sandbox']}")
    if permissions["approval_policy"] != "never":
        raise ValueError("Stage 1 requires approval_policy=never")
    _validate_bool(permissions["network"], "permissions.network")
    _validate_bool(permissions["dependency_install"], "permissions.dependency_install")
    _validate_str_array(permissions["writable_roots"], "permissions.writable_roots", allow_empty=True)
    _validate_bool(permissions["danger_full_access_authorized"], "permissions.danger_full_access_authorized")
    if permissions["sandbox"] == "danger-full-access" and not permissions["danger_full_access_authorized"]:
        raise ValueError("danger-full-access requires exact persisted authorization")
    unknown = set(permissions) - set(required)
    if unknown:
        raise ValueError(f"permissions contains unknown fields: {', '.join(sorted(unknown))}")


def _validate_commit_policy(commit_policy: dict[str, Any]) -> None:
    if not isinstance(commit_policy, dict):
        raise ValueError("commit_policy must be an object")
    if "mode" not in commit_policy:
        raise ValueError("commit_policy is missing 'mode'")
    if commit_policy["mode"] not in {"off", "controller_exact_paths"}:
        raise ValueError("Unsupported commit policy")
    unknown = set(commit_policy) - {"mode"}
    if unknown:
        raise ValueError(f"commit_policy contains unknown fields: {', '.join(sorted(unknown))}")


def _validate_stop_policy(stop_policy: dict[str, Any]) -> None:
    if not isinstance(stop_policy, dict):
        raise ValueError("stop_policy must be an object")
    required = ("on_blocked", "on_failed", "on_needs_input", "on_unexpected_changes")
    missing = [field for field in required if field not in stop_policy]
    if missing:
        raise ValueError(f"stop_policy is missing: {', '.join(missing)}")
    for field in required:
        if stop_policy[field] not in {"stop", "escalate"}:
            raise ValueError(f"stop_policy.{field} must be 'stop' or 'escalate'")
    unknown = set(stop_policy) - set(required)
    if unknown:
        raise ValueError(f"stop_policy contains unknown fields: {', '.join(sorted(unknown))}")


def validate_run_policy(policy: dict[str, Any]) -> None:
    if not isinstance(policy, dict):
        raise ValueError("Run policy must be an object")
    required = (
        "version", "run_id", "repository", "task_ids", "verification", "permissions",
        "commit_policy", "stop_policy",
    )
    missing = [field for field in required if field not in policy]
    if missing:
        raise ValueError(f"Run policy is missing: {', '.join(missing)}")
    if type(policy["version"]) is not int or policy["version"] != 1:
        raise ValueError("Unsupported run policy version")
    _validate_str(policy["run_id"], "run_id")
    _validate_str(policy["repository"], "repository")
    _validate_str_array(policy["task_ids"], "task_ids")
    _validate_verification(policy["verification"])
    _validate_permissions(policy["permissions"])
    _validate_commit_policy(policy["commit_policy"])
    _validate_stop_policy(policy["stop_policy"])
    unknown = set(policy) - set(required)
    if unknown:
        raise ValueError(f"Run policy contains unknown top-level fields: {', '.join(sorted(unknown))}")


def transition_task(current: str, requested: str, *, closure_decision: dict[str, Any] | None = None,
                    expected_identity: dict[str, str] | None = None) -> str:
    if current not in ALLOWED_TASK_TRANSITIONS:
        raise ValueError(f"Unknown task state: {current}")
    if requested not in ALLOWED_TASK_TRANSITIONS[current]:
        raise ValueError(f"Task transition {current} -> {requested} is not allowed")
    if requested == "accepted":
        decision = closure_decision or {}
        if decision.get("accepted") is not True:
            raise ValueError("Acceptance requires an accepting closure decision")
        allowed = decision.get("allowed_transitions")
        if not isinstance(allowed, list) or "accepted" not in allowed:
            raise ValueError("Acceptance requires 'accepted' in allowed transitions")
        if not expected_identity or decision.get("identity") != expected_identity:
            raise ValueError("Acceptance closure identity does not match current evidence")
    return requested


def validate_attempt_record(record: dict[str, Any]) -> None:
    for field in ATTEMPT_REQUIRED_FIELDS:
        if field not in record:
            raise ValueError(f"Attempt record is missing {field}")


def build_attempt_record(*, task_id: str, brief_path: str, prompt: str, policy: dict[str, Any],
                         baseline_ref: str) -> dict[str, Any]:
    validate_run_policy(policy)
    permissions = policy["permissions"]
    return {
        "task_id": task_id, "brief_path": brief_path, "prompt": prompt,
        "prompt_sha256": sha256_text(prompt), "baseline_ref": baseline_ref,
        "policy_sha256": sha256_text(canonical_json(policy)), "transport": "codex-cli",
        "model": None, "sandbox": permissions["sandbox"],
        "approval_policy": permissions["approval_policy"], "network": permissions["network"],
        "writable_roots": permissions["writable_roots"],
    }


def _validate_task_manifest_schema(manifest: dict[str, Any]) -> None:
    if not isinstance(manifest, dict):
        raise ValueError("Task manifest must be an object")
    required = ("version", "manifest_id", "completed_task_ids", "tasks")
    missing = [field for field in required if field not in manifest]
    if missing:
        raise ValueError(f"Task manifest is missing: {', '.join(missing)}")
    if type(manifest["version"]) is not int or manifest["version"] != 1:
        raise ValueError("Unsupported task manifest version")
    unknown = set(manifest) - set(required)
    if unknown:
        raise ValueError(f"Task manifest contains unknown fields: {', '.join(sorted(unknown))}")
    _validate_str(manifest["manifest_id"], "manifest_id")
    _validate_str_array(manifest["completed_task_ids"], "completed_task_ids", allow_empty=True)
    if not isinstance(manifest["tasks"], list) or len(manifest["tasks"]) < 1:
        raise ValueError("manifest.tasks must be a non-empty array")
    task_ids: set[str] = set()
    for task in manifest["tasks"]:
        if not isinstance(task, dict):
            raise ValueError("Each task must be an object")
        task_required = {"id", "title", "brief_path", "allowed_paths"}
        missing_task = task_required - set(task)
        if missing_task:
            raise ValueError(f"Task is missing required fields: {', '.join(sorted(missing_task))}")
        unknown_task = set(task) - {"id", "title", "brief_path", "dependencies", "allowed_paths", "required_checks"}
        if unknown_task:
            raise ValueError(f"Task contains unknown fields: {', '.join(sorted(unknown_task))}")
        _validate_str(task["id"], "tasks[].id")
        if task["id"] in task_ids:
            raise ValueError(f"Duplicate task id: {task['id']}")
        task_ids.add(task["id"])
        _validate_str(task["title"], "tasks[].title")
        _validate_str(task["brief_path"], "tasks[].brief_path")
        for field in ("dependencies", "required_checks", "allowed_paths"):
            if field in task:
                _validate_str_array(task[field], f"tasks[].{field}", allow_empty=True)


def _detect_dependency_cycles(manifest: dict[str, Any]) -> list[list[str]]:
    task_map = {task["id"]: task for task in manifest["tasks"]}
    cycles: list[list[str]] = []
    colors = {task_id: 0 for task_id in task_map}
    path: list[str] = []

    def visit(task_id: str) -> None:
        colors[task_id] = 1
        path.append(task_id)
        for dependency in task_map[task_id].get("dependencies", []):
            if dependency not in task_map:
                continue
            if colors[dependency] == 1:
                cycles.append(path[path.index(dependency):] + [dependency])
            elif colors[dependency] == 0:
                visit(dependency)
        path.pop()
        colors[task_id] = 2

    for task_id in task_map:
        if colors[task_id] == 0:
            visit(task_id)
    return cycles


def _is_valid_repo_relative_path(path_str: str) -> bool:
    if not path_str:
        return False
    return not any(part in {"", ".", ".."} for part in path_str.split("/"))


def validate_task_manifest(policy: dict[str, Any], manifest: dict[str, Any], repository: Path) -> dict[str, Any]:
    _validate_task_manifest_schema(manifest)
    policy_task_ids = list(policy["task_ids"])
    task_map = {task["id"]: task for task in manifest["tasks"]}
    completed = manifest.get("completed_task_ids", [])
    for task_id in policy_task_ids:
        if task_id not in task_map:
            raise ValueError(f"Policy task_id {task_id} not found in manifest")
        if task_id in completed:
            raise ValueError(f"Policy task_id {task_id} is already completed")
    all_task_ids = set(task_map)
    for task in manifest["tasks"]:
        dependencies = task.get("dependencies", [])
        for dependency in dependencies:
            if dependency not in all_task_ids:
                raise ValueError(f"Task {task['id']} depends on {dependency} which does not exist in manifest")
        if task["id"] in dependencies:
            raise ValueError(f"Task {task['id']} depends on itself")
    for task_id in policy_task_ids:
        for dependency in task_map[task_id].get("dependencies", []):
            if dependency not in set(policy_task_ids) and dependency not in completed:
                raise ValueError(
                    f"Authorized task {task_id} depends on {dependency} which is not completed and not in the authorized run"
                )
    for task in manifest["tasks"]:
        if not task.get("allowed_paths"):
            raise ValueError(f"Task {task['id']} must have a non-empty allowed_paths array")
        for allowed_path in task["allowed_paths"]:
            if not _is_valid_repo_relative_path(allowed_path):
                raise ValueError(f"Task {task['id']} allowed_path '{allowed_path}' is not a valid repository-relative path")
            if not (repository / allowed_path).resolve().is_relative_to(repository.resolve()):
                raise ValueError(f"Task {task['id']} allowed_path '{allowed_path}' resolves outside the repository")
    cycles = _detect_dependency_cycles(manifest)
    if cycles:
        raise ValueError(f"Dependency cycle detected in manifest: {'; '.join(' -> '.join(cycle) for cycle in cycles)}")
    for task in manifest["tasks"]:
        brief_path = repository / task["brief_path"]
        if not brief_path.resolve().is_relative_to(repository.resolve()):
            raise ValueError(f"Task {task['id']} brief is outside the repository: {task['brief_path']}")
        if not brief_path.is_file():
            raise ValueError(f"Task {task['id']} brief file does not exist: {task['brief_path']}")
    task_entries = []
    for task_id in policy_task_ids:
        task = task_map[task_id]
        task_entries.append({
            "id": task["id"], "title": task["title"], "brief_path": task["brief_path"],
            "dependencies": task.get("dependencies", []), "allowed_paths": task.get("allowed_paths", []),
            "required_checks": task.get("required_checks", []), "state": "initialized", "attempt_ids": [],
        })
    return {"manifest_id": manifest["manifest_id"], "completed_task_ids": completed, "task_entries": task_entries}


def dependency_ready_task_ids(
    tasks: list[dict[str, Any]], completed_task_ids: list[str]
) -> list[str]:
    completed = set(completed_task_ids)
    completed.update(task["id"] for task in tasks if task.get("state") == "accepted")
    return [
        task["id"]
        for task in tasks
        if task.get("state") in {"initialized", "ready"}
        and all(dependency in completed for dependency in task.get("dependencies", []))
    ]


def mark_ready_tasks(
    tasks: list[dict[str, Any]], completed_task_ids: list[str]
) -> list[dict[str, Any]]:
    next_tasks = json.loads(json.dumps(tasks))
    ready_ids = set(dependency_ready_task_ids(next_tasks, completed_task_ids))
    for task in next_tasks:
        if task["id"] in ready_ids and task["state"] == "initialized":
            task["state"] = "ready"
    return next_tasks


def select_task(ledger: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    if ledger["state"] != "ready":
        raise ValueError(f"Cannot select task from state '{ledger['state']}'")
    if ledger["selected_task_id"] is not None:
        raise ValueError(f"Task already selected: {ledger['selected_task_id']}")
    if ledger["active_attempt_id"] is not None:
        raise ValueError(f"Active attempt exists: {ledger['active_attempt_id']}")
    task_map = {task["id"]: task for task in ledger["tasks"]}
    ready = [task_id for task_id in policy["task_ids"] if task_map[task_id]["state"] == "ready"]
    if ready:
        return dict(task_map[ready[0]])
    completed = set(ledger.get("completed_task_ids", []))
    completed.update(task["id"] for task in ledger["tasks"] if task["state"] == "accepted")
    raise ValueError(f"No dependency-ready tasks found. Completed: {sorted(completed)}. Task IDs: {[task['id'] for task in ledger['tasks']]}. Ready: {ready}")


def validate_ledger(ledger: dict[str, Any]) -> None:
    required = (
        "version", "run_id", "repository", "created_at", "updated_at", "revision", "policy_path",
        "policy_sha256", "manifest_path", "manifest_sha256", "initial_baseline_path",
        "initial_baseline_digest", "completed_task_ids", "state", "selected_task_id",
        "active_attempt_id", "last_closure_path", "last_verification_path",
        "last_decision_path", "active_operation_path", "tasks",
    )
    missing = [field for field in required if field not in ledger]
    if missing:
        raise ValueError(f"Ledger is missing: {', '.join(missing)}")
    if ledger["state"] not in RUN_STATES:
        raise ValueError(f"Invalid ledger state: {ledger['state']}")
    if type(ledger["revision"]) is not int or ledger["revision"] < 1:
        raise ValueError("Ledger revision must be a positive integer")
    _validate_str_array(ledger["completed_task_ids"], "completed_task_ids", allow_empty=True)
    for field in (
        "selected_task_id", "active_attempt_id", "last_closure_path",
        "last_verification_path", "last_decision_path", "active_operation_path",
    ):
        if ledger[field] is not None:
            _validate_str(ledger[field], field)

    task_ids: set[str] = set()
    selected_task = None
    attempt_owners: dict[str, str] = {}
    for task in ledger["tasks"]:
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id or task_id in task_ids:
            raise ValueError("Ledger task IDs must be non-empty and unique")
        task_ids.add(task_id)
        if task.get("state") not in TASK_STATES:
            raise ValueError(f"Invalid task state for {task_id}: {task.get('state')}")
        attempts = task.get("attempt_ids")
        if not isinstance(attempts, list) or len(attempts) != len(set(attempts)):
            raise ValueError(f"Task {task_id} attempt IDs must be a unique array")
        for attempt_id in attempts:
            _validate_str(attempt_id, f"Task {task_id} attempt ID")
            if attempt_id in attempt_owners:
                raise ValueError(
                    f"Attempt {attempt_id} is owned by more than one task"
                )
            attempt_owners[attempt_id] = task_id
        if task_id == ledger["selected_task_id"]:
            selected_task = task

    if ledger["selected_task_id"] is not None and selected_task is None:
        raise ValueError("Selected task is missing from the ledger")

    state = ledger["state"]
    selected_states = {
        "running": "running",
        "awaiting_inspection": "awaiting_inspection",
        "resumable": "resumable",
        "finalizing": "awaiting_inspection",
    }
    if state in selected_states:
        if selected_task is None:
            raise ValueError(f"'{state}' requires selected_task_id")
        if selected_task["state"] != selected_states[state]:
            if state == "finalizing":
                raise ValueError("A finalizing task must remain awaiting_inspection")
            raise ValueError("Selected task state must match the run state")
        if not selected_task["attempt_ids"]:
            raise ValueError(f"'{state}' requires a selected attempt")
    elif ledger["selected_task_id"] is not None:
        raise ValueError(f"'{state}' must have no selected_task_id")

    if state == "running":
        if ledger["active_attempt_id"] != selected_task["attempt_ids"][-1]:
            raise ValueError("Active attempt must be the latest selected task attempt")
    elif ledger["active_attempt_id"] is not None:
        raise ValueError(f"'{state}' must have no active_attempt_id")

    if state in {"initialized", "ready", "running"}:
        for field in (
            "last_closure_path", "last_verification_path", "last_decision_path",
            "active_operation_path",
        ):
            if ledger[field] is not None:
                raise ValueError(f"'{state}' requires {field}=null")
    if state in {"awaiting_inspection", "resumable", "finalizing"}:
        if ledger["last_closure_path"] is None:
            raise ValueError(f"'{state}' requires last_closure_path")
    if ledger["last_decision_path"] is not None and ledger["last_verification_path"] is None:
        raise ValueError("last_decision_path requires last_verification_path")
    if ledger["last_verification_path"] is not None and ledger["last_closure_path"] is None:
        raise ValueError("last_verification_path requires last_closure_path")
    if state != "finalizing" and ledger["active_operation_path"] is not None:
        raise ValueError("active_operation_path is only compatible with finalizing")
    if state == "finalizing":
        for field in (
            "last_verification_path", "last_decision_path", "active_operation_path",
        ):
            if ledger[field] is None:
                raise ValueError(f"'finalizing' requires {field}")

    if state == "ready":
        ready_tasks = [task for task in ledger["tasks"] if task["state"] == "ready"]
        if not ready_tasks:
            raise ValueError("'ready' requires at least one ready unfinished task")
        completed = set(ledger["completed_task_ids"])
        completed.update(task["id"] for task in ledger["tasks"] if task["state"] == "accepted")
        for task in ready_tasks:
            if not all(dependency in completed for dependency in task["dependencies"]):
                raise ValueError(f"Ready task {task['id']} has incomplete dependencies")


def apply_ledger_update(
    ledger: dict[str, Any], updater: dict[str, Any], updated_at: str,
    *, expected_revision: int | None = None,
) -> dict[str, Any]:
    next_ledger = json.loads(json.dumps(ledger))
    validate_ledger(next_ledger)
    if expected_revision is not None and next_ledger["revision"] != expected_revision:
        raise ValueError(
            f"Stale ledger revision: expected {expected_revision}, "
            f"found {next_ledger['revision']}"
        )
    if "revision" in updater:
        raise ValueError("Ledger revision is controller-managed")
    previous_tasks = next_ledger["tasks"]
    next_ledger.update(updater)
    next_ledger["updated_at"] = updated_at
    next_ledger["revision"] = ledger["revision"] + 1
    candidate_tasks = next_ledger.get("tasks")
    if isinstance(candidate_tasks, list) and len(candidate_tasks) == len(previous_tasks):
        for previous, current in zip(previous_tasks, candidate_tasks):
            if not isinstance(current, dict) or current.get("id") != previous["id"]:
                continue
            attempts = current.get("attempt_ids")
            if (
                isinstance(attempts, list)
                and attempts[:len(previous["attempt_ids"])] != previous["attempt_ids"]
            ):
                raise ValueError(f"Task {previous['id']} attempt history is append-only")
    validate_ledger(next_ledger)
    if next_ledger["completed_task_ids"] != ledger["completed_task_ids"]:
        raise ValueError("Ledger completed_task_ids are immutable")
    if next_ledger["state"] != ledger["state"]:
        transition_run(ledger["state"], next_ledger["state"])
    next_tasks = next_ledger["tasks"]
    if [task["id"] for task in next_tasks] != [task["id"] for task in previous_tasks]:
        raise ValueError("Ledger task identity and order are immutable")
    immutable_task_fields = (
        "id", "title", "brief_path", "dependencies", "allowed_paths", "required_checks",
    )
    for previous, current in zip(previous_tasks, next_tasks):
        task_id = previous["id"]
        for field in immutable_task_fields:
            if current[field] != previous[field]:
                raise ValueError(f"Task {task_id} {field} is immutable")
        if current["state"] != previous["state"]:
            if current["state"] not in ALLOWED_TASK_TRANSITIONS[previous["state"]]:
                raise ValueError(
                    f"Task transition {previous['state']} -> {current['state']} is not allowed"
                )
        attempts = current["attempt_ids"]
        if attempts[:len(previous["attempt_ids"])] != previous["attempt_ids"]:
            raise ValueError(f"Task {task_id} attempt history is append-only")
    return next_ledger
