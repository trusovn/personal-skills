"""Shared application record access and ledger projections.

Owns operation lookup, observed-result binding, retained-byte checks and ledger
replacement under a caller-owned lock. It never selects work or acquires locks.
Dependencies: ledger rules, record predicates and run storage; no application workflow imports.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from . import ledger as ledger_rules
from . import record_validation
from . import run_storage as storage


def now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def active_actor(ledger: dict[str, Any]) -> dict[str, Any] | None:
    return next((operation for operation in ledger.get("actor_operations", [])
                 if operation["state"] != "terminal"), None)


def current_readiness(ledger: dict[str, Any]) -> bool:
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


def evidence_view(ledger: dict[str, Any], stage: str) -> dict[str, Any]:
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


def actor_operation(ledger: dict[str, Any], operation_id: str) -> dict[str, Any]:
    operation = next((item for item in ledger.get("actor_operations", [])
                      if item["operation_id"] == operation_id), None)
    if operation is None:
        raise ValueError("Unknown reserved operation")
    return operation


def save_actor_ledger(run_dir: Path, ledger: dict[str, Any]) -> None:
    ledger.update(revision=ledger["revision"] + 1, updated_at=now_iso())
    ledger_rules.validate_ledger(ledger)
    storage.atomic_write_json(run_dir / "ledger.json", ledger)


def actor_directory(run_dir: Path, operation: dict[str, Any]) -> Path:
    return run_dir / "actors" / operation["operation_id"]


def same_typed_assignment(value: Any, expected: Any) -> bool:
    """Compare to validated ledger authority without Python bool/number coercion."""
    if type(value) is not type(expected):
        return False
    if isinstance(expected, dict):
        return (value.keys() == expected.keys()
                and all(same_typed_assignment(value[key], item)
                        for key, item in expected.items()))
    return value == expected


def validate_observed_result(assignment: dict[str, Any], observed: dict[str, Any], result: dict[str, Any]) -> None:
    expected = {"assignment", "session_id", "status", "summary", "readiness"}
    if assignment["stage"] == "semantic_review":
        expected.add("collection")
    if assignment["stage"] == "acceptance":
        expected.add("decision")
    if set(result) != expected:
        raise ValueError("Malformed actor result")
    if not same_typed_assignment(result["assignment"], assignment):
        raise ValueError("Result assignment mismatch")
    if not observed.get("thread_id") or result["session_id"] not in (None, observed["thread_id"]):
        raise ValueError("Result session mismatch or missing observed session")
    if result["status"] not in {"complete", "blocked", "failed", "needs_input"} or not isinstance(result["summary"], str):
        raise ValueError("Invalid result status/summary")


def read_actor_observation(directory: Path, operation: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Only the adapter's exclusive terminal receipt proves a reaped child."""
    terminal = directory / "result.state.json"
    path = terminal if terminal.exists() else directory / "state.json"
    if not path.exists():
        return {}, False
    try:
        observed = storage.read_json(path)
    except json.JSONDecodeError:
        # An exclusive receipt path can be visible before its bytes are complete.
        # Missing terminal proof remains unresolved; never admit or relaunch.
        return {}, False
    transport = operation["transport"]
    if not same_typed_assignment(observed.get("assignment"), operation["assignment"]) or observed.get("configuration_sha256") != transport["configuration_sha256"]:
        raise ValueError("Transport observation binding mismatch")
    terminality = (terminal.exists() and observed.get("terminal_observed") is True
                   and observed.get("group_absent") is True)
    return observed, terminality


def retained_bytes(run_dir, relative, digest):
    if not isinstance(relative, str) or not record_validation.is_valid_repo_relative_path(relative):
        raise ValueError('Invalid retained evidence path')
    path = run_dir / relative
    if not path.resolve().is_relative_to(run_dir.resolve()):
        raise ValueError('Evidence escapes run directory')
    raw = path.read_bytes()
    if sha256_bytes(raw) != digest:
        raise ValueError('Retained evidence changed: ' + relative)
    return raw


def retained_json(run_dir, relative, digest):
    return json.loads(retained_bytes(run_dir, relative, digest))

