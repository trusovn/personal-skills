"""Repository-only staging helper for the fixture-driven owning tests.

Encapsulates the disposable `EVAL_WORK_ROOT` lifecycle, environment, and setup
subprocess execution repeated by the contextual and composition owners. Each
invocation owns its `TemporaryDirectory` and its cleanup; a failed setup raises
with the scenario and captured subprocess diagnostics instead of returning
partial evidence. Skill eval setup programs stay self-contained and must never
import this module.
"""

import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class SetupStagingError(RuntimeError):
    """Setup program failed; carries the scenario and subprocess diagnostics."""

    def __init__(self, scenario: str, completed: subprocess.CompletedProcess):
        self.scenario = scenario
        self.completed = completed
        details = completed.stderr or completed.stdout or ""
        super().__init__(
            f"setup fixture {scenario!r} failed with exit {completed.returncode}: {details}"
        )


def stage_setup(case: unittest.TestCase, fixture: Path, scenario: str) -> Path:
    """Run one setup fixture in a fresh disposable `EVAL_WORK_ROOT`.

    The returned `Path` lives in a `TemporaryDirectory` registered for cleanup
    on `case`, so each invocation owns its state regardless of outcome.
    """
    temporary = TemporaryDirectory()
    case.addCleanup(temporary.cleanup)
    work = Path(temporary.name)
    env = dict(os.environ, EVAL_WORK_ROOT=str(work))
    completed = subprocess.run(
        [sys.executable, str(fixture), scenario],
        env=env,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise SetupStagingError(scenario, completed)
    return work
