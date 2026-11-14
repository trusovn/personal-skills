"""Project current run status and reserve authorized actor assignments.

status_run is read-only; reserve_operation owns its entire locked admission and
publication. Evidence freshness and correction accounting determine available work.
Actor process lifecycle and outcome admission live elsewhere.
Dependencies: authority, run records, flow/ledger rules, storage and current
evidence workflows.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import run_records
from . import run_authority
from . import candidate_checks
from . import review_collection
from . import acceptance_workflow
from . import flow_policy
from . import ledger as ledger_rules
from . import run_storage as storage


def _reservation_options(
    ledger: dict[str, Any], *, stale: set[str], decision: dict[str, Any] | None,
) -> tuple[list[str], str | None]:
    active = run_records.active_actor(ledger)
    if active and active['assignment']['stage'] == 'verify':
        return ['check_candidate', 'intervene'], f"check_operation_{active['state']}"
    if active:
        actions = ["launch_operation", "stop_operation", "intervene"] if active["state"] == "reserved" else ["observe_operation", "stop_operation", "intervene"]
        return actions, f"operation_{active['state']}"
    if ledger["state"] not in {"ready", "resumable"}:
        return ["intervene"], "successor_admission_pending"
    correction = ledger.get("correction_request")
    if correction and ledger["correction_cycle"] >= 3:
        return ["intervene"], "corrections_exhausted"
    if correction == "environment_repair":
        return ["reserve:correction"], None
    if correction == "review_findings" and (
        decision is None or decision.get("correction_request") != "review_findings"
    ):
        return ["intervene"], "correction_authority_stale"
    if correction in {"check_failed", "review_findings"}:
        if not run_records.current_readiness(ledger):
            return ["reserve:preflight"], "current_preflight_readiness_required"
        return ["reserve:correction"], None
    if ledger.get('candidate_path') and (
        ledger['current_step'] == 'preflight' or not run_records.current_readiness(ledger)
    ):
        return ['reserve:preflight'], 'current_preflight_readiness_required'
    if 'candidate' in stale:
        return ['inspect_candidate', 'intervene'], 'candidate_stale'
    if 'verify' in stale:
        return ['reserve:verify', 'intervene'], 'checks_stale'
    if 'semantic_review' in stale:
        return ['reserve:semantic_review', 'intervene'], 'collection_stale'
    if decision and decision['decision']['action'] != 'accept':
        return list(dict.fromkeys(decision['next_actions'] + ['intervene'])), decision['decision']['rationale']
    if 'acceptance' in stale:
        return ['reserve:acceptance', 'reserve:verify', 'reserve:semantic_review', 'intervene'], 'acceptance_stale'
    if ledger.get('candidate_path') and not ledger.get('correction_request'):
        actions = ['reserve:verify', 'inspect_candidate', 'intervene']
        if run_records.evidence_view(ledger, 'verify')['status'] == 'passed':
            actions.insert(0, 'reserve:semantic_review')
            if run_records.evidence_view(ledger, 'semantic_review')['status'] == 'passed':
                actions.insert(0, 'reserve:acceptance')
        if decision:
            actions = decision['next_actions'] + actions
        return actions, None
    stage = ledger["current_step"] or "preflight"
    if stage in {"ready", "preflight"}:
        return ["reserve:preflight"], None
    if stage in {"implement", "correction"}:
        if not run_records.current_readiness(ledger):
            return ["reserve:preflight"], "current_preflight_readiness_required"
        if stage == "implement" and any(
            item["assignment"]["stage"] == "implement"
            for item in ledger.get("actor_operations", [])
        ):
            return ["intervene"], "successor_admission_pending"
        if stage == "correction" and correction not in {"check_failed", "review_findings"}:
            return ["intervene"], "correction_authorization_pending"
        return [f"reserve:{stage}"], None
    # Successors admit these records; reservations consume, never manufacture,
    # eligible prerequisites. Semantic validation remains T-004/T-005 work.
    predecessor = {"verify": "implement", "semantic_review": "verify", "acceptance": "semantic_review"}.get(stage)
    if predecessor:
        if not ledger.get("candidate_sha256") or run_records.evidence_view(ledger, predecessor)["status"] != "passed":
            return ["intervene"], "successor_evidence_required"
        return [f"reserve:{stage}"], None
    return ["intervene"], "successor_completion_pending"


def _reservation_evidence(run_dir, ledger, inputs):
    """Collect current proof facts without selecting actions or mutating authority."""
    ledger = json.loads(json.dumps(ledger))
    stale = set()
    if ledger.get('candidate_path'):
        try:
            candidate = candidate_checks.load_current_candidate(run_dir, ledger, inputs)
        except (ValueError, OSError, KeyError, TypeError):
            stale.add('candidate')
            for stage in ('implement', 'verify', 'semantic_review', 'acceptance'):
                if stage in ledger.get('evidence', {}):
                    ledger['evidence'][stage]['status'] = 'stale'
        if ledger.get('evidence', {}).get('verify', {}).get('status') == 'passed':
            try:
                candidate_checks.current_checks(run_dir, ledger, candidate)
            except (OSError, ValueError, KeyError, TypeError):
                stale.add('verify')
                ledger['evidence']['verify']['status'] = 'stale'
        if ledger.get('evidence', {}).get('semantic_review', {}).get('status') == 'passed':
            try:
                review_collection.validate_current_collection(run_dir, ledger)
            except (OSError, ValueError, KeyError, TypeError):
                stale.add('semantic_review')
                ledger['evidence']['semantic_review']['status'] = 'stale'
    decision = None
    if ledger.get('evidence', {}).get('acceptance', {}).get('path'):
        try:
            decision = acceptance_workflow.current_acceptance(run_dir, ledger)
        except (OSError, ValueError, KeyError, TypeError):
            stale.add('acceptance')
            ledger['evidence']['acceptance']['status'] = 'stale'
    return ledger, stale, decision


def status_run(run_dir: Path) -> dict[str, Any]:
    """Read one atomic ledger snapshot without advancing state or taking a lock."""
    ledger, flow = run_authority.load_run_context(run_dir)
    inputs = run_authority.load_frozen_inputs(run_dir, ledger)
    task_id = inputs['task_id']
    ledger, stale, decision = _reservation_evidence(run_dir, ledger, inputs)
    actions, blocker = _reservation_options(ledger, stale=stale, decision=decision)
    eligible = bool(decision and decision['decision']['action'] == 'accept'
                    and not run_records.active_actor(ledger) and not ledger.get('correction_request'))
    return {
        "status": "ok", "run_id": ledger["run_id"], "task_id": task_id,
        "inputs_sha256": ledger["inputs_sha256"],
        "policy_sha256": ledger["policy_sha256"],
        "flow_revision": ledger["flow_revision"], "flow_sha256": ledger["flow_sha256"],
        "state": ledger["state"], "state_version": ledger["revision"],
        "stage": ledger["current_step"] or "ready",
        "attempts": next(task["attempt_ids"] for task in ledger["tasks"] if task["id"] == task_id),
        "correction_count": ledger["correction_cycle"],
        "candidate_sha256": ledger.get("candidate_sha256"),
        "references": {field: ledger.get(field) for field in ("last_closure_path", "last_verification_path", "last_decision_path", "active_operation_path")},
        "evidence": {stage: run_records.evidence_view(ledger, stage) for stage in
                     ("preflight", "implement", "verify", "semantic_review", "acceptance")},
        "policy_omissions": ["repository_gate"] if flow_policy.flow_step(flow, "verify")["mode"] == "targeted" else [],
        "required_evidence": ["preflight", "implement", "verify", "semantic_review", "acceptance"],
        "completion_eligible": eligible, "acceptance_decision": decision,
        "outstanding_findings": ledger.get("outstanding_findings", []),
        "operation": run_records.active_actor(ledger), "operation_history": ledger.get("actor_operations", []),
        "readiness_current": run_records.current_readiness(ledger),
        "input_revision_history": ledger.get("input_revisions", []),
        "next_actions": actions, "blocker": ledger.get("actor_blocker") if blocker == "operation_unknown" and ledger.get("actor_blocker") else blocker or ledger.get("actor_blocker"),
        "interventions": ledger.get("interventions", []),
        "chat_relay_action": "relay precise blocker in active chat; delivery/response unknown unless recorded" if blocker not in {None, "operation_reserved", "operation_running"} or ledger.get("actor_blocker") else None,
    }


def reserve_operation(
    run_dir: Path, *, expected_version: int, task_id: str, stage: str,
    role: str, operation_key: str, reason: str = "initial",
) -> dict[str, Any]:
    """Reserve only current permitted work. T-003 owns launch/outcome admission."""
    options = None

    def refuse(code: str, ledger: dict[str, Any] | None = None) -> dict[str, Any]:
        if ledger and options is None:
            view, stale, decision = _reservation_evidence(run_dir, ledger, run_authority.load_frozen_inputs(run_dir, ledger))
            actions, _ = _reservation_options(view, stale=stale, decision=decision)
        else:
            actions, _ = options or (["intervene"], None)
        return {"status": "refused", "reason": code, "next_actions": actions,
                "state_version": ledger["revision"] if ledger else None}

    try:
        with storage.RunCommandLock(run_dir):
            ledger, flow = run_authority.load_run_context(run_dir)
            if (type(expected_version) is not int or expected_version < 1
                    or not isinstance(operation_key, str) or not operation_key
                    or any(not isinstance(value, str) for value in (task_id, stage, role, reason))):
                return refuse("invalid_request", ledger)
            request = dict(expected_version=expected_version, task_id=task_id,
                           stage=stage, role=role, operation_key=operation_key, reason=reason)
            for operation in ledger.get("actor_operations", []):
                if operation["request"]["operation_key"] == operation_key:
                    if operation["request"] != request:
                        return refuse("operation_key_conflict", ledger)
                    return {"status": "replayed", "assignment": operation["assignment"],
                            "state_version": ledger["revision"]}
            if expected_version != ledger["revision"]:
                return refuse("stale_version", ledger)
            inputs = run_authority.load_frozen_inputs(run_dir, ledger)
            view, stale, decision = _reservation_evidence(run_dir, ledger, inputs)
            options = _reservation_options(view, stale=stale, decision=decision)
            actions, blocker = options
            expected_role = "implementer" if stage == "correction" else flow_policy.FLOW_STEP_ROLES.get(stage)
            if task_id != inputs["task_id"] or role != expected_role:
                return refuse("task_or_role_mismatch", ledger)
            if f"reserve:{stage}" not in actions:
                return refuse(blocker or "stage_mismatch", ledger)
            if stage in {'verify', 'semantic_review', 'acceptance'} and ledger.get('candidate_path'):
                candidate_checks.load_current_candidate(run_dir, ledger, inputs)
                if stage == 'semantic_review':
                    candidate_checks.current_checks(run_dir, ledger, candidate_checks.load_current_candidate(run_dir, ledger, inputs))
                if stage == 'acceptance':
                    acceptance_workflow.acceptance_context(run_dir, ledger, inputs)
            is_correction = stage == "correction"
            if (is_correction and reason != ledger.get("correction_request")) or (
                not is_correction and reason not in {"initial", "retry"}
            ):
                return refuse("reason_not_authorized", ledger)
            if stage == "implement" and any(item["assignment"]["stage"] == "implement" for item in ledger.get("actor_operations", [])):
                return refuse("initial_implementation_already_reserved", ledger)
            mode = flow_policy.flow_step(flow, "implement" if is_correction else stage)["mode"]
            operation_id = f"operation-{len(ledger.get('actor_operations', [])) + 1:03d}"
            count = ledger["correction_cycle"] + int(is_correction)
            assignment = {
                "run_id": ledger["run_id"], "task_id": task_id,
                "operation_id": operation_id, "operation_key": operation_key,
                "stage": stage, "role": role, "reason": reason,
                "inputs_sha256": ledger["inputs_sha256"], "policy_sha256": ledger["policy_sha256"],
                "flow_sha256": ledger["flow_sha256"], "flow_revision": ledger["flow_revision"],
                "candidate_sha256": ledger.get("candidate_sha256"),
                "correction_count": count, "can_repair": is_correction and reason == "environment_repair",
                "can_change_files": stage in {"implement", "correction"},
                "actor": flow["actor_levels"].get(mode),
                "session_policy": "fresh" if is_correction else None,
            }
            operation = {"operation_id": operation_id, "state": "reserved",
                         "request": request, "assignment": assignment}
            updated = json.loads(json.dumps(ledger))
            updated.setdefault("actor_operations", []).append(operation)
            updated.update(revision=ledger["revision"] + 1, updated_at=run_records.now_iso(),
                           selected_task_id=task_id, current_step=stage,
                           correction_cycle=count,
                           active_operation_path=f"actor_operations/{operation_id}")
            if is_correction:
                updated["correction_request"] = None
            if stage == "preflight" or assignment["can_repair"]:
                updated["readiness"] = None
                updated["actor_blocker"] = None
            ledger_rules.validate_ledger(updated)
            storage.atomic_write_json(run_dir / "ledger.json", updated)
            return {"status": "reserved", "assignment": assignment, "state_version": updated["revision"]}
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {**refuse("authority_or_lock_unavailable"), "detail": str(error)}

