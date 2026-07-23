# S3-11: Prepare Acceptance with Side Effects Off

Status: ready after S3-08, S3-09, and S3-10
Depends on: S3-08, S3-09, S3-10
Blocks: S3-12

## Outcome

Add `accept` for a current accepting decision and implement the prepared
operation protocol with human tracker off and commit mode off. The operation is
journaled before any final acceptance ledger change and is the sole authority
for finalization. This task does not mark the task accepted.

## Required context

Read:

- `docs/stage-3-plan.md` — acceptance authority and durable operation
- `docs/controller-contract.md` — closure gate
- `scripts/controller.py`, `controller_state.py`, `controller_git.py`
- inspect/decision tests from S3-08

## Entry criteria

- S3-08 decision and S3-09/S3-10 recovery suites pass.
- Current run/task are `awaiting_inspection` with an immutable decision that
  explicitly offers `accept`.
- Policy has tracker mode off and commit mode off for this task's scenarios.

## Allowed changes

- `scripts/controller.py`
- `scripts/controller_state.py`
- `scripts/controller_git.py` only for the cheap current-identity comparison
- `tests/test_controller.py`
- `tests/test_controller_state.py`

Do not create commits, update a human tracker, or release dependencies.

## Work

1. Add `accept --run-dir ...` with no task/path/check/commit/tracker arguments.
2. Revalidate every persisted input, artifact digest, and identity.
3. Re-run the cheap HEAD/index/status comparison and require it to match the
   accepting decision.
4. Re-evaluate all mechanical blockers: questions, risks, unexpected paths,
   changed pre-existing work, failed checks, and unauthorized gaps.
5. Exclusively create `operations/<task>-accept.json` in `prepared` state with
   expected old identities, exact accepted paths, tracker intent `off`, and
   commit intent `off`.
6. Atomically move the run to `finalizing` without accepting the task.
7. With both optional side effects off, atomically record that all authorized
   side effects are complete while leaving the run `finalizing` and the task
   `awaiting_inspection`. S3-12 owns the one acceptance/readiness ledger write.

## Acceptance criteria

- **AC-01:** Caller-supplied authority is impossible through the CLI.
- **AC-02:** Stale/tampered evidence or Git drift creates no operation and does
  not mutate the ledger.
- **AC-03:** The operation is durable in `prepared` state before any acceptance
  ledger write.
- **AC-04:** A prepared operation never marks the task accepted by itself.
- **AC-05:** Mode off creates no tracker or Git history side effect.
- **AC-06:** No task becomes accepted in this slice; the only valid intermediate
  state is a `finalizing` run with an effects-complete operation.
- **AC-07:** Repeated accept cannot create another operation or replay a stale
  decision.

## Verification

Run one stale-decision denial test first, then acceptance integration tests and
the owning state module. Finish with the aggregate suite and `git diff --check`.

## Exit and handoff

Report operation states and the exact ledger write order. The run must remain
`finalizing`, with the selected task unaccepted, until S3-12.
