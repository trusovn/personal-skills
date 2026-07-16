import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


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
        """init_run must atomically expose dependency-ready tasks."""
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
        self.assertEqual(
            ["ready", "ready", "initialized"],
            [task["state"] for task in ledger["tasks"]],
        )
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
            "tasks": [
                {
                    "id": "T1",
                    "title": "Task 1",
                    "brief_path": "tasks/T1.md",
                    "dependencies": ["T99"],
                    "allowed_paths": ["allowed.txt"],
                    "required_checks": [],
                    "state": "initialized",
                    "attempt_ids": [],
                },
            ],
        }
        policy = self.policy()
        with self.assertRaises(ValueError) as ctx:
            controller.select_task(ledger, policy)
        self.assertIn("No dependency-ready tasks", ctx.exception.args[0])

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

        # Run next with a non-existent adapter
        run_result = subprocess.run(
            [
                sys.executable, str(CONTROLLER_PATH), "run-next",
                "--run-dir", str(run_dir),
                "--timeout-seconds", "10",
                "--codex-bin", "/nonexistent/codex",
            ],
            text=True,
            capture_output=True,
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

    def write_fake_codex(self, *, write_result=True, created_paths=("new.txt",)):
        """Write a fake codex that emits a thread and a valid result."""
        fake = self.root / "fake-codex"
        fake.write_text(
            f"""#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import sys

args = sys.argv[1:]
log_path = Path({str(self.root / 'argv.json')!r})
log = json.loads(log_path.read_text()) if log_path.exists() else []
log.append(args)
log_path.write_text(json.dumps(log))
if "--help" in args:
    raise SystemExit(0)
allowed = Path.cwd() / "allowed.txt"
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
        "task_id": "T1",
        "summary": "Implemented task T1.",
        "files_changed": ["allowed.txt", *created_paths],
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
        rewritten_tasks[0]["attempt_ids"] = []
        with self.assertRaisesRegex(ValueError, "append-only"):
            controller.update_ledger(
                run_dir, {"tasks": rewritten_tasks},
                expected_revision=ledger["revision"],
            )
        self.assertEqual(ledger_before, ledger_path.read_bytes())

    def test_run_lock_and_revision_prevent_duplicate_or_stale_reconciliation(self):
        controller = load_controller()
        run_dir = self.root / "runs" / "run-owned"
        policy_path = self.root / "run-policy.json"
        manifest_path = self.root / "task-manifest.json"
        marker = self.root / "worker-started"
        release_fifo = self.root / "release-worker"
        os.mkfifo(release_fifo)
        fake = self.root / "blocking-codex"
        fake.write_text(
            f"""#!/usr/bin/env python3
import json
from pathlib import Path
import sys

args = sys.argv[1:]
if "--help" in args:
    raise SystemExit(0)
with Path({str(marker)!r}).open("a") as stream:
    stream.write("started\\n")
with Path({str(release_fifo)!r}).open() as stream:
    stream.read(1)
print(json.dumps({{"type": "thread.started", "thread_id": "thread-blocked-001"}}), flush=True)
if "-o" in args:
    result_path = Path(args[args.index("-o") + 1])
    result_path.write_text(json.dumps({{
        "status": "complete",
        "task_id": "T1",
        "summary": "done",
        "files_changed": [],
        "verification": [],
        "decisions": [],
        "questions": [],
        "risks": [],
        "next_action": "inspect"
    }}))
raise SystemExit(0)
"""
        )
        fake.chmod(0o755)
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
        ledger_path = run_dir / "ledger.json"
        command = [
            sys.executable, str(CONTROLLER_PATH), "run-next",
            "--run-dir", str(run_dir),
            "--timeout-seconds", "10",
            "--codex-bin", str(fake),
        ]

        original = ledger_path.read_bytes()
        original_baselines = sorted(path.name for path in (run_dir / "baselines").iterdir())
        lock = controller.acquire_run_lock(run_dir)
        try:
            contended = subprocess.run(command, text=True, capture_output=True)
        finally:
            controller.release_run_lock(lock)
        self.assertNotEqual(0, contended.returncode)
        self.assertIn("Another controller command owns run", contended.stderr)
        self.assertEqual(original, ledger_path.read_bytes())
        self.assertFalse((run_dir / "attempts").exists())
        self.assertEqual(
            original_baselines,
            sorted(path.name for path in (run_dir / "baselines").iterdir()),
        )

        first = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.monotonic() + 5
            while not marker.exists() and first.poll() is None and time.monotonic() < deadline:
                pass
            self.assertTrue(marker.exists(), "first worker did not reach its wait boundary")
            running = json.loads(ledger_path.read_text())
            self.assertEqual("running", running["state"])
            self.assertEqual("attempt-001", running["active_attempt_id"])

            running_bytes = ledger_path.read_bytes()
            second = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(0, second.returncode)
            self.assertIn("Cannot select task from state 'running'", second.stderr)
            self.assertEqual(running_bytes, ledger_path.read_bytes())
            self.assertEqual(["started"], marker.read_text().splitlines())
            self.assertEqual(
                ["attempt-001"],
                sorted(path.name for path in (run_dir / "attempts").iterdir()),
            )

            stopped_tasks = json.loads(json.dumps(running["tasks"]))
            stopped_tasks[0]["state"] = "stopped"
            lock = controller.acquire_run_lock(run_dir)
            try:
                controller.update_ledger(
                    run_dir,
                    {
                        "state": "stopped",
                        "selected_task_id": None,
                        "active_attempt_id": None,
                        "tasks": stopped_tasks,
                    },
                    expected_revision=running["revision"],
                )
            finally:
                controller.release_run_lock(lock)
            competing_bytes = ledger_path.read_bytes()
            release_fifo.write_text("x")
            stdout, stderr = first.communicate(timeout=10)
            self.assertNotEqual(0, first.returncode, stdout)
            self.assertIn("refusing stale reconciliation", stderr)
            self.assertEqual(competing_bytes, ledger_path.read_bytes())
        finally:
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
