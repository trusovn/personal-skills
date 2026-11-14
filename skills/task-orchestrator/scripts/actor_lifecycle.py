"""Launch, observe, stop and admit reserved actor operations.

Owns supervisor handles, durable launch intent, terminal observation, readiness
admission and intervention records. Commands retain their locks and ledger commits;
collection and acceptance admission prepare changes within that same transaction.
Dependencies: authority, records, collection/acceptance workflows, storage and transport.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

from . import run_records
from . import run_authority
from . import review_collection
from . import acceptance_workflow
from . import codex_worker as worker
from . import run_storage as storage


_ACTOR_SUPERVISORS: dict[str, subprocess.Popen] = {}


def _actor_prompt(assignment: dict[str, Any], inputs: dict[str, Any], policy: dict[str, Any], collection_context=None) -> str:
    role_instructions = (
        "Acceptance: consume independent collection; do not implement, correct, collect evidence or write the tracker. "
        "Return decision {action: accept|correct|missing_evidence|blocker, rationale, evidence: exact context.evidence, dispositions, unfinished}. "
        "Account for every retained finding, including omissions. Missing proof is not a deferrable defect. "
        "A confirmed AC/gate violation or material operating/maintenance risk requires fix-now with separate impact and likelihood; preference alone is an observation. "
        "Known issues require bounded non-material effect, compatible consumers, follow-up and reassessment; waive no AC/check/proof/material risk. "
        "Preserve unchanged approvals; reopen only for new relevant evidence/exposure, stating why. "
        "Authorized bounded blockers take precedence over missing proof; retain each unfinished row with its owner. "
        "Unavailable mandatory installed roles block the profile unless explicit source-guided authority exists. "
        if assignment['stage'] == 'acceptance' else
        "Collection reports evidence only, never acceptance decisions or new disposition/deferral authority. "
    )
    return (role_instructions + "Execute only this frozen assignment. Actor output is a claim, never authority. "
            "Respect frozen run_policy permissions and task scope. Do not commit, change policy, select another task, or edit controller records. "
            "Review roles must not edit implementation. Always use a fresh session.\n"
            "For preflight, check every task-required tool, dependency and installed skill in "
            "this execution environment. Report tools/dependencies/skills arrays of "
            "{name, status: passed|blocked, evidence}; use empty arrays only when no such "
            "prerequisite is required. Report requirements_complete only after checking all "
            "frozen task requirements. Missing prerequisites mean blocked, never ready.\n"
            "Return the assigned result schema, echo the exact assignment and observed "
            "thread.started session_id if known, otherwise null; never invent it. "
            "Collection must call check_collection with its exact assignment, rerun every frozen check, "
            "and report collection {coverage: {requirements, behavior, code_quality}, gaps, findings, rerun_path}. "
            "Coverage values are passed|blocked|not_run with evidence; findings contain id, evidence, requirement, context, exposure. "
            "Follow the assigned role boundary.\n"
            + json.dumps({"assignment": assignment, "frozen_inputs": inputs, "run_policy": policy, "collection_context": collection_context}, sort_keys=True))


def launch_operation(run_dir: Path, assignment: dict[str, Any], *,
                     codex_bin: str = "codex", timeout_seconds: float = 300) -> dict[str, Any]:
    """Start one detached transport supervisor, after durable no-relaunch intent."""
    try:
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("Positive finite timeout required")
        with storage.RunCommandLock(run_dir):
            ledger, _ = run_authority.load_run_context(run_dir)
            policy, _, inputs = run_authority.load_input_authority(run_dir, ledger)
            operation = run_records.actor_operation(ledger, assignment["operation_id"])
            if not run_records.same_typed_assignment(assignment, operation["assignment"]):
                raise ValueError("Launch assignment mismatch")
            if any(assignment[field] != ledger[field] for field in ("inputs_sha256", "policy_sha256", "flow_sha256")):
                raise ValueError("Stale launch assignment; use current frozen authority")
            if assignment["actor"] is None:
                raise ValueError("Verifier uses the successor check pipeline")
            directory = run_records.actor_directory(run_dir, operation)
            config = {"assignment": assignment, "execution_authorization": policy["execution_authorization"],
                      "cwd": policy["repository"], "codex_bin": str(codex_bin),
                      "timeout_seconds": timeout_seconds}
            if operation.get("transport"):
                if storage.read_json(directory / "launch.json") != config:
                    raise ValueError("Launch replay configuration conflict")
                return {"status": "replayed", "operation": operation}
            if operation["state"] != "reserved" or run_records.active_actor(ledger) is not operation:
                raise ValueError("Only the active reserved operation can launch")
            directory.mkdir(parents=True, exist_ok=True)
            content = storage.canonical_record_bytes(config)
            storage.publish_or_reuse_bytes(directory / "launch.json", content)
            context = review_collection.collection_launch_context(run_dir, ledger, inputs, operation) if assignment['stage'] == 'semantic_review' else acceptance_workflow.acceptance_launch_context(run_dir, ledger, inputs, operation) if assignment['stage'] == 'acceptance' else None
            prompt = _actor_prompt(assignment, inputs, policy, context).encode()
            storage.publish_or_reuse_bytes(directory / "prompt.txt", prompt)
            operation["transport"] = {"configuration_sha256": run_records.sha256_bytes(content),
                                      "supervisor_pid": None, "outcome": None}
            # From this point uncertainty is durable. Never relaunch, even if
            # the coordinator dies before Popen or identity publication.
            operation["state"] = "unknown"
            run_records.save_actor_ledger(run_dir, ledger)
            with (directory / "supervisor.stdout.log").open("x") as output, (directory / "supervisor.stderr.log").open("x") as errors:
                supervisor = subprocess.Popen(
                    [sys.executable, str(Path(worker.__file__).resolve()), "actor", "--config", str((directory / "launch.json").resolve())],
                    stdin=subprocess.DEVNULL, stdout=output, stderr=errors, start_new_session=True,
                )
            operation["transport"]["supervisor_pid"] = supervisor.pid
            operation["state"] = "running"
            run_records.save_actor_ledger(run_dir, ledger)
            # Keep the handle until a later observation can reap it in this
            # coordinator; other coordinators rely solely on durable receipts.
            _ACTOR_SUPERVISORS[str(directory.resolve())] = supervisor
            return {"status": "launched", "operation": operation}
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {"status": "refused", "reason": "launch_refused", "detail": str(error),
                "next_actions": ["status", "observe_operation", "intervene"]}


def _validate_readiness(readiness: dict[str, Any]) -> None:
    if not isinstance(readiness, dict) or set(readiness) != {"status", "requirements_complete", "tools", "dependencies", "skills"}:
        raise ValueError("Incomplete readiness payload")
    if readiness["status"] != "ready" or readiness["requirements_complete"] is not True:
        raise ValueError("Preflight is not complete and ready")
    for category in ("tools", "dependencies", "skills"):
        items = readiness[category]
        if not isinstance(items, list):
            raise ValueError(f"Missing prerequisite inventory: {category}")
        for item in items:
            if not isinstance(item, dict) or set(item) != {"name", "status", "evidence"}:
                raise ValueError(f"Malformed prerequisite: {category}")
            if not isinstance(item["name"], str) or not item["name"] or not isinstance(item["evidence"], str) or not item["evidence"]:
                raise ValueError(f"Missing prerequisite evidence: {category}")
            if item["status"] != "passed":
                raise ValueError(f"Missing {category} prerequisite: {item['name']}; {item['evidence']}")


def _admit_actor_outcome(run_dir: Path, ledger: dict[str, Any], operation: dict[str, Any], observed: dict[str, Any], result: dict[str, Any]) -> str | None:
    """Single admission extension point for controller-owned actor authority."""
    assignment = operation["assignment"]
    try:
        if observed.get("exit_code") != 0 or observed.get("stop_requested") or observed.get("attempt_outcome") in {"timed_out", "interrupted"}:
            raise ValueError("Actor failed, stopped or interrupted")
        run_records.validate_observed_result(assignment, observed, result)
        if assignment["stage"] == "semantic_review":
            return review_collection.admit_collection(run_dir, ledger, operation, observed, result)
        if assignment["stage"] == "acceptance":
            return acceptance_workflow.admit_acceptance(run_dir, ledger, operation, observed, result)
        if assignment["stage"] != "preflight":
            return None  # Producer claims require separate candidate inspection.
        if result["status"] != "complete":
            raise ValueError(f"Preflight {result['status']}: {result['summary']}")
        if any(assignment[field] != ledger[field] for field in ("inputs_sha256", "policy_sha256", "flow_sha256")):
            raise ValueError("Stale preflight authority")
        _validate_readiness(result["readiness"])
        ledger["readiness"] = {field: assignment[field] for field in
                               ("task_id", "operation_id", "inputs_sha256", "policy_sha256", "flow_sha256")}
        ledger["readiness"]["status"] = "ready"
        ledger["current_step"] = "implement"
        ledger.setdefault("evidence", {})["preflight"] = {
            "status": "passed", "inputs_sha256": assignment["inputs_sha256"],
            "operation_id": assignment["operation_id"],
        }
        return None
    except (OSError, ValueError, KeyError, TypeError) as error:
        return str(error)


def _open_actor_intervention(ledger: dict[str, Any], operation: dict[str, Any], blocker: str) -> None:
    record = {"key": operation["operation_id"] + ":" + operation["state"],
              "blocker": blocker, "evidence": "actors/" + operation["operation_id"],
              "operation_id": operation["operation_id"],
              "required_action": "Coordinator inspect retained evidence; resolve liveness or obtain explicit repair authority before retry",
              "event": "opened", "text": "Relay and response unknown; relay in active coordinator chat"}
    records = ledger.setdefault("interventions", [])
    if record not in records:
        records.append(record)


def _publish_actor_outcome(run_dir: Path, ledger: dict[str, Any], operation: dict[str, Any],
                           observed: dict[str, Any]) -> dict[str, Any]:
    directory = run_records.actor_directory(run_dir, operation)
    try:
        result = storage.read_json(directory / "result.json")
        blocker = _admit_actor_outcome(run_dir, ledger, operation, observed, result)
    except (OSError, ValueError) as error:
        blocker = f"Missing or malformed actor result: {error}"
    operation["transport"]["outcome"] = {
        "observed": observed, "blocker": blocker,
        "raw_result_path": str(directory / "result.json"),
        "terminal_path": str(directory / "result.state.json"),
    }
    operation["state"] = "terminal"
    ledger["active_operation_path"] = None
    ledger["actor_blocker"] = blocker
    if blocker:
        _open_actor_intervention(ledger, operation, blocker)
        if operation['assignment']['stage'] == 'acceptance':
            ledger.setdefault('evidence', {})['acceptance'] = {
                'status': 'blocked', 'inputs_sha256': operation['assignment']['inputs_sha256'],
                'candidate_sha256': operation['assignment']['candidate_sha256'],
                'operation_id': operation['operation_id'], 'blocker': blocker}
        if operation["assignment"]["stage"] == "semantic_review":
            evidence = ledger.setdefault("evidence", {}).get("semantic_review", {})
            if evidence.get("operation_id") != operation["operation_id"]:
                review_collection.collection_evidence(ledger, operation, "stale" if "stale" in blocker.lower() else "missing" if not (directory / "result.json").exists() else "blocked", blocker)
        if operation["assignment"]["stage"] == "preflight":
            ledger["readiness"] = None
            ledger.setdefault("evidence", {})["preflight"] = {
                "status": "blocked", "inputs_sha256": operation["assignment"]["inputs_sha256"],
                "operation_id": operation["operation_id"],
            }
    run_records.save_actor_ledger(run_dir, ledger)
    return {"status": "terminal", "operation": operation, "blocker": blocker}


def observe_operation(run_dir: Path, operation_id: str) -> dict[str, Any]:
    """Collect once, retaining invalid raw output without granting eligibility."""
    try:
        with storage.RunCommandLock(run_dir):
            ledger, _ = run_authority.load_run_context(run_dir)
            operation = run_records.actor_operation(ledger, operation_id)
            if operation["state"] == "terminal":
                return {"status": "replayed", "operation": operation}
            if not operation.get("transport"):
                return {"status": "reserved", "operation": operation}
            directory = run_records.actor_directory(run_dir, operation)
            handle = _ACTOR_SUPERVISORS.get(str(directory.resolve()))
            if handle is not None and handle.poll() is not None:
                del _ACTOR_SUPERVISORS[str(directory.resolve())]
            observed, terminal = run_records.read_actor_observation(directory, operation)
            if not terminal:
                # Alive is not terminal; absence without a receipt is unknown,
                # and may hide a surviving child. No automatic retry.
                pid = operation["transport"]["supervisor_pid"]
                alive = pid is not None and worker.process_liveness(pid) == "alive"
                operation_state = "running" if alive and operation["state"] == "running" else "unknown"
                changed = operation["state"] != operation_state
                operation["state"] = operation_state
                before = len(ledger.get("interventions", []))
                if operation_state == "unknown":
                    _open_actor_intervention(ledger, operation, "No terminal receipt; actor liveness unresolved; retry and another writer prohibited")
                if changed or len(ledger.get("interventions", [])) != before:
                    run_records.save_actor_ledger(run_dir, ledger)
                return {"status": operation_state, "operation": operation, "observation": observed,
                        "next_actions": ["observe_operation", "intervene"]}
            if review_collection.collection_check_unresolved(run_dir, operation):
                operation["state"] = "unknown"
                _, rerun_path, _ = review_collection.collection_check_paths(operation)
                blocker = 'Collection rerun terminality unresolved; inspect collection-checks intent and logs before retry'
                try:
                    blocker = storage.read_json(run_dir / rerun_path).get('blocker') or blocker
                except (OSError, ValueError):
                    pass
                ledger['actor_blocker'] = blocker
                review_collection.collection_evidence(ledger, operation, 'blocked', blocker, rerun_path)
                _open_actor_intervention(ledger, operation, blocker)
                run_records.save_actor_ledger(run_dir, ledger)
                return {"status": "unknown", "operation": operation, "next_actions": ["intervene"]}
            if handle is not None:
                try:
                    handle.wait(timeout=1)
                    _ACTOR_SUPERVISORS.pop(str(directory.resolve()), None)
                except subprocess.TimeoutExpired:
                    pass
            return _publish_actor_outcome(run_dir, ledger, operation, observed)
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {"status": "refused", "reason": "observation_refused", "detail": str(error)}


def stop_operation(run_dir: Path, operation_id: str) -> dict[str, Any]:
    """Persist a stop request; the adapter, never a reused PID, receives it."""
    try:
        with storage.RunCommandLock(run_dir):
            ledger, _ = run_authority.load_run_context(run_dir)
            operation = run_records.actor_operation(ledger, operation_id)
            if operation["state"] == "terminal":
                return {"status": "replayed", "operation": operation}
            directory = run_records.actor_directory(run_dir, operation)
            directory.mkdir(parents=True, exist_ok=True)
            storage.publish_or_reuse_bytes(directory / "stop.request.json",
                                     storage.canonical_record_bytes({"operation_id": operation_id, "requested": True}))
            if not operation.get("transport"):
                operation["state"] = "terminal"
                ledger["active_operation_path"] = None
                ledger["actor_blocker"] = "Stopped before launch; reserve fresh preflight or intervene"
                run_records.save_actor_ledger(run_dir, ledger)
                return {"status": "terminal", "operation": operation}
        return observe_operation(run_dir, operation_id)
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {"status": "refused", "reason": "stop_refused", "detail": str(error)}


def record_intervention(run_dir: Path, request: dict[str, Any]) -> dict[str, Any]:
    """Retain active-chat relay/response observations; this grants no authority."""
    try:
        with storage.RunCommandLock(run_dir):
            ledger, _ = run_authority.load_run_context(run_dir)
            required = {"key", "blocker", "evidence", "operation_id", "required_action", "event", "text"}
            if set(request) != required or any(not isinstance(request[f], str) for f in required):
                raise ValueError("Incomplete intervention request")
            if any(not request[f] for f in ("key", "blocker", "evidence", "required_action")):
                raise ValueError("Precise blocker/evidence/owner action required")
            if request["event"] not in {"opened", "relayed", "response"}:
                raise ValueError("Unknown chat observation event")
            if request["operation_id"]:
                run_records.actor_operation(ledger, request["operation_id"])
            records = ledger.setdefault("interventions", [])
            if request in records:
                return {"status": "replayed", "interventions": records}
            if any(r["key"] == request["key"] and any(r[f] != request[f] for f in
                   ("blocker", "evidence", "operation_id", "required_action")) for r in records):
                raise ValueError("Intervention key conflict")
            records.append(request)
            run_records.save_actor_ledger(run_dir, ledger)
            return {"status": "recorded", "interventions": records}
    except (ValueError, OSError, KeyError, TypeError) as error:
        return {"status": "refused", "reason": "intervention_refused", "detail": str(error)}

