# Verification Design: T-003.3 — Preserve correction obligations and current evidence

Source brief: docs/tasks/T-003.3/brief.md
Source brief revision: SHA-256 1b9e712aad4e5487459ab2db88c416b7a75395ea67dced7fba62f3c7871fae4c
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

The brief has no declared revision number; the digest identifies its bytes.
Normative sources are `docs/project-plan.md` (sections 1, 5–8, 10/T-003 and
11), `docs/task-map.json` (T-003), and `docs/tasks/T-003/brief.md` (P-03–07).
T-003.1 supplies the existing ordered route protocol; this leaf extends its
correction obligations. Ready describes this design, not execution readiness
or passing implementation behavior.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02, V-03 | Complete row/finding continuity, current evidence, independent owners and mixed-condition precedence. |
| AC-02 | V-03 | Seven change categories, conditional freshness, policy-authorized tests exception and actual-effect reference contrast. |
| AC-03 | V-04 | Unchanged-authority revision, stale readiness/evidence rejection, focused recovery and ordinary-effect controls. |
| AC-04 | V-05, V-06 | Reconciliation, targeted proof, failure suppression, current discovery-owned gate and omitted-row recovery. |
| AC-05 | V-07, V-08 | Stable dispositions, six justified new-blocker reasons, uncertainty and task-specific stops. |
| R-01 / INV-004/005/008 | V-01, V-02, V-03, V-08 | Failure, correction, next submission, mixed owners and stopped continuation without advancement. |
| R-02 / INV-003/005 | V-04 | Retained IDs, obsolete-ready substitution, focused ready, current proof and changed-requirement contrast. |
| R-03 / INV-008 | V-03 | Full change-category matrix, tests with/without exception, genuine/disguised reference change. |
| R-04 / INV-005/006/011 | V-01, V-05, V-06, V-07, V-08 | Unfinished sibling proof, aggregate ownership, stable/new dispositions and two-failed-fixes stop. |

## Evidence boundary and setup

This task changes human guidance and supplied qualification inputs. Audit the
source correction protocol, affected consumer/report guidance and fixture
expectations together. A correct new paragraph does not compensate for a stale
shortcut elsewhere. Focused contract checks must reject the relevant old or
plausibly wrong rule for its semantic error, rather than for missing setup.
Text/schema checks prove contract properties, not actual agent compliance.

Reuse the existing implementer `record-correction`, entry/ledger and route
fixtures; preflight revision-recovery/expected-effect cases; discovery
correction-gate, diagnostic-aggregate and late-omission cases; and acceptance
mixed-condition, stable-disposition and repeated-review contrasts. Extend only
missing task-local evidence. Current focused owners are
`tests/test_bounded_task_implementer.py`, `tests/test_task_preflight.py`,
`tests/test_task_review_discovery.py` and `tests/test_task_acceptance_review.py`.
Do not duplicate inherited rubric/recovery cases that already prove the same
obligation.

Supply legitimate fixture authority and context, baseline/changed bytes,
policy and conditional-stage evidence, stable IDs, revision artifacts,
attempts, concrete incomplete-capability facts and exact runnable probes. In a
disposable filesystem/Git workspace, execute the supplied production or public
validator probes to establish each claimed failure, correction or control.
Expected reports and route labels alone cannot establish those facts. Check
the route/continuation contract against these independently established facts;
do not fabricate intermediate stage outputs as composition evidence.

Preflight confirms dependency applicability, resolves exact setup/selectors
and required capabilities, and freezes the relevant commands. Run changed
cases fail-first, then only each changed owning module, sequentially, using the
brief's root command pattern:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <owning-module>.py`.
No whole-repository gate or new workflow gate is introduced here.

Report contract assertions, executed fixture behavior and unrun role compliance
separately. T-003.4 owns sibling-output composition and installed projection;
T-005 owns actual stage-output consumption and separately authorized agent
calls. The scenarios below specify this leaf's obligations at its own guidance
and fixture boundaries, not cross-task integration execution.

## Verification scenarios

### V-01 — Fixing one target preserves every continuation row

Covers: AC-01, R-01, R-04

Intent: Reject a handoff that drops an unfinished sibling, loses prior status,
or treats a prior pass/verdict as proof of changed bytes.

Given:
- A legitimate correction package has stable finding/scenario IDs and passed,
  failed, blocked and unchecked rows, including an unfinished influenced
  sibling row and a prior decision.
- The record-correction setup supplies a reproducible target defect and
  reviewer regression, with authority, preflight/context, invariant, attempts,
  affected scope and concrete reasons/owners for incomplete rows.

When:
- Establish the target failure at its supplied boundary, then inspect the
  correction contract and supplied next-submission state after a bounded fix
  passes its target probe.

Then:
- Every original finding/scenario and row remains identifiable with prior
  status, current implementation evidence or incomplete reason, and next owner.
- The handoff retains authority/preflight/context references, current scoped
  diff, invariant, attempts, influenced siblings, exact probes and gate record.
- The target's pass does not close the unfinished sibling or certify other
  changed bytes. Affected old evidence/verdict is stale and cannot authorize
  advancement; applicable fresh discovery and separate acceptance remain due.
- Implementation claims, conditional evidence, discovery facts and acceptance
  disposition remain attributed to their separate producers.

Oracle / boundary:
- Compare the before/after ID and row inventories with the published correction
  fields and fixture expectations. Trace each unresolved sibling through the
  next-owner/full-remainder handoff, even when the first target is green.
- Execute the target probe against the supplied failing/corrected bytes; audit
  evidence applicability against the actual diff, not the old verdict label.

Variants:
- Passed, failed, blocked and unchecked rows; stale prior pass and prior verdict.

### V-02 — Mixed conditions keep separate correction and recovery owners

Covers: AC-01, R-01

Intent: Reject collapsing a confirmed blocker and unfinished proof into a
single route, or allowing either non-success verdict to advance work.

Given:
- The existing mixed-condition setup has a currently demonstrated blocker and
  a distinct required blocked/unchecked row, with supplied context and evidence.
- One policy permits bounded correction; the contrasting policy prevents that
  correction through ambiguous authority, inseparable scope or unavailable
  permission/dependency. An authority question, when present, is distinct from
  routine uncertainty.

When:
- Establish the blocker and missing-proof facts, then audit correction and
  consumer expectations for each policy state.

Then:
- Authorized bounded correction yields `CHANGES_REQUESTED` despite the other
  unfinished row or separate unresolved material-context question.
- A prevented correction route yields `INCONCLUSIVE` while retaining the
  confirmed blocker. Missing decisive proof without a correction-eligible
  blocker also yields `INCONCLUSIVE`.
- Every finding and unfinished row keeps its reason and separate correction,
  evidence/capability or authority owner through the coordinator.
- Neither verdict permits advancement or treats unfinished proof as clean.

Oracle / boundary:
- Compare the source precedence/continuation rules and supplied decision
  expectations against the actual blocker, missing capability and policy facts.
  Trace all owner routes; the verdict alone is insufficient evidence.

Variants:
- Correction allowed/forbidden; required row blocked/unchecked; separate
  decision-critical authority question; missing proof without an eligible blocker.

### V-03 — Change effects determine the next owner and full remainder

Covers: AC-01, AC-02, R-01, R-03

Intent: Reject routing by filename/category label, skipping applicable stages,
or treating an evidence request as a production-fix request.

Given:
- Supplied policy, before/after bytes, conditional-stage completion evidence
  and current behavioral proof distinguish the cases below.
- T-003.1's ordered route fields name the first outstanding owner and full
  remainder. Prior evidence is either applicable to current effects or stale.

When:
- Inspect actual changed effects and probe results, then compare the correction
  guidance and case expectations with this matrix.

Then:

| Case | Required route obligation |
|---|---|
| Clarification | Clarifying artifact/evidence owner; no inferred production change or design restart. |
| Evidence request | Discovery/capability evidence owner, then a separate current acceptance decision; no automatic production-fix request. |
| Production correction | Repeat applicable conditional stages in .1 order, then fresh discovery and separate fresh acceptance. |
| Tests-only correction, no authorized exception | Retain applicable stage obligations; a tests-only label cannot waive policy. |
| Tests-only correction, policy-authorized exception | Apply only the explicit exception to its stated scope; retain every remaining current-evidence and decision obligation. |
| Genuine reference-only correction, current behavioral proof supports it | Registry updater → fresh acceptance may use the narrow route. |
| Reference-labelled correction changes an executable contract/behavior, or lacks applicable behavioral proof | Reject the narrow shortcut; repeat affected discovery/gates and obtain a current separate decision. |
| Scenario coverage change under unchanged requirements | Verification designer → focused preflight → revised-scenario evidence → new decision, as V-04 specifies. |
| Authority/requirement change | Task designer/decision owner; scenario editing cannot settle it. |

- For production cases, only currently satisfied applicable conditional stages
  can be omitted from the outstanding remainder. A required architecture gate
  precedes fresh maintainability, then applicable registry updater, discovery
  and separate acceptance; no gate is added without policy authority.
- Naming a next stage does not claim its execution or a decision.

Oracle / boundary:
- Compare actual diff/effects, explicit exception authority and current proof
  with the expected first owner and complete remainder. Execute the supplied
  contract/behavior probes for genuine versus disguised reference changes.
- Audit source and affected consumer guidance for the same distinctions; reject
  a shortcut justified only by a filename or changed-file category.

Variants:
- All matrix rows; neither/either/both conditional stages, current versus stale
  stage evidence, required versus unrequired architecture gate. Reuse .1's
  existing policy matrix; add only missing correction contrasts.

### V-04 — Coverage revision requires matching readiness and new evidence

Covers: AC-03, R-02

Intent: Reject new scenarios used with obsolete readiness, ID replacement,
old evidence relabelled as current, or ordinary corrections restarting design.

Given:
- Unchanged task authority has a demonstrated material coverage gap, original
  scenario IDs, revision-1 readiness and evidence, and supplied revision-2
  scenarios with a recorded coverage reason.
- Contrasts include feasible versus unavailable revised proof, a requirement
  change, and ordinary authorized correction/clarification/report effects.

When:
- Audit the revision/recovery contract against old readiness, focused new
  readiness and a subsequent substitution of old readiness, including a case
  with new scenario evidence but obsolete readiness.

Then:
- The gap returns to verification design; the reasoned revision retains
  original IDs and supersedes affected readiness/evidence.
- Old readiness cannot admit the revised work, even with new scenario proof;
  focused preflight must first produce applicable ready revision-2 guidance.
- Unavailable indispensable revised proof remains blocked with its concrete
  reason/owner. Feasible future tests need not already exist to obtain ready.
- After focused ready, current revised-scenario evidence supports a new
  decision; revision-1 evidence alone cannot close the new obligations.
- Changed requirements return to task design. Ordinary corrections and
  clarifications do not restart design; expected edits/reports alone do not
  invalidate readiness.

Oracle / boundary:
- Compare unchanged/changed authority bytes, scenario-ID inventories, revision
  reason, readiness bindings and evidence applicability in the supplied
  before/after artifacts. Probe the available fixture boundary to distinguish
  feasible proof from a concrete missing capability.
- Check both initial stale-ready rejection and old-ready substitution after
  recovery; fixture labels alone do not prove an entry/readiness decision.

Variants:
- Feasible/unavailable revised proof; stale ready with current evidence; old
  ready reintroduced after recovery; changed requirements; ordinary expected effects.

### V-05 — Correction discovery owns the justified aggregate record

Covers: AC-04, R-04

Intent: Reject a broad gate run despite decisive failure, a copied prior pass,
or acceptance repeating discovery's current aggregate.

Given:
- Authority, ledger, scoped correction, required/material rows, selected probes
  and conditional-gate policy are supplied and can be reconciled.
- Contrasts have decisive targeted failure, clean corrected targeted evidence,
  and concrete blocked/unchecked rows whose reasons are unrelated to a gate.

When:
- Execute the supplied targeted probes, then audit the source and fixture
  gate obligations for failed and clean correction reviews.

Then:
- Reconciliation precedes aggregate selection. All safely runnable material
  rows and selected probes receive current targeted proof; unfinished rows
  retain concrete non-gate reasons and owners.
- Decisive targeted failure suppresses the aggregate unless a distinct
  diagnostic purpose is authorized; any diagnostic run cannot imply acceptance.
- Clean targeted evidence permits one justified aggregate for that current
  discovery review. Record its exact command or not-run state, owner, stage,
  reason and current evidence; an old correction pass cannot replace it.
- Separate acceptance consumes that record without duplicate execution.
  Conditional gate owners retain IF-003 duties; this rule waives no required
  conditional proof and introduces no gate.

Oracle / boundary:
- Observe supplied failing/clean probe results, then compare reconciled rows
  and aggregate execution/not-run records with published ownership rules.
- Local fixture command observations establish fixture behavior; source/report
  audits establish the distinct discovery/acceptance obligations, not role execution.

Variants:
- Targeted failure without diagnostic authority; authorized distinct diagnostic;
  clean correction; concrete non-gate blocked/unchecked remainder; IF-003 gate duty.

### V-06 — A later omitted row needs targeted recovery before gate reconsideration

Covers: AC-04, R-04

Intent: Reject retaining a premature aggregate as complete evidence, or rerunning
it before proving a newly recovered material row.

Given:
- A supplied late-omission fixture has an earlier aggregate record and a
  material validator obligation omitted from targeted evidence.
- Existing clean/fail recovery variants supply valid and invalid public-entry
  inputs, including boolean revision, older active attempt and second running task.

When:
- Execute those public validator probes and inspect the recovery ledger and
  next gate obligation for both variants.

Then:
- The earlier aggregate is recorded as premature; the omitted row gets current
  targeted proof before any justified aggregate rerun.
- Clean recovery accepts valid input and rejects each supplied invalid input;
  aggregate rerun occurs only if still justified after reconciliation.
- The failing variant still demonstrates the intended boolean-revision defect
  while rejecting the other invalid inputs. Its decisive failure suppresses a
  routine aggregate rerun and retains correction/evidence ownership.
- Acceptance consumes the resulting current record without repeating the gate.

Oracle / boundary:
- Observe real public-validator outcomes for all supplied inputs. Match the
  clean/fail contrast to the retained material row and published recovery order.
- A green earlier aggregate or fixture setup success cannot close the omission.

Variants:
- Existing late-omission clean/fail fixtures; valid input and all three distinct
  invalid inputs. Preserve their current distinct boundary coverage.

### V-07 — Stable dispositions remain stable until material evidence changes

Covers: AC-05, R-04

Intent: Reject optional-fix loops or suppressing a genuine new blocker merely
because an earlier disposition was accepted.

Given:
- Existing acceptance fixtures supply an accepted bounded disposition with
  unchanged exposure/context and an optional improvement control.
- Contrasting current evidence demonstrates each authorized new-blocker reason:
  regression, formerly blocked evidence, missed obligation, changed context,
  changed authority, or newly demonstrated material risk.

When:
- Establish the unchanged versus changed exposure/evidence facts, then audit
  repeated-review/correction instructions and supplied expectations.

Then:
- Unchanged accepted dispositions remain preserved; preferences and optional
  improvements do not restart correction or become new blockers.
- A new blocker retains stable identity/provenance and cites current evidence,
  contextual materiality and the applicable reason. Earlier acceptance does
  not suppress a demonstrated regression or missed required obligation.
- Changed authority routes to its owner; a reviewer cannot invent requirements
  to justify a blocker. No global correction-round limit is introduced.

Oracle / boundary:
- Compare existing disposition/context with the independently supplied current
  trigger, consequence, exposure/mitigation and probe evidence for each reason.
  Audit fixture verdict/rationale expectations without redesigning T-002's rubric.

Variants:
- Stable accepted disposition, optional improvement and all six new-blocker
  reasons above; reuse the existing stable/regression/repeated-review contrasts.

### V-08 — Uncertainty and task-specific stops preserve bounded continuation

Covers: AC-01, AC-05, R-01, R-04

Intent: Reject routine clarification stops, silent third fixes of the same
failed target, or a stop converted into clean completion or a global round cap.

Given:
- Supplied context distinguishes ordinary uncertainty within current authority
  from unresolved credible serious-delay or materially costly-later consequences
  that current authority cannot settle.
- Existing scheduler recovery inputs record two materially different failed
  fixes of one target, their hypotheses, exact probes/results and partial diff.
  Separate cases reach a task/user budget or genuine cancellation/capability stop.

When:
- Audit continuation and stop guidance against those facts, using the supplied
  target probes to establish both failed-fix observations.

Then:
- Ordinary uncertainty continues under a stated reasonable assumption within
  authority; it alone causes no new blocker, design restart or routine user prompt.
- The unresolved serious-delay/costly-later exception retains a focused
  authority question, consequence and needed fact without inventing an answer.
- Two materially different failed fixes of the same target stop ordinary editing;
  preserve attempts, discarded hypotheses, partial diff, all unfinished rows,
  reasons and owned next approach. Do not silently attempt a third ordinary fix.
- Task/user budgets and genuine stops remain effective and retain all current
  findings/evidence/owners. Stopped work is non-complete and cannot advance.
- The same-target stop does not become a global correction-round counter.

Oracle / boundary:
- Compare context/authority and failed-probe observations with source stop rules
  and supplied continuation expectations. Trace retained rows and owners after
  each stop, rather than accepting a generic non-success label.

Variants:
- Ordinary uncertainty; unresolved serious-delay/costly-later exception;
  two distinct failed fixes of one target; task/user budget, cancellation and
  unavailable-capability stops.

## Implementation handoff

- Treat this file as derived guidance, not a replacement for the task brief.
- Preserve stable scenario IDs across a reasoned coverage revision. Revised
  guidance supersedes affected readiness/evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest authorized source/test changes that exercise these
  scenarios. Concrete test structure, helpers and placement remain implementation
  choices within the brief's allowed ownership; add no enforcement mechanism.
- Inspect canonical installer selection, profile guide and managed helpers when
  changing source skills. Synchronize only declarations affected by this task;
  do not refresh active `.agents/` copies or broaden installer ownership.
- Preserve sufficient inherited rubric/recovery coverage by reference. Hand
  T-003.4/T-005 exact fixture inputs, stable IDs, revision states, current probes,
  unfinished routes and explicit unrun role-compliance gaps.
- If a stated boundary cannot be exercised, route that conflict to task
  design/preflight rather than weaken its oracle. Implementation and independent
  acceptance are subsequent stages.
