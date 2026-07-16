# S3-08: Implement Inspection and Closure Decisions

Status: ready after S3-03 and S3-07
Depends on: S3-03, S3-07
Blocks: S3-11

## Outcome

Add `controller.py inspect` for a run in `awaiting_inspection`. It revalidates
the Stage 2 closure, runs independent verification, detects verification-created
repository drift, and atomically publishes immutable verification and decision
records. It performs no acceptance side effect.

## Required context

Read:

- `docs/stage-3-plan.md` — records, authority, stop conditions
- `docs/controller-contract.md` — closure gate
- `scripts/controller.py`, `controller_state.py`, `controller_git.py`, and
  `verification_runner.py`
- focused tests for those modules

## Entry criteria

- S3-03 and S3-07 suites pass.
- A Stage 2 fake run can reach `awaiting_inspection` with immutable closure
  evidence.
- No live/ambiguous worker is recorded.

## Allowed changes

- `scripts/controller.py`
- `scripts/controller_state.py` only for task-local decision wiring defects
- `scripts/controller_git.py` only for task-local observation support
- `tests/test_controller.py`
- owning focused tests only when their boundary contract changes

Do not add acceptance, resume, tracker, commit, or next-task behavior.

## Work

1. Add `inspect --run-dir ... --timeout-seconds <positive>` valid only from
   `awaiting_inspection`.
2. Validate ledger and persisted policy/manifest/baseline/closure digests.
3. Validate adapter terminal state and worker result as claims.
4. Re-capture HEAD/index/status/content identities and require no drift from the
   Stage 2 closure before verification starts.
5. Derive the S3-06 plan and run it through S3-07.
6. Capture post-verification Git evidence; any created/changed path, HEAD, or
   index identity is a closure violation.
7. Exclusively publish `verification/<attempt>.json` and
   `decisions/<attempt>.json` with exact identity/digest binding.
8. Offer only mechanically valid actions among `accept`, `resume`, and `stop`.
   Record `semantic_review: not_collected`.
9. Update ledger references atomically without accepting the task.

## Acceptance criteria

- **AC-01:** `inspect` rejects every state except `awaiting_inspection` without
  mutation.
- **AC-02:** Stale or tampered Stage 2 evidence prevents command execution and
  record publication.
- **AC-03:** Worker-claimed passing checks cannot substitute for controller
  verification.
- **AC-04:** Failed/timeout checks, unexpected paths, pre-existing dirty-path
  changes, HEAD/index drift, questions, or unresolved risks prevent `accept`.
- **AC-05:** A verification-created tracked or untracked change is recorded and
  prevents `accept`.
- **AC-06:** An exact authorized repository-gate gap is recorded but never
  converts a failed targeted check.
- **AC-07:** Decision identity includes the verification digest and matches the
  current closure identity.
- **AC-08:** Re-running inspect cannot overwrite or create a contradictory
  decision.
- **AC-09:** No ledger task state becomes `accepted` in this task.

## Verification

Run one stale-evidence denial test, then the inspect integration tests and the
owning module suites. Finish with the aggregate suite and `git diff --check`.

## Exit and handoff

Report each denial reason tested and the decision action matrix. Stop before
implementing any action returned by the decision.
