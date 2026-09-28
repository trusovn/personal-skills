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
