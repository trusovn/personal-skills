# Task Brief: T-002.1 — Freeze the approved one-task policy

## Outcome

Freeze the human-reviewed brief, verification requirements and approved run
policy as one identifiable input revision. Give T-002.2 a validated stage and
role contract that cannot omit preflight, collection or separate acceptance.

## Direction trace

- Direction contribution: protect the task authority used by the one-task sbx loop.
- User-observable effect: new runs expose their approved inputs and policy;
  incompatible old runs return a clear refusal and next action.
- Why now: T-002.2 needs frozen authority before it can reserve work.
- Decisions used: [direction](../../direction-single-task-sbx.md), “What remains
  unchanged”; [plan](../../local-harness-orchestration-plan.md), “T-002 preparation
  and policy ownership”; [parent owner decision](../T-002/brief.md#direction-trace-and-owner-decision).
- New direction decisions required: None.

Status: `ready`
Task kind: `executable`
Brief revision: 1
Profile: `guided`; designed, with readiness still pending.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 14 tool calls / 35 minutes / 60k context
```

## Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Estimate: 14 agent calls, 35 implementation minutes, medium
confidence. Intended profile: `standard/medium`. Policy result: `fits`;
triggered limits: none; decomposition override: none. Estimate excludes
preflight and independent review.

## Authority and scope

- Authority: [parent](../T-002/brief.md), P-01/P-05/P-06; approved
  [plan](../../local-harness-orchestration-plan.md) and
  [review](../../project-plan-review-single-task-sbx-r2.md).
- Consumes: ART-001 owner inputs and historical ART-008. Produces: frozen
  ART-001 and the stage/role representation consumed by T-002.2.
- Stable refs: CAP-001/003, FLOW-001/003, IF-001, INV-001/008.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Allowed implementation changes: `skills/task-orchestrator/scripts/controller_state.py`,
  `scripts/controller.py`, affected `assets/` schemas/examples, their existing
  focused tests, and this package's implementation report/contract note.
  Paths after the first are relative to `skills/task-orchestrator/`.
- Reuse: flow/cursor validation, immutable policy storage, run initialization,
  ledger and schema fixtures. Inspect existing coverage before changing cases.
- Excludes: reservation behavior (T-002.2), input revision (T-002.3), changes
  to `codex_worker.py` launch behavior, evidence admission, actual sbx checks,
  official plan/review edits and installation changes.
- Dependencies: T-001 historical transport evidence reconciled by the parent;
  its obsolete isolation gates do not block this leaf. No new owner decision.

## Work and acceptance criteria

- **AC-01 — Frozen authority:** initialization freezes identifiable brief and
  verification content, scope/check requirements and policy. Reading a run
  after source-input edits cannot silently adopt those edits. Existing frozen
  records remain preserved. New runs authorize exactly one prepared task.
- **AC-02 — Required sequence:** validated representation covers ready,
  preflight, implementation, checks, independent collection, separate acceptance,
  completion gate and completed, plus bounded correction. Collection and
  acceptance have different actor roles; the completion gate is controller-owned.
  A weak/optional profile, invalid ordering or actor result cannot omit or
  replace a required stage or grant completion. Exact names/layout are delegated.
- **AC-03 — Approved policy:** synchronize runtime constants, validation,
  schemas and current examples for `gpt-6.1-sol` low/medium/high, a shared
  three-correction limit including environment repair, explicit sbx/YOLO
  authorization, and active-chat intervention. Unknown context occupancy
  requires a fresh correction session; reuse is allowed only under the existing
  reliable-occupancy rule and 0.5 threshold, never terminal token totals.
  Represent policy here; T-003 applies it at launch.
- **AC-04 — Compatibility and handoff:** incompatible frozen old runs are
  refused before continuation/mutation, with a next action to initialize a new
  run using reviewed current inputs. Do not migrate old bytes or refresh an
  installation. Publish exact implemented policy/input/stage contracts in
  `controller-contract.md` in this package, including the compatibility rule,
  missing runtime stages and commands actually supported.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R1: required authority cannot weaken | Omit preflight, checks, collection or acceptance; merge collection/acceptance roles; reorder required stages; request multiple active tasks | Runtime validation and persisted initialization reject each invalid input without adopting it | Focused cases reject old permissive behavior; owning state suite | Try a weaker profile through controller initialization | Implementer targeted/owning; fresh discovery corroborates |
| R2: policy and input identity remain frozen | low/medium/high mapping; known reusable/over-threshold/unknown occupancy; terminal totals only; brief/verification edits; incompatible old run | Loaded authority remains exact; unsupported continuation is refused without rewriting run records | Real temporary input/run files plus policy tests | Reopen a frozen run after editing source inputs; inspect refusal/non-adoption | Implementer targeted/owning; fresh discovery corroborates |

## Expected contract impact

Materialize ART-001 and required stage/role declarations used by IF-001;
preserve ART-008 limitations. There is no current contract registry under
`docs/contracts` or `skills/task-orchestrator/docs/contracts` at preparation.
Publish the package contract note; do not invent a registry. T-002.2 consumes
these implemented declarations instead of defining another validator.

## Verification and readiness

Verification reasoning: **separate** — frozen input identity, old-run compatibility
and mandatory roles admit plausible false passes. Use [verification.md](verification.md)
revision 1. Readiness route: **standalone guided preflight** — confirm current
authority, dependencies, ownership and focused fixture reuse before implementation.
No `preflight.md` has been issued by planning.

Start with the owning method selected by the implementer, then run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
```

Implementer owns these targeted/owning checks, including after corrections.
Fresh discovery owns the broader aggregate decision; use the full local
orchestrator suite if blast radius requires it. JSON/schema checks prove
structure only. No live model/network or sbx pilot is authorized here.

## Stops and handoff

Stop for conflicting authority, owner-work overlap, permission expansion or
scope growth. Preserve old runs and active installations. The installer excludes
task-orchestrator; this leaf adds no profile/shared dependency.

Next: ready standalone preflight, then implementation. Immediately after
implementation/correction and any applicable required architecture,
maintainability or registry stage, obtain fresh independent
`task-review-discovery` evidence and a separate `task-acceptance-review` decision.
Self-review cannot replace either. Hand the implemented contract and review
references to T-002.2 only after acceptance.
