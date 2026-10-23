---
name: task-brief-designer
description: Create, tighten, or gap-check one bounded implementation task from a user request, issue, approved plan, specification, or existing brief. Use when asked to make work implementation-ready, define acceptance criteria and verification, estimate oversized work and split it into bounded child briefs only when coherent boundaries justify the split, prepare an agent handoff, or repair a task contract. Prefer a lightweight delta over rewriting an adequate brief. Do not implement, certify current repository readiness, or invent unresolved product or architecture decisions.
---

# Task Brief Designer

Turn one bounded task into a clear, testable contract. Preserve useful existing
material and add only what the implementer or reviewer needs.

## Write for the person who will approve the work

Use the brief itself to explain the work. Follow this reading order: outcome,
scope and governing rules, acceptance and evidence, then execution details.
The template uses this order for both executable and composite briefs.

- Open with what completion demonstrates, who uses the result, and what it
  enables next. Distinguish rules or interfaces this task defines from behavior
  it executes and work a later task owns.
- Use concrete verbs and short sentences. Explain necessary technical terms
  on first use; pair stable IDs with their meaning, such as “approved task
  inputs (`ART-001`)”. When an abstract requirement hides important behavior,
  add one brief success or failure example drawn from approved requirements.
- Give each fact one home. Put operating rules beside their precise authority
  references; keep decision history in the source. Include dates, hashes, and
  provenance where precedence, freshness, audit, or a consumer requires them.
  A mutable link alone cannot replace a required exact baseline.
- Keep rationale that prevents a plausible wrong interpretation. Retain a
  sentence when it changes what someone builds, verifies, is allowed to do,
  or hands over. Use concise references for repeated facts and governing
  repository rules, while keeping every child independently understandable.

Revise existing explanations in place. An extra summary, glossary, or checklist
usually adds another account to maintain. Preserve required fields, distinct
cases, exact obligations, and machine-consumed values when compressing prose.

Repository and user instructions outrank this skill. Preserve existing user
work and never claim ownership of it.

When supplied owner-confirmed direction governs the task, classify direction
authority before selecting a profile, status, or output artifact. If the task
would introduce or change a material practical consequence beyond that
direction, return only the direction-delta-needed response in the conversation
and leave the requested task path absent or unchanged. This route takes
precedence over `blocked_design`; unresolved architecture does not convert a
direction gap into a blocked implementation-task artifact. If the task remains
within the approved consequences, continue normally and do not require
direction to authorize consequence-neutral technical details.

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
- Produce a compact `ready` brief when a durable artifact is useful; use the
  preparation route below.

### High assurance

- Require exact authority, dependency, policy, and artifact paths.
- Use the full template and status `ready_for_preflight` or `blocked_design`.
- Design durable evidence, verification-capability disposition, and explicit
  downstream handoffs for separate preflight and acceptance stages.

Do not upgrade a routine task merely because a fuller template exists. If a
guided task discovers a genuine high-assurance need, name the reason and the
smallest additional artifact or decision required.

## Preparation and permission to start

A supplied executable task package always requires a derived `verification.md`,
then a ready `preflight.md`, before implementation. This applies to compact
documentation work as well as code changes. A small clear conversational direct
edit may retain inline verification and a safety check only while no task package
has been supplied; it cannot use the conversational direct-edit exception to
bypass packaged preparation.

For an executable package, use `standalone guided preflight` after derived
verification, or `high-assurance preflight` for that profile. Reserve
`implementer self-preflight` for an unpackaged conversational direct edit;
standalone preflight there is useful for a named material readiness uncertainty.
These are human-readable routes, not extra launch metadata keys.

Explain `ready` as “brief prepared; execution prerequisites still required”.
Report preparation as passed only when supplied current evidence establishes
it; otherwise name the pending prerequisite. A designed brief is not evidence
that implementation may start. Put this distinction and the next action
together in the brief's execution section.

Composite/decomposed work, blocked design, and direct legacy briefs are not
prepared as executable packages. Route them to the dependency-ready leaf, the
task or decision owner, or package normalization respectively.

## Load flow policy

Before estimating a task that could become implementation-ready, read
`references/task-sizing.yaml` and use its active profile. The numeric thresholds
live there intentionally; do not copy them into this skill or silently replace
them with personal defaults.

When creating or updating durable task artifacts, read
`references/task-artifact-layout.md`. Repository or user authority may choose a
different task-package root or directory name, but every durable task must keep
its `brief.md` and required preparation artifacts inside one dedicated package
directory.
Do not create or consume direct briefs under the shared task root.

## Minimum inputs

Require enough information to identify:

- the requested outcome and its authority;
- any supplied governing direction and the part this task is intended to
  advance;
- repository or working context;
- known scope, dependencies, and constraints; and
- any existing task artifact that should be preserved.

Use `UNKNOWN` for non-blocking facts that later repository inspection can
resolve. Stop with `blocked_design` only when a missing product, architecture,
compatibility, permission, or scope decision could materially change the task.
Do not block merely because paths, command syntax, or current Git state still
need focused discovery. Use the abbreviated blocked-design output for a
material decision gap.

## Workflow

1. Read applicable instructions, the task authority, any supplied governing
   direction, and the existing brief if present. Load only cited context needed
   to understand the task.
2. State the smallest testable outcome. When governing direction is supplied,
   prepare the direction trace described in the template. When a technical
   artifact is an intermediate step in an approved end-to-end proof, state both
   its immediate user-observable result and the approved capability it enables;
   do not reduce the trace to a generic artifact property. Allow a task to have
   no direct user-observable effect only when it names the next demonstrable
   outcome it enables. Ground "why now" in approved sequencing or a real
   dependency rather than inventing priority. Separate confirmed requirements
   from implementation choices and unresolved decisions.
   If purpose is unknown, retain that uncertainty and use the existing
   authority-gap route when it prevents a ready brief. Mention unchanged areas
   only when they affect interpretation, scope, or the next action.
3. Run a delta check before drafting:
   - outcome testable;
   - allowed and prohibited scope clear enough to prevent adjacent work;
   - dependencies and meaningful stop conditions known;
   - acceptance criteria observable; and
   - verification can exercise the decisive behavior.
   When governing direction is supplied, also run this direction-authority
   check before claiming the task is ready:
   - Compare the task's material practical consequences, not every
     implementation detail, with the supplied direction.
   - Treat only owner-confirmed direction and specifically confirmed decisions
     as authority. Recommendations, assumptions, unresolved questions, and
     technical notes are not approvals.
   - Check user-observable behavior and operating scenarios, ordered priorities
     and their conflict rule, the first useful proof, scope and non-goals,
     assurance and trust, and intervention and decision ownership.
   - Allow a technical refinement when task authority permits it and it changes
     none of those consequences. Direction need not name every implementation
     detail.
   - Do not make a conflicting request appear authorized by silently dropping
     its stated or recommended behavior and inventing a different task. When
     the supplied request's only proposed approach crosses a direction
     boundary, and the owner has not explicitly rejected or replaced that
     approach with an authorized alternative, the missing choice still needs a
     direction delta. A hypothetical compliant architecture is not authority
     to draft a substitute implementation task.
   - Treat silence as unresolved for a material consequence, not as permission.
     If approval is absent, sources conflict, or the boundary cannot be
     established, return the direction-delta-needed form below in the
     conversation and stop without creating or modifying the requested task
     artifact.
   Preserve adequate sections verbatim or by reference. For other material
   product or architecture gaps, switch to `blocked_design` and stop before
   the remaining drafting steps.
4. Classify verification-capability uncertainty before choosing preflight or a
   split:
   - Use implementer self-preflight or standalone guided preflight when an
     authorized capability is present or reasonably believed to exist and only
     its current path, interface, command, permission, or availability needs
     confirmation. The implementation contract must remain bounded regardless
     of that current-state result.
   - Create a separate prerequisite evaluation/proof task when no approved or
     believed-existing mechanism can establish the decisive oracle, and
     feasibility would choose the enforcement design, change implementation
     scope, require cross-platform/environment proof, or introduce a shared
     helper or harness. The proof task resolves the mechanism and boundary
     without implementing production behavior. Mark the primary task
     `blocked_design`, record the prerequisite dependency, and do not imply
     preflight or the implementer may discover around it. Give the prerequisite
     task its own proof-only scope, real-boundary success and failure oracles,
     required environments, decision owner, and handoff. Classify the missing
     verification capability as prerequisite/uncertain feasibility; do not
     silently assign a reusable helper to either implementer.
   After this capability classification, apply the sizing/decomposition
   contract below before finalizing any implementation-ready leaf.
   Verification prerequisite tasks are not a way to evade sizing, and sizing
   is not a way to hide unresolved authority or feasibility.
5. Expand finite material risks when authority contains a universal or
   lifecycle claim whose cases are both enumerable and consequential. Name
   every approved artifact family, ordered publication prefix, exact
   cardinality, retry/recovery state, tamper case, or bounded cleanup state
   whose omission could permit false success. Do not expand open-ended quality
   words, speculative abuse cases, or a generic test catalog.
6. Define concise acceptance criteria. Include the positive behavior and the
   most credible negative, unchanged-state, or failure behavior. For lifecycle
   work—retry, resume, recovery, pagination, migration, repeated selection—name
   the first legitimate state change and the next real occurrence.
7. Design evidence using the finite-risk contract and verification defaults
   below. Classify verification reasoning as `inline` for obvious tests and
   oracles, or `separate — <reason>` for non-obvious negative/lifecycle semantics,
   finite cases, boundary behavior, or multiple plausible-wrong implementations.
   This recommendation is for `task-verification-designer`; either value keeps
   the required packaged preparation. Resolve ambiguous requirements with their
   owner before verification design.
8. Apply sizing, then read `references/task-brief-template.md` and assemble the
   applicable form. Keep the four scalar launch keys `agent_tier`, `reasoning`,
   `review`, and `budget` for executable leaves only. Use authority-approved
   values as intended launch guidance, not observed runtime configuration.
   Treat the budget as a soft checkpoint unless authority makes it hard.
   Add only the high-assurance fields needed for that profile.

When `review: immediate`, include the ordered follow-on in new briefs and
surgical gap-checks: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision. Following a review skill in the authoring or
implementation session does not state independent acceptance. This follow-on
comes after the preparation and implementation sequence, not in place of it.

## Sizing and decomposition contract

Treat the execution estimate as a gate that forces a boundary-quality
decision, not merely descriptive metadata and not an automatic split
command.

1. Estimate the candidate implementation task after its authority, outcome,
   scope, acceptance criteria, and decisive verification are clear. Estimate
   only the implementation-agent work: focused repository discovery, production
   edits, task-owned tests, and implementation verification. Exclude separate
   preflight, maintainability review, contract-registry synchronization,
   acceptance review, and orchestrator/controller work.
2. Record a numeric estimated agent-call count, numeric implementation duration
   in minutes, and estimate confidence. Use the intended `agent_tier` /
   `reasoning` pair from launch metadata for a leaf; record the original pair
   in sizing for a composite. Then evaluate the active profile from
   `references/task-sizing.yaml`. A configured execution-profile trigger
   applies to the complete pair; for example, a `strong` + `high` rule means
   both values together, not either value independently. Numeric maxima trigger
   only when the estimate is greater than the maximum; equality fits.
3. When any active decomposition trigger matches, make an explicit boundary
   decision; never split automatically on the trigger alone. Prefer coherent
   behavioral, ownership, interface, state-transition, or artifact boundaries
   whose outputs can be consumed explicitly by later work. Before committing
   to a split, assess the candidate boundary for clear single ownership of
   each child outcome, stable explicitly consumable handoffs, independent
   implementation and verification per child, shared edit/test surfaces the
   split would force back together, likely contract renegotiation, and net
   delivery benefit including coordination and rework cost. Prefer a split
   when settled boundaries produce independently verifiable outcomes with
   cheaper coordination than keeping the work whole; reject a poor partition
   by keeping coherent work together or choosing a better boundary. A
   component/layer split alone is not sufficient evidence. Do not split by
   arbitrary file halves, architectural layers, equal call counts, or a
   detached "write tests" task merely to force estimates below a threshold.
4. The original task becomes a `composite` parent with status `decomposed`.
   It is a coordination/coverage contract and is never a launch target for
   `bounded-task-implementer`. Give child IDs stable numeric suffixes such as
   `TASK-017.1`, `TASK-017.2`, and nested suffixes only when recursive
   decomposition is actually needed.
5. Give every child the same executable-brief contract as an ordinary task:
   authority, relevant direction trace, bounded scope, consumes/produces
   relationships, interfaces/invariants, acceptance criteria, verification,
   stops, launch metadata, and sizing evidence. Preserve relevant stable
   project-plan IDs rather than inventing child-local replacements for flows,
   artifacts, interfaces, or invariants.
6. Re-estimate every child independently and recursively apply the active sizing
   profile. Only leaf tasks may be handed to implementation. A decomposition is
   not successful merely because the parent was renamed: it must reduce the
   triggering work and leave each leaf within the active envelope, unless the
   permitted no-split override below applies.
7. If a parent-level acceptance criterion can only be proven after sibling work
   composes, create a final executable integration child that owns that proof
   and any required wiring. Do not invent a special composite-parent
   implementation or acceptance-review stage.
8. A triggered task may remain one executable leaf when concrete coupling or
   coordination/rework costs favor keeping it whole, even without strict
   atomicity. Use this no-split decision only when the active sizing profile
   allows the override, and record `decomposition_override:
   cannot_split_safely` with the triggered limit(s), the candidate boundary
   considered, the concrete coupling/coordination reason, and residual
   execution risk. Mere preference or high reasoning alone is insufficient:
   strong reasoning by itself is not evidence that a task is irreducible.
   Respect explicit hard authority limits; the decision may not override an
   authority-declared hard constraint, and it stays within the active
   policy's override permission.
9. Before writing the decomposition package, verify:
   - children collectively cover the parent outcome and every parent AC;
   - no approved requirement, invariant, interface, or contract impact
     disappeared during splitting;
   - every produced shared artifact/state/interface has one clear owning child;
   - dependencies are acyclic and do not require a child to consume unavailable
     work; and
   - each leaf fits the active profile or carries the permitted explicit
     override.
10. For a multi-brief decomposition, use the artifact layout's composite/child
    paths and create or update its structural `docs/tasks/index.json` unless
    repository authority declares an equivalent index. This index describes
    task structure only; do not mutate `docs/task-map.json`,
    `docs/project-plan.md`, review history, or runtime orchestration state.
    For an unsplit explicit-path gap-check, do not create or migrate an index
    merely for ceremony.

For surgical gap-checks of an existing executable brief, sizing remains
mandatory. Add the execution-sizing evidence as the smallest local addition;
when its estimate triggers the boundary decision, either keep the executable
leaf with the recorded reasoned no-split decision or replace the executable
handoff with a composite parent and bounded child briefs. Do not use the
gap-check form to avoid a triggered boundary decision, and do not split
merely to silence the trigger.

## Finite-risk coverage contract

Use finite-risk cases only when workflow step 5 finds a finite, material
dimension. Prefer one labelled block per risk ID, as shown in the template;
a table is suitable when its cells remain short. Preserve these six meanings
with each case:

- the invariant;
- the exact material dimensions or state transitions;
- the decisive observable oracle and real boundary;
- fail-first, targeted, or owning evidence the implementer must establish;
- a distinct independent-review probe, or `N/A` with a reason; and
- the gate owner and stage.

Cases may combine dimensions only when they share one invariant and oracle.
This is a coverage contract, not a Cartesian-product requirement. Keep
implementation evidence separate from review corroboration; an implementer
self-check is not acceptance. For an immediate-review correction flow, state
whether the correction implementer or final fresh reviewer owns the broader or
aggregate gate. Keep targeted evidence first while it is red instead of
requiring the same broad gate after every failed review. Shared gate ownership
may be stated once with explicit case IDs. Keep risk IDs stable across
corrections so later reviews can carry each case forward as
`pass`, `fail`, `blocked`, or `unchecked`; prior status is not proof for
corrected bytes.

## Verification defaults carried by the brief

The user should not need to repeat these instructions for every task:

- For a bug, require a regression that fails for the intended reason before the
  fix when feasible.
- For changed behavior, prefer a focused test capable of rejecting the old or
  faulty behavior.
- Use the lowest reliable test level, adding a real-boundary check only when it
  proves wiring, persistence, filesystem/database/process behavior, concurrency,
  permissions, or compatibility that lower-level evidence cannot establish.
- Name commands supplied by authority or local precedent. Guided command
  discovery may stay with the implementer; unresolved high-assurance commands
  belong to preflight.
- Run the targeted check first, then the nearest owning suite, then only the
  broader gate justified by blast radius and authorization.
- Assign each broader or aggregate gate to an owner and stage; do not silently
  duplicate it across correction and review.
- Record skipped stronger checks and residual risk without presenting them as
  passed evidence.

## Output contract

For a gap check, report only:

- whether the existing task is usable;
- concrete missing or contradictory items;
- the smallest proposed edits;
- which execution prerequisite remains and whether high-assurance preflight
  is warranted;
- whether verification design should stay inline or use a separate
  `task-verification-designer` pass, with the concrete reason when separate;
  and the immediate-review follow-on above when applicable.

When supplied direction does not authorize a needed product, priority,
assurance, trust, intervention, or scope choice, return only:

```markdown
# Direction delta needed: `<requested task>`

- Governing direction: `<exact source and relevant section>`
- Missing decision: `<plain-language choice the task cannot make>`
- Why it matters: `<practical consequence for the owner or user>`
- Options: `<concise choices and their practical tradeoffs>`
- Recommendation: `<optional and clearly non-authoritative, or none>`
- Downstream impact: `<briefs or plans that may need review>`
- Owner action: `<smallest decision or direction update needed>`
```

This is a routing response, not a task brief. Return it in the conversation and
leave the requested task path absent or unchanged. Write a durable delta only
when the user explicitly requests a separate direction-delta artifact path;
never store it at the requested implementation-task path.

For a durable brief, use `references/task-brief-template.md`. When governing
direction was supplied, include its `Direction trace` section and require
`New direction decisions required: None`; any other value requires the
direction-delta-needed response instead of a ready brief. Use one status:

- `ready`: an executable guided brief is prepared; execution still requires
  the preparation route above;
- `ready_for_preflight`: an executable high-assurance leaf is designed but
  current executability still requires preflight;
- `decomposed`: the original task is a non-executable composite parent whose
  child briefs are the only implementation launch targets;
- `blocked_design`: a material decision or authority gap prevents safe work.

Use task kind `executable` with `ready` / `ready_for_preflight`, and
`composite` with `decomposed`. Do not attach executable launch metadata to a
composite parent.

For `blocked_design`, return only the requested outcome as stated, the missing
decisions or authority, their owner, and the smallest planning action. Omit
launch metadata, readiness routing, proposed architecture, implementation
scope or paths, work items, implementation ACs, finite-risk coverage,
verification obligations, and implementation handoff language. Those details
would turn an unapproved premise into apparent authority.

Never update an official master plan merely to record completion of this
design task.

## Final read and ownership

Read the brief as a person unfamiliar with the design. They should be able to
explain the result, what completion proves versus enables, the governing rules,
and the pending execution prerequisite. Then check that compression preserved
each approved obligation, exception, stable ID, evidence role, and handoff.
Apply the same check to child coverage and dependencies after decomposition.

This skill owns brief design and the structural task-index entries it creates.
Current repository readiness belongs to preflight; expanded scope returns to
design. Implementation, acceptance, subagent launches, and runtime orchestration
state are outside this skill's work.


<!-- contract-registry-flow:task-brief-designer:begin -->
## Expected contract impact

When the repository has a contract registry, use it while preparing the brief to resolve already implemented dependencies before asking the implementation agent to explore code broadly.

For tasks that may materialize or change durable cross-task contracts, include a compact `Expected contract impact` section derived from existing task-map IDs and current repository state. It should identify:

- relevant stable plan refs and whether this task is expected to materialize/change/preserve them;
- current contract dependencies already available in `docs/contracts`;
- the expected durable current-state delta in behavioral/ownership terms.

When there is no expected durable cross-task impact, state `Expected contract impact: none` rather than inventing registry work.

The brief describes expected delta, not proof of what implementation eventually produced.
<!-- contract-registry-flow:task-brief-designer:end -->
