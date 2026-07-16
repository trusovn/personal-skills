# Task Orchestrator: Stage 3 Master Plan

Status: planning baseline; Stage 2 is assumed complete for this plan
Date: 2026-07-16
Parent direction: [direction.md](direction.md)
Stage 2 contract: [stage-2-plan.md](stage-2-plan.md)
Task briefs: [stage-3-tasks/](stage-3-tasks/)

## Objective

Complete the deterministic single-worktree controller path after the documented
Stage 2 exit state. Stage 3 independently verifies a terminal worker attempt,
produces a replay-resistant closure decision, supports safe recovery and
same-thread resume, finalizes acceptance in the controller ledger, releases
dependency-ready work without launching it, and creates an exact-path
controller-owned commit only when persisted policy authorizes one.

This master document owns Stage 3-wide context, ordering, architecture, and
completion criteria. Each linked task brief owns one bounded implementation
slice and is intended to be handed to one implementation agent in isolation.

## Entry contract

Stage 3 work may start only when all of the following are true:

- Stage 2 satisfies the exit criteria in [stage-2-plan.md](stage-2-plan.md).
- A run can be initialized, select one dependency-ready task, launch exactly
  one fake worker, and publish an immutable Stage 2 closure packet.
- The Stage 2 ledger and closure packet contain the task, attempt, prompt,
  policy, manifest, baseline, HEAD, index, adapter, and evidence identities
  needed by Stage 3.
- Focused controller and worker tests pass.
- No unresolved Stage 2 defect is being silently moved into a Stage 3 task.

This plan intentionally does not list or remediate current Stage 2 findings.
If an entry condition is false when implementation begins, stop and return the
work to Stage 2 instead of expanding the selected Stage 3 task.

## Settled decisions and constraints

- Keep Python standard-library-only, sequential, and single-worktree.
- Keep the corrected Codex CLI transport. Do not add SDK, MCP, workflow-engine,
  parallel-worktree, or live-model behavior.
- The controller owns policy, state, evidence, decisions, finalization, and any
  authorized commit. The worker never commits or changes orchestration state.
- Worker results remain untrusted claims. Mechanical acceptance uses only
  controller-observed Git evidence and controller-run verification.
- Parse verification commands with `shlex.split()` and execute argv with
  `shell=False`. Shell syntax and leading environment assignments fail closed.
- Mechanical acceptance records `semantic_review: not_collected`; Stage 3 does
  not choose a semantic reviewer.
- Human tracker mode is `off` in the Stage 3 core. Tracker support is a
  conditional extension requiring a separately approved versioned contract.
- Same-thread resume appends a new immutable turn to the existing attempt. A
  fresh retry would allocate a new attempt, but Stage 3 adds no public `retry`
  command because no retry transition/authority contract is approved.
- `accept` accepts no task ID, paths, checks, tracker choice, commit flag, or
  free-form authority. It derives every value from persisted records.
- An accepted task returns the run to `ready` or terminal `stopped`; it never
  auto-launches the next task.

## Brief architecture assessment

The responsibility boundaries in [direction.md](direction.md) remain sound:
controller policy is separate from worker transport, evidence is independent
from worker claims, and commits belong to controller finalization.

The current file shape will not scale safely through Stage 3 without a small
refactor:

- `scripts/controller.py` is already about 1,466 lines.
- `_cli_run_next()` combines persisted-input validation, Git integrity checks,
  task selection, prompt/attempt creation, transport invocation, result
  validation, closure evidence, decision construction, and ledger mutation.
- Git commands and record/state rules are repeated as raw dictionaries and
  subprocess calls, while the Stage 3 `inspect`, `recover`, `accept`, and commit
  paths need the same boundaries.
- `tests/test_controller.py` is similarly monolithic, making it expensive for a
  small-context agent to identify the contract it is changing.

The smallest beneficial target shape is:

```text
scripts/
  controller.py              # CLI parsing and use-case orchestration
  controller_state.py        # pure validators, transitions, identities, records
  controller_git.py          # Git snapshots, comparisons, and commit mechanics
  verification_runner.py     # chosen permission-bounded command boundary
  codex_worker.py             # Codex CLI transport and process lifecycle
tests/
  test_controller.py         # command/use-case integration coverage
  test_controller_state.py   # pure state and record contracts
  test_controller_git.py     # temporary-Git behavior
  test_verification_runner.py
  test_codex_worker.py
```

This is a functional split, not a new framework. Keep public CLI commands and
existing importable controller functions compatible. Do not add classes,
dependency injection machinery, a top-level package, or generalized storage/
workflow abstractions. Extract only the two demonstrated boundaries in tasks
S3-02 and S3-03; `verification_runner.py` is added only after S3-01 proves its
enforcement mechanism.

## Durable Stage 3 records

Stage 2 artifacts remain immutable. Stage 3 adds records rather than rewriting
the Stage 2 closure packet:

```text
<run-dir>/
  ledger.json
  attempts/
    attempt-001/
      record.json
      prompt.txt
      state.json
      turn-001.*
      turn-002.*
  closure/
    attempt-001.json
    attempt-001.*
  verification/
    attempt-001.json
    attempt-001.command-001.stdout.log
    attempt-001.command-001.stderr.log
  decisions/
    attempt-001.json
  operations/
    T1-accept.json
```

Every reference is repository- or run-directory-contained as appropriate and
digest-bound. Existing attempt, turn, closure, verification, and decision bytes
are never overwritten or deleted. A finalization operation may advance through
validated compare-and-swap state updates, but its prepared intent and completed
effect evidence are immutable once recorded.

## Task execution contract

An agent receiving one task brief must:

1. read this document's entry contract, settled decisions, and architecture;
2. read only its assigned task brief and the files explicitly listed there;
3. inspect `git status --short` and preserve all pre-existing user changes;
4. confirm every entry criterion before editing;
5. add or identify a test that rejects the missing behavior or a controlled
   fault before implementing it;
6. change only the allowed files in the task brief;
7. run the brief's targeted check first and broader checks only after it passes;
8. stop at the brief's exit boundary, even if adjacent work is obvious; and
9. report changed files, acceptance criteria satisfied, commands/results,
   decisions, and residual risks without editing this master or its task brief.

No task authorizes a live Codex call, network access, dependency installation,
destructive Git cleanup, installed/cached skill edits, or user-work rollback.

## Task index and dependency graph

The core path is ordered to keep each task independently reviewable. S3-01 may
run before or alongside the behavior-preserving refactors, but agents sharing a
working tree still execute sequentially.

| ID | Task | Depends on | Exit summary |
|---|---|---|---|
| S3-01 | [Prove the verification sandbox boundary](stage-3-tasks/S3-01-verification-sandbox-proof.md) | Stage 2 | Supported mechanism is recorded and locally proven, or Stage 3 is blocked without policy weakening |
| S3-02 | [Extract pure controller state](stage-3-tasks/S3-02-extract-controller-state.md) | Stage 2 | Pure state/validation code is isolated with unchanged behavior |
| S3-03 | [Extract controller Git observations](stage-3-tasks/S3-03-extract-controller-git.md) | S3-02 | Git observation/evidence code is isolated with unchanged behavior |
| S3-04 | [Extend the Stage 3 state model](stage-3-tasks/S3-04-stage-3-state-model.md) | S3-02 | Run/task transitions and ledger coherence are executable contracts |
| S3-05 | [Add immutable record and identity contracts](stage-3-tasks/S3-05-record-and-identity-contracts.md) | S3-04 | Verification, decision, and operation records reject stale/mismatched data |
| S3-06 | [Build the authorized verification command plan](stage-3-tasks/S3-06-verification-command-plan.md) | S3-05 | Required checks are safely parsed, deduplicated, sourced, and gap-aware |
| S3-07 | [Implement the sandboxed verification executor](stage-3-tasks/S3-07-verification-executor.md) | S3-01, S3-05, S3-06 | Commands run sequentially within policy and produce immutable logs/results |
| S3-08 | [Implement inspection and closure decisions](stage-3-tasks/S3-08-inspect-and-decide.md) | S3-03, S3-07 | `inspect` publishes immutable verification and decision records |
| S3-09 | [Reconcile running attempts and stop safely](stage-3-tasks/S3-09-recover-running-and-stop.md) | S3-04, S3-05 | Recovery proves process absence and maps terminal outcomes without guessing |
| S3-10 | [Implement same-thread resume](stage-3-tasks/S3-10-same-thread-resume.md) | S3-09 | `resume` appends one immutable turn without changing authority |
| S3-11 | [Prepare acceptance with side effects off](stage-3-tasks/S3-11-acceptance-operation.md) | S3-08, S3-09, S3-10 | `accept` journals intent and records that no optional effect is required without accepting yet |
| S3-12 | [Finalize acceptance and release dependencies](stage-3-tasks/S3-12-release-dependencies.md) | S3-11 | One atomic ledger write accepts the task, recomputes readiness, and launches nothing |
| S3-13A | [Build an exact-path commit candidate](stage-3-tasks/S3-13-exact-path-commit.md) | S3-03, S3-05 | A temporary index produces and proves the exact commit object without moving HEAD/index |
| S3-13B | [Publish the exact commit safely](stage-3-tasks/S3-13B-exact-commit-publication.md) | S3-13A | Compare-and-swap HEAD publication preserves unrelated index/worktree state |
| S3-14 | [Integrate controller-owned commit finalization](stage-3-tasks/S3-14-commit-finalization.md) | S3-12, S3-13B | Authorized commit intent is executed and evidence-bound before the shared acceptance finalizer |
| S3-15 | [Reconcile interrupted finalization](stage-3-tasks/S3-15-finalization-recovery.md) | S3-14 | Prepared operations recover idempotently or stop on ambiguous mutation |
| S3-16 | [Close Stage 3](stage-3-tasks/S3-16-stage-3-closure.md) | S3-12, S3-15 | Full local evidence and truthful Stage 3 handoff are complete |

```text
S3-01 -----------------------------> S3-07
S3-02 -> S3-03 --------------------> S3-08
   |       |                            |
   +-> S3-04 -> S3-05 -> S3-06 -> S3-07
          |        |                    |
          +------> S3-09 -> S3-10 ------+
                                        v
                                      S3-11 -> S3-12 --+
S3-03 -> S3-13A -> S3-13B -> S3-14 -> S3-15 ---------+-> S3-16
                                      ^
                                      +---- S3-12
```

## Conditional human-tracker extension

Human-tracker support is not on the core completion path. Use these tasks only
if the user separately requests it:

| ID | Task | Depends on | Exit summary |
|---|---|---|---|
| S3-T1 | [Freeze a human-tracker contract](stage-3-tasks/S3-T1-human-tracker-contract.md) | S3-05 plus a concrete tracker and user authority | One path, format, mapping, transition, atomicity, and commit treatment are approved |
| S3-T2 | [Implement the approved tracker adapter](stage-3-tasks/S3-T2-human-tracker-adapter.md) | S3-T1 | Exactly one mapped record updates atomically and idempotently without controller wiring |
| S3-T3 | [Integrate tracker finalization and recovery](stage-3-tasks/S3-T3-human-tracker-finalization.md) | S3-T2, S3-15 | Prepared tracker intent executes and reconciles before acceptance |

Do not create a generic Markdown editor or placeholder adapter. If S3-T1 is not
complete, tracker mode remains `off` and no tracker path appears in an accepting
operation.

## Risk-to-task coverage

| Risk | Primary task evidence |
|---|---|
| Verification escapes write/network policy | S3-01, S3-07 |
| Shell syntax or unpersisted environment changes authority | S3-06 |
| Stale or unrelated evidence authorizes acceptance | S3-05, S3-08, S3-11 |
| Worker claims become proof | S3-08 |
| Live or ambiguous worker is resumed | S3-09, S3-10 |
| Earlier turns or attempts are overwritten | S3-05, S3-10 |
| Acceptance side effects split from the ledger | S3-11, S3-15 |
| Commit includes the wrong paths or damages the index | S3-13A, S3-13B, S3-14 |
| Dependency release selects the wrong work or auto-launches | S3-12 |
| Tracker updates the wrong record | S3-T1, S3-T2 |
| Semantic review is implied but absent | S3-08 |

## Stage-wide verification progression

Each task gives its narrow command. After the task's focused test passes, use
this progression only as far as its exit criteria require:

1. nearest new unit or integration test;
2. owning test module;
3. real-boundary temporary-Git, filesystem, or local-process class;
4. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`;
5. parse every JSON asset and fixture with the standard library;
6. parse changed Python with `ast.parse` without generating bytecode;
7. `git diff --check`;
8. `git status --short` and a task-scoped diff inspection.

Use bounded polling and process events, never arbitrary sleeps as the oracle.
No live model, networked check, dependency install, or SDK spike is required.

## Stage-wide stop conditions

Stop and ask the user if:

- S3-01 cannot enforce the persisted permission envelope with an available
  approved mechanism;
- a Stage 3 behavior requires changing version 1 policy/manifest semantics;
- a legitimate verification command requires shell syntax or unpersisted
  environment state;
- semantic review is required before its actor and interface are approved;
- exact-path commit cannot preserve unrelated staged/index/worktree state;
- recovery cannot distinguish intended side effects from external mutation;
- tracker mutation is requested without S3-T1;
- implementation needs a dependency, network, live model, new top-level
  structure, installed/cached skill edit, or destructive Git operation; or
- pre-existing user changes overlap the selected task's allowed files.

## Stage 3 exit criteria

Stage 3 is complete when:

- controller verification is independently observed and permission-bounded;
- decisions are immutable, and operation transitions preserve prepared intent
  and recorded effects while remaining bound to exact identities/digests;
- live or ambiguous processes cannot be resumed;
- resume and recovery preserve one-worker ownership and prior evidence;
- acceptance updates exactly one task through a prepared operation;
- tracker mode off performs no tracker write;
- commit mode off performs no commit, while exact-path mode preserves unrelated
  worktree/index state and records verified commit evidence;
- interrupted finalization reconciles deterministically;
- valid dependencies become ready in policy order without auto-launch;
- all focused and aggregate local checks pass without generated artifacts;
- `docs/stage-3-handoff.md` truthfully records results and remaining decisions;
  and
- no Stage 4/5 behavior, live model call, network use, or dependency install was
  added.
