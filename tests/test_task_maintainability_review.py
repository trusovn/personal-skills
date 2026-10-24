"""Focused checks for the task-maintainability-review contract and fixture.

Contract checks reject the historical three-blocker cap and the
enough-blockers stop semantically and lock the preserved scope, materiality,
genuine-stop, gate, and eval expectations. Fixture checks stage the
skill-local setup in a disposable Git workspace and observe four
independently introduced production blockers plus tests-only defect, control
and correction contrasts at real filesystem, Git and scenario boundaries.
"""

import ast
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import hashlib
import unittest
from pathlib import Path

from review_fixture_support import FLOW, ROOT

PACKAGE = FLOW / "task-maintainability-review"
SKILL = PACKAGE / "SKILL.md"
EVALS = PACKAGE / "evals" / "evals.json"
FIXTURE = PACKAGE / "evals" / "files" / "setup_fixture.py"


def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).strip()


def collapse(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


COUNT_AND_SUFFICIENCY_SHORTCUTS = (
    re.compile(
        r"(?:at most|no more than|maximum of)\s*[`*]*\d+[`*]*\s*blockers?",
        re.IGNORECASE,
    ),
    re.compile(r"do not (?:keep|continue) (?:searching|search)", re.IGNORECASE),
    re.compile(r"enough(?: decisive)? blockers", re.IGNORECASE),
)


class MaintainabilityReportingContractTest(unittest.TestCase):

    def test_significant_test_assets_extend_the_existing_review_questions(self):
        text = normalized(SKILL)
        scope = text.split("## Review contract", 1)[1].split("## Independence", 1)[0]
        for required in (
            "tests, evaluations, fixture/setup code and harness code",
            "ownership", "dependencies", "scenario authority", "isolation",
            "oracle structure", "harness behavior",
            "ordinary assertion edit alone does not require this review",
            "../../testing-discipline/SKILL.md",
        ):
            self.assertIn(required, scope)
        for question in (
            "**Cohesion**", "**Coupling**", "**Explicit dependencies**",
            "**Change locality**", "**Testability**", "**Proportionate abstraction**",
        ):
            self.assertIn(question, scope)
        for defect in (
            "duplicated scenario authority", "fragile mutable fixtures",
            "cross-owner coupling", "incidental text/layout assertions",
            "harness-internal dependencies", "speculative abstraction",
            "Stable textual contracts remain legitimate",
            "legitimate separate observation boundaries",
        ):
            self.assertIn(defect, text)

    def test_provenance_and_freshness_follow_reviewed_test_assets(self):
        text = normalized(SKILL)
        independence = text.split("## Independence", 1)[1].split("## Inputs", 1)[0]
        self.assertIn("any reviewed implementation assets", independence)
        self.assertIn("including test/eval/harness bytes", independence)
        self.assertNotIn("author the production bytes", independence)
        self.assertIn("A correction, including a tests-only correction", independence)
        self.assertIn("changed implementation scope", text)
        loop = text.split("## Correction loop", 1)[1]
        self.assertIn("A tests-only label alone never waives an affected required review", loop)
        self.assertIn("Do not invent a gate or registry work for every test change", loop)

    def test_every_confirmed_blocker_is_reported_without_a_count_cap(self):
        text = normalized(SKILL)
        for pattern in COUNT_AND_SUFFICIENCY_SHORTCUTS:
            self.assertIsNone(pattern.search(text), pattern.pattern)
        self.assertIn(
            "Report **every confirmed blocker** found within the bounded "
            "review scope, ordered by architectural impact",
            text,
        )
        self.assertIn(
            "Finding count or verdict sufficiency cannot end discovery, cap "
            "the output, or relegate a confirmed blocker to warnings",
            text,
        )
        self.assertIn(
            "Completeness does not authorize a wider survey or a quota of findings",
            text,
        )
        for field in (
            "file/location or concrete dependency edge",
            "the exact introduced/worsened problem",
            "evidence",
            "maintainability consequence",
            "smallest reasonable correction direction",
        ):
            self.assertIn(field, text)
        self.assertIn("one numbered entry per confirmed blocker", text)
        self.assertIn(
            "Every confirmed concrete blocker in the reviewed scope is "
            "reported; count is neither a limit nor a quota",
            text,
        )

    def test_genuine_stops_retain_outstanding_coverage(self):
        text = normalized(SKILL)
        self.assertIn(
            "A specific permission, capability, or safe-budget limit — never "
            "finding count or verdict sufficiency — is the only reason to stop "
            "before the bounded review scope is complete",
            text,
        )
        self.assertIn("retain every confirmed finding with its full evidence", text)
        self.assertIn(
            "name the outstanding coverage, the concrete stop reason, and the next owner",
            text,
        )
        self.assertIn(
            "cannot become `ACCEPT` or a claim of cleanly completed review",
            text,
        )

    def test_scope_materiality_and_safeguards_are_preserved(self):
        text = normalized(SKILL)
        for preserved in (
            "Do **not** begin with a repo-wide architecture survey",
            "introduced or materially worsened",
            "If not, keep it in `WARNINGS` or omit it",
            "new/worsened HARD violation",
            "unchanged baselined legacy violation",
            "WARNING / heuristic signal",
            "gate passes",
            "Do not edit architecture config, exceptions, or baselines to make review pass",
            "Reviewing the whole repository instead of the current change",
            "Blocking on pre-existing untouched debt",
            "Padding the blocker list with low-value nits",
            "reviews/maintainability-NN.md",
        ):
            self.assertIn(preserved, text)

    def test_existing_evals_retain_distinct_setup_facts_and_expectations(self):
        cases = {
            case["id"]: case
            for case in json.loads(EVALS.read_text(encoding="utf-8"))["evals"]
        }
        self.assertEqual(list(range(1, 11)), sorted(cases))
        self.assertIn("wrote the current production bytes", cases[1]["prompt"])
        first = " ".join(cases[1]["expectations"])
        self.assertIn("SELF_CHECK_ONLY", first)
        self.assertIn(
            "fresh independent `task-maintainability-review` session", first
        )
        self.assertIn("test, eval and harness bytes", cases[1]["prompt"])
        self.assertIn("tests-only correction", cases[2]["prompt"])
        self.assertIn("`archcheck` binary is absent", cases[2]["prompt"])
        second = " ".join(cases[2]["expectations"])
        self.assertIn("VERDICT: INCONCLUSIVE", second)
        self.assertIn("ARCHITECTURE_GATE: NOT_AVAILABLE", second)
        self.assertIn("/work/task-runs/PAY-14/maintainability.md", cases[3]["prompt"])
        third = " ".join(cases[3]["expectations"])
        self.assertIn("docs/tasks/PAY-14/reviews/maintainability-01.md", third)
        self.assertIn("does not overwrite prior reports", third)
        self.assertIn(
            "docs/tasks/MNT-42/reviews/maintainability-01.md", cases[4]["prompt"]
        )
        fourth = " ".join(cases[4]["expectations"])
        self.assertIn("MNT-B1, MNT-B3, and MNT-B4 keep their unchanged IDs", fourth)
        self.assertIn(
            "MNT-B2 keeps its ID with its current corrected disposition", fourth
        )
        self.assertIn("not recycled", fourth)
        self.assertIn("reviews/maintainability-02.md", fourth)
        self.assertIn("does not rewrite the prior report", fourth)
        for case_id, scenario in ((5, "test-assets"), (6, "test-assets-control"),
                                  (7, "test-assets-correction"), (8, "test-assets-stop")):
            self.assertIn(f"setup_fixture.py {scenario}", cases[case_id]["prompt"])
            self.assertIn("before the reviewer session", cases[case_id]["prompt"])
            self.assertIn("held back", cases[case_id]["prompt"])
        self.assertIn("tests-only submission", cases[1]["prompt"])
        for case_id in cases:
            self.assertEqual([], cases[case_id]["files"])


class MaintainabilityIntegrationGapContractTest(unittest.TestCase):
    """INT-FLOW-001 focused checks for I-01, I-02, and I-03.

    These assertions reject the direct maintainability-to-discovery shortcut
    that drops applicable registry work, blanket verdict invalidation after
    any production correction, and display-order-only blocker identities.
    They fail against the pre-correction skill bytes.
    """

    def test_clean_review_hands_off_the_complete_conditional_route(self):
        text = normalized(SKILL)
        loop = text.split("## Correction loop", 1)[1].split(
            "## Definition of Done", 1
        )[0]
        self.assertIn(
            "only after `ACCEPT`, name the first outstanding stage and the "
            "complete ordered remainder of the submission route: applicable "
            "`task-contract-registry-updater` synchronization when the flow "
            "includes a registry stage and the change added, changed, or "
            "removed a durable cross-task contract, then fresh independent "
            "`task-review-discovery` evidence, then the separate functional "
            "`task-acceptance-review` decision when that stage is required",
            loop,
        )
        self.assertLess(
            loop.index("`task-contract-registry-updater`"),
            loop.index("`task-review-discovery`"),
        )
        self.assertIn(
            "Naming the route hands off the next owners without executing "
            "any named stage",
            loop,
        )
        self.assertIn(
            "current applicable evidence for a completed stage leaves it out "
            "of the outstanding remainder",
            loop,
        )
        self.assertIn("applicable registry work cannot be dropped", loop)
        self.assertIn("an absent registry stage cannot be invented", loop)
        self.assertNotIn(
            "only after `ACCEPT`, proceed to fresh independent "
            "`task-review-discovery`",
            loop,
        )
        self.assertIn(
            "re-enter only the conditional stages whose reviewed scope the "
            "correction affected",
            loop,
        )

    def test_correction_reentry_follows_affected_scope_and_current_evidence(self):
        text = normalized(SKILL)
        self.assertNotIn(
            "Every production correction invalidates the previous "
            "maintainability verdict",
            text,
        )
        independence = text.split("## Independence", 1)[1].split("## Inputs", 1)[0]
        self.assertIn(
            "Re-entry follows actual affected reviewed scope and current evidence",
            independence,
        )
        self.assertIn("invalidates this verdict for the corrected bytes", independence)
        self.assertIn(
            "demonstrably unaffected scope retains this review as current evidence",
            independence,
        )
        self.assertIn(
            "Stale, missing, or inapplicable proof never counts as a completed "
            "stage",
            independence,
        )
        self.assertIn(
            "a prior verdict's label alone is not current evidence", independence
        )
        guide = normalized(FLOW / "README.md")
        self.assertIn(
            "For a trivial correction that provably cannot affect reviewed implementation "
            "architecture",
            guide,
        )
        self.assertIn("Route by actual effects and current proof", guide)

    def test_findings_have_stable_ids_with_correction_continuity(self):
        text = normalized(SKILL)
        self.assertIn(
            "Give every confirmed finding a **stable finding ID** such as "
            "`MNT-01`",
            text,
        )
        self.assertIn("independent of display order", text)
        self.assertIn("Identity is a producer obligation, not a fixture convention", text)
        self.assertIn("prior reports remain unchanged", text)
        self.assertIn("a resolved ID is never recycled", text)
        self.assertIn(
            "an identity no earlier report or resolved finding already used", text
        )
        self.assertIn(
            "keeps the surviving findings' IDs and the corrected finding's ID "
            "with its current disposition and evidence",
            text,
        )
        self.assertIn("1. MNT-01 — <file/location>", text)
        self.assertIn(
            "Current disposition: <confirmed, or resolved/corrected with "
            "current evidence>",
            text,
        )
        self.assertIn("- <MNT-NN finding or NONE>", text)
        self.assertIn(
            "retain every confirmed finding with its full evidence, its stable "
            "ID, and its current disposition",
            text,
        )
        self.assertIn("one numbered entry per confirmed blocker", text)


class MaintainabilityFixtureTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.work = Path(tempfile.mkdtemp(prefix="maintainability-fixture-"))
        cls.addClassCleanup(shutil.rmtree, cls.work, ignore_errors=True)
        environment = os.environ | {"EVAL_WORK_ROOT": str(cls.work)}
        for scenario in (
            "four-blockers", "genuine-stop", "correction-round", "test-assets",
            "test-assets-control", "test-assets-correction", "test-assets-stop",
            "semantic-defects", "semantic-control",
        ):
            subprocess.run(
                [sys.executable, str(FIXTURE), scenario],
                check=True,
                cwd=ROOT,
                env=environment,
            )
        cls.repo = cls.work / "maintainability"
        cls.stop_repo = cls.work / "maintainability-stop"
        cls.correction_repo = cls.work / "maintainability-correction"
        cls.run_dir = cls.work / "task-runs" / "MNT-42"

    def test_semantic_variants_have_runnable_baselines_and_green_current_behavior(self):
        for variant in ("defects", "control"):
            repo = self.work / f"maintainability-semantics-{variant}"
            baseline = Path(tempfile.mkdtemp(dir=self.work))
            for relative in self.git(repo, "ls-files").splitlines():
                path = baseline / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(self.git(repo, "show", f"HEAD:{relative}"))
            for target in (baseline, repo):
                with self.subTest(variant=variant, target=target):
                    suite = subprocess.run(
                        [sys.executable, "-B", "-m", "unittest", "tests.test_controller"],
                        cwd=target, capture_output=True, text=True,
                    )
                    self.assertEqual(0, suite.returncode, suite.stderr)
                    gate = subprocess.run(
                        [sys.executable, "-B", "scripts/check-architecture"],
                        cwd=target, capture_output=True, text=True,
                    )
                    self.assertEqual(0, gate.returncode, gate.stderr)
            self.assertEqual(["src/controller.py", "tests/test_controller.py"],
                             self.git(repo, "diff", "--name-only").splitlines())

    def test_semantic_oracles_distinguish_contract_traps_and_valid_complexity(self):
        for variant in ("defects", "control"):
            repo = self.work / f"maintainability-semantics-{variant}"
            with self.subTest(variant=variant):
                result, _ = self.probe(repo, '''
import inspect, json
from src import controller, state as rules
from tests.test_controller import new_state

state = new_state()
query = getattr(controller, "_is_ready", rules.eligible)
if "_is_ready" in vars(controller):
    query(state, 1000, 5000)
else:
    query(state)
print(json.dumps([state["phase"], state["attempts"], state["expires"]]))
print(list(inspect.signature(controller.heartbeat).parameters)[-1])

# A future evidence kind extends the existing owner, not its callers.
previous = rules.invalidate_evidence
def extended(state):
    previous(state)
    state["receipt"] = None
rules.invalidate_evidence = extended
for command in (controller.revise_inputs, controller.recover):
    state = new_state() | {"receipt": "old-inputs"}
    command(state)
    print(json.dumps(state["receipt"]))

for error in (OSError("queue unavailable"), ValueError("receipt invalid")):
    def fail(operation_id):
        raise error
    print(json.dumps(controller.complete(new_state(), fail), sort_keys=True))
''')
                self.assertEqual(0, result.returncode, result.stderr)
                lines = result.stdout.splitlines()
                self.assertEqual(["running", 1, 6000] if variant == "defects"
                                 else ["ready", 0, 0], json.loads(lines[0]))
                self.assertEqual("lease_seconds" if variant == "defects" else "ttl_ms",
                                 lines[1])
                self.assertEqual(["old-inputs", "old-inputs"] if variant == "defects"
                                 else [None, None], [json.loads(line) for line in lines[2:4]])
                failures = [json.loads(line) for line in lines[4:]]
                if variant == "defects":
                    self.assertEqual([{"status": "failed"}] * 2, failures)
                else:
                    self.assertEqual(["queue unavailable", "receipt invalid"],
                                     [item["detail"] for item in failures])
                    self.assertTrue(all(item["operation_id"] == "job-7" for item in failures))

    def test_semantic_eval_execution_stages_real_reviewer_inputs(self):
        # Use the existing runner's planner, without launching model calls.
        import importlib.util
        runner_path = ROOT / "skills/skill-creator/scripts/run_behavior_evals.py"
        spec = importlib.util.spec_from_file_location("behavior_runner", runner_path)
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        for case in runner.load_evals(PACKAGE):
            if case["id"] < 9:
                continue
            run = Path(tempfile.mkdtemp(dir=self.work)).resolve()
            command, cwd, env, workspace = runner.execution_plan(case, PACKAGE, run)
            setup = subprocess.run(command, cwd=cwd, env=os.environ | env,
                                   capture_output=True, text=True)
            self.assertEqual(0, setup.returncode, setup.stderr)
            self.assertTrue((workspace / "docs/tasks/MNT-42/brief.md").is_file())
            self.assertTrue(self.git(workspace, "diff", "--name-only").strip())
            self.assertFalse((workspace / "task-runs").exists())

    def test_test_assets_supply_green_tests_only_diffs_and_policy(self):
        for variant in ("defects", "control", "correction", "stop"):
            with self.subTest(variant=variant):
                repo = self.work / f"maintainability-tests-{variant}"
                changed = self.git(repo, "diff", "--name-only").splitlines()
                self.assertTrue(changed)
                self.assertTrue(all(path.startswith("tests/") for path in changed))
                brief = (repo / "docs/tasks/MNT-42/brief.md").read_text()
                self.assertIn("tests/scenarios.py owns", brief)
                self.assertIn("Each occurrence receives independent mutable state", brief)
                self.assertIn("assertion clarification alone is exempt", brief)
                self.assertIn("No contract registry stage", brief)
                completed, _ = self.probe(repo,
                    'import unittest\n'
                    'suite = unittest.defaultTestLoader.discover(' + repr(str(repo / "tests")) +
                    ', top_level_dir=' + repr(str(repo)) + ')\n'
                    'result = unittest.TextTestRunner().run(suite)\n'
                    'raise SystemExit(not result.wasSuccessful())\n')
                self.assertEqual(0, completed.returncode, completed.stderr)
                registry = (repo / ".quality/gates.yaml").read_text()
                command = next(line.split("command:", 1)[1].strip()
                               for line in registry.splitlines() if "command:" in line)
                if variant == "stop":
                    with self.assertRaises(FileNotFoundError):
                        subprocess.run(shlex.split(command), cwd=repo, capture_output=True)
                else:
                    gate = subprocess.run(shlex.split(command), cwd=repo, capture_output=True)
                    self.assertEqual(0, gate.returncode, gate.stderr)

    def test_one_owner_divergence_and_repeatability_reject_changed_fixture(self):
        repo = self.work / "maintainability-tests-defects"
        baseline = Path(tempfile.mkdtemp(dir=self.work))
        for relative in self.git(repo, "ls-files").splitlines():
            path = baseline / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.git(repo, "show", f"HEAD:{relative}"))
        cases = ((baseline, False, True), (repo, True, False),
                 (self.work / "maintainability-tests-control", False, True),
                 (self.work / "maintainability-tests-correction", True, True))
        for target, diverges, repeatable in cases:
            with self.subTest(target=target):
                divergence, _ = self.probe(target,
                    'from tests import scenarios, test_receipt_contract, test_transport\n'
                    'scenarios.STANDARD.update(subtotal=200, expected="total 204.00")\n'
                    'print(test_receipt_contract.observe())\n'
                    'print(test_transport.observe())\n')
                self.assertEqual(0, divergence.returncode, divergence.stderr)
                owner, second = divergence.stdout.splitlines()
                self.assertEqual("(200, 'total 204.00')", owner)
                self.assertEqual(diverges, owner != second)
                repeated, _ = self.probe(target,
                    'import unittest\n'
                    'from tests.test_receipt_contract import ReceiptContractTest\n'
                    'for occurrence in range(2):\n'
                    '    result = unittest.TestResult()\n'
                    '    ReceiptContractTest("test_receipt").run(result)\n'
                    '    print(result.wasSuccessful())\n'
                    '    for _, error in result.errors:\n'
                    '        print(error)\n')
                self.assertEqual(0, repeated.returncode, repeated.stderr)
                self.assertEqual("True", repeated.stdout.splitlines()[0])
                self.assertEqual(str(repeatable), repeated.stdout.splitlines()[1])
                self.assertEqual(not repeatable, "KeyError" in repeated.stdout)

    def test_test_only_correction_stales_affected_identity_and_preserves_history(self):
        before = self.work / "maintainability-tests-defects"
        after = self.work / "maintainability-tests-correction"
        prior_path = after / "docs/tasks/MNT-42/reviews/maintainability-01.md"
        prior = prior_path.read_bytes()
        for relative, changed in (("tests/scenarios.py", True),
                                  ("tests/test_transport.py", False)):
            old = hashlib.sha256((before / relative).read_bytes()).hexdigest()
            current = hashlib.sha256((after / relative).read_bytes()).hexdigest()
            self.assertIn(f"{relative}: sha256:{old}", prior.decode())
            self.assertEqual(changed, old != current)
        self.assertIn("MNT-T1", prior.decode())
        self.assertIn("MNT-T2", prior.decode())
        probe, _ = self.probe(after,
            'from tests.test_receipt_contract import ReceiptContractTest\n'
            'ReceiptContractTest("test_receipt").test_receipt()\n'
            'ReceiptContractTest("test_receipt").test_receipt()\n')
        self.assertEqual(0, probe.returncode, probe.stderr)
        self.assertEqual(prior, prior_path.read_bytes())
        oracle = (self.run_dir / "test-assets-correction-oracle.md").read_text()
        for fact in ("MNT-T1 as confirmed", "MNT-T2 as corrected", "do not recycle IDs",
                     "maintainability-02.md", "Current applicable unaffected evidence"):
            self.assertIn(fact, collapse(oracle))

    @classmethod
    def git(cls, repo, *args):
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            text=True,
            capture_output=True,
        ).stdout

    @classmethod
    def probe(cls, repo, code):
        directory = Path(tempfile.mkdtemp(dir=cls.work))
        completed = subprocess.run(
            [sys.executable, "-c", code],
            cwd=directory,
            capture_output=True,
            text=True,
            env=os.environ | {"PYTHONPATH": str(repo)},
        )
        return completed, directory

    def changed_source(self, relative):
        return (self.repo / relative).read_text(encoding="utf-8")

    def baseline_source(self, relative):
        return self.git(self.repo, "show", f"HEAD:{relative}")

    def test_stage_supplies_legitimate_task_baseline_and_changed_diff(self):
        brief = collapse(
            (self.repo / "docs/tasks/MNT-42/brief.md").read_text(encoding="utf-8")
        )
        self.assertIn("Status: ready", brief)
        self.assertIn("AC-01", brief)
        self.assertIn("AC-02", brief)
        self.assertIn("single source of truth", brief)
        rules = collapse((self.repo / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("required before a verdict", rules)
        status = self.git(self.repo, "status", "--short")
        for relative in (
            "src/billing/pricing.py",
            "src/billing/receipts.py",
            "src/billing/service.py",
            "tests/test_billing.py",
        ):
            self.assertIn(relative, status)
            self.assertTrue(self.baseline_source(relative).strip())
        diff = self.git(self.repo, "diff")
        for marker in ("LATE_RATES", "SqliteStore", "datetime", '("card", "wire")'):
            self.assertIn(marker, diff)

    def test_b1_duplicated_rate_policy_diverges_under_one_policy_edit(self):
        completed, _ = self.probe(
            self.repo,
            'from src.billing import pricing, service\n'
            'pricing.SURCHARGE_RATES["standard"] = 0.99\n'
            'print(pricing.surcharge(100, 10))\n'
            'print(service.checkout(100, 10, "card"))\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        owner, copy_total = completed.stdout.splitlines()
        self.assertEqual("99.0", owner)
        self.assertIn("103.50", copy_total)
        changed = self.changed_source("src/billing/service.py")
        self.assertIn("LATE_RATES", changed)
        self.assertNotIn("pricing.surcharge", changed)
        self.assertNotIn("LATE_RATES", self.baseline_source("src/billing/service.py"))

    def test_b2_domain_policy_depends_on_concrete_sqlite_state(self):
        completed, directory = self.probe(
            self.repo,
            'from src.billing import pricing\n'
            'print(pricing.fee(100))\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("2.0", completed.stdout.strip())
        self.assertTrue((directory / "billing.db").exists())
        seeded, _ = self.probe(
            self.repo,
            'import sqlite3\n'
            'from src.billing import pricing\n'
            'connection = sqlite3.connect("billing.db")\n'
            'connection.execute("create table rates (name text, value real)")\n'
            "connection.execute(\"insert into rates values ('late:standard', 0.99)\")\n"
            'connection.commit()\n'
            'print(pricing.surcharge(100, 10))\n',
        )
        self.assertEqual(0, seeded.returncode, seeded.stderr)
        self.assertEqual("99.0", seeded.stdout.strip())
        changed = self.changed_source("src/billing/pricing.py")
        self.assertIn('"standard": 0.015', changed)
        self.assertIn("from src.billing.store import SqliteStore", changed)
        self.assertIn("store.connection.execute", changed)
        self.assertNotIn("import", self.baseline_source("src/billing/pricing.py"))
        self.assertNotIn(
            "src/billing/store.py", self.git(self.repo, "status", "--short")
        )

    def test_b3_receipt_rendering_lost_its_deterministic_seam(self):
        completed, _ = self.probe(
            self.repo,
            'import inspect\n'
            'from src.billing import receipts\n'
            'first = receipts.render(50, "card")\n'
            'second = receipts.render(50, "card")\n'
            'print(first == second)\n'
            'print(list(inspect.signature(receipts.render).parameters))\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        deterministic, parameters = completed.stdout.splitlines()
        self.assertEqual("False", deterministic)
        self.assertEqual("['total', 'kind']", parameters)
        changed = self.changed_source("src/billing/receipts.py")
        self.assertIn("datetime.datetime.now()", changed)
        self.assertNotIn("import datetime", self.baseline_source("src/billing/receipts.py"))

    def test_b4_kind_dispatch_is_duplicated_and_already_disagrees(self):
        completed, _ = self.probe(
            self.repo,
            'from src.billing import receipts, service\n'
            'print(receipts.render(50, "check"))\n'
            'try:\n'
            '    service.checkout(100, 0, "check")\n'
            'except ValueError:\n'
            '    print("raised")\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        receipt, outcome = completed.stdout.splitlines()
        self.assertIn("card total 50.00", receipt)
        self.assertEqual("raised", outcome)
        self.assertIn('("card", "wire")', self.changed_source("src/billing/service.py"))
        self.assertIn('elif kind == "wire":', self.changed_source("src/billing/receipts.py"))
        self.assertNotIn("wire", self.baseline_source("src/billing/service.py"))
        self.assertNotIn("wire", self.baseline_source("src/billing/receipts.py"))

    def test_preference_control_is_explicitly_non_material(self):
        completed, _ = self.probe(
            self.repo,
            'from src.billing import service\n'
            'print(service.describe(10))\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("subtotal 10.00", completed.stdout.strip())
        diff = self.git(self.repo, "diff")
        self.assertIn('-    return "subtotal " + format(subtotal, ".2f")', diff)
        self.assertIn('+    return f"subtotal {subtotal:.2f}"', diff)
        imports_of = lambda source: {
            node.module
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.ImportFrom) and node.module
        }
        self.assertEqual(
            imports_of(self.baseline_source("src/billing/service.py")),
            imports_of(self.changed_source("src/billing/service.py")),
        )

    def test_changed_bytes_are_runnable_and_functionally_green(self):
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "tests.test_billing"],
            cwd=self.repo,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)

    def test_oracle_manifest_supplies_independent_defect_oracles(self):
        oracle = collapse(
            (self.run_dir / "maintainability-oracle.md").read_text(encoding="utf-8")
        )
        blockers = ("MNT-B1", "MNT-B2", "MNT-B3", "MNT-B4")
        for blocker in blockers:
            self.assertIn(f"### {blocker}", oracle)
        for blocker in blockers:
            section = oracle.split(f"### {blocker}", 1)[1].split("###", 1)[0]
            for heading in (
                "Location:",
                "Observation:",
                "Consequence:",
                "Smallest correction direction:",
            ):
                self.assertIn(heading, section)
        self.assertIn("Non-blocking preference control", oracle)
        self.assertIn("no confirmed material regression", oracle)
        self.assertIn("remain four", oracle)
        self.assertIn("genuine-stop", oracle)
        self.assertIn("outstanding coverage", oracle)

    def test_complete_scenario_gate_runs_green_from_policy_registry(self):
        registry = (self.repo / ".quality/gates.yaml").read_text(encoding="utf-8")
        self.assertIn("required: true", registry)
        command = next(
            line.split("command:", 1)[1].strip()
            for line in registry.splitlines()
            if line.strip().startswith("command:")
        )
        completed = subprocess.run(
            shlex.split(command),
            cwd=self.repo,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("architecture gate: ok", completed.stdout)

    def test_genuine_stop_scenario_supplies_real_stop_inputs(self):
        registry = (self.stop_repo / ".quality/gates.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("tools/archcheck verify src", registry)
        self.assertIn("required: true", registry)
        self.assertFalse((self.stop_repo / "tools" / "archcheck").exists())
        with self.assertRaises(FileNotFoundError):
            subprocess.run(
                ["tools/archcheck", "verify", "src"],
                cwd=self.stop_repo,
                capture_output=True,
            )
        fake_bin = Path(tempfile.mkdtemp(dir=self.work, prefix="fake-bin-"))
        fake_archcheck = fake_bin / "archcheck"
        fake_archcheck.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        fake_archcheck.chmod(0o755)
        with self.assertRaises(FileNotFoundError):
            subprocess.run(
                ["tools/archcheck", "verify", "src"],
                cwd=self.stop_repo,
                capture_output=True,
                env=os.environ
                | {"PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", "")},
            )
        rules = collapse((self.stop_repo / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn(
            "Do not edit gate configuration, install tools, or substitute "
            "static inspection",
            rules,
        )
        diff = self.git(self.stop_repo, "diff")
        for marker in ("LATE_RATES", "SqliteStore", "datetime", '("card", "wire")'):
            self.assertIn(marker, diff)
        facts = collapse(
            (self.run_dir / "genuine-stop-facts.md").read_text(encoding="utf-8")
        )
        self.assertIn("tools/archcheck verify src", facts)
        self.assertIn("FileNotFoundError", facts)
        self.assertIn("independent of any host `PATH` content", facts)
        self.assertIn("outstanding coverage", facts)
        self.assertIn("next owner", facts)

    def test_correction_round_fixes_one_finding_and_supplies_identity_inputs(self):
        """INT-FLOW-001 I-03 / R-03: one corrected finding, three survivors,
        and prior-report preservation are real fixture inputs for the next
        maintainability role call; the correction itself is observed at the
        real import/behavior boundary, not asserted from text alone.
        """
        repo = self.correction_repo
        changed_pricing = (repo / "src/billing/pricing.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("SURCHARGE_RATES", changed_pricing)
        self.assertNotIn("SqliteStore", changed_pricing)
        status = self.git(repo, "status", "--short")
        for relative in ("src/billing/service.py", "src/billing/receipts.py"):
            self.assertIn(relative, status)
        clean_fee, clean_directory = self.probe(
            repo,
            'from src.billing import pricing\n'
            'print(pricing.fee(100))\n'
            'print(pricing.surcharge(100, 10))\n',
        )
        self.assertEqual(0, clean_fee.returncode, clean_fee.stderr)
        self.assertEqual(["2.0", "1.5"], clean_fee.stdout.splitlines())
        self.assertFalse((clean_directory / "billing.db").exists())
        seeded, _ = self.probe(
            repo,
            'import sqlite3\n'
            'from src.billing import pricing\n'
            'connection = sqlite3.connect("billing.db")\n'
            'connection.execute("create table rates (name text, value real)")\n'
            "connection.execute(\"insert into rates values ('late:standard', 0.99)\")\n"
            'connection.commit()\n'
            'print(pricing.surcharge(100, 10))\n',
        )
        self.assertEqual(0, seeded.returncode, seeded.stderr)
        self.assertEqual("1.5", seeded.stdout.strip())
        diverged, _ = self.probe(
            repo,
            'from src.billing import pricing, service\n'
            'pricing.SURCHARGE_RATES["standard"] = 0.99\n'
            'print(pricing.surcharge(100, 10))\n'
            'print(service.checkout(100, 10, "card"))\n',
        )
        self.assertEqual(0, diverged.returncode, diverged.stderr)
        owner, copy_total = diverged.stdout.splitlines()
        self.assertEqual("99.0", owner)
        self.assertIn("103.50", copy_total)
        prior = collapse(
            (repo / "docs/tasks/MNT-42/reviews/maintainability-01.md").read_text(
                encoding="utf-8"
            )
        )
        for finding in ("MNT-B1", "MNT-B2", "MNT-B3", "MNT-B4"):
            self.assertIn(f"{finding} — ", prior)
        self.assertIn("Current disposition: confirmed", prior)
        facts = collapse(
            (self.run_dir / "correction-round-facts.md").read_text(encoding="utf-8")
        )
        for token in (
            "smallest correction direction",
            "MNT-B1, MNT-B3, and MNT-B4 keep their unchanged IDs",
            "current disposition `corrected`",
            "identity no earlier report or resolved finding already used",
            "MNT-B5",
            "not recycled",
            "reviews/maintainability-01.md remains unchanged",
            "reviews/maintainability-02.md",
            "genuine stop",
            "stable ID",
        ):
            self.assertIn(token, facts)


if __name__ == "__main__":
    unittest.main()
