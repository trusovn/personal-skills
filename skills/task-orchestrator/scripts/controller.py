#!/usr/bin/env python3
"""Small Stage 1 policy, prompt, attempt, and closure primitives."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


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


def validate_run_policy(policy: dict[str, Any]) -> None:
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
    if policy["version"] != 1:
        raise ValueError("Unsupported run policy version")
    if not policy["task_ids"]:
        raise ValueError("Run policy requires at least one task id")
    permissions = policy["permissions"]
    sandbox = permissions.get("sandbox")
    if sandbox not in {"read-only", "workspace-write", "danger-full-access"}:
        raise ValueError(f"Unsupported sandbox: {sandbox}")
    if permissions.get("approval_policy") != "never":
        raise ValueError("Stage 1 requires approval_policy=never")
    if sandbox == "danger-full-access" and not permissions.get(
        "danger_full_access_authorized"
    ):
        raise ValueError("danger-full-access requires exact persisted authorization")
    if policy["commit_policy"].get("mode") not in {
        "off",
        "controller_exact_paths",
    }:
        raise ValueError("Unsupported commit policy")


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
) -> str:
    if current not in ALLOWED_TASK_TRANSITIONS:
        raise ValueError(f"Unknown task state: {current}")
    if requested not in ALLOWED_TASK_TRANSITIONS[current]:
        raise ValueError(f"Task transition {current} -> {requested} is not allowed")
    if requested == "accepted" and not (closure_decision or {}).get("accepted"):
        raise ValueError("Acceptance requires an accepting closure decision")
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
) -> dict[str, Any]:
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
        verification = {
            item.get("command"): item.get("outcome")
            for item in result.get("verification", [])
            if isinstance(item, dict)
        }
        required = list(policy["verification"]["targeted_checks"])
        repository_gate = policy["verification"].get("repository_gate")
        if repository_gate:
            required.append(repository_gate)
        for command in required:
            if verification.get(command) == "passed":
                continue
            if command == repository_gate and policy["verification"].get("authorized_gap"):
                continue
            reasons.append(f"required verification did not pass: {command}")
        if any(question.get("blocking") for question in result.get("questions", [])):
            reasons.append("worker result contains a blocking question")
        if result.get("risks"):
            reasons.append("worker result contains unresolved risks")

    accepted = not reasons
    allowed_transitions = ["accepted"] if accepted else ["resumable", "stopped"]
    allowed_actions = ["record_acceptance"] if accepted else ["inspect", "resume", "stop"]
    if accepted and policy["commit_policy"]["mode"] == "controller_exact_paths":
        allowed_actions.append("commit_exact_paths")
    return {
        "accepted": accepted,
        "reasons": reasons,
        "unexpected_paths": unexpected_paths,
        "observed_paths": sorted(current_status or {}),
        "allowed_transitions": allowed_transitions,
        "allowed_actions": allowed_actions,
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
    run_dir.mkdir(parents=True, exist_ok=True)
    attempt_number = 1
    while (run_dir / f"attempt-{attempt_number:03d}").exists():
        attempt_number += 1
    attempt_dir = run_dir / f"attempt-{attempt_number:03d}"
    attempt_dir.mkdir()
    persisted = dict(record)
    prompt = persisted.pop("prompt", "")
    persisted["attempt_number"] = attempt_number
    with (attempt_dir / "record.json").open("x") as stream:
        stream.write(json.dumps(persisted, indent=2, sort_keys=True) + "\n")
    with (attempt_dir / "prompt.txt").open("x") as stream:
        stream.write(prompt)
    return attempt_dir
