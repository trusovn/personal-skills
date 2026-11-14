"""Closed flow profiles, actor roles, cursor transitions and handoff envelopes.

Owns session-reuse rules and structured step outcomes. Depends only on shared
record predicates; run permissions, execution records and ledger consistency
belong to their respective owners."""

from __future__ import annotations

import json
import math
from typing import Any

from .record_validation import (
    validate_exact_object,
    validate_run_relative_reference,
    validate_sha256,
    validate_str,
    validate_str_array,
)


ACTOR_LEVELS = {
    "light": {"model": "gpt-6.1-sol", "reasoning": "low"},
    "standard": {"model": "gpt-6.1-sol", "reasoning": "medium"},
    "strong": {"model": "gpt-6.1-sol", "reasoning": "high"},
}


IMPLEMENTATION_SESSION_REUSE_THRESHOLD = 0.5


FLOW_STEP_ORDER = (
    "ready", "preflight", "implement", "verify", "semantic_review",
    "acceptance", "accept", "completed",
)


FLOW_STEP_ROLES = {
    "ready": "controller",
    "acceptance": "acceptance_reviewer",
    "completed": "controller",
    "preflight": "preflight",
    "implement": "implementer",
    "verify": "verifier",
    "semantic_review": "review_collector",
    "accept": "controller",
}


FLOW_STEP_MODES = {
    "ready": {"off"},
    "acceptance": {"standard", "strong"},
    "completed": {"off"},
    "preflight": {"light", "standard", "strong"},
    "implement": {"light", "standard", "strong"},
    "verify": {"targeted", "targeted_plus_repository_gate"},
    "semantic_review": {"standard", "strong"},
    "accept": {"off"},
}


FLOW_ROUTE_FIELDS = (
    "blocked", "failed", "needs_input", "unexpected_changes", "inconclusive",
    "corrections_exhausted", "permission_expansion",
    "plan_or_architecture_question",
)


def validate_flow_profile(flow: dict[str, Any]) -> None:
    required = (
        "version", "profile", "steps", "actor_levels",
        "implementation_session_reuse_threshold", "correction", "routes",
    )
    validate_exact_object(flow, required, "flow")
    if type(flow["version"]) is not int or flow["version"] != 2:
        raise ValueError("Unsupported flow version")
    validate_str(flow["profile"], "flow.profile")
    if flow["actor_levels"] != ACTOR_LEVELS:
        raise ValueError("flow.actor_levels must match the frozen actor mapping")
    if (
        type(flow["implementation_session_reuse_threshold"]) is not float
        or flow["implementation_session_reuse_threshold"]
        != IMPLEMENTATION_SESSION_REUSE_THRESHOLD
    ):
        raise ValueError(
            "flow.implementation_session_reuse_threshold must be exactly 0.5"
        )

    steps = flow["steps"]
    if not isinstance(steps, list):
        raise ValueError("flow.steps must be an array")
    kinds = []
    for step in steps:
        validate_exact_object(step, ("kind", "role", "mode"), "flow step")
        kind = step["kind"]
        if kind not in FLOW_STEP_ORDER:
            raise ValueError(f"Unsupported flow step: {kind}")
        if step["role"] != FLOW_STEP_ROLES[kind]:
            raise ValueError(f"flow step {kind} has an invalid role")
        if step["mode"] not in FLOW_STEP_MODES[kind]:
            raise ValueError(f"flow step {kind} has an unsupported mode")
        kinds.append(kind)
    if len(kinds) != len(set(kinds)):
        raise ValueError("flow steps must not be duplicated")
    if kinds != list(FLOW_STEP_ORDER):
        raise ValueError("flow requires every mandatory stage in order")

    correction = flow["correction"]
    if correction != {"enabled": True, "limit": 3, "includes_environment_repair": True} or (
        type(correction.get("limit")) is not int
        or correction.get("enabled") is not True
        or correction.get("includes_environment_repair") is not True
    ):
        raise ValueError("flow.correction requires three shared corrections including environment repair")

    routes = flow["routes"]
    validate_exact_object(routes, FLOW_ROUTE_FIELDS, "flow.routes")
    for field in FLOW_ROUTE_FIELDS:
        if routes[field] not in {"stop", "escalate"}:
            raise ValueError(f"flow.routes.{field} must be stop or escalate")


def resolve_flow_profile(policy: dict[str, Any]) -> dict[str, Any]:
    if "flow" not in policy:
        raise ValueError("Run policy requires an explicit flow")
    flow = json.loads(json.dumps(policy["flow"]))
    validate_flow_profile(flow)
    return flow


def correction_session_policy(*, occupancy: float | None, reliable: bool) -> str:
    """Terminal token totals are deliberately not an occupancy input."""
    if (
        reliable is True
        and type(occupancy) in {int, float}
        and math.isfinite(occupancy)
        and 0 <= occupancy < IMPLEMENTATION_SESSION_REUSE_THRESHOLD
    ):
        return "reuse"
    return "fresh"


def flow_step(flow: dict[str, Any], kind: str) -> dict[str, Any] | None:
    validate_flow_profile(flow)
    return next((dict(step) for step in flow["steps"] if step["kind"] == kind), None)


def validate_flow_cursor(
    flow: dict[str, Any], cursor: dict[str, Any],
) -> None:
    validate_flow_profile(flow)
    validate_exact_object(
        cursor, ("current_step", "correction_cycle"), "flow cursor"
    )
    current = cursor["current_step"]
    cycle = cursor["correction_cycle"]
    kinds = [step["kind"] for step in flow["steps"]]
    if current is not None and current not in kinds and current != "correction":
        raise ValueError("flow cursor current step does not belong to the flow")
    if type(cycle) is not int or cycle < 0:
        raise ValueError("flow cursor correction cycle is invalid")
    if current is None:
        if cycle != 0:
            raise ValueError("a null flow cursor requires correction cycle zero")
        return

    correction = flow["correction"]
    if cycle > correction["limit"]:
        raise ValueError("flow cursor correction cycle exceeds the flow limit")
    if cycle > 0 and not correction["enabled"]:
        raise ValueError("flow cursor correction cycle is disabled by the flow")
    if current == "correction":
        if cycle == 0 or not correction["enabled"]:
            raise ValueError("correction step requires an active correction cycle")


def transition_flow_cursor(
    flow: dict[str, Any],
    cursor: dict[str, Any],
    action: str,
    *,
    result: str | None = None,
) -> dict[str, Any]:
    validate_flow_cursor(flow, cursor)
    current = cursor["current_step"]
    cycle = cursor["correction_cycle"]
    kinds = [step["kind"] for step in flow["steps"]]

    if action == "select":
        if current is not None or cycle != 0:
            raise ValueError("task selection requires a null cursor at cycle zero")
        return {"current_step": kinds[0], "correction_cycle": 0}
    if action == "advance":
        if current not in kinds or current in {"accept", "completed"}:
            raise ValueError("cursor cannot advance from the current step")
        return {
            "current_step": kinds[kinds.index(current) + 1],
            "correction_cycle": cycle,
        }
    if action == "complete_inspection":
        if current != "implement":
            raise ValueError("inspection completion requires the implement cursor")
        next_index = kinds.index("implement") + 1
        if kinds[next_index] == "verify":
            next_index += 1
        return {
            "current_step": kinds[next_index],
            "correction_cycle": cycle,
        }
    if action == "begin_correction":
        if current not in {"verify", "semantic_review", "acceptance"} or result not in {"CHANGES_REQUESTED", "findings", "environment_repair"}:
            raise ValueError("correction requires findings, CHANGES_REQUESTED or environment repair at checks, collection or acceptance")
        correction = flow["correction"]
        if not correction["enabled"] or cycle >= correction["limit"]:
            return {
                "current_step": current,
                "correction_cycle": cycle,
                "stop_action": flow["routes"]["corrections_exhausted"],
            }
        return {"current_step": "correction", "correction_cycle": cycle + 1}
    if action == "complete_correction":
        if current != "correction" or cycle < 1:
            raise ValueError("fresh review requires an active correction cycle")
        return {"current_step": "verify", "correction_cycle": cycle}
    raise ValueError(f"Unsupported flow cursor action: {action}")


def _validate_flow_subject(
    subject: dict[str, Any], *, expected: dict[str, Any] | None = None,
) -> None:
    required = (
        "run_id", "task_id", "flow_revision", "flow_sha256", "step",
        "correction_cycle", "actor_role",
    )
    validate_exact_object(subject, required, "flow subject")
    for field in ("run_id", "task_id"):
        validate_str(subject[field], f"flow subject.{field}")
    if type(subject["flow_revision"]) is not int or subject["flow_revision"] < 1:
        raise ValueError("flow subject.flow_revision must be a positive integer")
    validate_sha256(subject["flow_sha256"], "flow subject.flow_sha256")
    if subject["step"] not in {*FLOW_STEP_ORDER, "correction"}:
        raise ValueError("flow subject.step is invalid")
    if type(subject["correction_cycle"]) is not int or subject["correction_cycle"] < 0:
        raise ValueError("flow subject.correction_cycle is invalid")
    expected_role = (
        "implementer" if subject["step"] == "correction"
        else FLOW_STEP_ROLES[subject["step"]]
    )
    if subject["actor_role"] != expected_role:
        raise ValueError("flow subject.actor_role contradicts its step")
    if expected is not None and subject != expected:
        raise ValueError("flow subject does not match expected cursor identity")


def validate_handoff_envelope(
    envelope: dict[str, Any], *, expected_subject: dict[str, Any] | None = None,
) -> None:
    required = (
        "version", "subject", "summary", "changed_paths", "evidence_refs",
        "transcript_ref",
    )
    validate_exact_object(envelope, required, "handoff envelope")
    if type(envelope["version"]) is not int or envelope["version"] != 1:
        raise ValueError("Unsupported handoff envelope version")
    _validate_flow_subject(envelope["subject"], expected=expected_subject)
    validate_str(envelope["summary"], "handoff.summary")
    for field in ("changed_paths", "evidence_refs"):
        validate_str_array(envelope[field], f"handoff.{field}", allow_empty=True)
        for index, value in enumerate(envelope[field]):
            validate_run_relative_reference(value, f"handoff.{field}[{index}]")
    validate_run_relative_reference(envelope["transcript_ref"], "handoff.transcript_ref")


def validate_step_outcome(
    envelope: dict[str, Any], *, expected_subject: dict[str, Any] | None = None,
) -> None:
    required = (
        "version", "subject", "result", "evidence_status", "artifact_refs",
        "payload",
    )
    validate_exact_object(envelope, required, "step outcome")
    if type(envelope["version"]) is not int or envelope["version"] != 1:
        raise ValueError("Unsupported step outcome version")
    _validate_flow_subject(envelope["subject"], expected=expected_subject)
    step = envelope["subject"]["step"]
    result_families = {
        "preflight": {"ready", "blocked", "needs_input"},
        "implement": {"complete", "needs_input", "failed"},
        "correction": {"complete", "needs_input", "failed"},
        "verify": {"mechanically_eligible", "findings"},
        "semantic_review": {"collected", "findings", "INCONCLUSIVE"},
        "acceptance": {"ACCEPT", "CHANGES_REQUESTED", "INCONCLUSIVE"},
    }
    if envelope["evidence_status"] != "reported" or envelope["result"] not in result_families.get(step, set()):
        raise ValueError("actor result cannot omit a required stage or grant completion")
    validate_str_array(
        envelope["artifact_refs"], "step outcome.artifact_refs", allow_empty=True
    )
    for index, value in enumerate(envelope["artifact_refs"]):
        validate_run_relative_reference(
            value, f"step outcome.artifact_refs[{index}]"
        )
    payload = envelope["payload"]
    validate_exact_object(payload, ("version", "reference"), "step outcome.payload")
    if type(payload["version"]) is not int or payload["version"] != 1:
        raise ValueError("Unsupported step outcome payload version")
    if payload["reference"] is not None:
        validate_run_relative_reference(
            payload["reference"], "step outcome.payload.reference"
        )
