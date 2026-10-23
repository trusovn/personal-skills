# T-002.2 correction handoff — F-01

Active assignments now have to agree with current ledger authority before status
or replay exposes them. Terminal assignments keep their historical identity.
This is implementation evidence; corrected bytes still need independent review.

Implemented: READY_FOR_REVIEW

- Authority: `skills/task-orchestrator/docs/tasks/T-002.2/brief.md`, revision 1.
- Preflight/context reference: this package's `preflight.md` (including Decision
  context), `verification.md` revision 1, parent `../T-002/brief.md`, and
  `../../local-harness-orchestration-plan.md`. Authority, dependencies,
  permissions and verification scope are unchanged. Project-local installed
  bounded-task-implementer and testing-discipline guided this correction.
- Preceding verdict: none. `reviews/discovery-01.md` publishes evidence only;
  its sole finding is F-01, suggested P2. `reviews/maintainability-01.md` accepted
  the earlier bytes for maintainability; it is not current correction evidence.
- Finding/scenario IDs: F-01; V-01, V-02, V-03, V-04, V-05; R1, R2, R3.
- Complete findings and invariant: F-01 allowed an active assignment to disagree
  with current flow revision, candidate, stage or parent lifecycle. An active
  operation must match the run/task/stage/input/policy/flow/candidate identity
  and cannot survive under a stopped parent. The validator now compares flow
  revision and candidate alongside the three existing authority digests, matches
  selected task and current stage, and permits active ownership only in `ready`,
  `running`, `awaiting_inspection` or `resumable`. Existing operation/run identity,
  role, ordering, pointer and count checks remain in force. Terminal history is
  exempt from current-authority matching.
- Influenced sibling surfaces: regressions cover all six reservable stages
  (`preflight`, `implement`, `correction`, `verify`, `semantic_review`,
  `acceptance`) in each active state (`reserved`, `running`, `unknown`). They
  check valid status/replay, then wrong input/policy/flow digest, flow revision,
  candidate, cursor, missing selected task, and initialized/finalizing/stopped
  parents. Invalid status raises; reserve refuses with
  `authority_or_lock_unavailable`; run/task bytes remain unchanged. A separate
  case preserves terminal-history status and exact original-assignment replay
  despite different historical authority. Successor admission remains labelled
  fixture setup, not a production-admission claim.
- Attempts and discarded hypotheses: the new active-assignment method first
  failed with 84 subtest failures in 3.234 seconds, confirming F-01 and siblings.
  After the validator change, both new methods passed in 5.400 seconds. The
  first owning controller run had 86 passing tests and one fixture error: an
  unknown preflight actor had an implementation cursor. Setting that fixture's
  current step to preflight preserves its nonterminal-readiness rejection
  purpose. No production workaround or discarded implementation remains.
- Current scoped diff: unstaged changes to
  `skills/task-orchestrator/scripts/controller_state.py` (shared validation),
  `skills/task-orchestrator/tests/test_controller.py` (two regressions and one
  fixture correction), plus this new report. All pre-existing staged bytes and
  review reports are preserved. HEAD remains
  `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`. Corrected worktree Git blobs:
  state `a27b1367fe7370ee64defc78653c4a6bd88dd49b`, controller tests
  `cd8ff075f2b976f38d5bf7cdea4f1ef741ae6504`.

## Complete coverage ledger

All commands run from the repository root without network, models or sbx.
The reviewer row statuses below remain historical; only a fresh reviewer can
assign statuses to corrected bytes.

| Row | Prior discovery status | Correction implementation evidence | Incomplete reason / next owner |
|---|---|---|---|
| V-01 / AC-01 | fail, F-01 | New active-assignment regression rejects contradictory public status; existing read-only/evidence-distinction case passes in the final controller suite. | None in implementation evidence; fresh discovery owns corroboration and current row status. |
| V-02 / AC-02/03, R1 | fail, F-01 | New regression rejects invalid replay in all active states/stages with unchanged bytes; terminal-history case retains replay. Existing reservation/reload/contention tests pass. | None in implementation evidence; fresh discovery owns corroboration and current row status. |
| V-03 / AC-04, R2 | pass | Existing shared-budget, pre-initial repair and free-retry cases pass in the final controller suite. No counting behavior changed. | Prior pass is navigation only; fresh discovery owns current corroboration. |
| V-04 / AC-03/05, R3 | fail, F-01 | New regression refuses contradictory persisted authority unchanged; existing invalid-request/readiness/legacy-guard cases pass with a coherent unknown-preflight fixture. | None in implementation evidence; fresh discovery owns corroboration and current row status. |
| V-05 / AC-05 | pass | Compared `controller-contract.md` with the correction: its active-current-authority rule, retained terminal history, authority-failure refusal and replay-after-validation semantics remain accurate. Existing CLI contract case passes. No public setter or interface field added. | Prior pass is navigation only; fresh discovery owns current source/contract comparison. |

## Commands and results

- Reviewer reproducer: exact DISC-02 `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PROBE'`
  block in `reviews/discovery-01.md`, section 4, rerun unchanged — exit 0.
  Valid control accepted; two owners, wrong input, wrong flow revision, wrong
  candidate, wrong current stage and stopped parent all rejected. The permanent
  regression additionally exercises public status and reserve for each variant.
- Focused correction command:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest.test_active_assignment_must_match_current_ledger skills.task-orchestrator.tests.test_controller.ControllerReservationTest.test_terminal_assignment_retains_historical_authority`
  — 2 passed, 5.400 seconds.
- Reviewer DISC-01 command:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest`
  — 11 passed, 8.327 seconds after the fixture correction.
- Owning suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — 44 passed, 0.502 seconds.
- Owning suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — final run: 87 passed, 33.070 seconds; initial run: 87 tests, one fixture
  error described above.
- Hygiene: `git diff --check` and `git diff --cached --check` passed. These are
  not behavioral evidence.
- Broad/aggregate gate:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — not run. The brief assigns its decision to fresh independent discovery.
  The prior retrieval-inventory issue remains unqualified by this correction.

## Remaining review route

Remaining reviewer coverage: all V-01..V-05 and R1..R3 need fresh corroboration;
the prior discovery had no blocked or unchecked rows. F-01 is corrected in
implementation evidence, not independently closed. Correction owner: this
implementer. Evidence/aggregate owner: fresh discovery. Decision owner: separate
acceptance reviewer. No new authority decision or capability gap was found.

Next: refresh `task-maintainability-review` for the changed validator/tests,
then fresh independent `task-review-discovery`, then a separate fresh
`task-acceptance-review` decision. No mandatory architecture command or contract
registry exists for this scope. The prior maintainability report is not reused
for changed bytes. These are separate caller-started invocations; this correction
does not claim their results. No installed skill or development-profile
dependency changed, so no installer change is needed.
