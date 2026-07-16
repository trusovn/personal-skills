# S3-13A: Build an Exact-Path Commit Candidate

Status: ready after S3-03 and S3-05
Depends on: S3-03, S3-05
Blocks: S3-13B

## Outcome

Implement and prove a controller-owned Git primitive that uses a temporary
index to construct an exact commit candidate for the accepted path set. It
creates and validates the commit object but does not move HEAD, change the real
index, touch worktree bytes, or read/mutate the orchestration ledger.

## Required context

Read:

- `docs/stage-3-plan.md` — commit invariants and architecture
- `scripts/controller_git.py`
- `scripts/controller_state.py` — operation/identity shapes
- `tests/test_controller_git.py`

## Entry criteria

- S3-03 Git extraction and S3-05 record contracts pass.
- Temporary local Git repositories are available.
- The accepted path set can be represented as exact repository-relative paths.

## Allowed changes

- `scripts/controller_git.py`
- `tests/test_controller_git.py`

Do not wire `accept`, inspect a human tracker, or mutate a ledger.

## Work

1. Accept expected HEAD, expected real-index tree, exact changed paths,
   deterministic commit metadata/message inputs, and repository root.
2. Reject empty sets, duplicates, invalid paths, pathspec magic, submodules,
   vanished/mismatched paths, and current HEAD/index drift before mutation.
3. Create a temporary index outside the repository and populate it from the
   expected HEAD.
4. Feed exact paths as NUL-delimited pathspec input; never use a shell, glob,
   blanket `git add`, or `git commit -a`.
5. Prove the temporary cached path set equals the accepted changed path set and
   excludes every pre-existing dirty path outside that set.
6. Create a commit object with the expected HEAD as its only parent and the
   prepared deterministic metadata.
7. Verify candidate parent, tree/diff path set, message, authoring policy, and
   unchanged HEAD/real-index/worktree identities. Return candidate evidence;
   do not update any ref or decide acceptance.

## Acceptance criteria

- **AC-01:** Allowed modified, added, deleted, renamed, and odd-name paths
  produce exactly the expected candidate diff or a fail-closed denial.
- **AC-02:** Unexpected and pre-existing dirty paths are absent from the commit.
- **AC-03:** HEAD and the real index have identical identities before and after
  candidate construction.
- **AC-04:** Unrelated worktree bytes and untracked files are unchanged.
- **AC-05:** A changed expected HEAD/index during candidate construction fails
  closed and no ref is updated.
- **AC-06:** Empty candidates, submodules, invalid paths, and path disappearance are
  rejected before HEAD mutation.
- **AC-07:** Returned evidence is sufficient for S3-13B to revalidate and
  publish the exact candidate independently.

## Verification

Run one wrong-path denial test first, then the temporary-Git commit class:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py
```

Finish with the aggregate suite and `git diff --check`.

## Exit and handoff

Report the temporary-index commands, candidate evidence, and unchanged real-Git
oracles. Stop before updating HEAD or the real index.
