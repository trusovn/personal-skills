#!/usr/bin/env python3
"""Capture raw begin/finish facts around one bounded-task-implementer invocation."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import time
from typing import Any
import uuid

from runtime_context import RuntimeContextError, load_runtime_context
from workflow_version import WorkflowVersionError, get_workflow_version


SCHEMA_VERSION = 1
WORKFLOW_ID = "bounded-task-implementer"
CLOSURE_OUTCOMES = ("completed", "reported_interrupted", "failed")
SNAPSHOT_REF_PREFIX = "refs/personal-skills/run-evidence"
RUN_ID_RE = re.compile(r"^run-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}$")


class RunEvidenceError(RuntimeError):
    pass


class ActiveRunError(RunEvidenceError):
    def __init__(self, run_id: str):
        super().__init__(f"Open implementation run already exists: {run_id}")
        self.run_id = run_id


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git(repo_root: Path, *args: str, env: dict[str, str] | None = None) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        diagnostic = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise RunEvidenceError(f"git {' '.join(args)} failed: {diagnostic}") from exc
    return result.stdout


def repository_root(start: str | Path = ".") -> Path:
    start_path = Path(start).resolve()
    root = _git(start_path, "rev-parse", "--show-toplevel").strip()
    return Path(root).resolve()


def storage_root(repo_root: Path) -> Path:
    git_dir = _git(repo_root, "rev-parse", "--absolute-git-dir").strip()
    root = Path(git_dir) / "personal-skills" / "run-evidence"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RunEvidenceError(f"Run evidence file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RunEvidenceError(f"Run evidence file is invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RunEvidenceError(f"Run evidence file must contain a JSON object: {path}")
    return value


def _validate_run_id(run_id: str) -> str:
    if not RUN_ID_RE.fullmatch(run_id):
        raise RunEvidenceError(f"Invalid run id: {run_id!r}")
    return run_id


def _run_dir(root: Path, run_id: str) -> Path:
    return root / "runs" / _validate_run_id(run_id)


def _manifest_path(root: Path, run_id: str) -> Path:
    return _run_dir(root, run_id) / "manifest.json"


def _active_path(root: Path) -> Path:
    return root / "active.json"


def _open_run_ids(root: Path) -> list[str]:
    runs_root = root / "runs"
    if not runs_root.exists():
        return []
    open_ids: list[str] = []
    for manifest_path in sorted(runs_root.glob("*/manifest.json")):
        try:
            manifest = _read_json(manifest_path)
        except RunEvidenceError:
            continue
        session = manifest.get("session")
        closure = manifest.get("closure")
        if (
            isinstance(session, dict)
            and session.get("finished_at") is None
            and isinstance(closure, dict)
            and closure.get("kind") is None
        ):
            run_id = manifest.get("run_id")
            if isinstance(run_id, str) and RUN_ID_RE.fullmatch(run_id):
                open_ids.append(run_id)
    return open_ids


def active_run_id(root: Path) -> str | None:
    active_path = _active_path(root)
    if active_path.exists():
        active = _read_json(active_path)
        run_id = active.get("run_id")
        if isinstance(run_id, str) and run_id:
            manifest_path = _manifest_path(root, run_id)
            if manifest_path.is_file():
                manifest = _read_json(manifest_path)
                if manifest.get("session", {}).get("finished_at") is None:
                    return run_id
    open_ids = _open_run_ids(root)
    if len(open_ids) > 1:
        raise RunEvidenceError(
            "Multiple open implementation runs exist: " + ", ".join(open_ids)
        )
    return open_ids[0] if open_ids else None


def _repository_branch(repo_root: Path) -> str | None:
    branch = _git(repo_root, "branch", "--show-current").strip()
    return branch or None


def _snapshot_ref(run_id: str, boundary: str) -> str:
    return f"{SNAPSHOT_REF_PREFIX}/{run_id}/{boundary}"


def _capture_worktree_tree(repo_root: Path, run_id: str, boundary: str) -> str:
    root = storage_root(repo_root)
    tmp_root = root / "tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="snapshot-", dir=tmp_root) as tempdir:
        index_path = Path(tempdir) / "index"
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(index_path)
        _git(repo_root, "read-tree", "HEAD", env=env)
        _git(repo_root, "add", "-A", "--", ".", env=env)
        tree = _git(repo_root, "write-tree", env=env).strip()
    _git(repo_root, "update-ref", _snapshot_ref(run_id, boundary), tree)
    return tree


def repository_facts(repo_root: Path, run_id: str, boundary: str) -> dict[str, Any]:
    head = _git(repo_root, "rev-parse", "HEAD").strip()
    branch = _repository_branch(repo_root)
    dirty = bool(
        _git(repo_root, "status", "--porcelain=v1", "--untracked-files=all").strip()
    )
    snapshot = _capture_worktree_tree(repo_root, run_id, boundary)
    return {
        "head": head,
        "branch": branch,
        "dirty": dirty,
        "snapshot": snapshot,
    }


def _normalize_brief(repo_root: Path, brief: str | None) -> str | None:
    if brief is None:
        return None
    path = Path(brief)
    resolved = path.resolve() if path.is_absolute() else (repo_root / path).resolve()
    if not resolved.is_file():
        raise RunEvidenceError(f"Task brief does not exist: {brief}")
    try:
        return resolved.relative_to(repo_root).as_posix()
    except ValueError:
        return str(resolved)


def _new_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"run-{stamp}-{uuid.uuid4().hex[:12]}"


def begin_run(
    repo_root: Path,
    *,
    task_id: str | None = None,
    task_brief: str | None = None,
    runtime_context_path: str | Path | None = None,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    root = storage_root(repo_root)
    existing = active_run_id(root)
    if existing is not None:
        raise ActiveRunError(existing)

    run_id = _new_run_id()
    workflow = get_workflow_version(repo_root, WORKFLOW_ID)
    runtime = load_runtime_context(runtime_context_path)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "session": {
            "started_at": _now(),
            "finished_at": None,
        },
        "closure": {
            "kind": None,
            "outcome": None,
            "recovered_at": None,
        },
        "task": {
            "id": task_id,
            "brief": _normalize_brief(repo_root, task_brief),
        },
        "workflow": {
            "id": WORKFLOW_ID,
            "fingerprint": workflow["fingerprint"],
        },
        "runtime": runtime,
        "repository": {
            "begin": repository_facts(repo_root, run_id, "begin"),
            "finish": None,
        },
        "checks": [],
    }
    manifest_path = _manifest_path(root, run_id)
    _atomic_write_json(manifest_path, manifest)
    _atomic_write_json(_active_path(root), {"run_id": run_id})
    return manifest


def load_run(repo_root: Path, run_id: str) -> tuple[Path, dict[str, Any]]:
    root = storage_root(repo_root)
    path = _manifest_path(root, run_id)
    return path, _read_json(path)


def _ensure_open(manifest: dict[str, Any], run_id: str) -> None:
    if manifest.get("run_id") != run_id:
        raise RunEvidenceError(f"Run manifest identity mismatch for {run_id}")
    if manifest.get("session", {}).get("finished_at") is not None:
        raise RunEvidenceError(f"Run is already closed: {run_id}")
    if manifest.get("closure", {}).get("kind") is not None:
        raise RunEvidenceError(f"Run already has closure facts: {run_id}")


def _clear_active(root: Path, run_id: str) -> None:
    path = _active_path(root)
    if not path.exists():
        return
    active = _read_json(path)
    if active.get("run_id") == run_id:
        path.unlink()


def finish_run(repo_root: Path, run_id: str, outcome: str) -> dict[str, Any]:
    if outcome not in CLOSURE_OUTCOMES:
        raise RunEvidenceError(f"Unsupported closure outcome: {outcome}")
    repo_root = Path(repo_root).resolve()
    root = storage_root(repo_root)
    manifest_path, manifest = load_run(repo_root, run_id)
    _ensure_open(manifest, run_id)
    finished_at = _now()
    manifest["repository"]["finish"] = repository_facts(repo_root, run_id, "finish")
    manifest["session"]["finished_at"] = finished_at
    manifest["closure"] = {
        "kind": "explicit_finish",
        "outcome": outcome,
        "recovered_at": None,
    }
    _atomic_write_json(manifest_path, manifest)
    _clear_active(root, run_id)
    return manifest


def recover_run(repo_root: Path, run_id: str) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    root = storage_root(repo_root)
    manifest_path, manifest = load_run(repo_root, run_id)
    _ensure_open(manifest, run_id)
    recovered_at = _now()
    manifest["repository"]["finish"] = repository_facts(repo_root, run_id, "recovery")
    manifest["session"]["finished_at"] = recovered_at
    manifest["closure"] = {
        "kind": "recovered_after_missing_finish",
        "outcome": None,
        "recovered_at": recovered_at,
    }
    _atomic_write_json(manifest_path, manifest)
    _clear_active(root, run_id)
    return manifest


def run_check(
    repo_root: Path,
    run_id: str,
    kind: str,
    command: list[str],
) -> tuple[dict[str, Any], int]:
    if not kind.strip():
        raise RunEvidenceError("Check kind must be non-empty")
    if not command:
        raise RunEvidenceError("Check command is required")
    repo_root = Path(repo_root).resolve()
    manifest_path, manifest = load_run(repo_root, run_id)
    _ensure_open(manifest, run_id)

    started_at = _now()
    started = time.monotonic_ns()
    try:
        result = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        duration_ms = (time.monotonic_ns() - started) // 1_000_000
        check = {
            "kind": kind,
            "command": shlex.join(command),
            "started_at": started_at,
            "duration_ms": duration_ms,
            "exit_code": None,
            "stdout": "",
            "stderr": str(exc),
        }
        manifest["checks"].append(check)
        _atomic_write_json(manifest_path, manifest)
        raise RunEvidenceError(f"Cannot execute check command: {exc}") from exc

    duration_ms = (time.monotonic_ns() - started) // 1_000_000
    check = {
        "kind": kind,
        "command": shlex.join(command),
        "started_at": started_at,
        "duration_ms": duration_ms,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    manifest["checks"].append(check)
    _atomic_write_json(manifest_path, manifest)
    return check, result.returncode


def _print_json(value: dict[str, Any]) -> None:
    print(json.dumps(value, sort_keys=True))


def _cli_repo(args: argparse.Namespace) -> Path:
    return repository_root(args.repo)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capture raw bounded implementation run facts.")
    parser.add_argument("--repo", default=".", help="Path inside the target Git worktree")
    subparsers = parser.add_subparsers(dest="command", required=True)

    begin = subparsers.add_parser("begin", help="Capture the beginning of one implementation run")
    begin.add_argument("--task-id")
    begin.add_argument("--task-brief")
    begin.add_argument("--runtime-context")

    subparsers.add_parser("active", help="Show the current open run for this worktree")

    finish = subparsers.add_parser("finish", help="Explicitly close a run")
    finish.add_argument("run_id")
    finish.add_argument("--outcome", choices=CLOSURE_OUTCOMES, default="completed")

    recover = subparsers.add_parser(
        "recover", help="Close a run whose original invocation never recorded finish"
    )
    recover.add_argument("run_id")

    check = subparsers.add_parser("check", help="Execute one deterministic check and record raw facts")
    check.add_argument("run_id")
    check.add_argument("--kind", required=True)
    check.add_argument("command_argv", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        repo_root = _cli_repo(args)
        if args.command == "begin":
            manifest = begin_run(
                repo_root,
                task_id=args.task_id,
                task_brief=args.task_brief,
                runtime_context_path=args.runtime_context,
            )
            root = storage_root(repo_root)
            _print_json(
                {
                    "run_id": manifest["run_id"],
                    "manifest": str(_manifest_path(root, manifest["run_id"])),
                }
            )
            return 0
        if args.command == "active":
            root = storage_root(repo_root)
            run_id = active_run_id(root)
            _print_json(
                {
                    "active": None
                    if run_id is None
                    else {
                        "run_id": run_id,
                        "manifest": str(_manifest_path(root, run_id)),
                    }
                }
            )
            return 0
        if args.command == "finish":
            manifest = finish_run(repo_root, args.run_id, args.outcome)
            _print_json(
                {
                    "run_id": manifest["run_id"],
                    "closure": manifest["closure"],
                    "repository_finish": manifest["repository"]["finish"],
                }
            )
            return 0
        if args.command == "recover":
            manifest = recover_run(repo_root, args.run_id)
            _print_json(
                {
                    "run_id": manifest["run_id"],
                    "closure": manifest["closure"],
                    "repository_finish": manifest["repository"]["finish"],
                }
            )
            return 0
        if args.command == "check":
            command = args.command_argv
            if command and command[0] == "--":
                command = command[1:]
            check, exit_code = run_check(repo_root, args.run_id, args.kind, command)
            if check["stdout"]:
                sys.stdout.write(check["stdout"])
            if check["stderr"]:
                sys.stderr.write(check["stderr"])
            return 128 + abs(exit_code) if exit_code < 0 else exit_code
    except ActiveRunError as exc:
        print(
            json.dumps(
                {"error": str(exc), "active_run_id": exc.run_id, "ok": False},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 3
    except (RunEvidenceError, RuntimeContextError, WorkflowVersionError) as exc:
        print(json.dumps({"error": str(exc), "ok": False}, sort_keys=True), file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
