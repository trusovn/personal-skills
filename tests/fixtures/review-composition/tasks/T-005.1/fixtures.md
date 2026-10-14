# T-005.1 fixtures.md — Reproducible qualification inputs

Status: supplied input data composed from the inherited T-002.4/T-003.4
composition records, INT-FLOW-001 qualification inputs and current repository
bytes. This inventory is never an observed role output; staged reports and
prior results are supplied history, not current role results. Every entry
names its setup command/environment, disposable workspace, authority, expected
oracle, inherited identity, producer/consumer, owning T-005 leaf and current
evidence level. Actual role compliance for every case remains unrun and is
owned by the named leaf per [docs/tasks/T-005/brief.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005/brief.md) evidence rules 1-4.

## Machine-readable inventory

The JSON block below is the auditable case inventory. Current selectors are
cross-checked against the inherited composition records by
`tests/test_review_composition.py` (`T0051QualificationInputTests`); a stale
owner test, missing fixture scenario, omitted identity or unresolved
evidence pointer fails that audit.

```json
{
  "task": "T-005.1",
  "artifact": "supplied reproducible qualification inputs: case inventory, disposable setup, projection receipts",
  "status": "supplied input data composed from inherited records and current repository bytes; never observed role outputs",
  "producers": [
    "bounded-task-implementer (T-005.1) composed this inventory; no skill-call agent produced or consumed it"
  ],
  "intended_consumers": [
    "T-005.2 \u2014 actual preparation/entry and verification-revision recovery role calls",
    "T-005.3 \u2014 actual discovery-to-decision role calls with contextual and mixed-condition contrasts",
    "T-005.4 \u2014 coordinator-recorded deferral consumption",
    "T-005.5 \u2014 actual conditional/correction continuity role calls",
    "T-005.6 \u2014 cross-child evidence audit and the ART-012 report",
    "task-review-discovery / task-acceptance-review \u2014 fresh evidence and decision calls over these supplied inputs"
  ],
  "setup_conventions": {
    "work_root": "one explicit disposable EVAL_WORK_ROOT per invocation; no shared or persistent workspace",
    "fixture_command": "EVAL_WORK_ROOT=<disposable> python3 <fixture path> <scenario>",
    "canonical_install": "python3 scripts/install_development_skills.py <disposable Git target>",
    "canonical_check": "python3 scripts/install_development_skills.py --check <disposable Git target> (read-only; exit 0 match / 1 drift / 2 failure)",
    "identity_rule": "workflow fingerprint is workflow-identity evidence only; full installed-projection equality is proven by an independent managed-path byte comparison plus a matching --check",
    "evidence_levels": [
      "structural_tests",
      "actual_behavior",
      "unrun_agent_compliance"
    ]
  },
  "case_inventory": [
    {
      "id": "INV-CASE-01",
      "kind": "lifecycle-repetition",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 1,
      "scenario": "queue-defect",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py queue-defect",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-01 source entry; task-review-discovery evals.json eval 1; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "`runner run-next` public entry point exercised for the first occurrence and the next real occurrence",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/fixtures/review-composition/tasks/T-005.1/evidence/V-02-setup-reconstruction.md (public probe receipt); tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-02",
      "kind": "public-entry",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-acceptance-review",
      "eval_id": 1,
      "scenario": "queue-defect-decision",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_acceptance_review.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py queue-defect-decision",
      "workspace": "acceptance-fixture disposable EVAL_WORK_ROOT staging",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-02 source entry; task-acceptance-review evals.json eval 1; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "decision consumes the staged discovery report for the run-next repetition case",
      "producer_consumer": "T-002.1-.3 task-acceptance-review producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_acceptance_review.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-03",
      "kind": "lifecycle-resume",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 2,
      "scenario": "exporter-accept",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py exporter-accept",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-03 source entry; task-review-discovery evals.json eval 2; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "`exportctl resume` recovery behavior with a real first state change",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-04",
      "kind": "lifecycle-retry",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-acceptance-review",
      "eval_id": 17,
      "scenario": "correction-regression-decision",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_acceptance_review.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py correction-regression-decision",
      "workspace": "acceptance-fixture disposable EVAL_WORK_ROOT staging",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-04 source entry; task-acceptance-review evals.json eval 17; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "orders retry emits processed rows per run; the correction regression duplicated every row (ORD-RERUN)",
      "producer_consumer": "T-002.1-.3 task-acceptance-review producer fixtures -> T-002.4 composition record -> T-005.5 actual role calls",
      "owning_leaf": "T-005.5",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_acceptance_review.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.5 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-05",
      "kind": "missing-capability",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-preflight",
      "eval_id": 2,
      "scenario": "scheduler-missing",
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_preflight.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py scheduler-missing",
      "workspace": "preflight-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-05 source entry; task-preflight evals.json eval 2; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "a missing decisive capability blocks readiness with its prerequisite owner",
      "producer_consumer": "T-002.1-.3 task-preflight producer fixtures -> T-002.4 composition record -> T-005.2 actual role calls",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_preflight.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.2 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-06",
      "kind": "missing-capability",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-acceptance-review",
      "eval_id": 13,
      "scenario": "mixed-conditions-authorized-decision",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_acceptance_review.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py mixed-conditions-authorized-decision",
      "workspace": "acceptance-fixture disposable EVAL_WORK_ROOT staging",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-06 source entry; task-acceptance-review evals.json eval 13; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "JOB-PAIR row blocked because the pair_claims.py helper is absent (composed in COMP-02)",
      "producer_consumer": "T-002.1-.3 task-acceptance-review producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_acceptance_review.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-07",
      "kind": "index-worktree-identity",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 4,
      "scenario": "exporter-restaged-stale",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py exporter-restaged-stale",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-07 source entry; task-review-discovery evals.json eval 4; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "matching worktree bytes and short-status text do not prove a matching index blob",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-08",
      "kind": "ledger-cardinality-order-type",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 5,
      "scenario": "ledger-defects",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py ledger-defects",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-08 source entry; task-review-discovery evals.json eval 5; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "ledger cardinality, ordering, and type-confusion defects across selected and non-selected entities",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-09",
      "kind": "ledger-cardinality-order-type",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 14,
      "scenario": "discovery-late-omission-clean",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-clean",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-09 source entry; task-review-discovery evals.json eval 14; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "LED-05 AC-03: exactly one running selected task with its latest active attempt",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-10",
      "kind": "workflow-tampering-replay-decision",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 7,
      "scenario": "workflow-matrix-defects",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py workflow-matrix-defects",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-10 source entry; task-review-discovery evals.json eval 7; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "WF-TAMPER: coherent tampering including recomputed internal digests",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-11",
      "kind": "workflow-tampering-replay-decision",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 8,
      "scenario": "workflow-matrix-defects",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py workflow-matrix-defects",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-11 source entry; task-review-discovery evals.json eval 8; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "WF-REPLAY and WF-DECISION replay and decision-boundary cases",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-12",
      "kind": "validator-valid-targeted-invalid",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 14,
      "scenario": "discovery-late-omission-clean",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-clean",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-12 source entry; task-review-discovery evals.json eval 14; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "valid instance exits 0; targeted boolean-revision, older-attempt, second-running instances exit 2",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-13",
      "kind": "validator-valid-targeted-invalid",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 13,
      "scenario": "discovery-late-omission-fail",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-fail",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-13 source entry; task-review-discovery evals.json eval 13; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "the fail variant keeps only the boolean-revision defect (exit 0) while the other invalid instances still exit 2",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-14",
      "kind": "process-resistant-descendant",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 9,
      "scenario": "process-cleanup-defects",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py process-cleanup-defects",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-14 source entry; task-review-discovery evals.json eval 9; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "PROC-RESIST: resistant descendant termination with observable synchronization",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-15",
      "kind": "process-pipe",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 9,
      "scenario": "process-cleanup-defects",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py process-cleanup-defects",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-15 source entry; task-review-discovery evals.json eval 9; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "PROC-PIPE: inherited-pipe release confirmed after each probe",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-16",
      "kind": "process-race",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 9,
      "scenario": "process-cleanup-defects",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py process-cleanup-defects",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-16 source entry; task-review-discovery evals.json eval 9; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "PROC-RACE: bounded waits, no arbitrary sleeps, and no fixture process survives discovery",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-17",
      "kind": "continuation",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 15,
      "scenario": "discovery-diagnostic-aggregate",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-diagnostic-aggregate",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-17 source entry; task-review-discovery evals.json eval 15; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "discovery-02.md continues the iteration with finding IDs, reviewer regressions, and the consumed gate record",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-18",
      "kind": "self-check-provenance",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-review-discovery",
      "eval_id": 6,
      "scenario": "authored-production-self-check",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py authored-production-self-check",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-18 source entry; task-review-discovery evals.json eval 6; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "SELF_CHECK_ONLY: an authoring session cannot publish independently corroborated rows",
      "producer_consumer": "T-002.1-.3 task-review-discovery producer fixtures -> T-002.4 composition record -> T-005.3 actual role calls",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.3 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-19",
      "kind": "preflight-readiness",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-preflight",
      "eval_id": 1,
      "scenario": "queue-ready",
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_preflight.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py queue-ready",
      "workspace": "preflight-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-19 source entry; task-preflight evals.json eval 1; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "material standalone value resolved from dirty ownership, dependencies, and command facts",
      "producer_consumer": "T-002.1-.3 task-preflight producer fixtures -> T-002.4 composition record -> T-005.2 actual role calls",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_preflight.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.2 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-20",
      "kind": "preflight-readiness",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-preflight",
      "eval_id": 3,
      "scenario": "api-overlap",
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_preflight.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py api-overlap",
      "workspace": "preflight-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-20 source entry; task-preflight evals.json eval 3; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "ownership overlap is separated or blocked before implementation",
      "producer_consumer": "T-002.1-.3 task-preflight producer fixtures -> T-002.4 composition record -> T-005.2 actual role calls",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_preflight.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.2 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-21",
      "kind": "preflight-readiness",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-preflight",
      "eval_id": 5,
      "scenario": "queue-guided",
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_preflight.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py queue-guided",
      "workspace": "preflight-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-21 source entry; task-preflight evals.json eval 5; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "guided direct request stays inline without durable paperwork",
      "producer_consumer": "T-002.1-.3 task-preflight producer fixtures -> T-002.4 composition record -> T-005.2 actual role calls",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_preflight.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.2 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-22",
      "kind": "preflight-readiness",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-preflight",
      "eval_id": 7,
      "scenario": null,
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_preflight.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py <scenario named by task-preflight eval 7 setup command; no single fixture scenario is declared>",
      "workspace": "preflight-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-22 source entry; task-preflight evals.json eval 7; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "a direct legacy brief is refused and routed to task-brief-designer for package normalization (prompt-only eval)",
      "producer_consumer": "T-002.1-.3 task-preflight producer fixtures -> T-002.4 composition record -> T-005.2 actual role calls",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_preflight.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.2 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-23",
      "kind": "preflight-readiness",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-preflight",
      "eval_id": 10,
      "scenario": "revision-recovery",
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_preflight.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py revision-recovery",
      "workspace": "preflight-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-23 source entry; task-preflight evals.json eval 10; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "a reasoned verification revision reuses unchanged facts and rejects affected obsolete readiness",
      "producer_consumer": "T-002.1-.3 task-preflight producer fixtures -> T-002.4 composition record -> T-005.2 actual role calls",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_preflight.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.2 role calls; no role result is claimed here"
    },
    {
      "id": "INV-CASE-24",
      "kind": "preflight-readiness",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json inherited_case_inventory",
      "skill": "task-preflight",
      "eval_id": 11,
      "scenario": "freshness-change",
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "owner_test": "tests/test_task_preflight.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py freshness-change",
      "workspace": "preflight-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json INV-CASE-24 source entry; task-preflight evals.json eval 11; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "material authority, dependency, ownership, permission, or capability change forces reconsideration",
      "producer_consumer": "T-002.1-.3 task-preflight producer fixtures -> T-002.4 composition record -> T-005.2 actual role calls",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_task_preflight.py",
      "role_boundary": "unrun: actual agent compliance is owned by T-005.2 role calls; no role result is claimed here"
    },
    {
      "id": "COMP-01",
      "kind": "preflight-only material exposure traced through discovery and decision inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json records",
      "skill": "task-acceptance-review",
      "scenarios": [
        "contextual-risk-blockers-decision"
      ],
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py contextual-risk-blockers-decision",
      "workspace": "acceptance-fixture disposable EVAL_WORK_ROOT staging",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json COMP-01 record; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "COMP-01 composed record semantics: preflight-only material exposure traced through discovery and decision inputs",
      "producer_consumer": "T-002.4 composed record -> T-005.3 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_review_composition.py; tests/test_contextual_export_risks.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.3"
    },
    {
      "id": "COMP-02",
      "kind": "confirmed blocker plus unfinished missing-proof row in one decision",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json records",
      "skill": "task-acceptance-review",
      "scenarios": [
        "mixed-conditions-authorized-decision",
        "mixed-conditions-forbidden-decision"
      ],
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py mixed-conditions-authorized-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py mixed-conditions-forbidden-decision",
      "workspace": "acceptance-fixture disposable EVAL_WORK_ROOT staging",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json COMP-02 record; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "COMP-02 composed record semantics: confirmed blocker plus unfinished missing-proof row in one decision",
      "producer_consumer": "T-002.4 composed record -> T-005.3 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.3"
    },
    {
      "id": "COMP-03",
      "kind": "failure, correction, and current clean evidence with discovery-owned gates",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json records",
      "skill": "task-review-discovery",
      "scenarios": [
        "discovery-correction-gate",
        "discovery-late-omission-fail",
        "discovery-late-omission-clean",
        "discovery-diagnostic-aggregate"
      ],
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-correction-gate; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-fail; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-clean; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-diagnostic-aggregate",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json COMP-03 record; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "COMP-03 composed record semantics: failure, correction, and current clean evidence with discovery-owned gates",
      "producer_consumer": "T-002.4 composed record -> T-005.5 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.5",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.5"
    },
    {
      "id": "COMP-04",
      "kind": "approved deferral record composed with later preflight inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json records",
      "skill": "task-acceptance-review",
      "scenarios": [
        "known-issue-consumption-decision",
        "known-issue-priority-only-decision",
        "correction-regression-decision"
      ],
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py known-issue-consumption-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py known-issue-priority-only-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py correction-regression-decision",
      "workspace": "acceptance-fixture disposable EVAL_WORK_ROOT staging",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json COMP-04 record; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "COMP-04 composed record semantics: approved deferral record composed with later preflight inputs",
      "producer_consumer": "T-002.4 composed record -> T-005.4 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.4",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.4"
    },
    {
      "id": "COMP-05",
      "kind": "prepared and direct review routes with session-authorship provenance",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-002.4/composition.json records",
      "skill": "task-review-discovery",
      "scenarios": [
        "discovery-prepared-ledger",
        "authored-production-self-check"
      ],
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-prepared-ledger; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py authored-production-self-check",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/T-002.4/composition.json COMP-05 record; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "COMP-05 composed record semantics: prepared and direct review routes with session-authorship provenance",
      "producer_consumer": "T-002.4 composed record -> T-005.2 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.2"
    },
    {
      "id": "CCR-01",
      "kind": "supplied conditional route cases",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json child_case_references",
      "fixture": "skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py",
      "scenarios": [
        "route-cases"
      ],
      "owner_test": "tests/test_bounded_task_implementer.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py route-cases",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace (T-003.1-.3 owner staging; reused, not restaged here)",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json CCR-01; tests/test_bounded_task_implementer.py; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "nineteen supplied route cases map conditional-stage policy and current/stale stage evidence to the expected submission route; the child owns the case setup and oracles",
      "producer_consumer": "T-003.1-.3 child-owned cases -> T-003.4 CCR-01 reference -> T-005.5 actual role calls (used_for ROUTE-01 (V-01))",
      "owning_leaf": "T-005.5",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_bounded_task_implementer.py",
      "role_boundary": "unrun: supplied child-owned inputs, never observed role outputs; actual compliance owned by T-005.5"
    },
    {
      "id": "CCR-02",
      "kind": "supplied change-effect cases",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json child_case_references",
      "fixture": "skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py",
      "scenarios": [
        "route-cases"
      ],
      "owner_test": "tests/test_bounded_task_implementer.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py route-cases",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace (T-003.1-.3 owner staging; reused, not restaged here)",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json CCR-02; tests/test_bounded_task_implementer.py; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "nine change-effect cases route by actual changed bytes and current proof; the genuine reference contract rejects the boolean revision while the executable-reference defect admits it despite its label",
      "producer_consumer": "T-003.1-.3 child-owned cases -> T-003.4 CCR-02 reference -> T-005.5 actual role calls (used_for EFF-01 (V-05))",
      "owning_leaf": "T-005.5",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_bounded_task_implementer.py",
      "role_boundary": "unrun: supplied child-owned inputs, never observed role outputs; actual compliance owned by T-005.5"
    },
    {
      "id": "CCR-03",
      "kind": "supplied correction record and owned stop",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json child_case_references",
      "fixture": "skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py",
      "scenarios": [
        "record-correction"
      ],
      "owner_test": "tests/test_bounded_task_implementer.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py record-correction",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace (T-003.1-.3 owner staging; reused, not restaged here)",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json CCR-03; tests/test_bounded_task_implementer.py; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "four row states keep stable identities through correction; two failed fixes of one target end in an owned non-complete stop with unfinished rows and a next owner",
      "producer_consumer": "T-003.1-.3 child-owned cases -> T-003.4 CCR-03 reference -> T-005.5 actual role calls (used_for ROWS-01 (V-03))",
      "owning_leaf": "T-005.5",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_bounded_task_implementer.py",
      "role_boundary": "unrun: supplied child-owned inputs, never observed role outputs; actual compliance owned by T-005.5"
    },
    {
      "id": "CCR-04",
      "kind": "four confirmed maintainability blockers plus a genuine stop",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json child_case_references",
      "fixture": "skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py",
      "scenarios": [
        "four-blockers",
        "genuine-stop"
      ],
      "owner_test": "tests/test_task_maintainability_review.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py four-blockers; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py genuine-stop",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace (T-003.1-.3 owner staging; reused, not restaged here)",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json CCR-04; tests/test_task_maintainability_review.py; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "four independent defect oracles MNT-B1-MNT-B4 with a non-blocking preference control remain four; the genuine stop preserves outstanding coverage and its next owner",
      "producer_consumer": "T-003.1-.3 child-owned cases -> T-003.4 CCR-04 reference -> T-005.5 actual role calls (used_for FIND-01 (V-02))",
      "owning_leaf": "T-005.5",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_maintainability_review.py",
      "role_boundary": "unrun: supplied child-owned inputs, never observed role outputs; actual compliance owned by T-005.5"
    },
    {
      "id": "CCR-05",
      "kind": "mixed-condition decision inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json child_case_references",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "scenarios": [
        "mixed-conditions-authorized-decision",
        "mixed-conditions-forbidden-decision"
      ],
      "owner_test": "tests/test_contextual_uncertainty_inputs.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py mixed-conditions-authorized-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py mixed-conditions-forbidden-decision",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace (T-003.1-.3 owner staging; reused, not restaged here)",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json CCR-05; tests/test_contextual_uncertainty_inputs.py; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "a confirmed blocker plus a blocked missing-proof row stay visible together; authorized bounded correction keeps CHANGES_REQUESTED while the run policy that denies production edits keeps INCONCLUSIVE",
      "producer_consumer": "T-003.1-.3 child-owned cases -> T-003.4 CCR-05 reference -> T-005.3 actual role calls (used_for ROWS-01 (V-03))",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_contextual_uncertainty_inputs.py",
      "role_boundary": "unrun: supplied child-owned inputs, never observed role outputs; actual compliance owned by T-005.3"
    },
    {
      "id": "CCR-06",
      "kind": "late-omission recovery inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json child_case_references",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "scenarios": [
        "discovery-late-omission-clean",
        "discovery-late-omission-fail"
      ],
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-clean; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-fail",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace (T-003.1-.3 owner staging; reused, not restaged here)",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json CCR-06; tests/test_task_review_discovery.py; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "the earlier aggregate stays explicitly premature; the omitted row receives current targeted proof before discovery reconsiders a still-justified aggregate",
      "producer_consumer": "T-003.1-.3 child-owned cases -> T-003.4 CCR-06 reference -> T-005.5 actual role calls (used_for GATE-01 (V-06, V-07))",
      "owning_leaf": "T-005.5",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: supplied child-owned inputs, never observed role outputs; actual compliance owned by T-005.5"
    },
    {
      "id": "CCR-07",
      "kind": "readiness revision-recovery inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json child_case_references",
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "scenarios": [
        "revision-recovery"
      ],
      "owner_test": "tests/test_task_preflight.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py revision-recovery",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace (T-003.1-.3 owner staging; reused, not restaged here)",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json CCR-07; tests/test_task_preflight.py; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "affected old readiness is superseded; focused ready for the new revision precedes revised evidence and the new decision; changed requirements return to design",
      "producer_consumer": "T-003.1-.3 child-owned cases -> T-003.4 CCR-07 reference -> T-005.2 actual role calls (used_for REV-01 (V-04))",
      "owning_leaf": "T-005.2",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_preflight.py",
      "role_boundary": "unrun: supplied child-owned inputs, never observed role outputs; actual compliance owned by T-005.2"
    },
    {
      "id": "CCR-08",
      "kind": "repeated-review disposition inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json child_case_references",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "scenarios": [
        "repeated-review-formerly-blocked-evidence-decision",
        "repeated-review-missed-existing-obligation-decision",
        "repeated-review-changed-context-authority-decision",
        "repeated-review-newly-demonstrated-material-risk-decision"
      ],
      "owner_test": "tests/test_task_acceptance_review.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py repeated-review-formerly-blocked-evidence-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py repeated-review-missed-existing-obligation-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py repeated-review-changed-context-authority-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py repeated-review-newly-demonstrated-material-risk-decision",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace (T-003.1-.3 owner staging; reused, not restaged here)",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json CCR-08; tests/test_task_acceptance_review.py; docs/tasks/T-005/brief.md evidence rule 1",
      "expected_oracle": "unchanged compatible exposure retains the accepted disposition while a demonstrated current regression or missed obligation stays visible with its justified reopening reason",
      "producer_consumer": "T-003.1-.3 child-owned cases -> T-003.4 CCR-08 reference -> T-005.3 actual role calls (used_for DISP-01 (V-08))",
      "owning_leaf": "T-005.3",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_acceptance_review.py",
      "role_boundary": "unrun: supplied child-owned inputs, never observed role outputs; actual compliance owned by T-005.3"
    },
    {
      "id": "ROUTE-01",
      "kind": "conditional submission route matrix reconciled across the overviews, the implementer template, and the installed guide",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json records (ROUTE-01); case_source CCR-01",
      "fixture": "skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py",
      "scenarios": [
        "route-cases"
      ],
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py route-cases",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace staging via the case_source CCR reference",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json ROUTE-01 record; docs/tasks/T-005/brief.md evidence rules 1 and 5",
      "expected_oracle": "ROUTE-01 record semantics: conditional submission route matrix reconciled across the overviews, the implementer template, and the installed guide",
      "producer_consumer": "T-003.4 ROUTE-01 composed record -> T-005.5 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.5",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.5"
    },
    {
      "id": "FIND-01",
      "kind": "four confirmed maintainability findings reach the correction input without truncation",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json records (FIND-01); case_source CCR-04",
      "fixture": "skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py",
      "scenarios": [
        "four-blockers",
        "genuine-stop"
      ],
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py four-blockers; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py genuine-stop",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace staging via the case_source CCR reference",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json FIND-01 record; docs/tasks/T-005/brief.md evidence rules 1 and 5",
      "expected_oracle": "FIND-01 record semantics: four confirmed maintainability findings reach the correction input without truncation",
      "producer_consumer": "T-003.4 FIND-01 composed record -> T-005.5 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.5",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.5"
    },
    {
      "id": "ROWS-01",
      "kind": "stable row identities, owned stop history, and mixed-condition routes across correction",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json records (ROWS-01); case_source CCR-03",
      "fixture": "skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py",
      "scenarios": [
        "record-correction"
      ],
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py record-correction",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace staging via the case_source CCR reference",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json ROWS-01 record; docs/tasks/T-005/brief.md evidence rules 1 and 5",
      "expected_oracle": "ROWS-01 record semantics: stable row identities, owned stop history, and mixed-condition routes across correction",
      "producer_consumer": "T-003.4 ROWS-01 composed record -> T-005.5 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.5",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.5"
    },
    {
      "id": "REV-01",
      "kind": "revision recovery rejects obsolete readiness even after recovery",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json records (REV-01); case_source CCR-07",
      "fixture": "skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py",
      "scenarios": [
        "revision-recovery"
      ],
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py revision-recovery",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace staging via the case_source CCR reference",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json REV-01 record; docs/tasks/T-005/brief.md evidence rules 1 and 5",
      "expected_oracle": "REV-01 record semantics: revision recovery rejects obsolete readiness even after recovery",
      "producer_consumer": "T-003.4 REV-01 composed record -> T-005.2 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.2",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.2"
    },
    {
      "id": "EFF-01",
      "kind": "actual effects distinguish reference, evidence, and production routes",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json records (EFF-01); case_source CCR-02",
      "fixture": "skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py",
      "scenarios": [
        "route-cases"
      ],
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py route-cases",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace staging via the case_source CCR reference",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json EFF-01 record; docs/tasks/T-005/brief.md evidence rules 1 and 5",
      "expected_oracle": "EFF-01 record semantics: actual effects distinguish reference, evidence, and production routes",
      "producer_consumer": "T-003.4 EFF-01 composed record -> T-005.5 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.5",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.5"
    },
    {
      "id": "GATE-01",
      "kind": "discovery-owned aggregate record and late-omission recovery",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json records (GATE-01); case_source CCR-06",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "scenarios": [
        "discovery-late-omission-clean",
        "discovery-late-omission-fail"
      ],
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-clean; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-fail",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace staging via the case_source CCR reference",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json GATE-01 record; docs/tasks/T-005/brief.md evidence rules 1 and 5",
      "expected_oracle": "GATE-01 record semantics: discovery-owned aggregate record and late-omission recovery",
      "producer_consumer": "T-003.4 GATE-01 composed record -> T-005.5 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.5",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.5"
    },
    {
      "id": "DISP-01",
      "kind": "stable disposition contrast preserves regression visibility",
      "inherited_from": "tests/fixtures/review-composition/tasks/T-003.4/composition.json records (DISP-01); case_source CCR-08",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "scenarios": [
        "repeated-review-formerly-blocked-evidence-decision",
        "repeated-review-missed-existing-obligation-decision",
        "repeated-review-changed-context-authority-decision",
        "repeated-review-newly-demonstrated-material-risk-decision"
      ],
      "owner_test": "tests/test_review_composition.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py repeated-review-formerly-blocked-evidence-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py repeated-review-missed-existing-obligation-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py repeated-review-changed-context-authority-decision; EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py repeated-review-newly-demonstrated-material-risk-decision",
      "workspace": "child-owned disposable EVAL_WORK_ROOT Git workspace staging via the case_source CCR reference",
      "authority": "tests/fixtures/review-composition/tasks/T-003.4/composition.json DISP-01 record; docs/tasks/T-005/brief.md evidence rules 1 and 5",
      "expected_oracle": "DISP-01 record semantics: stable disposition contrast preserves regression visibility",
      "producer_consumer": "T-003.4 DISP-01 composed record -> T-005.3 actual role calls (staged placeholder replaced by actual producer output at call time)",
      "owning_leaf": "T-005.3",
      "evidence_level": "structural_tests",
      "current_evidence": "tests/test_review_composition.py",
      "role_boundary": "unrun: composed fixture data, never an observed role output; actual compliance owned by T-005.3"
    },
    {
      "id": "IFQ-01",
      "kind": "maintainability correction-round finding-identity inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/INT-FLOW-001/results.md T-005 qualification inputs (I-03)",
      "fixture": "skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py",
      "scenario": "correction-round",
      "owner_test": "tests/test_task_maintainability_review.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py correction-round",
      "workspace": "maintainability-fixture disposable EVAL_WORK_ROOT Git workspace (task-runs/MNT-42)",
      "authority": "tests/fixtures/review-composition/tasks/INT-FLOW-001/results.md T-005 qualification inputs; docs/tasks/INT-FLOW-001/brief.md; docs/tasks/T-005/brief.md evidence rule 3",
      "expected_oracle": "three survivors keep IDs despite reorder; MNT-B2 keeps its ID with a corrected disposition; a new finding takes the next unused identity (MNT-B5); prior report bytes unchanged; next durable report is maintainability-02.md",
      "producer_consumer": "task-maintainability-review produces stable finding IDs and the conditional-remainder handoff; the correction implementer and fresh maintainability review consume the prior report and correction facts (INT-FLOW-001 results.md)",
      "owning_leaf": "T-005.5",
      "intflow_provenance": "`task-maintainability-review` eval case 4 (correction-round identity continuity)",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/fixtures/review-composition/tasks/T-005.1/evidence/V-02-setup-reconstruction.md (unrun-handoff receipt); tests/test_task_maintainability_review.py",
      "role_boundary": "unrun: role call (maintainability eval case 4 style) owned by T-005.5; this inventory supplies inputs only"
    },
    {
      "id": "IFQ-02",
      "kind": "verification-designer integration-leaf permission inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/INT-FLOW-001/results.md T-005 qualification inputs (I-05)",
      "fixture": "skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py",
      "scenario": "integration-leaf",
      "owner_test": "tests/test_task_preparation_contracts.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py integration-leaf",
      "workspace": "verification-designer-fixture disposable EVAL_WORK_ROOT staging",
      "authority": "tests/fixtures/review-composition/tasks/INT-FLOW-001/results.md T-005 qualification inputs; docs/tasks/INT-FLOW-001/brief.md; docs/tasks/T-005/brief.md evidence rule 3",
      "expected_oracle": "the integration leaf's own composition ACs are designed from supplied producer outputs at stated consumer boundaries while the composite parent, sibling requirements and unavailable oracles stay refused",
      "producer_consumer": "the verification designer consumes the INT-9 brief plus producer outputs and produces the leaf's composition scenarios (INT-FLOW-001 results.md)",
      "owning_leaf": "T-005.2",
      "intflow_provenance": "`task-verification-designer` eval case 9 (integration-leaf permission and refusals)",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_preparation_contracts.py",
      "role_boundary": "unrun: role call (verification-designer eval case 9 style) owned by T-005.2; this inventory supplies inputs only"
    },
    {
      "id": "IFQ-03",
      "kind": "discovery preparation-reference handoff inputs",
      "inherited_from": "tests/fixtures/review-composition/tasks/INT-FLOW-001/results.md T-005 qualification inputs (I-04)",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "scenario": "discovery-prepared-ledger",
      "owner_test": "tests/test_task_review_discovery.py",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-prepared-ledger",
      "workspace": "discovery-fixture disposable EVAL_WORK_ROOT Git workspace",
      "authority": "tests/fixtures/review-composition/tasks/INT-FLOW-001/results.md T-005 qualification inputs; docs/tasks/INT-FLOW-001/brief.md; docs/tasks/T-005/brief.md evidence rule 3",
      "expected_oracle": "complete, clean guided discovery handoffs carry the applicable packaged preparation references (verification revision, readiness/preflight, decision context); guided acceptance inputs identify and read them",
      "producer_consumer": "discovery/acceptance consume the preparation references; the supplied prepared package retains brief.md, verification.md and ready preflight.md inputs (INT-FLOW-001 results.md; COMP-05 parity)",
      "owning_leaf": "T-005.3",
      "intflow_provenance": "discovery eval case 11 and the acceptance guided cases supply prepared verification/preflight context for observing preparation-reference handoff and consumption",
      "evidence_level": "actual_behavior",
      "current_evidence": "tests/test_task_review_discovery.py",
      "role_boundary": "unrun: role call (discovery eval case 11 style) owned by T-005.3; this inventory supplies inputs only"
    }
  ]
}
```

## Parent requirements (P-01–P-07) represented with owning leaves

Owning leaves follow [docs/tasks/T-005/brief.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005/brief.md) (coverage and closure). This
leaf (T-005.1) supplies the P-01 inputs and the P-07 evidence distinctions
without claiming sibling role behavior or final ART-012 closure.

| Parent requirement | Owning leaf | T-005.1 supplied inputs |
|---|---|---|
| P-01 reproducible supplied fixtures; current qualified installed copies/helpers; retained public/continuation cases | T-005.1; every call leaf rechecks identity | this inventory; V-03/V-04 projection receipts; INV-CASE-01, 14–17 retention |
| P-02 packaged preparation reaches implementation; direct/refusal contrasts; unchanged-authority revision recovery | T-005.2 | INV-CASE-05, 19–24; COMP-05; CCR-07; REV-01; IFQ-02 |
| P-03 actual discovery/decision, wrong-green rejection, preflight-only exposure, contextual risk, mixed conditions | T-005.3 | INV-CASE-01–03, 06–18; COMP-01/02; CCR-05; CCR-08; DISP-01; IFQ-03 |
| P-04 accepted bounded issue recorded by coordinator and consumed by later preflight | T-005.3 produces the decision; T-005.4 records/consumes it | COMP-04 |
| P-05 conditional-stage matrix, actual-effect routing, complete IDs/rows, blockers, genuine stops, fresh correction proof | T-005.5 (T-005.2 supplies revision recovery) | INV-CASE-04; CCR-01–04, CCR-06; ROUTE-01; FIND-01; ROWS-01; EFF-01; GATE-01; IFQ-01 |
| P-06 failure → correction → clean discovery → decision with one justified aggregate | T-005.5 | COMP-03; CCR-03; ROWS-01; GATE-01; INV-CASE-17 |
| P-07 new ART-012 report, reproducible current claims, structure/runtime/role distinction, explicit unrun gaps | T-005.6 audits T-005.1–.5 | all inventory IDs; the three retained receipts; the unrun-boundary statements below |

## Placeholder replacement instructions for later leaves (AC-04 / V-06)

Each staged producer placeholder below names the raw actual producer output
that must replace it before grading, with provenance and preparation
references. Staged records are supplied history; an actual role call's raw
output must be retained byte-for-byte before any grading. Evaluator setup
code, expected answers and grading oracles stay outside the consuming role's
inputs (parent evidence rule 3).

| Owning leaf | Staged placeholder (supplied history) | Replaced by raw actual output of | Preparation references |
|---|---|---|---|
| T-005.2 | staged `docs/tasks/QR-12/preflight.md` packet and `INT-9`/`INT-PARENT` briefs (fixture data from `queue-defect` / `integration-leaf` staging) | an actual `task-verification-designer` and `task-preflight` invocation over the same package inputs | brief.md, verification.md, preflight.md of the consumed package; INV-CASE-19–24, COMP-05, CCR-07, IFQ-02 |
| T-005.3 | staged discovery reports and decision inputs under the fixture workspaces (e.g. `task-runs/QR-12/discovery-01.md`, mixed-condition and contextual records) | an actual `task-review-discovery` report, then an actual `task-acceptance-review` decision consuming that raw report | COMP-01/02, CCR-05, CCR-08, DISP-01, IFQ-03; expected verdicts and eval expectations stay with the evaluator |
| T-005.4 | `KI-001` deferral record fields (COMP-04 fixture data) | the coordinator's actual recorded deferral in `docs/known-issues.md` (or declared path) after a real accepted decision | COMP-04; [docs/tasks/T-005.4/brief.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005.4/brief.md) |
| T-005.5 | staged prior maintainability report `MNT-42` with `MNT-B1`–`MNT-B4`, staged correction facts and gate records | an actual fresh `task-maintainability-review` output and the actual correction/re-entry evidence with stable finding IDs | FIND-01, ROWS-01, GATE-01, CCR-01–04, IFQ-01 |
| T-005.6 | this inventory and the .1–.5 evidence set | the actual audited ART-012 report beside the dated proposal | `tests/fixtures/review-composition/tasks/T-005.6/brief.md`; all inventory IDs |

## Consumer-visible handoff input manifests (V-06 preparation)

Prepared in the `reviews/discovery-01.md` correction round: every claimed
staged producer-to-consumer handoff above now carries an exact,
machine-auditable input manifest. For each staged input set, the consumer
input set is `consumer_visible_inputs` minus the `evaluator_only` paths —
grading oracles, expected routes and expected next-report identities never
enter the consuming role's inputs. `not_staged_positions` name
producer-output positions that no staging supplies: they are filled only by
the raw actual role-call output of the named producing role, retained
byte-for-byte before any grading. Staged files remain supplied history,
never current role results. `tests/test_review_composition.py`
(`T0051QualificationInputTests`) stages every fixture-backed set and audits
these manifests: a missing handoff row, an unresolved input path, a
misclassified held-back record, an invented unstaged position or a stale
fixture scenario fails the audit, and a deliberately degraded manifest copy
is rejected problem-by-problem instead of accepted as green-looking rows.

F-02 correction: use the manifest's setup command for consumer assembly,
not the inventory's original evaluator fixture command. For `route-cases`,
`setup_consumer.py route-cases` reuses that fixture and produces two separate
roots: `route-cases` is evaluator-only staging, and `route-consumer` is the
consumer workspace. Grant only `route-consumer`, never its enclosing
`EVAL_WORK_ROOT` or the original `route-cases` repository. The consumer has
identical review files except `change-effects/cases.json`; its fresh clean Git
baseline contains no original objects, index, refs, reflogs or configuration.
The before/after change-effect files and task policy/context remain available.
Commit IDs are new supplied-fixture identities, not historical producer IDs;
later leaves must record these current identities in their actual preparation.
For every directory input, exclusion applies to accessible worktree, index
and all Git objects, including unreachable objects; deleting a file alone is
insufficient. Other held-back records remain outside their consumer roots.
The task-local setup code and evaluator roots are never consumer inputs.

```json
{
  "task": "T-005.1",
  "artifact": "consumer-visible handoff input manifests (V-06 preparation)",
  "status": "supplied input manifests composed from current fixture staging; never observed role outputs",
  "producers": [
    "bounded-task-implementer (T-005.1 correction round) composed these manifests from the staged fixture workspaces; no skill-call agent produced or consumed them"
  ],
  "consumer_input_rule": "per staged set, the consumer input set is consumer_visible_inputs minus evaluator_only paths; staged files are supplied history; raw actual role-call outputs replace placeholders and are retained byte-for-byte before grading",
  "staged_input_sets": [
    {
      "staging_id": "queue-defect",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "scenario": "queue-defect",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py queue-defect",
      "inventory_refs": ["INV-CASE-01"],
      "consumer_visible_inputs": ["queue-runner", "task-runs/QR-12/worker-result.json", "task-runs/policies/local-review-v1.json"],
      "evaluator_only": [],
      "not_staged_positions": [
        {
          "path": "task-runs/QR-12/discovery-01.md",
          "filled_by": "raw actual T-005.3 task-review-discovery role-call output over the QR-12 workspace; the placeholder-table example is a fill position, not a staged file"
        }
      ]
    },
    {
      "staging_id": "integration-leaf",
      "fixture": "skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py",
      "scenario": "integration-leaf",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py integration-leaf",
      "inventory_refs": ["IFQ-02"],
      "consumer_visible_inputs": ["integration-leaf"],
      "evaluator_only": [],
      "not_staged_positions": [
        {
          "path": "integration-leaf/docs/tasks/INT-9/verification.md",
          "filled_by": "raw actual task-verification-designer role-call output (the INT-9 leaf verification design)"
        }
      ]
    },
    {
      "staging_id": "mixed-conditions-authorized-decision",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "scenario": "mixed-conditions-authorized-decision",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py mixed-conditions-authorized-decision",
      "inventory_refs": ["INV-CASE-06", "COMP-02", "CCR-05"],
      "consumer_visible_inputs": ["mixed-runner", "task-runs/JOB-05/discovery-01.md", "task-runs/JOB-05/worker-result.json", "task-runs/policies/local-review-mixed.json"],
      "evaluator_only": [],
      "not_staged_positions": []
    },
    {
      "staging_id": "contextual-risk-blockers-decision",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "scenario": "contextual-risk-blockers-decision",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py contextual-risk-blockers-decision",
      "inventory_refs": ["COMP-01"],
      "consumer_visible_inputs": ["contextual-runner", "task-runs/INV-07/discovery-01.md", "task-runs/INV-07/worker-result.json"],
      "evaluator_only": [],
      "not_staged_positions": []
    },
    {
      "staging_id": "known-issue-consumption-decision",
      "fixture": "skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py",
      "scenario": "known-issue-consumption-decision",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py known-issue-consumption-decision",
      "inventory_refs": ["COMP-04"],
      "consumer_visible_inputs": ["ledger-consumer", "task-runs/RPT-12B/discovery-01.md", "task-runs/RPT-12B/worker-result.json"],
      "evaluator_only": [],
      "not_staged_positions": []
    },
    {
      "staging_id": "four-blockers",
      "fixture": "skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py",
      "scenario": "four-blockers",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py four-blockers",
      "inventory_refs": ["CCR-04", "FIND-01"],
      "consumer_visible_inputs": ["maintainability"],
      "evaluator_only": [
        {
          "path": "task-runs/MNT-42/maintainability-oracle.md",
          "reason": "held-back grading oracle that stays outside the reviewer workspace per the fixture's own contract; expected MNT-B1–MNT-B4 findings, the non-blocking preference control and the reporting expectations are expected answers, never reviewer inputs"
        }
      ],
      "not_staged_positions": [
        {
          "path": "maintainability/docs/tasks/MNT-42/reviews/maintainability-01.md",
          "filled_by": "raw actual task-maintainability-review role-call output (the first durable MNT-42 report naming MNT-B1–MNT-B4)"
        }
      ]
    },
    {
      "staging_id": "correction-round",
      "fixture": "skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py",
      "scenario": "correction-round",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py correction-round",
      "inventory_refs": ["IFQ-01"],
      "consumer_visible_inputs": ["maintainability-correction"],
      "evaluator_only": [
        {
          "path": "task-runs/MNT-42/correction-round-facts.md",
          "reason": "held-back record outside the reviewer workspace per the fixture's own contract; carries the applied-correction facts and the expected next-report identity obligations (expected answers: MNT-B1/B3/B4 keep their IDs, MNT-B2 keeps its ID with disposition corrected, the next new finding takes MNT-B5) that stay evaluator-side unless separated from the correction facts before consumption"
        }
      ],
      "not_staged_positions": [
        {
          "path": "maintainability-correction/docs/tasks/MNT-42/reviews/maintainability-02.md",
          "filled_by": "raw actual next task-maintainability-review role-call output (the next durable report with stable finding IDs)"
        }
      ]
    },
    {
      "staging_id": "route-cases",
      "fixture": "tests/fixtures/review-composition/tasks/T-005.1/setup_consumer.py",
      "scenario": "route-cases",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 tests/fixtures/review-composition/tasks/T-005.1/setup_consumer.py route-cases",
      "inventory_refs": ["CCR-01", "CCR-02", "ROUTE-01", "EFF-01"],
      "consumer_visible_inputs": ["route-consumer"],
      "evaluator_only": [
        {
          "path": "route-cases/change-effects/cases.json",
          "reason": "expected submission routes for the nine change-effect cases — expected answers the role must derive from the changed bytes and policy; retained only in the evaluator staging; route-consumer has a fresh Git baseline without this file or its objects"
        }
      ],
      "not_staged_positions": []
    },
    {
      "staging_id": "record-correction",
      "fixture": "skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py",
      "scenario": "record-correction",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py record-correction",
      "inventory_refs": ["CCR-03", "ROWS-01"],
      "consumer_visible_inputs": ["result-record"],
      "evaluator_only": [],
      "not_staged_positions": []
    },
    {
      "staging_id": "discovery-late-omission-clean",
      "fixture": "skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py",
      "scenario": "discovery-late-omission-clean",
      "setup": "EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-late-omission-clean",
      "inventory_refs": ["INV-CASE-09", "INV-CASE-12", "CCR-06", "GATE-01"],
      "consumer_visible_inputs": ["late-omission", "task-runs/LED-05/worker-result.json", "task-runs/policies/local-review-v1.json"],
      "evaluator_only": [],
      "not_staged_positions": [
        {
          "path": "late-omission/docs/tasks/LED-05/reviews/discovery-02.md",
          "filled_by": "raw actual T-005.5 discovery reconsideration output once the omitted row has current targeted proof"
        }
      ]
    },
    {
      "staging_id": "t0051-package",
      "fixture": null,
      "scenario": null,
      "setup": "none: repository artifacts resolved against the repository root",
      "inventory_refs": [],
      "consumer_visible_inputs": [
        "tests/fixtures/review-composition/tasks/T-005.1/fixtures.md",
        "tests/fixtures/review-composition/tasks/T-005.1/results.md",
        "tests/fixtures/review-composition/tasks/T-005.1/evidence/V-02-setup-reconstruction.md",
        "tests/fixtures/review-composition/tasks/T-005.1/evidence/V-03-install-projection.md",
        "tests/fixtures/review-composition/tasks/T-005.1/evidence/V-04-drift-contrast.md"
      ],
      "evaluator_only": [],
      "not_staged_positions": []
    }
  ],
  "handoff_manifests": [
    {
      "owning_leaf": "T-005.2",
      "staged_placeholder": "staged QR-12 package/preflight packet and INT-9/INT-PARENT briefs (supplied history)",
      "replaced_by": "raw actual outputs of the actual task-verification-designer and task-preflight invocations over the same package inputs",
      "staging_refs": ["queue-defect", "integration-leaf"],
      "preparation_references": ["INV-CASE-19", "INV-CASE-20", "INV-CASE-21", "INV-CASE-22", "INV-CASE-23", "INV-CASE-24", "COMP-05", "CCR-07", "IFQ-02"]
    },
    {
      "owning_leaf": "T-005.3",
      "staged_placeholder": "staged prior discovery reports and decision inputs (task-runs/JOB-05/discovery-01.md, task-runs/INV-07/discovery-01.md, staged QR-12 worker-result/policy); task-runs/QR-12/discovery-01.md is the unstaged position the actual discovery call fills",
      "replaced_by": "raw actual task-review-discovery report, then the raw actual task-acceptance-review decision consuming that raw report",
      "staging_refs": ["queue-defect", "mixed-conditions-authorized-decision", "contextual-risk-blockers-decision"],
      "preparation_references": ["COMP-01", "COMP-02", "CCR-05", "CCR-08", "DISP-01", "IFQ-03"]
    },
    {
      "owning_leaf": "T-005.4",
      "staged_placeholder": "staged KI-001 deferral record (ledger-consumer/docs/known-issues.md, supplied history)",
      "replaced_by": "the coordinator's actual recorded deferral in docs/known-issues.md (or declared path) after a real accepted decision",
      "staging_refs": ["known-issue-consumption-decision"],
      "preparation_references": ["COMP-04"]
    },
    {
      "owning_leaf": "T-005.5",
      "staged_placeholder": "staged prior maintainability report MNT-42 (MNT-B1–MNT-B4, supplied history), held-back correction facts and grading oracle, staged route/gate/correction case records",
      "replaced_by": "raw actual fresh task-maintainability-review output and the actual correction/re-entry evidence with stable finding IDs",
      "staging_refs": ["four-blockers", "correction-round", "route-cases", "record-correction", "discovery-late-omission-clean"],
      "preparation_references": ["FIND-01", "ROWS-01", "GATE-01", "CCR-01", "CCR-02", "CCR-03", "CCR-04", "IFQ-01"]
    },
    {
      "owning_leaf": "T-005.6",
      "staged_placeholder": "this inventory and the .1–.5 evidence set (supplied inputs)",
      "replaced_by": "the actual audited ART-012 report beside the dated proposal",
      "staging_refs": ["t0051-package"],
      "preparation_references": ["tests/fixtures/review-composition/tasks/T-005.6/brief.md"]
    }
  ]
}
```

## Retained receipts and unrun boundaries

- `evidence/V-02-setup-reconstruction.md` — one public-boundary case (INV-CASE-01
  `queue-defect`) and one unrun handoff (IFQ-01 `correction-round`)
  reconstructed from the supplied setup in fresh disposable workspaces; the
  public probe's observable result and the unrun handoff's retained
  reason/owner are recorded. No role call was launched.
- `evidence/V-03-install-projection.md` — fresh disposable Git-target
  installation receipts (corrected for discovery-01 F-01): canonical install +
  read-only `--check` match; an independent full managed-projection
  comparison covering the complete managed file set, all 85 copied file
  bytes and the marked `AGENTS.md` block, with the exact reproducible
  invocation retained; a marked-block replacement recheck on the existing
  target; target-local sibling `.agents/scripts/` helper availability; and
  workflow identity recorded as workflow-identity evidence only, distinct
  from full projection identity.
- `evidence/V-04-drift-contrast.md` — fingerprint-excluded drift
  demonstration: a copied eval/setup file changed in the disposable target
  only keeps workflow identity matching while `--check` reports drift and the
  independent comparison names the changed file; no fault is left in a target
  presented as qualified.
- Unrun boundaries: every actual role call, conditional-stage call, durable
  report writing and behavioral qualification. Owners: T-005.2–.6 per the
  parent brief; the dependency acceptance dispositions recorded as owed in
  [docs/tasks/T-005.1/preflight.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005.1/preflight.md) remain owed.
