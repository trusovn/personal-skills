#!/usr/bin/env python3
"""Run or resume one Codex worker while keeping its transcript out of context."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


SCHEMA = Path(__file__).parents[1] / "assets" / "worker-result.schema.json"
RESULT_STATUSES = {"complete", "needs_input", "blocked", "failed"}


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def result_status(path: Path) -> str | None:
    try:
        status = read_json(path).get("status")
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
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


def run_turn(
    *,
    command: list[str],
    state_path: Path,
    state: dict[str, Any],
    events_path: Path,
    stderr_path: Path,
    result_path: Path,
) -> int:
    state.update(
        status="starting",
        exit_code=None,
        events_path=str(events_path),
        stderr_path=str(stderr_path),
        result_path=str(result_path),
    )
    atomic_write_json(state_path, state)

    with events_path.open("w") as events, stderr_path.open("w") as errors:
        process = subprocess.Popen(
            command,
            cwd=state["cwd"],
            stdout=subprocess.PIPE,
            stderr=errors,
            text=True,
            bufsize=1,
        )
        state.update(status="running", process_pid=process.pid)
        atomic_write_json(state_path, state)

        assert process.stdout is not None
        for line in process.stdout:
            events.write(line)
            events.flush()
            thread_id = parse_thread_id(line)
            if thread_id and not state.get("thread_id"):
                state["thread_id"] = thread_id
                atomic_write_json(state_path, state)

        exit_code = process.wait()

    state["process_pid"] = None
    state["exit_code"] = exit_code
    if exit_code != 0:
        state["status"] = "interrupted" if state.get("thread_id") else "failed_to_start"
        wrapper_exit = exit_code
    else:
        state["status"] = result_status(result_path) or "missing_result"
        wrapper_exit = 0 if state["status"] in RESULT_STATUSES else 3
    atomic_write_json(state_path, state)

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

    cwd = Path(args.cwd).resolve()
    prompt_path = Path(args.prompt_file).resolve()
    if not cwd.is_dir():
        raise ValueError(f"Working directory does not exist: {cwd}")
    prompt = prompt_path.read_text()

    run_dir.mkdir(parents=True, exist_ok=True)
    turn = 1
    result_path = run_dir / f"turn-{turn:03d}.result.json"
    events_path = run_dir / f"turn-{turn:03d}.events.jsonl"
    stderr_path = run_dir / f"turn-{turn:03d}.stderr.log"
    state: dict[str, Any] = {
        "version": 1,
        "thread_id": None,
        "turn": turn,
        "cwd": str(cwd),
        "prompt_path": str(prompt_path),
        "model": args.model,
        "effort": args.effort,
        "sandbox": args.sandbox,
    }

    command = [
        args.codex_bin,
        "exec",
        "--json",
        "--output-schema",
        str(SCHEMA),
        "-o",
        str(result_path),
        "--sandbox",
        args.sandbox,
        "--ask-for-approval",
        "never",
    ]
    if args.model:
        command.extend(["--model", args.model])
    if args.effort:
        command.extend(["--config", f'model_reasoning_effort="{args.effort}"'])
    command.append(prompt)

    return run_turn(
        command=command,
        state_path=state_path,
        state=state,
        events_path=events_path,
        stderr_path=stderr_path,
        result_path=result_path,
    )


def resume(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state_path = run_dir / "state.json"
    state = read_json(state_path)
    thread_id = state.get("thread_id")
    if not isinstance(thread_id, str) or not thread_id:
        raise ValueError(f"Run at {run_dir} has no recorded thread id and cannot be resumed")

    prompt_path = Path(args.prompt_file).resolve()
    prompt = prompt_path.read_text()
    turn = int(state.get("turn", 0)) + 1
    state.update(turn=turn, prompt_path=str(prompt_path))
    result_path = run_dir / f"turn-{turn:03d}.result.json"
    events_path = run_dir / f"turn-{turn:03d}.events.jsonl"
    stderr_path = run_dir / f"turn-{turn:03d}.stderr.log"

    command = [
        args.codex_bin,
        "exec",
        "resume",
        "--json",
        "--output-schema",
        str(SCHEMA),
        "-o",
        str(result_path),
        thread_id,
        prompt,
    ]

    return run_turn(
        command=command,
        state_path=state_path,
        state=state,
        events_path=events_path,
        stderr_path=stderr_path,
        result_path=result_path,
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
    start_parser.add_argument("--codex-bin", default="codex", help=argparse.SUPPRESS)
    start_parser.set_defaults(handler=start)

    resume_parser = subparsers.add_parser("resume", help="Resume the recorded worker thread")
    resume_parser.add_argument("--run-dir", required=True)
    resume_parser.add_argument("--prompt-file", required=True)
    resume_parser.add_argument("--codex-bin", default="codex", help=argparse.SUPPRESS)
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
