---
name: project-plan-verification
description: Use after `project-delivery-plan` (or an equivalent lightweight project plan) and before task implementation to independently verify that the plan is complete, coherent, and executable as a set of composing tasks. Run this as a fresh/separate reviewer agent. Reconstruct the required end-to-end data/process/state flows from authoritative project inputs, then check scope coverage, artifact producer/consumer closure, interfaces, lifecycle/state semantics, invariants, task placement/dependencies, and verification coverage. Emit a separate review report with ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Do not edit or repair the plan in this skill.
---

# Project Plan Verification

Independently verify that a project delivery plan is a reliable coordination contract for downstream task planning and implementation.

The planner's job was to make system flow explicit. Your job is to **challenge that claim** from fresh context.

Do not optimize the plan. Do not implement features. Do not silently repair gaps while reviewing.

## Independence requirement

Run this skill with a fresh/separate agent from the one that authored the plan whenever possible.

Treat planner explanations as claims, not evidence. Reconstruct the required behavior from authoritative upstream inputs and the repository before trusting the plan's own flow/task mapping.

If you authored the plan in the same active reasoning context and no fresh reviewer can be used, state `INCONCLUSIVE — independence not achieved` rather than claiming independent verification.

## Inputs

Required:

- `docs/project-plan.md` (or the repository-declared equivalent)
- `docs/task-map.json`
- current repository/scaffold

Read all authoritative upstream planning/foundation sources referenced by the plan, including when applicable:

- approved proposal / project direction
- `docs/project-charter.md`
- `docs/ai-foundation.md`
- foundation/readiness review
- repository-local architecture/maintainability rules

Do not require artifacts that the project's planning route intentionally does not produce.

## Output

Create or replace:

- `docs/project-plan-review.md`

Use `references/plan-verification-report-template.md`.

Before semantic review, run:

```bash
python3 <this-skill>/scripts/verify_plan_artifacts.py docs/project-plan.md docs/task-map.json
```

This command is structural evidence only; it is not the semantic verdict.

## Verdicts

Return exactly one:

- `ACCEPT` — the plan is sufficiently complete and coherent to enter downstream task planning/implementation.
- `CHANGES_REQUESTED` — one or more concrete plan defects would cause task ambiguity, broken composition, missing behavior, or unverifiable semantics.
- `INCONCLUSIVE` — required authoritative input/evidence is unavailable, contradictory, or reviewer independence/freshness cannot be established.

Severity:

- `BLOCKER` — implementation should not begin; a fundamental scope/flow/contract gap exists.
- `MAJOR` — downstream tasks could plausibly diverge, omit required behavior, or compose incorrectly.
- `MINOR` — worthwhile clarification or cleanup that does not currently threaten correct composition.
- `NOTE` — non-blocking observation.

`ACCEPT` requires no `BLOCKER` or `MAJOR` findings and no unresolved system question that blocks a critical flow.

## Review stance

Verify the plan at the same abstraction boundary it is supposed to own:

- Be strict about system semantics, interfaces, artifact/state ownership, and cross-task invariants.
- Do not reject a plan merely because it leaves local implementation choices to strong reasoning agents.
- Do reject a plan when a supposedly "local" choice would change another task's contract or a critical system invariant.
- Do not demand full SDD artifacts unless the project's actual risk/authority requires them.
- Prefer concrete counterexamples: show the flow/task combination that would fail or become ambiguous.

## Protocol

### 1. Establish review freshness

Record:

- reviewer/session identity if available;
- current repository revision/worktree state as appropriate;
- SHA-256 digest of `docs/project-plan.md`;
- SHA-256 digest of `docs/task-map.json`;
- authoritative upstream documents used.

A prior verdict is stale whenever either reviewed planning artifact changes materially. Do not carry an old `ACCEPT` across new plan bytes.

### 2. Run structural artifact verification

Run the bundled checker.

Any invalid JSON, broken references, missing required plan sections, or task dependency cycle is at least `MAJOR`; a broken dependency graph or unreadable required artifact is normally `BLOCKER`.

Do not stop at a structural pass.

### 3. Independently reconstruct expected scope and critical journeys

From the approved/project-authoritative inputs, write a short private/review reconstruction of:

- product outcome;
- required capabilities;
- primary actors;
- critical user/system journeys;
- explicit non-goals;
- foundation constraints that materially affect the flow.

Then compare that reconstruction with the plan.

Look for:

- missing approved behavior;
- newly invented scope;
- silently weakened requirements;
- foundation constraints that disappeared during planning.

### 4. Verify end-to-end flow completeness

For each critical journey, trace from trigger to terminal observable outcome.

At every step ask:

- What data/state enters?
- Who owns the step?
- Which artifact is authoritative?
- Which interface is crossed?
- What state is written or transitioned?
- What can reject/fail/stale here?
- What consumes the result next?

Raise a finding when the plan uses vague bridges such as "process it", "call backend", "AI analyzes", "save result", or "update UI" where independent tasks need a concrete cross-boundary semantic contract.

Do not require implementation-local detail when no cross-task ambiguity exists.

### 5. Verify artifact producer/consumer closure

For every important artifact/state object:

- identify its legitimate producer or pre-existing source;
- identify its authoritative owner/source of truth;
- identify consumers;
- identify permitted mutations;
- verify lifecycle/invalidation/supersession semantics;
- confirm historical/audit artifacts are intentionally terminal if they have no active consumer.

Flag:

- consumed artifacts with no producer/source;
- multiple accidental sources of truth;
- produced artifacts with no purpose;
- derived/stale data with no invalidation rule;
- historical artifacts that can be silently rewritten.

### 6. Verify lifecycle and state semantics

For every important stateful process/artifact:

- valid transitions are representable;
- forbidden transitions are explicit enough for tasks to preserve;
- authority to transition state is clear;
- failure/cancellation/retry semantics terminate in known state;
- atomicity is explicit where partial completion would violate an invariant;
- stale/superseded states cannot masquerade as current truth.

For AI-bearing flows also verify that model output, parsing/validation, policy/human gates, persistence, retry, and side-effect boundaries remain compatible with `docs/ai-foundation.md`.

### 7. Verify system interfaces

For every interface that independent tasks meet at, check that the plan defines enough to compose:

- owner/producer;
- consumer;
- inputs;
- outputs;
- success semantics;
- important rejection/error semantics;
- authorization/idempotency/concurrency/version semantics when material.

The exact DTO/class/schema may be delegated if the owning task can choose it without forcing another task to guess. If two tasks need the same contract independently, the plan must settle the behavior sufficiently.

### 8. Verify invariants are complete and placed correctly

For each critical cross-task rule:

- it has a stable invariant or equivalent explicit statement;
- the artifacts/flows/interfaces it constrains are identified;
- at least one task owns/preserves it;
- verification evidence is planned.

Also search for implicit invariants not captured by the plan. Typical examples:

- version/provenance identity;
- no unauthorized side effect before approval;
- only one canonical current state;
- stale results cannot be applied as current;
- retries cannot duplicate a side effect;
- failed runs cannot appear successful;
- rejected actions do not mutate authoritative state.

### 9. Verify capability and task coverage

For every approved capability:

- at least one end-to-end flow realizes it;
- at least one task advances/owns the necessary behavior;
- relevant artifacts/interfaces/invariants are covered;
- there is an observable completion boundary.

For every task:

- it fits a real capability/flow;
- dependencies are sufficient and not circular;
- its consumed artifacts/interfaces exist before it starts;
- its outputs have downstream consumers or defined system value;
- `task_planner_context` preserves important cross-task nuance;
- it does not secretly require a system-level decision that the plan delegated away.

Do not reject a task because it may later need splitting. Task sizing belongs downstream.

### 10. Verify implementation order and handoffs

Mentally execute tasks in dependency order.

Check that:

- a task never requires an interface/artifact whose owning task is not yet available unless the plan explicitly defines a safe stub/contract seam;
- foundation-only seams are not mistaken for completed feature behavior;
- parallelizable tasks have stable shared contracts;
- tasks that mutate a shared contract are ordered or coordinated;
- no later task must reinterpret an earlier task's artifact because the contract was underspecified.

### 11. Verify system verification coverage

For critical flows and invariants, check that the plan identifies an adequate intended oracle/evidence level.

Raise findings when:

- all tasks can locally pass while a critical end-to-end journey remains untested/unverifiable;
- wiring/persistence/version/concurrency/permission behavior requires a real boundary but only unit-level intent is planned;
- model-quality acceptance is required but no eval strategy exists;
- model quality is not required but the plan unnecessarily depends on live-model tests for business correctness.

### 12. Check planning abstraction quality

Assess both failure modes:

**Too vague**
- tasks must rediscover system semantics;
- interfaces are names without contracts;
- artifacts lack ownership/lifecycle;
- flows skip state/failure transitions.

**Too prescriptive**
- class/method/file layouts are dictated without cross-task need;
- algorithms are preselected when behavior alone would suffice;
- UI component hierarchies or implementation sequences crowd out the actual contract;
- task-internal substeps are exhaustively planned despite being safe for strong-agent inference.

Only request changes when the abstraction problem has a concrete coordination, correctness, or maintainability consequence.

### 13. Write `docs/project-plan-review.md`

Use the bundled report template.

Every `BLOCKER`/`MAJOR` finding must contain:

- the affected flow/artifact/interface/invariant/task IDs;
- the concrete gap or contradiction;
- a plausible failure/divergence scenario;
- the smallest plan-level correction needed.

Do not prescribe implementation code as the correction.

### 14. Return the verdict

- `ACCEPT` when the plan is ready to feed downstream task planning.
- `CHANGES_REQUESTED` when planner correction is needed.
- `INCONCLUSIVE` when evidence or independence is insufficient.

If changes are requested, route back to the planning owner/agent. A corrected plan changes the reviewed bytes, so run this skill again with fresh context before implementation begins.

## Definition of Done

The review is complete when:

- reviewed artifact digests are recorded;
- authoritative upstream sources are named;
- scope was independently reconstructed;
- every critical flow was traced end to end;
- artifact producer/consumer/source-of-truth closure was checked;
- state/lifecycle and stale/failure semantics were checked;
- cross-task interfaces were checked;
- invariants and verification coverage were checked;
- every capability and task was traced into the system flow;
- dependency/order composition was checked;
- the plan was assessed for both under- and over-specification;
- findings are evidence-based and use plan IDs;
- exactly one verdict is issued;
- the reviewer did not modify the planning artifacts under review.

## Anti-patterns

- Editing the plan while reviewing it.
- Accepting because the JSON validator passes.
- Repeating the planner's flow instead of reconstructing it independently.
- Turning review into architecture redesign.
- Demanding implementation detail merely to make the document longer.
- Ignoring producer/consumer gaps because individual tasks sound reasonable.
- Treating task-size uncertainty as a project-plan defect.
- Verifying only the happy path.
- Trusting AI output/state without checking deterministic validation and authority boundaries.
- Reusing an old verdict after plan bytes changed.
- Claiming independent review from the same planning reasoning context.
