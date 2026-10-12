# Task Brief: `Q-01` — Review significant changed test assets for maintainability

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 15 tool calls / 40 minutes / 50k context
```

## Execution sizing

- Policy: `default@1`, project-local brief-designer `references/task-sizing.yaml`.
- Estimated implementation: 15 agent calls, 40 minutes; confidence: medium.
- Intended profile: `standard / high`. Policy result: fits; triggered limits:
  none; decomposition override: none. Separate preparation and independent
  review are excluded. Keep the scope extension, focused fixture variants and
  their regression checks together; no detached test-writing task.

## Readiness route

standalone guided preflight — after derived `verification.md`, confirm T-003
ownership of overlapping source/guide/test surfaces, existing fixture commands,
and the installation repair boundary. `ready` describes the designed contract,
not current executability or authorization to implement in this design pass.

## Verification-design recommendation

separate — tests-only authorship, corrected-byte freshness and conditional stage
re-entry can produce plausible false acceptance. Derive `verification.md`, then
obtain ready `preflight.md` before bounded implementation. Existing fixture,
staging and independent review mechanisms are believed available; no additional
runner or review infrastructure is authorized.

## Outcome and direction trace

The existing maintainability reviewer identifies consequential introduced or
worsened design defects in significant changed tests, evaluations and harness
code, including tests-only submissions, with the existing independent verdict
and correction process.

- Contribution: Q-01 in [FEATURE-MAP](../../future-work/FEATURE-MAP.md), family Q,
  and [concept 02](../../future-work/concepts/02-system-verification-and-test-quality.md),
  Q-01 and allocation/evidence rules.
- Effect: callers receive actionable test-architecture findings even when the
  submitted suite passes, while ordinary assertion edits stay lightweight.
- Why now: the user selected a separate bounded Q-01 task; the current reviewer
  still describes most provenance and correction rules as production-only.
- Authority: the user request to create this separately authorized task. The
  feature map and concept are candidate context; the
  [archived proposal](../../future-work/stale/test-suite-maintainability-integration-proposal.md)
  sections 3, 4.2, 6–8 explain the gap and constraints, not authority for its
  wider work.
- New direction decisions required: None.

## Authority and scope

- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Preparation authority does not fold this change into T-003, T-004 or T-005.
  Execution requires the separate Q-01 implementation authorization and ready
  preparation. Preflight must resolve any unfinished T-003 overlap with its
  owner; do not infer completion from task status, index entries or commits.
- Primary edits: `skills/task-implementation-flow/task-maintainability-review/`
  (`SKILL.md`, existing `evals/evals.json`, `evals/files/setup_fixture.py`) and
  `tests/test_task_maintainability_review.py`.
- Minimal alignment only where stale production-only scope or tests-only skip
  wording contradicts Q-01: `skills/task-implementation-flow/README.md`,
  `skills/README.md`, root `README.md`, and their existing owning checks in
  `tests/test_task_flow_guides.py` and `tests/test_install_development_skills.py`.
- Inspect `scripts/install_development_skills.py`: keep
  `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`,
  installer checks and installation docs coherent. No selection/helper change
  is expected. Use the canonical installer for disk projection after edits;
  preserve its managed ownership boundary and all unmanaged files.
- Read-only dependencies: existing implementer, discovery, acceptance and
  registry-updater contracts; T-003.2/.3/.4 task evidence; `testing-discipline`
  from the active installation root; existing test staging helpers.
- Excluded: broad fixture consolidation/Q-02, fixture-owner migration, copying
  the full testing policy, new stages/roles/verdicts, workflow automation,
  checker/framework infrastructure, plan/task-map edits, T-004/T-005 scope
  changes, global thresholds and refresh/restart of active agent sessions.

## Work and acceptance criteria

1. Extend the existing scope and six review questions to significant changed
   test assets. Use relevant canonical `testing-discipline` guidance from the
   same installation root; leave functional conformance to discovery/acceptance.
2. Reuse existing coverage and setup. Add only missing discriminating variants
   and narrowly align affected scope/routing references and disk projection.

- **AC-01 — Scope and proportionality:** Include changed tests, evaluations,
  fixture/setup code and harness code as reviewed implementation assets when
  this review applies. Identify significance through changed ownership,
  dependencies, scenario authority, isolation, oracle structure or harness
  behavior. Significant test architecture is a risk reason to use the existing
  conditional review; every assertion edit is not a new mandatory review.
  Inspect only changed/influenced surfaces and necessary immediate neighbors.
- **AC-02 — Consequential defects:** Review introduced/worsened duplicated
  scenario authority, fragile mutable fixtures, unclear/cross-owner coupling,
  incidental text/layout assertions, harness-internal dependencies and
  speculative abstraction. Findings need location, current evidence, concrete
  maintenance consequence and the smallest correction direction. Size/counts,
  style, unchanged debt and legitimate separate observation boundaries do not
  establish blockers. Stable textual contracts remain legitimate.
- **AC-03 — Independence and freshness:** Bind provenance, self-check refusal,
  reviewed scope, output and correction invalidation to actual reviewed assets.
  An author of reviewed test/eval/harness bytes cannot issue an independent
  verdict, even with unchanged production code. Tests-only corrections stale
  affected evidence; unaffected evidence remains usable only while current and
  applicable. Retain all confirmed finding IDs/dispositions and report history.
- **AC-04 — Workflow preservation:** Keep `ACCEPT`, `CHANGES_REQUESTED`,
  `INCONCLUSIVE`, required architecture-gate policy, genuine stops, complete
  bounded reporting and read-only reviewer permissions. Route by actual effects:
  affected applicable gate/maintainability review, applicable registry sync,
  fresh discovery, then separate acceptance. Do not create registry work or a
  gate for every test change. A tests-only label alone never permits skipping
  an affected required review; retain authorized trivial-change exceptions.
- **AC-05 — Discriminating evidence:** Supply executable tests-only baseline,
  changed bytes, authority and gate policy. Demonstrate at least two distinct
  consequential defects: duplicated scenario authority with an observable
  one-owner change divergence, and fixture/harness coupling with an observable
  isolation or repeatability failure. The normal submitted suite can pass.
  A clean small assertion change and legitimate independent fixtures remain
  non-blocking. A fresh reviewer using the changed skill detects the defects
  with evidence; deterministic setup/text checks alone cannot satisfy detection.
- **AC-06 — Distribution:** The complete installed skill package and profile
  guide match changed source, including executable fixture assets. Verify a
  disposable canonical install and the repository's on-disk projection. Do not
  refresh active agent sessions or claim they loaded the new skill. Record
  source identity, commands and any unrun behavioral proof in Q-01 results.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / proportionate detection | Tests-only duplicated authority; coupled mutable setup/harness; clean assertion edit; valid independent fixtures | Real Git diff and runnable defect/control probes; fresh reviewer reports material findings and no control blocker | Extend existing setup/owning tests; show divergence/isolation failure absent in baseline, present in changed fixture | Fresh reviewer inspects fixture without being given the expected verdict or defect oracle; compare output with held-back oracle | Implementer: targeted fixture checks; fresh discovery: Q-01 behavioral evidence; acceptance: admission |
| R-02 / reviewed-byte provenance | Test/eval/harness author versus independent reviewer; first report → tests-only correction → next review; unaffected scope | Author yields `SELF_CHECK_ONLY`; corrected affected bytes receive fresh evidence and stable finding dispositions; unchanged report preserved | Reuse self-check and correction-round cases, adding test-asset inputs without duplicating setup | Substitute a prior report after changing only its reviewed test asset; reject stale evidence and retain unaffected obligations | Implementer: focused contracts/setup; independent review owners: current provenance and route |
| R-03 / ordered obligations | Required gate available/unavailable; maintainability affected/unaffected; registry applicable/absent | Existing truthful verdicts and first outstanding stage/full ordered remainder; no filename-only shortcut or invented stage | Reuse unavailable-gate and routing coverage; update only distinct test-scope gaps | Trace an affected tests-only correction and a policy-authorized trivial correction through existing handoffs | Existing conditional-stage owners; discovery then separate acceptance |
| R-04 / projection | Disposable install; repository disk projection; active sessions unchanged | Canonical installer preserves unmanaged bytes; full managed file inventory/bytes equal source | Existing installer projection/preservation checks and post-install comparison | Verify installed setup runs independently of repository-only test helpers; corroborate inventory equality | Implementer: install/check; fresh discovery: focused corroboration |

## Verification

- Inspect existing cases before editing. Preserve the four-production-blocker,
  genuine-stop, correction-round, authoring-session and report-path contrasts.
  Reuse fixture construction and `tests/staging_fixture_support.py` where
  appropriate; packaged eval setup must not import repository-only helpers.
- Fail-first: establish that focused scope/provenance checks reject the old
  production-only contract. Execute defect probes against baseline and changed
  fixtures; failures must come from the intended oracle, not missing setup.
- Targeted, then owning suite, sequentially:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py`.
  Run `test_task_flow_guides.py` only for changed guide/routing surfaces, then
  `test_install_development_skills.py` for projection/preservation. Preflight
  freezes focused selectors; no whole-repository suite is required.
- Disk projection: `python3 scripts/install_development_skills.py .`, then
  compare complete managed skill files and profile guide against source,
  excluding only existing installer transient patterns. Use existing installer
  tests for disposable installation and unmanaged-file preservation.
- Fresh discovery owns the small Q-01 behavioral qualification and any justified
  aggregate gate after clean targeted evidence. Use the existing independent
  review process with explicit fixture setup and held-back expected findings;
  acceptance consumes that evidence without rerunning the catalog. Require the
  two defective cases, clean control, author self-check and corrected-byte
  contrast; combine inputs where one coherent fixture proves multiple cases.
- Ask before costly/live-networked model evals unless their exact class has been
  authorized. No new runner may be built to avoid that boundary. Unrun behavior
  is a gap, not Q-01 completion; T-005's qualification scope remains unchanged.

## Expected contract impact

- Q-01 changes the subjects of existing `ART-005 / IF-003` review; preserve
  `INV-004/005/006/008` independence, current evidence, permission and correction
  boundaries and downstream `IF-004/005/006`. These are compatibility references
  to existing contracts, not additions to T-003/T-004/T-005 acceptance criteria.
- No current `docs/contracts` registry exists; no registry foundation work.
  Expected delta: test assets receive the existing review/provenance rules.
- Design-time observation at source revision
  `1c3b2c96447c87815d5360fe5e6358b6773c7573`: installed maintainability `SKILL.md`
  and eval catalog differ, `evals/files/setup_fixture.py` is missing, and the
  profile guide differs. This is pre-existing drift, not repaired by this brief.

## Stops and handoff

Stop for unresolved overlapping ownership, changed authority, user-work overlap,
unsafe permissions, new infrastructure, or a missing decisive verification
capability. Budget is a soft checkpoint; reduce repetition before expanding scope.

Next: separate Q-01 execution authorization → derived verification → ready
standalone preflight → bounded implementation. Immediately after implementation
or correction, hand the completed bytes to fresh independent acceptance review
through the applicable ordered conditional stages, fresh discovery and the
separate acceptance decision. End the authoring invocation; do not self-accept.
Keep results and numbered reviews in this package; preserve existing plan docs.
