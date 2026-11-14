"""Ledger consistency, task/run transitions and authorized in-memory updates.

validate_ledger is the composition point for ownership, actor reservations,
input-revision history and closure/finalization references. These cross-record
invariants stay together. Uses flow/run policy, manifest structure and shared
record primitives; no I/O, publication or application-workflow dependencies."""

from __future__ import annotations

import json
from typing import Any

from .flow_policy import (
    ACTOR_LEVELS,
    FLOW_STEP_ORDER,
    FLOW_STEP_ROLES,
    transition_flow_cursor,
    validate_flow_cursor,
)
from .record_serialization import (
    canonical_json,
    sha256_text,
)
from .record_validation import (
    validate_exact_object,
    validate_sha256,
    validate_str,
    validate_str_array,
)
from .run_policy import (
    validate_run_policy,
)
from .task_manifest import (
    validate_task_manifest_structure,
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


ALLOWED_RUN_TRANSITIONS = {
    "initialized": {"ready", "stopped"},
    "ready": {"running", "stopped"},
    "running": {"awaiting_inspection", "resumable", "stopped"},
    "awaiting_inspection": {"resumable", "finalizing", "stopped"},
    "resumable": {"running", "stopped"},
    "finalizing": {"ready", "stopped"},
    "stopped": set(),
}


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


def transition_run(current: str, requested: str) -> str:
    if current not in ALLOWED_RUN_TRANSITIONS:
        raise ValueError(f"Unknown run state: {current}")
    if requested not in ALLOWED_RUN_TRANSITIONS[current]:
        raise ValueError(f"Run transition {current} -> {requested} is not allowed")
    return requested


def validate_actor_transport(operation: dict[str, Any]) -> None:
    transport = operation["transport"]
    validate_exact_object(transport, ("configuration_sha256", "supervisor_pid", "outcome"), "actor transport")
    validate_sha256(transport["configuration_sha256"], "transport configuration")
    pid = transport["supervisor_pid"]
    if pid is not None and (type(pid) is not int or pid <= 0):
        raise ValueError("Invalid supervisor identity")
    outcome = transport["outcome"]
    if outcome is not None:
        validate_exact_object(outcome, ("observed", "blocker", "raw_result_path", "terminal_path"), "actor outcome")
        if operation["state"] != "terminal":
            raise ValueError("Outcome requires terminal operation")
        observed = outcome["observed"]
        if not isinstance(observed, dict) or observed.get("assignment") != operation["assignment"]:
            raise ValueError("Outcome assignment mismatch")
        if observed.get("terminal_observed") is not True or observed.get("group_absent") is not True:
            raise ValueError("Outcome requires observed process/group terminality")
    if operation["state"] == "reserved":
        raise ValueError("Launch intent cannot remain reserved")


def validate_actor_operations(ledger: dict[str, Any]) -> None:
    operations = ledger.get("actor_operations", [])
    if not isinstance(operations, list):
        raise ValueError("actor_operations must be an array")
    active = []
    keys = set()
    count = 0
    for index, operation in enumerate(operations, 1):
        validate_exact_object({k: v for k, v in operation.items() if k != "transport"}, ("operation_id", "state", "request", "assignment"), "actor operation")
        if "transport" in operation:
            validate_actor_transport(operation)
        operation_id = f"operation-{index:03d}"
        if operation["operation_id"] != operation_id or operation["state"] not in {"reserved", "running", "unknown", "terminal"}:
            raise ValueError("Invalid actor operation identity/state")
        request = operation["request"]
        validate_exact_object(request, ("expected_version", "task_id", "stage", "role", "operation_key", "reason"), "reservation request")
        if type(request["expected_version"]) is not int or request["expected_version"] < 1:
            raise ValueError("Invalid reservation version")
        for field in ("task_id", "stage", "role", "operation_key", "reason"):
            validate_str(request[field], f"reservation {field}")
        if request["operation_key"] in keys:
            raise ValueError("Repeated operation key")
        keys.add(request["operation_key"])
        assignment = operation["assignment"]
        validate_exact_object(assignment, (
            "run_id", "task_id", "operation_id", "operation_key", "stage", "role", "reason",
            "inputs_sha256", "policy_sha256", "flow_sha256", "flow_revision",
            "candidate_sha256", "correction_count", "can_repair", "can_change_files", "actor", "session_policy",
        ), "assignment")
        if any(assignment[field] != request[field] for field in ("task_id", "operation_key", "stage", "role", "reason")) or assignment["operation_id"] != operation_id or assignment["run_id"] != ledger["run_id"]:
            raise ValueError("Assignment identity mismatch")
        stage = assignment["stage"]
        role = "implementer" if stage == "correction" else FLOW_STEP_ROLES.get(stage)
        if stage not in {"preflight", "implement", "correction", "verify", "semantic_review", "acceptance"} or assignment["role"] != role:
            raise ValueError("Invalid assignment stage/role")
        if assignment["task_id"] not in {task["id"] for task in ledger["tasks"]}:
            raise ValueError("Assignment task is outside the run")
        if type(assignment["flow_revision"]) is not int or assignment["flow_revision"] < 1:
            raise ValueError("Invalid assignment flow revision")
        if (stage == "verify" and assignment["actor"] is not None) or (
            stage != "verify" and assignment["actor"] not in ACTOR_LEVELS.values()
        ):
            raise ValueError("Invalid assignment actor profile")
        correction = stage == "correction"
        if assignment["session_policy"] != ("fresh" if correction else None):
            raise ValueError("Invalid assignment session policy")
        if assignment["reason"] not in ({"check_failed", "review_findings", "environment_repair"} if correction else {"initial", "retry"}):
            raise ValueError("Invalid assignment reason")
        count += int(correction)
        if type(assignment["correction_count"]) is not int or assignment["correction_count"] != count or count > 3:
            raise ValueError("Assignment correction accounting mismatch")
        if assignment["can_repair"] is not (correction and assignment["reason"] == "environment_repair") or assignment["can_change_files"] is not (stage in {"implement", "correction"}):
            raise ValueError("Assignment write authority mismatch")
        for field in ("inputs_sha256", "policy_sha256", "flow_sha256"):
            validate_sha256(assignment[field], f"assignment {field}")
        if assignment["candidate_sha256"] is not None:
            validate_sha256(assignment["candidate_sha256"], "assignment candidate")
        if operation["state"] != "terminal":
            active.append(operation)
            if index != len(operations) or any(assignment[field] != ledger.get(field) for field in (
                "inputs_sha256", "policy_sha256", "flow_sha256", "flow_revision", "candidate_sha256",
            )):
                raise ValueError("Active assignment authority mismatch")
            if assignment["task_id"] != ledger["selected_task_id"] or stage != ledger["current_step"]:
                raise ValueError("Active assignment task/stage mismatch")
    if operations and ledger["correction_cycle"] != count:
        raise ValueError("Persisted correction count contradicts reservations")
    if len(active) > 1:
        raise ValueError("Only one active actor operation is permitted")
    path = ledger["active_operation_path"]
    if active and (path != f"actor_operations/{active[0]['operation_id']}" or ledger["state"] not in {
        "ready", "running", "awaiting_inspection", "resumable",
    }):
        raise ValueError("Active operation pointer/state mismatch")
    if not active and (path or "").startswith("actor_operations/"):
        raise ValueError("Active operation pointer has no owner")
    if ledger.get("correction_request") not in {None, "check_failed", "review_findings", "environment_repair"}:
        raise ValueError("Invalid correction authorization")
    for item in ledger.get("evidence", {}).values():
        if item.get("status") not in {"passed", "failed", "stale", "blocked", "missing", "not_run", "omitted_by_policy"}:
            raise ValueError("Invalid evidence status")


def validate_input_revision_request(request: dict[str, Any]) -> None:
    """Validate a trusted caller's explicit owner decision, bound to its change.

    This records authority supplied by the coordinator; it does not authenticate
    external identities or turn actor output into an owner response.
    """
    validate_exact_object(request, ("expected_version", "task_id", "revision_key", "payload", "authorization"), "input revision")
    if type(request["expected_version"]) is not int or request["expected_version"] < 1:
        raise ValueError("Invalid input revision version")
    for field in ("task_id", "revision_key"):
        validate_str(request[field], field)
    payload = request["payload"]
    validate_exact_object(payload, ("policy", "manifest", "documents"), "revision payload")
    validate_run_policy(payload["policy"])
    validate_task_manifest_structure(payload["manifest"])
    validate_exact_object(payload["documents"], ("brief", "verification"), "revision documents")
    for name, content in payload["documents"].items():
        validate_str(content, f"revision {name}")
    authorization = request["authorization"]
    validate_exact_object(authorization, ("kind", "decision", "owner", "provenance", "request_sha256"), "revision authorization")
    if authorization["kind"] != "owner_response" or authorization["decision"] != "authorize_input_revision":
        raise ValueError("Explicit owner revision authority required")
    for field in ("owner", "provenance"):
        validate_str(authorization[field], f"authorization {field}")
    bound = {field: value for field, value in request.items() if field != "authorization"}
    if authorization["request_sha256"] != sha256_text(canonical_json(bound)):
        raise ValueError("Owner authority does not bind the requested revision")


def validate_input_revisions(ledger: dict[str, Any]) -> None:
    revisions = ledger.get("input_revisions", [])
    if not isinstance(revisions, list):
        raise ValueError("input_revisions must be an array")
    keys = set()
    for index, receipt in enumerate(revisions, 1):
        validate_exact_object(receipt, ("request", "path", "sha256", "inputs_sha256", "state_version", "previous"), "input revision receipt")
        validate_input_revision_request(receipt["request"])
        key = receipt["request"]["revision_key"]
        if key in keys or receipt["path"] != f"input-revisions/revision-{index:03d}.json":
            raise ValueError("Invalid input revision history")
        keys.add(key)
        for field in ("sha256", "inputs_sha256"):
            validate_sha256(receipt[field], f"revision {field}")
        if receipt["state_version"] != receipt["request"]["expected_version"] + 1 or receipt["state_version"] > ledger["revision"]:
            raise ValueError("Invalid input revision publication version")
        if not isinstance(receipt["previous"], dict) or receipt["previous"].get("revision") != receipt["request"]["expected_version"]:
            raise ValueError("Invalid previous input authority")
    if revisions and any(ledger[field] != revisions[-1]["path"] for field in ("policy_path", "manifest_path", "flow_path")):
        raise ValueError("Current input revision paths contradict history")
    if revisions and ledger.get("inputs_sha256") != revisions[-1]["inputs_sha256"]:
        raise ValueError("Current input identity contradicts revision history")


def _validate_ledger_header(ledger: dict[str, Any]) -> None:
    required = (
        "version", "run_id", "repository", "created_at", "updated_at", "revision", "policy_path",
        "policy_sha256", "manifest_path", "manifest_sha256", "initial_baseline_path",
        "initial_baseline_digest", "completed_task_ids", "state", "selected_task_id",
        "active_attempt_id", "last_closure_path", "tasks",
        "last_verification_path", "last_decision_path", "active_operation_path",
        "current_step", "correction_cycle", "flow_revision", "flow_path",
        "flow_sha256",
    )
    missing = [field for field in required if field not in ledger]
    if missing:
        raise ValueError(f"Ledger is missing: {', '.join(missing)}")
    _validate_ledger_flow_reference(ledger)
    if ledger["state"] not in ALLOWED_RUN_TRANSITIONS:
        raise ValueError(f"Invalid ledger state: {ledger['state']}")
    if type(ledger["revision"]) is not int or ledger["revision"] < 1:
        raise ValueError("Ledger revision must be a positive integer")


def _validate_ledger_flow_reference(ledger: dict[str, Any]) -> None:
    if type(ledger["flow_revision"]) is not int or ledger["flow_revision"] < 1:
        raise ValueError("Ledger flow_revision must be a positive integer")
    if not ledger.get("input_revisions") and ledger["flow_path"] != f"flows/flow-{ledger['flow_revision']:03d}.json":
        raise ValueError("Ledger flow_path does not match flow_revision")
    validate_sha256(ledger["flow_sha256"], "flow_sha256")


def _validate_ledger_cursor_fields(ledger: dict[str, Any]) -> None:
    if ledger["current_step"] is not None and ledger["current_step"] not in {
        *FLOW_STEP_ORDER, "correction",
    }:
        raise ValueError("Ledger current_step is invalid")
    if type(ledger["correction_cycle"]) is not int or ledger["correction_cycle"] < 0:
        raise ValueError("Ledger correction_cycle must be a non-negative integer")
    validate_str_array(
        ledger["completed_task_ids"], "completed_task_ids", allow_empty=True
    )


def _validate_ledger_closure_references(ledger: dict[str, Any]) -> None:
    for field in (
        "last_closure_path", "last_verification_path", "last_decision_path",
        "active_operation_path",
    ):
        if ledger[field] is not None:
            validate_str(ledger[field], field)
    closure_sha256 = ledger.get("last_closure_sha256")
    if closure_sha256 is not None:
        validate_sha256(closure_sha256, "last_closure_sha256")
    if bool(ledger["last_closure_path"]) != bool(closure_sha256):
        raise ValueError("closure reference requires an exact closure digest")
    if ledger["last_verification_path"] and not ledger["last_closure_path"]:
        raise ValueError("verification reference requires closure reference")
    if ledger["last_decision_path"] and not ledger["last_verification_path"]:
        raise ValueError("decision reference requires verification reference")


def _validate_ledger_tasks(ledger: dict[str, Any]) -> dict[str, Any] | None:
    task_ids: set[str] = set()
    selected_task = None
    for task in ledger["tasks"]:
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id or task_id in task_ids:
            raise ValueError("Ledger task IDs must be non-empty and unique")
        task_ids.add(task_id)
        if task.get("state") not in ALLOWED_TASK_TRANSITIONS:
            raise ValueError(f"Invalid task state for {task_id}: {task.get('state')}")
        attempts = task.get("attempt_ids")
        if not isinstance(attempts, list) or len(attempts) != len(set(attempts)):
            raise ValueError(f"Task {task_id} attempt IDs must be a unique array")
        if task_id == ledger["selected_task_id"]:
            selected_task = task
    return selected_task


def _ledger_attempt_owners(ledger: dict[str, Any]) -> dict[str, str]:
    attempt_owners: dict[str, str] = {}
    for task in ledger["tasks"]:
        for attempt_id in task["attempt_ids"]:
            if attempt_id in attempt_owners:
                raise ValueError("Attempt IDs must have exactly one task owner")
            attempt_owners[attempt_id] = task["id"]
    return attempt_owners


def _validate_ledger_task_ownership(
    ledger: dict[str, Any], selected_task: dict[str, Any] | None,
) -> None:
    state = ledger["state"]
    ownership_states = {"running", "awaiting_inspection", "resumable"}
    if state == "stopped" and any(
        task["state"] in ownership_states for task in ledger["tasks"]
    ):
        raise ValueError("'stopped' state cannot retain an active task state")
    if any(
        task["state"] in ownership_states and task is not selected_task
        for task in ledger["tasks"]
    ):
        raise ValueError("Only the selected task may have an ownership-bearing state")


def _validate_ledger_selection(ledger: dict[str, Any]) -> None:
    state = ledger["state"]
    if state in {"initialized", "stopped"}:
        if ledger["selected_task_id"] is not None or ledger["active_attempt_id"] is not None:
            raise ValueError(f"'{state}' state must have neither selected_task_id nor active_attempt_id")
    if ledger["selected_task_id"] is None:
        if ledger["current_step"] is not None or ledger["correction_cycle"] != 0:
            raise ValueError("A run without a selected task requires a null cycle-zero cursor")
    elif ledger["current_step"] is None:
        raise ValueError("A selected task requires a current flow step")


def _validate_idle_ledger(ledger: dict[str, Any]) -> None:
    state = ledger["state"]
    if state == "ready" and ledger["active_attempt_id"] is not None:
        raise ValueError("'ready' state cannot have an active attempt")
    if state == "initialized" and any(
        ledger[field] is not None for field in (
            "last_closure_path", "last_verification_path", "last_decision_path",
            "active_operation_path",
        )
    ):
        raise ValueError("'initialized' state requires null Stage 3 references")


def _validate_ready_ledger(ledger: dict[str, Any]) -> None:
    completed = set(ledger["completed_task_ids"])
    completed.update(
        task["id"] for task in ledger["tasks"] if task["state"] == "accepted"
    )
    ready_ids = set()
    expected_ready_ids = set()
    for task in ledger["tasks"]:
        if task["state"] == "ready":
            ready_ids.add(task["id"])
        if task["state"] not in {"accepted", "stopped"} and all(
            dependency in completed for dependency in task["dependencies"]
        ):
            expected_ready_ids.add(task["id"])
    if not ready_ids or ready_ids != expected_ready_ids:
        raise ValueError(
            "'ready' state requires exactly the dependency-ready unfinished tasks"
        )


def _validate_running_ledger(
    ledger: dict[str, Any], selected_task: dict[str, Any] | None,
    attempt_owners: dict[str, str],
) -> None:
    if not ledger["selected_task_id"] or not ledger["active_attempt_id"]:
        raise ValueError("'running' state requires both selected_task_id and active_attempt_id")
    if selected_task["state"] != "running":
        raise ValueError("Selected task must be running")
    if attempt_owners.get(ledger["active_attempt_id"]) != selected_task["id"]:
        raise ValueError("Active attempt must appear only in the selected task history")
    if selected_task["attempt_ids"][-1] != ledger["active_attempt_id"]:
        raise ValueError("Active attempt must be the latest selected task attempt")


def _validate_closed_attempt_ledger(
    ledger: dict[str, Any], selected_task: dict[str, Any] | None,
) -> None:
    state = ledger["state"]
    if not ledger["selected_task_id"]:
        raise ValueError(f"'{state}' requires selected_task_id")
    if ledger["active_attempt_id"] is not None:
        raise ValueError(f"'{state}' must have no active_attempt_id")
    expected_task_state = "awaiting_inspection" if state == "finalizing" else state
    if selected_task["state"] != expected_task_state:
        raise ValueError(f"Selected task state is incoherent with '{state}'")
    if not selected_task["attempt_ids"]:
        raise ValueError(f"'{state}' requires a current attempt in task history")


def _validate_ledger_finalization_references(ledger: dict[str, Any], actor_path: bool) -> None:
    state = ledger["state"]
    if state in {"awaiting_inspection", "finalizing"} and not ledger["last_closure_path"]:
        raise ValueError(f"'{state}' requires last_closure_path")
    if state == "finalizing" and not all(
        ledger[field] for field in (
            "last_closure_path", "last_verification_path", "last_decision_path",
            "active_operation_path",
        )
    ):
        raise ValueError("'finalizing' requires closure, verification, decision, and operation references")
    if state != "finalizing" and ledger["active_operation_path"] is not None and not actor_path:
        raise ValueError("active_operation_path is only valid while finalizing")


def validate_ledger(ledger: dict[str, Any]) -> None:
    """Validate record shape, ownership, then the selected run state's rules."""
    _validate_ledger_header(ledger)
    validate_input_revisions(ledger)
    _validate_ledger_cursor_fields(ledger)
    _validate_ledger_closure_references(ledger)
    actor_path = (ledger["active_operation_path"] or "").startswith("actor_operations/")
    validate_actor_operations(ledger)
    if ledger["active_operation_path"] and not actor_path and not ledger["last_decision_path"]:
        raise ValueError("operation reference requires decision reference")
    selected_task = _validate_ledger_tasks(ledger)
    attempt_owners = _ledger_attempt_owners(ledger)
    if ledger["selected_task_id"] is not None and selected_task is None:
        raise ValueError("Selected task is missing from the ledger")
    _validate_ledger_task_ownership(ledger, selected_task)
    _validate_ledger_selection(ledger)
    _validate_idle_ledger(ledger)
    state = ledger["state"]
    if state == "ready":
        _validate_ready_ledger(ledger)
    if state == "running":
        _validate_running_ledger(ledger, selected_task, attempt_owners)
    if state in {"awaiting_inspection", "resumable", "finalizing"}:
        _validate_closed_attempt_ledger(ledger, selected_task)
    _validate_ledger_finalization_references(ledger, actor_path)


def apply_ledger_update(
    ledger: dict[str, Any], updater: dict[str, Any], updated_at: str, *,
    expected_revision: int, closure_decision: dict[str, Any] | None = None,
    flow: dict[str, Any] | None = None, cursor_action: str | None = None,
    cursor_result: str | None = None,
) -> dict[str, Any]:
    next_ledger = json.loads(json.dumps(ledger))
    validate_ledger(next_ledger)
    if expected_revision != next_ledger["revision"]:
        raise ValueError(
            f"Expected ledger revision {expected_revision}, found {next_ledger['revision']}"
        )
    if set(updater) & {"actor_operations", "readiness", "correction_request", "candidate_sha256", "candidate_path", "evidence", "outstanding_findings"}:
        raise ValueError("Actor admission fields are controller-owned")
    if ledger.get("actor_operations") and set(updater) & {"current_step", "correction_cycle", "active_operation_path"}:
        raise ValueError("Actor reservation cursor is controller-owned")
    if "revision" in updater:
        raise ValueError("Ledger revision is controller-owned")
    previous_tasks = next_ledger["tasks"]
    previous_cursor = {
        "current_step": next_ledger["current_step"],
        "correction_cycle": next_ledger["correction_cycle"],
    }
    if flow is not None:
        validate_flow_cursor(flow, previous_cursor)
    immutable_top_level = (
        "version", "run_id", "repository", "created_at", "policy_path", "policy_sha256",
        "manifest_path", "manifest_sha256", "initial_baseline_path",
        "initial_baseline_digest", "inputs_sha256", "completed_task_ids", "flow_revision",
        "flow_path", "flow_sha256", "input_revisions",
    )
    next_ledger.update(updater)
    next_ledger["updated_at"] = updated_at
    next_ledger["revision"] = ledger["revision"] + 1
    validate_ledger(next_ledger)
    if any(next_ledger.get(field) != ledger.get(field) for field in immutable_top_level):
        raise ValueError("Ledger authority is immutable")
    next_cursor = {
        "current_step": next_ledger["current_step"],
        "correction_cycle": next_ledger["correction_cycle"],
    }
    if flow is not None:
        validate_flow_cursor(flow, next_cursor)
    if next_cursor != previous_cursor:
        if cursor_action == "task_boundary":
            expected_cursor = {"current_step": None, "correction_cycle": 0}
        elif flow is not None and cursor_action is not None:
            expected_cursor = transition_flow_cursor(
                flow, previous_cursor, cursor_action, result=cursor_result
            )
        else:
            raise ValueError("Flow cursor is controller-owned")
        if next_cursor != {
            "current_step": expected_cursor["current_step"],
            "correction_cycle": expected_cursor["correction_cycle"],
        }:
            raise ValueError("Flow cursor update contradicts the persisted flow")
    next_tasks = next_ledger["tasks"]
    if [task["id"] for task in next_tasks] != [task["id"] for task in previous_tasks]:
        raise ValueError("Ledger task IDs are immutable")
    immutable_task_fields = (
        "id", "title", "brief_path", "dependencies", "allowed_paths", "required_checks",
    )
    for previous, current in zip(previous_tasks, next_tasks):
        task_id = previous["id"]
        if any(current[field] != previous[field] for field in immutable_task_fields):
            raise ValueError(f"Task {task_id} authority is immutable")
        attempts = current["attempt_ids"]
        if (
            current["state"] == "accepted"
            and previous["state"] != "accepted"
            and attempts != previous["attempt_ids"]
        ):
            raise ValueError(
                f"Task {task_id} acceptance cannot append or replace attempt history"
            )
        if attempts[:len(previous["attempt_ids"])] != previous["attempt_ids"]:
            raise ValueError(f"Task {task_id} attempt history is append-only")
    if next_ledger["state"] != ledger["state"]:
        transition_run(ledger["state"], next_ledger["state"])
    for previous, current in zip(previous_tasks, next_tasks):
        if current["state"] == previous["state"]:
            continue
        expected_identity = None
        if current["state"] == "accepted":
            if previous["attempt_ids"]:
                expected_identity = {
                    "run_id": ledger["run_id"],
                    "task_id": previous["id"],
                    "attempt_id": previous["attempt_ids"][-1],
                }
        transition_task(
            previous["state"], current["state"],
            closure_decision=closure_decision,
            expected_identity=expected_identity,
        )
    return next_ledger
