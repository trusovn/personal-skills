# Task Acceptance Report: `S3-04` — Extend the Stage 3 state model

| Field | Value |
|---|---|
| Task ID | `S3-04` |
| Artifact status / verdict | `CHANGES_REQUESTED` |
| Producing stage | `task-acceptance-review` |
| Created at | `2026-07-17T12:45:29+01:00` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report path | `skills/task-orchestrator/docs/stage-3-tasks/S3-04-acceptance-report.md` |
| Task brief | `skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md`, SHA-256 `c3be72f8e5198c7618b5665cf451f7e8f839a63fc24379eff3f42c857d52f7d1` |
| Preflight packet | `/private/tmp/task-orchestrator-preflight/S3-04/execution-packet.md` |
| Implementer result | `/private/tmp/task-orchestrator-preflight/S3-04/worker-result.json`, status `complete`, schema valid |
| Run policy | `S3-04 explicit implementation envelope` in the task brief and Stage 3 plan |

## 1. Findings, ordered P0 through P3

### [P1] Derive the next revision from the persisted ledger, not caller input

| Field | Evidence |
|---|---|
| Current location | `skills/task-orchestrator/scripts/controller_state.py:467` |
| Triggering state/input | Call `apply_ledger_update()` on revision 1 with the correct `expected_revision=1` and an updater containing `{"revision": 0}` plus any otherwise valid change. |
| Consequence | The changed ledger is returned at revision 1 rather than revision 2. A later writer holding stale expectation 1 can therefore pass comparison and replace that change, defeating the monotonic revision and compare-before-write safety contract used by AC-07 and AC-08. |
| Evidence | REV-04 independently printed `before 1 after 1`. The updater is merged at line 467 and line 469 increments the updater-supplied value; `revision` is not protected by the immutable-field check. |
| Affected AC | `AC-07`, with knock-on risk to `AC-08` |
| Smallest corrective direction | Reject caller ownership of `revision` and always set the next value from the validated persisted revision; add pure and exact persisted-byte regression cases proving N becomes N+1 and a replay of N is rejected. |

### [P1] Enforce frozen transitions in the persisted update path

| Field | Evidence |
|---|---|
| Current location | `skills/task-orchestrator/scripts/controller_state.py:467` |
| Triggering state/input | Update a coherent ready ledger so task `T1` moves directly from `ready` to `accepted` while another task becomes ready, then persist through `apply_ledger_update()` / `controller.update_ledger()`. |
| Consequence | The real update boundary accepts a transition forbidden by `ALLOWED_TASK_TRANSITIONS` and bypasses `transition_task()`'s required accepting closure decision and identity checks. The transition tables are therefore advisory rather than executable persistence contracts. |
| Evidence | REV-05 independently printed `transition ready to accepted persistable_revision 2`. Lines 180–195 enforce the rule only when `transition_task()` is called; `apply_ledger_update()` validates the resulting snapshot but never compares previous and next run/task states through the frozen transition functions. |
| Affected AC | `AC-01`, `AC-07` |
| Smallest corrective direction | Make the ledger update boundary validate every changed run/task state against the frozen transition contracts, including the acceptance decision/identity requirement, and add negative unchanged-input and unchanged-byte tests for forbidden jumps. |

### [P1] Permit the next selected task after authorized accepted-task output

| Field | Evidence |
|---|---|
| Current location | `skills/task-orchestrator/scripts/controller.py:436` |
| Triggering state/input | Start a two-task run, reach a coherent post-acceptance `ready` ledger with `T1` accepted and dependent `T2` ready, retain ordinary accepted output in an allowed path, then invoke the public `run-next` command. |
| Consequence | `run-next` exits before `select_task()` because it still compares HEAD/status to the run-initial baseline. A normal first task's accepted output therefore prevents the required second dependency-ready task from launching. |
| Evidence | REV-06 used a disposable Git repository and public CLI and observed return code 2 with `Repository state has changed since initialization. Changed paths: allowed.txt`. The unchanged initial-baseline guard is at lines 436–453; the submitted integration suite has no post-acceptance second `run-next` occurrence. |
| Affected AC | `AC-06` |
| Smallest corrective direction | Add the task-required real post-acceptance second-occurrence test, then make the minimum authorized compatibility change that validates current Git state against existing controller-owned accepted evidence without weakening drift checks. If that needs new evidence fields or authority, stop and route to `task-brief-designer` as the brief requires. |

## 2. AC evidence matrix

| AC | Required invariant and oracle | Function/state/module evidence | Real public-entry and decisive-boundary evidence | Negative / unchanged-state evidence | Repeated / recovery evidence | Result and gap |
|---|---|---|---|---|---|---|
| `AC-01` | Every listed run/task edge succeeds and every unlisted edge rejects; oracle is the brief's frozen tables. | REV-01 reran 17 state tests; table/cartesian tests pass for `transition_run` and `transition_task`. | Controller compatibility aliases exist, but the persistence entry point bypasses both transition functions. | REV-05 proves forbidden `ready -> accepted` persists rather than rejecting unchanged. | Pure terminal-edge tests pass; persisted next occurrence is not protected. | `fail` — P1 transition-bypass finding. |
| `AC-02` | Running has one selected running task and one exclusively owned active attempt in its history. | Reviewed coherent and corruption fixtures; REV-01 passes missing selection, wrong state, absent ownership, and duplicate ownership cases. | REV-02/REV-03 exercise durable running state through the real controller and filesystem. | Duplicate owner and absent/wrong active attempt reject without input mutation. | REV-02 process test observes one durable attempt under contention. | `pass` |
| `AC-03` | Awaiting inspection has selected task, no active attempt, closure, and ordered later references. | REV-01 passes closure/reference prefix and corruption cases. | REV-10 real `init` + fake `run-next` reaches `awaiting_inspection` with a closure and no active attempt. | Missing closure, active attempt, wrong task state, and misordered references reject. | First closure publication is observed; later ordered-prefix validation is covered at module level. | `pass` |
| `AC-04` | Finalizing retains selected task awaiting inspection and requires all four ordered references. | REV-01 passes coherent finalizing fixture and missing-field/state corruptions. | Record-byte publication is expressly S3-05; S3-04's public boundary is structural ledger validation/update. | Missing/misordered references and an accepted selected task reject unchanged. | Repeated coherent read is deterministic; no S3-04 finalizing CLI exists by contract. | `pass` |
| `AC-05` | Resumable retains selection/current attempt without liveness; ready/stopped clear ownership. | REV-01 passes coherent state rows, transition edges, and corruptions. | REV-02 covers ready launch; later resume/stop commands are out of scope. | Missing resumable identity/history, live resumable attempt, and ready/stopped ownership reject. | Pure running/resumable/running state and transition evidence uses the same attempt history. | `pass` |
| `AC-06` | Initial and post-acceptance policy-order selection use persisted ready state and immutable completion authority. | Initial readiness and pure accepted-dependency selection tests pass; `completed_task_ids` remains unchanged. | Initial public flow passes in REV-10. REV-06 proves the real post-acceptance `run-next` exits at the initial-baseline guard before selecting T2. | Non-ready/incomplete selection rejects, but this does not cover legitimate accepted output. | Required second public occurrence fails in REV-06. | `fail` — P1 repeated-selection finding. |
| `AC-07` | Authority/history remain immutable; exact expected N updates once to N+1; stale replay preserves input/bytes. | Submitted stale/authority/history cases pass in REV-01. REV-04 proves caller-controlled `revision` can keep a changed ledger at N. | `controller.update_ledger()` delegates to the defective pure update before atomic replacement. | Existing stale and immutable-field tests pass, but omit caller-supplied `revision` and forbidden transitions. | N can remain N, so a stale N replay remains admissible. | `fail` — P1 revision and transition findings. |
| `AC-08` | One real process owns each mutation phase; competitor cannot duplicate work; stale reconciliation cannot overwrite. | Lock/revalidation code and deterministic test oracle were inspected. | REV-02/REV-03 independently reran the real two-process test: held-lock competitor loses, only attempt-001 launches, competing stopped ledger remains byte-identical after stale reconciliation refusal. | No duplicate attempt/worker and no stale overwrite are asserted. | First durable running occurrence, held/released competitor, competing update, and stale first-process reconciliation are all exercised. | `pass`, subject to AC-07 revision correction before relying on the revision invariant generally. |

## 3. Independent probes and command results

| ID | Exact command or probe | Working directory / environment | Purpose and ACs | Result and observed signal | Side effects / disposition | Independence or gap |
|---|---|---|---|---|---|---|
| `REV-BASE` | `git rev-parse HEAD && git status --short && shasum -a 256 ...` over every packet authority and scoped source/test path | Repository root; local filesystem | Baseline, authority, and scope reconstruction | Exit 0; HEAD and all authority/pre-existing-user digests matched; exact task-owned paths differed as expected. | None. | Independent baseline evidence. |
| `REV-DIAG-01` | `for path in ...; do git show ":$path" \| shasum -a 256; done ...` | Repository root; zsh | Initial index-digest attempt | Exit 127 after zsh's special `path` variable shadowed `PATH`; no digest claim taken from it. | None. | Failed diagnostic, rerun correctly as REV-DIAG-02. |
| `REV-DIAG-02` | `for file in ...; do git show ":$file" \| shasum -a 256; done && shasum -a 256 S3-04-result.md worker-result.json execution-packet.md` | Repository root | Separate index/worktree/artifact digests | Exit 0; all four index bytes matched preflight source/test digests; artifact digests recorded. | None. | Independent scope evidence. |
| `REV-01` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | Repository root; no network | AC-01 through AC-07 state evidence | Exit 0; 17 tests passed in 0.073s. | Temporary test directories cleaned; no repository artifacts. | Rerun independently; test oracles inspected. |
| `REV-DIAG-03` | `PYTHONDONTWRITEBYTECODE=1 python3 -c '... ControllerStateContractTest().ledger(); ...'` | Repository root | First revision probe setup | Exit 1 with `AttributeError` because fixture `setUp()` had not run. | None. | No behavioral conclusion; corrected in REV-04. |
| `REV-04` | `PYTHONDONTWRITEBYTECODE=1 python3 -c '... case.setUp(); ledger=case.ledger(); updated=apply_ledger_update(ledger,{"revision":0},...,expected_revision=1); print(...); case.tearDown()'` | Repository root; disposable temporary fixture | AC-07 monotonic revision oracle | Exit 0; `before 1 after 1`. | Temporary directory cleaned. | Independent focused defect reproduction. |
| `REV-02` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | Repository root; local Git/process/filesystem, Darwin `fcntl` | AC-03, AC-05 through AC-08 | Exit 0; 40 tests passed in 5.194s. | Temporary Git/run directories and processes cleaned. | Independently rerun; decisive contention test inspected. |
| `REV-03` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | Repository root; local-only aggregate | Transitive regression gate | Exit 0; 90 tests passed in 10.595s. | Temporary test artifacts cleaned; no repository artifacts. | Independent aggregate evidence. |
| `REV-05` | `PYTHONDONTWRITEBYTECODE=1 python3 -c '... ready ledger with T1/T2 ... apply_ledger_update(... T1 ready->accepted ..., expected_revision=1); print(...)'` | Repository root; disposable pure fixture | AC-01 persisted-transition oracle | Exit 0; `transition ready to accepted persistable_revision 2`. | Temporary directory cleaned. | Independent focused defect reproduction. |
| `REV-06` | `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY' ... initialize two-task disposable Git run; persist coherent accepted/ready state; retain accepted allowed-path output; invoke public run-next ... PY` | Repository root; disposable temp Git/run directories; fake local adapter; no network | AC-06 real post-acceptance next occurrence | Probe itself exited 0 after observing CLI return code 2 and `Repository state has changed since initialization. Changed paths: allowed.txt`. | All temporary repository/run/fake-adapter paths cleaned. | Independent public-entry defect reproduction; no submitted test covers this occurrence. |
| `REV-07` | `PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/scripts/controller.py --help` | Repository root | Public-command scope | Exit 0; exactly `init` and `run-next`. | None. | Independent compatibility evidence. |
| `REV-08` | Packet CMD-07 exact AST parse command | Repository root; no bytecode | Python syntax hygiene | Exit 0; no output. | None. | Independent hygiene evidence. |
| `REV-09` | Packet CMD-08 exact JSON parse command | Repository root | JSON asset hygiene | Exit 0; `parsed 4 JSON files`. | None. | Independent hygiene evidence. |
| `REV-10` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_full_init_and_run_next_flow` | Repository root; disposable Git/run/fake-worker boundary | Initial public occurrence; AC-03/06 | Exit 0; 1 test passed in 0.827s. | Temporary paths cleaned. | Independent rerun; complements failing next occurrence REV-06. |
| `REV-11` | `git diff --check` | Repository root | Scoped whitespace integrity | Exit 0; no output. | None. | Independent hygiene evidence. |
| `REV-12` | Worker-result Draft 2020-12 validation command recorded in the implementer result | Repository root; local `jsonschema` | Required result artifact consistency | Exit 0; `worker result schema valid`. | None. | Independently rerun against packet schema. |

## 4. Scope and baseline comparison

| Item | Preflight baseline | Current state | Classification and evidence |
|---|---|---|---|
| `HEAD` | `fd2e636cd7ea3320d2ca091198605427246b6a3b` | Same | Expected same-thread task state; no commit. |
| Exact `git status --short` | `?? .gitignore` | Pre-report review snapshot: ` M skills/task-orchestrator/scripts/controller.py`; ` M skills/task-orchestrator/scripts/controller_state.py`; ` M skills/task-orchestrator/tests/test_controller.py`; ` M skills/task-orchestrator/tests/test_controller_state.py`; `?? .gitignore`; `?? skills/task-orchestrator/docs/stage-3-tasks/S3-04-result.md` | Five expected task-owned changes plus preserved pre-existing user file; no unexplained path. This acceptance report is the separately authorized review output and was absent from the reviewed snapshot. |
| Dirty path index/worktree digests/states | `.gitignore`: index N/A, worktree `94df20...052d`; four tracked scoped paths had clean index/worktree bytes with packet digests `13228f...ec2d`, `9df1ba...a6948f`, `2f3528...760a`, `d5d249...958e5` | `.gitignore` unchanged; four index blobs still match those packet digests; worktrees are respectively `e2bf9f...ccaef`, `0fc094...1f37`, `4369a4...a0c8`, `54016a...c86`; result worktree `30ff1d...dd25`, index absent | User work is byte-separable and preserved. Tracked changes are unstaged task work; result is authorized untracked task output. |
| Task-owned paths | Four existing source/test paths plus new `S3-04-result.md` | Exactly those five paths; worker `files_changed` agrees | In scope. Reviewed full baseline-to-worktree diff: 597 insertions, 71 deletions across tracked files, plus the full new result document. |
| Runtime artifacts | Packet and worker result under `/private/tmp/task-orchestrator-preflight/S3-04/`; no repository runtime artifact | Same; review probes used temporary directories and cleaned them | Authorized; no residue. Acceptance report is the sole intentional review write. |
| Authority and policy | Brief, plan, controller contract, planning review, S3-02 result, README, schema, instructions, and environment recorded by packet | All recorded filesystem digests match; worker result is `complete` and schema-valid; `fcntl` boundary exercised | Unchanged authority. Packet is fresh for the expected same-thread implementation diff. |

## 5. Open questions

None.

## 6. Residual risks and unverified boundaries

| Risk or boundary | Evidence / reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| Advisory lock is single-host and run-local. | Explicitly frozen by the brief/plan; real Darwin process contention passed. | no | Stage 3 architecture owner; do not generalize in S3-04. |
| Reference containment and digest validation are not proved here. | Explicitly assigned to S3-05; S3-04 checks structural ordering only. | no | S3-05. |
| Original fail-first output is unavailable. | Worker result truthfully records the resumed checkpoint gap; independent review found current defects without reverting user/task work. | no | Same implementer thread should add regression tests that fail against the current defective behavior before correcting it. |

## 7. Verdict and next route

| Field | Value |
|---|---|
| Verdict | `CHANGES_REQUESTED` |
| Basis | Three independently reproduced P1 defects leave AC-01, AC-06, and AC-07 unsatisfied. AC-02 through AC-05 and AC-08 have proportionate independent evidence, and scope/baseline authority is clean. Passing 17-, 40-, and 90-test gates do not cover the failing persistence and second-occurrence contracts. |
| Next owner | same bounded-task-implementer thread |
| Exact next action | Correct the three findings within the existing S3-04 brief, allowed paths, helpers, dependencies, and permissions; add fail-first regressions at the pure/persisted and real post-acceptance public boundaries; rerun the packet's progressive gates; produce an updated worker result; then request a fresh acceptance review. If safe repeated selection requires new evidence fields or wider authority, stop and route that contract issue to `task-brief-designer` rather than weakening Git drift checks. |

- `CHANGES_REQUESTED` routes to the same implementer thread and requires a new acceptance review after correction.
