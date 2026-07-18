---
name: task-brief-designer
description: Create, tighten, or gap-check one bounded implementation task from a user request, issue, approved plan, specification, or existing brief. Use when asked to make work implementation-ready, define acceptance criteria and verification, split a task, prepare an agent handoff, or repair a task contract. Prefer a lightweight delta over rewriting an adequate brief. Do not implement, certify current repository readiness, or invent unresolved product or architecture decisions.
---

# Task Brief Designer

Turn one bounded task into a clear, testable contract. Preserve useful existing
material and add only what the implementer or reviewer needs.

Repository and user instructions outrank this skill. Preserve existing user
work and never claim ownership of it.

## Choose the profile

Use `guided` by default. Use `high-assurance` only when the user requests it,
an orchestrated artifact chain is already in use, or durable audit/freshness
evidence is proportionate to security, migration, destructive-state,
concurrency, multi-writer, or similar risk.

### Guided

- Accept a user request, issue, plan section, specification, or existing brief
  as authority.
- If an existing task already has a clear outcome, bounded scope, acceptance
  criteria, and useful verification, do not rewrite it. Return a concise gap
  check or make only the requested/local missing additions.
- Produce a compact `ready` brief when a durable artifact is useful. The
  implementer may perform its own focused readiness check; standalone preflight
  is optional.

### High assurance

- Require exact authority, dependency, policy, and artifact paths.
- Use the full template and status `ready_for_preflight` or `blocked_design`.
- Design durable evidence, verification-capability disposition, and explicit
  downstream handoffs for separate preflight and acceptance stages.

Do not upgrade a routine task merely because a fuller template exists. If a
guided task discovers a genuine high-assurance need, name the reason and the
smallest additional artifact or decision required.

## Minimum inputs

Require enough information to identify:

- the requested outcome and its authority;
- repository or working context;
- known scope, dependencies, and constraints; and
- any existing task artifact that should be preserved.

Use `UNKNOWN` for non-blocking facts that later repository inspection can
resolve. Stop with `blocked_design` only when a missing product, architecture,
compatibility, permission, or scope decision could materially change the task.
Do not block merely because paths, command syntax, or current Git state still
need focused discovery.

## Workflow

1. Read applicable instructions, the task authority, and the existing brief if
   present. Load only cited context needed to understand the task.
2. State the smallest testable outcome. Separate confirmed requirements from
   implementation choices and unresolved decisions.
3. Run a delta check before drafting:
   - outcome testable;
   - allowed and prohibited scope clear enough to prevent adjacent work;
   - dependencies and meaningful stop conditions known;
   - acceptance criteria observable; and
   - verification can exercise the decisive behavior.
   Preserve adequate sections verbatim or by reference. Do not expand them for
   template completeness.
4. Split only when pieces can be implemented and verified independently, or
   when a missing shared capability genuinely needs prerequisite work. Avoid
   handoffs whose only result is more coordination.
5. Define concise acceptance criteria. Include the positive behavior and the
   most credible negative, unchanged-state, or failure behavior. For lifecycle
   work—retry, resume, recovery, pagination, migration, repeated selection—name
   the first legitimate state change and the next real occurrence.
6. Map each material risk to the lowest reliable evidence. Use a public entry
   point or real boundary when pure/unit evidence cannot prove wiring,
   persistence, processes, filesystem behavior, database behavior,
   concurrency, permissions, or compatibility.
7. Name targeted and broader verification commands when authority or local
   precedent supplies them. In guided mode, focused command discovery may stay
   with the implementer. In high-assurance mode, unresolved required commands
   go to preflight and must not be presented as passing.
8. Add the task metadata block:

   ```yaml
   agent_tier: mechanical | standard | strong
   reasoning: low | medium | high
   review: mechanical | milestone | immediate
   budget: <tool calls> / <time> / <context>
   ```

   Treat the budget as a soft checkpoint unless higher-priority instructions
   explicitly make it a hard limit.
9. Read `references/task-brief-template.md`. Use only the core sections for a
   guided brief; add the high-assurance sections only for that profile.

## Verification defaults carried by the brief

The user should not need to repeat these instructions for every task:

- For a bug, require a regression that fails for the intended reason before the
  fix when feasible.
- For changed behavior, prefer a focused test capable of rejecting the old or
  faulty behavior.
- Use the lowest reliable test level, adding a real-boundary check only when it
  proves something lower-level evidence cannot.
- Run the targeted check first, then the nearest owning suite, then only the
  broader gate justified by blast radius and authorization.
- Record skipped stronger checks and residual risk without presenting them as
  passed evidence.

## Output contract

For a gap check, report only:

- whether the existing task is usable;
- concrete missing or contradictory items;
- the smallest proposed edits; and
- whether guided implementation may begin or high-assurance preflight is
  warranted.

For a durable brief, use `references/task-brief-template.md` with one status:

- `ready`: guided implementation may begin after a compact self-preflight;
- `ready_for_preflight`: high-assurance design is complete but current
  executability still requires preflight;
- `blocked_design`: a material decision or authority gap prevents safe work.

Never update an official master plan merely to record completion of this
design task.

## Boundaries and routing

- Route current Git state, command resolution, dirty ownership, and current
  dependency checks to a compact implementer self-preflight or standalone
  `task-preflight`.
- Route missing product or architecture authority to its owner or the user.
- Route wider scope or new shared infrastructure back through brief design.
- Do not implement, accept the result, update trackers, launch subagents, or
  modify orchestration state.

## Definition of done

- The task is independently understandable without this conversation.
- Every changed or added line in an existing brief closes a concrete gap.
- Outcome, scope, ACs, evidence, metadata, stops, and next action are clear.
- Guided briefs avoid high-assurance artifact ceremony unless risk justifies it.
- High-assurance briefs preserve exact stage and evidence contracts.
