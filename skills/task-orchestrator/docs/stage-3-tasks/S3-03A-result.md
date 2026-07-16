# S3-03A Result: Corrected Git Baseline Contract

Status: complete
Date: 2026-07-16

## Outcome

The Stage 2 Git baseline now retains both path identities from every
porcelain-v1 `-z` rename or copy entry. `capture_git_status()` stores the
destination and source paths in the existing `status` mapping, using the
existing status-code and content-digest value format for each path.

Closure capture therefore excludes either side of a pre-existing rename or
copy from task patch candidates. The durable baseline remains the source of
that decision: closure-time rename detection was not substituted for persisted
baseline evidence.

No S3-03B module-boundary cleanup was performed.

## Contract Decision

Selected representation: expand the existing baseline `status` mapping so an
`R` or `C` status record contributes one mapping entry for its destination and
one for its source. This is the smallest sufficient correction because the
existing task-patch filter and pre-existing-path drift comparisons already use
the mapping's keys and values.

Rejected alternatives:

- A parallel `dirty_paths` field would change the record shape, duplicate path
  identity, and still leave existing drift comparisons incomplete unless more
  consumers changed.
- A generalized Git status model or class hierarchy would exceed this contract
  correction and overlap S3-03B's module-boundary work.
- Detecting and excluding renames only at closure time would not prove that the
  paths were dirty in the persisted task baseline.

## Durable-Record Compatibility Impact

The task-baseline JSON field shape is unchanged: it still contains
`head_oid`, `index_tree`, and `status`. For a baseline containing a rename or
copy, `status` now has an additional source-path entry. Consequently, the
canonical task-baseline bytes and `selected_task_baseline_digest` change for
those baselines. This is an intentional semantic correction, not byte-for-byte
compatibility.

Newly captured baselines persist both identities and bind them through the
existing digest path. Previously persisted baseline records are immutable and
are not migrated; a pre-correction record does not retroactively gain a missing
rename source. No closure JSON fields unrelated to this correction changed.

## Changed Files

- `scripts/controller_git.py` — retain both destination and source identities
  while parsing rename/copy status records.
- `tests/test_controller_git.py` — characterize the pre-existing staged rename,
  its drift cases, and copy-entry identity parsing.
- `docs/stage-3-tasks/S3-03A-result.md` — this completion record.

## Test-First Evidence

Before the production correction:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_git.ControllerGitTest.test_task_patch_excludes_both_sides_of_preexisting_rename`
  — failed as expected. Allowing `old.txt`, alone or together with `new.txt`,
  produced a deletion patch for `old.txt`; the captured baseline also lacked
  the source identity. One test ran with three assertion failures.

After the correction:

- The same focused test passed: 1 test.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py`
  — passed: 9 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed: 39 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — passed: 82 tests.
- Both changed Python files parsed with `ast.parse` without generating
  bytecode.
- `git diff --check` passed. The no-index whitespace check for this new result
  file emitted no errors (its exit status was 1 because the file is new).

## Acceptance Criteria

- **AC-A01 — satisfied.** Persisted task-baseline data now contains exact
  destination and source keys for `R` and `C` entries. The tests assert exact
  fingerprints for both rename sides and both copy identities.
- **AC-A02 — satisfied.** An unchanged staged pre-existing rename produces an
  empty task patch when the source, destination, or both are allowed.
- **AC-A03 — satisfied.** A modified pre-existing rename reports both retained
  identities as modified; removing the rename state reports both as
  disappeared. Both cases keep the task patch empty.
- **AC-A04 — satisfied.** Existing temporary-Git coverage for tracked, staged,
  unstaged, deleted, renamed, and untracked post-baseline changes passes.
- **AC-A05 — satisfied.** Existing mixed-change coverage continues to exclude
  unexpected and baseline-dirty content while including allowed task changes.
- **AC-A06 — satisfied.** Parsing remains NUL-delimited and subprocess argv
  remains shell-free. Existing unusual-path coverage passes, and the copy
  characterization retains tab/newline path identities.
- **AC-A07 — satisfied.** The baseline-content and digest impact is stated
  above; unrelated closure fields were not changed.
- **AC-A08 — satisfied.** The 39-test controller and fake-worker compatibility
  suite passes without a controller change.

## Residual Risks

- Historical task baselines captured before this correction remain incomplete
  for rename sources because immutable records were not migrated.
- The decisive rename regression uses a real temporary Git repository. The
  copy parser branch is characterized with exact porcelain bytes because the
  controller does not request Git copy detection itself.

## Verdict

**ready for S3-03B** — the corrected baseline contract is covered by the
focused regression, the controller Git suite, and the controller compatibility
suite. S3-03B may now repair the module boundary without redefining this
behavior.
