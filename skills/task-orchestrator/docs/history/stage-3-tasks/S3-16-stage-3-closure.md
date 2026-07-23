# S3-16: Close Stage 3

Status: ready after S3-12 and S3-15
Depends on: S3-12, S3-15
Blocks: Stage 4

## Outcome

Verify the complete Stage 3 contract, inspect scope, and create a truthful
`docs/stage-3-handoff.md`. This task changes documentation only after all
behavioral gates pass; it does not fix failed implementation.

## Required context

Read:

- `docs/direction.md`
- `docs/controller-contract.md`
- `docs/stage-3-plan.md`
- completed S3 task reports or accepted diffs
- all changed Stage 3 source/test/schema files

## Entry criteria

- S3-12 and S3-15 are complete.
- No core task has an unresolved blocker or falsely documented acceptance
  criterion.
- Tracker mode is either off or separately backed by completed S3-T1/S3-T2.

## Allowed changes

- create `docs/stage-3-handoff.md`
- `docs/stage-3-plan.md` only where implementation facts changed

Do not change production code, tests, `SKILL.md`, evaluations, Stage 4/5 docs,
or installed/cached skill copies. A failed gate returns to its owning task.

## Work

1. Trace every Stage 3 exit criterion to code and deterministic evidence.
2. Run the verification progression one command at a time.
3. Inspect the full task-orchestrator diff for scope, architecture boundaries,
   generated artifacts, and preservation of user changes.
4. Confirm no live model, network, dependency, tracker-without-contract, or
   auto-launch behavior exists.
5. Write the handoff with exact changed files, commands/results, decisions,
   known gaps, recovery limitations, dirty state, and first Stage 4 action.
6. Update this master only for actual changed facts; do not rewrite its design
   history or mark optional tracker work complete when it was not run.

## Acceptance criteria

- **AC-01:** Every core task and Stage 3 exit criterion maps to passing evidence
  or an explicit user-accepted gap.
- **AC-02:** Focused and aggregate tests pass.
- **AC-03:** JSON assets/fixtures and changed Python parse without generated
  bytecode or repository artifacts.
- **AC-04:** `git diff --check` passes and status contains only intended files
  plus identified pre-existing user changes.
- **AC-05:** Handoff commands/results and residual risks are exact and truthful.
- **AC-06:** `SKILL.md` remains unchanged for Stage 4.

## Verification

Run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
```

Then run the JSON parse, Python AST parse, `git diff --check`, status, and
task-scoped diff inspections from the master progression.

## Exit and handoff

Exit complete only when the handoff can be used as the authoritative Stage 4
entry packet. Report any stronger check not run and why.
