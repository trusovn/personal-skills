# Task Review Discovery Report: T-004.1 — correction discovery

| Field | Value |
|---|---|
| Producing stage | task-review-discovery |
| Coverage completeness | partial — only V-07d/e supported-host legacy proof remains blocked |
| Discovery iteration | 2, fresh independent correction discovery |
| Created at | 2026-11-11T06:52:10.024601+00:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report | skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-02.md |
| Authority | skills/task-orchestrator/docs/tasks/T-004.1/brief.md r1 |
| Preparation/context | verification.md r1; preflight.md; controller-contract.md; parent T-004/brief.md; docs/direction-single-task-sbx.md, relative to task docs |
| Submission | implementation-report.md; correction-01.md; maintainability-02.md; contract-registry-02.md |

Evidence only: no acceptance verdict, no approved deferral, no advancement. This report applies only to identified reviewed bytes; it does not review or authenticate itself.

## 1. Discovery provenance

This newly spawned reviewer session authored no reviewed production or test assets. Independent evidence authority: yes. Active skill resolved and read at `.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`, including its report template; installation not refreshed. No subagents, production/test edits, commits, staging, network, provider, package installation or live model check performed. Disposable probes and raw logs are under `/tmp`; only this report is a repository write.

HEAD `aa99736e0fb02733d07e62aa382dbcee2ae46f1b`; complete staged binary diff SHA-256 `0c7c8a7da6c19674f494b8ba79632066cd64f18440addb1d492a516f4ba8e2b2`; complete unstaged binary diff SHA-256 `011a42d9673921c91bd60d97366a53b086ac76a1e4867ad9ce5374500f7c7ba8`. Staged original submission and unstaged correction are distinct; seven reviewed Python index/worktree identities appear below. No mixed authorship is inferred from matching status text. Prior pass labels are navigation only; current evidence is listed here.

## 2. Findings and continuity

No new findings.

F-01 (prior suggested P2) is corrected in the reviewed bytes: exact previous dirty owner chmod reproducer now returns `blocked`, reason `scope_or_owner_work_violation`, paths `["owner.txt"]`, while status remains identical and mode is 0755. Current public regression execution also verifies unchanged-owner positive controls, dirty files inside/outside allowed paths, symlink referent content and executable mode, no check invocation, and unchanged ledger after rejection. Code uses one Git-owned `_capture_file_identity` for baseline and candidates, compares every dirty path before publication, and retains staged-path/index checks. A valid frozen older dirty baseline without `dirty_files` is refused before candidate/check publication; no frozen record is migrated. Correction owner was implementer; evidence owner is this fresh reviewer; disposition/advancement authority is separate acceptance.

G-01 (prior blocked evidence gap, not a product defect) has current reviewer-owned evidence in maintainability-02.md: original B → fresh R, limits reconciliation,11 hotspot rationale dispositions and current architecture proof. This session corroborated B12/R7 inventory, complete/compared R, identical I/R identities and all7 current file hashes. No general maintainability review was repeated. Separate acceptance consumes that conditional evidence.

## 3. Completeness ledger

Frozen pre-aggregate ledger at `/tmp/t0041-correction-discovery-ledger-before.txt` retained all48 prior IDs before broad execution. Every V row consumes the matching submitted scenario claim from implementation-report.md/correction-01.md. Setup/oracle for P1/MATRIX/IGNORED/ACTOR: disposable real Git repository and external controller run directory, actual public initialization and local fake-Codex terminal producer, real product-reading check, independent file observations, durable record/log bytes, external launch counter. Actor fixture does not qualify sbx/provider. GIT uses actual temporary Git paths/rename/delete/mode. RUNNER/YOLO/EXTRA use actual local subprocess argv, markers/logs and injected I/O failure only at the publication boundary. No schema-only behavioral pass is claimed. Current pass means the listed bounded evidence or explicit interface trace agrees with its oracle; finite limitations stay named.

| Row | AC/invariant | Explicit material cases | Prior status | Current independent evidence/oracle | Current result |
|---|---|---|---|---|---|
| V-01 | AC-01 | Terminal producer; real tracked bytes; literal paths; actor claims grant no pass | pass | P1 independently compares allowed.txt SHA-256; GIT literal/unusual path controls; actor actual terminal outcome, no actor-summary authority | pass |
| V-02a | AC-01 | Unchanged dirty owner setup remains intact while allowed clean file changes | pass | ACTOR dirty-owner five-case positive controls: unchanged owner identities pass while allowed clean file changes; GIT baseline controls | pass |
| V-02b | AC-01 | Dirty allowed content change; hidden staging change; dirty file mode change | fail | P1 exact prior owner chmod now blocked with same porcelain; ACTOR five mode/referent cases inside/outside scope block without ledger write/check; MATRIX dirty_allowed plus actor hidden_staged | pass |
| V-02c | AC-01 | New tracked change outside scope | pass | MATRIX outside_tracked blocks | pass |
| V-02d | AC-01 | New untracked change outside scope | pass | ACTOR scope_and_invalid_timeout adds outside.txt and blocks | pass |
| V-03a | AC-01/02 | Wrong stage, absent/wrong operation; wrong run/task | pass | ACTOR assignment_refusals + current _producer_context/inspect_candidate terminal stage/operation guards | pass |
| V-03b | AC-01/02 | Wrong stage, absent/wrong operation; wrong run/task | pass | ACTOR assignment_refusals wrong run/task/operation; no mutation/launch | pass |
| V-03c | AC-01/02 | Wrong input/policy/flow/baseline binding | pass | ACTOR assignment_refusals, REVISION8; current baseline digest guard traced; EXTRA valid old frozen dirty baseline refuses without mutation | pass |
| V-03d | AC-01/02 | Live or unknown upstream actor cannot establish stable candidate/check | pass | UPSTREAM test_v05g + current active actor guard before inspection publication | pass |
| V-03e | AC-01/02 | Live or unknown upstream actor cannot establish stable candidate/check | pass | UPSTREAM test_v05g + unknown ownership guard; actor interruption/refusal controls | pass |
| V-03f | AC-01/02 | Second check/inspection while real check owns command lock | pass | ACTOR synchronized drift/check exclusion: real command owns lock, second inspection/check refuses | pass |
| V-04a | AC-02 | Same-size tracked bytes change after passing check | pass | P1 same-size tracked drift after real pass; stale with unchanged invocation counter | pass |
| V-04b | AC-02 | Visible untracked modify/add/remove independently | pass | MATRIX independent untracked modify/add/remove all stale; no rerun or ledger rewrite | pass |
| V-04c | AC-02 | Index-only change, HEAD/baseline drift | pass | MATRIX index-only stale; GIT identity controls; current HEAD and complete workspace comparisons traced | pass |
| V-04d | AC-02 | Evaluated configuration bytes change | pass | MATRIX configuration and IGNORED evaluated input before/during changes | pass |
| V-04e | AC-02 | Approved task-input/policy/flow revisions | pass | REVISION8 current cases and _producer_context/_load_current_candidate identity checks | pass |
| V-05a | AC-02 | Irrelevant ignored generated output leaves candidate current | pass | IGNORED generated output actual real check passes with candidate current | pass |
| V-05b | AC-02 | Ignored evaluated input drift before checking refuses eligibility | pass | IGNORED before: evaluated ignored input change makes status stale and reservation refuse; no counter | pass |
| V-05c | AC-02 | Ignored evaluated input changes at synchronized real-process checkpoint | pass | IGNORED during: synchronized actual check exits zero but result stale | pass |
| V-06 | AC-03/04 | Actual argv, logs, exit, environment, candidate; replacement-process replay | pass | P1 actual public record/log/check/replay; actual validator accepts record and rejects implicit_fallback; YOLO binary output/literal argv control | pass |
| V-07a | AC-03 | Exact explicit frozen YOLO authority versus absent/incomplete/invalid | pass | YOLO exact explicit authority real invocation and invalid authority/type matrix; public context loads frozen policy | pass |
| V-07b | AC-03 | Exact explicit frozen YOLO authority versus absent/incomplete/invalid | pass | YOLO invalid/incomplete/false/nonboolean/other transport refuse before marker/log; absent authority traced to legacy builder | pass |
| V-07c | AC-03 | Legacy policy on unsupported host refuses without fallback | pass | RUNNER current unsupported-host refusal passes; no unrestricted fallback; BASELINE same unsupported-host errors | pass |
| V-07d | AC-03 | Legacy launch-capability failure and real supported restrictive containment | blocked | Blocked: Linux lacks macOS /usr/bin/sandbox-exec; supported launch-failure/containment oracle unavailable. Supported-host verifier owns evidence | blocked |
| V-07e | AC-03 | Legacy launch-capability failure and real supported restrictive containment | blocked | Blocked: Linux lacks macOS /usr/bin/sandbox-exec; real restrictive filesystem/network containment cannot run. Supported-host verifier owns evidence | blocked |
| V-08a | AC-03 | Prohibited shell/malformed commands, invalid later command before any launch | pass | RUNNER parsing/shell denial cases and ACTOR invalid_later_command: later invalid command prevents all launch | pass |
| V-08b | AC-03 | Forbidden install versus explicit permission; planning only | pass | RUNNER closed installation-denial table/current allowed planning control; no package installation executed | pass |
| V-08c | AC-03 | Forbidden install versus explicit permission; planning only | pass | RUNNER explicit dependency permission is planning evidence only; no package installation executed | pass |
| V-08d | AC-03 | Quoted literal argv and near-miss non-install | pass | RUNNER parser near-miss controls and YOLO actual literal filename with metacharacters | pass |
| V-09a | AC-04 | Real wrong product exits nonzero without correction charge | pass | P1 real wrong-product failure; ACTOR failed_product evidence/count/history | pass |
| V-09b | AC-04 | Missing required executable blocks before any command | pass | ACTOR missing_later_executable blocks before any command/invocation | pass |
| V-09c | AC-04 | No check evidence is missing/not-run, never passed | pass | P1 before-check inspect and status: no passed check; _evidence_view missing default and runner empty-plan classification traced | pass |
| V-09d | AC-04 | Known issue cannot excuse required failed check | pass | Current check_candidate clears authorized_gap before planning; P1 actual required product failure; RUNNER current gap-planning cases | pass |
| V-09e | AC-04 | Targeted-only repository gate omission is explicit | pass | ACTOR actual targeted-only receipt policy_omissions; targeted branch traced | pass |
| V-09f | AC-04 | Failure stops later command | unchecked | EXTRA direct production YOLO targeted failure followed by marker command: one failed outcome, later marker/log absent | pass |
| V-10a | AC-02/04 | Tracked and untracked drift while real command waits | pass | ACTOR synchronized actual check before/after drift; zero-exit cannot yield current pass | pass |
| V-10b | AC-02/04 | Tracked and untracked drift while real command waits | pass | ACTOR actual check side effect makes candidate/check stale | pass |
| V-10c | AC-02/04 | Check side effect changes evaluated input despite exit zero | pass | YOLO real timeout and descendant cleanup controls; PID/process-group disappearance with bounded waits | pass |
| V-10d | AC-03/04 | Finite timeout, descendants, resistant child, exited parent/open pipe | pass | YOLO resistant descendant and exited-parent inherited open-pipe cleanup controls | pass |
| V-10e | AC-02/03 | Zero/negative/NaN/infinite/nonnumeric/boolean timeout refuses without launch | pass | ACTOR invalid-timeout finite/type matrix: no ledger or launch mutation | pass |
| V-11a | AC-02 | Completed API/CLI/reloaded replay executes exactly once | pass | P1 public replay plus ACTOR replacement CLI/API immutable replay; counter unchanged | pass |
| V-11b | AC-02/03 | Real controller killed before launch/during synchronized command; replay cannot relaunch | pass | ACTOR actual killed check coordinator before launch; unknown intent blocks relaunch | pass |
| V-11c | AC-02/03 | Real controller killed before launch/during synchronized command; replay cannot relaunch | pass | ACTOR actual killed check coordinator during process; unknown owner no second execution | pass |
| V-11d | AC-02 | Receipt published before ledger result; reload reconciles without rerun | pass | ACTOR actual killed coordinator after receipt; reload reconciles without rerun | pass |
| V-11e | AC-02/03 | Existing log collision and injected publication failure | unchecked | ACTOR log collision preserves bytes; EXTRA direct YOLO injected stdout log write failure raises RuntimeError, cannot publish complete execution record | pass |
| V-12 | AC-01/02/04 | Real failure -> admitted correction -> new pass; old receipt immutable; charge only correction | pass | ACTOR failed_product_correction_retains_history: failure then admitted correction then distinct pass, old receipt retained, correction_count1 | pass |
| V-13 | AC-05 | Actual API/CLI, identity, replay and collector fresh rerun documented | pass | Current controller-contract/API/CLI/record trace, correction-01 and registry02 caveat; P1 distinct reservation key runs genuinely new check, old key replays | pass |
| G-01 | Conditional maintainability | Current reviewer-owned original-B comparison, rationale dispositions and native evidence | blocked | Current maintainability02 reviewer-owned original-B R, complete compared,11 rationale dispositions/limits; independent I/R/current7 hash equality and identical tool/settings identity confirmed | pass |

## 4. Adversarial state/evidence observations

- P1 independently read actual allowed bytes, validated the actual execution record, then invalidated mechanism to `implicit_fallback` and observed validator refusal. Real rerun under a distinct operation key increments counter; identical completed assignment replay does not.
- Owner-work identity: unchanged dirty work passes; mode/referent changes with equal Git status cannot publish. Old frozen dirty baseline refuses without ledger/check/candidate side effects. Hidden staging protection remains exercised. Relevant same-size tracked/untracked/index/config and ignored evaluated drift makes evidence stale; irrelevant generated output keeps it current.
- Latest/historical producer and correction/check history, one active command owner, real command-lock exclusion, before/during/after interruption and durable replay are exercised by current producer20. The six direct YOLO controls include descendant PID/process-group absence and inherited-pipe release with bounded waits; no test depends on arbitrary success sleeps.
- EXTRA now supplies missing V-09f and V-11e direct portable evidence: failure prevents later marker/log; injected log streaming failure cannot create complete execution JSON. These controls use explicit frozen-shape authorization on the production runner, with no sandbox-invocation substitution.

## 5. Independent command records

All commands run from repository root on Linux with `PYTHONDONTWRITEBYTECODE=1`; no external services. Raw logs remain at paths below. Disposable fixtures tear down local trees/processes; direct group controls confirm bounded terminal cleanup. Commands that tail logs are not treated as suite exit evidence: results come from preserved unittest summaries/raw observations.

| ID | Exact command | Result / raw log |
|---|---|---|
| P1 | `python3 /tmp/t0041-correction-discovery-probe.py` | Public actual pass/fail, validation, replay/new rerun, same-size drift pass; owner chmod now blocked. `/tmp/t0041-correction-discovery-probe.log` |
| YOLO | `python3 /tmp/t0041-correction-discovery-yolo.py` | Six direct controls pass, including resistant descendants/open pipe. `/tmp/t0041-correction-discovery-yolo.log` |
| IGNORED | `python3 /tmp/t0041-correction-discovery-ignored.py` | generated/before/during histories3 pass. `/tmp/t0041-correction-discovery-ignored.log` |
| MATRIX | `python3 /tmp/t0041-correction-discovery-matrix.py` | Seven dirty/scope/drift histories pass. `/tmp/t0041-correction-discovery-matrix.log` |
| EXTRA | `python3 /tmp/t0041-correction-discovery-extra.py` | Later-command failure control, publication I/O failure, and valid old frozen dirty-baseline refusal pass. `/tmp/t0041-correction-discovery-extra.log` |
| ACTOR | `python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_producer` |20 pass, including five current dirty-owner cases. `/tmp/t0041-correction-discovery-actor.log` |
| GIT | `python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_git.py` |14 pass. `/tmp/t0041-correction-discovery-git.log` |
| REVISION | `python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py -k ControllerInputRevisionTest` |8 pass. `/tmp/t0041-correction-discovery-revision.log` |
| UPSTREAM | `python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_v05g` |1 pass. `/tmp/t0041-correction-discovery-upstream.log` |
| RUNNER | `python3 -m unittest discover -s skills/task-orchestrator/tests -p test_verification_runner.py` |40 run,5fail/1error/20skip; failures/errors reach unsupported macOS sandbox. `/tmp/t0041-correction-discovery-runner.log` |
| BASELINE | `python3 /tmp/t0041-correction-discovery-baseline.py` | HEAD runner/state seven fail-closed tests reproduce5fail/1error. `/tmp/t0041-correction-discovery-baseline.log` |
| LEGACY-BASELINE | `python3 /tmp/t0041-correction-discovery-legacy-baseline.py` | Pre-correction staged four runtime modules in disposable skill copy: seven legacy inspection host cases reproduce1fail/6errors, all UnsupportedSandbox. `/tmp/t0041-correction-discovery-legacy-baseline-02.log` |

The first LEGACY-BASELINE setup mixed a temporary controller with the original `LEGACY_CONTROLLER` command's captured import path and produced7 baseline-shape errors. No product conclusion came from that invalid setup. Corrected script sets both paths before invoking real tests and reproduces the exact current host-only subset; failed setup log retained at `/tmp/t0041-correction-discovery-legacy-baseline.log`. Its corrected attribution is diagnostic corroboration, not behavioral qualification.

## 6. Aggregate gate

`PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py`, owner this reviewer / correction discovery, **failed**:7 checks,1 failed. Raw authoritative log `/tmp/t0041-correction-discovery-aggregate.log`.

Justified after all safely runnable material rows had current targeted evidence; no current decisive targeted product failure; host rows V-07d/e had concrete unavailable non-gate oracle. This aggregate supplies repository regression evidence and cannot close those unavailable host rows. Orchestrator251 tests:6fail/7error/20skip, exact UnsupportedSandbox subsets independently reproduced above. Root311 tests passed with32 skips; other skill suites, registry8/35 and profile112 drift check passed. The skipped dedicated-analyzer/real-tool tests are not successful qualification. No all-green claim and no new platform waiver. Conditional architecture proof remains current in maintainability02 and the root aggregate constituent; no native duty is replaced with metrics.

## 7. Scope and reviewed identities

Scope remains four runtime modules and three focused test modules from T-004.1, with unstaged correction limited to controller.py, controller_git.py and test_actor_operations.py. Registry/reference changes belong to the updater; correction-01 and new numbered stage reports carry results. Existing parent/T-004.2/task index planning and .DS_Store files are preserved owner context, not authored/reclassified here. No authority/scope/dependency/permission revision or installation refresh occurred. Maintainability02 covers exact current seven hashes and the original baseline; registry02 synchronizes dirty owner identity without adding private helper contracts.

| Reviewed Python path | Index blob | Worktree SHA-256 |
|---|---|---|
| skills/task-orchestrator/scripts/controller.py | `9cd4360ec4b484528644dd098e34a7f27187fe77` | `1ff6e43f73d1a52a704f16ec63b0720f8928f37de743568f42153a8da03385ef` |
| skills/task-orchestrator/scripts/controller_git.py | `a5ee4517bf5c22c256c91910fb109f7899f13d5d` | `746ab7fa695b15ff2b9f68eb9198b4d9cb41a2802836c0e7a7736251d2bc553a` |
| skills/task-orchestrator/scripts/controller_state.py | `f06371275fcbe6a17b0ff383bb8af7a1d53801f9` | `a30ab322e417a62b936d5198e8297d41214a0c106a43c3dfdf262f5a6bac97a4` |
| skills/task-orchestrator/scripts/verification_runner.py | `720c81e94c4ebd3bb99fe967a4d12ca5470275b5` | `d7b7b19672fd4cfbca87e7400f7ee8fe51f66207f20c332dd5c6868f0c80fb2a` |
| skills/task-orchestrator/tests/test_actor_operations.py | `91423d7c6e7ced53f8a0b979d943731e22b91f4b` | `2a38d65634701a51a8e9e198eb05b6b739bd5b927111ac8e87b5bc385e6a7d14` |
| skills/task-orchestrator/tests/test_controller_git.py | `cf29efc77e7047c49c92c7be3a3f077f385e5025` | `70db0929b22c6f821666ec090bed0b1736e355c496621a830c6004b718359cbd` |
| skills/task-orchestrator/tests/test_verification_runner.py | `b0cee869e038a008299f5960063d70aa2c249261` | `deb48747c12f518d7f0774b5c0c1cdc2d24d14aa3e6af5f7f93ff1f687ddbf44` |

## 8. Unchecked work and residual limits

- V-07d/e remain **blocked**, unchanged reason: Linux lacks real macOS `/usr/bin/sandbox-exec`; supported-host verifier owns launch-capability-failure and actual restrictive containment proof. Separate acceptance owns disposition; this report approves no deferral. Exact rerun command on supported host: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_verification_runner.py` plus relevant legacy inspection suite. Current failures/skips are not passes.
- V-09f/V-11e and G-01 previously incomplete now have current evidence above. F-01 has corrected public regression evidence; no confirmed unresolved product defect was found in this bounded discovery.
- Six portable YOLO tests remain underneath the inherited macOS-only class decorator; default Linux suite skips them. Current direct execution provides evidence for this report, without claiming automatic Linux coverage was repaired.
- No real sbx/provider qualification, generic arbitrary file-read discovery, power-loss recovery or tamper resistance established. T-006 and T-004.2 retain their existing scopes. Metrics are advisory and schema/registry checks structural.

## 9. Completeness and next route

Partial because V-07d/e host-specific proof is unavailable; all48 identities and every prior finding/gap retained, with46 current pass rows and2 blocked rows. Next consumer: separate fresh `task-acceptance-review` decision, receiving this report, brief r1, verification r1, preflight, controller-contract/owner direction, current staged+unstaged scoped diff, implementation-report/correction01, maintainability02 with exact B/I/R pairs, registry02 and both blocked rows. The decision may route missing supported-host evidence to its owner; this report never advances the task.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity:2; HEAD aa99736e0fb02733d07e62aa382dbcee2ae46f1b; staged diff 0c7c8a7da6c19674f494b8ba79632066cd64f18440addb1d492a516f4ba8e2b2; unstaged diff 011a42d9673921c91bd60d97366a53b086ac76a1e4867ad9ce5374500f7c7ba8; seven separate index/worktree hashes above.
- Coverage rows: V-01=pass; V-02a=pass; V-02b=pass; V-02c=pass; V-02d=pass; V-03a=pass; V-03b=pass; V-03c=pass; V-03d=pass; V-03e=pass; V-03f=pass; V-04a=pass; V-04b=pass; V-04c=pass; V-04d=pass; V-04e=pass; V-05a=pass; V-05b=pass; V-05c=pass; V-06=pass; V-07a=pass; V-07b=pass; V-07c=pass; V-07d=blocked; V-07e=blocked; V-08a=pass; V-08b=pass; V-08c=pass; V-08d=pass; V-09a=pass; V-09b=pass; V-09c=pass; V-09d=pass; V-09e=pass; V-09f=pass; V-10a=pass; V-10b=pass; V-10c=pass; V-10d=pass; V-10e=pass; V-11a=pass; V-11b=pass; V-11c=pass; V-11d=pass; V-11e=pass; V-12=pass; V-13=pass; G-01=pass.
- Finding IDs: F-01 prior P2 corrected, current regression corroborated; no new findings. G-01 prior blocked conditional evidence gap supplied by maintainability02 and verified current.
- Continuity: prior pass rows re-established via named current probes/traces; V-02b prior fail now pass through owner chmod/symlink and hidden staging controls; V-09f/V-11e prior unchecked now pass direct portable controls; G-01 prior blocked now pass current reviewer evidence; V-07d/e remain blocked absent macOS oracle. Implementer owns corrections, fresh reviewer owns discovery evidence, supported-host verifier owns missing capability proof, separate acceptance owns verdict/advancement. Influenced siblings: dirty allowed/out-of-scope files, executable metadata and symlink referent/link semantics.
- Preparation/context: skills/task-orchestrator/docs/tasks/T-004.1/brief.md r1, verification.md r1, preflight.md, controller-contract.md, correction-01.md, implementation-report.md, parent T-004 and owner direction.
- Reviewer regressions: python3 /tmp/t0041-correction-discovery-probe.py; python3 /tmp/t0041-correction-discovery-extra.py; PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_producer. Custom sources below and prior report embedded probes.
- Aggregate gate: failed7checks/1failed; PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py; owner correction discovery; host legacy subsets reproduced, root32/orchestrator20 skips explicit.
- Next: separate fresh task-acceptance-review decision consumes current report and blocked host rows; supported-host evidence remains owed to its owner.
```

## Reproducible reviewer probes

P1/YOLO/IGNORED/MATRIX/HEAD-BASELINE source is exactly the matching embedded Python block in discovery-01.md, extracted to `/tmp/t0041-correction-discovery-*.py` by replacing `/tmp/t0041-discovery-` in the heading with `/tmp/t0041-correction-discovery-`; no source change. P1 now prints the corrected blocked owner result instead of the earlier pass. New scripts:

### /tmp/t0041-correction-discovery-extra.py

```python
import sys,json,subprocess
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
from test_verification_runner import VerificationExecutorLocalProcessTests as Cases
from test_actor_operations import ActorOperationsTest
import test_controller as fixtures
for name in ('test_targeted_failure_prevents_the_later_command','test_log_write_failure_cannot_publish_a_complete_record'):
 case=Cases(name);case.setUp()
 try:case.yolo_cleanup_control(getattr(case,name));print(name+': PASS',flush=True)
 finally:case.tearDown()
t=ActorOperationsTest();t.setUp()
try:
 (t.repo/'owner.txt').write_text('baseline owner\n')
 c=fixtures.load_controller();original=c._git_module.capture_task_baseline
 def old_baseline(repo):
  baseline=original(repo);baseline.pop('dirty_files');return baseline
 with mock.patch.object(c._git_module,'capture_task_baseline',side_effect=old_baseline), mock.patch.object(fixtures,'load_controller',return_value=c):
  c,r,op,counter=t.producer_run()
 before=(r/'ledger.json').read_bytes();result=c.inspect_candidate(r,op)
 assert result['status']=='refused' and 'Frozen baseline lacks owner/index identity' in result['reason'],result
 assert before==(r/'ledger.json').read_bytes();assert not counter.exists()
 assert not list((r/'candidates').glob('*')) if (r/'candidates').exists() else True
 print('PUBLIC valid frozen legacy dirty baseline refusal preserves ledger and no candidate/check: PASS',flush=True)
finally:t.tearDown()
```

### /tmp/t0041-correction-discovery-legacy-baseline.py

```python
import sys,tempfile,subprocess,shutil,unittest
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'skills/task-orchestrator/tests'))
import test_controller as t
names=['test_authorized_gap_cannot_excuse_a_targeted_failure','test_failed_verification_offers_resume_only_when_policy_escalates','test_inspect_keeps_pending_semantic_review_non_accepting','test_repository_gate_authorized_gap_preserves_pending_review','test_verifier_created_content_drift_is_recorded_and_denies_accept','test_verifier_created_drift_replay_reuses_published_records','test_inspect_reuses_execution_after_crash_with_review_pending']
with tempfile.TemporaryDirectory(prefix='t0041-discovery-baseline-') as base:
 root=Path(base)/'task-orchestrator'
 shutil.copytree('skills/task-orchestrator',root,ignore=shutil.ignore_patterns('docs','tests','__pycache__'))
 for name in ('controller.py','controller_git.py','controller_state.py','verification_runner.py'):
  (root/'scripts'/name).write_bytes(subprocess.check_output(['git','show',':skills/task-orchestrator/scripts/'+name]))
 t.LEGACY_CONTROLLER[-1]=t.LEGACY_CONTROLLER[-1].replace(str(t.CONTROLLER_PATH.parent),str(root/'scripts'))
 t.CONTROLLER_PATH=root/'scripts/controller.py'
 result=unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(t.ControllerInspectionIntegrationTest(n) for n in names))
 print('PRE-CORRECTION INDEX legacy host subset:',len(result.failures),'failures',len(result.errors),'errors')
```

## Publication provenance

Exact Git status before publication:

```text
M  README.md
M  docs/contracts/index.json
MM docs/contracts/task-orchestrator.json
A  skills/task-orchestrator/docs/tasks/T-004.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-004.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-004.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-004.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-004/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/references/architecture-map.md
M  skills/task-orchestrator/references/operator-guide.md
MM skills/task-orchestrator/scripts/controller.py
MM skills/task-orchestrator/scripts/controller_git.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/scripts/verification_runner.py
MM skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_verification_runner.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-004.1/correction-01.md
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-02.md
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-02.md
```

Exact Git status after publication:

```text
M  README.md
M  docs/contracts/index.json
MM docs/contracts/task-orchestrator.json
A  skills/task-orchestrator/docs/tasks/T-004.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-004.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-004.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-004.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-004.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-004.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-004/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/references/architecture-map.md
M  skills/task-orchestrator/references/operator-guide.md
MM skills/task-orchestrator/scripts/controller.py
MM skills/task-orchestrator/scripts/controller_git.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/scripts/verification_runner.py
MM skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_verification_runner.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-004.1/correction-01.md
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/contract-registry-02.md
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/discovery-02.md
?? skills/task-orchestrator/docs/tasks/T-004.1/reviews/maintainability-02.md
```

Only the new report entry differs; reviewed source/test/index identities stayed unchanged.
