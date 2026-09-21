# Project Plan Verification Checklist

Use this as a compact cross-check after the semantic review. Do not substitute it for reconstructing the system flow.

## Scope
- [ ] Approved capabilities are present.
- [ ] No material unapproved scope was introduced.
- [ ] Non-goals remain excluded.
- [ ] Foundation constraints remain intact.

## Flows
- [ ] Every critical journey has trigger and terminal observable outcome.
- [ ] Steps identify meaningful consumed/produced artifacts.
- [ ] Crossed interfaces are named.
- [ ] State transitions are explicit where material.
- [ ] Important rejection/failure/stale branches terminate in defined state.

## Artifacts/state
- [ ] Every consumed artifact has a producer/source.
- [ ] Every durable produced artifact has a consumer or intentional historical role.
- [ ] Source of truth is unambiguous.
- [ ] Mutation authority is clear.
- [ ] Invalidation/supersession is defined for derived/version-sensitive state.

## Interfaces
- [ ] Owner and consumer are clear.
- [ ] Inputs/outputs are clear.
- [ ] Success semantics are clear.
- [ ] Important rejection/error semantics are clear.
- [ ] Auth/idempotency/concurrency/version rules are explicit when material.

## Invariants
- [ ] Cross-task rules have stable IDs or equivalent explicit anchors.
- [ ] Each critical invariant maps to owning tasks.
- [ ] Each critical invariant has intended verification evidence.

## Tasks
- [ ] Every task maps to a capability/flow.
- [ ] Dependencies are sufficient and acyclic.
- [ ] Inputs exist before task execution.
- [ ] Outputs have downstream value.
- [ ] Integration boundary is observable.
- [ ] Task-planner context preserves cross-task nuance.
- [ ] Task does not depend on an unresolved system-level decision.

## Verification
- [ ] Critical flows can be proven end to end.
- [ ] Real-boundary risks have appropriate integration evidence.
- [ ] AI model quality uses evals only when quality is an acceptance dimension.
- [ ] Deterministic business correctness does not depend on live AI calls.

## Abstraction
- [ ] Plan is not merely a feature/task list.
- [ ] Plan does not force local implementation details without cross-task need.
- [ ] Strong reasoning agents can infer local details without guessing system semantics.
