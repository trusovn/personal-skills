import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts.evidence_records import (
    EvidenceRecordError,
    ProjectSnapshot,
    TaskRevision,
    capture_artifact,
    create_project_snapshot,
    create_task_revision,
    validate_task_revision,
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

    def _task_inputs(self):
        brief = self.store.put_blob(b"brief")
        artifact = {"logical_name": "verification", "content_ref": self.store.put_blob(b"verify")}
        return brief, [artifact]

    def test_task_revision_identity_is_canonical_and_path_independent(self):
        brief, artifacts = self._task_inputs()
        first = TaskRevision.create("W2.2", brief, artifacts, planning={"task_type": "bugfix"})
        second = TaskRevision.create(
            "W2.2",
            brief,
            [{"content_ref": artifacts[0]["content_ref"], "logical_name": "verification"}],
            planning={"task_type": "bugfix"},
        )
        self.assertEqual(first.id, second.id)
        self.assertEqual(first.record, second.record)
        self.assertNotIn("/tmp", json.dumps(first.record))

    def test_each_semantic_revision_dimension_changes_identity(self):
        brief, artifacts = self._task_inputs()
        base = dict(
            task_id="W2.2",
            task_brief_ref=brief,
            artifact_refs=artifacts,
            planning={"task_type": "bugfix", "planner_recommended_profile": "planner-default"},
            planning_project_snapshot_ref="sha256:" + "1" * 64,
            decomposition={"source_plan_ref": "W2"},
        )
        variants = [
            {**base, "artifact_refs": [{"logical_name": "other", "content_ref": artifacts[0]["content_ref"]}]},
            {**base, "planning": {"task_type": "feature", "planner_recommended_profile": "planner-default"}},
            {**base, "planning": {"task_type": "bugfix", "planner_recommended_profile": "planner-default", "expected_calls": 2}},
            {**base, "planning": {"task_type": "bugfix", "planner_recommended_profile": "planner-high"}},
            {**base, "decomposition": {"source_plan_ref": "W3"}},
            {**base, "planning_project_snapshot_ref": "sha256:" + "2" * 64},
            {**base, "planning": {"task_type": "bugfix", "planner_recommended_profile": "planner-default", "provenance": {"source": "planner-b"}}},
        ]
        baseline = TaskRevision.create(**base)
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertNotEqual(baseline.id, TaskRevision.create(**variant).id)

    def test_planning_is_sparse_and_preserves_supplied_values(self):
        brief, artifacts = self._task_inputs()
        planning = {
            "task_type": "bugfix",
            "expected_calls": 0,
            "confidence": False,
            "verification_work": None,
            "provenance": {"knowledge_status": "planner_estimated", "source": "planner"},
        }
        revision = TaskRevision.create("W2.2", brief, artifacts, planning=planning)
        self.assertEqual(planning, revision.record["planning"])
        self.assertNotIn("intended_scope", revision.record["planning"])
        self.assertNotIn("planning", TaskRevision.create("W2.2", brief, artifacts).record)

    def test_planning_paths_are_canonical_across_structured_fields(self):
        brief, artifacts = self._task_inputs()
        fields = [
            "task_type",
            "intended_scope",
            "behavioral_scope",
            "transformation_type",
            "implementation_precedent",
            "state_or_compatibility_constraints",
            "verification_work",
            "discovery_uncertainty",
            "expected_calls",
            "expected_duration",
            "confidence",
            "planner_recommended_profile",
            "reasoning_effort",
            "split_decision",
        ]
        for field in fields:
            with self.subTest(field=field):
                first = TaskRevision.create("W2.2", brief, artifacts, planning={field: "/tmp/package-a"})
                second = TaskRevision.create("W2.2", brief, artifacts, planning={field: "/tmp/package-b"})
                self.assertEqual(first.id, second.id)
                self.assertEqual(first.record, second.record)
                self.assertNotIn("/tmp/", json.dumps(first.record))
        first = TaskRevision.create("W2.2", brief, artifacts, planning={"intended_scope": {"root": ["/tmp/package-a"]}})
        second = TaskRevision.create("W2.2", brief, artifacts, planning={"intended_scope": {"root": ["/tmp/package-b"]}})
        self.assertEqual(first.record, second.record)

    def test_absolute_path_marker_is_reserved_in_all_planning_values(self):
        brief, artifacts = self._task_inputs()
        planning_values = [
            {"intended_scope": "<absolute-path>"},
            {"intended_scope": {"root": ["<absolute-path>"]}},
        ]
        for planning in planning_values:
            with self.subTest(planning=planning), self.assertRaises(EvidenceRecordError):
                TaskRevision.create("W2.2", brief, artifacts, planning=planning)

    def test_planner_recommended_profile_is_preserved_and_persisted(self):
        brief, artifacts = self._task_inputs()
        revision = create_task_revision(
            self.store,
            "W2.2",
            brief,
            artifacts,
            planning={"planner_recommended_profile": "planner-default"},
        )
        self.assertEqual("planner-default", revision.record["planning"]["planner_recommended_profile"])
        self.assertEqual(revision.record, self.store.get_record("task_revision", ("W2.2", revision.id)))
        with self.assertRaises(EvidenceRecordError):
            TaskRevision.create("W2.2", brief, artifacts, planning={"intended_profile": "planner-default"})

    def test_decomposition_persists_parent_and_child_without_attempt(self):
        brief, artifacts = self._task_inputs()
        parent = create_task_revision(
            self.store,
            "W2",
            brief,
            artifacts,
            planning={"split_decision": "split"},
            decomposition={"child_task_ids": ["W2.2"], "source_plan_ref": "W2"},
        )
        child = create_task_revision(
            self.store,
            "W2.2",
            brief,
            artifacts,
            decomposition={"parent_task_id": "W2", "source_plan_ref": "W2"},
        )
        self.assertEqual(parent.record, self.store.get_record("task_revision", ("W2", parent.id)))
        self.assertEqual(child.record, self.store.get_record("task_revision", ("W2.2", child.id)))
        self.assertIsNone(self.store.get_record("attempt", "W2"))

    def test_invalid_revision_and_immutable_conflict_preserve_existing_record(self):
        brief, artifacts = self._task_inputs()
        revision = create_task_revision(self.store, "W2.2", brief, artifacts)
        before = self.store.get_record("task_revision", ("W2.2", revision.id))
        with self.assertRaises(EvidenceRecordError):
            validate_task_revision({**revision.record, "schema_version": 1})
        with self.assertRaises(EvidenceRecordError):
            TaskRevision.create("W2.2", brief, artifacts, planning={"provenance": {"knowledge_status": "made_up"}})
        with self.assertRaises(EvidenceStoreError):
            self.store.put_immutable_record("task_revision", ("W2.2", revision.id), {"bad": True})
        self.assertEqual(before, self.store.get_record("task_revision", ("W2.2", revision.id)))

    def test_provenance_rejects_unknown_fields(self):
        brief, artifacts = self._task_inputs()
        with self.assertRaises(EvidenceRecordError):
            TaskRevision.create("W2.2", brief, artifacts, planning={"provenance": {"bogus": "accepted"}})

    def test_stable_ids_reject_newlines(self):
        brief, artifacts = self._task_inputs()
        base = {"task_id": "W2.2", "task_brief_ref": brief, "artifact_refs": artifacts}
        invalid_inputs = [
            {"task_id": "W2.2\nnext"},
            {"planning": {"provenance": {"source": "planner\nnext"}}},
            {"decomposition": {"parent_task_id": "W2\nnext"}},
            {"decomposition": {"child_task_ids": ["W2.3\nnext"]}},
            {"decomposition": {"source_plan_ref": "W2\nnext"}},
        ]
        for invalid in invalid_inputs:
            with self.subTest(invalid=invalid), self.assertRaises(EvidenceRecordError):
                TaskRevision.create(**{**base, **invalid})

    def test_decomposition_rejects_invalid_topology(self):
        brief, artifacts = self._task_inputs()
        invalid = [
            {"child_task_ids": []},
            {"child_task_ids": ["W2.2", "W2.2"]},
            {"parent_task_id": "W2.2"},
            {"child_task_ids": ["W2.2"]},
        ]
        for decomposition in invalid:
            with self.subTest(decomposition=decomposition), self.assertRaises(EvidenceRecordError):
                TaskRevision.create("W2.2", brief, artifacts, decomposition=decomposition)

    def test_schema_encodes_task_revision_structures(self):
        schema = json.loads(Path("scripts/execution-evidence.schema.v2.json").read_text(encoding="utf-8"))
        task_schema = next(item for item in schema["oneOf"] if item["properties"]["record_type"]["const"] == "TaskRevision")
        planning = task_schema["properties"]["planning"]
        self.assertFalse(planning["additionalProperties"])
        self.assertIn("task_type", planning["properties"])
        self.assertIn("planner_recommended_profile", planning["properties"])
        self.assertNotIn("intended_profile", planning["properties"])
        provenance = planning["properties"]["provenance"]
        self.assertIn("planner_estimated", provenance["properties"]["knowledge_status"]["enum"])
        decomposition = task_schema["properties"]["decomposition"]
        self.assertFalse(decomposition["additionalProperties"])
        self.assertEqual(1, decomposition["properties"]["child_task_ids"]["minItems"])
        self.assertTrue(decomposition["properties"]["child_task_ids"]["uniqueItems"])

    def test_schema_rejects_whitespace_only_stable_ids(self):
        schema = json.loads(Path("scripts/execution-evidence.schema.v2.json").read_text(encoding="utf-8"))
        task_schema = next(item for item in schema["oneOf"] if item["properties"]["record_type"]["const"] == "TaskRevision")
        planning = task_schema["properties"]["planning"]
        decomposition = task_schema["properties"]["decomposition"]["properties"]
        identifier_schemas = [
            task_schema["properties"]["task_id"],
            planning["properties"]["provenance"]["properties"]["source"],
            decomposition["parent_task_id"],
            decomposition["child_task_ids"]["items"],
            decomposition["source_plan_ref"],
        ]
        for identifier_schema in identifier_schemas:
            with self.subTest(identifier_schema=identifier_schema):
                self.assertIsNone(re.fullmatch(identifier_schema["pattern"], "   "))


if __name__ == "__main__":
    unittest.main()
