import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


STATE_PATH = Path(__file__).parents[1] / "scripts" / "controller_state.py"
CONTROLLER_PATH = Path(__file__).parents[1] / "scripts" / "controller.py"


def load_controller_state():
    spec = importlib.util.spec_from_file_location(
        "task_orchestrator_controller_state", STATE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_controller():
    spec = importlib.util.spec_from_file_location(
        "task_orchestrator_controller", CONTROLLER_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ControllerStateContractTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repository = Path(self.temp_dir.name) / "repository"
        self.repository.mkdir()
        (self.repository / "tasks").mkdir()
        (self.repository / "tasks" / "T1.md").write_text("# T1\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def policy(self):
        return {
            "version": 1,
            "run_id": "run-1",
            "repository": str(self.repository),
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
                "writable_roots": [str(self.repository)],
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

    def manifest(self):
        return {
            "version": 1,
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": ["make verify"],
            }],
        }

    def ledger(self):
        return {
            "version": 1,
            "run_id": "run-1",
            "repository": str(self.repository),
            "created_at": "2026-07-16T00:00:00+00:00",
            "updated_at": "2026-07-16T00:00:00+00:00",
            "revision": 1,
            "policy_path": "run-policy.json",
            "policy_sha256": "abc",
            "manifest_path": "task-manifest.json",
            "manifest_sha256": "def",
            "initial_baseline_path": "run-initial.json",
            "initial_baseline_digest": "ghi",
            "completed_task_ids": [],
            "state": "initialized",
            "selected_task_id": None,
            "active_attempt_id": None,
            "last_closure_path": None,
            "last_verification_path": None,
            "last_decision_path": None,
            "active_operation_path": None,
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": [],
                "state": "initialized",
                "attempt_ids": [],
            }],
        }

    def test_direct_import_has_no_controller_fallback(self):
        state = load_controller_state()

        self.assertEqual(STATE_PATH, Path(state.__file__))
        for name in (
            "canonical_json", "sha256_text", "validate_run_policy", "transition_task",
            "transition_run",
            "validate_attempt_record", "build_attempt_record", "validate_task_manifest",
            "select_task", "validate_ledger", "apply_ledger_update",
        ):
            with self.subTest(name=name):
                self.assertEqual(STATE_PATH, Path(getattr(state, name).__code__.co_filename))

    def test_controller_compatibility_names_delegate_to_state_module(self):
        controller = load_controller()

        for name in (
            "canonical_json", "sha256_text", "validate_run_policy", "transition_task",
            "transition_run",
            "validate_attempt_record", "build_attempt_record", "validate_task_manifest",
            "select_task", "_validate_task_manifest_schema",
            "_detect_dependency_cycles", "_is_valid_repo_relative_path", "_validate_ledger",
        ):
            with self.subTest(name=name):
                self.assertEqual(STATE_PATH, Path(getattr(controller, name).__code__.co_filename))

        controller.validate_run_policy(self.policy())
        self.assertEqual(
            "T1",
            controller.validate_task_manifest(
                self.policy(), self.manifest(), self.repository
            )["task_entries"][0]["id"],
        )

    def test_canonical_json_and_attempt_record_keep_exact_digests(self):
        state = load_controller_state()
        policy = self.policy()

        self.assertEqual('{"a":1,"b":2}', state.canonical_json({"b": 2, "a": 1}))
        self.assertEqual(
            hashlib.sha256(b'{"a":1,"b":2}').hexdigest(),
            state.sha256_text(state.canonical_json({"b": 2, "a": 1})),
        )
        record = state.build_attempt_record(
            task_id="T1", brief_path="tasks/T1.md", prompt="prompt", policy=policy,
            baseline_ref="run-initial.json",
        )
        self.assertEqual(hashlib.sha256(b"prompt").hexdigest(), record["prompt_sha256"])
        self.assertEqual(
            hashlib.sha256(state.canonical_json(policy).encode()).hexdigest(),
            record["policy_sha256"],
        )
        self.assertEqual({
            "task_id": "T1",
            "brief_path": "tasks/T1.md",
            "prompt": "prompt",
            "prompt_sha256": hashlib.sha256(b"prompt").hexdigest(),
            "baseline_ref": "run-initial.json",
            "policy_sha256": hashlib.sha256(
                state.canonical_json(policy).encode()
            ).hexdigest(),
            "transport": "codex-cli",
            "model": None,
            "sandbox": "workspace-write",
            "approval_policy": "never",
            "network": False,
            "writable_roots": [str(self.repository)],
        }, record)

    def test_valid_manifest_keeps_exact_ledger_entries(self):
        state = load_controller_state()

        self.assertEqual({
            "manifest_id": "test-feature",
            "completed_task_ids": [],
            "task_entries": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": ["make verify"],
                "state": "initialized",
                "attempt_ids": [],
            }],
        }, state.validate_task_manifest(self.policy(), self.manifest(), self.repository))

    def test_policy_and_manifest_rejections_keep_error_contracts(self):
        state = load_controller_state()
        policy = self.policy()
        policy["unknown"] = True
        with self.assertRaisesRegex(ValueError, "unknown top-level fields: unknown"):
            state.validate_run_policy(policy)

        manifest = self.manifest()
        manifest["tasks"][0]["allowed_paths"] = ["allowed.txt", "allowed.txt"]
        with self.assertRaisesRegex(ValueError, "allowed_paths items must be unique"):
            state.validate_task_manifest(self.policy(), manifest, self.repository)

    def test_missing_duplicate_unknown_and_wrong_type_errors_are_exact(self):
        state = load_controller_state()
        cases = []

        policy = self.policy()
        del policy["run_id"]
        cases.append((state.validate_run_policy, (policy,), "Run policy is missing: run_id"))
        policy = self.policy()
        policy["task_ids"] = ["T1", "T1"]
        cases.append((state.validate_run_policy, (policy,), "task_ids items must be unique"))
        policy = self.policy()
        policy["permissions"]["network"] = "no"
        cases.append((state.validate_run_policy, (policy,), "permissions.network must be a boolean"))

        manifest = self.manifest()
        manifest["extra"] = True
        cases.append((
            state.validate_task_manifest,
            (self.policy(), manifest, self.repository),
            "Task manifest contains unknown fields: extra",
        ))
        manifest = self.manifest()
        del manifest["tasks"][0]["title"]
        cases.append((
            state.validate_task_manifest,
            (self.policy(), manifest, self.repository),
            "Task is missing required fields: title",
        ))

        for function, arguments, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, f"^{message}$"):
                    function(*arguments)

    def test_graph_and_path_errors_are_exact(self):
        state = load_controller_state()

        manifest = self.manifest()
        manifest["tasks"][0]["dependencies"] = ["missing"]
        with self.assertRaisesRegex(
            ValueError,
            "^Task T1 depends on missing which does not exist in manifest$",
        ):
            state.validate_task_manifest(self.policy(), manifest, self.repository)

        manifest = self.manifest()
        manifest["tasks"][0]["allowed_paths"] = ["../escape"]
        with self.assertRaisesRegex(
            ValueError,
            "^Task T1 allowed_path '\\.\\./escape' is not a valid repository-relative path$",
        ):
            state.validate_task_manifest(self.policy(), manifest, self.repository)

        (self.repository / "tasks" / "T2.md").write_text("# T2\n")
        policy = self.policy()
        policy["task_ids"] = ["T1", "T2"]
        manifest = self.manifest()
        manifest["tasks"] = [
            manifest["tasks"][0],
            {
                "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
                "dependencies": ["T1"], "allowed_paths": ["allowed.txt"],
            },
        ]
        manifest["tasks"][0]["dependencies"] = ["T2"]
        with self.assertRaisesRegex(
            ValueError,
            "^Dependency cycle detected in manifest: T1 -> T2 -> T1$",
        ):
            state.validate_task_manifest(policy, manifest, self.repository)

    def test_selection_transition_and_ledger_update_are_pure(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger["state"] = "ready"
        ledger["tasks"][0]["state"] = "ready"

        self.assertEqual("T1", state.select_task(ledger, self.policy())["id"])
        self.assertEqual("awaiting_inspection", state.transition_task("running", "awaiting_inspection"))
        updated = state.apply_ledger_update(
            ledger, {}, "2026-07-16T01:00:00+00:00", expected_revision=1
        )
        self.assertEqual("ready", updated["state"])
        self.assertEqual(2, updated["revision"])
        self.assertEqual(1, ledger["revision"])

    def test_unavailable_selection_and_invalid_transitions_are_exact(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger["state"] = "ready"
        ledger["tasks"][0]["state"] = "ready"
        ledger["tasks"][0]["dependencies"] = ["T99"]

        with self.assertRaisesRegex(
            ValueError,
            "^No ready tasks found\\. Completed: \\[\\]\\. Task IDs: \\['T1'\\]$",
        ):
            state.select_task(ledger, self.policy())

        with self.assertRaisesRegex(
            ValueError, "^Task transition running -> accepted is not allowed$"
        ):
            state.transition_task("running", "accepted")

        identity = {"run_id": "run-1", "task_id": "T1", "attempt_id": "attempt-1"}
        stale = dict(identity, attempt_id="attempt-0")
        with self.assertRaisesRegex(
            ValueError, "^Acceptance closure identity does not match current evidence$"
        ):
            state.transition_task(
                "awaiting_inspection",
                "accepted",
                closure_decision={
                    "accepted": True,
                    "allowed_transitions": ["accepted"],
                    "identity": stale,
                },
                expected_identity=identity,
            )

    def test_malformed_attempt_and_incoherent_ledger_errors_are_exact(self):
        state = load_controller_state()

        with self.assertRaisesRegex(ValueError, "^Attempt record is missing task_id$"):
            state.validate_attempt_record({})

        ledger = self.ledger()
        original = json.dumps(ledger, sort_keys=True)
        with self.assertRaisesRegex(
            ValueError,
            "^'running' state requires both selected_task_id and active_attempt_id$",
        ):
            state.apply_ledger_update(
                ledger, {"state": "running"}, "2026-07-16T01:00:00+00:00",
                expected_revision=1,
            )
        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

    def test_invalid_ledger_update_leaves_input_unchanged(self):
        state = load_controller_state()
        ledger = self.ledger()
        original = json.dumps(ledger, sort_keys=True)

        with self.assertRaisesRegex(ValueError, "Ledger task IDs are immutable"):
            state.apply_ledger_update(
                ledger, {"tasks": []}, "2026-07-16T01:00:00+00:00",
                expected_revision=1,
            )

        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

    def test_rejected_controller_update_leaves_persisted_bytes_unchanged(self):
        controller = load_controller()
        run_dir = Path(self.temp_dir.name) / "run"
        run_dir.mkdir()
        ledger_path = run_dir / "ledger.json"
        ledger_path.write_text(json.dumps(self.ledger(), indent=2, sort_keys=True) + "\n")
        original = ledger_path.read_bytes()

        with self.assertRaisesRegex(ValueError, "^Ledger task IDs are immutable$"):
            controller.update_ledger(run_dir, {"tasks": []}, expected_revision=1)

        self.assertEqual(original, ledger_path.read_bytes())
        with self.assertRaisesRegex(ValueError, "Expected ledger revision 0, found 1"):
            controller.update_ledger(run_dir, {}, expected_revision=0)
        self.assertEqual(original, ledger_path.read_bytes())

        with self.assertRaisesRegex(ValueError, "revision is controller-owned"):
            controller.update_ledger(
                run_dir, {"revision": 0}, expected_revision=1
            )
        self.assertEqual(original, ledger_path.read_bytes())

    def test_persisted_updates_enforce_frozen_state_transitions(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger["state"] = "ready"
        ledger["tasks"] = [
            dict(ledger["tasks"][0], state="ready"),
            {
                "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
                "dependencies": ["T1"], "allowed_paths": ["second.txt"],
                "required_checks": [], "state": "initialized", "attempt_ids": [],
            },
        ]
        original = json.dumps(ledger, sort_keys=True)
        accepted_tasks = [dict(task) for task in ledger["tasks"]]
        accepted_tasks[0]["state"] = "accepted"
        accepted_tasks[1]["state"] = "ready"

        with self.assertRaisesRegex(
            ValueError, "Task transition ready -> accepted is not allowed"
        ):
            state.apply_ledger_update(
                ledger, {"tasks": accepted_tasks},
                "2026-07-16T01:00:00+00:00", expected_revision=1,
            )

        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

        finalizing = self.ledger()
        finalizing.update({
            "state": "finalizing", "selected_task_id": "T1",
            "last_closure_path": "closure/attempt-001.json",
            "last_verification_path": "verification/attempt-001.json",
            "last_decision_path": "decisions/attempt-001.json",
            "active_operation_path": "operations/T1-accept.json",
        })
        finalizing["tasks"] = [
            dict(
                finalizing["tasks"][0], state="awaiting_inspection",
                attempt_ids=["attempt-001"],
            ),
            {
                "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
                "dependencies": ["T1"], "allowed_paths": ["second.txt"],
                "required_checks": [], "state": "initialized", "attempt_ids": [],
            },
        ]
        released_tasks = [dict(task) for task in finalizing["tasks"]]
        released_tasks[0]["state"] = "accepted"
        released_tasks[1]["state"] = "ready"
        updater = {
            "state": "ready", "selected_task_id": None,
            "active_operation_path": None, "tasks": released_tasks,
        }
        identity = {
            "run_id": "run-1", "task_id": "T1", "attempt_id": "attempt-001",
        }
        decision = {
            "accepted": True, "allowed_transitions": ["accepted"],
            "identity": identity,
        }

        with self.assertRaisesRegex(ValueError, "identity does not match"):
            state.apply_ledger_update(
                finalizing, updater, "2026-07-16T01:00:00+00:00",
                expected_revision=1,
                closure_decision=dict(decision, identity=dict(identity, attempt_id="attempt-000")),
            )
        released = state.apply_ledger_update(
            finalizing, updater, "2026-07-16T01:00:00+00:00",
            expected_revision=1, closure_decision=decision,
        )
        self.assertEqual(2, released["revision"])
        self.assertEqual("ready", released["state"])
        self.assertEqual(["accepted", "ready"], [task["state"] for task in released["tasks"]])

    def test_acceptance_cannot_change_attempt_history(self):
        state = load_controller_state()
        controller = load_controller()
        ledger = self.ledger()
        ledger.update({
            "state": "finalizing", "selected_task_id": "T1",
            "last_closure_path": "closure/attempt-001.json",
            "last_verification_path": "verification/attempt-001.json",
            "last_decision_path": "decisions/attempt-001.json",
            "active_operation_path": "operations/T1-accept.json",
        })
        ledger["tasks"] = [
            dict(
                ledger["tasks"][0], state="awaiting_inspection",
                attempt_ids=["attempt-001"],
            ),
            {
                "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
                "dependencies": ["T1"], "allowed_paths": ["second.txt"],
                "required_checks": [], "state": "initialized", "attempt_ids": [],
            },
        ]
        released_tasks = json.loads(json.dumps(ledger["tasks"]))
        released_tasks[0].update({
            "state": "accepted",
            "attempt_ids": ["attempt-001", "attempt-002"],
        })
        released_tasks[1]["state"] = "ready"
        updater = {
            "state": "ready", "selected_task_id": None,
            "active_operation_path": None, "tasks": released_tasks,
        }
        decision = {
            "accepted": True, "allowed_transitions": ["accepted"],
            "identity": {
                "run_id": "run-1", "task_id": "T1",
                "attempt_id": "attempt-001",
            },
        }
        original_ledger = json.dumps(ledger, sort_keys=True)
        original_updater = json.dumps(updater, sort_keys=True)

        with self.assertRaisesRegex(
            ValueError, "acceptance cannot append or replace attempt history"
        ):
            state.apply_ledger_update(
                ledger, updater, "2026-07-16T01:00:00+00:00",
                expected_revision=1, closure_decision=decision,
            )
        self.assertEqual(original_ledger, json.dumps(ledger, sort_keys=True))
        self.assertEqual(original_updater, json.dumps(updater, sort_keys=True))

        run_dir = Path(self.temp_dir.name) / "acceptance-history"
        run_dir.mkdir()
        ledger_path = run_dir / "ledger.json"
        ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
        original_bytes = ledger_path.read_bytes()
        with self.assertRaisesRegex(
            ValueError, "acceptance cannot append or replace attempt history"
        ):
            controller.update_ledger(
                run_dir, updater, expected_revision=1,
                closure_decision=decision,
            )
        self.assertEqual(original_bytes, ledger_path.read_bytes())
        self.assertEqual(original_updater, json.dumps(updater, sort_keys=True))

    def test_stage_3_transition_tables_are_exhaustive(self):
        state = load_controller_state()
        run_edges = {
            "initialized": {"ready", "stopped"},
            "ready": {"running", "stopped"},
            "running": {"awaiting_inspection", "resumable", "stopped"},
            "awaiting_inspection": {"resumable", "finalizing", "stopped"},
            "resumable": {"running", "stopped"},
            "finalizing": {"ready", "stopped"},
            "stopped": set(),
        }
        task_edges = {
            "initialized": {"ready", "stopped"},
            "ready": {"running", "stopped"},
            "running": {"awaiting_inspection", "resumable", "stopped"},
            "awaiting_inspection": {"accepted", "resumable", "stopped"},
            "resumable": {"running", "stopped"},
            "accepted": set(),
            "stopped": set(),
        }
        self.assertEqual(run_edges, state.ALLOWED_RUN_TRANSITIONS)
        self.assertEqual(task_edges, state.ALLOWED_TASK_TRANSITIONS)
        for current, requested_states in run_edges.items():
            for requested in run_edges:
                if requested in requested_states:
                    self.assertEqual(requested, state.transition_run(current, requested))
                else:
                    with self.assertRaises(ValueError):
                        state.transition_run(current, requested)
        for current, requested_states in task_edges.items():
            for requested in task_edges:
                if requested == "accepted" and requested in requested_states:
                    identity = {"run_id": "run-1", "task_id": "T1", "attempt_id": "attempt-1"}
                    self.assertEqual(requested, state.transition_task(
                        current, requested,
                        closure_decision={"accepted": True, "allowed_transitions": ["accepted"], "identity": identity},
                        expected_identity=identity,
                    ))
                elif requested in requested_states:
                    self.assertEqual(requested, state.transition_task(current, requested))
                else:
                    with self.assertRaises(ValueError):
                        state.transition_task(current, requested)

    def test_stage_3_ledger_coherence_and_reference_order(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger.update({
            "state": "running", "selected_task_id": "T1",
            "active_attempt_id": "attempt-001",
        })
        ledger["tasks"][0].update({"state": "running", "attempt_ids": ["attempt-001"]})
        state.validate_ledger(ledger)

        ledger.update({
            "state": "awaiting_inspection", "active_attempt_id": None,
            "last_closure_path": "closure/attempt-001.json",
        })
        ledger["tasks"][0]["state"] = "awaiting_inspection"
        state.validate_ledger(ledger)
        ledger["last_decision_path"] = "decisions/decision-001.json"
        with self.assertRaisesRegex(ValueError, "decision.*verification"):
            state.validate_ledger(ledger)

        ledger["last_verification_path"] = "verification/verification-001.json"
        ledger["active_operation_path"] = "operations/operation-001.json"
        ledger["state"] = "finalizing"
        state.validate_ledger(ledger)

        ledger["state"] = "resumable"
        ledger["tasks"][0]["state"] = "resumable"
        ledger["active_operation_path"] = None
        state.validate_ledger(ledger)

    def test_stage_3_references_are_non_empty_strings_or_null(self):
        state = load_controller_state()

        def finalizing_ledger():
            ledger = self.ledger()
            ledger.update({
                "state": "finalizing", "selected_task_id": "T1",
                "last_closure_path": "closure/attempt-001.json",
                "last_verification_path": "verification/attempt-001.json",
                "last_decision_path": "decisions/attempt-001.json",
                "active_operation_path": "operations/T1-accept.json",
            })
            ledger["tasks"][0].update({
                "state": "awaiting_inspection",
                "attempt_ids": ["attempt-001"],
            })
            return ledger

        reference_fields = (
            "last_closure_path", "last_verification_path",
            "last_decision_path", "active_operation_path",
        )
        invalid_values = ("", {"not": "a path"}, [], 1, True)
        for field in reference_fields:
            for value in invalid_values:
                ledger = finalizing_ledger()
                ledger[field] = value
                original = json.dumps(ledger, sort_keys=True)
                with self.subTest(field=field, value=value):
                    with self.assertRaisesRegex(
                        ValueError, f"{field} must be a non-empty string"
                    ):
                        state.validate_ledger(ledger)
                    self.assertEqual(original, json.dumps(ledger, sort_keys=True))

        state.validate_ledger(finalizing_ledger())
        nullable = self.ledger()
        state.validate_ledger(nullable)
        self.assertTrue(all(nullable[field] is None for field in reference_fields))

    def test_stage_3_ledger_coherence_rejects_each_critical_corruption(self):
        state = load_controller_state()

        def running_ledger():
            ledger = self.ledger()
            ledger.update({
                "state": "running",
                "selected_task_id": "T1",
                "active_attempt_id": "attempt-001",
            })
            ledger["tasks"][0].update({
                "state": "running",
                "attempt_ids": ["attempt-001"],
            })
            return ledger

        def awaiting_ledger():
            ledger = running_ledger()
            ledger.update({
                "state": "awaiting_inspection",
                "active_attempt_id": None,
                "last_closure_path": "closure/attempt-001.json",
            })
            ledger["tasks"][0]["state"] = "awaiting_inspection"
            return ledger

        def resumable_ledger():
            ledger = running_ledger()
            ledger["state"] = "resumable"
            ledger["active_attempt_id"] = None
            ledger["tasks"][0]["state"] = "resumable"
            return ledger

        def finalizing_ledger():
            ledger = awaiting_ledger()
            ledger.update({
                "state": "finalizing",
                "last_verification_path": "verification/verification-001.json",
                "last_decision_path": "decisions/decision-001.json",
                "active_operation_path": "operations/operation-001.json",
            })
            return ledger

        ready = self.ledger()
        ready["state"] = "ready"
        ready["tasks"][0]["state"] = "ready"
        stopped = self.ledger()
        stopped["state"] = "stopped"
        stopped["tasks"][0]["state"] = "stopped"
        for ledger in (
            self.ledger(), ready, running_ledger(), awaiting_ledger(),
            resumable_ledger(), finalizing_ledger(), stopped,
        ):
            state.validate_ledger(ledger)

        corruptions = []
        ledger = running_ledger()
        ledger["selected_task_id"] = None
        corruptions.append(ledger)
        ledger = running_ledger()
        ledger["tasks"][0]["state"] = "ready"
        corruptions.append(ledger)
        ledger = running_ledger()
        ledger["tasks"][0]["attempt_ids"] = ["attempt-002"]
        corruptions.append(ledger)
        ledger = running_ledger()
        ledger["tasks"].append({
            "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
            "dependencies": [], "allowed_paths": ["second.txt"],
            "required_checks": [], "state": "initialized",
            "attempt_ids": ["attempt-001"],
        })
        corruptions.append(ledger)
        ledger = awaiting_ledger()
        ledger["last_closure_path"] = None
        corruptions.append(ledger)
        ledger = awaiting_ledger()
        ledger["active_attempt_id"] = "attempt-001"
        corruptions.append(ledger)
        ledger = awaiting_ledger()
        ledger["tasks"][0]["state"] = "running"
        corruptions.append(ledger)
        ledger = awaiting_ledger()
        ledger["last_closure_path"] = None
        ledger["last_verification_path"] = "verification/verification-001.json"
        corruptions.append(ledger)
        ledger = awaiting_ledger()
        ledger["last_decision_path"] = "decisions/decision-001.json"
        corruptions.append(ledger)
        ledger = awaiting_ledger()
        ledger.update({
            "last_verification_path": "verification/verification-001.json",
            "last_decision_path": "decisions/decision-001.json",
            "active_operation_path": "operations/operation-001.json",
        })
        corruptions.append(ledger)
        for field in (
            "last_closure_path", "last_verification_path", "last_decision_path",
            "active_operation_path",
        ):
            ledger = finalizing_ledger()
            ledger[field] = None
            corruptions.append(ledger)
        ledger = finalizing_ledger()
        ledger["tasks"][0]["state"] = "accepted"
        corruptions.append(ledger)
        ledger = resumable_ledger()
        ledger["selected_task_id"] = None
        corruptions.append(ledger)
        ledger = resumable_ledger()
        ledger["active_attempt_id"] = "attempt-001"
        corruptions.append(ledger)
        ledger = resumable_ledger()
        ledger["tasks"][0]["attempt_ids"] = []
        corruptions.append(ledger)
        for base in (ready, stopped):
            ledger = json.loads(json.dumps(base))
            ledger["selected_task_id"] = "T1"
            corruptions.append(ledger)
            ledger = json.loads(json.dumps(base))
            ledger["active_attempt_id"] = "attempt-001"
            corruptions.append(ledger)

        for index, ledger in enumerate(corruptions):
            original = json.dumps(ledger, sort_keys=True)
            with self.subTest(index=index):
                with self.assertRaises(ValueError):
                    state.validate_ledger(ledger)
                self.assertEqual(original, json.dumps(ledger, sort_keys=True))

    def test_nonselected_task_cannot_hold_ownership_bearing_state(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger.update({"state": "ready"})
        ledger["tasks"][0]["state"] = "ready"
        ledger["tasks"].append({
            "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
            "dependencies": [], "allowed_paths": ["second.txt"],
            "required_checks": [], "state": "running",
            "attempt_ids": ["attempt-002"],
        })

        with self.assertRaisesRegex(ValueError, "Only the selected task"):
            state.validate_ledger(ledger)

    def test_running_active_attempt_must_be_latest(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger.update({
            "state": "running", "selected_task_id": "T1",
            "active_attempt_id": "attempt-001",
        })
        ledger["tasks"][0].update({
            "state": "running",
            "attempt_ids": ["attempt-001", "attempt-002"],
        })

        with self.assertRaisesRegex(ValueError, "latest selected task attempt"):
            state.validate_ledger(ledger)

    def test_ready_state_requires_exact_dependency_ready_set(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger.update({"state": "ready"})
        ledger["tasks"][0]["state"] = "ready"
        ledger["tasks"].append({
            "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
            "dependencies": [], "allowed_paths": ["second.txt"],
            "required_checks": [], "state": "initialized", "attempt_ids": [],
        })

        with self.assertRaisesRegex(ValueError, "exactly the dependency-ready"):
            state.validate_ledger(ledger)

    def test_stopped_state_rejects_ownership_bearing_tasks(self):
        state = load_controller_state()
        for task_state in ("running", "awaiting_inspection", "resumable"):
            with self.subTest(task_state=task_state):
                ledger = self.ledger()
                ledger.update({"state": "stopped"})
                ledger["tasks"][0]["state"] = "stopped"
                ledger["tasks"].append({
                    "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
                    "dependencies": [], "allowed_paths": ["second.txt"],
                    "required_checks": [], "state": task_state,
                    "attempt_ids": ["attempt-002"],
                })
                with self.assertRaisesRegex(ValueError, "stopped.*active task state"):
                    state.validate_ledger(ledger)

    def test_ledger_scalar_and_array_boundaries(self):
        state = load_controller_state()
        for revision in (True, 0, -1):
            with self.subTest(revision=revision):
                ledger = self.ledger()
                ledger["revision"] = revision
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    state.validate_ledger(ledger)
        ledger = self.ledger()
        ledger["completed_task_ids"] = "T0"
        with self.assertRaisesRegex(ValueError, "completed_task_ids.*array"):
            state.validate_ledger(ledger)

    def test_incoherent_updates_preserve_input_and_persisted_bytes(self):
        state = load_controller_state()
        controller = load_controller()

        partial_ready = self.ledger()
        partial_ready["tasks"].append({
            "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
            "dependencies": [], "allowed_paths": ["second.txt"],
            "required_checks": [], "state": "initialized", "attempt_ids": [],
        })
        partial_ready_tasks = json.loads(json.dumps(partial_ready["tasks"]))
        partial_ready_tasks[0]["state"] = "ready"

        stopped_with_running = self.ledger()
        stopped_with_running.update({
            "state": "running", "selected_task_id": "T1",
            "active_attempt_id": "attempt-001",
        })
        stopped_with_running["tasks"][0].update({
            "state": "running", "attempt_ids": ["attempt-001"],
        })

        cases = (
            (
                "partial_ready", partial_ready,
                {"state": "ready", "tasks": partial_ready_tasks},
                "exactly the dependency-ready",
            ),
            (
                "stopped_with_running", stopped_with_running,
                {
                    "state": "stopped", "selected_task_id": None,
                    "active_attempt_id": None,
                },
                "stopped.*active task state",
            ),
        )
        for name, ledger, updater, error in cases:
            with self.subTest(name=name, boundary="pure"):
                original_ledger = json.dumps(ledger, sort_keys=True)
                original_updater = json.dumps(updater, sort_keys=True)
                with self.assertRaisesRegex(ValueError, error):
                    state.apply_ledger_update(
                        ledger, updater, "2026-07-16T01:00:00+00:00",
                        expected_revision=1,
                    )
                self.assertEqual(original_ledger, json.dumps(ledger, sort_keys=True))
                self.assertEqual(original_updater, json.dumps(updater, sort_keys=True))

            with self.subTest(name=name, boundary="persisted"):
                run_dir = Path(self.temp_dir.name) / name
                run_dir.mkdir()
                ledger_path = run_dir / "ledger.json"
                ledger_path.write_text(
                    json.dumps(ledger, indent=2, sort_keys=True) + "\n"
                )
                original_bytes = ledger_path.read_bytes()
                original_updater = json.dumps(updater, sort_keys=True)
                with self.assertRaisesRegex(ValueError, error):
                    controller.update_ledger(
                        run_dir, updater, expected_revision=1
                    )
                self.assertEqual(original_bytes, ledger_path.read_bytes())
                self.assertEqual(original_updater, json.dumps(updater, sort_keys=True))

    def test_selection_uses_persisted_ready_state_and_accepted_dependencies(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger["state"] = "ready"
        ledger["tasks"] = [
            dict(ledger["tasks"][0], state="accepted"),
            {
                "id": "T2", "title": "Second", "brief_path": "tasks/T2.md",
                "dependencies": ["T1"], "allowed_paths": ["second.txt"],
                "required_checks": [], "state": "ready", "attempt_ids": [],
            },
        ]
        self.assertEqual("T2", state.select_task(ledger, self.policy())["id"])
        self.assertEqual([], ledger["completed_task_ids"])
        ledger["tasks"][1]["state"] = "initialized"
        with self.assertRaisesRegex(ValueError, "No ready tasks"):
            state.select_task(ledger, self.policy())

    def test_expected_revision_and_authority_are_immutable(self):
        state = load_controller_state()
        ledger = self.ledger()
        original = json.dumps(ledger, sort_keys=True)
        with self.assertRaisesRegex(ValueError, "Expected ledger revision 0, found 1"):
            state.apply_ledger_update(
                ledger, {}, "2026-07-16T01:00:00+00:00", expected_revision=0
            )
        changed_tasks = [dict(task) for task in ledger["tasks"]]
        changed_tasks[0]["allowed_paths"] = ["other.txt"]
        with self.assertRaisesRegex(ValueError, "authority is immutable"):
            state.apply_ledger_update(
                ledger, {"tasks": changed_tasks}, "2026-07-16T01:00:00+00:00",
                expected_revision=1,
            )
        with self.assertRaisesRegex(ValueError, "revision is controller-owned"):
            state.apply_ledger_update(
                ledger, {"revision": 0}, "2026-07-16T01:00:00+00:00",
                expected_revision=1,
            )
        self.assertEqual(original, json.dumps(ledger, sort_keys=True))


class Stage3RecordContractTest(unittest.TestCase):
    def identity(self):
        return {
            "run_id": "run-1",
            "task_id": "T1",
            "attempt_id": "attempt-001",
            "turn": 1,
            "policy_sha256": "1" * 64,
            "manifest_sha256": "2" * 64,
            "prompt_sha256": "3" * 64,
            "selected_task_baseline_sha256": "4" * 64,
        }

    def closure_identity(self):
        return {
            "subject": self.identity(),
            "stage2_git_evidence_sha256": "5" * 64,
            "post_worker_head_oid": "a" * 40,
            "post_worker_index_tree_oid": "b" * 40,
            "post_worker_status_sha256": "6" * 64,
        }

    def command(self, command_id="command-001", role="targeted"):
        return {
            "id": command_id,
            "argv": ["python3", "-m", "unittest"],
            "sources": ["policy.targeted_checks[0]"],
            "role": role,
        }

    def outcome(self, command_id="command-001", status="passed"):
        exit_codes = {
            "passed": 0, "failed": 1, "timed_out": None,
            "interrupted": None, "authorized_gap": 1,
        }
        return {
            "id": command_id,
            "status": status,
            "exit_code": exit_codes[status],
            "started_at": "2026-07-18T10:00:00+00:00",
            "ended_at": "2026-07-18T10:00:01+00:00",
            "effective_argv": ["/usr/bin/sandbox-exec", "/usr/bin/python3"],
            "stdout_path": (
                f"verification/attempt-001.turn-001.{command_id}.stdout.log"
            ),
            "stdout_sha256": "7" * 64,
            "stderr_path": (
                f"verification/attempt-001.turn-001.{command_id}.stderr.log"
            ),
            "stderr_sha256": "8" * 64,
        }

    def execution(self):
        return {
            "version": 1,
            "closure_identity": self.closure_identity(),
            "plan": [self.command()],
            "outcomes": [self.outcome()],
            "effective_envelope": {
                "sandbox": "workspace-write",
                "approval_policy": "never",
                "network": False,
                "dependency_install": False,
                "writable_roots": ["/workspace"],
                "danger_full_access_authorized": False,
            },
            "started_at": "2026-07-18T10:00:00+00:00",
            "ended_at": "2026-07-18T10:00:01+00:00",
            "terminal_reason": "complete",
            "authorized_gap": None,
        }

    def git_identity(self):
        return {
            "head_oid": "a" * 40,
            "index_tree_oid": "b" * 40,
            "status_sha256": "6" * 64,
        }

    def verification(self):
        return {
            "version": 1,
            "closure_identity": self.closure_identity(),
            "execution_path": "verification/attempt-001.turn-001.execution.json",
            "execution_sha256": "9" * 64,
            "pre_verification_git": self.git_identity(),
            "post_verification_git": self.git_identity(),
            "drift_findings": [],
            "outcome": "passed",
        }

    def decision(self, accepted=True):
        return {
            "version": 1,
            "closure_identity": self.closure_identity(),
            "verification_path": "verification/attempt-001.turn-001.json",
            "verification_sha256": "a" * 64,
            "accepted": accepted,
            "reasons": ["mechanical checks passed" if accepted else "verification failed"],
            "allowed_actions": ["accept"] if accepted else ["resume", "stop"],
            "allowed_transitions": ["accepted"] if accepted else ["resumable", "stopped"],
            "gap_details": None,
            "semantic_review": "not_collected",
        }

    def operation(self, state="prepared"):
        evidence = []
        if state in {"effects_complete", "complete"}:
            evidence = [{
                "effect_id": "commit",
                "effect_type": "commit",
                "outcome": "not_required",
                "evidence_sha256": None,
            }]
        mismatch = None
        if state == "mismatch":
            mismatch = {"reason": "contradictory persisted effect", "evidence_sha256": "b" * 64}
        return {
            "version": 1,
            "operation_id": "T1-accept",
            "closure_identity": self.closure_identity(),
            "decision_path": "decisions/attempt-001.turn-001.json",
            "decision_sha256": "c" * 64,
            "state": state,
            "prepared_intent": {
                "action": "accept",
                "commit_mode": "off",
                "tracker_mode": "off",
            },
            "effect_evidence": evidence,
            "mismatch": mismatch,
        }

    def test_attempt_turn_identity_rejects_mismatched_turn(self):
        state = load_controller_state()
        expected = self.identity()
        stale = dict(expected, turn=2)

        with self.assertRaisesRegex(ValueError, "identity does not match expected subject"):
            state.validate_attempt_turn_identity(stale, expected=expected)

    def test_exact_identity_and_record_fixtures_validate(self):
        state = load_controller_state()
        subject = self.identity()
        closure = self.closure_identity()
        state.validate_attempt_turn_identity(subject, expected=subject)
        state.validate_closure_identity(closure, expected_subject=subject)
        state.validate_command_execution_record(
            self.execution(), expected_closure_identity=closure
        )

        failed = self.execution()
        failed["plan"].append({
            **self.command("command-002", "repository_gate"),
            "argv": ["make", "verify"],
        })
        failed["outcomes"] = [self.outcome(status="failed")]
        failed["terminal_reason"] = "command_failed"
        state.validate_command_execution_record(failed, expected_closure_identity=closure)

        authorized_gap = self.execution()
        authorized_gap["outcomes"][0] = self.outcome(status="authorized_gap")
        authorized_gap["terminal_reason"] = "authorized_gap"
        authorized_gap["authorized_gap"] = {
            "reason": "repository gate unavailable",
            "owner": "controller",
            "follow_up": "run the gate before release",
        }
        state.validate_command_execution_record(
            authorized_gap, expected_closure_identity=closure
        )

        state.validate_verification_record(
            self.verification(), expected_closure_identity=closure,
            expected_execution_sha256="9" * 64,
        )
        failed_verification = self.verification()
        failed_verification["outcome"] = "failed"
        failed_verification["drift_findings"] = ["tracked workspace drift"]
        state.validate_verification_record(
            failed_verification, expected_closure_identity=closure,
            expected_execution_sha256="9" * 64,
        )
        for accepted in (True, False):
            state.validate_closure_decision(
                self.decision(accepted), expected_closure_identity=closure,
                expected_verification_sha256="a" * 64,
            )
        for operation_state in ("prepared", "effects_complete", "complete", "mismatch"):
            state.validate_finalization_operation(
                self.operation(operation_state), expected_closure_identity=closure,
                expected_decision_sha256="c" * 64,
            )

    def test_identity_fields_are_exact_canonical_and_input_preserving(self):
        state = load_controller_state()
        subject = self.identity()
        closure = self.closure_identity()
        original_subject = json.dumps(subject, sort_keys=True)
        original_closure = json.dumps(closure, sort_keys=True)

        for field in tuple(subject):
            missing = dict(subject)
            del missing[field]
            with self.subTest(kind="missing", field=field), self.assertRaises(ValueError):
                state.validate_attempt_turn_identity(missing)
            changed = dict(subject)
            changed[field] = 2 if field == "turn" else "changed"
            with self.subTest(kind="changed", field=field), self.assertRaises(ValueError):
                state.validate_attempt_turn_identity(changed, expected=subject)
        with self.assertRaisesRegex(ValueError, "unknown fields"):
            state.validate_attempt_turn_identity(dict(subject, own_sha256="f" * 64))
        with self.assertRaisesRegex(ValueError, "positive integer"):
            state.validate_attempt_turn_identity(dict(subject, turn=True))
        with self.assertRaisesRegex(ValueError, "lowercase SHA-256"):
            state.validate_attempt_turn_identity(dict(subject, policy_sha256="A" * 64))

        for field in tuple(closure):
            changed = json.loads(json.dumps(closure))
            if field == "subject":
                changed[field]["turn"] = 2
            else:
                changed[field] = "changed"
            with self.subTest(kind="closure", field=field), self.assertRaises(ValueError):
                state.validate_closure_identity(changed, expected_subject=subject)
        self.assertEqual(original_subject, json.dumps(subject, sort_keys=True))
        self.assertEqual(original_closure, json.dumps(closure, sort_keys=True))

    def test_each_consuming_identity_link_rejects_stale_data(self):
        state = load_controller_state()
        closure = self.closure_identity()
        subject_changes = {
            "run_id": "run-2", "task_id": "T2", "attempt_id": "attempt-002",
            "turn": 2, "policy_sha256": "0" * 64, "manifest_sha256": "0" * 64,
            "prompt_sha256": "0" * 64,
            "selected_task_baseline_sha256": "0" * 64,
        }
        for field, value in subject_changes.items():
            stale = json.loads(json.dumps(closure))
            stale["subject"][field] = value
            execution = self.execution()
            execution["closure_identity"] = stale
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, "execution closure identity"
            ):
                state.validate_command_execution_record(
                    execution, expected_closure_identity=closure
                )
        for field, value in (
            ("stage2_git_evidence_sha256", "0" * 64),
            ("post_worker_head_oid", "c" * 40),
            ("post_worker_index_tree_oid", "d" * 40),
            ("post_worker_status_sha256", "0" * 64),
        ):
            stale = json.loads(json.dumps(closure))
            stale[field] = value
            execution = self.execution()
            execution["closure_identity"] = stale
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, "execution closure identity"
            ):
                state.validate_command_execution_record(
                    execution, expected_closure_identity=closure
                )

        verification = self.verification()
        with self.assertRaisesRegex(ValueError, "execution digest"):
            state.validate_verification_record(
                verification, expected_closure_identity=closure,
                expected_execution_sha256="0" * 64,
            )
        decision = self.decision()
        with self.assertRaisesRegex(ValueError, "verification digest"):
            state.validate_closure_decision(
                decision, expected_closure_identity=closure,
                expected_verification_sha256="0" * 64,
            )
        operation = self.operation()
        with self.assertRaisesRegex(ValueError, "decision digest"):
            state.validate_finalization_operation(
                operation, expected_closure_identity=closure,
                expected_decision_sha256="0" * 64,
            )

    def test_canonical_digests_bind_the_acyclic_chain(self):
        state = load_controller_state()
        closure = self.closure_identity()
        execution = self.execution()
        external_execution_json = json.dumps(
            execution, sort_keys=True, separators=(",", ":")
        )
        self.assertEqual(external_execution_json, state.canonical_json(execution))
        execution_digest = hashlib.sha256(external_execution_json.encode()).hexdigest()
        verification = self.verification()
        verification["execution_sha256"] = execution_digest
        state.validate_verification_record(
            verification, expected_closure_identity=closure,
            expected_execution_sha256=execution_digest,
        )
        external_verification_json = json.dumps(
            verification, sort_keys=True, separators=(",", ":")
        )
        verification_digest = hashlib.sha256(external_verification_json.encode()).hexdigest()
        decision = self.decision()
        decision["verification_sha256"] = verification_digest
        state.validate_closure_decision(
            decision, expected_closure_identity=closure,
            expected_verification_sha256=verification_digest,
        )
        with self.assertRaisesRegex(ValueError, "unknown fields"):
            state.validate_verification_record(
                dict(verification, own_sha256="d" * 64),
                expected_closure_identity=closure,
                expected_execution_sha256=execution_digest,
            )
        with self.assertRaisesRegex(ValueError, "unknown fields"):
            state.validate_closure_decision(
                dict(decision, own_sha256="e" * 64),
                expected_closure_identity=closure,
                expected_verification_sha256=verification_digest,
            )

    def test_execution_rejects_duplicates_types_times_and_contradictions(self):
        state = load_controller_state()
        closure = self.closure_identity()
        cases = []
        record = self.execution()
        record["plan"].append(dict(self.command(), id="command-002"))
        record["outcomes"].append(self.outcome("command-002"))
        cases.append(record)
        record = self.execution()
        record["outcomes"][0]["exit_code"] = True
        cases.append(record)
        record = self.execution()
        record["outcomes"][0]["ended_at"] = "2026-07-18T09:00:00+00:00"
        cases.append(record)
        record = self.execution()
        record["terminal_reason"] = "command_failed"
        cases.append(record)
        record = self.execution()
        record["plan"].append({
            **self.command("command-002", "repository_gate"),
            "argv": ["make", "verify"],
        })
        record["outcomes"] = [
            self.outcome(status="failed"), self.outcome("command-002", "passed")
        ]
        record["terminal_reason"] = "command_failed"
        cases.append(record)
        record = self.execution()
        record["unknown"] = True
        cases.append(record)
        for index, record in enumerate(cases):
            with self.subTest(index=index), self.assertRaises(ValueError):
                state.validate_command_execution_record(
                    record, expected_closure_identity=closure
                )

    def test_artifact_paths_are_exact_and_structurally_safe(self):
        state = load_controller_state()
        closure = self.closure_identity()
        for invalid in (
            "/verification/log", "verification/../log", "verification//log",
            "verification/./log", "decisions/attempt-001.turn-001.execution.json",
            "verification/attempt-002.turn-001.execution.json",
            "verification/attempt-001.turn-002.execution.json",
        ):
            record = self.verification()
            record["execution_path"] = invalid
            with self.subTest(path=invalid), self.assertRaises(ValueError):
                state.validate_verification_record(
                    record, expected_closure_identity=closure,
                    expected_execution_sha256="9" * 64,
                )
        decision = self.decision()
        decision["verification_path"] = "decisions/attempt-001.turn-001.json"
        with self.assertRaisesRegex(ValueError, "verification/"):
            state.validate_closure_decision(
                decision, expected_closure_identity=closure,
                expected_verification_sha256="a" * 64,
            )
        execution = self.execution()
        execution["outcomes"][0]["stdout_path"] = (
            "decisions/attempt-001.turn-001.command-001.stdout.log"
        )
        with self.assertRaisesRegex(ValueError, "verification/"):
            state.validate_command_execution_record(
                execution, expected_closure_identity=closure
            )

    def test_decision_verdict_gap_and_semantic_review_are_consistent(self):
        state = load_controller_state()
        closure = self.closure_identity()
        cases = []
        record = self.decision()
        record["accepted"] = 1
        cases.append(record)
        record = self.decision()
        record["allowed_actions"] = ["stop"]
        cases.append(record)
        record = self.decision()
        record["semantic_review"] = "passed"
        cases.append(record)
        record = self.decision(False)
        record["allowed_transitions"].append("accepted")
        cases.append(record)
        record = self.decision(False)
        record["allowed_actions"] = ["resume"]
        record["allowed_transitions"] = ["stopped"]
        cases.append(record)
        for index, record in enumerate(cases):
            with self.subTest(index=index), self.assertRaises(ValueError):
                state.validate_closure_decision(
                    record, expected_closure_identity=closure,
                    expected_verification_sha256="a" * 64,
                )

    def test_operation_transitions_are_ordered_append_only_and_pure(self):
        state = load_controller_state()
        closure = self.closure_identity()
        prepared = self.operation("prepared")
        effects = self.operation("effects_complete")
        complete = self.operation("complete")
        original_prepared = json.dumps(prepared, sort_keys=True)
        original_effects = json.dumps(effects, sort_keys=True)

        updated = state.update_finalization_operation(
            prepared, effects, expected_state="prepared",
            expected_closure_identity=closure, expected_decision_sha256="c" * 64,
        )
        self.assertEqual(effects, updated)
        completed = state.update_finalization_operation(
            effects, complete, expected_state="effects_complete",
            expected_closure_identity=closure, expected_decision_sha256="c" * 64,
        )
        self.assertEqual(complete, completed)
        replayed = state.update_finalization_operation(
            complete, complete, expected_state="complete",
            expected_closure_identity=closure, expected_decision_sha256="c" * 64,
        )
        self.assertEqual(complete, replayed)
        self.assertIsNot(complete, replayed)
        self.assertEqual(original_prepared, json.dumps(prepared, sort_keys=True))
        self.assertEqual(original_effects, json.dumps(effects, sort_keys=True))

    def test_operation_rejects_skips_stale_updates_and_history_changes(self):
        state = load_controller_state()
        closure = self.closure_identity()
        prepared = self.operation("prepared")
        effects = self.operation("effects_complete")
        complete = self.operation("complete")
        cases = []
        cases.append((prepared, complete, "prepared"))
        cases.append((prepared, effects, "effects_complete"))
        changed_intent = self.operation("effects_complete")
        changed_intent["prepared_intent"]["commit_mode"] = "controller_exact_paths"
        cases.append((prepared, changed_intent, "prepared"))
        removed = self.operation("complete")
        removed["effect_evidence"] = []
        cases.append((effects, removed, "effects_complete"))
        altered = self.operation("complete")
        altered["effect_evidence"][0]["effect_id"] = "changed"
        cases.append((effects, altered, "effects_complete"))
        cases.append((complete, effects, "complete"))
        for index, (current, proposed, expected_state) in enumerate(cases):
            with self.subTest(index=index), self.assertRaises(ValueError):
                state.update_finalization_operation(
                    current, proposed, expected_state=expected_state,
                    expected_closure_identity=closure,
                    expected_decision_sha256="c" * 64,
                )

        mismatch = self.operation("mismatch")
        updated = state.update_finalization_operation(
            prepared, mismatch, expected_state="prepared",
            expected_closure_identity=closure, expected_decision_sha256="c" * 64,
        )
        self.assertEqual("mismatch", updated["state"])
        effects_mismatch = self.operation("mismatch")
        effects_mismatch["effect_evidence"] = effects["effect_evidence"]
        updated = state.update_finalization_operation(
            effects, effects_mismatch, expected_state="effects_complete",
            expected_closure_identity=closure, expected_decision_sha256="c" * 64,
        )
        self.assertEqual("mismatch", updated["state"])
        with self.assertRaisesRegex(ValueError, "not allowed"):
            state.update_finalization_operation(
                mismatch, complete, expected_state="mismatch",
                expected_closure_identity=closure,
                expected_decision_sha256="c" * 64,
            )
