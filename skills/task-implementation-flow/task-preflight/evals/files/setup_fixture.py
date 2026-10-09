#!/usr/bin/env python3
"""Create deterministic Git repositories and policy inputs for preflight evals."""

from pathlib import Path
import json
import hashlib
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


def commit(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture baseline"], check=True)


def common(root: Path, task_id: str) -> None:
    write(root, "AGENTS.md", "# Fixture rules\n\nPreflight may write only the canonical `docs/tasks/<TASK-ID>/preflight.md` packet. Preserve every other repository path.")
    write(root, ".runner/tracker.json", json.dumps({"complete": [task_id]}, indent=2))
    write(root, "pyproject.toml", "[project]\nname = \"eval-fixture\"\nversion = \"0.0.0\"\nrequires-python = \">=3.11\"")
    policy = RUNS / "policies/local-medium-v1.json"
    policy.parent.mkdir(parents=True, exist_ok=True)
    policy.write_text(json.dumps({
        "id": "local-medium-v1",
        "runtime_root": str(RUNS),
        "allow": ["cheap local tests", "canonical task-package preflight write"],
        "deny": ["network", "dependency installation", "commits", "other repository writes during preflight"],
    }, indent=2) + "\n", encoding="utf-8")


def queue_ready() -> None:
    root = WORK / "queue-runner"
    initialize(root)
    common(root, "QR-11")
    write(
        root,
        "docs/tasks/QR-12/brief.md",
        """
        # QR-12 — Repeated queue selection

        Artifact status: ready_for_preflight
        Authority: docs/plan.md#repeated-selection
        Dependency: QR-11 complete in .runner/tracker.json
        Allowed paths: src/queue/run_next.py; tests/integration/test_run_next.py
        AC-01: two public `runner run-next` invocations persist state and claim
        TASK-1 then TASK-2. Empty queues remain unchanged.
        Required helper: tests/helpers/queue_state.py::seed_queue
        Candidate targeted test: test_second_selection[queue with spaces [persisted]]
        Canonical command family: uv run pytest
        """,
    )
    write(
        root,
        "docs/tasks/QR-12/verification.md",
        """
        # Verification Design: QR-12 — Repeated queue selection

        Source brief: docs/tasks/QR-12/brief.md
        Verification revision: 1
        Status: ready

        ### V-01 — Consecutive public selections advance persisted state
        Covers: AC-01
        Oracle / boundary: invoke `runner run-next` twice and observe TASK-1 then
        TASK-2 plus persisted status at the real filesystem boundary.

        ### V-02 — Empty queue remains unchanged
        Covers: AC-01 negative behavior
        Oracle / boundary: compare state bytes before and after the public call.
        """,
    )
    write(root, "docs/plan.md", "# Plan\n\n## repeated-selection\nApprove persisted repeated queue selection through the public CLI.")
    write(
        root,
        "tests/helpers/queue_state.py",
        """
        import json

        def seed_queue(path):
            path.write_text(json.dumps({"tasks": [
                {"id": "TASK-1", "status": "ready"},
                {"id": "TASK-2", "status": "ready"},
            ]}))
        """,
    )
    write(
        root,
        "tests/integration/test_run_next.py",
        """
        import pytest
        from tests.helpers.queue_state import seed_queue

        @pytest.mark.parametrize("case", ["queue with spaces [persisted]"])
        def test_second_selection(tmp_path, case):
            state = tmp_path / "state.json"
            seed_queue(state)
            assert state.exists() and case.endswith("[persisted]")
        """,
    )
    write(root, "tests/__init__.py", "")
    write(root, "tests/helpers/__init__.py", "")
    write(root, "tests/integration/__init__.py", "")
    write(root, "src/queue/run_next.py", "def run_next(state_path):\n    raise NotImplementedError")
    write(root, "runner", """
        #!/usr/bin/env python3
        import sys
        from pathlib import Path
        from src.queue.run_next import run_next

        if sys.argv[1] != 'run-next':
            raise SystemExit('usage: runner run-next <state-path>')
        selected = run_next(Path(sys.argv[2]))
        if selected is not None:
            print(selected)
    """)
    (root / "runner").chmod(0o755)
    commit(root)


def scheduler_missing() -> None:
    root = WORK / "scheduler"
    initialize(root)
    common(root, "SCH-08")
    write(
        root,
        "docs/tasks/SCH-09/brief.md",
        """
        # SCH-09 — Exclusive claim

        Artifact status: ready_for_preflight
        Dependency: SCH-08 complete in .runner/tracker.json
        Allowed paths: src/scheduler/claim.py; tests/integration/test_claim.py
        AC-01: two simultaneous workers cannot claim the same ready job.
        Believed-existing required helper: tests/helpers/concurrent_claims.py
        The oracle must coordinate two real workers at a barrier.
        """,
    )
    write(root, "src/scheduler/claim.py", "def claim(job):\n    return job")
    write(root, "docs/tasks/SCH-09/verification.md", """
        Source brief: docs/tasks/SCH-09/brief.md
        Verification revision: 1
        V-01 / AC-01: coordinate two real workers at a barrier with
        tests/helpers/concurrent_claims.py; assert exactly one claim persists.
    """)
    write(root, "tests/test_claim_unit.py", "def test_placeholder():\n    assert True")
    commit(root)


def api_overlap() -> None:
    root = WORK / "api"
    initialize(root)
    common(root, "API-30")
    write(
        root,
        "docs/tasks/API-31/brief.md",
        """
        # API-31 — Session expiry

        Artifact status: ready_for_preflight
        Dependency: API-30 complete in .runner/tracker.json
        Allowed paths: src/auth/session.py; tests/auth/test_session.py
        AC-01: expired sessions are rejected without refreshing their token.
        Command: python -m unittest tests.auth.test_session
        """,
    )
    write(root, "src/auth/session.py", "def is_valid(session):\n    return True")
    write(root, "docs/tasks/API-31/verification.md", """
        Source brief: docs/tasks/API-31/brief.md
        Verification revision: 1
        V-01 / AC-01: call is_valid with expired session; assert rejection and
        unchanged token. Use the authorized tests/auth/test_session.py boundary.
    """)
    write(root, "tests/auth/test_session.py", "import unittest\n\nclass SessionTest(unittest.TestCase):\n    def test_valid(self):\n        self.assertTrue(True)")
    write(root, "tests/__init__.py", "")
    write(root, "tests/auth/__init__.py", "")
    commit(root)
    # Real MM state: staged user change, followed by different unstaged bytes.
    write(root, "src/auth/session.py", "def is_valid(session):\n    # staged user token-refresh work\n    return bool(session)")
    subprocess.run(["git", "-C", str(root), "add", "src/auth/session.py"], check=True)
    write(root, "src/auth/session.py", "def is_valid(session):\n    # unstaged continuation of user token-refresh work\n    return bool(session.get('token'))")


def queue_guided() -> None:
    queue_ready()
    root = WORK / "queue-runner"
    brief = root / "docs/tasks/QR-12/brief.md"
    brief.write_text(
        brief.read_text(encoding="utf-8").replace(
            "Artifact status: ready_for_preflight", "Artifact status: ready"
        ),
        encoding="utf-8",
    )
    subprocess.run(["git", "-C", str(root), "add", "docs/tasks/QR-12/brief.md"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "--amend", "-qm", "fixture baseline"], check=True)


def api_routine() -> None:
    root = WORK / "api-routine"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        "# Fixture rules\n\nPreflight may write only docs/tasks/API-07/preflight.md. Preserve every other path. Use the exact targeted unittest command in the task brief.",
    )
    write(
        root,
        "docs/tasks/API-07/brief.md",
        """
        # API-07 — Reject expired sessions

        Artifact status: ready
        Standalone readiness route: guided preflight to confirm the local test command.
        Allowed paths: src/auth/session.py; tests/auth/test_session.py
        Dependencies: complete; Python standard library only.
        AC-01: an unexpired session is valid when its expiry is later than the current time.
        Targeted command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.auth.test_session.SessionTest.test_unexpired_session_is_valid
        Oracle: the public `is_valid` result is true for expires_at=200 and now=100.
        """,
    )
    write(
        root,
        "src/auth/session.py",
        """
        def is_valid(session, now):
            return session["expires_at"] > now
        """,
    )
    write(
        root,
        "tests/auth/test_session.py",
        """
        import unittest

        from src.auth.session import is_valid


        class SessionTest(unittest.TestCase):
            def test_unexpired_session_is_valid(self):
                session = {"expires_at": 200}

                self.assertTrue(is_valid(session, now=100))
        """,
    )
    write(root, "tests/__init__.py", "")
    write(root, "tests/auth/__init__.py", "")
    write(root, "docs/tasks/API-07/verification.md", """
        Source brief: docs/tasks/API-07/brief.md
        Verification revision: 1
        V-01 / AC-01: use the brief's exact unittest command and public is_valid
        boundary; expires_at=200 and now=100 must return true.
    """)
    commit(root)


def readiness_base(name: str) -> Path:
    root = WORK / name
    initialize(root)
    write(root, "AGENTS.md", "Preflight may write only docs/tasks/*/preflight.md. Preserve other paths; no network, installation or commits.")
    write(root, "docs/direction.md", """
        # Approved direction, revision 1
        Internal offline session checker; Python standard library, local CLI.
        AC-01: expiry=200 at now=100 is valid. AC-02: expiry=100 at now=100
        is invalid and the input token is unchanged. Boundary: public is_valid.
        Consumer: local maintenance script; no external service or production data.
        Priority: preserve token state and deterministic local operation.
        Consequence: accepting an expired session gives an incorrect local result.
        Planned maintenance: the same expiry predicate will serve a second local script.
        Mitigation: explicit expiry boundary tests; unknown: date of second consumer.
        Delay of a critical security fix can expose privileged production access;
        approving a destructive migration without retention policy can require costly repair.
        For those two deployments the governing facts must be resolved before execution.
    """)
    write(root, "src/session.py", "def is_valid(session, now):\n    return session['expires_at'] > now")
    write(root, "tests/test_existing.py", """
        import unittest
        from src.session import is_valid

        class ExistingTest(unittest.TestCase):
            def test_unexpired(self):
                self.assertTrue(is_valid({'expires_at': 200}, 100))
    """)
    write(root, "tests/__init__.py", "")
    return root


def readiness_package(root: Path, task_id: str) -> None:
    write(root, f"docs/tasks/{task_id}/brief.md", """
        Status: ready
        Task kind: executable
        Brief revision: 1
        Authority: docs/direction.md, revision 1
        Allowed paths: src/session.py; tests/test_future.py
        Dependencies: Python standard library only.
        AC-01: unexpired session returns true.
        AC-02: expired session returns false without changing token.
        Planned command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_future
        Future tests/test_future.py is task-owned; absent before implementation.
        Available baseline: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_existing
    """)
    write(root, f"docs/tasks/{task_id}/verification.md", f"""
        Source brief: docs/tasks/{task_id}/brief.md
        Verification revision: 1
        Status: ready
        V-01 / AC-01: use public is_valid with expires_at=200, now=100; assert true.
        V-02 / AC-02: use expires_at=100, now=100, token='keep'; assert false
        and identical input bytes. Task-owned future test uses stdlib unittest;
        no external capability required. Setup: construct the stated dicts.
    """)


def readiness_cases() -> None:
    root = readiness_base("readiness-cases")
    cases = ("VALID", "MISSING", "FOREIGN", "OMITTED", "UNSUPPORTED", "WEAK",
             "CAPABILITY", "DEPENDENCY", "PERMISSION")
    for task_id in cases:
        readiness_package(root, task_id)
    (root / "docs/tasks/MISSING/verification.md").unlink()
    path = root / "docs/tasks/FOREIGN/verification.md"
    path.write_text(path.read_text().replace("tasks/FOREIGN/brief.md", "tasks/VALID/brief.md"))
    path = root / "docs/tasks/OMITTED/verification.md"
    path.write_text(path.read_text().split("V-02 / AC-02:")[0])
    write(root, "docs/tasks/UNSUPPORTED/extra-scenario.md", "V-03: require remote OAuth federation. No such requirement in the brief or direction.")
    path = root / "docs/tasks/UNSUPPORTED/verification.md"
    path.write_text(path.read_text() + "V-03: require remote OAuth federation (see extra-scenario.md).\n")
    write(root, "docs/tasks/WEAK/verification.md", """
        Source brief: docs/tasks/WEAK/brief.md
        Verification revision: 1
        V-01 / AC-01 and V-02 / AC-02: assert only that tests/test_future.py exists.
        This does not observe validity or token preservation.
    """)
    for task_id, fact in {
        "CAPABILITY": "Required indispensable oracle: tools/secure_clock.py from prerequisite owner; absent and outside allowed scope. No supported equivalent. Do not create it.",
        "DEPENDENCY": "Required dependency: approved enterprise time SDK, not installed; installation prohibited. Dependency owner must supply it.",
        "PERMISSION": "Required real boundary: production clock service; policy prohibits network. Permission owner must authorize access before fresh preflight.",
    }.items():
        for file_name in ("brief.md", "verification.md"):
            path = root / f"docs/tasks/{task_id}/{file_name}"
            path.write_text(path.read_text() + fact + "\n")
    write(root, "requests/direct.md", "Correct one heading in docs/direction.md. Keep all policy text unchanged. Small unpackaged direct request; inline readiness permitted.")
    commit(root)


def revision_recovery() -> None:
    root = readiness_base("revision-recovery")
    for task_id in ("FEASIBLE", "UNAVAILABLE"):
        readiness_package(root, task_id)
        package = root / f"docs/tasks/{task_id}"
        write(root, f"docs/tasks/{task_id}/verification-v1.md", (package / "verification.md").read_text())
        write(root, f"docs/tasks/{task_id}/preflight.md", f"""
            Status: ready
            Source brief: docs/tasks/{task_id}/brief.md
            Brief revision: 1; allowed scope: src/session.py; tests/test_future.py
            Verification revision: 1; V-01/V-02 feasible using stdlib unittest.
            Context: docs/direction.md. Future tests not run; baseline test passed.
            No ownership overlap; no network/installation needed.
        """)
    commit(root)
    for task_id in ("FEASIBLE", "UNAVAILABLE"):
        path = root / f"docs/tasks/{task_id}/verification.md"
        path.write_text(path.read_text().replace("Verification revision: 1", "Verification revision: 2") +
                        "Reason: omitted expiry=now+1 boundary is justified by AC-01; retain V-01/V-02.\n"
                        "V-03 / AC-01: expires_at=101, now=100 must return true.\n" +
                        ("Required indispensable tools/secure_clock.py unavailable, outside allowed scope; prerequisite owner must supply it.\n" if task_id == "UNAVAILABLE" else "Use existing public is_valid and stdlib unittest setup.\n"))
    for dimension, fact in {
        "expected-implementation": "Task-owned src/session.py predicate and tests/test_future.py change within scope; authority and capabilities unchanged.",
        "expected-report": "Only task implementation result text added; authority and capabilities unchanged.",
        "authority": "docs/direction.md revision 2 supersedes cited operating envelope; reassess exposure.",
        "prerequisite": "Approved prerequisite SDK removed; previously feasible proof cannot execute.",
        "ownership": "User now owns inseparable changes on src/session.py; no merge permission.",
        "permission": "Owner revoked required local clock process execution; previously permitted proof is prohibited.",
        "capability": "Required supported clock helper removed; no equivalent is available.",
        "requirement": "Proposed AC-03 adds retention export; not approved in current authority. Return to task design.",
    }.items():
        # Each alternative has a real Git before/after boundary, not merely a claim.
        state = readiness_base(f"revision-recovery/transitions/{dimension}")
        readiness_package(state, "CURRENT")
        write(state, "tools/secure_clock.py", "def now():\n    return 100\n\nif __name__ == '__main__':\n    print(now())")
        write(state, "vendor/time_sdk.py", "def now():\n    return 100")
        write(state, "policy.md", "Permission: required local clock process execution allowed; no network or installation.")
        for artifact in ("brief.md", "verification.md"):
            path = state / f"docs/tasks/CURRENT/{artifact}"
            path.write_text(path.read_text() +
                            "Required approved prerequisites: vendor/time_sdk.py::now and tools/secure_clock.py local process.\n"
                            "Clock command: PYTHONDONTWRITEBYTECODE=1 python3 tools/secure_clock.py; oracle stdout 100.\n"
                            "Permission authority: policy.md. Replacements outside task scope belong to prerequisite owner.\n")
        write(state, "docs/tasks/CURRENT/preflight.md", """
            Status: ready
            Source brief: docs/tasks/CURRENT/brief.md
            Brief revision: 1; Verification revision: 1
            Scope: src/session.py; tests/test_future.py
            Authority: docs/direction.md revision 1; context: local offline use.
            Prerequisite: vendor/time_sdk.py exists; capability: tools/secure_clock.py exists.
            Ownership: clean, no user overlap; permission: policy.md allows local clock process execution.
            Planned stdlib tests feasible, not run. Reassess affected changed facts only.
        """)
        commit(state)
        if dimension == "expected-implementation":
            write(state, "src/session.py", "# Task-owned in-scope implementation effect\ndef is_valid(session, now):\n    return session['expires_at'] > now")
        elif dimension == "expected-report":
            write(state, "docs/tasks/CURRENT/result.md", "Task-owned implementation report; no authority change.")
        elif dimension == "authority":
            path = state / "docs/direction.md"
            path.write_text(path.read_text().replace("revision 1", "revision 2") + "Operating envelope now includes production use; reassess consequences.\n")
        elif dimension == "prerequisite":
            (state / "vendor/time_sdk.py").unlink()
        elif dimension == "ownership":
            write(state, "src/session.py", "# Staged user edit\ndef is_valid(session, now):\n    return True")
            subprocess.run(["git", "-C", str(state), "add", "src/session.py"], check=True)
            write(state, "src/session.py", "# Unstaged user continuation\ndef is_valid(session, now):\n    return False")
        elif dimension == "permission":
            write(state, "policy.md", "Permission: required local clock process execution revoked. Permission owner must authorize before execution.")
        elif dimension == "capability":
            (state / "tools/secure_clock.py").unlink()
        elif dimension == "requirement":
            path = state / "docs/tasks/CURRENT/brief.md"
            path.write_text(path.read_text() + "Proposed AC-03: retention export. Not approved by docs/direction.md; return to task design.\n")
        write(root, f"transitions/{dimension}.md", f"Before: {dimension}/docs/tasks/CURRENT/preflight.md and Git HEAD.\nAfter: {fact}\nInspect the real changed state in transitions/{dimension}; preserve it.")


def readiness_context() -> None:
    root = readiness_base("readiness-context")
    variants = {
        "RELEVANT": "Recorded issue KI-01: exact expiry boundary was omitted; impacts this task's session consumer. Existing AC-02 remains binding; planned boundary proof mitigates it.",
        "UNRELATED": "Recorded issue KI-02: static report footer alignment; no session consumer, state or proof impact. Do not broaden discovery.",
        "NONE": "No recorded known-issues file. Ordinary unknown: second consumer's release date; assume current local envelope.",
        "ORDINARY": "Unknown business detail: second script's schedule. Continue under local-use assumption without weakening AC-01/02.",
        "DELAY-RESOLVED": "Potential privileged-access exposure from delayed fix. Authority resolves exposure: internal offline fixture, no production users or privileged data; continue current scope.",
        "DELAY-UNRESOLVED": "Deployment may be the privileged production service; delay could leave expired privileged sessions active. Authority does not identify deployment. Decision owner must answer: is this deployed to that service?",
        "REPAIR-RESOLVED": "Potential costly retention repair. Authority resolves it: this task writes no persistent data and is not a migration; continue current scope.",
        "REPAIR-UNRESOLVED": "Consumer may irreversibly replace retained production tokens; later repair could require restoring a full archive. Retention policy is not supplied. Decision owner must identify whether replacement is permitted before execution.",
    }
    for task_id, context in variants.items():
        readiness_package(root, task_id)
        write(root, f"docs/tasks/{task_id}/context.md", f"Direction: docs/direction.md\n{context}\nAll AC and proof obligations remain binding; do not invent missing business policy.")
        if task_id in {"RELEVANT", "UNRELATED"}:
            write(root, f"docs/tasks/{task_id}/known-issues.md", context)
        if task_id in {"DELAY-UNRESOLVED", "REPAIR-UNRESOLVED"}:
            package = root / f"docs/tasks/{task_id}"
            brief = package / "brief.md"
            brief.write_text(brief.read_text().replace(
                "Authority: docs/direction.md, revision 1",
                "Authority: context.md, deployment decision; docs/direction.md for AC-01/02 only"))
            path = package / "context.md"
            path.write_text(path.read_text() +
                            "Authority: local fixture operation is approved; deployment envelope is not established.\n"
                            "The local-use assumptions in docs/direction.md cannot settle this consumer's deployment decision.\n")
    commit(root)


def freshness_change() -> None:
    api_overlap()
    root = WORK / "api"
    path = "src/auth/session.py"
    baseline = {
        "status": subprocess.check_output(["git", "-C", str(root), "status", "--short"], text=True),
        "index_sha256": hashlib.sha256(subprocess.check_output(["git", "-C", str(root), "show", f":{path}"])).hexdigest(),
        "worktree_sha256": hashlib.sha256((root / path).read_bytes()).hexdigest(),
    }
    write(RUNS, "freshness-baseline.json", json.dumps(baseline, indent=2))
    write(root, path, "def is_valid(session):\n    # later user work, same MM status\n    return False")


SCENARIOS = {
    "readiness-cases": readiness_cases,
    "revision-recovery": revision_recovery,
    "readiness-context": readiness_context,
    "freshness-change": freshness_change,
    "api-routine": api_routine,
    "queue-ready": queue_ready,
    "queue-guided": queue_guided,
    "scheduler-missing": scheduler_missing,
    "api-overlap": api_overlap,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
RUNS.mkdir(parents=True, exist_ok=True)
SCENARIOS[sys.argv[1]]()
