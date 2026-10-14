import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "workflow_version.py"
SPEC = importlib.util.spec_from_file_location("workflow_version", MODULE_PATH)
workflow_version = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(workflow_version)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def write_skill_fixture(repo: Path) -> Path:
    """Write the bounded-task-implementer fixture into a repository's skills tree."""
    skill = repo / "skills" / "bounded-task-implementer"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: bounded-task-implementer\ndescription: test skill\n---\nbody\n",
        encoding="utf-8",
    )
    (skill / "references").mkdir()
    (skill / "references" / "rules.md").write_text("rule one\n", encoding="utf-8")
    return skill


class WorkflowVersionTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name).resolve()
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "tests@example.com")
        git(self.repo, "config", "user.name", "Workflow Version Tests")
        git(self.repo, "config", "core.quotePath", "true")

        self.skill = write_skill_fixture(self.repo)

        other = self.repo / "skills" / "other-skill"
        other.mkdir(parents=True)
        (other / "SKILL.md").write_text(
            "---\nname: other-skill\ndescription: other skill\n---\nbody\n",
            encoding="utf-8",
        )

        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "initial")

    def tearDown(self):
        self.tempdir.cleanup()

    def version(self):
        return workflow_version.get_workflow_version(
            self.repo, "bounded-task-implementer"
        )

    def test_unchanged_workflow_is_stable(self):
        first = self.version()
        second = self.version()
        self.assertEqual(first["fingerprint"], second["fingerprint"])
        self.assertFalse(first["workflow_dirty"])

    def test_included_file_change_changes_fingerprint_and_marks_dirty(self):
        before = self.version()
        rules = self.skill / "references" / "rules.md"
        rules.write_text("rule two\n", encoding="utf-8")

        after = self.version()

        self.assertNotEqual(before["fingerprint"], after["fingerprint"])
        self.assertTrue(after["workflow_dirty"])
        self.assertTrue(after["repository_dirty"])

    def test_unicode_untracked_file_changes_fingerprint_and_marks_dirty(self):
        before = self.version()
        (self.skill / "version-é.txt").write_text("new input\n", encoding="utf-8")

        after = self.version()

        self.assertNotEqual(before["fingerprint"], after["fingerprint"])
        self.assertTrue(after["workflow_dirty"])

    def test_unrelated_change_does_not_change_workflow_fingerprint(self):
        before = self.version()
        unrelated = self.repo / "skills" / "other-skill" / "SKILL.md"
        unrelated.write_text(
            "---\nname: other-skill\ndescription: changed elsewhere\n---\nbody\n",
            encoding="utf-8",
        )

        after = self.version()

        self.assertEqual(before["fingerprint"], after["fingerprint"])
        self.assertFalse(after["workflow_dirty"])
        self.assertTrue(after["repository_dirty"])

    def test_dirty_fingerprint_uses_current_worktree_content(self):
        before = self.version()
        skill_md = self.skill / "SKILL.md"
        skill_md.write_text(
            "---\nname: bounded-task-implementer\ndescription: dirty content\n---\nbody\n",
            encoding="utf-8",
        )
        dirty = self.version()
        git(self.repo, "add", str(skill_md.relative_to(self.repo)))
        git(self.repo, "commit", "-m", "update workflow")
        committed = self.version()

        self.assertTrue(dirty["workflow_dirty"])
        self.assertNotEqual(before["fingerprint"], dirty["fingerprint"])
        self.assertEqual(dirty["fingerprint"], committed["fingerprint"])
        self.assertFalse(committed["workflow_dirty"])

    def test_development_only_files_do_not_change_fingerprint(self):
        before = self.version()
        evals = self.skill / "evals"
        evals.mkdir()
        (evals / "evals.json").write_text('{"changed": true}\\n', encoding="utf-8")
        git(self.repo, "add", str((evals / "evals.json").relative_to(self.repo)))
        git(self.repo, "commit", "-m", "add eval only")

        after = self.version()

        self.assertEqual(before["fingerprint"], after["fingerprint"])
        self.assertFalse(after["workflow_dirty"])

    def test_repository_commit_is_independent_from_fingerprint(self):
        first = self.version()
        unrelated = self.repo / "README.md"
        unrelated.write_text("repo docs\n", encoding="utf-8")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-m", "unrelated commit")

        second = self.version()

        self.assertEqual(first["fingerprint"], second["fingerprint"])
        self.assertNotEqual(first["repository_commit"], second["repository_commit"])

    def test_repository_branch_is_reported(self):
        branch = git(self.repo, "branch", "--show-current").strip()

        info = self.version()

        self.assertEqual(branch, info["repository_branch"])

    def test_detached_head_reports_null_branch(self):
        commit = git(self.repo, "rev-parse", "HEAD").strip()
        git(self.repo, "checkout", "--detach", commit)

        info = self.version()

        self.assertIsNone(info["repository_branch"])
        self.assertEqual(commit, info["repository_commit"])

    def test_fingerprint_is_independent_of_discovery_order(self):
        canonical = workflow_version.fingerprint_workflow(self.repo, self.skill)
        expected_files = workflow_version.workflow_files(self.repo, self.skill)
        reversed_git_output = "\0".join(
            path.relative_to(self.repo).as_posix()
            for path in reversed(expected_files)
        ) + "\0"
        original_git = workflow_version._git

        def git_with_reversed_discovery(repo_root, *args):
            if args and args[0] == "ls-files":
                return reversed_git_output
            return original_git(repo_root, *args)

        try:
            workflow_version._git = git_with_reversed_discovery
            reversed_order = workflow_version.fingerprint_workflow(
                self.repo, self.skill
            )
        finally:
            workflow_version._git = original_git

        self.assertEqual(canonical, reversed_order)

    def test_copied_skill_is_portable_to_standalone_repository(self):
        source_fingerprint = self.version()["fingerprint"]

        with tempfile.TemporaryDirectory() as target_dir:
            target_repo = Path(target_dir)
            git(target_repo, "init")
            git(target_repo, "config", "user.email", "target@example.com")
            git(target_repo, "config", "user.name", "Target Repo Tests")

            target_skill = target_repo / "skills" / "bounded-task-implementer"
            (target_skill / "references").mkdir(parents=True)
            (target_skill / "SKILL.md").write_bytes((self.skill / "SKILL.md").read_bytes())
            (target_skill / "references" / "rules.md").write_bytes(
                (self.skill / "references" / "rules.md").read_bytes()
            )

            target_scripts = target_repo / "scripts"
            target_scripts.mkdir()
            target_script = target_scripts / "workflow_version.py"
            target_script.write_bytes(MODULE_PATH.read_bytes())

            git(target_repo, "add", ".")
            git(target_repo, "commit", "-m", "install selected workflow")
            target_commit = git(target_repo, "rev-parse", "HEAD").strip()
            target_branch = git(target_repo, "branch", "--show-current").strip()

            result = subprocess.run(
                ["python3", str(target_script), "bounded-task-implementer"],
                cwd=target_repo,
                check=True,
                capture_output=True,
                text=True,
            )
            info = json.loads(result.stdout)

            self.assertEqual(source_fingerprint, info["fingerprint"])
            self.assertEqual(target_commit, info["repository_commit"])
            self.assertEqual(target_branch, info["repository_branch"])
            self.assertFalse(info["repository_dirty"])
            self.assertFalse(info["workflow_dirty"])


    def test_project_local_agents_install_discovers_skills_beside_shared_script(self):
        source_fingerprint = self.version()["fingerprint"]

        with tempfile.TemporaryDirectory() as target_dir:
            target_repo = Path(target_dir)
            git(target_repo, "init")
            git(target_repo, "config", "user.email", "target@example.com")
            git(target_repo, "config", "user.name", "Target Repo Tests")

            target_skill = target_repo / ".agents" / "skills" / "bounded-task-implementer"
            (target_skill / "references").mkdir(parents=True)
            (target_skill / "SKILL.md").write_bytes((self.skill / "SKILL.md").read_bytes())
            (target_skill / "references" / "rules.md").write_bytes(
                (self.skill / "references" / "rules.md").read_bytes()
            )

            target_scripts = target_repo / ".agents" / "scripts"
            target_scripts.mkdir(parents=True)
            target_script = target_scripts / "workflow_version.py"
            target_script.write_bytes(MODULE_PATH.read_bytes())

            git(target_repo, "add", ".")
            git(target_repo, "commit", "-m", "install selected workflow under .agents")

            result = subprocess.run(
                ["python3", str(target_script), "bounded-task-implementer"],
                cwd=target_repo,
                check=True,
                capture_output=True,
                text=True,
            )
            info = json.loads(result.stdout)

            self.assertEqual(source_fingerprint, info["fingerprint"])
            self.assertFalse(info["workflow_dirty"])


    def test_ignored_project_local_agents_install_keeps_workflow_identity(self):
        source_fingerprint = self.version()["fingerprint"]

        with tempfile.TemporaryDirectory() as target_dir:
            target_repo = Path(target_dir)
            git(target_repo, "init")
            git(target_repo, "config", "user.email", "target@example.com")
            git(target_repo, "config", "user.name", "Target Repo Tests")
            (target_repo / ".gitignore").write_text(".agents/\n", encoding="utf-8")
            (target_repo / "app.txt").write_text("application\n", encoding="utf-8")
            git(target_repo, "add", ".")
            git(target_repo, "commit", "-m", "application baseline")

            target_skill = target_repo / ".agents" / "skills" / "bounded-task-implementer"
            (target_skill / "references").mkdir(parents=True)
            (target_skill / "SKILL.md").write_bytes((self.skill / "SKILL.md").read_bytes())
            (target_skill / "references" / "rules.md").write_bytes(
                (self.skill / "references" / "rules.md").read_bytes()
            )
            (target_skill / "evals").mkdir()
            (target_skill / "evals" / "ignored.json").write_text("ignored\n", encoding="utf-8")

            target_scripts = target_repo / ".agents" / "scripts"
            target_scripts.mkdir(parents=True)
            target_script = target_scripts / "workflow_version.py"
            target_script.write_bytes(MODULE_PATH.read_bytes())

            self.assertEqual("", git(target_repo, "status", "--porcelain=v1"))

            result = subprocess.run(
                ["python3", str(target_script), "bounded-task-implementer"],
                cwd=target_repo,
                check=True,
                capture_output=True,
                text=True,
            )
            info = json.loads(result.stdout)

            self.assertEqual(source_fingerprint, info["fingerprint"])
            self.assertNotEqual(
                "sha256:" + __import__("hashlib").sha256().hexdigest(),
                info["fingerprint"],
            )
            self.assertFalse(info["workflow_dirty"])
            self.assertFalse(info["repository_dirty"])
            self.assertEqual("", git(target_repo, "status", "--porcelain=v1"))


class UnbornWorkflowVersionTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name).resolve()
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "tests@example.com")
        git(self.repo, "config", "user.name", "Workflow Version Tests")
        git(self.repo, "config", "core.quotePath", "true")
        self.skill = write_skill_fixture(self.repo)
        # Deliberately no `git add`/`git commit`: HEAD names a still-unborn branch.

    def tearDown(self):
        self.tempdir.cleanup()

    def version(self):
        return workflow_version.get_workflow_version(
            self.repo, "bounded-task-implementer"
        )

    def test_unborn_head_reports_explicit_unborn_identity(self):
        branch = git(self.repo, "branch", "--show-current").strip()

        info = self.version()

        self.assertIsNone(info["repository_commit"])
        self.assertEqual(branch, info["repository_branch"])
        self.assertTrue(info["fingerprint"].startswith("sha256:"))

    def test_unborn_identity_transitions_to_real_commits_without_fingerprint_change(self):
        unborn = self.version()

        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "first commit")
        first = self.version()
        first_commit = git(self.repo, "rev-parse", "HEAD").strip()

        unrelated = self.repo / "README.md"
        unrelated.write_text("unrelated\n", encoding="utf-8")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-m", "later unrelated commit")
        later = self.version()
        later_commit = git(self.repo, "rev-parse", "HEAD").strip()

        self.assertIsNone(unborn["repository_commit"])
        self.assertEqual(first_commit, first["repository_commit"])
        self.assertEqual(later_commit, later["repository_commit"])
        self.assertNotEqual(first_commit, later_commit)
        self.assertEqual(unborn["fingerprint"], first["fingerprint"])
        self.assertEqual(first["fingerprint"], later["fingerprint"])
        self.assertFalse(first["workflow_dirty"])
        self.assertFalse(later["workflow_dirty"])

    def _version_with_ref_lookup(self, ref_lookup):
        """Read identity with one controlled `show-ref` lookup result.

        The unborn fallback path stays real: HEAD resolution fails on the
        still-unborn branch and `symbolic-ref` still resolves. Only the
        ref lookup is controlled, mirroring a ref-database I/O failure.
        """
        head_ref = git(self.repo, "symbolic-ref", "HEAD").strip()
        real_git_check = workflow_version._git_check

        def git_check(repo_root, *args):
            self.assertEqual(("show-ref", "--verify", "--quiet", head_ref), args)
            return ref_lookup

        try:
            workflow_version._git_check = git_check
            return self.version()
        finally:
            workflow_version._git_check = real_git_check

    def test_failed_branch_ref_lookup_is_not_reported_as_unborn(self):
        # A ref lookup that fails outright (a ref-database I/O error exits
        # 128) supplies no evidence that the branch ref is absent, so
        # identity must stay a Git failure, never unborn success.
        fatal_lookup = subprocess.CompletedProcess(
            args=[],
            returncode=128,
            stdout="",
            stderr="fatal: controlled ref-database I/O failure\n",
        )

        with self.assertRaises(workflow_version.WorkflowVersionError):
            self._version_with_ref_lookup(fatal_lookup)

    def test_existing_branch_ref_keeps_head_resolution_failure(self):
        # The single-failure control: when the branch ref verifies as
        # existing, the failed HEAD resolution stays the reported error.
        existing_ref = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )

        with self.assertRaises(workflow_version.WorkflowVersionError):
            self._version_with_ref_lookup(existing_ref)

    def test_git_failure_is_not_represented_as_unborn(self):
        with tempfile.TemporaryDirectory() as non_repo_dir:
            non_repo = Path(non_repo_dir).resolve()
            write_skill_fixture(non_repo)

            with self.assertRaises(workflow_version.WorkflowVersionError):
                workflow_version.get_workflow_version(
                    non_repo, "bounded-task-implementer"
                )

    def test_unresolvable_head_in_committed_repository_is_not_reported_as_unborn(self):
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "initial")
        (self.repo / ".git" / "HEAD").write_text(
            "not a symbolic ref or object\n", encoding="utf-8"
        )

        with self.assertRaises(workflow_version.WorkflowVersionError):
            self.version()


if __name__ == "__main__":
    unittest.main()
