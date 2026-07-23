# S3-13B: Publish the Exact Commit Safely

Status: ready after S3-13A
Depends on: S3-13A
Blocks: S3-14

## Outcome

Publish an already-proven S3-13A commit candidate using compare-and-swap HEAD
semantics, then refresh only the committed paths in the real index while
preserving unrelated staged entries and all worktree bytes. This task does not
read or mutate the orchestration ledger.

## Required context

Read:

- `docs/stage-3-plan.md` — exact-path commit constraints
- S3-13A candidate builder and its temporary-Git tests
- `scripts/controller_git.py`
- `tests/test_controller_git.py`

## Entry criteria

- S3-13A passes and returns complete candidate evidence.
- Current HEAD and real-index identity still match the candidate preconditions.
- The candidate commit object independently validates.

## Allowed changes

- `scripts/controller_git.py`
- `tests/test_controller_git.py`

Do not wire `accept`, read/update the ledger, or perform rollback/cleanup of
user work.

## Work

1. Revalidate candidate OID, parent, tree, diff path set, exact paths, message,
   authoring metadata, expected HEAD, and expected real-index tree.
2. Update HEAD only with compare-and-swap semantics; never force or retry after
   mismatch.
3. Refresh only committed path entries in the real index from the new tree,
   using exact NUL-safe input/plumbing and without changing worktree bytes.
4. Verify the commit now at HEAD and the real-index state for committed paths.
5. Prove every unrelated staged entry retains its exact mode/blob/stage
   identity and every unrelated worktree/untracked byte remains unchanged.
6. Return publication evidence sufficient for controller operation/recovery.

## Acceptance criteria

- **AC-01:** HEAD moves only from the expected parent to the exact candidate.
- **AC-02:** Concurrent HEAD or index change fails closed without force update or
  broad index rewrite.
- **AC-03:** Committed paths no longer appear as staged inverse changes after
  publication.
- **AC-04:** Unrelated staged entries retain exact index identity.
- **AC-05:** Worktree bytes and unrelated untracked files remain unchanged.
- **AC-06:** Returned evidence includes old/new HEAD, commit/tree/diff identity,
  before/after real-index identity, and preservation observations.

## Verification

Run one compare-and-swap failure test first, then the focused publication
temporary-Git class and full `test_controller_git.py`. Finish with the aggregate
suite and `git diff --check`.

## Exit and handoff

Report HEAD update and exact-index-refresh plumbing plus race/preservation
oracles. Stop before controller finalization wiring.
