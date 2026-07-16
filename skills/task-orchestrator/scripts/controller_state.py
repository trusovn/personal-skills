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

ALLOWED_TASK_TRANSITIONS = {
    "initialized": {"ready", "stopped"},
    "ready": {"running", "stopped"},
    "running": {"awaiting_inspection", "resumable", "stopped"},
    "awaiting_inspection": {"accepted", "resumable", "stopped"},
    "resumable": {"running", "stopped"},
    "accepted": set(),
    "stopped": set(),
}


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


def select_task(ledger: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    if ledger["state"] != "initialized":
        raise ValueError(f"Cannot select task from state '{ledger['state']}'")
    if ledger["selected_task_id"] is not None:
        raise ValueError(f"Task already selected: {ledger['selected_task_id']}")
    if ledger["active_attempt_id"] is not None:
        raise ValueError(f"Active attempt exists: {ledger['active_attempt_id']}")
    completed = set(ledger.get("completed_task_ids", []))
    for task in ledger["tasks"]:
        if all(dependency in completed for dependency in task.get("dependencies", [])):
            return dict(task)
    ready = [task["id"] for task in ledger["tasks"] if all(dependency in completed for dependency in task.get("dependencies", []))]
    raise ValueError(f"No dependency-ready tasks found. Completed: {sorted(completed)}. Task IDs: {[task['id'] for task in ledger['tasks']]}. Ready: {ready}")


def validate_ledger(ledger: dict[str, Any]) -> None:
    required = (
        "version", "run_id", "repository", "created_at", "updated_at", "revision", "policy_path",
        "policy_sha256", "manifest_path", "manifest_sha256", "initial_baseline_path",
        "initial_baseline_digest", "completed_task_ids", "state", "selected_task_id",
        "active_attempt_id", "last_closure_path", "tasks",
    )
    missing = [field for field in required if field not in ledger]
    if missing:
        raise ValueError(f"Ledger is missing: {', '.join(missing)}")
    if ledger["state"] not in {"initialized", "ready", "running", "awaiting_inspection", "stopped"}:
        raise ValueError(f"Invalid ledger state: {ledger['state']}")
    if ledger["state"] == "running":
        if not ledger["selected_task_id"] or not ledger["active_attempt_id"]:
            raise ValueError("'running' state requires both selected_task_id and active_attempt_id")
    elif ledger["selected_task_id"] is not None and ledger["active_attempt_id"] is not None:
        raise ValueError("Cannot have both a selected task and active attempt")
    if ledger["state"] == "initialized" and (ledger["selected_task_id"] is not None or ledger["active_attempt_id"] is not None):
        raise ValueError("'initialized' state must have neither selected_task_id nor active_attempt_id")
    if ledger["state"] == "awaiting_inspection":
        if not ledger["selected_task_id"]:
            raise ValueError("'awaiting_inspection' requires selected_task_id")
        if ledger["active_attempt_id"] is not None:
            raise ValueError("'awaiting_inspection' must have no active_attempt_id")
        if not ledger["last_closure_path"]:
            raise ValueError("'awaiting_inspection' requires last_closure_path")
    task_ids: set[str] = set()
    selected_task = None
    for task in ledger["tasks"]:
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id or task_id in task_ids:
            raise ValueError("Ledger task IDs must be non-empty and unique")
        task_ids.add(task_id)
        if task.get("state") not in {"initialized", "ready", "running", "awaiting_inspection", "stopped"}:
            raise ValueError(f"Invalid task state for {task_id}: {task.get('state')}")
        attempts = task.get("attempt_ids")
        if not isinstance(attempts, list) or len(attempts) != len(set(attempts)):
            raise ValueError(f"Task {task_id} attempt IDs must be a unique array")
        if task_id == ledger["selected_task_id"]:
            selected_task = task
    if ledger["selected_task_id"] is not None and selected_task is None:
        raise ValueError("Selected task is missing from the ledger")
    if ledger["state"] in {"running", "awaiting_inspection"} and selected_task["state"] != ledger["state"]:
        raise ValueError("Selected task state must match the run state")
    if ledger["state"] == "running" and ledger["active_attempt_id"] not in selected_task["attempt_ids"]:
        raise ValueError("Active attempt must appear in the selected task history")


def apply_ledger_update(ledger: dict[str, Any], updater: dict[str, Any], updated_at: str) -> dict[str, Any]:
    next_ledger = json.loads(json.dumps(ledger))
    validate_ledger(next_ledger)
    previous_tasks = {task["id"]: task for task in next_ledger["tasks"]}
    next_ledger.update(updater)
    next_ledger["updated_at"] = updated_at
    next_ledger["revision"] = next_ledger.get("revision", 1) + 1
    validate_ledger(next_ledger)
    next_tasks = {task["id"]: task for task in next_ledger["tasks"]}
    if next_tasks.keys() != previous_tasks.keys():
        raise ValueError("Ledger task IDs are immutable")
    for task_id, previous in previous_tasks.items():
        attempts = next_tasks[task_id]["attempt_ids"]
        if attempts[:len(previous["attempt_ids"])] != previous["attempt_ids"]:
            raise ValueError(f"Task {task_id} attempt history is append-only")
    return next_ledger
