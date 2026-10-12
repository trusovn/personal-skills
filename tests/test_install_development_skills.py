import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = ROOT / "scripts" / "install_development_skills.py"

SPEC = importlib.util.spec_from_file_location("install_development_skills", INSTALLER_PATH)
installer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(installer)


EXPECTED_DEVELOPMENT_SKILL_SOURCES = (
    ("project-direction", "skills/project-direction"),
    ("project-bootstrap", "skills/project-bootstrap"),
    ("ai-flow-foundation", "skills/ai-flow-foundation"),
    ("repo-foundation", "skills/repo-foundation"),
    ("architecture-guardrails", "skills/architecture-guardrails"),
    ("foundation-readiness-review", "skills/foundation-readiness-review"),
    ("project-delivery-plan", "skills/project-delivery-plan"),
    ("project-plan-verification", "skills/project-plan-verification"),
    ("task-brief-designer", "skills/task-implementation-flow/task-brief-designer"),
    ("task-preflight", "skills/task-implementation-flow/task-preflight"),
    (
        "task-verification-designer",
        "skills/task-implementation-flow/task-verification-designer",
    ),
    (
        "bounded-task-implementer",
        "skills/task-implementation-flow/bounded-task-implementer",
    ),
    (
        "task-maintainability-review",
        "skills/task-implementation-flow/task-maintainability-review",
    ),
    (
        "task-contract-registry-updater",
        "skills/task-implementation-flow/task-contract-registry-updater",
    ),
    (
        "task-acceptance-review",
        "skills/task-implementation-flow/task-acceptance-review",
    ),
    (
        "task-review-discovery",
        "skills/task-implementation-flow/task-review-discovery",
    ),
    ("senior-code-review", "skills/senior-code-review"),
    ("ollama-delegate", "skills/ollama-delegate"),
    ("testing-discipline", "skills/testing-discipline"),
    ("session-handoff", "skills/session-handoff"),
)


PREPARATION_PROFILE_SKILLS = (
    "task-brief-designer",
    "task-verification-designer",
    "task-preflight",
    "bounded-task-implementer",
)

PREPARATION_SKILL_SOURCES = tuple(
    source
    for source in EXPECTED_DEVELOPMENT_SKILL_SOURCES
    if source[0] in PREPARATION_PROFILE_SKILLS
)

CROSS_STAGE_GUIDE_PATHS = {
    "root-readme": "README.md",
    "profile-guide": "skills/README.md",
    "task-flow-readme": "skills/task-implementation-flow/README.md",
}

REQUIRED_PREPARATION_ROUTE_WORDING = {
    "root-readme": (
        "required for a supplied executable task package",
        "required ready preflight for that package",
        "executable task package always follows verification design and ready preflight",
        "**unpackaged conversational**",
        "scenario ID to current evidence or an explicit blocked/unchecked reason and",
    ),
    "profile-guide": (
        "(required for an executable task package)",
        "(required ready preflight for that package)",
        "Required derived `<task-package>/verification.md` before packaged implementation.",
        "Compact canonical `<task-package>/preflight.md` bound to brief/scope/verification revision",
    ),
    "task-flow-readme": (
        "required task-verification-designer for an executable task package",
        "required before packaged implementation",
        "required ready preflight before implementation",
        "Every executable package requires derived verification and compact canonical readiness",
        "requires no digest ledger or machine schema",
    ),
}

FORBIDDEN_OPTIONAL_PREPARATION_WORDING = {
    "root-readme": (
        "when task-local verification semantics are non-obvious",
        "when readiness needs an independent check",
        "For small, unambiguous work, go directly to `bounded-task-implementer`",
    ),
    "profile-guide": (
        "(when verification is non-obvious)",
        "(when a separate readiness check adds value)",
    ),
    "task-flow-readme": (
        "optional task-verification-designer",
        "only when separate verification design is used",
        "only when a durable preflight artifact is needed",
        "A routine guided task can perform the same compact self-check inside the implementer.",
    ),
}


def assert_preparation_route_wording(case: unittest.TestCase, doc: str, text: str) -> None:
    path = CROSS_STAGE_GUIDE_PATHS[doc]
    for phrase in REQUIRED_PREPARATION_ROUTE_WORDING[doc]:
        case.assertIn(phrase, text, f"{path}: missing packaged-route wording")
    for phrase in FORBIDDEN_OPTIONAL_PREPARATION_WORDING[doc]:
        case.assertNotIn(phrase, text, f"{path}: stale optional-route wording")


VERIFICATION_DESIGN_ROUTE_MARKERS = (
    "task-verification-designer",
    "verification design",
    "verification.md",
)

TASK_ROUTE_BRIEF_MARKERS = (
    "task brief",
    "task-brief",
    "brief.md",
    "request or brief",
)


def extract_fenced_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if current is None:
            if line.lstrip().startswith("```"):
                current = []
        elif line.lstrip().startswith("```"):
            blocks.append("\n".join(current))
            current = None
        else:
            current.append(line)
    return blocks


def collect_package_files(root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    if not root.is_dir():
        return files
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in ("__pycache__", "node_modules") for part in relative.parts):
            continue
        if path.name == ".DS_Store" or path.name.endswith(".pyc"):
            continue
        files[relative.as_posix()] = path.read_bytes()
    return files


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def init_repo(
    repo: Path,
    *,
    ignore_agents: bool = True,
    agents_text: str | None = None,
    commit: bool = True,
) -> None:
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "tests@example.com")
    git(repo, "config", "user.name", "Development Installer Tests")
    if ignore_agents:
        (repo / ".gitignore").write_text(".agents/\n", encoding="utf-8")
    (repo / "app.txt").write_text("baseline\n", encoding="utf-8")
    if agents_text is not None:
        (repo / "AGENTS.md").write_text(agents_text, encoding="utf-8")
    if not commit:
        return
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "baseline")


def run_installer(
    target_repo: Path, *, cwd: Path = ROOT, extra_args: tuple[str, ...] = ()
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER_PATH), str(target_repo), *extra_args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


class DevelopmentSkillInstallerTests(unittest.TestCase):
    def test_profile_contains_repo_stage_and_bounded_delivery_skills(self):
        self.assertEqual(
            EXPECTED_DEVELOPMENT_SKILL_SOURCES,
            installer.DEVELOPMENT_SKILL_SOURCES,
        )

    def test_profile_guide_covers_every_installed_skill_and_usage_contract(self):
        guide = (ROOT / installer.PROFILE_SKILLS_README).read_text(encoding="utf-8")

        self.assertIn("## Recommended flow", guide)
        self.assertIn("## Skill reference", guide)
        for name, _ in EXPECTED_DEVELOPMENT_SKILL_SOURCES:
            self.assertIn(f"| `{name}` |", guide)
        for name in (
            "ask-user-questions",
            "idea-challenger",
            "idea-investigator",
            "idea-brief",
        ):
            self.assertNotIn(f"| `{name}` |", guide)
        for heading in ("Skill", "What it does", "Requires", "Produces"):
            self.assertIn(heading, guide)

    def test_ai_flow_routing_distinguishes_product_model_use_from_coding_agents(self):
        bootstrap = (ROOT / "skills/project-bootstrap/SKILL.md").read_text(encoding="utf-8")
        ai_flow = (ROOT / "skills/ai-flow-foundation/SKILL.md").read_text(encoding="utf-8")
        foundation_plan = (
            ROOT / "skills/project-bootstrap/templates/foundation-plan.md"
        ).read_text(encoding="utf-8")
        guide = (ROOT / installer.PROFILE_SKILLS_README).read_text(encoding="utf-8")

        self.assertIn("system being built calls an AI/LLM/model", bootstrap)
        self.assertIn("coding-agent use", bootstrap)
        self.assertIn("AI/model behavior **inside the system being built**", ai_flow)
        self.assertIn("coding agents will develop or maintain", ai_flow)
        self.assertIn("Product/runtime calls AI/LLM/model", foundation_plan)
        self.assertIn("coding-agent maintenance alone does not trigger it", guide)

    def assert_projected_from_source(self, repo: Path, relative: str) -> None:
        source = collect_package_files(ROOT / relative)
        installed = collect_package_files(
            repo / ".agents" / "skills" / Path(relative).relative_to("skills")
        )
        self.assertEqual(
            sorted(source), sorted(installed), f"managed file set differs for {relative}"
        )
        for name, content in source.items():
            self.assertEqual(
                content, installed[name], f"managed bytes differ for {relative}/{name}"
            )

    def installed_identity(self, repo: Path) -> dict:
        result = subprocess.run(
            [
                sys.executable,
                str(repo / ".agents" / "scripts" / "workflow_version.py"),
                "bounded-task-implementer",
            ],
            cwd=repo,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_cross_stage_guides_require_packaged_preparation_route(self):
        for doc, path in CROSS_STAGE_GUIDE_PATHS.items():
            assert_preparation_route_wording(
                self, doc, (ROOT / path).read_text(encoding="utf-8")
            )

    def test_every_documented_task_route_carries_packaged_preparation(self):
        for doc, path in CROSS_STAGE_GUIDE_PATHS.items():
            text = (ROOT / path).read_text(encoding="utf-8")
            routes = 0
            for block in extract_fenced_blocks(text):
                if not any(marker in block for marker in TASK_ROUTE_BRIEF_MARKERS):
                    continue
                routes += 1
                self.assertTrue(
                    any(marker in block for marker in VERIFICATION_DESIGN_ROUTE_MARKERS),
                    f"{path}: documented task route omits separate verification design",
                )
                self.assertTrue(
                    "preflight" in block,
                    f"{path}: documented task route omits ready preflight",
                )
            self.assertGreater(routes, 0, f"{path}: no documented task route found")

    def test_installs_profile_preserves_agents_text_and_final_availability(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo, agents_text="# Project instructions\n\nKeep this line.\n")

            result = run_installer(repo)

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

            for _, relative in PREPARATION_SKILL_SOURCES:
                self.assert_projected_from_source(repo, relative)

            self.assertEqual(b"baseline\n", (repo / "app.txt").read_bytes())

            for name in installer.SHARED_SCRIPT_FILES:
                installed = repo / ".agents" / "scripts" / name
                self.assertEqual(
                    (ROOT / "scripts" / name).read_bytes(),
                    installed.read_bytes(),
                    name,
                )

            installed_guide = repo / ".agents" / "skills" / "README.md"
            self.assertEqual(
                (ROOT / installer.PROFILE_SKILLS_README).read_bytes(),
                installed_guide.read_bytes(),
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

    def test_installs_profile_into_unborn_repository_without_creating_a_commit(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(
                repo,
                agents_text="# Project instructions\n\nKeep this line.\n",
                commit=False,
            )

            head_ref = git(repo, "symbolic-ref", "HEAD").strip()
            objects_before = sorted(
                path.name for path in (repo / ".git" / "objects").iterdir()
            )
            show_ref = subprocess.run(
                ["git", "-C", str(repo), "show-ref"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual("", show_ref.stdout)

            result = run_installer(repo)

            self.assertEqual(0, result.returncode, result.stderr)
            info = json.loads(result.stdout)
            self.assertTrue(info["installed"])
            self.assertTrue(info["availability"]["available"])

            # HEAD stays genuinely unborn: same unborn branch, no commit, and
            # no fabricated Git object.
            self.assertEqual(head_ref, git(repo, "symbolic-ref", "HEAD").strip())
            show_ref_after = subprocess.run(
                ["git", "-C", str(repo), "show-ref"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual("", show_ref_after.stdout)
            self.assertEqual(
                objects_before,
                sorted(path.name for path in (repo / ".git" / "objects").iterdir()),
            )

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
            self.assertEqual(0, availability.returncode, availability.stderr)
            self.assertTrue(json.loads(availability.stdout)["available"])

            unborn_identity = self.installed_identity(repo)
            self.assertIsNone(unborn_identity["repository_commit"])
            self.assertTrue(unborn_identity["fingerprint"].startswith("sha256:"))

            # The first and a later unrelated application commit replace the
            # unborn identity without changing the installed fingerprint.
            git(repo, "add", ".")
            git(repo, "commit", "-qm", "first unrelated application commit")
            first_commit = git(repo, "rev-parse", "HEAD").strip()
            first_identity = self.installed_identity(repo)
            self.assertEqual(first_commit, first_identity["repository_commit"])

            (repo / "app.txt").write_text("changed later\n", encoding="utf-8")
            git(repo, "add", "app.txt")
            git(repo, "commit", "-qm", "later unrelated application commit")
            later_commit = git(repo, "rev-parse", "HEAD").strip()
            later_identity = self.installed_identity(repo)
            self.assertEqual(later_commit, later_identity["repository_commit"])
            self.assertNotEqual(first_commit, later_commit)

            self.assertEqual(
                unborn_identity["fingerprint"], first_identity["fingerprint"]
            )
            self.assertEqual(
                unborn_identity["fingerprint"], later_identity["fingerprint"]
            )

            committed_availability = subprocess.run(
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
            self.assertEqual(
                0, committed_availability.returncode, committed_availability.stderr
            )
            self.assertTrue(json.loads(committed_availability.stdout)["available"])

    def test_invalid_git_target_fails_without_installing(self):
        with tempfile.TemporaryDirectory() as tempdir:
            non_repo = Path(tempdir)
            (non_repo / "app.txt").write_text("not a repository\n", encoding="utf-8")

            result = run_installer(non_repo)

            self.assertEqual(2, result.returncode)
            self.assertIn("target repository is not usable", result.stderr)
            self.assertFalse((non_repo / ".agents").exists())

    def test_rerun_removes_stale_managed_files_and_preserves_unmanaged_installations(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo, agents_text="# Project instructions\n\nKeep this line.\n")

            first = run_installer(repo)
            self.assertEqual(0, first.returncode, first.stderr)

            bounded = (
                repo
                / ".agents"
                / "skills"
                / "task-implementation-flow"
                / "bounded-task-implementer"
            )
            (bounded / "stale-file.txt").write_text("stale\n", encoding="utf-8")
            installed_guide = repo / ".agents" / "skills" / "README.md"
            installed_guide.write_text("stale guide\n", encoding="utf-8")

            unmanaged_skill = repo / ".agents" / "skills" / "custom-local-skill"
            unmanaged_skill.mkdir(parents=True)
            (unmanaged_skill / "SKILL.md").write_text(
                "---\nname: custom-local-skill\ndescription: local\n---\nbody\n",
                encoding="utf-8",
            )
            (unmanaged_skill / "references").mkdir()
            (unmanaged_skill / "references" / "note.md").write_text(
                "note\n", encoding="utf-8"
            )
            unmanaged_files = collect_package_files(unmanaged_skill)
            unmanaged_script = repo / ".agents" / "scripts" / "custom_helper.py"
            unmanaged_script.write_text("VALUE = 1\n", encoding="utf-8")

            agents_before = (repo / "AGENTS.md").read_text(encoding="utf-8")
            second = run_installer(repo)

            self.assertEqual(0, second.returncode, second.stderr)
            self.assertFalse((bounded / "stale-file.txt").exists())
            self.assertEqual(
                (ROOT / installer.PROFILE_SKILLS_README).read_bytes(),
                installed_guide.read_bytes(),
            )
            self.assertEqual(unmanaged_files, collect_package_files(unmanaged_skill))
            self.assertEqual("VALUE = 1\n", unmanaged_script.read_text(encoding="utf-8"))
            agents_after = (repo / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(agents_before, agents_after)
            self.assertIn("# Project instructions", agents_after)
            self.assertIn("Keep this line.", agents_after)
            self.assertEqual(1, agents_after.count(installer.AGENTS_BEGIN))
            self.assertEqual(1, agents_after.count(installer.AGENTS_END))
            for _, relative in PREPARATION_SKILL_SOURCES:
                self.assert_projected_from_source(repo, relative)

    def test_install_projects_task_review_discovery_and_preserves_unrelated_target_bytes(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo, agents_text="# Project instructions\n\nKeep this line.\n")

            result = run_installer(repo)
            self.assertEqual(0, result.returncode, result.stderr)

            relative = "skills/task-implementation-flow/task-review-discovery"
            installed_skill = (
                repo
                / ".agents"
                / "skills"
                / "task-implementation-flow"
                / "task-review-discovery"
            )
            self.assertTrue((installed_skill / "SKILL.md").is_file())
            self.assertTrue(
                (installed_skill / "references" / "discovery-report-template.md").is_file()
            )
            self.assertTrue((installed_skill / "evals" / "evals.json").is_file())
            self.assertTrue(
                (installed_skill / "evals" / "files" / "setup_fixture.py").is_file()
            )
            self.assert_projected_from_source(repo, relative)

            unrelated = repo / "notes" / "unrelated.txt"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("user bytes\n", encoding="utf-8")
            stale = installed_skill / "references" / "stale-managed.md"
            stale.write_text("stale\n", encoding="utf-8")

            rerun = run_installer(repo)

            self.assertEqual(0, rerun.returncode, rerun.stderr)
            self.assertFalse(stale.exists())
            self.assertEqual(b"user bytes\n", unrelated.read_bytes())
            self.assert_projected_from_source(repo, relative)
            agents_text = (repo / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Keep this line.", agents_text)
            self.assertEqual(1, agents_text.count(installer.AGENTS_BEGIN))
            self.assertEqual(1, agents_text.count(installer.AGENTS_END))

    def test_source_repository_is_inferred_from_installer_when_cwd_differs(self):
        with (
            tempfile.TemporaryDirectory() as target_dir,
            tempfile.TemporaryDirectory() as cwd_dir,
        ):
            target = Path(target_dir)
            init_repo(target)

            result = run_installer(target, cwd=Path(cwd_dir))

            self.assertEqual(0, result.returncode, result.stderr)
            info = json.loads(result.stdout)
            self.assertEqual(str(ROOT), info["source_repo"])
            self.assertEqual(str(target.resolve()), info["target_repo"])

    def test_cli_rejects_the_removed_source_repository_argument(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir)
            init_repo(target)

            result = run_installer(target, extra_args=(str(target),))

            self.assertEqual(2, result.returncode)
            self.assertIn("unrecognized arguments", result.stderr)
            self.assertFalse((target / ".agents").exists())

    def test_missing_source_dependency_fails_before_target_installation(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            init_repo(target, agents_text="# Existing\n")

            with mock.patch.object(installer, "SOURCE_REPO", source):
                with self.assertRaisesRegex(
                    installer.InstallError, "missing development-profile inputs"
                ):
                    installer.install(target)

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

            result = run_installer(repo)

            self.assertEqual(2, result.returncode)
            self.assertIn("malformed development-install markers", result.stderr)
            self.assertFalse((repo / ".agents").exists())

    def test_repo_instructions_make_installer_maintenance_explicit(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for text in (agents, readme):
            self.assertIn("scripts/install_development_skills.py", text)
            self.assertIn("DEVELOPMENT_SKILL_SOURCES", text)
            self.assertIn("PROFILE_SKILLS_README", text)
            self.assertIn("SHARED_SCRIPT_FILES", text)

        self.assertIn("same change", agents)
        self.assertIn("development profile", readme)


    def test_install_projects_acceptance_review_package_and_preserves_unrelated_bytes(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo, agents_text="# Project instructions\n\nKeep this line.\n")

            result = run_installer(repo)
            self.assertEqual(0, result.returncode, result.stderr)

            relative = "skills/task-implementation-flow/task-acceptance-review"
            installed_skill = (
                repo
                / ".agents"
                / "skills"
                / "task-implementation-flow"
                / "task-acceptance-review"
            )
            for required in (
                "SKILL.md",
                "references/acceptance-report-template.md",
                "references/tests-only-reproducer.md",
                "evals/evals.json",
                "evals/files/setup_fixture.py",
            ):
                self.assertTrue((installed_skill / required).is_file(), required)
            self.assert_projected_from_source(repo, relative)

            unrelated = repo / "notes" / "unrelated.txt"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("user bytes\n", encoding="utf-8")
            stale = installed_skill / "references" / "stale-managed.md"
            stale.write_text("stale\n", encoding="utf-8")

            rerun = run_installer(repo)

            self.assertEqual(0, rerun.returncode, rerun.stderr)
            self.assertFalse(stale.exists())
            self.assertEqual(b"user bytes\n", unrelated.read_bytes())
            self.assert_projected_from_source(repo, relative)
            self.assertEqual(
                (ROOT / installer.PROFILE_SKILLS_README).read_bytes(),
                (repo / ".agents" / "skills" / "README.md").read_bytes(),
            )
            agents_text = (repo / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Keep this line.", agents_text)
            self.assertEqual(1, agents_text.count(installer.AGENTS_BEGIN))
            self.assertEqual(1, agents_text.count(installer.AGENTS_END))


    def test_install_projects_maintainability_and_registry_updater_families_and_guide_routes(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo, agents_text="# Project instructions\n\nKeep this line.\n")

            result = run_installer(repo)
            self.assertEqual(0, result.returncode, result.stderr)

            maintainability = "skills/task-implementation-flow/task-maintainability-review"
            registry_updater = (
                "skills/task-implementation-flow/task-contract-registry-updater"
            )
            installed_maintainability = (
                repo
                / ".agents"
                / "skills"
                / "task-implementation-flow"
                / "task-maintainability-review"
            )
            for required in (
                "SKILL.md",
                "evals/evals.json",
                "evals/files/setup_fixture.py",
            ):
                self.assertTrue(
                    (installed_maintainability / required).is_file(), required
                )
            self.assertTrue(
                (
                    repo
                    / ".agents"
                    / "skills"
                    / "task-implementation-flow"
                    / "task-contract-registry-updater"
                    / "SKILL.md"
                ).is_file()
            )
            self.assert_projected_from_source(repo, maintainability)
            self.assert_projected_from_source(repo, registry_updater)

            # Installed setup must run with no repository-only test helpers.
            work = repo / "fixture-work"
            for scenario, variant, second, repeatable in (
                ("test-assets", "defects", "(100, 'total 102.00')", False),
                ("test-assets-control", "control", "(200, 'total 204.00')", True),
            ):
                setup = subprocess.run(
                    [sys.executable, str(installed_maintainability / "evals/files/setup_fixture.py"),
                     scenario],
                    cwd=repo, env=os.environ | {"EVAL_WORK_ROOT": str(work), "PYTHONPATH": ""},
                    capture_output=True, text=True,
                )
                self.assertEqual(0, setup.returncode, setup.stderr)
                target = work / f"maintainability-tests-{variant}"
                probe = subprocess.run(
                    [sys.executable, "-c",
                     'from tests import scenarios, test_receipt_contract, test_transport\n'
                     'scenarios.STANDARD.update(subtotal=200, expected="total 204.00")\n'
                     'print(test_receipt_contract.observe())\n'
                     'print(test_transport.observe())\n'],
                    cwd=repo, env=os.environ | {"PYTHONPATH": str(target)},
                    capture_output=True, text=True,
                )
                self.assertEqual(0, probe.returncode, probe.stderr)
                self.assertEqual(["(200, 'total 204.00')", second], probe.stdout.splitlines())
                repeated = subprocess.run(
                    [sys.executable, "-c",
                     'import unittest\n'
                     'from tests.test_receipt_contract import ReceiptContractTest\n'
                     'for occurrence in range(2):\n'
                     '    result = unittest.TestResult()\n'
                     '    ReceiptContractTest("test_receipt").run(result)\n'
                     '    print(result.wasSuccessful())\n'
                     '    for _, error in result.errors:\n'
                     '        print(error)\n'],
                    cwd=repo, env=os.environ | {"PYTHONPATH": str(target)},
                    capture_output=True, text=True,
                )
                self.assertEqual(0, repeated.returncode, repeated.stderr)
                self.assertEqual(["True", str(repeatable)], repeated.stdout.splitlines()[:2])
                self.assertEqual(not repeatable, "KeyError" in repeated.stdout)

            installed_guide = repo / ".agents" / "skills" / "README.md"
            self.assertEqual(
                (ROOT / installer.PROFILE_SKILLS_README).read_bytes(),
                installed_guide.read_bytes(),
            )
            guide_text = " ".join(installed_guide.read_text(encoding="utf-8").split())
            for phrase in (
                "first outstanding applicable stage",
                "complete ordered remainder",
                "fresh maintainability review when applicable",
                "the contract-registry updater when applicable",
                "then fresh discovery evidence and the separate fresh acceptance decision",
                "implementation corrections, including tests-only corrections, re-enter the stages they affected",
            ):
                self.assertIn(phrase, guide_text)

            stale = installed_maintainability / "evals" / "files" / "stale-managed.py"
            stale.write_text("stale\n", encoding="utf-8")
            unmanaged_agents_file = repo / ".agents" / "unmanaged-note.md"
            unmanaged_agents_file.write_text("user bytes\n", encoding="utf-8")
            unrelated = repo / "notes" / "unrelated.txt"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("user bytes\n", encoding="utf-8")

            rerun = run_installer(repo)

            self.assertEqual(0, rerun.returncode, rerun.stderr)
            self.assertFalse(stale.exists())
            self.assertEqual(b"user bytes\n", unmanaged_agents_file.read_bytes())
            self.assertEqual(b"user bytes\n", unrelated.read_bytes())
            self.assert_projected_from_source(repo, maintainability)
            self.assert_projected_from_source(repo, registry_updater)
            agents_text = (repo / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Keep this line.", agents_text)
            self.assertEqual(1, agents_text.count(installer.AGENTS_BEGIN))
            self.assertEqual(1, agents_text.count(installer.AGENTS_END))


if __name__ == "__main__":
    unittest.main()
