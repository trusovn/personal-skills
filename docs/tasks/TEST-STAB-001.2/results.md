# Results: TEST-STAB-001.2 — Consolidate test setup and incidental assertions

Status: implementation complete; handed to review (not independently reviewed).

Baseline confirmed green before any edit (focused gates 6/5/6/9/11). No .1
artifact was modified; this delta map extends `.1/results.md`'s fixed
ownership map. Test counts are unchanged everywhere: no test was added,
dropped, skipped, or relabeled.

## Delta map: .1 evidence rows → owner / consolidation

| .1 evidence row | Disposition | Protected defect | Current execution result |
|---|---|---|---|
| `ReviewerDisciplineTests` acceptance checks (7) | Unchanged owner | acceptance admission / disposition contract | 7 pass in union |
| `ReviewerDisciplineTests` senior-review prerequisites (2) | Unchanged owner | senior-review reference prerequisites | 2 pass in union |
| `ReviewDiscoveryDisciplineTests` (12) | Unchanged owner | discovery contract + fixture parity | 12 pass in union |
| `DiscoveryLateOmissionFixtureTests` (2) | Unchanged owner | late-omission validator exits | 2 pass in union |
| `AcceptanceAdmissionEvalTests` (2) | Unchanged owner | admission eval metadata | 2 pass in union |
| `ContextualDispositionContractTests` (8) | Unchanged owner | contextual disposition contract | 8 pass in union |
| `ContextualDispositionEvalTests` (2) | Unchanged owner | disposition eval metadata | 2 pass in union |
| `ContextualRiskFixtureTests` eval-metadata (2) | Unchanged owner | mixed/optional-link eval metadata | 2 pass in union |
| `ContextualRiskFixtureTests` export/consumer probes (6) | Surviving owner `test_contextual_export_risks.py`; staging via shared helper | destructive vs mitigated export; consumer contract; `--clean`; duplicated parsing | 6 pass (module run) |
| `ContextualRiskFixtureTests` uncertainty/mixed probes (5) | Surviving owner `test_contextual_uncertainty_inputs.py`; staging via shared helper | readiness-only exposure; mixed conditions; retention/region | 5 pass (module run) |
| `ContextualRiskFixtureTests` known-issue/repeated-review probes (6) | Surviving owner `test_contextual_known_issues.py`; staging via shared helper | known-issue fields; regression retry; repeated-review reasons | 6 pass (module run) |
| `ComposedReviewFlowGuideTests` (11) | Unchanged owner | flow-guide composition checks | 11 pass in union |
| `ComposedQualificationSetupTests` (9) | Surviving owner `test_review_composition.py`; staging via shared helper; one consolidation (below) | COMP-01–05 records, INV-CASE-01–24 inventory, T-005 unrun boundaries | 9 pass (module run) |
| `PreflightContractTest` (7) | Unchanged owner | preflight stage contract | 7 pass in union |
| `ImplementerContractTest` (9) | Unchanged owner | implementer entry contract | 9 pass in union |
| `TaskBriefDesignerPackageTest` cross-skill checks (11) | Surviving owner `test_task_preparation_contracts.py`; preparation assertion whitespace-normalized | both stages + order still required; all other contract assertions preserved | 11 pass (module run) |
| `TaskBriefDesignerPackageTest` designer-local (3) | Unchanged owner | packaged designer resources | 3 pass (designer suite) |

Consolidation row (removed composition export probes): the two malformed-invoice
export subprocess blocks removed from
`ComposedQualificationSetupTests.test_preflight_only_exposure_survives_into_discovery_and_decision_inputs`
use the same inputs (invoices `inv-1`/`inv-2` with malformed `oops`, seeded
`out/ledger.csv` bytes `inv-9001,10.00\n`) and the same oracle (nonzero exit;
empty ledger for risky, preserved seed bytes for mitigated) as the surviving
canonical owners `test_failed_risky_export_destroys_the_existing_ledger` and
`test_failed_mitigated_export_preserves_the_existing_ledger`. Both survive and
pass. The composition test keeps its COMP-01-specific assertions (preflight-only
exposure present in preflight and supplied discovery input, absent from the
staged discovery report, `CHANGES_REQUESTED` route and material-risk decision
obligations); a comment in the test documents this separation. No other .1 row
was consolidated.

## Verification evidence

Focused gates (fresh process per module, repository root,
`PYTHONDONTWRITEBYTECODE=1`), post-edit, all green:

```sh
python3 -m unittest discover -s tests -p test_contextual_export_risks.py         # 6 OK
python3 -m unittest discover -s tests -p test_contextual_uncertainty_inputs.py   # 5 OK
python3 -m unittest discover -s tests -p test_contextual_known_issues.py         # 6 OK
python3 -m unittest discover -s tests -p test_review_composition.py              # 9 OK
python3 -m unittest discover -s tests -p test_task_preparation_contracts.py      # 11 OK
```

Aggregate owning union, then designer and installer suites, sequential, all green:

```sh
PYTHONPATH=tests python3 -m unittest test_task_acceptance_review test_task_review_discovery \
  test_senior_review_discipline test_task_flow_guides test_review_composition \
  test_contextual_export_risks test_contextual_uncertainty_inputs \
  test_contextual_known_issues test_task_preflight test_bounded_task_implementer \
  test_task_preparation_contracts                                                  # 101 OK
python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py  # 3 OK
python3 -m unittest discover -s tests -p test_install_development_skills.py       # 14 OK
```

Disposable experiments (removed after use; no permanent harness):

- V-01: two successive `stage_setup` invocations returned distinct
  `EVAL_WORK_ROOT`s staging their own `contextual-runner` workspaces; after
  `doCleanups()` neither root survived. PASS.
- V-02: staging an unregistered scenario name raised `SetupStagingError`
  carrying the scenario and the setup subprocess exit/stderr diagnostics
  (`exit 1` + usage output); the failed invocation's temp root did not survive
  cleanup. PASS.
- V-05: the changed preparation assertion, applied to disposable text files,
  accepted the original passage and a whitespace-only reflow, and rejected
  missing-verification, missing-readiness, and reversed-sequence variants.
  PASS. Source guidance was not modified.

Independent-package boundary (V-07): copies of the acceptance and discovery
packages staged `contextual-risk-blockers-decision` and
`discovery-late-omission-clean` from an unrelated cwd with `python3 -I`, a
fresh `EVAL_WORK_ROOT`, and no `PYTHONPATH`/repository import access — both
exited 0 and produced their workspaces (`contextual-runner`/`task-runs`,
`late-omission`/`task-runs`). No skill/eval imports the staging helper (it
lives under `tests/` and imports only stdlib). PASS.

## Evidence categories

- Structural protection: inherited discovery fixture source-parity guard, role
  adaptations and scenario registrations unchanged (union row `test_task_review_discovery.py` 14 pass; `test_task_acceptance_review.py` 21 pass). No skip,
  no weakened oracle, no changed expected failure, no source guidance edited.
- Observed fixture behavior: subprocess probes above (exports, consumers,
  claims, retention, retry, validator) are real staged-fixture observations.
- Unrun T-005 agent compliance: unchanged — `ComposedQualificationSetupTests`
  still asserts the `t005_unrun_boundaries` records; this cleanup qualifies
  nothing.

## Changed surfaces

- `tests/staging_fixture_support.py` (new): repository-only `stage_setup`
  operation — per-invocation `TemporaryDirectory`/`EVAL_WORK_ROOT`, cleanup via
  the test case, and `SetupStagingError` carrying scenario + captured
  subprocess exit/stderr on failure. Not a configurable fixture framework; no
  shared mutable state; never imported by skill/eval code.
- `tests/test_contextual_export_risks.py`,
  `tests/test_contextual_uncertainty_inputs.py`,
  `tests/test_contextual_known_issues.py`,
  `tests/test_review_composition.py`: `stage` methods now delegate to the
  helper (scenario choices, paths, data and assertions stay in the tests); the
  composition test's duplicate export probes removed with a documenting note.
- `tests/test_task_preparation_contracts.py`: preparation assertion now
  matches `"derived `verification.md`, then a ready `preflight.md`"` against
  whitespace-normalized designer text (both stages and their order retained;
  every other assertion unchanged).
- `tests/README.md`: shared-support paragraph names the new helper.
- This file (new delta map). Read-only surfaces and all `.1` artifacts untouched.

## Residual gaps

- Local Git object store still misses the HEAD tree object (`git diff HEAD`
  fails); change sets were determined via `git diff-files` and
  `git ls-files --others`. Pre-existing, out of scope to repair.
- Best-effort run-evidence instrumentation could not start: `run_evidence.py
  begin` fails on the same missing HEAD tree. Recorded evidence above directly.
- `.DS_Store` files untouched.

## Next

Fresh independent `task-review-discovery`, then a separate fresh
`task-acceptance-review`, per the brief's follow-on sequence.
