# Task Preflight Packet: `S3-04` — Extend the Stage 3 state model

## 1. Identity and status

| Field | Value |
|---|---|
| Task ID | `S3-04` |
| Artifact status | `ready` |
| Producing stage | `task-preflight` |
| Created at | `2026-07-17T11:22:48+01:00` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable packet path | `/private/tmp/task-orchestrator-preflight/S3-04/execution-packet.md` |
| Task brief | `skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md` |

`ready` means this packet is fresh and executable under the recorded policy.

## 2. Authoritative inputs and digests

All digests are lowercase SHA-256 digests of file bytes.

| Input | Identifier or path | Digest / value | Confirmed fact or decision |
|---|---|---|---|
| Task brief | `skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md` | `c3be72f8e5198c7618b5665cf451f7e8f839a63fc24379eff3f42c857d52f7d1` | Status is `ready_for_preflight`; bytes stayed unchanged. |
| Primary authority | `skills/task-orchestrator/docs/stage-3-plan.md` (`Entry contract`, `Settled decisions and constraints`, `Architecture assessment after S3-01 through S3-03`, `Durable Stage 3 records`, `Task execution contract`, `S3-04` row) | `8f30291bda35be1568dcc4f38efbfed70e3190b1bae1ddb7b5a3067166fd1d14` | Standard-library-only, sequential, single-worktree; state rules stay in `controller_state.py`, command locking stays in `controller.py`; no automatic next-task launch. |
| State authority | `skills/task-orchestrator/docs/controller-contract.md#State model` | `ec62a8356d02d61e20d9b9a4c63f12ad441706e127cc48a68b02abbbff175214` | Frozen task transitions and controller ownership boundaries. |
| Planning review | `skills/task-orchestrator/docs/stage-3-tasks/stage-3-tasks-04-08-review.md` | `bc8616742ae033b58fbe5cc8dbec22c8273a165fa7db611a10584f5a7e0e60cf` | S3-04 owns local per-run exclusion, expected revisions, exhaustive state/selection tests, and the real two-process boundary. |
| Dependency source | `skills/task-orchestrator/docs/stage-3-tasks/S3-02-result.md` | `6c075f1726ff200a6587f4e43ac6e618053dbad77b07bdf874bb194dc8a19cff` | `S3-02` is `complete`; its focused state baseline passed in this preflight. |
| Repository convention | `README.md` | `e27934f048a670e83c153a1b30b3f2080cbbe8e4c46d1272e0060fa8a76f4071` | Skill-owned source, tests, scripts, and docs remain inside `skills/task-orchestrator/`; no new top-level structure. |
| Repository instruction | Conversation-supplied `AGENTS.md` instructions for this root | `not_applicable` (not a filesystem file) | Explicit assumptions, surgical scope, one-command-at-a-time progressive verification, user-work preservation, and the stated soft budget apply. No repository `AGENTS.md` file exists in the current tree. |
| Run policy | `S3-04 explicit implementation envelope` in the task brief and Stage 3 plan | Task brief/plan digests above | Only named paths may change; no dependency install, network, live model, destructive Git, commit, tracker, installed-skill edit, or user-work rollback; two-strike and budget stops apply. |
| Worker result schema | `skills/task-orchestrator/assets/worker-result.schema.json` | `32effc1988202bb7b16280169c4914b7300d6632d22ac805827b517675fec9ac` | Structured worker result must validate against this schema. |
| Preflight instruction | `.agents/skills/task-preflight/SKILL.md` | `c948134987f6d1116312a777177a0f86620d90389c4c6b2d603182c09f7a95aa` | Read-only readiness and freshness rules used. |
| Oracle guidance | `/Users/mtrusov/.agents/skills/testing-discipline/SKILL.md` | `4a2221c5e8e6e4e7886e0da9c9ba7a911cefd224432daf08082b09c96ec86478` | Independent observable oracles, negative space, deterministic real-boundary evidence, fail-first proof. |
| Placement guidance | `/Users/mtrusov/.agents/skills/repo-foundation/SKILL.md` | `2f4ba173d73b84ead104e1793f1018135115e0158ab3a213ac6802476626d86e` | Existing source/test ownership and canonical `unittest` commands are confirmed; no new helper framework. |
| Environment fingerprint | `python3 --version`; `uname -srm`; `fcntl` probe | `Python 3.14.6`; `Darwin 25.5.0 arm64`; `flock=True, LOCK_EX=2, LOCK_NB=4` | The supported local platform exposes the required standard-library non-blocking advisory lock. |
| Current source/helper bytes | `controller_state.py`; `controller.py`; `test_controller_state.py`; `test_controller.py` | `13228f0b111829fce12509176c73a8f9584e287280899268b9a4f5b6d7feec2d`; `9df1bac6fcdf7b54fbad765634cc6e730c43223b8a354b0836923dcdb7a6948f`; `2f35281abdfb20d37d825125f9cc08c7462cba24f60e72a4e8e0bdc8dae8760a`; `d5d2497e7da52664babfffcea017caf5d9b67a7fef9a679941b457f0ad4958e5` | Exact implementation and task-local test interfaces inspected by preflight. |

## 3. Repository baseline and dirty-path ownership

| Field | Value |
|---|---|
| `HEAD` | `fd2e636cd7ea3320d2ca091198605427246b6a3b` |
| Exact `git status --short` | `?? .gitignore` |
| Baseline recaptured after packet write | `unchanged` |
| Packet-path neutrality | Outside repository at `/private/tmp/task-orchestrator-preflight/S3-04/execution-packet.md`; repository status unchanged before/after write. |
| Incidental check artifacts | None; commands used `PYTHONDONTWRITEBYTECODE=1` where Python imports/tests could otherwise create bytecode. |

| Status entry / path | Index blob SHA-256 or state | Worktree SHA-256 or state | Ownership | Task overlap | Evidence / disposition |
|---|---|---|---|---|---|
| `?? .gitignore` | `not_applicable` | `94df20a272b459fd0ed54eef4635d0d3b89150e77f2f7d89564ad18ca22c052d` | User (pre-existing and named by the task brief) | `no` | Preserve exactly; it is outside every S3-04 allowed path. |

## 4. Entry criteria and dependency evidence

| Criterion | Required state | Observed evidence | Result | Owner if failed |
|---|---|---|---|---|
| Brief status | `ready_for_preflight` | Task brief identity table and unchanged digest | `pass` | `task-brief-designer` |
| S3-02 dependency | Complete and focused pure-state baseline passes | `S3-02-result.md` says `complete`; CMD-02 passed 12 tests | `pass` | Stage 2 / S3-02 |
| Stage 2 fake flow | `init` + fake `run-next` reaches `awaiting_inspection` | CMD-01 passed at the real subprocess, temporary-Git, and run-directory boundary | `pass` | Stage 2 |
| No later Stage 3 CLI | Only `init` and `run-next` exist | CMD-05 output lists exactly `{init,run-next}`; parser definitions only at `controller.py:367,374` | `pass` | Task design |
| Allowed files/helper interfaces | Exist and do not overlap user edits | Four allowed existing files resolved; `write_fake_codex` at `test_controller.py:1198`; no dirty allowed path | `pass` | Task preflight |
| Local lock mechanism | Standard-library non-blocking process lock is available | Darwin `fcntl.flock`, `LOCK_EX`, and `LOCK_NB` probe succeeded | `pass` | Platform / task preflight |
| Focused and aggregate baseline | Local commands pass without generated repository artifacts | CMD-02, CMD-03, CMD-04, CMD-06, CMD-07, CMD-08 | `pass` | Task preflight |

## 5. Confirmed scope and prohibited paths

| Item | Confirmed contract and evidence |
|---|---|
| Allowed paths | `skills/task-orchestrator/scripts/controller_state.py`; `skills/task-orchestrator/scripts/controller.py` only for initialization/readiness, repeated `run-next`, expected-revision persistence, and the per-run command lock; `skills/task-orchestrator/tests/test_controller_state.py`; `skills/task-orchestrator/tests/test_controller.py` only for corresponding state/command/process tests; new `skills/task-orchestrator/docs/stage-3-tasks/S3-04-result.md`. |
| Read-only context | This packet's authoritative input paths, the current four source/test files, and the worker-result schema. |
| Prohibited paths/work | No task brief/master-plan edits; no new CLI commands; no retry/resume/recover/stop/inspect/accept implementation; no policy/manifest changes; no record validators owned by S3-05; no Git-observation redesign; no generalized storage/workflow/locking abstraction; no unrelated cleanup. |
| Pre-existing user work | `.gitignore` remains user-owned and byte-for-byte preserved. |
| Missing or wider scope request | None. If deterministic contention requires a shared harness, new module, or paths outside this table, stop and route to `task-brief-designer`. |

## 6. AC execution plan

| AC | Invariant and oracle | Positive evidence | Negative / unchanged evidence | Real entry point and boundary | Repeated / recovery path | Exact command reference | Executable? |
|---|---|---|---|---|---|---|---|
| AC-01 | Frozen run/task transition tables are exhaustive; independent oracle is membership in the brief's explicit tables. | Every listed edge returns the requested state. | Cartesian-product every unlisted edge; all edges from run `stopped` and task `accepted`/`stopped` reject. | Public pure transition functions in `controller_state.py`, with sampled compatibility aliases in `controller.py`. | Legal edge followed by illegal/terminal edge. | CMD-02 | `yes` — module command passed baseline; task-local table tests are authorized. |
| AC-02 | `running` has exactly one selected `running` task and one active attempt owned only by its append-only history. | One coherent running ledger validates. | Missing/wrong selection, absent history membership, or duplicate owner rejects without mutating input. | `validate_ledger` / pure update API. | Append attempt, enter running, then reject a second owner. | CMD-02 | `yes` — pure state fixture boundary exists. |
| AC-03 | `awaiting_inspection` has one selected task, no active process/attempt, required closure, and ordered later references. | Closure-only and ordered publication prefixes validate. | Missing closure, live attempt, wrong state, or reversed reference dependency rejects. | Pure validator plus existing fake `run-next` filesystem/subprocess flow. | First closure publication then next ordered-reference validation. | CMD-01, CMD-02, CMD-03 | `yes` — exact fake flow passed. |
| AC-04 | `finalizing` requires closure, verification, decision, prepared operation, while selected task remains `awaiting_inspection`. | Complete coherent finalizing fixture validates. | Missing/misordered reference or already-accepted selected task rejects unchanged. | `validate_ledger` and expected-revision pure update; paths are structural only in S3-04. | Prepare once, then repeated read preserves pre-acceptance state. | CMD-02 | `yes` — independent table/fixture oracle; record-byte semantics remain S3-05. |
| AC-05 | `resumable` retains selected/current attempt without liveness; `ready` and `stopped` clear selection/active attempt. | `running -> resumable -> running` retains identity; coherent ready/stopped validate. | Missing resumable identity, live resumable attempt, or active ready/stopped ownership rejects. | Pure lifecycle plus fake local command boundary for ready launch. | Same attempt across resumable round trip. | CMD-02, CMD-03 | `yes` — pure and process boundaries exist. |
| AC-06 | Readiness/selection uses persisted `ready` state in policy order and derives completion from immutable manifest IDs plus accepted task entries. | Multi-task initial choice, legitimate acceptance/recompute, then next choice. | Non-ready selection, unmet dependency, no-ready run, or `completed_task_ids` rewrite rejects. | Pure selection/update API plus public `init`/`run-next` filesystem flow. | Initial selection, accepted-state change, recomputation, next selection without auto-launch. | CMD-02, CMD-03 | `yes` — local manifest/temp-run fixtures and fake worker exist. |
| AC-07 | Authority/history are immutable and expected revision is compared before replacement. | Exact revision N updates to N+1 once. | Changed authority/order, truncated history, duplicate ownership, or stale N replay leaves caller and persisted bytes unchanged. | `apply_ledger_update` plus `controller.update_ledger` atomic filesystem boundary. | Apply N once, replay N against N+1. | CMD-02, CMD-03 | `yes` — existing byte-preservation tests and temp run directories exist. |
| AC-08 | One process owns each mutation phase; stale reconciliation compares before write. | Process A persists one running attempt, releases only while event-controlled fake worker waits, then safely reacquires. | Process B loses held lock; after release sees `running` and cannot allocate; a competing valid update makes A refuse stale reconciliation without overwrite. | Real `controller.py run-next` subprocesses, `fcntl.flock`, local filesystem, temporary Git repository. | Second command during held phase, then competing update during A's wait. | CMD-03, CMD-04 | `yes` — subprocess/temp-Git/fake-worker interfaces exist; task brief explicitly authorizes adding one-use event/bounded-polling controls in `test_controller.py`. |

Oracle assessment: all decisive state oracles compare behavior to the frozen tables/invariants rather than mirroring production logic. AC-03/06/07/08 cross their real filesystem/process boundaries. Negative space includes unchanged input/bytes, no duplicate attempt/worker, and no stale overwrite. Repeated lifecycle paths are explicit. Tests must use events or bounded polling, never sleeps, and remain network-free and deterministic.

## 7. Legacy-assumption findings

| Entry point / search | Exact relevant location | Finding | Implementation follow-through | Brief defect? |
|---|---|---|---|---|
| Transition/state literals | `controller_state.py:16-24,344-390` | Task transitions exist, but ledger run/task state sets omit `resumable`, `finalizing`, and task `accepted`; only `last_closure_path` exists. | Centralize the frozen run table, retain task table, add only the four brief-authorized nullable references, and exhaustively test both tables. | `no` |
| `select_task` | `controller_state.py:329-341` | It only accepts run `initialized`, derives readiness solely from manifest-completed IDs, and does not require persisted task state `ready`. | Permit only approved ready-run occurrences, derive accepted IDs without mutating `completed_task_ids`, and select the first persisted-ready task in policy order. | `no` |
| Pure/persisted updates | `controller_state.py:392-409`; `controller.py:348-354` | Revision increments, but neither API accepts a caller-supplied expected revision; immutable task comparison is incomplete. | Add exact expected-revision validation before replacement and compare all brief-frozen immutable authority/history fields. | `no` |
| Initialization | `controller.py:223-333` | Ledgers initialize every task and the run as `initialized`, with only one Stage 3 reference field. | Compute dependency-ready task states/run `ready`; add exactly the four nullable Stage 3 references for newly initialized ledgers. | `no` |
| `run-next` fixed first-occurrence assumptions | `controller.py:395-534`; fixed `task-001.json` at 456, `attempt-001` at 480, single-attempt guard at 500 | Current path assumes first selection and one attempt and compares against the initial baseline. | Make only the minimum repeated-selection compatibility changes; do not weaken drift checks or invent Git-evidence authority. Stop if new evidence fields are needed. | `no` |
| Mutation sequence | `controller.py:198-216,348-354,395-534,660-673` | Attempt/artifact writes and ledger replacements have no per-run lock, so revision validation alone cannot exclude another process. | Hold one run-contained non-blocking descriptor lock through validation, allocation/artifacts, and durable `running`; reacquire and compare exact state/revision before terminal reconciliation. | `no` |
| Public CLI | `controller.py:360-381`; CMD-05 | Only `init` and `run-next` exist. | Preserve public command set; do not implement later Stage 3 commands. | `no` |
| Test/helper placement | `test_controller_state.py:33-370`; `test_controller.py:1149-1471`, especially `write_fake_codex` at 1198 | Exact pure fixtures, persisted-byte oracle, temp Git/run directories, subprocess CLI calls, and fake worker already live in the owning test files; the fake is not yet event-controlled. | Extend these files task-locally; add no shared harness. Use event/control files or bounded polling for cross-process timing. | `no` |

## 8. Verification helpers and exact commands

### Helper and oracle inventory

| Capability | Exact path / interface | Existence evidence | Authorized and usable? | Disposition |
|---|---|---|---|---|
| Pure ledger fixture | `tests/test_controller_state.py::ControllerStateContractTest.ledger` | Current fixture used by passing 12-test module | `yes` | Extend task-locally for coherent state rows. |
| Pure/persisted unchanged-byte oracle | `test_invalid_ledger_update_leaves_input_unchanged`; `test_rejected_controller_update_leaves_persisted_bytes_unchanged` | Both collected by CMD-02 | `yes` | Extend for stale revision and immutable authority. |
| Real fake-worker flow | `tests/test_controller.py::ControllerIntegrationTest.write_fake_codex` and `test_full_init_and_run_next_flow` | CMD-01 passed at subprocess/temp-Git/run-directory boundary | `yes` | Extend task-locally with deterministic wait/release controls. |
| Separate controller processes | Standard-library `subprocess`; CLI at `scripts/controller.py` | Existing tests invoke CLI subprocesses; CMD-01/CMD-03 passed | `yes` | Launch two `run-next` processes in one test only. |
| Local advisory lock | `fcntl.flock(fd, LOCK_EX | LOCK_NB)` | Environment probe succeeded on Darwin | `yes` | Implement run-contained descriptor-held lock in `controller.py`; no abstraction/module. |
| Canonical runner | Standard-library `unittest` from repository root | CMD-01 through CMD-04 passed | `yes` | Use commands below in order. |

### Commands

| ID | Class / cost | Exact copy-pasteable command | Working directory | Required environment | Purpose / ACs | Expected signal | Run? | Result | Broader authorization required? |
|---|---|---|---|---|---|---|---|---|---|
| CMD-01 | `entry; cheap/local` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_full_init_and_run_next_flow` | `/Users/mtrusov/work/skill-sources/personal-skills` | Local Git, subprocess, temp directory; no network | Stage 2 fake flow / AC-03, AC-06 | One test passes and reaches `awaiting_inspection` | `yes` | Exit 0; 1 test passed in 0.719s | `no` |
| CMD-02 | `fail-first + targeted; cheap/local` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | same repository root | None beyond Python stdlib | AC-01 through AC-07 pure/state evidence. After adding the first new test, run this before implementation and require the intended assertion to fail; after implementation require all tests to pass. | Pre-change baseline exit 0; fail-first nonzero for intended missing behavior; final exit 0 | `yes` | Baseline exit 0; 12 tests passed in 0.057s | `no` |
| CMD-03 | `targeted; cheap/local` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | same repository root | Local Git, subprocess, temp directories, Darwin `fcntl`; no network | AC-03 and AC-05 through AC-08 command/filesystem/process evidence | Exit 0; all module tests pass with deterministic contention coverage | `yes` | Baseline exit 0; 39 tests passed in 3.492s | `no` |
| CMD-04 | `broader; local` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | same repository root | Existing task-orchestrator local capabilities; no live model/network | Transitive task-orchestrator regression gate | Exit 0 | `yes` | Baseline exit 0; 84 tests passed in 9.381s | `no` |
| CMD-05 | `entry/compatibility; cheap/local` | `PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/scripts/controller.py --help` | same repository root | None | Prove no later Stage 3 public command exists / scope check | Usage lists exactly `init` and `run-next` | `yes` | Exit 0; exact command set confirmed | `no` |
| CMD-06 | `hygiene; cheap/local` | `git diff --check` | same repository root | None | Whitespace integrity for scoped change | Exit 0, no output | `yes` | Exit 0, no output | `no` |
| CMD-07 | `hygiene; cheap/local` | `PYTHONDONTWRITEBYTECODE=1 python3 -c 'import ast; from pathlib import Path; paths=("skills/task-orchestrator/scripts/controller_state.py","skills/task-orchestrator/scripts/controller.py","skills/task-orchestrator/tests/test_controller_state.py","skills/task-orchestrator/tests/test_controller.py"); [ast.parse(Path(path).read_text(), filename=path) for path in paths]'` | same repository root | None | Parse every task-owned Python candidate without bytecode | Exit 0, no output | `yes` | Exit 0, no output | `no` |
| CMD-08 | `hygiene; cheap/local` | `python3 -c 'import json; from pathlib import Path; paths=sorted(Path("skills/task-orchestrator").glob("**/*.json")); [json.loads(path.read_text()) for path in paths]; print("parsed", len(paths), "JSON files")'` | same repository root | None | Preserve parseability of the four task-orchestrator JSON assets | Exit 0 and `parsed 4 JSON files` | `yes` | Exit 0; `parsed 4 JSON files` | `no` |

Implementation verification order: establish fail-first evidence with CMD-02; make the minimum implementation; rerun CMD-02; run CMD-03; then CMD-04, CMD-07, CMD-08, CMD-06; finish with exact `git status --short` and a task-scoped diff inspection. Do not run commands in parallel.

## 9. Permission and commit envelope

| Action | Policy decision | Evidence / limit |
|---|---|---|
| Repository writes | Allowed only in the five path entries listed in Section 5 after freshness comparison | Task brief `Scope and boundaries` |
| Dependency changes / install | Prohibited | Task brief mutation limits; Stage 3 plan task execution contract |
| Network / live services | Prohibited | Task brief mutation limits; no command above needs network |
| Privileged / destructive action | Prohibited | No destructive Git cleanup, user rollback, or privileged action |
| Slow / flaky verification | Approval required before any check outside the exact local commands above | Conversation instructions and task brief escalation rules |
| Commit / push | Prohibited | Task brief mutation limits; no commit is authorized |
| Stop / budget policy | Two materially different failed fixes for the same targeted behavior => stop. At 24 tool calls, 70 minutes, or 80k input, assess and hand off if likely to cross the hard `30 calls / 90 minutes / 100k` envelope. | Task brief `Effort, budget, and escalation` |

## 10. Risks, gaps, and stop conditions

| Risk or gap | Evidence | Effect on verdict | Owning stage / person | Smallest next action |
|---|---|---|---|---|
| Local lock is single-host only | Stage 3 plan and planning review explicitly freeze this boundary | Authorized residual gap; does not block | Stage 3 architecture owner | Keep `fcntl` lock local/run-contained; do not generalize. |
| Event-controlled fake worker is not yet present | Existing `write_fake_codex` helper is local and synchronous | Does not block; the brief explicitly authorizes one-use task-local extension | S3-04 implementer | Add deterministic control files/events and bounded polling inside `test_controller.py`; no shared harness. |
| Repeated selection may collide with current initial-baseline drift guard | Fixed initial comparison and first-occurrence names found in `controller.py:395-500` | Stop condition if minimum compatibility cannot preserve safety | `task-brief-designer` / Stage 3 owner | Do not bypass checks; report exact missing authority/field and repair the brief. |

- Stop before the first edit if any recorded digest, `HEAD`, Git status entry, index state/digest, worktree state/digest, dependency source, instruction source, run-policy source, or environment fingerprint changed without explanation.
- Stop on dirty overlap, scope widening, missing authority/helper/oracle, undeclared infrastructure, an unapproved required check, or a need to migrate/rewrite an existing ledger/artifact.
- Stop if the lock is unavailable/unenforceable, contention cannot be observed deterministically, repeated selection needs weakened Git drift checks/new evidence fields, or any lifecycle needs an unlisted transition/reference combination.
- Route contract defects or wider paths to `task-brief-designer`; route stale/current-state failures through a fresh `task-preflight`.

## 11. Implementer instructions and required result format

1. Re-read the listed instructions and compare every freshness value, including `.gitignore`'s worktree digest, before the first edit. Route any unexplained change back to `task-preflight`.
2. Change only the confirmed allowed paths and preserve all pre-existing user work. Do not create undeclared shared infrastructure or widen scope.
3. Add the highest-risk task-local tests first. Run CMD-02 and prove the new test rejects pre-change behavior for the intended assertion; leave no temporary mutation. Implement the minimum task, then follow the exact command order in Section 8.
4. Preserve compatibility names and the current functional split. Use a run-contained descriptor-held non-blocking local lock, deterministic process events or bounded polling, and exact expected-revision comparison before replacement/reconciliation.
5. Follow the permission, no-commit, checkpoint, two-strike, and stop envelope. Stop at S3-04 before any S3-05/S3-09/later behavior.
6. Create `skills/task-orchestrator/docs/stage-3-tasks/S3-04-result.md` with the brief-required transition/coherence tables, reference compatibility, lock lifetime, exact command results, and residual risks.
7. Write the structured result to `/private/tmp/task-orchestrator-preflight/S3-04/worker-result.json` and validate it against `skills/task-orchestrator/assets/worker-result.schema.json`. Report exact files changed, AC evidence, every command and truthful outcome, local decisions, questions, residual risks, status, and exact next action. Submission is not acceptance.

