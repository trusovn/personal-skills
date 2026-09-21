---
name: project-delivery-plan
description: Use after the project foundation is ready and before detailed task planning/implementation when a small-to-medium project needs a coherent delivery plan without full SDD. Produce an end-to-end system plan plus a machine-readable task map that makes data/process/state flows, system interfaces, artifacts, invariants, producer/consumer relationships, and task placement explicit. Use this whenever multiple implementation tasks must compose into one working product, especially when downstream agents need to know what each task consumes and produces. Do not use this skill to implement features or to over-specify task-internal design that a strong reasoning agent can determine locally.
---

# Project Delivery Plan

Create the smallest planning package that is detailed enough for independent implementation tasks to compose into one coherent system.

This is deliberately lighter than full SDD. It resolves **system-level ambiguity** and preserves cross-task semantics, while leaving task-local implementation choices to the task planner and implementation agent.

## Core stance

- Plan the product as **data + process + state moving through explicit boundaries**, not as a feature list.
- Every important runtime artifact/state must have an owner, producer, consumer, and source-of-truth rule.
- Every important interface must have an observable contract at the level needed for independent work to compose.
- Every implementation task must have a clear place in one or more end-to-end flows.
- Preserve important behavioral nuances as invariants and transition rules rather than prescribing code structure.
- Prefer strong-agent latitude: specify **what must be true across boundaries**, not how local code must be written.
- Do not manufacture ceremony. A small project should still have a compact plan.

## Position in the workflow

Typical route:

```text
project-direction / approved concept
    -> project-bootstrap
    -> ai-flow-foundation          when AI participates in the flow
    -> repo-foundation
    -> foundation-readiness-review
    -> project-delivery-plan       THIS SKILL
    -> project-plan-verification   fresh independent agent
    -> task planning / task-brief-designer
    -> bounded implementation flow
```

If foundation readiness recommends full SDD because the project genuinely needs it, do not silently replace that with this lightweight path. State the mismatch and stop unless the project owner explicitly authorizes the lighter route.

## Inputs

Required where present in the repository:

- current repository/scaffold
- `docs/project-charter.md` or equivalent project authority
- foundation/readiness artifacts produced by the project's bootstrap flow

Read when applicable:

- `docs/ai-foundation.md`
- `docs/foundation-plan.md`
- repository-local architecture/maintainability rules
- approved product proposal or project-direction artifact
- relevant existing API/domain/schema documentation

If file names differ, locate the authoritative equivalents rather than inventing duplicates.

## Required outputs

Create or update exactly these planning artifacts unless repository authority names different canonical paths:

1. `docs/project-plan.md` — human-readable system plan.
2. `docs/task-map.json` — machine-readable map tying tasks to flows, artifacts, interfaces, invariants, and dependencies.

Use the bundled templates/contracts:

- `references/project-plan-template.md`
- `references/task-map-contract.md`

Validate `docs/task-map.json` with:

```bash
python3 <this-skill>/scripts/validate_task_map.py docs/task-map.json
```

The JSON validator proves structural/reference consistency only. Full plan validation `project-plan-verification`
 is to be invoked separately by the user - instruct the user to do so, on completion.

## Planning depth rule

A plan is deep enough when a strong reasoning agent can take any task entry and answer, without guessing:

- what outcome this task contributes to;
- where it enters the overall runtime/user flow;
- what authoritative artifacts/state it consumes;
- what artifacts/state/interfaces it produces, changes, or exposes;
- what upstream work must already exist;
- what downstream work depends on it;
- what cross-task invariants and lifecycle/state rules it must preserve;
- what observable boundary proves the task fits the larger system.

A plan is **too shallow** when downstream work must rediscover cross-task semantics.

A plan is **too detailed** when it prescribes local classes, helper methods, file-by-file edits, algorithms, UI component trees, or implementation sequences that do not define a cross-task contract.

## Protocol

### 1. Establish planning authority and scope

Read the project authority first. Record:

- product outcome;
- primary users/actors;
- approved capabilities;
- explicit non-goals;
- repository/foundation constraints;
- settled decisions that downstream agents must not reopen.

Do not expand scope merely because an adjacent capability would be useful.

If the approved concept conflicts materially with the foundation or repository authority, surface the conflict instead of normalizing it away.

### 2. Identify the system's authoritative artifacts and state

Build an artifact catalog before task decomposition.

An **artifact** is any piece of information/state whose lifecycle matters across steps or tasks, for example:

- persisted domain entities and versions;
- API request/response carriers when they are cross-boundary contracts;
- generated analysis/findings;
- approval decisions;
- uploaded/imported source material;
- cached or derived state when staleness/invalidation matters;
- audit/event records;
- configuration that changes product behavior.

For each important artifact record:

- stable ID;
- name and kind;
- authoritative owner/source of truth;
- who/what creates it;
- who/what reads or consumes it;
- who/what may mutate it;
- lifecycle states if any;
- invalidation/supersession semantics where relevant;
- persistence/durability expectation.

Do not model ephemeral local variables or incidental DTOs unless they define a system boundary.

### 3. Define important state machines and lifecycle invariants

For stateful artifacts/processes, describe only externally meaningful states and transitions.

Capture:

- valid transitions;
- forbidden transitions;
- transition authority/actor;
- atomicity requirements that cross a boundary;
- failure/retry outcome;
- cancellation/reversal semantics where relevant;
- stale/superseded semantics where relevant.

Assign stable invariant IDs such as `INV-001`.

Good invariant:

> `INV-003` A finding remains bound to the exact immutable document versions used by its analysis run; later document versions never rewrite historical provenance.

Too implementation-specific:

> Put `documentVersionId` in `FindingEntity` and use a JPA `@ManyToOne(fetch = LAZY)` relationship.

### 4. Define system interfaces

Create an interface map for every boundary that independent tasks may meet at.

Typical boundaries include:

- user/UI -> backend API;
- backend module/service -> another owning subsystem;
- backend -> persistence;
- application -> AI/provider seam;
- deterministic validation -> side-effect boundary;
- background process -> persisted state;
- import/export boundary.

For each important interface record:

- stable ID (`IF-001` etc.);
- producer/owner and consumer;
- purpose;
- input artifacts/state;
- output artifacts/state;
- important success semantics;
- important error/rejection semantics;
- authorization/idempotency/concurrency requirements when material;
- whether the exact wire/schema contract is fixed now or delegated to the owning task.

Do **not** invent a formal OpenAPI/schema artifact unless the project needs it. The plan may state behaviorally meaningful fields and leave exact local DTO design to task planning.

### 5. Reconstruct end-to-end data/process/state flows

For every critical user/system journey, write an explicit flow from trigger to terminal observable outcome.

Each step must identify, where applicable:

- actor/system owner;
- action/process;
- artifacts consumed/read;
- artifacts produced/written;
- interface crossed;
- state transition;
- invariant(s) that apply;
- rejection/failure path if it changes downstream semantics.

Use stable flow IDs such as `FLOW-001`.

A flow should look conceptually like:

```text
trigger
 -> validate/read authoritative state
 -> cross interface
 -> transform/process
 -> persist or transition state
 -> expose result
 -> terminal observable outcome
```

For AI-bearing flows, explicitly connect the project-level flow to the seams established by `docs/ai-foundation.md`: deterministic preprocessing, provider boundary, parsing/validation, policy gate, persistence/side effect, and human approval where applicable. Do not redesign those foundation seams here unless the product flow reveals a real contradiction.

### 6. Check producer/consumer closure

Before creating tasks, inspect the flow as a system:

- Every consumed artifact must have a legitimate producer or pre-existing source.
- Every produced durable artifact must have a purpose, consumer, or explicitly documented historical/audit role.
- Every state transition must have an owner and trigger.
- Every important interface must connect actual producers and consumers.
- Every invalidation/supersession event must say what becomes stale and what remains historical truth.
- Every failure path must terminate in a defined state rather than "something errors".

Resolve system-level gaps now. Leave only task-local implementation questions for later.

### 7. Map capabilities onto flows

For each approved product capability:

- identify which flow(s) realize it;
- identify which artifacts and interfaces it depends on;
- identify the invariants that define its correctness;
- confirm at least one observable user/system outcome.

A capability that cannot be traced through the flow is not planned yet.

### 8. Produce the implementation task map

Only after the system flow is coherent, split delivery into implementation tasks.

Prefer vertical or behaviorally coherent slices. Avoid layer batches such as "all entities", "all repositories", "all controllers", then "all UI" unless the repository or foundation genuinely requires that sequence.

For each task record:

- `id` and short title;
- outcome in product/system terms;
- dependencies;
- capabilities/flows it advances;
- artifacts/state it consumes;
- artifacts/state it produces or changes;
- interfaces it implements, extends, or consumes;
- invariants it owns/preserves;
- observable integration/acceptance boundary;
- a short `task_planner_context` describing the nuances a later task-planning agent must retain.

Do **not** optimize here for exact task size. Do not recursively decompose task-internal work. The downstream task-planning skill owns complexity/splitting decisions.

The task map's primary test is: **does each task fit cleanly into the already-defined system flow?**

### 9. Define system verification coverage

Describe how the completed product will prove the critical flows and invariants.

At minimum map:

- critical flow -> intended verification level/oracle;
- invariant -> where it should be proven;
- important interface -> integration/contract evidence where needed;
- critical failure/stale/concurrency/permission behavior -> appropriate test or deterministic check.

Do not write a full test implementation plan. Give downstream tasks enough context to avoid locally "passing" while leaving the end-to-end flow unproven.

### 10. Record assumptions, risks, and deliberately deferred decisions

Separate:

- **settled cross-task decisions** — downstream agents should preserve them;
- **open system-level questions** — block verification or require owner decision;
- **task-local delegated choices** — intentionally left for a strong reasoning agent;
- **risks** — things likely to break composition, semantics, or delivery.

Use `DELEGATED` deliberately. It should mean "safe to decide locally without changing another task's contract", not "planner did not think about it".

### 11. Write the artifacts and run structural validation

Populate `docs/project-plan.md` using the bundled template.

Populate `docs/task-map.json` according to `references/task-map-contract.md`.

Run:

```bash
python3 <this-skill>/scripts/validate_task_map.py docs/task-map.json
```

Correct structural/reference failures before handoff.

### 12. Hand off for independent plan verification

End with status:

```text
READY_FOR_PLAN_VERIFICATION
```

Report:

- plan path;
- task-map path;
- validator result;
- unresolved system-level questions, if any;
- explicit instruction that `project-plan-verification` should be run by a fresh/separate agent.

Do not self-certify semantic completeness. Do not invoke the verifier in the same agent/session and treat that as independent review.

## Definition of Done

The plan is ready for independent verification only when:

- approved scope and non-goals are explicit;
- critical capabilities map to end-to-end flows;
- critical flows expose data/process/state changes from trigger to terminal outcome;
- important artifacts have producer/consumer/source-of-truth semantics;
- important system interfaces have explicit contracts at the required planning depth;
- cross-task invariants and lifecycle/state rules have stable IDs;
- failure/stale/retry/approval semantics are explicit where material;
- every planned task has a coherent place in the flow and names relevant inputs/outputs/interfaces/invariants;
- the task map has no broken references or dependency cycles under the validator;
- verification coverage exists for critical flows and invariants;
- task-local choices are delegated intentionally rather than left accidentally vague;
- no implementation work is claimed as complete merely because it is planned.

## Anti-patterns

- A feature list presented as a delivery plan.
- A task list created before the data/process/state flow is understood.
- "Frontend task" / "backend task" decomposition that hides the end-to-end journey.
- Artifacts that are consumed but have no producer or source of truth.
- Interfaces named only as "API" without inputs, outputs, rejection semantics, or owner/consumer.
- State transitions spread across tasks without an owning invariant.
- Treating AI output as authoritative state without validation/provenance rules.
- Repeating the full repository architecture instead of defining only cross-task boundaries.
- Pre-solving local classes, methods, algorithms, or component hierarchies.
- Making tasks tiny solely to simplify planning.
- Leaving important semantics for task agents to independently rediscover.
- Self-reviewing the plan and calling it independently verified.


<!-- contract-registry-flow:project-delivery-plan:begin -->
## Planned contracts vs implemented contracts

`docs/project-plan.md` and `docs/task-map.json` describe the **intended coordinated system**, including contracts that may not exist yet. They are not proof that a capability is currently implemented.

Keep using the existing stable artifact/interface/invariant IDs and each task's existing consumes/produces/interfaces/invariants relationships. Do not add a duplicate contract-impact structure to `task-map.json`.

When downstream task planning happens after predecessor tasks may already be implemented, preserve the stable IDs and reconcile relevant dependencies with the repository's current contract registry. A material semantic mismatch between a planned ID and implemented current state must be surfaced; do not silently redefine the planned contract around accidental implementation details.
<!-- contract-registry-flow:project-delivery-plan:end -->
