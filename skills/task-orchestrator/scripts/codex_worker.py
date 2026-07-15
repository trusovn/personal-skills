#!/usr/bin/env python3
"""Run or resume one Codex worker while keeping its transcript out of context."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
from typing import Any


SCHEMA = Path(__file__).parents[1] / "assets" / "worker-result.schema.json"
RESULT_STATUSES = {"complete", "needs_input", "blocked", "failed"}
RESULT_FIELDS = {
    "status",
    "task_id",
    "summary",
    "files_changed",
    "verification",
    "decisions",
    "questions",
    "risks",
    "next_action",
}


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def exclusive_write_json(path: Path, value: dict[str, Any]) -> None:
    with path.open("x") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def result_status(path: Path) -> str | None:
    try:
        result = read_json(path)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None
    if set(result) != RESULT_FIELDS:
        return None
    status = result.get("status")
    if not isinstance(result.get("task_id"), str) or not result["task_id"]:
        return None
    for field in ("files_changed", "verification", "decisions", "questions", "risks"):
        if not isinstance(result.get(field), list):
            return None
    return status if status in RESULT_STATUSES else None


def parse_thread_id(line: str) -> str | None:
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        return None
    if event.get("type") != "thread.started":
        return None
    thread_id = event.get("thread_id")
    return thread_id if isinstance(thread_id, str) and thread_id else None


def safe_codex_prefix(codex_bin: str) -> list[str]:
    return [codex_bin, "--ask-for-approval", "never", "exec"]


def preflight_codex(
    codex_bin: str,
    cwd: Path,
    *,
    sandbox: str,
    resume: bool = False,
) -> None:
    command = [*safe_codex_prefix(codex_bin)]
    if resume:
        command.extend(["resume", "-c", f'sandbox_mode="{sandbox}"'])
    else:
        command.extend(["--sandbox", sandbox])
    command.append("--help")
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        diagnostic = result.stderr.strip() or result.stdout.strip() or "no diagnostic"
        raise ValueError(
            "Codex CLI does not support the required workspace-write/approval-never "
            f"command shape: {diagnostic}"
        )


def process_liveness(pid: int) -> str:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return "absent"
    except PermissionError:
        return "ambiguous"
    return "alive"


def terminate_process_group(process: subprocess.Popen[str]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=1)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait(timeout=1)


def run_turn(
    *,
    command: list[str],
    state_path: Path,
    state: dict[str, Any],
    events_path: Path,
    stderr_path: Path,
    result_path: Path,
    timeout_seconds: float | None,
) -> int:
    state.update(
        status="starting",
        exit_code=None,
        started_at=datetime.now(timezone.utc).isoformat(),
        ended_at=None,
        events_path=str(events_path),
        stderr_path=str(stderr_path),
        result_path=str(result_path),
    )
    atomic_write_json(state_path, state)

    with events_path.open("x") as events, stderr_path.open("x") as errors:
        process = subprocess.Popen(
            command,
            cwd=state["cwd"],
            stdout=subprocess.PIPE,
            stderr=errors,
            text=True,
            bufsize=1,
            start_new_session=True,
        )
        state.update(status="running", process_pid=process.pid)
        atomic_write_json(state_path, state)

        assert process.stdout is not None
        reader_errors: list[BaseException] = []

        def consume_stdout() -> None:
            try:
                for line in process.stdout:
                    events.write(line)
                    events.flush()
                    thread_id = parse_thread_id(line)
                    if thread_id and not state.get("thread_id"):
                        state["thread_id"] = thread_id
                        atomic_write_json(state_path, state)
            except BaseException as error:
                reader_errors.append(error)

        reader = threading.Thread(target=consume_stdout, daemon=True)
        reader.start()
        timed_out = False
        try:
            exit_code = process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            terminate_process_group(process)
            exit_code = process.returncode
        reader.join(timeout=1)
        if reader.is_alive():
            raise RuntimeError("Worker stdout reader did not terminate after process exit")
        if reader_errors:
            raise RuntimeError(f"Worker stdout reader failed: {reader_errors[0]}")

    state["process_pid"] = None
    state["exit_code"] = exit_code
    state["ended_at"] = datetime.now(timezone.utc).isoformat()
    if timed_out:
        state["attempt_outcome"] = "timed_out"
        state["status"] = "resumable" if state.get("thread_id") else "stopped"
        wrapper_exit = 124
    elif exit_code != 0:
        state["attempt_outcome"] = (
            "interrupted" if state.get("thread_id") else "failed_to_start"
        )
        state["status"] = "resumable" if state.get("thread_id") else "stopped"
        wrapper_exit = exit_code
    else:
        state["attempt_outcome"] = result_status(result_path) or "missing_result"
        if state["attempt_outcome"] == "complete":
            state["status"] = "awaiting_inspection"
            wrapper_exit = 0
        elif state["attempt_outcome"] in {"needs_input", "blocked"}:
            state["status"] = "resumable"
            wrapper_exit = 0
        elif state["attempt_outcome"] == "failed":
            state["status"] = "stopped"
            wrapper_exit = 0
        else:
            state["status"] = "stopped"
            wrapper_exit = 3
    atomic_write_json(state_path, state)
    terminal_path = result_path.with_suffix(".state.json")
    exclusive_write_json(terminal_path, state)

    print(
        json.dumps(
            {
                "status": state["status"],
                "thread_id": state.get("thread_id"),
                "turn": state["turn"],
                "result_path": str(result_path),
                "state_path": str(state_path),
            },
            sort_keys=True,
        )
    )
    return wrapper_exit


def start(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state_path = run_dir / "state.json"
    if state_path.exists():
        raise ValueError(f"Run already exists at {run_dir}; use resume with a follow-up prompt")
    if args.sandbox == "danger-full-access":
        raise ValueError("danger-full-access requires persisted authorization not accepted by this adapter")
    if args.timeout_seconds is not None and args.timeout_seconds <= 0:
        raise ValueError("timeout must be greater than zero")

    cwd = Path(args.cwd).resolve()
    prompt_path = Path(args.prompt_file).resolve()
    if not cwd.is_dir():
        raise ValueError(f"Working directory does not exist: {cwd}")
    prompt = prompt_path.read_text()
    preflight_codex(args.codex_bin, cwd, sandbox=args.sandbox)

    run_dir.mkdir(parents=True, exist_ok=True)
    turn = 1
    result_path = run_dir / f"turn-{turn:03d}.result.json"
    events_path = run_dir / f"turn-{turn:03d}.events.jsonl"
    stderr_path = run_dir / f"turn-{turn:03d}.stderr.log"
    durable_prompt_path = run_dir / f"turn-{turn:03d}.prompt.txt"
    with durable_prompt_path.open("x") as stream:
        stream.write(prompt)
    state: dict[str, Any] = {
        "version": 1,
        "thread_id": None,
        "turn": turn,
        "cwd": str(cwd),
        "prompt_path": str(durable_prompt_path),
        "source_prompt_path": str(prompt_path),
        "model": args.model,
        "effort": args.effort,
        "sandbox": args.sandbox,
        "approval_policy": "never",
        "network": False,
        "writable_roots": [str(cwd)],
        "transport": "codex-cli",
    }

    command = [
        *safe_codex_prefix(args.codex_bin),
        "--json",
        "--output-schema",
        str(SCHEMA),
        "-o",
        str(result_path),
        "--sandbox",
        args.sandbox,
    ]
    if args.model:
        command.extend(["--model", args.model])
    if args.effort:
        command.extend(["--config", f'model_reasoning_effort="{args.effort}"'])
    command.append(prompt)
    state["effective_command"] = command
    state["prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()

    return run_turn(
        command=command,
        state_path=state_path,
        state=state,
        events_path=events_path,
        stderr_path=stderr_path,
        result_path=result_path,
        timeout_seconds=args.timeout_seconds,
    )


def resume(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state_path = run_dir / "state.json"
    state = read_json(state_path)
    if state.get("sandbox") == "danger-full-access":
        raise ValueError("danger-full-access requires persisted authorization not accepted by this adapter")
    if args.timeout_seconds is not None and args.timeout_seconds <= 0:
        raise ValueError("timeout must be greater than zero")
    thread_id = state.get("thread_id")
    if not isinstance(thread_id, str) or not thread_id:
        raise ValueError(f"Run at {run_dir} has no recorded thread id and cannot be resumed")

    process_pid = state.get("process_pid")
    if process_pid is not None:
        if not isinstance(process_pid, int):
            raise ValueError(f"Run at {run_dir} has ambiguous process identity")
        liveness = process_liveness(process_pid)
        if liveness == "alive":
            raise ValueError(f"Recorded worker process {process_pid} is still alive")
        if liveness == "ambiguous":
            raise ValueError(f"Recorded worker process {process_pid} liveness is ambiguous")
    elif state.get("status") == "running":
        raise ValueError(f"Run at {run_dir} is running with ambiguous process identity")

    preflight_codex(
        args.codex_bin,
        Path(state["cwd"]),
        sandbox=state["sandbox"],
        resume=True,
    )

    prompt_path = Path(args.prompt_file).resolve()
    prompt = prompt_path.read_text()
    turn = int(state.get("turn", 0)) + 1
    durable_prompt_path = run_dir / f"turn-{turn:03d}.prompt.txt"
    with durable_prompt_path.open("x") as stream:
        stream.write(prompt)
    state.update(
        turn=turn,
        prompt_path=str(durable_prompt_path),
        source_prompt_path=str(prompt_path),
    )
    result_path = run_dir / f"turn-{turn:03d}.result.json"
    events_path = run_dir / f"turn-{turn:03d}.events.jsonl"
    stderr_path = run_dir / f"turn-{turn:03d}.stderr.log"

    command = [
        *safe_codex_prefix(args.codex_bin),
        "resume",
        "--json",
        "--output-schema",
        str(SCHEMA),
        "-o",
        str(result_path),
        "-c",
        f'sandbox_mode="{state["sandbox"]}"',
        thread_id,
        prompt,
    ]
    state["effective_command"] = command
    state["prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()

    return run_turn(
        command=command,
        state_path=state_path,
        state=state,
        events_path=events_path,
        stderr_path=stderr_path,
        result_path=result_path,
        timeout_seconds=args.timeout_seconds,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one Codex worker and retain only its structured handoff in normal context."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Start a new worker thread")
    start_parser.add_argument("--run-dir", required=True)
    start_parser.add_argument("--cwd", required=True)
    start_parser.add_argument("--prompt-file", required=True)
    start_parser.add_argument("--model")
    start_parser.add_argument("--effort", choices=("low", "medium", "high", "xhigh"))
    start_parser.add_argument(
        "--sandbox",
        choices=("read-only", "workspace-write", "danger-full-access"),
        default="workspace-write",
    )
    start_parser.add_argument("--timeout-seconds", type=float)
    start_parser.add_argument("--codex-bin", default="codex", help=argparse.SUPPRESS)
    start_parser.set_defaults(handler=start)

    resume_parser = subparsers.add_parser("resume", help="Resume the recorded worker thread")
    resume_parser.add_argument("--run-dir", required=True)
    resume_parser.add_argument("--prompt-file", required=True)
    resume_parser.add_argument("--codex-bin", default="codex", help=argparse.SUPPRESS)
    resume_parser.add_argument("--timeout-seconds", type=float)
    resume_parser.set_defaults(handler=resume)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    sys.exit(main())
