#!/usr/bin/env python3
"""Create deterministic repositories used by task-brief-designer evals."""

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


def initialize(root: Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "eval@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Eval Fixture"], check=True)


def commit(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture baseline"], check=True)


def queue_runner() -> None:
    root = WORK / "queue-runner"
    initialize(root)
    write(root, "AGENTS.md", "# Fixture rules\n\nPlanning artifacts may be written under `docs/stage-3-tasks/`. Do not edit implementation during task design.")
    write(
        root,
        "docs/stage-3-plan.md",
        """
        # Stage 3 plan

        ## S3-04 — Continue queue execution

        Add `runner run-next`. It selects the next ready task, persists that task
        as running in `.runner/state.json`, and returns its ID. Later invocations
        must select remaining ready tasks rather than stopping after the first.
        Preserve existing empty-queue behavior and never reclaim a running task.
        """,
    )
    write(
        root,
        "src/queue/select.py",
        """
        def select_next(tasks):
            return next((task for task in tasks if task["status"] == "ready"), None)
        """,
    )
    write(
        root,
        "src/cli.py",
        """
        def run_next(state_path):
            # Public `runner run-next` entry point; implementation is pending.
            raise NotImplementedError
        """,
    )
    write(
        root,
        "tests/test_select.py",
        """
        from src.queue.select import select_next

        def test_selects_one_ready_task():
            assert select_next([{"id": "TASK-1", "status": "ready"}])["id"] == "TASK-1"
        """,
    )
    commit(root)


def process_tree() -> None:
    root = WORK / "verification-runner"
    initialize(root)
    write(root, "AGENTS.md", "# Fixture rules\n\nKeep implementation tasks small. Shared verification infrastructure requires its own approved task.")
    write(
        root,
        "docs/verification-plan.md",
        """
        # Verification runner plan

        ## deny-child-process-tree

        On macOS and Linux, a timed-out verification command must be terminated
        together with every descendant process. Evidence must observe that the
        parent timed out and no descendant remains alive. The approved plan does
        not choose a process-group, process-tree inspection, or sandbox mechanism.
        Resolve feasibility before production implementation.
        """,
    )
    write(root, "tests/fixtures/exit_zero.py", "raise SystemExit(0)")
    write(
        root,
        "tests/test_runner.py",
        """
        def test_ordinary_fixture_exists():
            from pathlib import Path
            assert Path("tests/fixtures/exit_zero.py").is_file()
        """,
    )
    commit(root)


def existing_brief() -> None:
    root = WORK / "api"
    initialize(root)
    write(root, "AGENTS.md", "# Fixture rules\n\nPreserve adequate task content. Edit planning artifacts only under `docs/tasks/`.")
    write(
        root,
        "docs/tasks/API-31.md",
        """
        # API-31 — Reject expired sessions

        Status: ready

        ## Outcome

        Reject an expired session without refreshing its token.

        ## Authority and scope

        Authority: approved issue API-31.
        Approved launch guidance: standard agent tier, medium reasoning, and
        immediate fresh acceptance review.
        Allowed changes: `src/auth/session.py`, `tests/auth/test_session.py`.
        Out of scope: token format changes, dependencies, network, and commits.

        ## Acceptance criteria

        - AC-01: an unexpired session remains valid.
        - AC-02: an expired session is rejected and its token is unchanged.

        ## Verification

        Targeted: `python -m unittest tests.auth.test_session`.
        Broader: `python -m unittest discover -s tests`.

        ## Stops and handoff

        Preserve user work and stop for ambiguous expiry semantics or wider
        paths. Next action: guided implementation.
        """,
    )
    commit(root)


def finite_risk_matrix() -> None:
    root = WORK / "evidence-flow"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        "# Fixture rules\n\nDesign artifacts may be written only under `docs/tasks/`. Do not edit implementation or tests during task design.",
    )
    write(
        root,
        "docs/evidence-plan.md",
        """
        # Evidence flow plan

        ## EVD-12 — Reject tampered or contradictory publication state

        Design a guided implementation task for the public command
        `evidence-runner resume --state <path>`.

        Persisted evidence families are exactly: policy, manifest, attempt
        record, structured result, and closure. Resume must validate every
        present family before any filesystem mutation or subprocess start.

        Publications occur in this exact order: execution, verification,
        decision, ledger. The only legal prefixes are: none; execution;
        execution + verification; execution + verification + decision; and
        execution + verification + decision + ledger. A valid prefix reuses
        its existing bytes and publishes only the next missing stage.

        Reject these contradictory orphan states before side effects:
        structured result without an attempt record; closure without a
        decision publication; ledger without a verification publication; and
        a manifest that references a missing attempt record. Reject tampering
        of each named persisted evidence family at the same boundary.

        Implementation evidence must establish fail-first and targeted public
        command coverage. A fresh independent reviewer must use a distinct
        tamper/recovery probe and owns the aggregate suite after corrections;
        correction implementers rerun targeted evidence first and do not rerun
        the aggregate suite while targeted evidence is red.

        Material readiness uncertainty: the repository has no confirmed
        deterministic observer for proving that rejection precedes both file
        writes and subprocess starts. Recommend standalone guided preflight to
        resolve that exact capability before implementation.

        Allowed implementation paths are `src/evidence_flow.py` and
        `tests/test_evidence_flow.py`. Do not add shared harnesses, new
        dependencies, or unrelated generic corruption, fuzz, platform, or
        performance cases.
        """,
    )
    write(
        root,
        "tests/test_evidence_flow.py",
        """
        import unittest

        from evidence_flow import validate_publication_state


        class EvidenceFlowTest(unittest.TestCase):
            def test_complete_happy_path_is_accepted(self):
                state = {
                    "evidence": ["policy", "manifest", "attempt record", "structured result", "closure"],
                    "publications": ["execution", "verification", "decision", "ledger"],
                }

                self.assertTrue(validate_publication_state(state))
        """,
    )
    commit(root)


SCENARIOS = {
    "finite-risk-matrix": finite_risk_matrix,
    "queue-runner": queue_runner,
    "process-tree": process_tree,
    "existing-brief": existing_brief,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
SCENARIOS[sys.argv[1]]()
