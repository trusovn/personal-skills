# Task Brief: T-004 — Collect current evidence and repeat bounded correction

## Outcome

Give the coordinator current candidate, check and independent collection records
for one prepared task. A real failing task can be corrected, checked again and
collected again without reusing stale evidence or resetting the correction count.
T-005 consumes these records to decide separate acceptance and completion.

## Authority and scope

- Authority: [owner-confirmed direction](../../direction-single-task-sbx.md);
  [orchestration plan](../../local-harness-orchestration-plan.md), T-004,
  ART-003/005/006, IF-003, FLOW-001 steps 2–6, FLOW-002/003 and INV-001..008;
  [accepted plan review](../../project-plan-review-single-task-sbx-r2.md).
- Dependency: [T-003 acceptance-02](../T-003/reviews/acceptance-02.md) permits
  advancement. Consume its [successor contract](../T-003/controller-contract.md)
  and the [T-002 controller contract](../T-002/controller-contract.md).
- Allowed: controller, Git identity, verification runner, state, affected schemas,
  focused tests and directly affected references inside `skills/task-orchestrator/`;
  task-local handoff records. Keep one ledger and one actor-admission path.
- Excludes: semantic ART-009 admission, final acceptance/completion, known-issue
  recording, commits, dependency release, provisioning, parallel execution,
  automatic recovery, official-plan edits and active-install refresh.

The coordinator runs inside an owner-supplied sbx on a separate branch with
explicit YOLO authority. These are operating assumptions, not containment proof.
Collection assignments prohibit implementation edits; runtime-enforced reviewer
read-only access is not required. Keep implementation, collection and later
acceptance roles separate. Do not add a classifier, tracker migration or a new
repetition-stop rule from recommendations in
[correction/disposition notes](../../correction-and-disposition-options.md).

## Child outcomes and sequence

| Child | Owned output and consumer | Depends on | Brief |
|---|---|---|---|
| T-004.1 | Controller-produced candidate and check records, including an explicitly authorized sbx check path; consumed by collection | T-003 | [brief](../T-004.1/brief.md) |
| T-004.2 | Independent collection admission, correction-loop wiring and composed T-004 proof; consumed by T-005 | T-004.1 | [brief](../T-004.2/brief.md) |

Candidate/check production has a stable handoff: the collector consumes its
identity and check-runner interface. Splitting here reduces each review surface.
The second child owns integration, so no parent-only proof remains unassigned.
Shared controller/state edits occur sequentially after the producer is accepted.

## Coverage and closure

| Parent requirement | Owner |
|---|---|
| P-01: inspect actual scope and bind tracked/untracked bytes, baseline, configuration and task inputs to ART-003 | T-004.1 AC-01/02 |
| P-02: execute configured checks as ART-005, including sbx-compatible execution and truthful failure states | T-004.1 AC-03/04 |
| P-03: fresh independent collection reruns checks, inspects behavior/code and retains findings as ART-006 | T-004.2 AC-01/02 |
| P-04: real correction repeats inspection/checks/collection; drift makes prior evidence stale | T-004.2 AC-03/04 |
| P-05: cycle zero plus three shared corrections; replay/reload cannot reset or double-charge; fourth refused with intervention | T-004.2 AC-03/05 |
| P-06: separate acceptance remains unavailable until T-005; publish exact successor interfaces and proof limits | Both handoffs; T-004.2 AC-06 consolidates |

IF-003 candidate/check production and ART-003/005 belong to T-004.1. IF-003
collection semantics and ART-006 belong to T-004.2, extending T-003's
`observe_operation` → `_admit_actor_outcome` → `_publish_actor_outcome` path.
T-004.2 integrates the inherited IF-001/002 correction accounting and launch
guards. Neither child owns ART-009 semantics or IF-004 completion.
Preserve INV-001..008 within these slices; T-005 owns the final gate proof.

Expected contract impact: extend the current
[`task-orchestrator` registry record](../../../../../docs/contracts/task-orchestrator.json),
resolved through [the index](../../../../../docs/contracts/index.json), from raw
implementation/collection claims to current candidate/check/collection evidence.
Each child's registry-updater stage registers only implemented capability.
Do not register future acceptance or completion as delivered.

## Execution and handoff

Status: `decomposed`
Task kind: `composite`
Brief revision: 1

This parent is not an implementation target. Start with T-004.1 verification
design, then standalone guided preflight. Each leaf needs its own derived
`verification.md`, ready `preflight.md`, implementation and required review route.
No readiness or implementation result is supplied by this planning package.
Close T-004 only after both leaves, including T-004.2 integration, finish their
required independent reviews. T-005 consumes `controller-contract.md` in this
directory and the accepted leaf results. T-006 retains the real sbx/model pilot.

### Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Original estimate: 50 implementation agent calls; 125 minutes;
medium confidence; intended profile `strong/medium`. Calls greater than 15 and
duration greater than 40 trigger decomposition. Both smaller leaves retain
explicit permitted overrides for their cohesive lifecycle boundaries. Review,
preflight and registry synchronization are excluded from these estimates.
