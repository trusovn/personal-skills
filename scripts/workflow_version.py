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


def workflow_skills_root(repo_root: Path) -> Path:
    """Resolve skills beside the installed shared scripts when they live in this repo."""
    repo_root = Path(repo_root).resolve()
    script_path = Path(__file__).resolve()
    try:
        script_path.relative_to(repo_root)
    except ValueError:
        return repo_root / "skills"

    installed_root = script_path.parent.parent
    installed_skills = installed_root / "skills"
    return installed_skills if installed_skills.is_dir() else repo_root / "skills"


def discover_workflows(repo_root: Path) -> dict[str, Path]:
    skills_root = workflow_skills_root(repo_root)
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


def _is_explicit_installed_workflow(repo_root: Path, skill_dir: Path) -> bool:
    """Return whether the active workflow comes from a sibling installed skills tree."""
    source_skills = (Path(repo_root).resolve() / "skills").resolve()
    active_skills = workflow_skills_root(repo_root).resolve()
    if active_skills == source_skills:
        return False

    try:
        Path(skill_dir).resolve().relative_to(active_skills)
    except ValueError:
        return False
    return True


def _installed_workflow_files(skill_dir: Path) -> list[Path]:
    """Enumerate explicit installed-package bytes independently of app Git ignore policy."""
    skill_dir = Path(skill_dir).resolve()
    files = [
        path
        for path in skill_dir.rglob("*")
        if path.is_file() and not _is_excluded(path.relative_to(skill_dir))
    ]
    return sorted(files, key=lambda path: path.relative_to(skill_dir).as_posix())


def workflow_files(repo_root: Path, skill_dir: Path) -> list[Path]:
    repo_root = Path(repo_root).resolve()
    skill_dir = Path(skill_dir).resolve()

    if _is_explicit_installed_workflow(repo_root, skill_dir):
        return _installed_workflow_files(skill_dir)

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


# IMPORTANT: FINGERPRINT SEMANTICS ARE A COMPATIBILITY CONTRACT.
# DO NOT CHANGE INPUT SELECTION, PATH NORMALIZATION, ORDERING, HASH FRAMING,
# OR HASH ALGORITHM WITHOUT AN EXPLICIT COMPATIBILITY/VERSIONING DECISION.
def fingerprint_workflow(repo_root: Path, skill_dir: Path) -> str:
    skill_dir = Path(skill_dir).resolve()
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


def repository_branch(repo_root: Path) -> str | None:
    branch = _git(repo_root, "branch", "--show-current").strip()
    return branch or None


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
        "repository_branch": repository_branch(repo_root),
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
