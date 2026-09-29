import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = ROOT / "scripts" / "install_development_skills.py"

SPEC = importlib.util.spec_from_file_location("install_development_skills", INSTALLER_PATH)
installer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(installer)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def init_repo(repo: Path, *, ignore_agents: bool = True, agents_text: str | None = None) -> None:
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "tests@example.com")
    git(repo, "config", "user.name", "Development Installer Tests")
    if ignore_agents:
        (repo / ".gitignore").write_text(".agents/\n", encoding="utf-8")
    (repo / "app.txt").write_text("baseline\n", encoding="utf-8")
    if agents_text is not None:
        (repo / "AGENTS.md").write_text(agents_text, encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "baseline")


def run_installer(source_repo: Path, target_repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER_PATH), str(source_repo), str(target_repo)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class DevelopmentSkillInstallerTests(unittest.TestCase):
    def test_installs_profile_preserves_agents_text_and_final_availability(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo, agents_text="# Project instructions\n\nKeep this line.\n")

            result = run_installer(ROOT, repo)

            self.assertEqual(0, result.returncode, result.stderr)
            info = json.loads(result.stdout)
            self.assertTrue(info["installed"])
            self.assertEqual("development", info["profile"])
            self.assertTrue(info["availability"]["available"])
            self.assertEqual(
                (repo / ".agents").resolve(),
                Path(info["availability"]["installation_root"]).resolve(),
            )
            self.assertEqual(
                [name for name, _ in installer.DEVELOPMENT_SKILL_SOURCES],
                info["skills"],
            )

            for _, relative in installer.DEVELOPMENT_SKILL_SOURCES:
                relative_under_skills = Path(relative).relative_to("skills")
                self.assertTrue(
                    (repo / ".agents" / "skills" / relative_under_skills / "SKILL.md").is_file(),
                    relative,
                )

            for name in installer.SHARED_SCRIPT_FILES:
                installed = repo / ".agents" / "scripts" / name
                self.assertEqual(
                    (ROOT / "scripts" / name).read_bytes(),
                    installed.read_bytes(),
                    name,
                )

            agents_text = (repo / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Project instructions", agents_text)
            self.assertIn("Keep this line.", agents_text)
            self.assertEqual(1, agents_text.count(installer.AGENTS_BEGIN))
            self.assertEqual(1, agents_text.count(installer.AGENTS_END))
            self.assertIn("project-local copy exists under `.agents/skills/`", agents_text)

            before = git(repo, "status", "--porcelain=v1")
            availability = subprocess.run(
                [
                    sys.executable,
                    str(repo / ".agents" / "scripts" / "run_evidence.py"),
                    "--repo",
                    str(repo),
                    "availability",
                ],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )
            after = git(repo, "status", "--porcelain=v1")
            self.assertEqual(0, availability.returncode, availability.stderr)
            self.assertTrue(json.loads(availability.stdout)["available"])
            self.assertEqual(before, after)

    def test_rerun_removes_stale_managed_files_and_preserves_unmanaged_installations(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo)

            first = run_installer(ROOT, repo)
            self.assertEqual(0, first.returncode, first.stderr)

            bounded = (
                repo
                / ".agents"
                / "skills"
                / "task-implementation-flow"
                / "bounded-task-implementer"
            )
            (bounded / "stale-file.txt").write_text("stale\n", encoding="utf-8")

            unmanaged_skill = repo / ".agents" / "skills" / "custom-local-skill"
            unmanaged_skill.mkdir(parents=True)
            (unmanaged_skill / "SKILL.md").write_text(
                "---\nname: custom-local-skill\ndescription: local\n---\nbody\n",
                encoding="utf-8",
            )
            unmanaged_script = repo / ".agents" / "scripts" / "custom_helper.py"
            unmanaged_script.write_text("VALUE = 1\n", encoding="utf-8")

            agents_before = (repo / "AGENTS.md").read_text(encoding="utf-8")
            second = run_installer(ROOT, repo)

            self.assertEqual(0, second.returncode, second.stderr)
            self.assertFalse((bounded / "stale-file.txt").exists())
            self.assertTrue((unmanaged_skill / "SKILL.md").is_file())
            self.assertEqual("VALUE = 1\n", unmanaged_script.read_text(encoding="utf-8"))
            agents_after = (repo / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(agents_before, agents_after)
            self.assertEqual(1, agents_after.count(installer.AGENTS_BEGIN))

    def test_missing_source_dependency_fails_before_target_installation(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            init_repo(target, agents_text="# Existing\n")

            result = run_installer(source, target)

            self.assertEqual(2, result.returncode)
            self.assertIn("missing development-profile inputs", result.stderr)
            self.assertFalse((target / ".agents").exists())
            self.assertEqual(
                "# Existing\n",
                (target / "AGENTS.md").read_text(encoding="utf-8"),
            )

    def test_malformed_managed_agents_block_fails_before_target_installation(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(
                repo,
                agents_text=(
                    "# Existing\n\n"
                    f"{installer.AGENTS_BEGIN}\n"
                    "incomplete managed block\n"
                ),
            )

            result = run_installer(ROOT, repo)

            self.assertEqual(2, result.returncode)
            self.assertIn("malformed development-install markers", result.stderr)
            self.assertFalse((repo / ".agents").exists())

    def test_repo_instructions_make_installer_maintenance_explicit(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for text in (agents, readme):
            self.assertIn("scripts/install_development_skills.py", text)
            self.assertIn("DEVELOPMENT_SKILL_SOURCES", text)
            self.assertIn("SHARED_SCRIPT_FILES", text)

        self.assertIn("same change", agents)
        self.assertIn("development profile", readme)


if __name__ == "__main__":
    unittest.main()
