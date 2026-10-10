# Task Brief: `TEST-STAB-001.2` — Consolidate test setup and incidental assertions

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / 40k context
```

## Execution sizing

Policy: `default@1`, active project-local brief designer
`references/task-sizing.yaml`. Estimate: **12 agent calls / 35 minutes**;
confidence medium; `standard / medium`. Policy result: fits. Triggered limits:
none. Decomposition override: none. Estimate covers implementation and local
checks, excluding separate preparation/review.

## Readiness and verification design

Readiness route: **standalone guided preflight** — confirm accepted .1, its owner
map, current runnable baseline and unchanged independent-package execution.

Verification-design recommendation: **separate** — fewer probes and relaxed text
formatting must retain the same defect detection. Create derived `verification.md`,
then ready `preflight.md`; design readiness does not authorize implementation.

## Outcome, authority and boundaries

Repeated repository-test staging uses one small reusable operation; each export
failure signal has one canonical runtime owner; preparation guidance checks
tolerate incidental line wrapping without losing required-stage protection.

Authority: [parent](../TEST-STAB-001/brief.md), user request, root `AGENTS.md` and
active project-local `testing-discipline`. Repository/branch:
`trusovn/personal-skills` / `t-o-new-flow`. Dependency: accepted
[TEST-STAB-001.1](../TEST-STAB-001.1/brief.md); consume its published owner/evidence
map, selectors and passing results. Keep its ownership decisions fixed.

Direction contribution: no workflow change; enables T-003–T-005 to extend clear
owners with stable evidence and less repeated setup. Finish before T-003.
Preserve the plan's evidence and independent-package promises.
New direction decisions required: None.

Allowed: .1's repository review fixture/composition modules, a small support
module under `tests/`, the relocated preparation contract test, navigation-guide
updates for those changes, and new evidence within this leaf. The helper may
encapsulate temporary workspace lifecycle, environment and setup subprocess
execution already repeated in `ContextualRiskFixtureTests.stage` and
`ComposedQualificationSetupTests.stage`. Use it across their relocated consumers;
leave meaningful scenario choices, paths, data and assertions with the tests.
Do not build a configurable fixture framework or share mutable staged state.

Read-only: all skill eval generators/JSON; all source guidance/references; installer,
shared scripts and installation docs; active installation; official planning and
all prior task packages/reviews/results, including .1's map. No new scenarios,
contract registry, installation dependency or runtime feature. Do not move
ownership again or absorb future task qualification.

## Required bounded cleanup

1. Share the repeated repository-test staging operation above. Each invocation
   keeps its own disposable `EVAL_WORK_ROOT`, cleanup and captured setup failure.
   Do not import this helper from any shipped skill/eval file.
2. Consolidate the duplicated malformed-invoice export probes originally inside
   `ComposedQualificationSetupTests.test_preflight_only_exposure_survives_into_discovery_and_decision_inputs`.
   Its risky and mitigated CLI calls use the same inputs and oracles as
   `ContextualRiskFixtureTests.test_failed_risky_export_destroys_the_existing_ledger`
   and `test_failed_mitigated_export_preserves_the_existing_ledger`.
   Keep those two canonical runtime tests. Keep composition-specific assertions
   for COMP-01, preflight-only exposure, report omission and expected decision
   obligations; they protect a different boundary. Document that separation.
3. Remove incidental newline coupling from the assertion originally in
   `TaskBriefDesignerPackageTest.test_packaged_preparation_contract` for
   `derived verification.md, then a ready preflight.md`. Normalize whitespace
   locally while retaining both required stages and their order. Preserve all
   other contract-bearing assertions. Further deletions require a demonstrated
   same-input/same-failure/same-oracle replacement and must stay within these owners;
   there is no mandate for an assertion-count reduction.

Keep the inherited fixture source-parity guard, its role adaptations and scenario
registrations unchanged. Extraction of generator setup or replacement of its
parity proof is explicitly deferred because cross-skill imports/distribution or
a larger behavioral comparison would expand this task.

## Acceptance criteria

- **AC-01 — Local reuse:** relocated contextual and composition tests use one
  repository-only staging helper with per-invocation state and cleanup. Running
  either module alone still succeeds; setup failures include the scenario and
  subprocess diagnostics. Skill evals remain independent of repository tests.
- **AC-02 — Distinct evidence retained:** canonical risky/mitigated tests still
  observe nonzero CLI exits and respectively an empty/preserved seeded ledger.
  Composition still checks its unique producer/consumer inputs and fixture-data
  labels. The delta map identifies the surviving test for every removed probe;
  changing a header, footer, clean behavior or parser case cannot be hidden by
  removing its separate existing test.
- **AC-03 — Stable text protection:** whitespace-only reflow passes the changed
  preparation assertion. Removing verification, removing readiness or reversing
  their required order still fails. No source guidance is edited to satisfy tests.
- **AC-04 — Full preservation:** every .1 evidence-map row remains covered or has
  a justified consolidation row with equivalent surviving evidence. All existing
  scenario/subtest meanings, eval IDs/setup commands, permissions, inherited
  parity checks and COMP/INV-CASE inputs remain intact. No skipped checks or
  changed expected failures conceal regressions.
- **AC-05 — Closure:** documented focused commands, the mapped owning union,
  remaining designer suite and existing installer suite pass. Independent eval
  setup still runs from an installed/copied package without source/test-helper
  access. Reports preserve the distinction between structural protection,
  observed fixture behavior and unrun T-005 agent compliance.

## Verification expectations

Establish a passing baseline from .1's current commands before changing tests.
Maintain a delta map in this leaf's new `results.md`: old evidence row → unchanged
owner or surviving replacement, protected defect and current execution result.
Do not overwrite .1's map or count fewer tests as success.

| Risk | Lowest reliable evidence and decisive oracle |
|---|---|
| Reuse leaks state or masks a setup failure | Run helper consumers separately with distinct temporary roots; exercise one invalid existing setup name and inspect scenario/exit/stderr diagnostics; no generated state survives cleanup |
| Consolidation loses destructive/mitigated contrast | Run the two canonical public CLI probes with malformed invoices and a seeded existing ledger; retain nonzero exit plus empty/preserved bytes |
| Composition mapping is lost | Run the relocated composition checks against unchanged COMP-01–05 and INV-CASE-01–24 inputs; preserve preflight-only exposure and incomplete-row/role-output distinctions |
| Text assertion becomes permissive | Disposable copies of the asserted text: whitespace reflow passes; each missing stage and reversed-stage sequence fails for the intended assertion |
| Independence/import or install regression | Existing installer suite plus scenario setup from isolated copied/installed discovery and acceptance packages using `EVAL_WORK_ROOT`; unchanged no-source/no-repository-test import boundary |

Use temporary experiments for fault/reflow demonstrations; no permanent generic
mutation harness or guidance mutation is needed. Existing stronger consumer,
cleanup, parser, repeated-review/history and validator probes remain in the owning
union. Do not replace them with counts, JSON syntax checks or source equality.

After targeted checks pass, the implementer owns one aggregate execution of .1's
mapped owning union plus the remaining designer suite, followed by:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

Verification design/preflight bind exact current selectors and isolated setup
commands; use already supplied scenarios rather than inventing qualification.
Discovery owns corroboration and any justified review aggregate; acceptance
consumes its record. No whole-repository, live-network or model-budget checks are
required. Ask before expensive expansion; report unrun stronger evidence honestly.

## Stops and handoff

Stop for a red baseline, unknown surviving failure oracle, changed scenario
meaning, cross-skill packaging need, production-contract change or user-work
overlap. Do not weaken the guard or repair unfinished T-004 features. Escalate
material scope expansion to the task owner instead of adding a shared eval harness.

Next: derived verification → ready standalone preflight → implementation.
Required follow-on: immediately after implementation or correction, pass completed
bytes through applicable conditional stages to fresh independent
`task-review-discovery`, then a separate fresh `task-acceptance-review` decision.
On acceptance, provide T-003 with the ownership guide, .1 map, .2 delta map,
commands/results and explicit deferred generator/parity work. No T-003–T-005
acceptance criterion is satisfied by this cleanup.

Expected contract impact: none. Repository-only support is not a shipped dependency.
