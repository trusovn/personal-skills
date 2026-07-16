#!/usr/bin/env python3
"""Small Stage 1 policy, prompt, attempt, and closure primitives."""

from __future__ import annotations

import hashlib
import importlib.util
import json
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


ATTEMPT_REQUIRED_FIELDS = (
    "task_id",
    "brief_path",
    "prompt_sha256",
    "baseline_ref",
    "policy_sha256",
    "transport",
    "model",
    "sandbox",
    "approval_policy",
    "network",
    "writable_roots",
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


def atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(value)
    temporary.replace(path)


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
    missing = [f for f in required if f not in verification]
    if missing:
        raise ValueError(f"verification is missing: {', '.join(missing)}")
    _validate_str_array(verification["targeted_checks"], "verification.targeted_checks")
    rg = verification["repository_gate"]
    if rg is not None:
        _validate_str(rg, "verification.repository_gate")
    ag = verification["authorized_gap"]
    if ag is not None:
        if not isinstance(ag, dict):
            raise ValueError("verification.authorized_gap must be an object or null")
        ag_required = ("reason", "owner", "follow_up")
        ag_missing = [f for f in ag_required if f not in ag]
        if ag_missing:
            raise ValueError(f"verification.authorized_gap is missing: {', '.join(ag_missing)}")
        for f in ag_required:
            _validate_str(ag[f], f"verification.authorized_gap.{f}")
        unknown = set(ag.keys()) - set(ag_required)
        if unknown:
            raise ValueError(
                f"verification.authorized_gap contains unknown fields: {', '.join(sorted(unknown))}"
            )
    unknown = set(verification.keys()) - set(required)
    if unknown:
        raise ValueError(
            f"verification contains unknown fields: {', '.join(sorted(unknown))}"
        )


def _validate_permissions(permissions: dict[str, Any]) -> None:
    if not isinstance(permissions, dict):
        raise ValueError("permissions must be an object")
    required = (
        "sandbox",
        "approval_policy",
        "network",
        "dependency_install",
        "writable_roots",
        "danger_full_access_authorized",
    )
    missing = [f for f in required if f not in permissions]
    if missing:
        raise ValueError(f"permissions is missing: {', '.join(missing)}")
    sandbox = permissions["sandbox"]
    if sandbox not in {"read-only", "workspace-write", "danger-full-access"}:
        raise ValueError(f"Unsupported sandbox: {sandbox}")
    if permissions["approval_policy"] != "never":
        raise ValueError("Stage 1 requires approval_policy=never")
    _validate_bool(permissions["network"], "permissions.network")
    _validate_bool(permissions["dependency_install"], "permissions.dependency_install")
    _validate_str_array(
        permissions["writable_roots"],
        "permissions.writable_roots",
        allow_empty=True,
    )
    _validate_bool(
        permissions["danger_full_access_authorized"],
        "permissions.danger_full_access_authorized",
    )
    if sandbox == "danger-full-access" and not permissions["danger_full_access_authorized"]:
        raise ValueError(
            "danger-full-access requires exact persisted authorization"
        )
    unknown = set(permissions.keys()) - set(required)
    if unknown:
        raise ValueError(
            f"permissions contains unknown fields: {', '.join(sorted(unknown))}"
        )


def _validate_commit_policy(commit_policy: dict[str, Any]) -> None:
    if not isinstance(commit_policy, dict):
        raise ValueError("commit_policy must be an object")
    if "mode" not in commit_policy:
        raise ValueError("commit_policy is missing 'mode'")
    if commit_policy["mode"] not in {"off", "controller_exact_paths"}:
        raise ValueError("Unsupported commit policy")
    unknown = set(commit_policy.keys()) - {"mode"}
    if unknown:
        raise ValueError(
            f"commit_policy contains unknown fields: {', '.join(sorted(unknown))}"
        )


def _validate_stop_policy(stop_policy: dict[str, Any]) -> None:
    if not isinstance(stop_policy, dict):
        raise ValueError("stop_policy must be an object")
    required = ("on_blocked", "on_failed", "on_needs_input", "on_unexpected_changes")
    missing = [f for f in required if f not in stop_policy]
    if missing:
        raise ValueError(f"stop_policy is missing: {', '.join(missing)}")
    valid_values = {"stop", "escalate"}
    for f in required:
        if stop_policy[f] not in valid_values:
            raise ValueError(f"stop_policy.{f} must be 'stop' or 'escalate'")
    unknown = set(stop_policy.keys()) - set(required)
    if unknown:
        raise ValueError(
            f"stop_policy contains unknown fields: {', '.join(sorted(unknown))}"
        )


def validate_run_policy(policy: dict[str, Any]) -> None:
    if not isinstance(policy, dict):
        raise ValueError("Run policy must be an object")
    required = (
        "version",
        "run_id",
        "repository",
        "task_ids",
        "verification",
        "permissions",
        "commit_policy",
        "stop_policy",
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
    unknown_top = set(policy.keys()) - set(required)
    if unknown_top:
        raise ValueError(
            f"Run policy contains unknown top-level fields: {', '.join(sorted(unknown_top))}"
        )


def persist_run_policy(path: Path, policy: dict[str, Any]) -> str:
    validate_run_policy(policy)
    serialized = json.dumps(policy, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        stream.write(serialized)
    return sha256_text(canonical_json(policy))


def transition_task(
    current: str,
    requested: str,
    *,
    closure_decision: dict[str, Any] | None = None,
    expected_identity: dict[str, str] | None = None,
) -> str:
    if current not in ALLOWED_TASK_TRANSITIONS:
        raise ValueError(f"Unknown task state: {current}")
    if requested not in ALLOWED_TASK_TRANSITIONS[current]:
        raise ValueError(f"Task transition {current} -> {requested} is not allowed")
    if requested == "accepted":
        decision = closure_decision or {}
        if decision.get("accepted") is not True:
            raise ValueError("Acceptance requires an accepting closure decision")
        allowed_transitions = decision.get("allowed_transitions")
        if not isinstance(allowed_transitions, list) or "accepted" not in allowed_transitions:
            raise ValueError("Acceptance requires 'accepted' in allowed transitions")
        if not expected_identity or decision.get("identity") != expected_identity:
            raise ValueError("Acceptance closure identity does not match current evidence")
    return requested


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


def capture_git_status(repository: Path) -> dict[str, str]:
    result = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        check=True,
        capture_output=True,
    )
    entries = result.stdout.decode(errors="surrogateescape").split("\0")
    status: dict[str, str] = {}
    index = 0
    while index < len(entries):
        entry = entries[index]
        if not entry:
            index += 1
            continue
        code = entry[:2]
        path = entry[3:]
        worktree_path = repository / path
        if worktree_path.is_symlink():
            content = str(worktree_path.readlink()).encode()
        elif worktree_path.is_file():
            content = worktree_path.read_bytes()
        else:
            content = b"<missing>"
        status[path] = f"{code}:{hashlib.sha256(content).hexdigest()}"
        if "R" in code or "C" in code:
            index += 1
        index += 1
    return status


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


def validate_attempt_record(record: dict[str, Any]) -> None:
    for field in ATTEMPT_REQUIRED_FIELDS:
        if field not in record:
            raise ValueError(f"Attempt record is missing {field}")


def build_attempt_record(
    *,
    task_id: str,
    brief_path: str,
    prompt: str,
    policy: dict[str, Any],
    baseline_ref: str,
) -> dict[str, Any]:
    validate_run_policy(policy)
    permissions = policy["permissions"]
    return {
        "task_id": task_id,
        "brief_path": brief_path,
        "prompt": prompt,
        "prompt_sha256": sha256_text(prompt),
        "baseline_ref": baseline_ref,
        "policy_sha256": sha256_text(canonical_json(policy)),
        "transport": "codex-cli",
        "model": None,
        "sandbox": permissions["sandbox"],
        "approval_policy": permissions["approval_policy"],
        "network": permissions["network"],
        "writable_roots": permissions["writable_roots"],
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


def _validate_task_manifest_schema(manifest: dict[str, Any]) -> None:
    if not isinstance(manifest, dict):
        raise ValueError("Task manifest must be an object")
    required = ("version", "manifest_id", "completed_task_ids", "tasks")
    missing = [f for f in required if f not in manifest]
    if missing:
        raise ValueError(f"Task manifest is missing: {', '.join(missing)}")
    if type(manifest["version"]) is not int or manifest["version"] != 1:
        raise ValueError("Unsupported task manifest version")
    unknown_top = set(manifest.keys()) - set(required)
    if unknown_top:
        raise ValueError(
            f"Task manifest contains unknown fields: {', '.join(sorted(unknown_top))}"
        )
    _validate_str(manifest["manifest_id"], "manifest_id")
    # completed_task_ids may be empty (no tasks completed yet)
    if not isinstance(manifest["completed_task_ids"], list):
        raise ValueError("completed_task_ids must be an array")
    for item in manifest["completed_task_ids"]:
        _validate_str(item, "completed_task_ids item")
    if len(manifest["completed_task_ids"]) != len(set(manifest["completed_task_ids"])):
        raise ValueError("completed_task_ids items must be unique")
    if not isinstance(manifest["tasks"], list) or len(manifest["tasks"]) < 1:
        raise ValueError("manifest.tasks must be a non-empty array")
    task_ids: set[str] = set()
    for task in manifest["tasks"]:
        if not isinstance(task, dict):
            raise ValueError("Each task must be an object")
        task_required = {"id", "title", "brief_path", "allowed_paths"}
        task_missing = task_required - set(task)
        if task_missing:
            raise ValueError(
                f"Task is missing required fields: {', '.join(sorted(task_missing))}"
            )
        unknown = set(task.keys()) - {"id", "title", "brief_path", "dependencies", "allowed_paths", "required_checks"}
        if unknown:
            raise ValueError(f"Task contains unknown fields: {', '.join(sorted(unknown))}")
        _validate_str(task["id"], "tasks[].id")
        if task["id"] in task_ids:
            raise ValueError(f"Duplicate task id: {task['id']}")
        task_ids.add(task["id"])
        _validate_str(task["title"], "tasks[].title")
        _validate_str(task["brief_path"], "tasks[].brief_path")
        if "dependencies" in task:
            if not isinstance(task["dependencies"], list):
                raise ValueError("tasks[].dependencies must be an array")
            for dep in task["dependencies"]:
                _validate_str(dep, "tasks[].dependencies item")
            if len(task["dependencies"]) != len(set(task["dependencies"])):
                raise ValueError("tasks[].dependencies items must be unique")
        if "required_checks" in task:
            if not isinstance(task["required_checks"], list):
                raise ValueError("tasks[].required_checks must be an array")
            for check in task["required_checks"]:
                _validate_str(check, "tasks[].required_checks item")
            if len(task["required_checks"]) != len(set(task["required_checks"])):
                raise ValueError("tasks[].required_checks items must be unique")
        if "allowed_paths" in task:
            if not isinstance(task["allowed_paths"], list):
                raise ValueError("tasks[].allowed_paths must be an array")
            for ap in task["allowed_paths"]:
                _validate_str(ap, "tasks[].allowed_paths item")
            if len(task["allowed_paths"]) != len(set(task["allowed_paths"])):
                raise ValueError("tasks[].allowed_paths items must be unique")


def _detect_dependency_cycles(manifest: dict[str, Any]) -> list[list[str]]:
    """Detect dependency cycles in the manifest using DFS.

    Returns a list of cycles found, where each cycle is a list of task IDs.
    An empty list means no cycles.
    """
    manifest_task_map: dict[str, dict[str, Any]] = {}
    for task in manifest["tasks"]:
        manifest_task_map[task["id"]] = task

    cycles: list[list[str]] = []
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {tid: WHITE for tid in manifest_task_map}
    path: list[str] = []

    def dfs(node_id: str) -> None:
        color[node_id] = GRAY
        path.append(node_id)
        for dep_id in manifest_task_map[node_id].get("dependencies", []):
            if dep_id not in manifest_task_map:
                continue  # Already caught by existence check
            if color[dep_id] == GRAY:
                # Found a cycle: extract it
                cycle_start = path.index(dep_id)
                cycle = path[cycle_start:] + [dep_id]
                cycles.append(cycle)
            elif color[dep_id] == WHITE:
                dfs(dep_id)
        path.pop()
        color[node_id] = BLACK

    for task_id in manifest_task_map:
        if color[task_id] == WHITE:
            dfs(task_id)

    return cycles


def _is_valid_repo_relative_path(path_str: str) -> bool:
    """Reject absolute paths, .., empty segments, directory-only entries."""
    if not path_str:
        return False
    parts = path_str.split("/")
    return not any(part in {"", ".", ".."} for part in parts)


def validate_task_manifest(
    policy: dict[str, Any],
    manifest: dict[str, Any],
    repository: Path,
) -> dict[str, Any]:
    """Validate the manifest against the schema and cross-validate with policy.

    Returns a dict with task entries ready to be embedded in the ledger.
    """
    _validate_task_manifest_schema(manifest)
    policy_task_ids = list(policy["task_ids"])
    manifest_task_map: dict[str, dict[str, Any]] = {}
    for task in manifest["tasks"]:
        manifest_task_map[task["id"]] = task

    # Require every policy.task_ids entry exists in manifest and is not completed
    for pid in policy_task_ids:
        if pid not in manifest_task_map:
            raise ValueError(f"Policy task_id {pid} not found in manifest")
        if pid in manifest.get("completed_task_ids", []):
            raise ValueError(f"Policy task_id {pid} is already completed")

    # Require every dependency and completed_task_id exists in tasks
    all_task_ids = set(manifest_task_map.keys())
    for task in manifest["tasks"]:
        deps = task.get("dependencies", [])
        for dep_id in deps:
            if dep_id not in all_task_ids:
                raise ValueError(
                    f"Task {task['id']} depends on {dep_id} which does not exist in manifest"
                )
        # Reject self-dependencies
        if task["id"] in deps:
            raise ValueError(f"Task {task['id']} depends on itself")

    # Reject authorized tasks that depend on incomplete tasks outside the authorized run
    for pid in policy_task_ids:
        task = manifest_task_map[pid]
        for dep_id in task.get("dependencies", []):
            if dep_id not in set(policy_task_ids) and dep_id not in manifest.get("completed_task_ids", []):
                raise ValueError(
                    f"Authorized task {pid} depends on {dep_id} which is not completed and not in the authorized run"
                )

    # Validate allowed_paths are valid repo-relative paths and contained within the repository
    for task in manifest["tasks"]:
        # Empty allowed_paths arrays are rejected (exact paths required)
        if "allowed_paths" not in task or not task["allowed_paths"]:
            raise ValueError(
                f"Task {task['id']} must have a non-empty allowed_paths array"
            )
        for ap in task.get("allowed_paths", []):
            if not _is_valid_repo_relative_path(ap):
                raise ValueError(
                    f"Task {task['id']} allowed_path '{ap}' is not a valid repository-relative path"
                )
            resolved = (repository / ap).resolve()
            if not resolved.is_relative_to(repository.resolve()):
                raise ValueError(
                    f"Task {task['id']} allowed_path '{ap}' resolves outside the repository"
                )

    # Reject dependency cycles
    cycles = _detect_dependency_cycles(manifest)
    if cycles:
        cycle_strs = [" -> ".join(c) for c in cycles]
        raise ValueError(
            f"Dependency cycle detected in manifest: {'; '.join(cycle_strs)}"
        )

    # Validate brief files exist and are contained within the repository
    for task in manifest["tasks"]:
        brief_path = repository / task["brief_path"]
        if not brief_path.resolve().is_relative_to(repository.resolve()):
            raise ValueError(
                f"Task {task['id']} brief is outside the repository: {task['brief_path']}"
            )
        if not brief_path.is_file():
            raise ValueError(
                f"Task {task['id']} brief file does not exist: {task['brief_path']}"
            )

    # Build ledger-ready task entries preserving policy order
    task_entries: list[dict[str, Any]] = []
    for pid in policy_task_ids:
        task = manifest_task_map[pid]
        task_entries.append({
            "id": task["id"],
            "title": task["title"],
            "brief_path": task["brief_path"],
            "dependencies": task.get("dependencies", []),
            "allowed_paths": task.get("allowed_paths", []),
            "required_checks": task.get("required_checks", []),
            "state": "initialized",
            "attempt_ids": [],
        })

    return {
        "manifest_id": manifest["manifest_id"],
        "completed_task_ids": manifest.get("completed_task_ids", []),
        "task_entries": task_entries,
    }


# ── Git baseline ─────────────────────────────────────────────────────


def capture_initial_baseline(repository: Path) -> dict[str, Any]:
    """Capture HEAD OID, porcelain status, and untracked paths."""
    head_result = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    head_oid = head_result.stdout.strip()
    if not head_oid:
        raise ValueError("Repository has no HEAD (unborn repository)")
    status = capture_git_status(repository)
    return {
        "head_oid": head_oid,
        "status": status,
    }


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
        top_result = subprocess.run(
            ["git", "-C", str(resolved_repo), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        actual_top = Path(top_result.stdout.strip()).resolve()
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
            "state": "initialized",
            "selected_task_id": None,
            "active_attempt_id": None,
            "last_closure_path": None,
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
        "state": "initialized",
        "ledger_path": str(run_dir / "ledger.json"),
        "baseline_path": str(run_dir / "baselines" / baseline_ref),
    }


# ── Deterministic task selection ──────────────────────────────────────


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def select_task(ledger: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Select the first dependency-ready authorized task in policy order.

    A task is ready when all its dependencies are in completed_task_ids
    or marked as 'accepted' in the ledger.

    Returns the selected task entry or raises ValueError with reasons.
    """
    if ledger["state"] != "initialized":
        raise ValueError(f"Cannot select task from state '{ledger['state']}'")
    if ledger["selected_task_id"] is not None:
        raise ValueError(f"Task already selected: {ledger['selected_task_id']}")
    if ledger["active_attempt_id"] is not None:
        raise ValueError(f"Active attempt exists: {ledger['active_attempt_id']}")

    completed = set(ledger.get("completed_task_ids", []))
    for task in ledger["tasks"]:
        deps = task.get("dependencies", [])
        if all(dep in completed for dep in deps):
            return dict(task)

    ready_ids = [
        task["id"]
        for task in ledger["tasks"]
        if all(dep in completed for dep in task.get("dependencies", []))
    ]
    raise ValueError(
        f"No dependency-ready tasks found. Completed: {sorted(completed)}. "
        f"Task IDs: {[t['id'] for t in ledger['tasks']]}. "
        f"Ready: {ready_ids}"
    )


# ── Ledger update helpers ─────────────────────────────────────────────


def update_ledger(run_dir: Path, updater: dict[str, Any]) -> dict[str, Any]:
    """Read, update, validate, and atomically write the ledger."""
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    _validate_ledger(ledger)
    previous_tasks = {task["id"]: task for task in ledger["tasks"]}
    ledger.update(updater)
    ledger["updated_at"] = _now_iso()
    ledger["revision"] = ledger.get("revision", 1) + 1
    _validate_ledger(ledger)
    next_tasks = {task["id"]: task for task in ledger["tasks"]}
    if next_tasks.keys() != previous_tasks.keys():
        raise ValueError("Ledger task IDs are immutable")
    for task_id, previous in previous_tasks.items():
        prior_attempts = previous["attempt_ids"]
        next_attempts = next_tasks[task_id]["attempt_ids"]
        if next_attempts[:len(prior_attempts)] != prior_attempts:
            raise ValueError(f"Task {task_id} attempt history is append-only")
    atomic_write_json(ledger_path, ledger)
    return ledger


def _validate_ledger(ledger: dict[str, Any]) -> None:
    required = (
        "version", "run_id", "repository", "created_at", "updated_at",
        "revision", "policy_path", "policy_sha256", "manifest_path",
        "manifest_sha256", "initial_baseline_path", "initial_baseline_digest",
        "completed_task_ids", "state", "selected_task_id", "active_attempt_id",
        "last_closure_path", "tasks",
    )
    missing = [f for f in required if f not in ledger]
    if missing:
        raise ValueError(f"Ledger is missing: {', '.join(missing)}")
    if ledger["state"] not in {"initialized", "ready", "running", "awaiting_inspection", "stopped"}:
        raise ValueError(f"Invalid ledger state: {ledger['state']}")
    # Running state requires both selected task and active attempt.
    # Other states must not have both set simultaneously.
    if ledger["state"] == "running":
        if not ledger["selected_task_id"] or not ledger["active_attempt_id"]:
            raise ValueError("'running' state requires both selected_task_id and active_attempt_id")
    else:
        if ledger["selected_task_id"] is not None and ledger["active_attempt_id"] is not None:
            raise ValueError("Cannot have both a selected task and active attempt")
    if ledger["state"] == "initialized":
        if ledger["selected_task_id"] is not None or ledger["active_attempt_id"] is not None:
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
        if task.get("state") not in {
            "initialized", "ready", "running", "awaiting_inspection", "stopped"
        }:
            raise ValueError(f"Invalid task state for {task_id}: {task.get('state')}")
        attempt_ids = task.get("attempt_ids")
        if not isinstance(attempt_ids, list) or len(attempt_ids) != len(set(attempt_ids)):
            raise ValueError(f"Task {task_id} attempt IDs must be a unique array")
        if task_id == ledger["selected_task_id"]:
            selected_task = task
    if ledger["selected_task_id"] is not None and selected_task is None:
        raise ValueError("Selected task is missing from the ledger")
    if ledger["state"] in {"running", "awaiting_inspection"}:
        if selected_task["state"] != ledger["state"]:
            raise ValueError("Selected task state must match the run state")
    if ledger["state"] == "running" and ledger["active_attempt_id"] not in selected_task["attempt_ids"]:
        raise ValueError("Active attempt must appear in the selected task history")


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

    # Compare current HEAD and status with initial baseline before any mutation
    repo = Path(ledger["repository"]).resolve()
    initial_baseline = json.loads(
        (run_dir / "baselines" / ledger["initial_baseline_path"]).read_text()
    )
    current_head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
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
    task_baseline = capture_git_status(repo)
    task_baseline_ref = "task-001.json"
    task_head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    task_index_tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    task_baseline_data = {
        "head_oid": task_head,
        "index_tree": task_index_tree,
        "status": task_baseline,
    }
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
    expected_attempt_dir = run_dir / "attempts" / "attempt-001"
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
        raise ValueError("Stage 2 permits exactly one immutable attempt")

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
    })

    def stop_active_attempt(reason: str) -> int:
        print(reason, file=sys.stderr)
        stopped_tasks = [dict(entry) for entry in ledger["tasks"]]
        next(entry for entry in stopped_tasks if entry["id"] == task["id"])["state"] = "stopped"
        update_ledger(run_dir, {
            "state": "stopped",
            "selected_task_id": None,
            "active_attempt_id": None,
            "tasks": stopped_tasks,
        })
        return 1

    # Launch through worker adapter
    result = subprocess.run(
        adapter_invocation,
        text=True,
        capture_output=True,
    )

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
    current_status = capture_git_status(repo)
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

    closure_dir = run_dir / "closure"
    closure_dir.mkdir(exist_ok=True)

    # Compute full Git evidence
    head_before = task_baseline["head_oid"]
    head_after = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    staged_result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--name-status"],
        check=True,
        capture_output=True,
        text=True,
    )
    unstaged_result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-status"],
        check=True,
        capture_output=True,
        text=True,
    )
    staged_stat_result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--stat"],
        check=True,
        capture_output=True,
        text=True,
    )
    unstaged_stat_result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--stat"],
        check=True,
        capture_output=True,
        text=True,
    )
    untracked_result = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True,
    )
    untracked_paths = (
        sorted(untracked_result.stdout.rstrip("\n").split("\n"))
        if untracked_result.stdout.strip()
        else []
    )
    task_patch_result = subprocess.run(
        [
            "git", "-C", str(repo), "diff", "--binary", head_before, "--",
            *task["allowed_paths"],
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    task_patch = task_patch_result.stdout
    for untracked_path in sorted(set(untracked_paths) & set(task["allowed_paths"])):
        untracked_patch = subprocess.run(
            [
                "git", "-C", str(repo), "diff", "--no-index", "--binary", "--",
                os.devnull, untracked_path,
            ],
            capture_output=True,
            text=True,
        )
        if untracked_patch.returncode not in {0, 1}:
            raise ValueError(
                f"Could not capture patch for untracked allowed path {untracked_path}"
            )
        task_patch += untracked_patch.stdout
    # Compute index tree identity for reconciliation
    index_tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    artifact_contents = {
        "staged_name_status": staged_result.stdout,
        "unstaged_name_status": unstaged_result.stdout,
        "staged_stat": staged_stat_result.stdout,
        "unstaged_stat": unstaged_stat_result.stdout,
        "task_patch": task_patch,
    }
    artifact_paths = {
        "staged_name_status": closure_dir / f"{attempt_id}.staged.name-status.txt",
        "unstaged_name_status": closure_dir / f"{attempt_id}.unstaged.name-status.txt",
        "staged_stat": closure_dir / f"{attempt_id}.staged.stat.txt",
        "unstaged_stat": closure_dir / f"{attempt_id}.unstaged.stat.txt",
        "task_patch": closure_dir / f"{attempt_id}.diff.patch",
    }
    artifact_digests: dict[str, str] = {}
    for name, content in artifact_contents.items():
        atomic_write_text(artifact_paths[name], content)
        artifact_digests[name] = sha256_text(content)

    staged_digest = artifact_digests["staged_name_status"]
    unstaged_digest = artifact_digests["unstaged_name_status"]
    patch_digest = artifact_digests["task_patch"]
    index_tree_digest = sha256_text(index_tree)
    head_changed = head_before != head_after
    index_changed = task_baseline["index_tree"] != index_tree
    mechanical_violations = []
    if head_changed:
        mechanical_violations.append("worker changed HEAD despite commit prohibition")
    if index_changed:
        mechanical_violations.append("worker changed the Git index")
    adapter_state_digest = sha256_text(canonical_json(adapter_state))
    evidence_record = {
        "policy_sha256": ledger["policy_sha256"],
        "manifest_sha256": ledger["manifest_sha256"],
        "baseline_sha256": task_baseline_digest,
        "prompt_sha256": attempt_record["prompt_sha256"],
        "head_before": head_before,
        "head_after": head_after,
        "index_tree_before": task_baseline["index_tree"],
        "index_tree_after": index_tree,
        "artifact_digests": artifact_digests,
        "untracked_paths": untracked_paths,
        "adapter_state_digest": adapter_state_digest,
    }
    evidence_digest = sha256_text(canonical_json(evidence_record))
    baseline_status = task_baseline["status"]
    current_paths = set(current_status)
    baseline_paths = set(baseline_status)
    allowed_paths = set(task["allowed_paths"])
    allowed_changed_paths = sorted(
        path
        for path in current_paths
        if path in allowed_paths
        and (path not in baseline_status or current_status[path] != baseline_status[path])
    )
    unexpected_paths = sorted(current_paths - baseline_paths - allowed_paths)
    disappeared_preexisting_paths = sorted(baseline_paths - current_paths)
    modified_preexisting_paths = sorted(
        path
        for path in baseline_paths & current_paths
        if baseline_status[path] != current_status[path]
    )

    # Build the complete closure packet
    closure_packet = {
        "run_id": policy["run_id"],
        "task_id": task["id"],
        "attempt_id": attempt_id,
        "policy_sha256": ledger["policy_sha256"],
        "manifest_sha256": ledger["manifest_sha256"],
        "baseline_sha256": task_baseline_digest,
        "prompt_sha256": attempt_record.get("prompt_sha256"),
        "head_before": head_before,
        "head_after": head_after,
        "index_tree": index_tree,
        "index_tree_digest": index_tree_digest,
        "staged_changes": staged_result.stdout.strip(),
        "staged_digest": staged_digest,
        "unstaged_changes": unstaged_result.stdout.strip(),
        "unstaged_digest": unstaged_digest,
        "untracked_paths": untracked_paths,
        "task_patch": task_patch,
        "task_patch_digest": patch_digest,
        "staged_stat_digest": artifact_digests["staged_stat"],
        "unstaged_stat_digest": artifact_digests["unstaged_stat"],
        "evidence_digest": evidence_digest,
        "adapter_state_digest": adapter_state_digest,
        "evidence_artifacts": {
            name: {
                "path": str(path.relative_to(run_dir)),
                "sha256": artifact_digests[name],
            }
            for name, path in artifact_paths.items()
        },
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
        "controller_observations": {
            "head_changed": head_changed,
            "index_changed": index_changed,
            "mechanical_violations": mechanical_violations,
            "allowed_changed_paths": allowed_changed_paths,
            "unexpected_paths": unexpected_paths,
            "disappeared_preexisting_paths": disappeared_preexisting_paths,
            "modified_preexisting_paths": modified_preexisting_paths,
            "staged_changes": staged_result.stdout.strip(),
            "staged_digest": staged_digest,
            "unstaged_changes": unstaged_result.stdout.strip(),
            "unstaged_digest": unstaged_digest,
            "untracked_paths": untracked_paths,
            "index_tree": index_tree,
            "index_tree_digest": index_tree_digest,
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
    closure_json_path = closure_dir / f"{attempt_id}.json"
    atomic_write_json(closure_json_path, closure_packet)

    awaiting_tasks = [dict(entry) for entry in ledger["tasks"]]
    next(entry for entry in awaiting_tasks if entry["id"] == task["id"])["state"] = "awaiting_inspection"
    update_ledger(run_dir, {
        "state": "awaiting_inspection",
        "selected_task_id": task["id"],
        "active_attempt_id": None,
        "last_closure_path": str(closure_json_path.relative_to(run_dir)),
        "tasks": awaiting_tasks,
    })

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
