# Task Review Discovery Report: T-004.1 — candidate-bound scope and check evidence

| Field | Value |
|---|---|
| Producing stage | task-review-discovery |
| Coverage completeness | partial — F-01 confirmed; G-01 and legacy host proof blocked; V-09f/V-11e incomplete |
| Discovery iteration | 1, independent initial discovery |
| Created at | 2026-11-10T22:43:39.869379+00:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report path | skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-01.md |
| Task brief | skills/task-orchestrator/docs/tasks/T-004.1/brief.md revision 1 |
| Verification / readiness / context | skills/task-orchestrator/docs/tasks/T-004.1/verification.md revision 1; preflight.md; controller-contract.md; owner direction docs/direction-single-task-sbx.md and parent T-004 brief |
| Submission | skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md; submitted local proof is a claim until corroborated below |

Evidence only: no acceptance verdict, approved deferral or advancement. This report applies only to the identified reviewed bytes, and does not review or authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production or test bytes. Independent evidence authority: yes. The active installation was resolved at `.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`, including its report template; it was not refreshed. No subagents, production edits, commits or staging operations were used.

HEAD: `aa99736e0fb02733d07e62aa382dbcee2ae46f1b`. SHA-256 of complete staged binary diff: `975abb03d12af7eecd52149ecc0c85a5f07cc62f4524f1368d438b4405567b6d`. All staged files have identical index and working-tree bytes; separate index blob IDs and worktree SHA-256 values appear below. This review does not adopt pre-existing task-planning work as runtime authorship.

## 2. Findings

### F-01 [suggested P2] Executable-bit changes to pre-existing dirty owner files are admitted

| Field | Evidence |
|---|---|
| Location | skills/task-orchestrator/scripts/controller.py:1572–1577; initial baseline capture uses controller_git.capture_task_baseline |
| Trigger | Commit nonexecutable owner.txt, dirty its content before initialization, initialize and admit a terminal implementation, then chmod owner.txt from 0644 to 0755 without changing its dirty content or index; call inspect_candidate. |
| Consequence | Inspection publishes a passed eligible candidate despite an additional change to protected owner work outside the task's allowed paths. The baseline cannot distinguish the executable mode of dirty owner work. |
| Observed evidence | P1 prints status_equal=true, mode=0o755, result.status=passed and a published candidate. Both status strings contain the same ` M` and content digest; index trees remain identical. |
| Affected AC | AC-01; V-02b; owner-work preservation and out-of-scope rejection |
| Broken invariant | A pre-existing dirty path must remain unchanged regardless of scope membership; unchanged porcelain text and content digest do not prove unchanged filesystem identity. |
| Credible sibling surface | Dirty allowed files and dirty out-of-scope files share this check; pre-existing dirty symlinks also lack baseline referent identity even though candidate capture evaluates referents. These are the bounded sibling surfaces to assess, not additional reproduced findings. |
| Smallest corrective direction | Preserve and compare the evaluated identity needed to protect baseline owner work, consistently with candidate identity, including executable metadata and relevant link semantics. Do not limit the correction to owner.txt or to porcelain status values. |

Correction owner: implementer. Evidence owner after correction: fresh discovery reviewer. Decision owner: separate acceptance call. No fix was made here.

## 3. Completeness ledger

Before any aggregate, review was organized around V-01–V-13 and their finite subcases, plus conditional maintainability proof. The original-B/rationale obligation remains owned by its prior stage. Submitted evidence for each V row is the matching row in implementation-report.md's scenario table; it is not itself independent proof. Setup/oracle: disposable real Git repository and external run directory, upstream fake Codex admitted through public operations, actual product-reading command, external invocation counter, real receipt/log bytes and independent filesystem observations. Specific deviations and missing oracles appear per row. No schema-text-only behavioral pass is claimed.

| Row | AC / invariant | Explicit cases | Independent current probe / oracle | Result / reason |
|---|---|---|---|---|
| V-01 | AC-01 | Terminal producer; real tracked bytes; literal paths; actor claims grant no pass | P1 + Git unusual-path controls; public digest independently compared with actual allowed.txt | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-02a | AC-01 | Unchanged dirty owner setup remains intact while allowed clean file changes | P1 and actor producer fixtures; Git dirty-baseline controls | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-02b | AC-01 | Dirty allowed content change; hidden staging change; dirty file mode change | P5 dirty_allowed + actor hidden_staged + P1 owner-mode counterexample | **fail** — Content/staging refusals work, but executable-bit-only owner changes pass inspection: F-01. |
| V-02c | AC-01 | New tracked change outside scope | P5 outside_tracked | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-02d | AC-01 | New untracked change outside scope | Actor test_producer_scope_and_invalid_timeout_preserve_state | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-03a | AC-01/02 | Wrong stage, absent/wrong operation; wrong run/task | Actor assignment_refusals; _producer_context and inspect_candidate guards | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-03b | AC-01/02 | Wrong stage, absent/wrong operation; wrong run/task | Actor assignment_refusals; _producer_context and inspect_candidate guards | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-03c | AC-01/02 | Wrong input/policy/flow/baseline binding | Actor assignment_refusals; inspect_candidate baseline digest check; revision suite. Baseline rejection is traced, not separately injected at public boundary. | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-03d | AC-01/02 | Live or unknown upstream actor cannot establish stable candidate/check | Upstream nonterminal test; _active_actor refusal precedes inspection publication | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-03e | AC-01/02 | Live or unknown upstream actor cannot establish stable candidate/check | Upstream nonterminal test; _active_actor refusal precedes inspection publication | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-03f | AC-01/02 | Second check/inspection while real check owns command lock | Actor drift_during_real_check_and_exclusion | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-04a | AC-02 | Same-size tracked bytes change after passing check | P1 public same-size drift; unchanged invocation count | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-04b | AC-02 | Visible untracked modify/add/remove independently | P5 untracked_modify, untracked_add, untracked_remove | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-04c | AC-02 | Index-only change, HEAD/baseline drift | P5 index; Git identity controls and _load_current_candidate full-workspace comparison. HEAD refusal traced. | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-04d | AC-02 | Evaluated configuration bytes change | P5 configuration; P3 ignored evaluated input | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-04e | AC-02 | Approved task-input/policy/flow revisions | 8 current ControllerInputRevisionTest cases; _producer_context and _load_current_candidate authority comparisons | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-05a | AC-02 | Irrelevant ignored generated output leaves candidate current | P3 generated | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-05b | AC-02 | Ignored evaluated input drift before checking refuses eligibility | P3 before | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-05c | AC-02 | Ignored evaluated input changes at synchronized real-process checkpoint | P3 during; zero-exit check becomes stale | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-06 | AC-03/04 | Actual argv, logs, exit, environment, candidate; replacement-process replay | P1 + actor real_check_replay + P2 binary output/literal argument; execution-record validator accepts actual record and rejects invalid mechanism | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-07a | AC-03 | Exact explicit frozen YOLO authority versus absent/incomplete/invalid | P2 direct real execution and invalid authority matrix; _producer_context loads frozen authority; absent runner authority traces to legacy builder | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-07b | AC-03 | Exact explicit frozen YOLO authority versus absent/incomplete/invalid | P2 direct real execution and invalid authority matrix; _producer_context loads frozen authority; absent runner authority traces to legacy builder | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-07c | AC-03 | Legacy policy on unsupported host refuses without fallback | Runner test_unsupported_host_is_rejected passed on Linux; build_sandbox_invocation rejects before launch | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-07d | AC-03 | Legacy launch-capability failure and real supported restrictive containment | Current runner module: 20 skips and 5 failures/1 error; HEAD controls reproduce same 5 failures/1 error | **blocked** — Linux host lacks macOS /usr/bin/sandbox-exec. Current supported-host containment cannot execute here; next evidence owner is supported-host verifier. No unrestricted fallback was observed. |
| V-07e | AC-03 | Legacy launch-capability failure and real supported restrictive containment | Current runner module: 20 skips and 5 failures/1 error; HEAD controls reproduce same 5 failures/1 error | **blocked** — Linux host lacks macOS /usr/bin/sandbox-exec. Current supported-host containment cannot execute here; next evidence owner is supported-host verifier. No unrestricted fallback was observed. |
| V-08a | AC-03 | Prohibited shell/malformed commands, invalid later command before any launch | Current runner parser cases; actor invalid_later_command | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-08b | AC-03 | Forbidden install versus explicit permission; planning only | Current runner closed install table and permitted planning test; no installation executed | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-08c | AC-03 | Forbidden install versus explicit permission; planning only | Current runner closed install table and permitted planning test; no installation executed | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-08d | AC-03 | Quoted literal argv and near-miss non-install | Current runner parser tables; P2 actual literal filename | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-09a | AC-04 | Real wrong product exits nonzero without correction charge | P1 failure + actor failed_product | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-09b | AC-04 | Missing required executable blocks before any command | Actor missing_later_executable; exact blocked diagnostic and unknown owner | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-09c | AC-04 | No check evidence is missing/not-run, never passed | P1 inspect-before-check; status _evidence_view defaults and runner empty-plan classification traced | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-09d | AC-04 | Known issue cannot excuse required failed check | check_candidate clears authorized_gap before planning; P1 actual required failure; current legacy gap planning tests | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-09e | AC-04 | Targeted-only repository gate omission is explicit | Actor fixture actual receipt policy_omissions; check_candidate targeted branch | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-09f | AC-04 | Failure stops later command | Runner loop breaks after failed outcome; producer actual first failure; platform-gated two-command behavioral control not independently executed | **unchecked** — Distinct later-marker behavior in direct YOLO path not yet independently exercised; Linux skipped existing executor test. Next evidence owner: discovery reviewer, portable two-command fixture. |
| V-10a | AC-02/04 | Tracked and untracked drift while real command waits | Actor drift_during_real_check_and_exclusion; both changed in one synchronized scenario, plus separate P5 after-check cases | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-10b | AC-02/04 | Tracked and untracked drift while real command waits | Actor drift_during_real_check_and_exclusion; both changed in one synchronized scenario, plus separate P5 after-check cases | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-10c | AC-02/04 | Check side effect changes evaluated input despite exit zero | Actor check_side_effect; P3 during | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-10d | AC-03/04 | Finite timeout, descendants, resistant child, exited parent/open pipe | P2 six portable controls executed directly; PID absence and bounded runner group terminality | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-10e | AC-02/03 | Zero/negative/NaN/infinite/nonnumeric/boolean timeout refuses without launch | Actor scope_and_invalid_timeout; no counter and byte-identical ledger | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-11a | AC-02 | Completed API/CLI/reloaded replay executes exactly once | P1 + actor real_check_replay; public distinct-key rerun executes separately | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-11b | AC-02/03 | Real controller killed before launch/during synchronized command; replay cannot relaunch | Actor real_interruption_before_launch and during_command; real subprocesses; retained unknown ownership and invocation counter | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-11c | AC-02/03 | Real controller killed before launch/during synchronized command; replay cannot relaunch | Actor real_interruption_before_launch and during_command; real subprocesses; retained unknown ownership and invocation counter | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-11d | AC-02 | Receipt published before ledger result; reload reconciles without rerun | Actor real_interruption_after_result_reuses_one_execution | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-11e | AC-02/03 | Existing log collision and injected publication failure | Actor log_collision passed; runner write-failure case skipped on Linux | **unchecked** — Current log collision is proven; direct YOLO injected log-publication failure has not been executed. Next evidence owner: discovery reviewer with portable I/O-failure fixture. |
| V-12 | AC-01/02/04 | Real failure -> admitted correction -> new pass; old receipt immutable; charge only correction | Actor failed_product_correction_retains_history: two executions, distinct candidates, correction count 1 | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| V-13 | AC-05 | Actual API/CLI, identity, replay and collector fresh rerun documented | controller-contract.md versus staged controller dispatch, records and P1 distinct-key new rerun; registry routes implemented producer only | **pass** — Current targeted execution and/or narrow interface trace agree with the stated oracle. |
| G-01 | Conditional maintainability | Current reviewer-owned original-B comparison, rationale dispositions and native evidence | maintainability-01.md; original/final measurement reports present; seven source hashes match current index/worktree | **blocked** — Report gives general structural assessment and native checks, but no reviewer-owned comparison against original B, measurement-limit reconciliation or explicit required rationale dispositions. Evidence owner: maintainability reviewer; discovery does not repeat this stage. |

## 4. Adversarial state and evidence checks

- Current versus historical producer/check: historical operation refusal and corrected candidate/history retention passed in the producer cases; P1 executed a second genuine check with a new key, rather than treating replay as a rerun.
- Single owner: lock-contention test refused both second check and inspection; unknown interrupted checks blocked relaunch. Upstream live/unknown guard was traced and exercised with the current nonterminal actor case.
- Pre/post drift: independent tracked same-size, untracked add/edit/remove, index, configuration, generated and ignored-input controls; synchronized during-check drift remained stale even when the command exited zero.
- Persisted/executable validator boundary: actual execution record validated successfully; changing execution_mechanism to implicit_fallback raised ValueError. Invalid timeout/authority type controls refused before launch.
- Lifecycle: P2 used actual process groups, timeout, descendant PID absence, resistant child and open inherited pipe controls; all six direct portable checks returned within bounded waits. Actor interruption cases use their real checkpoints and bounded communicate/join. No fixture processes remained in the post-probe process inspection. The evidence does not claim power-loss recovery, coherent-tamper resistance or outer sbx containment.
- Owner work: dirty-content and hidden-index refusals passed; dirty executable metadata failed (F-01).

## 5. Independent probes and command results

All commands ran from the repository root, using local Python/Git only on Linux. `/tmp` scripts and logs are session-local reviewer evidence; the source of each custom probe is preserved below for reproduction. Temporary fixture trees were removed by tearDown/TemporaryDirectory; no target project was edited. No network, provider, package installation or live model call was made.

| ID | Exact command | Result / observed signal | Raw evidence |
|---|---|---|---|
| P1 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery-probe.py` | Public pass/fail/digest/replay/new rerun/drift + executable validator; owner-mode counterexample reproduced | /tmp/t0041-discovery-probe.log |
| P2 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery-yolo.py` | 6 portable controls passed when invoked directly; normal class is macOS-skipped | /tmp/t0041-discovery-yolo.log |
| P3 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery-ignored.py` | 3 ignored-input/generated-output histories passed | /tmp/t0041-discovery-ignored.log |
| P5 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery-matrix.py` | 7 scope/drift histories passed | /tmp/t0041-discovery-matrix.log |
| ACTOR | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_producer` | 15 passed | /tmp/t0041-discovery-actor.log |
| GIT | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_git.py` | 14 passed | /tmp/t0041-discovery-git.log |
| RUNNER | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_verification_runner.py` | 40 run: 5 failures, 1 error, 20 skipped; not a passing module | /tmp/t0041-discovery-runner.log |
| BASELINE | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery-baseline.py` | HEAD runner/state in disposable directory: same 5 failures and 1 error among 7 fail-closed tests; current faults are reproduced baseline host limitations | /tmp/t0041-discovery-baseline.log |
| REVISION | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py -k ControllerInputRevisionTest` | 8 passed | /tmp/t0041-discovery-revision.log |
| UPSTREAM | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_v05g` | 1 passed | /tmp/t0041-discovery-upstream.log |
| ARCH | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | 4 passed; structural CLEAN evidence | tool transcript |
| REG | `python3 tools/check_contracts.py --root .` | 8 subsystems / 35 refs valid; structural evidence | tool transcript |

The initial P1 invocation stopped after a reviewer-script TypeError (missing expected_closure_identity keyword); no product failure was inferred from that setup error. The corrected invocation ran all controls; the corrected script below is the regression source. Shell wrappers that tailed logs returned the tail status; suite outcomes above are taken from the preserved unittest summaries, including all failures/skips.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact command | `python3 tools/verify.py` |
| Status | not run |
| Owner / stage | this reviewer / initial discovery |
| Reason | Decisive targeted failure F-01 suppresses aggregate execution. Unfinished rows and G-01 also remain explicit; a broad gate cannot close them. |
| Current evidence | Targeted results above, not copied implementation gate claims. Focused runner-module execution was diagnostic contract coverage, not the aggregate. |

Architecture and registry commands are existing required focused structural checks, not substitutes for behavioral qualification. No new gate was introduced.

## 7. Scope and baseline comparison

Runtime scope is exactly four orchestrator scripts plus three associated test files. T-004.1 package files are current submission/preparation; parent T-004, T-004.2 and tasks/index.json are staged user task-planning context, reviewed only for scope/authority. README, contract registry and runtime reference edits are the designated updater's changes. Three untracked .DS_Store files are pre-existing excluded user/runtime artifacts. No unexplained interleaved runtime work was found.

Maintainability report references an older complete-diff digest `c3ce9704e173132cd81e7fcca7eb60a7cd8d1048f90cf0456e5b9cbde4865ba1`; later report/registry/reference staging explains the full-diff change. Seven Python files match the final measurement report hashes independently. The original preflight and final measurement JSON/text pairs exist: complete/full_profile=true, final comparison.status=compared. These facts establish consistency, not a reviewer-owned original-B comparison. G-01 preserves the missing comparison/limits/rationale dispositions; a prior structural verdict cannot supply them. The registry update report correctly describes its then-unstaged reference edits, now present in the index. Current registry structural validation passed.

| Reviewed path | Index blob | Worktree SHA-256 |
|---|---|---|
| README.md | `a51b298bf3d0f41ff0478c955eb3c869995db193` | `9a0c38baab653ceedc0dff06eb131332e9cd9623526699b088743d490be4e447` |
| docs/contracts/index.json | `23d7c3554487dc17239bf106f51d0d2c523a6108` | `27adf2a86555200d70e508eb368c96a982971d2d3017c9dacb7ac019dccc6f63` |
| docs/contracts/task-orchestrator.json | `ef61d7042a1436d0fd6fc8e7ed7af0b38bbab77f` | `35526d6961ef7b45ca8963bd79e49ea8e90c683fb8ecdebf2de8205638950fd3` |
| skills/task-orchestrator/docs/tasks/T-004.1/brief.md | `cae221548704221dfc304918beb25b85679ce262` | `e93033e49204821b476e547930559f1c3cd83feeb176152808cf0b467cfd701c` |
| skills/task-orchestrator/docs/tasks/T-004.1/controller-contract.md | `89db2c717e730e213c38e13ce94fbbab51186ea0` | `ccd09b554cbc7d74605c0f44db27fd0ca9aa683419d3bf381fce1e44a10efe74` |
| skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md | `ac31c689a819ca20e2f6f8d925350caec3fc125b` | `2f23501770a60a8696aff72758b46b0e88c3d0beeae431a395f6c5620fd6233b` |
| skills/task-orchestrator/docs/tasks/T-004.1/preflight.md | `b3eaad9625502f85c11a8f0629bf7eb68f2b6373` | `ffe20bed93fc2db6772d5e9bac985569a871cc1e0ab1e3f8072c46537d4e9aed` |
| skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-01.md | `b7655be46d02d981af60bc7b9cd1f96caf5ec195` | `42dc33578b5952343794bda412c53e795ed3ac551bdc809bf82701715fd83338` |
| skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-01.md | `a2ef4be144265f362991e7d7eda7177cc20aeb3e` | `a9906e607f7dbabc11b6842153732a17db9b1297b8483f19743dda80bd405df3` |
| skills/task-orchestrator/docs/tasks/T-004.1/verification.md | `61ea86dbf113ee951ea671faa603c1b34b888fbe` | `e70c3d1895e3a746967b45a2af9df63750da657e6a9e8e0a0148513858c3154d` |
| skills/task-orchestrator/docs/tasks/T-004.2/brief.md | `9c6104358b0419c1091a933a445221d16f0080b1` | `43679cdb3299d61c8be917fca578d782919bbad343b5f94074e45ee188644fa3` |
| skills/task-orchestrator/docs/tasks/T-004/brief.md | `70cfc1967358f4fd3efc77590f5962d7fb14cc72` | `099bd9d46bd7ac73a4b8a6ba4d5cd4a43a4eb4787f9d19613202ac1c85475139` |
| skills/task-orchestrator/docs/tasks/index.json | `24f0137dadf7542fe90ad2e2fc4cc497a9b75ba1` | `429f2733772a78ea6f90560f76c41ee7cc07c5c3f791cd36e34acc765e5084ee` |
| skills/task-orchestrator/references/architecture-map.md | `efdb7e6763f525a0b3fbf2c024676098419304cd` | `9edcd04ee5a7fcfaec18d463e99e2b358142e7ce3e5a816dc7e30e3b93de1765` |
| skills/task-orchestrator/references/operator-guide.md | `2dda493b3b7a66c8b8697d379351ff1d58ab500c` | `6e1fcd965a1fc344c088ab7d6a4e077a296d8c8a315b0510c9cf0023f2df5e14` |
| skills/task-orchestrator/scripts/controller.py | `9cd4360ec4b484528644dd098e34a7f27187fe77` | `d08f50104d05fe473a0797fea614ab4758d444dab2ac70e29571ee6d6ddefed1` |
| skills/task-orchestrator/scripts/controller_git.py | `a5ee4517bf5c22c256c91910fb109f7899f13d5d` | `746c6835ae6a79269249a855767d0f0c51651307ce2b6ca44f040f986123def1` |
| skills/task-orchestrator/scripts/controller_state.py | `f06371275fcbe6a17b0ff383bb8af7a1d53801f9` | `a30ab322e417a62b936d5198e8297d41214a0c106a43c3dfdf262f5a6bac97a4` |
| skills/task-orchestrator/scripts/verification_runner.py | `720c81e94c4ebd3bb99fe967a4d12ca5470275b5` | `d7b7b19672fd4cfbca87e7400f7ee8fe51f66207f20c332dd5c6868f0c80fb2a` |
| skills/task-orchestrator/tests/test_actor_operations.py | `91423d7c6e7ced53f8a0b979d943731e22b91f4b` | `5846a091c4854557c499851275adc0f3ce77b795b4d284bd1effad1f0f275b8f` |
| skills/task-orchestrator/tests/test_controller_git.py | `cf29efc77e7047c49c92c7be3a3f077f385e5025` | `70db0929b22c6f821666ec090bed0b1736e355c496621a830c6004b718359cbd` |
| skills/task-orchestrator/tests/test_verification_runner.py | `b0cee869e038a008299f5960063d70aa2c249261` | `deb48747c12f518d7f0774b5c0c1cdc2d24d14aa3e6af5f7f93ff1f687ddbf44` |

Exact status immediately before report publication:

```text
M  README.md
M  docs/contracts/index.json
M  docs/contracts/task-orchestrator.json
A  skills/task-orchestrator/docs/tasks/T-004.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-004.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-004.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-01.md
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
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
```

Exact status after publication (verified by writer):

```text
M  README.md
M  docs/contracts/index.json
M  docs/contracts/task-orchestrator.json
A  skills/task-orchestrator/docs/tasks/T-004.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-004.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-004.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-01.md
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
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-01.md
```

Only the new untracked report entry differs. The report is not staged.

## 8. Questions, unchecked work and residual risk

- G-01 blocked: maintainability reviewer must provide focused original-B comparison, coverage/measurement limits and explicit rationale dispositions. Discovery does not repeat the general structural review or approve a waiver.
- V-07d/e blocked: supported macOS verifier owns launch-failure and real containment proof. Current Linux runner failures reproduced unchanged against HEAD; they are not newly attributed production defects.
- V-09f unchecked: direct portable two-command failure/later-marker control remains owed by discovery; static loop trace alone is not reported as full behavioral evidence.
- V-11e unchecked in part: log collision passed, but injected publication-failure behavior remains owed by discovery under direct YOLO execution.
- Linux automatic test coverage limit: all six new YOLO controls sit under the inherited macOS-only class decorator. Direct invocation supplies current evidence here, but the default Linux suite still skips them. This report does not count those skips as passes.
- No real sbx/provider qualification; T-006 retains it. Full collection/correction composition belongs to T-004.2. No acceptance/completion behavior was inferred.

## 9. Coverage completeness and next route

Partial evidence report, with F-01 confirmed and all material scenario identities retained. First concrete action: implementer corrects F-01, preserving the unmodified scope/history. Then complete affected architecture/maintainability duties (including G-01), affected registry synchronization, fresh correction discovery including unfinished scenarios and reviewer regressions, and a separate acceptance decision call. No route named here has been executed or delegated.

The separate acceptance consumer must receive this report, the staged scoped diff, T-004.1 brief revision 1, verification revision 1, preflight.md, controller-contract.md, implementation-report.md, maintainability-01.md, contract-registry-01.md, owner decision context and all failed/blocked/unchecked rows. This report supplies evidence, never an advancement decision.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: 1; HEAD aa99736e0fb02733d07e62aa382dbcee2ae46f1b; staged binary diff SHA-256 975abb03d12af7eecd52149ecc0c85a5f07cc62f4524f1368d438b4405567b6d; all scoped index/worktree bytes equal.
- Coverage rows: V-01=pass; V-02a=pass; V-02b=fail; V-02c=pass; V-02d=pass; V-03a=pass; V-03b=pass; V-03c=pass; V-03d=pass; V-03e=pass; V-03f=pass; V-04a=pass; V-04b=pass; V-04c=pass; V-04d=pass; V-04e=pass; V-05a=pass; V-05b=pass; V-05c=pass; V-06=pass; V-07a=pass; V-07b=pass; V-07c=pass; V-07d=blocked; V-07e=blocked; V-08a=pass; V-08b=pass; V-08c=pass; V-08d=pass; V-09a=pass; V-09b=pass; V-09c=pass; V-09d=pass; V-09e=pass; V-09f=unchecked; V-10a=pass; V-10b=pass; V-10c=pass; V-10d=pass; V-10e=pass; V-11a=pass; V-11b=pass; V-11c=pass; V-11d=pass; V-11e=unchecked; V-12=pass; V-13=pass; G-01=blocked.
- Finding IDs: F-01 suggested P2, independently reproduced, no correction yet.
- Finding/scenario continuity: first pass, no prior discovery ledger. Current producer evidence is implementation-report.md; independent evidence is the command table and embedded probes. F-01 correction owner=implementer, evidence owner=fresh discovery reviewer, decision owner=separate acceptance call; sibling surfaces=dirty allowed/out-of-scope files and dirty symlinks. G-01 missing reviewer-owned comparison/rationale/limits owner=maintainability reviewer. V-07d/e missing host oracle owner=supported-host verifier. V-09f/V-11e missing targeted direct-path execution owner=discovery reviewer. No gap is deferred or approved.
- Preparation/context: T-004.1 brief r1; verification r1; preflight.md; controller-contract.md; implementation-report.md; parent T-004 and direction-single-task-sbx.md; maintainability-01.md and contract-registry-01.md.
- Reviewer regressions: reproduce P1 owner-mode history using embedded /tmp/t0041-discovery-probe.py; run PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0041-discovery-probe.py. Other exact commands and source below. Sources are embedded because /tmp persistence is not guaranteed.
- Aggregate gate: not run; python3 tools/verify.py; owner=this reviewer, initial discovery; suppressed by decisive F-01.
- Next: implementer corrects F-01 -> affected required architecture/maintainability proof including G-01 -> affected registry synchronization -> fresh discovery completes current/unfinished rows and owns justified aggregate -> separate acceptance decision.
```

## Reproducible reviewer probes

Extract each block to its named `/tmp` path and invoke with the exact command from section 5. These are disposable review fixtures, not repository test changes. The P1 owner-mode reproduction succeeds as a script while demonstrating an incorrect passed product result; after correction, its output must show refusal/blocking rather than passed.

### /tmp/t0041-discovery-probe.py

```python
import sys,json,copy,subprocess,os,hashlib
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
from test_actor_operations import ActorOperationsTest

def fixture():
 t=ActorOperationsTest();t.setUp();return t

t=fixture()
try:
 c,r,op,counter=t.producer_run()
 expected=(t.repo/'allowed.txt').read_bytes()
 a=c.inspect_candidate(r,op);assert a['status']=='passed',a
 candidate=json.loads((r/a['path']).read_text());assert candidate['workspace']['files']['allowed.txt']['sha256']==hashlib.sha256(expected).hexdigest()
 reservation=t.reserve(r,'verify','independent-pass');result=c.check_candidate(r,reservation['assignment'],timeout_seconds=5);assert result['status']=='passed',result
 record=json.loads((r/result['execution_path']).read_text());c._state_module.validate_command_execution_record(record,expected_closure_identity=record["closure_identity"])
 bad=copy.deepcopy(record);bad['execution_mechanism']='implicit_fallback'
 try:c._state_module.validate_command_execution_record(bad,expected_closure_identity=record["closure_identity"])
 except ValueError:pass
 else:raise AssertionError('validator accepted invalid mechanism')
 snapshot=(r/'ledger.json').read_bytes();assert result==c.check_candidate(r,reservation['assignment'],timeout_seconds=5);assert snapshot==(r/'ledger.json').read_bytes();assert counter.read_bytes()==b'x'
 fresh=t.reserve(r,'verify','independent-fresh');again=c.check_candidate(r,fresh['assignment'],timeout_seconds=5);assert again['status']=='passed';assert counter.read_bytes()==b'xx';assert again['path']!=result['path']
 (t.repo/'allowed.txt').write_bytes(b'X'+expected[1:]);assert c.status_run(r)['evidence']['verify']['status']=='stale';assert c.check_candidate(r,fresh['assignment'],timeout_seconds=5)['status']=='stale';assert counter.read_bytes()==b'xx'
 print('PUBLIC pass, independent file digest, executable validator valid/invalid, replay, new rerun, same-size drift: PASS')
finally:t.tearDown()

t=fixture()
try:
 c,r,op,counter=t.producer_run();(t.repo/'allowed.txt').write_text('wrong product\n')
 assert c.inspect_candidate(r,op)['status']=='passed';v=t.reserve(r,'verify','independent-fail');result=c.check_candidate(r,v['assignment'],timeout_seconds=5);assert result['status']=='failed',result
 print('PUBLIC real product failure: PASS, status='+result['status'])
finally:t.tearDown()

t=fixture()
try:
 owner=t.repo/'owner.txt';owner.write_text('base\n');subprocess.run(['git','-C',str(t.repo),'add','owner.txt'],check=True);subprocess.run(['git','-C',str(t.repo),'commit','-qm','owner'],check=True)
 owner.write_text('dirty owner content\n')
 c,r,op,counter=t.producer_run();before=c.capture_git_status(t.repo)['owner.txt'];owner.chmod(0o755);after=c.capture_git_status(t.repo)['owner.txt'];result=c.inspect_candidate(r,op)
 print('OWNER MODE probe:',json.dumps({'status_equal':before==after,'result':result,'mode':oct(owner.stat().st_mode&0o777)}))
finally:t.tearDown()
```

### /tmp/t0041-discovery-yolo.py

```python
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
from test_verification_runner import VerificationExecutorLocalProcessTests as Cases
# Invoke only portable YOLO controls directly; the class decorator gates legacy sandbox tests on macOS.
for name in ('test_explicit_yolo_uses_production_runner_without_sandbox_substitution','test_invalid_yolo_authority_never_executes','test_yolo_timeout_reuses_owned_group_cleanup','test_yolo_timeout_descendant_cleanup','test_yolo_sigterm_resistant_descendant_cleanup','test_yolo_exited_parent_open_pipe_cleanup'):
 case=Cases(name);case.setUp()
 try:getattr(case,name)();print(name+': PASS',flush=True)
 finally:case.tearDown()
```

### /tmp/t0041-discovery-ignored.py

```python
import sys, json, threading
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
import test_controller as fixtures
from test_actor_operations import ActorOperationsTest
for mode in ('generated','before','during'):
 t=ActorOperationsTest();t.setUp()
 try:
  c=fixtures.load_controller();original=c.init_run
  def init(run,policy,manifest,repo):
   d=json.loads(manifest.read_text());d['tasks'][0]['allowed_paths'].append('ignored.cfg');manifest.write_text(json.dumps(d))
   with (repo/'.gitignore').open('a') as f:f.write('ignored.cfg\ngenerated.out\n')
   (repo/'ignored.cfg').write_text('original')
   return original(run,policy,manifest,repo)
  c.init_run=init
  waiting=t.root/'waiting';release=t.root/'release'
  setup="\nPath('ignored.cfg').read_text()\nPath('generated.out').write_text('generated')\n"
  if mode=='during':setup+=f"import time\nPath({str(waiting)!r}).touch()\nwhile not Path({str(release)!r}).exists(): time.sleep(.01)\n"
  with mock.patch.object(fixtures,'load_controller',return_value=c):c,r,op,counter=t.producer_run(setup)
  assert c.inspect_candidate(r,op)['status']=='passed'
  if mode=='before':
   (t.repo/'ignored.cfg').write_text('modified');assert c.status_run(r)['evidence']['implement']['status']=='stale';assert t.reserve(r,'verify','stale')['status']=='refused';assert not counter.exists()
  else:
   a=t.reserve(r,'verify',mode)['assignment'];results=[]
   thread=threading.Thread(target=lambda:results.append(c.check_candidate(r,a,timeout_seconds=5)));thread.start()
   try:
    if mode=='during':t.wait_file(waiting);(t.repo/'ignored.cfg').write_text('modified')
   finally:release.touch();thread.join(8)
   assert not thread.is_alive();assert results[0]['status']==('stale' if mode=='during' else 'passed'),results
  print('Ignored evaluated input/generated output '+mode+': PASS',flush=True)
 finally:t.tearDown()
```

### /tmp/t0041-discovery-matrix.py

```python
import sys,subprocess
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
from test_actor_operations import ActorOperationsTest
for mode in ('dirty_allowed','outside_tracked','untracked_modify','untracked_add','untracked_remove','index','configuration'):
 t=ActorOperationsTest();t.setUp()
 try:
  if mode=='dirty_allowed':(t.repo/'allowed.txt').write_text('owner dirty content\n')
  if mode=='outside_tracked':
   (t.repo/'outside').write_text('base');subprocess.run(['git','-C',str(t.repo),'add','outside'],check=True);subprocess.run(['git','-C',str(t.repo),'commit','-qm','outside'],check=True)
  c,r,op,counter=t.producer_run()
  if mode=='outside_tracked':(t.repo/'outside').write_text('violation')
  a=c.inspect_candidate(r,op)
  if mode in ('dirty_allowed','outside_tracked'):assert a['status']=='blocked',a
  else:
   assert a['status']=='passed';v=t.reserve(r,'verify','matrix');result=c.check_candidate(r,v['assignment'],timeout_seconds=5);assert result['status']=='passed',result
   if mode=='untracked_modify':(t.repo/'test_targeted.py').write_text('replaced')
   elif mode=='untracked_add':(t.repo/'new-file').write_text('added')
   elif mode=='untracked_remove':(t.repo/'test_targeted.py').unlink()
   elif mode=='index':subprocess.run(['git','-C',str(t.repo),'add','allowed.txt'],check=True)
   else:(t.repo/'.gitignore').write_text('different config\n')
   snapshot=(r/'ledger.json').read_bytes();assert c.status_run(r)['evidence']['verify']['status']=='stale';assert c.check_candidate(r,v['assignment'],timeout_seconds=5)['status']=='stale';assert snapshot==(r/'ledger.json').read_bytes();assert counter.read_bytes()==b'x'
  print(mode+': PASS',flush=True)
 finally:t.tearDown()
```

### /tmp/t0041-discovery-baseline.py

```python
import sys,tempfile,subprocess,unittest
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
import test_verification_runner as t
with tempfile.TemporaryDirectory() as root:
 root=Path(root)
 for name in ('verification_runner.py','controller_state.py'):
  (root/name).write_bytes(subprocess.check_output(['git','show','HEAD:skills/task-orchestrator/scripts/'+name]))
 t.RUNNER_PATH=root/'verification_runner.py'
 result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(t.VerificationSandboxFailClosedTests))
 print('HEAD baseline:',len(result.failures),'failures',len(result.errors),'errors')
```
