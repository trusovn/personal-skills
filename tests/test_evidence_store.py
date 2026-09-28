import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "evidence_store.py"
SPEC = importlib.util.spec_from_file_location("evidence_store", MODULE_PATH)
evidence_store = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(evidence_store)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout


class GitMetadataEvidenceStoreTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)
        git(self.repo, "init", "-q")
        self.store = evidence_store.GitMetadataEvidenceStore(self.repo)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_root_is_under_absolute_git_directory(self):
        git_dir = Path(git(self.repo, "rev-parse", "--absolute-git-dir").strip())
        self.assertEqual(git_dir / "personal-skills" / "evidence" / "v2", self.store.root)
        self.assertFalse(self.store.root.is_relative_to(self.repo))

    def test_blobs_are_content_addressed_and_idempotent(self):
        blob_ref = self.store.put_blob(b"artifact bytes")
        self.assertEqual(blob_ref, self.store.put_blob(b"artifact bytes"))
        self.assertNotEqual(blob_ref, self.store.put_blob(b"changed bytes"))
        digest = blob_ref.removeprefix("sha256:")
        self.assertEqual(
            b"artifact bytes",
            (self.store.root / "blobs" / "sha256" / digest[:2] / digest).read_bytes(),
        )
        self.assertTrue(self.store.record_exists("blob", blob_ref))
        self.assertEqual(b"artifact bytes", self.store.get_record("blob", blob_ref))

    def test_immutable_namespaces_are_isolated_and_conflicts_preserve_value(self):
        cases = (
            ("project_snapshot", "same-id", {"kind": "project"}),
            ("task_revision", ("same-id", "r1"), {"kind": "task"}),
            ("association", ("same-id", "a1"), {"kind": "association"}),
        )
        for namespace, record_id, value in cases:
            with self.subTest(namespace=namespace):
                self.store.put_immutable_record(namespace, record_id, value)
                self.store.put_immutable_record(namespace, record_id, dict(value))
                self.assertTrue(self.store.record_exists(namespace, record_id))
                self.assertEqual(value, self.store.get_record(namespace, record_id))
                with self.assertRaises(evidence_store.EvidenceStoreError):
                    self.store.put_immutable_record(namespace, record_id, {"kind": "changed"})
                self.assertEqual(value, self.store.get_record(namespace, record_id))

        self.assertEqual({"kind": "project"}, self.store.get_record("project_snapshot", "same-id"))
        self.assertIsNone(self.store.get_record("attempt", "same-id"))
        self.assertFalse(self.store.record_exists("attempt", "same-id"))

    def test_attempt_lifecycle_is_one_way_and_ids_are_independent(self):
        self.store.create_attempt("attempt-one", {"state": "created"})
        self.store.create_attempt("attempt-two", {"state": "created"})
        with self.assertRaises(evidence_store.EvidenceStoreError):
            self.store.create_attempt("attempt-one", {"state": "different"})

        self.store.update_active_attempt("attempt-one", {"state": "updated"})
        self.store.finalize_attempt("attempt-one", {"state": "final"})
        self.assertEqual({"state": "final"}, self.store.get_record("attempt", "attempt-one"))
        self.store.update_active_attempt("attempt-two", {"state": "still-active"})
        self.assertEqual({"state": "still-active"}, self.store.get_record("attempt", "attempt-two"))

        for operation, value in (
            (self.store.update_active_attempt, {"state": "late"}),
            (self.store.finalize_attempt, {"state": "final"}),
        ):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(evidence_store.EvidenceStoreError):
                    operation("attempt-one", value)
                self.assertEqual({"state": "final"}, self.store.get_record("attempt", "attempt-one"))

    def test_atomic_write_failure_leaves_prior_or_new_target_unexposed(self):
        self.store.create_attempt("attempt", {"state": "old"})
        attempt_path = self.store.root / "attempts" / "attempt" / "attempt.json"
        original = attempt_path.read_bytes()
        with mock.patch.object(evidence_store.os, "replace", side_effect=OSError("forced")):
            with self.assertRaises(OSError):
                self.store.update_active_attempt("attempt", {"state": "new"})
            with self.assertRaises(OSError):
                self.store.put_immutable_record("project_snapshot", "new", {"value": 1})
        self.assertEqual(original, attempt_path.read_bytes())
        self.assertFalse((self.store.root / "project" / "snapshots" / "new.json").exists())
        self.assertEqual(
            {"finalized": False, "value": {"state": "old"}}, json.loads(original)
        )


if __name__ == "__main__":
    unittest.main()
