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
            "validate_attempt_record", "build_attempt_record", "validate_task_manifest",
            "select_task", "validate_ledger", "apply_ledger_update",
        ):
            with self.subTest(name=name):
                self.assertEqual(STATE_PATH, Path(getattr(state, name).__code__.co_filename))

    def test_controller_compatibility_names_delegate_to_state_module(self):
        controller = load_controller()

        for name in (
            "canonical_json", "sha256_text", "validate_run_policy", "transition_task",
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

        self.assertEqual("T1", state.select_task(ledger, self.policy())["id"])
        self.assertEqual("awaiting_inspection", state.transition_task("running", "awaiting_inspection"))
        updated = state.apply_ledger_update(ledger, {"state": "ready"}, "2026-07-16T01:00:00+00:00")
        self.assertEqual("ready", updated["state"])
        self.assertEqual(2, updated["revision"])
        self.assertEqual(1, ledger["revision"])

    def test_unavailable_selection_and_invalid_transitions_are_exact(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger["tasks"][0]["dependencies"] = ["T99"]

        with self.assertRaisesRegex(
            ValueError,
            "^No dependency-ready tasks found\\. Completed: \\[\\]\\. "
            "Task IDs: \\['T1'\\]\\. Ready: \\[\\]$",
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
                ledger, {"state": "running"}, "2026-07-16T01:00:00+00:00"
            )
        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

    def test_invalid_ledger_update_leaves_input_unchanged(self):
        state = load_controller_state()
        ledger = self.ledger()
        original = json.dumps(ledger, sort_keys=True)

        with self.assertRaisesRegex(ValueError, "Ledger task IDs are immutable"):
            state.apply_ledger_update(ledger, {"tasks": []}, "2026-07-16T01:00:00+00:00")

        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

    def test_rejected_controller_update_leaves_persisted_bytes_unchanged(self):
        controller = load_controller()
        run_dir = Path(self.temp_dir.name) / "run"
        run_dir.mkdir()
        ledger_path = run_dir / "ledger.json"
        ledger_path.write_text(json.dumps(self.ledger(), indent=2, sort_keys=True) + "\n")
        original = ledger_path.read_bytes()

        with self.assertRaisesRegex(ValueError, "^Ledger task IDs are immutable$"):
            controller.update_ledger(run_dir, {"tasks": []})

        self.assertEqual(original, ledger_path.read_bytes())
