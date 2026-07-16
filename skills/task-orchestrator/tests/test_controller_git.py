import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
CONTROLLER_PATH = SCRIPTS_DIR / "controller.py"
CONTROLLER_GIT_PATH = SCRIPTS_DIR / "controller_git.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_git(repository: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
    )


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def status_value(code: str, content: bytes) -> str:
    return f"{code}:{hashlib.sha256(content).hexdigest()}"


class ControllerGitTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        run_git(self.repo, "init", "-q")
        run_git(self.repo, "config", "user.name", "Test")
        run_git(self.repo, "config", "user.email", "test@example.invalid")
        for path, content in {
            "allowed.txt": "allowed baseline\n",
            "staged.txt": "staged baseline\n",
            "delete.txt": "delete baseline\n",
            "rename-old.txt": "rename baseline\n",
            "dirty-modified.txt": "dirty baseline\n",
            "dirty-unchanged.txt": "dirty unchanged baseline\n",
        }.items():
            (self.repo / path).write_text(content)
        run_git(self.repo, "add", ".")
        run_git(self.repo, "commit", "-qm", "baseline")
        self.git = load_module(CONTROLLER_GIT_PATH, "task_orchestrator_controller_git_test")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_snapshots_and_closure_artifacts_preserve_git_observations(self):
        (self.repo / "dirty-modified.txt").write_text("pre-existing dirty\n")
        (self.repo / "dirty-unchanged.txt").write_text("unchanged dirty\n")
        (self.repo / "dirty-disappeared.txt").write_text("pre-existing untracked\n")
        baseline = self.git.capture_task_baseline(self.repo)
        self.assertEqual(
            status_value(" M", b"pre-existing dirty\n"),
            baseline["status"]["dirty-modified.txt"],
        )
        self.assertEqual(
            status_value("??", b"pre-existing untracked\n"),
            baseline["status"]["dirty-disappeared.txt"],
        )

        (self.repo / "allowed.txt").write_text("allowed worker change\n")
        (self.repo / "staged.txt").write_text("staged worker change\n")
        run_git(self.repo, "add", "staged.txt")
        (self.repo / "delete.txt").unlink()
        run_git(self.repo, "mv", "rename-old.txt", "rename-new.txt")
        (self.repo / "allowed-untracked.txt").write_text("allowed untracked\n")
        (self.repo / "unexpected.txt").write_text("unexpected scope drift\n")
        (self.repo / "dirty-modified.txt").write_text("worker replaced dirty content\n")
        (self.repo / "dirty-disappeared.txt").unlink()

        allowed_paths = [
            "allowed.txt",
            "staged.txt",
            "delete.txt",
            "rename-old.txt",
            "rename-new.txt",
            "allowed-untracked.txt",
        ]
        expected_artifacts = {
            "staged_name_status": run_git(
                self.repo, "diff", "--cached", "--name-status"
            ).stdout.decode(),
            "unstaged_name_status": run_git(
                self.repo, "diff", "--name-status"
            ).stdout.decode(),
            "staged_stat": run_git(self.repo, "diff", "--cached", "--stat").stdout.decode(),
            "unstaged_stat": run_git(self.repo, "diff", "--stat").stdout.decode(),
        }
        expected_task_patch = run_git(
            self.repo, "diff", "--binary", baseline["head_oid"], "--", *allowed_paths
        ).stdout.decode()
        untracked_patch = subprocess.run(
            [
                "git", "-C", str(self.repo), "diff", "--no-index", "--binary", "--",
                os.devnull, "allowed-untracked.txt",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, untracked_patch.returncode)
        expected_artifacts["task_patch"] = expected_task_patch + untracked_patch.stdout

        run_dir = self.root / "run"
        evidence = self.git.capture_closure_evidence(
            repository=self.repo,
            run_dir=run_dir,
            attempt_id="attempt-001",
            task_baseline=baseline,
            task_baseline_digest="baseline-digest",
            allowed_paths=allowed_paths,
            policy_sha256="policy-digest",
            manifest_sha256="manifest-digest",
            prompt_sha256="prompt-digest",
            adapter_state_digest="adapter-digest",
        )
        fields = evidence["closure_fields"]
        observations = fields["controller_observations"]

        self.assertEqual(baseline["head_oid"], fields["head_before"])
        self.assertEqual(baseline["head_oid"], fields["head_after"])
        self.assertTrue(observations["index_changed"])
        self.assertIn("worker changed the Git index", evidence["mechanical_violations"])
        self.assertEqual(
            ["dirty-modified.txt"], observations["modified_preexisting_paths"]
        )
        self.assertEqual(
            ["dirty-disappeared.txt"], observations["disappeared_preexisting_paths"]
        )
        self.assertEqual(["unexpected.txt"], observations["unexpected_paths"])
        self.assertIn("allowed-untracked.txt", observations["untracked_paths"])
        self.assertEqual(
            status_value(" M", b"allowed worker change\n"),
            evidence["current_status"]["allowed.txt"],
        )
        self.assertEqual(
            status_value("M ", b"staged worker change\n"),
            evidence["current_status"]["staged.txt"],
        )
        self.assertEqual(
            status_value(" D", b"<missing>"),
            evidence["current_status"]["delete.txt"],
        )
        self.assertEqual(
            status_value("R ", b"rename baseline\n"),
            evidence["current_status"]["rename-new.txt"],
        )
        self.assertEqual(
            status_value(" M", b"unchanged dirty\n"),
            evidence["current_status"]["dirty-unchanged.txt"],
        )
        self.assertIn("D\tdelete.txt", fields["unstaged_changes"])
        self.assertIn("R100\trename-old.txt\trename-new.txt", fields["staged_changes"])

        patch = fields["task_patch"]
        self.assertIn("allowed worker change", patch)
        self.assertIn("staged worker change", patch)
        self.assertIn("allowed untracked", patch)
        self.assertIn("delete baseline", patch)
        self.assertIn("rename from rename-old.txt", patch)
        self.assertIn("rename to rename-new.txt", patch)
        self.assertNotIn("unexpected scope drift", patch)
        self.assertNotIn("worker replaced dirty content", patch)
        self.assertNotIn("unchanged dirty", patch)

        expected_names = {
            "staged_name_status",
            "unstaged_name_status",
            "staged_stat",
            "unstaged_stat",
            "task_patch",
        }
        self.assertEqual(expected_names, set(fields["evidence_artifacts"]))
        for name, artifact in fields["evidence_artifacts"].items():
            artifact_path = run_dir / artifact["path"]
            content = artifact_path.read_text()
            self.assertEqual(expected_artifacts[name], content, name)
            self.assertEqual(sha256_text(content), artifact["sha256"], name)
        self.assertEqual(sha256_text(patch), fields["task_patch_digest"])

    def test_task_patch_excludes_allowed_paths_that_were_dirty_at_baseline(self):
        (self.repo / "dirty-modified.txt").write_text("pre-existing allowed dirty\n")
        (self.repo / "dirty-unchanged.txt").write_text(
            "pre-existing allowed unchanged\n"
        )
        baseline = self.git.capture_task_baseline(self.repo)

        (self.repo / "dirty-modified.txt").write_text(
            "worker changed allowed dirty\n"
        )
        run_dir = self.root / "run"
        evidence = self.git.capture_closure_evidence(
            repository=self.repo,
            run_dir=run_dir,
            attempt_id="attempt-001",
            task_baseline=baseline,
            task_baseline_digest="baseline-digest",
            allowed_paths=["dirty-modified.txt", "dirty-unchanged.txt"],
            policy_sha256="policy-digest",
            manifest_sha256="manifest-digest",
            prompt_sha256="prompt-digest",
            adapter_state_digest="adapter-digest",
        )

        fields = evidence["closure_fields"]
        self.assertEqual("", fields["task_patch"])
        task_patch_artifact = run_dir / fields["evidence_artifacts"]["task_patch"]["path"]
        self.assertEqual("", task_patch_artifact.read_text())

    def test_status_preserves_unusual_path_identity_without_shell_interpretation(self):
        unusual_paths = (
            "space name.txt",
            "-leading-dash.txt",
            "tab\tname.txt",
            "line\nname.txt",
            "shell$(touch side-effect).txt",
        )
        for path in unusual_paths:
            (self.repo / path).write_text(path)
        blob = subprocess.run(
            ["git", "-C", str(self.repo), "hash-object", "-w", "--stdin"],
            input=b"raw path\n",
            check=True,
            capture_output=True,
        ).stdout.strip()
        subprocess.run(
            [
                b"git",
                b"-C",
                os.fsencode(self.repo),
                b"update-index",
                b"--add",
                b"--cacheinfo",
                b"100644",
                blob,
                b"non-utf-8-\xff.txt",
            ],
            check=True,
            capture_output=True,
        )

        status = self.git.capture_git_status(self.repo)

        self.assertTrue(set(unusual_paths).issubset(status))
        self.assertIn(os.fsdecode(b"non-utf-8-\xff.txt"), status)
        self.assertFalse((self.repo / "side-effect").exists())

    def test_shell_metacharacter_is_literal_in_untracked_patch(self):
        baseline = self.git.capture_task_baseline(self.repo)
        path = "literal;touch injected.txt"
        (self.repo / path).write_text("literal path content\n")

        evidence = self.git.capture_closure_evidence(
            repository=self.repo,
            run_dir=self.root / "run",
            attempt_id="attempt-001",
            task_baseline=baseline,
            task_baseline_digest="baseline-digest",
            allowed_paths=[path],
            policy_sha256="policy-digest",
            manifest_sha256="manifest-digest",
            prompt_sha256="prompt-digest",
            adapter_state_digest="adapter-digest",
        )

        self.assertIn("literal path content", evidence["closure_fields"]["task_patch"])
        self.assertFalse((self.repo / "injected.txt").exists())

    def test_nonzero_git_command_cannot_publish_complete_evidence(self):
        baseline = self.git.capture_task_baseline(self.repo)
        run_dir = self.root / "run"

        with self.assertRaises(subprocess.CalledProcessError):
            self.git.capture_closure_evidence(
                repository=self.root / "not-a-repository",
                run_dir=run_dir,
                attempt_id="attempt-001",
                task_baseline=baseline,
                task_baseline_digest="baseline-digest",
                allowed_paths=["allowed.txt"],
                policy_sha256="policy-digest",
                manifest_sha256="manifest-digest",
                prompt_sha256="prompt-digest",
                adapter_state_digest="adapter-digest",
            )

        self.assertFalse((run_dir / "closure").exists())

    def test_repository_top_level_is_explicit(self):
        nested = self.repo / "nested"
        nested.mkdir()
        self.assertEqual(self.repo.resolve(), self.git.repository_top_level(nested))


class ControllerGitWiringTest(unittest.TestCase):
    def test_run_next_uses_controller_git_task_baseline(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            repo.mkdir()
            run_git(repo, "init", "-q")
            run_git(repo, "config", "user.name", "Test")
            run_git(repo, "config", "user.email", "test@example.invalid")
            (repo / "allowed.txt").write_text("baseline\n")
            (repo / "tasks").mkdir()
            (repo / "tasks" / "T1.md").write_text("# T1\n")
            run_git(repo, "add", ".")
            run_git(repo, "commit", "-qm", "baseline")
            controller = load_module(CONTROLLER_PATH, "task_orchestrator_controller_wiring")
            policy = {
                "version": 1,
                "run_id": "run-1",
                "repository": str(repo),
                "task_ids": ["T1"],
                "verification": {
                    "targeted_checks": ["python3 -m unittest test_targeted"],
                    "repository_gate": None,
                    "authorized_gap": None,
                },
                "permissions": {
                    "sandbox": "workspace-write",
                    "approval_policy": "never",
                    "network": False,
                    "dependency_install": False,
                    "writable_roots": [str(repo)],
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
            manifest = {
                "version": 1,
                "manifest_id": "test",
                "completed_task_ids": [],
                "tasks": [{
                    "id": "T1",
                    "title": "Test",
                    "brief_path": "tasks/T1.md",
                    "dependencies": [],
                    "allowed_paths": ["allowed.txt"],
                    "required_checks": ["python3 -m unittest test_targeted"],
                }],
            }
            policy_path = root / "policy.json"
            manifest_path = root / "manifest.json"
            controller.persist_run_policy(policy_path, policy)
            manifest_path.write_text(json.dumps(manifest))
            run_dir = root / "run"
            controller.init_run(run_dir, policy_path, manifest_path, repo)
            fake_codex = root / "fake-codex"
            fake_codex.write_text("#!/bin/sh\nexit 0\n")
            fake_codex.chmod(0o755)

            sentinel = RuntimeError("controller-git task baseline sentinel")
            with (
                mock.patch.dict(sys.modules, {"codex_worker": controller._worker_module}),
                mock.patch.object(
                    controller._git_module,
                    "capture_task_baseline",
                    side_effect=sentinel,
                ),
                self.assertRaisesRegex(RuntimeError, "controller-git task baseline sentinel"),
            ):
                controller._cli_run_next(SimpleNamespace(
                    run_dir=str(run_dir), timeout_seconds=10.0, codex_bin=str(fake_codex)
                ))


if __name__ == "__main__":
    unittest.main()
