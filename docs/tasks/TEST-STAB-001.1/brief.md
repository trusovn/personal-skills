# Task Brief: `TEST-STAB-001.1` — Assign clear test owners without changing evidence

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / 45k context
```

## Execution sizing

Policy: `default@1`, active project-local brief designer
`references/task-sizing.yaml`. Estimate: **14 agent calls / 40 minutes**;
confidence medium; `standard / medium`. Policy result: fits. Triggered limits:
none. Decomposition override: none. Implementation work only; separate
preparation/review stages are excluded.

## Readiness and verification design

Readiness route: **standalone guided preflight** — confirm accepted T-002.4,
current baseline, discovery/import behavior and disposable installation checks.

Verification-design recommendation: **separate** — moves can silently drop or
double-discover tests, and source-only imports can break copied-package use.
Create this package's derived `verification.md`, then obtain ready `preflight.md`
before implementation. `ready` describes design, not permission to bypass entry.

## Outcome and authority

Every existing test has one discoverable owner and a focused command; moved
tests retain their assertions, inputs and failure signals.

Authority: [parent](../TEST-STAB-001/brief.md), user request and root `AGENTS.md`;
active project-local `testing-discipline`. Work in `trusovn/personal-skills`,
branch `t-o-new-flow`. Dependency: accepted T-002.4, with unchanged applicable
T-001/T-002 source contracts. Read the parent for plan links and exclusions.

Direction contribution: no direct workflow change; enables T-003 additions to
use settled test owners and commands. Execute in the user-required interval.
Preserve FLOW-001/002/003 evidence, INV-001–011 and ART-009 package independence.
New direction decisions required: None.

## Permitted ownership changes

| Current responsibility | Required owner after migration |
|---|---|
| Brief designer's own resources, sizing and authoring route | Keep in `task-brief-designer/tests/test_package_resources.py` |
| `PreflightContractTest` | Repository `tests/test_task_preflight.py` |
| `ImplementerContractTest` | Repository `tests/test_bounded_task_implementer.py` |
| Cross-skill preparation/resource/legacy-path checks in `TaskBriefDesignerPackageTest` | Repository `tests/test_task_preparation_contracts.py` |
| Acceptance admission, contextual contract and acceptance eval metadata | Repository `tests/test_task_acceptance_review.py` |
| Discovery contract, inherited parity/registration and late-omission validator probes | Repository `tests/test_task_review_discovery.py` |
| The two senior-review prerequisite checks | Repository `tests/test_senior_review_discipline.py` |
| Export/consumer risks; uncertainty/mixed-context inputs; known-issue/repeated-review facts in `ContextualRiskFixtureTests` | Separate repository fixture modules for those three responsibilities |
| `ComposedReviewFlowGuideTests` | Repository `tests/test_task_flow_guides.py` |
| `ComposedQualificationSetupTests` | Repository `tests/test_review_composition.py` |

Use existing naming/style; names for the three fixture modules may be chosen
locally and recorded in the map. Keep genuine cross-stage assertions together
instead of duplicating them per skill. Do not split by arbitrary line count.
Class names alone do not decide ownership: move a whole mixed test when it also
reads sibling skills or source-only guides. In particular, the designer's
`test_readme_identifies_packaged_resources_as_authoritative` and mixed
`test_decomposition_trigger_requires_boundary_quality_decision` belong with
repository preparation/guide checks. Remaining package-local tests must resolve
their own package from their file location, without assuming a source checkout.

Allowed edits: the two original modules, these owning modules, minimal
repository-test support needed for imports, `tests/README.md`, and new evidence
inside this leaf. Preserve assertion bodies and scenario selection; adapt only
imports, paths and class organization needed by the move. Setup simplification
belongs to .2. Remove obsolete source modules if emptied; do not leave forwarding
test classes that duplicate discovery.

All eval generators/JSON, source guidance, installer, shared scripts, plans,
existing packages/reviews/results and active `.agents/` remain read-only.
Historical commands remain history; document current selectors without editing
their original reports. No source-contract or permission change is authorized.

## Work and acceptance criteria

1. Establish a passing current baseline and enumerate collected tests before
   editing. Record all subtest/scenario distinctions, not just method counts.
2. Move responsibilities to their owners. Give remaining large fixture classes
   domain-based boundaries and keep setup/data visible.
3. Add one concise navigation guide with owner, purpose, fixture dependency and
   targeted/aggregate commands. Publish an old-to-new evidence map in this
   leaf's new `results.md`, with inventories alongside it if needed.

- **AC-01 — Ownership:** the old mixed review module no longer combines these
  responsibilities; designer-local tests cover its own package. Cross-stage
  checks have explicit repository ownership. Each module has one stated purpose.
- **AC-02 — Preservation:** each baseline test maps to exactly one collected
  post-move test, retaining its assertions, scenario/subtest inputs and boundary
  probes. No added skip, mock of the decisive boundary, relaxed expected failure,
  duplicated discovery or lost test is used to get a green suite.
- **AC-03 — Execution:** all mapped tests pass through documented aggregate and
  focused commands and when owning modules run alone. Import resolution does
  not depend on execution order, inherited cwd or another test's mutable state.
- **AC-04 — Independence:** the remaining designer-local suite and discovery/
  acceptance eval setups need no repository-test helper when copied or installed.
  Installer selection/ownership and unmanaged preservation remain unchanged.
- **AC-05 — Scope:** source guidance, eval inputs/meaning, expected verdicts,
  policy allow/deny values, COMP-01–05, INV-CASE-01–24 and T-005 unrun labels are
  unchanged. Retain the source-parity guard; label its evidence purpose accurately.

## Verification expectations

Before editing, run from the repository root, sequentially:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

Use `unittest` collection plus an explicit relocation map to compare executed
evidence; AST counts alone cannot prove discovery. After targeted module checks
pass, run the mapped union plus the remaining designer suite, then the existing
installer suite. Preserve discovery scenario/role checks and actual fixture
subprocess outcomes, including valid/invalid validator contrasts and current
Git index/worktree distinctions. No new behavior requires a fabricated red test;
the unchanged assertion map and identical boundary evidence prove migration.

Preflight/verification design resolve post-move selectors and the copied-package
check. Use existing committed disposable installer fixtures. Run remaining
designer tests from the copied/installed package with no source-tree/test-helper
fallback. Existing installer byte projection is real installation evidence, not
proof that an installed test imports or a role complies. Do not test unfinished
T-004 unborn behavior or run T-005 agents.

The implementer owns these local aggregate gates after targeted checks pass;
fresh discovery may corroborate current results and must record any justified
additional gate. Acceptance consumes that record. No whole-repository, live,
network or model-budget gate is required; obtain authorization before costly
expansion. Report commands, collected totals and actual pass/fail evidence,
distinguishing text checks, fixture runtime and unrun role behavior.

## Stops and handoff

Stop for a red baseline, lost/ambiguous scenario ownership, user-work overlap,
unsafe permission need or a requirement to change package/runtime contracts.
Do not repair unrelated failures or refresh `.agents/`. At the budget checkpoint,
preserve completed mapping and outstanding verification without claiming success.

Next: derived verification → ready standalone preflight → implementation.
Required follow-on: immediately after implementation or correction, hand the
completed bytes through any applicable conditional stages to fresh independent
`task-review-discovery`, then a separate fresh `task-acceptance-review` decision.
Accepted .1 supplies .2 with the exact test map, new owners, selectors and baseline.

Expected contract impact: none; relocation changes test discovery locations only.
