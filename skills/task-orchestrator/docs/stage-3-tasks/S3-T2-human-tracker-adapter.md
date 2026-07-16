# S3-T2: Implement the Approved Human-Tracker Adapter

Status: conditional; ready only after S3-T1
Depends on: S3-T1
Blocks: S3-T3

## Outcome

Implement the single named tracker adapter from
`docs/human-tracker-contract.md` as an isolated, deterministic boundary. It
validates and atomically changes exactly one task record but does not wire
controller acceptance or recovery.

## Required context

Read:

- `docs/human-tracker-contract.md`
- the concrete tracker fixture/format authority named there
- `scripts/controller_state.py` — operation identity/digest conventions
- local repository instructions for the tracker path

Do not read or implement any format not named by the contract.

## Entry criteria

- S3-T1 has no unresolved field and records explicit user approval.
- The exact before/after fixture and path containment rule exist.
- Core Stage 3 tests pass before adapter work.

## Allowed changes

- one narrowly named tracker adapter under `scripts/`
- one matching focused test module and small fixtures
- no controller wiring

Exact filenames must follow S3-T1. Do not create a generic tracker abstraction.

## Work

1. Validate adapter version, canonical path, pre-update digest, task mapping,
   unique task ID, and expected old state.
2. Compute the exact one-record update in memory.
3. Reject unrelated data/formatting changes.
4. Write atomically and return before/after digests plus exact changed record.
5. Treat the exact already-applied update as idempotent only when all contract
   evidence matches.
6. On any mismatch, leave bytes unchanged.

## Acceptance criteria

- **AC-01:** The approved happy-path fixture changes exactly one mapped record.
- **AC-02:** Wrong/duplicate/missing task IDs, wrong old state, digest mismatch,
  path mismatch, malformed format, and concurrent replacement fail unchanged.
- **AC-03:** Exact replay is idempotent; lookalike state is not.
- **AC-04:** Atomic-write interruption leaves either complete old or complete
  new content, never a partial file.
- **AC-05:** No ledger, Git commit, worker, or acceptance side effect occurs.

## Verification

Run one digest-mismatch/no-write test first, then the adapter module. Finish with
the aggregate task-orchestrator suite and `git diff --check`.

## Exit and handoff

Report the adapter API, exact file mutation, and idempotency oracle. Stop before
calling it from `accept` or `recover`.
