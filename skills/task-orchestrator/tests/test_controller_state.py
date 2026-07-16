import hashlib
import importlib.util
import json
from itertools import product
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
            "validate_attempt_record", "build_attempt_record", "validate_task_manifest",
            "transition_run", "dependency_ready_task_ids", "mark_ready_tasks",
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
        ledger["state"] = "ready"
        ledger["tasks"][0]["state"] = "ready"

        self.assertEqual("T1", state.select_task(ledger, self.policy())["id"])
        self.assertEqual("awaiting_inspection", state.transition_task("running", "awaiting_inspection"))
        running_tasks = json.loads(json.dumps(ledger["tasks"]))
        running_tasks[0]["state"] = "running"
        running_tasks[0]["attempt_ids"] = ["attempt-001"]
        updated = state.apply_ledger_update(
            ledger,
            {
                "state": "running",
                "selected_task_id": "T1",
                "active_attempt_id": "attempt-001",
                "tasks": running_tasks,
            },
            "2026-07-16T01:00:00+00:00",
            expected_revision=1,
        )
        self.assertEqual("running", updated["state"])
        self.assertEqual(2, updated["revision"])
        self.assertEqual(1, ledger["revision"])

    def test_unavailable_selection_and_invalid_transitions_are_exact(self):
        state = load_controller_state()
        ledger = self.ledger()
        ledger["state"] = "ready"
        ledger["tasks"][0]["state"] = "initialized"
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
            "^'running' requires selected_task_id$",
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

        with self.assertRaisesRegex(ValueError, "Ledger task identity and order are immutable"):
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

        with self.assertRaisesRegex(
            ValueError, "^Ledger task identity and order are immutable$"
        ):
            controller.update_ledger(run_dir, {"tasks": []}, expected_revision=1)

        self.assertEqual(original, ledger_path.read_bytes())
        with self.assertRaisesRegex(TypeError, "expected_revision"):
            controller.update_ledger(run_dir, {})
        self.assertEqual(original, ledger_path.read_bytes())
        with self.assertRaisesRegex(ValueError, "^Stale ledger revision"):
            controller.update_ledger(run_dir, {}, expected_revision=0)
        self.assertEqual(original, ledger_path.read_bytes())

    def test_all_run_and_task_transitions_are_explicit(self):
        state = load_controller_state()
        expected_run_transitions = {
            "initialized": {"ready", "stopped"},
            "ready": {"running", "stopped"},
            "running": {"awaiting_inspection", "resumable", "stopped"},
            "awaiting_inspection": {"resumable", "finalizing", "stopped"},
            "resumable": {"running", "stopped"},
            "finalizing": {"ready", "stopped"},
            "stopped": set(),
        }
        expected_task_transitions = {
            "initialized": {"ready", "stopped"},
            "ready": {"running", "stopped"},
            "running": {"awaiting_inspection", "resumable", "stopped"},
            "awaiting_inspection": {"accepted", "resumable", "stopped"},
            "resumable": {"running", "stopped"},
            "accepted": set(),
            "stopped": set(),
        }

        self.assertEqual(expected_run_transitions, state.ALLOWED_RUN_TRANSITIONS)
        self.assertEqual(expected_task_transitions, state.ALLOWED_TASK_TRANSITIONS)
        self.assertEqual(set(), expected_run_transitions["stopped"])
        self.assertEqual(set(), expected_task_transitions["accepted"])
        self.assertEqual(set(), expected_task_transitions["stopped"])

        for current, requested in product(expected_run_transitions, repeat=2):
            with self.subTest(kind="run", current=current, requested=requested):
                if requested in expected_run_transitions[current]:
                    self.assertEqual(requested, state.transition_run(current, requested))
                else:
                    with self.assertRaisesRegex(ValueError, "not allowed"):
                        state.transition_run(current, requested)

        identity = {"run_id": "run-1", "task_id": "T1", "attempt_id": "attempt-001"}
        for current, requested in product(expected_task_transitions, repeat=2):
            with self.subTest(kind="task", current=current, requested=requested):
                kwargs = {}
                if current == "awaiting_inspection" and requested == "accepted":
                    kwargs = {
                        "closure_decision": {
                            "accepted": True,
                            "allowed_transitions": ["accepted"],
                            "identity": identity,
                        },
                        "expected_identity": identity,
                    }
                if requested in expected_task_transitions[current]:
                    self.assertEqual(
                        requested, state.transition_task(current, requested, **kwargs)
                    )
                else:
                    with self.assertRaisesRegex(ValueError, "not allowed"):
                        state.transition_task(current, requested, **kwargs)

    def coherent_ledger(self, run_state):
        ledger = self.ledger()
        task = ledger["tasks"][0]
        attempt_id = "attempt-001"
        if run_state == "ready":
            ledger["state"] = task["state"] = "ready"
        elif run_state in {"running", "awaiting_inspection", "resumable", "finalizing"}:
            ledger["state"] = run_state
            ledger["selected_task_id"] = "T1"
            task["attempt_ids"] = [attempt_id]
            if run_state == "running":
                task["state"] = "running"
                ledger["active_attempt_id"] = attempt_id
            else:
                task["state"] = (
                    "awaiting_inspection" if run_state == "finalizing" else run_state
                )
                ledger["last_closure_path"] = "closure/attempt-001.json"
            if run_state == "finalizing":
                ledger["last_verification_path"] = "verification/attempt-001.json"
                ledger["last_decision_path"] = "decisions/attempt-001.json"
                ledger["active_operation_path"] = "operations/T1-accept.json"
        elif run_state == "stopped":
            ledger["state"] = task["state"] = "stopped"
        return ledger

    def test_one_coherent_ledger_validates_for_every_run_state(self):
        state = load_controller_state()

        for run_state in state.RUN_STATES:
            with self.subTest(run_state=run_state):
                state.validate_ledger(self.coherent_ledger(run_state))

    def test_ready_ledger_rejects_unselected_active_task(self):
        state = load_controller_state()
        ledger = self.coherent_ledger("ready")
        ledger["tasks"].append({
            **json.loads(json.dumps(ledger["tasks"][0])),
            "id": "T2",
            "title": "Second",
            "brief_path": "tasks/T2.md",
            "state": "running",
            "attempt_ids": ["attempt-002"],
        })

        with self.assertRaisesRegex(ValueError, "active lifecycle state"):
            state.validate_ledger(ledger)

    def test_active_run_states_reject_any_second_active_task(self):
        state = load_controller_state()
        cases = []

        running = self.coherent_ledger("running")
        second = {
            **json.loads(json.dumps(running["tasks"][0])),
            "id": "T2",
            "title": "Second",
            "brief_path": "tasks/T2.md",
            "attempt_ids": ["attempt-002"],
        }
        running["tasks"].append(second)
        cases.append(("running", "running", running))

        for active_state in ("running", "awaiting_inspection", "resumable"):
            finalizing = self.coherent_ledger("finalizing")
            second = {
                **json.loads(json.dumps(finalizing["tasks"][0])),
                "id": "T2",
                "title": "Second",
                "brief_path": "tasks/T2.md",
                "state": active_state,
                "attempt_ids": ["attempt-002"],
            }
            finalizing["tasks"].append(second)
            cases.append(("finalizing", active_state, finalizing))

        for run_state, task_state, ledger in cases:
            with self.subTest(run_state=run_state, task_state=task_state):
                with self.assertRaisesRegex(ValueError, "active lifecycle state"):
                    state.validate_ledger(ledger)

    def test_stopped_run_rejects_active_task_states(self):
        state = load_controller_state()

        for task_state in ("running", "awaiting_inspection", "resumable"):
            with self.subTest(task_state=task_state):
                ledger = self.coherent_ledger("stopped")
                ledger["tasks"][0]["state"] = task_state
                ledger["tasks"][0]["attempt_ids"] = ["attempt-001"]
                with self.assertRaisesRegex(ValueError, "active lifecycle state"):
                    state.validate_ledger(ledger)

    def test_state_coherence_rejects_missing_or_mismatched_ownership_and_references(self):
        state = load_controller_state()
        cases = []

        running = self.coherent_ledger("running")
        running["selected_task_id"] = "missing"
        cases.append((running, "Selected task is missing"))
        running = self.coherent_ledger("running")
        running["tasks"][0]["state"] = "resumable"
        cases.append((running, "Selected task state"))
        running = self.coherent_ledger("running")
        running["active_attempt_id"] = "attempt-002"
        cases.append((running, "latest selected task attempt"))

        duplicate = self.coherent_ledger("running")
        other = json.loads(json.dumps(duplicate["tasks"][0]))
        other.update({"id": "T2", "title": "Second", "brief_path": "tasks/T2.md"})
        duplicate["tasks"].append(other)
        cases.append((duplicate, "owned by more than one task"))

        awaiting = self.coherent_ledger("awaiting_inspection")
        awaiting["last_closure_path"] = None
        cases.append((awaiting, "requires last_closure_path"))
        awaiting = self.coherent_ledger("awaiting_inspection")
        awaiting["last_decision_path"] = "decisions/attempt-001.json"
        cases.append((awaiting, "requires last_verification_path"))

        ready = self.coherent_ledger("ready")
        ready["tasks"][0]["state"] = "initialized"
        cases.append((ready, "at least one ready unfinished task"))
        resumable = self.coherent_ledger("resumable")
        resumable["tasks"][0]["attempt_ids"] = []
        cases.append((resumable, "selected attempt"))
        finalizing = self.coherent_ledger("finalizing")
        finalizing["tasks"][0]["state"] = "accepted"
        cases.append((finalizing, "must remain awaiting_inspection"))
        finalizing = self.coherent_ledger("finalizing")
        finalizing["active_operation_path"] = None
        cases.append((finalizing, "requires active_operation_path"))

        for ledger, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    state.validate_ledger(ledger)

    def test_dependency_readiness_uses_manifest_completions_and_accepted_tasks(self):
        state = load_controller_state()
        tasks = [
            dict(self.ledger()["tasks"][0], id="T1", state="accepted"),
            dict(
                self.ledger()["tasks"][0], id="T2", title="Second",
                brief_path="tasks/T2.md", dependencies=["T1", "external"],
                state="initialized",
            ),
        ]
        completed = ["external"]

        self.assertEqual(["T2"], state.dependency_ready_task_ids(tasks, completed))
        marked = state.mark_ready_tasks(tasks, completed)
        self.assertEqual(["accepted", "ready"], [task["state"] for task in marked])
        self.assertEqual(["external"], completed)
        self.assertEqual("initialized", tasks[1]["state"])

        ledger = self.ledger()
        ledger.update({"state": "ready", "completed_task_ids": completed, "tasks": marked})
        policy = self.policy()
        policy["task_ids"] = ["T1", "T2"]
        self.assertEqual("T2", state.select_task(ledger, policy)["id"])

    def finalizing_to_ready_update(self):
        ledger = self.coherent_ledger("finalizing")
        second = {
            **json.loads(json.dumps(self.ledger()["tasks"][0])),
            "id": "T2",
            "title": "Second",
            "brief_path": "tasks/T2.md",
        }
        ledger["tasks"].append(second)
        tasks = json.loads(json.dumps(ledger["tasks"]))
        tasks[0]["state"] = "accepted"
        tasks[1]["state"] = "ready"
        updater = {
            "state": "ready",
            "selected_task_id": None,
            "last_closure_path": None,
            "last_verification_path": None,
            "last_decision_path": None,
            "active_operation_path": None,
            "tasks": tasks,
        }
        identity = {
            "run_id": "run-1",
            "task_id": "T1",
            "attempt_id": "attempt-001",
        }
        return ledger, updater, identity

    def test_ledger_acceptance_update_requires_accepting_decision(self):
        state = load_controller_state()
        ledger, updater, identity = self.finalizing_to_ready_update()
        original = json.dumps(ledger, sort_keys=True)

        with self.assertRaisesRegex(ValueError, "accepting closure decision"):
            state.apply_ledger_update(
                ledger, updater, "later", expected_revision=1,
                expected_identity=identity,
            )

        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

    def test_ledger_acceptance_update_rejects_stale_identity(self):
        state = load_controller_state()
        ledger, updater, identity = self.finalizing_to_ready_update()
        original = json.dumps(ledger, sort_keys=True)
        stale_identity = dict(identity, attempt_id="attempt-000")

        with self.assertRaisesRegex(ValueError, "identity does not match"):
            state.apply_ledger_update(
                ledger, updater, "later", expected_revision=1,
                closure_decision={
                    "accepted": True,
                    "allowed_transitions": ["accepted"],
                    "identity": stale_identity,
                },
                expected_identity=identity,
            )

        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

    def test_ledger_acceptance_update_accepts_exact_decision_identity(self):
        state = load_controller_state()
        ledger, updater, identity = self.finalizing_to_ready_update()

        updated = state.apply_ledger_update(
            ledger, updater, "later", expected_revision=1,
            closure_decision={
                "accepted": True,
                "allowed_transitions": ["accepted"],
                "identity": identity,
            },
            expected_identity=identity,
        )

        self.assertEqual("ready", updated["state"])
        self.assertEqual(["accepted", "ready"], [task["state"] for task in updated["tasks"]])
        self.assertEqual(2, updated["revision"])

    def test_ledger_update_requires_expected_revision(self):
        state = load_controller_state()

        with self.assertRaisesRegex(TypeError, "expected_revision"):
            state.apply_ledger_update(self.ledger(), {}, "later")

    def test_top_level_ledger_authority_is_immutable(self):
        state = load_controller_state()
        replacements = {
            "version": 2,
            "run_id": "different-run",
            "repository": "/different/repository",
            "created_at": "different-created-at",
            "policy_path": "different-policy.json",
            "policy_sha256": "different-policy-digest",
            "manifest_path": "different-manifest.json",
            "manifest_sha256": "different-manifest-digest",
            "initial_baseline_path": "different-baseline.json",
            "initial_baseline_digest": "different-baseline-digest",
        }

        for field, replacement in replacements.items():
            with self.subTest(field=field):
                ledger = self.ledger()
                original = json.dumps(ledger, sort_keys=True)
                with self.assertRaisesRegex(ValueError, f"{field} is immutable"):
                    state.apply_ledger_update(
                        ledger, {field: replacement}, "later", expected_revision=1
                    )
                self.assertEqual(original, json.dumps(ledger, sort_keys=True))

    def test_stale_or_authority_changing_updates_leave_input_unchanged(self):
        state = load_controller_state()
        authorities = (
            ("tasks", lambda value: value.reverse()),
            ("title", lambda value: value.__setitem__("title", "Changed")),
            ("dependencies", lambda value: value.__setitem__("dependencies", ["other"])),
            ("allowed_paths", lambda value: value.__setitem__("allowed_paths", ["other.txt"])),
            ("required_checks", lambda value: value.__setitem__("required_checks", ["other"])),
        )
        base = self.ledger()
        second = dict(base["tasks"][0], id="T2", title="Second", brief_path="tasks/T2.md")
        base["tasks"].append(second)

        for name, mutate in authorities:
            ledger = json.loads(json.dumps(base))
            original = json.dumps(ledger, sort_keys=True)
            tasks = json.loads(json.dumps(ledger["tasks"]))
            mutate(tasks if name == "tasks" else tasks[0])
            with self.subTest(authority=name):
                with self.assertRaisesRegex(ValueError, "immutable"):
                    state.apply_ledger_update(
                        ledger, {"tasks": tasks}, "later", expected_revision=1
                    )
                self.assertEqual(original, json.dumps(ledger, sort_keys=True))

        ledger = self.ledger()
        original = json.dumps(ledger, sort_keys=True)
        with self.assertRaisesRegex(ValueError, "Stale ledger revision"):
            state.apply_ledger_update(
                ledger, {}, "later", expected_revision=0
            )
        self.assertEqual(original, json.dumps(ledger, sort_keys=True))
        with self.assertRaisesRegex(ValueError, "revision is controller-managed"):
            state.apply_ledger_update(
                ledger, {"revision": 10}, "later", expected_revision=1
            )
        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

        ledger = self.ledger()
        original = json.dumps(ledger, sort_keys=True)
        with self.assertRaisesRegex(ValueError, "completed_task_ids are immutable"):
            state.apply_ledger_update(
                ledger, {"completed_task_ids": ["external"]}, "later",
                expected_revision=1,
            )
        self.assertEqual(original, json.dumps(ledger, sort_keys=True))

        running = self.coherent_ledger("running")
        original = json.dumps(running, sort_keys=True)
        tasks = json.loads(json.dumps(running["tasks"]))
        tasks[0]["attempt_ids"] = []
        with self.assertRaisesRegex(ValueError, "attempt history is append-only"):
            state.apply_ledger_update(
                running, {"tasks": tasks}, "later", expected_revision=1
            )
        self.assertEqual(original, json.dumps(running, sort_keys=True))
