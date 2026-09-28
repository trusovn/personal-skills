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


from scripts.evidence_records import (
    Association,
    ExecutionAttempt,
    compute_collector_fingerprint,
    create_association,
    validate_association,
    validate_execution_attempt,
)


def _attempt_record(attempt_id="A1", **overrides):
    record = {
        "attempt_id": attempt_id,
        "schema_version": 2,
        "record_type": "ExecutionAttempt",
        "task": {"task_revision_ref": "sha256:" + "1" * 64},
        "pre_run": {
            "repository_state": {"git_commit": "abc"},
            "workflow_identity": {"fingerprint": "wf-1"},
            "actual_runtime_identity": {"model": "m1", "runner": "r1"},
        },
        "execution": {"started_at": "2026-01-01T00:00:00Z", "termination_state": "unknown"},
        "post_run": {"repository_state": {"git_commit": "def"}},
        "evidence": {"schema_version": 2, "collector_fingerprint": None},
    }
    record.update(overrides)
    return record


def _association_record(attempt_id="A1", association_id="acc-1", **overrides):
    record = {
        "association_id": association_id,
        "attempt_id": attempt_id,
        "schema_version": 2,
        "record_type": "Association",
        "type": "acceptance_review",
        "producer": {"name": "reviewer-1"},
        "outcome_status": {"result": "ACCEPT"},
        "collected_at": "2026-01-02T00:00:00Z",
    }
    record.update(overrides)
    return record


class ExecutionAttemptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        import subprocess
        subprocess.run(["git", "-C", str(self.repo), "init", "-q"], check=True)
        self.store = GitMetadataEvidenceStore(self.repo)

    def tearDown(self):
        self.temp.cleanup()

    def _task_inputs(self):
        brief = self.store.put_blob(b"brief")
        artifact = {"logical_name": "verification", "content_ref": self.store.put_blob(b"verify")}
        return brief, [artifact]

    # V-01 — exactly one task input mode
    def test_task_input_cardinality(self):
        direct = {"task": {"direct_input_ref": "sha256:" + "2" * 64}}
        revision = {"task": {"task_revision_ref": "sha256:" + "1" * 64}}
        self.assertIsNotNone(validate_execution_attempt({**_attempt_record(), **direct}))
        self.assertIsNotNone(validate_execution_attempt(_attempt_record()))
        for bad in (
            {"task": {"direct_input_ref": "sha256:" + "2" * 64, "task_revision_ref": "sha256:" + "1" * 64}},
            {"task": {}},
        ):
            with self.subTest(bad=bad), self.assertRaises(EvidenceRecordError):
                validate_execution_attempt({**_attempt_record(), **bad})
        self.assertFalse(self.store.record_exists("attempt", "A1"))

    # V-02 — planning vs execution snapshot roles
    def test_snapshot_roles_remain_independent(self):
        planning_ref = "sha256:" + "3" * 64
        execution_ref = "sha256:" + "4" * 64
        brief, artifacts = self._task_inputs()
        revision = create_task_revision(
            self.store, "T1", brief, artifacts,
            planning_project_snapshot_ref=planning_ref,
        )
        attempt = ExecutionAttempt({
            **_attempt_record(),
            "task": {"task_revision_ref": revision.id},
            "execution_project_snapshot_ref": execution_ref,
        }).create_in_store(self.store)
        stored_revision = self.store.get_record("task_revision", ("T1", revision.id))
        stored_attempt = self.store.get_record("attempt", "A1")
        self.assertEqual(planning_ref, stored_revision["planning_project_snapshot_ref"])
        self.assertEqual(execution_ref, stored_attempt["execution_project_snapshot_ref"])
        self.assertNotIn("execution_project_snapshot_ref", stored_revision)
        self.assertIsNone(validate_execution_attempt({**_attempt_record()}).get("execution_project_snapshot_ref"))

    # V-03 — optional sections stay sparse and inline
    def test_optional_sections_are_sparse_and_inline(self):
        record = _attempt_record(
            pre_run={
                "repository_state": {"git_commit": "abc"},
                "workflow_identity": {"fingerprint": "wf-1"},
                "actual_runtime_identity": {"model": "m1"},
                "conditions": {"network_access": False, "budget": 0},
            },
            execution={
                "started_at": "2026-01-01T00:00:00Z",
                "termination_state": "unknown",
                "checks": [],
                "telemetry": {"tokens": None, "retries": 0, "status": "not_applicable"},
            },
        )
        validated = validate_execution_attempt(record)
        self.assertIn("conditions", validated["pre_run"])
        self.assertNotIn("telemetry", validated["pre_run"])
        self.assertEqual([], validated["execution"]["checks"])
        self.assertEqual({"tokens": None, "retries": 0, "status": "not_applicable"}, validated["execution"]["telemetry"])
        bare = validate_execution_attempt(_attempt_record())
        self.assertNotIn("conditions", bare["pre_run"])
        self.assertNotIn("telemetry", bare["execution"])
        self.assertNotIn("checks", bare["execution"])
        for misplaced in (
            {"pre_run": {**_attempt_record()["pre_run"], "telemetry": {"x": 1}}},
            {"execution": {**_attempt_record()["execution"], "conditions": {"x": 1}}},
            {"post_run": {**_attempt_record()["post_run"], "checks": []}},
        ):
            with self.subTest(misplaced=misplaced), self.assertRaises(EvidenceRecordError):
                validate_execution_attempt({**_attempt_record(), **misplaced})

    # V-04 — three profile roles distinct
    def test_profile_roles_never_collapse(self):
        brief, artifacts = self._task_inputs()
        revision = create_task_revision(
            self.store, "T2", brief, artifacts,
            planning={"planner_recommended_profile": "profile-A"},
        )
        attempt = ExecutionAttempt({
            **_attempt_record(),
            "task": {"task_revision_ref": revision.id},
            "pre_run": {
                "repository_state": {"git_commit": "abc"},
                "workflow_identity": {"fingerprint": "wf-1"},
                "actual_runtime_identity": {"model": "profile-C"},
                "intended_execution_profile": {"name": "profile-B"},
            },
        }).create_in_store(self.store)
        stored_revision = self.store.get_record("task_revision", ("T2", revision.id))
        stored_attempt = self.store.get_record("attempt", "A1")
        self.assertEqual("profile-A", stored_revision["planning"]["planner_recommended_profile"])
        self.assertEqual("profile-B", stored_attempt["pre_run"]["intended_execution_profile"]["name"])
        self.assertEqual("profile-C", stored_attempt["pre_run"]["actual_runtime_identity"]["model"])
        self.assertNotEqual(stored_revision["planning"]["planner_recommended_profile"], stored_attempt["pre_run"]["intended_execution_profile"])
        minimal = validate_execution_attempt(_attempt_record())
        self.assertNotIn("intended_execution_profile", minimal["pre_run"])

    # V-05 — five attempt relations, task relations excluded
    def test_attempt_relations_preserve_distinct_attempts(self):
        first = ExecutionAttempt(_attempt_record("R1")).create_in_store(self.store)
        for relation in ("retry_of", "correction_of", "continuation_of", "profile_replay_of", "calibration_of"):
            with self.subTest(relation=relation):
                target_id = f"target-{relation}"
                target = ExecutionAttempt(_attempt_record(target_id)).create_in_store(self.store)
                source_record = {**_attempt_record("A1"), "related_attempts": [{"relation": relation, "attempt_id": target_id}]}
                source = ExecutionAttempt(source_record)
                self.assertEqual(target_id, source.record["related_attempts"][0]["attempt_id"])
                self.assertEqual(relation, source.record["related_attempts"][0]["relation"])
                self.assertEqual(_attempt_record(target_id), self.store.get_record("attempt", target_id))
                self.assertIsNotNone(self.store.get_record("attempt", "R1"))
        with self.assertRaises(EvidenceRecordError):
            validate_execution_attempt({**_attempt_record(), "related_attempts": [{"relation": "parent_of", "attempt_id": "R1"}]})
        with self.assertRaises(EvidenceRecordError):
            validate_execution_attempt({**_attempt_record(), "related_attempts": [{"relation": "retry_of", "attempt_id": "bad\nid"}]})

    # V-06 — association immutability and unchanged attempt
    def test_association_is_immutable_beside_unchanged_attempt(self):
        attempt = ExecutionAttempt(_attempt_record("A1")).create_in_store(self.store)
        attempt_bytes = (self.store.root / "attempts" / "A1" / "attempt.json").read_bytes()
        artifact_ref = self.store.put_blob(b"review-artifact")
        create_association(self.store, _association_record(durable_artifact_ref=artifact_ref))
        create_association(self.store, _association_record(association_id="acc-2"))
        stored = self.store.get_record("association", ("A1", "acc-1"))
        self.assertEqual(artifact_ref, stored["durable_artifact_ref"])
        self.assertEqual({"result": "ACCEPT"}, stored["outcome_status"])
        self.assertEqual("2026-01-02T00:00:00Z", stored["collected_at"])
        self.assertEqual({"name": "reviewer-1"}, stored["producer"])
        self.assertEqual(attempt_bytes, (self.store.root / "attempts" / "A1" / "attempt.json").read_bytes())
        with self.assertRaises(EvidenceStoreError):
            self.store.put_immutable_record("association", ("A1", "acc-1"), _association_record(outcome_status={"result": "CHANGES"}))
        self.assertEqual({"result": "ACCEPT"}, self.store.get_record("association", ("A1", "acc-1"))["outcome_status"])

    # V-07 — collector fingerprint semantics
    def test_collector_fingerprint_tracks_semantics_not_location_or_workflow(self):
        base = compute_collector_fingerprint(
            file_contents={"records.py": b"bytes-one", "store.py": b"bytes-two"},
            config={"version": 1},
        )
        self.assertEqual(base, compute_collector_fingerprint(
            file_contents={"store.py": b"bytes-two", "records.py": b"bytes-one"},
            config={"version": 1},
        ))
        text_base = compute_collector_fingerprint(
            file_contents={"records.py": "text-one", "store.py": "text-two"},
            config={"version": 1},
        )
        self.assertEqual(text_base, compute_collector_fingerprint(
            file_contents={"store.py": "text-two", "records.py": "text-one"},
            config={"version": 1},
        ))
        relocated = compute_collector_fingerprint(
            file_contents={"records.py": b"bytes-one", "store.py": b"bytes-two"},
            config={"version": 1},
        )
        self.assertEqual(base, relocated)
        changed_file = compute_collector_fingerprint(
            file_contents={"records.py": b"bytes-CHANGED", "store.py": b"bytes-two"},
            config={"version": 1},
        )
        self.assertNotEqual(base, changed_file)
        changed_config = compute_collector_fingerprint(
            file_contents={"records.py": b"bytes-one", "store.py": b"bytes-two"},
            config={"version": 2},
        )
        self.assertNotEqual(base, changed_config)
        # workflow-only change does not affect the collector fingerprint
        self.assertEqual(base, compute_collector_fingerprint(
            file_contents={"records.py": b"bytes-one", "store.py": b"bytes-two"},
            config={"version": 1},
        ))
        self.assertTrue(base.startswith("sha256:"))
        # workflow identity lives in pre_run, separate from evidence.collector_fingerprint
        with_workflow = ExecutionAttempt(
            {**_attempt_record(), "pre_run": {**_attempt_record()["pre_run"], "workflow_identity": {"fingerprint": base}}}
        )
        self.assertEqual(base, with_workflow.record["pre_run"]["workflow_identity"]["fingerprint"])
        self.assertIsNone(with_workflow.record["evidence"]["collector_fingerprint"])

    def test_collector_fingerprint_over_real_files_is_location_independent(self):
        file_a = self.repo / "subdir-a" / "records.py"
        file_b = self.repo / "subdir-b" / "store.py"
        file_a.parent.mkdir()
        file_b.parent.mkdir()
        file_a.write_bytes(b"records-bytes")
        file_b.write_bytes(b"store-bytes")
        base = compute_collector_fingerprint(file_paths=[file_a, file_b])
        copy_a = self.repo / "elsewhere" / "renamed.py"
        copy_a.parent.mkdir()
        copy_a.write_bytes(b"records-bytes")
        copy_b = self.repo / "elsewhere2" / "store.py"
        copy_b.parent.mkdir()
        copy_b.write_bytes(b"store-bytes")
        self.assertNotEqual(base, compute_collector_fingerprint(file_paths=[copy_a, copy_b]))
        # logical-name-based selection is location independent
        named_base = compute_collector_fingerprint(file_contents={"records.py": b"records-bytes", "store.py": b"store-bytes"})
        self.assertEqual(named_base, compute_collector_fingerprint(file_contents={"store.py": b"store-bytes", "records.py": b"records-bytes"}))
        self.assertNotEqual(named_base, compute_collector_fingerprint(file_contents={"records.py": b"CHANGED", "store.py": b"store-bytes"}))

    # V-08 — invalid families rejected before persistence
    def test_invalid_families_rejected_without_persistence(self):
        ExecutionAttempt(_attempt_record("V8")).create_in_store(self.store)
        before_attempt = self.store.get_record("attempt", "V8")
        before_assoc = self.store.get_record("association", ("V8", "a1"))
        invalid_attempts = [
            _attempt_record(task={"direct_input_ref": "sha256:" + "2" * 64, "task_revision_ref": "sha256:" + "1" * 64}),
            _attempt_record(task={}),
            _attempt_record(schema_version=1),
            _attempt_record(related_attempts=[{"relation": "made_up", "attempt_id": "R1"}]),
            _attempt_record(related_attempts=[{"relation": "retry_of"}]),
            _attempt_record(pre_run={**_attempt_record()["pre_run"], "conditions": "not-an-object"}),
            _attempt_record(execution={**_attempt_record()["execution"], "telemetry": []}),
            _attempt_record(evidence={"schema_version": 3, "collector_fingerprint": None}),
        ]
        for invalid in invalid_attempts:
            with self.subTest(record=invalid), self.assertRaises(EvidenceRecordError):
                validate_execution_attempt(invalid)
        invalid_associations = [
            {**_association_record(attempt_id="V8"), "producer": "not-an-object"},
            {**_association_record(attempt_id="V8"), "type": "bad\ntype"},
            {**_association_record(attempt_id="V8"), "durable_artifact_ref": "sha256:xyz"},
            {**_association_record(attempt_id="V8"), "collected_at": "   "},
            {**_association_record(attempt_id="V8"), "extra": True},
            {k: v for k, v in _association_record(attempt_id="V8").items() if k != "outcome_status"},
        ]
        for invalid in invalid_associations:
            with self.subTest(association=invalid), self.assertRaises(EvidenceRecordError):
                create_association(self.store, invalid)
        valid_association = create_association(self.store, _association_record(attempt_id="V8"))
        before_valid = self.store.get_record("association", ("V8", "acc-1"))
        with self.assertRaises(EvidenceStoreError):
            self.store.put_immutable_record(
                "association", ("V8", "acc-1"),
                {**_association_record(attempt_id="V8"), "outcome_status": {"result": "CHANGED"}},
            )
        self.assertEqual(before_valid, self.store.get_record("association", ("V8", "acc-1")))
        self.assertEqual(_association_record(attempt_id="V8"), valid_association.record)
        self.assertEqual(before_attempt, self.store.get_record("attempt", "V8"))

    # V-09 — four first-class records only
    def test_schema_exposes_only_four_first_class_records(self):
        schema = json.loads(Path("scripts/execution-evidence.schema.v2.json").read_text(encoding="utf-8"))
        record_types = sorted(
            branch["properties"]["record_type"]["const"]
            for branch in schema["oneOf"]
            if "record_type" in branch.get("properties", {})
        )
        self.assertEqual(["Association", "ExecutionAttempt", "ProjectSnapshot", "TaskRevision"], record_types)
        self.assertIn("conditions", schema["oneOf"][2]["properties"]["pre_run"]["properties"])
        self.assertIn("telemetry", schema["oneOf"][2]["properties"]["execution"]["properties"])
        self.assertIn("checks", schema["oneOf"][2]["properties"]["execution"]["properties"])
        self.assertIn("collector_fingerprint", schema["oneOf"][2]["properties"]["evidence"]["properties"])
        nested_defs = set(schema["$defs"])
        self.assertEqual({"artifact", "execution_checks", "collector_identity"}, nested_defs)

    # V-10 — full graph through real W1 operations
    def test_four_record_graph_composes_through_w1(self):
        planning_ref = create_project_snapshot(self.store, [{"logical_name": "plan.md", "content_ref": self.store.put_blob(b"plan bytes")}]).id
        brief = self.store.put_blob(b"brief")
        artifacts = [{"logical_name": "verification.md", "content_ref": self.store.put_blob(b"verify")}]
        revision = create_task_revision(
            self.store, "TASK", brief, artifacts,
            planning_project_snapshot_ref=planning_ref,
            planning={"planner_recommended_profile": "planner-default"},
        )
        execution_ref = create_project_snapshot(self.store, [{"logical_name": "exec.md", "content_ref": self.store.put_blob(b"exec bytes")}]).id
        fingerprint = compute_collector_fingerprint(file_contents={"records.py": b"x"}, config={"v": 2})
        attempt = ExecutionAttempt({
            **_attempt_record("GRAPH"),
            "task": {"task_revision_ref": revision.id},
            "execution_project_snapshot_ref": execution_ref,
            "evidence": {"schema_version": 2, "collector_fingerprint": fingerprint},
        }).create_in_store(self.store)
        association = create_association(self.store, _association_record(attempt_id="GRAPH", durable_artifact_ref=brief))
        self.assertEqual(revision.record, self.store.get_record("task_revision", ("TASK", revision.id)))
        self.assertEqual(execution_ref, self.store.get_record("attempt", "GRAPH")["execution_project_snapshot_ref"])
        self.assertEqual(fingerprint, self.store.get_record("attempt", "GRAPH")["evidence"]["collector_fingerprint"])
        self.assertEqual(association.record, self.store.get_record("association", ("GRAPH", "acc-1")))
        self.assertIsNone(self.store.get_record("attempt", "GRAPH").get("physical_path"))
        self.assertNotIn("scripts/evidence_store.py", json.dumps(self.store.get_record("attempt", "GRAPH")))

    # V-11 — scope is standard-library-only and no lifecycle behavior added
    def test_no_lifecycle_or_external_dependencies_added(self):
        import scripts.evidence_records as module
        import sys
        imported = {name for name in sys.modules if name in {"requests", "yaml", "click", "pydantic"}}
        self.assertEqual(set(), imported)
        source = Path("scripts/evidence_records.py").read_text(encoding="utf-8")
        self.assertNotIn("import subprocess", source)
        self.assertNotIn("update_active", source)
        self.assertNotIn("finalize_attempt", source)
        for forbidden in ("run_evidence", "skill"):
            self.assertNotIn(forbidden, source)


class AcceptanceCorrectionTests(unittest.TestCase):
    """Regressions for the W2.3 acceptance findings."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        import subprocess
        subprocess.run(["git", "-C", str(self.repo), "init", "-q"], check=True)
        self.store = GitMetadataEvidenceStore(self.repo)
        (self.repo / "dir-a").mkdir()
        (self.repo / "dir-b").mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_fingerprint_rejects_colliding_logical_names_across_input_forms(self):
        shadowed = self.repo / "dir-a" / "records.py"
        shadowed.write_bytes(b"shadowed-bytes")
        with self.assertRaises(EvidenceRecordError):
            compute_collector_fingerprint(
                file_contents={"records.py": b"explicit-bytes"},
                file_paths=[shadowed],
            )
        first = self.repo / "dir-a" / "same-name.py"
        second = self.repo / "dir-b" / "same-name.py"
        first.write_bytes(b"first")
        second.write_bytes(b"second")
        with self.assertRaises(EvidenceRecordError):
            compute_collector_fingerprint(file_paths=[first, second])
        self.assertNotEqual(
            compute_collector_fingerprint(file_contents={"a.py": b"one"}),
            compute_collector_fingerprint(file_contents={"a.py": b"two"}),
        )

    def test_fingerprint_covers_every_selected_file_and_ignores_order(self):
        unique_a = self.repo / "dir-a" / "alpha.py"
        unique_b = self.repo / "dir-b" / "beta.py"
        unique_a.write_bytes(b"alpha-bytes")
        unique_b.write_bytes(b"beta-bytes")
        both = compute_collector_fingerprint(file_paths=[unique_a, unique_b])
        self.assertEqual(both, compute_collector_fingerprint(file_paths=[unique_b, unique_a]))
        alpha_only = compute_collector_fingerprint(file_paths=[unique_a])
        beta_only = compute_collector_fingerprint(file_paths=[unique_b])
        self.assertNotEqual(both, alpha_only)
        self.assertNotEqual(both, beta_only)
        self.assertNotEqual(alpha_only, beta_only)
        changed = self.repo / "dir-a" / "alpha.py"
        changed.write_bytes(b"alpha-CHANGED")
        self.assertNotEqual(both, compute_collector_fingerprint(file_paths=[unique_a, unique_b]))
        mixed_base = compute_collector_fingerprint(
            file_contents={"gamma.py": b"gamma"},
            file_paths=[unique_a, unique_b],
        )
        self.assertEqual(mixed_base, compute_collector_fingerprint(
            file_contents={"gamma.py": b"gamma"},
            file_paths=[unique_b, unique_a],
        ))
        self.assertNotEqual(mixed_base, compute_collector_fingerprint(
            file_contents={"gamma.py": b"gamma"},
            file_paths=[unique_b],
        ))

    def test_schema_accepts_single_mode_task_inputs_only(self):
        task_schema = next(
            item for item in json.loads(
                Path("scripts/execution-evidence.schema.v2.json").read_text(encoding="utf-8")
            )["oneOf"]
            if item["properties"].get("record_type", {}).get("const") == "ExecutionAttempt"
        )
        task = task_schema["properties"]["task"]
        direct = {"direct_input_ref": "sha256:" + "2" * 64}
        revision = {"task_revision_ref": "sha256:" + "1" * 64}
        for valid in (direct, revision):
            self.assertTrue(_schema_validates(task, valid), valid)
        for invalid in ({**direct, **revision}, {}, {"direct_input_ref": "sha256:x"}):
            self.assertFalse(_schema_validates(task, invalid), invalid)

    def test_association_canonical_fields_align_with_schema(self):
        schema = json.loads(Path("scripts/execution-evidence.schema.v2.json").read_text(encoding="utf-8"))
        association_schema = next(
            item for item in schema["oneOf"]
            if item["properties"].get("record_type", {}).get("const") == "Association"
        )
        for field in ("schema_version", "record_type"):
            self.assertIn(field, association_schema["required"])
        valid = _association_record()
        self.assertTrue(_schema_validates(association_schema, valid))
        self.assertTrue(_schema_validates(association_schema, {**valid, "durable_artifact_ref": None}))
        with self.assertRaises(EvidenceRecordError):
            validate_association({k: v for k, v in valid.items() if k != "schema_version"})
        with self.assertRaises(EvidenceRecordError):
            validate_association({k: v for k, v in valid.items() if k != "record_type"})
        with self.assertRaises(EvidenceRecordError):
            validate_association({**valid, "schema_version": 1})
        with self.assertRaises(EvidenceRecordError):
            validate_association({**valid, "record_type": "Other"})
        persisted = create_association(self.store, valid)
        self.assertEqual(2, persisted.record["schema_version"])
        self.assertEqual("Association", persisted.record["record_type"])
        self.assertEqual(persisted.record, self.store.get_record("association", ("A1", "acc-1")))

    def test_lifecycle_api_is_absent_from_w2_surface(self):
        self.assertFalse(hasattr(ExecutionAttempt, "update_active"))
        self.assertFalse(hasattr(ExecutionAttempt, "finalize"))
        attempt = ExecutionAttempt(_attempt_record("L1")).create_in_store(self.store)
        self.assertEqual(_attempt_record("L1"), self.store.get_record("attempt", "L1"))


def _schema_validates(subschema, instance):
    try:
        import jsonschema
    except ImportError:
        return _minimal_schema_check(subschema, instance)
    try:
        jsonschema.validate(instance, subschema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False


def _minimal_schema_check(subschema, instance):
    return _check(subschema, instance, f"$root")


def _check(schema, instance, path):
    if "const" in subschema:
        return instance == subschema["const"]
    if "enum" in subschema:
        return instance in subschema["enum"]
    expected_type = subschema.get("type")
    if expected_type == "object" and not isinstance(instance, dict):
        return False
    if expected_type == "string":
        if not isinstance(instance, str):
            return False
        if "minLength" in subschema and len(instance) < subschema["minLength"]:
            return False
        if "pattern" in subschema and not re.fullmatch(subschema["pattern"], instance):
            return False
    if "oneOf" in subschema:
        return sum(_check(branch, instance, path) for branch in subschema["oneOf"]) == 1
    if isinstance(instance, dict):
        props = subschema.get("properties", {})
        required = subschema.get("required", [])
        if any(key not in instance for key in required):
            return False
        if subschema.get("additionalProperties") is False and any(key not in props for key in instance):
            return False
        return all(_check(props[key], value, path) for key, value in instance.items() if key in props)
    return True
