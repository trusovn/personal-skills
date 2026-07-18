#!/usr/bin/env python3
"""Create staged implementations and review artifacts for acceptance evals."""

from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import textwrap


WORK = Path(os.environ.get("EVAL_WORK_ROOT", "/work"))
RUNS = WORK / "task-runs"


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


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, text=True, capture_output=True).stdout.rstrip("\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def policy() -> Path:
    path = RUNS / "policies/local-review-v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "id": "local-review-v1",
        "runtime_root": str(RUNS),
        "allow": ["cheap local tests", "disposable probes outside repository", "one acceptance report"],
        "deny": ["source/test edits", "network", "dependency installation", "commits", "tracker updates"],
    }, indent=2) + "\n", encoding="utf-8")
    return path


def worker(run_dir: Path, task_id: str, changed: list[str], commands: list[str]) -> None:
    data = {
        "status": "complete",
        "task_id": task_id,
        "summary": f"bounded-task-implementer submitted {task_id} for independent review",
        "files_changed": changed,
        "verification": [{"command": command, "outcome": "passed", "summary": "worker-observed pass"} for command in commands],
        "decisions": [],
        "questions": [],
        "risks": [],
        "next_action": "Run task-acceptance-review.",
    }
    (run_dir / "worker-result.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def queue_defect() -> None:
    root = WORK / "queue-runner"
    initialize(root)
    run_policy = policy()
    write(root, "AGENTS.md", "# Fixture rules\n\nAcceptance is read-only. Write reports and disposable probe state only under `/work/task-runs/`.")
    write(root, "docs/tasks/QR-12.md", "# QR-12\n\nArtifact status: ready_for_preflight\nAC-01: two consecutive public invocations persist state and claim TASK-1 then TASK-2.\nAllowed paths: src/queue/run_next.py; tests/integration/test_run_next.py")
    write(root, "src/__init__.py", "")
    write(root, "src/queue/__init__.py", "")
    write(root, "src/queue/run_next.py", "def run_next(path):\n    raise NotImplementedError")
    write(root, "tests/__init__.py", "")
    write(root, "tests/integration/__init__.py", "")
    write(root, "tests/integration/test_run_next.py", "import unittest\n\nclass Placeholder(unittest.TestCase):\n    def test_placeholder(self):\n        self.assertTrue(True)")
    git(root, "add", ".")
    git(root, "commit", "-qm", "preflight baseline")
    head = git(root, "rev-parse", "HEAD")
    run_dir = RUNS / "QR-12"
    run_dir.mkdir(parents=True, exist_ok=True)
    packet = f"""# Task Preflight Packet: QR-12
Artifact status: ready
Repository root: {root}
Task brief: docs/tasks/QR-12.md
Task brief SHA-256: {file_sha(root / 'docs/tasks/QR-12.md')}
Baseline HEAD: {head}
Baseline exact git status --short: clean
Allowed paths: src/queue/run_next.py; tests/integration/test_run_next.py
Run policy: {run_policy}
Report path: {run_dir / 'acceptance.md'}
AC-01 requires an independent two-invocation public-entry probe in disposable state.
Legacy finding: trace guards that compare against any initially running task.
"""
    (run_dir / "preflight.md").write_text(packet, encoding="utf-8")
    write(
        root,
        "src/queue/run_next.py",
        """
        import argparse
        import json
        from pathlib import Path

        def run_next(state_path):
            path = Path(state_path)
            state = json.loads(path.read_text())
            if any(task["status"] == "running" for task in state["tasks"]):
                return None
            task = next((item for item in state["tasks"] if item["status"] == "ready"), None)
            if task is None:
                return None
            task["status"] = "running"
            path.write_text(json.dumps(state))
            return task["id"]

        if __name__ == "__main__":
            parser = argparse.ArgumentParser()
            parser.add_argument("state")
            args = parser.parse_args()
            claimed = run_next(args.state)
            if claimed:
                print(claimed)
        """,
    )
    write(
        root,
        "tests/integration/test_run_next.py",
        """
        import json
        from pathlib import Path
        from tempfile import TemporaryDirectory
        import unittest
        from src.queue.run_next import run_next

        class RunNextTest(unittest.TestCase):
            def test_first_invocation_and_state(self):
                with TemporaryDirectory() as directory:
                    state = Path(directory) / "state.json"
                    state.write_text(json.dumps({"tasks": [{"id": "TASK-1", "status": "ready"}]}))
                    self.assertEqual(run_next(state), "TASK-1")
                    self.assertEqual(json.loads(state.read_text())["tasks"][0]["status"], "running")
        """,
    )
    worker(run_dir, "QR-12", ["src/queue/run_next.py", "tests/integration/test_run_next.py"], ["python -m unittest tests.integration.test_run_next"])


def exporter_accept() -> None:
    root = WORK / "exporter"
    initialize(root)
    run_policy = policy()
    write(root, "AGENTS.md", "# Fixture rules\n\nAcceptance is read-only. Preserve user notes and use disposable state outside the repository.")
    write(root, "docs/tasks/EXP-08.md", "# EXP-08\n\nArtifact status: ready_for_preflight\nAC-01: `exportctl resume` appends remaining rows after checkpoint.\nAC-02: retry adds no duplicate rows.\nAllowed paths: src/exporter/resume.py; tests/integration/test_resume.py")
    write(root, "notes/local.md", "baseline note")
    write(root, "src/__init__.py", "")
    write(root, "src/exporter/__init__.py", "")
    write(root, "src/exporter/resume.py", "def resume(*args):\n    raise NotImplementedError")
    write(root, "tests/__init__.py", "")
    write(root, "tests/integration/__init__.py", "")
    write(root, "tests/integration/test_resume.py", "import unittest\n\nclass Placeholder(unittest.TestCase):\n    def test_placeholder(self):\n        self.assertTrue(True)")
    git(root, "add", ".")
    git(root, "commit", "-qm", "preflight baseline")
    # Pre-existing MM user work is part of the preflight baseline.
    write(root, "notes/local.md", "staged user note")
    git(root, "add", "notes/local.md")
    write(root, "notes/local.md", "unstaged continuation of user note")
    index_bytes = subprocess.run(["git", "-C", str(root), "show", ":notes/local.md"], check=True, capture_output=True).stdout
    baseline_status = git(root, "status", "--short")
    run_dir = RUNS / "EXP-08"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "preflight.md").write_text(f"""# Task Preflight Packet: EXP-08
Artifact status: ready
Repository root: {root}
Task brief: docs/tasks/EXP-08.md
Task brief SHA-256: {file_sha(root / 'docs/tasks/EXP-08.md')}
Baseline HEAD: {git(root, 'rev-parse', 'HEAD')}
Baseline exact git status --short:\n{baseline_status}
Pre-existing path: notes/local.md
Index SHA-256: {sha(index_bytes)}
Worktree SHA-256: {file_sha(root / 'notes/local.md')}
Ownership: user; task overlap: no
Allowed paths: src/exporter/resume.py; tests/integration/test_resume.py
Run policy: {run_policy}
Report path: {run_dir / 'acceptance.md'}
Targeted: python -m unittest tests.integration.test_resume
Public probe: python -m src.exporter.resume INPUT CHECKPOINT OUTPUT
""", encoding="utf-8")
    write(
        root,
        "src/exporter/resume.py",
        """
        import argparse
        import json
        from pathlib import Path

        def resume(input_path, checkpoint_path, output_path):
            rows = json.loads(Path(input_path).read_text())
            checkpoint = int(Path(checkpoint_path).read_text()) if Path(checkpoint_path).exists() else 0
            existing = Path(output_path).read_text().splitlines() if Path(output_path).exists() else []
            for row in rows[checkpoint:]:
                if row not in existing:
                    existing.append(row)
            Path(output_path).write_text("\\n".join(existing) + ("\\n" if existing else ""))
            Path(checkpoint_path).write_text(str(len(rows)))

        if __name__ == "__main__":
            parser = argparse.ArgumentParser(prog="exportctl resume")
            parser.add_argument("input")
            parser.add_argument("checkpoint")
            parser.add_argument("output")
            args = parser.parse_args()
            resume(args.input, args.checkpoint, args.output)
        """,
    )
    write(
        root,
        "tests/integration/test_resume.py",
        """
        import json
        from pathlib import Path
        from tempfile import TemporaryDirectory
        import unittest
        from src.exporter.resume import resume

        class ResumeTest(unittest.TestCase):
            def test_resume_and_retry_are_idempotent(self):
                with TemporaryDirectory() as directory:
                    root = Path(directory)
                    source, checkpoint, output = root / "in.json", root / "checkpoint", root / "out.csv"
                    source.write_text(json.dumps(["one", "two"]))
                    resume(source, checkpoint, output)
                    resume(source, checkpoint, output)
                    self.assertEqual(output.read_text().splitlines(), ["one", "two"])
        """,
    )
    worker(run_dir, "EXP-08", ["src/exporter/resume.py", "tests/integration/test_resume.py"], ["python -m unittest tests.integration.test_resume", "python -m unittest discover -s tests"])


def scheduler_inconclusive() -> None:
    root = WORK / "scheduler"
    initialize(root)
    run_policy = policy()
    write(root, "AGENTS.md", "# Fixture rules\n\nAcceptance may not invent missing concurrency infrastructure or use live services.")
    write(root, "docs/tasks/SCH-09.md", "# SCH-09\n\nArtifact status: ready_for_preflight\nAC-01: two coordinated workers cannot claim the same job.\nRequired helper: tests/helpers/concurrent_claims.py")
    write(root, "src/scheduler/claim.py", "def claim(job):\n    return job['id']")
    write(root, "tests/helpers/concurrent_claims.py", "def coordinated_claims(claim):\n    return claim(), claim()")
    write(root, "tests/test_claim.py", "import unittest\n\nclass ClaimTest(unittest.TestCase):\n    def test_unit(self):\n        self.assertTrue(True)")
    git(root, "add", ".")
    git(root, "commit", "-qm", "preflight baseline")
    helper_digest = file_sha(root / "tests/helpers/concurrent_claims.py")
    run_dir = RUNS / "SCH-09"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "preflight.md").write_text(f"""# Task Preflight Packet: SCH-09
Artifact status: ready
Repository root: {root}
Task brief: docs/tasks/SCH-09.md
Baseline HEAD: {git(root, 'rev-parse', 'HEAD')}
Baseline status: clean
Required helper: tests/helpers/concurrent_claims.py
Helper SHA-256: {helper_digest}
Allowed paths: src/scheduler/claim.py; tests/test_claim.py
Run policy: {run_policy}
Report path: {run_dir / 'acceptance.md'}
""", encoding="utf-8")
    write(root, "src/scheduler/claim.py", "def claim(job):\n    # worker implementation\n    return job['id']")
    (root / "tests/helpers/concurrent_claims.py").unlink()
    worker(run_dir, "SCH-09", ["src/scheduler/claim.py"], ["python -m unittest tests.test_claim"])


def exporter_restaged_stale() -> None:
    exporter_accept()
    root = WORK / "exporter"
    # Preserve short status and worktree bytes while changing only the index
    # blob recorded as pre-existing user work by preflight.
    worktree_bytes = (root / "notes/local.md").read_bytes()
    write(root, "notes/local.md", "different staged user note after preflight")
    git(root, "add", "notes/local.md")
    (root / "notes/local.md").write_bytes(worktree_bytes)


SCENARIOS = {
    "queue-defect": queue_defect,
    "exporter-accept": exporter_accept,
    "scheduler-inconclusive": scheduler_inconclusive,
    "exporter-restaged-stale": exporter_restaged_stale,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
RUNS.mkdir(parents=True, exist_ok=True)
SCENARIOS[sys.argv[1]]()
