import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
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
        self.assertEqual("accepted", controller.transition_task(
            "awaiting_inspection", "accepted", closure_decision={"accepted": True}
        ))

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


if __name__ == "__main__":
    unittest.main()
