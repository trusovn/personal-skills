# S3-10: Implement Same-Thread Resume

Status: ready after S3-09
Depends on: S3-09
Blocks: S3-11

## Outcome

Add controller-owned same-thread resume for a `resumable` task. Resume appends
one immutable turn within the existing attempt, preserves all earlier evidence,
and reapplies the original persisted authority.

## Required context

Read:

- `docs/stage-3-plan.md` — resume/fresh-retry decision
- `docs/controller-contract.md` — lifecycle and transport boundary
- `scripts/controller.py`, `controller_state.py`, `codex_worker.py`
- recovery and resume tests in both owning suites

## Entry criteria

- S3-09 recovery tests pass.
- The task is `resumable`, the run has no active worker, process absence is
  proven, and a thread ID exists.
- Original policy, task, attempt, prompt, and baseline records validate.

## Allowed changes

- `scripts/controller.py`
- `scripts/controller_state.py`
- `scripts/codex_worker.py` only for a state-checked append-only resume defect
- `tests/test_controller.py`
- `tests/test_controller_state.py`
- `tests/test_codex_worker.py`

Do not add a fresh-retry command or change scope/permission authority.

## Work

1. Add `resume --run-dir ... --prompt-file ... --timeout-seconds ...` valid only
   for the current resumable task/attempt.
2. Treat prompt-file content as clarification, not authority. Render a bounded
   controller prompt that restates immutable task, paths, checks, permissions,
   commit prohibition, and recorded question/failure context.
3. Preflight the exact resume command before ledger mutation or turn creation.
4. Atomically move run/task to `running`, set active attempt, and invoke the
   recorded thread through the adapter.
5. Append `turn-NNN` prompt/events/stderr/result/state artifacts exclusively.
6. Preserve all earlier attempt/turn bytes and bind the new prompt/turn to the
   same policy, manifest, baseline, and scope.
7. Route the terminal outcome through S3-09 reconciliation rules.

## Acceptance criteria

- **AC-01:** Any non-resumable state, live/ambiguous PID, missing thread, or
  identity mismatch is denied without mutation.
- **AC-02:** Exact preflight failure creates no turn and leaves ledger bytes
  unchanged.
- **AC-03:** Resume invokes the recorded thread ID, not a new start.
- **AC-04:** Earlier turn bytes/digests remain unchanged; the next turn number is
  monotonic and exclusive.
- **AC-05:** Clarification text cannot change task ID, allowed paths, checks,
  permissions, commit mode, or tracker mode in controller records/prompt.
- **AC-06:** A fake resume can return to `awaiting_inspection` or a mapped
  resumable/stopped outcome without acceptance.

## Verification

Run one live-process denial test, then focused controller resume tests and the
worker resume module. Finish with the aggregate suite and `git diff --check`.

## Exit and handoff

Report the turn artifacts added and authority fields proven unchanged. Stop
before implementing fresh retry or acceptance.
