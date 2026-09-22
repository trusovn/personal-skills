#!/usr/bin/env python3
"""Deterministic workflow fingerprinting for skills in this repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


EXCLUDED_DIRS = {"__pycache__", "node_modules"}
EXCLUDED_ROOT_DIRS = {"evals", "tests"}
EXCLUDED_FILES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc"}


class WorkflowVersionError(RuntimeError):
    pass


def _git(repo_root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise WorkflowVersionError(message) from exc
    return result.stdout


def repository_root_from_script() -> Path:
    script_dir = Path(__file__).resolve().parent
    root = _git(script_dir, "rev-parse", "--show-toplevel").strip()
    return Path(root)


def _skill_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise WorkflowVersionError(f"Missing YAML frontmatter: {skill_md}")

    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            value = line.split(":", 1)[1].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            if value:
                return value

    raise WorkflowVersionError(f"Missing skill name in frontmatter: {skill_md}")


def discover_workflows(repo_root: Path) -> dict[str, Path]:
    skills_root = repo_root / "skills"
    workflows: dict[str, Path] = {}

    for skill_md in sorted(skills_root.rglob("SKILL.md")):
        workflow_id = _skill_name(skill_md)
        if workflow_id in workflows:
            raise WorkflowVersionError(
                f"Duplicate workflow id '{workflow_id}': "
                f"{workflows[workflow_id]} and {skill_md.parent}"
            )
        workflows[workflow_id] = skill_md.parent

    return workflows


def _is_excluded(relative_path: Path) -> bool:
    if relative_path.parts and relative_path.parts[0] in EXCLUDED_ROOT_DIRS:
        return True
    if any(part in EXCLUDED_DIRS for part in relative_path.parts):
        return True
    if relative_path.name in EXCLUDED_FILES:
        return True
    return relative_path.suffix in EXCLUDED_SUFFIXES


def workflow_files(repo_root: Path, skill_dir: Path) -> list[Path]:
    skill_rel = skill_dir.relative_to(repo_root).as_posix()
    output = _git(
        repo_root,
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        skill_rel,
    )

    files: list[Path] = []
    for repo_relative in output.split("\0"):
        if not repo_relative:
            continue
        path = repo_root / repo_relative
        if not path.is_file():
            continue
        skill_relative = path.relative_to(skill_dir)
        if not _is_excluded(skill_relative):
            files.append(path)

    return sorted(files, key=lambda path: path.relative_to(skill_dir).as_posix())


def fingerprint_workflow(repo_root: Path, skill_dir: Path) -> str:
    hasher = hashlib.sha256()

    for path in workflow_files(repo_root, skill_dir):
        relative_bytes = path.relative_to(skill_dir).as_posix().encode("utf-8")
        content = path.read_bytes()

        hasher.update(len(relative_bytes).to_bytes(8, "big"))
        hasher.update(relative_bytes)
        hasher.update(len(content).to_bytes(8, "big"))
        hasher.update(content)

    return f"sha256:{hasher.hexdigest()}"


def workflow_dirty(repo_root: Path, skill_dir: Path) -> bool:
    skill_rel = skill_dir.relative_to(repo_root).as_posix()
    output = _git(
        repo_root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--no-renames",
        "--",
        skill_rel,
    )

    for entry in output.split("\0"):
        if not entry:
            continue
        repo_relative = entry[3:]
        path = repo_root / repo_relative
        try:
            skill_relative = path.relative_to(skill_dir)
        except ValueError:
            continue
        if not _is_excluded(skill_relative):
            return True

    return False


def get_workflow_version(repo_root: Path, workflow_id: str) -> dict[str, object]:
    repo_root = Path(repo_root).resolve()
    workflows = discover_workflows(repo_root)

    try:
        skill_dir = workflows[workflow_id]
    except KeyError as exc:
        available = ", ".join(sorted(workflows))
        raise WorkflowVersionError(
            f"Unknown workflow '{workflow_id}'. Available workflows: {available}"
        ) from exc

    return {
        "workflow": workflow_id,
        "fingerprint": fingerprint_workflow(repo_root, skill_dir),
        "repository_commit": _git(repo_root, "rev-parse", "HEAD").strip(),
        "repository_dirty": bool(
            _git(repo_root, "status", "--porcelain=v1", "--untracked-files=all").strip()
        ),
        "workflow_dirty": workflow_dirty(repo_root, skill_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print deterministic workflow version information as JSON."
    )
    parser.add_argument("workflow", help="Skill/workflow id from SKILL.md frontmatter")
    args = parser.parse_args()

    try:
        info = get_workflow_version(repository_root_from_script(), args.workflow)
    except WorkflowVersionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(info, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
