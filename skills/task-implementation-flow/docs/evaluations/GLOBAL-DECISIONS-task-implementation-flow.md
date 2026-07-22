# Global decisions: task implementation flow after the 2026-07-21 evaluation

Status: `decisions_required`

This document contains only choices and integration work that cannot be owned
cleanly by one of the four skill-specific implementation briefs. It is
self-contained; a decision owner should not need to reread the evaluation or
this conversation.

## Critical read

The central recommendation is sound: keep independent acceptance review and
reduce repeated discovery with finite risk matrices, invariant-level
correction, targeted reviewer probes, and one final broad gate.

The strongest upside is deterministic scaffolding for medium-reasoning agents.
The evidence shows that requirements were often already present but did not
become a bounded case ledger.

The main failure risks in the proposed redesign are:

1. A matrix can become generic test ceremony. Expand only explicit finite and
   material cases; never promise exhaustive bug discovery.
2. Reviewer-written tests blur ownership. An allowed test path is not write
   permission, and the writing reviewer cannot later accept corrected bytes.
3. Richer metadata can remain decorative. No repository consumer of
   `agent_tier`, `reasoning`, or `review` was found beyond Markdown examples and
   skill guidance.
4. The economic claim is not yet proven. The observed sessions have no
   controlled no-preflight, revised-skill, or higher-reasoning-reviewer
   comparison.
5. Four agents editing the shared README would create coordination cost and
   conflict risk. Treat README integration as one final owned change after the
   four skill sources stabilize.

## Decision summary

| ID | Decision | Recommended resolution | Blocks |
|---|---|---|---|
| G-01 | Meaning and shape of launch metadata | Keep the current four-key schema for now; define values as truthful intended launch guidance, use medium when medium is intended, and do not add nested fields until a named launcher consumes them | Metadata portion of `task-brief-designer`; shared README |
| G-02 | Reviewer tests-only write authority | First release requires explicit current user/review-invocation authorization plus an exact allowed test path; task scope and `review: immediate` are insufficient | Tests-only portion of `task-acceptance-review`; shared README |
| G-03 | Standalone preflight's default place | Adopt implementer self-preflight for routine guided work; keep standalone preflight for material readiness uncertainty and all required high-assurance flows | Shared README only; skill-local value reporting can proceed |
| G-04 | One-pass review ambition | Require completeness against explicit finite rows and selected material invariants, with visible unchecked areas; do not promise all latent bugs | Shared README only; reviewer skill-local work can proceed |
| G-05 | Reviewer production repair | Keep it out of the default flow; any future bounded repair mode is a separate experiment and never self-accepts | Nothing in the four current briefs; prevents scope creep |
| G-06 | Comparative live evaluation | Defer until revised skills and fixtures are frozen; require explicit cost/live-model authorization and immutable baseline/revised snapshots | Claims of improved effectiveness or economy, not skill-text implementation |

## G-01 — reasoning and agent metadata

### Problem

S3-06, S3-07, and S3-08 declared:

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 30 tool calls / 90 minutes / 100k context
```

The observed implementation and review sessions used medium reasoning. Neither
preflight nor the skills flagged the mismatch. The current repository contains
Markdown producers/examples but no launcher that is visibly enforcing these
fields.

### Options considered

1. Split execution and review into nested launch blocks. This expresses the
   long-term strategy but is a schema migration with no current consumer.
2. Keep the four-key block and define it as intended launch guidance. This is
   compatible and makes current briefs truthful if authors choose medium when
   medium is intended.
3. Remove `agent_tier` and `reasoning` until a launcher consumes them. This is
   honest but discards useful human routing guidance.

### Recommended resolution

Choose option 2 now:

- `agent_tier` and `reasoning` are intended launch guidance, not claims about
  the actual current session.
- Task authors must choose the economical setting they actually intend; do not
  write high as a generic signal that a task is important.
- `review: immediate` means an immediate handoff to a fresh reviewer, never an
  instruction for the implementer to self-review.
- If a launcher receives both intended and actual configuration, that launcher
  owns mismatch enforcement. None of these four conversational skills should
  pretend it can inspect hidden launch settings.
- Revisit separate execution/review fields only when a named launcher will
  parse and enforce them in the same authorized change.

This is deliberately more conservative than immediately adopting nested
metadata. It fixes the observed false guidance without building an unused
schema.

Approval needed: **yes**. Until approved, the metadata subtask in
`IMPLEMENTATION-BRIEF-task-brief-designer.md` remains blocked.

## G-02 — reviewer-created failing tests

### Problem

Reviewer-authored regressions were effective executable handoffs, but the
current skill is read-only and the writes occurred only after follow-up user
instructions. Making them implicit would create dirty-worktree and role
confusion.

### Options considered

1. Explicit authorization in the current user/review invocation.
2. A new durable task metadata field.
3. Keep review strictly read-only.
4. Allow production repair and acceptance in one review session.

Option 4 is rejected. It recreates the same-authorship acceptance failure. A
future non-accepting production-repair experiment is covered by `G-05`, not
this change.

### Recommended resolution

Choose option 1 for the first release:

- The user or exact review invocation must explicitly authorize
  `tests_only_reproducer`.
- The task/review input must name the owning test path or an exact allowed test
  area. Scope alone does not grant writes.
- The reviewer fixes `CHANGES_REQUESTED` before writing, changes only authorized
  test files, proves the focused intended failure, reports status/diff side
  effects, and never stages or commits.
- Production code, dependencies, plan/task/result/tracker files, and shared
  harnesses remain unchanged.
- Correction is followed by a fresh review; the writing reviewer cannot accept
  the corrected bytes.

Defer a metadata flag until repeated use proves that automation needs it and a
consumer/precedence contract is identified.

Approval needed: **yes**. Until approved, the tests-only subtask in
`IMPLEMENTATION-BRIEF-task-acceptance-review.md` remains blocked.

## G-03 — standalone preflight

### Recommended resolution

Adopt the evaluation's recommendation:

- Routine guided work uses the implementer's compact self-preflight.
- Standalone guided preflight remains separately invocable and is used when
  dirty ownership, dependencies, environment, permission, helper/capability,
  command/oracle resolution, or durable handoff uncertainty is material.
- High-assurance/orchestrated flows keep standalone preflight.
- A directly requested but routine preflight still returns a compact truthful
  readiness result and labels its incremental value marginal; it does not
  refuse the request.

This decision is reversible and does not delete capability. It changes default
flow documentation and evaluation criteria, not high-assurance safety.

Approval needed: **yes for shared-flow documentation**. The skill-local
classification and compact-output changes are safe to implement before that
approval because they do not remove standalone availability.

## G-04 — bounded completeness in review

### Recommended resolution

Adopt the bounded contract:

- A reviewer accounts for every explicit finite task row and each selected
  material risk dimension.
- It continues after a finding only when remaining probes are independent,
  safe, authorized, and affordable.
- It reports unchecked areas and stop reasons.
- It never promises to find every latent defect or perform generic fuzzing and
  repository archaeology.

This is the key safeguard against both one-finding-at-a-time review and an
unbounded “be more thorough” prompt.

Approval needed: **yes for shared-flow wording**. The reviewer and brief skill
changes may implement this contract directly because it is bounded by existing
authority.

## G-05 — reviewer production repair

### Recommended resolution

Do not add it in this change set.

A one-line diff is not necessarily trivial when it crosses persistence,
concurrency, recovery, public schema, or compatibility boundaries. If a future
experiment is desired, it must be explicitly opt-in, limited to an
authority-determined local correction, return a non-accepting result such as
`CHANGES_APPLIED_REVIEW_REQUIRED`, and require a fresh reviewer. It needs its
own fixture and cost comparison.

Approval needed: **no** to defer it. Any attempt to add it now is scope
expansion and must stop.

## G-06 — comparative evaluation and reasoning experiment

### Problem

The existing sessions show absolute cost and defects but do not isolate the
effect of revised skills, standalone preflight, or reasoning level. A broad live
benchmark can also be expensive and noisy.

### Recommended design

After all four skill changes, mirrors, fixtures, and shared README are frozen:

1. Preserve immutable baseline and revised skill snapshots.
2. Run at least two fresh fixtures/snapshots under the same medium reasoning and
   permission envelope:
   - current/baseline skills;
   - revised skills.
3. Measure material defects after initial implementation, defects reported in
   the first review, independent review rounds to `ACCEPT`, fresh-session count,
   tool calls, uncached/cached input, output, quota delta, broad-suite runs,
   false findings, and unnecessary test changes.
4. Only then consider a third configuration with a higher-reasoning reviewer.

Use deterministic local fixtures and identical task authority. Do not compare
different repository states or count schema/syntax checks as behavioral
success. Report variance and avoid inferring savings from one run.

Approval needed: **yes**, immediately before any paid/live model execution.
This benchmark is not a completion condition for the four skill-text tasks, but
no claim that the revised flow is cheaper or equally effective is justified
without it.

## Shared README integration task

One owner should update `skills/task-implementation-flow/README.md` only after
the four skill-specific changes are accepted and `G-01` through `G-04` are
resolved. Do not split this shared-file edit across the four implementation
agents.

Required README changes:

1. Define independence as non-authorship of reviewed production bytes in the
   current session; loading another skill does not reset provenance.
2. Change the guided diagram to show implementer self-preflight by default and
   an explicit fresh-session review handoff when review is required.
3. Add the material standalone-preflight criteria from `G-03`.
4. Document gate ownership:
   - initial implementer: fail-first, targeted, owning, justified broad gate;
   - failed discovery review: adversarial probes, no broad gate after decisive
     failure;
   - correction implementer: reviewer regressions plus owning suite;
   - fresh final reviewer: clean adversarial rows plus one justified aggregate
     gate.
5. Explain that a self-check may find and fix issues but cannot issue a verdict.
6. If `G-02` is approved, document the opt-in tests-only reproducer protocol
   and mandatory fresh review.
7. Reflect the final `G-01` metadata semantics exactly; do not publish a nested
   example unless a named consumer supports it.

The README already contained user changes when these documents were created.
The integration owner must inspect and preserve them rather than replacing the
file wholesale.

## Source mirror and integration order

The canonical sources are under `skills/task-implementation-flow/`; active
copies are under `.agents/skills/`. They were byte-identical when these briefs
were written. The relevant repository README says to edit and validate sources
before redistribution, but no exact sync/install command was found.

Use this order:

1. Approve or revise `G-01` and `G-02`; record `G-03` and `G-04` for README
   integration.
2. Implement and independently review each canonical skill task.
3. Resolve and use the repository-approved mirror process; prove byte identity.
4. Assign one owner to the shared README integration task and review it against
   all four accepted skills.
5. Run cheap structural and fixture checks.
6. Run focused behavioral skill evals only with the required live-model/cost
   authorization.
7. Decide separately whether to authorize the comparative benchmark in `G-06`.

Stop if the canonical/mirror process is unavailable, if shared README ownership
is unclear, or if a decision is being encoded differently in two skills.

## Decision record to complete

Before implementation of blocked portions, replace `PENDING` below with the
decision owner's explicit choices. Do not treat recommendations as approval.

| ID | Decision | Owner | State |
|---|---|---|---|
| G-01 | `PENDING` | User / flow owner | unresolved |
| G-02 | `PENDING` | User / flow owner | unresolved |
| G-03 | `PENDING` | User / flow owner | unresolved for shared docs |
| G-04 | `PENDING` | User / flow owner | unresolved for shared docs |
| G-05 | Defer production repair | Flow owner | recommended default |
| G-06 | `PENDING` until benchmark authorization | User / budget owner | deferred |

## Resolution notes — 2026-07-23

These notes record the flow owner's decisions without rewriting the preceding
evaluation-time record. They supersede the `PENDING` states above for future
implementation.

| ID | Resolution | State |
|---|---|---|
| G-01 | Approve the recommended four-key schema. `agent_tier`, `reasoning`, and `review` are intended launch guidance for future automated or manual routing; `budget` remains a soft checkpoint unless explicitly made hard. Keep the current scalar fields and add no nested execution/review schema until a named launcher consumes and enforces it. | resolved |
| G-02 | Approve explicit current-invocation authorization for `tests_only_reproducer`, together with an exact writable test path or area. Keep the mode in `task-acceptance-review` so it can reuse the reviewer's demonstrated trigger and invariant, but place its conditional procedure in a focused reference loaded only after `CHANGES_REQUESTED` is fixed. The reviewer must not switch into production implementation or accept corrected bytes. | resolved |
| G-03 | Approve implementer self-preflight as the routine guided default and standalone preflight for material readiness uncertainty or required high-assurance work. `task-brief-designer` should recommend a human-readable readiness route per task, with a concrete reason when standalone preflight is recommended. Do not add a machine metadata field yet; a future orchestrator owns parsing, precedence, and current-state override rules. | resolved |
| G-04 | Approve bounded completeness and require a transferable coverage ledger across review rounds. Every explicit finite row and selected material invariant must end `pass`, `fail`, `blocked`, or `unchecked` with a reason. Review continues while remaining probes are independent, safe, authorized, and affordable; any earlier stop carries the remaining rows forward. Previous passes guide the next review but are not acceptance evidence for corrected bytes. | resolved |
| G-05 | Defer reviewer production repair. Any later experiment remains separately authorized, non-accepting, and outside the four current skill tasks. | resolved by deferral |
| G-06 | Approve the comparative benchmark design, but do not authorize live or paid execution yet. Execution remains deferred until revised skills and fixtures are frozen and the user gives explicit cost/model authorization. | design resolved; execution deferred |

### Acceptance-review task shape

Keep the acceptance-review change as one implementation task. A formal split
would add an implementation and review handoff while losing some of the
reviewer's useful reproducer context. Isolate the optional write behavior
instead through a conditional `tests-only-reproducer` reference and its own
fixture. The implementation may use an internal checkpoint between the
read-only completeness work and the opt-in reproducer work, but it receives one
fresh acceptance review as a coherent skill change.

### Review continuation contract

A fresh reviewer receives the authoritative brief, current scoped diff,
preceding verdict and complete coverage ledger, reviewer-created regressions
and commands, the broad-gate decision, and every unchecked or previously
blocked row. The correction implementer preserves this handoff and reports its
own correction evidence separately; it does not promote prior reviewer passes
or unchecked rows.

The final reviewer must establish its verdict against the current corrected
bytes. A future orchestrator should persist and transfer this compact state
rather than reviewer transcripts. The exact machine schema and invalidation
rules are intentionally deferred until that orchestrator has a named consuming
interface.

### Common integration work still to resolve

The global product decisions no longer block the four briefs. These shared
execution facts remain:

1. The repository-approved canonical-to-`.agents/skills` distribution process
   is still undocumented. Each implementation must stop before mirror writes
   until the owner supplies or approves that process.
2. The focused live skill-eval runner is still unresolved. Deterministic
   fixture behavior and structural checks may proceed, but they do not prove
   revised skill behavior; any paid/live run still needs explicit approval.
3. One owner must perform the shared README integration after all four
   canonical skill changes are independently accepted. That change must also
   document per-task readiness routing and transfer of the review coverage
   ledger.
4. Machine consumption of readiness routes and review-continuation state is a
   later orchestrator contract. The current skills should emit stable,
   human-readable handoffs without inventing an unconsumed schema.
