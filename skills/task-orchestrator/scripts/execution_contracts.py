"""Attempt identities, execution, verification, closure and finalization contracts.

Owns exact cross-record identity links and append-only finalization transitions.
Uses flow/run policy, canonical serialization and shared record predicates.
No process execution, record publication, review policy or ledger dependency."""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any

from .flow_policy import (
    ACTOR_LEVELS,
    flow_step,
    validate_flow_profile,
)
from .record_serialization import (
    canonical_json,
    sha256_text,
)
from .record_validation import (
    validate_bool,
    validate_exact_object,
    validate_sha256,
    validate_str,
    validate_str_array,
)
from .run_policy import (
    validate_run_policy,
)


ATTEMPT_REQUIRED_FIELDS = (
    "task_id", "brief_path", "prompt_sha256", "baseline_ref", "policy_sha256",
    "flow_revision", "flow_sha256", "transport", "model", "effort", "sandbox",
    "approval_policy", "network", "writable_roots",
)


def validate_attempt_turn_identity(
    identity: dict[str, Any], *, expected: dict[str, Any] | None = None,
) -> None:
    """Validate the immutable subject shared by Stage 3 records."""

    required = (
        "run_id", "task_id", "attempt_id", "turn", "policy_sha256",
        "manifest_sha256", "prompt_sha256", "selected_task_baseline_sha256",
    )
    validate_exact_object(identity, required, "attempt/turn identity")
    for field in ("run_id", "task_id", "attempt_id"):
        validate_str(identity[field], f"identity.{field}")
    if type(identity["turn"]) is not int or identity["turn"] < 1:
        raise ValueError("identity.turn must be a positive integer")
    for field in required[4:]:
        validate_sha256(identity[field], f"identity.{field}")
    if expected is not None:
        validate_attempt_turn_identity(expected)
        if identity != expected:
            raise ValueError("identity does not match expected subject")


def _validate_git_oid(value: Any, field: str) -> None:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value) is None:
        raise ValueError(f"{field} must be a canonical Git object ID")


def _validate_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a UTC offset")
    return parsed


def _validate_time_range(started_at: Any, ended_at: Any, field: str) -> None:
    if _validate_timestamp(ended_at, f"{field}.ended_at") < _validate_timestamp(
        started_at, f"{field}.started_at"
    ):
        raise ValueError(f"{field} timestamps are reversed")


def _validate_artifact_path(value: Any, expected: str, field: str) -> None:
    validate_str(value, field)
    if value.startswith("/") or "\\" in value:
        raise ValueError(f"{field} must be a run-relative artifact path")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError(f"{field} contains an invalid path segment")
    if value != expected:
        raise ValueError(f"{field} must be {expected}")


def _turn_stem(identity: dict[str, Any]) -> str:
    subject = identity["subject"] if "subject" in identity else identity
    return f"{subject['attempt_id']}.turn-{subject['turn']:03d}"


def validate_closure_identity(
    identity: dict[str, Any], *, expected_subject: dict[str, Any] | None = None,
) -> None:
    required = (
        "subject", "stage2_git_evidence_sha256", "post_worker_head_oid",
        "post_worker_index_tree_oid", "post_worker_status_sha256",
    )
    validate_exact_object(identity, required, "closure identity")
    validate_attempt_turn_identity(identity["subject"], expected=expected_subject)
    validate_sha256(
        identity["stage2_git_evidence_sha256"],
        "closure_identity.stage2_git_evidence_sha256",
    )
    _validate_git_oid(identity["post_worker_head_oid"], "closure_identity.post_worker_head_oid")
    _validate_git_oid(
        identity["post_worker_index_tree_oid"],
        "closure_identity.post_worker_index_tree_oid",
    )
    validate_sha256(
        identity["post_worker_status_sha256"],
        "closure_identity.post_worker_status_sha256",
    )


def _validate_git_identity(value: Any, field: str) -> None:
    required = ("head_oid", "index_tree_oid", "status_sha256")
    validate_exact_object(value, required, field)
    _validate_git_oid(value["head_oid"], f"{field}.head_oid")
    _validate_git_oid(value["index_tree_oid"], f"{field}.index_tree_oid")
    validate_sha256(value["status_sha256"], f"{field}.status_sha256")


def _validate_authorized_gap(value: Any, field: str) -> None:
    required = ("reason", "owner", "follow_up")
    validate_exact_object(value, required, field)
    for name in required:
        validate_str(value[name], f"{field}.{name}")


def validate_command_execution_record(
    record: dict[str, Any], *, expected_closure_identity: dict[str, Any],
) -> None:
    required = (
        "version", "closure_identity", "plan", "outcomes", "effective_envelope",
        "started_at", "ended_at", "terminal_reason", "authorized_gap",
    )
    if "execution_mechanism" in record:
        if record["execution_mechanism"] != "sbx_yolo":
            raise ValueError("Invalid execution mechanism")
        required = (*required, "execution_mechanism")
    validate_exact_object(record, required, "command execution record")
    if type(record["version"]) is not int or record["version"] != 1:
        raise ValueError("Unsupported command execution record version")
    validate_closure_identity(record["closure_identity"])
    validate_closure_identity(expected_closure_identity)
    if record["closure_identity"] != expected_closure_identity:
        raise ValueError("execution closure identity does not match expected closure")
    if not isinstance(record["plan"], list):
        raise ValueError("execution.plan must be an array")
    plan_ids = []
    command_identities = []
    for index, command in enumerate(record["plan"], 1):
        validate_exact_object(command, ("id", "argv", "sources", "role"), "execution.plan item")
        expected_id = f"command-{index:03d}"
        if command["id"] != expected_id:
            raise ValueError(f"execution.plan command id must be {expected_id}")
        plan_ids.append(command["id"])
        validate_str_array(command["argv"], "execution.plan.argv")
        command_identities.append(tuple(command["argv"]))
        validate_str_array(command["sources"], "execution.plan.sources")
        if command["role"] not in {"targeted", "repository_gate"}:
            raise ValueError("execution.plan.role is invalid")
    if len(plan_ids) != len(set(plan_ids)):
        raise ValueError("execution.plan command IDs must be unique")
    if len(command_identities) != len(set(command_identities)):
        raise ValueError("execution.plan normalized command identities must be unique")
    if (
        not isinstance(record["outcomes"], list)
        or len(record["outcomes"]) > len(plan_ids)
    ):
        raise ValueError("execution.outcomes must be a plan prefix")
    statuses = []
    for index, outcome in enumerate(record["outcomes"]):
        required_outcome = (
            "id", "status", "exit_code", "started_at", "ended_at", "stdout_path",
            "stdout_sha256", "stderr_path", "stderr_sha256", "effective_argv",
        )
        validate_exact_object(outcome, required_outcome, "execution outcome")
        if outcome["id"] != plan_ids[index]:
            raise ValueError("execution outcomes must preserve plan identity and order")
        status = outcome["status"]
        if status not in {"passed", "failed", "timed_out", "interrupted", "authorized_gap"}:
            raise ValueError("execution outcome status is invalid")
        statuses.append(status)
        exit_code = outcome["exit_code"]
        if status == "passed" and (type(exit_code) is not int or exit_code != 0):
            raise ValueError("passed execution outcome requires exit_code 0")
        if status == "failed" and (type(exit_code) is not int or exit_code == 0):
            raise ValueError("failed execution outcome requires a nonzero exit_code")
        if status == "authorized_gap" and (type(exit_code) is not int or exit_code == 0):
            raise ValueError("authorized_gap outcome requires a nonzero exit_code")
        if status in {"timed_out", "interrupted"} and exit_code is not None:
            raise ValueError(f"{status} execution outcome requires null exit_code")
        validate_str_array(outcome["effective_argv"], "execution outcome effective_argv")
        _validate_time_range(outcome["started_at"], outcome["ended_at"], "execution outcome")
        stem = _turn_stem(record["closure_identity"])
        for stream in ("stdout", "stderr"):
            _validate_artifact_path(
                outcome[f"{stream}_path"],
                f"verification/{stem}.{outcome['id']}.{stream}.log",
                f"execution outcome {stream}_path",
            )
            validate_sha256(outcome[f"{stream}_sha256"], f"execution outcome {stream}_sha256")
    envelope = record["effective_envelope"]
    validate_exact_object(
        envelope,
        (
            "sandbox", "approval_policy", "network", "dependency_install",
            "writable_roots", "danger_full_access_authorized",
        ),
        "execution.effective_envelope",
    )
    if envelope["sandbox"] not in {"read-only", "workspace-write", "danger-full-access"}:
        raise ValueError("execution.effective_envelope.sandbox is invalid")
    if envelope["approval_policy"] != "never":
        raise ValueError("execution.effective_envelope.approval_policy must be never")
    validate_bool(envelope["network"], "execution.effective_envelope.network")
    validate_bool(
        envelope["dependency_install"], "execution.effective_envelope.dependency_install"
    )
    validate_bool(
        envelope["danger_full_access_authorized"],
        "execution.effective_envelope.danger_full_access_authorized",
    )
    if (
        envelope["sandbox"] == "danger-full-access"
        and not envelope["danger_full_access_authorized"]
    ):
        raise ValueError("execution danger-full-access lacks separate authorization")
    validate_str_array(
        envelope["writable_roots"], "execution.effective_envelope.writable_roots",
        allow_empty=True,
    )
    _validate_time_range(record["started_at"], record["ended_at"], "execution")
    reason = record["terminal_reason"]
    if reason not in {
        "complete", "command_failed", "timed_out", "interrupted", "authorized_gap",
        "omitted_by_policy",
    }:
        raise ValueError("execution.terminal_reason is invalid")
    if record["authorized_gap"] is not None:
        _validate_authorized_gap(record["authorized_gap"], "execution.authorized_gap")
    terminal_status = {
        "complete": None,
        "command_failed": "failed",
        "timed_out": "timed_out",
        "interrupted": "interrupted",
        "authorized_gap": "authorized_gap",
        "omitted_by_policy": None,
    }[reason]
    if reason == "omitted_by_policy":
        statuses_match_reason = not plan_ids and not statuses
    elif reason == "complete":
        statuses_match_reason = (
            len(statuses) == len(plan_ids) and all(status == "passed" for status in statuses)
        )
    else:
        statuses_match_reason = (
            statuses[-1] == terminal_status
            and all(status == "passed" for status in statuses[:-1])
        )
    if (
        not statuses_match_reason
        or (reason == "authorized_gap") != (record["authorized_gap"] is not None)
    ):
        raise ValueError("execution outcome contradicts terminal reason")


def validate_verification_record(
    record: dict[str, Any], *, expected_closure_identity: dict[str, Any],
    expected_execution_sha256: str,
) -> None:
    required = (
        "version", "closure_identity", "execution_path", "execution_sha256",
        "pre_verification_git", "post_verification_git", "drift_findings", "outcome",
    )
    validate_exact_object(record, required, "verification record")
    if type(record["version"]) is not int or record["version"] != 1:
        raise ValueError("Unsupported verification record version")
    validate_closure_identity(record["closure_identity"])
    validate_closure_identity(expected_closure_identity)
    if record["closure_identity"] != expected_closure_identity:
        raise ValueError("verification closure identity does not match expected closure")
    validate_sha256(record["execution_sha256"], "verification.execution_sha256")
    validate_sha256(expected_execution_sha256, "expected_execution_sha256")
    if record["execution_sha256"] != expected_execution_sha256:
        raise ValueError("verification execution digest does not match expected execution")
    stem = _turn_stem(record["closure_identity"])
    _validate_artifact_path(
        record["execution_path"], f"verification/{stem}.execution.json",
        "verification.execution_path",
    )
    _validate_git_identity(record["pre_verification_git"], "verification.pre_verification_git")
    _validate_git_identity(record["post_verification_git"], "verification.post_verification_git")
    validate_str_array(record["drift_findings"], "verification.drift_findings", allow_empty=True)
    if record["outcome"] not in {"passed", "failed", "omitted_by_policy"}:
        raise ValueError("verification.outcome is invalid")
    if record["outcome"] == "passed" and record["drift_findings"]:
        raise ValueError("passed verification cannot contain drift findings")


def validate_closure_decision(
    record: dict[str, Any], *, expected_closure_identity: dict[str, Any],
    expected_verification_sha256: str,
) -> None:
    required = (
        "version", "closure_identity", "verification_path", "verification_sha256",
        "accepted", "reasons", "allowed_actions", "allowed_transitions",
        "gap_details", "semantic_review",
    )
    validate_exact_object(record, required, "closure decision")
    if type(record["version"]) is not int or record["version"] != 1:
        raise ValueError("Unsupported closure decision version")
    validate_closure_identity(record["closure_identity"])
    validate_closure_identity(expected_closure_identity)
    if record["closure_identity"] != expected_closure_identity:
        raise ValueError("decision closure identity does not match expected closure")
    validate_sha256(record["verification_sha256"], "decision.verification_sha256")
    validate_sha256(expected_verification_sha256, "expected_verification_sha256")
    if record["verification_sha256"] != expected_verification_sha256:
        raise ValueError("decision verification digest does not match expected verification")
    _validate_artifact_path(
        record["verification_path"], f"verification/{_turn_stem(record['closure_identity'])}.json",
        "decision.verification_path",
    )
    validate_bool(record["accepted"], "decision.accepted")
    validate_str_array(record["reasons"], "decision.reasons")
    validate_str_array(record["allowed_actions"], "decision.allowed_actions")
    validate_str_array(record["allowed_transitions"], "decision.allowed_transitions")
    if not set(record["allowed_actions"]).issubset({"accept", "resume", "stop"}):
        raise ValueError("decision.allowed_actions contains an invalid action")
    if not set(record["allowed_transitions"]).issubset({"accepted", "resumable", "stopped"}):
        raise ValueError("decision.allowed_transitions contains an invalid transition")
    has_accept_action = "accept" in record["allowed_actions"]
    has_accept_transition = "accepted" in record["allowed_transitions"]
    if (
        has_accept_action != record["accepted"]
        or has_accept_transition != record["accepted"]
    ):
        raise ValueError("decision verdict contradicts allowed actions or transitions")
    for action, transition in (("resume", "resumable"), ("stop", "stopped")):
        if (action in record["allowed_actions"]) != (
            transition in record["allowed_transitions"]
        ):
            raise ValueError(
                f"decision action {action} must match transition {transition}"
            )
    if record["gap_details"] is not None:
        _validate_authorized_gap(record["gap_details"], "decision.gap_details")
    if record["semantic_review"] != "not_collected":
        raise ValueError("decision.semantic_review must be not_collected")


def validate_finalization_operation(
    record: dict[str, Any], *, expected_closure_identity: dict[str, Any],
    expected_decision_sha256: str,
) -> None:
    required = (
        "version", "operation_id", "closure_identity", "decision_path",
        "decision_sha256", "state", "prepared_intent", "effect_evidence", "mismatch",
    )
    validate_exact_object(record, required, "finalization operation")
    if type(record["version"]) is not int or record["version"] != 1:
        raise ValueError("Unsupported finalization operation version")
    subject = record["closure_identity"].get("subject", {}) if isinstance(
        record["closure_identity"], dict
    ) else {}
    validate_closure_identity(record["closure_identity"])
    validate_closure_identity(expected_closure_identity)
    if record["closure_identity"] != expected_closure_identity:
        raise ValueError("operation closure identity does not match expected closure")
    if record["operation_id"] != f"{subject['task_id']}-accept":
        raise ValueError("operation.operation_id does not match the task")
    validate_sha256(record["decision_sha256"], "operation.decision_sha256")
    validate_sha256(expected_decision_sha256, "expected_decision_sha256")
    if record["decision_sha256"] != expected_decision_sha256:
        raise ValueError("operation decision digest does not match expected decision")
    _validate_artifact_path(
        record["decision_path"], f"decisions/{_turn_stem(record['closure_identity'])}.json",
        "operation.decision_path",
    )
    if record["state"] not in {"prepared", "effects_complete", "complete", "mismatch"}:
        raise ValueError("operation.state is invalid")
    intent = record["prepared_intent"]
    validate_exact_object(
        intent, ("action", "commit_mode", "tracker_mode"), "operation.prepared_intent"
    )
    if intent["action"] != "accept":
        raise ValueError("operation.prepared_intent.action must be accept")
    if intent["commit_mode"] not in {"off", "controller_exact_paths"}:
        raise ValueError("operation.prepared_intent.commit_mode is invalid")
    if intent["tracker_mode"] != "off":
        raise ValueError("operation.prepared_intent.tracker_mode must be off")
    if not isinstance(record["effect_evidence"], list):
        raise ValueError("operation.effect_evidence must be an array")
    effect_ids = []
    for evidence in record["effect_evidence"]:
        validate_exact_object(
            evidence, ("effect_id", "effect_type", "outcome", "evidence_sha256"),
            "operation effect evidence",
        )
        validate_str(evidence["effect_id"], "operation effect_evidence.effect_id")
        effect_ids.append(evidence["effect_id"])
        if evidence["effect_type"] not in {"commit", "tracker"}:
            raise ValueError("operation effect type is invalid")
        if evidence["outcome"] not in {"complete", "not_required"}:
            raise ValueError("operation effect outcome is invalid")
        if evidence["outcome"] == "complete":
            validate_sha256(
                evidence["evidence_sha256"], "operation effect_evidence.evidence_sha256"
            )
        elif evidence["evidence_sha256"] is not None:
            raise ValueError("not-required effect evidence requires a null digest")
    if len(effect_ids) != len(set(effect_ids)):
        raise ValueError("operation effect IDs must be unique")
    if record["state"] == "prepared" and record["effect_evidence"]:
        raise ValueError("prepared operation cannot contain effect evidence")
    if record["mismatch"] is not None:
        validate_exact_object(
            record["mismatch"], ("reason", "evidence_sha256"), "operation.mismatch"
        )
        validate_str(record["mismatch"]["reason"], "operation.mismatch.reason")
        validate_sha256(
            record["mismatch"]["evidence_sha256"], "operation.mismatch.evidence_sha256"
        )
    if (record["state"] == "mismatch") != (record["mismatch"] is not None):
        raise ValueError("operation mismatch evidence contradicts state")


def update_finalization_operation(
    current: dict[str, Any], proposed: dict[str, Any], *, expected_state: str,
    expected_closure_identity: dict[str, Any], expected_decision_sha256: str,
) -> dict[str, Any]:
    validate_finalization_operation(
        current, expected_closure_identity=expected_closure_identity,
        expected_decision_sha256=expected_decision_sha256,
    )
    validate_finalization_operation(
        proposed, expected_closure_identity=expected_closure_identity,
        expected_decision_sha256=expected_decision_sha256,
    )
    if current["state"] != expected_state:
        raise ValueError(
            f"Expected operation state {expected_state}, found {current['state']}"
        )
    if current == proposed:
        return json.loads(json.dumps(current))
    immutable = (
        "version", "operation_id", "closure_identity", "decision_path",
        "decision_sha256", "prepared_intent",
    )
    if any(current[field] != proposed[field] for field in immutable):
        raise ValueError("operation prepared identity and intent are immutable")
    previous_evidence = current["effect_evidence"]
    if proposed["effect_evidence"][:len(previous_evidence)] != previous_evidence:
        raise ValueError("operation effect evidence is append-only")
    transitions = {
        "prepared": {"effects_complete", "mismatch"},
        "effects_complete": {"complete", "mismatch"},
        "complete": set(),
        "mismatch": set(),
    }
    if proposed["state"] not in transitions[current["state"]]:
        raise ValueError(
            f"Operation transition {current['state']} -> {proposed['state']} is not allowed"
        )
    if current["state"] == "effects_complete" and proposed["effect_evidence"] != previous_evidence:
        raise ValueError("complete transition cannot add effect evidence")
    return json.loads(json.dumps(proposed))


def validate_attempt_record(record: dict[str, Any]) -> None:
    for field in ATTEMPT_REQUIRED_FIELDS:
        if field not in record:
            raise ValueError(f"Attempt record is missing {field}")
    if type(record["flow_revision"]) is not int or record["flow_revision"] < 1:
        raise ValueError("Attempt record flow revision must be a positive integer")
    validate_sha256(record["flow_sha256"], "attempt flow_sha256")
    if record["transport"] != "codex-cli":
        raise ValueError("Attempt record transport must be codex-cli")
    if (record["model"], record["effort"]) not in {
        (mapping["model"], mapping["reasoning"])
        for mapping in ACTOR_LEVELS.values()
    }:
        raise ValueError("Attempt record actor selection contradicts the frozen mapping")


def build_attempt_record(
    *, task_id: str, brief_path: str, prompt: str, policy: dict[str, Any],
    flow: dict[str, Any], flow_revision: int, flow_sha256: str, baseline_ref: str,
) -> dict[str, Any]:
    validate_run_policy(policy)
    validate_flow_profile(flow)
    if type(flow_revision) is not int or flow_revision < 1:
        raise ValueError("Flow revision must be a positive integer")
    validate_sha256(flow_sha256, "flow_sha256")
    if sha256_text(canonical_json(flow) + "\n") != flow_sha256:
        raise ValueError("Flow bytes do not match the supplied digest")
    permissions = policy["permissions"]
    implement = flow_step(flow, "implement")
    assert implement is not None
    actor = ACTOR_LEVELS[implement["mode"]]
    return {
        "task_id": task_id, "brief_path": brief_path, "prompt": prompt,
        "prompt_sha256": sha256_text(prompt), "baseline_ref": baseline_ref,
        "policy_sha256": sha256_text(canonical_json(policy)),
        "flow_revision": flow_revision, "flow_sha256": flow_sha256,
        "transport": "codex-cli",
        "model": actor["model"], "effort": actor["reasoning"],
        "sandbox": permissions["sandbox"],
        "approval_policy": permissions["approval_policy"], "network": permissions["network"],
        "writable_roots": permissions["writable_roots"],
    }
