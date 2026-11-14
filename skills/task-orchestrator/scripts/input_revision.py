"""Publish owner-authorized frozen input revisions at an idle boundary.

revise_inputs owns validation, immutable preparation, exact replay and the atomic
ledger pointer change under one lock. It preserves history and correction charges.
Dependencies: authority, run records, state and storage; no actor/process control.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import run_records
from . import run_authority
from . import flow_policy
from . import ledger as ledger_rules
from . import record_serialization
from . import task_manifest
from . import run_storage as storage


def revise_inputs(run_dir: Path, request: dict[str, Any]) -> dict[str, Any]:
    """Publish explicitly owner-authorized inputs at an idle task boundary.

    The caller is responsible for obtaining the owner response; actor prose is
    not an authorization object. A bundle is immutable preparation. Only the
    atomic ledger replacement makes it current, including its replay receipt.
    """
    ledger = None
    publishing = False

    def refuse(reason: str, detail: str | None = None) -> dict[str, Any]:
        result = {"status": "refused", "reason": reason,
                  "state_version": ledger["revision"] if ledger else None,
                  "next_actions": ["intervene"]}
        if detail is not None:
            result["detail"] = detail
        return result

    try:
        # Detach caller-owned objects before validation, hashing or persistence.
        request = json.loads(json.dumps(request))
        ledger_rules.validate_input_revision_request(request)
    except (ValueError, KeyError, TypeError) as error:
        return refuse("invalid_revision_request", str(error))
    try:
        with storage.RunCommandLock(run_dir):
            ledger, _ = run_authority.load_run_context(run_dir)
            for receipt in ledger.get("input_revisions", []):
                if receipt["request"]["revision_key"] == request["revision_key"]:
                    if receipt["request"] != request:
                        return refuse("revision_key_conflict")
                    return {"status": "replayed", "state_version": ledger["revision"],
                            "revision_state_version": receipt["state_version"],
                            "inputs_sha256": receipt["inputs_sha256"], "revision_path": receipt["path"]}
            if request["expected_version"] != ledger["revision"]:
                return refuse("stale_version")
            task_id = run_authority.load_frozen_inputs(run_dir, ledger)["task_id"]
            if request["task_id"] != task_id:
                return refuse("task_mismatch")
            if task_id in ledger["completed_task_ids"] or any(task["state"] == "accepted" for task in ledger["tasks"]):
                return refuse("task_completed")
            active = run_records.active_actor(ledger)
            if active:
                return refuse(f"operation_{active['state']}")
            if ledger["active_attempt_id"] or ledger["active_operation_path"] or ledger["state"] in {"running", "finalizing"}:
                return refuse("operation_active_or_unknown")
            # An interrupted legacy flow change must be resolved explicitly.
            _, _, pending_flow = run_authority.load_flow_authority_state(run_dir, ledger)
            if pending_flow:
                return refuse("pending_flow_revision")

            payload = request["payload"]
            policy, manifest = payload["policy"], payload["manifest"]
            if (policy["run_id"] != ledger["run_id"] or policy["task_ids"] != [task_id]
                    or Path(policy["repository"]).resolve() != Path(ledger["repository"]).resolve()):
                return refuse("run_task_or_repository_mismatch")
            validated = task_manifest.validate_task_manifest(policy, manifest, Path(ledger["repository"]))
            if validated["completed_task_ids"] != ledger["completed_task_ids"]:
                return refuse("completion_history_mismatch")
            selected = next(task for task in manifest["tasks"] if task["id"] == task_id)
            policy_digest = record_serialization.sha256_text(record_serialization.canonical_json(policy))
            manifest_digest = record_serialization.sha256_text(record_serialization.canonical_json(manifest))
            inputs = {"version": 1, "task_id": task_id, "revision_key": request["revision_key"],
                      "policy_sha256": policy_digest, "manifest_sha256": manifest_digest,
                      "allowed_paths": selected["allowed_paths"],
                      "required_checks": selected.get("required_checks", []),
                      "required_reviews": selected.get("required_reviews", []), "documents": {}}
            for name, content in payload["documents"].items():
                source = selected["brief_path"] if name == "brief" else str(Path(selected["brief_path"]).with_name("verification.md"))
                inputs["documents"][name] = {"source_path": source, "content": content,
                                             "sha256": run_records.sha256_bytes(content.encode("utf-8")),
                                             "source_sha256": run_records.sha256_bytes((Path(ledger["repository"]) / source).read_bytes())}
            inputs_digest = run_records.sha256_bytes(storage.canonical_record_bytes(inputs))
            bundle_bytes = storage.canonical_record_bytes({"version": 1, "request": request, "inputs": inputs})
            history = ledger.get("input_revisions", [])
            relative = f"input-revisions/revision-{len(history) + 1:03d}.json"
            receipt = {"request": request, "path": relative, "sha256": run_records.sha256_bytes(bundle_bytes),
                       "inputs_sha256": inputs_digest, "state_version": ledger["revision"] + 1,
                       "previous": {key: value for key, value in ledger.items() if key != "input_revisions"}}
            updated = json.loads(json.dumps(ledger))
            flow_digest = run_records.sha256_bytes(run_authority.canonical_flow_bytes(flow_policy.resolve_flow_profile(policy)))
            updated.update(revision=receipt["state_version"], updated_at=run_records.now_iso(),
                           inputs_sha256=inputs_digest, policy_sha256=policy_digest,
                           manifest_sha256=manifest_digest, policy_path=relative, manifest_path=relative,
                           flow_path=relative, flow_sha256=flow_digest,
                           flow_revision=ledger["flow_revision"] + int(flow_digest != ledger["flow_sha256"]),
                           input_revisions=[*history, receipt], state="ready", selected_task_id=task_id,
                           active_attempt_id=None, active_operation_path=None, current_step="preflight",
                           readiness=None, candidate_sha256=None, correction_request=None,
                           last_closure_path=None, last_closure_sha256=None,
                           last_verification_path=None, last_decision_path=None)
            # Task projection changes, but implementation history and count do not.
            task = validated["task_entries"][0]
            task.update(state="ready", attempt_ids=ledger["tasks"][0]["attempt_ids"])
            updated["tasks"] = [task]
            ledger_rules.validate_ledger(updated)
            path = run_dir / relative
            if path.exists():
                if path.read_bytes() != bundle_bytes:
                    return refuse("pending_revision_conflict")
            else:
                publishing = True
                storage.write_durable_exclusive(path, bundle_bytes)
            publishing = True
            storage.atomic_write_json(run_dir / "ledger.json", updated)
            return {"status": "revised", "state_version": updated["revision"],
                    "revision_state_version": updated["revision"],
                    "inputs_sha256": inputs_digest, "revision_path": relative}
    except (ValueError, OSError, KeyError, TypeError) as error:
        if publishing:
            return {"status": "refused", "reason": "revision_publication_uncertain",
                    "state_version": None, "next_actions": ["intervene"],
                    "detail": f"{error}. Read status and retry the exact original revision request."}
        return refuse("authority_or_lock_unavailable", str(error))

