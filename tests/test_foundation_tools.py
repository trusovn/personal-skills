"""Exercise the repository gates with disposable inputs, never live providers."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify.py"
CHECK_CONTRACTS = ROOT / "tools" / "check_contracts.py"


class VerificationTests(unittest.TestCase):
    def test_discovery_failure_and_skips_cross_real_subprocesses(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory in ("tests", "skills/sample/tests", "skills/sample/evals/fixtures"):
                suite = root / directory
                suite.mkdir(parents=True)
                (suite / "test_sample.py").write_text(
                    'import unittest\nclass Example(unittest.TestCase):\n'
                    '    @unittest.skip("optional tool unavailable")\n'
                    '    def test_optional(self): pass\n'
                )
            (root / "tools").mkdir()
            (root / "tools/check_contracts.py").write_text("raise SystemExit(0)\n")
            spec = importlib.util.spec_from_file_location("verify", VERIFY)
            verify = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(verify)
            self.assertEqual(
                ["skills/sample/tests", "tests"],
                [path.relative_to(root).as_posix() for path in verify.test_roots(root)],
            )
            def run():
                return subprocess.run(
                    [sys.executable, str(VERIFY), "--root", str(root)],
                    capture_output=True, text=True, check=False,
                )
            passed = run()
            self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
            self.assertIn("optional tool unavailable", passed.stderr)
            self.assertIn("3 checks, 0 failed", passed.stdout)
            (root / "skills/sample/tests/test_sample.py").write_text(
                'import unittest\nclass Broken(unittest.TestCase):\n'
                '    def test_failure(self): self.fail("sentinel failure")\n'
            )
            failed = run()
            self.assertNotEqual(0, failed.returncode)
            self.assertIn("sentinel failure", failed.stderr)
            self.assertIn("3 checks, 1 failed", failed.stdout)

    def test_empty_scope_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [sys.executable, str(VERIFY), "--root", temporary],
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("no test suites", result.stderr)


class ContractRegistryTests(unittest.TestCase):
    def test_plan_scoped_identity(self):
        for validator in (CHECK_CONTRACTS, ROOT / "skills/repo-foundation/scripts/check_contracts.py"):
            with self.subTest(validator=validator), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                contracts = root / "docs/contracts"
                contracts.mkdir(parents=True)
                for plan in ("first.md", "second.md"):
                    (root / plan).write_text("# Plan\n")
                def save(sid, ref):
                    (contracts / f"{sid}.json").write_text(json.dumps({
                        "schema_version": 1, "id": sid, "owner_paths": ["first.md"],
                        "provides": [{"name": "actor", "kind": "cli", "plan_refs": [ref]}],
                    }))
                def run():
                    return subprocess.run([sys.executable, str(validator), "--root", str(root),
                                           "--write-index"], capture_output=True, text=True)
                save("first", {"plan": "first.md", "id": "IF-002"})
                save("second", {"plan": "second.md", "id": "IF-002"})
                save("legacy", "IF-002")
                result = run()
                self.assertEqual(0, result.returncode, result.stderr)
                index = (contracts / "index.json").read_bytes()
                self.assertEqual({"first.md#IF-002": ["first"], "second.md#IF-002": ["second"],
                                  "IF-002": ["legacy"]}, json.loads(index)["plan_refs"])
                self.assertEqual(0, run().returncode)
                self.assertEqual(index, (contracts / "index.json").read_bytes())
                for ref, message in (
                    ({"plan": "first.md", "id": "IF-002"}, "mapped to multiple subsystems"),
                    ({"plan": "missing.md", "id": "IF-002"}, "path does not exist"),
                    ({"plan": "../escape.md", "id": "IF-002"}, "canonical"),
                    ({"plan": "./first.md", "id": "IF-002"}, "canonical"),
                    ({"plan": "first.md", "id": "bad"}, "invalid stable ID"),
                    ({"id": "IF-002"}, "plan"),
                ):
                    save("second", ref)
                    rejected = run()
                    self.assertNotEqual(0, rejected.returncode)
                    self.assertIn(message, rejected.stderr)
                    self.assertEqual(index, (contracts / "index.json").read_bytes())

    def test_generated_index_and_broken_reference_failures(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contracts = root / "docs/contracts"
            contracts.mkdir(parents=True)
            (root / "runtime.py").write_text("# declaration\n")
            record = {
                "schema_version": 1, "id": "runtime", "owner_paths": ["runtime.py"],
                "provides": [{"name": "runner", "kind": "cli", "declarations": ["runtime.py"]}],
            }
            record_path = contracts / "runtime.json"
            record_path.write_text(json.dumps(record))
            def run(*args):
                return subprocess.run(
                    [sys.executable, str(CHECK_CONTRACTS), "--root", str(root), *args],
                    capture_output=True, text=True, check=False,
                )
            generated = run("--write-index")
            self.assertEqual(0, generated.returncode, generated.stderr)
            index = (contracts / "index.json").read_bytes()
            self.assertEqual(0, run().returncode)
            self.assertEqual(0, run("--write-index").returncode)
            self.assertEqual(index, (contracts / "index.json").read_bytes())
            record["provides"][0]["declarations"] = ["missing.py"]
            record_path.write_text(json.dumps(record))
            rejected = run("--write-index")
            self.assertNotEqual(0, rejected.returncode)
            self.assertIn("path does not exist: missing.py", rejected.stderr)
            self.assertEqual(index, (contracts / "index.json").read_bytes())
            record["provides"][0]["declarations"] = ["runtime.py"]
            record["id"] = "renamed"
            record_path.write_text(json.dumps(record))
            stale = run()
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("stale or non-canonical", stale.stderr)


if __name__ == "__main__":
    unittest.main()
