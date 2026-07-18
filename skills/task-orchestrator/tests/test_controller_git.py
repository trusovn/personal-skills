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

    def test_accepted_workspace_requires_exact_git_and_evidence_bytes(self):
        (self.repo / "dirty-unchanged.txt").write_text("pre-existing dirty\n")
        baseline = self.git.capture_task_baseline(self.repo)
        baseline_digest = sha256_text(self.git._canonical_json(baseline))
        (self.repo / "allowed.txt").write_text("worker change\n")
        run_dir = self.root / "accepted-run"
        (run_dir / "baselines").mkdir(parents=True)
        (run_dir / "baselines" / "task-001.json").write_text(json.dumps(baseline))
        evidence = self.git.capture_closure_evidence(
            repository=self.repo,
            run_dir=run_dir,
            attempt_id="attempt-001",
            task_baseline=baseline,
            task_baseline_digest=baseline_digest,
            allowed_paths=["allowed.txt"],
            policy_sha256="policy-digest",
            manifest_sha256="manifest-digest",
            prompt_sha256="prompt-digest",
            adapter_state_digest="adapter-digest",
        )
        closure = {
            "run_id": "run-1",
            "task_id": "T1",
            "attempt_id": "attempt-001",
            "policy_sha256": "policy-digest",
            "manifest_sha256": "manifest-digest",
            "baseline_sha256": baseline_digest,
            "prompt_sha256": "prompt-digest",
            **evidence["closure_fields"],
        }
        closure["controller_observations"]["mechanical_violations"] = []
        closure_path = run_dir / "closure" / "attempt-001.json"
        closure_path.write_text(json.dumps(closure))
        arguments = {
            "repository": self.repo,
            "run_dir": run_dir,
            "task_baseline_ref": "task-001.json",
            "task_baseline_digest": baseline_digest,
            "closure_ref": "closure/attempt-001.json",
            "allowed_paths": ["allowed.txt"],
            "expected_identity": {
                "run_id": "run-1",
                "task_id": "T1",
                "attempt_id": "attempt-001",
                "policy_sha256": "policy-digest",
                "manifest_sha256": "manifest-digest",
                "prompt_sha256": "prompt-digest",
            },
        }
        self.git.validate_accepted_workspace(**arguments)

        (self.repo / "allowed.txt").write_text("later! change\n")
        with self.assertRaisesRegex(ValueError, "bytes changed after acceptance"):
            self.git.validate_accepted_workspace(**arguments)
        (self.repo / "allowed.txt").write_text("worker change\n")

        (self.repo / "dirty-unchanged.txt").write_text("external dirty edit\n")
        with self.assertRaisesRegex(ValueError, "Pre-existing repository state"):
            self.git.validate_accepted_workspace(**arguments)
        (self.repo / "dirty-unchanged.txt").write_text("pre-existing dirty\n")

        (self.repo / "unexpected.txt").write_text("unexpected\n")
        with self.assertRaisesRegex(ValueError, "Unexpected repository path"):
            self.git.validate_accepted_workspace(**arguments)
        (self.repo / "unexpected.txt").unlink()

        run_git(self.repo, "add", "allowed.txt")
        with self.assertRaisesRegex(ValueError, "index changed after acceptance"):
            self.git.validate_accepted_workspace(**arguments)
        run_git(self.repo, "restore", "--staged", "allowed.txt")

        patch_path = run_dir / closure["evidence_artifacts"]["task_patch"]["path"]
        exact_patch = patch_path.read_text()
        patch_path.write_text(exact_patch + "tamper\n")
        with self.assertRaisesRegex(ValueError, "artifact digest mismatch"):
            self.git.validate_accepted_workspace(**arguments)
        patch_path.write_text(exact_patch)

        run_git(self.repo, "add", "allowed.txt")
        run_git(self.repo, "commit", "-qm", "external accepted-output commit")
        with self.assertRaisesRegex(ValueError, "HEAD changed after acceptance"):
            self.git.validate_accepted_workspace(**arguments)

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
        self.assertTrue(evidence["index_changed"])
        self.assertNotIn("mechanical_violations", evidence)
        self.assertNotIn("mechanical_violations", observations)
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

    def test_closure_evidence_returns_raw_comparison_facts_without_worker_policy(self):
        baseline = self.git.capture_task_baseline(self.repo)
        (self.repo / "allowed.txt").write_text("committed worker change\n")
        run_git(self.repo, "add", "allowed.txt")
        run_git(self.repo, "commit", "-qm", "worker commit")
        (self.repo / "staged.txt").write_text("staged worker change\n")
        run_git(self.repo, "add", "staged.txt")

        evidence = self.git.capture_closure_evidence(
            repository=self.repo,
            run_dir=self.root / "run-comparison-facts",
            attempt_id="attempt-001",
            task_baseline=baseline,
            task_baseline_digest="baseline-digest",
            allowed_paths=["allowed.txt", "staged.txt"],
            policy_sha256="policy-digest",
            manifest_sha256="manifest-digest",
            prompt_sha256="prompt-digest",
            adapter_state_digest="adapter-digest",
        )

        self.assertTrue(evidence["head_changed"])
        self.assertTrue(evidence["index_changed"])
        self.assertNotIn("mechanical_violations", evidence)
        self.assertNotIn(
            "mechanical_violations",
            evidence["closure_fields"]["controller_observations"],
        )

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

    def test_task_patch_excludes_both_sides_of_preexisting_rename(self):
        (self.repo / "old.txt").write_text("pre-existing rename\n")
        run_git(self.repo, "add", "old.txt")
        run_git(self.repo, "commit", "-qm", "add rename source")
        run_git(self.repo, "mv", "old.txt", "new.txt")
        baseline = self.git.capture_task_baseline(self.repo)

        for allowed_paths in (["old.txt"], ["new.txt"], ["old.txt", "new.txt"]):
            with self.subTest(allowed_paths=allowed_paths):
                evidence = self.git.capture_closure_evidence(
                    repository=self.repo,
                    run_dir=self.root / ("run-" + "-".join(allowed_paths)),
                    attempt_id="attempt-001",
                    task_baseline=baseline,
                    task_baseline_digest="baseline-digest",
                    allowed_paths=allowed_paths,
                    policy_sha256="policy-digest",
                    manifest_sha256="manifest-digest",
                    prompt_sha256="prompt-digest",
                    adapter_state_digest="adapter-digest",
                )

                self.assertEqual("", evidence["closure_fields"]["task_patch"])
                observations = evidence["closure_fields"]["controller_observations"]
                self.assertEqual([], observations["disappeared_preexisting_paths"])
                self.assertEqual([], observations["modified_preexisting_paths"])

        self.assertEqual(
            status_value("R ", b"<missing>"), baseline["status"]["old.txt"]
        )
        self.assertEqual(
            status_value("R ", b"pre-existing rename\n"),
            baseline["status"]["new.txt"],
        )

        (self.repo / "new.txt").write_text("modified pre-existing rename\n")
        modified = self.git.capture_closure_evidence(
            repository=self.repo,
            run_dir=self.root / "run-modified-rename",
            attempt_id="attempt-001",
            task_baseline=baseline,
            task_baseline_digest="baseline-digest",
            allowed_paths=["old.txt", "new.txt"],
            policy_sha256="policy-digest",
            manifest_sha256="manifest-digest",
            prompt_sha256="prompt-digest",
            adapter_state_digest="adapter-digest",
        )
        modified_observations = modified["closure_fields"]["controller_observations"]
        self.assertEqual(
            ["new.txt", "old.txt"],
            modified_observations["modified_preexisting_paths"],
        )
        self.assertEqual("", modified["closure_fields"]["task_patch"])

        run_git(self.repo, "restore", "--staged", "--", "old.txt", "new.txt")
        run_git(self.repo, "restore", "--worktree", "--", "old.txt")
        (self.repo / "new.txt").unlink()
        disappeared = self.git.capture_closure_evidence(
            repository=self.repo,
            run_dir=self.root / "run-disappeared-rename",
            attempt_id="attempt-001",
            task_baseline=baseline,
            task_baseline_digest="baseline-digest",
            allowed_paths=["old.txt", "new.txt"],
            policy_sha256="policy-digest",
            manifest_sha256="manifest-digest",
            prompt_sha256="prompt-digest",
            adapter_state_digest="adapter-digest",
        )
        disappeared_observations = disappeared["closure_fields"][
            "controller_observations"
        ]
        self.assertEqual(
            ["new.txt", "old.txt"],
            disappeared_observations["disappeared_preexisting_paths"],
        )
        self.assertEqual("", disappeared["closure_fields"]["task_patch"])

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

    def test_status_preserves_both_copy_path_identities(self):
        source = "copy\nsource.txt"
        destination = "copy\tdestination.txt"
        for path in (source, destination):
            (self.repo / path).write_text("copied content\n")
        porcelain = f"C  {destination}\0{source}\0".encode()

        with mock.patch.object(
            self.git,
            "_run_git",
            return_value=subprocess.CompletedProcess([], 0, porcelain, b""),
        ):
            status = self.git.capture_git_status(self.repo)

        expected = status_value("C ", b"copied content\n")
        self.assertEqual({source: expected, destination: expected}, status)

    def test_closure_evidence_preserves_unusual_paths_and_artifact_digests(self):
        baseline = self.git.capture_task_baseline(self.repo)
        unusual_paths = [
            "space name.txt",
            "-leading-dash.txt",
            "tab\tname.txt",
            "line\nname.txt",
            "shell$(touch side-effect).txt",
        ]
        for index, path in enumerate(unusual_paths):
            (self.repo / path).write_text(f"unusual content {index}\n")

        raw_path = os.fsdecode(b"non-utf-8-\xff.txt")
        blob = subprocess.run(
            ["git", "-C", str(self.repo), "hash-object", "-w", "--stdin"],
            input=b"raw path content\n",
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
                os.fsencode(raw_path),
            ],
            check=True,
            capture_output=True,
        )
        allowed_paths = [*unusual_paths, raw_path]
        original_run_git = self.git._run_git

        with mock.patch.object(self.git, "_run_git", wraps=original_run_git) as git_call:
            evidence = self.git.capture_closure_evidence(
                repository=self.repo,
                run_dir=self.root / "run-unusual-paths",
                attempt_id="attempt-001",
                task_baseline=baseline,
                task_baseline_digest="baseline-digest",
                allowed_paths=allowed_paths,
                policy_sha256="policy-digest",
                manifest_sha256="manifest-digest",
                prompt_sha256="prompt-digest",
                adapter_state_digest="adapter-digest",
            )

        git_call.assert_any_call(
            self.repo,
            "diff",
            "--binary",
            baseline["head_oid"],
            "--",
            *allowed_paths,
        )
        self.assertTrue(set(allowed_paths).issubset(evidence["current_status"]))
        self.assertEqual(
            sorted(unusual_paths),
            evidence["closure_fields"]["untracked_paths"],
        )
        self.assertFalse((self.repo / "side-effect").exists())

        fields = evidence["closure_fields"]
        patch = fields["task_patch"]
        for index in range(len(unusual_paths)):
            self.assertIn(f"unusual content {index}", patch)
        # The sandbox permits the raw-byte index identity but not creation of
        # its matching worktree path, so no raw-file content enters this patch.
        self.assertIn(raw_path, evidence["current_status"])
        for name, artifact in fields["evidence_artifacts"].items():
            content = (self.root / "run-unusual-paths" / artifact["path"]).read_text(
                errors="surrogateescape"
            )
            self.assertEqual(sha256_text(content), artifact["sha256"], name)
        self.assertEqual(sha256_text(patch), fields["task_patch_digest"])

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
    def test_run_next_uses_controller_git_task_baseline_and_closure_evidence(self):
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
            fake_codex.write_text(
                """#!/usr/bin/env python3
import json
from pathlib import Path
import sys

args = sys.argv[1:]
if "--help" in args:
    raise SystemExit(0)
Path.cwd().joinpath("allowed.txt").write_text("worker change\\n")
print(json.dumps({"type": "thread.started", "thread_id": "thread-wiring"}), flush=True)
result_path = Path(args[args.index("-o") + 1])
result_path.write_text(json.dumps({
    "status": "complete",
    "task_id": "T1",
    "summary": "done",
    "files_changed": ["allowed.txt"],
    "verification": [],
    "decisions": [],
    "questions": [],
    "risks": [],
    "next_action": "inspect",
}))
"""
            )
            fake_codex.chmod(0o755)

            original_task_baseline = controller._git_module.capture_task_baseline
            original_closure_evidence = controller._git_module.capture_closure_evidence
            with (
                mock.patch.dict(sys.modules, {"codex_worker": controller._worker_module}),
                mock.patch.object(
                    controller._git_module,
                    "capture_task_baseline",
                    wraps=original_task_baseline,
                ) as task_baseline,
                mock.patch.object(
                    controller._git_module,
                    "capture_closure_evidence",
                    wraps=original_closure_evidence,
                ) as closure_evidence,
                mock.patch("builtins.print"),
            ):
                return_code = controller._cli_run_next(SimpleNamespace(
                    run_dir=str(run_dir), timeout_seconds=10.0, codex_bin=str(fake_codex)
                ))

            self.assertEqual(0, return_code)
            task_baseline.assert_called_once_with(repo.resolve())
            closure_evidence.assert_called_once()
            closure = json.loads((run_dir / "closure" / "attempt-001.json").read_text())
            self.assertEqual("worker change\n", (repo / "allowed.txt").read_text())
            self.assertIn("worker change", closure["task_patch"])
            self.assertEqual(
                closure["task_patch_digest"],
                sha256_text(closure["task_patch"]),
            )


if __name__ == "__main__":
    unittest.main()
