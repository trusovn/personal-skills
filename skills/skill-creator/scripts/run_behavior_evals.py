#!/usr/bin/env python3
"""Run Codex-backed skill evals from structured eval metadata."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import string
import subprocess
import sys
import tempfile
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", type=Path, help="current skill directory")
    parser.add_argument("--ids", help="comma-separated eval IDs (default: all)")
    parser.add_argument("--baseline-skill", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--reasoning")
    return parser.parse_args()


def parse_ids(value: str | None, available: list[int]) -> list[int]:
    if value is None:
        return available
    try:
        selected = [int(part.strip()) for part in value.split(",") if part.strip()]
    except ValueError as exc:
        raise ValueError("--ids must contain comma-separated integers") from exc
    if not selected:
        raise ValueError("--ids must select at least one eval")
    missing = [eval_id for eval_id in selected if eval_id not in available]
    if missing:
        raise ValueError(f"unknown eval IDs: {', '.join(map(str, missing))}")
    if len(selected) != len(set(selected)):
        raise ValueError("--ids must not contain duplicates")
    return selected


def load_evals(skill: Path) -> list[dict[str, Any]]:
    eval_path = skill / "evals" / "evals.json"
    data = json.loads(eval_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("evals.json must contain an object")
    evals = data.get("evals")
    if not isinstance(evals, list):
        raise ValueError("evals.json must contain an evals array")
    ids = [entry.get("id") for entry in evals if isinstance(entry, dict)]
    if len(ids) != len(evals) or any(type(eval_id) is not int for eval_id in ids):
        raise ValueError("every eval must have an integer id")
    if len(ids) != len(set(ids)):
        raise ValueError("eval IDs must be unique")
    return evals


def ensure_skill(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not (resolved / "SKILL.md").is_file():
        raise ValueError(f"{label} does not contain SKILL.md: {resolved}")
    return resolved


def reject_unknown_placeholders(value: str, field: str) -> None:
    try:
        parsed = list(string.Formatter().parse(value))
    except ValueError as exc:
        raise ValueError(f"{field} contains an invalid placeholder") from exc
    fields = {
        field_name
        for _, field_name, _, _ in parsed
        if field_name is not None
    }
    unknown = fields - {"run_root"}
    if unknown:
        raise ValueError(
            f"{field} contains unknown placeholders: {', '.join(sorted(unknown))}"
        )
    if any(
        field_name == "run_root" and (format_spec or conversion)
        for _, field_name, format_spec, conversion in parsed
    ):
        raise ValueError(f"{field} may use only the literal {{run_root}} placeholder")


def resolve_inside(template: str, run_root: Path, field: str) -> Path:
    reject_unknown_placeholders(template, field)
    resolved = Path(template.format(run_root=str(run_root))).resolve()
    if not resolved.is_relative_to(run_root):
        raise ValueError(f"{field} must resolve inside the run directory")
    return resolved


def execution_plan(
    eval_entry: dict[str, Any], skill: Path, run_root: Path
) -> tuple[list[str] | None, Path | None, dict[str, str], Path]:
    execution = eval_entry.get("execution")
    if execution is None:
        workspace = run_root / "work"
        workspace.mkdir(parents=True)
        return None, None, {}, workspace
    if not isinstance(execution, dict):
        raise ValueError("execution must be an object")

    setup = execution.get("setup")
    if setup is None:
        if "workspace" in execution:
            raise ValueError("workspace is only valid when setup is present")
        workspace = run_root / "work"
        workspace.mkdir(parents=True)
        return None, None, {}, workspace
    if not isinstance(setup, dict):
        raise ValueError("execution.setup must be an object")

    command = setup.get("command")
    if (
        not isinstance(command, list)
        or not command
        or any(not isinstance(argument, str) or not argument for argument in command)
    ):
        raise ValueError("execution.setup.command must be a non-empty argument array")

    cwd_value = setup.get("cwd", ".")
    if not isinstance(cwd_value, str):
        raise ValueError("execution.setup.cwd must be a string")
    cwd = (skill / cwd_value).resolve()
    if not cwd.is_relative_to(skill) or not cwd.is_dir():
        raise ValueError("execution.setup.cwd must resolve inside the current skill")

    env_value = setup.get("env", {})
    if not isinstance(env_value, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in env_value.items()
    ):
        raise ValueError("execution.setup.env must map strings to strings")
    env: dict[str, str] = {}
    for key, value in env_value.items():
        reject_unknown_placeholders(value, f"execution.setup.env.{key}")
        env[key] = value.format(run_root=str(run_root))

    workspace_value = execution.get("workspace")
    if not isinstance(workspace_value, str):
        raise ValueError("execution.workspace is required when setup is present")
    workspace = resolve_inside(workspace_value, run_root, "execution.workspace")
    return command, cwd, env, workspace


def git_status_paths(workspace: Path) -> list[str]:
    if not (workspace / ".git").exists():
        return []
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(workspace),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode != 0:
        return []
    return [line[3:] for line in completed.stdout.splitlines() if len(line) >= 4]


def write_result(
    run_dir: Path,
    *,
    eval_id: int,
    configuration: str,
    model: str | None,
    reasoning: str | None,
    setup_exit_code: int | None,
    codex_exit_code: int | None,
    workspace: Path,
    error: str | None,
) -> None:
    result = {
        "eval_id": eval_id,
        "configuration": configuration,
        "model": model,
        "reasoning": reasoning,
        "setup_exit_code": setup_exit_code,
        "codex_exit_code": codex_exit_code,
        "workspace": str(workspace.resolve()),
        "git_status_paths": git_status_paths(workspace),
        "error": error,
    }
    (run_dir / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )


def run_one(
    eval_entry: dict[str, Any],
    configuration: str,
    selected_skill: Path,
    setup_skill: Path,
    output_dir: Path,
    model: str | None,
    reasoning: str | None,
) -> bool:
    eval_id = eval_entry["id"]
    run_dir = output_dir / configuration / f"eval-{eval_id}"
    run_dir.mkdir(parents=True)
    final_response = run_dir / "final-response.txt"
    final_response.write_text("", encoding="utf-8")
    workspace = run_dir / "work"
    setup_exit_code: int | None = None
    codex_exit_code: int | None = None
    error: str | None = None

    prompt = eval_entry.get("prompt")
    if not isinstance(prompt, str):
        error = "eval prompt must be a string"
        effective_prompt = ""
    else:
        effective_prompt = (
            f"Read and follow the skill at {selected_skill / 'SKILL.md'}.\n\n"
            f"{prompt}"
        )
    (run_dir / "effective-prompt.txt").write_text(
        effective_prompt, encoding="utf-8"
    )

    try:
        command, setup_cwd, setup_env, workspace = execution_plan(
            eval_entry, setup_skill, run_dir.resolve()
        )
        if error is not None:
            raise ValueError(error)

        if command is not None:
            setup = subprocess.run(
                command,
                cwd=setup_cwd,
                env={**os.environ, **setup_env},
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            setup_exit_code = setup.returncode
            if setup.stderr:
                (run_dir / "stderr.txt").write_text(
                    setup.stderr, encoding="utf-8"
                )
            if setup.returncode != 0:
                raise RuntimeError(f"setup exited with code {setup.returncode}")

        workspace = workspace.resolve()
        if not workspace.is_relative_to(run_dir.resolve()):
            raise RuntimeError(
                "declared workspace must remain inside the run directory after setup"
            )
        if not workspace.is_dir():
            raise RuntimeError(f"declared workspace was not created: {workspace}")

        codex_command = [
            "codex",
            "exec",
            "--ephemeral",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "-C",
            str(workspace),
            "-o",
            str(final_response),
        ]
        if model is not None:
            codex_command.extend(["--model", model])
        if reasoning is not None:
            codex_command.extend(
                ["--config", f"model_reasoning_effort={json.dumps(reasoning)}"]
            )
        codex_command.append(effective_prompt)
        codex = subprocess.run(
            codex_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        codex_exit_code = codex.returncode
        if codex.stderr:
            stderr_path = run_dir / "stderr.txt"
            previous = (
                stderr_path.read_text(encoding="utf-8")
                if stderr_path.exists()
                else ""
            )
            stderr_path.write_text(previous + codex.stderr, encoding="utf-8")
        if codex.returncode != 0:
            error = f"codex exited with code {codex.returncode}"
    except (OSError, ValueError, RuntimeError) as exc:
        error = str(exc)

    write_result(
        run_dir,
        eval_id=eval_id,
        configuration=configuration,
        model=model,
        reasoning=reasoning,
        setup_exit_code=setup_exit_code,
        codex_exit_code=codex_exit_code,
        workspace=workspace,
        error=error,
    )
    return error is None


def main() -> int:
    args = parse_args()
    try:
        skill = ensure_skill(args.skill, "skill")
        baseline = (
            ensure_skill(args.baseline_skill, "baseline skill")
            if args.baseline_skill
            else None
        )
        evals = load_evals(skill)
        available_ids = [entry["id"] for entry in evals]
        selected_ids = parse_ids(args.ids, available_ids)
        selected = [entry for entry in evals if entry["id"] in selected_ids]

        if args.output_dir:
            output_dir = args.output_dir.resolve()
            output_dir.mkdir(parents=True, exist_ok=False)
        else:
            output_dir = Path(
                tempfile.mkdtemp(prefix="skill-behavior-evals-")
            ).resolve()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"output: {output_dir}")
    results: list[tuple[str, int, bool]] = []
    configurations = [("current", skill)]
    if baseline is not None:
        configurations.append(("baseline", baseline))
    for configuration, selected_skill in configurations:
        for eval_entry in selected:
            succeeded = run_one(
                eval_entry,
                configuration,
                selected_skill,
                skill,
                output_dir,
                args.model,
                args.reasoning,
            )
            results.append((configuration, eval_entry["id"], succeeded))
            print(
                f"{configuration} eval-{eval_entry['id']}: "
                f"{'completed' if succeeded else 'failed'}"
            )

    failures = sum(not succeeded for _, _, succeeded in results)
    print(f"summary: {len(results) - failures} completed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
