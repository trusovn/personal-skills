import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SKILL = ROOT / "skills" / "task-implementation-flow" / "bounded-task-implementer"
MODULE_PATH = SCRIPTS / "run_evidence.py"

sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("run_evidence_availability", MODULE_PATH)
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


def init_repo(repo: Path) -> None:
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "tests@example.com")
    git(repo, "config", "user.name", "Run Evidence Availability Tests")
    (repo / ".gitignore").write_text(".agents/\n", encoding="utf-8")
    (repo / "app.txt").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "baseline")


def install_skill(repo: Path) -> Path:
    target = repo / ".agents" / "skills" / "task-implementation-flow" / "bounded-task-implementer"
    shutil.copytree(SKILL, target)
    return target


def install_shared_scripts(repo: Path, names: tuple[str, ...]) -> Path:
    target = repo / ".agents" / "scripts"
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copy2(SCRIPTS / name, target / name)
    return target


class RunEvidenceAvailabilityTests(unittest.TestCase):
    def test_complete_ignored_agents_install_is_available_without_dirtying_repo(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo)
            install_skill(repo)
            scripts = install_shared_scripts(
                repo,
                (
                    "run_evidence.py",
                    "workflow_version.py",
                    "runtime_context.py",
                    "runtime-context.schema.v1.json",
                ),
            )

            before = git(repo, "status", "--porcelain=v1")
            result = subprocess.run(
                [sys.executable, str(scripts / "run_evidence.py"), "--repo", str(repo), "availability"],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )
            after = git(repo, "status", "--porcelain=v1")

            self.assertEqual(0, result.returncode, result.stderr)
            info = json.loads(result.stdout)
            self.assertTrue(info["available"])
            self.assertEqual([], info["missing"])
            self.assertIsNone(info["reason"])
            self.assertEqual(str(repo / ".agents"), info["installation_root"])
            self.assertTrue(info["workflow"]["fingerprint"].startswith("sha256:"))
            self.assertEqual(before, after)

    def test_incomplete_agents_install_reports_missing_dependencies_cleanly(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo)
            install_skill(repo)
            scripts = install_shared_scripts(repo, ("run_evidence.py",))

            result = subprocess.run(
                [sys.executable, str(scripts / "run_evidence.py"), "--repo", str(repo), "availability"],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(2, result.returncode)
            info = json.loads(result.stdout)
            self.assertFalse(info["available"])
            self.assertEqual("missing_shared_dependencies", info["reason"])
            self.assertEqual(
                {
                    "runtime-context.schema.v1.json",
                    "runtime_context.py",
                    "workflow_version.py",
                },
                set(info["missing"]),
            )
            self.assertNotIn("Traceback", result.stderr)

    def test_project_local_install_is_used_even_with_stale_user_global_skill(self):
        with tempfile.TemporaryDirectory() as tempdir, tempfile.TemporaryDirectory() as homedir:
            repo = Path(tempdir)
            home = Path(homedir)
            init_repo(repo)
            install_skill(repo)
            scripts = install_shared_scripts(
                repo,
                (
                    "run_evidence.py",
                    "workflow_version.py",
                    "runtime_context.py",
                    "runtime-context.schema.v1.json",
                ),
            )

            stale = home / ".agents" / "skills" / "bounded-task-implementer"
            stale.mkdir(parents=True)
            (stale / "SKILL.md").write_text(
                "---\nname: bounded-task-implementer\ndescription: stale global copy\n---\nstale\n",
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["HOME"] = str(home)
            result = subprocess.run(
                [sys.executable, str(scripts / "run_evidence.py"), "--repo", str(repo), "availability"],
                cwd=repo,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            info = json.loads(result.stdout)
            self.assertTrue(info["available"])
            self.assertEqual(str(repo / ".agents"), info["installation_root"])

    def test_git_metadata_failure_is_classified_as_unavailable(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            git(repo, "init", "-q")
            git(repo, "config", "user.email", "tests@example.com")
            git(repo, "config", "user.name", "Run Evidence Availability Tests")
            skill = repo / "skills" / "bounded-task-implementer"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: bounded-task-implementer\ndescription: test\n---\nbody\n",
                encoding="utf-8",
            )
            git(repo, "add", ".")
            git(repo, "commit", "-qm", "baseline")

            original_storage_root = run_evidence.storage_root

            def denied(_repo: Path) -> Path:
                raise run_evidence.RunEvidenceError("permission denied")

            try:
                run_evidence.storage_root = denied
                info = run_evidence.evidence_availability(repo)
            finally:
                run_evidence.storage_root = original_storage_root

            self.assertFalse(info["available"])
            self.assertEqual("git_metadata_unwritable", info["reason"])
            self.assertIn("permission denied", info["error"])

    def test_skill_declares_repo_local_precedence_and_single_skip(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Repository-local `.agents/skills/` takes precedence", text)
        self.assertIn("Do not probe a user-global skill path", text)
        self.assertIn("run_evidence.py --repo <worktree> availability", text)
        self.assertIn("do not retry evidence operations during this invocation", text)
        self.assertIn("explicit repository, user, or machine", text)


if __name__ == "__main__":
    unittest.main()
