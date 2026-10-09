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


def policy(authorized_test_path: str | None = None) -> Path:
    path = RUNS / "policies/local-review-v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    allow = ["cheap local tests", "disposable probes outside repository", "one canonical task-package acceptance report"]
    deny = ["source/test edits", "network", "dependency installation", "commits", "tracker updates"]
    if authorized_test_path is not None:
        allow.append(f"post-verdict tests_only_reproducer write to {authorized_test_path}")
        deny[0] = "source edits and test edits outside the explicitly authorized path"
    path.write_text(json.dumps({
        "id": "local-review-v1",
        "runtime_root": str(RUNS),
        "allow": allow,
        "deny": deny,
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


def queue_defect(*, authorize_reproducer: bool = False) -> None:
    root = WORK / "queue-runner"
    initialize(root)
    test_path = "tests/integration/test_run_next.py" if authorize_reproducer else None
    run_policy = policy(test_path)
    if authorize_reproducer:
        fixture_rule = (
            "# Fixture rules\n\nAcceptance is read-only until a fixed "
            "`CHANGES_REQUESTED` verdict. This invocation may then use "
            "`tests_only_reproducer` only in "
            "`tests/integration/test_run_next.py`. Production remains read-only."
        )
    else:
        fixture_rule = "# Fixture rules\n\nAcceptance is read-only except for the next numbered report under the task package's `reviews/` directory."
    write(root, "AGENTS.md", fixture_rule)
    write(root, "docs/tasks/QR-12/brief.md", "# QR-12\n\nArtifact status: ready_for_preflight\nAC-01: two consecutive public invocations persist state and claim TASK-1 then TASK-2.\nAllowed paths: src/queue/run_next.py; tests/integration/test_run_next.py")
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
Task brief: docs/tasks/QR-12/brief.md
Task brief SHA-256: {file_sha(root / 'docs/tasks/QR-12/brief.md')}
Baseline HEAD: {head}
Baseline exact git status --short: clean
Allowed paths: src/queue/run_next.py; tests/integration/test_run_next.py
Run policy: {run_policy}
Packet path: docs/tasks/QR-12/preflight.md
Post-packet status: ?? docs/tasks/QR-12/preflight.md
Report path: docs/tasks/QR-12/reviews/acceptance-01.md
AC-01 requires an independent two-invocation public-entry probe in disposable state.
Legacy finding: trace guards that compare against any initially running task.
"""
    packet_path = root / "docs/tasks/QR-12/preflight.md"
    packet_path.write_text(packet, encoding="utf-8")
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


def queue_defect_reproducer() -> None:
    queue_defect(authorize_reproducer=True)


def exporter_accept() -> None:
    root = WORK / "exporter"
    initialize(root)
    run_policy = policy()
    write(root, "AGENTS.md", "# Fixture rules\n\nAcceptance may write only the next numbered task-package report. Preserve user notes and use disposable probe state outside the repository.")
    write(root, "docs/tasks/EXP-08/brief.md", "# EXP-08\n\nArtifact status: ready_for_preflight\nAC-01: `exportctl resume` appends remaining rows after checkpoint.\nAC-02: retry adds no duplicate rows.\nAllowed paths: src/exporter/resume.py; tests/integration/test_resume.py")
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
    packet_path = root / "docs/tasks/EXP-08/preflight.md"
    packet_path.write_text(f"""# Task Preflight Packet: EXP-08
Artifact status: ready
Repository root: {root}
Task brief: docs/tasks/EXP-08/brief.md
Task brief SHA-256: {file_sha(root / 'docs/tasks/EXP-08/brief.md')}
Baseline HEAD: {git(root, 'rev-parse', 'HEAD')}
Baseline exact git status --short:\n{baseline_status}
Post-packet git status --short:\n__POST_PACKET_STATUS__
Pre-existing path: notes/local.md
Index SHA-256: {sha(index_bytes)}
Worktree SHA-256: {file_sha(root / 'notes/local.md')}
Ownership: user; task overlap: no
Allowed paths: src/exporter/resume.py; tests/integration/test_resume.py
Run policy: {run_policy}
Packet path: docs/tasks/EXP-08/preflight.md
Report path: docs/tasks/EXP-08/reviews/acceptance-01.md
Targeted: python -m unittest tests.integration.test_resume
Public probe: python -m src.exporter.resume INPUT CHECKPOINT OUTPUT
""", encoding="utf-8")
    packet_path.write_text(
        packet_path.read_text(encoding="utf-8").replace(
            "__POST_PACKET_STATUS__", git(root, "status", "--short")
        ),
        encoding="utf-8",
    )
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
            existing.extend(rows[checkpoint:])
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
                    source.write_text(json.dumps(["one", "same", "same"]))
                    resume(source, checkpoint, output)
                    resume(source, checkpoint, output)
                    self.assertEqual(
                        output.read_text().splitlines(), ["one", "same", "same"]
                    )
        """,
    )
    worker(run_dir, "EXP-08", ["src/exporter/resume.py", "tests/integration/test_resume.py"], ["python -m unittest tests.integration.test_resume", "python -m unittest discover -s tests"])


def scheduler_inconclusive() -> None:
    root = WORK / "scheduler"
    initialize(root)
    run_policy = policy()
    write(root, "AGENTS.md", "# Fixture rules\n\nAcceptance may not invent missing concurrency infrastructure or use live services.")
    write(root, "docs/tasks/SCH-09/brief.md", "# SCH-09\n\nArtifact status: ready_for_preflight\nAC-01: two coordinated workers cannot claim the same job.\nRequired helper: tests/helpers/concurrent_claims.py")
    write(root, "src/scheduler/claim.py", "def claim(job):\n    return job['id']")
    write(root, "tests/helpers/concurrent_claims.py", "def coordinated_claims(claim):\n    return claim(), claim()")
    write(root, "tests/test_claim.py", "import unittest\n\nclass ClaimTest(unittest.TestCase):\n    def test_unit(self):\n        self.assertTrue(True)")
    git(root, "add", ".")
    git(root, "commit", "-qm", "preflight baseline")
    helper_digest = file_sha(root / "tests/helpers/concurrent_claims.py")
    run_dir = RUNS / "SCH-09"
    run_dir.mkdir(parents=True, exist_ok=True)
    packet_path = root / "docs/tasks/SCH-09/preflight.md"
    packet_path.write_text(f"""# Task Preflight Packet: SCH-09
Artifact status: ready
Repository root: {root}
Task brief: docs/tasks/SCH-09/brief.md
Baseline HEAD: {git(root, 'rev-parse', 'HEAD')}
Baseline status: clean
Post-packet git status --short: __POST_PACKET_STATUS__
Required helper: tests/helpers/concurrent_claims.py
Helper SHA-256: {helper_digest}
Allowed paths: src/scheduler/claim.py; tests/test_claim.py
Run policy: {run_policy}
Packet path: docs/tasks/SCH-09/preflight.md
Report path: docs/tasks/SCH-09/reviews/acceptance-01.md
""", encoding="utf-8")
    packet_path.write_text(
        packet_path.read_text(encoding="utf-8").replace(
            "__POST_PACKET_STATUS__", git(root, "status", "--short")
        ),
        encoding="utf-8",
    )
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


def ledger_defects() -> None:
    root = WORK / "ledger-runner"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        "# Fixture rules\n\nReview is read-only. Use guided acceptance and report findings inline.",
    )
    write(
        root,
        "docs/tasks/LED-04/brief.md",
        """
        # LED-04 — Enforce ledger coherence

        Status: ready
        Allowed paths: src/ledger/state.py; tests/test_state.py.
        AC-01: a ready run has no running task and its ready set equals every
        dependency-ready task.
        AC-02: a running run has exactly one running selected task and its
        active attempt is that task's latest attempt.
        AC-03: a stopped run has no running task; revisions reject booleans;
        completed_task_ids is an array.
        Review: immediate.
        """,
    )
    write(root, "src/__init__.py", "")
    write(root, "src/ledger/__init__.py", "")
    write(root, "src/ledger/state.py", "def validate_ledger(ledger):\n    raise NotImplementedError")
    write(root, "tests/__init__.py", "")
    write(root, "tests/test_state.py", "import unittest\n\nclass Placeholder(unittest.TestCase):\n    def test_placeholder(self):\n        self.assertTrue(True)")
    git(root, "add", ".")
    git(root, "commit", "-qm", "review baseline")
    write(
        root,
        "src/ledger/state.py",
        """
        def validate_ledger(ledger):
            if not isinstance(ledger.get("revision"), int):
                raise ValueError("revision")

            tasks = ledger["tasks"]
            selected_id = ledger.get("selected_task_id")
            selected = next((task for task in tasks if task["id"] == selected_id), None)

            if ledger["status"] == "ready":
                if selected is not None and selected["status"] == "running":
                    raise ValueError("selected task running")
                if not any(task["status"] == "ready" for task in tasks):
                    raise ValueError("no ready task")
            elif ledger["status"] == "running":
                if selected is None or selected["status"] != "running":
                    raise ValueError("selected task not running")
                if ledger.get("active_attempt_id") not in selected["attempt_ids"]:
                    raise ValueError("unknown active attempt")
            elif ledger["status"] == "stopped":
                if selected is not None and selected["status"] == "running":
                    raise ValueError("selected task running")

            return True
        """,
    )
    write(
        root,
        "tests/test_state.py",
        """
        import unittest

        from src.ledger.state import validate_ledger


        class LedgerTest(unittest.TestCase):
            def test_valid_running_ledger(self):
                ledger = {
                    "revision": 2,
                    "status": "running",
                    "selected_task_id": "TASK-1",
                    "active_attempt_id": "A-2",
                    "completed_task_ids": [],
                    "tasks": [
                        {"id": "TASK-1", "status": "running", "attempt_ids": ["A-1", "A-2"]},
                        {"id": "TASK-2", "status": "initialized", "attempt_ids": []},
                    ],
                }
                self.assertTrue(validate_ledger(ledger))
        """,
    )


def authored_production_self_check() -> None:
    root = WORK / "authored-production"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        "# Fixture rules\n\nThe requested implementation edit is authorized. "
        "Any acceptance check in the authoring session is self-check only.",
    )
    write(
        root,
        "docs/tasks/PRICE-02/brief.md",
        """
        # PRICE-02 — Add the approved service fee

        Status: ready
        Allowed paths: src/pricing.py.
        AC-01: `total(100)` returns `110.0`.
        Review: immediate and independent after implementation.
        """,
    )
    write(root, "src/pricing.py", "def total(subtotal):\n    return subtotal")
    write(
        root,
        "tests/test_pricing.py",
        """
        import unittest

        from src.pricing import total


        class PricingTest(unittest.TestCase):
            def test_approved_service_fee(self):
                self.assertEqual(total(100), 110.0)
        """,
    )
    write(root, "src/__init__.py", "")
    write(root, "tests/__init__.py", "")
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture baseline")


def workflow_matrix_defects() -> None:
    root = WORK / "workflow-runner"
    initialize(root)
    write(root, "AGENTS.md", "# Fixture rules\n\nAcceptance is read-only. Use only disposable copies of case state for probes.")
    write(
        root,
        "docs/tasks/WF-21/brief.md",
        """
        # WF-21 — Validate persisted workflow state before execution

        Status: ready
        Allowed paths: src/workflow/runner.py; tests/test_contract_probes.py.
        Public entry: `python -m src.workflow.runner STATE AUTHORITY`.
        Owning suite: `python -m unittest discover -s tests`.

        Coverage rows:
        - WF-TAMPER: prompt and model must match the independently stored
          authority hashes. Coherent changes to both fields and their mutable
          manifest hashes must be rejected before execution.
        - WF-REPLAY: an existing execution publication is reused after verifier
          drift; only current verification may run and execution_count remains
          one.
        - WF-DECISION: publication order is a legal prefix of execution,
          verification, decision, ledger. A decision-only artifact is rejected
          before execution or writes.

        """,
    )
    write(root, "src/__init__.py", "")
    write(root, "src/workflow/__init__.py", "")
    runner_source = """
        import hashlib
        import json
        from pathlib import Path
        import sys


        def digest(value):
            return hashlib.sha256(value.encode()).hexdigest()


        def resume(state_path, authority_path):
            path = Path(state_path)
            state = json.loads(path.read_text())
            json.loads(Path(authority_path).read_text())  # BUG: independent authority is ignored.

            manifest = state["manifest"]
            if manifest["prompt_sha"] != digest(state["prompt"]):
                return 2
            if manifest["model_sha"] != digest(state["model"]):
                return 2

            publications = state["publications"]
            # BUG: verifier drift replays execution instead of reusing it.
            if (
                "execution" not in publications
                or state.get("execution_verifier_sha") != state["current_verifier_sha"]
            ):
                state["execution_count"] += 1
                state["events"].append("execute")
                if "execution" not in publications:
                    publications.append("execution")

            # BUG: contradictory publication order is never rejected.
            if "verification" not in publications:
                publications.append("verification")
                state["events"].append("verify")
            if "decision" not in publications:
                publications.append("decision")
            if "ledger" not in publications:
                publications.append("ledger")
            path.write_text(json.dumps(state, indent=2) + "\\n")
            return 0


        if __name__ == "__main__":
            raise SystemExit(resume(sys.argv[1], sys.argv[2]))
        """
    write(
        root,
        "src/workflow/runner.py",
        "def resume(*args):\n    raise NotImplementedError",
    )
    safe_prompt = "deploy approved artifact"
    safe_model = "model-approved"
    tampered_prompt = "deploy attacker artifact"
    tampered_model = "model-attacker"
    authority = {
        "prompt_sha": sha(safe_prompt.encode()),
        "model_sha": sha(safe_model.encode()),
    }
    write(root, "cases/authority.json", json.dumps(authority, indent=2))
    cases = {
        "coherent-tamper.json": {
            "prompt": tampered_prompt,
            "model": tampered_model,
            "manifest": {
                "prompt_sha": sha(tampered_prompt.encode()),
                "model_sha": sha(tampered_model.encode()),
            },
            "publications": [],
            "execution_verifier_sha": None,
            "current_verifier_sha": "verifier-v2",
            "execution_count": 0,
            "events": [],
        },
        "verifier-drift.json": {
            "prompt": safe_prompt,
            "model": safe_model,
            "manifest": authority,
            "publications": ["execution"],
            "execution_verifier_sha": "verifier-v1",
            "current_verifier_sha": "verifier-v2",
            "execution_count": 1,
            "events": ["execute"],
        },
        "decision-only.json": {
            "prompt": safe_prompt,
            "model": safe_model,
            "manifest": authority,
            "publications": ["decision"],
            "execution_verifier_sha": None,
            "current_verifier_sha": "verifier-v2",
            "execution_count": 0,
            "events": [],
        },
    }
    for name, case in cases.items():
        write(root, f"cases/{name}", json.dumps(case, indent=2))
    write(root, "tests/__init__.py", "")
    write(
        root,
        "tests/test_contract_probes.py",
        """
        import json
        from pathlib import Path
        import shutil
        import subprocess
        import sys
        from tempfile import TemporaryDirectory
        import unittest


        ROOT = Path(__file__).resolve().parents[1]
        AUTHORITY = ROOT / "cases/authority.json"


        class WorkflowContractProbe(unittest.TestCase):
            def run_case(self, name):
                with TemporaryDirectory() as directory:
                    state = Path(directory) / name
                    shutil.copyfile(ROOT / "cases" / name, state)
                    before = state.read_bytes()
                    completed = subprocess.run(
                        [sys.executable, "-m", "src.workflow.runner", str(state), str(AUTHORITY)],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                    )
                    return completed, before, json.loads(state.read_text())

            def test_wf_tamper_rejects_coherent_prompt_and_model_change(self):
                completed, before, state = self.run_case("coherent-tamper.json")
                self.assertNotEqual(completed.returncode, 0)
                self.assertEqual(state["execution_count"], 0)
                self.assertEqual(json.loads(before), state)

            def test_wf_replay_reuses_execution_after_verifier_drift(self):
                completed, before, state = self.run_case("verifier-drift.json")
                self.assertEqual(completed.returncode, 0)
                self.assertEqual(state["execution_count"], 1)
                self.assertEqual(state["events"].count("execute"), 1)

            def test_wf_decision_rejects_decision_only_artifact(self):
                completed, before, state = self.run_case("decision-only.json")
                self.assertNotEqual(completed.returncode, 0)
                self.assertEqual(state["execution_count"], 0)
                self.assertEqual(json.loads(before), state)
        """,
    )
    git(root, "add", ".")
    git(root, "commit", "-qm", "review baseline")
    # The submitted implementation is intentionally defective but scoped.
    write(root, "src/workflow/runner.py", runner_source)
    run_dir = RUNS / "WF-21"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "review-continuation.md").write_text(
        """Review continuation:
- Iteration / current byte identity: prior review; bytes have since changed
- Coverage rows: WF-TAMPER=pass; WF-REPLAY=fail; WF-DECISION=unchecked
- Finding IDs: WF-F1
- Reviewer regressions: tests.test_contract_probes.WorkflowContractProbe.test_wf_replay_reuses_execution_after_verifier_drift
- Broad gate: not run after targeted failure
- Next: continue independent review of the current bytes
""",
        encoding="utf-8",
    )


def process_cleanup_defects() -> None:
    root = WORK / "process-runner"
    initialize(root)
    write(root, "AGENTS.md", "# Fixture rules\n\nUse bounded process probes. Every probe must clean its process group in `finally`.")
    write(
        root,
        "docs/tasks/PROC-17/brief.md",
        """
        # PROC-17 — Clean an entire timed-out process tree

        Status: ready
        Allowed paths: src/process_runner.py; tests/test_cleanup_contract.py.
        Invariant PROC-CLEANUP: after timeout or leader exit, no descendant may
        remain alive or retain inherited output pipes.

        Material cases:
        - PROC-RESIST: a descendant ignores SIGTERM after the leader times out.
        - PROC-PIPE: the leader exits while a descendant holds inherited pipes.
        - PROC-RACE: descendant visibility changes as the leader exits.

        Probes use file events and bounded polling; arbitrary sleeps and
        unbounded waits are prohibited.
        """,
    )
    write(root, "src/__init__.py", "")
    runner_source = """
        import subprocess


        def run_command(command, timeout=0.25):
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )
            try:
                return process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # BUG: only the leader is terminated; descendants and inherited
                # pipes are not handled, and an exited leader skips cleanup.
                if process.poll() is None:
                    process.terminate()
                return process.wait(timeout=0.5)
        """
    write(
        root,
        "src/process_runner.py",
        "def run_command(*args, **kwargs):\n    raise NotImplementedError",
    )
    write(
        root,
        "fixtures/process_tree.py",
        """
        from pathlib import Path
        import os
        import signal
        import subprocess
        import sys
        import threading
        import time


        def wait_path(path, timeout=2.0):
            deadline = time.monotonic() + timeout
            event = threading.Event()
            while time.monotonic() < deadline:
                if path.exists():
                    return
                event.wait(0.01)
            raise TimeoutError(path)


        state = Path(sys.argv[2])
        state.mkdir(parents=True, exist_ok=True)

        if sys.argv[1] == "child":
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            (state / "child.pid").write_text(str(os.getpid()))
            (state / "child.ready").write_text("ready")
            threading.Event().wait(5.0)
            raise SystemExit(0)

        (state / "parent.pid").write_text(str(os.getpid()))
        scenario = sys.argv[1]
        child_command = [sys.executable, __file__, "child", str(state)]

        if scenario == "resistant":
            subprocess.Popen(child_command)
            wait_path(state / "child.ready")
            (state / "parent.ready").write_text("ready")
            threading.Event().wait(5.0)
        elif scenario == "pipe-holder":
            subprocess.Popen(child_command)
            wait_path(state / "child.ready")
        elif scenario == "visibility-race":
            (state / "parent.ready").write_text("ready")
            wait_path(state / "release")
            subprocess.Popen(child_command)
            wait_path(state / "child.ready")
        else:
            raise SystemExit(f"unknown scenario: {scenario}")
        """,
    )
    write(root, "tests/__init__.py", "")
    write(
        root,
        "tests/test_cleanup_contract.py",
        """
        from pathlib import Path
        import os
        import signal
        import subprocess
        import sys
        from tempfile import TemporaryDirectory
        import threading
        import time
        import unittest

        from src import process_runner


        ROOT = Path(__file__).resolve().parents[1]
        TREE = ROOT / "fixtures/process_tree.py"


        def wait_path(path, timeout=2.0):
            deadline = time.monotonic() + timeout
            event = threading.Event()
            while time.monotonic() < deadline:
                if path.exists():
                    return
                event.wait(0.01)
            raise AssertionError(f"timed out waiting for {path}")


        REAL_POPEN = subprocess.Popen


        def is_alive(pid):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return False
            return True


        def group_is_alive(pgid):
            try:
                os.killpg(pgid, 0)
            except ProcessLookupError:
                return False
            return True


        def wait_until(predicate, description, timeout=2.0):
            deadline = time.monotonic() + timeout
            event = threading.Event()
            while time.monotonic() < deadline:
                if predicate():
                    return
                event.wait(0.01)
            raise AssertionError(f"cleanup timed out waiting for {description}")


        def run_tracked(command, processes):
            def tracked_popen(*args, **kwargs):
                process = REAL_POPEN(*args, **kwargs)
                processes.append(process)
                return process

            original = process_runner.subprocess.Popen
            process_runner.subprocess.Popen = tracked_popen
            try:
                return process_runner.run_command(command)
            finally:
                process_runner.subprocess.Popen = original


        def cleanup_group(state, processes):
            parent_path = state / "parent.pid"
            parent_pid = (
                int(parent_path.read_text())
                if parent_path.exists()
                else processes[0].pid if processes else None
            )
            child_path = state / "child.pid"
            child_pid = int(child_path.read_text()) if child_path.exists() else None

            if parent_pid is not None:
                try:
                    os.killpg(parent_pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if child_pid is not None:
                try:
                    os.kill(child_pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

            for process in processes:
                try:
                    process.communicate(timeout=2.0)
                except subprocess.TimeoutExpired as error:
                    for stream_name in ("stdout", "stderr"):
                        stream = getattr(process, stream_name)
                        if stream is not None:
                            stream.close()
                    raise AssertionError(
                        "cleanup timed out waiting for inherited output pipes to close"
                    ) from error
                for stream_name in ("stdout", "stderr"):
                    stream = getattr(process, stream_name)
                    if stream is not None and not stream.closed:
                        raise AssertionError(
                            f"cleanup left {stream_name} pipe open for pid {process.pid}"
                        )

            if parent_pid is not None:
                wait_until(
                    lambda: not group_is_alive(parent_pid),
                    f"process group {parent_pid} to disappear",
                )
                wait_until(
                    lambda: not is_alive(parent_pid),
                    f"leader pid {parent_pid} to disappear",
                )
            if child_pid is not None:
                wait_until(
                    lambda: not is_alive(child_pid),
                    f"descendant pid {child_pid} to disappear",
                )


        class CleanupContractProbe(unittest.TestCase):
            def command(self, scenario, state):
                return [sys.executable, str(TREE), scenario, str(state)]

            def assert_child_cleaned(self, state):
                wait_path(state / "child.pid")
                self.assertFalse(is_alive(int((state / "child.pid").read_text())))

            def test_proc_resist_kills_resistant_descendant(self):
                with TemporaryDirectory() as directory:
                    state = Path(directory)
                    processes = []
                    try:
                        run_tracked(self.command("resistant", state), processes)
                        self.assert_child_cleaned(state)
                    finally:
                        cleanup_group(state, processes)

            def test_proc_pipe_cleans_holder_after_leader_exit(self):
                with TemporaryDirectory() as directory:
                    state = Path(directory)
                    processes = []
                    try:
                        run_tracked(self.command("pipe-holder", state), processes)
                        self.assert_child_cleaned(state)
                    finally:
                        cleanup_group(state, processes)

            def test_proc_race_rechecks_descendant_after_leader_exit(self):
                with TemporaryDirectory() as directory:
                    state = Path(directory)
                    result = {}
                    processes = []
                    thread = threading.Thread(
                        target=lambda: result.setdefault(
                            "code",
                            run_tracked(
                                self.command("visibility-race", state), processes
                            ),
                        )
                    )
                    try:
                        thread.start()
                        wait_path(state / "parent.ready")
                        (state / "release").write_text("go")
                        thread.join(timeout=2.0)
                        self.assertFalse(thread.is_alive(), "runner did not finish within bound")
                        self.assertEqual(result.get("code"), 0)
                        self.assert_child_cleaned(state)
                    finally:
                        cleanup_group(state, processes)
                        thread.join(timeout=1.0)
                        self.assertFalse(
                            thread.is_alive(), "runner thread survived fixture cleanup"
                        )
        """,
    )
    git(root, "add", ".")
    git(root, "commit", "-qm", "review baseline")
    write(root, "src/process_runner.py", runner_source)


def discovery_report(task_id: str, root: Path, completeness: str, body: str) -> None:
    """Stage the independent discovery report consumed by the decision evals.

    The inherited scenario functions keep their real public/process inputs and
    outputs untouched; this helper adds the discovery publication on top.
    """
    run_dir = RUNS / task_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "discovery-01.md").write_text(
        "# Task Review Discovery Report: " + task_id + "\n\n"
        "| Field | Value |\n|---|---|\n"
        "| Producing stage | `task-review-discovery` |\n"
        "| Coverage completeness | " + completeness + " |\n"
        "| Discovery iteration | first independent discovery pass |\n"
        "| Repository root | " + str(root) + " |\n"
        "| Durable report path | task-runs/" + task_id + "/discovery-01.md |\n"
        "| Current submission | task-runs/" + task_id + "/worker-result.json |\n\n"
        "This report publishes evidence only. It contains no acceptance verdict, no\n"
        "approved deferral, and no advancement. The separate acceptance decision call\n"
        "consumes it.\n\n"
        + textwrap.dedent(body).strip().replace("{head}", git(root, "rev-parse", "HEAD")) + "\n",
        encoding="utf-8",
    )


def queue_defect_decision() -> None:
    queue_defect()
    discovery_report(
        "QR-12",
        WORK / "queue-runner",
        "complete",
        """
        ## Coverage ledger

        | Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
        |---|---|---|---|---|---|---|
        | QR-RUN1 | AC-01: two consecutive public invocations persist state and claim TASK-1 then TASK-2 | first invocation claims TASK-1 and persists; second claims TASK-2 | disposable persisted state; `runner run-next STATE` twice | worker-observed pass | first invocation claimed TASK-1 and persisted the running state; the second real invocation returned no claim because the first task is still running | fail |

        ## Findings

        ### F-01 [suggested P1] Second invocation cannot claim TASK-2

        | Field | Evidence |
        |---|---|
        | Finding ID | `F-01` |
        | Suggested severity | `P1` |
        | Current location | `src/queue/run_next.py` |
        | Triggering state/input | a state file whose first task is still running when `run_next` runs again |
        | Consequence | the required second consecutive public invocation cannot claim TASK-2 |
        | Evidence | real public entry `runner run-next` executed twice against persisted disposable state; first invocation claimed TASK-1 and persisted, second returned no claim |
        | Affected AC | `AC-01` |
        | Broken invariant | repeated flow must claim both tasks across two consecutive public invocations |
        | Credible sibling surface | any persisted state whose first task is running hides later ready tasks |
        | Smallest corrective direction | claim the next ready task across repeated public invocations instead of guarding against any running task |

        ## Aggregate-gate decision

        | Field | Value |
        |---|---|
        | Gate / exact command | `python -m unittest discover -s tests` |
        | Status | `not run` |
        | Owner and stage | `initial discovery` |
        | Reason | decisive targeted failure of `QR-RUN1` suppressed the aggregate |

        ## Discovery continuation

        ```markdown
        Discovery continuation:
        - Iteration / current byte identity: first discovery pass; HEAD {head}
        - Coverage rows: QR-RUN1=fail
        - Finding IDs: F-01 (suggested P1)
        - Reviewer regressions: none
        - Aggregate gate: not run after targeted failure; owner: initial discovery
        - Next: separate acceptance decision call
        ```
        """,
    )


def queue_defect_reproducer_decision() -> None:
    queue_defect_reproducer()
    discovery_report(
        "QR-12",
        WORK / "queue-runner",
        "complete",
        """
        ## Coverage ledger

        | Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
        |---|---|---|---|---|---|---|
        | QR-RUN1 | AC-01: two consecutive public invocations persist state and claim TASK-1 then TASK-2 | first invocation claims TASK-1 and persists; second claims TASK-2 | disposable persisted state; `runner run-next STATE` twice | worker-observed pass | first invocation claimed TASK-1 and persisted the running state; the second real invocation returned no claim because the first task is still running | fail |

        ## Findings

        ### F-01 [suggested P1] Second invocation cannot claim TASK-2

        | Field | Evidence |
        |---|---|
        | Finding ID | `F-01` |
        | Suggested severity | `P1` |
        | Current location | `src/queue/run_next.py` |
        | Triggering state/input | a state file whose first task is still running when `run_next` runs again |
        | Consequence | the required second consecutive public invocation cannot claim TASK-2 |
        | Evidence | real public entry `runner run-next` executed twice against persisted disposable state; first invocation claimed TASK-1 and persisted, second returned no claim |
        | Affected AC | `AC-01` |
        | Broken invariant | repeated flow must claim both tasks across two consecutive public invocations |
        | Credible sibling surface | any persisted state whose first task is running hides later ready tasks |
        | Smallest corrective direction | claim the next ready task across repeated public invocations instead of guarding against any running task |

        ## Aggregate-gate decision

        | Field | Value |
        |---|---|
        | Gate / exact command | `python -m unittest discover -s tests` |
        | Status | `not run` |
        | Owner and stage | `initial discovery` |
        | Reason | decisive targeted failure of `QR-RUN1` suppressed the aggregate |

        ## Discovery continuation

        ```markdown
        Discovery continuation:
        - Iteration / current byte identity: first discovery pass; HEAD {head}
        - Coverage rows: QR-RUN1=fail
        - Finding IDs: F-01 (suggested P1)
        - Reviewer regressions: none
        - Aggregate gate: not run after targeted failure; owner: initial discovery
        - Next: separate acceptance decision call
        ```
        """,
    )


def exporter_accept_decision() -> None:
    exporter_accept()
    discovery_report(
        "EXP-08",
        WORK / "exporter",
        "complete",
        """
        ## Coverage ledger

        | Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
        |---|---|---|---|---|---|---|
        | EXP-RESUME | AC-01: `exportctl resume` appends remaining rows after checkpoint; AC-02: retry adds no duplicate rows | first export; resume appends; retry is idempotent | real public `exportctl resume INPUT CHECKPOINT OUTPUT` in disposable state | worker-observed pass | first export wrote the rows and checkpoint; a resumed run appended only the remaining positional rows; a retry created no duplicate rows | pass |
        | EXP-SCOPE | clean scoped diff; pre-existing user work untouched | preflight baseline versus current state | separate index/worktree identities for `notes/local.md` | worker claim | index and worktree fingerprints of the pre-existing `MM` user path are unchanged; only allowed task-owned paths changed | pass |

        ## Findings

        No findings.

        ## Aggregate-gate decision

        | Field | Value |
        |---|---|
        | Gate / exact command | `python -m unittest discover -s tests` |
        | Status | `passed` |
        | Owner and stage | `initial discovery` |
        | Reason | clean targeted public evidence justified one aggregate |
        | Current evidence | all tests passed after the clean public resume/retry observations |

        ## Discovery continuation

        ```markdown
        Discovery continuation:
        - Iteration / current byte identity: first discovery pass; HEAD {head}
        - Coverage rows: EXP-RESUME=pass; EXP-SCOPE=pass
        - Finding IDs: none
        - Reviewer regressions: none
        - Aggregate gate: passed; owner: initial discovery
        - Next: separate acceptance decision call
        ```
        """,
    )


def scheduler_inconclusive_decision() -> None:
    scheduler_inconclusive()
    discovery_report(
        "SCH-09",
        WORK / "scheduler",
        "partial — blocked capability",
        """
        ## Coverage ledger

        | Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
        |---|---|---|---|---|---|---|
        | SCH-CLAIM | AC-01: two coordinated workers cannot claim the same job | coordinated pair claiming one job | required helper `tests/helpers/concurrent_claims.py` plus a coordinated run | worker-observed unit pass | the preflight-recorded helper digest exists but the helper file is now absent; the passing unit suite does not exercise two coordinated workers; no decisive concurrency capability is available | blocked — helper removed after preflight |

        ## Findings

        No confirmed findings. The blocked row is an evidence gap, not a defect claim.

        ## Aggregate-gate decision

        | Field | Value |
        |---|---|
        | Gate / exact command | `python -m unittest discover -s tests` |
        | Status | `not run` |
        | Owner and stage | `initial discovery` |
        | Reason | blocked decisive capability; the unit suite does not cover the AC |

        ## Discovery continuation

        ```markdown
        Discovery continuation:
        - Iteration / current byte identity: first discovery pass; HEAD {head}
        - Coverage rows: SCH-CLAIM=blocked (helper removed after preflight)
        - Finding IDs: none
        - Reviewer regressions: none
        - Aggregate gate: not run; blocked capability
        - Next: evidence owner `task-preflight` or the prerequisite capability owner, then renewed discovery and decision
        ```
        """,
    )


def exporter_restaged_stale_decision() -> None:
    exporter_restaged_stale()
    discovery_report(
        "EXP-08",
        WORK / "exporter",
        "partial — scope gap",
        """
        ## Coverage ledger

        | Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
        |---|---|---|---|---|---|---|
        | EXP-SCOPE | reconstruct a safe scoped diff from the preflight baseline | index blob versus worktree bytes and short status | preflight-recorded separate index/worktree identities for `notes/local.md` | worker claim | the preflight-recorded index digest differs from the current index blob while worktree bytes and short-status text still match; the baseline is unsafe to reconstruct | blocked — unexplained index state |

        ## Findings

        No confirmed findings. The blocked row is a published scope gap, not a defect claim.

        ## Aggregate-gate decision

        | Field | Value |
        |---|---|
        | Gate / exact command | `python -m unittest discover -s tests` |
        | Status | `not run` |
        | Owner and stage | `initial discovery` |
        | Reason | unsafe scope reconstruction precedes any gate |

        ## Discovery continuation

        ```markdown
        Discovery continuation:
        - Iteration / current byte identity: first discovery pass; HEAD {head}
        - Coverage rows: EXP-SCOPE=blocked (unexplained index state)
        - Finding IDs: none
        - Reviewer regressions: none
        - Aggregate gate: not run; scope gap
        - Next: fresh `task-preflight`, then renewed discovery and decision
        ```
        """,
    )


def ledger_defects_decision() -> None:
    ledger_defects()
    discovery_report(
        "LED-04",
        WORK / "ledger-runner",
        "complete",
        """
        ## Coverage ledger

        All validator rows exercise the staged boundary `validate_ledger` from
        `src.ledger.state` on the concrete instances named in each row.

        | Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
        |---|---|---|---|---|---|---|
        | LED-VALID | a valid running ledger is accepted | valid running ledger with latest attempt | `validate_ledger` from `src.ledger.state` on the staged valid running ledger in `tests/test_state.py`; staged focused check `python -m unittest tests.test_state` exit 0 | worker-observed pass | staged focused check `python -m unittest tests.test_state` exited 0; `validate_ledger` accepted the valid running ledger | pass |
        | LED-SELECT | a valid selected task cannot hide an invalid non-selected running task | non-selected task also running | invalid instance targeting the constraint | worker claim | validator accepted a running non-selected task alongside a valid selected task | fail |
        | LED-CARD | a running run has exactly one running task | zero, one, and two running tasks | invalid instances targeting cardinality | worker claim | validator admitted more than one running task | fail |
        | LED-ORDER | the active attempt is the latest attempt | older, latest, missing attempts | invalid instance targeting ordering | worker claim | validator accepted a non-latest active attempt | fail |
        | LED-READY | the ready set equals every dependency-ready task | missing and extra ready tasks | invalid instances targeting the ready set | worker claim | validator accepted an inexact ready set | fail |
        | LED-STOP | a stopped run has no running task | stopped run with completed selected task and running sibling | invalid instance targeting stopped-parent/running-child coherence | worker claim | validator accepted a stopped run with a completed selected task and a running sibling task | fail |
        | LED-TYPES | revisions are integers and completed_task_ids is an array | boolean revision; string completed_task_ids | invalid instances targeting type strictness | worker claim | validator accepted a boolean revision and a string completed_task_ids | fail |

        ## Findings

        - F-01 [suggested P1] selected/non-selected state coherence: a running non-selected task survives validation; broken invariant: ready/running states must reject incoherent sibling states; credible sibling surface: any non-selected task state; smallest corrective direction: validate every task, not only the selected one.
        - F-02 [suggested P1] exact cardinality: more than one running task is admitted; broken invariant: exactly one running selected task; sibling surface: zero and two running tasks; direction: enforce the exact running count.
        - F-07 [suggested P1] stopped-run state coherence: a stopped run with a running non-selected task survives validation; broken invariant: a stopped run has no running task; sibling surface: terminal-parent/non-selected-child coherence; direction: reject any running task in a stopped run, not only the selected one.
        - F-03 [suggested P2] latest-attempt ordering: a non-latest active attempt is accepted; broken invariant: active attempt is the latest attempt; sibling surface: older, missing, duplicated attempts; direction: compare against the latest attempt.
        - F-04 [suggested P2] inexact ready set: ready tasks are not compared against dependencies; broken invariant: the ready set equals every dependency-ready task; sibling surface: missing and extra ready tasks; direction: compare the exact ready set.
        - F-05 [suggested P2] boolean revision accepted as an integer revision; broken invariant: revisions are integers; sibling surface: boolean and string revisions; direction: reject non-integer revisions.
        - F-06 [suggested P2] string completed_task_ids accepted as an array; broken invariant: completed_task_ids is an array; sibling surface: string and boolean collections; direction: reject non-array completed_task_ids.

        ## Aggregate-gate decision

        | Field | Value |
        |---|---|
        | Gate / exact command | `python -m unittest discover -s tests` |
        | Status | `not run` |
        | Owner and stage | `initial discovery` |
        | Reason | decisive targeted validator failures suppressed the aggregate |

        ## Discovery continuation

        ```markdown
        Discovery continuation:
        - Iteration / current byte identity: first discovery pass; HEAD {head}
        - Coverage rows: LED-VALID=pass; LED-SELECT=fail; LED-CARD=fail; LED-ORDER=fail; LED-READY=fail; LED-STOP=fail; LED-TYPES=fail
        - Finding IDs: F-01, F-02, F-03, F-04, F-05, F-06, F-07
        - Reviewer regressions: none
        - Aggregate gate: not run after targeted failures; owner: initial discovery
        - Next: separate acceptance decision call
        ```
        """,
    )


def workflow_matrix_defects_decision() -> None:
    workflow_matrix_defects()
    discovery_report(
        "WF-21",
        WORK / "workflow-runner",
        "complete",
        """
        ## Coverage ledger

        | Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
        |---|---|---|---|---|---|---|
        | WF-TAMPER | prompt and model must match the independently stored authority hashes | coherent prompt+model change with recomputed manifest hashes | public `python -m src.workflow.runner STATE AUTHORITY` on disposable copies | submitted test pass claim | coherent tampering reached execution: the runner returned 0 and appended an execute event | fail |
        | WF-REPLAY | an existing execution publication is reused after verifier drift; execution_count stays one | verifier drift with a prior execution publication | public entry on disposable copies | submitted claim | verifier drift replayed execution: execution_count incremented and a second execute event was appended | fail |
        | WF-DECISION | publication order is a legal prefix of execution, verification, decision, ledger | decision-only artifact | public entry on disposable copies | submitted claim | the decision-only artifact reached execution and writes instead of being rejected | fail |

        ## Findings

        - WF-F1 [suggested P1] coherent tampering reaches execution; broken invariant: only independently authorized prompt/model pairs may execute; sibling surface: any coherent prompt+model rewrite with matching manifest hashes; direction: verify against the independent authority, not the mutable manifest.
        - WF-F2 [suggested P1] verifier drift replays execution; broken invariant: an existing execution publication is reused, execution_count stays one; sibling surface: missing, duplicated, and drifted execution records; direction: reuse the publication instead of re-executing after drift.
        - WF-F3 [suggested P2] decision-only artifacts are not rejected; broken invariant: publication order is a legal prefix; sibling surface: any out-of-order publication set; direction: reject illegal publication prefixes before execution or writes.

        ## Aggregate-gate decision

        | Field | Value |
        |---|---|
        | Gate / exact command | `python -m unittest discover -s tests` |
        | Status | `not run` |
        | Owner and stage | `initial discovery` |
        | Reason | decisive targeted failures suppressed the aggregate |

        ## Discovery continuation

        ```markdown
        Discovery continuation:
        - Iteration / current byte identity: first discovery pass; HEAD {head}
        - Coverage rows: WF-TAMPER=fail; WF-REPLAY=fail; WF-DECISION=fail
        - Finding IDs: WF-F1, WF-F2, WF-F3
        - Reviewer regressions: tests.test_contract_probes.WorkflowContractProbe.test_wf_replay_reuses_execution_after_verifier_drift
        - Aggregate gate: not run after targeted failures; owner: initial discovery
        - Next: separate acceptance decision call
        ```
        """,
    )


def process_cleanup_defects_decision() -> None:
    process_cleanup_defects()
    discovery_report(
        "PROC-17",
        WORK / "process-runner",
        "complete",
        """
        ## Coverage ledger

        | Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
        |---|---|---|---|---|---|---|
        | PROC-RESIST | a descendant that ignores SIGTERM is killed after leader timeout | resistant descendant | real local process boundary with file events and bounded polling | submitted claim | the resistant descendant survived the leader termination and the cleanup probe failed; bounded cleanup confirmed the group afterwards | fail |
        | PROC-PIPE | an exited leader releases inherited output pipes | leader exits while a descendant holds inherited pipes | real local process boundary with bounded waits | submitted claim | inherited output pipes remained open after the leader exited; cleanup probe failed | fail |
        | PROC-RACE | descendant visibility is rechecked as the leader exits | transient leader/descendant visibility | real local process boundary with observable synchronization | submitted claim | a descendant appeared after the leader exit and was not reaped; cleanup probe failed | fail |

        ## Findings

        - PROC-F1 [suggested P1] resistant descendant survives timeout; broken invariant: timeout or leader exit must terminate and reap the whole process group and release inherited pipes; sibling surfaces: PROC-PIPE and PROC-RACE; direction: terminate the full process group on timeout and leader exit.
        - PROC-F2 [suggested P1] inherited pipes remain open after leader exit; broken invariant: same cleanup invariant; sibling surfaces: PROC-RESIST and PROC-RACE; direction: close and release inherited pipes for the whole group.
        - PROC-F3 [suggested P2] transient descendant visibility defeats cleanup; broken invariant: same cleanup invariant; sibling surfaces: PROC-RESIST and PROC-PIPE; direction: recheck descendants after leader exit and reap any late-visible child.

        ## Aggregate-gate decision

        | Field | Value |
        |---|---|
        | Gate / exact command | `python -m unittest discover -s tests` |
        | Status | `not run` |
        | Owner and stage | `initial discovery` |
        | Reason | decisive targeted process failures suppressed the aggregate |

        ## Discovery continuation

        ```markdown
        Discovery continuation:
        - Iteration / current byte identity: first discovery pass; HEAD {head}
        - Coverage rows: PROC-RESIST=fail; PROC-PIPE=fail; PROC-RACE=fail
        - Finding IDs: PROC-F1, PROC-F2, PROC-F3
        - Reviewer regressions: none
        - Aggregate gate: not run after targeted failures; owner: initial discovery
        - Next: separate acceptance decision call
        ```

        No fixture process survives discovery.
        """,
    )


SCENARIOS = {
    "queue-defect": queue_defect,
    "queue-defect-reproducer": queue_defect_reproducer,
    "exporter-accept": exporter_accept,
    "scheduler-inconclusive": scheduler_inconclusive,
    "exporter-restaged-stale": exporter_restaged_stale,
    "ledger-defects": ledger_defects,
    "authored-production-self-check": authored_production_self_check,
    "workflow-matrix-defects": workflow_matrix_defects,
    "process-cleanup-defects": process_cleanup_defects,
    "queue-defect-decision": queue_defect_decision,
    "queue-defect-reproducer-decision": queue_defect_reproducer_decision,
    "exporter-accept-decision": exporter_accept_decision,
    "scheduler-inconclusive-decision": scheduler_inconclusive_decision,
    "exporter-restaged-stale-decision": exporter_restaged_stale_decision,
    "ledger-defects-decision": ledger_defects_decision,
    "workflow-matrix-defects-decision": workflow_matrix_defects_decision,
    "process-cleanup-defects-decision": process_cleanup_defects_decision,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
RUNS.mkdir(parents=True, exist_ok=True)
SCENARIOS[sys.argv[1]]()
