# S3-09: Reconcile Running Attempts and Stop Safely

Status: ready after S3-04 and S3-05
Depends on: S3-04, S3-05
Blocks: S3-10, S3-11

## Outcome

Add running-attempt recovery and an explicit safe `stop` action. Recovery must
prove process ownership/absence, reconcile durable adapter artifacts, and move
the run/task only to a state allowed by persisted policy. It never launches or
resumes a worker.

## Required context

Read:

- `docs/controller-contract.md` — process and task outcomes
- `docs/stage-3-plan.md` — recovery constraints
- `scripts/controller.py`, `controller_state.py`, `controller_git.py`
- `scripts/codex_worker.py` — liveness, terminal state, cleanup
- process/recovery tests in controller and worker suites

## Entry criteria

- S3-04/S3-05 focused tests pass.
- Stage 2 records process identity, adapter state, thread ID, and terminal
  artifacts durably.

## Allowed changes

- `scripts/controller.py`
- `scripts/controller_state.py`
- `scripts/controller_git.py` only to reuse Stage 2 closure publication
- `tests/test_controller.py`
- `tests/test_controller_state.py`

Do not implement resume, acceptance, finalizing-state recovery, or commits.

## Work

1. Add `recover --run-dir ...` for `running` only in this slice.
2. Validate PID type plus recorded ownership. Treat permission errors, reused
   PIDs, incomplete identity, and contradictory state as ambiguous.
3. Refuse recovery mutation while an owned worker is alive or identity is
   ambiguous.
4. When the process is absent, reconcile adapter state and immutable artifacts.
5. Map `complete` to `awaiting_inspection` only after a valid Stage 2 closure is
   present or can be deterministically published from existing evidence.
6. Map `needs_input` and `blocked` to `resumable` only with a thread ID and an
   escalation policy; otherwise stop. Map `timed_out`/`interrupted` to
   `resumable` only with a thread ID. Map `failed`, `missing_result`, and
   `failed_to_start` to `stopped`.
7. Add `stop`; if a specifically owned process is live, terminate/reap it and
   persist one terminal outcome before stopping. Never signal an ambiguous PID.

## Acceptance criteria

- **AC-01:** Alive or ambiguous ownership leaves ledger bytes unchanged and
  prevents recovery/resume eligibility.
- **AC-02:** Absent-process outcomes follow the exact mapping above.
- **AC-03:** `complete` never becomes accepted and cannot reach inspection
  without complete Stage 2 evidence.
- **AC-04:** Stop of a live owned process uses bounded cleanup and leaves no
  child process.
- **AC-05:** Ambiguous stop performs no signal or ledger mutation.
- **AC-06:** Re-running recovery after a completed reconciliation is
  idempotent or returns a no-op result; it does not duplicate artifacts.

## Verification

Run one alive-PID denial test first, then the local-process recovery class and
owning controller module. Use events/bounded polling, not sleeps. Finish with
the aggregate suite and `git diff --check`.

## Exit and handoff

Report the terminal-outcome mapping and process-ownership oracle. Stop before
calling `codex_worker.py resume`.
