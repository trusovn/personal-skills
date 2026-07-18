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


SCENARIOS = {"queue-runner": queue_runner, "process-tree": process_tree}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
SCENARIOS[sys.argv[1]]()
