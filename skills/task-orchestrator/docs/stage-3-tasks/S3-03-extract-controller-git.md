# S3-03: Extract Controller Git Observations

Status: ready after S3-02
Depends on: S3-02
Blocks: S3-08, S3-13

```yaml
agent_tier: strong
reasoning: high
review: immediate
estimated_budget: 30 tool calls / 90 minutes / 100k context
```

## Outcome

Move Stage 2 Git snapshot, comparison, and closure-artifact construction into a
small functional `controller_git.py` boundary. Preserve all Stage 2 evidence,
digests, path handling, and CLI behavior.

## Required context

Read:

- `docs/stage-3-plan.md` — architecture and durable records
- `scripts/controller.py` — baseline capture and `_cli_run_next` Git sections
- `scripts/controller_state.py` — shared record/digest contracts
- owning Git/closure tests in `tests/test_controller.py`

## Entry criteria

- S3-02 is complete and the aggregate suite passes.
- Stage 2 closure fixtures/output and the required Git/path characterizations
  below pass before extraction. A failure returns to Stage 2; do not redefine
  behavior inside this refactor.
- No overlapping user edits exist in the Git-evidence sections.

## Allowed changes

- `scripts/controller.py`
- new `scripts/controller_git.py`
- new `tests/test_controller_git.py`
- `tests/test_controller.py` only to move or retain integration assertions

Do not implement verification execution, acceptance, commit creation, or new
Stage 3 evidence fields.

## Work

1. Extract Git command execution and parsing needed for repository top-level,
   HEAD/index/status snapshots, staged/unstaged/untracked views, task patch, and
   closure artifact publication.
2. Return explicit data records to `controller.py`; do not let the Git module
   mutate the ledger or choose transitions.
3. Preserve odd path bytes using the established encoding/path strategy and
   exact argv invocation with no shell.
4. Add temporary-Git tests at this boundary and keep one `run-next` integration
   test proving the wiring.

## Required test evidence

Positive cases:

- Temporary repositories exercise tracked, staged, unstaged, untracked,
  deleted, renamed, and unchanged pre-existing dirty paths, with exact status,
  artifact content, and digest oracles.
- Allowed tracked and untracked changes appear in the task-scoped patch, and
  the existing fake-worker `run-next` case proves `controller.py` uses the new
  boundary while preserving the closure packet.
- Paths containing spaces, a leading dash, tabs/newlines, and non-UTF-8 bytes
  where the established Stage 2 strategy supports them retain their exact
  identity without shell interpretation.

Negative cases:

- Unexpected paths and modified or disappeared pre-existing dirty paths remain
  classified as violations and are excluded from the task-scoped patch even
  when they coexist with allowed changes.
- A controlled nonzero Git command cannot return a successful or complete
  observation record; the error is surfaced to the caller.
- Shell metacharacters in a valid path are passed as literal argv data and
  cannot execute a side effect.

At least one test must fail if `run-next` bypasses `controller_git.py`. Confirm
the absence of duplicate Git parsing/observation logic by task-scoped diff
inspection rather than a broad source-shape assertion.

## Acceptance criteria

- **AC-01:** Stage 2 closure JSON and artifact content remain compatible.
- **AC-02:** Git subprocess and parsing logic are not duplicated between
  `controller.py` and `controller_git.py`.
- **AC-03:** `controller_git.py` has no ledger mutation, worker launch, or policy
  decision responsibility.
- **AC-04:** Temporary-Git tests cover tracked, staged, unstaged, untracked,
  deleted, renamed, and pre-existing dirty observations already promised by
  Stage 2.
- **AC-05:** The existing fake-worker `run-next` flow still passes.
- **AC-06:** Task patches exclude unexpected and pre-existing dirty changes, and
  controlled Git failures cannot produce apparently complete evidence.
- **AC-07:** The promised unusual-path cases pass before and after extraction,
  or the task stops and returns the gap to Stage 2.

## Verification

Before editing, run the existing controller suite to establish the Stage 2
baseline and required Git/path characterizations:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
```

After extraction, run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
```

Then run the aggregate suite and `git diff --check`.

## Exit and handoff

Report the Git operations now owned by the module. Stop before adding commit
mechanics; S3-13 owns that separate mutating boundary.
