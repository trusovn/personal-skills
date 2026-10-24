#!/usr/bin/env python3
"""Run the repository's local tests and structural gates without installing tools."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys


def test_roots(root: Path) -> list[Path]:
    """Keep independent discovery roots so local fixture imports keep working."""
    roots = set()
    for base in (root / "tests", root / "skills"):
        for path in base.rglob("test_*.py"):
            relative = path.relative_to(base)
            if not {"fixtures", "evals", "__pycache__"}.intersection(relative.parts):
                roots.add(path.parent)
    return sorted(roots)


def verify(root: Path) -> int:
    suites = test_roots(root)
    if not suites:
        print("ERROR: no test suites found", file=sys.stderr)
        return 1
    commands = [
        [sys.executable, "-m", "unittest", "discover", "-s",
         str(path.relative_to(root)), "-p", "test_*.py", "-v"]
        for path in suites
    ]
    commands.append([sys.executable, "tools/check_contracts.py", "--root", "."])
    if (root / ".agents" / "skills").is_dir():
        commands.append([
            sys.executable, "scripts/install_development_skills.py", "--check", ".",
        ])
    else:
        print("SKIP: development-profile drift check (no .agents/skills installation)", flush=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    failed = []
    for command in commands:
        print(f"CHECK: {shlex.join(command)}", flush=True)
        result = subprocess.run(command, cwd=root, env=env, check=False)
        if result.returncode:
            failed.append(shlex.join(command))
    for command in failed:
        print(f"FAILED: {command}", file=sys.stderr)
    print(f"Verification: {len(commands)} checks, {len(failed)} failed", flush=True)
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    return verify(args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
