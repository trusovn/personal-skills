import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "run_evidence.py"
SKILL_PATH = Path(__file__).resolve().parents[1] / "skills" / "task-implementation-flow" / "bounded-task-implementer" / "SKILL.md"
SPEC = importlib.util.spec_from_file_location("run_evidence", MODULE_PATH)
run_evidence = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(run_evidence)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


class RunEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "tests@example.com")
        git(self.repo, "config", "user.name", "Run Evidence Tests")
        (self.repo / "tracked.txt").write_text("initial\n", encoding="utf-8")
        skill = self.repo / "skills" / "task-implementation-flow" / "bounded-task-implementer"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: bounded-task-implementer\ndescription: test\n---\nbody\n",
            encoding="utf-8",
        )
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "initial")

    def tearDown(self):
        self.tempdir.cleanup()

    def manifest(self, run_id):
        root = run_evidence.storage_root(self.repo)
        return json.loads((root / "runs" / run_id / "manifest.json").read_text())

    def test_missing_task_and_runtime_metadata_are_valid(self):
        manifest = run_evidence.begin_run(self.repo)
        self.assertEqual({"id": None, "brief": None}, manifest["task"])
        self.assertEqual("unavailable", manifest["runtime"]["identity_source"])
        self.assertIsNone(manifest["runtime"]["runner"])
        self.assertEqual("bounded-task-implementer", manifest["workflow"]["id"])
        self.assertTrue(manifest["workflow"]["fingerprint"].startswith("sha256:"))


    def test_existing_task_metadata_is_recorded_without_becoming_required(self):
        brief = self.repo / "docs" / "tasks" / "T-1" / "brief.md"
        brief.parent.mkdir(parents=True)
        brief.write_text("# T-1\n", encoding="utf-8")
        manifest = run_evidence.begin_run(
            self.repo, task_id="T-1", task_brief="docs/tasks/T-1/brief.md"
        )
        self.assertEqual("T-1", manifest["task"]["id"])
        self.assertEqual("docs/tasks/T-1/brief.md", manifest["task"]["brief"])

    def test_trusted_runtime_context_is_consumed_via_generic_interface(self):
        runtime = {
            "schema_version": 1,
            "runner": "opencode",
            "provider": "ollama",
            "model": "qwen3-coder",
            "variant": "local",
            "effort": None,
            "session_id": "session-1",
            "identity_source": "adapter",
        }
        path = self.repo / "runtime-context.json"
        path.write_text(json.dumps(runtime), encoding="utf-8")
        manifest = run_evidence.begin_run(self.repo, runtime_context_path=path)
        self.assertEqual(runtime, manifest["runtime"])

    def test_begin_and_finish_persist_snapshots(self):
        begin = run_evidence.begin_run(self.repo)
        (self.repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
        finished = run_evidence.finish_run(self.repo, begin["run_id"], "completed")

        self.assertIsNotNone(finished["repository"]["begin"]["snapshot"])
        self.assertIsNotNone(finished["repository"]["finish"]["snapshot"])
        self.assertNotEqual(
            finished["repository"]["begin"]["snapshot"],
            finished["repository"]["finish"]["snapshot"],
        )
        self.assertEqual("explicit_finish", finished["closure"]["kind"])
        self.assertEqual("completed", finished["closure"]["outcome"])

    def test_snapshot_remains_usable_after_worktree_changes_again(self):
        begin = run_evidence.begin_run(self.repo)
        (self.repo / "tracked.txt").write_text("finish-state\n", encoding="utf-8")
        finished = run_evidence.finish_run(self.repo, begin["run_id"], "completed")
        finish_tree = finished["repository"]["finish"]["snapshot"]

        (self.repo / "tracked.txt").write_text("later-state\n", encoding="utf-8")
        listing = git(self.repo, "ls-tree", "-r", finish_tree)
        self.assertIn("tracked.txt", listing)
        blob = git(self.repo, "show", f"{finish_tree}:tracked.txt")
        self.assertEqual("finish-state\n", blob)

    def test_existing_dirty_worktree_is_captured_without_changing_status(self):
        (self.repo / "tracked.txt").write_text("dirty\n", encoding="utf-8")
        (self.repo / "untracked.txt").write_text("untracked\n", encoding="utf-8")
        before = git(self.repo, "status", "--porcelain=v1", "--untracked-files=all")

        manifest = run_evidence.begin_run(self.repo)

        after = git(self.repo, "status", "--porcelain=v1", "--untracked-files=all")
        self.assertTrue(manifest["repository"]["begin"]["dirty"])
        self.assertEqual(before, after)
        tree = manifest["repository"]["begin"]["snapshot"]
        self.assertEqual("dirty\n", git(self.repo, "show", f"{tree}:tracked.txt"))
        self.assertEqual("untracked\n", git(self.repo, "show", f"{tree}:untracked.txt"))

    def test_second_begin_exposes_existing_open_run(self):
        first = run_evidence.begin_run(self.repo)
        with self.assertRaises(run_evidence.ActiveRunError) as raised:
            run_evidence.begin_run(self.repo)
        self.assertEqual(first["run_id"], raised.exception.run_id)
        self.assertEqual(first["run_id"], run_evidence.active_run_id(run_evidence.storage_root(self.repo)))

    def test_explicit_interrupted_finish(self):
        started = run_evidence.begin_run(self.repo)
        finished = run_evidence.finish_run(
            self.repo, started["run_id"], "reported_interrupted"
        )
        self.assertEqual("explicit_finish", finished["closure"]["kind"])
        self.assertEqual("reported_interrupted", finished["closure"]["outcome"])
        self.assertIsNotNone(finished["session"]["finished_at"])

    def test_killed_agent_recovery_then_new_run_starts_at_takeover_state(self):
        run_a = run_evidence.begin_run(self.repo)
        (self.repo / "tracked.txt").write_text("takeover\n", encoding="utf-8")

        recovered = run_evidence.recover_run(self.repo, run_a["run_id"])
        recovery_tree = recovered["repository"]["finish"]["snapshot"]
        run_b = run_evidence.begin_run(self.repo)

        self.assertEqual("recovered_after_missing_finish", recovered["closure"]["kind"])
        self.assertIsNone(recovered["closure"]["outcome"])
        self.assertIsNotNone(recovered["closure"]["recovered_at"])
        self.assertEqual(recovery_tree, run_b["repository"]["begin"]["snapshot"])
        self.assertEqual(run_b["run_id"], run_evidence.active_run_id(run_evidence.storage_root(self.repo)))

    def test_architecture_check_captures_raw_facts_without_interpretation(self):
        started = run_evidence.begin_run(self.repo)
        check, exit_code = run_evidence.run_check(
            self.repo,
            started["run_id"],
            "architecture",
            [sys.executable, "-c", "import sys; print('OUT'); print('ERR', file=sys.stderr); raise SystemExit(7)"],
        )
        self.assertEqual(7, exit_code)
        self.assertEqual("architecture", check["kind"])
        self.assertIn("OUT", check["stdout"])
        self.assertIn("ERR", check["stderr"])
        self.assertEqual(7, check["exit_code"])
        self.assertIsInstance(check["duration_ms"], int)
        self.assertGreaterEqual(check["duration_ms"], 0)
        saved = self.manifest(started["run_id"])["checks"]
        self.assertEqual([check], saved)

    def test_collector_does_not_change_real_index_or_status(self):
        (self.repo / "staged.txt").write_text("staged\n", encoding="utf-8")
        git(self.repo, "add", "staged.txt")
        (self.repo / "tracked.txt").write_text("unstaged\n", encoding="utf-8")
        (self.repo / "untracked.txt").write_text("untracked\n", encoding="utf-8")
        status_before = git(self.repo, "status", "--porcelain=v1", "--untracked-files=all")
        index_before = git(self.repo, "write-tree").strip()

        started = run_evidence.begin_run(self.repo)
        run_evidence.finish_run(self.repo, started["run_id"], "completed")

        status_after = git(self.repo, "status", "--porcelain=v1", "--untracked-files=all")
        index_after = git(self.repo, "write-tree").strip()
        self.assertEqual(status_before, status_after)
        self.assertEqual(index_before, index_after)

    def test_evidence_storage_does_not_dirty_repository(self):
        self.assertEqual("", git(self.repo, "status", "--porcelain=v1"))
        started = run_evidence.begin_run(self.repo)
        run_evidence.finish_run(self.repo, started["run_id"], "completed")
        self.assertEqual("", git(self.repo, "status", "--porcelain=v1"))
        root = run_evidence.storage_root(self.repo)
        git_dir = Path(git(self.repo, "rev-parse", "--absolute-git-dir").strip())
        self.assertTrue(root.is_relative_to(git_dir))

    def test_manifest_contains_no_diff_or_statistics_artifacts(self):
        started = run_evidence.begin_run(self.repo)
        finished = run_evidence.finish_run(self.repo, started["run_id"], "completed")
        serialized = json.dumps(finished)
        for forbidden in ("session.patch", "additions", "deletions", "change_statistics"):
            self.assertNotIn(forbidden, serialized)

    def test_skill_keeps_ordinary_evidence_best_effort_and_task_metadata_optional(self):
        if not SKILL_PATH.exists():
            self.skipTest("skill source is not present in prototype workspace")
        text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("best-effort", text)
        self.assertIn("does not invalidate an otherwise executable bounded task", text)
        self.assertIn("Do not create a task brief", text)
        self.assertIn("task ID", text)
        self.assertIn("task package", text)
        self.assertIn("solely for evidence collection", text)
        self.assertIn("Runtime identity is optional", text)


    def test_ignored_agents_install_runs_copied_tooling_end_to_end(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            target_repo = root / "target-repo"
            target_repo.mkdir()
            git(target_repo, "init", "-q")
            git(target_repo, "config", "user.email", "target@example.com")
            git(target_repo, "config", "user.name", "Installed Tooling Tests")
            (target_repo / ".gitignore").write_text(".agents/\n", encoding="utf-8")
            (target_repo / "app.txt").write_text("baseline\n", encoding="utf-8")
            git(target_repo, "add", ".")
            git(target_repo, "commit", "-qm", "application baseline")

            target_skill = (
                target_repo
                / ".agents"
                / "skills"
                / "task-implementation-flow"
                / "bounded-task-implementer"
            )
            shutil.copytree(SKILL_PATH.parent, target_skill)

            target_scripts = target_repo / ".agents" / "scripts"
            target_scripts.mkdir(parents=True)
            for name in (
                "workflow_version.py",
                "runtime_context.py",
                "runtime-context.schema.v1.json",
                "run_evidence.py",
            ):
                shutil.copy2(SCRIPTS / name, target_scripts / name)

            runtime_path = root / "runtime-context.json"
            runtime = {
                "schema_version": 1,
                "runner": "test-runner",
                "provider": "test-provider",
                "model": "test-model",
                "variant": None,
                "effort": None,
                "session_id": "session-installed",
                "identity_source": "adapter",
            }
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")

            self.assertEqual("", git(target_repo, "status", "--porcelain=v1"))

            version_result = subprocess.run(
                [
                    sys.executable,
                    str(target_scripts / "workflow_version.py"),
                    "bounded-task-implementer",
                ],
                cwd=target_repo,
                check=True,
                capture_output=True,
                text=True,
            )
            version = json.loads(version_result.stdout)
            self.assertTrue(version["fingerprint"].startswith("sha256:"))
            self.assertNotEqual(
                "sha256:" + __import__("hashlib").sha256().hexdigest(),
                version["fingerprint"],
            )

            begin_result = subprocess.run(
                [
                    sys.executable,
                    str(target_scripts / "run_evidence.py"),
                    "--repo",
                    str(target_repo),
                    "begin",
                    "--runtime-context",
                    str(runtime_path),
                ],
                cwd=target_repo,
                check=True,
                capture_output=True,
                text=True,
            )
            begun = json.loads(begin_result.stdout)
            manifest_path = Path(begun["manifest"])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(version["fingerprint"], manifest["workflow"]["fingerprint"])
            self.assertEqual(runtime, manifest["runtime"])
            self.assertEqual("", git(target_repo, "status", "--porcelain=v1"))

            finish_result = subprocess.run(
                [
                    sys.executable,
                    str(target_scripts / "run_evidence.py"),
                    "--repo",
                    str(target_repo),
                    "finish",
                    begun["run_id"],
                    "--outcome",
                    "completed",
                ],
                cwd=target_repo,
                check=True,
                capture_output=True,
                text=True,
            )
            finished = json.loads(finish_result.stdout)
            self.assertEqual("explicit_finish", finished["closure"]["kind"])
            self.assertEqual("completed", finished["closure"]["outcome"])
            self.assertIsNotNone(finished["repository_finish"]["snapshot"])
            self.assertEqual("", git(target_repo, "status", "--porcelain=v1"))


if __name__ == "__main__":
    unittest.main()
