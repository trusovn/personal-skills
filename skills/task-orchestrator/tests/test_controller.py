import fcntl
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock


CONTROLLER_PATH = Path(__file__).parents[1] / "scripts" / "controller.py"


def load_controller():
    spec = importlib.util.spec_from_file_location("task_orchestrator_controller", CONTROLLER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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
            "version": 1,
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
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        with self.assertRaises(ValueError) as ctx:
            controller.init_run(
                run_dir=run_dir,
                policy_path=policy_path,
                manifest_path=manifest_path,
                repository=self.repo,
            )
        self.assertIn("depends on T99", ctx.exception.args[0])

    def test_select_task_returns_first_ready_in_policy_order(self):
        """select_task must return the first ready task in policy.task_ids order."""
        controller = load_controller()
        run_dir = self.root / "runs" / "run-003"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"

        policy = self.policy()
        policy["task_ids"] = ["T2", "T1", "T3"]
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
        # T2 comes before T1 in policy order, so T2 is selected
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
        policy["task_ids"] = ["T1", "T2"]
        controller.persist_run_policy(policy_path, policy)

        manifest = {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
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
        ledger_path = run_dir / "ledger.json"
        ledger_before = ledger_path.read_bytes()
        baseline_paths_before = sorted(
            path.relative_to(run_dir) for path in (run_dir / "baselines").iterdir()
        )

        run_next_command = [
            sys.executable, str(CONTROLLER_PATH), "run-next",
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
                sys.executable, str(CONTROLLER_PATH), "run-next",
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
        controller = load_controller()
        run_dir = self.root / "locked-run"
        run_dir.mkdir()
        ledger_path = run_dir / "ledger.json"
        ledger_path.write_text("{}\n")
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
            "version": 1,
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

    def test_post_acceptance_run_next_launches_next_ready_task(self):
        controller = load_controller()
        run_dir = self.root / "runs" / "run-accepted-next"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"
        policy = self.policy()
        policy["task_ids"] = ["T1", "T2"]
        controller.persist_run_policy(policy_path, policy)
        (self.repo / "tasks").mkdir()
        for task_id in ("T1", "T2"):
            (self.repo / "tasks" / f"{task_id}.md").write_text(f"# {task_id}\n")
        manifest_path.write_text(json.dumps({
            "version": 1,
            "manifest_id": "accepted-next",
            "completed_task_ids": [],
            "tasks": [
                {
                    "id": "T1", "title": "First", "brief_path": "tasks/T1.md",
                    "dependencies": [], "allowed_paths": ["allowed.txt"],
                    "required_checks": ["python3 -m unittest test_targeted"],
                },
                {
                    "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
                    "dependencies": ["T1"], "allowed_paths": ["allowed.txt"],
                    "required_checks": ["python3 -m unittest test_targeted"],
                },
            ],
        }, indent=2, sort_keys=True) + "\n")
        init_result = subprocess.run([
            sys.executable, str(CONTROLLER_PATH), "init",
            "--run-dir", str(run_dir), "--policy", str(policy_path),
            "--manifest", str(manifest_path), "--repository", str(self.repo),
        ], text=True, capture_output=True)
        self.assertEqual(0, init_result.returncode, init_result.stderr)

        fake = self.write_fake_codex(
            created_paths=(), clean_mutation=True, task_id="T1",
        )
        first = subprocess.run([
            sys.executable, str(CONTROLLER_PATH), "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)
        self.assertEqual(0, first.returncode, first.stderr)
        ledger = json.loads((run_dir / "ledger.json").read_text())
        first_attempt = ledger["tasks"][0]["attempt_ids"][-1]
        controller.update_ledger(run_dir, {
            "state": "finalizing",
            "last_verification_path": "verification/attempt-001.json",
            "last_decision_path": "decisions/attempt-001.json",
            "active_operation_path": "operations/T1-accept.json",
        }, expected_revision=ledger["revision"])
        ledger = json.loads((run_dir / "ledger.json").read_text())
        released_tasks = [dict(task) for task in ledger["tasks"]]
        released_tasks[0]["state"] = "accepted"
        released_tasks[1]["state"] = "ready"
        controller.update_ledger(run_dir, {
            "state": "ready", "selected_task_id": None,
            "active_operation_path": None, "tasks": released_tasks,
        }, expected_revision=ledger["revision"], closure_decision={
            "accepted": True,
            "allowed_transitions": ["accepted"],
            "identity": {
                "run_id": "run-1", "task_id": "T1", "attempt_id": first_attempt,
            },
        })

        fake = self.write_fake_codex(
            created_paths=(), clean_mutation=True, task_id="T2",
        )
        second_command = [
            sys.executable, str(CONTROLLER_PATH), "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ]
        accepted_bytes = (self.repo / "allowed.txt").read_bytes()
        ledger_before_drift = (run_dir / "ledger.json").read_bytes()
        baseline_paths_before_drift = sorted((run_dir / "baselines").iterdir())
        attempt_paths_before_drift = sorted((run_dir / "attempts").iterdir())
        invocation_log = self.root / "argv.json"
        invocations_before_drift = invocation_log.read_bytes()
        (self.repo / "allowed.txt").write_text("later ordinary drift\n")
        drift = subprocess.run(second_command, text=True, capture_output=True)
        self.assertNotEqual(0, drift.returncode)
        self.assertIn("Repository bytes changed after acceptance", drift.stderr)
        self.assertEqual(ledger_before_drift, (run_dir / "ledger.json").read_bytes())
        self.assertEqual(baseline_paths_before_drift, sorted((run_dir / "baselines").iterdir()))
        self.assertEqual(attempt_paths_before_drift, sorted((run_dir / "attempts").iterdir()))
        self.assertEqual(invocations_before_drift, invocation_log.read_bytes())

        (self.repo / "allowed.txt").write_bytes(accepted_bytes)
        second = subprocess.run(second_command, text=True, capture_output=True)
        self.assertEqual(0, second.returncode, second.stderr)
        ledger = json.loads((run_dir / "ledger.json").read_text())
        self.assertEqual("T2", ledger["selected_task_id"])
        self.assertEqual("awaiting_inspection", ledger["tasks"][1]["state"])
        self.assertEqual(2, sum(len(task["attempt_ids"]) for task in ledger["tasks"]))

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

        # Run next
        run_result = subprocess.run(
            [
                sys.executable, str(CONTROLLER_PATH), "run-next",
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
            sorted([*created_paths, "tasks/T1.md"]),
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
        command = [
            sys.executable, str(CONTROLLER_PATH), "run-next",
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
                    "tasks": stopped_tasks,
                }, expected_revision=running["revision"])
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

        result = subprocess.run(
            [
                sys.executable, str(CONTROLLER_PATH), "run-next",
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


class ControllerInspectionIntegrationTest(unittest.TestCase):
    setUp = ControllerIntegrationTest.setUp
    tearDown = ControllerIntegrationTest.tearDown
    policy = ControllerIntegrationTest.policy
    write_fake_codex = ControllerIntegrationTest.write_fake_codex

    def create_clean_inspection_run(
        self, *, targeted="/usr/bin/true", repository_gate=None, authorized_gap=None,
        stop_overrides=None,
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
        controller.persist_run_policy(policy_path, policy)
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
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
        fake = self.write_fake_codex(created_paths=(), clean_mutation=True)
        result = subprocess.run([
            sys.executable, str(CONTROLLER_PATH), "run-next",
            "--run-dir", str(run_dir), "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ], text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        return controller, run_dir

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
        fake = self.write_fake_codex(created_paths=(), clean_mutation=True)
        run_result = subprocess.run([
            sys.executable, str(CONTROLLER_PATH), "run-next",
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

    def test_inspect_reuses_execution_after_crash_and_publishes_accepting_decision(self):
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

        self.assertTrue(result["accepted"])
        self.assertEqual(["accept", "stop"], result["allowed_actions"])
        self.assertEqual(execution_bytes, execution_path.read_bytes())
        verification = json.loads(Path(result["verification_path"]).read_text())
        decision = json.loads(Path(result["decision_path"]).read_text())
        self.assertEqual("passed", verification["outcome"])
        self.assertEqual([], verification["drift_findings"])
        self.assertTrue(decision["accepted"])
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
        self.assertTrue(replay["accepted"])
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

    def test_repository_gate_only_authorized_gap_can_still_offer_accept(self):
        gap = {
            "reason": "Known repository-only failure",
            "owner": "test-owner",
            "follow_up": "Resolve after this bounded task",
        }
        controller, run_dir = self.create_clean_inspection_run(
            repository_gate="/usr/bin/false", authorized_gap=gap,
        )

        result = controller.inspect_run(run_dir, 10)

        self.assertTrue(result["accepted"])
        decision = json.loads(Path(result["decision_path"]).read_text())
        execution = json.loads(
            (run_dir / "verification/attempt-001.turn-001.execution.json").read_text()
        )
        self.assertEqual("authorized_gap", execution["terminal_reason"])
        self.assertEqual(gap, decision["gap_details"])
        self.assertEqual(["accept", "stop"], decision["allowed_actions"])

    def test_authorized_gap_cannot_excuse_a_targeted_failure(self):
        gap = {
            "reason": "Repository exception",
            "owner": "test-owner",
            "follow_up": "Resolve later",
        }
        controller, run_dir = self.create_clean_inspection_run(
            targeted="/usr/bin/false",
            repository_gate="/usr/bin/false",
            authorized_gap=gap,
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
