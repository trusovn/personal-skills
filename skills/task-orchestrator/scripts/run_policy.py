"""Explicit run permissions, verification settings and policy validation.

Uses flow-policy and shared record predicates; task graph validation, ledger
updates and execution-record validation have separate owners."""

from __future__ import annotations

from typing import Any

from .flow_policy import (
    validate_flow_profile,
)
from .record_validation import (
    validate_bool,
    validate_str,
    validate_str_array,
)


def _validate_non_empty_object_keys(obj: dict[str, Any], prefix: str) -> None:
    for key in obj:
        validate_str(key, f"{prefix}.{key}")


def _validate_verification(verification: dict[str, Any]) -> None:
    if not isinstance(verification, dict):
        raise ValueError("verification must be an object")
    required = ("targeted_checks", "repository_gate", "authorized_gap")
    missing = [field for field in required if field not in verification]
    if missing:
        raise ValueError(f"verification is missing: {', '.join(missing)}")
    validate_str_array(verification["targeted_checks"], "verification.targeted_checks")
    if verification["repository_gate"] is not None:
        validate_str(verification["repository_gate"], "verification.repository_gate")
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
            validate_str(authorized_gap[field], f"verification.authorized_gap.{field}")
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
    validate_bool(permissions["network"], "permissions.network")
    validate_bool(permissions["dependency_install"], "permissions.dependency_install")
    validate_str_array(permissions["writable_roots"], "permissions.writable_roots", allow_empty=True)
    validate_bool(permissions["danger_full_access_authorized"], "permissions.danger_full_access_authorized")
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
        "commit_policy", "stop_policy", "flow", "execution_authorization",
    )
    missing = [field for field in required if field not in policy]
    if missing:
        raise ValueError(f"Run policy is missing: {', '.join(missing)}")
    if type(policy["version"]) is not int or policy["version"] != 2:
        raise ValueError("Unsupported run policy version")
    validate_str(policy["run_id"], "run_id")
    validate_str(policy["repository"], "repository")
    validate_str_array(policy["task_ids"], "task_ids")
    if len(policy["task_ids"]) != 1:
        raise ValueError("Run policy must authorize exactly one prepared task")
    if policy["execution_authorization"] != {
        "transport": "sbx", "yolo": True, "intervention": "active_chat",
    } or policy["execution_authorization"].get("yolo") is not True:
        raise ValueError("Explicit sbx/YOLO authorization and active-chat intervention are required")
    _validate_verification(policy["verification"])
    _validate_permissions(policy["permissions"])
    _validate_commit_policy(policy["commit_policy"])
    _validate_stop_policy(policy["stop_policy"])
    if "flow" in policy:
        validate_flow_profile(policy["flow"])
    unknown = set(policy) - {*required, "flow"}
    if unknown:
        raise ValueError(f"Run policy contains unknown top-level fields: {', '.join(sorted(unknown))}")
