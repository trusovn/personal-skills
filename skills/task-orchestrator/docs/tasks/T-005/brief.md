# Task Brief: T-005 — Admit separate acceptance and complete one task

## Outcome

The coordinator can obtain a separate acceptance decision, route correction or
missing evidence, record approved bounded deferrals, and complete the exact
eligible candidate once. T-006 can use this assembled local loop for coordinator
instructions and the separately authorized real sbx proof. Completion here proves
local controller behavior; it does not qualify live model execution.

## Child outcomes and sequence

| Child | Owned output and consumer | Depends on | Brief |
|---|---|---|---|
| T-005.1 | Admitted separate decision, finding dispositions and recovery routes; consumed by the completion gate | T-004 | [brief](../T-005.1/brief.md) |
| T-005.2 | Validated deferral recording, completion publication and composed loop proof; consumed by T-006 | T-005.1 | [brief](../T-005.2/brief.md) |

An admitted decision is a stable boundary: it can authorize correction or make
a candidate eligible without completing it. The second child consumes that
contract and owns integration. Shared controller/state edits are sequential;
neither child needs a provisional completion implementation to prove its result.

## Authority and scope

- Authority: [plan](../../local-harness-orchestration-plan.md), T-005,
  ART-002/007/009/010, IF-003/004, FLOW-001 steps 5–7, FLOW-002/003 and
  INV-001..008; [task map](../../local-harness-task-map.json), T-005;
  [owner-confirmed direction](../../direction-single-task-sbx.md);
  [accepted plan review](../../project-plan-review-single-task-sbx-r2.md).
- Reviewed baseline: plan SHA-256
  `9e32bc96f8dad2776e94b995aaf2831ef8c788b120ebf8a218a95354a4a811e2`;
  map `a669e740ee1fcb4a71b9b705d60f2b710e7619bd93ac46023f34534aed7b9082`.
- Dependency: [T-004 closure](../T-004/result.md), accepted
  [T-004.1](../T-004.1/reviews/acceptance-02.md) and
  [T-004.2](../T-004.2/reviews/acceptance-01.md), and the consolidated
  [controller contract](../T-004/controller-contract.md).
- Allowed: controller/state, affected schemas, focused tests/fixtures, actor
  assignments and directly affected instructions/references under
  `skills/task-orchestrator/`; child-owned successor handoffs.
- Excludes: automatic commit, dependency release, parallel coordination,
  provisioning, automatic recovery, new model or correction policies, classifier,
  tracker migration, official-plan edits and active-install refresh.

Preserve human-reviewed inputs, required preflight/collection/acceptance,
`gpt-6.1-sol` low/medium/high, fresh correction when occupancy is unknown,
cycle zero plus three shared corrections, and active-chat intervention only
when blocked. Owner-supplied sbx/YOLO/separate-branch conditions are operating
assumptions, not protection guarantees. Reviewer assignments prohibit edits;
runtime-enforced isolation is outside this delivery.

The approved recording authority in [disposition notes](../../correction-and-disposition-options.md#existing-skill-and-approved-source-update)
and the current installed acceptance skill permits an authorized AI coordinator
to record acceptance-approved bounded deferrals. JSON migration and another
repetition-stop rule remain proposals. Required checks or material unresolved
risk cannot be waived as a known issue.

### Expected contract impact

Consume the current [registry](../../../../../docs/contracts/task-orchestrator.json):
reserved actor lifecycle, candidate/check production, independent collection,
finding history, correction accounting and intervention persistence exist.
T-005.1 materializes ART-009 and the IF-003 acceptance slice; T-005.2 materializes
ART-010 recording validation and IF-004/ART-007 completion. Both extend ART-002
status and preserve IF-001/002 and INV-001..008. Use the existing
`observe_operation` → `_admit_actor_outcome` → `_publish_actor_outcome` path
and one ledger. Registry synchronization records implemented deltas after each
child, not this expected future capability.

## Coverage and closure

| Parent requirement | Owner |
|---|---|
| P-01: fresh separate ART-009 with current required evidence and observed provenance | T-005.1 AC-01/02 |
| P-02: contextual dispositions; correction, missing-evidence and blocker routing | T-005.1 AC-03/04 |
| P-03: review-driven real correction and shared-budget/replay/exhaustion proof | T-005.1 AC-04/05 |
| P-04: coordinator-only approved deferrals, stable provenance/history and bounded tracker exception | T-005.2 AC-01/02 |
| P-05: current required evidence, scope and terminality gate; exactly-once completion without commit/release | T-005.2 AC-03/04 |
| P-06: unseeded composed loop and truthful T-006 interface/qualification handoff | T-005.2 AC-05/06; consumes T-005.1 AC-06 |

T-005.1 owns decision/disposition records and their routing. T-005.2 owns
recording receipts, the final gate and completion records. The latter proves
their composition; no parent-only verification or implementation stage remains.
Both leaves have explicit permitted sizing overrides for their coupled lifecycle
work. Detailed finite scenarios belong in each leaf's verification document.

## Execution and handoff

Status: `decomposed`
Task kind: `composite`
Brief revision: 1

This parent is not executable. Next: derive T-005.1 `verification.md`, then a ready
standalone guided `preflight.md`. Each leaf requires its own preparation,
implementation and independent review route. Close T-005 after both accepted
leaves, including T-005.2 integration. Hand the consolidated
`controller-contract.md` in this directory and accepted child results to T-006.
No implementation readiness, acceptance or live execution is claimed here.

### Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Original estimate: 44 implementation agent calls; 110 minutes;
medium confidence; intended profile `strong/medium`. Calls greater than 15 and
duration greater than 40 trigger boundary evaluation. The decision/completion
split gives independently consumable outputs and smaller review surfaces; it
adds modest integration cost. Estimates exclude separate preparation, reviews,
registry synchronization and coordinator work.
