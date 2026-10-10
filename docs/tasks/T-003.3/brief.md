# Task Brief: `T-003.3` — Preserve correction obligations and current evidence

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 15 tool calls / 40 minutes / 50k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 15. Duration: 40 minutes. Confidence: medium.
- Intended profile: `standard / high`. Policy result: fits; triggered limits:
  none; decomposition override: none. Implementation work only. Existing
  T-001/T-002 recovery/rubric coverage is preserved rather than reimplemented.

## Readiness route

standalone guided preflight — confirm .1's route fields and existing revision,
mixed-condition and correction fixtures. Derive verification, then ready preflight.

## Verification-design recommendation

separate — scenario revision, stale readiness, actual-effect reference routing,
mixed findings and aggregate ownership require distinct state transitions.
Existing implementer/discovery/acceptance fixture setups are believed available;
task-owned extensions suffice without a new enforcement mechanism.

## Outcome and direction trace

Correction handoffs retain every finding and coverage obligation with current
evidence, separate owners and fresh applicable review under unchanged authority.

- Contribution: `CAP-002`, `FLOW-002/003`; `ART-004/005/006/007/009`;
  `IF-002/003/004/005/006`; `INV-003/004/005/006/008/011`.
- Effect: the caller can continue authorized correction/evidence work without
  losing unfinished rows, reusing stale verdicts or restarting optional fixes.
  Enables .4 and T-005's revision/correction composition proof.
- Why now: extends .1's submission protocol using T-001 preparation and T-002
  current discovery/decision contracts.
- Decisions: plan sections 1, 5–8, 10 T-003 and 11; parent P-03–07.
- New direction decisions required: None.

## Authority and scope

- Authority: [plan](../../project-plan.md), cited sections;
  `T-003` [task-map entry](../../task-map.json); [parent](../T-003/brief.md).
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Depends on completed/reviewed .1. Consumes `ART-001/002/003/004/005/006/007/009`;
  produces correction ART-004, current ART-005/006/007 handoff obligations and ART-009.
- Allowed: source implementer correction guidance/evals/setup; minimal stale
  correction sections in discovery/acceptance skill/report templates, registry
  updater skill and flow README. Task-owned focused extensions to existing
  implementer/discovery/acceptance fixture cases and their owning tests:
  `test_bounded_task_implementer.py`, `test_task_review_discovery.py`,
  `test_task_acceptance_review.py`, `test_task_preflight.py` under `tests/`.
  Change preflight guidance only if an approved revision obligation is absent.
  Inspect installer selection/guide/helpers; no new skill/helper expected.
- Read-only: .1 protocol, T-001/T-002 authority/history, .2 maintainability scope,
  active `.agents/` copies. Preserve adequate rubric/recovery wording by reference.
- Excluded: new requirements, business policy, rubric redesign, task registry
  foundation, controller state, counters, auto-launches and agent-budget checks.

## Work and acceptance criteria

1. Carry the full continuation through .1's route fields, including reasons,
   current row evidence, correction owner and influenced sibling surfaces.
2. Close gaps in existing correction/revision/reference guidance and supplied
   fixtures. Keep each producer's evidence distinct from acceptance disposition.

- **AC-01:** Every finding/scenario ID and unfinished pass/fail/blocked/unchecked
  row survives correction, with prior status, current implementation evidence,
  incomplete reason and next owner. Include authority/preflight/context references,
  scoped diff, invariant, attempts, sibling surfaces, exact probes and gate record.
  Prior pass or verdict cannot certify changed bytes; neither non-success verdict
  permits advancement. Preserve separate correction/evidence/authority routes in
  mixed conditions and T-002's CHANGES_REQUESTED/INCONCLUSIVE precedence.
- **AC-02:** Distinguish clarification, evidence request, production, tests,
  reference, scenario and authority changes. Production corrections repeat
  applicable conditional stages, fresh discovery and separate acceptance. A
  tests-only exception needs policy authority. Reference-only updater → fresh
  acceptance is allowed only when actual effects and current behavioral proof
  support it; executable/behavioral effects repeat affected discovery/gates.
- **AC-03:** Under unchanged requirements, a coverage gap returns to verification
  design for a reasoned revision retaining existing IDs, supersedes affected
  readiness, needs focused ready preflight, then current revised-scenario evidence
  and a new decision. Changed requirements return to task design. Ordinary
  corrections/clarifications do not restart design; expected edits/reports alone
  do not invalidate readiness.
- **AC-04:** Discovery retains the justified aggregate gate after correction:
  reconcile authority/ledger first; safely runnable material rows and selected
  probes get current targeted evidence; blocked/unchecked rows retain concrete
  non-gate reasons. A decisive failure suppresses aggregate execution absent an
  authorized distinct diagnostic purpose. Clean targeted evidence permits one
  justified gate for that review; acceptance consumes without duplication. A
  later omitted material row requires targeted recovery before any justified
  rerun. Conditional gate owners retain IF-003 duties.
- **AC-05:** Preserve accepted dispositions unless exposure/context changes.
  New blockers need current evidence, contextual materiality and a reason:
  regression, formerly blocked evidence, missed obligation, changed context/
  authority or newly demonstrated material risk. Optional fixes do not restart
  correction. Continue through ordinary uncertainty within authority; preserve
  exceptional serious-delay/costly-later escalation. Keep two materially different
  failed fixes of one target and task/user budgets; add no global round limit.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-004/005/008 | First failure → authorized correction → next submission → fresh discovery/decision; mixed blocker plus unfinished proof, correction allowed/forbidden; stopped continuation | Stable IDs/reasons/owners and current scoped evidence remain at each handoff; no inferred clean state or advancement | Extend record-correction/mixed fixtures; reject missing row, stale evidence and collapsed next-owner routes | Trace an unfinished sibling row after a targeted fix passes | .3 implementer: targeted local checks; .4: composed inputs; T-005: actual stage outputs |
| R-02 / INV-003/005 | Coverage gap under unchanged authority → revised scenarios → obsolete readiness rejected → focused ready → new evidence; changed requirements; expected report effect | Original IDs remain; only applicable revised readiness admits next implementation; authority change returns to owner | Reuse existing revision/continuation fixtures with explicit before/after artifacts | Substitute old ready revision while keeping new scenario evidence | Preflight: readiness; discovery: current proof; acceptance: decision |
| R-03 / INV-008 | Clarification/evidence only; production; tests-only with/without authorized exception; genuine reference-only versus disguised executable/behavioral change | Route reflects actual changed effects and current proof, not filename/category label | Supplied diffs/policy/conditional evidence with exact expected first owner/full remainder | Reference change alters an executable contract; ensure narrow shortcut is rejected | .3 implementer: local contrasts; .4: integration; fresh stage owners: corroboration |
| R-04 / INV-005/006/011 | Stable disposition; optional improvement; material regression/new obligation; targeted failure/clean correction/later omitted row; two failed fixes of one target | No optional-fix restart or suppressed material blocker; current aggregate record with owner/reason; no duplicate decision gate | Reuse T-002 stable/regression and late-omission fixtures; retain scheduler two-fix stop case | Audit correction with green first probe but unfinished material sibling coverage | Correction implementer: regressions/owning suite; discovery: justified workflow aggregate; acceptance: consume only |

## Verification

- Fail-first changed cases, then the relevant owning module only. From root:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <owning-module>.py`
  using the allowed current modules above; derived verification/preflight freezes
  exact selectors and setup before implementation. Run gates sequentially.
- Supply real fixture authority, starting/changed bytes, revision artifacts,
  executable probes and incomplete-capability state. Report contract assertions,
  observed fixture behavior and unrun agent compliance separately.
- Do not duplicate inherited rubric scenarios or run every owner unless changed.
  .4 owns the composed local union; T-005 owns real role calls. No whole-repo gate.

## Expected contract impact

- Change ART-004 / IF-002/006 continuation; close ART-005/006/007 consumers under
  IF-003/004/005; preserve readiness authority and contextual decision ownership.
- Dependencies: .1 route protocol, T-001 revision/readiness, T-002 rubric/ledgers;
  no current `docs/contracts` registry and no registry foundation work.
- Delta: complete correction/recovery evidence and actual-effect routing, not
  machine enforcement or new verdicts. .4 consumes revised fixture states.

## Stops and handoff

Stop for changed requirements, contradictory stage authority, unsafe permissions,
user-work overlap, scope expansion or decisive capability requiring infrastructure.
Budget is soft. Next: derived verification → ready preflight → bounded implementation.
Required follow-on: immediately after implementation or correction, hand completed
bytes to a fresh independent acceptance reviewer through .1's applicable ordered
conditional stages, fresh discovery and separate acceptance; end the invocation.
Supply .4 with stable IDs, revision artifacts, current probes and unfinished routes.
