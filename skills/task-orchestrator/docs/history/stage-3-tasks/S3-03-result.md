# S3-03 Result: Controller Git Observation Extraction

Status: complete
Date: 2026-07-16

## Outcome

Extracted Stage 2 Git command execution, parsing, snapshots, comparison data,
task-scoped patch capture, and closure text-artifact publication from
`scripts/controller.py` into `scripts/controller_git.py`. `controller.py`
retains compatibility aliases for `capture_git_status` and
`capture_initial_baseline`, and continues to own worker launch, closure
decisions, ledger mutation, and CLI transitions.

Git operations now owned by `controller_git.py`:

- repository top-level and HEAD resolution;
- index-tree and porcelain-v1 status snapshots;
- initial and selected-task baseline construction;
- staged and unstaged name-status/stat observations;
- NUL-delimited untracked-path parsing;
- allowed-path binary task patches, including allowed untracked files;
- changed-path classifications and HEAD/index mechanical violations; and
- immutable closure text artifacts and their evidence digests.

No commit creation or publication mechanics were added.

This completion supersedes the earlier blocked result in this file. Before the
restart, the Stage 2 closure path had been corrected to use NUL-delimited
untracked-path output; the required pre-edit controller and unusual-path
characterizations passed, so the prior Stage 2 blocker was no longer present.

## Acceptance evidence

- Stage 2 controller compatibility tests preserve closure JSON fields,
  artifacts, digests, fake-worker `run-next` behavior, and CLI transitions.
- Temporary-Git tests cover tracked, staged, unstaged, untracked, deleted,
  renamed, unchanged pre-existing dirty, modified pre-existing dirty, and
  disappeared pre-existing dirty paths.
- Exact status values, artifact content, and SHA-256 values are checked against
  independent test oracles.
- Unexpected and pre-existing dirty content is classified and excluded from
  the allowed-path patch in the characterized mixed-change scenario.
- Spaces, a leading dash, tabs, newlines, shell metacharacters, and a raw
  non-UTF-8 Git path retain literal identity under the existing
  surrogate-escape strategy. Shell metacharacters produce no side effect.
- A nonzero Git command raises before the closure artifact directory is
  published.
- A controlled monkeypatch proves `run-next` calls the extracted task-baseline
  boundary and would fail if it bypassed `controller_git.py`.
- Task-scoped inspection confirms `controller.py` contains no Git argv or Git
  parsing implementation; its remaining subprocess call launches the worker
  adapter.

## Verification

- Pre-edit:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 39 tests passed.
- Pre-edit aggregate:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — 73 tests passed with the local loopback permission required by the existing
  sandbox-capability test.
- Test-first demonstration: the new Git-boundary suite failed because
  `controller_git.py` and controller wiring did not yet exist.
- Final Git boundary:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py`
  — 6 tests passed.
- Final controller:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 39 tests passed.
- Final aggregate:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — 79 tests passed with the same local loopback permission.
- Parsed all 4 task-orchestrator JSON assets with the standard library.
- Parsed the 3 changed Python files with `ast.parse` without generating
  bytecode.
- `git diff --check` passed; equivalent no-index checks passed for the new
  untracked task files.

## Residual risk

No known S3-03 behavior gap. The non-UTF-8 characterization exercises raw Git
path identity through the index because the execution sandbox rejects direct
creation of a non-UTF-8 filesystem pathname. Commit mechanics remain deferred
to S3-13.
