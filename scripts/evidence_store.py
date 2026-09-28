"""Git-metadata-backed storage for local execution evidence."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any


class EvidenceStoreError(RuntimeError):
    """Raised when an evidence-store invariant would be violated."""


class EvidenceStore:
    def put_blob(self, value: bytes) -> str:
        raise NotImplementedError

    def put_immutable_record(self, namespace: str, record_id: object, value: Any) -> None:
        raise NotImplementedError

    def create_attempt(self, attempt_id: str, value: Any) -> None:
        raise NotImplementedError

    def update_active_attempt(self, attempt_id: str, value: Any) -> None:
        raise NotImplementedError

    def finalize_attempt(self, attempt_id: str, value: Any) -> None:
        raise NotImplementedError

    def get_record(self, namespace: str, record_id: object) -> Any | None:
        raise NotImplementedError

    def record_exists(self, namespace: str, record_id: object) -> bool:
        raise NotImplementedError


def _git_directory(repo_root: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--absolute-git-dir"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip()
        raise EvidenceStoreError(f"Unable to resolve Git directory: {detail}") from exc
    return Path(result.stdout.strip()).resolve()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode(
        "utf-8"
    )


def _atomic_write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _segment(value: object, name: str) -> str:
    if not isinstance(value, str) or not value or value in {".", ".."} or "/" in value or "\\" in value:
        raise EvidenceStoreError(f"Invalid {name}: {value!r}")
    return value


class GitMetadataEvidenceStore(EvidenceStore):
    def __init__(self, repository_root: str | Path = "."):
        self.repository_root = Path(repository_root).resolve()
        self.root = _git_directory(self.repository_root) / "personal-skills" / "evidence" / "v2"

    def put_blob(self, value: bytes) -> str:
        if not isinstance(value, bytes):
            raise EvidenceStoreError("Blob value must be bytes")
        digest = hashlib.sha256(value).hexdigest()
        path = self.root / "blobs" / "sha256" / digest[:2] / digest
        if path.exists():
            if path.read_bytes() != value:
                raise EvidenceStoreError(f"Blob conflict for sha256:{digest}")
        else:
            _atomic_write(path, value)
        return f"sha256:{digest}"

    def put_immutable_record(self, namespace: str, record_id: object, value: Any) -> None:
        path = self._record_path(namespace, record_id)
        serialized = _json_bytes(value)
        if path.exists():
            if path.read_bytes() != serialized:
                raise EvidenceStoreError(f"Immutable record already exists: {namespace} {record_id!r}")
            return
        _atomic_write(path, serialized)

    def create_attempt(self, attempt_id: str, value: Any) -> None:
        path = self._attempt_path(attempt_id)
        if path.exists():
            raise EvidenceStoreError(f"Attempt already exists: {attempt_id}")
        _atomic_write(path, _json_bytes({"finalized": False, "value": value}))

    def update_active_attempt(self, attempt_id: str, value: Any) -> None:
        path, _ = self._active_attempt(attempt_id)
        _atomic_write(path, _json_bytes({"finalized": False, "value": value}))

    def finalize_attempt(self, attempt_id: str, value: Any) -> None:
        path, _ = self._active_attempt(attempt_id)
        _atomic_write(path, _json_bytes({"finalized": True, "value": value}))

    def get_record(self, namespace: str, record_id: object) -> Any | None:
        path = self._record_path(namespace, record_id)
        if not path.is_file():
            return None
        if namespace == "blob":
            return path.read_bytes()
        value = self._read_json(path)
        return value["value"] if namespace == "attempt" else value

    def record_exists(self, namespace: str, record_id: object) -> bool:
        return self._record_path(namespace, record_id).is_file()

    def _active_attempt(self, attempt_id: str) -> tuple[Path, dict[str, Any]]:
        path = self._attempt_path(attempt_id)
        if not path.is_file():
            raise EvidenceStoreError(f"Attempt does not exist: {attempt_id}")
        attempt = self._read_json(path)
        if attempt.get("finalized") is not False or "value" not in attempt:
            raise EvidenceStoreError(f"Attempt is finalized: {attempt_id}")
        return path, attempt

    def _record_path(self, namespace: str, record_id: object) -> Path:
        if namespace == "blob":
            digest = _segment(str(record_id).removeprefix("sha256:"), "blob reference")
            if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
                raise EvidenceStoreError(f"Invalid blob reference: {record_id!r}")
            return self.root / "blobs" / "sha256" / digest[:2] / digest
        if namespace == "project_snapshot":
            return self.root / "project" / "snapshots" / f"{_segment(record_id, 'project snapshot id')}.json"
        if namespace == "attempt":
            return self._attempt_path(_segment(record_id, "attempt id"))
        if namespace == "task_revision":
            task_id, revision_id = self._pair(record_id, "task revision")
            return self.root / "tasks" / task_id / "revisions" / f"{revision_id}.json"
        if namespace == "association":
            attempt_id, association_id = self._pair(record_id, "association")
            return self.root / "attempts" / attempt_id / "associations" / f"{association_id}.json"
        raise EvidenceStoreError(f"Unsupported record namespace: {namespace!r}")

    def _attempt_path(self, attempt_id: str) -> Path:
        return self.root / "attempts" / _segment(attempt_id, "attempt id") / "attempt.json"

    @staticmethod
    def _pair(record_id: object, name: str) -> tuple[str, str]:
        if not isinstance(record_id, tuple) or len(record_id) != 2:
            raise EvidenceStoreError(f"{name} id must be a two-item tuple")
        return _segment(record_id[0], f"{name} parent id"), _segment(record_id[1], f"{name} id")

    @staticmethod
    def _read_json(path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise EvidenceStoreError(f"Invalid JSON record: {path}") from exc
