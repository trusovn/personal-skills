"""Canonical v2 evidence records and explicit artifact capture helpers."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from scripts.evidence_store import EvidenceStore, EvidenceStoreError


SCHEMA_VERSION = 2
PROJECT_SNAPSHOT_NAMESPACE = "project_snapshot"
PROJECT_SNAPSHOT_TYPE = "ProjectSnapshot"
_MISSING = object()


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
