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


class WorkflowVersionTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "tests@example.com")
        git(self.repo, "config", "user.name", "Workflow Version Tests")
        git(self.repo, "config", "core.quotePath", "true")

        self.skill = self.repo / "skills" / "bounded-task-implementer"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: bounded-task-implementer\ndescription: test skill\n---\nbody\n",
            encoding="utf-8",
        )
        (self.skill / "references").mkdir()
        (self.skill / "references" / "rules.md").write_text("rule one\n", encoding="utf-8")

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


if __name__ == "__main__":
    unittest.main()
