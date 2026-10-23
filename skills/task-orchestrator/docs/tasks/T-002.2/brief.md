# Task Brief: T-002.2 — Reserve one operation and retain its correction count

## Outcome

Let the coordinator read current status and reserve only permitted work against
an expected state version. Keep one active operation and charge each authorized
correction once, including environment repair. T-003 will use these assignments
to launch actors.

## Direction trace

- Direction contribution: bound ordinary corrections and stop duplicate or
  uncertain work in the approved one-task loop.
- User-observable effect: status exposes the operation, correction count and
  precise permitted next actions across controller restarts.
- Why now: T-002.3 needs operation guards for safe revision; T-003 needs assignments.
- Decisions used: [plan](../../local-harness-orchestration-plan.md), IF-001 and
  operation/correction lifecycle; [parent owner decision](../T-002/brief.md#direction-trace-and-owner-decision)
  charges environment repair to the same budget.
- New direction decisions required: None.

Status: `ready`
Task kind: `executable`
Brief revision: 1
Profile: `guided`; dependency completion and readiness still pending.

```yaml
agent_tier: strong
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / 60k context
```

## Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Estimate: 15 agent calls, 40 implementation minutes, medium
confidence. Intended profile: `strong/medium`. Policy result: `fits`;
triggered limits: none; decomposition override: none. Reuse existing run lock,
ledger, validation and process-contention fixtures; estimate excludes independent review.

## Authority and scope

- Authority: [parent](../T-002/brief.md), P-02/P-03/P-05/P-06;
  [plan](../../local-harness-orchestration-plan.md), IF-001, ART-002/004,
  INV-001/002/005/008, FLOW-001/003. Status also supports INV-007.
- Dependency: accepted T-002.1 and its `controller-contract.md`; absent implemented
  contract blocks preflight, not task design.
- Consumes: frozen ART-001 and T-002.1 stage/role representation. Produces:
  ART-002 status/reservations and controller assignment half of ART-004.
- Allowed changes: controller/state scripts, affected schemas, owning
  `test_controller_state.py`/`test_controller.py` and reused fixtures under
  `skills/task-orchestrator/`, plus this package's reports/contract note.
- Excludes: adapter launches, observed terminal/preflight admission (T-003),
  semantic check/collection/acceptance routing (T-004/005), input revision
  (T-002.3), completion publication, installation changes and plan edits.

## Work and acceptance criteria

- **AC-01 — Truthful status:** expose run/task/input/flow identity, stage, state
  version, attempts/correction count, candidate/evidence references, required
  evidence, outstanding findings, operation state, next action and blocker as
  available. Distinguish passed, failed, stale, blocked, missing/not-run and
  policy omission; required stages cannot be represented as optional omissions.
  Reading status cannot advance the task.
- **AC-02 — Atomic reservation:** validate expected version, task/role/stage,
  current authority and prerequisites before atomically reserving one operation
  and publishing its assignment. Bind run/task/role/operation/input identity,
  frozen policy and candidate identity where applicable. A duplicate/replayed
  request cannot allocate another operation or charge again. Stale versions and
  conflicting requests return structured reasons and permitted actions.
- **AC-03 — One operation and no bypass:** reserved, running and unknown
  operations prevent another actor reservation and completion. Preserve their
  identity/history across reload. No missing receipt implies terminality.
  Implementation requires current admitted preflight readiness, bound to the
  terminal preflight operation/current inputs. New commands and applicable
  existing `run-next`, `inspect` and `revise-flow` paths cannot bypass guards or
  complete a new-policy run through legacy behavior. Unconnected actions report
  unavailable/pending successor work. T-003 owns real readiness admission.
- **AC-04 — Shared budget:** initial implementation is cycle zero. Each newly
  authorized correction reservation charges exactly one of three cycles,
  including a repair actor that can change files/environment. Reservations are
  the accounting boundary; launch retry with the same key cannot charge again.
  Preflight/retry and evidence-only collection/check/acceptance retries charge
  none and cannot authorize repairs. Restart, replay and route changes cannot
  reset the count. A repair before initial implementation also charges the
  shared count; starting cycle-zero implementation cannot reset earlier repair
  charges. Refuse a fourth correction unchanged and expose intervention
  as the required next action. Record that environment repair requires preflight
  again; T-003/004 apply runtime admission/routing. Do not implement a separate
  repair budget or automatic refund for an uncertain launch.
- **AC-05 — Refusal and contract:** invalid requests preserve authoritative
  state/version, policy, count and task files. Diagnostics may be separate.
  Publish exact status/reserve requests, results, refusal/replay behavior,
  record fields and successor admission seams in this package's
  `controller-contract.md`; do not expose a generic state-setting bypass.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R1: one active operation | First reserve; repeated key; competing key/version; reserved/running/unknown/terminal fixture; controller reload | Public operations and real persisted records permit one reservation only; unknown stays stopped | Reuse real lock/contention setup; no actor launch | Submit conflicting reservation from a second controller process | Implementer targeted/owning; fresh discovery corroborates |
| R2: shared budget persists | Cycle zero; corrections 1/2/3; fourth; check/review correction and repair reason; repair before initial implementation; replay/restart; free preflight/evidence retries | Count increments once per new authorized correction reservation; fourth leaves records/files unchanged | Real record reload between requests; focused fail-first case | Mix repair and review reasons, reopen controller before fourth request | Implementer targeted/owning; fresh discovery corroborates |
| R3: role/stage/authority cannot bypass | Stale version; wrong task/role/stage; absent/stale readiness; weak profile; legacy entry points | Structured refusal and unchanged authoritative bytes/task files | Owning public-controller cases using T-002.1 policy | Try legacy path and implementation without current readiness | Implementer targeted/owning; fresh discovery corroborates |

## Expected contract impact

Materialize IF-001 status/reserve and ART-002/004 assignment semantics in the
existing ledger/controller. Preserve T-002.1 authority. T-003 extends the single
admission path with observed outcomes; T-004/005 supply semantic prerequisites
for later stages. Missing successor evidence remains missing. No current
contract registry exists; publish the package contract note without creating one.

## Verification and readiness

Verification reasoning: **separate** — replay, persisted count and ownership
require lifecycle evidence. Use [verification.md](verification.md) revision 1.
Readiness route: **standalone guided preflight** after T-002.1 acceptance;
confirm actual predecessor interfaces and existing fixture reuse. No readiness
claim is made by this brief.

Implementer runs the selected focused method first, then the state and controller
modules using the commands in [T-002.1](../T-002.1/brief.md#verification-and-readiness).
These targeted/owning gates also belong to correction implementation. Fresh
discovery owns the broader aggregate decision. Explicit test setup may supply
terminal/readiness/evidence states whose production admission belongs to later
tasks; it cannot replace reservation logic or create a public fixture injector.
No live runtime, network or model launch is part of this proof.

## Stops and handoff

Stop for changed authority, material predecessor-contract mismatch, unsafe
permissions, owner-work overlap or scope growth. Do not add orchestration to
shared installer dependencies or refresh installed skills.

Next: predecessor acceptance, ready standalone preflight, implementation, then
applicable required architecture/maintainability/registry stages, fresh independent
`task-review-discovery` and a separate `task-acceptance-review` decision immediately
after implementation/correction. No self-review substitution. T-002.3 consumes
the accepted persisted status/reservation contract.
