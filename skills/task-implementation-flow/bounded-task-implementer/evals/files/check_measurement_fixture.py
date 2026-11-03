"""Check supplied states and real CLI boundaries; does not execute an agent."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import measurement_fixture as cases
import setup_fixture as fixture


class MeasurementFixtureTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        fixture.WORK = Path(temporary.name)
        fixture.RUNS = fixture.WORK / "task-runs"
        fixture.SCHEMA = fixture.WORK / "contracts/worker-result.schema.json"
        fixture.RUNS.mkdir()

    def test_source_hash_mismatch_preserves_status_and_other_entry_facts(self):
        case = next(case for case in cases.CASES if case["id"] == "V-01d")
        root = fixture.WORK / "measurement-fixture"
        cases.basic(root, case)
        status = fixture.git(root, "status", "--short")
        before = cases.snapshot(root)
        cases.change_start(root, case)
        after = cases.snapshot(root)
        self.assertEqual(status, fixture.git(root, "status", "--short"))
        self.assertEqual(before["source"].keys(), after["source"].keys())
        self.assertNotEqual(before["source"]["src/logic.py"], after["source"]["src/logic.py"])
        self.assertEqual(before["index"], after["index"])
        self.assertEqual(before["reports"], after["reports"])

    def test_finite_inputs_and_metric_oracles(self):
        for case in cases.CASES:
            with self.subTest(case=case["id"]):
                cases.prepare(case["id"])
                scenario = case["scenario"]
                if scenario in ("V-01b", "V-01h"):
                    root = fixture.WORK / "queue-runner"
                    packet = (root / "docs/tasks/QR-12/preflight.md").read_text()
                    index = subprocess.check_output(["git", "-C", str(root), "show", ":notes/local.md"])
                    self.assertEqual(scenario == "V-01b", f"Index SHA-256: {fixture.sha(index)}" in packet)
                    self.assertIn(cases.BASE, packet)
                    continue
                if scenario in ("V-10a", "V-10b"):
                    continue  # Existing refusal/provenance fixtures, unchanged.
                root = fixture.WORK / ("result-record" if scenario == "V-06" else "measurement-fixture")
                control = json.loads((root / "fixture-snapshot.json").read_text())
                self.assertEqual(cases.snapshot(root), control)
                if scenario == "V-06":
                    self.assertIn("ROW-REMOTE-ANCHOR", (root / "docs/tasks/REC-44/reviews/acceptance-01.md").read_text())
                    self.assertTrue((root / ".quality/reports/C1.txt").is_file())
                    continue
                self.assertEqual(case["id"], json.loads((root / "oracle.json").read_text())["id"])
                if scenario == "V-05a":
                    self.assertFalse((root / cases.BASE).exists())
                    continue
                before = json.loads((root / cases.BASE).read_text())
                self.assertEqual(set(cases.SCOPES), set(before["identity"]["scope_directories"]))
                if scenario == "V-01d":
                    self.assertNotEqual(before["files"]["src/logic.py"]["sha256"], fixture.file_sha(root / "src/logic.py"))
                if scenario == "V-01e":
                    if case["variant"] == "removed":
                        self.assertIn("src/deleted.py", before["files"])
                        self.assertFalse((root / "src/deleted.py").exists())
                    else:
                        self.assertNotIn("src/unexpected.py", before["files"])
                        self.assertTrue((root / "src/unexpected.py").is_file())
                if scenario == "V-02a":
                    self.assertIn("harness/untracked.py", before["files"])
                    self.assertEqual(fixture.file_sha(root / "src/user.py"), before["files"]["src/user.py"]["sha256"])
                    self.assertNotEqual(subprocess.check_output(["git", "-C", str(root), "show", ":src/user.py"]), (root / "src/user.py").read_bytes())
                if scenario in ("V-02c", "V-02d", "V-05f", "V-09d"):
                    self.assertFalse((root / ".agents/scripts/measure_maintainability.py").exists())
                if scenario in ("V-09b", "V-09c"):
                    self.assertFalse((root / ".agents/scripts/run_evidence.py").exists())
                if scenario.startswith("V-04") and scenario[-1] in "abcdefghik":
                    path = root / "src/logic.py"
                    original = path.read_bytes()
                    path.write_bytes((root / "inputs/desired.txt").read_bytes())
                    state = cases.snapshot(root)
                    cases.measure(root, "compare", ["src/logic.py"], ".quality/reports/probe.json", cases.BASE)
                    after = json.loads((root / ".quality/reports/probe.json").read_text())
                    self.assertEqual("complete", after["measurement_status"])
                    metric = case["variant"]
                    key, name = {"statements": ("ruff", "PLR0915"), "arguments": ("ruff", "PLR0913")}.get(metric, ("complexity", "cyclomatic_complexity"))
                    records = [row for row in after["checks"][key]["values"] if row["symbol"] == "active" and row["metric"] == name]
                    self.assertEqual(1, len(records))
                    expected = {"a": 8, "b": 10, "c": 11, "d": 11, "e": 12, "f": 11, "g": 11, "h": 10, "i": 8, "k": 12}[scenario[-1]]
                    self.assertEqual(expected + {"statements": 40, "arguments": -5}.get(metric, 0), records[0]["value"])
                    self.assertEqual(state["source"], cases.snapshot(root)["source"])
                    self.assertEqual(state["index"], cases.snapshot(root)["index"])
                    for name, digest in state["reports"].items():
                        self.assertEqual(digest, fixture.file_sha(root / name))
                    path.write_bytes(original)
                if scenario in ("V-08h", "V-08i", "V-08j"):
                    history = [json.loads(line) for line in (root / ".quality/reports/native-history.jsonl").read_text().splitlines()]
                    self.assertEqual([0, 1], [row["exit_code"] for row in history])
                    self.assertIn("outside/control.py", history[-1]["checked_bytes"])
                    if scenario == "V-08j":
                        fixture.write(root, "outside/control.py", "VALUE = 1")
                        cases.run(root, cases.PYTHON, "tools/native.py")
                        latest = json.loads((root / ".quality/reports/native-history.jsonl").read_text().splitlines()[-1])
                        self.assertEqual(0, latest["exit_code"])
                        self.assertNotEqual(latest["checked_bytes"], history[-1]["checked_bytes"])
                if scenario in ("V-08d", "V-08e", "V-08f"):
                    aggregate = json.loads((root / ".quality/reports/aggregate.json").read_text())
                    if scenario == "V-08e":
                        self.assertEqual([], aggregate["constituents"])
                    else:
                        checked = aggregate["constituents"][0]["checked_bytes"]
                        matching = all(fixture.file_sha(root / path) == digest for path, digest in checked.items())
                        self.assertEqual(scenario == "V-08d", matching)
                        self.assertEqual(1, len((root / ".quality/reports/native-history.jsonl").read_text().splitlines()))


if __name__ == "__main__":
    unittest.main()
