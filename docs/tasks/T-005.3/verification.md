# Verification Design: T-005.3 — Exercise independent contextual review decisions

Source brief: docs/tasks/T-005.3/brief.md
Source brief revision: SHA-256 `0f577d56b18fe48368d6b096a6ef625ca5b64c54e7a4c5db46037fb1d0169fe0`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

This status applies to the verification design only. Standalone guided preflight
must resolve current dependency/installation identities, raw-call isolation,
held-back evaluator inputs, invocation capability and concrete call authorization.
This file authorizes no role calls or model-budget checks and claims no observed
qualification. Use the supplied T-005.1 inventory and consumer-input manifests;
staged reports remain labeled history.

## Coverage summary

| AC / risk row | Scenarios | Notes |
| --- | --- | --- |
| AC-01 | V-01, V-02, V-09 | Actual independent producer-to-consumer provenance, current preparation/byte identities, aggregate ownership and truthful claim boundaries. |
| AC-02 | V-02, V-03, V-08 | Wrong-green and weak/stale proof cannot advance; inherited finite cases retain current evidence or explicit gaps. |
| AC-03 | V-04, V-05 | Material exposure blocks despite passing ACs; mitigated debt may defer; preferences stay observations. |
| AC-04 | V-02, V-05, V-06 | Ordinary/resolved uncertainty continues; exceptional questions and missing-proof requests reach distinct owners. |
| AC-05 | V-05, V-07, V-09 | Mixed-condition precedence retains every route; actual deferral or explicit unrun gap reaches T-005.4. |
| D-01 / INV-004/005 | V-01, V-02, V-03, V-09 | Separate calls, author self-check, complete/partial/stale proof and retained real boundaries. |
| D-02 / INV-006/011 | V-04, V-05, V-08 | Operating/business/refactoring exposure, catastrophic and required-consumer consequences, mitigation and stable versus reopened dispositions. |
| D-03 / INV-011 | V-02, V-06 | Observe actual prompt behavior, assumptions and evidence-owner versus authority-owner routing. |
| D-04 / INV-005/006/008 | V-07 | Authorized and prevented bounded correction with JOB-PAIR blocked/unchecked; neither verdict advances. |

## Verification scenarios

### V-01 — Acceptance consumes the actual independent discovery output

Covers: AC-01; D-01 / INV-004/005

Intent: Reject a staged report substituted for a producer, merged reviewer roles,
an author presented as independent, or duplicate acceptance-side verification.

Given:
- Supplied current code/tests, task authority, verification revision, ready
  preflight/context and submission identities for a selected prepared case.
- Qualified disposable installed copies with their own sibling helpers; evaluator
  setup, expected answers and grading oracles are outside reviewer inputs,
  including accessible index/history/Git objects.

When:
- An authorized fresh discovery invocation examines those inputs and its raw
  report is retained before grading.
- A separate independent acceptance invocation consumes that exact report and
  its preparation references/current identities.

Then:
- Discovery supplies evidence, rows/findings and its aggregate record, without
  an advancement verdict or approved deferral.
- Acceptance identifies and admits the actual report and current preparation
  context without broad rediscovery, repeated probes or duplicate aggregate
  execution. Any justified aggregate remains discovery-owned, with command or
  not-run status, stage, reason and current evidence.
- An authoring-session contrast remains `SELF_CHECK_ONLY`, has no independent
  verdict and cannot supply independently corroborated rows or advance work.

Oracle / boundary:
- Compare raw invocation provenance and consumed report bytes/identity, actual
  input visibility and action/write records. Report wording alone cannot prove
  independence or absence of duplicate execution. Reuse qualified projection
  receipts only after their current applicability is checked.

Variants:
- Prepared handoff references from IFQ-03 and the applicable COMP-05 provenance
  contrast; INV-CASE-18 authorship. This does not close T-005.2 preparation work.

### V-02 — Green tests do not conceal failure or incomplete current proof

Covers: AC-01, AC-02, AC-04; D-01 / INV-004/005; D-03 / INV-011

Intent: Reject clean advancement based on passing tests, partial reports, stale
identities or a weak oracle that misses an actual AC failure.

Given:
- A wrong implementation with passing submitted tests and a decisive public
  probe of its AC violation; a clean contrasting implementation with current
  required proof; and missing/weak or stale required-proof controls.
- Actual separate discovery reports for claimed composed decisions, with all
  selected rows and their evidence states visible.

When:
- Acceptance admits each report against the current authority and reviewed
  worktree/index identities.

Then:
- A demonstrated AC failure cannot produce clean advancement; an eligible
  authorized bounded correction yields `CHANGES_REQUESTED`.
- In the supplied queue defect, the first real public call claims TASK-1 but
  the next fails to claim the still-ready TASK-2; the clean contrast claims
  TASK-2 on that next call. A one-call or state-only check cannot distinguish it.
- Without a correction-eligible confirmed blocker, missing/weak decisive proof
  yields `INCONCLUSIVE` and a focused request to its discovery/capability owner.
  It is not turned into a generic user choice or an assumed production fix.
- Partial or stale evidence is not copied as a current pass. Matching worktree
  bytes and short status do not establish matching index blobs.
- The clean/current contrast is eligible for acceptance when all other required
  obligations pass. Every unfinished row retains its ID, reason and next owner.

Oracle / boundary:
- Compare actual public-probe observations, raw discovery rows, worktree/index
  identities and acceptance disposition/routes. The expected failure must be
  the AC violation, rather than setup/import/timeout failure.

Variants:
- Complete, partial/missing, weak and stale report/evidence; wrong-green repeated
  public operation versus clean/current proof; INV-CASE-07 index/worktree contrast.

### V-03 — Every retained case keeps its decisive boundary and evidence state

Covers: AC-02; D-01 / INV-004/005

Intent: Reject an inventory that keeps case names while losing lifecycle,
validator, process or continuation obligations.

Given:
- Read-only T-005.1 inventory/receipts and inherited case authority, including
  this leaf's INV-CASE-01–03 and 06–18, COMP-01/02, CCR-05/08, DISP-01 and IFQ-03.
- Current owning-test references and renewed evidence where needed; other
  inherited cases retain their declared owners.

When:
- Reconcile each retained case with the results ledger and its actual evidence
  or explicit gap. Exercise selected available probes at their existing boundary
  rather than replacing them with report/schema checks.

Then:
- Public queue repetition uses the first state change and next real invocation;
  exporter resume uses real persisted recovery state. Ledger cardinality,
  ordering/type confusion and selected/non-selected entities remain represented.
- Workflow coherent tampering, replay and decision-boundary cases retain their
  independent rows, including recomputed internal digests.
- Validator proof includes a valid instance exiting 0 and targeted boolean-
  revision, older-attempt and second-running invalid instances exiting 2 in
  the clean control. The faulty control accepts the boolean-revision instance
  (exit 0) while the other invalid controls still reject (exit 2); it cannot
  establish a clean validator pass.
- Process rows PROC-RESIST, PROC-PIPE and PROC-RACE retain observable
  synchronization, bounded cleanup, pipe-release evidence and confirmation
  that no fixture process survives; arbitrary sleeps do not supply proof.
- Continuation preserves row/finding IDs, reviewer regressions and consumed
  gate status. Earlier passes are reconciled with current evidence.
- Each case is mapped to current evidence at that boundary or a concrete gap
  with its owner; omission and a green sibling row cannot waive it.

Oracle / boundary:
- Audit the ledger against the supplied inventory and inherited oracles, then
  inspect referenced CLI/persisted-state, validator exit, Git identity and real
  process observations. Reuse applicable evidence; do not rerun every case for
  ceremony or claim new role behavior from existing local results.

Variants:
- All finite retained families above, including valid/targeted-invalid pairs
  and pass/fail/blocked/unchecked rows. Preserve sibling-owned cases without
  taking over their composition closure.

### V-04 — Material exposure blocks despite passing ACs

Covers: AC-03; D-02 / INV-006/011

Intent: Reject severity-only judgment or a permissive decision that ignores
material facts found only in readiness context.

Given:
- Passing ACs/tests in the supplied contextual-risk context, including material
  operating/business/refactoring exposure and a preflight-only exposure fact.
- Actual discovery evidence for each concern; evaluator expectations are held
  back from both reviewers.

When:
- Discovery selects decisive bounded probes using preflight context and
  acceptance evaluates the resulting current findings.

Then:
- Confirmed material findings block with `CHANGES_REQUESTED` under the supplied
  bounded correction authority, despite passing ACs and green tests.
- Reasons connect trigger, consequence, affected boundary, impact,
  likelihood/exposure, mitigation and why deferral is inadequate.
- The preflight-only nightly-regeneration fact informs the operating-risk
  decision. Low likelihood does not erase catastrophic irreversible directory
  destruction. Declared required-consumer breach remains material even when
  the AC text omits the header. Demonstrated duplicated parsing authority with
  credible same-kind planned change is evaluated without demanding a formal
  future ticket or hard-rule breach.
- Preferences and unproved concerns remain observations, not correction work.

Oracle / boundary:
- Trace COMP-01's preflight fact into an actual discovery probe and separate
  acceptance rationale. Inspect substantive consequence/exposure reasoning
  for every finding, rather than treating severity labels as the oracle.

Variants:
- Supplied operating/business, catastrophic low-likelihood, required-consumer
  and refactoring cases; speculative preference/unproved concern controls.

### V-05 — Existing mitigation supports a bounded deferral handed to the coordinator

Covers: AC-03, AC-04, AC-05; D-02 / INV-006/011

Intent: Reject both fix-everything judgment and deferral based on speculative
future work instead of existing safeguards and compatible consumers.

Given:
- The mitigated contextual contrast with passing required proof, an actual
  bounded non-material footer finding, existing atomic-write safeguard and a
  declared consumer that treats the footer as informational.
- A proposed migration, speculative preferences and an ordinary timezone
  unknown are distinguished from established safeguards/facts.

When:
- Separate discovery and acceptance calls assess the supplied mitigated context.

Then:
- `ACCEPT` with an approved bounded deferral is justified by bounded impact,
  actual mitigation and consumer compatibility. Proposed uncommitted work is
  not counted as existing mitigation.
- The decision provides stable issue/finding and task/review provenance,
  trigger/consequence/evidence, impact/likelihood, affected boundary/consumers,
  rationale, follow-up owner/action and reassessment conditions for recording.
- The consumer contract settles footer tolerance locally; the ordinary timezone
  unknown proceeds under a stated assumption without a routine user prompt.
  Preferences and unproved concerns stay observations.
- Reviewers write no tracker/known-issues record and do not advance work. The
  raw accepted disposition is handed to T-005.4 for coordinator recording before
  authorized advancement; an unrun decision supplies an explicit gap instead.

Oracle / boundary:
- Inspect raw decision, consumed actual discovery evidence, context-based
  rationale, recording fields and reviewer write records. A staged deferral
  cannot be represented as the real decision consumed by T-005.4.

Variants:
- Supplied mitigated/bounded-debt context versus V-04 material exposure;
  optional context links may be absent and do not affect eligibility.

### V-06 — Questions depend on unresolved serious consequences

Covers: AC-04; D-03 / INV-011

Intent: Reject routine prompts for ordinary uncertainty and assumptions that
conceal unresolved serious-delay or materially costly later-repair risk.

Given:
- Current passing required proof and supplied uncertainty contexts: an ordinary
  unknown, unresolved consequential retention-region uncertainty, serious-delay
  exposure, and locally resolved contrasts for the serious cases.
- Supplied policy/deadline facts are available where authorized; no required
  proof gap is disguised as a context question.

When:
- Separate discovery/acceptance calls assess each context and attempt resolution
  within the existing authority before escalation.

Then:
- Ordinary uncertainty continues with a recorded reasonable assumption and
  observation, without a user prompt or new blocker.
- Authorized local policy resolves the serious contrasts; passing evidence
  remains admitted and the decision continues without a region/permission
  question. Serious consequences alone do not force escalation once resolved.
- When current authority cannot settle the decision-critical fact, the decision
  is `INCONCLUSIVE` with one focused authority-owner question through the
  coordinator. It names the needed region fact and irreversible wrong-horizon
  consequence/materially costly recovery, or the supplied serious contractual
  delay/service-suspension consequence. It does not invent the region or waive
  proof. Missing required proof follows V-02's evidence-owner route.

Oracle / boundary:
- Inspect actual invocation prompts/questions as well as raw reports, assumptions,
  permitted local reads and next owners. A report saying “no prompt” does not
  override an observed routine question in the invocation record.

Variants:
- Ordinary unknown; unresolved costly-later and serious-delay contexts; locally
  resolved consequential and serious-delay contrasts from supplied fixtures.

### V-07 — Mixed conditions retain distinct correction, evidence and authority routes

Covers: AC-05; D-04 / INV-005/006/008

Intent: Reject blanket inconclusiveness despite authorized correction, a verdict
that ignores prevented correction, or dropping unfinished proof after a blocker.

Given:
- COMP-02/CCR-05's confirmed eligible blocker F-01, JOB-PAIR blocked/unchecked
  proof and unresolved ordering/consumer-contract question.
- Contrasting supplied run policies authorize or prevent bounded production
  correction while leaving the finding and unfinished evidence visible.

When:
- Separate discovery and acceptance calls assess each policy/context pair.

Then:
- Authorized bounded correction yields `CHANGES_REQUESTED` despite unfinished
  JOB-PAIR proof and the separate unresolved question.
- Prevented correction yields `INCONCLUSIVE`, retains the blocker and names
  the authority/permission constraint rather than attributing it to ordinary
  uncertainty.
- Both decisions preserve all finding/row IDs, reasons and evidence states;
  correction goes to the owning implementer, JOB-PAIR capability/evidence to its
  discovery/capability owner, and the unresolved authority question through the
  coordinator. Neither decision invents the missing helper or advances work.

Oracle / boundary:
- Compare actual raw decisions against the supplied correction policies; trace
  F-01, JOB-PAIR and the question through complete separate continuation routes.

Variants:
- Authorized versus prevented bounded correction; supplied blocked/unchecked
  proof states remain distinct and never become a clean row.

### V-08 — Stable dispositions survive while demonstrated new blockers remain visible

Covers: AC-02, AC-03; D-01 / INV-005; D-02 / INV-006/011

Intent: Reject needless reopening under unchanged compatible exposure and copying
an old disposition over a current regression or missed obligation.

Given:
- CCR-08/DISP-01 supplied prior decisions as labeled history, current actual
  discovery evidence and the relevant unchanged/changed exposure contrasts.

When:
- Acceptance reconciles current findings and retained rows against that history.

Then:
- Unchanged compatible exposure preserves justified accepted dispositions;
  optional improvements do not restart correction.
- A demonstrated current regression, previously blocked proof now exposing a
  defect, missed existing obligation, changed context/authority or newly
  demonstrated material risk retains its finding and justified reopening reason.
- Old passes never replace current proof; all unfinished rows remain explicit.
  Acceptance consumes discovery's aggregate record without re-execution.

Oracle / boundary:
- Compare supplied prior/current evidence and exposure with raw decision reasons
  and stable finding/row IDs. This is disposition observation within this leaf,
  not execution of T-005.5's correction campaign or T-005.4's later preflight.

Variants:
- The supplied stable-disposition and regression/reopening contrasts represented
  by CCR-08/DISP-01; no invented repeated-review requirements.

### V-09 — Results distinguish observed qualification from unavailable calls

Covers: AC-01, AC-05; D-01 / INV-004/005

Intent: Reject qualification claims inferred from structural tests, unauthorized
calls, overwritten raw evidence or unauthorized reviewer effects.

Given:
- Case-local results/evidence, before-state of protected files/Git state and
  current call/projection receipts; any unavailable/unapproved capability is
  identifiable with its next owner.

When:
- Audit each claimed decision and the handoff to T-005.4 against raw evidence
  and the protected after-state.

Then:
- Each claim supplies authority/context, starting state, actual implementation/
  tests, exact setup/probes, expected oracle, output identity, observed result
  and next owner. Qualification pass/fail/blocked/unchecked is separate from
  the fixture verdict: observing correct rejection may pass qualification while
  the fixture task remains blocked.
- Unapproved/unavailable calls are explicitly unrun with reason/owner; no staged
  report or local test pass fills the missing observed handoff or certifies full
  behavioral qualification. Failures and all unfinished rows survive.
- T-005.4 receives the actual raw deferral decision or its explicit unrun gap.
  No real known-issue record is seeded from a fabricated/unrun decision.
- Raw outputs remain preserved before grading. Protected source/tests,
  inventories/receipts, active installation, plans/history and tracker state
  are unchanged; only authorized task-local artifacts/adapters and disposable
  corrections change. No process or temporary fault remains after probes.

Oracle / boundary:
- Reconcile results with raw outputs, authorization/identity receipts, actual
  filesystem/Git before/after evidence and process cleanup records. A document
  or syntax check proves only its stated structural property.

Variants:
- Observed accepting/rejecting decisions and any explicit unrun/blocked case;
  no unauthorized call is made merely to exercise the unrun contrast.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  brief. Preserve stable scenario IDs across a reasoned coverage revision;
  affected readiness/evidence stays superseded until focused preflight is ready.
- Resolve execution/authorization, current supplied identities and held-back
  inputs in standalone guided preflight before implementation. Do not refresh
  the active installation or launch model-budget checks from this design.
- Reuse current owning fixtures/tests and applicable T-005.1 evidence. Renew
  selected probes before any justified aggregate, sequentially; discovery owns
  the fixture-review aggregate and acceptance consumes it. No full-suite/live
  gate is added. Check protected state and `git diff --check`.
- Implement the smallest allowed task-local changes. Concrete test structure,
  framework usage, helpers and placement remain implementation choices unless
  already fixed by authority; this design prescribes no production repair.
- If a scenario cannot be exercised at its stated boundary, route capability
  uncertainty to preflight or an authority/oracle conflict to task design.
  Keep explicit gaps rather than silently weakening the oracle.
- Supply the deferral decision/gap to T-005.4 and retain evidence for the named
  later consumers; do not perform their tracker, correction or final audit work.
