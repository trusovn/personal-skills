#!/usr/bin/env python3
"""Create deterministic repositories for task-verification-designer evals."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import textwrap


WORK = Path(os.environ.get("EVAL_WORK_ROOT", "/work"))


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def initialize(name: str) -> Path:
    root = WORK / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(
        ["git", "-C", str(root), "config", "user.email", "eval@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(root), "config", "user.name", "Eval Fixture"],
        check=True,
    )
    write(
        root,
        "AGENTS.md",
        """
        # Fixture rules

        Verification design may write only the requested `verification.md`.
        Do not edit briefs, authority, production code, tests, or dependencies.
        """,
    )
    return root


def commit(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", "fixture baseline"],
        check=True,
    )


def lifecycle() -> None:
    root = initialize("lifecycle")
    write(
        root,
        "docs/import-policy.md",
        """
        # Import policy

        A valid bundle is committed atomically through `bundle import`. A retry
        after interruption resumes from the last complete item without
        duplicating committed items. Invalid bundles are rejected before any
        durable file is created or changed.
        """,
    )
    write(
        root,
        "docs/tasks/IMP-21/brief.md",
        """
        # Task Brief: IMP-21 — Resume bundle import

        Status: ready
        Task kind: executable
        Authority: docs/import-policy.md
        Verification-design recommendation: separate — retry and unchanged-state
        semantics need discriminating real-boundary scenarios.

        AC-01: `bundle import valid.bundle` persists each approved item once.
        AC-02: after interruption following the first committed item, the next
        invocation resumes with the next item and does not duplicate the first.
        AC-03: invalid input returns an error and leaves the destination bytes
        unchanged.

        Finite-risk rows:
        - ROW-RESUME — first commit, interruption, and next invocation.
        - ROW-INVALID — malformed header and missing manifest share the same
          pre-write rejection invariant.
        """,
    )
    write(root, "src/importer.py", "# production placeholder")
    write(root, "tests/test_importer.py", "# test placeholder")
    commit(root)


def ambiguous() -> None:
    root = initialize("ambiguous")
    write(
        root,
        "docs/tasks/RET-8/brief.md",
        """
        # Task Brief: RET-8 — Bound backup storage

        Status: ready
        Task kind: executable
        Owner: product owner
        AC-01: keep backup storage bounded.

        The authority does not decide how many backups remain, which backups may
        be deleted, or whether deletion is automatic or owner-confirmed.
        """,
    )
    write(root, "docs/tasks/RET-8/existing-marker.txt", "preserve me")
    commit(root)


def small_explicit() -> None:
    root = initialize("small-explicit")
    write(
        root,
        "docs/tasks/API-5/brief.md",
        """
        # Task Brief: API-5 — Reject blank display names

        Status: ready
        Task kind: executable
        AC-01: submitting a non-blank display name succeeds and returns it.
        AC-02: submitting a blank display name returns the existing validation
        error and does not update the stored name.
        """,
    )
    commit(root)


SCENARIOS = {
    "ambiguous": ambiguous,
    "lifecycle": lifecycle,
    "small-explicit": small_explicit,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
SCENARIOS[sys.argv[1]]()
