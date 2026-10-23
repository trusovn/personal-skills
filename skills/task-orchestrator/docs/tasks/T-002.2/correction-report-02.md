# T-002.2 correction handoff — F-02

Active assignments now have to match the actor selected by the frozen flow
before status or replay exposes them. Terminal assignments retain their
historical actors. This record contains implementation evidence, not an
independent review or acceptance decision.

Implemented: READY_FOR_REVIEW

## Authority and pre-edit coverage map

- Authority: `skills/task-orchestrator/docs/tasks/T-002.2/brief.md`, revision 1.
- Preflight/context: `skills/task-orchestrator/docs/tasks/T-002.2/preflight.md`
  including Decision context; `verification.md` revision 1;
  `../T-002/brief.md`; `../../local-harness-orchestration-plan.md`;
  `../T-002.1/controller-contract.md` and `reviews/discovery-02.md`.
  Authority, dependencies, permissions and verification scenarios are unchanged.
- Preceding verdict: none. Discovery-02 publishes evidence only. F-01's original
  defects are rejected by its probes; F-02 is unresolved, suggested P2.
- Complete finding inventory: F-01 (prior active-assignment identity/lifecycle
  mismatch, preserve its regressions); F-02 (known actor profiles accepted even
  when they contradict the frozen flow's selection).
- Broken invariant: every active assignment's actor must equal the selection
  for its frozen stage mode. Correction uses implementation mode; verify has
  no actor. Terminal history keeps its historical assignment.
- Scenario inventory: V-01, V-02, V-03, V-04, V-05; R1, R2, R3.
- Scope: preserve all existing staged work. Change only the controller's
  reservation-context validation, existing controller regressions, and this
  report. No installed skill or development-profile dependency changes.

This map was written before production/test edits. Prior reviewer statuses
remain unchanged; earlier passes guide navigation and do not qualify corrected
bytes. No prior row is blocked or unchecked.

| Row | Prior discovery status | Correction evidence / navigation | Incomplete reason / next owner |
|---|---|---|---|
| V-01 / AC-01 | fail — F-02 | Focused matrix and controller suite pass: valid status stays readable; wrong known actors make status fail without changing run/task bytes. Covers fast-local and strong-local flows and reserved/running/unknown. Existing read-only evidence/status cases pass. | None in implementation checks; fresh discovery owns current row status. |
| V-02 / AC-02/03, R1 | fail — F-02; R1 one-owner cases pass | Focused matrix rejects exact-request replay of a wrong actor after reload. Terminal assignment/actor replay passes. Reservation/reload/contention cases pass in DISC-01 and the controller suite. | None in implementation checks; fresh discovery owns corroboration and current row status. |
| V-03 / AC-04, R2 | pass | Existing shared-budget, pre-initial repair and free-retry cases pass in DISC-01 and the controller suite. No counting behavior changed. | Prior pass is navigation only; fresh discovery owns current row status. |
| V-04 / AC-03/05, R3 | fail — F-02 | Focused matrix passes for all six stages, null verify actor, both other known actor profiles, and byte-preserving authority refusal. F-01 identity/lifecycle variants and invalid-request/readiness/legacy cases pass in the controller suite. | None in implementation checks; fresh discovery owns current row status. |
| V-05 / AC-05 | pass | Compared the unchanged controller contract's frozen stage mapping, history and authority-validation-before-replay rules with the fix: no contract change needed. CLI contract case passes in DISC-01 and the controller suite. No public setter or new fields. | Prior pass is navigation only; fresh discovery owns source/contract corroboration. |

## Correction and scoped diff

- `skills/task-orchestrator/scripts/controller.py`: seven lines in
  `_reservation_context` compare the active assignment's actor with its stage
  mode in the loaded authoritative flow. Both status and reservation/replay use
  this context. Correction resolves implementation mode; verify resolves null.
  Structural ledger validation remains separate from loading flow authority.
- `skills/task-orchestrator/tests/test_controller.py`: extend the existing
  matrix rather than add a duplicate fixture/test. Both supplied fast/strong
  profiles retain valid controls and reject other known actor selections in all
  active states. Verify rejects actor-bearing assignments. Extend the terminal
  history case to preserve an actor different from current policy.
- This new report records the pre-edit map and results. Existing staged work,
  review reports, plan documents and installed skills remain unchanged.
  HEAD is `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`; corrected worktree Git
  blobs are controller `0a21618a11b192bae891c373f0ae61caf0c0499b` and controller
  tests `6bf2b95a1f6ca9a398f8beccf03c9b9c4997acff`.

The explicit successor fixture still supplies terminal/readiness/evidence
states only. These checks do not prove production admission, launch or routing.
F-01 regressions are retained; F-02 is corrected in implementation evidence,
not independently closed. No alternative fix was attempted or discarded.

## Commands and results

All checks used local Python and disposable fixture Git repositories, without
network, model launches, dependency installation or active-skill refresh.

- Focused command:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest.test_active_assignment_must_match_current_ledger skills.task-orchestrator.tests.test_controller.ControllerReservationTest.test_terminal_assignment_retains_historical_authority`
  — before the production fix: 2 tests, 60 actor subtest failures, 11.399 seconds;
  each failure was the intended missing status rejection, not a setup error.
  After the fix: 2 passed, 12.937 seconds. Public status/refusal/replay and
  unchanged run/task bytes are the oracles; no decisive logic is mocked.
- Reviewer DISC-01:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest`
  — 11 passed, 16.129 seconds.
- Reviewer DISC-02: executed its exact inline body from
  `reviews/discovery-02.md`, section 4, using the wrapper below. The embedded
  original F-01 control was accepted and all six invalid variants rejected.
  F-02's old acceptance oracle now stops at the first wrong active actor with
  the expected authority error. The permanent matrix above supplies complete
  corrected-behavior sibling evidence; this probe alone does not.
- Owning suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — 44 passed, 0.491 seconds.
- Owning suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 87 passed, 39.989 seconds.
- Reviewer DISC-03 bounded contention/cleanup probe: not separately rerun;
  contention code is unchanged and the existing process-contention test passed.
  That test does not prove timeout robustness. Fresh discovery owns separate
  bounded corroboration and cleanup evidence.
- Hygiene: `git diff --check` and `git diff --cached --check` passed. These
  checks establish whitespace hygiene only, not behavior.
- Optional run-evidence instrumentation is available from `.agents/scripts/`;
  invocation ID: `run-20261023T160156Z-11fd0743ec28`. No runtime identity was
  invented and no active installation was refreshed.

Exact DISC-02 wrapper, exit 0 (expected rejection observed):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
report = Path('skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md').read_text()
source = report.split("python3 - <<'PY'\n", 1)[1].split('\nPY', 1)[0]
try:
    exec(compile(source, 'discovery-02:DISC-02', 'exec'))
except ValueError as error:
    assert str(error) == 'Active assignment actor contradicts the frozen flow', error
    print('F-02 old acceptance probe stopped at the first wrong active actor, as expected after correction')
else:
    raise AssertionError('The old actor-acceptance reproducer must no longer succeed')
PY
```

## Verification ownership and remaining route

The commands above ran progressively: changed methods, reservation class,
reviewer reproducer, state module, then controller module. No blocked or
unchecked row was inherited. All V-01..V-05 and R1..R3 still require fresh
independent corroboration for corrected bytes; reviewer row statuses above
remain unchanged.

The aggregate command
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
belongs to fresh discovery and will not run during correction. The prior
retrieval-inventory issue remains outside this correction's evidence.

Next: fresh `task-maintainability-review`, then fresh independent
`task-review-discovery` (including its aggregate decision), then a separate
fresh `task-acceptance-review` decision. No mandatory architecture command or
contract registry applies to this scope. Previous maintainability evidence
covers earlier bytes. Correction owner: implementer; evidence/capability owner:
fresh discovery; authority/decision owner: separate acceptance reviewer.
