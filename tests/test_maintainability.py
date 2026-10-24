import base64
from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
import shlex
import venv
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import unittest
from unittest.mock import patch

from test_install_development_skills import build_relocated_source_distribution, init_repo, installer, snapshot_tree


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("maintainability", ROOT / "scripts" / "maintainability.py")
metrics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(metrics)
HAS_TOOLS = metrics.tool_version("radon") and metrics.tool_version("ruff")
ENV_SPEC = importlib.util.spec_from_file_location("maintainability_env", ROOT / "scripts/maintainability_env.py")
environment = importlib.util.module_from_spec(ENV_SPEC)
ENV_SPEC.loader.exec_module(environment)


def function(name, branches):
    return f"def {name}(value):\n" + "    if value: pass\n" * branches + "    return value\n"


@unittest.skipUnless(HAS_TOOLS, "Run with the Python environment printed by setup; real Radon and Ruff required")
class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = self.root / "sample.py"
        self.source.write_text(function("small", 1))

    def report(self, checks=("complexity", "ruff")):
        return metrics.build_report(self.root, ["."], list(checks))

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True, text=True).stdout

    def installed_launcher(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        source, install_cli = build_relocated_source_distribution(base)
        init_repo(self.root)
        result = subprocess.run([sys.executable, str(install_cli), str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        shutil.rmtree(source)  # No source-distribution resources remain accessible.
        unrelated = base / "unrelated"
        unrelated.mkdir()
        return self.root / ".agents/scripts/measure_maintainability.py", unrelated

    def launch(self, launcher, cwd, *args):
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        return subprocess.run([sys.executable, str(launcher), *args, "--root", str(self.root)],
                              cwd=cwd, env=env, capture_output=True, text=True)

    def test_installed_and_source_launchers_work_without_distribution(self):
        installed, cwd = self.installed_launcher()
        for label, launcher in (("installed", installed), ("source", ROOT / "scripts/measure_maintainability.py")):
            with self.subTest(launcher=label):
                self.source.write_text(function("small", 1))
                before_path = self.root / f".quality/reports/{label}-before.json"
                after_path = self.root / f".quality/reports/{label}-after.json"
                before = self.launch(launcher, cwd, "baseline", ".", "--output", str(before_path))
                self.assertEqual(0, before.returncode, before.stderr)
                saved = {path: path.read_bytes() for path in (before_path, before_path.with_suffix(".txt"))}
                self.source.write_text(function("small", 2))
                after = self.launch(launcher, cwd, "compare", "sample.py", "--baseline", str(before_path), "--output", str(after_path))
                self.assertEqual(0, after.returncode, after.stderr)
                report = json.loads(after_path.read_text())
                row, = report["comparison"]["complexity"]
                self.assertEqual((2, 3, 1), tuple(row[key] for key in ("before", "value", "delta")))
                self.assertEqual("complete", report["measurement_status"])
                self.assertTrue(after_path.with_suffix(".txt").is_file())
                for name, setting in report["identity"]["settings"].items():
                    self.assertEqual("shipped", setting["origin"])
                    self.assertEqual(launcher.parent.resolve(), Path(setting["path"]).parent)
                self.assertEqual(saved, {path: path.read_bytes() for path in saved})
                measured = self.launch(launcher, cwd, "measure", "sample.py")
                self.assertEqual(0, measured.returncode, measured.stderr)
                self.assertIn("CC 3:", measured.stdout)
                self.assertFalse((self.root / ".quality/envs").exists())

    def test_real_complexity_boundaries_and_below_target_increase(self):
        self.source.write_text(function("small", 1) + function("at_target", 9)
                               + function("legacy", 10) + function("improves", 15))
        baseline = self.report()
        self.assertEqual([2, 10, 11, 16], [x["value"] for x in baseline["checks"]["complexity"]["values"]])
        self.source.write_text("\n\n" + function("small", 2) + function("at_target", 9)
                               + function("legacy", 10) + function("improves", 1)
                               + function("new_hotspot", 10))
        result = metrics.comparison(self.report(), baseline)
        rows = {row["symbol"]: row for row in result["complexity"]}
        self.assertEqual("compared", result["status"])
        self.assertEqual((2, 3, 1, ["got_worse"]), tuple(rows["small"][key] for key in ("before", "value", "delta", "highlights")))
        self.assertEqual("unchanged", rows["legacy"]["classification"])
        self.assertEqual([], rows["legacy"]["highlights"])
        self.assertEqual("improved", rows["improves"]["classification"])
        self.assertEqual("new", rows["new_hotspot"]["classification"])
        self.assertIn("new_above_threshold", rows["new_hotspot"]["highlights"])
        self.source.write_text(function("at_target", 10))
        row = metrics.comparison(self.report(), baseline)["complexity"][0]
        self.assertEqual(["got_worse", "crossed_above_threshold"], row["highlights"])

    def test_nested_scopes_async_and_duplicate_names_are_not_conflated(self):
        self.source.write_text("""class Outer:
    def method(self, value):
        class Local:
            def method(self):
                return 1
        async def nested():
            return 2
        if value:
            return nested
        return Local
def duplicate(): pass
def duplicate(): pass
""")
        baseline = self.report()
        values = baseline["checks"]["complexity"]["values"]
        self.assertEqual(["Outer.method", "Outer.method.Local.method", "Outer.method.nested", "duplicate", "duplicate"],
                         [item["symbol"] for item in values])
        self.assertEqual([2, 1, 1, 1, 1], [item["value"] for item in values])
        result = metrics.comparison(self.report(), baseline)
        self.assertTrue(all(item["classification"] == "unmatched" for item in result["complexity"][-2:]))
        duplicates = [item for item in result["ruff"] if item["symbol"] == "duplicate"]
        self.assertEqual(2, len(duplicates))
        self.assertTrue(all(item["classification"] == "unmatched" and item["delta"] is None for item in duplicates))

    def test_added_and_removed_symbols_need_interpretation_without_guessing_relationships(self):
        baseline = self.report()
        self.source.write_text(function("renamed", 1) + function("extracted", 0))
        rows = metrics.comparison(self.report(), baseline)["complexity"]
        self.assertEqual({"small", "renamed", "extracted"}, {item["symbol"] for item in rows})
        self.assertEqual(["new", "new", "removed"], [item["classification"] for item in rows])
        self.assertTrue(all(item["highlights"] == ["needs_interpretation"] for item in rows))

    def test_ruff_real_diagnostics_and_override_exemption(self):
        self.source.write_text("from typing import override\n"
                               "def five(a,b,c,d,e): pass\n"
                               "def six(a,b,c,d,e,f): pass  # noqa: PLR0913\n"
                               "class Child:\n"
                               "    @override\n"
                               "    def method(self,a,b,c,d,e,f): pass\n"
                               "def long_function():\n" + "    value = 1\n" * 51)
        report = self.report()
        self.assertEqual("complete", report["measurement_status"])
        self.assertEqual(4, report["format_version"])
        self.assertEqual({"lint.pylint.max-args": 0, "lint.pylint.max-statements": 0},
                         report["identity"]["ruff_collection_limits"])
        findings = report["checks"]["ruff"]["values"]
        values = {(item["symbol"], item["code"]): item for item in findings}
        self.assertEqual({("five", "PLR0913"): 5, ("five", "PLR0915"): 1,
                          ("six", "PLR0913"): 6, ("six", "PLR0915"): 1,
                          ("Child.method", "PLR0915"): 1, ("long_function", "PLR0915"): 51},
                         {key: item["value"] for key, item in values.items()})
        for item in findings:
            self.assertEqual(0, item["collection_threshold"])
            self.assertEqual(5 if item["code"] == "PLR0913" else 50, item["target"])
        self.assertIn("6 > 0", values["six", "PLR0913"]["message"])
        self.assertIn("51 > 0", values["long_function", "PLR0915"]["message"])
        report["comparison"] = metrics.comparison(report, None)
        self.assertEqual({("six", "PLR0913"), ("long_function", "PLR0915")},
                         {(item["symbol"], item["metric"]) for item in metrics.report_highlights(report)})

    def test_incompatible_scope_tool_configuration_and_failed_baseline(self):
        baseline = self.report()
        for change in ("tools", "ruff_config", "ruff_collection_limits", "adapter_sha256", "python_implementation"):
            with self.subTest(change=change):
                changed = json.loads(json.dumps(baseline))
                changed["identity"][change] = "different"
                self.assertEqual("incompatible", metrics.comparison(self.report(), changed)["status"])
        changed = dict(baseline, format_version=3)
        self.assertIn("report format differs", metrics.comparison(self.report(), changed)["reasons"])
        changed = json.loads(json.dumps(baseline))
        changed["identity"].pop("ruff_collection_limits")
        self.assertEqual("incompatible", metrics.comparison(self.report(), changed)["status"])
        baseline["measurement_status"] = "incomplete"
        self.assertEqual("incompatible", metrics.comparison(self.report(), baseline)["status"])
        path = self.root / "incomplete.json"
        path.write_text(json.dumps(baseline))
        result = self.launch(ROOT / "scripts/measure_maintainability.py", self.root, "compare", ".", "--baseline", str(path))
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertIn("comparison: incompatible", result.stdout)

    def test_report_can_be_compared_from_a_different_mount_path(self):
        baseline = self.report()
        with tempfile.TemporaryDirectory() as relocated:
            root = Path(relocated)
            (root / "sample.py").write_text(function("small", 2))
            current = metrics.build_report(root, ["."], ["complexity", "ruff"])
        # Patch versions may differ between host and sandbox; parser versions may not.
        baseline["identity"]["python"] = ".".join(map(str, sys.version_info[:2])) + ".0"
        result = metrics.comparison(current, baseline)
        self.assertEqual("compared", result["status"])
        self.assertEqual(1, result["complexity"][0]["delta"])
        baseline["identity"]["python"] = "3.0.0"
        self.assertEqual("incompatible", metrics.comparison(current, baseline)["status"])

    def test_cli_report_handoff_uses_target_root_for_relative_report_paths(self):
        launcher = [sys.executable, str(ROOT / "scripts/measure_maintainability.py")]
        before = subprocess.run([*launcher, "baseline", ".", "--root", str(self.root),
                                 "--output", ".quality/reports/before.json"], capture_output=True, text=True)
        self.assertEqual(0, before.returncode, before.stderr)
        with tempfile.TemporaryDirectory() as temporary:
            other = Path(temporary) / "checkout"
            shutil.copytree(self.root, other)
            (other / "sample.py").write_text(function("small", 3))
            result = subprocess.run([*launcher, "compare", "sample.py", "--root", str(other),
                                     "--baseline", ".quality/reports/before.json",
                                     "--output", ".quality/reports/after.json"], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads((other / ".quality/reports/after.json").read_text())
            self.assertEqual("compared", report["comparison"]["status"])
            self.assertEqual(2, report["highlights"][0]["delta"])
            self.assertEqual(["sample.py"], list(report["files"]))
            self.assertTrue((other / ".quality/reports/after.txt").is_file())
            (other / "sample.py").unlink()
            removed = subprocess.run([*launcher, "compare", "sample.py", "--root", str(other),
                                      "--baseline", ".quality/reports/before.json"], capture_output=True, text=True)
            self.assertEqual(0, removed.returncode, removed.stderr)
            self.assertIn("Needs interpretation: CC 2->none: sample.py:1 small", removed.stdout)

    def test_identical_ruff_messages_on_new_symbols_remain_new_diagnostics(self):
        self.source.write_text("def existing(a,b,c,d,e,f): pass\n")
        baseline = self.report()
        self.source.write_text("\n\ndef existing(a,b,c,d,e,f): pass\n"
                               "def added(a,b,c,d,e,f): pass\n")
        findings = metrics.comparison(self.report(), baseline)["ruff"]
        arguments = [item for item in findings if item["metric"] == "PLR0913"]
        self.assertEqual(["unchanged", "new_diagnostic"], [item["classification"] for item in arguments])
        self.assertEqual([[], ["above_threshold", "needs_interpretation"]], [item["highlights"] for item in arguments])
        statements = [item for item in findings if item["metric"] == "PLR0915"]
        self.assertEqual([[], ["needs_interpretation"]], [item["highlights"] for item in statements])

    def test_ruff_native_counts_distinguish_improvement_and_worsening(self):
        for old, new, classification, highlights in (
            (7, 6, "improved", ["improved"]),
            (6, 7, "worsened", ["got_worse"]),
            (5, 6, "worsened", ["got_worse", "crossed_above_threshold"]),
            (6, 5, "improved", ["improved"]),
            (4, 5, "worsened", ["got_worse"]),
        ):
            with self.subTest(old=old, new=new):
                self.source.write_text("def wide(" + ",".join(f"a{i}" for i in range(old)) + "): pass\n")
                baseline = self.report()
                self.source.write_text("def wide(" + ",".join(f"a{i}" for i in range(new)) + "): pass\n")
                current = self.report()
                row = next(item for item in metrics.comparison(current, baseline)["ruff"]
                           if item["metric"] == "PLR0913")
                self.assertEqual((old, new, new - old), tuple(row[key] for key in ("before", "value", "delta")))
                self.assertEqual(classification, row["classification"])
                self.assertEqual(highlights, row["highlights"])

    def test_ruff_statement_changes_keep_advisory_targets(self):
        for old, new, highlights in ((20, 25, ["got_worse"]),
                                     (50, 51, ["got_worse", "crossed_above_threshold"]),
                                     (25, 20, ["improved"])):
            with self.subTest(old=old, new=new):
                self.source.write_text("def body():\n" + "    value = 1\n" * old)
                baseline = self.report(("ruff",))
                self.source.write_text("def body():\n" + "    value = 1\n" * new)
                row, = metrics.comparison(self.report(("ruff",)), baseline)["ruff"]
                self.assertEqual((old, new, new - old, 50),
                                 tuple(row[key] for key in ("before", "value", "delta", "target")))
                self.assertEqual(highlights, row["highlights"])

    def test_ruff_missing_diagnostics_never_become_numeric_zero(self):
        for before, after, metric, count, highlights in (
            ("def f(): pass\n", "def f(a): pass\n", "PLR0913", 1, ["needs_interpretation"]),
            ("def f(): return 1\n", "def f():\n    a = 1\n    return a\n", "PLR0915", 1, ["needs_interpretation"]),
            ("class C:\n    @overload\n    def f(self,a,b,c,d,e,f): ...\n",
             "class C:\n    def f(self,a,b,c,d,e,f): ...\n", "PLR0913", 6,
             ["above_threshold", "needs_interpretation"]),
            ("class C:\n    @override\n    def f(self,a,b,c,d,e,f): pass\n",
             "class C:\n    def f(self,a,b,c,d,e,f): pass\n", "PLR0913", 6,
             ["above_threshold", "needs_interpretation"]),
        ):
            with self.subTest(before=before, metric=metric):
                reports = []
                for source in (before, after):
                    self.source.write_text("from typing import override, overload\n" + source)
                    reports.append(self.report(("ruff",)))
                added = next(item for item in metrics.comparison(reports[1], reports[0])["ruff"]
                             if item["metric"] == metric)
                self.assertEqual((None, count, None, "new_diagnostic", highlights),
                                 tuple(added[key] for key in ("before", "value", "delta", "classification", "highlights")))
                removed = next(item for item in metrics.comparison(reports[0], reports[1])["ruff"]
                               if item["metric"] == metric)
                self.assertEqual((count, None, None, "diagnostic_resolved", ["needs_interpretation"]),
                                 tuple(removed[key] for key in ("before", "value", "delta", "classification", "highlights")))

    def test_settings_select_each_target_file_independently(self):
        self.source.write_text(function("branch", 4) + "def f(a,b,c): pass\n")
        quality = self.root / ".quality"
        quality.mkdir()
        launcher, cwd = self.installed_launcher()
        defaults = {name: launcher.parent / path.name for name, path in metrics.DEFAULT_FILES.items()}
        policies = {
            "maintainability.toml": defaults["maintainability.toml"].read_text().replace("complexity_target = 10", "complexity_target = 3"),
            "ruff.toml": defaults["ruff.toml"].read_text().replace("max-args = 5", "max-args = 2").replace("max-statements = 50", "max-statements = 3"),
        }
        for present in ((), ("maintainability.toml",), ("ruff.toml",), tuple(policies)):
            with self.subTest(present=present):
                for name, content in policies.items():
                    path = quality / name
                    path.unlink(missing_ok=True)
                    if name in present:
                        path.write_text(content)
                output = f".quality/reports/policy-{len(present)}-{'ruff' if 'ruff.toml' in present else 'cc'}.json"
                result = self.launch(launcher, cwd, "measure", ".", "--output", output)
                self.assertEqual(0, result.returncode, result.stderr)
                report = json.loads((self.root / output).read_text())
                branch = next(row for row in report["checks"]["complexity"]["values"] if row["symbol"] == "branch")
                self.assertEqual((5, 3 if "maintainability.toml" in present else 10),
                                 (branch["value"], branch["target"]))
                rows = [row for row in report["checks"]["ruff"]["values"] if row["symbol"] == "f"]
                self.assertEqual([(3, 2 if "ruff.toml" in present else 5, 0),
                                  (1, 3 if "ruff.toml" in present else 50, 0)],
                                 [(row["value"], row["target"], row["collection_threshold"]) for row in rows])
                for name in policies:
                    origin = "target" if name in present else "shipped"
                    effective = (quality / name) if name in present else defaults[name]
                    self.assertEqual({"origin": origin, "path": str(effective.resolve()),
                                      "sha256": metrics.digest(effective.read_bytes())},
                                     report["identity"]["settings"][name])
                    if name in present:
                        self.assertEqual(policies[name], effective.read_text())

    def test_invalid_policy_settings_fail_before_measurement(self):
        launcher, cwd = self.installed_launcher()
        path = self.root / ".quality/maintainability.toml"
        path.parent.mkdir(exist_ok=True)
        defaults = metrics.DEFAULT_FILES["maintainability.toml"].read_text()
        (self.root / ".git/hidden.py").write_text("def invalid(:")
        path.write_text(defaults)
        control = self.launch(launcher, cwd, "measure", ".", "--output", "control.json")
        self.assertEqual(0, control.returncode, control.stderr)
        report = json.loads((self.root / "control.json").read_text())
        self.assertEqual(["sample.py"], list(report["files"]))
        self.assertEqual(10, report["checks"]["complexity"]["values"][0]["target"])
        cases = {
            "complexity_target": ("true", '"10"', "1.5", "-1"),
            "exclude_directories": ('".git"', "[1]", '[""]'),
            "checks": ('"complexity"', "[true]", '["unknown"]', "[]"),
            "profile": ("true", '""'),
        }
        for field, invalid_values in cases.items():
            for index, value in enumerate((*invalid_values, None)):
                with self.subTest(field=field, value=value):
                    policy = "\n".join(
                        line if not line.startswith(field + " =") else f"{field} = {value}"
                        for line in defaults.splitlines()
                        if value is not None or not line.startswith(field + " ="))
                    path.write_text(policy)
                    before = snapshot_tree(self.root)
                    result = self.launch(launcher, cwd, "measure", ".", "--output", f"invalid-{field}-{index}.json")
                    self.assertEqual(2, result.returncode, result.stderr)
                    self.assertIn("Invalid settings", result.stderr)
                    self.assertIn(str(path), result.stderr)
                    self.assertIn(field, result.stderr)
                    self.assertNotIn("Measurement: complete", result.stdout)
                    self.assertEqual(before, snapshot_tree(self.root))
        # A custom profile, zero advisory target, subset and empty exclusions are valid.
        path.write_text('profile = "custom"\nchecks = ["complexity"]\n'
                        'complexity_target = 0\nexclude_directories = []\n')
        control = self.launch(launcher, cwd, "measure", "sample.py", "--output", "custom.json")
        self.assertEqual(0, control.returncode, control.stderr)
        report = json.loads((self.root / "custom.json").read_text())
        self.assertEqual("custom", report["profile"])
        self.assertEqual(["complexity"], report["requested_checks"])
        self.assertEqual(0, report["checks"]["complexity"]["values"][0]["target"])
        self.assertEqual([], report["excluded_directories"])

    def test_invalid_target_settings_and_unrelated_root_ruff(self):
        launcher, cwd = self.installed_launcher()
        quality = self.root / ".quality"
        quality.mkdir(exist_ok=True)
        for name, default in metrics.DEFAULT_FILES.items():
            (quality / name).write_bytes(default.read_bytes())
        for name in metrics.DEFAULT_FILES:
            with self.subTest(invalid=name):
                path = quality / name
                valid = path.read_bytes()
                path.write_bytes(b"[invalid TOML")
                result = self.launch(launcher, cwd, "measure", ".")
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn(name, result.stderr)
                self.assertNotIn("Measurement: complete", result.stdout)
                self.assertEqual(b"[invalid TOML", path.read_bytes())
                path.write_bytes(valid)
        self.source.write_text("def f(a,b,c): pass\n")
        for present in (False, True):
            with self.subTest(target_ruff=present):
                ruff = quality / "ruff.toml"
                ruff.unlink(missing_ok=True)
                if present:
                    ruff.write_bytes(metrics.DEFAULT_FILES["ruff.toml"].read_bytes())
                result = self.launch(launcher, cwd, "measure", ".", "--output", f".quality/reports/before-root-{present}.json")
                self.assertEqual(0, result.returncode, result.stderr)
                before = json.loads((quality / f"reports/before-root-{present}.json").read_text())
                unrelated = self.root / "ruff.toml"
                unrelated.write_text('[lint]\nignore = ["ALL"]\n')
                saved = unrelated.read_bytes()
                result = self.launch(launcher, cwd, "measure", ".", "--output", f".quality/reports/root-{present}.json")
                self.assertEqual(0, result.returncode, result.stderr)
                after = json.loads((quality / f"reports/root-{present}.json").read_text())
                self.assertEqual(before["checks"]["ruff"]["values"], after["checks"]["ruff"]["values"])
                self.assertEqual(before["identity"]["settings"], after["identity"]["settings"])
                self.assertEqual(saved, unrelated.read_bytes())
                unrelated.unlink()

    def test_folder_baseline_can_compare_affected_new_and_deleted_files(self):
        untouched = self.root / "untouched.py"
        untouched.write_text(function("legacy", 15))
        baseline = self.report()
        self.source.write_text(function("small", 2))
        added = self.root / "added.py"
        added.write_text(function("added", 0))
        current = metrics.build_report(self.root, ["sample.py", "added.py"], ["complexity", "ruff"])
        result = metrics.comparison(current, baseline)
        self.assertEqual("compared", result["status"])
        self.assertEqual({"small", "added"}, {row["symbol"] for row in result["complexity"]})
        outside = dict(baseline, identity=dict(baseline["identity"], scope=["untouched.py"], scope_directories=[]))
        self.assertEqual("incompatible", metrics.comparison(current, outside)["status"])
        self.source.unlink()
        current = metrics.build_report(self.root, ["sample.py"], ["complexity", "ruff"], baseline=baseline)
        result = metrics.comparison(current, baseline)
        self.assertEqual("complete", current["measurement_status"])
        self.assertEqual(["removed"], [row["classification"] for row in result["complexity"]])

    def test_snapshot_preserves_staged_unstaged_untracked_and_index(self):
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.git("add", ".")
        self.git("commit", "-qm", "initial")
        self.source.write_text(function("small", 2))
        self.git("add", ".")
        index = (self.root / ".git" / "index").read_bytes()
        staged = self.git("show", ":sample.py")
        self.source.write_text(function("small", 3))
        (self.root / "untracked.py").write_text(function("untracked", 0))
        source_before = {p.name: p.read_bytes() for p in self.root.glob("*.py")}
        report = self.report()
        self.assertEqual("complete", report["measurement_status"])
        self.assertEqual(source_before, {p.name: p.read_bytes() for p in self.root.glob("*.py")})
        self.assertEqual(index, (self.root / ".git" / "index").read_bytes())
        self.assertEqual(staged, self.git("show", ":sample.py"))
        self.assertIn("MM sample.py", report["repository"]["status"])
        self.assertIn("?? untracked.py", report["repository"]["status"])
        self.assertEqual(self.source.read_bytes(), base64.b64decode(report["files"]["sample.py"]["source_base64"]))
        self.assertEqual(4, report["checks"]["complexity"]["values"][0]["value"])

        self.assertEqual([4, 1], [row["value"] for row in report["checks"]["complexity"]["values"]])
        for name, data in source_before.items():
            self.assertEqual(data, base64.b64decode(report["files"][name]["source_base64"]))
            self.assertEqual(metrics.digest(data), report["files"][name]["sha256"])
        baseline = self.root / "before.json"
        baseline.write_text(json.dumps(report))
        baseline.with_suffix(".txt").write_text("preserved summary\n")
        saved = {p: p.read_bytes() for p in (baseline, baseline.with_suffix(".txt"))}
        self.source.write_text(function("small", 4))
        source_after = {p.name: p.read_bytes() for p in self.root.glob("*.py")}
        result = subprocess.run([sys.executable, str(ROOT / "scripts/measure_maintainability.py"),
                                 "compare", "sample.py", "--root", str(self.root), "--baseline", str(baseline), "--output", "after.json"], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        after = json.loads((self.root / "after.json").read_text())
        row, = after["comparison"]["complexity"]
        self.assertEqual((4, 5, 1), tuple(row[key] for key in ("before", "value", "delta")))
        self.assertEqual(saved, {p: p.read_bytes() for p in saved})
        self.assertEqual(source_after, {p.name: p.read_bytes() for p in self.root.glob("*.py")})
        self.assertEqual(index, (self.root / ".git/index").read_bytes())
        self.assertEqual(staged, self.git("show", ":sample.py"))

    def test_partial_completion_missing_tool_and_invalid_python(self):
        version = metrics.tool_version
        with patch.object(metrics, "tool_version", side_effect=lambda name: None if name == "ruff" else version(name)):
            report = self.report()
            with redirect_stdout(io.StringIO()):
                self.assertEqual(2, metrics.main(["measure", ".", "--root", str(self.root)]))
        self.assertEqual("incomplete", report["measurement_status"])
        self.assertEqual("completed", report["checks"]["complexity"]["status"])
        self.assertEqual("unavailable", report["checks"]["ruff"]["status"])
        self.source.write_text("def broken(:\n")
        report = self.report()
        self.assertEqual("incomplete", report["measurement_status"])
        self.assertEqual("failed", report["checks"]["complexity"]["status"])
        self.assertEqual("failed", report["checks"]["ruff"]["status"])
        report["comparison"] = metrics.comparison(report, None)
        report["highlights"] = []
        self.assertIn("invalid syntax", metrics.summarize(report))
        result = self.launch(ROOT / "scripts/measure_maintainability.py", self.root, "measure", ".")
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertIn("Measurement: incomplete", result.stdout)

    def test_concurrent_input_change_marks_results_incomplete(self):
        measure = metrics.measure

        def change_during_measurement(*args):
            self.source.write_text(function("small", 5))
            return measure(*args)

        with patch.object(metrics, "measure", side_effect=change_during_measurement):
            report = self.report()
            self.source.write_text(function("small", 1))
            with redirect_stdout(io.StringIO()):
                self.assertEqual(2, metrics.main(["measure", ".", "--root", str(self.root)]))
        self.assertEqual("incomplete", report["measurement_status"])
        self.assertIn("Source inputs changed", report["errors"][0])
        self.assertEqual(2, report["checks"]["complexity"]["values"][0]["value"])

    def test_cli_file_scope_baseline_comparison_and_no_overwrite(self):
        baseline_path = self.root / "before.json"
        output = self.root / "after.json"
        args = [sys.executable, str(ROOT / "scripts" / "measure_maintainability.py")]
        console = subprocess.run([*args, "measure", "sample.py", "--root", str(self.root)],
                                 capture_output=True, text=True)
        self.assertEqual(0, console.returncode, console.stderr)
        self.assertIn("Measurement: complete", console.stdout)
        self.assertIn("CC 2: sample.py:1 small", console.stdout)
        self.assertIn("Top five by complexity:", console.stdout)
        self.assertNotIn("Response required:", console.stdout)
        self.assertNotIn("Changed symbols", console.stdout)
        self.assertNotIn("Report:", console.stdout)
        self.assertEqual([self.source], list(self.root.iterdir()))
        missing_output = subprocess.run([*args, "baseline", "sample.py", "--root", str(self.root)],
                                        capture_output=True, text=True)
        self.assertEqual(2, missing_output.returncode)
        self.assertIn("baseline requires --output", missing_output.stderr)
        first = subprocess.run([*args, "baseline", "sample.py", "--root", str(self.root),
                                "--output", str(baseline_path)], capture_output=True, text=True)
        self.assertEqual(0, first.returncode, first.stderr)
        self.source.write_text(function("small", 2))
        second = subprocess.run([*args, "compare", "sample.py", "--root", str(self.root),
                                 "--baseline", str(baseline_path), "--output", str(output)], capture_output=True, text=True)
        self.assertEqual(0, second.returncode, second.stderr)
        report = json.loads(output.read_text())
        self.assertNotIn("required_response", report)
        self.assertEqual(2, len(report["highlights"]))
        self.assertIn("Highlights: 2", output.with_suffix(".txt").read_text())
        files_before = set(self.root.iterdir())
        console_compare = subprocess.run([*args, "compare", "sample.py", "--root", str(self.root),
                                         "--baseline", str(baseline_path)], capture_output=True, text=True)
        self.assertEqual(0, console_compare.returncode, console_compare.stderr)
        self.assertIn("Highlights: 2", console_compare.stdout)
        self.assertIn("  Got worse: CC 2->3 (+1): sample.py:1 small [implementation]",
                      console_compare.stdout)
        self.assertIn("  Got worse: PLR0915 2->4 (+2): sample.py:1 small [implementation]",
                      console_compare.stdout)
        self.assertEqual(files_before, set(self.root.iterdir()))
        for operation, destination in (("baseline", baseline_path), ("compare", output),
                                       ("baseline", self.root / "sibling.json"), ("compare", self.root / "sibling.json")):
            with self.subTest(operation=operation, destination=destination.name):
                destination.with_suffix(".txt").write_text("preserve summary\n")
                saved = {p: p.read_bytes() for p in self.root.iterdir() if p.is_file()}
                extra = ["--baseline", str(baseline_path)] if operation == "compare" else []
                retry = subprocess.run([*args, operation, "sample.py", "--root", str(self.root),
                                        "--output", str(destination), *extra], capture_output=True, text=True)
                self.assertEqual(2, retry.returncode)
                self.assertIn("already exists", retry.stderr)
                self.assertEqual(saved, {p: p.read_bytes() for p in self.root.iterdir() if p.is_file()})

    def test_console_compare_prints_identities_and_deltas_before_top_five(self):
        baseline_path = self.root / "console-baseline.json"
        args = [sys.executable, str(ROOT / "scripts" / "measure_maintainability.py")]
        self.source.write_text(function("target", 15))
        baseline = subprocess.run([*args, "baseline", "sample.py", "--root", str(self.root),
                                   "--output", str(baseline_path)], capture_output=True, text=True)
        self.assertEqual(0, baseline.returncode, baseline.stderr)
        self.source.write_text(function("target", 1) + function("helper", 1) + function("hotspot", 10)
                               + "def wide(a,b,c,d,e,f): pass\n")
        console = subprocess.run([*args, "compare", "sample.py", "--root", str(self.root),
                                  "--baseline", str(baseline_path)], capture_output=True, text=True)
        self.assertEqual(0, console.returncode, console.stderr)
        self.assertIn("Highlights: 11\n", console.stdout)
        self.assertIn("  Improved: CC 16->2 (-14): sample.py:1 target [implementation]\n", console.stdout)
        self.assertIn("Needs interpretation: CC 2: sample.py:4 helper [implementation]\n", console.stdout)
        self.assertIn("New above threshold, needs interpretation: CC 11: sample.py:7 hotspot [implementation]\n", console.stdout)
        self.assertIn("Needs interpretation: CC 1: sample.py:19 wide [implementation]\n", console.stdout)
        self.assertIn("Above threshold, needs interpretation: PLR0913 6: sample.py:19 wide [implementation]\n", console.stdout)
        self.assertIn("Improved: PLR0915 30->2 (-28): sample.py:1 target [implementation]\n", console.stdout)
        self.assertIn("Needs interpretation: PLR0915 2: sample.py:4 helper [implementation]\n", console.stdout)
        self.assertIn("Top five by complexity:", console.stdout)
        self.assertLess(console.stdout.index("Improved:"), console.stdout.index("Top five by complexity:"))

    def test_standalone_measurement_prints_ruff_findings(self):
        self.source.write_text("def wide(a,b,c,d,e,f): pass\n")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/measure_maintainability.py"),
                                 "measure", "sample.py", "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Above threshold: PLR0913 6: sample.py:1 wide", result.stdout)

    def test_directory_exclusions_selected_check_and_empty_scope(self):
        excluded = self.root / ".agents"
        excluded.mkdir()
        (excluded / "invalid.py").write_text("def invalid(:")
        report = self.report(("complexity",))
        self.assertEqual("complete", report["measurement_status"])
        self.assertFalse(report["full_profile"])
        self.assertEqual([".agents"], report["skipped_paths"])
        self.assertEqual(["sample.py"], list(report["files"]))
        for name in ("tests/test_sample.py", "evals/fixture.py", "nested/.venv/invalid.py"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("def invalid(:" if ".venv" in name else function("asset", 0))
        report = self.report(("complexity",))
        self.assertEqual({"implementation", "test", "eval_or_harness"}, {row["asset_group"] for row in report["files"].values()})
        self.assertIn("nested/.venv", report["skipped_paths"])
        launcher = ROOT / "scripts/measure_maintainability.py"
        result = self.launch(launcher, self.root, "measure", str(self.source), "--checks", "complexity", "--output", "partial.json")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(json.loads((self.root / "partial.json").read_text())["full_profile"])
        link = self.root / "link.py"
        link.symlink_to(self.source)
        for scope in ("../outside.py", "link.py", ".agents"):
            with self.subTest(scope=scope):
                result = self.launch(launcher, self.root, "measure", scope)
                self.assertEqual(2, result.returncode)
                self.assertIn("Measurement error", result.stderr)
        link.unlink()
        shutil.rmtree(self.root / "tests")
        shutil.rmtree(self.root / "evals")
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, "no included Python"):
            self.report()


class LauncherTests(unittest.TestCase):
    def test_environment_key_separates_native_runtimes_and_dependency_versions(self):
        original = environment.environment_path()
        for name, value in (("system", "OtherOS"), ("machine", "OtherCPU"),
                            ("python_version", ".".join([*environment.platform.python_version().split(".")[:2], "999"]))):
            with self.subTest(name=name), patch.object(environment.platform, name, return_value=value):
                self.assertNotEqual(original, environment.environment_path())
        with patch.object(environment.sys, "implementation", type("Runtime", (), {"name": "other"})):
            self.assertNotEqual(original, environment.environment_path())
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            (target / ".quality").mkdir()
            (target / ".quality/requirements.txt").write_text("radon==0.0.0\n")
            self.assertEqual(original.name, environment.environment_path(target).name)
            pins = Path(temporary) / "requirements.txt"
            pins.write_text("radon==0.0.0\n")
            with patch.object(environment, "REQUIREMENTS", pins):
                self.assertNotEqual(original, environment.environment_path())
                self.assertFalse(environment.pins_available())

    def test_missing_pins_recipe_dispatches_setup_for_selected_target(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            root = base / "target with spaces"
            root.mkdir()
            init_repo(root)
            source = root / "app.py"
            source.write_text(function("staged", 1))
            subprocess.run(["git", "-C", str(root), "add", "app.py"], check=True)
            source.write_text(function("dirty", 2))
            (root / "untracked.py").write_text(function("untracked", 0))
            scripts = base / "installation with spaces"
            scripts.mkdir()
            for name in installer.SHARED_SCRIPT_FILES:
                if name.startswith(("maintainability", "measure_maintainability")):
                    shutil.copy(ROOT / "scripts" / name, scripts / name)
            quality = root / ".quality"
            for name in ("venv/bin/python", "envs/ForeignOS/bin/python", "reports/before.json", "reports/before.txt", "requirements.txt", "maintainability.toml"):
                path = quality / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("foreign or user bytes\n")
            before = snapshot_tree(root)
            launcher = scripts / "measure_maintainability.py"
            missing = subprocess.run([sys.executable, "-S", str(launcher), "measure", "--root", str(root)],
                                     cwd=base, capture_output=True, text=True)
            self.assertEqual(2, missing.returncode, missing.stderr)
            self.assertIn("Pinned tools unavailable", missing.stderr)
            recipe = shlex.split(missing.stderr.split("Run: ", 1)[1].strip())
            self.assertEqual([str(launcher), "setup", "--root", str(root.resolve())], recipe[1:])
            self.assertEqual(before, snapshot_tree(root))
            self.assertEqual({p.parent for p in quality.glob("envs/*/bin/python")}, {quality / "envs/ForeignOS/bin"})
            self.assertFalse((scripts / ".quality").exists())
            # Replay the printed setup arguments at the real provisioning seam; no download.
            spec = importlib.util.spec_from_file_location("setup_env", scripts / "maintainability_env.py")
            setup_env = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(setup_env)
            with patch.object(setup_env.venv.EnvBuilder, "create") as create, patch.object(setup_env.subprocess, "run") as install, redirect_stdout(io.StringIO()):
                self.assertEqual(0, setup_env.main(recipe[2:]))
            expected_env = setup_env.environment_path(root.resolve())
            create.assert_called_once_with(expected_env)
            install.assert_called_once_with([str(setup_env.environment_python(expected_env)), "-m", "pip", "install", "-r", str(scripts / "maintainability-requirements.txt")], check=True)
            self.assertEqual(before, snapshot_tree(root))

    @unittest.skipUnless(HAS_TOOLS, "Real pinned dependencies required")
    def test_native_target_environment_reaches_real_adapter(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "sample.py").write_text(function("native", 2))
            native = environment.environment_path(root)
            venv.EnvBuilder(with_pip=False).create(native)
            site = next(native.glob("lib/python*/site-packages")) if os.name != "nt" else native / "Lib/site-packages"
            (site / "prepared-dependencies.pth").write_text(sysconfig.get_path("purelib") + "\n")
            shutil.copy2(Path(sysconfig.get_path("scripts")) / ("ruff.exe" if os.name == "nt" else "ruff"), environment.environment_python(native).parent)
            for foreign in (root / ".quality/venv/bin/python", root / ".quality/envs/ForeignOS/bin/python"):
                foreign.parent.mkdir(parents=True)
                foreign.write_text("foreign binary cannot execute\n")
            result = subprocess.run([sys._base_executable, str(ROOT / "scripts/measure_maintainability.py"),
                                     "measure", "sample.py", "--root", str(root), "--output", ".quality/reports/native.json"],
                                    capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr + result.stdout + (root / ".quality/reports/native.json").read_text())
            report = json.loads((root / ".quality/reports/native.json").read_text())
            self.assertEqual(str(environment.environment_python(native)), report["checks"]["ruff"]["raw"]["command"][0])
            self.assertEqual(3, report["checks"]["complexity"]["values"][0]["value"])
            self.assertEqual({"complexity": "6.0.1", "ruff": "0.14.2"}, report["identity"]["tools"])


if __name__ == "__main__":
    unittest.main()
