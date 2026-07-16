# S3-04 Correction Result: State Model Review Findings

Status: complete; ready for repeat S3-04 review
Date: 2026-07-16

## Outcome

Corrected the four confirmed S3-04 review findings without importing the
sibling implementation from `main` or expanding the Stage 3 contract.

- Ledger validation now rejects every unselected task in `running`,
  `awaiting_inspection`, or `resumable`. Active run states require exactly one
  such task, owned by `selected_task_id`; `initialized`, `ready`, and `stopped`
  permit none.
- `apply_ledger_update` now routes every changed task state through
  `transition_task`, including its accepting-decision and exact-identity guard.
  Missing or stale acceptance evidence is rejected without mutating the input;
  an exact accepting decision remains executable.
- Pure and persisted ledger updates now require `expected_revision`.
  Controller-owned revision/timestamp fields cannot be supplied by an updater,
  and run, repository, policy, manifest, and baseline authority fields cannot
  be changed. Valid updates still advance the revision by exactly one.
- Transition tests now own literal expected run and task maps, assert exact
  equality with production, exercise every literal state pair, and explicitly
  freeze the terminal `accepted` and `stopped` rows.

## Changed Files

- `scripts/controller_state.py`
- `scripts/controller.py`
- `tests/test_controller_state.py`
- `tests/test_controller.py`
- `docs/stage-3-tasks/S3-04-correction-result.md`

The pre-existing modified `docs/session-handoff.md` and untracked `AGENTS.md`
and `agent-output.analysis.md` were preserved unchanged by this correction.

## Fail-First Evidence

Before changing production code, only
`test_ready_ledger_rejects_unselected_active_task` was added and run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -k unselected_active_task skills/task-orchestrator/tests/test_controller_state.py
```

It ran one test and failed for the intended reason:

```text
AssertionError: ValueError not raised
Ran 1 test
FAILED (failures=1)
```

This proved that the pre-correction validator accepted a `ready` ledger with
an unselected `running` task; the failure was not caused by fixture, import, or
syntax errors.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — passed, 25 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed, 40 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — passed, 98 tests.
- Parsed all 4 task-orchestrator JSON files with the Python standard library.
- Parsed the 4 changed Python files with `ast.parse` and bytecode disabled.
- `git diff --check` passed.
- Final status, changed-file, and task-scoped diff inspection found no changes
  outside the allowed correction files; unrelated dirty files remain present.

No network access, dependency installation, live model, commit, reset, clean,
or destructive Git operation was used.

## Residual Risk

None known within S3-04. The intentionally local single-host lock and the
later-stage record-schema and authority-chain work remain outside this
correction, as specified by the Stage 3 plan.
