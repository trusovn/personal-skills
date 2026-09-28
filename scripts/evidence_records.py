"""Canonical v2 evidence records and explicit artifact capture helpers."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path, PureWindowsPath
from typing import Any, Mapping

from scripts.evidence_store import EvidenceStore, EvidenceStoreError


SCHEMA_VERSION = 2
PROJECT_SNAPSHOT_NAMESPACE = "project_snapshot"
PROJECT_SNAPSHOT_TYPE = "ProjectSnapshot"
TASK_REVISION_NAMESPACE = "task_revision"
TASK_REVISION_TYPE = "TaskRevision"
_MISSING = object()

_TASK_CONTEXT_FIELDS = {
    "task_type",
    "intended_scope",
    "behavioral_scope",
    "transformation_type",
    "implementation_precedent",
    "state_or_compatibility_constraints",
    "verification_work",
    "discovery_uncertainty",
}
_PLANNING_FIELDS = _TASK_CONTEXT_FIELDS | {
    "expected_calls",
    "expected_duration",
    "confidence",
    "planner_recommended_profile",
    "reasoning_effort",
    "split_decision",
    "provenance",
}
_PROVENANCE_VALUES = {
    "observed",
    "mechanically_extracted",
    "planner_declared",
    "planner_estimated",
    "externally_supplied",
    "inferred",
    "unknown",
    "not_applicable",
}
_PROVENANCE_FIELDS = {"knowledge_status", "source"}
_ABSOLUTE_PATH_MARKER = "<absolute-path>"


class EvidenceRecordError(ValueError):
    """Raised when a supplied evidence record is malformed."""


def canonical_json(value: Any) -> bytes:
    """Return the one canonical UTF-8 JSON representation used for identity."""
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise EvidenceRecordError("Value is not JSON-serializable") from exc


def content_id(value: Any) -> str:
    return f"sha256:{hashlib.sha256(canonical_json(value)).hexdigest()}"


def _is_sha256_reference(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        return False
    digest = value.removeprefix("sha256:")
    return len(digest) == 64 and all(char in "0123456789abcdef" for char in digest)


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise EvidenceRecordError(f"{label} must be an object")
    return value


def _validate_stable_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or any(character in value for character in "/\\\r\n"):
        raise EvidenceRecordError(f"{label} must be a non-empty path-independent string")
    return value


def _validate_sha256_or_none(value: Any, label: str) -> str | None:
    if value is not None and not _is_sha256_reference(value):
        raise EvidenceRecordError(f"{label} must be a sha256 reference or null")
    return value


def _canonicalize_planning_value(value: Any) -> Any:
    if value == _ABSOLUTE_PATH_MARKER:
        raise EvidenceRecordError(f"Planning values cannot use reserved marker {_ABSOLUTE_PATH_MARKER!r}")
    if isinstance(value, str) and (Path(value).is_absolute() or PureWindowsPath(value).is_absolute()):
        return _ABSOLUTE_PATH_MARKER
    if isinstance(value, Mapping):
        return {key: _canonicalize_planning_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_canonicalize_planning_value(item) for item in value]
    return deepcopy(value)


def _validate_provenance(value: Any) -> dict[str, Any]:
    provenance = _require_mapping(value, "Planning provenance")
    if set(provenance) - _PROVENANCE_FIELDS:
        raise EvidenceRecordError("Planning provenance contains unsupported fields")
    result = dict(provenance)
    if "knowledge_status" in result and result["knowledge_status"] not in _PROVENANCE_VALUES:
        raise EvidenceRecordError("Planning provenance knowledge_status is invalid")
    if "source" in result:
        _validate_stable_id(result["source"], "Planning provenance source")
    return result


def validate_artifact_descriptor(value: Any) -> dict[str, str]:
    descriptor = _require_mapping(value, "Artifact descriptor")
    if set(descriptor) != {"logical_name", "content_ref"}:
        raise EvidenceRecordError("Artifact descriptor must contain logical_name and content_ref only")
    logical_name = descriptor["logical_name"]
    content_ref = descriptor["content_ref"]
    if not isinstance(logical_name, str) or not logical_name.strip():
        raise EvidenceRecordError("Artifact logical_name must be a non-empty string")
    if "/" in logical_name or "\\" in logical_name or Path(logical_name).is_absolute():
        raise EvidenceRecordError("Artifact logical_name must be stable and path-independent")
    if not _is_sha256_reference(content_ref):
        raise EvidenceRecordError("Artifact content_ref must be a sha256 reference")
    return {"logical_name": logical_name, "content_ref": content_ref}


def capture_artifact(
    store: EvidenceStore,
    logical_name: str,
    *,
    data: bytes | None = None,
    source_path: str | Path | None = None,
) -> dict[str, str]:
    """Store explicitly supplied bytes or one explicitly selected regular file."""
    if (data is None) == (source_path is None):
        raise EvidenceRecordError("Supply exactly one of data or source_path")
    if data is None:
        path = Path(source_path)  # type: ignore[arg-type]
        if not path.is_file():
            raise EvidenceRecordError(f"Artifact source is not a regular file: {path}")
        data = path.read_bytes()
    if not isinstance(data, bytes):
        raise EvidenceRecordError("Artifact data must be bytes")
    try:
        content_ref = store.put_blob(data)
    except EvidenceStoreError:
        raise
    return validate_artifact_descriptor({"logical_name": logical_name, "content_ref": content_ref})


def validate_project_snapshot(value: Any) -> dict[str, Any]:
    record = _require_mapping(value, "ProjectSnapshot")
    expected = {"schema_version", "record_type", "artifacts"}
    allowed = expected | {"collector_fingerprint"}
    extra = set(record) - allowed
    missing = expected - set(record)
    if missing or extra:
        raise EvidenceRecordError(f"Invalid ProjectSnapshot fields; missing={sorted(missing)}, extra={sorted(extra)}")
    version = record["schema_version"]
    if isinstance(version, bool) or version != SCHEMA_VERSION:
        raise EvidenceRecordError(f"Unsupported schema_version {version!r}; expected {SCHEMA_VERSION}")
    if record["record_type"] != PROJECT_SNAPSHOT_TYPE:
        raise EvidenceRecordError("ProjectSnapshot record_type is invalid")
    artifacts = record["artifacts"]
    if not isinstance(artifacts, list):
        raise EvidenceRecordError("ProjectSnapshot artifacts must be a list")
    normalized = []
    names = set()
    for artifact in artifacts:
        descriptor = validate_artifact_descriptor(artifact)
        if descriptor["logical_name"] in names:
            raise EvidenceRecordError("ProjectSnapshot artifact logical_name values must be unique")
        names.add(descriptor["logical_name"])
        normalized.append(descriptor)
    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "record_type": PROJECT_SNAPSHOT_TYPE,
        "artifacts": normalized,
    }
    if "collector_fingerprint" in record:
        fingerprint = record["collector_fingerprint"]
        if fingerprint is not None and not _is_sha256_reference(fingerprint):
            raise EvidenceRecordError("collector_fingerprint must be a sha256 reference or null")
        result["collector_fingerprint"] = fingerprint
    return result


class ProjectSnapshot:
    """Validated immutable ProjectSnapshot value and its deterministic ID."""

    def __init__(self, record: Mapping[str, Any]):
        self._record = validate_project_snapshot(record)
        self.id = content_id(self._record)

    @property
    def record(self) -> dict[str, Any]:
        """Return an isolated copy so identity-bearing state cannot be mutated."""
        return deepcopy(self._record)

    @classmethod
    def create(
        cls,
        artifacts: list[Mapping[str, Any]],
        *,
        collector_fingerprint: str | None | object = _MISSING,
    ) -> "ProjectSnapshot":
        record: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "record_type": PROJECT_SNAPSHOT_TYPE,
            "artifacts": artifacts,
        }
        if collector_fingerprint is not _MISSING:
            record["collector_fingerprint"] = collector_fingerprint
        return cls(record)

    def persist(self, store: EvidenceStore) -> "ProjectSnapshot":
        try:
            store.put_immutable_record(PROJECT_SNAPSHOT_NAMESPACE, self.id, self._record)
        except EvidenceStoreError:
            raise
        return self


def create_project_snapshot(
    store: EvidenceStore,
    artifacts: list[Mapping[str, Any]],
    *,
    collector_fingerprint: str | None | object = _MISSING,
) -> ProjectSnapshot:
    return ProjectSnapshot.create(artifacts, collector_fingerprint=collector_fingerprint).persist(store)


def validate_task_revision(value: Any) -> dict[str, Any]:
    record = _require_mapping(value, "TaskRevision")
    required = {"schema_version", "record_type", "task_id", "task_brief_ref", "artifact_refs"}
    allowed = required | {"planning_project_snapshot_ref", "planning", "decomposition"}
    missing = required - set(record)
    extra = set(record) - allowed
    if missing or extra:
        raise EvidenceRecordError(f"Invalid TaskRevision fields; missing={sorted(missing)}, extra={sorted(extra)}")
    if isinstance(record["schema_version"], bool) or record["schema_version"] != SCHEMA_VERSION:
        raise EvidenceRecordError(f"Unsupported schema_version {record['schema_version']!r}; expected {SCHEMA_VERSION}")
    if record["record_type"] != TASK_REVISION_TYPE:
        raise EvidenceRecordError("TaskRevision record_type is invalid")
    task_id = _validate_stable_id(record["task_id"], "TaskRevision task_id")
    task_brief_ref = _validate_sha256_or_none(record["task_brief_ref"], "TaskRevision task_brief_ref")
    if task_brief_ref is None:
        raise EvidenceRecordError("TaskRevision task_brief_ref is required")
    artifact_refs = record["artifact_refs"]
    if not isinstance(artifact_refs, list):
        raise EvidenceRecordError("TaskRevision artifact_refs must be a list")
    artifacts = [validate_artifact_descriptor(artifact) for artifact in artifact_refs]
    if len({artifact["logical_name"] for artifact in artifacts}) != len(artifacts):
        raise EvidenceRecordError("TaskRevision artifact logical_name values must be unique")
    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "record_type": TASK_REVISION_TYPE,
        "task_id": task_id,
        "task_brief_ref": task_brief_ref,
        "artifact_refs": artifacts,
    }
    if "planning_project_snapshot_ref" in record:
        result["planning_project_snapshot_ref"] = _validate_sha256_or_none(
            record["planning_project_snapshot_ref"], "planning_project_snapshot_ref"
        )
    if "planning" in record:
        planning = _require_mapping(record["planning"], "TaskRevision planning")
        extra_planning = set(planning) - _PLANNING_FIELDS
        if extra_planning:
            raise EvidenceRecordError(f"Invalid planning fields: {sorted(extra_planning)}")
        normalized_planning = _canonicalize_planning_value(planning)
        if "provenance" in normalized_planning:
            normalized_planning["provenance"] = _validate_provenance(normalized_planning["provenance"])
        result["planning"] = normalized_planning
    if "decomposition" in record:
        decomposition = _require_mapping(record["decomposition"], "TaskRevision decomposition")
        expected = {"parent_task_id", "child_task_ids", "source_plan_ref"}
        if set(decomposition) - expected:
            raise EvidenceRecordError("Invalid TaskRevision decomposition fields")
        normalized_decomposition: dict[str, Any] = {}
        if "parent_task_id" in decomposition:
            normalized_decomposition["parent_task_id"] = _validate_stable_id(
                decomposition["parent_task_id"], "parent_task_id"
            )
            if normalized_decomposition["parent_task_id"] == task_id:
                raise EvidenceRecordError("TaskRevision cannot be its own parent")
        if "child_task_ids" in decomposition:
            child_ids = decomposition["child_task_ids"]
            if not isinstance(child_ids, list) or not child_ids or any(not isinstance(child, str) for child in child_ids):
                raise EvidenceRecordError("child_task_ids must be a non-empty list of task IDs")
            normalized_decomposition["child_task_ids"] = [
                _validate_stable_id(child, "child_task_id") for child in child_ids
            ]
            if len(set(normalized_decomposition["child_task_ids"])) != len(child_ids):
                raise EvidenceRecordError("TaskRevision child_task_ids must be unique")
            if task_id in normalized_decomposition["child_task_ids"]:
                raise EvidenceRecordError("TaskRevision cannot be its own child")
            if normalized_decomposition.get("parent_task_id") in normalized_decomposition["child_task_ids"]:
                raise EvidenceRecordError("TaskRevision parent and child relationships cannot self-cycle")
        if "source_plan_ref" in decomposition:
            normalized_decomposition["source_plan_ref"] = _validate_stable_id(
                decomposition["source_plan_ref"], "source_plan_ref"
            )
        if not normalized_decomposition:
            raise EvidenceRecordError("TaskRevision decomposition cannot be empty")
        result["decomposition"] = normalized_decomposition
    return result


class TaskRevision:
    """Validated immutable TaskRevision value and its deterministic ID."""

    def __init__(self, record: Mapping[str, Any]):
        self._record = validate_task_revision(record)
        self.id = content_id(self._record)

    @property
    def task_id(self) -> str:
        return self._record["task_id"]

    @property
    def record(self) -> dict[str, Any]:
        return deepcopy(self._record)

    @classmethod
    def create(
        cls,
        task_id: str,
        task_brief_ref: str,
        artifact_refs: list[Mapping[str, Any]],
        *,
        planning_project_snapshot_ref: str | None | object = _MISSING,
        planning: Mapping[str, Any] | object = _MISSING,
        decomposition: Mapping[str, Any] | object = _MISSING,
    ) -> "TaskRevision":
        record: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "record_type": TASK_REVISION_TYPE,
            "task_id": task_id,
            "task_brief_ref": task_brief_ref,
            "artifact_refs": artifact_refs,
        }
        if planning_project_snapshot_ref is not _MISSING:
            record["planning_project_snapshot_ref"] = planning_project_snapshot_ref
        if planning is not _MISSING:
            record["planning"] = planning
        if decomposition is not _MISSING:
            record["decomposition"] = decomposition
        return cls(record)

    def persist(self, store: EvidenceStore) -> "TaskRevision":
        store.put_immutable_record(TASK_REVISION_NAMESPACE, (self.task_id, self.id), self._record)
        return self


def create_task_revision(
    store: EvidenceStore,
    task_id: str,
    task_brief_ref: str,
    artifact_refs: list[Mapping[str, Any]],
    *,
    planning_project_snapshot_ref: str | None | object = _MISSING,
    planning: Mapping[str, Any] | object = _MISSING,
    decomposition: Mapping[str, Any] | object = _MISSING,
) -> TaskRevision:
    return TaskRevision.create(
        task_id,
        task_brief_ref,
        artifact_refs,
        planning_project_snapshot_ref=planning_project_snapshot_ref,
        planning=planning,
        decomposition=decomposition,
    ).persist(store)


EXECUTION_ATTEMPT_NAMESPACE = "attempt"
EXECUTION_ATTEMPT_TYPE = "ExecutionAttempt"
ASSOCIATION_NAMESPACE = "association"
ASSOCIATION_TYPE = "Association"

_ATTEMPT_RELATIONS = {
    "retry_of",
    "correction_of",
    "continuation_of",
    "profile_replay_of",
    "calibration_of",
}


def compute_collector_fingerprint(
    *,
    file_contents: Mapping[str, bytes | str] | None = None,
    file_paths: list[str | Path] | None = None,
    config: Any = None,
) -> str:
    """Return a deterministic fingerprint over explicitly selected collector semantics.

    Ordering of inputs is irrelevant and absolute locations are ignored; every
    selected file participates under one unambiguous logical name. Duplicate
    logical names across all input forms are rejected rather than shadowed.
    """
    semantic: dict[str, Any] = {}
    if file_contents:
        for logical_name, data in file_contents.items():
            _validate_stable_id(logical_name, "collector file logical_name")
            key = f"file:{logical_name}"
            if key in semantic:
                raise EvidenceRecordError(f"Collector file logical_name collision: {logical_name}")
            semantic[key] = data if isinstance(data, str) else data.hex()
    if file_paths:
        for path in file_paths:
            resolved = Path(path)
            if not resolved.is_file():
                raise EvidenceRecordError(f"Collector file is not a regular file: {resolved}")
            logical_name = resolved.name
            _validate_stable_id(logical_name, "collector file logical_name")
            key = f"file:{logical_name}"
            if key in semantic:
                raise EvidenceRecordError(f"Collector file logical_name collision: {logical_name}")
            semantic[key] = resolved.read_bytes().hex()
    if config is not None:
        semantic["config"] = config
    return content_id({"collector_semantics": semantic})


def validate_execution_attempt(value: Any) -> dict[str, Any]:
    record = _require_mapping(value, "ExecutionAttempt")
    required = {"attempt_id", "schema_version", "record_type", "task", "pre_run", "execution", "post_run", "evidence"}
    allowed = required | {"execution_project_snapshot_ref", "related_attempts"}
    missing = required - set(record)
    extra = set(record) - allowed
    if missing or extra:
        raise EvidenceRecordError(f"Invalid ExecutionAttempt fields; missing={sorted(missing)}, extra={sorted(extra)}")
    if isinstance(record["schema_version"], bool) or record["schema_version"] != SCHEMA_VERSION:
        raise EvidenceRecordError(f"Unsupported schema_version {record['schema_version']!r}; expected {SCHEMA_VERSION}")
    if record["record_type"] != EXECUTION_ATTEMPT_TYPE:
        raise EvidenceRecordError("ExecutionAttempt record_type is invalid")
    attempt_id = _validate_stable_id(record["attempt_id"], "ExecutionAttempt attempt_id")

    task = _require_mapping(record["task"], "ExecutionAttempt task")
    task_keys = set(task) - {"direct_input_ref", "task_revision_ref"}
    if task_keys:
        raise EvidenceRecordError("ExecutionAttempt task contains unsupported fields")
    direct_ref = task.get("direct_input_ref")
    revision_ref = task.get("task_revision_ref")
    if (direct_ref is not None) == (revision_ref is not None):
        raise EvidenceRecordError("ExecutionAttempt task must use exactly one of direct_input_ref or task_revision_ref")
    normalized_task: dict[str, Any] = {}
    if direct_ref is not None:
        normalized_task["direct_input_ref"] = _validate_sha256_or_none(direct_ref, "direct_input_ref")
        if normalized_task["direct_input_ref"] is None:
            raise EvidenceRecordError("direct_input_ref is required when supplied")
    else:
        normalized_task["task_revision_ref"] = _validate_sha256_or_none(revision_ref, "task_revision_ref")
        if normalized_task["task_revision_ref"] is None:
            raise EvidenceRecordError("task_revision_ref is required when supplied")

    result: dict[str, Any] = {
        "attempt_id": attempt_id,
        "schema_version": SCHEMA_VERSION,
        "record_type": EXECUTION_ATTEMPT_TYPE,
        "task": normalized_task,
        "pre_run": _validate_pre_run(record["pre_run"]),
        "execution": _validate_execution(record["execution"]),
        "post_run": _validate_post_run(record["post_run"]),
        "evidence": _validate_evidence(record["evidence"]),
    }
    if "execution_project_snapshot_ref" in record:
        result["execution_project_snapshot_ref"] = _validate_sha256_or_none(
            record["execution_project_snapshot_ref"], "execution_project_snapshot_ref"
        )
    if "related_attempts" in record:
        related = record["related_attempts"]
        if not isinstance(related, list):
            raise EvidenceRecordError("related_attempts must be a list")
        normalized_related = []
        for relation in related:
            if not isinstance(relation, Mapping):
                raise EvidenceRecordError("Each related_attempts entry must be an object")
            if set(relation) != {"relation", "attempt_id"}:
                raise EvidenceRecordError("related_attempts entry must contain relation and attempt_id only")
            if relation["relation"] not in _ATTEMPT_RELATIONS:
                raise EvidenceRecordError(f"Unsupported attempt relation: {relation['relation']!r}")
            normalized_related.append({
                "relation": relation["relation"],
                "attempt_id": _validate_stable_id(relation["attempt_id"], "related attempt_id"),
            })
        result["related_attempts"] = normalized_related
    return result


def _validate_pre_run(value: Any) -> dict[str, Any]:
    pre_run = _require_mapping(value, "ExecutionAttempt pre_run")
    expected = {"repository_state", "workflow_identity", "actual_runtime_identity"}
    allowed = expected | {"intended_execution_profile", "assignment_provenance", "conditions"}
    missing = expected - set(pre_run)
    extra = set(pre_run) - allowed
    if missing or extra:
        raise EvidenceRecordError(f"Invalid pre_run fields; missing={sorted(missing)}, extra={sorted(extra)}")
    result: dict[str, Any] = {}
    for field in ("repository_state", "workflow_identity", "actual_runtime_identity"):
        if not isinstance(pre_run[field], Mapping):
            raise EvidenceRecordError(f"pre_run {field} must be an object")
        result[field] = deepcopy(pre_run[field])
    if "intended_execution_profile" in pre_run:
        if not isinstance(pre_run["intended_execution_profile"], Mapping):
            raise EvidenceRecordError("pre_run intended_execution_profile must be an object")
        result["intended_execution_profile"] = deepcopy(pre_run["intended_execution_profile"])
    if "assignment_provenance" in pre_run:
        if not isinstance(pre_run["assignment_provenance"], Mapping):
            raise EvidenceRecordError("pre_run assignment_provenance must be an object")
        result["assignment_provenance"] = deepcopy(pre_run["assignment_provenance"])
    if "conditions" in pre_run:
        if not isinstance(pre_run["conditions"], Mapping):
            raise EvidenceRecordError("pre_run conditions must be an object")
        result["conditions"] = deepcopy(pre_run["conditions"])
    return result


def _validate_execution(value: Any) -> dict[str, Any]:
    execution = _require_mapping(value, "ExecutionAttempt execution")
    expected = {"started_at", "termination_state"}
    allowed = expected | {"finished_at", "terminated_at", "checks", "telemetry"}
    missing = expected - set(execution)
    extra = set(execution) - allowed
    if missing or extra:
        raise EvidenceRecordError(f"Invalid execution fields; missing={sorted(missing)}, extra={sorted(extra)}")
    result: dict[str, Any] = {"started_at": execution["started_at"]}
    if not isinstance(result["started_at"], str) or not result["started_at"].strip():
        raise EvidenceRecordError("execution started_at must be a non-empty string")
    termination_state = execution["termination_state"]
    if not isinstance(termination_state, str) or not termination_state.strip():
        raise EvidenceRecordError("execution termination_state must be a non-empty string")
    result["termination_state"] = termination_state
    for field in ("finished_at", "terminated_at"):
        if field in execution:
            value_at = execution[field]
            if not isinstance(value_at, str) or not value_at.strip():
                raise EvidenceRecordError(f"execution {field} must be a non-empty string")
            result[field] = value_at
    if "checks" in execution:
        checks = execution["checks"]
        if not isinstance(checks, list):
            raise EvidenceRecordError("execution checks must be a list")
        normalized_checks = []
        for check in checks:
            if not isinstance(check, Mapping):
                raise EvidenceRecordError("Each execution check must be an object")
            normalized_checks.append(deepcopy(check))
        result["checks"] = normalized_checks
    if "telemetry" in execution:
        if not isinstance(execution["telemetry"], Mapping):
            raise EvidenceRecordError("execution telemetry must be an object")
        result["telemetry"] = deepcopy(execution["telemetry"])
    return result


def _validate_post_run(value: Any) -> dict[str, Any]:
    post_run = _require_mapping(value, "ExecutionAttempt post_run")
    if set(post_run) != {"repository_state"}:
        raise EvidenceRecordError("post_run must contain repository_state only")
    if not isinstance(post_run["repository_state"], Mapping):
        raise EvidenceRecordError("post_run repository_state must be an object")
    return {"repository_state": deepcopy(post_run["repository_state"])}


def _validate_evidence(value: Any) -> dict[str, Any]:
    evidence = _require_mapping(value, "ExecutionAttempt evidence")
    if set(evidence) != {"schema_version", "collector_fingerprint"}:
        raise EvidenceRecordError("evidence must contain schema_version and collector_fingerprint only")
    if isinstance(evidence["schema_version"], bool) or evidence["schema_version"] != SCHEMA_VERSION:
        raise EvidenceRecordError(f"Unsupported evidence schema_version {evidence['schema_version']!r}; expected {SCHEMA_VERSION}")
    fingerprint = evidence["collector_fingerprint"]
    if fingerprint is not None and not _is_sha256_reference(fingerprint):
        raise EvidenceRecordError("evidence collector_fingerprint must be a sha256 reference or null")
    return {"schema_version": SCHEMA_VERSION, "collector_fingerprint": fingerprint}


class ExecutionAttempt:
    """Validated ExecutionAttempt value; lifecycle persistence is delegated to later work."""

    def __init__(self, record: Mapping[str, Any]):
        self._record = validate_execution_attempt(record)
        self.id = self._record["attempt_id"]

    @property
    def attempt_id(self) -> str:
        return self._record["attempt_id"]

    @property
    def record(self) -> dict[str, Any]:
        return deepcopy(self._record)

    def create_in_store(self, store: EvidenceStore) -> "ExecutionAttempt":
        store.create_attempt(self.attempt_id, self._record)
        return self


def validate_association(value: Any) -> dict[str, Any]:
    record = _require_mapping(value, "Association")
    required = {
        "association_id",
        "attempt_id",
        "schema_version",
        "record_type",
        "type",
        "producer",
        "outcome_status",
        "collected_at",
    }
    allowed = required | {"durable_artifact_ref", "provenance"}
    missing = required - set(record)
    extra = set(record) - allowed
    if missing or extra:
        raise EvidenceRecordError(f"Invalid Association fields; missing={sorted(missing)}, extra={sorted(extra)}")
    if isinstance(record["schema_version"], bool) or record["schema_version"] != SCHEMA_VERSION:
        raise EvidenceRecordError(f"Unsupported schema_version {record['schema_version']!r}; expected {SCHEMA_VERSION}")
    if record["record_type"] != ASSOCIATION_TYPE:
        raise EvidenceRecordError("Association record_type is invalid")
    association_id = _validate_stable_id(record["association_id"], "Association association_id")
    attempt_id = _validate_stable_id(record["attempt_id"], "Association attempt_id")
    association_type = _validate_stable_id(record["type"], "Association type")
    if not isinstance(record["producer"], Mapping):
        raise EvidenceRecordError("Association producer must be an object")
    if not isinstance(record["outcome_status"], Mapping):
        raise EvidenceRecordError("Association outcome_status must be an object")
    collected_at = record["collected_at"]
    if not isinstance(collected_at, str) or not collected_at.strip():
        raise EvidenceRecordError("Association collected_at must be a non-empty string")
    result: dict[str, Any] = {
        "association_id": association_id,
        "attempt_id": attempt_id,
        "schema_version": SCHEMA_VERSION,
        "record_type": ASSOCIATION_TYPE,
        "type": association_type,
        "producer": deepcopy(record["producer"]),
        "outcome_status": deepcopy(record["outcome_status"]),
        "collected_at": collected_at,
    }
    if "durable_artifact_ref" in record:
        artifact_ref = record["durable_artifact_ref"]
        if artifact_ref is not None and not _is_sha256_reference(artifact_ref):
            raise EvidenceRecordError("Association durable_artifact_ref must be a sha256 reference or null")
        result["durable_artifact_ref"] = artifact_ref
    if "provenance" in record:
        if not isinstance(record["provenance"], Mapping):
            raise EvidenceRecordError("Association provenance must be an object")
        result["provenance"] = deepcopy(record["provenance"])
    return result


def _association_record(
    association_id: str,
    attempt_id: str,
    record_type: str,
    association_type: str,
    producer: Mapping[str, Any],
    outcome_status: Mapping[str, Any],
    collected_at: str,
    *,
    durable_artifact_ref: str | None | object = _MISSING,
    provenance: Mapping[str, Any] | object = _MISSING,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "association_id": association_id,
        "attempt_id": attempt_id,
        "schema_version": SCHEMA_VERSION,
        "record_type": record_type,
        "type": association_type,
        "producer": producer,
        "outcome_status": outcome_status,
        "collected_at": collected_at,
    }
    if durable_artifact_ref is not _MISSING:
        record["durable_artifact_ref"] = durable_artifact_ref
    if provenance is not _MISSING:
        record["provenance"] = provenance
    return record


class Association:
    """Validated immutable Association value persisted beside an attempt."""

    def __init__(self, record: Mapping[str, Any]):
        self._record = validate_association(record)

    @property
    def association_id(self) -> str:
        return self._record["association_id"]

    @property
    def attempt_id(self) -> str:
        return self._record["attempt_id"]

    @property
    def record(self) -> dict[str, Any]:
        return deepcopy(self._record)

    @classmethod
    def create(
        cls,
        attempt_id: str,
        association_id: str,
        association_type: str,
        producer: Mapping[str, Any],
        outcome_status: Mapping[str, Any],
        collected_at: str,
        *,
        durable_artifact_ref: str | None | object = _MISSING,
        provenance: Mapping[str, Any] | object = _MISSING,
    ) -> "Association":
        return cls(_association_record(
            association_id,
            attempt_id,
            ASSOCIATION_TYPE,
            association_type,
            producer,
            outcome_status,
            collected_at,
            durable_artifact_ref=durable_artifact_ref,
            provenance=provenance,
        ))

    def persist(self, store: EvidenceStore) -> "Association":
        store.put_immutable_record(
            ASSOCIATION_NAMESPACE, (self.attempt_id, self.association_id), self._record
        )
        return self


def create_association(store: EvidenceStore, record: Mapping[str, Any]) -> Association:
    return Association(record).persist(store)
