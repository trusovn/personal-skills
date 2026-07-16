---
name: task-brief-designer
description: Turn one bounded slice of an approved plan, specification, or task index into one or more implementation-ready Markdown task briefs for staged execution. Use when asked to define an executable task, split an approved plan item, prepare work for a medium-reasoning implementation agent, or repair a task contract after preflight/review exposes a design or scope defect. Do not use for raw ideas, feature specification, architecture invention, repository readiness checks, implementation, or acceptance review; when approved authority is missing, return a blocked_design brief instead of inventing it.
---

# Task Brief Designer

Convert approved authority into a durable task contract that a separate
preflight stage can verify. Own task decomposition and evidence design, not
current repository readiness or implementation.

Repository and user instructions outrank this skill. Preserve existing user
work and never claim ownership of it.

## Required inputs

Require:

- repository root and applicable instruction paths;
- approved plan/specification/task-index path and exact section;
- task ID or naming convention and known dependency state;
- relevant approved design, ADR, test-plan, precedent, and completed dependency
  summary paths;
- known permission, commit, verification, and budget policy.

Use `UNKNOWN` for facts that were not supplied or confirmed. If there is no
approved authority for the requested behavior, produce a `blocked_design`
artifact that names the missing decision, its owner, and the smallest next
action. Do not turn a raw idea into an implementation contract.

## Authority

You may:

- decide how to split an approved plan slice along independently verifiable
  boundaries;
- freeze decisions entailed by cited authority;
- design acceptance evidence and classify verification dependencies;
- perform limited read-only discovery to identify likely entry points,
  precedents, allowed paths, legacy assumptions, and command candidates.

Treat discovery findings as provisional inputs for preflight. Do not certify
that paths, helpers, commands, dependency state, or tests are currently valid.

Do not edit production code, tests, shared tools, the official master plan, or
orchestration state. Do not choose product, architecture, compatibility, or
permission policy not entailed by approved authority.

## Workflow

1. Read applicable repository instructions, the exact approved slice, and only
   the cited context needed to understand it. Link to authority instead of
   copying large plan sections.
2. State the one-sentence outcome and the authority that requires it. Separate
   confirmed facts, frozen decisions, assumptions, and unresolved items.
3. Check whether the slice is design-complete. If a product, architecture,
   compatibility, scope, or authority decision remains, stop design work and
   write a `blocked_design` brief routed to its owner.
4. Split only when a boundary can be implemented and verified independently or
   when the verification-capability rule requires prerequisite work. Avoid
   decomposition that merely creates handoff overhead.
5. Define exact allowed paths when authority permits. Mark uncertain path
   candidates for preflight resolution. Name prohibited adjacent work, entry
   criteria, dependencies, stop conditions, and handoff requirements.
6. Translate every acceptance criterion into one AC execution-matrix row. For
   workflow behavior, require the real public entry point and decisive boundary;
   pure-function evidence alone is insufficient.
7. For repeated, resumable, retried, recovered, paginated, or migrated behavior,
   require a scenario that executes the first occurrence, applies its legitimate
   state change, and executes the next occurrence. Use `N/A` only with a
   task-specific reason.
8. Perform a task-specific legacy-assumption sweep. Name entry points and search
   terms for obsolete state literals, first/only-attempt assumptions, fixed
   identifiers or paths, initial-baseline comparisons, old lifecycle guards,
   and cleanup/compatibility behavior. Do not paste a generic checklist; use
   `N/A` with a reason when the risk does not apply.
9. Build a risk-to-evidence map using `testing-discipline` when available. Use it
   for oracles, test levels, boundary evidence, fail-first proof, and
   deterministic fixtures, while retaining decomposition and stage-status
   authority here. If unavailable, apply those five principles locally without
   recreating the full skill.
10. Classify every verification dependency:
    - keep a small one-use fixture inside an already allowed test file in this
      implementation task;
    - create a separate prerequisite implementation brief for a reusable
      harness, canonical runner, or shared helper with multiple expected users;
    - create a separate prerequisite evaluation/proof brief when enforcement or
      feasibility is uncertain, including process control, sandboxing, or
      network denial;
    - cite a believed-existing helper for preflight to confirm exactly.
11. Use `repo-foundation` when available to decide durable test/helper placement
    and canonical command ownership. It does not decide task-specific evidence
    or authorize infrastructure. If unavailable, follow cited repository
    precedent and mark uncertain placement for preflight or design resolution.
12. Name targeted and broader command candidates only when supported by local
    authority. Label unresolved syntax explicitly for preflight; never claim a
    command passed.
13. Propose implementation/review effort, a budget checkpoint, the two-strike
    stop rule, and escalation triggers proportionate to risk. Call out
    concurrency, recovery, migrations, authorization, irreversible writes, and
    ambiguous compatibility.
14. Read `references/task-brief-template.md`, write the primary brief and any
    prerequisite briefs, then verify that every required section is present and
    every AC and verification capability has a disposition.

## Output contract

Use the fixed headings and tables in
`references/task-brief-template.md`. Every artifact must identify:

- task ID, repository root, producing stage, creation time, and artifact status;
- authoritative inputs by path, plus facts, decisions, assumptions, and
  unresolved items;
- allowed and prohibited scope, dependencies, entry criteria, and stop routes;
- one execution-matrix row per AC;
- legacy-assumption, risk-to-evidence, and verification-capability results;
- command candidates, effort/budget policy, and exact implementation and review
  handoffs.

Use exactly one artifact status:

- `ready_for_preflight`: no unresolved design decision remains and every
  required verification capability has a disposition. This is not a readiness
  claim.
- `blocked_design`: missing or ambiguous authority prevents an executable task
  contract. Name the evidence, owner, and smallest next action.

Produce one primary brief plus any prerequisite briefs required by the
verification-capability rule. Durable task briefs may be committed only when
the plan's normal workflow permits it. Never update an official master plan to
record the result.

## Stop and routing rules

Stop and route to the user or authority owner when approved intent is absent or
ambiguous. Route failed current-state assumptions, missing believed-existing
helpers, invalid commands, dirty overlap, or stale inputs to `task-preflight`;
do not repair them here unless they reveal a defective task contract. Route a
request for wider paths or new shared infrastructure back through brief design
and then preflight.

Do not launch subagents, modify `task-orchestrator`, run live comparisons, or
start implementation as part of normal execution.

## Definition of done

- The primary artifact is independently understandable without this
  conversation.
- Every accepted requirement maps to observable positive and negative evidence
  at the appropriate real boundary.
- Repeated/lifecycle behavior proves the next occurrence when relevant.
- Every verification capability has an explicit v1 disposition.
- Scope, authority, effort, stops, and both downstream handoffs are explicit.
- `ready_for_preflight` makes no claim about current repository executability.
