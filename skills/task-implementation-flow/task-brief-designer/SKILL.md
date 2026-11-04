---
name: task-brief-designer
description: Create, tighten or gap-check a bounded task from a request, issue, approved plan, specification or brief. Use for implementation readiness, acceptance/verification, sizing, justified splitting, handoff or contract repair. Prefer small deltas. Do not implement, certify repository readiness or invent product/architecture decisions.
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
- Use short sentences, concrete verbs and consistent terms, following
  ASD-STE100 principles without claiming formal compliance. Explain necessary
  technical terms on first use; pair stable IDs with their meaning, such as
  “approved task inputs (`ART-001`)”. When an abstract requirement hides important behavior,
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
- Use the applicable high-assurance addendum and status `ready_for_preflight` or `blocked_design`.
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

Check these conditions before the first dependent action. Read only applicable
references. Do not read every reference at startup. If required instructions are
missing or unreadable, stop the affected action and report the exact gap; do not
infer permission to bypass them.

| Reference | Required condition and timing |
|---|---|
| [Sizing policy](references/task-sizing.yaml) (`references/task-sizing.yaml`) | Before estimating a task that could become implementation-ready; use its active profile. |
| [Artifact layout](references/task-artifact-layout.md) (`references/task-artifact-layout.md`) | Before creating or updating durable task artifacts. |
| [Executable brief form](references/task-brief-template.md) | Before assembling a durable executable brief. |
| [Decomposition package](references/decomposition.md) | After choosing a split, before writing any parent, child or structural index. |
| [Exceptional output](references/exceptional-output.md) | Before returning a direction-delta-needed or blocked-design response. |
| [High-assurance fields](references/high-assurance.md) | Before assembling high-assurance fields or the addendum. |

Numeric thresholds live in the sizing policy; do not copy them here or silently
replace them with personal defaults. Repository or user authority may choose a
different task-package root or directory name, but every durable task must keep
its `brief.md` and required preparation artifacts inside one dedicated package
directory. Do not create or consume direct briefs under the shared task root.

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
   retain the applicable direction decisions beside outcome and authority;
   a separate direction trace is not required. When a technical
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
     established, return the direction-delta-needed form from `references/exceptional-output.md` in the
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
5. Identify finite material requirements in universal or lifecycle claims.
   Preserve every approved artifact family, legal publication prefix, exact
   cardinality, retry/recovery state, tamper case, and bounded cleanup state
   in acceptance or a precise authority reference. These values define the
   contract; their detailed proof belongs to verification design.
6. Define stable AC IDs with descriptive titles. Use prose for one cohesive
   condition and short flat bullets or a clear table for independent obligations.
   Include success, refusal, boundaries and unchanged state where required.
   For lifecycle work, retain the first legitimate state change and next real
   occurrence. Leave setup, assertions and implementation choices to their owners.
7. Record only necessary evidence boundaries or capability uncertainties in
   the brief. Risk notes are optional; use the content boundary below.
   Classify verification reasoning as `inline` for obvious tests and oracles,
   or `separate — <reason>` for non-obvious failure/lifecycle or finite cases.
   Either recommendation keeps required packaged preparation. Resolve ambiguous
   requirements with their owner before verification design.
8. Apply sizing, then load the applicable form from the table above and assemble
   the brief. Keep the four scalar launch keys `agent_tier`, `reasoning`,
   `review`, and `budget` for executable leaves only. Use authority-approved
   values as intended launch guidance, not observed runtime configuration.
   Treat the budget as a soft checkpoint unless authority makes it hard.
   Add only the high-assurance fields needed for that profile.

When `review: immediate`, cite the [shared submission route](../../README.md#submission-route)
in the brief. Retain local exceptions and gate ownership in their owning artifact.
A shared reference must preserve the route after implementation and corrections;
it cannot imply same-session self-review is independent acceptance.

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
After choosing a split, read [decomposition package](references/decomposition.md)
before writing any parent, child or structural index. Follow its complete child,
integration, coverage and structural-index contract.

4. A triggered task may remain one executable leaf when concrete coupling or
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

A risk section is optional. Include a consequential failure, invariant or
essential proof boundary only when it adds information needed to interpret or
safely execute the task. Do not require R IDs or six-field blocks in a brief.
Keep existing supplied risk IDs traceable without duplicating their requirements.

Acceptance or precise cited authority owns finite values and allowed transitions.
`verification.md` owns detailed scenario enumeration, fixtures, observations,
evidence reuse, distinct independent probes, and gate owner/stage allocation.
It derives these even when the brief has no risk rows. Do not reproduce that
matrix under a different heading. An unresolved observer capability still needs
its concise local uncertainty and preparation route.

The verification designer carries the testing defaults: fail-first where feasible,
lowest reliable level, real-boundary proof where required, targeted checks before
owning and justified broader gates, truthful skips, and separate implementation
and independent-review evidence. Preserve task-authority exceptions, including
final-reviewer aggregate ownership, by precise reference rather than repetition.

## Output contract

For a gap check, report only:

- whether the existing task is usable;
- concrete missing or contradictory items;
- the smallest proposed edits;
- which execution prerequisite remains and whether high-assurance preflight
  is warranted;
- whether verification design should stay inline or use a separate
  `task-verification-designer` pass, with the concrete reason when separate;
  and the shared submission-route reference when review is immediate.

For direction-delta-needed and `blocked_design` responses, use
[exceptional output](references/exceptional-output.md) before returning the
response. Direction gaps retain precedence and leave the task path unchanged.

For a durable executable brief, use `references/task-brief-template.md`. When governing
direction was supplied, preserve its exact applicable decisions in outcome or
authority without a mandatory separate trace. A new material direction decision
requires the direction-delta-needed response instead of a ready brief. Use one status:

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

Never update an official master plan merely to record completion of this
design task.

## Final read and ownership

Read the brief as a person unfamiliar with the design. They should be able to
explain the result, what completion proves versus enables, the governing rules,
and the pending execution prerequisite. Then check that compression preserved
each approved obligation, exception, stable ID, essential evidence boundary,
and handoff. Remove empty fields, repeated summaries and workflow recitations;
use no fixed word limit, section count or formatting quota.
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
