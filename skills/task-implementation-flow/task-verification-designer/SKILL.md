---
name: task-verification-designer
description: Design a compact, implementation-neutral verification specification for one executable task brief before implementation. A supplied executable task package always requires this stage; an unpackaged direct edit uses it when non-obvious acceptance or failure semantics, state/lifecycle behavior, finite material cases, or test-design burden justify it. Produce a separate verification.md in the task folder. Do not write tests or production code, invent requirements, or redesign the task.
---

# Task Verification Designer

Turn one implementation-ready task contract into clear, falsifiable verification
cases. Help the implementation agent identify each required case and expected
result, and help a human understand the promises covered, the planned proof,
and its limits. The goal is to answer:

> What observations would convincingly show that this task was implemented
> according to its specification?

This is a derived preparation stage between task design and implementation. It
is not a second requirements document. For a supplied executable task package,
it is required before ready preflight and implementation.

Repository and user instructions outrank this skill. Preserve existing user
work and never claim ownership of it.

## Inputs and authority

Require an executable task brief with clear acceptance criteria and enough
authority to state expected behavior without guessing.

Before proceeding:

- use an executable leaf when a supplied brief has `Task kind: composite` and
  `Status: decomposed`;
- return `blocked_design` work to its decision owner;
- treat the task brief and its cited authority as normative;
- treat this verification artifact as derived guidance, not as authority that
  may add or change requirements.

If a decisive expected result cannot be stated without inventing product,
architecture, compatibility, or scope behavior, stop and route the gap back to
`task-brief-designer` or the decision owner. Do not repair the requirement
inside the verification artifact.

## When this stage adds value

Every supplied executable task package uses this stage, even when its brief
recommends `inline` verification or the edit is small. An unpackaged
conversational direct edit uses the skill when explicitly requested or when its
task reasoning recommends it. Typical reasons include:

- several distinct acceptance criteria whose evidence is not obvious;
- negative, unchanged-state, recovery, retry, resume, migration, ordering, or
  other lifecycle behavior;
- finite material cases or invariants where omission could permit false success;
- important public/boundary behavior that a happy-path unit test could miss;
- multiple plausible implementation shortcuts that satisfy the obvious example
  but violate the intended semantics; or
- enough verification reasoning that separating it from implementation reduces
  cognitive load for the implementation agent.

Do not use this stage by default for an **unpackaged** small localized change
with one obvious regression and an unambiguous oracle. More scenarios are not
automatically better.

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

## Authority, coverage, and revision

Identify the source brief and a revision in every `verification.md`. Map every
material AC and finite-risk row to identifiable cases with setup, action, and a
decisive expected result (the oracle). Derive each expectation from the brief or
its cited authority. Coverage is complete only when every required obligation
is represented, regardless of green evidence for other cases.

Keep stable scenario IDs such as `V-01`. Where a scenario groups related cases,
give them stable child IDs such as `V-01a` and `V-01b`, and reference those cases
in the coverage map. Preserve existing scenario IDs when making cases explicit.

When unchanged authority exposes a coverage gap, record the reason for the
revision, retain existing scenario IDs, add only the needed justified scenario,
and route affected readiness and evidence to focused preflight. A changed
requirement or unresolved expected result routes to task design or the decision
owner; scenario editing cannot settle it.

## Workflow

1. Read the executable brief, its cited normative authority, and the repository
   context needed to understand public boundaries and existing test conventions.
   Keep discovery focused on verification design.
2. Name the promises from the brief in plain language. Map every material AC and
   finite-risk row to cases, with links to the relevant brief sections. Identify
   any authority gap before writing a ready artifact.
3. Select the smallest set of cases that distinguishes the intended behavior
   from credible wrong behavior:
   - the positive behavior;
   - the most credible negative, failure, or unchanged-state behavior;
   - a boundary case when the specification contains a meaningful boundary;
   - the next real occurrence for retry/resume/recovery/repeated-state behavior;
   - every finite material case already required by the brief.
4. Choose the lowest reliable test level and observation boundary. Explain its
   scope, the real behavior exercised, and why it catches the intended failure.
   Unit/component checks can prove pure policy decisions. Persistence and reload
   need real storage behavior; contention needs concurrent execution at the actual
   locking boundary; publication safety needs controlled interruption at meaningful
   durable boundaries. Add higher-level evidence for distinct wiring or interaction
   risks. Keep interface/document review and schema checks visibly separate from
   behavioral tests.
5. Write the artifact using the structure below. Establish the feature and
   testing approach first, then the promises and cases. Share common setup and
   test-level reasoning; keep each case's decisive inputs and results easy to find.
6. Apply the completion checks and write only the standalone `verification.md`.
   Leave test names, file placement, framework usage, doubles, helpers, and
   production design to `bounded-task-implementer` within repository authority.

## Make cases easy to implement and review

**One behavioral question per case.** Separate independently different starting
conditions, actions, expected decisions, or decisive boundaries. Several assertions
can describe one outcome, such as a refusal reason plus unchanged version, count,
and files. Share setup across related cases while keeping each obligation visible.
Named cases describe coverage; parameterization and test-function count remain
implementation choices.

**Concrete expected results.** State the correct decision, state transition, and
important unchanged state separately from how they will be checked. Cite the
specific authority locally when the coverage link alone leaves a rule unclear.
Give explicit outcomes for meaningful boundary values, including equality. For
refusals, establish the other prerequisites so the intended guard is reached and
distinguish the required refusal from an unrelated exception or harness failure.
Include a success control wherever an always-refusing implementation could pass.
For permitted alternative outcomes, state their conditions and required safe
postconditions, including the useful blocked state after a conservative stop.

**Visible variants and history.** Use a small case table when related inputs have
different expected decisions: include case ID, relevant input/starting state,
action, and exact expected result. Put shared observations beside the table and
record row-specific differences in the row. Give material lifecycle variants
their own identities. Select combinations based on required coverage and credible
interaction risk, explaining any reduction whose sufficiency is not obvious.
Keep history-dependent proofs as sequences with numbered actions and expected
checkpoints; separate independent guards and alternative histories. A composed
journey should protect its required interaction and reference focused cases for
the remaining matrix.

**Each explanation has one home.** Use behavior-focused titles and explain the
practical consequence of failure in the rationale. Let `Then` state correctness
and `Check` describe observation. Put common level-selection reasoning and shared
setup once, with local additions where a case differs. Use short sentences,
concrete verbs and consistent terms, following ASD-STE100 principles without
claiming formal compliance. Define necessary terms near first use and retain
exact contract names where useful.
Fill the parts that aid understanding; omit empty optional fields and repeated
process reminders.

Keep limitations beside the affected evidence claim. Label seeded states and
identify what creates them in production: setup may provide an upstream state,
while the behavior claimed by the case must still be exercised. Describe what
the evidence leaves unproved, such as real actor execution or model provenance.

## Cross-task integration boundary

Design verification within one executable leaf's acceptance scope. When its
own ACs require composing supplied producer outputs at stated consumer
boundaries, derive cases for exactly those composition ACs. The leaf's brief
and supplied inputs remain the authority.

Route a decomposed composite parent to its dependency-ready executable leaf.
Leave sibling requirements, system-wide integration strategy, and parent-level
composition closure with their owners. For unavailable inputs or an unresolvable
oracle, use the routing below and report the gap truthfully before readiness.

Packaged preparation remains mandatory for that leaf: derived
`verification.md` and a ready `preflight.md` still precede implementation.

## Output contract

Use this single starting structure. Adapt labels and combine short sections when
that improves readability while preserving the required information. The shared
setup section is optional. Case tables and checkpoint sequences may replace the
individual case shape below.

```markdown
# Verification Design: <TASK-ID> — <title>

<Briefly explain the behavior protected and its main failure risks in plain
language.>

## Testing approach

| Checks | Level and real boundary | Why this evidence is sufficient |
|---|---|---|
| <named group; case IDs as needed> | <scope and real behavior exercised> | <distinct risk proved and important limits> |

## Source and revision

Source brief: <path>
Source brief revision: <identified brief revision or supplied revision>
Verification revision: <integer>
Authority: derived from the task brief and its cited normative sources
Status: ready

Ready means the verification design is complete; execution and implementation
readiness are established by later stages.

## Coverage summary

| Promise from the brief | AC / risk row | Required cases |
|---|---|---|
| <short promise with link to the relevant brief section> | AC-01 | V-01 |

## Shared setup

<Common starting state, inputs, and assumptions referenced by related cases.>

## Verification scenarios

### V-01 — <observable behavior and expected outcome>

Covers: AC-01

Why: <practical consequence this check protects against>

Given:
- <starting state and decisive inputs, including relevant shared setup>

When:
- <observable action>

Then:
- <exact decision or result, state transition, and important unchanged state>

Check:
- <how to observe the result at the selected boundary; refer to shared reasoning>

## Implementation handoff

- Implement these cases under the brief's authority, reusing relevant existing
  tests and fixtures. Choose concrete test structure within repository rules.
- Use current preflight for implementation readiness. A reasoned verification
  revision preserves IDs and supersedes affected readiness and evidence until
  focused preflight is ready for that revision.
- Route an unresolved expected result to task design/the decision owner, and an
  unavailable boundary or capability to preflight/its owner, preserving the
  required coverage and expected results.
- <task-specific handoff needs, exclusions, or remaining evidence limits>
```

If the brief is materially insufficient, do not create or overwrite
`verification.md`. Return a concise `needs_brief_revision` result with the
AC/authority gap and smallest next action.

## Completion checks

Read the artifact as both its next implementer and a human reviewer:

- Can each material AC and finite-risk row be followed from a named promise to
  its required cases, including negative, boundary, and lifecycle obligations?
- Can the implementer enumerate those cases and exact expected results without
  unpacking variants or interpreting the policy again?
- Does each case reach its intended behavior and reject a credible wrong result
  at a reliable boundary, with observable checkpoints where history matters?
- Can the human explain what is checked, why it matters, why the selected levels
  are sufficient, and what remains unproved after one reading?
- Is the information stated once where practical, with all required behavior
  grounded in task authority and test-code choices left to implementation?

Resolve coverage or explanation gaps before marking the design ready. A source
ambiguity uses the routing below; formatting checks alone establish neither
coverage nor usefulness.

## Boundaries and routing

- Route ambiguous or missing requirements to `task-brief-designer` or the
  decision owner.
- Route current repository executability, commands, permissions, environment,
  helpers, fixtures, and capability uncertainty to `task-preflight` when a
  separate readiness pass is useful.
- Route production/test implementation to `bounded-task-implementer`.
- Keep edits confined to the verification artifact; preserve production code,
  tests, dependencies, task briefs, project plans, contract registries, reviews,
  and runtime orchestration state.
- Report design readiness; implementation correctness belongs to acceptance
  review.
