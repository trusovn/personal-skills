import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock


CONTROLLER_PATH = Path(__file__).parents[1] / "scripts" / "controller.py"


# Historical transport mechanics have no public launch route in the new policy.
# Exercise them explicitly, preserving Git/timeout/inspection regression oracles.
LEGACY_CONTROLLER = [sys.executable, "-c", (
    "import sys; from pathlib import Path; "
    f"sys.path.insert(0, {str(CONTROLLER_PATH.parent)!r}); "
    "import controller; parser = controller.build_parser(); args = parser.parse_args(); "
    "args.handler = controller._legacy_run_next if args.command == 'run-next' else args.handler; "
    "sys.exit(args.handler(args))"
)]


def load_controller():
    spec = importlib.util.spec_from_file_location("task_orchestrator_controller", CONTROLLER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def flow_profile(profile="fast-local"):
    path = Path(__file__).parents[1] / "assets" / "examples" / f"{profile}-flow.json"
    return json.loads(path.read_text())


def stage_transport_fixture(run_dir):
    """Seed the transport boundary; this does not prove readiness admission.

    T-002.1 has no ready/preflight admission adapter. Transport/inspection
    regressions start from this explicit fixture, while the pending-stage test
    exercises the real initial boundary without this setup.
    """
    path = run_dir / "ledger.json"
    ledger = json.loads(path.read_text())
    ledger.update(selected_task_id="T1", current_step="implement")
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")


class ControllerContractTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"],
            check=True,
        )
        (self.repo / "allowed.txt").write_text("baseline\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "allowed.txt"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "baseline"], check=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def policy(self, *, commit_mode="off"):
        return {
            "version": 2,
            "execution_authorization": {"transport": "sbx", "yolo": True, "intervention": "active_chat"},
            "run_id": "run-1",
            "repository": str(self.repo),
            "task_ids": ["T1"],
            "verification": {
                "targeted_checks": ["python3 -m unittest test_targeted"],
                "repository_gate": "make verify",
                "authorized_gap": None,
            },
            "permissions": {
                "sandbox": "workspace-write",
                "approval_policy": "never",
                "network": False,
                "dependency_install": False,
                "writable_roots": [str(self.repo)],
                "danger_full_access_authorized": False,
            },
            "commit_policy": {"mode": commit_mode},
            "stop_policy": {
                "on_blocked": "stop",
                "on_failed": "stop",
                "on_needs_input": "escalate",
                "on_unexpected_changes": "stop",
            },
            "flow": flow_profile(),
        }

    def complete_result(self):
        return {
            "status": "complete",
            "task_id": "T1",
            "verification": [
                {"command": "python3 -m unittest test_targeted", "outcome": "passed"},
                {"command": "make verify", "outcome": "passed"},
            ],
            "questions": [],
            "risks": [],
        }

    def test_worker_complete_requires_independent_inspection(self):
        controller = load_controller()

        decision = controller.decide_closure(
            policy=self.policy(),
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status={},
            current_status=None,
            result=self.complete_result(),
        )

        self.assertFalse(decision["accepted"])
        self.assertNotIn("accepted", decision["allowed_transitions"])
        self.assertIn("independent Git inspection is missing", decision["reasons"])

    def test_unexpected_changed_and_untracked_paths_block_acceptance(self):
        controller = load_controller()
        baseline = controller.capture_git_status(self.repo)
        (self.repo / "allowed.txt").write_text("implemented\n")
        (self.repo / "unexpected.txt").write_text("scope drift\n")
        current = controller.capture_git_status(self.repo)

        decision = controller.decide_closure(
            policy=self.policy(),
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status=baseline,
            current_status=current,
            result=self.complete_result(),
        )

        self.assertFalse(decision["accepted"])
        self.assertEqual(["unexpected.txt"], decision["unexpected_paths"])
        self.assertNotIn("accepted", decision["allowed_transitions"])

    def test_commit_off_never_changes_git_or_offers_commit(self):
        controller = load_controller()
        baseline_head = subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        baseline = controller.capture_git_status(self.repo)
        (self.repo / "allowed.txt").write_text("implemented\n")
        current = controller.capture_git_status(self.repo)

        decision = controller.decide_closure(
            policy=self.policy(commit_mode="off"),
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status=baseline,
            current_status=current,
            result=self.complete_result(),
            controller_verification={
                "python3 -m unittest test_targeted": "passed",
                "make verify": "passed",
            },
            stage2_mode=False,  # Legacy mode: verify acceptance logic
        )

        current_head = subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        cached_diff = subprocess.run(
            ["git", "-C", str(self.repo), "diff", "--cached", "--quiet"],
            check=False,
        )
        self.assertTrue(decision["accepted"])
        self.assertNotIn("commit_exact_paths", decision["allowed_actions"])
        self.assertEqual(baseline_head, current_head)
        self.assertEqual(0, cached_diff.returncode)

    def test_worker_prompt_prohibits_commits_under_every_commit_policy(self):
        controller = load_controller()

        for mode in ("off", "controller_exact_paths"):
            with self.subTest(mode=mode):
                prompt = controller.render_worker_prompt(
                    task_id="T1",
                    brief_path="tasks/T1.md",
                    task_instructions="Implement only the selected task.",
                    policy=self.policy(commit_mode=mode),
                )
                self.assertIn("Do not commit", prompt)
                self.assertIn("Do not update the orchestration ledger", prompt)

    def test_installed_skill_and_controller_paths_are_scope_violations(self):
        controller = load_controller()
        baseline = controller.capture_git_status(self.repo)
        controller_path = ".agents/skills/task-orchestrator/scripts/codex_worker.py"
        path = self.repo / controller_path
        path.parent.mkdir(parents=True)
        path.write_text("unsafe patch\n")

        decision = controller.decide_closure(
            policy=self.policy(),
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status=baseline,
            current_status=controller.capture_git_status(self.repo),
            result=self.complete_result(),
        )

        self.assertFalse(decision["accepted"])
        self.assertEqual([controller_path], decision["unexpected_paths"])

    def test_attempt_records_require_recovery_identity_fields(self):
        controller = load_controller()
        incomplete = {
            "task_id": "T1",
            "brief_path": "tasks/T1.md",
            "prompt_sha256": "abc",
        }

        with self.assertRaisesRegex(ValueError, "baseline_ref"):
            controller.validate_attempt_record(incomplete)

    def test_retry_allocates_new_attempt_without_overwriting_evidence(self):
        controller = load_controller()
        run_dir = self.root / "run"
        record = controller.build_attempt_record(
            task_id="T1",
            brief_path="tasks/T1.md",
            prompt="first prompt",
            policy=self.policy(),
            flow=self.policy()["flow"],
            flow_revision=1,
            flow_sha256=controller.sha256_text(
                controller.canonical_json(self.policy()["flow"]) + "\n"
            ),
            baseline_ref="baseline-1.json",
        )
        first = controller.create_attempt(run_dir, record)
        evidence = first / "stderr.log"
        evidence.write_bytes(b"original failure\n")
        before = {path.name: path.read_bytes() for path in first.iterdir() if path.is_file()}

        retry_record = controller.build_attempt_record(
            task_id="T1",
            brief_path="tasks/T1.md",
            prompt="retry prompt",
            policy=self.policy(),
            flow=self.policy()["flow"],
            flow_revision=1,
            flow_sha256=controller.sha256_text(
                controller.canonical_json(self.policy()["flow"]) + "\n"
            ),
            baseline_ref="baseline-1.json",
        )
        second = controller.create_attempt(run_dir, retry_record)

        after = {path.name: path.read_bytes() for path in first.iterdir() if path.is_file()}
        self.assertNotEqual(first, second)
        self.assertEqual(before, after)
        self.assertEqual("attempt-002", second.name)

    def test_persisted_run_policy_cannot_be_replaced(self):
        controller = load_controller()
        policy_path = self.root / "run-policy.json"
        controller.persist_run_policy(policy_path, self.policy())
        original = policy_path.read_bytes()

        with self.assertRaises(FileExistsError):
            controller.persist_run_policy(policy_path, self.policy(commit_mode="controller_exact_paths"))

        self.assertEqual(original, policy_path.read_bytes())

    def test_unlisted_task_state_transition_is_rejected(self):
        controller = load_controller()

        with self.assertRaisesRegex(ValueError, "not allowed"):
            controller.transition_task("running", "accepted")

        self.assertEqual("awaiting_inspection", controller.transition_task(
            "running", "awaiting_inspection"
        ))

        with self.assertRaisesRegex(ValueError, "closure decision"):
            controller.transition_task("awaiting_inspection", "accepted")
        identity = {
            "run_id": "run-1",
            "task_id": "T1",
            "attempt_id": "attempt-001",
            "prompt_sha256": "prompt-digest",
            "evidence_digest": "evidence-digest",
        }
        self.assertEqual("accepted", controller.transition_task(
            "awaiting_inspection",
            "accepted",
            closure_decision={
                "accepted": True,
                "allowed_transitions": ["accepted"],
                "identity": identity,
            },
            expected_identity=identity,
        ))
        stale = dict(identity, attempt_id="attempt-000")
        with self.assertRaisesRegex(ValueError, "identity"):
            controller.transition_task(
                "awaiting_inspection",
                "accepted",
                closure_decision={
                    "accepted": True,
                    "allowed_transitions": ["accepted"],
                    "identity": stale,
                },
                expected_identity=identity,
            )
        with self.assertRaisesRegex(ValueError, "accepting closure decision"):
            controller.transition_task(
                "awaiting_inspection",
                "accepted",
                closure_decision={
                    "accepted": "yes",
                    "allowed_transitions": ["accepted"],
                    "identity": identity,
                },
                expected_identity=identity,
            )

    def test_preexisting_dirty_content_cannot_be_absorbed_by_task(self):
        controller = load_controller()
        dirty = self.repo / "user-notes.txt"
        dirty.write_text("user draft\n")
        baseline = controller.capture_git_status(self.repo)
        dirty.write_text("worker replacement\n")

        decision = controller.decide_closure(
            policy=self.policy(),
            task_id="T1",
            allowed_paths={"allowed.txt", "user-notes.txt"},
            baseline_status=baseline,
            current_status=controller.capture_git_status(self.repo),
            result=self.complete_result(),
        )

        self.assertFalse(decision["accepted"])
        self.assertIn("pre-existing dirty paths changed: user-notes.txt", decision["reasons"])

    def test_strict_run_policy_rejects_empty_task_ids_and_targeted_checks(self):
        """Empty task_ids and targeted_checks arrays must be rejected."""
        controller = load_controller()
        policy = self.policy()
        # Empty task_ids must fail (at least one required)
        policy["task_ids"] = []
        with self.assertRaises(ValueError) as ctx:
            controller.validate_run_policy(policy)
        self.assertIn("task_ids", ctx.exception.args[0])

        # Reset and empty targeted_checks
        policy["task_ids"] = ["T1"]
        policy["verification"]["targeted_checks"] = []
        with self.assertRaises(ValueError) as ctx:
            controller.validate_run_policy(policy)
        self.assertIn("targeted_checks", ctx.exception.args[0])

    def test_strict_nested_run_policy_rejects_missing_nested_required_fields(self):
        """validate_run_policy must enforce nested required fields from the schema."""
        controller = load_controller()
        policy = self.policy()
        # Strip the nested verification.targeted_checks — schema requires it.
        del policy["verification"]["targeted_checks"]
        with self.assertRaises(ValueError) as ctx:
            controller.validate_run_policy(policy)
        self.assertIn("verification", ctx.exception.args[0].lower())

    def test_strict_nested_run_policy_rejects_missing_nested_permission_fields(self):
        """validate_run_policy must enforce nested required fields in permissions."""
        controller = load_controller()
        policy = self.policy()
        # Strip network — schema requires it as a boolean.
        del policy["permissions"]["network"]
        with self.assertRaises(ValueError) as ctx:
            controller.validate_run_policy(policy)
        self.assertIn("network", ctx.exception.args[0].lower())

    def test_strict_nested_run_policy_rejects_unknown_nested_properties(self):
        """validate_run_policy must reject unknown properties in nested objects."""
        controller = load_controller()
        policy = self.policy()
        policy["verification"]["bogus_field"] = "should be rejected"
        with self.assertRaises(ValueError) as ctx:
            controller.validate_run_policy(policy)
        self.assertIn("unknown", ctx.exception.args[0].lower())

    def test_strict_nested_run_policy_rejects_wrong_type_in_nested_field(self):
        """validate_run_policy must reject wrong JSON types in nested fields."""
        controller = load_controller()
        policy = self.policy()
        # network must be boolean, not a string.
        policy["permissions"]["network"] = "yes"
        with self.assertRaises(ValueError) as ctx:
            controller.validate_run_policy(policy)
        self.assertIn("network", ctx.exception.args[0].lower())

    def test_strict_nested_run_policy_rejects_missing_stop_policy_fields(self):
        """validate_run_policy must enforce stop_policy nested required fields."""
        controller = load_controller()
        policy = self.policy()
        del policy["stop_policy"]["on_blocked"]
        with self.assertRaises(ValueError) as ctx:
            controller.validate_run_policy(policy)
        self.assertIn("stop_policy", ctx.exception.args[0].lower())

    def test_strict_nested_run_policy_rejects_danger_full_access_without_auth(self):
        """danger-full-access sandbox must require danger_full_access_authorized=true."""
        controller = load_controller()
        policy = self.policy()
        policy["permissions"]["sandbox"] = "danger-full-access"
        policy["permissions"]["danger_full_access_authorized"] = False
        with self.assertRaises(ValueError) as ctx:
            controller.validate_run_policy(policy)
        self.assertIn("danger-full-access", ctx.exception.args[0])

    def test_strict_nested_run_policy_accepts_valid_full_policy(self):
        """A fully valid policy must pass validation."""
        controller = load_controller()
        controller.validate_run_policy(self.policy())

    def test_run_policy_rejects_duplicate_array_items(self):
        """Run-policy arrays declared unique by the schema reject duplicates."""
        controller = load_controller()
        cases = (
            ("task_ids", lambda policy: policy.__setitem__("task_ids", ["T1", "T1"])),
            (
                "targeted_checks",
                lambda policy: policy["verification"].__setitem__(
                    "targeted_checks", ["make test", "make test"]
                ),
            ),
            (
                "writable_roots",
                lambda policy: policy["permissions"].__setitem__(
                    "writable_roots", [str(self.repo), str(self.repo)]
                ),
            ),
        )
        for field, mutate in cases:
            with self.subTest(field=field):
                policy = self.policy()
                mutate(policy)
                with self.assertRaisesRegex(ValueError, "unique"):
                    controller.validate_run_policy(policy)

    def test_task_manifest_rejects_schema_invalid_unique_arrays_and_unknown_fields(self):
        """Manifest arrays and top-level fields match the persisted schema."""
        controller = load_controller()
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        base = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": ["make test"],
            }],
        }
        cases = {
            "top-level unknown": lambda manifest: manifest.__setitem__("unknown", True),
            "completed_task_ids": lambda manifest: manifest.__setitem__(
                "completed_task_ids", ["T1", "T1"]
            ),
            "dependencies": lambda manifest: manifest["tasks"][0].__setitem__(
                "dependencies", ["T1", "T1"]
            ),
            "allowed_paths": lambda manifest: manifest["tasks"][0].__setitem__(
                "allowed_paths", ["allowed.txt", "allowed.txt"]
            ),
            "required_checks": lambda manifest: manifest["tasks"][0].__setitem__(
                "required_checks", ["make test", "make test"]
            ),
        }
        for field, mutate in cases.items():
            with self.subTest(field=field):
                manifest = json.loads(json.dumps(base))
                mutate(manifest)
                with self.assertRaisesRegex(ValueError, "unknown|unique"):
                    controller.validate_task_manifest(self.policy(), manifest, self.repo)

    def test_init_run_creates_ready_ledger_outside_repo(self):
        """init_run must atomically create a dependency-ready run directory."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-001"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        # Write a valid policy
        controller.persist_run_policy(policy_path, self.policy())

        # Write a valid manifest
        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": ["allowed.txt"],
                    "required_checks": ["python3 -m unittest test_targeted"],
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        result = controller.init_run(
            run_dir=run_dir,
            policy_path=policy_path,
            manifest_path=manifest_path,
            repository=self.repo,
        )

        self.assertEqual("run-1", result["run_id"])
        self.assertEqual("ready", result["state"])
        self.assertTrue((run_dir / "run-policy.json").exists())
        self.assertTrue((run_dir / "task-manifest.json").exists())
        self.assertTrue((run_dir / "ledger.json").exists())
        self.assertTrue((run_dir / "baselines" / "run-initial.json").exists())
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("ready", ledger["state"])
        self.assertIsNone(ledger["selected_task_id"])
        self.assertIsNone(ledger["active_attempt_id"])
        self.assertEqual(1, len(ledger["tasks"]))
        self.assertEqual("T1", ledger["tasks"][0]["id"])
        self.assertEqual("ready", ledger["tasks"][0]["state"])
        self.assertIsNone(ledger["last_closure_path"])
        self.assertIsNone(ledger["last_verification_path"])
        self.assertIsNone(ledger["last_decision_path"])
        self.assertIsNone(ledger["active_operation_path"])
        self.assertEqual(1, ledger["flow_revision"])
        self.assertEqual("flows/flow-001.json", ledger["flow_path"])
        self.assertEqual(
            sha256_bytes((run_dir / ledger["flow_path"]).read_bytes()),
            ledger["flow_sha256"],
        )

    def test_init_run_rejects_incomplete_dependencies(self):
        """init_run must reject authorized tasks depending on incomplete external tasks."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-002"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        controller.persist_run_policy(policy_path, self.policy())

        # T1 depends on T99 which is not in the manifest or completed
        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": ["T99"],
                    "allowed_paths": ["allowed.txt"],
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with self.assertRaises(ValueError) as ctx:
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )
        self.assertIn("depends on T99", ctx.exception.args[0])

    def test_select_task_returns_only_authorized_task(self):
        """Other manifest tasks do not become authorized by being ready."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-003"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        policy = self.policy()
        policy["task_ids"] = ["T2"]
        controller.persist_run_policy(policy_path, policy)

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {"id": "T1", "title": "Task 1", "brief_path": "tasks/T1.md",
                 "dependencies": [], "allowed_paths": ["allowed.txt"]},
                {"id": "T2", "title": "Task 2", "brief_path": "tasks/T2.md",
                 "dependencies": [], "allowed_paths": ["allowed.txt"]},
                {"id": "T3", "title": "Task 3", "brief_path": "tasks/T3.md",
                 "dependencies": ["T1"], "allowed_paths": ["allowed.txt"]},
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        (self.repo / "tasks" / "T2.md").write_text("# T2\n")
        (self.repo / "tasks" / "T3.md").write_text("# T3\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        controller.init_run(
            run_dir=run_dir,
            policy_path=policy_path,
            manifest_path=manifest_path,
            repository=self.repo,
        )

        ledger = json.loads((run_dir / "ledger.json").read_text())
        selected = controller.select_task(ledger, policy)
        # Only T2 is authorized even though T1 is also ready
        self.assertEqual("T2", selected["id"])

    def test_select_task_blocks_on_incomplete_deps(self):
        """select_task must block when no task is dependency-ready."""
        controller = load_controller()
        # Construct a ledger manually where all tasks have incomplete deps.
        ledger = {
            "version": 1,
            "run_id": "run-1",
            "repository": str(self.repo),
            "created_at": "2026-07-16T00:00:00+00:00",
            "updated_at": "2026-07-16T00:00:00+00:00",
            "revision": 1,
            "flow_revision": 1,
            "flow_path": "flows/flow-001.json",
            "flow_sha256": "a" * 64,
            "policy_path": "run-policy.json",
            "policy_sha256": "abc",
            "manifest_path": "task-manifest.json",
            "manifest_sha256": "def",
            "initial_baseline_path": "run-initial.json",
            "initial_baseline_digest": "ghi",
            "state": "ready",
            "selected_task_id": None,
            "active_attempt_id": None,
            "last_closure_path": None,
            "last_verification_path": None,
            "last_decision_path": None,
            "active_operation_path": None,
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Task 1",
                    "brief_path": "tasks/T1.md",
                    "dependencies": ["T99"],
                    "allowed_paths": ["allowed.txt"],
                    "required_checks": [],
                    "state": "ready",
                    "attempt_ids": [],
                },
            ],
        }
        policy = self.policy()
        with self.assertRaises(ValueError) as ctx:
            controller.select_task(ledger, policy)
        self.assertIn("No ready tasks", ctx.exception.args[0])

    def test_init_run_replaces_no_existing_run_dir(self):
        """init_run must not replace an existing run directory."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-existing"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        controller.persist_run_policy(policy_path, self.policy())

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": ["allowed.txt"],
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        # First init succeeds
        controller.init_run(
            run_dir=run_dir,
            policy_path=policy_path,
            manifest_path=manifest_path,
            repository=self.repo,
        )

        # Second init must fail
        with self.assertRaises(FileExistsError):
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )

    def test_init_run_atomic_on_validation_failure(self):
        """init_run must leave no run directory when validation fails."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-bad"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        controller.persist_run_policy(policy_path, self.policy())

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": ["T99"],
                    "allowed_paths": ["allowed.txt"],
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with self.assertRaises(ValueError):
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )

        self.assertFalse(run_dir.exists(), "Failed init must leave no run directory")

    def test_init_run_rejects_missing_brief_file(self):
        """init_run must reject a manifest where a brief file does not exist."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-005"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        controller.persist_run_policy(policy_path, self.policy())

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/nonexistent.md",
                    "dependencies": [],
                    "allowed_paths": ["allowed.txt"],
                }
            ],
        }
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with self.assertRaises(ValueError) as ctx:
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )
        self.assertIn("brief file does not exist", ctx.exception.args[0])

    def test_init_run_rejects_invalid_allowed_paths(self):
        """Allowed paths reject absolute, empty-segment, and directory forms."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-006"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        controller.persist_run_policy(policy_path, self.policy())

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": ["/absolute/path"],
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        for invalid_path in ("/absolute/path", "dir//file.py", "dir/", "dir/./file.py"):
            with self.subTest(path=invalid_path):
                manifest["tasks"][0]["allowed_paths"] = [invalid_path]
                manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
                with self.assertRaisesRegex(ValueError, "not a valid repository-relative path"):
                    controller.init_run(
                        run_dir=run_dir,
                        policy_path=policy_path,
                        manifest_path=manifest_path,
                        repository=self.repo,
                    )

    def test_init_run_rejects_parent_traversal_allowed_paths(self):
        """init_run must reject .. traversal in allowed_paths."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-007"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        controller.persist_run_policy(policy_path, self.policy())

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": ["../parent"],
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with self.assertRaises(ValueError) as ctx:
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )
        self.assertIn("not a valid repository-relative path", ctx.exception.args[0])

    def test_init_run_rejects_empty_allowed_paths(self):
        """init_run must reject manifests with empty allowed_paths arrays."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-008"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        controller.persist_run_policy(policy_path, self.policy())

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": [],  # Empty array
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with self.assertRaises(ValueError) as ctx:
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )
        self.assertIn("non-empty allowed_paths", ctx.exception.args[0])

    def test_init_run_rejects_dependency_cycles(self):
        """init_run must reject manifests with dependency cycles."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-009"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        policy = self.policy()
        policy["task_ids"] = ["T1"]
        controller.persist_run_policy(policy_path, policy)

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": ["T2"],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Task 1",
                    "brief_path": "tasks/T1.md",
                    "dependencies": ["T2"],
                    "allowed_paths": ["allowed.txt"],
                },
                {
                    "id": "T2",
                    "title": "Task 2",
                    "brief_path": "tasks/T2.md",
                    "dependencies": ["T1"],  # Cycle: T1 -> T2 -> T1
                    "allowed_paths": ["allowed.txt"],
                },
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        (self.repo / "tasks" / "T2.md").write_text("# T2\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with self.assertRaises(ValueError) as ctx:
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )
        self.assertIn("dependency cycle detected", ctx.exception.args[0].lower())

    def test_init_run_rejects_run_directory_inside_repository(self):
        """init_run must reject a run directory inside the repository."""
        controller = load_controller()
        # Run directory inside repo
        run_dir = self.repo / "runs" / "run-inside"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        controller.persist_run_policy(policy_path, self.policy())

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": ["allowed.txt"],
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with self.assertRaises(ValueError) as ctx:
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )
        self.assertIn("outside the repository", ctx.exception.args[0].lower())

    def test_preflight_before_mutation_blocks_on_failed_adapter(self):
        """run-next must preflight the adapter before any ledger mutation."""
        run_dir = self.root / "runs" / "run-010"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"
        controller = load_controller()

        controller.persist_run_policy(policy_path, self.policy())

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": ["allowed.txt"],
                    "required_checks": ["python3 -m unittest test_targeted"],
                }
            ],
        }
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        # Init succeeds
        init_result = subprocess.run(
            [
                sys.executable, str(CONTROLLER_PATH), "init",
                "--run-dir", str(run_dir),
                "--policy", str(policy_path),
                "--manifest", str(manifest_path),
                "--repository", str(self.repo),
            ],
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, init_result.returncode, init_result.stderr)
        stage_transport_fixture(run_dir)
        ledger_path = run_dir / "ledger.json"
        ledger_before = ledger_path.read_bytes()
        baseline_paths_before = sorted(
            path.relative_to(run_dir) for path in (run_dir / "baselines").iterdir()
        )

        run_next_command = [
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir),
            "--timeout-seconds", "10",
            "--codex-bin", "/nonexistent/codex",
        ]
        allowed_before = (self.repo / "allowed.txt").read_bytes()
        (self.repo / "allowed.txt").write_text("initial drift\n")
        drift_result = subprocess.run(
            run_next_command,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(0, drift_result.returncode)
        self.assertIn("Repository state has changed since initialization", drift_result.stderr)
        self.assertEqual(ledger_before, ledger_path.read_bytes())
        self.assertEqual(
            baseline_paths_before,
            sorted(path.relative_to(run_dir) for path in (run_dir / "baselines").iterdir()),
        )
        self.assertFalse((run_dir / "attempts").exists())
        (self.repo / "allowed.txt").write_bytes(allowed_before)

        # Run next with a non-existent adapter after restoring the exact baseline.
        run_result = subprocess.run(
            run_next_command, text=True, capture_output=True,
        )
        self.assertNotEqual(0, run_result.returncode)
        self.assertEqual(ledger_before, ledger_path.read_bytes())
        self.assertEqual(
            baseline_paths_before,
            sorted(path.relative_to(run_dir) for path in (run_dir / "baselines").iterdir()),
        )
        self.assertFalse(any(run_dir.glob("attempt-*")))
        self.assertFalse((run_dir / "attempts").exists())
        self.assertFalse((run_dir / "closure").exists())

        fake = self.root / "preflight-only-codex"
        fake.write_text("#!/bin/sh\nexit 0\n")
        fake.chmod(0o755)
        invalid_timeout = subprocess.run(
            [
                *LEGACY_CONTROLLER, "run-next",
                "--run-dir", str(run_dir),
                "--timeout-seconds", "0",
                "--codex-bin", str(fake),
            ],
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(0, invalid_timeout.returncode)
        self.assertIn("greater than zero", invalid_timeout.stderr)
        self.assertEqual(ledger_before, ledger_path.read_bytes())
        self.assertFalse((run_dir / "attempts").exists())

    def test_direct_update_ledger_obeys_run_lock(self):
        controller, run_dir = ControllerIntegrationTest.create_initialized_run(self, name="locked-run")
        ledger_path = run_dir / "ledger.json"
        lock_path = run_dir / "controller.lock"
        holder_code = (
            "import fcntl, pathlib, sys; "
            f"stream=pathlib.Path({str(lock_path)!r}).open('a+'); "
            "fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB); "
            "print('locked', flush=True); sys.stdin.readline(); "
            "fcntl.flock(stream.fileno(), fcntl.LOCK_UN); stream.close()"
        )
        holder = subprocess.Popen(
            [sys.executable, "-c", holder_code], text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        assert holder.stdout is not None
        before = ledger_path.read_bytes()
        try:
            self.assertEqual("locked", holder.stdout.readline().strip())
            with self.assertRaisesRegex(
                ValueError, "Another controller command owns"
            ):
                controller.update_ledger(run_dir, {}, expected_revision=1)
            self.assertEqual(before, ledger_path.read_bytes())
        finally:
            if holder.poll() is None:
                assert holder.stdin is not None
                holder.stdin.write("release\n")
                holder.stdin.flush()
            holder.communicate(timeout=5)

    def test_closure_rejects_worker_claimed_verification_without_controller_evidence(self):
        """decide_closure must not accept worker-claimed verification as independent proof."""
        controller = load_controller()
        policy = self.policy()
        baseline = controller.capture_git_status(self.repo)
        (self.repo / "allowed.txt").write_text("implemented\n")
        current = controller.capture_git_status(self.repo)
        # Worker claims all checks passed, but controller has no independent evidence.
        worker_result = {
            "status": "complete",
            "task_id": "T1",
            "verification": [
                {"command": "python3 -m unittest test_targeted", "outcome": "passed"},
                {"command": "make verify", "outcome": "passed"},
            ],
            "questions": [],
            "risks": [],
        }
        decision = controller.decide_closure(
            policy=policy,
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status=baseline,
            current_status=current,
            result=worker_result,
        )
        self.assertFalse(decision["accepted"])
        self.assertNotIn("accepted", decision["allowed_transitions"])
        # The closure must flag that verification claims came only from the worker.
        self.assertTrue(
            any("verification" in r.lower() or "claim" in r.lower() for r in decision["reasons"]),
            f"Expected a verification-claim reason, got: {decision['reasons']}",
        )

    def test_closure_accepts_when_controller_verification_is_provided(self):
        """When controller provides independent verification evidence, acceptance is possible."""
        controller = load_controller()
        policy = self.policy()
        baseline = controller.capture_git_status(self.repo)
        (self.repo / "allowed.txt").write_text("implemented\n")
        current = controller.capture_git_status(self.repo)
        worker_result = {
            "status": "complete",
            "task_id": "T1",
            "verification": [],
            "questions": [],
            "risks": [],
        }
        # Controller provides independent verification evidence.
        controller_verification = {
            "python3 -m unittest test_targeted": "passed",
            "make verify": "passed",
        }
        decision = controller.decide_closure(
            policy=policy,
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status=baseline,
            current_status=current,
            result=worker_result,
            controller_verification=controller_verification,
            stage2_mode=False,  # Legacy mode: verify acceptance logic
        )
        self.assertTrue(decision["accepted"])
        self.assertIn("accepted", decision["allowed_transitions"])

        stage2_decision = controller.decide_closure(
            policy=policy,
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status=baseline,
            current_status=current,
            result=worker_result,
            controller_verification=controller_verification,
        )
        self.assertFalse(stage2_decision["accepted"])
        self.assertNotIn("accepted", stage2_decision["allowed_transitions"])

    def test_closure_identity_binding_includes_run_task_attempt(self):
        """Closure decision must bind to run_id, task_id, attempt_id."""
        controller = load_controller()
        policy = self.policy()
        decision = controller.decide_closure(
            policy=policy,
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status={},
            current_status={},
            result=None,
            run_id="run-1",
            attempt_id="attempt-001",
        )
        self.assertIn("identity", decision)
        self.assertEqual("run-1", decision["identity"]["run_id"])
        self.assertEqual("T1", decision["identity"]["task_id"])
        self.assertEqual("attempt-001", decision["identity"]["attempt_id"])

    def test_closure_rejects_acceptance_in_stage_2(self):
        """Stage 2 closure must never allow acceptance, only inspect/stop."""
        controller = load_controller()
        policy = self.policy()
        decision = controller.decide_closure(
            policy=policy,
            task_id="T1",
            allowed_paths={"allowed.txt"},
            baseline_status={},
            current_status={},
            result=None,
            run_id="run-1",
            attempt_id="attempt-001",
            stage2_mode=True,  # Explicit Stage 2 mode
        )
        self.assertFalse(decision["accepted"])
        self.assertNotIn("accepted", decision["allowed_transitions"])
        # Stage 2 closures still allow resumable as a worker state transition
        self.assertIn("resumable", decision["allowed_transitions"])
        self.assertIn("inspect", decision["allowed_actions"])
        self.assertIn("stop", decision["allowed_actions"])
        self.assertNotIn("resume", decision["allowed_actions"])
        self.assertNotIn("record_acceptance", decision["allowed_actions"])


if __name__ == "__main__":
    unittest.main()


class ControllerIntegrationTest(unittest.TestCase):
    """Integration tests for controller CLI (init + run-next) using fake transport."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"],
            check=True,
        )
        (self.repo / "allowed.txt").write_text("baseline\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "allowed.txt"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "baseline"], check=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def policy(self):
        return {
            "version": 2,
            "execution_authorization": {"transport": "sbx", "yolo": True, "intervention": "active_chat"},
            "run_id": "run-1",
            "repository": str(self.repo),
            "task_ids": ["T1"],
            "verification": {
                "targeted_checks": ["python3 -m unittest test_targeted"],
                "repository_gate": "make verify",
                "authorized_gap": None,
            },
            "permissions": {
                "sandbox": "workspace-write",
                "approval_policy": "never",
                "network": False,
                "dependency_install": False,
                "writable_roots": [str(self.repo)],
                "danger_full_access_authorized": False,
            },
            "commit_policy": {"mode": "off"},
            "stop_policy": {
                "on_blocked": "stop",
                "on_failed": "stop",
                "on_needs_input": "escalate",
                "on_unexpected_changes": "stop",
            },
            "flow": flow_profile(),
        }

    def write_fake_codex(
        self, *, write_result=True, created_paths=("new.txt",),
        preflight_ready=None, preflight_release=None,
        worker_ready=None, worker_release=None, mutate_repository=True,
        clean_mutation=False, task_id="T1",
    ):
        """Write a fake codex that emits a thread and a valid result."""
        fake = self.root / "fake-codex"
        preflight_ready_path = str(preflight_ready) if preflight_ready else None
        preflight_release_path = str(preflight_release) if preflight_release else None
        worker_ready_path = str(worker_ready) if worker_ready else None
        worker_release_path = str(worker_release) if worker_release else None
        result_files = ["allowed.txt", *created_paths] if mutate_repository else []
        fake.write_text(
            f"""#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import sys
import time

def signal_and_wait(ready_value, release_value):
    if ready_value is None:
        return
    Path(ready_value).write_text("ready\\n")
    deadline = time.monotonic() + 10
    release_path = Path(release_value)
    while not release_path.exists():
        if time.monotonic() >= deadline:
            raise SystemExit("timed out waiting for test release")
        time.sleep(0.01)

args = sys.argv[1:]
log_path = Path({str(self.root / 'argv.json')!r})
log = json.loads(log_path.read_text()) if log_path.exists() else []
log.append(args)
log_path.write_text(json.dumps(log))
if "--help" in args:
    signal_and_wait({preflight_ready_path!r}, {preflight_release_path!r})
    raise SystemExit(0)
signal_and_wait({worker_ready_path!r}, {worker_release_path!r})
if {mutate_repository!r}:
    allowed = Path.cwd() / "allowed.txt"
    if not {clean_mutation!r}:
        allowed.write_text("committed change\\n")
        subprocess.run(["git", "add", "allowed.txt"], check=True)
        subprocess.run(["git", "commit", "-qm", "unauthorized worker commit"], check=True)
        allowed.write_text("staged change\\n")
        subprocess.run(["git", "add", "allowed.txt"], check=True)
    allowed.write_text("worker change\\n")
    created_paths = {created_paths!r}
    for index, path in enumerate(created_paths):
        Path.cwd().joinpath(path).write_text(f"untracked content {{index}}\\n")
print(json.dumps({{"type": "thread.started", "thread_id": "thread-fake-001"}}), flush=True)
if {write_result!r} and "-o" in args:
    result_path = Path(args[args.index("-o") + 1])
    result_path.write_text(json.dumps({{
        "status": "complete",
        "task_id": {task_id!r},
        "summary": "Implemented task {task_id}.",
        "files_changed": {result_files!r},
        "verification": [],
        "decisions": [],
        "questions": [],
        "risks": [],
        "next_action": "Inspect the diff."
    }}))
raise SystemExit(0)
"""
        )
        fake.chmod(0o755)
        return fake

    def create_initialized_run(self, *, flow=None, name="run-flow"):
        controller = load_controller()
        run_dir = self.root / "runs" / name
        policy_path = self.root / f"{name}-policy.json"
        manifest_path = self.root / f"{name}-manifest.json"
        policy = self.policy()
        if flow is not None:
            policy["flow"] = flow
        controller.persist_run_policy(policy_path, policy)
        (self.repo / "tasks").mkdir(exist_ok=True)
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps({
            "version": 1,
            "manifest_id": "flow-boundary",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": ["python3 -m unittest test_targeted"],
            }],
        }, indent=2, sort_keys=True) + "\n")
        controller.init_run(run_dir, policy_path, manifest_path, self.repo)
        return controller, run_dir

    def test_frozen_authority_survives_source_edits(self):
        controller, run_dir = self.create_initialized_run()
        ledger = json.loads((run_dir / "ledger.json").read_text())
        before = {p.relative_to(run_dir): p.read_bytes() for p in run_dir.rglob("*") if p.is_file()}
        frozen = controller.load_frozen_inputs(run_dir, ledger)
        inputs_bytes = (run_dir / "inputs.json").read_bytes()
        self.assertFalse(inputs_bytes.endswith(b"\n"))
        self.assertEqual(sha256_bytes(inputs_bytes), ledger["inputs_sha256"])
        self.assertEqual("# T1\n", frozen["documents"]["brief"]["content"])
        self.assertEqual("Source brief: T1.md\n", frozen["documents"]["verification"]["content"])
        self.assertEqual(["allowed.txt"], frozen["allowed_paths"])
        self.assertEqual(["python3 -m unittest test_targeted"], frozen["required_checks"])
        self.assertEqual(self.policy(), json.loads((run_dir / "run-policy.json").read_text()))
        for path in (self.repo / "tasks/T1.md", self.repo / "tasks/verification.md", self.root / "run-flow-policy.json", self.root / "run-flow-manifest.json"):
            with self.subTest(source=path):
                path.write_text("unapproved replacement\n")
                self.assertEqual(frozen, controller.load_frozen_inputs(run_dir, ledger))
                controller._load_flow_authority(run_dir, ledger)
                self.assertEqual(before, {p.relative_to(run_dir): p.read_bytes() for p in run_dir.rglob("*") if p.is_file()})

    def test_old_run_continuation_refuses_without_mutation(self):
        for family in ("version", "model", "optional_profile", "missing_snapshot"):
            with self.subTest(family=family):
                controller, run_dir = self.create_initialized_run(name=f"old-{family}")
                policy_path = run_dir / "run-policy.json"
                policy = json.loads(policy_path.read_text())
                if family == "version":
                    policy["version"] = 1
                elif family == "model":
                    policy["flow"]["actor_levels"]["light"]["model"] = "gpt-5.6-sol"
                elif family == "optional_profile":
                    policy["flow"]["steps"] = [step for step in policy["flow"]["steps"] if step["kind"] != "preflight"]
                else:
                    ledger_path = run_dir / "ledger.json"
                    ledger = json.loads(ledger_path.read_text())
                    del ledger["inputs_sha256"]
                    ledger_path.write_bytes(canonical_bytes(ledger))
                policy_path.write_bytes(canonical_bytes(policy))
                before = {p.relative_to(run_dir): p.read_bytes() for p in run_dir.rglob("*") if p.is_file()}
                result = subprocess.run([*LEGACY_CONTROLLER, "run-next", "--run-dir", str(run_dir), "--timeout-seconds", "10", "--codex-bin", str(self.root / "must-not-launch")], text=True, capture_output=True)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("Initialize a new run using reviewed current inputs", result.stderr)
                self.assertEqual(before, {p.relative_to(run_dir): p.read_bytes() for p in run_dir.rglob("*") if p.is_file()})

    def test_init_refuses_weakened_authority_without_partial_publication(self):
        controller, seed = self.create_initialized_run()
        base_policy = json.loads((seed / "run-policy.json").read_text())
        manifest_path = self.root / "run-flow-manifest.json"
        source_bytes = {p.relative_to(self.repo): p.read_bytes() for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts}
        variants = {}
        for kind in ("ready", "preflight", "implement", "verify", "semantic_review", "acceptance", "accept", "completed"):
            policy = json.loads(json.dumps(base_policy))
            policy["flow"]["steps"] = [step for step in policy["flow"]["steps"] if step["kind"] != kind]
            variants[f"omit-{kind}"] = policy
        for name, change in (
            ("merged-role", lambda p: p["flow"]["steps"][4].update(role="acceptance_reviewer")),
            ("reordered", lambda p: p["flow"]["steps"].reverse()),
            ("optional", lambda p: p["flow"]["steps"][1].update(mode="off")),
            ("multiple-tasks", lambda p: p["task_ids"].append("T2")),
        ):
            policy = json.loads(json.dumps(base_policy))
            change(policy)
            variants[name] = policy
        for name, policy in variants.items():
            with self.subTest(variant=name):
                policy_path = self.root / "invalid-policy.json"
                policy_path.write_bytes(canonical_bytes(policy))
                run_dir = self.root / "runs" / name
                before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
                result = subprocess.run([
                    sys.executable, str(CONTROLLER_PATH), "init",
                    "--run-dir", str(run_dir), "--policy", str(policy_path),
                    "--manifest", str(manifest_path), "--repository", str(self.repo),
                ], text=True, capture_output=True)
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(run_dir.exists())
                self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertEqual(source_bytes, {p.relative_to(self.repo): p.read_bytes() for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts})

    def test_old_flow_refuses_all_mutation_entries_without_touching_run(self):
        controller, run_dir = self.create_initialized_run()
        ready_ledger = json.loads((run_dir / "ledger.json").read_text())
        stage_transport_fixture(run_dir)
        fake = self.write_fake_codex(created_paths=(), clean_mutation=True)
        launch = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)
        self.assertEqual(0, launch.returncode, launch.stderr)
        inspection_ledger = json.loads((run_dir / "ledger.json").read_text())
        flow_path = run_dir / "flows/flow-001.json"
        flow = json.loads(flow_path.read_text())
        flow["version"] = 1
        flow_path.write_bytes(canonical_bytes(flow))
        ledger_path = run_dir / "ledger.json"
        revision_path = self.root / "new-flow.json"
        revision_path.write_bytes(canonical_bytes(flow_profile()))
        for entry in ("run-next", "inspect", "revise-flow", "update-ledger"):
            with self.subTest(entry=entry):
                ledger = dict(inspection_ledger if entry == "inspect" else ready_ledger)
                ledger["flow_sha256"] = sha256_bytes(flow_path.read_bytes())
                ledger_path.write_bytes(canonical_bytes(ledger))
                before = {p.relative_to(run_dir): p.read_bytes() for p in run_dir.rglob("*") if p.is_file()}
                if entry == "run-next":
                    result = subprocess.run([
                        *LEGACY_CONTROLLER, "run-next",
                        "--run-dir", str(run_dir), "--timeout-seconds", "10",
                        "--codex-bin", str(self.root / "must-not-launch"),
                    ], text=True, capture_output=True)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("Initialize a new run using reviewed current inputs", result.stderr)
                else:
                    with self.assertRaisesRegex(ValueError, "Initialize a new run using reviewed current inputs"):
                        if entry == "update-ledger":
                            controller.update_ledger(run_dir, {}, expected_revision=ledger["revision"])
                        elif entry == "revise-flow":
                            controller.revise_flow(run_dir, revision_path)
                        elif entry == "inspect":
                            controller.inspect_run(run_dir, 10)
                self.assertEqual(before, {p.relative_to(run_dir): p.read_bytes() for p in run_dir.rglob("*") if p.is_file()})

    def test_pending_ready_persists_cursor_without_launching_worker(self):
        reviewed = flow_profile("reviewed")
        controller, run_dir = self.create_initialized_run(flow=reviewed)
        repository_before = controller.capture_git_status(self.repo)
        missing_worker = self.root / "must-not-launch"

        result = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(missing_worker),
        ], text=True, capture_output=True)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({
            "status": "pending",
            "task_id": "T1",
            "current_step": "ready",
            "reason": "no MVP adapter owns the current flow step",
        }, json.loads(result.stdout))
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("ready", ledger["state"])
        self.assertEqual("T1", ledger["selected_task_id"])
        self.assertEqual("ready", ledger["current_step"])
        self.assertEqual(0, ledger["correction_cycle"])
        self.assertFalse((run_dir / "attempts").exists())
        self.assertFalse((self.root / "argv.json").exists())
        self.assertEqual(repository_before, controller.capture_git_status(self.repo))

        ledger_bytes = (run_dir / "ledger.json").read_bytes()
        repeated = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(missing_worker),
        ], text=True, capture_output=True)
        self.assertEqual(0, repeated.returncode, repeated.stderr)
        self.assertEqual(ledger_bytes, (run_dir / "ledger.json").read_bytes())
        self.assertFalse((run_dir / "attempts").exists())

    def test_flow_revision_is_immutable_noop_and_rejected_during_owned_work(self):
        controller, run_dir = self.create_initialized_run()
        first_path = run_dir / "flows/flow-001.json"
        first_bytes = first_path.read_bytes()
        reviewed_path = self.root / "reviewed-flow.json"
        reviewed_path.write_text(
            json.dumps(flow_profile("reviewed"), indent=2, sort_keys=True) + "\n"
        )
        fast_path = self.root / "fast-flow.json"
        fast_path.write_text(
            json.dumps(flow_profile(), indent=2, sort_keys=True) + "\n"
        )

        revised = controller.revise_flow(run_dir, reviewed_path)

        self.assertEqual("revised", revised["status"])
        self.assertEqual(2, revised["flow_revision"])
        self.assertEqual(first_bytes, first_path.read_bytes())
        second_path = run_dir / "flows/flow-002.json"
        second_bytes = second_path.read_bytes()
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual(2, ledger["flow_revision"])
        self.assertEqual("flows/flow-002.json", ledger["flow_path"])
        self.assertEqual(sha256_bytes(second_bytes), ledger["flow_sha256"])

        ledger_bytes = (run_dir / "ledger.json").read_bytes()
        unchanged = controller.revise_flow(run_dir, reviewed_path)
        self.assertEqual("unchanged", unchanged["status"])
        self.assertEqual(ledger_bytes, (run_dir / "ledger.json").read_bytes())
        self.assertEqual(
            ["flow-001.json", "flow-002.json"],
            sorted(path.name for path in (run_dir / "flows").iterdir()),
        )

        with mock.patch.object(
            controller,
            "_write_flow_pointer",
            side_effect=RuntimeError("injected pointer pre-commit failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "pre-commit"):
                controller.revise_flow(run_dir, fast_path)
        self.assertEqual(ledger_bytes, (run_dir / "ledger.json").read_bytes())
        self.assertEqual(
            "reviewed",
            controller._load_flow_authority(run_dir, ledger)["profile"],
        )
        self.assertTrue((run_dir / "flows/flow-003.json").is_file())

        write_flow_pointer = controller._write_flow_pointer

        def write_flow_pointer_then_fail(*args, **kwargs):
            write_flow_pointer(*args, **kwargs)
            raise RuntimeError("injected pointer publication failure")

        with mock.patch.object(
            controller,
            "_write_flow_pointer",
            side_effect=write_flow_pointer_then_fail,
        ):
            committed = controller.revise_flow(run_dir, fast_path)
        self.assertEqual("revised", committed["status"])
        self.assertEqual(3, committed["flow_revision"])
        committed_ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual(3, committed_ledger["flow_revision"])
        self.assertEqual(
            "fast-local",
            controller._load_flow_authority(run_dir, committed_ledger)["profile"],
        )

        restored = controller.revise_flow(run_dir, reviewed_path)
        self.assertEqual(4, restored["flow_revision"])

        pending = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(self.root / "must-not-launch"),
        ], text=True, capture_output=True)
        self.assertEqual(0, pending.returncode, pending.stderr)
        owned_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }
        with self.assertRaisesRegex(ValueError, "safe task boundary"):
            controller.revise_flow(run_dir, fast_path)
        self.assertEqual(
            owned_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )
        self.assertEqual(first_bytes, first_path.read_bytes())
        self.assertEqual(second_bytes, second_path.read_bytes())

    def test_flow_revision_publication_is_atomic_across_process_exit(self):
        controller, run_dir = self.create_initialized_run()
        revised_flow = flow_profile("reviewed")
        revised_path = self.root / "interrupted-flow.json"
        revised_path.write_text(
            json.dumps(revised_flow, indent=2, sort_keys=True) + "\n"
        )

        child = os.fork()
        if child == 0:
            with mock.patch.object(
                controller,
                "_write_flow_pointer",
                side_effect=lambda *_, **__: os._exit(23),
            ):
                controller.revise_flow(run_dir, revised_path)
            os._exit(24)

        waited, status = os.waitpid(child, 0)
        self.assertEqual(child, waited)
        self.assertEqual(23, os.waitstatus_to_exitcode(status))

        ledger = json.loads((run_dir / "ledger.json").read_text())
        try:
            current = controller._load_flow_authority(run_dir, ledger)
        except ValueError as error:
            self.fail(f"flow revision exposed split authority: {error}")
        self.assertEqual("fast-local", current["profile"])
        self.assertEqual(1, ledger["flow_revision"])

        resumed = controller.revise_flow(run_dir, revised_path)
        self.assertEqual(2, resumed["flow_revision"])
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual(
            "reviewed",
            controller._load_flow_authority(run_dir, ledger)["profile"],
        )

    def test_tampered_flow_fails_before_worker_preflight_or_run_mutation(self):
        controller, run_dir = self.create_initialized_run()
        flow_path = run_dir / "flows/flow-001.json"
        tampered = json.loads(flow_path.read_text())
        tampered["profile"] = "coherently-tampered"
        flow_path.write_text(json.dumps(tampered, separators=(",", ":")) + "\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }
        repository_before = controller.capture_git_status(self.repo)

        result = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(self.root / "must-not-launch"),
        ], text=True, capture_output=True)

        self.assertNotEqual(0, result.returncode)
        self.assertTrue(
            any(
                marker in result.stderr
                for marker in ("canonical", "digest")
            ),
            result.stderr,
        )
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )
        self.assertFalse((run_dir / "attempts").exists())
        self.assertFalse((self.root / "argv.json").exists())
        self.assertEqual(repository_before, controller.capture_git_status(self.repo))

    def test_impossible_correction_cycle_fails_before_worker_preflight(self):
        controller, run_dir = self.create_initialized_run(
            flow=flow_profile("reviewed")
        )
        ledger_path = run_dir / "ledger.json"
        ledger = json.loads(ledger_path.read_text())
        for current_step, correction_cycle in (
            ("implement", 4),
            ("correction", 0),
            ("correction", 4),
            ("semantic_review", 4),
            ("accept", 4),
        ):
            with self.subTest(
                current_step=current_step,
                correction_cycle=correction_cycle,
            ):
                invalid = json.loads(json.dumps(ledger))
                invalid.update({
                    "selected_task_id": "T1",
                    "current_step": current_step,
                    "correction_cycle": correction_cycle,
                })
                with self.assertRaisesRegex(ValueError, "correction cycle"):
                    controller._load_flow_authority(run_dir, invalid)

        ledger.update({
            "selected_task_id": "T1",
            "current_step": "implement",
            "correction_cycle": 4,
        })
        ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }
        repository_before = controller.capture_git_status(self.repo)
        fake = self.write_fake_codex(created_paths=(), mutate_repository=False)

        result = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("correction cycle", result.stderr)
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )
        self.assertFalse((run_dir / "attempts").exists())
        self.assertFalse((self.root / "argv.json").exists())
        self.assertEqual(repository_before, controller.capture_git_status(self.repo))

    def test_coherent_flow_history_truncation_fails_before_worker_preflight(self):
        controller, run_dir = self.create_initialized_run()
        current = flow_profile()
        current["profile"] = "strong-current"
        current["steps"][2]["mode"] = "strong"
        current_path = self.root / "strong-current.json"
        current_path.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
        controller.revise_flow(run_dir, current_path)

        (run_dir / "flows/flow-002.json").unlink()
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }
        repository_before = controller.capture_git_status(self.repo)
        fake = self.write_fake_codex(created_paths=(), mutate_repository=False)

        result = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)

        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )
        self.assertFalse((run_dir / "attempts").exists())
        self.assertFalse((self.root / "argv.json").exists())
        self.assertEqual(repository_before, controller.capture_git_status(self.repo))

    def test_revised_flow_controls_implementation_actor_selection(self):
        controller, run_dir = self.create_initialized_run()
        revised_flow = flow_profile()
        revised_flow["profile"] = "strong-implementation"
        revised_flow["steps"][2]["mode"] = "strong"
        revised_path = self.root / "strong-implementation-flow.json"
        revised_path.write_text(
            json.dumps(revised_flow, indent=2, sort_keys=True) + "\n"
        )
        controller.revise_flow(run_dir, revised_path)
        stage_transport_fixture(run_dir)
        fake = self.write_fake_codex(created_paths=(), mutate_repository=False)

        result = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)

        self.assertEqual(0, result.returncode, result.stderr)
        attempt = json.loads(
            (run_dir / "attempts/attempt-001/record.json").read_text()
        )
        self.assertEqual(
            ("gpt-6.1-sol", "high"),
            (attempt["model"], attempt["effort"]),
        )

    def test_accepted_workspace_rejects_later_drift(self):
        controller, run_dir = self.create_initialized_run()
        stage_transport_fixture(run_dir)
        fake = self.write_fake_codex(created_paths=(), clean_mutation=True)
        result = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        ledger = json.loads((run_dir / "ledger.json").read_text())
        # Fixture for the historical integrity checker, not an acceptance path.
        ledger["tasks"][0]["state"] = "accepted"
        controller._validate_accepted_workspace(run_dir, ledger)
        before = {p.relative_to(run_dir): p.read_bytes() for p in run_dir.rglob("*") if p.is_file()}
        accepted_bytes = (self.repo / "allowed.txt").read_bytes()
        (self.repo / "allowed.txt").write_text("later ordinary drift\n")
        with self.assertRaisesRegex(ValueError, "Repository bytes changed after acceptance"):
            controller._validate_accepted_workspace(run_dir, ledger)
        self.assertEqual(before, {p.relative_to(run_dir): p.read_bytes() for p in run_dir.rglob("*") if p.is_file()})
        (self.repo / "allowed.txt").write_bytes(accepted_bytes)
        controller._validate_accepted_workspace(run_dir, ledger)
        ledger["state"] = "ready"
        ledger["selected_task_id"] = None
        with self.assertRaisesRegex(ValueError, "No ready tasks found"):
            controller.select_task(ledger, self.policy())

    def test_full_init_and_run_next_flow(self):
        """End-to-end: init + run-next with fake transport produces awaiting_inspection."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-001"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"
        created_paths = (
            "new.txt",
            "space name.txt",
            "-leading-dash.txt",
            "tab\tname.txt",
            "line\nname.txt",
            "shell$(touch side-effect).txt",
        )
        fake = self.write_fake_codex(created_paths=created_paths)

        # Write policy
        controller.persist_run_policy(policy_path, self.policy())

        # Write manifest
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1",
                    "title": "Test task",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": ["allowed.txt", *created_paths],
                    "required_checks": ["python3 -m unittest test_targeted"],
                }
            ],
        }
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        # Init
        init_result = subprocess.run(
            [
                sys.executable, str(CONTROLLER_PATH), "init",
                "--run-dir", str(run_dir),
                "--policy", str(policy_path),
                "--manifest", str(manifest_path),
                "--repository", str(self.repo),
            ],
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, init_result.returncode, init_result.stderr)
        init_data = json.loads(init_result.stdout)
        self.assertEqual("run-1", init_data["run_id"])
        self.assertEqual("ready", init_data["state"])

        stage_transport_fixture(run_dir)
        # The worker receives approved documents, with identity bound by inputs.json.
        # Run next
        run_result = subprocess.run(
            [
                *LEGACY_CONTROLLER, "run-next",
                "--run-dir", str(run_dir),
                "--timeout-seconds", "10",
                "--codex-bin", str(fake),
            ],
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, run_result.returncode, f"run-next stderr: {run_result.stderr}")
        run_data = json.loads(run_result.stdout)
        self.assertEqual("awaiting_inspection", run_data["status"])
        self.assertEqual("T1", run_data["task_id"])

        # Verify ledger state
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("awaiting_inspection", ledger["state"])
        prompt = (run_dir / "attempts/attempt-001/prompt.txt").read_text()
        self.assertIn("Frozen brief:\n# T1\n", prompt)
        self.assertIn("Frozen verification:\nSource brief: T1.md\n", prompt)
        self.assertEqual("T1", ledger["selected_task_id"])
        self.assertIsNone(ledger["active_attempt_id"])
        self.assertIsNotNone(ledger["last_closure_path"])

        # Verify closure packet exists
        closure_path = run_dir / ledger["last_closure_path"]
        self.assertTrue(closure_path.exists())
        closure = json.loads(closure_path.read_text())
        self.assertFalse(closure["accepted"])
        # Should note missing controller verification
        self.assertTrue(
            any("verification" in r.lower() or "missing" in r.lower() for r in closure["reasons"]),
            f"Expected verification-missing reason, got: {closure['reasons']}",
        )

        # Verify attempt directory exists
        attempt_dirs = list((run_dir / "attempts").iterdir())
        attempt_dirs = [d for d in attempt_dirs if d.is_dir() and d.name.startswith("attempt-")]
        self.assertEqual(1, len(attempt_dirs))
        attempt = attempt_dirs[0]
        self.assertTrue((attempt / "record.json").exists())
        self.assertTrue((attempt / "prompt.txt").exists())
        attempt_record = json.loads((attempt / "record.json").read_text())
        self.assertEqual(str(fake), attempt_record["codex_bin"])
        self.assertEqual(10.0, attempt_record["timeout_seconds"])
        self.assertEqual(
            self.policy()["permissions"],
            attempt_record["effective_permission_envelope"],
        )
        self.assertEqual("start", attempt_record["adapter_invocation"][2])

        # Verify closure artifacts
        closure_dir = run_dir / "closure"
        self.assertTrue((closure_dir / f"{attempt.name}.json").exists())
        self.assertTrue((closure_dir / f"{attempt.name}.staged.name-status.txt").exists())
        self.assertTrue((closure_dir / f"{attempt.name}.unstaged.name-status.txt").exists())
        self.assertTrue((closure_dir / f"{attempt.name}.staged.stat.txt").exists())
        self.assertTrue((closure_dir / f"{attempt.name}.unstaged.stat.txt").exists())
        patch_path = closure_dir / f"{attempt.name}.diff.patch"
        patch = patch_path.read_text()
        self.assertIn("worker change", patch)
        for index in range(len(created_paths)):
            self.assertIn(f"untracked content {index}", patch)
        self.assertFalse((self.repo / "side-effect").exists())
        # Verify the closure packet has complete identity and evidence
        closure_data = json.loads((closure_dir / f"{attempt.name}.json").read_text())
        self.assertIn("run_id", closure_data)
        self.assertIn("task_id", closure_data)
        self.assertIn("attempt_id", closure_data)
        self.assertIn("policy_sha256", closure_data)
        self.assertIn("manifest_sha256", closure_data)
        self.assertIn("head_before", closure_data)
        self.assertIn("head_after", closure_data)
        self.assertIn("controller_observations", closure_data)
        self.assertEqual(closure_data["controller_verification"], "not_collected")
        # Verify closure file digests
        self.assertIn("index_tree_digest", closure_data)
        self.assertIn("staged_digest", closure_data)
        self.assertIn("task_patch_digest", closure_data)
        self.assertIn("staged_stat_digest", closure_data)
        self.assertIn("unstaged_stat_digest", closure_data)
        self.assertEqual("awaiting_inspection", closure_data["worker_claims"]["terminal_state"])
        self.assertEqual(0, closure_data["worker_claims"]["exit_code"])
        self.assertEqual("complete", closure_data["worker_claims"]["attempt_outcome"])
        self.assertEqual(
            sorted(["allowed.txt", *created_paths]),
            closure_data["controller_observations"]["allowed_changed_paths"],
        )
        self.assertEqual(
            sorted([*created_paths, "tasks/T1.md", "tasks/verification.md"]),
            closure_data["controller_observations"]["untracked_paths"],
        )
        self.assertEqual([], closure_data["controller_observations"]["unexpected_paths"])
        self.assertTrue(closure_data["controller_observations"]["head_changed"])
        self.assertTrue(closure_data["controller_observations"]["index_changed"])
        mechanical_violations = [
            "worker changed HEAD despite commit prohibition",
            "worker changed the Git index",
        ]
        self.assertEqual(
            mechanical_violations,
            closure_data["controller_observations"]["mechanical_violations"],
        )
        for violation in mechanical_violations:
            self.assertIn(violation, closure_data["reasons"])
        # Verify identity binding
        self.assertIn("identity", closure_data)
        self.assertEqual("run-1", closure_data["identity"]["run_id"])
        self.assertEqual("T1", closure_data["identity"]["task_id"])
        self.assertEqual(
            closure_data["evidence_digest"],
            closure_data["identity"]["evidence_digest"],
        )
        # Stage 2: never accept, only inspect/stop
        self.assertFalse(closure_data["accepted"])
        self.assertNotIn("accepted", closure_data["allowed_transitions"])
        self.assertIn("inspect", closure_data["allowed_actions"])
        self.assertIn("stop", closure_data["allowed_actions"])
        self.assertEqual(["attempt-001"], ledger["tasks"][0]["attempt_ids"])
        self.assertEqual("awaiting_inspection", ledger["tasks"][0]["state"])

        ledger_path = run_dir / "ledger.json"
        ledger_before = ledger_path.read_bytes()
        rewritten_tasks = [dict(entry) for entry in ledger["tasks"]]
        rewritten_tasks[0]["attempt_ids"] = ["attempt-002"]
        with self.assertRaisesRegex(ValueError, "append-only"):
            controller.update_ledger(
                run_dir, {"tasks": rewritten_tasks}, expected_revision=ledger["revision"]
            )
        self.assertEqual(ledger_before, ledger_path.read_bytes())

    def wait_for_path(self, path, process, timeout=5):
        deadline = time.monotonic() + timeout
        while not path.exists():
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                self.fail(
                    f"controller exited before {path.name}: "
                    f"stdout={stdout!r}, stderr={stderr!r}"
                )
            if time.monotonic() >= deadline:
                self.fail(f"timed out waiting for {path}")
            time.sleep(0.01)

    def test_run_next_lock_and_stale_reconciliation_are_process_safe(self):
        controller = load_controller()
        run_dir = self.root / "runs" / "run-locked"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"
        preflight_ready = self.root / "preflight-ready"
        preflight_release = self.root / "preflight-release"
        worker_ready = self.root / "worker-ready"
        worker_release = self.root / "worker-release"
        fake = self.write_fake_codex(
            created_paths=(),
            preflight_ready=preflight_ready,
            preflight_release=preflight_release,
            worker_ready=worker_ready,
            worker_release=worker_release,
            mutate_repository=False,
        )
        controller.persist_run_policy(policy_path, self.policy())
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps({
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": ["python3 -m unittest test_targeted"],
            }],
        }, indent=2, sort_keys=True) + "\n")
        controller.init_run(run_dir, policy_path, manifest_path, self.repo)
        stage_transport_fixture(run_dir)
        command = [
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir),
            "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ]
        first = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            self.wait_for_path(preflight_ready, first)
            held_competitor = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(0, held_competitor.returncode)
            self.assertIn("owns this run's mutation phase", held_competitor.stderr)
            self.assertFalse((run_dir / "attempts").exists())

            preflight_release.write_text("release\n")
            self.wait_for_path(worker_ready, first)
            running = json.loads((run_dir / "ledger.json").read_text())
            self.assertEqual("running", running["state"])
            self.assertEqual(["attempt-001"], running["tasks"][0]["attempt_ids"])

            running_competitor = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(0, running_competitor.returncode)
            self.assertIn("Cannot select task from state 'running'", running_competitor.stderr)
            self.assertEqual(
                ["attempt-001"],
                json.loads((run_dir / "ledger.json").read_text())["tasks"][0]["attempt_ids"],
            )
            invocations = json.loads((self.root / "argv.json").read_text())
            self.assertEqual(1, sum("--help" not in args for args in invocations))

            lock_stream = (run_dir / "controller.lock").open("a+")
            try:
                fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                stopped_tasks = [dict(entry) for entry in running["tasks"]]
                stopped_tasks[0]["state"] = "stopped"
                controller._update_ledger_locked(run_dir, {
                    "state": "stopped",
                    "selected_task_id": None,
                    "active_attempt_id": None,
                    "current_step": None,
                    "correction_cycle": 0,
                    "tasks": stopped_tasks,
                }, expected_revision=running["revision"],
                    cursor_action="task_boundary")
            finally:
                fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)
                lock_stream.close()
            competing_bytes = (run_dir / "ledger.json").read_bytes()

            worker_release.write_text("release\n")
            stdout, stderr = first.communicate(timeout=15)
            self.assertNotEqual(0, first.returncode, stdout)
            self.assertIn("refusing stale reconciliation", stderr)
            self.assertEqual(competing_bytes, (run_dir / "ledger.json").read_bytes())
        finally:
            preflight_release.touch()
            worker_release.touch()
            if first.poll() is None:
                first.kill()
                first.communicate()

    def test_run_next_stops_on_missing_terminal_result(self):
        controller = load_controller()
        run_dir = self.root / "runs" / "run-missing-result"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"
        fake = self.write_fake_codex(write_result=False)
        controller.persist_run_policy(policy_path, self.policy())
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps({
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt", "new.txt"],
                "required_checks": ["python3 -m unittest test_targeted"],
            }],
        }, indent=2, sort_keys=True) + "\n")
        controller.init_run(run_dir, policy_path, manifest_path, self.repo)

        stage_transport_fixture(run_dir)
        result = subprocess.run(
            [
                *LEGACY_CONTROLLER, "run-next",
                "--run-dir", str(run_dir),
                "--timeout-seconds", "10",
                "--codex-bin", str(fake),
            ],
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(0, result.returncode)
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("stopped", ledger["state"])
        self.assertIsNone(ledger["selected_task_id"])
        self.assertIsNone(ledger["active_attempt_id"])
        self.assertEqual("stopped", ledger["tasks"][0]["state"])
        self.assertEqual(["attempt-001"], ledger["tasks"][0]["attempt_ids"])
        self.assertFalse((run_dir / "closure").exists())


class ControllerReservationTest(unittest.TestCase):
    setUp = ControllerIntegrationTest.setUp
    tearDown = ControllerIntegrationTest.tearDown
    policy = ControllerIntegrationTest.policy
    create_initialized_run = ControllerIntegrationTest.create_initialized_run

    def test_reserve_replay_survives_reload(self):
        controller, run_dir = self.create_initialized_run()
        request = dict(expected_version=1, task_id="T1", stage="preflight",
                       role="preflight", operation_key="first", reason="initial")
        first = controller.reserve_operation(run_dir, **request)
        self.assertEqual("reserved", first["status"])
        before = (run_dir / "ledger.json").read_bytes()
        replay = load_controller().reserve_operation(run_dir, **request)
        self.assertEqual("replayed", replay["status"])
        self.assertEqual(first["assignment"], replay["assignment"])
        self.assertEqual(before, (run_dir / "ledger.json").read_bytes())

    def read_ledger(self, run_dir):
        return json.loads((run_dir / "ledger.json").read_text())

    def seed_successor(self, run_dir, *, stage=None, readiness=False, **changes):
        """Test-only T-003/004/005 admission; no production outcome is claimed."""
        ledger = self.read_ledger(run_dir)
        if ledger["actor_operations"]:
            ledger["actor_operations"][-1]["state"] = "terminal"
        ledger["active_operation_path"] = None
        if stage:
            ledger["current_step"] = stage
        if readiness:
            operation = ledger["actor_operations"][-1]
            ledger["readiness"] = {field: operation["assignment"][field] for field in
                                   ("task_id", "operation_id", "inputs_sha256", "policy_sha256", "flow_sha256")}
            ledger["readiness"]["status"] = "ready"
        ledger.update(changes)
        ledger["revision"] += 1
        (run_dir / "ledger.json").write_text(json.dumps(ledger))

    def reserve(self, run_dir, stage="preflight", key="first", reason="initial", **overrides):
        request = dict(expected_version=self.read_ledger(run_dir)["revision"], task_id="T1",
                       stage=stage, role={"correction": "implementer", "implement": "implementer",
                       "verify": "verifier", "semantic_review": "review_collector",
                       "acceptance": "acceptance_reviewer", "preflight": "preflight"}[stage],
                       operation_key=key, reason=reason)
        request.update(overrides)
        return load_controller().reserve_operation(run_dir, **request)

    def snapshot(self, run_dir):
        return {str(path): path.read_bytes() for root in (run_dir, self.repo)
                for path in root.rglob("*") if path.is_file() and path.name != "controller.lock"}

    def ready_implementation(self, run_dir, key="ready"):
        self.assertEqual("reserved", self.reserve(run_dir, key=key)["status"])
        self.seed_successor(run_dir, stage="implement", readiness=True)

    def test_public_cli_contract_and_weakened_authority_refusal(self):
        controller, run_dir = self.create_initialized_run()
        status_command = [sys.executable, str(CONTROLLER_PATH), "status", "--run-dir", str(run_dir)]
        result = subprocess.run(status_command, text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(1, json.loads(result.stdout)["state_version"])
        command = [sys.executable, str(CONTROLLER_PATH), "reserve", "--run-dir", str(run_dir),
                   "--expected-version", "1", "--task-id", "T1", "--stage", "preflight",
                   "--role", "preflight", "--operation-key", "cli"]
        result = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("reserved", json.loads(result.stdout)["status"])
        before = self.snapshot(run_dir)
        replay = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual("replayed", json.loads(replay.stdout)["status"])
        refused = subprocess.run(command[:-1] + ["competing"], text=True, capture_output=True)
        self.assertEqual(1, refused.returncode)
        self.assertEqual("stale_version", json.loads(refused.stdout)["reason"])
        self.assertEqual(before, self.snapshot(run_dir))
        self.seed_successor(run_dir, stage="implement", readiness=True)
        policy_path = run_dir / "run-policy.json"
        policy = json.loads(policy_path.read_text())
        policy["flow"]["steps"] = policy["flow"]["steps"][1:]
        policy_path.write_text(json.dumps(policy))
        before = self.snapshot(run_dir)
        self.assertEqual("authority_or_lock_unavailable", self.reserve(run_dir, "implement", "weak")["reason"])
        self.assertEqual(before, self.snapshot(run_dir))


    def test_status_is_read_only_and_preserves_evidence_distinctions(self):
        controller, run_dir = self.create_initialized_run()
        self.ready_implementation(run_dir)
        ledger = self.read_ledger(run_dir)
        for evidence_status, expected in (("passed", "passed"), ("failed", "failed"),
                ("stale", "stale"), ("blocked", "blocked"), ("missing", "missing"),
                ("not_run", "not_run"), ("omitted_by_policy", "blocked")):
            with self.subTest(evidence_status=evidence_status):
                evidence = {"verify": {"status": evidence_status, "inputs_sha256": ledger["inputs_sha256"],
                                      "candidate_sha256": "a" * 64, "reference": "checks/check-1.json"}}
                self.seed_successor(run_dir, candidate_sha256="a" * 64, evidence=evidence,
                                    outstanding_findings=[{"id": "F1", "status": "open"}])
                before = self.snapshot(run_dir)
                status = load_controller().status_run(run_dir)
                self.assertEqual(expected, status["evidence"]["verify"]["status"])
                self.assertEqual("checks/check-1.json", status["evidence"]["verify"]["reference"])
                self.assertEqual("F1", status["outstanding_findings"][0]["id"])
                self.assertEqual("T1", status["task_id"])
                self.assertEqual("run-1", status["run_id"])
                self.assertEqual(0, status["correction_count"])
                self.assertEqual(["reserve:implement"], status["next_actions"])
                self.assertEqual(before, self.snapshot(run_dir))
        self.seed_successor(run_dir, evidence={"verify": {"status": "passed", "inputs_sha256": "b" * 64}})
        self.assertEqual("stale", controller.status_run(run_dir)["evidence"]["verify"]["status"])
        targeted = flow_profile()
        targeted["steps"][3]["mode"] = "targeted"
        controller, other = self.create_initialized_run(flow=targeted, name="targeted")
        self.assertEqual(["repository_gate"], controller.status_run(other)["policy_omissions"])

    def test_active_states_and_conflicts_preserve_files_and_charge(self):
        controller, run_dir = self.create_initialized_run()
        first = self.reserve(run_dir)
        self.assertEqual("reserved", first["status"])
        for state in ("reserved", "running", "unknown"):
            ledger = self.read_ledger(run_dir)
            ledger["actor_operations"][-1]["state"] = state
            (run_dir / "ledger.json").write_text(json.dumps(ledger))
            before = self.snapshot(run_dir)
            self.assertEqual("refused", self.reserve(run_dir, key="competitor")["status"])
            self.assertEqual("operation_key_conflict", self.reserve(run_dir, key="first", reason="retry")["reason"])
            status = load_controller().status_run(run_dir)
            self.assertEqual(state, status["operation"]["state"])
            self.assertEqual(["observe_operation", "intervene"], status["next_actions"])
            self.assertEqual("refused", controller.inspect_run(run_dir, 10)["status"])
            with self.assertRaisesRegex(ValueError, "Active actor"):
                controller.update_ledger(run_dir, {}, expected_revision=ledger["revision"])
            flow_path = self.root / "same-flow.json"
            flow_path.write_text(json.dumps(flow_profile()))
            with self.assertRaises(ValueError):
                controller.revise_flow(run_dir, flow_path)
            self.assertEqual(before, self.snapshot(run_dir))
        self.seed_successor(run_dir, stage="preflight")
        self.assertEqual("reserved", self.reserve(run_dir, key="terminal-retry", reason="retry")["status"])

    def test_active_assignment_must_match_current_ledger(self):
        for profile, stage, prior in (
            (profile, stage, prior) for profile in ("fast-local", "strong-local")
            for stage, prior in (("preflight", None), ("implement", None), ("correction", None),
                                 ("verify", "implement"), ("semantic_review", "verify"),
                                 ("acceptance", "semantic_review"))
        ):
            controller, run_dir = self.create_initialized_run(
                flow=flow_profile(profile), name=f"identity-{profile}-{stage}")
            if stage != "preflight":
                self.ready_implementation(run_dir)
            if prior:
                ledger = self.read_ledger(run_dir)
                evidence = {prior: {"status": "passed", "inputs_sha256": ledger["inputs_sha256"],
                                    "candidate_sha256": "a" * 64}}
                self.seed_successor(run_dir, stage=stage, candidate_sha256="a" * 64, evidence=evidence)
            if stage == "correction":
                self.seed_successor(run_dir, correction_request="environment_repair")
            result = self.reserve(run_dir, stage, "active", "environment_repair" if stage == "correction" else "initial")
            self.assertEqual("reserved", result["status"], result)
            base = self.read_ledger(run_dir)
            for state in ("reserved", "running", "unknown"):
                good = json.loads(json.dumps(base))
                good["actor_operations"][-1]["state"] = state
                (run_dir / "ledger.json").write_text(json.dumps(good))
                self.assertEqual(state, controller.status_run(run_dir)["operation"]["state"])
                request = good["actor_operations"][-1]["request"]
                self.assertEqual("replayed", controller.reserve_operation(run_dir, **request)["status"])
                variants = []
                for field, value in (("inputs_sha256", "b" * 64), ("policy_sha256", "b" * 64),
                                     ("flow_sha256", "b" * 64), ("flow_revision", 2),
                                     ("candidate_sha256", "b" * 64)):
                    invalid = json.loads(json.dumps(good))
                    invalid["actor_operations"][-1]["assignment"][field] = value
                    variants.append((field, invalid))
                for reasoning in ("low", "medium", "high"):
                    actor = {"model": "gpt-6.1-sol", "reasoning": reasoning}
                    if actor != good["actor_operations"][-1]["assignment"]["actor"]:
                        invalid = json.loads(json.dumps(good))
                        invalid["actor_operations"][-1]["assignment"]["actor"] = actor
                        variants.append((f"actor {reasoning}", invalid))
                invalid = json.loads(json.dumps(good))
                invalid["current_step"] = "verify" if stage != "verify" else "acceptance"
                variants.append(("current stage", invalid))
                invalid = json.loads(json.dumps(good))
                invalid.update(selected_task_id=None, current_step=None, correction_cycle=0)
                variants.append(("selected task", invalid))
                for parent in ("initialized", "finalizing", "stopped"):
                    invalid = json.loads(json.dumps(good))
                    invalid.update(state=parent, selected_task_id=None, current_step=None, correction_cycle=0)
                    variants.append((f"{parent} parent", invalid))
                for name, invalid in variants:
                    with self.subTest(profile=profile, stage=stage, state=state, mismatch=name):
                        (run_dir / "ledger.json").write_text(json.dumps(invalid))
                        before = self.snapshot(run_dir)
                        with self.assertRaises(ValueError):
                            controller.status_run(run_dir)
                        denied = load_controller().reserve_operation(run_dir, **request)
                        self.assertEqual("refused", denied["status"], denied)
                        self.assertEqual("authority_or_lock_unavailable", denied["reason"])
                        self.assertEqual(before, self.snapshot(run_dir))

    def test_terminal_assignment_retains_historical_authority(self):
        controller, run_dir = self.create_initialized_run()
        self.ready_implementation(run_dir)
        self.assertEqual("reserved", self.reserve(run_dir, "implement", "initial")["status"])
        self.seed_successor(run_dir, stage="verify", candidate_sha256="a" * 64)
        ledger = self.read_ledger(run_dir)
        operation = ledger["actor_operations"][-1]
        operation["assignment"].update(inputs_sha256="b" * 64, policy_sha256="b" * 64,
                                       flow_sha256="b" * 64, flow_revision=2, candidate_sha256="b" * 64,
                                       actor={"model": "gpt-6.1-sol", "reasoning": "low"})
        (run_dir / "ledger.json").write_text(json.dumps(ledger))
        before = self.snapshot(run_dir)
        self.assertIsNone(controller.status_run(run_dir)["operation"])
        replay = load_controller().reserve_operation(run_dir, **operation["request"])
        self.assertEqual("replayed", replay["status"])
        self.assertEqual(operation["assignment"], replay["assignment"])
        self.assertEqual(before, self.snapshot(run_dir))

    def test_separate_process_reservations_have_one_winner(self):
        controller, run_dir = self.create_initialized_run()
        script = (
            "import sys,json; from pathlib import Path; "
            f"sys.path.insert(0, {str(CONTROLLER_PATH.parent)!r}); import controller; "
            "print('ready', flush=True); sys.stdin.readline(); "
            "print(json.dumps(controller.reserve_operation(Path(sys.argv[1]), expected_version=1, "
            "task_id='T1',stage='preflight',role='preflight',operation_key=sys.argv[2])))"
        )
        processes = [subprocess.Popen([sys.executable, "-c", script, str(run_dir), key],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                     for key in ("one", "two")]
        try:
            for process in processes:
                self.assertEqual("ready\n", process.stdout.readline())
            for process in processes:
                process.stdin.write("go\n")
                process.stdin.flush()
            results = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=10)
                self.assertEqual(0, process.returncode, stderr)
                results.append(json.loads(stdout))
            self.assertEqual(["refused", "reserved"], sorted(item["status"] for item in results))
            self.assertEqual(1, len(self.read_ledger(run_dir)["actor_operations"]))
            self.assertEqual(0, controller.status_run(run_dir)["correction_count"])
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                process.wait()

    def test_shared_budget_repair_replay_restart_and_fourth_refusal(self):
        controller, run_dir = self.create_initialized_run()
        self.ready_implementation(run_dir)
        self.assertEqual(0, self.reserve(run_dir, "implement", "initial")["assignment"]["correction_count"])
        for count, reason in enumerate(("check_failed", "review_findings", "environment_repair"), 1):
            self.seed_successor(run_dir, stage="verify", correction_request=reason, candidate_sha256="a" * 64)
            request_version = self.read_ledger(run_dir)["revision"]
            result = self.reserve(run_dir, "correction", f"fix-{count}", reason)
            self.assertEqual("reserved", result["status"], result)
            assignment = result["assignment"]
            self.assertEqual(count, assignment["correction_count"])
            self.assertEqual("fresh", assignment["session_policy"])
            self.assertEqual(reason == "environment_repair", assignment["can_repair"])
            before = self.snapshot(run_dir)
            self.assertEqual("replayed", self.reserve(run_dir, "correction", f"fix-{count}", reason,
                             expected_version=request_version)["status"])
            self.assertEqual("refused", self.reserve(run_dir, "correction", "uncertain", reason)["status"])
            self.assertEqual(before, self.snapshot(run_dir))
        self.seed_successor(run_dir, stage="verify", correction_request="review_findings")
        before = self.snapshot(run_dir)
        refusal = self.reserve(run_dir, "correction", "fourth", "review_findings")
        self.assertEqual("corrections_exhausted", refusal["reason"])
        self.assertEqual(["intervene"], load_controller().status_run(run_dir)["next_actions"])
        self.assertEqual(before, self.snapshot(run_dir))
        self.assertFalse(controller.status_run(run_dir)["readiness_current"])

    def test_repair_before_initial_implementation_does_not_reset_count(self):
        controller, run_dir = self.create_initialized_run()
        self.assertEqual("reserved", self.reserve(run_dir)["status"])
        self.seed_successor(run_dir, stage="preflight", correction_request="environment_repair")
        self.assertEqual(1, self.reserve(run_dir, "correction", "repair", "environment_repair")["assignment"]["correction_count"])
        self.seed_successor(run_dir, stage="implement")
        denied = self.reserve(run_dir, "implement", "too-soon")
        self.assertEqual("current_preflight_readiness_required", denied["reason"])
        self.ready_implementation(run_dir, key="re-preflight")
        result = self.reserve(run_dir, "implement", "initial-after-repair")
        self.assertEqual("reserved", result["status"], result)
        self.assertEqual(1, result["assignment"]["correction_count"])
        for count in (2, 3):
            self.seed_successor(run_dir, stage="verify", correction_request="check_failed")
            self.assertEqual(count, self.reserve(run_dir, "correction", f"fix-{count}", "check_failed")["assignment"]["correction_count"])
        self.seed_successor(run_dir, stage="verify", correction_request="check_failed")
        self.assertEqual("corrections_exhausted", self.reserve(run_dir, "correction", "fourth", "check_failed")["reason"])

    def test_free_evidence_and_preflight_retries_never_authorize_repair(self):
        controller, run_dir = self.create_initialized_run()
        self.ready_implementation(run_dir)
        self.assertEqual("reserved", self.reserve(run_dir, "implement", "initial")["status"])
        for stage, prior in (("verify", "implement"), ("semantic_review", "verify"), ("acceptance", "semantic_review")):
            ledger = self.read_ledger(run_dir)
            evidence = {prior: {"status": "passed", "inputs_sha256": ledger["inputs_sha256"], "candidate_sha256": "a" * 64}}
            for retry in range(2):
                self.seed_successor(run_dir, stage=stage, candidate_sha256="a" * 64, evidence=evidence)
                before = self.snapshot(run_dir)
                self.assertEqual("refused", self.reserve(run_dir, stage, "repair-in-disguise", "environment_repair")["status"])
                self.assertEqual(before, self.snapshot(run_dir))
                assignment = self.reserve(run_dir, stage, f"{stage}-{retry}", "retry")["assignment"]
                self.assertEqual(0, assignment["correction_count"])
                self.assertFalse(assignment["can_change_files"])
                self.assertFalse(assignment["can_repair"])
        self.seed_successor(run_dir, stage="preflight")
        assignment = self.reserve(run_dir, key="preflight-retry", reason="retry")["assignment"]
        self.assertEqual(0, assignment["correction_count"])
        self.assertFalse(assignment["can_repair"])

    def test_invalid_requests_readiness_and_public_legacy_guards(self):
        controller, run_dir = self.create_initialized_run()
        for overrides in (dict(expected_version=0), dict(expected_version=99), dict(task_id="other"),
                          dict(role="implementer"), dict(operation_key=""), dict(stage="implement"),
                          dict(reason="environment_repair")):
            before = self.snapshot(run_dir)
            self.assertEqual("refused", self.reserve(run_dir, **overrides)["status"])
            self.assertEqual(before, self.snapshot(run_dir))
        self.ready_implementation(run_dir)
        good = self.read_ledger(run_dir)
        variants = [None]
        for field, value in (("inputs_sha256", "b" * 64), ("operation_id", "absent"),
                             ("task_id", "other"), ("status", "failed"), ("flow_sha256", "c" * 64)):
            invalid = dict(good["readiness"])
            invalid[field] = value
            variants.append(invalid)
        for readiness in variants:
            ledger = json.loads(json.dumps(good))
            ledger["readiness"] = readiness
            (run_dir / "ledger.json").write_text(json.dumps(ledger))
            before = self.snapshot(run_dir)
            self.assertEqual("current_preflight_readiness_required", self.reserve(run_dir, "implement", "denied")["reason"])
            self.assertEqual(before, self.snapshot(run_dir))
        # A nonterminal preflight record cannot grant readiness.
        ledger = json.loads(json.dumps(good))
        ledger["actor_operations"][-1]["state"] = "unknown"
        ledger["active_operation_path"] = "actor_operations/operation-001"
        ledger["current_step"] = "preflight"
        (run_dir / "ledger.json").write_text(json.dumps(ledger))
        self.assertFalse(controller.status_run(run_dir)["readiness_current"])
        # A terminal non-preflight actor is not an admitted preflight result.
        wrong_role = json.loads(json.dumps(good))
        operation = wrong_role["actor_operations"][-1]
        operation["request"].update(stage="implement", role="implementer")
        operation["assignment"].update(stage="implement", role="implementer", can_change_files=True)
        (run_dir / "ledger.json").write_text(json.dumps(wrong_role))
        self.assertFalse(controller.status_run(run_dir)["readiness_current"])
        before = self.snapshot(run_dir)
        self.assertEqual("refused", self.reserve(run_dir, "implement", "wrong-readiness-role")["status"])
        self.assertEqual(before, self.snapshot(run_dir))
        # Public run-next stays pending even with a test-seeded implement cursor.
        for ledger in (ledger, good):
            (run_dir / "ledger.json").write_text(json.dumps(ledger))
            before = self.snapshot(run_dir)
            result = subprocess.run([sys.executable, str(CONTROLLER_PATH), "run-next", "--run-dir", str(run_dir),
                                     "--timeout-seconds", "10", "--codex-bin", str(self.root / "must-not-launch")],
                                    text=True, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("pending", json.loads(result.stdout)["status"])
            self.assertEqual(before, self.snapshot(run_dir))
        # Generic ledger mutation cannot inject readiness, evidence or a counter.
        with self.assertRaisesRegex(ValueError, "controller-owned"):
            controller.update_ledger(run_dir, {"readiness": good["readiness"]}, expected_revision=good["revision"])



class ControllerInputRevisionTest(unittest.TestCase):
    # Reuse owning real-file fixtures without inheriting unrelated test cases.
    setUp = ControllerReservationTest.setUp
    tearDown = ControllerReservationTest.tearDown
    policy = ControllerReservationTest.policy
    create_initialized_run = ControllerReservationTest.create_initialized_run
    read_ledger = ControllerReservationTest.read_ledger
    seed_successor = ControllerReservationTest.seed_successor
    reserve = ControllerReservationTest.reserve
    snapshot = ControllerReservationTest.snapshot
    ready_implementation = ControllerReservationTest.ready_implementation

    def revision_request(self, run_dir, *, key="owner-revision", **changes):
        ledger = self.read_ledger(run_dir)
        if ledger.get("input_revisions"):
            prior = ledger["input_revisions"][-1]["request"]["payload"]
            payload = json.loads(json.dumps(prior))
        else:
            payload = {"policy": json.loads((run_dir / "run-policy.json").read_text()),
                       "manifest": json.loads((run_dir / "task-manifest.json").read_text()),
                       "documents": {name: item["content"] for name, item in
                                     json.loads((run_dir / "inputs.json").read_text())["documents"].items()}}
        payload["documents"]["brief"] += "\nOwner-approved requirement\n"
        request = dict(expected_version=ledger["revision"], task_id="T1", revision_key=key,
                       payload=payload)
        request.update(changes)
        self.bind_owner(request)
        return request

    def bind_owner(self, request):
        bound = {field: value for field, value in request.items() if field != "authorization"}
        request["authorization"] = dict(kind="owner_response", decision="authorize_input_revision",
                                       owner="task-owner", provenance="active-chat/response-17",
                                       request_sha256=sha256_bytes(canonical_bytes(bound).rstrip(b"\n")))

    def test_authorized_document_policy_and_scope_revisions_preserve_old_files(self):
        controller, run_dir = self.create_initialized_run()
        original = self.snapshot(run_dir)
        for index, variant in enumerate(("documents", "policy", "scope"), 1):
            request = self.revision_request(run_dir, key=f"revision-{index}")
            if variant == "policy":
                request["payload"]["documents"] = self.read_ledger(run_dir)["input_revisions"][-1]["request"]["payload"]["documents"]
                request["payload"]["policy"]["flow"] = flow_profile("strong-local")
            if variant == "scope":
                request["payload"]["manifest"]["tasks"][0]["allowed_paths"].append("new.txt")
                request["payload"]["manifest"]["tasks"][0]["required_checks"].append("python3 -m unittest new_check")
                request["payload"]["documents"]["verification"] += "\nVerify new requirement\n"
            self.bind_owner(request)
            before = self.read_ledger(run_dir)
            result = controller.revise_inputs(run_dir, request)
            self.assertEqual("revised", result["status"], result)
            ledger = self.read_ledger(run_dir)
            self.assertEqual(before["revision"] + 1, result["state_version"])
            self.assertNotEqual(before["inputs_sha256"], result["inputs_sha256"])
            self.assertEqual(before["correction_cycle"], ledger["correction_cycle"])
            self.assertEqual(index, len(ledger["input_revisions"]))
            inputs = load_controller().load_frozen_inputs(run_dir, ledger)
            policy, manifest, approved_inputs = controller.load_input_authority(run_dir, ledger)
            self.assertEqual(request["payload"]["policy"], policy)
            self.assertEqual(request["payload"]["manifest"], manifest)
            self.assertEqual(inputs, approved_inputs)
            self.assertEqual(request["payload"]["documents"]["brief"], inputs["documents"]["brief"]["content"])
            self.assertEqual(request["payload"]["documents"]["verification"], inputs["documents"]["verification"]["content"])
            for document in inputs["documents"].values():
                self.assertEqual(sha256_bytes(document["content"].encode()), document["sha256"])
            self.assertEqual(request["payload"]["manifest"]["tasks"][0]["allowed_paths"], ledger["tasks"][0]["allowed_paths"])
            self.assertEqual(request["payload"]["manifest"]["tasks"][0]["required_checks"], ledger["tasks"][0]["required_checks"])
            self.assertEqual("preflight", controller.status_run(run_dir)["stage"])
            if variant == "policy":
                self.assertEqual(2, ledger["flow_revision"])
                self.assertEqual(flow_profile("strong-local")["actor_levels"]["strong"],
                                 self.reserve(run_dir, key="strong-preflight")["assignment"]["actor"])
                self.seed_successor(run_dir, stage="preflight")
        current = self.snapshot(run_dir)
        for path, content in original.items():
            if Path(path).name != "ledger.json":
                self.assertEqual(content, current[path], path)

    def test_invalid_revision_requests_are_byte_preserving(self):
        controller, run_dir = self.create_initialized_run()
        valid = self.revision_request(run_dir)
        variants = []
        for field, value in (("authorization", None), ("expected_version", 99), ("expected_version", True),
                             ("task_id", "other"), ("revision_key", ""), ("payload", {})):
            case = json.loads(json.dumps(valid)); case[field] = value
            if field not in {"authorization", "payload"}:
                self.bind_owner(case)
            variants.append((field, case))
        for field, value in (("kind", "actor_result"), ("decision", "acknowledged"),
                             ("request_sha256", "a" * 64), ("owner", ""), ("provenance", "")):
            case = json.loads(json.dumps(valid)); case["authorization"][field] = value
            variants.append((field, case))
        for change in ("stage", "policy", "run", "repo", "task", "scope", "documents"):
            case = json.loads(json.dumps(valid))
            payload = case["payload"]
            if change == "stage": payload["policy"]["flow"]["steps"].pop()
            if change == "policy": payload["policy"]["version"] = 1
            if change == "run": payload["policy"]["run_id"] = "other"
            if change == "repo": payload["policy"]["repository"] = str(self.root)
            if change == "task": payload["policy"]["task_ids"] = ["other"]
            if change == "scope": payload["manifest"]["tasks"][0]["allowed_paths"] = ["../outside"]
            if change == "documents": payload["documents"]["brief"] = None
            self.bind_owner(case); variants.append((change, case))
        variants.extend((("prose", "Owner says go ahead"), ("empty", None)))
        for label, request in variants:
            with self.subTest(label=label):
                before = self.snapshot(run_dir)
                self.assertEqual("refused", controller.revise_inputs(run_dir, request)["status"])
                self.assertEqual(before, self.snapshot(run_dir))
        with controller.RunCommandLock(run_dir):
            before = self.snapshot(run_dir)
            self.assertEqual("authority_or_lock_unavailable", controller.revise_inputs(run_dir, valid)["reason"])
            self.assertEqual(before, self.snapshot(run_dir))
        self.assertEqual("revised", controller.revise_inputs(run_dir, valid)["status"])

    def test_active_and_completed_tasks_refuse_revision(self):
        controller, run_dir = self.create_initialized_run()
        self.assertEqual("reserved", self.reserve(run_dir)["status"])
        original = self.read_ledger(run_dir)
        for state in ("reserved", "running", "unknown"):
            ledger = json.loads(json.dumps(original))
            ledger["actor_operations"][-1]["state"] = state
            (run_dir / "ledger.json").write_bytes(canonical_bytes(ledger))
            before = self.snapshot(run_dir)
            result = controller.revise_inputs(run_dir, self.revision_request(run_dir))
            self.assertEqual(f"operation_{state}", result["reason"])
            self.assertEqual(before, self.snapshot(run_dir))
        self.seed_successor(run_dir, stage="acceptance")
        ledger = self.read_ledger(run_dir)
        ledger["tasks"][0]["state"] = "accepted"
        ledger.update(state="stopped", selected_task_id=None, current_step=None)
        ledger["completed_task_ids"] = ["T1"]
        (run_dir / "ledger.json").write_bytes(canonical_bytes(ledger))
        before = self.snapshot(run_dir)
        self.assertEqual("task_completed", controller.revise_inputs(run_dir, self.revision_request(run_dir))["reason"])
        self.assertEqual(before, self.snapshot(run_dir))

    def test_revision_invalidates_evidence_but_preserves_historical_contents(self):
        for variant in ("brief", "verification", "policy"):
            with self.subTest(variant=variant):
                controller, run_dir = self.create_initialized_run(name=f"invalidation-{variant}")
                self.ready_implementation(run_dir)
                old = self.read_ledger(run_dir)
                evidence = {stage: dict(status="passed", inputs_sha256=old["inputs_sha256"],
                                       candidate_sha256="a" * 64, reference=f"evidence/{stage}.json")
                            for stage in ("preflight", "implement", "verify", "semantic_review", "acceptance")}
                for item in evidence.values():
                    path = run_dir / item["reference"]; path.parent.mkdir(exist_ok=True)
                    path.write_bytes(canonical_bytes(item))
                self.seed_successor(run_dir, stage="implement", evidence=evidence, candidate_sha256="a" * 64,
                                    outstanding_findings=["finding-1"])
                old = self.read_ledger(run_dir)
                files = self.snapshot(run_dir)
                request = self.revision_request(run_dir)
                if variant != "brief":
                    request["payload"]["documents"]["brief"] = controller.load_frozen_inputs(run_dir, old)["documents"]["brief"]["content"]
                if variant == "verification":
                    request["payload"]["documents"]["verification"] += "\nOwner-approved verification revision\n"
                if variant == "policy":
                    request["payload"]["policy"]["flow"] = flow_profile("strong-local")
                self.bind_owner(request)
                result = controller.revise_inputs(run_dir, request)
                self.assertEqual("revised", result["status"], result)
                revised = self.read_ledger(run_dir)
                self.assertEqual(old["readiness"], revised["input_revisions"][-1]["previous"]["readiness"])
                self.assertEqual(old["actor_operations"], revised["actor_operations"])
                self.assertEqual(evidence, revised["evidence"])
                self.assertIsNone(revised["candidate_sha256"])
                self.assertIsNone(revised["readiness"])
                self.assertEqual(["finding-1"], revised["outstanding_findings"])
                for path, content in files.items():
                    if Path(path).name != "ledger.json": self.assertEqual(content, Path(path).read_bytes())
                self.assertFalse(load_controller().status_run(run_dir)["readiness_current"])
                self.assertEqual({"stale"}, {item["status"] for item in controller.status_run(run_dir)["evidence"].values()})
                # Repointing old evidence/readiness cannot make it current after reload.
                stale = json.loads(json.dumps(revised))
                stale.update(current_step="implement", readiness=old["readiness"])
                (run_dir / "ledger.json").write_bytes(canonical_bytes(stale))
                self.assertEqual("current_preflight_readiness_required", self.reserve(run_dir, "implement", "stale-ready")["reason"])
                for stage in ("verify", "semantic_review", "acceptance"):
                    self.seed_successor(run_dir, stage=stage, candidate_sha256="a" * 64)
                    self.assertEqual("successor_evidence_required", self.reserve(run_dir, stage, f"old-{stage}")["reason"])
                (run_dir / "ledger.json").write_bytes(canonical_bytes(revised))
                self.ready_implementation(run_dir, key="fresh-ready")
                self.assertEqual("reserved", self.reserve(run_dir, "implement", "fresh-implementation")["status"])

    def test_interrupted_publication_and_exact_replay(self):
        for boundary in ("before_content", "before_pointer", "after_pointer"):
            with self.subTest(boundary=boundary):
                controller, run_dir = self.create_initialized_run(name=boundary)
                request = self.revision_request(run_dir)
                old = controller.status_run(run_dir)
                old_files = self.snapshot(run_dir)
                write = controller.atomic_write_json
                def fault(path, value):
                    if boundary == "after_pointer": write(path, value)
                    raise OSError("injected publication interruption")
                target = "_write_durable_exclusive" if boundary == "before_content" else "atomic_write_json"
                with mock.patch.object(controller, target, side_effect=fault):
                    uncertain = controller.revise_inputs(run_dir, request)
                    self.assertEqual("revision_publication_uncertain", uncertain["reason"])
                    self.assertIsNone(uncertain["state_version"])
                state = load_controller().status_run(run_dir)
                self.assertEqual(old["state_version"] + int(boundary == "after_pointer"), state["state_version"])
                self.assertEqual(old["inputs_sha256"] == state["inputs_sha256"], boundary != "after_pointer")
                if boundary == "before_content": self.assertEqual(old_files, self.snapshot(run_dir))
                if boundary == "before_pointer":
                    conflicting = json.loads(json.dumps(request)); conflicting["payload"]["documents"]["brief"] += "different"
                    self.bind_owner(conflicting)
                    before = self.snapshot(run_dir)
                    self.assertEqual("pending_revision_conflict", controller.revise_inputs(run_dir, conflicting)["reason"])
                    self.assertEqual(before, self.snapshot(run_dir))
                result = load_controller().revise_inputs(run_dir, request)
                self.assertEqual("replayed" if boundary == "after_pointer" else "revised", result["status"], result)
                self.assertEqual(old["state_version"] + 1, result["state_version"])
                before = self.snapshot(run_dir)
                self.assertEqual("replayed", controller.revise_inputs(run_dir, request)["status"])
                self.assertEqual(before, self.snapshot(run_dir))
                later = self.revision_request(run_dir, key="later")
                self.assertEqual("revised", controller.revise_inputs(run_dir, later)["status"])
                before = self.snapshot(run_dir)
                self.assertEqual("replayed", load_controller().revise_inputs(run_dir, request)["status"])
                self.assertEqual(before, self.snapshot(run_dir))
                request["payload"]["documents"]["brief"] += "conflicting"
                self.bind_owner(request)
                self.assertEqual("revision_key_conflict", controller.revise_inputs(run_dir, request)["reason"])
                self.assertEqual(before, self.snapshot(run_dir))

    def test_composed_three_corrections_revision_and_legacy_guards(self):
        controller, run_dir = self.create_initialized_run()
        self.assertEqual("refused", self.reserve(run_dir, "implement", "premature")["status"])
        self.ready_implementation(run_dir)
        self.assertEqual(0, self.reserve(run_dir, "implement", "cycle-zero")["assignment"]["correction_count"])
        for count, reason in enumerate(("check_failed", "review_findings", "environment_repair"), 1):
            self.seed_successor(run_dir, stage="verify", correction_request=reason)
            version = self.read_ledger(run_dir)["revision"]
            reserved = self.reserve(run_dir, "correction", f"fix-{count}", reason)
            self.assertEqual(count, reserved["assignment"]["correction_count"])
            self.assertEqual("replayed", self.reserve(run_dir, "correction", f"fix-{count}", reason,
                                                     expected_version=version)["status"])
        self.seed_successor(run_dir, stage="implement")
        self.assertFalse(controller.status_run(run_dir)["readiness_current"])
        self.assertEqual(["reserve:preflight"], controller.status_run(run_dir)["next_actions"])
        history = self.read_ledger(run_dir)["actor_operations"]
        request = self.revision_request(run_dir)
        self.assertEqual("revised", controller.revise_inputs(run_dir, request)["status"])
        self.assertEqual(history, self.read_ledger(run_dir)["actor_operations"])
        self.assertEqual(3, load_controller().status_run(run_dir)["correction_count"])
        self.assertEqual(["reserve:preflight"], controller.status_run(run_dir)["next_actions"])
        self.ready_implementation(run_dir, key="post-revision-preflight")
        before = self.snapshot(run_dir)
        self.assertEqual("successor_admission_pending", self.reserve(run_dir, "implement", "another-cycle-zero")["reason"])
        self.assertEqual(before, self.snapshot(run_dir))
        self.seed_successor(run_dir, stage="verify", correction_request="review_findings")
        before = self.snapshot(run_dir)
        self.assertEqual("corrections_exhausted", self.reserve(run_dir, "correction", "fourth", "review_findings")["reason"])
        self.assertEqual(before, self.snapshot(run_dir))
        # Public legacy entry points cannot manufacture the missing successor evidence.
        self.assertEqual("successor_inspection_pending", controller.inspect_run(run_dir, 10)["reason"])
        command = [sys.executable, str(CONTROLLER_PATH), "run-next", "--run-dir", str(run_dir), "--timeout-seconds", "10"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual("pending", json.loads(result.stdout)["status"], result.stderr)
        path = self.root / "flow.json"; path.write_bytes(canonical_bytes(flow_profile("strong-local")))
        with self.assertRaisesRegex(ValueError, "safe task boundary"):
            controller.revise_flow(run_dir, path)
        for updater in ({"correction_cycle": 0}, {"readiness": {}}, {"input_revisions": []}):
            with self.assertRaises(ValueError):
                controller.update_ledger(run_dir, updater, expected_revision=self.read_ledger(run_dir)["revision"])
        self.assertEqual(before, self.snapshot(run_dir))

    def test_process_exit_during_publication_preserves_charge_and_releases_lock(self):
        for committed in (False, True):
            with self.subTest(committed=committed):
                controller, run_dir = self.create_initialized_run(name=f"process-exit-{committed}")
                self.assertEqual("reserved", self.reserve(run_dir, key="initial-preflight")["status"])
                self.seed_successor(run_dir, stage="preflight", correction_request="environment_repair")
                self.assertEqual(1, self.reserve(run_dir, "correction", "repair", "environment_repair")["assignment"]["correction_count"])
                self.seed_successor(run_dir, stage="preflight")
                old = self.read_ledger(run_dir)
                request = self.revision_request(run_dir)
                path = self.root / "exit-request.json"; path.write_bytes(canonical_bytes(request))
                script = (
                    "import sys, os, json; from pathlib import Path; "
                    f"sys.path.insert(0, {str(CONTROLLER_PATH.parent)!r}); import controller; "
                    "write = controller.atomic_write_json\n"
                    "def interrupt(path, value):\n"
                    f"    if {committed!r}: write(path, value)\n"
                    "    os._exit(23)\n"
                    "controller.atomic_write_json = interrupt\n"
                    "controller.revise_inputs(Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()))\n"
                )
                result = subprocess.run([sys.executable, "-c", script, str(run_dir), str(path)],
                                        text=True, capture_output=True, timeout=10)
                self.assertEqual(23, result.returncode, result.stderr)
                status = load_controller().status_run(run_dir)
                self.assertEqual(old["revision"] + int(committed), status["state_version"])
                self.assertEqual(1, status["correction_count"])
                self.assertEqual(old["actor_operations"], status["operation_history"])
                self.assertFalse(status["readiness_current"])
                retried = controller.revise_inputs(run_dir, request)
                self.assertEqual("replayed" if committed else "revised", retried["status"], retried)
                self.assertEqual(old["revision"] + 1, self.read_ledger(run_dir)["revision"])
                self.assertEqual(1, self.read_ledger(run_dir)["correction_cycle"])

    def test_cli_revision_uses_explicit_request_file(self):
        controller, run_dir = self.create_initialized_run()
        request = self.revision_request(run_dir)
        path = self.root / "owner-request.json"; path.write_bytes(canonical_bytes(request))
        command = [sys.executable, str(CONTROLLER_PATH), "revise-inputs", "--run-dir", str(run_dir), "--request", str(path)]
        result = subprocess.run(command, text=True, capture_output=True, timeout=10)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("revised", json.loads(result.stdout)["status"])
        before = self.snapshot(run_dir)
        result = subprocess.run(command, text=True, capture_output=True, timeout=10)
        self.assertEqual("replayed", json.loads(result.stdout)["status"])
        self.assertEqual(before, self.snapshot(run_dir))


class ControllerInspectionIntegrationTest(unittest.TestCase):
    setUp = ControllerIntegrationTest.setUp
    tearDown = ControllerIntegrationTest.tearDown
    policy = ControllerIntegrationTest.policy
    write_fake_codex = ControllerIntegrationTest.write_fake_codex

    def create_clean_inspection_run(
        self, *, targeted="/usr/bin/true", repository_gate=None, authorized_gap=None,
        stop_overrides=None, flow=None,
    ):
        controller = load_controller()
        run_dir = self.root / "runs" / "run-clean-inspect"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"
        policy = self.policy()
        policy["verification"]["targeted_checks"] = [targeted]
        policy["verification"]["repository_gate"] = repository_gate
        policy["verification"]["authorized_gap"] = authorized_gap
        policy["stop_policy"].update(stop_overrides or {})
        if flow is not None:
            policy["flow"] = flow
        controller.persist_run_policy(policy_path, policy)
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps({
            "version": 1,
            "manifest_id": "clean-inspect",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": [targeted],
            }],
        }, indent=2, sort_keys=True) + "\n")
        controller.init_run(run_dir, policy_path, manifest_path, self.repo)
        stage_transport_fixture(run_dir)
        fake = self.write_fake_codex(created_paths=(), clean_mutation=True)
        result = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        return controller, run_dir

    def test_verify_off_profile_is_refused_before_execution(self):
        verify_off = flow_profile()
        verify_off["steps"] = [
            step for step in verify_off["steps"] if step["kind"] != "verify"
        ]
        with mock.patch.object(
            load_controller()._verification_module, "execute_verification_plan",
            side_effect=AssertionError("weak profile reached command execution"),
        ) as execute:
            with self.assertRaisesRegex(ValueError, "mandatory stage"):
                self.create_clean_inspection_run(flow=verify_off)
        execute.assert_not_called()
        self.assertFalse((self.root / "runs/run-clean-inspect").exists())

    def test_targeted_verification_excludes_configured_repository_gate(self):
        targeted = flow_profile()
        targeted["steps"][3]["mode"] = "targeted"
        controller, run_dir = self.create_clean_inspection_run(
            targeted="/usr/bin/true",
            repository_gate="/usr/bin/false",
            flow=targeted,
        )

        class ExpectedPlan(Exception):
            pass

        def inspect_plan(*, plan, **_kwargs):
            self.assertEqual(
                [["/usr/bin/true"]],
                [command["argv"] for command in plan["commands"]],
            )
            self.assertEqual(
                [["task_required", "policy_targeted"]],
                [command["roles"] for command in plan["commands"]],
            )
            raise ExpectedPlan

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=inspect_plan,
        ):
            with self.assertRaises(ExpectedPlan):
                controller.inspect_run(run_dir, 10)

    def test_repository_gate_mode_requires_persisted_repository_gate(self):
        with_gate = flow_profile()
        with_gate["steps"][3]["mode"] = "targeted_plus_repository_gate"
        controller, run_dir = self.create_clean_inspection_run(
            repository_gate=None,
            flow=with_gate,
        )
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("invalid verification mode reached execution"),
        ) as execute:
            with self.assertRaisesRegex(ValueError, "repository gate"):
                controller.inspect_run(run_dir, 10)

        execute.assert_not_called()
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_inspect_keeps_pending_semantic_review_non_accepting(self):
        pending_review = flow_profile("reviewed")
        pending_review["profile"] = "review-only"
        controller, run_dir = self.create_clean_inspection_run(
            flow=pending_review
        )

        result = controller.inspect_run(run_dir, 10)

        decision = json.loads(Path(result["decision_path"]).read_text())
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("semantic_review", ledger["current_step"])
        self.assertFalse(
            result["accepted"],
            "mechanical eligibility crossed a pending semantic-review boundary",
        )
        self.assertNotIn("accept", result["allowed_actions"])
        self.assertFalse(decision["accepted"])
        self.assertNotIn("accepted", decision["allowed_transitions"])
        self.assertEqual("not_collected", decision["semantic_review"])

    def test_durable_adapter_command_actor_mismatch_fails_before_inspection(self):
        controller, run_dir = self.create_clean_inspection_run()
        attempt_dir = run_dir / "attempts/attempt-001"
        state_path = attempt_dir / "state.json"
        terminal_path = attempt_dir / "turn-001.result.state.json"
        state = json.loads(state_path.read_text())
        state["effective_command"] = [
            'model_reasoning_effort="high"'
            if item == 'model_reasoning_effort="medium"' else item
            for item in state["effective_command"]
        ]
        state_bytes = (
            json.dumps(state, indent=2, sort_keys=True) + "\n"
        ).encode()
        state_path.write_bytes(state_bytes)
        terminal_path.write_bytes(state_bytes)

        ledger_path = run_dir / "ledger.json"
        ledger = json.loads(ledger_path.read_text())
        closure_path = run_dir / ledger["last_closure_path"]
        closure = json.loads(closure_path.read_text())
        closure["adapter_state_digest"] = controller.sha256_text(
            controller.canonical_json(state)
        )
        closure["worker_claims"]["effective_command"] = state["effective_command"]
        closure_bytes = (
            json.dumps(closure, indent=2, sort_keys=True) + "\n"
        ).encode()
        closure_path.write_bytes(closure_bytes)
        ledger["last_closure_sha256"] = sha256_bytes(closure_bytes)
        ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("actor mismatch reached verification"),
        ) as execute:
            with self.assertRaisesRegex(ValueError, "adapter command actor"):
                controller.inspect_run(run_dir, 10)

        execute.assert_not_called()
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_inspect_rejects_preexisting_decision_before_execution_or_publication(self):
        controller, run_dir = self.create_clean_inspection_run()
        execution_path = run_dir / "verification/attempt-001.turn-001.execution.json"
        verification_path = run_dir / "verification/attempt-001.turn-001.json"
        decision_path = run_dir / "decisions/attempt-001.turn-001.json"
        decision_path.write_bytes(b"{}\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError(
                "pre-existing contradictory decision reached verification execution"
            ),
        ) as execute:
            with self.assertRaises(ValueError):
                controller.inspect_run(run_dir, 10)

        execute.assert_not_called()
        self.assertFalse(execution_path.exists())
        self.assertFalse(verification_path.exists())
        self.assertEqual(b"{}\n", decision_path.read_bytes())
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_inspect_rejects_same_path_same_size_preverification_drift_without_execution(self):
        controller = load_controller()
        run_dir = self.root / "runs" / "run-inspect-drift"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"
        marker_path = self.repo / "verification-executed"
        verifier = self.repo / "verify-marker"
        verifier.write_text(
            "#!/bin/sh\nprintf executed > verification-executed\n"
        )
        verifier.chmod(0o755)
        subprocess.run(["git", "-C", str(self.repo), "add", "verify-marker"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-qm", "add verifier"], check=True
        )

        policy = self.policy()
        policy["verification"]["targeted_checks"] = ["./verify-marker"]
        policy["verification"]["repository_gate"] = None
        controller.persist_run_policy(policy_path, policy)
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps({
            "version": 1,
            "manifest_id": "inspect-drift",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": ["./verify-marker"],
            }],
        }, indent=2, sort_keys=True) + "\n")
        controller.init_run(run_dir, policy_path, manifest_path, self.repo)
        stage_transport_fixture(run_dir)
        fake = self.write_fake_codex(created_paths=(), clean_mutation=True)
        run_result = subprocess.run([
            *LEGACY_CONTROLLER, "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)
        self.assertEqual(0, run_result.returncode, run_result.stderr)

        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*")
            if path.is_file()
        }
        self.assertEqual(14, len((self.repo / "allowed.txt").read_bytes()))
        (self.repo / "allowed.txt").write_text("drifted bytes\n")

        inspection = subprocess.run([
            sys.executable, str(CONTROLLER_PATH), "inspect",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
        ], text=True, capture_output=True)

        self.assertNotEqual(0, inspection.returncode)
        self.assertIn("Workspace identity changed before verification", inspection.stderr)
        self.assertFalse(marker_path.exists())
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*")
                if path.is_file()
            },
        )

    def test_inspect_reuses_execution_after_crash_with_review_pending(self):
        controller, run_dir = self.create_clean_inspection_run()
        ledger_before = json.loads((run_dir / "ledger.json").read_text())
        closure = json.loads((run_dir / ledger_before["last_closure_path"]).read_text())
        self.assertEqual(closure["head_after"], closure["head_before"])
        self.assertEqual(closure["index_tree"], closure["controller_observations"]["index_tree"])
        self.assertRegex(closure["post_worker_status_sha256"], r"^[0-9a-f]{64}$")

        original_capture = controller._git_module.capture_workspace_identity
        capture_count = 0

        def fail_after_execution(repository):
            nonlocal capture_count
            capture_count += 1
            if capture_count == 2:
                raise RuntimeError("injected crash after execution publication")
            return original_capture(repository)

        with mock.patch.object(
            controller._git_module,
            "capture_workspace_identity",
            side_effect=fail_after_execution,
        ):
            with self.assertRaisesRegex(RuntimeError, "injected crash"):
                controller.inspect_run(run_dir, 10)

        execution_path = run_dir / "verification/attempt-001.turn-001.execution.json"
        self.assertTrue(execution_path.is_file())
        self.assertFalse((run_dir / "verification/attempt-001.turn-001.json").exists())
        self.assertFalse((run_dir / "decisions/attempt-001.turn-001.json").exists())
        self.assertEqual(
            ledger_before,
            json.loads((run_dir / "ledger.json").read_text()),
        )
        execution_bytes = execution_path.read_bytes()

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("verification command was rerun"),
        ):
            result = controller.inspect_run(run_dir, 10)

        self.assertFalse(result["accepted"])
        self.assertEqual(["stop"], result["allowed_actions"])
        self.assertEqual(execution_bytes, execution_path.read_bytes())
        verification = json.loads(Path(result["verification_path"]).read_text())
        decision = json.loads(Path(result["decision_path"]).read_text())
        self.assertEqual("passed", verification["outcome"])
        self.assertEqual([], verification["drift_findings"])
        self.assertFalse(decision["accepted"])
        self.assertEqual("not_collected", decision["semantic_review"])
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("awaiting_inspection", ledger["state"])
        self.assertEqual("awaiting_inspection", ledger["tasks"][0]["state"])
        self.assertEqual(
            "verification/attempt-001.turn-001.json",
            ledger["last_verification_path"],
        )
        self.assertEqual(
            "decisions/attempt-001.turn-001.json",
            ledger["last_decision_path"],
        )

        completed_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*")
            if path.is_file()
        }
        replay = controller.inspect_run(run_dir, 10)
        self.assertFalse(replay["accepted"])
        self.assertEqual(
            completed_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*")
                if path.is_file()
            },
        )

    def test_inspect_recovers_after_execution_drift_and_crash_before_final_record(self):
        verifier = self.repo / "verify-drift"
        verifier.write_text(
            "#!/bin/sh\nprintf 'verification drift\\n' > allowed.txt\n"
        )
        verifier.chmod(0o755)
        subprocess.run(["git", "-C", str(self.repo), "add", "verify-drift"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-qm", "add drift verifier"],
            check=True,
        )
        controller, run_dir = self.create_clean_inspection_run(
            targeted="./verify-drift"
        )
        original_capture = controller._git_module.capture_workspace_identity
        capture_count = 0

        def fail_after_execution(repository):
            nonlocal capture_count
            capture_count += 1
            if capture_count == 2:
                raise RuntimeError("injected crash after drift execution")
            return original_capture(repository)

        with mock.patch.object(
            controller._git_module,
            "capture_workspace_identity",
            side_effect=fail_after_execution,
        ), mock.patch.object(
            controller._verification_module,
            "build_sandbox_invocation",
            side_effect=lambda argv, permissions: list(argv),
        ):
            with self.assertRaisesRegex(RuntimeError, "injected crash after drift"):
                controller.inspect_run(run_dir, 10)

        execution_path = run_dir / "verification/attempt-001.turn-001.execution.json"
        self.assertTrue(execution_path.is_file())
        self.assertFalse((run_dir / "verification/attempt-001.turn-001.json").exists())
        execution_bytes = execution_path.read_bytes()

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("verification command was rerun"),
        ):
            result = controller.inspect_run(run_dir, 10)

        self.assertFalse(result["accepted"])
        self.assertEqual(execution_bytes, execution_path.read_bytes())
        verification = json.loads(Path(result["verification_path"]).read_text())
        self.assertEqual("failed", verification["outcome"])
        self.assertEqual(
            ["verification changed workspace content or paths"],
            verification["drift_findings"],
        )
        decision = json.loads(Path(result["decision_path"]).read_text())
        self.assertEqual(["stop"], decision["allowed_actions"])
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("awaiting_inspection", ledger["state"])
        self.assertEqual(
            "verification/attempt-001.turn-001.json",
            ledger["last_verification_path"],
        )
        self.assertEqual(
            "decisions/attempt-001.turn-001.json",
            ledger["last_decision_path"],
        )

    def test_inspect_rejects_historical_unanchored_closure(self):
        controller, run_dir = self.create_clean_inspection_run()
        ledger = json.loads((run_dir / "ledger.json").read_text())
        closure_path = run_dir / ledger["last_closure_path"]
        closure = json.loads(closure_path.read_text())
        closure.pop("post_worker_status_sha256")
        evidence_record = {
            "policy_sha256": closure["policy_sha256"],
            "manifest_sha256": closure["manifest_sha256"],
            "baseline_sha256": closure["baseline_sha256"],
            "prompt_sha256": closure["prompt_sha256"],
            "head_before": closure["head_before"],
            "head_after": closure["head_after"],
            "index_tree_before": json.loads(
                (run_dir / "baselines/task-001.json").read_text()
            )["index_tree"],
            "index_tree_after": closure["index_tree"],
            "artifact_digests": {
                name: artifact["sha256"]
                for name, artifact in closure["evidence_artifacts"].items()
            },
            "untracked_paths": closure["untracked_paths"],
            "adapter_state_digest": closure["adapter_state_digest"],
        }
        closure["evidence_digest"] = controller.sha256_text(
            controller.canonical_json(evidence_record)
        )
        closure["identity"]["evidence_digest"] = closure["evidence_digest"]
        closure_path.write_text(json.dumps(closure, indent=2, sort_keys=True) + "\n")
        ledger.pop("last_closure_sha256")
        (run_dir / "ledger.json").write_text(
            json.dumps(ledger, indent=2, sort_keys=True) + "\n"
        )
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("historical closure reached execution"),
        ):
            with self.assertRaisesRegex(ValueError, "exact closure digest"):
                controller.inspect_run(run_dir, 10)

        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_worker_result_task_identity_tamper_stops_before_verification(self):
        controller, run_dir = self.create_clean_inspection_run()
        result_path = run_dir / "attempts/attempt-001/turn-001.result.json"
        worker_result = json.loads(result_path.read_text())
        worker_result["task_id"] = "TAMPERED"
        result_path.write_text(json.dumps(worker_result, indent=2, sort_keys=True) + "\n")

        ledger = json.loads((run_dir / "ledger.json").read_text())
        closure_path = run_dir / ledger["last_closure_path"]
        closure = json.loads(closure_path.read_text())
        closure["worker_claims"]["result"] = worker_result
        closure_path.write_text(json.dumps(closure, indent=2, sort_keys=True) + "\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("tampered worker result reached verification"),
        ):
            with self.assertRaisesRegex(ValueError, "worker result task id"):
                controller.inspect_run(run_dir, 10)

        self.assertFalse(
            (run_dir / "verification/attempt-001.turn-001.execution.json").exists()
        )
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_coherent_worker_result_tamper_stops_before_verification(self):
        controller, run_dir = self.create_clean_inspection_run()
        result_path = run_dir / "attempts/attempt-001/turn-001.result.json"
        worker_result = json.loads(result_path.read_text())
        worker_result["summary"] = "coherently tampered"
        result_path.write_text(json.dumps(worker_result, indent=2, sort_keys=True) + "\n")

        ledger = json.loads((run_dir / "ledger.json").read_text())
        closure_path = run_dir / ledger["last_closure_path"]
        closure = json.loads(closure_path.read_text())
        closure["worker_claims"]["result"] = worker_result
        closure_path.write_text(json.dumps(closure, indent=2, sort_keys=True) + "\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("tampered worker result reached verification"),
        ):
            with self.assertRaises(ValueError):
                controller.inspect_run(run_dir, 10)

        self.assertFalse(
            (run_dir / "verification/attempt-001.turn-001.execution.json").exists()
        )
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_semantically_equal_worker_result_rewrite_stops_before_verification(self):
        controller, run_dir = self.create_clean_inspection_run()
        result_path = run_dir / "attempts/attempt-001/turn-001.result.json"
        worker_result = json.loads(result_path.read_text())
        result_path.write_text(json.dumps(worker_result, sort_keys=True) + "\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("rewritten worker result reached verification"),
        ):
            with self.assertRaisesRegex(ValueError, "Worker result bytes"):
                controller.inspect_run(run_dir, 10)

        self.assertFalse(
            (run_dir / "verification/attempt-001.turn-001.execution.json").exists()
        )
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_attempt_record_prompt_tamper_stops_before_verification(self):
        controller, run_dir = self.create_clean_inspection_run()
        attempt_path = run_dir / "attempts/attempt-001/record.json"
        attempt = json.loads(attempt_path.read_text())
        attempt["prompt"] = "tampered embedded prompt"
        attempt_path.write_text(json.dumps(attempt, indent=2, sort_keys=True) + "\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("tampered attempt prompt reached verification"),
        ):
            with self.assertRaisesRegex(ValueError, "prompt"):
                controller.inspect_run(run_dir, 10)

        self.assertFalse(
            (run_dir / "verification/attempt-001.turn-001.execution.json").exists()
        )
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_attempt_record_model_tamper_stops_before_verification(self):
        controller, run_dir = self.create_clean_inspection_run()
        attempt_path = run_dir / "attempts/attempt-001/record.json"
        attempt = json.loads(attempt_path.read_text())
        attempt["model"] = "tampered-model"
        attempt_path.write_text(json.dumps(attempt, indent=2, sort_keys=True) + "\n")
        run_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("tampered attempt record reached verification"),
        ) as execute:
            with self.assertRaises(ValueError):
                controller.inspect_run(run_dir, 10)

        execute.assert_not_called()
        self.assertFalse(
            (run_dir / "verification/attempt-001.turn-001.execution.json").exists()
        )
        self.assertEqual(
            run_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_repository_gate_authorized_gap_preserves_pending_review(self):
        gap = {
            "reason": "Known repository-only failure",
            "owner": "test-owner",
            "follow_up": "Resolve after this bounded task",
        }
        with_gate = flow_profile()
        with_gate["steps"][3]["mode"] = "targeted_plus_repository_gate"
        controller, run_dir = self.create_clean_inspection_run(
            repository_gate="/usr/bin/false", authorized_gap=gap,
            flow=with_gate,
        )

        result = controller.inspect_run(run_dir, 10)

        self.assertFalse(result["accepted"])
        decision = json.loads(Path(result["decision_path"]).read_text())
        execution = json.loads(
            (run_dir / "verification/attempt-001.turn-001.execution.json").read_text()
        )
        self.assertEqual("authorized_gap", execution["terminal_reason"])
        self.assertEqual(gap, decision["gap_details"])
        self.assertEqual(["stop"], decision["allowed_actions"])

    def test_authorized_gap_cannot_excuse_a_targeted_failure(self):
        gap = {
            "reason": "Repository exception",
            "owner": "test-owner",
            "follow_up": "Resolve later",
        }
        with_gate = flow_profile()
        with_gate["steps"][3]["mode"] = "targeted_plus_repository_gate"
        controller, run_dir = self.create_clean_inspection_run(
            targeted="/usr/bin/false",
            repository_gate="/usr/bin/false",
            authorized_gap=gap,
            flow=with_gate,
        )

        result = controller.inspect_run(run_dir, 10)

        self.assertFalse(result["accepted"])
        decision = json.loads(Path(result["decision_path"]).read_text())
        execution = json.loads(
            (run_dir / "verification/attempt-001.turn-001.execution.json").read_text()
        )
        self.assertEqual("command_failed", execution["terminal_reason"])
        self.assertIsNone(decision["gap_details"])
        self.assertEqual(["stop"], decision["allowed_actions"])
        self.assertTrue(any("targeted verification" in reason for reason in decision["reasons"]))

    def test_verifier_created_content_drift_is_recorded_and_denies_accept(self):
        verifier = self.repo / "verify-drift"
        verifier.write_text(
            "#!/bin/sh\nprintf 'verification drift\\n' > allowed.txt\n"
        )
        verifier.chmod(0o755)
        subprocess.run(["git", "-C", str(self.repo), "add", "verify-drift"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-qm", "add drift verifier"],
            check=True,
        )
        controller, run_dir = self.create_clean_inspection_run(
            targeted="./verify-drift"
        )

        result = controller.inspect_run(run_dir, 10)

        self.assertFalse(result["accepted"])
        verification = json.loads(Path(result["verification_path"]).read_text())
        decision = json.loads(Path(result["decision_path"]).read_text())
        self.assertEqual("failed", verification["outcome"])
        self.assertEqual(
            ["verification changed workspace content or paths"],
            verification["drift_findings"],
        )
        self.assertNotIn("accept", decision["allowed_actions"])
        self.assertEqual(["stop"], decision["allowed_actions"])
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("awaiting_inspection", ledger["state"])
        self.assertEqual("awaiting_inspection", ledger["tasks"][0]["state"])

    def test_verifier_created_drift_replay_reuses_published_records(self):
        verifier = self.repo / "verify-drift"
        verifier.write_text(
            "#!/bin/sh\nprintf 'verification drift\\n' > allowed.txt\n"
        )
        verifier.chmod(0o755)
        subprocess.run(["git", "-C", str(self.repo), "add", "verify-drift"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-qm", "add drift verifier"],
            check=True,
        )
        controller, run_dir = self.create_clean_inspection_run(
            targeted="./verify-drift"
        )
        first = controller.inspect_run(run_dir, 10)
        self.assertFalse(first["accepted"])
        completed_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("verification command was rerun"),
        ):
            replay = controller.inspect_run(run_dir, 10)

        self.assertEqual(first, replay)
        self.assertEqual(
            completed_bytes,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )

    def test_failed_verification_offers_resume_only_when_policy_escalates(self):
        controller, run_dir = self.create_clean_inspection_run(
            targeted="/usr/bin/false",
            stop_overrides={"on_failed": "escalate"},
        )

        result = controller.inspect_run(run_dir, 10)

        self.assertFalse(result["accepted"])
        decision = json.loads(Path(result["decision_path"]).read_text())
        self.assertEqual(["resume", "stop"], decision["allowed_actions"])
        self.assertEqual(["resumable", "stopped"], decision["allowed_transitions"])

    def test_invalid_timeout_lock_contention_and_wrong_state_do_not_execute_or_mutate(self):
        controller, run_dir = self.create_clean_inspection_run()

        def snapshot():
            return {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            }

        original = snapshot()
        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("rejected inspect reached execution"),
        ):
            with self.assertRaisesRegex(ValueError, "timeout"):
                controller.inspect_run(run_dir, 0)
        self.assertEqual(original, snapshot())

        lock_stream = (run_dir / "controller.lock").open("a+")
        try:
            fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(ValueError, "owns this run's mutation phase"):
                controller.inspect_run(run_dir, 10)
        finally:
            fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)
            lock_stream.close()
        self.assertEqual(original, snapshot())

        ledger_path = run_dir / "ledger.json"
        ledger = json.loads(ledger_path.read_text())
        ledger["state"] = "ready"
        ledger["selected_task_id"] = None
        ledger["tasks"][0]["state"] = "ready"
        ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
        wrong_state = snapshot()
        with mock.patch.object(
            controller._verification_module,
            "execute_verification_plan",
            side_effect=AssertionError("wrong state reached execution"),
        ):
            with self.assertRaisesRegex(ValueError, "awaiting_inspection"):
                controller.inspect_run(run_dir, 10)
        self.assertEqual(wrong_state, snapshot())

    def test_inspect_replay_rejects_nonfinite_timeout(self):
        controller, run_dir = self.create_clean_inspection_run()
        with mock.patch.object(
            controller._verification_module,
            "build_sandbox_invocation",
            side_effect=lambda argv, permissions: list(argv),
        ):
            controller.inspect_run(run_dir, 10)
        completed_bytes = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }

        for invalid_timeout in (float("nan"), float("inf")):
            with self.subTest(timeout=invalid_timeout):
                with self.assertRaises(ValueError):
                    controller.inspect_run(run_dir, invalid_timeout)
                self.assertEqual(
                    completed_bytes,
                    {
                        path.relative_to(run_dir): path.read_bytes()
                        for path in run_dir.rglob("*") if path.is_file()
                    },
                )

    def test_ready_run_rejection_does_not_create_the_controller_lock(self):
        controller = load_controller()
        run_dir = self.root / "runs" / "ready-run"
        policy_path = self.root / "ready-policy.json"
        manifest_path = self.root / "ready-manifest.json"
        policy = self.policy()
        policy["verification"]["targeted_checks"] = ["/usr/bin/true"]
        policy["verification"]["repository_gate"] = None
        controller.persist_run_policy(policy_path, policy)
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps({
            "version": 1,
            "manifest_id": "ready-rejection",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1", "title": "Test task", "brief_path": "tasks/T1.md",
                "dependencies": [], "allowed_paths": ["allowed.txt"],
                "required_checks": ["/usr/bin/true"],
            }],
        }, indent=2, sort_keys=True) + "\n")
        controller.init_run(run_dir, policy_path, manifest_path, self.repo)
        before = {
            path.relative_to(run_dir): path.read_bytes()
            for path in run_dir.rglob("*") if path.is_file()
        }
        self.assertFalse((run_dir / "controller.lock").exists())

        with self.assertRaisesRegex(ValueError, "awaiting_inspection"):
            controller.inspect_run(run_dir, 10)

        self.assertFalse((run_dir / "controller.lock").exists())
        self.assertEqual(
            before,
            {
                path.relative_to(run_dir): path.read_bytes()
                for path in run_dir.rglob("*") if path.is_file()
            },
        )
