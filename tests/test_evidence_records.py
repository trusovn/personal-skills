import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts.evidence_records import (
    EvidenceRecordError,
    ProjectSnapshot,
    capture_artifact,
    create_project_snapshot,
    validate_project_snapshot,
)
from scripts.evidence_store import EvidenceStoreError, GitMetadataEvidenceStore


class EvidenceRecordsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        (self.repo / ".git").mkdir()
        import subprocess
        subprocess.run(["git", "-C", str(self.repo), "init", "-q"], check=True)
        self.store = GitMetadataEvidenceStore(self.repo)

    def tearDown(self):
        self.temp.cleanup()

    def test_capture_recovers_exact_bytes_and_reuses_content(self):
        first = capture_artifact(self.store, "plan", data=b"{}\n")
        source = self.repo / "elsewhere" / "renamed.json"
        source.parent.mkdir()
        source.write_bytes(b"{}\n")
        second = capture_artifact(self.store, "plan", source_path=source)
        self.assertEqual(first, second)
        self.assertEqual(b"{}\n", self.store.get_record("blob", first["content_ref"]))
        self.assertNotIn(str(source), json.dumps(first))

    def test_identity_is_canonical_but_paths_and_key_order_are_irrelevant(self):
        ref = self.store.put_blob(b"a")
        a = ProjectSnapshot.create([{"content_ref": ref, "logical_name": "a"}])
        b = ProjectSnapshot.create([{"logical_name": "a", "content_ref": ref}])
        self.assertEqual(a.id, b.id)
        self.assertEqual(a.record, b.record)

    def test_identity_preserves_order_and_semantic_changes(self):
        one = self.store.put_blob(b"1")
        two = self.store.put_blob(b"2")
        base = ProjectSnapshot.create([
            {"logical_name": "one", "content_ref": one},
            {"logical_name": "two", "content_ref": two},
        ])
        self.assertNotEqual(base.id, ProjectSnapshot.create(list(reversed(base.record["artifacts"]))).id)
        self.assertNotEqual(base.id, ProjectSnapshot.create([{**base.record["artifacts"][0], "content_ref": two}, base.record["artifacts"][1]]).id)
        self.assertNotEqual(base.id, ProjectSnapshot.create([{**base.record["artifacts"][0], "logical_name": "changed"}, base.record["artifacts"][1]]).id)
        self.assertNotEqual(base.id, ProjectSnapshot.create(base.record["artifacts"], collector_fingerprint=None).id)

    def test_persists_and_reuses_snapshot_in_w1_namespace(self):
        ref = self.store.put_blob(b"plan")
        snapshot = create_project_snapshot(self.store, [{"logical_name": "plan", "content_ref": ref}])
        same = create_project_snapshot(self.store, [{"content_ref": ref, "logical_name": "plan"}])
        self.assertEqual(snapshot.id, same.id)
        self.assertEqual(snapshot.record, self.store.get_record("project_snapshot", snapshot.id))
        self.assertTrue(self.store.record_exists("project_snapshot", snapshot.id))

    def test_fingerprint_requires_full_sha256_reference(self):
        with self.assertRaises(EvidenceRecordError):
            ProjectSnapshot.create([], collector_fingerprint="sha256:x")
        valid = "sha256:" + "a" * 64
        self.assertEqual(valid, ProjectSnapshot.create([], collector_fingerprint=valid).record["collector_fingerprint"])

    def test_schema_rejects_non_logical_artifact_names(self):
        schema = json.loads(Path("scripts/execution-evidence.schema.v2.json").read_text(encoding="utf-8"))
        pattern = schema["properties"]["artifacts"]["items"]["properties"]["logical_name"]["pattern"]
        for value in ("", "   ", "/tmp/plan.md", "C:\\tmp\\plan.md", "nested/plan.md"):
            self.assertIsNone(re.fullmatch(pattern, value), value)
        self.assertIsNotNone(re.fullmatch(pattern, "plan.md"))

    def test_record_isolated_from_mutation_after_identity(self):
        snapshot = ProjectSnapshot.create([])
        exposed = snapshot.record
        exposed["artifacts"].append({"logical_name": "x", "content_ref": "sha256:" + "0" * 64})
        self.assertEqual([], snapshot.record["artifacts"])
        snapshot.persist(self.store)
        self.assertEqual([], self.store.get_record("project_snapshot", snapshot.id)["artifacts"])

    def test_invalid_inputs_do_not_persist_snapshots(self):
        with self.assertRaises(EvidenceRecordError):
            capture_artifact(self.store, "missing", source_path=self.repo / "missing")
        with self.assertRaises(EvidenceRecordError):
            ProjectSnapshot.create([{"logical_name": "same", "content_ref": "sha256:" + "0" * 64}, {"logical_name": "same", "content_ref": "sha256:" + "1" * 64}])
        with self.assertRaises(EvidenceRecordError):
            validate_project_snapshot({"schema_version": 1, "record_type": "ProjectSnapshot", "artifacts": []})
        self.assertEqual([], list((self.store.root / "project" / "snapshots").glob("*.json")) if (self.store.root / "project" / "snapshots").exists() else [])

    def test_store_failure_does_not_create_snapshot(self):
        class BrokenStore(GitMetadataEvidenceStore):
            def put_immutable_record(self, namespace, record_id, value):
                raise EvidenceStoreError("controlled failure")
        broken = BrokenStore(self.repo)
        ref = broken.put_blob(b"plan")
        with self.assertRaises(EvidenceStoreError):
            create_project_snapshot(broken, [{"logical_name": "plan", "content_ref": ref}])


if __name__ == "__main__":
    unittest.main()
