#!/usr/bin/env python3
"""Create executable repositories, packets, and checkpoints for implementer evals."""

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
SCHEMA = WORK / "contracts/worker-result.schema.json"


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


def install_contracts() -> Path:
    SCHEMA.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA.write_text(json.dumps({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["complete", "needs_input", "blocked", "failed"]},
            "task_id": {"type": "string"},
            "summary": {"type": "string"},
            "files_changed": {"type": "array", "items": {"type": "string"}},
            "verification": {"type": "array", "items": {"type": "object", "properties": {"command": {"type": "string"}, "outcome": {"type": "string", "enum": ["passed", "failed", "not_run"]}, "summary": {"type": "string"}}, "required": ["command", "outcome", "summary"], "additionalProperties": False}},
            "decisions": {"type": "array", "items": {"type": "object", "properties": {"decision": {"type": "string"}, "reason": {"type": "string"}, "scope": {"type": "string", "enum": ["task", "plan"]}}, "required": ["decision", "reason", "scope"], "additionalProperties": False}},
            "questions": {"type": "array", "items": {"type": "object", "properties": {"question": {"type": "string"}, "recommendation": {"type": "string"}, "blocking": {"type": "boolean"}}, "required": ["question", "recommendation", "blocking"], "additionalProperties": False}},
            "risks": {"type": "array", "items": {"type": "string"}},
            "next_action": {"type": "string"},
        },
        "required": ["status", "task_id", "summary", "files_changed", "verification", "decisions", "questions", "risks", "next_action"],
        "additionalProperties": False,
    }, indent=2) + "\n", encoding="utf-8")
    policy = RUNS / "policies/local-medium-v1.json"
    policy.parent.mkdir(parents=True, exist_ok=True)
    policy.write_text(json.dumps({
        "id": "local-medium-v1",
        "runtime_root": str(RUNS),
        "allow": ["packet allowed repository writes", "cheap local tests", "runtime artifact writes"],
        "deny": ["network", "dependency installation", "commits", "other repository paths"],
    }, indent=2) + "\n", encoding="utf-8")
    return policy


def queue_task() -> None:
    root = WORK / "queue-runner"
    initialize(root)
    policy = install_contracts()
    write(root, "AGENTS.md", "# Fixture rules\n\nEdit only packet-authorized paths. Preserve pre-existing user work. Runtime artifacts live outside the repository.")
    write(
        root,
        "docs/tasks/QR-12.md",
        """
        # QR-12 — Repeated queue selection

        Artifact status: ready_for_preflight
        Allowed paths: src/queue/run_next.py; tests/integration/test_run_next.py
        AC-01: two consecutive public invocations persist state and claim TASK-1 then TASK-2.
        AC-02: an empty queue returns no claim and does not rewrite state.
        Legacy sweep: inspect guards that stop when any task is already running.
        """,
    )
    write(root, ".runner/tracker.json", '{"complete": ["QR-11"]}')
    write(root, "notes/local.md", "baseline notes")
    write(root, "src/__init__.py", "")
    write(root, "src/queue/__init__.py", "")
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
    write(root, "tests/__init__.py", "")
    write(root, "tests/integration/__init__.py", "")
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
            def test_first_selection(self):
                with TemporaryDirectory() as directory:
                    state = Path(directory) / "state.json"
                    state.write_text(json.dumps({"tasks": [{"id": "TASK-1", "status": "ready"}]}))
                    self.assertEqual(run_next(state), "TASK-1")
        """,
    )
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture baseline")
    # Preserve an unrelated real MM user change outside task scope.
    write(root, "notes/local.md", "staged user note")
    git(root, "add", "notes/local.md")
    write(root, "notes/local.md", "unstaged continuation of user note")
    run_dir = RUNS / "QR-12"
    run_dir.mkdir(parents=True, exist_ok=True)
    index_bytes = subprocess.run(["git", "-C", str(root), "show", ":notes/local.md"], check=True, capture_output=True).stdout
    packet = f"""# Task Preflight Packet: QR-12

Artifact status: ready
Repository root: {root}
Task brief: docs/tasks/QR-12.md
Task brief SHA-256: {file_sha(root / 'docs/tasks/QR-12.md')}
HEAD: {git(root, 'rev-parse', 'HEAD')}
Exact git status --short:
```
{git(root, 'status', '--short')}
```
Dirty path: notes/local.md
Index SHA-256: {sha(index_bytes)}
Worktree SHA-256: {file_sha(root / 'notes/local.md')}
Ownership: pre-existing user; task overlap: no
Instruction SHA-256: {file_sha(root / 'AGENTS.md')}
Dependency SHA-256: {file_sha(root / '.runner/tracker.json')}
Run policy: {policy}
Run policy SHA-256: {file_sha(policy)}
Packet path: {run_dir / 'preflight.md'} (outside repository)
Allowed paths: src/queue/run_next.py; tests/integration/test_run_next.py
Schema: {SCHEMA}
Result path: {run_dir / 'worker-result.json'}
AC-01 oracle: add and first run `python -m unittest tests.integration.test_run_next.RunNextTest.test_two_consecutive_public_invocations`; it must fail because the second claim is absent, then pass with TASK-1/TASK-2 and persisted state.
AC-02 oracle: empty state remains byte-for-byte unchanged.
CMD-01 targeted: python -m unittest tests.integration.test_run_next.RunNextTest.test_two_consecutive_public_invocations
CMD-02 owning: python -m unittest tests.integration.test_run_next
CMD-03 broader: python -m unittest discover -s tests
Working directory for all commands: {root}
Permissions: only allowed paths and runtime result; no network, install, commit, or other writes.
Next route after complete: task-acceptance-review.
"""
    (run_dir / "preflight.md").write_text(packet, encoding="utf-8")


def scheduler_resume() -> None:
    root = WORK / "scheduler"
    initialize(root)
    policy = install_contracts()
    write(root, "AGENTS.md", "# Fixture rules\n\nPreserve same-thread partial changes and obey the two-strike stop.")
    write(root, "docs/tasks/SCH-09.md", "# SCH-09\n\nArtifact status: ready_for_preflight\nAC-01: two coordinated workers never claim the same job.\nAllowed paths: src/scheduler/claim.py; tests/integration/test_claim.py")
    write(root, "src/scheduler/claim.py", "def claim(job):\n    return job['id']")
    write(root, "tests/integration/test_claim.py", "import unittest\n\nclass ClaimTest(unittest.TestCase):\n    def test_exclusive_claim(self):\n        self.fail('both workers claimed JOB-1')")
    write(root, "tests/__init__.py", "")
    write(root, "tests/integration/__init__.py", "")
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture baseline")
    baseline_head = git(root, "rev-parse", "HEAD")
    # Same-thread partial diff after two disproved fixes.
    write(root, "src/scheduler/claim.py", "def claim(job):\n    # conditional update attempt remains incomplete\n    return job['id']")
    write(root, "tests/integration/test_claim.py", "import unittest\n\nclass ClaimTest(unittest.TestCase):\n    def test_exclusive_claim(self):\n        self.fail('trace: both workers claimed JOB-1 after conditional update')")
    run_dir = RUNS / "SCH-09"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "preflight.md").write_text(f"""# Task Preflight Packet: SCH-09
Artifact status: ready
Repository root: {root}
Baseline HEAD: {baseline_head}
Baseline status: clean
Allowed paths: src/scheduler/claim.py; tests/integration/test_claim.py
Targeted command: python -m unittest tests.integration.test_claim.ClaimTest.test_exclusive_claim
Run policy: {policy}
Schema: {SCHEMA}
Result path: {run_dir / 'worker-result.json'}
Resume rule: current allowed-path changes are attributed to this implementation thread and recorded in checkpoint.md.
""", encoding="utf-8")
    (run_dir / "checkpoint.md").write_text(f"""# SCH-09 checkpoint
Current status:\n{git(root, 'status', '--short')}
Attempt 1: transaction guard; disproved by trace showing both workers entered before commit.
Attempt 2: conditional update; disproved by trace showing both workers still claimed JOB-1.
Targeted command remains failed. Preserve the partial diff and apply the two-strike stop.
src/scheduler/claim.py SHA-256: {file_sha(root / 'src/scheduler/claim.py')}
tests/integration/test_claim.py SHA-256: {file_sha(root / 'tests/integration/test_claim.py')}
""", encoding="utf-8")


def queue_restaged_stale() -> None:
    queue_task()
    root = WORK / "queue-runner"
    # Replace only the index blob after preflight. Restore identical worktree
    # bytes so `git status --short` remains `MM` and the worktree digest matches.
    worktree_bytes = (root / "notes/local.md").read_bytes()
    write(root, "notes/local.md", "different staged user note after preflight")
    git(root, "add", "notes/local.md")
    (root / "notes/local.md").write_bytes(worktree_bytes)


def api_guided() -> None:
    root = WORK / "api-guided"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        "# Fixture rules\n\nUse guided implementation. Preserve user work, add behavioral tests, and run targeted verification before the broader suite.",
    )
    write(
        root,
        "docs/tasks/API-31.md",
        """
        # API-31 — Reject expired sessions

        Status: ready

        ```yaml
        agent_tier: standard
        reasoning: medium
        review: milestone
        budget: 20 tool calls / 45 minutes / 60k context
        ```

        Outcome: reject expired sessions without changing their token.
        Allowed changes: src/auth/session.py; tests/auth/test_session.py.
        AC-01: an unexpired session remains valid.
        AC-02: an expired session is rejected and its token remains unchanged.
        Targeted: python -m unittest tests.auth.test_session
        Broader: python -m unittest discover -s tests
        No network, dependency installation, commits, or other repository writes.
        """,
    )
    write(root, "src/__init__.py", "")
    write(root, "src/auth/__init__.py", "")
    write(
        root,
        "src/auth/session.py",
        """
        def is_valid(session, now):
            return bool(session.get("token"))
        """,
    )
    write(root, "tests/__init__.py", "")
    write(root, "tests/auth/__init__.py", "")
    write(
        root,
        "tests/auth/test_session.py",
        """
        import unittest

        from src.auth.session import is_valid


        class SessionTest(unittest.TestCase):
            def test_unexpired_session_is_valid(self):
                session = {"token": "abc", "expires_at": 20}
                self.assertTrue(is_valid(session, now=10))
        """,
    )
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture baseline")


SCENARIOS = {
    "queue-task": queue_task,
    "scheduler-resume": scheduler_resume,
    "queue-restaged-stale": queue_restaged_stale,
    "api-guided": api_guided,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
RUNS.mkdir(parents=True, exist_ok=True)
SCENARIOS[sys.argv[1]]()
