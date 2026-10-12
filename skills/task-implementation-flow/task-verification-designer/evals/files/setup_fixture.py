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


def preparation_routes() -> None:
    root = initialize("preparation-routes")
    write(
        root,
        "docs/tasks/PKG-1/brief.md",
        """
        # Task Brief: PKG-1

        Status: ready
        Task kind: executable
        AC-01: update the compact documentation package.
        """,
    )
    write(
        root,
        "docs/tasks/PARENT/brief.md",
        """
        # Task Brief: PARENT

        Status: decomposed
        Task kind: composite
        Children: PKG-1
        """,
    )
    write(
        root,
        "docs/tasks/BLOCKED/brief.md",
        """
        # Design block: BLOCKED

        Status: blocked_design
        Missing decision: retention owner
        """,
    )
    write(root, "docs/tasks/LEGACY.md", "# Legacy task\n\nAC-01: normalize me.")
    commit(root)


def coverage_revision() -> None:
    root = initialize("coverage-revision")
    write(
        root,
        "docs/tasks/REV-1/brief.md",
        """
        # Task Brief: REV-1

        Status: ready
        Task kind: executable
        AC-01: export a report.
        AC-02: preserve the source timestamp.
        """,
    )
    write(
        root,
        "docs/tasks/REV-1/verification.md",
        """
        Source brief: docs/tasks/REV-1/brief.md
        Source brief revision: 1
        Verification revision: 1
        V-01 covers AC-01.
        """,
    )
    write(
        root,
        "docs/tasks/REV-1/preflight.md",
        """
        Status: ready
        Verification revision: 1
        Evidence: V-01 passed.
        """,
    )
    write(
        root,
        "docs/tasks/REV-1/changed-requirement.md",
        "AC-02 now requires an approved retention decision.",
    )
    commit(root)


def coverage_closure() -> None:
    root = initialize("coverage-closure")
    write(
        root,
        "docs/report-policy.md",
        """
        # Report policy

        Every export includes the approved report title and the exact source
        timestamp. No other report field is required by this policy.
        """,
    )
    verification_by_package = {
        "COV-VALID": """
            Source brief: docs/tasks/COV-VALID/brief.md
            Source brief revision: 1
            Verification revision: 1
            V-01 covers AC-01 with title setup, export action, and title oracle.
            V-02 covers AC-02 and ROW-TIMESTAMP with source timestamp setup,
            export action, and exact timestamp oracle.
        """,
        "COV-OMITTED": """
            Source brief: docs/tasks/COV-OMITTED/brief.md
            Source brief revision: 1
            Verification revision: 1
            V-01 covers AC-01; its title evidence is green.
        """,
        "COV-UNSUPPORTED": """
            Source brief: docs/tasks/COV-UNSUPPORTED/brief.md
            Source brief revision: 1
            Verification revision: 1
            V-01 covers AC-01.
            V-99 requires encrypting every export before delivery.
        """,
        "COV-WEAK": """
            Source brief: docs/tasks/COV-WEAK/brief.md
            Source brief revision: 1
            Verification revision: 1
            V-01 covers AC-01 with a title oracle.
            V-02 covers AC-02 by checking only that an export file exists.
        """,
    }
    for package, verification in verification_by_package.items():
        write(
            root,
            f"docs/tasks/{package}/brief.md",
            f"""
            # Task Brief: {package}

            Status: ready
            Task kind: executable
            Authority: docs/report-policy.md
            AC-01: export the approved report title.
            AC-02: preserve the exact source timestamp in the export.
            Finite-risk rows:
            - ROW-TIMESTAMP — source and export timestamps must match exactly.
            """,
        )
        write(root, f"docs/tasks/{package}/verification.md", verification)
    commit(root)


def verification_conflicts() -> None:
    root = initialize("verification-conflicts")
    declarations = {
        "CONFLICT-MISSING": "Preserve missing declaration bytes.",
        "CONFLICT-MALFORMED": "Source brief docs/tasks/CONFLICT-MALFORMED/brief.md\nPreserve malformed declaration bytes.",
        "CONFLICT-DUPLICATE": """
            Source brief: docs/tasks/CONFLICT-DUPLICATE/brief.md
            Source brief: docs/tasks/CONFLICT-DUPLICATE/brief.md
            Preserve duplicate declaration bytes.
        """,
        "CONFLICT-FOREIGN": """
            Source brief: docs/tasks/OTHER/brief.md
            Preserve foreign declaration bytes.
        """,
        "CONFLICT-VALID": """
            Source brief: docs/tasks/CONFLICT-VALID/brief.md
            Preserve valid control bytes.
        """,
    }
    for package, verification in declarations.items():
        write(
            root,
            f"docs/tasks/{package}/brief.md",
            f"""
            # Task Brief: {package}

            Status: ready
            Task kind: executable
            AC-01: preserve the supplied artifact.
            """,
        )
        write(root, f"docs/tasks/{package}/verification.md", verification)
    commit(root)


def workflow_scope() -> None:
    root = initialize("workflow-scope")
    write(
        root,
        "docs/tasks/GUIDE-1/brief.md",
        """
        # Task Brief: GUIDE-1

        Status: ready
        Task kind: executable
        AC-01: update one compact documentation page.
        """,
    )
    write(
        root,
        "requests/unpackaged-direct-edit.md",
        "Correct one heading and verify the rendered Markdown.",
    )
    commit(root)


def integration_leaf() -> None:
    root = initialize("integration-leaf")
    write(
        root,
        "docs/settlement-policy.md",
        """
        # Settlement policy

        Settlement consumes the export handoff exactly once per item at the
        consumer boundary. A missing or incompatible handoff is reported to
        its owner, never invented or silently replaced.
        """,
    )
    write(
        root,
        "docs/producer-outputs/export-handoff.json",
        '{"items": [{"id": "EXP-1", "total": "102.00"}]}',
    )
    write(
        root,
        "docs/tasks/INT-9/brief.md",
        """
        # Task Brief: INT-9 — Compose export handoff into settlement

        Status: ready
        Task kind: executable
        Authority: docs/settlement-policy.md

        Producers: the completed export task's supplied producer outputs live
        at `docs/producer-outputs/export-handoff.json`; the consumer boundary
        is the settlement consume command.

        AC-01: consuming a supplied producer output applies each settled item
        exactly once at the consumer boundary.
        AC-02: a missing or incompatible producer output is reported to its
        owner and never invented or silently replaced.
        """,
    )
    write(
        root,
        "docs/tasks/INT-PARENT/brief.md",
        """
        # Task Brief: INT-PARENT

        Status: decomposed
        Task kind: composite
        Children: INT-9
        """,
    )
    write(
        root,
        "requests/integration-contrasts.md",
        """
        Contrasts for the INT-9 verification request:

        - Sibling requirement: `INT-10` (export retention) is outside this
          leaf's authority; the request must not invent or own it.
        - System-wide: an end-to-end export-to-archive integration strategy
          is not owned by this leaf's verification design.
        - Unavailable: the decisive settlement oracle's expected result is
          not stated by any supplied authority, and the unavailable input or
          capability must be reported to its owner instead of fabricating a
          report or claiming readiness.
        """,
    )
    commit(root)


SCENARIOS = {
    "ambiguous": ambiguous,
    "coverage-closure": coverage_closure,
    "coverage-revision": coverage_revision,
    "integration-leaf": integration_leaf,
    "lifecycle": lifecycle,
    "preparation-routes": preparation_routes,
    "small-explicit": small_explicit,
    "verification-conflicts": verification_conflicts,
    "workflow-scope": workflow_scope,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
SCENARIOS[sys.argv[1]]()
