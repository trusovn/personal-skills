"""Manifest structure, dependency/path validation and ready-task selection.

Uses shared record predicates and reads brief/path facts supplied by repository
location. Run permissions and ledger-wide consistency belong elsewhere."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .record_validation import (
    validate_str,
    validate_str_array,
    is_valid_repo_relative_path,
)


def validate_task_manifest_structure(manifest: dict[str, Any]) -> None:
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
    validate_str(manifest["manifest_id"], "manifest_id")
    validate_str_array(manifest["completed_task_ids"], "completed_task_ids", allow_empty=True)
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
        unknown_task = set(task) - {"id", "title", "brief_path", "dependencies", "allowed_paths", "required_checks", "required_reviews"}
        if unknown_task:
            raise ValueError(f"Task contains unknown fields: {', '.join(sorted(unknown_task))}")
        validate_str(task["id"], "tasks[].id")
        if task["id"] in task_ids:
            raise ValueError(f"Duplicate task id: {task['id']}")
        task_ids.add(task["id"])
        validate_str(task["title"], "tasks[].title")
        validate_str(task["brief_path"], "tasks[].brief_path")
        for field in ("dependencies", "required_checks", "allowed_paths", "required_reviews"):
            if field in task:
                validate_str_array(task[field], f"tasks[].{field}", allow_empty=True)

        if any(stage not in {'maintainability', 'registry'} for stage in task.get('required_reviews', [])):
            raise ValueError('Unknown required conditional review stage')


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


def validate_task_manifest(policy: dict[str, Any], manifest: dict[str, Any], repository: Path) -> dict[str, Any]:
    validate_task_manifest_structure(manifest)
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
            if not is_valid_repo_relative_path(allowed_path):
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
    if ledger["state"] != "ready":
        raise ValueError(f"Cannot select task from state '{ledger['state']}'")
    if ledger["selected_task_id"] is not None:
        raise ValueError(f"Task already selected: {ledger['selected_task_id']}")
    if ledger["active_attempt_id"] is not None:
        raise ValueError(f"Active attempt exists: {ledger['active_attempt_id']}")
    completed = set(ledger.get("completed_task_ids", []))
    completed.update(task["id"] for task in ledger["tasks"] if task["state"] == "accepted")
    for task in ledger["tasks"]:
        if task["state"] == "ready" and all(
            dependency in completed for dependency in task.get("dependencies", [])
        ):
            return dict(task)
    raise ValueError(
        f"No ready tasks found. Completed: {sorted(completed)}. "
        f"Task IDs: {[task['id'] for task in ledger['tasks']]}"
    )
