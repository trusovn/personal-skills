# S3-T3: Integrate Tracker Finalization and Recovery

Status: conditional; ready after S3-T2 and S3-15
Depends on: S3-T2, S3-15
Blocks: tracker-enabled Stage 3 completion

## Outcome

Integrate the approved tracker adapter into the prepared acceptance operation
and finalization recovery. The task remains unaccepted until the exact tracker
update is proven and recorded; interruption is reconciled idempotently.

## Required context

Read:

- `docs/human-tracker-contract.md`
- the S3-T2 adapter and tests
- S3-11 acceptance, S3-14 commit, and S3-15 recovery code/tests
- the approved policy schema/record from S3-T1

## Entry criteria

- S3-T2 and S3-15 pass.
- The run policy explicitly selects the named adapter and exact path.
- Contract rules decide whether tracker change is outside the commit, inside the
  accepted path set, or a separately ordered controller effect.

## Allowed changes

- `scripts/controller.py`
- `scripts/controller_state.py`
- the named tracker adapter only for integration-contract defects
- controller/state/adapter tests

Do not support a second tracker format or change the approved effect ordering.

## Work

1. Persist exact tracker intent and pre-update digest in the prepared operation.
2. Execute it in the approved order relative to commit finalization.
3. Record before/after digests and exact mapped transition before acceptance.
4. Extend `recover` to recognize exact pre-effect, exact post-effect, and
   ambiguous/external states.
5. Continue or finalize idempotently only when operation evidence matches.
6. Stop without mutation on any lookalike or concurrent tracker change.

## Acceptance criteria

- **AC-01:** Tracker mode off still performs no tracker read/write beyond any
  validation already required by core records.
- **AC-02:** Enabled mode cannot update a path/record absent from persisted
  authority.
- **AC-03:** Acceptance occurs only after exact tracker evidence is recorded.
- **AC-04:** Fault injection before/after tracker write recovers exactly once or
  stops without an additional write.
- **AC-05:** Commit/tracker ordering matches S3-T1 and preserves exact-path
  commit invariants.
- **AC-06:** External tracker mutation is never overwritten or mistaken for the
  intended effect.

## Verification

Run one post-write/pre-record crash case first, then the tracker finalization
fault matrix, owning adapter tests, and aggregate task-orchestrator suite.
Finish with `git diff --check`.

## Exit and handoff

Report effect ordering, recovery states, and exact policy authority. Update the
Stage 3 handoff only if tracker-enabled mode was actually verified.
