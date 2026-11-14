"""Run-file persistence and command-lock resource lifecycle.

The controller authorizes transitions and owns transaction scope/order. These
primitives never choose a stage, launch a process, or mutate a ledger value.
Transport-local persistence remains owned by codex_worker; no adapter dependency.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object; reject malformed/non-object input without mutation."""
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    """Atomic replacement, pretty JSON + newline; no fsync or temp cleanup promise."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def sync_directory(path: Path) -> None:
    """Fsync an existing directory; propagate failures and always close its fd."""
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_durable_exclusive(path: Path, content: bytes) -> None:
    """Fsync bytes, link without overwrite, then sync parent; clean temp on failure.

    A failure after linking can leave the destination published. Callers retain
    their existing uncertain-publication/replay handling; no rollback is implied.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
        sync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def canonical_record_bytes(record: dict[str, Any]) -> bytes:
    """Canonical compact sorted JSON bytes, with no trailing newline."""
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode()


def publish_or_reuse_record(
    path: Path,
    record: dict[str, Any],
    validator: Callable[[dict[str, Any]], None],
) -> tuple[dict[str, Any], str]:
    """Validate and publish canonical JSON, or reuse exactly equal validated bytes.

    The caller supplies its record validator; storage owns no schema/policy. New
    files use exclusive direct creation and file fsync, without directory sync.
    A failed write may leave a partial file; replay validates rather than repairs.
    """
    validator(record)
    serialized = canonical_record_bytes(record)
    if path.exists():
        existing_bytes = path.read_bytes()
        try:
            existing = json.loads(existing_bytes)
        except json.JSONDecodeError as error:
            raise ValueError(f"Existing record is invalid: {path.name}") from error
        validator(existing)
        if existing_bytes != serialized:
            raise ValueError(f"Existing record bytes contradict inspection: {path.name}")
        return existing, hashlib.sha256(existing_bytes).hexdigest()
    with path.open("xb") as stream:
        stream.write(serialized)
        stream.flush()
        os.fsync(stream.fileno())
    return json.loads(serialized), hashlib.sha256(serialized).hexdigest()


def publish_or_reuse_bytes(path: Path, content: bytes) -> None:
    """Reuse exact existing bytes or publish durably/exclusively; reject conflicts.

    Replay does not resync existing bytes. The caller holds transaction authority.
    """
    if path.exists():
        if path.read_bytes() != content:
            raise ValueError(f"Conflicting prepared actor record: {path.name}")
        return
    write_durable_exclusive(path, content)


class RunCommandLock:
    """One non-blocking local lock for an existing run."""

    def __init__(self, run_dir: Path):
        self.path = run_dir / "controller.lock"
        self.stream = None

    def acquire(self) -> None:
        if self.stream is not None:
            return
        stream = self.path.open("a+")
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            stream.close()
            raise ValueError(
                "Another controller command owns this run's mutation phase"
            )
        self.stream = stream

    def release(self) -> None:
        if self.stream is None:
            return
        fcntl.flock(self.stream.fileno(), fcntl.LOCK_UN)
        self.stream.close()
        self.stream = None

    def __enter__(self) -> "RunCommandLock":
        self.acquire()
        return self

    def __exit__(self, *_args: object) -> None:
        self.release()
