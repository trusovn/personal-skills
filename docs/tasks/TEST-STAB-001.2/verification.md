# Verification Design: TEST-STAB-001.2 — Consolidate test setup and incidental assertions

Source brief: docs/tasks/TEST-STAB-001.2/brief.md
Source brief revision: SHA-256 `4ae8ce1d11be7f1ac484f1afae108a0e9a390ba97687aaa6df5bbede913f3389`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

The parent brief, root `AGENTS.md`, and project-local
`.agents/skills/testing-discipline/SKILL.md` govern evidence preservation.
Use `.1/results.md` in `docs/tasks/TEST-STAB-001.1/` as the fixed ownership map,
`tests/README.md` for current navigation, and `.1/reviews/discovery-01.md`
for the copied-package setup inventory. These are existing evidence inputs;
this design neither reopens .1 ownership nor verifies sibling implementation.
Ready means the verification design is complete, not that implementation or
preflight has passed.

## Coverage summary

Risk IDs below label the brief's five risk-table rows in their original order.

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 — Local reuse | V-01, V-02, V-07 | Shared repository operation; independent state, failure diagnostics and package boundary. |
| AC-02 — Distinct evidence retained | V-03, V-04, V-06 | Same-input export replacements; unique composition and consumer/parser evidence retained. |
| AC-03 — Stable text protection | V-05, V-06 | Reflow accepted; missing/reversed stages rejected; other assertions unchanged. |
| AC-04 — Full preservation | V-04, V-06, V-08 | Each .1 evidence row reconciled; finite inputs, permissions, parity and expected failures preserved. |
| AC-05 — Closure | V-07, V-08 | Real isolated setup, installer and mapped execution; truthful evidence categories. |
| R-01 — Reuse leaks state or masks a setup failure | V-01, V-02 | Distinct disposable roots and cleanup on both success and failure. |
| R-02 — Consolidation loses destructive/mitigated contrast | V-03 | Nonzero CLI exit plus empty/preserved seeded ledger. |
| R-03 — Composition mapping is lost | V-04, V-06 | COMP-01–05 and INV-CASE-01–24 retained at their existing boundaries. |
| R-04 — Text assertion becomes permissive | V-05 | Disposable text contrasts exercise the changed assertion itself. |
| R-05 — Independence/import or install regression | V-07, V-08 | Copied setup subprocesses and unchanged real installer checks. |

## Verification scenarios

### V-01 — Reused staging keeps each invocation independent

Covers: AC-01, R-01

Intent: Reject shared mutable workspaces, execution-order dependence or a helper
that only one relocated consumer actually uses.

Given:
- The contextual export, uncertainty and known-issue modules and the composition
  module retain their existing scenarios and use one repository-only staging
  operation.
- Each invocation starts with its own disposable `EVAL_WORK_ROOT`.

When:
- Run each consumer module alone in a fresh process using the focused selectors
  below.
- Observe two successive staging invocations, including existing tests that
  stage contrasting fixtures, through their normal cleanup lifecycle.

Then:
- Every standalone consumer run passes without another module's state.
- The two roots differ, and the later invocation does not overwrite or consume
  the earlier invocation's staged state.
- After cleanup, neither temporary root nor its generated files survives.
- Scenario choices, meaningful paths, inputs and assertions remain with the
  tests; the reusable operation is not a configurable fixture framework.

Oracle / boundary:
- Real setup subprocesses and filesystem roots before and after cleanup prove
  isolation. Inspect consumer wiring to confirm one shared repository operation;
  that inspection alone cannot prove runtime independence.

Variants:
- The three contextual owners and composition; successive same/contrasting
  existing setups exercise the per-invocation invariant without new evals.

### V-02 — Failed setup retains diagnostics and releases its workspace

Covers: AC-01, R-01

Intent: Reject a helper that hides the scenario or captured subprocess failure,
returns a partial workspace as success, or leaks state on the error path.

Given:
- A disposable invocation of the shared staging operation uses an unchanged
  existing setup program and a name absent from its scenario registration.

When:
- Invoke staging, observe the setup rejection, and complete the caller's normal
  cleanup lifecycle.

Then:
- Staging fails rather than returning successful setup evidence.
- Failure diagnostics identify the supplied scenario and subprocess exit and
  stderr diagnostics; captured setup failure information is available.
- The failed invocation's temporary root and generated state do not survive
  cleanup.

Oracle / boundary:
- Observe the real setup process rejection, surfaced failure diagnostics and
  filesystem cleanup. A temporary local experiment is enough; no permanent
  mutation harness or generator edit is required.

Variants:
- none

### V-03 — Canonical export probes preserve both failure outcomes

Covers: AC-02, R-02

Intent: Reject consolidation that observes only failure status or loses the
opposite persisted-state outcomes.

Given:
- Stage `contextual-risk-blockers-decision` and
  `contextual-risk-mitigated-decision` in separate roots.
- In each `contextual-runner`, seed `out/ledger.csv` with the bytes
  `inv-9001,10.00\n` and provide invoices
  `[{"id":"inv-1","amount":"5.25"},{"id":"inv-2","amount":"oops"}]`.

When:
- Execute the existing public `python -m src.invoices.export` CLI with those
  invoice and output paths in each staged runner.

Then:
- Both CLI invocations exit nonzero.
- The risky ledger is empty; the mitigated ledger retains the exact seed bytes.
- These outcomes remain owned by
  `ContextualExportRiskFixtureTests.test_failed_risky_export_destroys_the_existing_ledger`
  and `test_failed_mitigated_export_preserves_the_existing_ledger` in
  `tests/test_contextual_export_risks.py`.
- The delta map links each removed composition export probe to its corresponding
  surviving canonical test and the same input, failure and persisted-state oracle.

Oracle / boundary:
- Real CLI exit and ledger bytes after the failed export. A source check, test
  count or successful setup cannot replace these observations.

Variants:
- Risky and mitigated fixture implementations, with identical malformed input.

### V-04 — Composition keeps its distinct producer and consumer evidence

Covers: AC-02, AC-04, R-03

Intent: Reject deleting the whole composition test or treating an export probe
as proof of preflight exposure, report omission or decision-input obligations.

Given:
- Unchanged `docs/tasks/T-002.4/composition.json` records COMP-01–05 and inherited
  INV-CASE-01–24 inputs.
- The existing composition scenarios are staged through the shared operation.

When:
- Run `tests/test_review_composition.py` against those records and generated
  artifacts after removal of the duplicate export calls.

Then:
- COMP-01 exposure remains present in preflight and supplied discovery input,
  absent from the staged discovery report, and tied to `CHANGES_REQUESTED` and
  the existing material-risk decision obligation.
- Existing checks for COMP-02 mixed-condition IDs/reasons/owners and both routes,
  COMP-03 current correction/unfinished rows and discovery-owned gates, COMP-04
  relevant/unrelated deferral inputs, and COMP-05 route/provenance remain intact.
- All 24 inherited case identities and their existing input distinctions remain
  checked; fixture data is still distinguished from observed role outputs.
- Navigation and the delta map explain why canonical export behavior and these
  composition-specific assertions have separate owners.

Oracle / boundary:
- Existing assertions over composition records and actual staged files/process
  results remain active. These establish fixture composition facts, not executed
  skill-call or T-005 agent compliance.

Variants:
- Every existing COMP-01–05 record and INV-CASE-01–24 inventory case; retain
  their original scenarios, role/output distinctions and expected routes.

### V-05 — Preparation assertion accepts reflow but rejects stage loss or reversal

Covers: AC-03, R-04

Intent: Reject replacing an incidental newline assertion with independent token
presence checks that allow either required stage to disappear or change order.

Given:
- Disposable copies of the text used by
  `TaskBriefDesignerPackageTest.test_packaged_preparation_contract` in
  `tests/test_task_preparation_contracts.py`.
- The baseline passage requires derived `verification.md`, then ready
  `preflight.md`; all unrelated asserted text is held constant.

When:
- Exercise the changed preparation assertion on the original passage and a
  whitespace-only reflow.
- Separately remove the verification stage, remove the readiness stage, and
  reverse their sequence in disposable text.

Then:
- Original and whitespace-only reflow pass.
- Each missing-stage variant and the reversed-stage variant fails because of
  the changed assertion, not a missing file or unrelated contract check.
- Both stage qualifications and their required order remain protected; all
  other contract-bearing assertions are preserved.
- Source guidance remains unchanged, and disposable changes are removed.

Oracle / boundary:
- Observe the changed assertion's pass/fail results against supplied text.
  Merely inspecting normalization code is not evidence of sensitivity.

Variants:
- Original, whitespace-only reflow, missing verification, missing readiness,
  reversed sequence. No source-guidance mutation or new generic harness.

### V-06 — Every original evidence row has a justified surviving owner

Covers: AC-02, AC-03, AC-04, R-03

Intent: Reject fewer tests or a green subset being treated as preservation when
consumer, parser, validator or lifecycle evidence has disappeared.

Given:
- A passing pre-edit baseline and the fixed .1 ownership/evidence map, including
  scenario/subtest distinctions and existing failure oracles.

When:
- Reconcile the task-local diff and actual collected/executed evidence into this
  leaf's new `results.md` delta map.

Then:
- Every .1 row identifies its unchanged owner or justified consolidation,
  protected defect and current execution result.
- Each removed probe has a same-input/same-failure/same-oracle survivor; the two
  duplicate export calls do not justify deleting separate header/footer consumer,
  clean-behavior, duplicated-parser, repeated-review/history or validator probes.
- All existing scenario/subtest meanings, COMP/INV-CASE inputs, eval IDs/setup
  commands, permission allow/deny values and expected failures are unchanged.
- Inherited source-parity checks, role adaptations and scenario registrations
  remain unchanged and are labeled structural protection.
- No added skip, weakened failure oracle or changed source guidance conceals a
  regression. Read-only surfaces and .1 evidence remain untouched.

Oracle / boundary:
- Compare the baseline map and scoped diff with collected tests and their actual
  boundary results. Counts, syntax checks and source equality cannot replace
  behavioral evidence; source inspection does establish the preservation of the
  explicitly retained structural guard and read-only surfaces.

Variants:
- Every .1 evidence-map row and its original finite subtest/scenario distinctions.

### V-07 — Copied eval packages stage their existing scenarios independently

Covers: AC-01, AC-05, R-05

Intent: Reject introducing a shipped dependency on the repository staging helper
or relying on source-checkout imports to make independent setup pass.

Given:
- Disposable copies or installations of discovery and acceptance packages,
  outside the source tree, with unrelated cwd and no source/test-helper import
  path supplied to setup subprocesses.
- Fresh `EVAL_WORK_ROOT` per invocation and the existing 21 setup scenarios
  selected in `.1/reviews/discovery-01.md`, P-03 (18 acceptance, 3 discovery).

When:
- Invoke each copied package's setup entry point using the command form below,
  and observe the existing owning tests' staged-fact oracles.

Then:
- Each setup exits successfully and stages the corresponding existing workspace
  and artifacts, satisfying its unchanged scenario-specific assertions.
- Setup processes use the copied/installed entry points and need no repository
  helper or source-package access. No skill/eval imports the staging helper.
- Temporary packages and workspaces are cleaned up.

Oracle / boundary:
- Real copied-package setup subprocesses and generated facts. The repository
  observer may use its existing assertions; the setup subprocess must remain
  independent. A zero setup exit or import scan alone is insufficient.

Variants:
- All P-03 scenarios, retaining both discovery late-omission variants and the
  acceptance risky/mitigated, uncertainty, known-issue and repeated-review cases.

### V-08 — Closure records passing gates with honest evidence categories

Covers: AC-04, AC-05, R-05

Intent: Reject declaring closure from targeted tests alone, reusing historical
passes, changing installer ownership, or relabeling fixture facts as compliance.

Given:
- All targeted scenarios pass and the delta map has no unresolved evidence row.
- The existing installer suite and .1 mapped owners retain their current inputs.

When:
- Run one aggregate of the mapped owning union, then the remaining designer
  suite, then the existing installer suite, sequentially using the selectors
  below. Record commands and current results in this leaf's `results.md`.

Then:
- All gates pass, and every mapped row has current evidence rather than only a
  collected count or historical result.
- Existing disposable installer checks retain projection, narrow managed
  ownership, rerun and unmanaged-preservation evidence. Active installation is
  not refreshed.
- Reports distinguish structural protection, observed fixture behavior and
  unrun T-005 agent compliance; no future task qualification is claimed.

Oracle / boundary:
- Actual suite executions, real disposable installer effects, reconciled results
  and evidence labels. If a baseline or targeted check fails, follow the brief's
  stop rather than weakening assertions or using aggregate green to waive it.

Variants:
- All mapped owners, remaining designer-local checks and existing installer
  cases. No whole-repository, network or model-budget expansion.

## Bound selectors and execution handoff

Design-stage inspection identifies these current selectors; preflight must
confirm current executability, accepted .1 dependency and a passing baseline.
No implementation test or setup execution is claimed by this artifact.

Focused command form, from repository root, in a fresh invocation per owner:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <owner>.py
```

The fixed owning union is:
`test_task_acceptance_review`, `test_task_review_discovery`,
`test_senior_review_discipline`, `test_task_flow_guides`,
`test_review_composition`, `test_contextual_export_risks`,
`test_contextual_uncertainty_inputs`, `test_contextual_known_issues`,
`test_task_preflight`, `test_bounded_task_implementer`,
`test_task_preparation_contracts`. The first focused post-edit gates are the
three contextual owners, composition and preparation; retain the other owners
in baseline and final preservation evidence.

After targeted checks pass, the implementer owns the following sequential gates.
The aggregate below selects the mapped union without unrelated repository suites:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_task_acceptance_review test_task_review_discovery test_senior_review_discipline test_task_flow_guides test_review_composition test_contextual_export_risks test_contextual_uncertainty_inputs test_contextual_known_issues test_task_preflight test_bounded_task_implementer test_task_preparation_contracts
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

For V-07, `COPY` means the absolute disposable package-copy parent, `WORK` a
fresh absolute disposable work root, and `SCENARIO` a scenario from P-03's
existing inventory. Run from unrelated cwd, with `PYTHONPATH` removed:

```sh
PYTHONDONTWRITEBYTECODE=1 EVAL_WORK_ROOT="$WORK" python3 -I "$COPY/task-acceptance-review/evals/files/setup_fixture.py" "$SCENARIO"
PYTHONDONTWRITEBYTECODE=1 EVAL_WORK_ROOT="$WORK" python3 -I "$COPY/task-review-discovery/evals/files/setup_fixture.py" "$SCENARIO"
```

Use each scenario only with its listed package. Preserve the corresponding
generated-state/process oracles from the existing contextual owners, composition
and discovery late-omission tests; preflight resolves the disposable roots and
observer execution, not new scenarios or qualification.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Obtain ready standalone preflight before implementation.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios; this task authorizes repository-test cleanup only.
- Concrete test structure, framework usage, helpers and file placement remain
  implementation choices within the brief's fixed ownership boundaries.
- Use disposable experiments for setup failure and text sensitivity. Do not add
  scenarios, mutate source guidance or extract shared shipped eval generators.
- If implementation discovery shows that a scenario cannot be exercised at its
  stated boundary, route the conflict back to task design/preflight rather than
  silently weakening the oracle.
- Publish this leaf's delta map and results without overwriting .1 evidence or
  official plans; retain the brief's fresh discovery and separate acceptance
  follow-on stages. This artifact issues no implementation acceptance decision.
