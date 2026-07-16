# S3-03B Result: Repaired Controller Git Boundary

Status: complete
Date: 2026-07-16

## Outcome

The S3-03 Git boundary is observational against the corrected S3-03A
baseline contract. `controller_git.py` executes Git, parses snapshots, compares
HEAD and index identities, classifies paths, constructs closure evidence, and
publishes immutable text artifacts. It now returns raw `head_changed` and
`index_changed` facts without choosing worker-policy consequences.

`controller.py` owns the current `run-next` policy that a worker changing HEAD
or the index is a closure violation. It converts the raw facts into the
existing messages:

- `worker changed HEAD despite commit prohibition`
- `worker changed the Git index`

Those messages retain their existing locations in closure `reasons` and
`controller_observations.mechanical_violations`. Closure JSON fields, artifact
contents, and digest construction remain unchanged from the corrected S3-03A
contract.

## Boundary Ownership

`controller_git.py` owns:

- repository top-level, HEAD, index-tree, and porcelain status observations;
- NUL-delimited status/untracked parsing and exact rename/copy identities;
- staged, unstaged, task-patch, and path-classification observations;
- raw HEAD/index comparison facts; and
- immutable closure text artifacts and their content digests.

`controller.py` owns:

- worker launch and the `run-next` operation;
- worker-specific HEAD/index prohibition messages;
- closure decision assembly and publication;
- ledger mutation and state transitions; and
- all interpretation of Git facts as policy violations.

## Changed Files

- `scripts/controller.py` — translate raw HEAD/index facts into the existing
  worker-policy violations and durable observation field.
- `scripts/controller_git.py` — return raw comparison facts and remove
  worker-policy message construction while preserving the staged S3-03A
  rename/copy baseline correction.
- `tests/test_controller_git.py` — prove the raw-fact boundary, complete
  unusual-path closure evidence, literal argv, artifact digests, and both
  `run-next` Git-boundary calls.
- `tests/test_controller.py` — assert the exact preserved violation text and
  closure locations in the fake-worker flow.
- `docs/stage-3-tasks/S3-03B-result.md` — this new completion record.

No existing plan, task, result, S3-01, or handoff document was modified. No
unrelated file was removed.

## Test-First Evidence

Before the production boundary repair:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_git.ControllerGitTest.test_closure_evidence_returns_raw_comparison_facts_without_worker_policy`
  — failed as expected with one error because the Git boundary did not return
  `head_changed` and still owned `mechanical_violations`.

After the repair, the same focused test passed: 1 test.

The unusual-path test initially used an unsupported raw-worktree-content
oracle. The sandbox permits a non-UTF-8 index identity but not creation of its
matching filesystem path. The final test therefore asserts exact
surrogate-escaped identity through complete closure capture and artifact
readability, while text-path cases prove task-patch content. This matches the
established S3-03 limitation rather than weakening production behavior.

## Verification

Prerequisite gates before editing:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py`
  — passed: 9 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed: 39 tests.

Final focused and owning evidence:

- Raw comparison-fact test — passed: 1 test.
- Complete unusual-path closure-evidence test — passed: 1 test.
- Dual-entry-point `run-next` wiring test — passed: 1 test.
- Fake-worker full closure flow — passed: 1 test.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py`
  — passed: 11 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed: 39 tests on the final tree.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — passed: 84 tests.
- All four changed Python files parsed with `ast.parse` without bytecode.
- `git diff --check` passed.
- `git diff HEAD --check` passed, including the staged S3-03A correction.

## Task-Scoped Inspection

Inspection found no duplicated Git argv or parsing logic in `controller.py`.
Its only `subprocess.run` launches the worker adapter. `controller_git.py`
contains the Git subprocess calls and raw comparisons, with no worker-policy
message text, ledger mutation, transition, or worker launch.

## Acceptance Criteria

- **AC-B01 — satisfied.** The Git boundary returns observations and raw
  comparison facts and contains no worker-policy violation messages or
  controller state responsibilities.
- **AC-B02 — satisfied.** `controller.py` applies both worker prohibitions with
  the exact existing text and closure locations.
- **AC-B03 — satisfied.** Git subprocess and parsing logic remain isolated from
  `controller.py`.
- **AC-B04 — satisfied.** Closure field locations, artifact bytes, and digest
  behavior are preserved; integration and independent digest assertions pass.
- **AC-B05 — satisfied.** A fake-worker `run-next` flow observes exactly one
  call to both `capture_task_baseline` and `capture_closure_evidence` and
  publishes a complete closure packet.
- **AC-B06 — satisfied.** The existing controlled nonzero-Git test passes and
  proves no closure directory is published on capture failure.
- **AC-B07 — satisfied.** Spaces, a leading dash, tabs, newlines, shell
  metacharacters, and the supported raw-byte index identity pass through full
  closure capture. Literal argv, no shell side effect, readable artifacts, and
  matching digests are asserted.
- **AC-B08 — satisfied.** Targeted and aggregate suites pass, and the diff is
  limited to allowed S3-03B files plus preserved S3-03A changes and unrelated
  pre-existing user files.

## Residual Risks

- As established by S3-03, the execution sandbox supports a non-UTF-8 Git index
  identity through surrogate escape but prevents direct creation of its
  matching worktree path; raw-byte worktree patch content is therefore not
  directly characterized.
- Historical baselines created before S3-03A remain incomplete for rename
  sources and are not migrated.

## Verdict

**complete**
