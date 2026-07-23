# S3-02 Result: Pure Controller State Extraction

Status: complete
Date: 2026-07-16

## Outcome

Extracted the pure policy, manifest, transition, attempt-record, selection, and
ledger rules from `scripts/controller.py` into
`scripts/controller_state.py`. `controller.py` retains compatibility aliases
for existing callers and owns the atomic ledger persistence wrapper.

Moved implementations:

- `canonical_json` and `sha256_text`
- run-policy validation and its private validation helpers
- `transition_task`
- `validate_attempt_record` and `build_attempt_record`
- task-manifest validation, dependency-cycle detection, and path validation
- `select_task`
- ledger validation and the pure `apply_ledger_update` rule

Compatibility names retained in `controller.py`:

- `ATTEMPT_REQUIRED_FIELDS` and `ALLOWED_TASK_TRANSITIONS`
- `canonical_json`, `sha256_text`, `validate_run_policy`, and `transition_task`
- `validate_attempt_record` and `build_attempt_record`
- `_validate_task_manifest_schema`, `_detect_dependency_cycles`, and
  `_is_valid_repo_relative_path`
- `validate_task_manifest`, `select_task`, and `_validate_ledger`

## Acceptance evidence

- Direct state-module tests cover valid policy/manifest fixtures and retained
  controller compatibility names.
- Exact canonical JSON, SHA-256, attempt-record, and ledger-entry values are
  characterized.
- Missing, unknown, duplicate, and wrong-type fields retain their exception
  contracts.
- Invalid dependencies, cycles, paths, unavailable selection, invalid
  transitions, stale closure identity, malformed attempt records, and
  incoherent ledger updates are rejected.
- Rejected pure updates do not mutate their input, and rejected controller
  updates leave persisted ledger bytes unchanged.
- Direct-import ownership checks ensure state functions are implemented by
  `controller_state.py`, not delegated back to `controller.py`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — 12 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 39 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — 73 tests passed. The first sandboxed run could not bind the loopback socket
  required by the pre-existing verification-runner capability test; the same
  suite passed with that local host permission.
- Parsed all 4 task-orchestrator JSON files with the Python standard library.
- Parsed the 3 changed Python files with `ast.parse`.
- `git diff --check` passed for staged and unstaged changes before final staging.

## Residual risk

No known S3-02 behavior gap. No Stage 3 fields, CLI changes, Git behavior,
transport behavior, or storage abstraction were added.
