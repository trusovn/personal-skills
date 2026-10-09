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
    write(root, "AGENTS.md", "# Fixture rules\n\nEdit only packet-authorized paths. Preserve pre-existing user work. Durable preflight lives in the task package; machine results remain runtime artifacts.")
    write(
        root,
        "docs/tasks/QR-12/brief.md",
        """
        # QR-12 — Repeated queue selection

        Status: ready
        Task kind: executable
        Outcome: claim consecutive ready tasks through persisted public invocations.
        Allowed paths: src/queue/run_next.py; tests/integration/test_run_next.py
        AC-01: two consecutive public invocations persist state and claim TASK-1 then TASK-2.
        AC-02: an empty queue returns no claim and does not rewrite state.
        Legacy sweep: inspect guards that stop when any task is already running.
        """,
    )
    write(
        root,
        "docs/tasks/QR-12/verification.md",
        """
        # Verification Design: QR-12 — Repeated queue selection

        Source brief: docs/tasks/QR-12/brief.md
        Status: ready
        Verification revision: 1

        ### V-01 — Consecutive public invocations claim different tasks
        Covers: AC-01
        Oracle / boundary: invoke the public operation twice and observe TASK-1,
        TASK-2, and both persisted state transitions.

        ### V-02 — Empty queue is byte-for-byte unchanged
        Covers: AC-02
        Oracle / boundary: compare state bytes before and after the public call.
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
    packet_path = root / "docs/tasks/QR-12/preflight.md"
    pre_packet_status = git(root, "status", "--short")
    packet = f"""# Task Preflight Packet: QR-12

Artifact status: ready
Repository root: {root}
Task brief: docs/tasks/QR-12/brief.md
Task brief SHA-256: {file_sha(root / 'docs/tasks/QR-12/brief.md')}
Verification design: docs/tasks/QR-12/verification.md
Verification design SHA-256: {file_sha(root / 'docs/tasks/QR-12/verification.md')}
Verification revision: 1
HEAD: {git(root, 'rev-parse', 'HEAD')}
Pre-write git status --short:
```
{pre_packet_status}
```
Post-write git status --short:
```
__POST_PACKET_STATUS__
```
Packet artifact delta: ?? docs/tasks/QR-12/preflight.md
Dirty path: notes/local.md
Index SHA-256: {sha(index_bytes)}
Worktree SHA-256: {file_sha(root / 'notes/local.md')}
Ownership: pre-existing user; task overlap: no
Instruction SHA-256: {file_sha(root / 'AGENTS.md')}
Dependency SHA-256: {file_sha(root / '.runner/tracker.json')}
Run policy: {policy}
Run policy SHA-256: {file_sha(policy)}
Packet path: docs/tasks/QR-12/preflight.md
Allowed paths: src/queue/run_next.py; tests/integration/test_run_next.py
Schema: {SCHEMA}
Result path: {run_dir / 'worker-result.json'}
V-01 / AC-01 oracle: add and first run `python -m unittest tests.integration.test_run_next.RunNextTest.test_two_consecutive_public_invocations`; it must fail because the second claim is absent, then pass with TASK-1/TASK-2 and persisted state.
V-02 / AC-02 oracle: empty state remains byte-for-byte unchanged.
CMD-01 targeted: python -m unittest tests.integration.test_run_next.RunNextTest.test_two_consecutive_public_invocations
CMD-02 owning: python -m unittest tests.integration.test_run_next
CMD-03 broader: python -m unittest discover -s tests
Working directory for all commands: {root}
Permissions: only allowed paths and runtime result; no network, install, commit, or other writes.
Next route after complete: task-acceptance-review.
"""
    packet_path.write_text(packet, encoding="utf-8")
    post_packet_status = git(root, "status", "--short")
    packet_path.write_text(
        packet.replace("__POST_PACKET_STATUS__", post_packet_status),
        encoding="utf-8",
    )


def scheduler_resume() -> None:
    root = WORK / "scheduler"
    initialize(root)
    policy = install_contracts()
    write(root, "AGENTS.md", "# Fixture rules\n\nPreserve same-thread partial changes and obey the two-strike stop.")
    write(root, "docs/tasks/SCH-09/brief.md", "# SCH-09\n\nArtifact status: ready_for_preflight\nAC-01: two coordinated workers never claim the same job.\nAllowed paths: src/scheduler/claim.py; tests/integration/test_claim.py")
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
    packet_path = root / "docs/tasks/SCH-09/preflight.md"
    packet_path.write_text(f"""# Task Preflight Packet: SCH-09
Artifact status: ready
Repository root: {root}
Baseline HEAD: {baseline_head}
Baseline status: clean
Post-packet status: ?? docs/tasks/SCH-09/preflight.md
Packet path: docs/tasks/SCH-09/preflight.md
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
        "docs/tasks/API-31/brief.md",
        """
        # API-31 — Reject expired sessions

        Status: ready
        Task kind: executable

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
    write(
        root,
        "docs/tasks/API-31/verification.md",
        """
        # Verification Design: API-31 — Reject expired sessions

        Source brief: docs/tasks/API-31/brief.md
        Status: ready

        Verification revision: 1

        ### V-01 — Unexpired session remains valid
        Covers: AC-01
        Oracle / boundary: assert is_valid for an unexpired session.

        ### V-02 — Expired session rejected and token unchanged
        Covers: AC-02
        Oracle / boundary: assert not is_valid and token bytes unchanged.
        """,
    )
    write(
        root,
        "docs/tasks/API-31/preflight.md",
        """
        # Preflight: API-31

        Status: ready
        Profile: guided
        Source brief: docs/tasks/API-31/brief.md
        Verification design: docs/tasks/API-31/verification.md
        Verification revision: 1
        Allowed changes: src/auth/session.py; tests/auth/test_session.py
        Dependency: Python standard library only
        Ownership: clean committed baseline; no overlapping user work
        Permission: local writes and local tests allowed; network, installs and commits denied
        Capability: Python unittest observes session validity and unchanged token locally
        Authority: docs/tasks/API-31/brief.md; outcome and scope unchanged
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


def api_immediate() -> None:
    root = WORK / "api-immediate"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        "# Fixture rules\n\nUse guided implementation. Preserve user work, add behavioral tests, and run the exact targeted command before the owning suite.",
    )
    write(
        root,
        "docs/tasks/API-32/brief.md",
        """
        # API-32 — Reject expired sessions

        Status: ready
        Task kind: executable

        ```yaml
        agent_tier: standard
        reasoning: medium
        review: immediate
        budget: 20 tool calls / 45 minutes / 60k context
        ```

        Outcome: reject expired sessions without changing their token.
        Allowed changes: src/auth/session.py; tests/auth/test_session.py.
        AC-01: an unexpired session remains valid.
        AC-02: an expired session is rejected and its token remains unchanged.
        Targeted: python -m unittest tests.auth.test_session.SessionTest.test_expired_session_is_invalid
        Owning: python -m unittest tests.auth.test_session
        No network, dependency installation, commits, machine result schema, or other repository writes.
        After implementation checks, hand the current bytes to a fresh acceptance reviewer.
        """,
    )
    write(
        root,
        "docs/tasks/API-32/verification.md",
        """
        # Verification Design: API-32 — Reject expired sessions

        Source brief: docs/tasks/API-32/brief.md
        Status: ready

        Verification revision: 1

        ### V-01 — Unexpired session remains valid
        Covers: AC-01
        Oracle / boundary: assert is_valid for an unexpired session.

        ### V-02 — Expired session rejected and token unchanged
        Covers: AC-02
        Oracle / boundary: assert not is_valid and token bytes unchanged.
        """,
    )
    write(
        root,
        "docs/tasks/API-32/preflight.md",
        """
        # Preflight: API-32

        Status: ready
        Profile: guided
        Source brief: docs/tasks/API-32/brief.md
        Verification design: docs/tasks/API-32/verification.md
        Verification revision: 1
        Allowed changes: src/auth/session.py; tests/auth/test_session.py
        Dependency: Python standard library only
        Ownership: clean committed baseline; no overlapping user work
        Permission: local writes and local tests allowed; network, installs and commits denied
        Capability: Python unittest observes session validity and unchanged token locally
        Authority: docs/tasks/API-32/brief.md; outcome and scope unchanged
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

            def test_expired_session_is_invalid(self):
                session = {"token": "abc", "expires_at": 10}
                self.assertFalse(is_valid(session, now=10))
                self.assertEqual(session["token"], "abc")
        """,
    )
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture baseline")


def record_correction() -> None:
    root = WORK / "result-record"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        "# Fixture rules\n\nEdit only task-authorized paths. Preserve reviewer regressions and correction handoff state. A fresh reviewer owns final acceptance.",
    )
    original = {
        "task_id": "REC-44",
        "summary": "validated result",
        "files_changed": ["src/result_integrity.py"],
    }
    body = json.dumps(original, sort_keys=True, separators=(",", ":")).encode()
    original["content_digest"] = sha(body)
    exact_bytes = (
        json.dumps(original, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    write(
        root,
        "docs/tasks/REC-44/brief.md",
        """
        # REC-44 — Bind the complete result record

        Status: ready
        Task kind: executable

        ```yaml
        agent_tier: strong
        reasoning: high
        review: immediate
        budget: 18 tool calls / 40 minutes / 50k context
        ```

        This is a correction after `CHANGES_REQUESTED`.
        Outcome: accept a result only when all exact serialized bytes match the independently anchored digest in `authority/result.sha256`.
        Invariant: every result byte is bound; equality of one demonstrated field or internal consistency is insufficient.
        AC-01: original anchored bytes are accepted and any changed serialized bytes are rejected, including coherent field mutations and equivalent byte rewrites.
        AC-02: replay-boundary review remains with the assigned fresh reviewer; implementation must carry its unchecked status without claiming acceptance.
        Allowed changes: src/result_integrity.py; tests/test_record_integrity.py.
        Reviewer regression: python -m unittest tests.test_record_integrity.RecordIntegrityTest.test_coherent_mutation_is_rejected
        Owning suite: python -m unittest tests.test_record_integrity
        Aggregate gate: python -m unittest discover -s tests
        Gate ownership: skip the aggregate during correction; the assigned fresh reviewer owns any final aggregate decision.
        Required sibling evidence: add at least one other field mutation or semantically equivalent byte rewrite using the same exact-byte oracle.
        No network, dependency installation, commits, or other repository writes.
        """,
    )
    write(root, "docs/tasks/REC-44/verification.md", """
        # Verification Design: REC-44

        Source brief: docs/tasks/REC-44/brief.md
        Status: ready
        Verification revision: 1

        ### V-01 — Exact bytes bind the complete record
        Covers: AC-01
        Reviewer row: ROW-EXACT-BYTES
        Setup: authority/result.json and its independently anchored authority/result.sha256.
        Command: python -m unittest tests.test_record_integrity
        Oracle / boundary: original bytes are accepted; coherent summary mutation and task-owned sibling mutations or equivalent rewrites are rejected.

        ### V-02 — Replay-boundary coverage remains explicit
        Covers: AC-02
        Reviewer row: ROW-REPLAY-BOUNDARY
        Setup: reviews/acceptance-01.md retains the unchecked row.
        Oracle / boundary: handoff preserves the unchecked row and names fresh task-acceptance-review as next owner; no implementation acceptance claim.
        """)
    write(root, "docs/tasks/REC-44/preflight.md", """
        # Preflight: REC-44

        Status: ready
        Profile: guided
        Source brief: docs/tasks/REC-44/brief.md
        Verification design: docs/tasks/REC-44/verification.md
        Verification revision: 1
        Allowed changes: src/result_integrity.py; tests/test_record_integrity.py
        Dependency: Python standard library only
        Ownership: reviewer-owned regression appended to tests/test_record_integrity.py is authorized correction input; preserve it; no other overlap
        Permission: local writes and local tests allowed; network, installs and commits denied
        Capability: Python unittest and hashlib observe exact byte binding against authority/result.sha256
        Authority: docs/tasks/REC-44/brief.md; unchanged correction outcome and scope; CHANGES_REQUESTED in reviews/acceptance-01.md
        Expected effects: appended reviewer regression and authorized correction edits do not change guided applicability
        Commands: reviewer reproducer first, then owning suite from brief; aggregate remains fresh-review-owned
        """)
    write(root, "authority/result.json", exact_bytes.decode())
    write(root, "authority/result.sha256", sha(exact_bytes))
    write(root, "src/__init__.py", "")
    write(
        root,
        "src/result_integrity.py",
        """
        import json


        def is_anchored_result(result_bytes, anchor_digest):
            result = json.loads(result_bytes)
            return result.get("task_id") == "REC-44"
        """,
    )
    write(root, "tests/__init__.py", "")
    write(
        root,
        "tests/test_record_integrity.py",
        """
        import hashlib
        import json
        from pathlib import Path
        import unittest

        from src.result_integrity import is_anchored_result


        ROOT = Path(__file__).parents[1]
        ORIGINAL_BYTES = (ROOT / "authority/result.json").read_bytes()
        ANCHOR_DIGEST = (ROOT / "authority/result.sha256").read_text().strip()


        def serialize_coherently(result):
            body = {
                key: value
                for key, value in result.items()
                if key != "content_digest"
            }
            result["content_digest"] = hashlib.sha256(
                json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                ).encode()
            ).hexdigest()
            return (
                json.dumps(result, sort_keys=True, separators=(",", ":"))
                + "\\n"
            ).encode()


        class RecordIntegrityTest(unittest.TestCase):
            def test_original_record_is_accepted(self):
                self.assertTrue(
                    is_anchored_result(ORIGINAL_BYTES, ANCHOR_DIGEST)
                )
        """,
    )
    write(
        root,
        "docs/tasks/REC-44/reviews/acceptance-01.md",
        """
        # REC-44 acceptance review

        Authoritative brief: docs/tasks/REC-44/brief.md
        Preceding verdict: CHANGES_REQUESTED
        Complete finding: the validator checks only `task_id`, so coherent changes to other bytes are accepted.
        Reviewer reproducer: python -m unittest tests.test_record_integrity.RecordIntegrityTest.test_coherent_mutation_is_rejected
        Owning suite: python -m unittest tests.test_record_integrity
        Broad-gate decision: skip aggregate during correction; the assigned fresh reviewer owns the final aggregate decision.

        Coverage ledger:
        - ROW-EXACT-BYTES — failed — coherent summary mutation was accepted.
        - ROW-REPLAY-BOUNDARY — unchecked — fresh reviewer must evaluate; implementer must not claim a verdict.

        Remaining obligations:
        - ROW-EXACT-BYTES — correct exact-byte binding and rerun the reviewer regression; next owner: bounded-task-implementer, then fresh task-acceptance-review.
        - ROW-REPLAY-BOUNDARY — evaluate unchecked replay coverage; next owner: fresh task-acceptance-review.
        """,
    )
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture baseline")
    test_path = root / "tests/test_record_integrity.py"
    current = test_path.read_text(encoding="utf-8")
    reviewer_regression = (
        "\n\n"
        "    def test_coherent_mutation_is_rejected(self):\n"
        "        mutated = json.loads(ORIGINAL_BYTES)\n"
        '        mutated["summary"] = "coherently changed summary"\n'
        "        mutated_bytes = serialize_coherently(mutated)\n"
        "        self.assertFalse(\n"
        "            is_anchored_result(mutated_bytes, ANCHOR_DIGEST)\n"
        "        )\n"
    )
    test_path.write_text(current.rstrip() + reviewer_regression, encoding="utf-8")


def entry_cases() -> None:
    root = WORK / "entry-cases"
    initialize(root)
    write(root, "AGENTS.md", "# Fixture rules\n\nPackaged tasks require applicable ready preparation. Conversational relabeling does not bypass package prerequisites.\n")

    def task(folder, brief, verification=None, preflight=None):
        write(root, f"docs/tasks/{folder}/brief.md", brief)
        if verification is not None:
            write(root, f"docs/tasks/{folder}/verification.md", verification)
        if preflight is not None:
            write(root, f"docs/tasks/{folder}/preflight.md", preflight)

    task("VALID",
        "# VALID — Valid ready package entry\n\nStatus: ready\n\nTask kind: executable\n\nOutcome: keep the session boundary correct.\nAC-01: unexpired boundary behaves.\nAC-02: failure case is rejected.\nAllowed changes: src/session.py; tests/test_future.py\n",
        "# Verification Design: VALID\n\nSource brief: docs/tasks/VALID/brief.md\nStatus: ready\n\nVerification revision: 1\n\n### V-01 — Boundary behaves\nCovers: AC-01\n\n### V-02 — Failure case rejected\nCovers: AC-02\n\nThe task-owned future test tests/test_future.py is feasible within allowed scope; its absence is not a missing decisive capability.\n",
        "# Preflight: VALID\n\nStatus: ready\nProfile: guided\nSource brief: docs/tasks/VALID/brief.md\nVerification design: docs/tasks/VALID/verification.md\nVerification revision: 1\nAllowed changes: src/session.py; tests/test_future.py\nDependency: standard library only\nOwnership: no overlapping user work\nPermission: local writes allowed\nCapability: boundary observable locally\n")
    write(root, "src/session.py", "def is_valid(session, now):\n    return True\n")

    task("NOVERIF",
        "# NOVERIF — Missing verification\n\nStatus: ready\n\nTask kind: executable\n",
        None,
        "# Preflight: NOVERIF\n\nStatus: ready\nProfile: guided\nVerification revision: 1\n")
    task("NOPREP",
        "# NOPREP — Missing readiness\n\nStatus: ready\n\nTask kind: executable\n",
        "# Verification Design: NOPREP\n\nSource brief: docs/tasks/NOPREP/brief.md\nStatus: ready\n\nVerification revision: 1\n",
        None)
    task("BLOCKED",
        "# BLOCKED — Blocked readiness\n\nStatus: ready\n\nTask kind: executable\n",
        "# Verification Design: BLOCKED\n\nSource brief: docs/tasks/BLOCKED/brief.md\nStatus: ready\n\nVerification revision: 1\n",
        "# Preflight: BLOCKED\n\nStatus: blocked\nProfile: guided\nVerification revision: 1\n")
    task("STALE",
        "# STALE — Stale readiness\n\nStatus: ready\n\nTask kind: executable\n\nBrief revision: 2\n",
        "# Verification Design: STALE\n\nSource brief: docs/tasks/STALE/brief.md\nStatus: ready\n\nVerification revision: 1\n",
        "# Preflight: STALE\n\nStatus: ready\nProfile: guided\nSource brief: docs/tasks/STALE/brief.md\nSource brief revision: 1\nVerification revision: 1\n")
    task("FOREIGN",
        "# FOREIGN — Foreign verification\n\nStatus: ready\n\nTask kind: executable\n",
        "# Verification Design: FOREIGN\n\nSource brief: docs/tasks/OTHER/brief.md\nStatus: ready\n\nVerification revision: 1\n",
        "# Preflight: FOREIGN\n\nStatus: ready\nProfile: guided\nSource brief: docs/tasks/FOREIGN/brief.md\nVerification design: docs/tasks/FOREIGN/verification.md\nVerification revision: 1\n")
    task("REVMISMATCH",
        "# REVMISMATCH — Revision mismatch\n\nStatus: ready\n\nTask kind: executable\n",
        "# Verification Design: REVMISMATCH\n\nSource brief: docs/tasks/REVMISMATCH/brief.md\nStatus: ready\n\nVerification revision: 2\n\n### V-01 — Covers AC-01\n\n### V-02 — Covers AC-01\n",
        "# Preflight: REVMISMATCH\n\nStatus: ready\nProfile: guided\nSource brief: docs/tasks/REVMISMATCH/brief.md\nVerification revision: 1\n")
    task("WRONGSCOPE",
        "# W-31 — Ready brief in package WRONGSCOPE\n\nStatus: ready\n\nTask kind: executable\n",
        "# Verification Design: WRONGSCOPE\n\nSource brief: docs/tasks/WRONGSCOPE/brief.md\nStatus: ready\n\nVerification revision: 1\n",
        "# Preflight: WRONGSCOPE\n\nStatus: ready\nProfile: guided\nTask brief: docs/tasks/W-32/brief.md\nVerification revision: 1\n")
    task("COMPOSITE",
        "# COMPOSITE — Decomposed parent\n\nStatus: decomposed\n\nTask kind: composite\n\nChildren: T-C1; T-C2\n",
        None, None)
    write(root, "docs/tasks/index.json",
          '{\n  "version": 1,\n  "tasks": {\n    "COMPOSITE": {"kind": "composite", "brief": "docs/tasks/COMPOSITE/brief.md", "parent": null, "children": ["T-C1", "T-C2"], "depends_on": []},\n    "T-C1": {"kind": "executable", "brief": "docs/tasks/T-C1/brief.md", "parent": "COMPOSITE", "children": [], "depends_on": []},\n    "T-C2": {"kind": "executable", "brief": "docs/tasks/T-C2/brief.md", "parent": "COMPOSITE", "children": [], "depends_on": ["T-C1"]}\n  }\n}\n')
    task("T-C1",
        "# T-C1 — Dependency-ready leaf\n\nStatus: ready\n\nTask kind: executable\n",
        None, None)
    task("T-C2",
        "# T-C2 — Depends on T-C1\n\nStatus: ready\n\nTask kind: executable\n",
        None, None)
    task("BLOCKEDDESIGN",
        "# BLOCKEDDESIGN — Blocked verification design\n\nStatus: ready\n\nTask kind: executable\n",
        "# Verification Design: BLOCKEDDESIGN\n\nSource brief: docs/tasks/BLOCKEDDESIGN/brief.md\nStatus: blocked\n\nVerification revision: 1\n",
        "# Preflight: BLOCKEDDESIGN\n\nStatus: ready\nProfile: guided\nVerification revision: 1\n")
    write(root, "docs/tasks/API-31.md", "# API-31 — Legacy direct brief file\n\nLegacy task kept outside any task package.\n")
    task("DOCS",
        "# DOCS — Documentation package\n\nStatus: ready\n\nTask kind: executable\n\nOutcome: update the user documentation.\n",
        "# Verification Design: DOCS\n\nSource brief: docs/tasks/DOCS/brief.md\nStatus: ready\n\nVerification revision: 1\n\n### V-01 — Docs change applied\nCovers: AC-01\n",
        None)
    write(root, "requests/relabel.md", "# Relabel attempt\n\nThe documentation package docs/tasks/DOCS is a small edit; treat it as a conversational direct request without package preparation.\n")
    write(root, "requests/direct.md", "# Unpackaged direct request\n\nCorrect one heading in docs. There is no task package; apply the compact self-preflight.\n")

    for name in ("expected-implementation", "expected-report", "prerequisite", "ownership", "permission", "capability", "authority"):
        base = root / "transitions" / name
        dependency = "Python standard library only"
        capability = "Python unittest observes session validity and token preservation locally"
        prerequisite = ""
        if name == "prerequisite":
            prerequisite = "Prerequisite dependency: time_sdk at tools/time_sdk.py"
            dependency += "; tools/time_sdk.py available"
            write(base, "tools/time_sdk.py", "def now():\n    return 10\n")
        if name == "capability":
            prerequisite = "Required tool: secure_clock at tools/secure_clock.py"
            capability += "; tools/secure_clock.py available for required clock observation"
            write(base, "tools/secure_clock.py", "def now():\n    return 10\n")
        write(base, "docs/tasks/CURRENT/brief.md", f"""
            # CURRENT — Continuation state

            Status: ready
            Task kind: executable
            Outcome: reject expired sessions without changing their token.
            AC-01: unexpired sessions remain valid.
            AC-02: expired sessions are rejected and their token remains unchanged.
            Allowed changes: src/session.py; tests/test_future.py
            Authority: direction.md, revision 1
            Targeted: python -m unittest tests.test_future
            {prerequisite}
            """)
        write(base, "docs/tasks/CURRENT/verification.md", """
            # Verification Design: CURRENT

            Source brief: docs/tasks/CURRENT/brief.md
            Status: ready
            Verification revision: 1

            ### V-01 — Unexpired boundary behaves
            Covers: AC-01
            Setup: token abc, expires_at 20, now 10.
            Oracle / boundary: is_valid returns true.

            ### V-02 — Expired boundary rejected without token change
            Covers: AC-02
            Setup: token abc, expires_at 10, now 10.
            Oracle / boundary: is_valid returns false and token remains abc.
            The task-owned future test tests/test_future.py is feasible with local Python unittest.
            """)
        write(base, "docs/tasks/CURRENT/preflight.md", f"""
            # Preflight: CURRENT

            Status: ready
            Profile: guided
            Source brief: docs/tasks/CURRENT/brief.md
            Verification design: docs/tasks/CURRENT/verification.md
            Verification revision: 1
            Allowed changes: src/session.py; tests/test_future.py
            Dependency: {dependency}
            Ownership: committed baseline; no overlapping user work
            Permission: policy.md allows local writes and tests; network, installs and commits denied
            Capability: {capability}
            Authority: direction.md, revision 1; docs/tasks/CURRENT/brief.md
            Authority revision: 1
            Expected effects: in-scope implementation and docs/tasks/CURRENT/result.md report preserve readiness
            """)
        write(base, "policy.md", "# Policy\n\nLocal writes allowed. Local tests allowed. Network, installs and commits denied.\n")
        write(base, "direction.md", "# Direction\n\nDirection revision 1. Reject expired sessions without changing tokens.\n")
        write(base, "src/session.py", "def is_valid(session, now):\n    return bool(session.get('token'))\n")
        write(base, "tests/__init__.py", "")

    def revised_state(folder, verification_revision, preflight_revision, note):
        write(root, f"docs/tasks/REVISED/{folder}/brief.md", "# REVISED — Scenario revision\n\nStatus: ready\nTask kind: executable\nOutcome: reject expired sessions without changing their token.\nAC-01: unexpired sessions remain valid.\nAC-02: expired sessions are rejected and their token remains unchanged.\nAllowed changes: src/session.py; tests/test_future.py\nTargeted: python -m unittest tests.test_future\n")
        write(root, f"docs/tasks/REVISED/{folder}/verification.md", f"# Verification Design: REVISED\n\nSource brief: docs/tasks/REVISED/{folder}/brief.md\nStatus: ready\n\nVerification revision: {verification_revision}\n\n### V-01 — Unexpired session remains valid\nCovers: AC-01\nSetup: token abc, expires_at 20, now 10.\nOracle / boundary: is_valid returns true.\n\n### V-02 — Expired session rejected\nCovers: AC-02\nSetup: token abc, expires_at 10, now 10.\nOracle / boundary: is_valid returns false.\nThe task-owned future test tests/test_future.py is feasible with local Python unittest.\n{note}")
        write(root, f"docs/tasks/REVISED/{folder}/preflight.md", f"# Preflight: REVISED\n\nStatus: ready\nProfile: guided\nSource brief: docs/tasks/REVISED/{folder}/brief.md\nVerification design: docs/tasks/REVISED/{folder}/verification.md\nVerification revision: {preflight_revision}\nAllowed changes: src/session.py; tests/test_future.py\nDependency: Python standard library only\nOwnership: committed baseline; no overlapping user work\nPermission: local writes and tests allowed; network, installs and commits denied\nCapability: Python unittest observes src/session.py; task-owned future test is feasible\nAuthority: docs/tasks/REVISED/{folder}/brief.md; outcome and scope unchanged\n")

    for folder in ("old", "refreshed", "old-again"):
        revised_state(folder, 1, 1, "")

    task("EVIDENCE",
        "# EVIDENCE — Scenario evidence submission\n\nStatus: ready\n\nTask kind: executable\n\nAC-01: positive boundary behaves.\nAC-02: failure case is rejected.\n",
        "# Verification Design: EVIDENCE\n\nSource brief: docs/tasks/EVIDENCE/brief.md\nStatus: ready\n\nVerification revision: 2\n\n### V-01 — Positive boundary holds\nCovers: AC-01\n\n### V-02 — Negative boundary is rejected\nCovers: AC-02\n\n### V-03 — Network oracle\nCovers: AC-02\n\n### V-04 — Regression oracle\nCovers: AC-01\nCoverage revision under unchanged authority; scenario IDs retained.\n",
        "# Preflight: EVIDENCE\n\nStatus: ready\nProfile: guided\nSource brief: docs/tasks/EVIDENCE/brief.md\nVerification design: docs/tasks/EVIDENCE/verification.md\nVerification revision: 2\n")
    write(root, "docs/tasks/EVIDENCE/verification-v1.md", "# Verification Design: EVIDENCE\n\nSource brief: docs/tasks/EVIDENCE/brief.md\nStatus: ready\n\nVerification revision: 1\n\n### V-01 — Positive boundary holds\nCovers: AC-01\n\n### V-02 — Negative boundary is rejected\nCovers: AC-02\n")
    write(root, "tests/__init__.py", "")
    write(root, "tests/test_boundary.py", "import unittest\n\n\ndef is_within(value, limit):\n    return value <= limit\n\n\nclass BoundaryTest(unittest.TestCase):\n    def test_positive_boundary_holds(self):\n        self.assertTrue(is_within(5, 10))\n")
    write(root, "tests/test_negative.py", "import unittest\n\n\ndef is_within(value, limit):\n    return True  # faulty: accepts every boundary violation\n\n\nclass NegativeTest(unittest.TestCase):\n    def test_negative_boundary_is_rejected(self):\n        self.assertFalse(is_within(11, 10), 'boundary violation was accepted')\n")

    write(root, "evidence/ledger-complete.md",
          "# Scenario evidence ledger (complete)\n\nVerification design: docs/tasks/EVIDENCE/verification.md\nVerification revision: 2\n\nV-01 — passed — command: python -m unittest tests.test_boundary; setup: entry-cases fixture root; oracle: positive boundary assert holds; result: ok\nV-02 — failed — command: python -m unittest tests.test_negative; setup: entry-cases fixture root; oracle: negative boundary assert rejects; result: AssertionError reproduced\nV-03 — blocked — reason: policy denies network access; next owner: task-preflight\nV-04 — unchecked — reason: not exercised in this pass; next owner: fresh task-acceptance-review\nContext reference: docs/tasks/EVIDENCE/preflight.md\nRemaining obligations:\n- V-02 — repair the rejected-boundary failure and rerun python -m unittest tests.test_negative; next owner: bounded-task-implementer, then fresh task-acceptance-review\n- V-03 — resolve the denied network oracle or record a justified replacement; next owner: task-preflight\n- V-04 — exercise unchecked regression coverage; next owner: fresh task-acceptance-review\n")
    write(root, "evidence/ledger-green-gap.md",
          "# Scenario evidence ledger (green gap)\n\nVerification design: docs/tasks/EVIDENCE/verification.md\nAuthoritative AC mapping: AC-01 <- V-01, V-04; AC-02 <- V-02, V-03\nV-01 — passed — green\nAll tests green. Omitted negative scenario V-02: not covered here.\n")
    write(root, "evidence/ledger-obsolete.md",
          "# Scenario evidence ledger (obsolete)\n\nVerification design: docs/tasks/EVIDENCE/verification.md\nAuthoritative AC mapping: AC-01 <- V-01, V-04; AC-02 <- V-02, V-03\nEvidence verification revision: 1\nV-01 — passed — evidence collected before implementation bytes changed.\nCurrent authoritative revision: 2 (docs/tasks/EVIDENCE/verification.md)\n")

    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture baseline")
    write(root, "transitions/expected-implementation/src/session.py", "def is_valid(session, now):\n    return bool(session.get('token')) and session['expires_at'] > now\n")
    write(root, "transitions/expected-report/docs/tasks/CURRENT/result.md", "# Implementation result\n\nReport artifact produced by expected work.\n")
    write(root, "transitions/ownership/src/session.py", "def is_valid(session, now):\n    return True  # user staged change\n")
    git(root, "add", "transitions/ownership/src/session.py")
    write(root, "transitions/ownership/src/session.py", "def is_valid(session, now):\n    return True  # unstaged continuation after staging\n")
    write(root, "transitions/permission/policy.md", "# Policy\n\nLocal writes revoked. Local tests allowed. Network, installs and commits denied.\n")
    write(root, "transitions/authority/direction.md", "# Direction\n\nDirection revision 2. Expired sessions may be accepted.\n")
    (root / "transitions/prerequisite/tools/time_sdk.py").unlink()
    (root / "transitions/capability/tools/secure_clock.py").unlink()
    for folder, preflight_revision in (("old", 1), ("refreshed", 2), ("old-again", 1)):
        revised_state(folder, 2, preflight_revision,
                      "Coverage revision under unchanged authority; scenario IDs retained. V-02 now also asserts token remains abc, closing the existing AC-02 evidence gap.\n")


SCENARIOS = {
    "queue-task": queue_task,
    "scheduler-resume": scheduler_resume,
    "queue-restaged-stale": queue_restaged_stale,
    "api-guided": api_guided,
    "api-immediate": api_immediate,
    "record-correction": record_correction,
    "entry-cases": entry_cases,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
RUNS.mkdir(parents=True, exist_ok=True)
SCENARIOS[sys.argv[1]]()
