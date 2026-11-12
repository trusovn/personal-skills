# Task Review Discovery Report: T-004.1 — staged producer boundary

| Field | Value |
|---|---|
| Producing stage | task-review-discovery |
| Coverage completeness | complete — all 48 preserved required/material rows have current evidence |
| Discovery iteration | 3; fresh independent staged discovery after supported-host evidence became available |
| Created at | 2026-11-12T15:28:10.656370+00:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report | skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-03.md |
| Task brief | skills/task-orchestrator/docs/tasks/T-004.1/brief.md revision 1 |
| Preparation/context | sibling verification.md revision 1, preflight.md including Decision context, controller-contract.md; parent T-004/brief.md; skills/task-orchestrator/docs/direction-single-task-sbx.md; cited ART-003/005 and accepted T-003 successor contract/acceptance-02 |
| Submission | sibling implementation-report.md and correction-01.md; reviews/maintainability-03.md and contract-registry-02.md |

Evidence only: no acceptance verdict, approved deferral or advancement. This report applies only to the identified reviewed bytes and does not review or authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production, tests or existing task artifacts. Independent evidence authority: yes. The active task-review-discovery and testing-discipline skills were read from the project-local `.agents/skills/` installation; it was not refreshed. No delegation, production/test edits, staging, commits, dependencies, provider or external-network probes occurred. Local loopback is used only by the approved containment fixture. The sole repository write is this report. Disposable probe sources, frozen/reconciled ledgers and raw logs are retained under `/tmp/t0041-discovery03*`.

HEAD `aa99736e0fb02733d07e62aa382dbcee2ae46f1b`. Complete staged binary diff SHA-256 `f9f5271abf3987177e1e1bc5162025b242c91c8d1233e72eab63b7e1b9349871`. Complete unstaged binary diff SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty diff). All 28 staged paths were independently read from the index and compared byte-for-byte to the worktree. Current reviewed implementation agrees with maintainability-03's seven file hashes. Historical discovery-02 reviewed a mixed staged/unstaged snapshot; its result labels are navigation only. Current identities and probes below replace those labels for this pass.

## 2. Findings and continuity

No findings.

F-01 (prior suggested P2, AC-01/V-02b) has current correction evidence: exact same-porcelain dirty owner chmod returns blocked, `scope_or_owner_work_violation`, owner.txt; mode remains 0755, with no repair or overwrite. Five public positive/negative sibling cases cover dirty files inside/outside allowed paths and symlink referent content/executable mode. Hidden staged-owner drift also refuses. Correction owner: implementer; current evidence owner: discovery iteration 3; disposition authority: separate acceptance. No new disposition is made here.

G-01 (prior conditional evidence gap) has current evidence in maintainability-03 and independently verified B/R/current identities. M-01..M-11 rationale dispositions and analyzer limits remain explicit. Radon/Ruff metrics do not prove behavior; native architecture and registry checks were separately rerun. No general maintainability review was repeated. Structural evidence owner: maintainability reviewer; registry synchronization owner: registry updater; current admission evidence owner: this discovery; decision owner: separate acceptance.

V-07d/e were blocked in discovery-02 and acceptance-01 because the host was Linux. Both now have current macOS evidence. The initial containment attempt failed before its oracle at the agent sandbox's loopback bind (`PermissionError`); the exact focused test was rerun with approved escalation and passed. The failed setup is retained, not counted as containment evidence or a product defect. Launch-failure refusal is separately controlled at capability response, paired with actual containment. No requirement was waived.

## 3. Completeness ledger

All rows consume the matching submitted scenario claim in implementation-report.md/correction-01.md. Prior is discovery-02's **current result**, not its historical prior-status column. Before broad execution all 48 IDs were retained in `/tmp/t0041-discovery03/ledger-before.txt`; reconciliation in `ledger-reconciled.txt` confirmed no selected probe remained. Every required/material row is below; no optional concern is substituted for required coverage.

Setup/oracle: P1/ACTOR/MATRIX/IGNORED use disposable real Git repositories, external controller run directories and actual local fake-Codex terminal producers followed by public inspection/reservation/check APIs. Commands read actual product bytes; independent hashes, invocation counters, raw records/logs, stale/refusal statuses and byte-identical ledgers are the oracles. GIT exercises real unusual paths/renames/deletes/index changes. RUNNER/EXTRA/LIFECYCLE use real argv/process/log boundaries; mocks control only authorization-negative inputs or explicit failure/publication boundaries. CAPABILITY exercises actual macOS sandbox-exec, including permitted/denied local loopback and filesystem actions. REVISION and UPSTREAM use existing public revision/live-owner fixtures. G-01 uses reviewer artifact identities and native checks. No schema/configuration-only check is called behavioral proof.

| Row | AC/invariant | Explicit cases | Prior | Current independent probe / oracle | Result |
|---|---|---|---|---|---|
| V-01 | AC-01 | Terminal producer; real tracked bytes; literal paths; actor claims grant no pass | pass | P1 independently hashes actual allowed.txt; GIT unusual literal paths; ACTOR actual terminal producer, no actor-summary authority. | pass |
| V-02a | AC-01 | Unchanged dirty owner setup remains intact while allowed clean file changes | pass | ACTOR dirty-owner controls first inspect unchanged owner and pass; allowed clean file changes remain separate. | pass |
| V-02b | AC-01 | Dirty allowed content change; hidden staging change; dirty file mode change | pass | P1 same-porcelain owner chmod is blocked; ACTOR five inside/outside owner mode/referent controls and hidden staged-owner regression; MATRIX dirty_allowed blocks. No ledger mutation or check launch. | pass |
| V-02c | AC-01 | New tracked change outside scope | pass | MATRIX outside_tracked blocks, preserving actual files. | pass |
| V-02d | AC-01 | New untracked change outside scope | pass | ACTOR scope_and_invalid_timeout adds outside.txt and blocks without launch. | pass |
| V-03a | AC-01/02 | Wrong stage, absent/wrong operation; wrong run/task | pass | ACTOR assignment_refusals wrong-stage/absent operation refuses; current inspect_candidate checks terminal stage and validates admitted raw complete outcome. | pass |
| V-03b | AC-01/02 | Wrong stage, absent/wrong operation; wrong run/task | pass | ACTOR assignment_refusals wrong run/task/operation refuses with unchanged ledger and no check counter. | pass |
| V-03c | AC-01/02 | Wrong input/policy/flow/baseline binding | pass | ACTOR assignment_refusals independently varies input/policy/flow binding. Current baseline digest guard traced; EXTRA valid older frozen dirty baseline refuses with no candidate/ledger/check mutation. | pass |
| V-03d | AC-01/02 | Live or unknown upstream actor cannot establish stable candidate/check | pass | UPSTREAM live actor control and current _active_actor guard before candidate publication prevent overlapping stable candidate. | pass |
| V-03e | AC-01/02 | Live or unknown upstream actor cannot establish stable candidate/check | pass | UPSTREAM unknown/nonterminal actor control; ACTOR unknown check intent and before/during interruption retain ownership without relaunch. | pass |
| V-03f | AC-01/02 | Second check/inspection while real check owns command lock | pass | ACTOR synchronized real checking holds RunCommandLock; replacement check and inspection refuse. | pass |
| V-04a | AC-02 | Same-size tracked bytes change after passing check | pass | P1 executes pass then same-size tracked mutation; status and replay stale, counter unchanged. | pass |
| V-04b | AC-02 | Visible untracked modify/add/remove independently | pass | MATRIX untracked_modify/add/remove each execute real pass first, then stale admission with unchanged ledger and counter. | pass |
| V-04c | AC-02 | Index-only change, HEAD/baseline drift | pass | MATRIX index-only change invalidates actual pass; GIT HEAD/index identities and current workspace/baseline comparisons traced. | pass |
| V-04d | AC-02 | Evaluated configuration bytes change | pass | MATRIX configuration mutation and IGNORED explicit evaluated input mutation invalidate evidence. | pass |
| V-04e | AC-02 | Approved task-input/policy/flow revisions | pass | REVISION8 approved input/policy/flow revision controls; current _producer_context and _load_current_candidate compare frozen bindings. | pass |
| V-05a | AC-02 | Irrelevant ignored generated output leaves candidate current | pass | IGNORED generated history: actual check writes irrelevant ignored output and remains passed/current. | pass |
| V-05b | AC-02 | Ignored evaluated input drift before checking refuses eligibility | pass | IGNORED before history: changed explicit ignored input makes status stale and reserve refuses without launch. | pass |
| V-05c | AC-02 | Ignored evaluated input changes at synchronized real-process checkpoint | pass | IGNORED during history: actual process checkpoint, input change, release; zero exit yields stale. | pass |
| V-06 | AC-03/04 | Actual argv, logs, exit, environment, candidate; replacement-process replay | pass | P1 real public check plus actual valid/invalid execution validator; ACTOR API/replacement CLI replay; RUNNER binary stdout/stderr, literal argv and ordered multi-command execution. | pass |
| V-07a | AC-03 | Exact explicit frozen YOLO authority versus absent/incomplete/invalid | pass | RUNNER exact explicit sbx/YOLO object executes real direct argv and records sbx_yolo; P1 public frozen policy path. | pass |
| V-07b | AC-03 | Exact explicit frozen YOLO authority versus absent/incomplete/invalid | pass | RUNNER absent authority selects legacy sandbox; incomplete/false/integer-yolo/other transport matrix refuses before marker or artifact; ACTOR legacy/unauthorized launch guards traced. | pass |
| V-07c | AC-03 | Legacy policy on unsupported host refuses without fallback | pass | RUNNER controlled Linux platform/missing-executable refusal uses production sandbox builder, without YOLO fallback. | pass |
| V-07d | AC-03 | Legacy launch-capability failure and real supported restrictive containment | blocked | LAUNCH-FAILURE actual production legacy argv, controlled nonzero capability preflight: UnsupportedSandbox, zero Popen calls, no marker/artifact. This proves refusal/selection, not containment; paired with CAPABILITY. | pass |
| V-07e | AC-03 | Legacy launch-capability failure and real supported restrictive containment | blocked | CAPABILITY approved actual macOS sandbox-exec: workspace roots allowed, outside/read-only writes denied, loopback allowed/denied as configured, explicit full-access write permitted. RUNNER exact invocation and permission validation controls pass. | pass |
| V-08a | AC-03 | Prohibited shell/malformed commands, invalid later command before any launch | pass | RUNNER closed shell/launcher/parser tables and ACTOR invalid_later_command refuse all-command plan before any invocation. | pass |
| V-08b | AC-03 | Forbidden install versus explicit permission; planning only | pass | RUNNER recognized install denial table; no package command executed. | pass |
| V-08c | AC-03 | Forbidden install versus explicit permission; planning only | pass | RUNNER explicit install-allowed planner control only; no install or network execution claimed. | pass |
| V-08d | AC-03 | Quoted literal argv and near-miss non-install | pass | RUNNER near-miss parser controls and real literal/quoted argv command writes expected marker and exact binary logs. | pass |
| V-09a | AC-04 | Real wrong product exits nonzero without correction charge | pass | P1 independently sets wrong product and gets failed; ACTOR failed_product shows actual nonzero exit and no correction charge. | pass |
| V-09b | AC-04 | Missing required executable blocks before any command | pass | ACTOR missing_later_executable blocks all commands before first counter; receipt and unknown operation retain precise intervention. Arbitrary output text is not an infrastructure classifier. | pass |
| V-09c | AC-04 | No check evidence is missing/not-run, never passed | pass | P1 candidate inspection creates no successful verify evidence; current _evidence_view missing default and check empty-outcome not_run branch traced. | pass |
| V-09d | AC-04 | Known issue cannot excuse required failed check | pass | Current check_candidate clears authorized_gap before plan execution; P1 actual required product failure remains failed; RUNNER planner/targeted failure controls. | pass |
| V-09e | AC-04 | Targeted-only repository gate omission is explicit | pass | ACTOR targeted-only receipt explicitly lists repository_gate omission; required task check actually executes. | pass |
| V-09f | AC-04 | Failure stops later command | pass | EXTRA direct production YOLO and RUNNER failure-before-later-marker controls: one failed outcome, later marker/log absent. | pass |
| V-10a | AC-02/04 | Tracked evaluated drift at real check checkpoint | pass | ACTOR synchronized check mutates tracked bytes while real command waits; exit zero is recorded but receipt stale. | pass |
| V-10b | AC-02/04 | Visible untracked evaluated drift during check | pass | Same ACTOR checkpoint also creates a visible untracked evaluated file; IGNORED independently varies evaluated input before/during; complete workspace comparison covers visible untracked changes. | pass |
| V-10c | AC-02/04 | Check side effect modifies evaluated input despite zero exit | pass | ACTOR check_side_effect actual command edits allowed input and exits zero; no current pass. IGNORED during corroborates pre/post evaluated identity. | pass |
| V-10d | AC-03/04 | Finite timeout, descendants, resistant child, exited parent/open pipe | pass | RUNNER real timeout, resistant grandchild and exited-parent/open-pipe controls; LIFECYCLE independently observes process groups disappear and captured inherited pipes close within bounded waits. | pass |
| V-10e | AC-02/03 | Zero/negative/NaN/infinite/nonnumeric/boolean timeout refuses without launch | pass | ACTOR zero/negative/NaN/infinity/string/boolean timeout matrix refuses with unchanged authoritative ledger and no counter. | pass |
| V-11a | AC-02 | Completed API/CLI/reloaded replay executes exactly once | pass | P1 pass/replay under same identity executes once; new reservation executes again; ACTOR replacement CLI/API replay preserves receipt/logs and ledger. | pass |
| V-11b | AC-02/03 | Real controller killed before launch/during synchronized command; replay cannot relaunch | pass | ACTOR killed coordinator after unknown intent before launch; replay blocked, no marker, no second reservation. | pass |
| V-11c | AC-02/03 | Real controller killed before launch/during synchronized command; replay cannot relaunch | pass | ACTOR killed coordinator during synchronized real command; release lets original command finish, invocation once; replay blocked and no overlap. | pass |
| V-11d | AC-02 | Receipt published before ledger result; reload reconciles without rerun | pass | ACTOR killed coordinator after complete check receipt before ledger completion; reload reconciles original result with invocation once. | pass |
| V-11e | AC-02/03 | Existing log collision and injected publication failure | pass | ACTOR existing log collision preserves bytes/no launch; EXTRA production YOLO stream-write fault cannot publish complete execution record. RUNNER publication/collision controls pass. | pass |
| V-12 | AC-01/02/04 | Real failure -> admitted correction -> new pass; old receipt immutable; charge only correction | pass | ACTOR real failed product -> admitted charged correction -> distinct actual pass. Old failure immutable, old assignment cannot rerun, correction_count stays 1. | pass |
| V-13 | AC-05 | Actual API/CLI, identity, replay and collector fresh rerun documented | pass | Static current API/CLI/producer-contract/registry trace agrees with P1 actual requests, paths, logs, fresh rerun and replay. Collection/acceptance unavailable; real sbx/provider qualification remains T-006. | pass |
| G-01 | Conditional maintainability | Current reviewer-owned original-B comparison, rationale dispositions and native evidence | pass | Consumed maintainability-03, its original-B/reviewer-R comparison, M-01..11 rationale and native references. Independently decoded B7 snapshots equal HEAD; R7 snapshots/hashes equal current index/worktree; full complete/compared. Current ARCH4 and REG8/35 pass. Registry-02 remains applicable, no later contract edits. | pass |

## 4. Adversarial state and evidence checks

- Owner scope is crossed with allowed/out-of-scope dirty files and regular/symlink identity. Unchanged-owner positive controls prevent an always-refusing implementation from satisfying the row.
- Same-size tracked, visible untracked modify/add/remove, index-only, configuration and explicit ignored-input drift invalidate real previously passed evidence. Irrelevant ignored generated output alone keeps it current.
- Exact complete assignment and authority bindings are varied independently. Integer-for-boolean YOLO authority and invalid timeout types refuse before execution. No unrestricted fallback follows legacy capability failure.
- One real command lock excludes another check/inspection. Completed replay versus fresh operation key observes one versus two actual invocations. Failed/corrected candidates retain distinct immutable histories and correction accounting.
- Killed coordinator histories exercise before launch, during execution and after receipt publication. Unknown ownership prevents a replacement writer; reconciliation never reruns a completed receipt.
- Changed executable mechanism is tested against the actual execution-record validator: valid record accepted, invalid `implicit_fallback` rejected. No changed standalone JSON schema exists for these records; the Python validator is the executable authority.
- LIFECYCLE observes real timeout, SIGTERM-resistant descendants and exited-parent inherited pipes. Existing PID assertions plus independent group disappearance and pipe closure checks pass with bounded waits. A final approved process inventory found no remaining fixture process. No tamper resistance or power-loss durability is claimed.

## 5. Independent command records

All commands use repository root as cwd, existing Python/Git and disposable local state. Every test/probe command below exited 0 except the explicitly recorded initial containment setup. `LOG` identifies the retained raw output path. All behavioral commands use `PYTHONDONTWRITEBYTECODE=1`; no packages or external services are used. Focused tests ran before owning/aggregate gates. Approved escalation was used for macOS containment suites; it is an execution capability, not a changed product policy.

| ID | Exact command (output redirected to LOG with `> LOG 2>&1`) | Result / LOG |
|---|---|---|
| ACTOR | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_producer` | 20 pass; `/tmp/t0041-discovery03-producer.log` |
| CAPABILITY-initial | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_verification_runner.py -k VerificationSandboxCapabilityTests` | exit 1, 1 setup error at loopback bind; `/tmp/t0041-discovery03-capability.log`; no containment oracle reached |
| CAPABILITY | Same exact focused command as preceding row, approved outside agent sandbox | 1 pass; `/tmp/t0041-discovery03-capability-escalated.log` |
| P1 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery03/probe.py` | actual pass/fail, hash, validator positive/negative, replay/fresh rerun, same-size drift, corrected owner-mode refusal pass; `/tmp/t0041-discovery03-probe.log` |
| IGNORED | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery03/ignored.py` | generated/before/during 3 histories pass; `/tmp/t0041-discovery03-ignored.log` |
| RUNNER | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_verification_runner.py` | 40 pass, no skips; `/tmp/t0041-discovery03-runner.log` |
| MATRIX | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery03/matrix.py` | 7 histories pass; `/tmp/t0041-discovery03-matrix.log` |
| EXTRA | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery03/extra.py` | later-command omission, publication fault and legacy dirty-baseline refusal pass; `/tmp/t0041-discovery03-extra.log` |
| LAUNCH-FAILURE | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery03/launch-failure.py` | V-07d controlled refusal, no marker/artifacts/Popen; `/tmp/t0041-discovery03-launch-failure.log` |
| GIT | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_git.py` | 14 pass; `/tmp/t0041-discovery03-git.log` |
| REVISION | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py -k ControllerInputRevisionTest` | 8 pass; `/tmp/t0041-discovery03-revision.log` |
| UPSTREAM | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_v05g` | 1 pass; `/tmp/t0041-discovery03-upstream.log` |
| ARCH | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | 4 pass; whole-repository CLEAN policy; `/tmp/t0041-discovery03-architecture.log` |
| REG | `python3 tools/check_contracts.py --root .` | 8 subsystems / 35 indexed plan references valid; structural only; `/tmp/t0041-discovery03-contracts.log` |
| LIFECYCLE | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery03/lifecycle.py` | 3 real process histories pass including group disappearance/pipes; `/tmp/t0041-discovery03-lifecycle.log` |
| OWNING | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests` | 251 pass, no skips, 105.040s; `/tmp/t0041-discovery03-owning.log` |
| AGGREGATE | `PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py` | exit 0; 7 checks, 0 failed; 32 analyzer-related root skips; `/tmp/t0041-discovery03-aggregate.log` |

Read-only identity checks compared every index blob/worktree file, decoded original-B/reviewer-R snapshots and verified their hashes without running or replacing analyzers. `git diff --cached --check` passed. The command `ps -axo pid=,ppid=,etime=,state=,command= | rg 'unittest discover|test_targeted|task-orchestrator' | head -n 15` was first denied by the agent sandbox, then approved and showed only the inventory command itself (before aggregate launch). Cleanup controls did not leave fixture processes behind. No baseline failure was hidden or converted into a pass.

Reproduction: P1/IGNORED/MATRIX sources are embedded in discovery-01's matching `/tmp/t0041-discovery-*.py` sections; this pass extracted them without replacing production behavior. P1 additionally asserts corrected owner refusal rather than only printing it. EXTRA source is embedded in discovery-02's `/tmp/t0041-correction-discovery-extra.py` section. Current derived files remain at the exact command paths above. New LAUNCH-FAILURE and LIFECYCLE sources are embedded below for transfer. Existing test paths and exact commands are sufficient to rerun the maintained regressions.

## 6. Aggregate-gate record

Owner/stage: this independent reviewer, discovery iteration 3. Exact command: `PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py > /tmp/t0041-discovery03-aggregate.log 2>&1`. Status: passed.

Justification: all 48 rows were reconciled against brief/verification revision 1 and staged scope before broad execution. Current targeted probes, including former V-07d/e blockers and reviewer regressions, were clean; no decisive targeted product failure or selected adversarial probe remained. The initial containment setup denial was resolved with an approved rerun that reached and passed the actual oracle. Owning suite then passed 251 tests. One repository aggregate supplies cross-cutting regression evidence; it is not a substitute for targeted rows, maintainability/native duties or separate acceptance. Prior Linux aggregate failures remain historical records, not current evidence.

Current result: exit 0, 7 checks, 0 failed. Suites: skill-creator 3 tests, task-brief-designer 13 tests, verification-designer 4 tests, orchestrator 251 tests, root 311 tests (32 skipped). Registry: 8 subsystems/35 plan references. Development-profile drift: 112 paths match. The 32 skips require real pinned Radon/Ruff dependencies or their dedicated native Python environment; they do not count as successful analyzer behavioral qualification. Current maintainability-03 already owns the separate advisory native-tool proof and identities. No install or environment repair was attempted. Root aggregate log retains each skipped test and reason.

## 7. Scope and reviewed identities

The four changed runtime owners and three focused test modules are T-004.1 implementation. README, contract registry/index and runtime references describe only its implemented producer slice. The package brief, verification, preflight, controller-contract and result/review files are task authority/submission/history. Parent T-004, T-004.2 brief and task index are pre-existing preparation work recorded in preflight and prior discovery; preserved as staged owner context, not reviewed as implemented collection behavior. The untracked maintainability-03 report predates this invocation and is consumed evidence, not authored here. No unexplained production overlap was found. No source task plan was modified, and no installed skill copy was refreshed.

The orchestrator is outside the selected development profile and adds no shared runtime dependency; the canonical installer was inspected for membership, not changed. Baseline dependency remains accepted T-003; task authority and verification revisions are unchanged. Prior reports remain immutable historical evidence, even where their platform outcomes differ.

All 28 staged paths below were separately read as index bytes and worktree bytes and matched. This table records index object ID and SHA-256 of both equal byte streams, not an inference from short status.

| Staged path | Index blob | Index/worktree SHA-256 |
|---|---|---|
| `README.md` | `a51b298bf3d0f41ff0478c955eb3c869995db193` | `9a0c38baab653ceedc0dff06eb131332e9cd9623526699b088743d490be4e447` |
| `docs/contracts/index.json` | `23d7c3554487dc17239bf106f51d0d2c523a6108` | `27adf2a86555200d70e508eb368c96a982971d2d3017c9dacb7ac019dccc6f63` |
| `docs/contracts/task-orchestrator.json` | `814038c3d12aab2d587f8c4758d4efc2f9486daa` | `91d244810ea2fbb0670b91e00c75f074dbc054ee25676165d212ec18e780a366` |
| `skills/task-orchestrator/docs/tasks/T-004.1/brief.md` | `cae221548704221dfc304918beb25b85679ce262` | `e93033e49204821b476e547930559f1c3cd83feeb176152808cf0b467cfd701c` |
| `skills/task-orchestrator/docs/tasks/T-004.1/controller-contract.md` | `89db2c717e730e213c38e13ce94fbbab51186ea0` | `ccd09b554cbc7d74605c0f44db27fd0ca9aa683419d3bf381fce1e44a10efe74` |
| `skills/task-orchestrator/docs/tasks/T-004.1/correction-01.md` | `ef016b5c330c0744352c70f6b08de493a41d7e16` | `7a14dbf8ef2581e63da905df746d0f82ac9b357780cc78c90bbb909cb9c10830` |
| `skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md` | `ac31c689a819ca20e2f6f8d925350caec3fc125b` | `2f23501770a60a8696aff72758b46b0e88c3d0beeae431a395f6c5620fd6233b` |
| `skills/task-orchestrator/docs/tasks/T-004.1/preflight.md` | `b3eaad9625502f85c11a8f0629bf7eb68f2b6373` | `ffe20bed93fc2db6772d5e9bac985569a871cc1e0ab1e3f8072c46537d4e9aed` |
| `skills/task-orchestrator/docs/tasks/T-004.1/reviews/acceptance-01.md` | `28898c37b6ddc9a27293c60d78a84f9fc15f4a99` | `d7c5d524e16dcaa16c8fad22a455a23598ebb16514b955d157a6fb8b713777d0` |
| `skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-01.md` | `b7655be46d02d981af60bc7b9cd1f96caf5ec195` | `42dc33578b5952343794bda412c53e795ed3ac551bdc809bf82701715fd83338` |
| `skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-02.md` | `46dcbc74e2dec756ec0703a780a2b7166db138ba` | `7ee6d812aa95f2e8a6f6a4e93be293c0e8ee1b4e8f1bf1be0ea319bb835bdb0b` |
| `skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-01.md` | `c57b091b99659ec6513c2792db6b8b84e74a9eae` | `7bb809314d5e8c232cf38dc9aac31a6dab6e908398bee506457218ea6ca7eab1` |
| `skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-02.md` | `b21eda6abc414687cb2db0d0e318bc8aaa9cd886` | `332ea3d0f2576590d6982e43d8e2dac9f97397775eab4b7c067c9c469eb80016` |
| `skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-01.md` | `a2ef4be144265f362991e7d7eda7177cc20aeb3e` | `a9906e607f7dbabc11b6842153732a17db9b1297b8483f19743dda80bd405df3` |
| `skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-02.md` | `5801df5012f10d8c65751357c438a41d58983751` | `68e761a89b0a4bde490a204dedb06462a6d1464b9489bd2b43ac3cd17154c111` |
| `skills/task-orchestrator/docs/tasks/T-004.1/verification.md` | `61ea86dbf113ee951ea671faa603c1b34b888fbe` | `e70c3d1895e3a746967b45a2af9df63750da657e6a9e8e0a0148513858c3154d` |
| `skills/task-orchestrator/docs/tasks/T-004.2/brief.md` | `9c6104358b0419c1091a933a445221d16f0080b1` | `43679cdb3299d61c8be917fca578d782919bbad343b5f94074e45ee188644fa3` |
| `skills/task-orchestrator/docs/tasks/T-004/brief.md` | `70cfc1967358f4fd3efc77590f5962d7fb14cc72` | `099bd9d46bd7ac73a4b8a6ba4d5cd4a43a4eb4787f9d19613202ac1c85475139` |
| `skills/task-orchestrator/docs/tasks/index.json` | `24f0137dadf7542fe90ad2e2fc4cc497a9b75ba1` | `429f2733772a78ea6f90560f76c41ee7cc07c5c3f791cd36e34acc765e5084ee` |
| `skills/task-orchestrator/references/architecture-map.md` | `efdb7e6763f525a0b3fbf2c024676098419304cd` | `9edcd04ee5a7fcfaec18d463e99e2b358142e7ce3e5a816dc7e30e3b93de1765` |
| `skills/task-orchestrator/references/operator-guide.md` | `2dda493b3b7a66c8b8697d379351ff1d58ab500c` | `6e1fcd965a1fc344c088ab7d6a4e077a296d8c8a315b0510c9cf0023f2df5e14` |
| `skills/task-orchestrator/scripts/controller.py` | `4e0f08a53061a915527e3363b659d77c3d44cd8e` | `1ff6e43f73d1a52a704f16ec63b0720f8928f37de743568f42153a8da03385ef` |
| `skills/task-orchestrator/scripts/controller_git.py` | `b0edb5b148d4c98b1d3cb171ebff80edc5e6f851` | `746ab7fa695b15ff2b9f68eb9198b4d9cb41a2802836c0e7a7736251d2bc553a` |
| `skills/task-orchestrator/scripts/controller_state.py` | `f06371275fcbe6a17b0ff383bb8af7a1d53801f9` | `a30ab322e417a62b936d5198e8297d41214a0c106a43c3dfdf262f5a6bac97a4` |
| `skills/task-orchestrator/scripts/verification_runner.py` | `720c81e94c4ebd3bb99fe967a4d12ca5470275b5` | `d7b7b19672fd4cfbca87e7400f7ee8fe51f66207f20c332dd5c6868f0c80fb2a` |
| `skills/task-orchestrator/tests/test_actor_operations.py` | `2e06c82dd7cef9e05962ebd266797aedb6ddedf1` | `2a38d65634701a51a8e9e198eb05b6b739bd5b927111ac8e87b5bc385e6a7d14` |
| `skills/task-orchestrator/tests/test_controller_git.py` | `cf29efc77e7047c49c92c7be3a3f077f385e5025` | `70db0929b22c6f821666ec090bed0b1736e355c496621a830c6004b718359cbd` |
| `skills/task-orchestrator/tests/test_verification_runner.py` | `b0cee869e038a008299f5960063d70aa2c249261` | `deb48747c12f518d7f0774b5c0c1cdc2d24d14aa3e6af5f7f93ff1f687ddbf44` |

## 8. Questions, unchecked work and residual risk

No required/material row remains blocked or unchecked. No newly confirmed product defect or unresolved scope question. Evidence is bounded to current local filesystem/Git/process behavior and actual macOS restrictive containment. Fake Codex fixtures do not qualify real sbx, Codex/model/provider identity or outer isolation; T-006 owns that proof. T-004.2 owns independent collection/correction composition; T-005 owns acceptance/completion admission. Ignored evaluated inputs must be explicit allowed paths; arbitrary command-read discovery is not claimed. No power-loss or coherent-tamper guarantee is asserted. Analyzer reports remain local ignored artifacts and must be transferred with their JSON/text siblings for another checkout.

## 9. Coverage completeness and next route

Complete discovery, no findings, 48/48 rows with current evidence. This statement publishes evidence only.

Next: a separate `task-acceptance-review` call consumes T-004.1 brief r1, verification r1, preflight and Decision context, controller-contract, current staged diff/identities, implementation-report/correction-01, this report, maintainability-03 (plus original B/current I/R JSON/text references), contract-registry-02 and prior acceptance/discovery continuity. Include the reviewer regression paths/commands above and zero blocked/unchecked rows. No acceptance call or advancement was performed here.

Discovery continuation:
- Iteration/current bytes: 3; HEAD and staged/unstaged identities in section 1; all 28 index/worktree pairs in section 7.
- Coverage rows: V-01=pass; V-02a=pass; V-02b=pass; V-02c=pass; V-02d=pass; V-03a=pass; V-03b=pass; V-03c=pass; V-03d=pass; V-03e=pass; V-03f=pass; V-04a=pass; V-04b=pass; V-04c=pass; V-04d=pass; V-04e=pass; V-05a=pass; V-05b=pass; V-05c=pass; V-06=pass; V-07a=pass; V-07b=pass; V-07c=pass; V-07d=pass; V-07e=pass; V-08a=pass; V-08b=pass; V-08c=pass; V-08d=pass; V-09a=pass; V-09b=pass; V-09c=pass; V-09d=pass; V-09e=pass; V-09f=pass; V-10a=pass; V-10b=pass; V-10c=pass; V-10d=pass; V-10e=pass; V-11a=pass; V-11b=pass; V-11c=pass; V-11d=pass; V-11e=pass; V-12=pass; V-13=pass; G-01=pass.
- Finding IDs: F-01 prior P2 has current correction evidence; G-01 conditional evidence supplied; no new findings.
- Finding/scenario continuity: discovery-02 V-07d/e blocked -> current pass (approved supported-host containment and controlled launch failure); all other prior current passes independently corroborated. F-01 correction owner implementer, evidence owner this discovery, decision owner separate acceptance; sibling surface dirty allowed/out-of-scope files and symlink referents. G-01 proof owner maintainability-03, registry proof owner registry-02, admission evidence owner this discovery, disposition owner separate acceptance. No unfinished reason or approved deferral.
- Preparation/context: brief r1, verification r1, preflight Decision context, parent/direction/T-003 references in section 1.
- Reviewer regressions: ACTOR `-k test_producer` (includes five dirty-owner and staging controls), P1 and EXTRA exact paths/commands in section 5; new LAUNCH-FAILURE/LIFECYCLE sources below.
- Aggregate: passed, exact command and discovery ownership in section 6; targeted evidence clean before launch, one current gate.
- Next: separate task-acceptance-review with the complete evidence package listed above.

## Reproducible added reviewer probes

### /tmp/t0041-discovery03/launch-failure.py

```python
import sys, subprocess
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
from test_verification_runner import VerificationExecutorLocalProcessTests as Cases
case=Cases(); case.setUp()
try:
 marker=case.repository/'must-not-run'
 plan=case.plan(case.command(f'from pathlib import Path; Path({str(marker)!r}).touch()'))
 def denied(argv,**kwargs):
  assert argv[0]=='/usr/bin/sandbox-exec',argv
  return subprocess.CompletedProcess(argv, 1)
 with mock.patch.object(case.runner.subprocess,'run',side_effect=denied) as capability, mock.patch.object(case.runner.subprocess,'Popen',side_effect=AssertionError('unrestricted command launch')) as launch:
  try:case.execute(plan)
  except case.runner.UnsupportedSandbox as exc: print('Legacy capability launch failure refused:',str(exc))
  else:raise AssertionError('capability failure admitted')
  assert capability.call_count==1
  assert launch.call_count==0
 assert not marker.exists()
 assert not list(case.verification_directory.iterdir())
 print('V-07d PASS: production sandbox argv, controlled capability failure, no marker, no launch, no artifacts')
finally:case.tearDown()
```

### /tmp/t0041-discovery03/lifecycle.py

```python
import os,sys,time,threading
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
from test_verification_runner import VerificationExecutorLocalProcessTests as Cases
for name in ('test_yolo_timeout_descendant_cleanup','test_yolo_sigterm_resistant_descendant_cleanup','test_yolo_exited_parent_open_pipe_cleanup'):
 case=Cases(name);case.setUp();groups=[]
 original=case.runner.subprocess.Popen
 def observe(*args,**kwargs):
  process=original(*args,**kwargs)
  if kwargs.get('start_new_session'):groups.append(process)
  return process
 try:
  with mock.patch.object(case.runner.subprocess,'Popen',side_effect=observe):getattr(case,name)()
  assert groups, 'No real group observed'
  for process in groups:
   deadline=time.monotonic()+2
   while True:
    try:os.killpg(process.pid,0)
    except ProcessLookupError:break
    assert time.monotonic()<deadline,('group survives',process.pid)
    threading.Event().wait(.01)
   assert process.poll() is not None
   assert process.stdout is None or process.stdout.closed
   assert process.stderr is None or process.stderr.closed
  print(name+': PID/descendant controls, process group disappearance and inherited pipe closure PASS',flush=True)
 finally:case.tearDown()
```

## Publication provenance

Exact reviewed status immediately before publication:

```text
M  README.md
M  docs/contracts/index.json
M  docs/contracts/task-orchestrator.json
A  skills/task-orchestrator/docs/tasks/T-004.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-004.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-004.1/correction-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-004.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/acceptance-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-02.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-02.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-02.md
A  skills/task-orchestrator/docs/tasks/T-004.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-004.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-004/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/references/architecture-map.md
M  skills/task-orchestrator/references/operator-guide.md
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_git.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/scripts/verification_runner.py
M  skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_verification_runner.py
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-03.md
```

Exact status after publication:

```text
M  README.md
M  docs/contracts/index.json
M  docs/contracts/task-orchestrator.json
A  skills/task-orchestrator/docs/tasks/T-004.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-004.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-004.1/correction-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-004.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/acceptance-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-02.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-02.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-02.md
A  skills/task-orchestrator/docs/tasks/T-004.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-004.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-004/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/references/architecture-map.md
M  skills/task-orchestrator/references/operator-guide.md
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_git.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/scripts/verification_runner.py
M  skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_verification_runner.py
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-03.md
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-03.md
```

Only the new discovery-03.md entry differs. All 28 reviewed staged index/worktree byte identities and the staged diff digest remain unchanged.
