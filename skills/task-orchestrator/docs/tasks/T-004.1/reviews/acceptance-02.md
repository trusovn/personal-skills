# T-004.1 acceptance — staged producer boundary

The staged change provides candidate-bound inspection and actual check execution for T-004.2. Current independent discovery supports all 48 required/material rows, including the previously blocked restrictive execution cases. The producer handoff may advance to T-004.2; collection composition and real sbx/provider qualification remain separate work.

Verdict: ACCEPT

Provenance: independent session; no reviewed production or test bytes authored. Guided profile. No findings. Approved deferrals: none.

Authority and preparation: brief.md revision 1, verification.md revision 1, preflight.md and its Decision context; controller-contract.md; implementation-report.md and correction-01.md. Prior acceptance-01 is historical INCONCLUSIVE, superseded for these bytes by this decision. Admitted discovery: reviews/discovery-03.md, complete, independent iteration 3. Conditional evidence: maintainability-03.md (original B, implementer I and reviewer R, full compared profile, M-01–M-11 dispositions, architecture PASS), contract-registry-02.md and current discovery registry confirmation. No general maintainability rerun was performed.

Reviewed HEAD: aa99736e0fb02733d07e62aa382dbcee2ae46f1b. Staged binary diff SHA-256: f9f5271abf3987177e1e1bc5162025b242c91c8d1233e72eab63b7e1b9349871. Acceptance independently matched that identity and every one of 28 index blobs to worktree bytes. Unstaged tracked diff is empty. Existing untracked discovery-03 and maintainability-03 are consumed evidence. Parent/T-004.2 briefs and task index are preserved preparation, not implemented collection scope.

Coverage below preserves discovery's stable IDs, cases, prior statuses and producer-attributed decisive evidence. Each current pass is admitted for the matching staged bytes and unchanged authority; submitted scenario claims are implementation-report/correction-01, independently corroborated by discovery-03. The executable record validator has both valid-record acceptance and deliberately invalid implicit_fallback rejection (V-06). Structural checks alone are not behavioral proof.

| Row | AC/invariant | Explicit cases | Prior | Current independent probe / oracle | Reconciled result |
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

F-01: resolved, not deferred. The dirty-owner chmod trigger now refuses without changing owner work; allowed/out-of-scope regular files, symlink referents and staging siblings are covered. Impact of regression would be owner-work damage; exposure occurs on dirty baselines. Current identity and scope guards mitigate it, with current negative and unchanged-owner positive controls. Correction owner: implementer; evidence owner: discovery-03; disposition owner: this acceptance.

G-01: resolved by current maintainability-03 original-B comparison, M-01–M-11 dispositions and independent discovery identity admission. Evidence owner: maintainability reviewer; registry owner: registry updater; decision owner: this acceptance. V-07d/e move from blocked to pass through controlled production launch refusal paired with actual supported-host containment. The initial sandbox loopback setup denial was not counted as a pass; discovery retains it and the approved successful rerun.

Contract reconciliation: brief ART-003/005 and producer IF-003 correspond to inspect_candidate/check_candidate, candidate/check ledger fields, execution mechanism validation and actual runner behavior. Current registry describes this producer slice, dirty-owner protection and compatibility refusal. Index and routing references represent implemented capability; collector/acceptance remain excluded. Discovery's canonical registry check passed (8 subsystems, 35 references). No installer dependency or membership changed.

Aggregate gate (consumed): discovery iteration 3 owns `PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py > /tmp/t0041-discovery03-aggregate.log 2>&1`, after clean targeted reconciliation and owning suite. Exit 0; 7 checks, 0 failed; orchestrator 251 tests; root 311 tests with 32 analyzer-dependency skips. Acceptance inspected the retained log and added no gate. Skips do not qualify analyzer behavior; native maintainability evidence is separate. Historical Linux failures are not current results.

Observations / residual risk: local fake actors do not qualify real sbx/provider identity or outer isolation. YOLO supplies no filesystem/network enforcement. Explicit evaluated ignored inputs are covered; arbitrary command-read discovery, coherent tamper resistance and power-loss recovery are not claimed. No required row remains blocked or unchecked. No reviewer reproducer or tests were written or executed by acceptance.

Next: coordinator consumes this ACCEPT and publishes the producer handoff for T-004.2 under its prepared task workflow. No advancement, commit, tracker or plan mutation was performed here.

## Publication audit

Exact status before publication:

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
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/acceptance-02.md
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-03.md
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-03.md
```

Only the new acceptance report entry differs; the index remains unchanged.
