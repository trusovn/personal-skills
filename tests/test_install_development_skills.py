import importlib.util
import json
import os
import shutil
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


EXPECTED_MEASUREMENT_FILES = (
    "measure_maintainability.py", "maintainability.py", "maintainability_env.py",
    "maintainability-default.toml", "maintainability-ruff-default.toml",
    "maintainability-requirements.txt",
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


def seed_measurement_target(repo: Path) -> dict[Path, bytes]:
    """Existing target-owned policy/evidence and real dirty Git input."""
    source = repo / "app.py"
    source.write_text("staged bytes\n")
    git(repo, "add", "app.py")
    source.write_text("unstaged bytes\n")
    names = (
        "untracked.py", ".quality/maintainability.toml", ".quality/ruff.toml",
        ".quality/requirements.txt", ".quality/envs/native/bin/python",
        ".quality/reports/before.json", ".quality/reports/before.txt",
        ".agents/scripts/existing_helper.py", ".agents/skills/existing/SKILL.md",
    )
    for name in names:
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"---\nname: existing\ndescription: User-owned skill.\n---\nKeep.\n" if name.endswith("SKILL.md") else b"target-owned sentinel\n")
    paths = [source, repo / ".git/index", *(repo / name for name in names)]
    return {path: path.read_bytes() for path in paths}


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


def run_check(
    target_repo: Path, *, cwd: Path = ROOT
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER_PATH), "--check", str(target_repo)],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def installed_identity(repo: Path) -> dict:
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


def expected_managed_paths() -> set[str]:
    """Independently enumerate every managed path the check must compare."""
    paths: set[str] = set()
    for _, relative in installer.DEVELOPMENT_SKILL_SOURCES:
        for name in collect_package_files(ROOT / relative):
            paths.add(f".agents/{relative}/{name}")
    for name in installer.SHARED_SCRIPT_FILES:
        paths.add(f".agents/scripts/{name}")
    paths.add(".agents/skills/README.md")
    paths.add("AGENTS.md")
    return paths


def source_projection_snapshot() -> dict[str, bytes]:
    """Record the canonical source bytes the check compares against."""
    snapshot: dict[str, bytes] = {}
    for _, relative in installer.DEVELOPMENT_SKILL_SOURCES:
        for name, content in collect_package_files(ROOT / relative).items():
            snapshot[f"{relative}/{name}"] = content
    for name in installer.SHARED_SCRIPT_FILES:
        snapshot[f"scripts/{name}"] = (ROOT / "scripts" / name).read_bytes()
    snapshot[installer.PROFILE_SKILLS_README] = (
        ROOT / installer.PROFILE_SKILLS_README
    ).read_bytes()
    return snapshot


def snapshot_tree(root: Path) -> dict[str, object]:
    """Record path existence, type, and bytes for every entry under ``root``.

    Unreadable files are recorded with their permission mode so a read-only
    oracle can still prove that checking leaves them untouched.
    """
    entries: dict[str, object] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries[relative] = ("symlink", os.readlink(path))
        elif path.is_dir():
            entries[relative] = ("dir",)
        elif path.is_file():
            try:
                entries[relative] = ("file", path.read_bytes())
            except PermissionError:
                entries[relative] = ("file", "unreadable", path.stat().st_mode)
        else:
            entries[relative] = ("other",)
    return entries


CHECK_GUIDE_PATHS = ("README.md", "skills/README.md")

CHECK_GUIDE_REQUIRED_PHRASES = (
    "--check",
    "read-only",
    "exit 0",
    "exit 1",
    "exit 2",
    "marked `AGENTS.md` block",
    "changed, missing, and unexpected managed paths",
    "unselected skills",
    "not the caller's working directory",
    "retains no versions",
    "refresh deliberately by rerunning the installer",
    "follows directory symlinks",
    "Acyclic directory aliases",
    "one of its own ancestors",
)


def build_relocated_source_distribution(base: Path) -> tuple[Path, Path]:
    """Copy a complete disposable source distribution with a relocated CLI."""
    source = base / "source"
    source.mkdir()
    for _, relative in installer.DEVELOPMENT_SKILL_SOURCES:
        shutil.copytree(
            ROOT / relative,
            source / relative,
            ignore=shutil.ignore_patterns(*installer.TRANSIENT_PATTERNS),
        )
    scripts_dir = source / "scripts"
    scripts_dir.mkdir()
    for name in (*installer.SHARED_SCRIPT_FILES, INSTALLER_PATH.name):
        shutil.copy2(ROOT / "scripts" / name, scripts_dir / name)
    shutil.copy2(
        ROOT / installer.PROFILE_SKILLS_README,
        source / installer.PROFILE_SKILLS_README,
    )
    return source, scripts_dir / INSTALLER_PATH.name


class DevelopmentSkillInstallerTests(unittest.TestCase):
    def test_profile_contains_repo_stage_and_bounded_delivery_skills(self):
        for name in EXPECTED_MEASUREMENT_FILES:
            self.assertIn(name, installer.SHARED_SCRIPT_FILES)
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

            unborn_identity = installed_identity(repo)
            self.assertIsNone(unborn_identity["repository_commit"])
            self.assertTrue(unborn_identity["fingerprint"].startswith("sha256:"))

            # The first and a later unrelated application commit replace the
            # unborn identity without changing the installed fingerprint.
            git(repo, "add", ".")
            git(repo, "commit", "-qm", "first unrelated application commit")
            first_commit = git(repo, "rev-parse", "HEAD").strip()
            first_identity = installed_identity(repo)
            self.assertEqual(first_commit, first_identity["repository_commit"])

            (repo / "app.txt").write_text("changed later\n", encoding="utf-8")
            git(repo, "add", "app.txt")
            git(repo, "commit", "-qm", "later unrelated application commit")
            later_commit = git(repo, "rev-parse", "HEAD").strip()
            later_identity = installed_identity(repo)
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


class DevelopmentProfileCheckTests(unittest.TestCase):
    maxDiff = None

    DRIFT_FAMILIES = (
        ("selected skill SKILL.md", ".agents/skills/project-direction/SKILL.md"),
        (
            "selected skill reference",
            ".agents/skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md",
        ),
        (
            "selected skill eval/setup",
            ".agents/skills/task-implementation-flow/bounded-task-implementer/evals/evals.json",
        ),
        ("profile guide", ".agents/skills/README.md"),
        ("shared script", ".agents/scripts/run_evidence.py"),
        ("shared config", ".agents/scripts/ollama-models.json"),
        ("shared schema", ".agents/scripts/runtime-context.schema.v1.json"),
    )

    def install_profile(self, repo: Path, *, commit: bool = True) -> None:
        repo.mkdir(parents=True, exist_ok=True)
        init_repo(repo, agents_text="# Project instructions\n", commit=commit)
        result = run_installer(repo)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_check_reports_match_after_fresh_install_in_committed_and_unborn_repos(self):
        for commit in (True, False):
            with self.subTest(commit=commit):
                with tempfile.TemporaryDirectory() as tempdir:
                    repo = Path(tempdir)
                    self.install_profile(repo, commit=commit)

                    result = run_check(repo)

                    self.assertEqual(0, result.returncode, result.stderr)
                    info = json.loads(result.stdout)
                    self.assertTrue(info["checked"])
                    self.assertTrue(info["match"])
                    self.assertEqual([], info["differences"])
                    self.assertEqual(
                        len(expected_managed_paths()), info["compared_paths"]
                    )

    def test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes(self):
        line_endings = {
            "LF": b"\n",
            "CRLF": b"\r\n",
            "mixed": b"\n\r\n\r",
            "CR": b"\r",
        }
        for commit in (False, True):
            for label, ending in line_endings.items():
                with self.subTest(commit=commit, line_endings=label):
                    with tempfile.TemporaryDirectory() as tempdir:
                        repo = Path(tempdir)
                        init_repo(repo, commit=commit)
                        agents = repo / "AGENTS.md"
                        original = b"# Instructions" + ending + b"Keep spaces.  " + ending * 2
                        agents.write_bytes(original)
                        first = run_installer(repo)
                        self.assertEqual(0, first.returncode, first.stderr)
                        self.assertTrue(agents.read_bytes().startswith(original))

                        prefix = b"# Instructions" + ending + b"\t " + ending * 2
                        suffix = ending + b"\tSuffix.  " + ending * 2
                        begin = installer.AGENTS_BEGIN.encode()
                        end = installer.AGENTS_END.encode()
                        agents.write_bytes(
                            prefix + installer.AGENTS_BLOCK.rstrip().encode() + suffix
                        )
                        before = snapshot_tree(repo)
                        checked = run_check(repo)
                        self.assertEqual(0, checked.returncode, checked.stderr)
                        self.assertEqual(before, snapshot_tree(repo))
                        refresh = run_installer(repo)
                        self.assertEqual(0, refresh.returncode, refresh.stderr)
                        actual = agents.read_bytes()
                        self.assertEqual(1, actual.count(begin))
                        self.assertEqual(1, actual.count(end))
                        self.assertEqual(prefix, actual[:actual.index(begin)])
                        self.assertEqual(suffix, actual[actual.index(end) + len(end):])
                        self.assertEqual(
                            installer.AGENTS_BLOCK.rstrip().encode(),
                            actual[actual.index(begin):actual.index(end) + len(end)],
                        )
                        checked = run_check(repo)
                        self.assertEqual(0, checked.returncode, checked.stderr)

    def test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family(
        self,
    ):
        for commit in (True, False):
            with self.subTest(commit=commit):
                with tempfile.TemporaryDirectory() as tempdir:
                    repo = Path(tempdir)
                    original_agents = (
                        "# Project instructions\n"
                        "\n"
                        "Keep this line.   \n"
                        "\n"
                        "Prefix note:\n"
                        "    keep this aligned detail.  \n"
                        "\n"
                        "\n"
                    )
                    init_repo(repo, agents_text=original_agents, commit=commit)
                    head_ref = git(repo, "symbolic-ref", "HEAD").strip()
                    committed_head = (
                        git(repo, "rev-parse", "HEAD").strip() if commit else None
                    )

                    def assert_repository_identity_stable() -> None:
                        show_ref = subprocess.run(
                            ["git", "-C", str(repo), "show-ref"],
                            capture_output=True,
                            text=True,
                            check=False,
                        )
                        if commit:
                            self.assertEqual(0, show_ref.returncode)
                            self.assertEqual(
                                committed_head,
                                git(repo, "rev-parse", "HEAD").strip(),
                            )
                        else:
                            # The unborn target keeps its unborn branch state:
                            # no commit identity is fabricated anywhere in the
                            # journey.
                            self.assertEqual("", show_ref.stdout)
                            self.assertEqual(
                                head_ref, git(repo, "symbolic-ref", "HEAD").strip()
                            )

                    assert_repository_identity_stable()

                    preserved = seed_measurement_target(repo)
                    staged = git(repo, "show", ":app.py")

                    # First install, then a matching fresh check.
                    first = run_installer(repo)
                    self.assertEqual(0, first.returncode, first.stderr)
                    self.assertEqual(preserved, {p: p.read_bytes() for p in preserved})
                    self.assertEqual(staged, git(repo, "show", ":app.py"))
                    fresh = run_check(repo)
                    self.assertEqual(0, fresh.returncode, fresh.stderr)
                    fresh_info = json.loads(fresh.stdout)
                    self.assertTrue(fresh_info["match"])
                    self.assertEqual([], fresh_info["differences"])
                    self.assertEqual(
                        len(expected_managed_paths()), fresh_info["compared_paths"]
                    )

                    # Unmanaged state that must survive the whole journey.
                    unmanaged_skill = (
                        repo / ".agents" / "skills" / "custom-local-skill"
                    )
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
                    unrelated = repo / "notes" / "unrelated.txt"
                    unrelated.parent.mkdir(parents=True)
                    unrelated.write_text("user bytes\n", encoding="utf-8")

                    # Record outside-block bytes around the first insertion.
                    # First insertion must retain the original instruction
                    # bytes, including terminal trailing whitespace. The
                    # unrelated project edit below additionally places
                    # whitespace immediately at both marker boundaries: a
                    # tab-space line directly before the begin marker and an
                    # indented first suffix line ending in trailing spaces
                    # and blank lines.
                    agents_path = repo / "AGENTS.md"
                    rendered = agents_path.read_bytes().decode("utf-8")
                    self.assertEqual(1, rendered.count(installer.AGENTS_BEGIN))
                    self.assertEqual(1, rendered.count(installer.AGENTS_END))
                    self.assertTrue(rendered.startswith(original_agents))
                    agents_path.write_text(
                        rendered.replace(
                            installer.AGENTS_BEGIN, "\t \n" + installer.AGENTS_BEGIN
                        )
                        + "\n\tAfter-block project note:\n"
                        "    indented suffix survives.  \n"
                        "\n\n",
                        encoding="utf-8",
                    )
                    with_block = agents_path.read_bytes().decode("utf-8")
                    begin_at = with_block.index(installer.AGENTS_BEGIN)
                    end_at = with_block.index(installer.AGENTS_END) + len(
                        installer.AGENTS_END
                    )
                    outside_prefix = with_block[:begin_at]
                    outside_suffix = with_block[end_at:]
                    self.assertIn("Keep this line.   ", outside_prefix)
                    self.assertIn("\n    keep this aligned detail.", outside_prefix)
                    self.assertTrue(outside_prefix.endswith("\t \n"))
                    self.assertIn("\n\tAfter-block project note:", outside_suffix)
                    self.assertIn("\n    indented suffix survives.", outside_suffix)
                    self.assertTrue(outside_suffix.endswith("  \n\n\n"))

                    # Deliberate managed drift across representative families:
                    # changed, missing, an owned extra, and a changed but still
                    # valid marked block.
                    for relative in (
                        ".agents/skills/project-direction/SKILL.md",
                        ".agents/skills/README.md",
                        ".agents/scripts/run_evidence.py",
                        ".agents/scripts/ollama-models.json",
                        ".agents/scripts/runtime-context.schema.v1.json",
                    ):
                        (repo / relative).write_bytes(b"deliberately drifted bytes\n")
                    for relative in (
                        ".agents/skills/task-implementation-flow/"
                        "task-review-discovery/references/discovery-report-template.md",
                        ".agents/skills/task-implementation-flow/"
                        "bounded-task-implementer/evals/evals.json",
                    ):
                        (repo / relative).unlink()
                    extra = (
                        repo
                        / ".agents"
                        / "skills"
                        / "project-direction"
                        / "unexpected-local.md"
                    )
                    extra.write_text("extra owned file\n", encoding="utf-8")
                    agents_path.write_text(
                        with_block.replace(
                            "Rerun the installer to update it",
                            "Drifted managed block bytes",
                        ),
                        encoding="utf-8",
                    )

                    # The drift check reports every mutated family and
                    # repairs nothing; refresh needs a separate explicit call.
                    tree_before = snapshot_tree(repo / ".agents")
                    agents_before = agents_path.read_bytes()
                    status_before = git(repo, "status", "--porcelain=v1")
                    drift = run_check(repo)
                    self.assertEqual(1, drift.returncode)
                    drift_info = json.loads(drift.stdout)
                    self.assertFalse(drift_info["match"])
                    self.assertEqual(
                        [
                            {
                                "category": "changed",
                                "path": ".agents/scripts/ollama-models.json",
                            },
                            {
                                "category": "changed",
                                "path": ".agents/scripts/run_evidence.py",
                            },
                            {
                                "category": "changed",
                                "path": (
                                    ".agents/scripts/"
                                    "runtime-context.schema.v1.json"
                                ),
                            },
                            {
                                "category": "changed",
                                "path": ".agents/skills/README.md",
                            },
                            {
                                "category": "changed",
                                "path": ".agents/skills/project-direction/SKILL.md",
                            },
                            {
                                "category": "unexpected",
                                "path": (
                                    ".agents/skills/project-direction/"
                                    "unexpected-local.md"
                                ),
                            },
                            {
                                "category": "missing",
                                "path": (
                                    ".agents/skills/task-implementation-flow/"
                                    "bounded-task-implementer/evals/evals.json"
                                ),
                            },
                            {
                                "category": "missing",
                                "path": (
                                    ".agents/skills/task-implementation-flow/"
                                    "task-review-discovery/references/"
                                    "discovery-report-template.md"
                                ),
                            },
                            {"category": "changed", "path": "AGENTS.md"},
                        ],
                        drift_info["differences"],
                    )
                    self.assertEqual(tree_before, snapshot_tree(repo / ".agents"))
                    self.assertEqual(agents_before, agents_path.read_bytes())
                    self.assertEqual(
                        status_before, git(repo, "status", "--porcelain=v1")
                    )
                    self.assertEqual(
                        b"deliberately drifted bytes\n",
                        (repo / ".agents/skills/project-direction/SKILL.md").read_bytes(),
                    )
                    assert_repository_identity_stable()

                    # Explicit refresh: one separate installer rerun.
                    refresh = run_installer(repo)
                    self.assertEqual(0, refresh.returncode, refresh.stderr)

                    # Independent projection inspection before trusting the
                    # matching recheck: every managed path holds current
                    # source bytes, and the owned extra is gone.
                    projection = source_projection_snapshot()
                    for managed in sorted(expected_managed_paths()):
                        if managed == "AGENTS.md":
                            continue
                        source_key = managed[len(".agents/") :]
                        self.assertIn(source_key, projection, managed)
                        installed = repo / managed
                        self.assertTrue(installed.is_file(), managed)
                        self.assertEqual(
                            projection[source_key],
                            installed.read_bytes(),
                            managed,
                        )
                    self.assertFalse(extra.exists())
                    refreshed_agents = agents_path.read_bytes().decode("utf-8")
                    begin_at = refreshed_agents.index(installer.AGENTS_BEGIN)
                    end_at = refreshed_agents.index(installer.AGENTS_END) + len(
                        installer.AGENTS_END
                    )
                    self.assertEqual(
                        installer.AGENTS_BLOCK.rstrip(),
                        refreshed_agents[begin_at:end_at],
                    )
                    self.assertEqual(outside_prefix, refreshed_agents[:begin_at])
                    self.assertEqual(outside_suffix, refreshed_agents[end_at:])
                    self.assertEqual(
                        1, refreshed_agents.count(installer.AGENTS_BEGIN)
                    )
                    self.assertEqual(1, refreshed_agents.count(installer.AGENTS_END))
                    self.assertEqual(
                        unmanaged_files, collect_package_files(unmanaged_skill)
                    )
                    self.assertEqual(
                        "VALUE = 1\n", unmanaged_script.read_text(encoding="utf-8")
                    )
                    self.assertEqual(b"user bytes\n", unrelated.read_bytes())
                    assert_repository_identity_stable()

                    self.assertEqual(preserved, {p: p.read_bytes() for p in preserved})
                    self.assertEqual(staged, git(repo, "show", ":app.py"))

                    # Matching recheck, then a second matching check that
                    # agrees with it, close the journey.
                    restored = run_check(repo)
                    self.assertEqual(0, restored.returncode, restored.stderr)
                    restored_again = run_check(repo)
                    self.assertEqual(0, restored_again.returncode, restored_again.stderr)
                    self.assertEqual(
                        json.loads(restored.stdout), json.loads(restored_again.stdout)
                    )
                    restored_info = json.loads(restored.stdout)
                    self.assertTrue(restored_info["match"])
                    self.assertEqual([], restored_info["differences"])
                    self.assertEqual(
                        len(expected_managed_paths()), restored_info["compared_paths"]
                    )

    def test_measurement_resources_changed_missing_checks_and_refresh(self):
        source_before = source_projection_snapshot()
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            init_repo(repo, agents_text="# Keep these instructions.\n")
            preserved = seed_measurement_target(repo)
            result = run_installer(repo)
            self.assertEqual(0, result.returncode, result.stderr)
            agents = (repo / "AGENTS.md").read_bytes()
            for name in EXPECTED_MEASUREMENT_FILES:
                managed = repo / ".agents/scripts" / name
                self.assertEqual((ROOT / "scripts" / name).read_bytes(), managed.read_bytes())
                for category in ("changed", "missing"):
                    with self.subTest(resource=name, category=category):
                        if category == "changed":
                            managed.write_bytes(b"changed managed resource\n")
                        else:
                            managed.unlink()
                        before = snapshot_tree(repo)
                        for _ in range(2):
                            result = run_check(repo)
                            self.assertEqual(1, result.returncode, result.stderr)
                            self.assertEqual([{"category": category, "path": f".agents/scripts/{name}"}], json.loads(result.stdout)["differences"])
                            self.assertEqual(before, snapshot_tree(repo))
                        refreshed = run_installer(repo)
                        self.assertEqual(0, refreshed.returncode, refreshed.stderr)
                        self.assertEqual((ROOT / "scripts" / name).read_bytes(), managed.read_bytes())
                        self.assertEqual(preserved, {p: p.read_bytes() for p in preserved})
                        self.assertEqual(agents, (repo / "AGENTS.md").read_bytes())
                        checked = run_check(repo)
                        self.assertEqual(0, checked.returncode, checked.stderr)
                        self.assertEqual([], json.loads(checked.stdout)["differences"])
        self.assertEqual(source_before, source_projection_snapshot())

    def test_check_reports_changed_bytes_for_every_managed_family(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)

            for label, managed_relative in self.DRIFT_FAMILIES:
                with self.subTest(family=label):
                    managed = repo / managed_relative
                    original = managed.read_bytes()
                    managed.write_bytes(b"deliberately drifted bytes\n")

                    result = run_check(repo)

                    self.assertEqual(1, result.returncode)
                    info = json.loads(result.stdout)
                    self.assertFalse(info["match"])
                    self.assertEqual(
                        [{"category": "changed", "path": managed_relative}],
                        info["differences"],
                    )
                    managed.write_bytes(original)

    def test_check_reports_missing_bytes_for_every_managed_family(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)

            for label, managed_relative in self.DRIFT_FAMILIES:
                with self.subTest(family=label):
                    managed = repo / managed_relative
                    original = managed.read_bytes()
                    managed.unlink()

                    result = run_check(repo)

                    self.assertEqual(1, result.returncode)
                    info = json.loads(result.stdout)
                    self.assertFalse(info["match"])
                    self.assertEqual(
                        [{"category": "missing", "path": managed_relative}],
                        info["differences"],
                    )
                    managed.write_bytes(original)

    def test_check_reports_every_file_of_a_missing_selected_skill_directory(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)

            shutil.rmtree(repo / ".agents/skills/project-direction")

            result = run_check(repo)

            self.assertEqual(1, result.returncode)
            info = json.loads(result.stdout)
            expected = [
                {"category": "missing", "path": path}
                for path in sorted(
                    f".agents/skills/project-direction/{name}"
                    for name in collect_package_files(ROOT / "skills/project-direction")
                )
            ]
            self.assertEqual(expected, info["differences"])

    def test_check_detects_managed_drift_that_the_workflow_fingerprint_excludes(self):
        # evals/ files are copied by the installer but excluded from workflow
        # fingerprints; a check that trusted fingerprint equivalence would
        # wrongly report a match here.
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)

            fingerprint_before = installed_identity(repo)["fingerprint"]
            managed_relative = (
                ".agents/skills/task-implementation-flow/"
                "bounded-task-implementer/evals/evals.json"
            )
            managed = repo / managed_relative
            original = managed.read_bytes()
            managed.write_bytes(b"deliberately drifted eval\n")

            identity_after = installed_identity(repo)
            self.assertEqual(fingerprint_before, identity_after["fingerprint"])
            self.assertFalse(identity_after["workflow_dirty"])

            result = run_check(repo)

            self.assertEqual(1, result.returncode)
            info = json.loads(result.stdout)
            self.assertEqual(
                [{"category": "changed", "path": managed_relative}],
                info["differences"],
            )
            managed.write_bytes(original)

    def test_check_ignores_unmanaged_content_and_installer_transient_files(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)

            unmanaged_skill = repo / ".agents/skills/custom-local-skill"
            unmanaged_skill.mkdir(parents=True)
            (unmanaged_skill / "SKILL.md").write_text(
                "---\nname: custom-local-skill\n---\nlocal\n", encoding="utf-8"
            )
            (repo / ".agents/scripts/custom_helper.py").write_text(
                "VALUE = 1\n", encoding="utf-8"
            )
            (repo / ".agents/unmanaged-note.md").write_text("note\n", encoding="utf-8")

            selected = repo / ".agents/skills/project-direction"
            (selected / "__pycache__").mkdir()
            (selected / "__pycache__/cache.pyc").write_bytes(b"\x00cached")
            (selected / "node_modules").mkdir()
            (selected / "node_modules/dep.txt").write_text("dep\n", encoding="utf-8")
            (selected / ".DS_Store").write_bytes(b"\x00store")
            (selected / "reference.pyc").write_bytes(b"\x00compiled")

            agents_path = repo / "AGENTS.md"
            agents_text = agents_path.read_text(encoding="utf-8")
            agents_path.write_text(
                "Before the marked block.\n\n"
                + agents_text
                + "\nAfter the marked block.\n",
                encoding="utf-8",
            )

            result = run_check(repo)

            self.assertEqual(0, result.returncode, result.stderr)
            info = json.loads(result.stdout)
            self.assertTrue(info["match"], info["differences"])

            # Contrast: an extra non-transient file inside a selected skill
            # directory is owned drift, unlike the unmanaged bytes above.
            (selected / "unexpected-local.md").write_text("extra\n", encoding="utf-8")
            contrast = run_check(repo)
            self.assertEqual(1, contrast.returncode)
            self.assertEqual(
                [
                    {
                        "category": "unexpected",
                        "path": ".agents/skills/project-direction/unexpected-local.md",
                    }
                ],
                json.loads(contrast.stdout)["differences"],
            )

    def test_check_reports_agents_block_drift_and_precise_marker_failures(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)
            agents_path = repo / "AGENTS.md"
            original = agents_path.read_text(encoding="utf-8")

            agents_path.write_text(
                original.replace(
                    "Rerun the installer to update it",
                    "Deliberately changed managed bytes",
                ),
                encoding="utf-8",
            )
            changed = run_check(repo)
            self.assertEqual(1, changed.returncode)
            self.assertEqual(
                [{"category": "changed", "path": "AGENTS.md"}],
                json.loads(changed.stdout)["differences"],
            )

            agents_path.write_text("# Project instructions\n", encoding="utf-8")
            missing_block = run_check(repo)
            self.assertEqual(1, missing_block.returncode)
            self.assertEqual(
                [{"category": "missing", "path": "AGENTS.md"}],
                json.loads(missing_block.stdout)["differences"],
            )

            agents_path.unlink()
            missing_file = run_check(repo)
            self.assertEqual(1, missing_file.returncode)
            self.assertEqual(
                [{"category": "missing", "path": "AGENTS.md"}],
                json.loads(missing_file.stdout)["differences"],
            )

            for label, defective, diagnostic in (
                (
                    "unmatched begin marker",
                    f"# Title\n\n{installer.AGENTS_BEGIN}\nincomplete managed block\n",
                    "malformed development-install markers",
                ),
                (
                    "duplicate marker pairs",
                    original + "\n\n" + original,
                    "malformed development-install markers",
                ),
                (
                    "reversed markers",
                    f"# Title\n\n{installer.AGENTS_END}\n{installer.AGENTS_BEGIN}\n",
                    "reversed development-install markers",
                ),
            ):
                with self.subTest(defect=label):
                    agents_path.write_text(defective, encoding="utf-8")

                    result = run_check(repo)

                    self.assertEqual(2, result.returncode)
                    self.assertEqual("", result.stdout)
                    self.assertIn("error:", result.stderr)
                    self.assertIn(diagnostic, result.stderr)

    def test_check_failures_retain_existing_refusals_and_stay_distinct_from_drift(self):
        with tempfile.TemporaryDirectory() as tempdir:
            result = run_check(Path(tempdir) / "absent-target")
            self.assertEqual(2, result.returncode)
            self.assertEqual("", result.stdout)
            self.assertIn("target repository does not exist", result.stderr)

        with tempfile.TemporaryDirectory() as tempdir:
            non_repo = Path(tempdir)
            (non_repo / "app.txt").write_text("not a repository\n", encoding="utf-8")
            result = run_check(non_repo)
            self.assertEqual(2, result.returncode)
            self.assertIn("target repository is not usable", result.stderr)

        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            init_repo(repo)
            (repo / "nested").mkdir()
            result = run_check(repo / "nested")
            self.assertEqual(2, result.returncode)
            self.assertIn("target path must be the Git repository root", result.stderr)

        with (
            tempfile.TemporaryDirectory() as repo_dir,
            tempfile.TemporaryDirectory() as outside_dir,
        ):
            repo = Path(repo_dir)
            outside = Path(outside_dir)
            init_repo(repo)
            (outside / "payload.txt").write_text("outside content\n", encoding="utf-8")
            (repo / ".agents").symlink_to(outside)
            result = run_check(repo)
            self.assertEqual(2, result.returncode)
            self.assertIn(
                "refusing to manage symlinked installation path", result.stderr
            )
            self.assertTrue((repo / ".agents").is_symlink())
            self.assertEqual(b"outside content\n", (outside / "payload.txt").read_bytes())

        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)
            script = repo / ".agents/scripts/run_evidence.py"
            script.unlink()
            script.mkdir()
            result = run_check(repo)
            self.assertEqual(2, result.returncode)
            self.assertIn("shared script destination is not a file", result.stderr)

        with (
            tempfile.TemporaryDirectory() as source_dir,
            tempfile.TemporaryDirectory() as target_dir,
        ):
            source = Path(source_dir)
            target = Path(target_dir)
            init_repo(target, agents_text="# Existing\n")
            with mock.patch.object(installer, "SOURCE_REPO", source):
                with self.assertRaisesRegex(
                    installer.InstallError, "missing development-profile inputs"
                ):
                    installer.check(target)
            self.assertFalse((target / ".agents").exists())
            self.assertEqual(
                "# Existing\n", (target / "AGENTS.md").read_text(encoding="utf-8")
            )

    def test_check_reports_unreadable_required_content_as_failure(self):
        if os.geteuid() == 0:
            self.skipTest("read-failure oracle requires a non-root user")
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)
            managed = repo / ".agents/skills/project-direction/SKILL.md"
            os.chmod(managed, 0o000)
            try:
                result = run_check(repo)
            finally:
                os.chmod(managed, 0o644)

            self.assertEqual(2, result.returncode)
            self.assertEqual("", result.stdout)
            self.assertIn("cannot read required skill content", result.stderr)
            self.assertIn(str(managed), result.stderr)
            self.assertEqual(
                (ROOT / "skills/project-direction/SKILL.md").read_bytes(),
                managed.read_bytes(),
            )

            # A dangling symlink at a required managed path is a metadata
            # failure with a precise diagnostic, never silently dropped
            # content and never a match.
            original = managed.read_bytes()
            managed.unlink()
            managed.symlink_to(repo / ".agents/skills/project-direction/absent")
            try:
                result = run_check(repo)
            finally:
                managed.unlink()
                managed.write_bytes(original)

            self.assertEqual(2, result.returncode, result.stderr)
            self.assertEqual("", result.stdout)
            self.assertIn("cannot access installed skill content", result.stderr)
            self.assertIn(str(managed), result.stderr)
            self.assertEqual(original, managed.read_bytes())

    def test_check_reports_unreadable_managed_directories_as_failures(self):
        # F-01 regression: enumeration denial inside a selected skill tree
        # must never collapse to a false match (unexpected subtree) or to
        # ordinary missing-content drift (expected subtree).
        if os.geteuid() == 0:
            self.skipTest("read-failure oracle requires a non-root user")
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            self.install_profile(repo)
            selected = repo / ".agents/skills/project-direction"
            unexpected_drift = [
                {
                    "category": "unexpected",
                    "path": ".agents/skills/project-direction/reviewer-unreadable/extra.txt",
                }
            ]

            extra_dir = selected / "reviewer-unreadable"
            extra_dir.mkdir()
            (extra_dir / "extra.txt").write_bytes(b"extra owned bytes\n")
            extra_bytes = (extra_dir / "extra.txt").read_bytes()

            # While readable, the extra subtree is ordinary owned drift.
            readable = run_check(repo)
            self.assertEqual(1, readable.returncode)
            self.assertEqual(
                unexpected_drift, json.loads(readable.stdout)["differences"]
            )

            for denied in (extra_dir, selected / "references"):
                with self.subTest(denied=denied.name):
                    original_mode = denied.stat().st_mode & 0o777
                    os.chmod(denied, 0)
                    try:
                        first = run_check(repo)
                        second = run_check(repo)
                    finally:
                        os.chmod(denied, original_mode)

                    self.assertEqual(2, first.returncode, first.stderr)
                    self.assertEqual(2, second.returncode)
                    self.assertEqual("", first.stdout)
                    self.assertIn(
                        "cannot enumerate installed skill directory", first.stderr
                    )
                    self.assertIn(str(denied), first.stderr)
                    self.assertEqual(first.stderr, second.stderr)

            # Checking left the denied subtrees untouched: the extra bytes
            # are unchanged, readable state returns to the prior drift, and
            # the rest of the projection still matches the source.
            self.assertEqual(extra_bytes, (extra_dir / "extra.txt").read_bytes())
            restored = run_check(repo)
            self.assertEqual(1, restored.returncode)
            self.assertEqual(
                unexpected_drift, json.loads(restored.stdout)["differences"]
            )
            shutil.rmtree(extra_dir)
            self.assertEqual(0, run_check(repo).returncode)

    def test_check_reports_unreadable_source_directories_as_failures(self):
        # The source side uses the same collector: a source subtree that
        # cannot be enumerated is a check failure, never a silently smaller
        # expected projection.
        if os.geteuid() == 0:
            self.skipTest("read-failure oracle requires a non-root user")
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            for _, relative in installer.DEVELOPMENT_SKILL_SOURCES:
                skill_dir = source / relative
                skill_dir.mkdir(parents=True, exist_ok=True)
                (skill_dir / "SKILL.md").write_text("source\n", encoding="utf-8")
            scripts_dir = source / "scripts"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            for name in installer.SHARED_SCRIPT_FILES:
                (scripts_dir / name).write_text("source\n", encoding="utf-8")
            (source / installer.PROFILE_SKILLS_README).write_text(
                "source\n", encoding="utf-8"
            )

            references = source / "skills/project-direction/references"
            references.mkdir()
            (references / "direction-template.md").write_text(
                "source\n", encoding="utf-8"
            )
            os.chmod(references, 0)

            target = Path(target_dir)
            init_repo(target)
            try:
                with mock.patch.object(installer, "SOURCE_REPO", source):
                    with self.assertRaisesRegex(
                        installer.InstallError,
                        "cannot enumerate source skill directory",
                    ):
                        installer.check(target)
            finally:
                os.chmod(references, 0o700)
            self.assertFalse((target / ".agents").exists())

    def test_check_covers_directory_linked_source_content_the_installer_copies(self):
        # F-02 regression: install-time copying dereferences directory
        # symlinks inside selected source packages, so the expected
        # projection must cover linked content. A fresh installation is an
        # exact match, and deleting copied linked content is exact missing
        # drift, never a false match.
        with (
            tempfile.TemporaryDirectory() as base_dir,
            tempfile.TemporaryDirectory() as target_dir,
        ):
            base = Path(base_dir)
            source, cli = build_relocated_source_distribution(base)
            outside = base / "outside"
            outside.mkdir()
            (outside / "copied.txt").write_text(
                "copied source bytes\n", encoding="utf-8"
            )
            (source / "skills/project-direction/linked-reference").symlink_to(
                outside, target_is_directory=True
            )

            def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    [sys.executable, str(cli), *args],
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=ROOT,
                    timeout=60,
                )

            target = Path(target_dir)
            init_repo(target, agents_text="# Project instructions\n")

            installed = run_cli(str(target))
            self.assertEqual(0, installed.returncode, installed.stderr)
            copied = target / (
                ".agents/skills/project-direction/linked-reference/copied.txt"
            )
            self.assertEqual(
                "copied source bytes\n", copied.read_text(encoding="utf-8")
            )

            fresh = run_cli("--check", str(target))
            self.assertEqual(0, fresh.returncode, fresh.stderr)
            info = json.loads(fresh.stdout)
            self.assertTrue(info["match"], info["differences"])
            self.assertEqual(str(source.resolve()), info["source_repo"])
            self.assertEqual(
                len(expected_managed_paths()) + 1, info["compared_paths"]
            )

            # Contrast: an inner installed symlink is never traversed as a
            # trusted installation; the expected real files report missing.
            references = target / ".agents/skills/project-direction/references"
            saved = target / "references-saved"
            references.rename(saved)
            references.symlink_to(saved, target_is_directory=True)
            try:
                symlinked = run_cli("--check", str(target))
                self.assertEqual(1, symlinked.returncode)
                self.assertEqual(
                    [
                        {"category": "missing", "path": path}
                        for path in sorted(
                            f".agents/skills/project-direction/references/{name}"
                            for name in collect_package_files(
                                ROOT / "skills/project-direction/references"
                            )
                        )
                    ],
                    json.loads(symlinked.stdout)["differences"],
                )
            finally:
                references.unlink()
                saved.rename(references)

            shutil.rmtree(copied.parent)
            deleted = run_cli("--check", str(target))
            self.assertEqual(1, deleted.returncode)
            self.assertEqual(
                [
                    {
                        "category": "missing",
                        "path": ".agents/skills/project-direction/"
                        "linked-reference/copied.txt",
                    }
                ],
                json.loads(deleted.stdout)["differences"],
            )

    def test_check_matches_acyclic_directory_aliases_the_installer_copies(self):
        # F-03 regression: install-time copying dereferences every acyclic
        # linked path, so two links to one external directory and a real
        # directory aliased by a link are valid copied content. The check
        # compares every copy and reports the fresh installation as a match;
        # a repeated identical check agrees, and deleting one aliased copy
        # is exact missing drift rather than a match through the surviving
        # alias. A link that closes an ancestor cycle still fails precisely
        # (covered by the cyclic test below).
        with (
            tempfile.TemporaryDirectory() as base_dir,
            tempfile.TemporaryDirectory() as target_dir,
        ):
            base = Path(base_dir)
            source, cli = build_relocated_source_distribution(base)
            outside = base / "outside"
            outside.mkdir()
            (outside / "copied.txt").write_text(
                "shared source bytes\n", encoding="utf-8"
            )
            package = source / "skills/project-direction"
            for name in ("linked-a", "linked-b"):
                (package / name).symlink_to(outside, target_is_directory=True)
            (package / "references-alias").symlink_to(
                package / "references", target_is_directory=True
            )

            def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    [sys.executable, str(cli), *args],
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=ROOT,
                    timeout=60,
                )

            target = Path(target_dir)
            init_repo(target, agents_text="# Project instructions\n")

            installed = run_cli(str(target))
            self.assertEqual(0, installed.returncode, installed.stderr)

            fresh = run_cli("--check", str(target))
            self.assertEqual(0, fresh.returncode, fresh.stderr)
            info = json.loads(fresh.stdout)
            self.assertTrue(info["match"], info["differences"])
            reference_names = collect_package_files(
                ROOT / "skills/project-direction/references"
            )
            self.assertEqual(
                len(expected_managed_paths())
                + 2
                + len(reference_names),
                info["compared_paths"],
            )
            for name in ("linked-a", "linked-b"):
                copied = target / (
                    f".agents/skills/project-direction/{name}/copied.txt"
                )
                self.assertEqual(
                    "shared source bytes\n", copied.read_text(encoding="utf-8")
                )
                self.assertFalse(copied.is_symlink())

            repeated = run_cli("--check", str(target))
            self.assertEqual(
                (fresh.returncode, fresh.stdout, fresh.stderr),
                (repeated.returncode, repeated.stdout, repeated.stderr),
            )

            shutil.rmtree(target / ".agents/skills/project-direction/linked-a")
            deleted = run_cli("--check", str(target))
            self.assertEqual(1, deleted.returncode)
            self.assertEqual(
                [
                    {
                        "category": "missing",
                        "path": ".agents/skills/project-direction/"
                        "linked-a/copied.txt",
                    }
                ],
                json.loads(deleted.stdout)["differences"],
            )

    def test_check_fails_precisely_on_cyclic_source_directory_symlinks(self):
        # Following linked source directories must terminate: a link that
        # points back at an ancestor is a precise check failure, not a
        # hanging or silently shrunk comparison.
        with (
            tempfile.TemporaryDirectory() as base_dir,
            tempfile.TemporaryDirectory() as target_dir,
        ):
            base = Path(base_dir)
            source, cli = build_relocated_source_distribution(base)
            package = source / "skills/project-direction"
            (package / "loop").symlink_to(package, target_is_directory=True)

            target = Path(target_dir)
            init_repo(target, agents_text="# Project instructions\n")
            result = subprocess.run(
                [sys.executable, str(cli), "--check", str(target)],
                capture_output=True,
                text=True,
                check=False,
                cwd=ROOT,
                timeout=60,
            )

            self.assertEqual(2, result.returncode)
            self.assertEqual("", result.stdout)
            self.assertIn("cannot enumerate source skill directory", result.stderr)
            self.assertIn("directory cycle", result.stderr)
            self.assertIn(str(package / "loop"), result.stderr)
            self.assertFalse((target / ".agents").exists())

    def test_check_results_and_repeated_checks_leave_all_state_unchanged(self):
        with tempfile.TemporaryDirectory() as tempdir:
            base = Path(tempdir)
            fixtures: dict[Path, int] = {}

            match_committed = base / "match-committed"
            self.install_profile(match_committed)
            fixtures[match_committed] = 0

            match_unborn = base / "match-unborn"
            self.install_profile(match_unborn, commit=False)
            fixtures[match_unborn] = 0

            drift_committed = base / "drift-committed"
            self.install_profile(drift_committed)
            (drift_committed / ".agents/skills/README.md").write_text(
                "deliberately drifted guide\n", encoding="utf-8"
            )
            fixtures[drift_committed] = 1

            absent_unborn = base / "absent-unborn"
            absent_unborn.mkdir()
            init_repo(absent_unborn, commit=False)
            fixtures[absent_unborn] = 1

            failure_committed = base / "failure-committed"
            unreadable = None
            if os.geteuid() != 0:
                self.install_profile(failure_committed)
                unreadable = failure_committed / ".agents/skills/project-direction/SKILL.md"
                os.chmod(unreadable, 0o000)
                fixtures[failure_committed] = 2

            # Snapshots cover the whole target tree including Git metadata and
            # the installer-written evidence storage under
            # .git/personal-skills/run-evidence. Two behavioral canaries reject
            # a check that repairs behind the scenes: the drifted fixture must
            # keep reporting the same drift twice, and the absent installation
            # must stay absent.
            source_before = source_projection_snapshot()

            try:
                for fixture, expected_exit in fixtures.items():
                    with self.subTest(fixture=fixture.name):
                        before = snapshot_tree(fixture)
                        first = run_check(fixture)
                        self.assertEqual(expected_exit, first.returncode, first.stderr)
                        middle = snapshot_tree(fixture)
                        second = run_check(fixture)
                        self.assertEqual(first.returncode, second.returncode)
                        self.assertEqual(first.stdout, second.stdout)
                        self.assertEqual(first.stderr, second.stderr)
                        after = snapshot_tree(fixture)
                        self.assertEqual(before, middle)
                        self.assertEqual(before, after)
                        if fixture is absent_unborn:
                            self.assertFalse((fixture / ".agents").exists())
                        if expected_exit == 2:
                            self.assertIn(
                                "cannot read required skill content", first.stderr
                            )
            finally:
                if unreadable is not None:
                    os.chmod(unreadable, 0o644)

            self.assertEqual(source_before, source_projection_snapshot())

    def test_check_matches_install_from_unrelated_cwd_and_guides_document_semantics(self):
        with (
            tempfile.TemporaryDirectory() as target_dir,
            tempfile.TemporaryDirectory() as cwd_dir,
        ):
            target = Path(target_dir)
            unrelated_cwd = Path(cwd_dir)
            init_repo(target, agents_text="# Project instructions\n\nKeep this line.\n")
            unmanaged_skill = target / ".agents/skills/custom-local-skill"
            unmanaged_skill.mkdir(parents=True)
            (unmanaged_skill / "SKILL.md").write_text(
                "---\nname: custom-local-skill\n---\nlocal\n", encoding="utf-8"
            )
            unmanaged_script = target / ".agents/scripts/custom_helper.py"
            unmanaged_script.parent.mkdir(parents=True)
            unmanaged_script.write_text("VALUE = 1\n", encoding="utf-8")

            # Positional installation keeps working and resolves source from
            # the installer location, not the caller's working directory.
            installed = run_installer(target, cwd=unrelated_cwd)
            self.assertEqual(0, installed.returncode, installed.stderr)

            result = run_check(target, cwd=unrelated_cwd)

            self.assertEqual(0, result.returncode, result.stderr)
            info = json.loads(result.stdout)
            self.assertTrue(info["match"], info["differences"])
            self.assertEqual(str(ROOT), info["source_repo"])
            self.assertEqual(str(target.resolve()), info["target_repo"])
            self.assertEqual(
                "---\nname: custom-local-skill\n---\nlocal\n",
                (unmanaged_skill / "SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertEqual("VALUE = 1\n", unmanaged_script.read_text(encoding="utf-8"))
            agents_text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Project instructions", agents_text)
            self.assertIn("Keep this line.", agents_text)

            for path in CHECK_GUIDE_PATHS:
                text = " ".join((ROOT / path).read_text(encoding="utf-8").split())
                for phrase in CHECK_GUIDE_REQUIRED_PHRASES:
                    self.assertIn(
                        phrase, text, f"{path}: missing check guidance: {phrase}"
                    )


if __name__ == "__main__":
    unittest.main()
