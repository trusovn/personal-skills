# Task Brief: `INT-FLOW-001` — Close preparation and review integration gaps

Status: `ready`

Task kind: `executable`

Brief revision: 1

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 18 tool calls / 45 minutes / 55k context
```

## Outcome

Make the source preparation and review contracts agree on correction routes,
review applicability, finding identity, context transfer, and verification of
an executable integration task's own ACs. Supply focused local evidence and
usable qualification inputs for the separate T-005 role calls.

## Direction trace

- Contribution: preserve `FLOW-001/002/003`, `IF-001` through `IF-006`, and
  `INV-001/002/003/004/005/006/008/010/011` from the
  [project plan](../../project-plan.md), sections 4–8, 10–12.
- User-observable effect: a coordinator gets one consistent next route and
  complete preparation/finding references. Enables T-005 to observe actual
  producer-to-consumer continuity using qualified installed skills.
- Why now: the user requested a correction document after an integration audit
  of completed T-001–T-003. Their isolated source/fixture checks leave the
  inconsistencies below undetected before installed-flow qualification.
- Decisions used: scoped conditional review, stable IDs, contextual acceptance,
  compact guided preparation, and truthful evidence categories already required
  by the plan; the current user request authorizes addressing the five findings.
- New direction decisions required: None. Allowing verification of one
  integration leaf's own ACs does not add a system-verification stage or ownership
  of sibling requirements.

## Authority and scope

- Authority: user request of 2026-10-12, “create document to address these
  issues,” following the `testing-discipline` integration audit. This brief
  records that audit below so execution does not need the conversation.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: completed T-001, T-002, T-003 source contracts and existing local
  fixture/installer capabilities. This is a standalone correction task, not a
  new child or replacement of an official plan task.
- Primary changes: `skills/task-implementation-flow/task-maintainability-review/`,
  `task-review-discovery/`, `task-acceptance-review/`, and
  `task-verification-designer/`: only affected skill instructions, templates,
  existing eval expectations and task-local fixture setup.
- Synchronize only affected claims in `README.md`, `skills/README.md`, and
  `skills/task-implementation-flow/README.md`. Focus tests in
  `tests/test_task_maintainability_review.py`, `test_task_review_discovery.py`,
  `test_task_acceptance_review.py`, `test_task_preparation_contracts.py`,
  `test_task_flow_guides.py`, `test_review_composition.py`, and
  `test_install_development_skills.py`. Reuse existing staging helpers.
- New task-owned outputs: implementation results and, only if needed, a compact
  composition/qualification input record in this package. Separate preparation
  and review roles own their canonical artifacts here.
- Inspect `scripts/install_development_skills.py`, including
  `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`,
  focused installer tests and README installation guidance. Change distribution
  declarations only if these corrections require it; preserve narrow ownership.
- Read-only: official plans/task-map, existing task/review/results/composition
  history, active `.agents/` installation, and implementer/registry-updater
  source contracts used as route references. No active installation refresh.
- Excluded: T-004 installer features, T-005 role execution, model-budget/live
  checks, new runner/schema/shared harness, orchestration, global correction
  limits, changed verdicts or materiality policy, portfolio/tracker writes.
- Assumptions: the existing deterministic tests and disposable Git fixtures are
  sufficient for contract/fixture/projection evidence. Actual agent compliance
  remains a separately authorized T-005 obligation, not a prerequisite to these
  source corrections. Preflight confirms current paths and commands.

## Audit findings to close

| ID | Current gap and affected source | Required correction |
|---|---|---|
| I-01 | Maintainability's `Correction loop` routes its clean review directly to discovery/acceptance, although the implementer route and appended registry section require applicable registry synchronization first. | Name the first outstanding stage and full ordered remainder, including applicable registry work; do not imply that naming stages executes them. |
| I-02 | Maintainability's `Independence` section invalidates its verdict for every production correction; the implementer's `Name the complete ordered submission route` preserves applicable current evidence for unaffected reviewed scope. | Use the existing scope/currentness rule consistently, without reusing stale proof or rerunning an unaffected stage merely because a production file changed. |
| I-03 | Maintainability's `Output` numbers blockers by impact but requires no stable finding IDs or continuity. Composition tests supply `MNT-B1`–`MNT-B4` themselves. | Require stable finding identity across reordered reports and correction rounds; fixture IDs cannot substitute for a producer obligation. |
| I-04 | Guided acceptance's input list and discovery's final handoff list omit explicit verification/readiness/context references, although acceptance's rubric uses readiness context. | Carry and consume applicable packaged preparation references even in complete, clean guided reports; keep direct requests compact. |
| I-05 | Verification designer's `Cross-task integration boundary` refuses a brief requiring composition of separate outputs, conflicting with executable integration leaves such as T-003.4. | Permit verification of that leaf's explicit composition ACs while preserving task-local authority and the exclusion of system-wide strategy/sibling requirement design. |

Audit baseline, not readiness or behavioral certification: the composition suite
passed 16 tests; a relevant 11-module local union passed 143 tests. No actual
role calls were exercised. Existing results correctly defer those to T-005.

## Execution sizing

- Sizing policy: `default@1`, project-local
  `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 18. Estimated implementation duration: 45 minutes.
  Confidence: medium. Intended profile: `standard / high`.
- Triggered limits: `max_agent_calls` (15), `max_duration_minutes` (40).
- Policy result: `override_cannot_split_safely`.
- Decomposition override: `cannot_split_safely`. Candidate split: maintainability
  routes/IDs versus preparation/context/composition policy, followed by an
  integration child. Both slices would revise the same flow/profile guidance and
  composition tests, then require another reconciliation and distribution pass.
  The bounded instruction/template changes and existing fixture checks can be
  reconciled together with less repeated discovery and review coordination.
  Residual risk: several contracts must remain aligned; use the five explicit
  coverage rows below and stop for wider policy or tooling changes. The active
  profile permits this reasoned override; separate review work is not estimated.

## Readiness route

Standalone guided preflight after derived verification — confirm current source
ownership, affected test owners, existing fixture capability and command scope.
`ready` describes brief design, not current repository executability.

## Verification-design recommendation

Separate — scoped invalidation, stable finding identity, preparation/context
handoffs and integration-leaf authority need distinct negative contrasts.
Write derived `verification.md`, then obtain ready `preflight.md`, before edits.
This correction task owns source-policy and fixture ACs; its preparation does
not depend on first running the corrected integration-leaf policy.

## Work and acceptance criteria

Use `testing-discipline` before changing tests/evals/fixtures. Inspect and reuse
existing cases; add only distinct missing evidence. Correct contradictory
instructions, not just an added paragraph that leaves the old route intact.

- **AC-01 / I-01:** Maintainability's main correction instructions, output/next
  handoff and relevant guidance agree with the implementer route: required
  architecture gate → fresh applicable maintainability review → applicable
  registry synchronization → fresh discovery → separate acceptance. Include
  stages only when required and outstanding; registry work cannot be dropped
  when applicable, and an absent registry stage cannot be invented.
- **AC-02 / I-02:** Re-entry follows actual affected reviewed scope and current
  evidence. A correction affecting maintainability scope requires fresh review;
  demonstrably unaffected scope with applicable current proof retains that
  evidence. Stale, missing or inapplicable proof never counts as completed.
  Preserve existing tests-only exceptions and reference-only route conditions.
- **AC-03 / I-03:** Maintainability findings have stable IDs separate from display
  order. Four confirmed findings are retained; after one is corrected, fresh
  review preserves the other three IDs and identifies the corrected finding's
  current disposition/evidence. Prior reports remain unchanged, resolved IDs are
  not recycled, and newly confirmed findings cannot reuse an existing identity.
  Retain full evidence and genuine-stop coverage without a finding cap.
- **AC-04 / I-04:** Packaged guided discovery hands off, and acceptance identifies
  and reads, the applicable brief, verification revision, readiness and decision
  context references for complete as well as partial evidence. Revised-scenario
  proof cannot rescue obsolete readiness. A material risk supported only by
  preflight exposure reaches contextual disposition; a bounded compatible
  contrast is not automatically material. Missing decision-relevant preparation
  proof gets focused recovery from its owner. Unpackaged direct edits use supplied
  conversational/repository context, without a mandatory packet or routine prompt.
- **AC-05 / I-05:** Verification designer can derive scenarios for one executable
  integration leaf's explicit ACs using supplied producer outputs and consumer
  boundaries. It still rejects non-executable composite parents, invented sibling
  requirements and system-wide strategy ownership. It reports unavailable inputs
  or an unresolvable oracle to the proper owner instead of inventing reports or
  claiming readiness. Packaged preparation remains mandatory.
- **AC-06:** Local evidence rejects the old contract gaps where feasible, and
  results separate structural checks, real fixture/filesystem/Git observations
  and unrun role behavior. Canonical disposable committed-target installation
  projects corrected packages/templates/fixtures and guide bytes. Reuse current
  projection coverage; preserve unmanaged state and installer ownership.
  T-005 receives exact setup, intended producers/consumers, expected contrasts
  and every unrun role-call boundary. Existing history and active copies stay intact.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-008 | Registry applicable versus absent after corrected maintainability review | Source handoff retains the first outstanding stage/full remainder; supplied public-contract change needs registry sync | Extend current route/composition cases; reject the existing shortcut | Trace the registry-required correction through each source consumer | Implementer: targeted/owning checks; fresh discovery: aggregate; T-005: role calls |
| R-02 / INV-003/008 | Affected scope; unaffected/current scope; stale/missing/inapplicable proof | All stage instructions select the same owed review from explicit scope/evidence facts | Reuse current route/currentness fixtures; reject blanket invalidation and stale reuse | Check an unaffected correction plus a stale-evidence contrast | Same owners as R-01 |
| R-03 / INV-008 | Four findings → one corrected → three remaining; reordered output; new finding; genuine stop | Stable IDs and current dispositions survive supplied report/correction inputs without rewriting history | Extend current four-blocker/composition fixtures; reject renumbering or ID loss | Follow one resolved ID and one surviving ID through fresh-review inputs | Same owners as R-01 |
| R-04 / INV-003/006/011 | Complete versus partial packaged evidence; preflight-only material versus bounded exposure; old revision versus current; direct request | Preparation references reach the decision input with the correct context and revision; direct entry remains compact | Reuse contextual and revision fixtures; reject omitted references/stale readiness | Locate the decisive exposure solely in preflight and trace its handoff | Same owners as R-01 |
| R-05 / INV-001/002/010 | Executable integration leaf versus composite parent; own AC versus invented sibling/system requirement; unavailable oracle | Designer policy admits task-local composition and retains authority/feasibility refusal boundaries | Extend preparation-policy cases using explicit briefs/inputs; reject the old blanket refusal | Contrast an integration leaf with a composite-parent request | Same owners as R-01 |

## Verification and evidence limits

Run new/changed focused checks first, then the nearest owning module sequentially.
Existing root commands use
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <owner-file>`.
For the installer, use `test_install_development_skills.py`; exercise only
disposable committed Git targets. Leave the active installation untouched.

Fresh discovery owns one justified affected-module aggregate after targeted
rows/probes are clean; acceptance consumes it without rerunning it. Initial
candidate command from root (preflight narrows it to actual changed owners):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_task_maintainability_review test_task_review_discovery test_task_acceptance_review test_task_preparation_contracts test_task_flow_guides test_review_composition test_install_development_skills
```

Show that new checks reject old instructions or a controlled relevant fault when
feasible, with the intended assertion failing and no mutation left behind.
Text presence is structural evidence. Running fixture staging or comparing
manually constructed reports does not prove role compliance or an actual handoff.
State those limits; preserve executable setup and independent expected outcomes
for separately authorized T-005 calls. Do not create a role runner to close them.
Check `git diff --check` and protected-file preservation. No whole-repository,
live-network or model-budget gate is required by this brief.

## Expected contract impact

Preserve `ART-001/002/003/004/005/006/007/009`, `IF-001` through `IF-006`, and
the direction-trace invariants. Repair conditional handoff/currentness rules,
stable maintainability finding identity and packaged context references;
clarify task-local integration verification authority. No `docs/contracts`
registry exists here; do not create one or add a registry stage for this task.

## Stops and handoff

Stop for authority conflict, inseparable user work, unsafe permissions, a missing
decisive local capability, new shared tooling or scope expansion. Preserve
ordinary guided uncertainty and existing task-specific correction stops.

Next: verification design → standalone guided preflight → bounded implementation.
Immediately after implementation or correction, hand completed bytes and the
full finding/scenario inventory to fresh independent review through applicable
conditional stages, fresh discovery and separate acceptance; end the implementer
invocation. Name the first outstanding owner and complete remaining route.
Write results beside this brief; do not update official plans or old task history.
