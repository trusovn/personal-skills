#!/usr/bin/env python3
"""Delegate a bounded read-only repository task to an Ollama-backed model."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

TRANSIENT_PARTS = {"__pycache__", "node_modules", ".git"}
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".go", ".rs",
    ".sh", ".bash", ".zsh", ".xml", ".html", ".css", ".sql",
}
MAX_SKILL_FILE_BYTES = 256_000
MAX_SEARCH_MATCHES = 200

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files recursively under a repository-relative path.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_text",
            "description": "Search literal text in repository files under a relative path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "path": {"type": "string"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a repository text file with optional 1-based line bounds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "start_line": {"type": "integer", "minimum": 1},
                    "end_line": {"type": "integer", "minimum": 1},
                },
                "required": ["path"],
            },
        },
    },
]


class DelegateError(RuntimeError):
    pass


def installation_root(script_path: Path) -> Path:
    scripts_dir = script_path.resolve().parent
    if scripts_dir.name != "scripts":
        raise DelegateError(f"runtime must live in a scripts directory: {scripts_dir}")
    return scripts_dir.parent


def skills_root(script_path: Path) -> Path:
    root = installation_root(script_path)
    candidate = root / "skills"
    if not candidate.is_dir():
        raise DelegateError(f"matching skills directory is missing: {candidate}")
    return candidate


def default_config_path(script_path: Path) -> Path:
    return script_path.resolve().with_name("ollama-models.json")


def load_config(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DelegateError(f"cannot read model config {path}: {exc}") from exc
    if data.get("schema_version") != 1:
        raise DelegateError("unsupported ollama model config schema_version")
    if not isinstance(data.get("models"), dict) or not data["models"]:
        raise DelegateError("model config must contain a non-empty models object")
    return data


def discover_skills(root: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for skill_file in sorted(root.rglob("SKILL.md")):
        if any(part in TRANSIENT_PARTS for part in skill_file.parts):
            continue
        name = _frontmatter_name(skill_file)
        if not name:
            continue
        if name in found:
            raise DelegateError(f"duplicate skill id {name!r}: {found[name]} and {skill_file.parent}")
        found[name] = skill_file.parent
    return found


def _frontmatter_name(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    for line in text[4:end].splitlines():
        if line.startswith("name:"):
            value = line.split(":", 1)[1].strip()
            return value or None
    return None


def skill_package(skill_dir: Path) -> str:
    blocks: list[str] = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(skill_dir)
        if any(part in TRANSIENT_PARTS or part in {"tests", "evals"} for part in relative.parts):
            continue
        if path.stat().st_size > MAX_SKILL_FILE_BYTES:
            continue
        if path.name != "SKILL.md" and path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        blocks.append(f"\n--- skill file: {relative.as_posix()} ---\n{content}")
    if not blocks:
        raise DelegateError(f"skill package has no readable text files: {skill_dir}")
    return "".join(blocks)


class ReadOnlyTools:
    def __init__(self, repo: Path):
        self.repo = repo.resolve()

    def _path(self, relative: str, *, require_exists: bool = True) -> Path:
        candidate = (self.repo / relative).resolve()
        if candidate != self.repo and self.repo not in candidate.parents:
            raise DelegateError(f"path escapes repository: {relative}")
        if require_exists and not candidate.exists():
            raise DelegateError(f"path does not exist: {relative}")
        return candidate

    def execute(self, name: str, args: dict[str, Any]) -> str:
        try:
            if name == "list_files":
                return self.list_files(args.get("path", "."))
            if name == "search_text":
                return self.search_text(args["query"], args.get("path", "."))
            if name == "read_file":
                return self.read_file(
                    args["path"],
                    int(args.get("start_line", 1)),
                    int(args["end_line"]) if args.get("end_line") is not None else None,
                )
            raise DelegateError(f"unknown tool: {name}")
        except (KeyError, ValueError, OSError, UnicodeError, DelegateError) as exc:
            return json.dumps({"error": str(exc)})

    def list_files(self, relative: str) -> str:
        root = self._path(relative)
        paths = [root] if root.is_file() else root.rglob("*")
        files = []
        for path in paths:
            if not path.is_file():
                continue
            rel = path.relative_to(self.repo)
            if any(part in TRANSIENT_PARTS for part in rel.parts):
                continue
            files.append(rel.as_posix())
        return json.dumps({"files": sorted(files)})

    def search_text(self, query: str, relative: str) -> str:
        if not query:
            raise DelegateError("search query must not be empty")
        root = self._path(relative)
        paths = [root] if root.is_file() else root.rglob("*")
        matches: list[dict[str, Any]] = []
        truncated = False
        for path in sorted(paths):
            if not path.is_file():
                continue
            rel = path.relative_to(self.repo)
            if any(part in TRANSIENT_PARTS for part in rel.parts):
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for number, line in enumerate(lines, 1):
                if query in line:
                    if len(matches) >= MAX_SEARCH_MATCHES:
                        truncated = True
                        break
                    matches.append({"path": rel.as_posix(), "line": number, "text": line})
            if truncated:
                break
        return json.dumps({"matches": matches, "truncated": truncated})

    def read_file(self, relative: str, start: int = 1, end: int | None = None) -> str:
        if start < 1 or (end is not None and end < start):
            raise DelegateError("invalid line range")
        path = self._path(relative)
        if not path.is_file():
            raise DelegateError(f"not a file: {relative}")
        lines = path.read_text(encoding="utf-8").splitlines()
        final = min(end if end is not None else len(lines), len(lines))
        return "\n".join(f"{i}: {lines[i - 1]}" for i in range(start, final + 1))


def build_system_prompt(skill_id: str, package: str) -> str:
    return f"""You are a delegated repository agent operating independently from the caller.

Repository instructions and explicit user task requirements outrank the selected skill.
Before substantive reasoning, locate and read any applicable AGENTS.md or equivalent repository instructions using the supplied tools.
You are read-only: never claim to edit files or run shell commands. Use only the supplied
repository inspection tools. Inspect evidence yourself before reaching conclusions.
If required evidence cannot be accessed, say so explicitly.

Selected skill: {skill_id}

The complete readable selected skill package follows:
{package}
"""


def ollama_complete(
    endpoint: str,
    model_cfg: dict[str, Any],
    messages: list[dict[str, Any]],
    *,
    timeout: float,
) -> dict[str, Any]:
    options: dict[str, Any] = {}
    mapping = {
        "context_length": "num_ctx",
        "temperature": "temperature",
        "top_p": "top_p",
        "seed": "seed",
        "max_tokens": "num_predict",
    }
    for source, target in mapping.items():
        if source in model_cfg:
            options[target] = model_cfg[source]
    payload: dict[str, Any] = {
        "model": model_cfg["model"],
        "messages": messages,
        "tools": TOOL_SCHEMAS,
        "stream": False,
        "options": options,
    }
    if "think" in model_cfg:
        payload["think"] = model_cfg["think"]
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise DelegateError(f"Ollama request failed at {endpoint}: {exc}") from exc


def run_delegate(
    *,
    repo: Path,
    skill_id: str,
    task: str,
    model_alias: str | None,
    config_path: Path,
    max_turns: int,
    script_path: Path,
) -> dict[str, Any]:
    repo = repo.resolve()
    if not repo.is_dir():
        raise DelegateError(f"repository path does not exist: {repo}")
    config = load_config(config_path)
    alias = model_alias or config.get("default_model")
    if not alias or alias not in config["models"]:
        raise DelegateError(
            f"unknown model alias {alias!r}; configured aliases: {', '.join(sorted(config['models']))}"
        )
    model_cfg = config["models"][alias]
    if not isinstance(model_cfg, dict) or not model_cfg.get("model"):
        raise DelegateError(f"invalid model config for alias {alias!r}")
    all_skills = discover_skills(skills_root(script_path))
    if skill_id not in all_skills:
        raise DelegateError(
            f"unknown skill {skill_id!r}; installed skills: {', '.join(sorted(all_skills))}"
        )
    package = skill_package(all_skills[skill_id])
    endpoint = os.environ.get("OLLAMA_BASE_URL") or config.get("endpoint")
    if not endpoint:
        raise DelegateError("no Ollama endpoint configured")
    timeout = float(model_cfg.get("timeout_seconds", 900))
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": build_system_prompt(skill_id, package)},
        {"role": "user", "content": task},
    ]
    tools = ReadOnlyTools(repo)
    started = time.monotonic()
    tool_log: list[dict[str, Any]] = []
    final = ""
    for turn in range(1, max_turns + 1):
        event = ollama_complete(endpoint, model_cfg, messages, timeout=timeout)
        message = event.get("message") or {}
        final = message.get("content") or ""
        calls = message.get("tool_calls") or []
        assistant: dict[str, Any] = {"role": "assistant", "content": final}
        if message.get("thinking"):
            assistant["thinking"] = message["thinking"]
        if calls:
            assistant["tool_calls"] = calls
        messages.append(assistant)
        if not calls:
            return {
                "status": "completed",
                "model_alias": alias,
                "model": model_cfg["model"],
                "skill": skill_id,
                "endpoint": endpoint,
                "turns": turn,
                "wall_seconds": time.monotonic() - started,
                "final_message": final,
                "tool_calls": tool_log,
                "usage": {
                    "input_tokens": event.get("prompt_eval_count"),
                    "output_tokens": event.get("eval_count"),
                },
            }
        for call in calls:
            function = call.get("function") or {}
            name = function.get("name", "")
            args = function.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError as exc:
                    args = {"_invalid_json": str(exc)}
            result = tools.execute(name, args)
            tool_log.append({"tool": name, "arguments": args, "result_chars": len(result)})
            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": call.get("id", ""),
            })
    return {
        "status": "max_turns",
        "model_alias": alias,
        "model": model_cfg["model"],
        "skill": skill_id,
        "endpoint": endpoint,
        "turns": max_turns,
        "wall_seconds": time.monotonic() - started,
        "final_message": final,
        "tool_calls": tool_log,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config_path(Path(__file__)),
        help="Path to ollama-models.json (default: adjacent to this script)",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("models", help="List configured model aliases")
    sub.add_parser("skills", help="List skills from the matching installation root")
    run = sub.add_parser("run", help="Run one bounded read-only delegated task")
    run.add_argument("--repo", type=Path, default=Path.cwd())
    run.add_argument("--model")
    run.add_argument("--skill", required=True)
    run.add_argument("--max-turns", type=int, default=12)
    run.add_argument("task")
    args = parser.parse_args(argv)
    try:
        if args.command == "models":
            config = load_config(args.config)
            print(json.dumps({
                "endpoint": os.environ.get("OLLAMA_BASE_URL") or config.get("endpoint"),
                "default_model": config.get("default_model"),
                "models": config["models"],
            }, indent=2, sort_keys=True))
            return 0
        if args.command == "skills":
            print(json.dumps({"skills": sorted(discover_skills(skills_root(Path(__file__))))}, indent=2))
            return 0
        if args.max_turns < 1:
            raise DelegateError("--max-turns must be at least 1")
        result = run_delegate(
            repo=args.repo,
            skill_id=args.skill,
            task=args.task,
            model_alias=args.model,
            config_path=args.config,
            max_turns=args.max_turns,
            script_path=Path(__file__),
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "completed" else 3
    except (DelegateError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
