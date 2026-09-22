---
name: task-brief-designer
description: Create, tighten, or gap-check one bounded implementation task from a user request, issue, approved plan, specification, or existing brief. Use when asked to make work implementation-ready, define acceptance criteria and verification, estimate and recursively split oversized work into bounded child briefs, prepare an agent handoff, or repair a task contract. Prefer a lightweight delta over rewriting an adequate brief. Do not implement, certify current repository readiness, or invent unresolved product or architecture decisions.
---

# Task Brief Designer

Turn one bounded task into a clear, testable contract. Preserve useful existing
material and add only what the implementer or reviewer needs.

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
- Produce a compact `ready` brief when a durable artifact is useful. The
  routine readiness route is implementer self-preflight. Recommend standalone
  guided preflight only for a named material readiness uncertainty.

### High assurance

- Require exact authority, dependency, policy, and artifact paths.
- Use the full template and status `ready_for_preflight` or `blocked_design`.
- Design durable evidence, verification-capability disposition, and explicit
  downstream handoffs for separate preflight and acceptance stages.

Do not upgrade a routine task merely because a fuller template exists. If a
guided task discovers a genuine high-assurance need, name the reason and the
smallest additional artifact or decision required.

## Load flow policy

Before estimating a task that could become implementation-ready, read
`references/task-sizing.yaml` and use its active profile. The numeric thresholds
live there intentionally; do not copy them into this skill or silently replace
them with personal defaults.

Each configured maximum is exclusive: split only when the corresponding
estimate is greater than that maximum. An estimate equal to a maximum fits.

When creating or updating durable task artifacts, read
`references/task-artifact-layout.md`. Repository or user authority may choose a
different task-package root or directory name, but every durable task must keep
its `brief.md` and optional artifacts inside one dedicated package directory.
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
need focused discovery. Once `blocked_design` applies, use the abbreviated
blocked-design output and stop drafting: do not infer architecture,
implementation scope, acceptance criteria, finite cases, or verification from
an unapproved premise.

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
   Preserve adequate sections verbatim or by reference. Do not expand them for
   template completeness. If the task would need to introduce or change product
   behavior, priority, assurance, trust, intervention, or scope beyond supplied
   governing direction, return the plain-language direction-delta-needed form
   below and stop. For other material product or architecture gaps, switch to
   `blocked_design` and stop before the remaining drafting steps.
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
7. Map each material risk to the lowest reliable evidence. Use a public entry
   point or real boundary when pure/unit evidence cannot prove wiring,
   persistence, processes, filesystem behavior, database behavior,
   concurrency, permissions, or compatibility.
8. Name targeted and broader verification commands when authority or local
   precedent supplies them. In guided mode, focused command discovery may stay
   with the implementer. In high-assurance mode, unresolved required commands
   go to preflight and must not be presented as passing.
9. Add the task metadata block:

   ```yaml
   agent_tier: mechanical | standard | strong
   reasoning: low | medium | high
   review: mechanical | milestone | immediate
   budget: <tool calls> / <time> / <context>
   ```

   For executable leaves, choose this block after sizing. A composite parent
   uses status `decomposed` and does not carry launch metadata or a readiness
   route. Treat `agent_tier`, `reasoning`, and `review` as intended launch guidance
   for future automated or current manual routing, and use the values the task
   authority actually calls for. They are not claims about the eventual
   runtime configuration; do not claim to have observed a runtime reasoning
   setting unless it was supplied. Keep these four scalar keys and treat the
   budget as a soft checkpoint unless higher-priority instructions explicitly
   make it hard. When `review: immediate`, preserve implementation as the next
   action and add the ordered follow-on: immediately after implementation or
   correction, hand the completed bytes to a fresh independent acceptance
   reviewer. Apply this to surgical gap-checks as well as newly drafted briefs;
   a generic implementation next action or a review workflow loaded in the
   authoring or implementation session does not state independent acceptance.
10. Give every durable brief one human-readable readiness route:
    - `implementer self-preflight` for routine guided work;
    - `standalone guided preflight — <material uncertainty>` only when naming
      the concrete uncertainty that makes a separate readiness check useful; or
    - `high-assurance preflight` when the selected profile requires it.
    Do not add a route metadata key. Current repository facts may require the
    implementer or orchestrator to escalate the recommendation at execution
    time. A prerequisite feasibility/proof task from step 4 is a design
    dependency, not a readiness route.
11. Explicitly classify whether a separate `task-verification-designer` pass
    is recommended before implementation:
    - `inline` when the task is small and its decisive tests/oracles are
      obvious from the brief;
    - `separate — <reason>` when non-obvious negative/lifecycle semantics,
      finite material cases, boundary behavior, or multiple plausible-wrong
      implementations make a focused verification-design pass useful.
    This is a recommendation, not a mandatory stage. Do not recommend it merely
    because the skill exists, and do not use it to compensate for ambiguous
    requirements that should block or return to the decision owner.
12. Read `references/task-brief-template.md`. Use only the core sections for a
    guided brief; add the high-assurance sections only for that profile.

## Sizing and decomposition contract

Treat the execution estimate as a decomposition gate, not merely descriptive
metadata.

1. Estimate the candidate implementation task after its authority, outcome,
   scope, acceptance criteria, and decisive verification are clear. Estimate
   only the implementation-agent work: focused repository discovery, production
   edits, task-owned tests, and implementation verification. Exclude separate
   preflight, maintainability review, contract-registry synchronization,
   acceptance review, and orchestrator/controller work.
2. Record a numeric estimated agent-call count, numeric implementation duration
   in minutes, estimate confidence, and the intended `agent_tier` /
   `reasoning` pair. Then evaluate the active profile from
   `references/task-sizing.yaml`. A configured execution-profile trigger
   applies to the complete pair; for example, a `strong` + `high` rule means
   both values together, not either value independently. Numeric maxima trigger
   only when the estimate is greater than the maximum; equality fits.
3. When any active decomposition trigger matches, split by default. Prefer
   coherent behavioral, ownership, interface, state-transition, or artifact
   boundaries whose outputs can be consumed explicitly by later work. Do not
   split by arbitrary file halves, architectural layers, equal call counts, or
   a detached "write tests" task merely to force estimates below a threshold.
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
   explicit unsplittable override below applies.
7. If a parent-level acceptance criterion can only be proven after sibling work
   composes, create a final executable integration child that owns that proof
   and any required wiring. Do not invent a special composite-parent
   implementation or acceptance-review stage.
8. Use an unsplittable override only when the active sizing profile allows it
   and further decomposition would destroy a real atomic boundary or create
   coordination-only handoffs. The executable leaf must record
   `decomposition_override: cannot_split_safely`, the triggered limit(s), the
   concrete reason, and residual execution risk. Strong reasoning by itself is
   not evidence that a task is irreducible.
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
if its estimate triggers decomposition, replace the executable handoff with a
composite parent and bounded child briefs. Do not use the gap-check form to
avoid a triggered split.

## Finite-risk coverage contract

Use the optional finite-risk table only when step 5 finds at least one finite,
material dimension. Use exactly these six columns, in this table rather than
scattering their semantics across other sections:

- the invariant;
- the exact material dimensions or state transitions;
- the decisive observable oracle and real boundary;
- fail-first, targeted, or owning evidence the implementer must establish;
- a distinct independent-review probe, or `N/A` with a reason; and
- the gate owner and stage.

Rows may combine cases only when they share one invariant and oracle. The table
is a coverage contract, not a Cartesian-product requirement. Keep
implementation evidence separate from review corroboration; an implementer
self-check is not acceptance. For an immediate-review correction flow, state
whether the correction implementer or final fresh reviewer owns the broader or
aggregate gate. Keep targeted evidence first while it is red instead of
requiring the same broad gate after every failed review. Keep row identity
stable across corrections so later reviews can carry each row forward as
`pass`, `fail`, `blocked`, or `unchecked`; prior status is not proof for
corrected bytes.

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
- Assign each broader or aggregate gate to an owner and stage; do not silently
  duplicate it across correction and review.
- Record skipped stronger checks and residual risk without presenting them as
  passed evidence.

## Output contract

For a gap check, report only:

- whether the existing task is usable;
- concrete missing or contradictory items;
- the smallest proposed edits; and
- whether guided implementation may begin or high-assurance preflight is
  warranted;
- whether verification design should stay inline or use a separate
  `task-verification-designer` pass, with the concrete reason when separate;
  and
- when `review: immediate`, the ordered handoff from implementation or
  correction to fresh independent acceptance review immediately afterward.

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

Do not continue into task scope, acceptance criteria, launch metadata,
verification, or implementation handoff until the owner supplies the missing
direction. A technical recommendation is not governing authority.

For a durable brief, use `references/task-brief-template.md`. When governing
direction was supplied, include its `Direction trace` section and require
`New direction decisions required: None`; any other value requires the
direction-delta-needed response instead of a ready brief. Use one status:

- `ready`: an executable guided leaf may begin after its recommended readiness
  route is satisfied;
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

## Boundaries and routing

- Route current Git state, command resolution, dirty ownership, and current
  dependency checks to a compact implementer self-preflight or standalone
  `task-preflight`.
- Route unresolved feasibility that determines the implementation mechanism,
  scope, cross-platform enforcement, or shared verification infrastructure to
  a separate prerequisite evaluation/proof task and block the primary task on
  its result.
- Route missing product or architecture authority to its owner or the user.
- Route gaps in supplied product direction through the plain-language
  direction-delta-needed form rather than silently resolving them in a
  technical brief.
- Route wider scope or new shared infrastructure back through brief design.
- Do not implement, accept the result, launch subagents, or modify runtime
  orchestration state. The structural task index defined by the artifact layout
  is the only task-index write owned here when creating or decomposing durable
  briefs.

## Definition of done

- The task is independently understandable without this conversation.
- Every changed or added line in an existing brief closes a concrete gap.
- Outcome, scope, ACs, evidence, metadata, stops, readiness route, verification-
  design recommendation, and next action are clear.
- When direction is supplied, the contribution, user-observable effect or
  enabled outcome, sequencing reason, and approved decisions are traceable.
- Every ready brief with supplied governing direction says
  `New direction decisions required: None`; otherwise brief design stopped
  with a direction delta.
- Guided briefs avoid high-assurance artifact ceremony unless risk justifies it.
- Every executable leaf records sizing evidence and fits the active sizing
  profile or carries the allowed explicit unsplittable override.
- Every composite parent has complete child coverage, explicit dependencies,
  and no implementation handoff of its own.
- High-assurance briefs preserve exact stage and evidence contracts.


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
