# Verification Design: T-003.4 — Verify composed handoffs and installed source projection

Source brief: docs/tasks/T-003.4/brief.md
Source brief revision: SHA-256 5834ac29048b28f5cc22e62adf8cbcd2ed0c7b6e104af48cc5aa5e2e90445313
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

The brief has no declared revision number; the digest identifies its source
bytes. Normative sources are `docs/project-plan.md` (sections 1, 4–8, 10/T-003
and 11), `docs/task-map.json` (T-003), and `docs/tasks/T-003/brief.md` (P-01–07).
Ready describes this design, not dependency readiness or passing behavior.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02, V-09 | Full policy matrix, currentness/correction re-entry, complete blocker input and projected guidance. |
| AC-02 | V-02, V-03, V-04, V-05, V-08 | Stable identities, unfinished siblings and separate owners survive mixed routes, revision recovery, effect-based routing and regression contrasts. |
| AC-03 | V-03, V-06, V-07 | Current correction evidence, discovery-owned aggregate lifecycle, late coverage recovery and preserved stops. |
| AC-04 | V-09 | Complete changed-package projection and real committed-target reinstall within existing ownership. |
| AC-05 | V-10 | Reproducible local observations, fixture provenance and complete unrun role-call handoff to T-005. |
| R-01 / INV-003/004/005/006/008/011 | V-01–V-08, V-10 | P-01–06 cases at this leaf's guidance, fixture-input and probe boundaries; actual role consumption remains unrun. |
| R-02 / ART-009 / IF-003 | V-09, V-10 | Every changed selected package, guide/helpers, stale managed removal, unmanaged preservation and truthful installation evidence. |

## Evidence boundary and reuse

This leaf owns reconciliation of source/profile guidance, a new
`docs/tasks/T-003.4/composition.json`, local fixture observations and
`docs/tasks/T-003.4/results.md`. Its composition record references child-owned
inputs and oracles; it does not copy their entire setup or rewrite T-002.4
history. Audit field meaning and producer/consumer compatibility, not merely
stage-name presence or successful JSON parsing.

Reuse the following existing evidence obligations without redesigning sibling
tasks:

| Supplied child cases | Use here |
|---|---|
| T-003.1 verification V-01–V-03; implementer `route-cases` | Conditional policy, completion currentness and production re-entry in V-01. |
| T-003.2 verification V-01–V-04; maintainability `four-blockers` / `genuine-stop` | Four distinct blockers, preference control and bounded incomplete coverage in V-02/V-03. |
| T-003.3 verification V-01/V-02/V-08; implementer `record-correction` and acceptance mixed-condition inputs | Complete rows, separate owners, influenced siblings and stop history in V-03. |
| T-003.3 verification V-03/V-04; change-effect and existing readiness-recovery inputs | Reference effects, scenario revisions and authority contrasts in V-04/V-05. |
| T-003.3 verification V-05/V-06; discovery correction/diagnostic and late-omission inputs | Current probe facts and aggregate ownership/recovery in V-06/V-07. |
| T-003.3 verification V-07; acceptance stable-disposition/regression/repeated-review inputs | Stable deferral and optional-improvement contrast in V-08. |

Stage current source fixtures in disposable workspaces using existing
`tests/staging_fixture_support.py` where applicable. Supply legitimate task
authority, preparation/context, policy, baseline/changed bytes, stable IDs,
revision bindings, attempts, incomplete reasons/owners and exact probes.
Execute the relevant real production/validator probes before claiming their
facts. Labels, constructed reports and setup success cannot establish failure,
correction, readiness decisions or role compliance.

These scenarios concern T-003.4's own supplied inputs and source projection.
They neither design parent-level closure nor prove that separate agents
produced or consumed intermediate artifacts. T-005 retains that qualification;
V-10 requires a complete, explicitly unrun handoff.

## Verification scenarios

### V-01 — Every public route names the same first owner and remainder

Covers: AC-01, R-01

Intent: Reject a reconciled overview that skips a conditional stage, consumes
stale completion evidence or sends production correction directly to acceptance.

Given:
- Reviewed child contracts and supplied prepared `route-cases` inputs identify
  each policy, gate applicability and current/stale stage evidence.
- Initial and production-corrected submissions have explicit affected scope.

When:
- Compare root/profile/flow overview routes, source initial/correction templates
  and the disposable installed guide against the supplied states.

Then:
- With no current stage completion, the full route is the applicable row below;
  its first stage is the first outstanding owner.

| Conditional policy | Full route |
|---|---|
| Neither | Fresh discovery → separate fresh acceptance |
| Maintainability only; gate required | Architecture gate → fresh maintainability → discovery → acceptance |
| Maintainability only; no gate required | Fresh maintainability → discovery → acceptance |
| Registry only | Registry updater → discovery → acceptance |
| Both; gate required | Architecture gate → fresh maintainability → registry updater → discovery → acceptance |
| Both; no gate required | Fresh maintainability → registry updater → discovery → acceptance |

- Current applicable completion removes only satisfied stages; stale/missing
  completion leaves the obligation outstanding. In the both case, completed
  maintainability still leaves registry before discovery; completed registry
  cannot erase outstanding maintainability.
- Production correction re-enters every applicable stage whose proof is stale,
  then fresh discovery and separate acceptance. Guidance agrees on the full
  remainder and never treats naming a stage as executing it.

Oracle / boundary:
- Reconcile the supplied policy/currentness facts with each public route and
  V-09's installed guide bytes. Compare ordered obligations, not word counts.

Variants:
- All four policies; required/absent architecture gate where applicable;
  initial/corrected submissions and current/stale/missing stage evidence.

### V-02 — Four confirmed blockers reach correction without truncation

Covers: AC-01, AC-02, R-01

Intent: Reject a composition that carries only three findings, merges distinct
defects or expands review scope to satisfy a finding quota.

Given:
- The child-owned maintainability fixture has a committed baseline, changed
  scope, four independent defect oracles MNT-B1–MNT-B4 and a preference control.

When:
- Exercise the supplied defect/control probes and trace all four oracle-backed
  fixture findings into the composed correction input.

Then:
- The probes demonstrate duplicated rate-policy divergence, concrete SQLite
  coupling, loss of deterministic receipt rendering and disagreeing kind
  dispatch. The preference control remains non-blocking.
- All four finding identities and their location, evidence, consequence and
  correction direction remain available downstream; no cap or verdict-based
  early stop drops a finding. Carrying them adds no wider survey or quota.

Oracle / boundary:
- Observe real fixture operations and filesystem/Git changes using the existing
  maintainability owner; reconcile its four findings with the correction-input
  inventory. A supplied finding record remains fixture data.

Variants:
- All four independent defect probes and the existing preference control.

### V-03 — A corrected target cannot erase siblings, routes or stop history

Covers: AC-02, AC-03, R-01

Intent: Reject a green target used to close unfinished rows, collapse mixed
conditions to one owner or bypass an existing task-specific stop.

Given:
- Supplied correction inputs retain finding/scenario IDs, prior pass/fail/
  blocked/unchecked states, context, influenced siblings and current evidence.
- Mixed-condition inputs establish a real blocker and distinct missing proof;
  policy either permits or prevents bounded correction. Stop inputs retain two
  materially different failed fixes of one target or another existing stop.

When:
- Establish the supplied failure/correction and missing-capability facts, then
  trace the next guided and durable consumer inputs and continuation records.

Then:
- Every finding/row retains identity, prior state, current producer-attributed
  evidence or incomplete reason, and next owner. A target pass leaves unfinished
  siblings visible; changed bytes cannot inherit an old semantic verdict.
- Authorized bounded correction retains the `CHANGES_REQUESTED` route; prevented
  correction retains `INCONCLUSIVE` and the blocker. Correction, evidence and
  decision-critical authority routes remain separate; neither permits advancement.
- Genuine stops preserve attempts, hypotheses, partial changes, findings,
  unfinished rows and next owner. Two distinct failed fixes of the same target
  do not permit a silent third ordinary fix or create a global round counter.

Oracle / boundary:
- Compare before/after row inventories and both consumer forms against actual
  probe, policy and capability facts. Trace a corrected mixed submission with
  an unfinished influenced sibling; a verdict label alone is insufficient.

Variants:
- All four row states; authorized/prevented correction, blocked/unchecked proof
  and a separate material authority question; existing failed-fix, budget,
  cancellation and capability stops.

### V-04 — Revision recovery rejects obsolete readiness even after recovery

Covers: AC-02, R-01

Intent: Reject changed scenario IDs, new proof admitted under old readiness or
using verification edits to decide changed requirements.

Given:
- Unchanged authority has a material coverage gap, original IDs, revision-1
  readiness/evidence and reasoned revision-2 verification inputs.
- Existing recovery inputs distinguish feasible/unavailable revised proof and
  changed requirements from expected correction/report effects.

When:
- Trace old-ready rejection, focused new readiness and revised evidence into
  the next decision input; then substitute old readiness again.

Then:
- Original IDs and the revision reason survive. Affected old readiness/evidence
  is superseded; current revised-scenario proof alone cannot rescue old readiness.
- Focused ready for the new revision precedes its evidence/new-decision route.
  Reintroduced old readiness remains inadmissible; indispensable unavailable
  proof retains its reason/owner rather than becoming ready.
- Changed requirements return to task design/decision owner. Ordinary authorized
  correction and expected report effects alone do not restart task design.

Oracle / boundary:
- Compare authority bytes, scenario inventories, revision/readiness bindings,
  available capability facts and consumer admission guidance. Constructed ready
  records specify inputs; they do not prove an actual preflight decision.

Variants:
- Feasible/unavailable revised proof; old-ready with current proof, including
  substitution after recovery; changed requirements and ordinary expected effects.

### V-05 — Actual effects distinguish reference, evidence and production routes

Covers: AC-02, R-01

Intent: Reject a reference filename used to bypass affected discovery or an
evidence request converted into an unauthorized production fix.

Given:
- Existing change-effect inputs supply before/after bytes, explicit policy,
  current proof and genuine/disguised/missing-proof reference contrasts.

When:
- Inspect actual effects and run the supplied valid/invalid contract probes;
  reconcile composed first-owner/full-remainder expectations with source guidance.

Then:
- Genuine reference-only correction with applicable behavioral proof retains
  registry updater → fresh acceptance. Executable/behavioral effects or absent
  applicable proof require affected discovery/gates and a current separate decision.
- Clarification and evidence requests retain their artifact/evidence owner;
  neither implies a production fix. Production corrections follow V-01.
- A tests-only label waives nothing by itself; only an explicit policy exception
  changes its stated obligations. Scenario and authority routes remain as V-04.

Oracle / boundary:
- Compare real diff/probe effects, submitted proof applicability and exception
  authority with the source and composed routes. The genuine contract rejects
  boolean revision; the executable-reference defect admits it despite its label.

Variants:
- Genuine/disguised/missing-proof reference; clarification/evidence/production;
  tests-only with/without authorized exception; scenario/authority change.

### V-06 — Correction carries current evidence and a discovery-owned gate record

Covers: AC-03, R-01

Intent: Reject a copied prior gate pass, aggregate execution despite a decisive
failure or acceptance assigned a duplicate aggregate run.

Given:
- Existing failure, correction, clean-discovery and diagnostic inputs supply
  authority, required rows, selected probes, changed bytes and conditional policy.

When:
- Execute the supplied failure/corrected public probes and trace current evidence
  and the aggregate record through the composed discovery/acceptance inputs.

Then:
- Failure and the next legitimate occurrence distinguish defective from corrected
  behavior; all safely runnable required/material rows and selected probes have
  current targeted evidence before routine aggregate proof.
- Decisive failure suppresses a routine aggregate; a separately authorized
  diagnostic purpose cannot erase failed/incomplete rows or authorize acceptance.
- Clean discovery owns one justified aggregate for its current review. Its record
  names exact command or not-run state, current evidence, reason, owner and stage;
  prior evidence cannot substitute. Concrete incomplete reasons remain visible.
- Separate acceptance consumes the record without duplicate execution.
  Applicable conditional gate owners keep their separate duties.

Oracle / boundary:
- Observe actual repeated public-operation outcomes, then reconcile evidence
  identities and gate-record fields/order against discovery and acceptance
  contracts. Local command execution is fixture evidence, not role execution.

Variants:
- Targeted failure, clean correction, authorized distinct diagnostic and concrete
  non-gate incomplete reasons; applicable conditional gates.

### V-07 — Late omitted coverage invalidates premature aggregate proof

Covers: AC-03, R-01

Intent: Reject an earlier green aggregate used to close an omitted material row
or a rerun scheduled before that row's targeted recovery.

Given:
- Existing late-omission clean/fail inputs retain an earlier aggregate record,
  the omitted row and valid/targeted-invalid public validator inputs.

When:
- Exercise the validator inputs and trace recovered-row evidence and next gate
  obligations through the composed continuation.

Then:
- The earlier record remains explicitly premature. The omitted row receives
  current targeted proof before discovery reconsiders a still-justified aggregate.
- Valid input passes. Clean recovery rejects boolean revision, an older active
  attempt and a second running task; defective recovery still admits the boolean
  revision while rejecting the other two, retaining correction/evidence owners.
- Decisive recovery failure suppresses the routine aggregate. Acceptance consumes
  the current record without rerunning it.

Oracle / boundary:
- Observe all four real validator outcomes in both existing variants; reconcile
  their retained row and record order. Setup or the prior pass cannot close it.

Variants:
- Existing clean/fail recovery; valid input and all three distinct invalid inputs.

### V-08 — Stable deferral and optional improvement cannot hide a regression

Covers: AC-02, R-01

Intent: Reject optional-fix loops or an old accepted disposition used to erase
current material failure.

Given:
- Existing acceptance inputs supply an unchanged accepted disposition, optional
  improvement control and current regression/repeated-review contrasts.

When:
- Establish the supplied exposure/probe facts and trace finding provenance and
  disposition obligations into correction and next-decision inputs.

Then:
- Unchanged exposure retains the accepted disposition; optional improvement does
  not create correction. A real regression or missed required obligation remains
  visible with current evidence, materiality and its justified reopening reason.
- Formerly blocked proof, changed context/authority and newly demonstrated
  material risk keep their existing distinct reasons; authority changes return
  to their owner. No new requirement or global correction limit is introduced.

Oracle / boundary:
- Compare supplied prior/current context, finding identity and actual probes with
  continuation and disposition contracts; a prior accepted label cannot waive
  a demonstrated current failure.

Variants:
- Stable deferral/optional improvement and the existing six reopening reasons:
  regression, formerly blocked evidence, missed obligation, changed context,
  changed authority and newly demonstrated material risk.

### V-09 — Install and reinstall project every changed package within ownership

Covers: AC-01, AC-04, R-02

Intent: Reject top-level skill-only projection, omitted setup/reference files,
stale managed bytes or replacement of unmanaged target content.

Given:
- A disposable target has a real committed Git baseline, unrelated files and
  `AGENTS.md` text. Source inventory identifies all selected packages changed
  by reviewed .1–.3 outputs and current guide/helper declarations.
- Existing installer cases already cover preparation, discovery and acceptance
  package families; add only missing distinct projection evidence.

When:
- Run the canonical installer, compare projected contents, add stale managed
  bytes and unmanaged skill/helper/file sentinels, then run it again.

Then:
- Both installations project complete relative-file inventories and bytes for
  every changed selected package, including references, eval metadata and setup
  files, plus the current profile guide and declared sibling helpers.
- Installed maintainability setup and implementer correction template are present
  and equal current source. Installed guide routes satisfy V-01.
- Reinstall removes stale managed files/restores managed bytes; unmanaged files,
  helpers, skill packages and text outside the single managed AGENTS block survive.
- Selection/helper declarations change only if actual child outputs require it;
  installer ownership remains narrow and active repository `.agents/` is untouched.

Oracle / boundary:
- Observe real installer CLI results and complete source/target package byte
  inventories, before/after sentinels, guide/helpers and AGENTS block/text in
  the committed target. Verify committed setup, not an invented HEAD.
- Current affected families are implementer, maintainability, registry updater,
  discovery and acceptance; preflight confirms this inventory against child diffs.

Variants:
- Every changed selected family; first install and reinstall with stale managed
  content plus unmanaged sentinels. No unborn/drift-check or active-refresh claim.

### V-10 — Results and T-005 handoff retain truthful evidence boundaries

Covers: AC-05, R-01, R-02

Intent: Reject historical proof treated as current, constructed intermediate
records relabelled as role outputs or a local pass claimed as installed-flow
behavioral qualification.

Given:
- The task-owned composition record, current local observations and disposable
  package projection exist; separate role calls remain unrun.

When:
- Audit new `results.md` and its T-005 handoff against raw commands, fixture
  identities, probe outcomes, installation inventories and intended interfaces.

Then:
- Results distinguish contract structure/audit, real fixture/filesystem/Git
  observations and unrun agent behavior. Constructed intermediate artifacts
  remain labeled fixture data; old reports/results are unchanged.
- T-005 receives exact setup/commands and starting state, current source/projected
  package identities, intended producers/consumers, required inputs/oracles and
  every unrun separate-call boundary with reason and owner.
- The inventory covers implementer → applicable conditional owners → discovery →
  separate acceptance, correction re-entry, revised verification → focused
  preflight → current evidence/new decision, and mixed correction/evidence/
  authority continuation. Local fixtures do not claim those calls occurred.

Oracle / boundary:
- Trace every result claim and intended consumption boundary to current observed
  evidence or an explicit T-005 gap. Structural success cannot upgrade a gap.

Variants:
- Contract, local runtime/filesystem/Git and unrun role evidence categories;
  every supplied route/recovery variant from V-01–V-09.

## Verification execution handoff

Use the brief's targeted composition and installer commands first, sequentially,
after dependency/setup readiness. Preserve predecessor cases; reuse existing
canonical probes rather than duplicate them in a new harness. Run changed cases
before their owning modules. Module selectors use the existing root pattern:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

The affected aggregate union is composition, guide, implementer, maintainability,
preflight, discovery, acceptance and installer owners, plus the existing
mixed-condition and known-issue/regression probe owners. Those last two supply
canonical fixture facts for V-03/V-08 without copying their tests. After current
required targeted rows/probes are clean, fresh discovery owns the justified
union below from the repository root; preflight checks command resolution and
affected ownership before freezing it:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition test_task_flow_guides test_bounded_task_implementer test_task_maintainability_review test_task_preflight test_task_review_discovery test_task_acceptance_review test_contextual_uncertainty_inputs test_contextual_known_issues test_install_development_skills
```

This finite union covers route/consumer changes, recovery inputs, actual reused
fixture facts and package projection. It excludes unrelated repository tests.
Discovery records the exact command or not-run state, reason, owner/stage and
current evidence under IF-004; acceptance consumes it without duplicate execution.
A focused failure suppresses routine aggregate proof. Late coverage recovery
follows V-07; conditional gate owners retain their duties. No whole-repository,
live-network or model-budget gate is part of this design.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Standalone preflight must confirm reviewed dependencies, current
  ownership, setup, permissions and the source/scenario revision before entry.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness/evidence until focused preflight
  produces a ready result for that revision.
- Implement the smallest authorized source/test changes that satisfy the brief
  and exercise these scenarios. Test structure, helpers and placement remain
  implementation choices within the brief's scope; add no checker or role runner.
- Inspect canonical installer selection, profile guide and helper declarations;
  synchronize only changes required by child outputs. Do not refresh active
  `.agents/`, edit official plans/history or write real known issues.
- If discovery finds a child contract mismatch, missing decisive capability or
  an unexercisable boundary, route it to task design/preflight or the owning child;
  do not weaken the oracle or expand this leaf's policy ownership.
- Local composition/projection evidence is not acceptance or parent closure.
  After implementation, follow the required fresh independent review route;
  T-005 receives exact reusable inputs and all unrun role-compliance gaps.
