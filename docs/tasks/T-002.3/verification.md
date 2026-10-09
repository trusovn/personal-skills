# Verification Design: T-002.3 — Apply contextual risk and coordinator-owned deferrals

Source brief: docs/tasks/T-002.3/brief.md
Source brief revision: SHA-256 `5c8ae6113f6be1e38c1fda58efa7caba5b889306401978bf60e31b3867000ec2`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

Normative references: [brief.md](brief.md); [project-plan.md](../../project-plan.md),
sections 1, 4, 6, 7, 10 (T-002), and 11; [task-map.json](../../task-map.json),
T-002; parent [brief.md](../T-002/brief.md), P-04–07.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02 | Contextual materiality, separate impact/exposure, mitigated contrast, and complete finding rationale. |
| AC-02 | V-02, V-03, V-04 | Bounded deferral versus observation; ordinary versus consequential unknowns; required proof remains binding. |
| AC-03 | V-04 | Exact mixed-condition precedence, retained rows, separate owners, and no advancement. |
| AC-04 | V-05, V-07 | Coordinator record contract and independently supplied relevant/unrelated consumer cases. |
| AC-05 | V-06, V-07 | Optional context semantics, planned work, portfolio limits, and changed material facts. |
| AC-06 | V-06, V-08 | Stable dispositions, justified new blockers, optional fixes, and existing stop rules. |
| R-01 | V-01, V-02 | All six named cases; preflight-only exposure and refactoring risk without a hard-rule breach. |
| R-02 | V-04 | Allowed/forbidden bounded correction, missing proof alone, and unresolved context beside a blocker. |
| R-03 | V-03, V-04 | Stated assumptions, authority-resolvable uncertainty, necessary escalation, and evidence-owner routing. |
| R-04 | V-05, V-06, V-07, V-08 | Record provenance, consumer compatibility, unchanged/changed exposure, and priority-only changes. |

## Evidence scope and setup

This design verifies T-002.3's contextual decision and recording/consumer
contracts. Use supplied task authority, operating/business/consumer and credible
maintenance context, legitimate implementations and tests, and current admitted
reports with stable finding and unfinished-row IDs. Runnable fixture probes must
establish the asserted trigger, consequence, mitigation, or compatibility;
expected verdict text cannot establish those facts by itself.

Local contract checks establish what source guidance and report/eval contracts
require. Local runnable fixture checks establish the underlying facts and setup.
Neither proves an agent made the intended decision, asked a question, or obeyed
writer permissions. Preserve those behavioral gaps for T-005; T-002.4 owns local
cross-stage composition. Record and later-consumer scenarios below use supplied
stage inputs independently, without executing a sibling-task pipeline.

## Verification scenarios

### V-01 — Material consequences block despite green evidence or low exposure

Covers: AC-01, R-01

Intent: Reject unconditional acceptance on green tests, severity-only judgments,
and a rubric that requires a hard-rule breach before material risk can block.

Given:
- Current admitted evidence and explicit context support each case below.
- An authorized bounded correction is available for each blocking case.
- Contrasting contexts keep the concern comparable and state the changed
  exposure, consequence, consumer obligation, or existing safeguard explicitly.

When:
- Apply the contextual disposition contract to each supplied case.

Then:

| Supplied case | Required distinction |
|---|---|
| Demonstrated AC violation with green tests | CHANGES_REQUESTED; green tests cannot excuse the violated authority. |
| Passing ACs with demonstrated material operating or business risk | CHANGES_REQUESTED with credible exposure/consequence and inadequate-mitigation rationale. |
| Required consumer breach | CHANGES_REQUESTED tied to that consumer obligation. |
| Introduced/worsened coupling, duplicated authority, locality, or testability with a credible material maintenance/refactoring consequence and no hard-rule breach | CHANGES_REQUESTED; a formal future ticket or rule breach is unnecessary. |
| Low-likelihood catastrophic data, security, or irreversible-state consequence | Material consequence is not erased by low likelihood; CHANGES_REQUESTED. |
| Comparable concern with an existing demonstrated safeguard that genuinely bounds its effect to a non-material defect | Eligible for V-02 deferral with required evidence passing; the safeguard changes the rationale. |
| Speculative redesign or preference without demonstrated material consequence | Observation; no new correction obligation. |

- Every confirmed finding states trigger, consequence, affected boundary,
  separate impact and likelihood/exposure, existing mitigation, and contextual
  fix-now/deferral rationale.
- In at least one passing-AC material-risk case, exposure appears only in
  ART-003; the decision still accounts for it and the decisive discovery probe.

Oracle / boundary:
- Compare acceptance guidance/report/eval expectations against the case table
  and admitted finding facts. Run fixture probes that distinguish the risky and
  genuinely mitigated behavior, including the refactoring consequence without
  a hard-rule breach. Source text alone proves only the contract.

Variants:
- Each table row; operating/business and maintenance contexts supplied by R-01.

### V-02 — Only evidenced bounded defects receive approved deferrals

Covers: AC-01, AC-02, R-01

Intent: Reject both endless optional-fix loops and acceptance that labels a
material or unproved concern as an approved known issue.

Given:
- All required evidence passes and no material blocker remains.
- Separate supplied concerns are a confirmed bounded non-material defect,
  preference/polish, and an unproved minor concern.
- The defect's context establishes bounded effects and compatible consumers.

When:
- Classify every concern under the acceptance contract.

Then:
- ACCEPT plus an approved known issue is permitted for the confirmed defect,
  with bounded effect, contextual rationale, follow-up, and reassessment conditions.
- Preferences, polish, and unproved minor concerns are observations; they do
  not become mandatory fixes or confirmed defects.
- Confirmed finding fields remain complete as specified in V-01. Deferral does
  not waive a required AC, proof obligation, or demonstrated material risk.

Oracle / boundary:
- Inspect acceptance disposition/report contracts and contrasting fixture
  expectations. Runnable probes establish the bounded defect and compatible
  consumer behavior; a preference label is not proof of non-materiality.

Variants:
- Confirmed bounded defect; preference/polish; unproved minor concern.

### V-03 — Uncertainty routes according to consequence and existing authority

Covers: AC-02, R-03

Intent: Reject routine permission prompts, fabricated context, and escalation
that skips an available authorized resolution.

Given:
- Supplied facts distinguish an ordinary unknown from uncertainty with credible
  serious consequences of delay or materially costly later repair.
- Required proof otherwise passes and there is no correction-eligible blocker.
- For consequential uncertainty, supplied permissions and authority distinguish
  a resolvable case from one that cannot be settled within existing authority.

When:
- Determine the disposition and next route using the available facts.

Then:
- Ordinary uncertainty continues with a stated reasonable assumption and an
  observation; it creates no routine question or blocking verdict by itself.
- Consequential uncertainty is resolved within existing authority first. If
  settled, use the established facts for the decision without a permission prompt.
- An unresolved decision-critical consequential question yields INCONCLUSIVE
  and one focused question identifying the consequence and needed fact.
- Assumptions remain distinguishable from evidence; no missing business,
  operating, or consumer fact is invented, and required proof is never waived.

Oracle / boundary:
- Compare guidance and fixture routes with supplied facts/permissions; verify
  the internal-resolution case supplies the fact needed to settle the question.
  Expected question/assumption fields prove contract coverage, not actual prompt
  behavior. Evidence-owner requests are distinguished in V-04.

Variants:
- Ordinary unknown; serious-delay and costly-later uncertainty, each resolvable
  within authority or not resolvable within authority.

### V-04 — Mixed conditions preserve verdict precedence and every route

Covers: AC-02, AC-03, R-02, R-03

Intent: Reject dropped unfinished rows, an INCONCLUSIVE verdict that hides an
authorized correction, or an evidence request treated as a production fix.

Given:
- Current admitted ledgers include stable IDs, findings, evidence, and concrete
  reasons for blocked/unchecked required rows.
- Fixture authority explicitly allows or prevents bounded correction; an
  unrunnable row is actually unavailable under the supplied setup/permissions.

When:
- Apply disposition and continuation contracts to each combination.

Then:

| Conditions | Verdict and route |
|---|---|
| Confirmed blocker; authorized bounded correction; another required row unrunnable | CHANGES_REQUESTED; retain the blocker and unfinished row; separate correction and evidence-owner routes. |
| Same blocker and unfinished row; bounded correction prevented | INCONCLUSIVE; retain both, identify the correction constraint and evidence owner. |
| Confirmed blocker; authorized bounded correction; unresolved material-context question | CHANGES_REQUESTED; retain the blocker/question and route correction and necessary authority separately. |
| Missing decisive required proof alone | INCONCLUSIVE; focused request to discovery/capability/evidence owner; no implied production fix or generic user approval. |
| No correction-eligible blocker; unresolved decision-critical uncertainty | INCONCLUSIVE; focused authority route as in V-03. |

- Every finding and unfinished row retains its ID, reason, evidence state, and
  next owner; the selected verdict cannot drop another obligation.
- Neither CHANGES_REQUESTED nor INCONCLUSIVE permits advancement. Ordinary
  uncertainty alone does not force either verdict.

Oracle / boundary:
- Compare expected verdicts and complete continuation rows against admitted
  ledgers, authority, and acceptance/report contracts. Local setup checks must
  establish why the required probe cannot run; an invented blocked label does
  not exercise mixed-condition precedence.

Variants:
- All table rows; authority/scope/permission/dependency constraints that prevent
  bounded correction; blocked and unchecked required rows remain unfinished.
  Also combine an authorized blocker, missing proof, and an unresolved material
  question: CHANGES_REQUESTED retains all three separate routes.

### V-05 — Deferral recording belongs to the coordinator before advancement

Covers: AC-04, R-04

Intent: Reject reviewer tracker writes, premature advancement, or an issue
record that loses the basis for later reassessment.

Given:
- A supplied acceptance decision approves a bounded deferral with stable task,
  review, and finding provenance; coordinator advancement authority is explicit.
- A contrasting supplied state has no approved deferral and no known-issues file.

When:
- Apply coordinator recording and advancement guidance to each supplied state.

Then:
- The coordinator alone records the approved deferral before authorized
  advancement, using `docs/known-issues.md` by default.
- The record carries stable ID; task/review/finding provenance;
  trigger/consequence/evidence; impact/likelihood; affected boundary/consumers;
  deferral rationale; follow-up owner/action; and reassessment conditions.
- Discovery and acceptance do not acquire tracker-writing authority.
- With no deferral, a known-issues file is not required. This task creates no
  real record without an acceptance-approved deferral and coordinator authority.

Oracle / boundary:
- Inspect recording guidance and supplied record/report fixtures for complete
  provenance/fields, writer ownership, and ordering before advancement. Local
  fixture files exercise record representation only; actual writer/order
  compliance belongs to later authorized role qualification.

Variants:
- Approved deferral; no deferral/file; default record path unless repo authority
  supplies another path.

### V-06 — Context links and portfolio priority do not manufacture mitigation

Covers: AC-05, AC-06, R-04

Intent: Reject planned-work promises as safeguards, missing links as proof of
no relationship, or a priority change as grounds to reopen acceptance.

Given:
- Supplied approved-deferral records have either no optional links or already
  known relevant context links.
- Contrasts distinguish proposed from committed work, a priority-only change,
  and a new material fact that invalidates an acceptance assumption.

When:
- Interpret context and determine whether focused review is required.

Then:
- Optional links identify subsystem; stable contracts/flows/plans; confirmed
  versus suspected relations and related issue IDs; safeguards/assumptions and reassessment triggers;
  and proposed versus committed relevant work.
- Missing links mean unknown relations, not absence. Links remain optional;
  no formal graph/schema, mandatory ontology, or complete dossier is required.
- Planned work alone, whether proposed or committed, is not existing mitigation.
- Priority change alone preserves acceptance; changed material facts can require
  focused review under existing authority.
- Acceptance gains no portfolio scheduling, backlog-write, or requirement-making
  authority; portfolio choices cannot excuse a current material blocker.

Oracle / boundary:
- Compare record and acceptance guidance with supplied contrasting context;
  identify exactly which fact changed versus a scheduling label. An expected
  deferral relying only on future work fails this contract check.

Variants:
- No links; supplied confirmed/suspected relations; proposed/committed work;
  priority-only change versus invalidated material assumption.

### V-07 — Relevant later consumers reassess supplied known issues

Covers: AC-04, AC-05, R-04

Intent: Reject hidden consumer workarounds and broad issue searches for unrelated
tasks while retaining a genuine changed-consumer incompatibility.

Given:
- A supplied coordinator-owned issue record includes provenance, safeguards,
  affected consumers, and reassessment conditions.
- Independent later-preflight inputs describe a relevant consumer with unchanged
  exposure, a changed required consumer/exposure, and an unrelated task.

When:
- Apply the relevant preflight consumption contract to each supplied input.

Then:
- Relevant preflight reassesses compatibility/exposure against the record and
  current consumer obligation, stating whether its assumptions still hold.
- Unchanged compatible exposure preserves the justified deferral; changed
  exposure or a consumer requirement is assessed using current facts and routes
  any demonstrated material incompatibility for focused resolution/review.
- No hidden workaround substitutes for compatibility. An unrelated issue causes
  no broad search or unrelated-task reassessment requirement.

Oracle / boundary:
- Inspect existing T-001 consumer guidance and any authorized minimal update,
  plus supplied consumer/record fixtures. Runnable consumer probes establish
  compatible versus incompatible behavior. No exact new preflight verdict is
  imposed where the brief only requires reassessment and an owned route.

Variants:
- Relevant unchanged exposure; changed exposure/required consumer; unrelated task.

### V-08 — Repeated review retains dispositions until current proof justifies change

Covers: AC-06, R-04

Intent: Reject optional-fix correction loops and suppression of a genuinely new
material blocker under a prior acceptance label.

Given:
- A supplied earlier decision contains an accepted disposition with known
  context/exposure and stable finding IDs.
- Independent current-review inputs distinguish unchanged exposure/optional
  improvements from the justified new-blocker reasons below.

When:
- Review the next legitimate occurrence against current proof and authority.

Then:
- Unchanged exposure preserves the accepted disposition; optional improvements
  create no new correction obligation and never restart correction.
- A new blocker has current proof, contextual materiality, and an explicit
  reason: regression, formerly blocked evidence, missed existing obligation,
  changed context/authority, or newly demonstrated material risk.
- A stale severity label or prior acceptance alone cannot supply or suppress
  the new blocker. Applicable findings and unfinished rows remain visible.
- No global correction-round limit is introduced; T-003's existing task-specific
  stop rules remain in force.

Oracle / boundary:
- Compare prior/current decision fixtures and source guidance; runnable probes
  establish the new failure/consequence for each supplied new-blocker case.
  Observe retained dispositions and stated reasons at the decision contract,
  without executing T-003's correction pipeline.

Variants:
- Unchanged exposure with optional fixes; each of the five named new-blocker
  reasons, with current evidence and materiality.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Ready design is not ready preflight or behavioral acceptance.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Preflight confirms .2 admission and T-001 consumer applicability, fixture
  capabilities/permissions, targeted selectors, and the source brief revision.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios. Concrete test structure, framework usage, helpers,
  and file placement remain implementation choices within the brief's scope.
- Start with focused fail-first checks for ACCEPT-on-green-tests, ordinary-unknown
  prompts, and dropped mixed rows. After the targeted pass, the brief names
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py`.
  Run a changed preflight fixture's local setup check only if that source changes.
- Inspect installer constants when implementing source/profile guidance changes;
  keep distribution synchronized within existing ownership. Do not refresh active
  `.agents/` copies or create real known issues during this task.
- Preserve runnable fixtures and identify structural, local runtime, and unrun
  role-behavior evidence separately. No live/model-budget or repository-wide
  gate is authorized here. A fresh reviewer checks a distinct contextual trace;
  T-002.4 and T-005 retain their composition/behavioral evidence ownership.
- If discovery shows a scenario cannot be exercised at its stated boundary,
  route the conflict to task design/preflight rather than weakening the oracle.
