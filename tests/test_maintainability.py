import base64
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("maintainability", ROOT / "tools" / "maintainability.py")
metrics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(metrics)
HAS_TOOLS = metrics.tool_version("radon") and metrics.tool_version("ruff")
ENV_SPEC = importlib.util.spec_from_file_location("maintainability_env", ROOT / "tools/maintainability_env.py")
environment = importlib.util.module_from_spec(ENV_SPEC)
ENV_SPEC.loader.exec_module(environment)


def function(name, branches):
    return f"def {name}(value):\n" + "    if value: pass\n" * branches + "    return value\n"


@unittest.skipUnless(HAS_TOOLS, "Run with the Python environment printed by setup; real Radon and Ruff required")
class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "sample.py"
        self.source.write_text(function("small", 1))

    def report(self, checks=("complexity", "ruff")):
        return metrics.build_report(self.root, ["."], list(checks))

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True, text=True).stdout

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

    def test_ruff_configured_targets_are_separate_from_collection_limits(self):
        self.source.write_text("def f(a,b,c): pass\n")
        with tempfile.TemporaryDirectory() as temporary:
            quality = Path(temporary)
            shutil.copy(metrics.QUALITY / "maintainability.toml", quality)
            (quality / "ruff.toml").write_text((metrics.QUALITY / "ruff.toml").read_text()
                                              .replace("max-args = 5", "max-args = 2")
                                              .replace("max-statements = 50", "max-statements = 3"))
            with patch.object(metrics, "QUALITY", quality):
                report = self.report(("ruff",))
        self.assertEqual([(3, 2, 0), (1, 3, 0)],
                         [(row["value"], row["target"], row["collection_threshold"])
                          for row in report["checks"]["ruff"]["values"]])

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
        report = self.report()
        self.assertEqual("complete", report["measurement_status"])
        self.assertEqual(index, (self.root / ".git" / "index").read_bytes())
        self.assertEqual(staged, self.git("show", ":sample.py"))
        self.assertIn("MM sample.py", report["repository"]["status"])
        self.assertIn("?? untracked.py", report["repository"]["status"])
        self.assertEqual(self.source.read_bytes(), base64.b64decode(report["files"]["sample.py"]["source_base64"]))
        self.assertEqual(4, report["checks"]["complexity"]["values"][0]["value"])

    def test_partial_completion_missing_tool_and_invalid_python(self):
        version = metrics.tool_version
        with patch.object(metrics, "tool_version", side_effect=lambda name: None if name == "ruff" else version(name)):
            report = self.report()
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

    def test_concurrent_input_change_marks_results_incomplete(self):
        measure = metrics.measure

        def change_during_measurement(*args):
            self.source.write_text(function("small", 5))
            return measure(*args)

        with patch.object(metrics, "measure", side_effect=change_during_measurement):
            report = self.report()
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
        before = baseline_path.read_bytes()
        retry = subprocess.run([*args, "baseline", "sample.py", "--root", str(self.root),
                                "--output", str(baseline_path)], capture_output=True, text=True)
        self.assertEqual(2, retry.returncode)
        self.assertEqual(before, baseline_path.read_bytes())

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
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, "no included Python"):
            self.report()


class LauncherTests(unittest.TestCase):
    def test_environment_key_separates_native_runtimes_and_dependency_versions(self):
        original = environment.environment_path()
        for name, value in (("system", "OtherOS"), ("machine", "OtherCPU"),
                            ("python_version", "3.99.0")):
            with self.subTest(name=name), patch.object(environment.platform, name, return_value=value):
                self.assertNotEqual(original, environment.environment_path())
        with tempfile.TemporaryDirectory() as temporary:
            pins = Path(temporary) / "requirements.txt"
            pins.write_text("radon==0.0.0\n")
            with patch.object(environment, "REQUIREMENTS", pins):
                self.assertNotEqual(original, environment.environment_path())
                self.assertFalse(environment.pins_available())

    def test_foreign_legacy_venv_is_not_executed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            (root / "tools").mkdir()
            shutil.copy(ROOT / "scripts/measure_maintainability.py", root / "scripts")
            shutil.copy(ROOT / "tools/maintainability_env.py", root / "tools")
            shutil.copytree(ROOT / ".quality", root / ".quality",
                            ignore=shutil.ignore_patterns("venv", "envs", "reports"))
            foreign = root / ".quality/venv/bin/python"
            foreign.parent.mkdir(parents=True)
            foreign.write_text("foreign binary, cannot execute on this OS")
            (root / "tools/maintainability.py").write_text("print('adapter reached')\n")
            result = subprocess.run([sys.executable, str(root / "scripts/measure_maintainability.py"), "--help"],
                                    capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("adapter reached", result.stdout)
            missing = subprocess.run([sys.executable, "-S", str(root / "scripts/measure_maintainability.py"), "measure"],
                                     capture_output=True, text=True)
            self.assertEqual(2, missing.returncode, missing.stderr)
            self.assertIn("setup", missing.stderr)
            self.assertNotIn("adapter reached", missing.stdout)
            self.assertFalse((root / ".quality/envs").exists())


if __name__ == "__main__":
    unittest.main()
