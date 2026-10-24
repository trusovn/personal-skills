import base64
import importlib.util
import json
from pathlib import Path
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


def function(name, branches):
    return f"def {name}(value):\n" + "    if value: pass\n" * branches + "    return value\n"


@unittest.skipUnless(HAS_TOOLS, "Run with .quality/venv/bin/python; real Radon and Ruff required")
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
        self.assertEqual((2, 3, 1, True), tuple(rows["small"][key] for key in ("before", "value", "delta", "requires_response")))
        self.assertEqual("unchanged", rows["legacy"]["classification"])
        self.assertFalse(rows["legacy"]["requires_response"])
        self.assertEqual("improved", rows["improves"]["classification"])
        self.assertEqual("new", rows["new_hotspot"]["classification"])
        self.assertTrue(rows["new_hotspot"]["requires_response"])

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

    def test_renamed_or_extracted_symbols_remain_unmatched(self):
        baseline = self.report()
        self.source.write_text(function("renamed", 1) + function("extracted", 0))
        rows = metrics.comparison(self.report(), baseline)["complexity"]
        self.assertEqual({"small", "renamed", "extracted"}, {item["symbol"] for item in rows})
        self.assertTrue(all(item["classification"] == "unmatched" and item["requires_response"] for item in rows))

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
        findings = report["checks"]["ruff"]["values"]
        self.assertEqual(["PLR0913", "PLR0915"], [item["code"] for item in findings])
        self.assertEqual([3, 7], [item["line"] for item in findings])
        self.assertIn("6 > 5", findings[0]["message"])
        self.assertIn("51 > 50", findings[1]["message"])
        self.assertIn("unavailable", " ".join(report["limitations"]))

    def test_incompatible_scope_tool_configuration_and_failed_baseline(self):
        baseline = self.report()
        for change in ("scope", "tools", "ruff_config", "adapter_sha256"):
            with self.subTest(change=change):
                changed = json.loads(json.dumps(baseline))
                changed["identity"][change] = "different"
                self.assertEqual("incompatible", metrics.comparison(self.report(), changed)["status"])
        baseline["measurement_status"] = "incomplete"
        self.assertEqual("incompatible", metrics.comparison(self.report(), baseline)["status"])

    def test_identical_ruff_messages_on_new_symbols_remain_new_diagnostics(self):
        self.source.write_text("def existing(a,b,c,d,e,f): pass\n")
        baseline = self.report()
        self.source.write_text("\n\ndef existing(a,b,c,d,e,f): pass\n"
                               "def added(a,b,c,d,e,f): pass\n")
        findings = metrics.comparison(self.report(), baseline)["ruff"]
        self.assertEqual(["existing_diagnostic", "new_diagnostic"], [item["classification"] for item in findings])
        self.assertEqual([False, True], [item["requires_response"] for item in findings])

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
        self.assertEqual(1, len(report["required_response"]))
        self.assertIn("Required response items: 1", output.with_suffix(".txt").read_text())
        files_before = set(self.root.iterdir())
        console_compare = subprocess.run([*args, "compare", "sample.py", "--root", str(self.root),
                                         "--baseline", str(baseline_path)], capture_output=True, text=True)
        self.assertEqual(0, console_compare.returncode, console_compare.stderr)
        self.assertIn("Required response items: 1", console_compare.stdout)
        self.assertIn("  Response required: worsened CC 2->3 (+1): sample.py:1 small [implementation]",
                      console_compare.stdout)
        self.assertIn("Changed symbols: 1", console_compare.stdout)
        self.assertIn("  Worsened CC 2->3 (+1): sample.py:1 small [implementation]", console_compare.stdout)
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
        self.assertIn("Required response items: 2\n", console.stdout)
        self.assertIn("  Response required: new CC 11: sample.py:7 hotspot [implementation]\n", console.stdout)
        self.assertIn("  Response required: new_diagnostic PLR0913 Too many arguments in function "
                      "definition (6 > 5): sample.py:19 wide [implementation]\n", console.stdout)
        self.assertIn("Changed symbols: 4\n", console.stdout)
        self.assertIn("  Improved CC 16->2 (-14): sample.py:1 target [implementation]\n", console.stdout)
        self.assertIn("  New CC 2: sample.py:4 helper [implementation]\n", console.stdout)
        self.assertIn("  New CC 11: sample.py:7 hotspot [implementation]\n", console.stdout)
        self.assertIn("  New CC 1: sample.py:19 wide [implementation]\n", console.stdout)
        self.assertIn("Top five by complexity:", console.stdout)
        self.assertLess(console.stdout.index("Response required:"), console.stdout.index("Top five by complexity:"))
        self.assertLess(console.stdout.index("Changed symbols:"), console.stdout.index("Top five by complexity:"))

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


if __name__ == "__main__":
    unittest.main()
