#!/usr/bin/env python3
"""Install the predefined development skill profile into another Git repository."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PROFILE_NAME = "development"
SOURCE_REPO = Path(__file__).resolve().parents[1]

# MAINTENANCE CONTRACT:
# When a selected skill is renamed/moved/added/removed, or when its shared runtime
# dependencies change, update this profile, the profile guide, the focused
# installer tests, and the installation documentation in the same change.
DEVELOPMENT_SKILL_SOURCES: tuple[tuple[str, str], ...] = (
    ("project-direction", "skills/project-direction"),
    ("project-bootstrap", "skills/project-bootstrap"),
    ("ai-flow-foundation", "skills/ai-flow-foundation"),
    ("repo-foundation", "skills/repo-foundation"),
    ("architecture-guardrails", "skills/architecture-guardrails"),
    ("foundation-readiness-review", "skills/foundation-readiness-review"),
    ("project-delivery-plan", "skills/project-delivery-plan"),
    ("project-plan-verification", "skills/project-plan-verification"),
    ("task-brief-designer", "skills/task-implementation-flow/task-brief-designer"),
    ("task-preflight", "skills/task-implementation-flow/task-preflight"),
    ("task-verification-designer", "skills/task-implementation-flow/task-verification-designer"),
    ("bounded-task-implementer", "skills/task-implementation-flow/bounded-task-implementer"),
    ("task-maintainability-review", "skills/task-implementation-flow/task-maintainability-review"),
    ("task-contract-registry-updater", "skills/task-implementation-flow/task-contract-registry-updater"),
    ("task-acceptance-review", "skills/task-implementation-flow/task-acceptance-review"),
    ("senior-code-review", "skills/senior-code-review"),
    ("testing-discipline", "skills/testing-discipline"),
    ("session-handoff", "skills/session-handoff"),
)

PROFILE_SKILLS_README = "skills/README.md"

SHARED_SCRIPT_FILES: tuple[str, ...] = (
    "run_evidence.py",
    "workflow_version.py",
    "runtime_context.py",
    "runtime-context.schema.v1.json",
)

AGENTS_BEGIN = "<!-- personal-skills:development-install:begin -->"
AGENTS_END = "<!-- personal-skills:development-install:end -->"
AGENTS_BLOCK = f"""\
{AGENTS_BEGIN}
## Skill installation resolution

This block is managed by the `personal-skills` development-profile installer.
Rerun the installer to update it; keep repository-specific instructions outside
these markers.

- When work in the current repository uses a named skill and a matching project-local copy exists under `.agents/skills/`, resolve and read that project-local copy before considering user-global skill paths. Do not probe or switch to a user-global copy after a matching project-local skill has been selected for the invocation.
- Resolve shared tooling from the same installation root as the active skill. For a project-local `.agents/skills/` installation, use only the sibling `.agents/scripts/`; do not mix project-local skills with user-global helpers or vice versa.
- If optional shared tooling is missing or unavailable, follow the active skill's documented fallback behavior. Do not silently replace it with tooling from another installation root.
{AGENTS_END}
"""

TRANSIENT_PATTERNS = ("__pycache__", "*.pyc", ".DS_Store", "node_modules")


class InstallError(RuntimeError):
    pass


def _git_root(path: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "not a Git repository"
        raise InstallError(f"target repository is not usable: {message}")
    return Path(result.stdout.strip()).resolve()


def _validate_source(source_repo: Path) -> None:
    missing: list[str] = []

    for _, relative in DEVELOPMENT_SKILL_SOURCES:
        skill_dir = source_repo / relative
        if not skill_dir.is_dir():
            missing.append(relative)
        elif not (skill_dir / "SKILL.md").is_file():
            missing.append(f"{relative}/SKILL.md")

    for name in SHARED_SCRIPT_FILES:
        if not (source_repo / "scripts" / name).is_file():
            missing.append(f"scripts/{name}")

    if not (source_repo / PROFILE_SKILLS_README).is_file():
        missing.append(PROFILE_SKILLS_README)

    if missing:
        joined = ", ".join(sorted(missing))
        raise InstallError(f"source repository is missing development-profile inputs: {joined}")


def _validate_target(target_repo: Path) -> None:
    if not target_repo.is_dir():
        raise InstallError(f"target repository does not exist: {target_repo}")

    actual_root = _git_root(target_repo)
    if actual_root != target_repo.resolve():
        raise InstallError(
            f"target path must be the Git repository root: got {target_repo.resolve()}, "
            f"root is {actual_root}"
        )

    agents_root = target_repo / ".agents"
    for path in (agents_root, agents_root / "skills", agents_root / "scripts"):
        if path.is_symlink():
            raise InstallError(f"refusing to manage symlinked installation path: {path}")
        if path.exists() and not path.is_dir():
            raise InstallError(f"installation path is not a directory: {path}")

    for _, relative in DEVELOPMENT_SKILL_SOURCES:
        destination = target_repo / ".agents" / relative
        if destination.is_symlink():
            raise InstallError(f"refusing to replace symlinked managed skill: {destination}")
        if destination.exists() and not destination.is_dir():
            raise InstallError(f"managed skill destination is not a directory: {destination}")

    for name in SHARED_SCRIPT_FILES:
        destination = target_repo / ".agents" / "scripts" / name
        if destination.is_symlink():
            raise InstallError(f"refusing to replace symlinked shared script: {destination}")
        if destination.exists() and not destination.is_file():
            raise InstallError(f"shared script destination is not a file: {destination}")

    skills_readme = target_repo / ".agents" / "skills" / "README.md"
    if skills_readme.is_symlink():
        raise InstallError(f"refusing to replace symlinked profile guide: {skills_readme}")
    if skills_readme.exists() and not skills_readme.is_file():
        raise InstallError(f"profile guide destination is not a file: {skills_readme}")

    agents_md = target_repo / "AGENTS.md"
    if agents_md.is_symlink():
        raise InstallError(f"refusing to manage symlinked AGENTS.md: {agents_md}")
    if agents_md.exists() and not agents_md.is_file():
        raise InstallError(f"AGENTS.md is not a file: {agents_md}")


def _render_agents(existing: str) -> str:
    begin_count = existing.count(AGENTS_BEGIN)
    end_count = existing.count(AGENTS_END)

    if begin_count != end_count or begin_count > 1:
        raise InstallError("AGENTS.md contains malformed development-install markers")

    if begin_count == 1:
        begin = existing.index(AGENTS_BEGIN)
        end_marker = existing.index(AGENTS_END)
        if end_marker < begin:
            raise InstallError("AGENTS.md contains reversed development-install markers")
        end = end_marker + len(AGENTS_END)
        prefix = existing[:begin].rstrip()
        suffix = existing[end:].strip()
        parts = [part for part in (prefix, AGENTS_BLOCK.rstrip(), suffix) if part]
        return "\n\n".join(parts) + "\n"

    prefix = existing.rstrip()
    if not prefix:
        return AGENTS_BLOCK.rstrip() + "\n"
    return prefix + "\n\n" + AGENTS_BLOCK.rstrip() + "\n"


def _copy_profile_to_stage(source_repo: Path, stage_root: Path) -> None:
    skills_root = stage_root / "skills"
    scripts_root = stage_root / "scripts"
    skills_root.mkdir(parents=True, exist_ok=True)
    scripts_root.mkdir(parents=True, exist_ok=True)

    ignore = shutil.ignore_patterns(*TRANSIENT_PATTERNS)

    for _, relative in DEVELOPMENT_SKILL_SOURCES:
        relative_under_skills = Path(relative).relative_to("skills")
        source = source_repo / relative
        destination = skills_root / relative_under_skills
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination, ignore=ignore)

    for name in SHARED_SCRIPT_FILES:
        shutil.copy2(source_repo / "scripts" / name, scripts_root / name)

    shutil.copy2(source_repo / PROFILE_SKILLS_README, skills_root / "README.md")


def _run_availability(stage_root: Path, target_repo: Path) -> dict[str, object]:
    script = stage_root / "scripts" / "run_evidence.py"
    result = subprocess.run(
        [sys.executable, str(script), "--repo", str(target_repo), "availability"],
        cwd=target_repo,
        capture_output=True,
        text=True,
        check=False,
    )

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    try:
        info = json.loads(stdout) if stdout else {}
    except json.JSONDecodeError as exc:
        raise InstallError(
            f"staged run-evidence availability returned non-JSON output: {stdout or stderr}"
        ) from exc

    if result.returncode != 0 or info.get("available") is not True:
        detail = stdout or stderr or f"exit {result.returncode}"
        raise InstallError(f"staged run-evidence availability failed: {detail}")

    return info


def _replace_managed_profile(stage_root: Path, target_repo: Path) -> None:
    target_skills = target_repo / ".agents" / "skills"
    target_scripts = target_repo / ".agents" / "scripts"
    target_skills.mkdir(parents=True, exist_ok=True)
    target_scripts.mkdir(parents=True, exist_ok=True)

    for _, relative in DEVELOPMENT_SKILL_SOURCES:
        relative_under_skills = Path(relative).relative_to("skills")
        staged = stage_root / "skills" / relative_under_skills
        destination = target_skills / relative_under_skills
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            shutil.rmtree(destination)
        os.replace(staged, destination)

    for name in SHARED_SCRIPT_FILES:
        staged = stage_root / "scripts" / name
        destination = target_scripts / name
        os.replace(staged, destination)

    os.replace(stage_root / "skills" / "README.md", target_skills / "README.md")


def _write_agents(target_repo: Path, content: str) -> None:
    destination = target_repo / "AGENTS.md"
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=target_repo,
        prefix=".AGENTS.md.personal-skills.",
        delete=False,
    ) as handle:
        temp_path = Path(handle.name)
        handle.write(content)

    if destination.exists():
        os.chmod(temp_path, destination.stat().st_mode & 0o777)
    else:
        os.chmod(temp_path, 0o644)

    try:
        os.replace(temp_path, destination)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def install(target_repo: Path) -> dict[str, object]:
    source_repo = SOURCE_REPO
    target_repo = target_repo.expanduser().resolve()

    _validate_source(source_repo)
    _validate_target(target_repo)

    agents_path = target_repo / "AGENTS.md"
    existing_agents = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    rendered_agents = _render_agents(existing_agents)

    agents_root = target_repo / ".agents"
    agents_existed = agents_root.exists()
    agents_root.mkdir(parents=True, exist_ok=True)

    try:
        with tempfile.TemporaryDirectory(
            prefix=".development-install-",
            dir=agents_root,
        ) as tempdir:
            stage_root = Path(tempdir)
            _copy_profile_to_stage(source_repo, stage_root)
            _run_availability(stage_root, target_repo)
            _replace_managed_profile(stage_root, target_repo)
            availability = _run_availability(agents_root, target_repo)
    except Exception:
        if not agents_existed and agents_root.exists() and not any(agents_root.iterdir()):
            agents_root.rmdir()
        raise

    _write_agents(target_repo, rendered_agents)

    return {
        "installed": True,
        "profile": PROFILE_NAME,
        "source_repo": str(source_repo),
        "target_repo": str(target_repo),
        "skills": [name for name, _ in DEVELOPMENT_SKILL_SOURCES],
        "shared_scripts": list(SHARED_SCRIPT_FILES),
        "availability": availability,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install the predefined personal-skills development profile."
    )
    parser.add_argument("target_repo", help="Path to the target Git repository root")
    args = parser.parse_args()

    try:
        result = install(Path(args.target_repo))
    except (InstallError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
