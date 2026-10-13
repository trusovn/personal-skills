"""Stage the route fixture with a separate, answer-free consumer Git baseline."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def route_cases():
    subprocess.run(
        [sys.executable, str(ROOT / "skills/task-implementation-flow/"
         "bounded-task-implementer/evals/files/setup_fixture.py"), "route-cases"],
        check=True, timeout=20,
    )
    work = Path(os.environ["EVAL_WORK_ROOT"])
    source = work / "route-cases"
    consumer = work / "route-consumer"
    # Never copy source Git objects, refs, index, configuration or reflogs.
    shutil.copytree(source, consumer, ignore=shutil.ignore_patterns(".git"))
    (consumer / "change-effects/cases.json").unlink()
    for args in (
        ("init", "-q"),
        ("config", "user.email", "eval@example.invalid"),
        ("config", "user.name", "Eval Fixture"),
        ("add", "."),
        ("commit", "-qm", "consumer fixture baseline without evaluator answers"),
    ):
        subprocess.run(["git", "-C", str(consumer), *args], check=True, timeout=10)


if __name__ == "__main__":
    {"route-cases": route_cases}[sys.argv[1]]()
