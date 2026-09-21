---
name: task-verification-designer
description: Design a compact, implementation-neutral verification specification for one executable task brief before implementation. Use when a task has non-obvious acceptance or failure semantics, state/lifecycle behavior, finite material cases, or enough test-design burden that a dedicated pass would help the implementation agent. Produce a separate verification.md in the task folder. Do not write tests or production code, invent requirements, redesign the task, or require this stage for every task.
---

# Task Verification Designer

Turn one implementation-ready task contract into a compact set of falsifiable
verification scenarios. The goal is to answer:

> What observations would convincingly show that this task was implemented
> according to its specification?

This is an optional preparation stage between task design and implementation.
It is not a second requirements document and is not mandatory merely because the
skill exists.

Repository and user instructions outrank this skill. Preserve existing user
work and never claim ownership of it.

## Inputs and authority

Require an executable task brief with clear acceptance criteria and enough
authority to state expected behavior without guessing.

Before proceeding:

- reject a brief with `Task kind: composite` and `Status: decomposed`; use an
  executable leaf instead;
- reject `blocked_design` work;
- treat the task brief and its cited authority as normative;
- treat this verification artifact as derived guidance, not as authority that
  may add or change requirements.

If a decisive expected result cannot be stated without inventing product,
architecture, compatibility, or scope behavior, stop and route the gap back to
`task-brief-designer` or the decision owner. Do not repair the requirement
inside the verification artifact.

## When this stage adds value

Use the skill when explicitly requested or when the task brief recommends it.
Typical reasons include:

- several distinct acceptance criteria whose evidence is not obvious;
- negative, unchanged-state, recovery, retry, resume, migration, ordering, or
  other lifecycle behavior;
- finite material cases or invariants where omission could permit false success;
- important public/boundary behavior that a happy-path unit test could miss;
- multiple plausible implementation shortcuts that satisfy the obvious example
  but violate the intended semantics; or
- enough verification reasoning that separating it from implementation reduces
  cognitive load for the implementation agent.

Do not use this stage by default for a small localized change with one obvious
regression and an unambiguous oracle. More scenarios are not automatically
better.

## Artifact location

When repository or user authority does not name another path, use the task
package convention from
`../task-brief-designer/references/task-artifact-layout.md`.

For a normal task package:

```text
docs/tasks/TASK-017/
  brief.md
  verification.md
```

Write `verification.md` in the same task package as `brief.md`. Do not append it
to the brief, project plan, review report, or runtime state.

If repository authority uses another task-package root or directory naming
convention, follow it while preserving one dedicated directory per task and the
fixed `brief.md` and `verification.md` names. Do not create or consume a direct
brief under a shared task root.

Before overwriting an existing `verification.md`, require its singular
`Source brief:` value to resolve to the package's `brief.md`. If the declaration
is absent, malformed, or names another brief, leave the target unchanged and
report the artifact conflict.

## Workflow

1. Read the executable brief, its cited normative authority, and only the
   repository context needed to understand public boundaries or existing test
   conventions. Do not perform broad implementation discovery.
2. Build an AC coverage map. Every material AC must have at least one scenario
   or a clearly stated reason that verification cannot yet be designed.
3. For each AC, identify the smallest set of scenarios that can distinguish the
   intended behavior from credible wrong behavior:
   - the positive behavior;
   - the most credible negative, failure, or unchanged-state behavior;
   - a boundary case when the specification contains a meaningful boundary;
   - the next real occurrence for retry/resume/recovery/repeated-state behavior;
   - every finite material case already required by the brief.
4. Prefer scenarios that would reject a plausible shortcut, stale behavior, or
   partial implementation. Avoid scenarios that merely restate the happy path
   in different words.
5. Choose the lowest reliable observation boundary. A unit/module-level oracle
   is enough when it proves the contract. Name a public or real boundary when
   lower-level evidence cannot prove wiring, persistence, filesystem/database/
   process behavior, authorization, recovery, or another task-local material
   property.
6. Express each scenario in a BDD-shaped, implementation-neutral form. Use
   `Given / When / Then` when state and transitions benefit from it; otherwise
   concise preconditions, stimulus, and oracle are sufficient.
7. Keep test implementation choices with `bounded-task-implementer`. Do not
   prescribe test class/function names, exact file placement, mocking strategy,
   helper architecture, production design, or framework-specific structure
   unless the task authority already fixes them.
8. Run the completion checks below, then write the standalone
   `verification.md`.

## Scenario contract

Use stable scenario IDs such as `V-01`, `V-02`, and `V-03`.

Each scenario must contain:

- **Covers:** one or more task AC IDs or finite-risk rows;
- **Intent:** the semantic mistake or obligation the scenario distinguishes;
- **Given:** relevant preconditions or starting state;
- **When:** the observable action/stimulus;
- **Then:** the externally meaningful result or invariant;
- **Oracle / boundary:** what must be observed and at what reliable boundary;
- **Variants:** only material variants already implied by the task, or `none`.

Do not use scenario count as a quality metric. Combine cases when they exercise
the same invariant and oracle; split them when materially different behavior
could pass or fail independently.

### Example shape

```markdown
### V-02 — Repeating the operation does not duplicate persisted state

Covers: AC-03

Intent: Reject an implementation that handles the first call correctly but
creates duplicate state on the next legitimate occurrence.

Given:
- the first operation completed successfully and its state is persisted

When:
- the same permitted operation occurs again under the task-defined conditions

Then:
- the externally visible result follows AC-03
- no duplicate persisted entity/state is created

Oracle / boundary:
- observe the public operation result and persisted state at the task-defined
  real boundary

Variants:
- none
```

The example is structural only. Never copy its semantics into an unrelated
task.

## Cross-task integration boundary

This initial skill version does **not** own verification design across sibling
tasks, decomposed-child composition, or parent-level integration closure.

Task-local use of a real boundary is still allowed when needed to prove that
single task's own ACs. If the supplied brief can only be verified by composing
separate task outputs, report that limitation to the caller rather than
inventing cross-task scenarios here.

## Output contract

Write one standalone artifact:

```markdown
# Verification Design: <TASK-ID> — <title>

Source brief: <path>
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02 | <why these are sufficient or key residual limitation> |

## Verification scenarios

### V-01 — <short discriminating title>

Covers: AC-01

Intent: <what wrong behavior this catches>

Given:
- <precondition>

When:
- <stimulus>

Then:
- <observable result>

Oracle / boundary:
- <decisive observation and boundary>

Variants:
- <material variants or none>

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios.
- Concrete test structure, framework usage, helpers, and file placement remain
  implementation choices unless already fixed by repository authority.
- If implementation discovery shows that a scenario cannot be exercised at its
  stated boundary, route the conflict back to task design/preflight rather than
  silently weakening the oracle.
```

If the brief is materially insufficient, do not create or overwrite
`verification.md`. Return a concise `needs_brief_revision` result with the
AC/authority gap and smallest next action.

## Completion checks

Before writing the artifact, verify:

- every material task AC is mapped;
- every finite-risk row in the brief is mapped when present;
- scenarios have decisive observable oracles rather than implementation-detail
  assertions;
- important negative/lifecycle behavior from the brief is represented;
- at least one scenario rejects the most credible plausible-wrong behavior for
  each non-trivial semantic obligation when such a distinction exists;
- no scenario adds a requirement absent from the brief/authority;
- no test implementation architecture has been prescribed unnecessarily; and
- no cross-task integration verification has been invented.

## Boundaries and routing

- Route ambiguous or missing requirements to `task-brief-designer` or the
  decision owner.
- Route current repository executability, commands, permissions, environment,
  helpers, fixtures, and capability uncertainty to `task-preflight` when a
  separate readiness pass is useful.
- Route production/test implementation to `bounded-task-implementer`.
- Do not edit production code, tests, dependencies, task briefs, project plans,
  contract registries, reviews, or runtime orchestration state.
- Do not approve implementation correctness; this is design guidance, not
  acceptance review.

## Definition of done

- The verification design is compact, task-local, and independently readable.
- Every material AC maps to falsifiable evidence.
- Scenarios emphasize semantic discrimination rather than test quantity.
- Requirements remain owned by the brief and its authority.
- The implementer retains freedom over concrete test implementation.
- The artifact lives separately inside the executable task package.
