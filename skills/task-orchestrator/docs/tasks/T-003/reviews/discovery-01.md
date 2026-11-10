# Task review discovery: T-003 and staged repo-foundation supplement

- Producing stage: `task-review-discovery`; first independent discovery pass.
- Coverage: **partial** — current Draft 2020-12 schema boundaries could not execute; actual sbx/provider V-13 remains unrun. All material rows have explicit dispositions below.
- Created: 2026-11-09T18:39:01.748018+00:00.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Report: `skills/task-orchestrator/docs/tasks/T-003/reviews/discovery-01.md`.
- Task authority: `brief.md` revision 1, `verification.md` revision 1, `preflight.md` including Decision context; current `controller-contract.md`; owner-confirmed `direction-single-task-sbx.md`, accepted plan review and cited plan/predecessor contracts. T-002.1 acceptance-02, T-002.2 acceptance-01 and T-002.3 acceptance-02 remain predecessor context.
- Submission: `implementation-report.md`, its V-01..14 map and evidence logs, and `reviews/maintainability-01.md`. The user's staged-data request additionally includes the foundation/registry changes, assessed against their staged reference, schema, README/development and executable contracts. They are not silently assigned to T-003's original allowed-path list.

This report publishes evidence only. It contains no acceptance decision, approved deferral or advancement. It applies only to the identified reviewed bytes; changed bytes require new evidence. The report does not review or authenticate itself.

## Provenance and scope

This session authored none of the reviewed production or test bytes. Evidence below is independent of implementation authorship. The active skill is the supplied project-local `.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`; its report template was read. Installed `testing-discipline` governed test assessment. The installed repo-foundation instructions were read as invocation-review context; source instructions were not substituted for the active installation and no installation was refreshed. No subagents, provider calls or messages were launched.

- HEAD: `9a050f034f0ce6929b104698cca425cae870788e`.
- Index tree: `0b86f257d2cb57feb5d76f45437bfd7f24b94d33`.
- Staged binary diff SHA-256: `e61df9f0d783a891213bea34606b5dc435d10fa54d0df4e6ad76b5216d4c2ff7`.
- All **49** staged paths independently matched their worktree bytes at entry and immediately before publication. Per-path index/worktree SHA-256 inventory: `/tmp/T-003-discovery.Cb6KSI/identity.json`. The exact status below enumerates the complete scope.
- T-003 production/tests/schema and directly affected skill/reference documents are task implementation. Task brief/verification/index were identified as pre-existing user preparation by the submission, not reviewer-authored changes. The supplemental records, copied validators, foundation schemas/tests and root docs are the explicitly requested additional staged scope.
- Untracked `.DS_Store`, `docs/.DS_Store`, `skills/.DS_Store` are excluded user state. Logs/generated files used by reviewer probes live only under `/tmp/T-003-discovery.Cb6KSI` or cleaned disposable fixture directories. The sole repository write is this new report.

## Confirmed finding

### F-01 [suggested P2] Malformed typed assignments can launch and admit preflight readiness

- Location: `skills/task-orchestrator/scripts/controller.py:1831`; public launch sibling at `controller.py:1781`.
- Trigger: a real terminal preflight returns the otherwise exact assignment with `correction_count: false` instead of integer `0`. Python dictionary equality treats these values as equal. `_validate_observed_result` therefore accepts it, admission reports no blocker, `readiness_current` becomes true, and a subsequent public implementation reservation succeeds.
- Evidence: D-02 and minimal D-04; `F-01-repro.log` records `false_correction_count_admitted=true`, `readiness_current=true`, `implementation_reservation=reserved`. The actor PID and group are absent afterward. D-02 separately reproduces `flow_revision: true` instead of integer `1`, and integer `0` replacing boolean `can_change_files` or `can_repair`; each yields readiness with no blocker. An integer `0` in the public launch assignment's `can_change_files` also returns `launched`.
- Consequence: the malformed-output guard can enable implementation from a contract-invalid preflight, while the launch boundary accepts a non-exact typed assignment. This demonstrates a validation failure, not a proven correction-budget reset or permission escalation; the original ledger assignment is not rewritten by this probe.
- Affected AC: AC-01 exact reserved launch, AC-02 malformed output/provenance refusal, AC-03 valid complete preflight, and AC-06 truthful successor contract.
- Broken invariant: untrusted persisted/API assignment values must preserve their JSON types as well as their values; malformed assignments cannot establish readiness.
- Explicit sibling surface: numeric `flow_revision`/`correction_count` and boolean `can_change_files`/`can_repair` in launch requests, result assignment echoes and adapter-observation bindings. The result schema declares these distinct types. The additional three result fields and public-launch case were actually exercised; other downstream equality sites remain a bounded correction-review surface, not separately asserted defects.
- Smallest corrective direction: enforce the complete typed assignment/envelope contract at each incoming boundary before comparing identity or admitting an outcome, consistently across launch, raw results and observation bindings. Preserve invalid raw evidence and no-advance behavior. Avoid a special case for only `correction_count`.
- Ownership: implementer owns correction and focused behavioral regressions; affected maintainability/native duties and registry synchronization retain their stage owners; a fresh discovery session owns corroboration, and a separate acceptance call owns the decision. No correction was made here.

## Completeness ledger

The frozen initial ledger was written before targeted execution to `/tmp/T-003-discovery.Cb6KSI/ledger-initial.json`; it enumerates all V rows and supplemental risks. The table below resolves and refines those initial row names without dropping an authority case. Submitted evidence is the implementation report's scenario-to-test table and its referenced `evidence/T-003-*.log` for every V row; supplemental foundation claims come from the staged executable/reference/test changes, without a separate invocation results packet. Prior submission passes are claims; the independent D commands supply current evidence. No prior discovery ledger or finding IDs existed for this package.

Shared setup/oracle: disposable real Git repositories and external run directories, valid frozen one-task sbx/YOLO policy, task/verification documents, allowed work file and disposable prerequisite tool/dependency/installed-skill files. Reach readiness by actual public reserve/launch/observe; compare independent child invocation logs, frozen input bytes, terminal receipts, ledger/history/count and filesystem markers. Invalid cases alter one otherwise-valid field and require refusal/no readiness/no extra invocation. Only explicitly unavailable T-004/005 reason/candidate/check prerequisites are seeded. Process probes use observable marker files and bounded waits. D-01 reuses submitted test cases; D-02..04 are additional reviewer-written probes in disposable state.

| Stable row | AC / invariant | Explicit cases | Independent probe / oracle | Current disposition |
|---|---|---|---|---|
| V-01 | AC-01 | light/standard/strong model/effort; frozen source bytes; revised input occurrence | D-01 model matrix; D-02 actual revised preflight and implementation marker | pass — actual local child argv/input/marker match frozen authority; configured model remains separate from observed identity. |
| V-02 | AC-01 | a missing/false authorization; b incompatible old policy; c stale revised assignment; d wrong task/role separately; e altered policy/flow/input; additional strict typed-assignment risk | D-01 valid/invalid public launches; D-02 stale assignment and unchanged ledger; D-04 sibling launch typing | fail — named a..e controls pass, but integer 0 replacing can_change_files=False still launches (F-01). |
| V-03 | AC-01 | unknown/unreliable/invalid occupancy; reliable .499/.5/.501; actual correction fresh session | D-01 finite policy boundaries; D-02 three actual corrections, no resume argv, replay after module reload | pass — fresh actual correction execution; below-threshold reuse remains optional. |
| V-04 | AC-01/04 | first launch; replay while running/reload/terminal; conflicting config; two and three simultaneous launchers | D-01 exact replay/configuration/2-process contention; D-03 independent 3-process public CLI contention | pass — one actual invocation per operation; losing callers refused; original outcomes/count preserved. |
| V-05 | AC-02 | a valid terminal control; b missing; c malformed; d wrong role; e task/operation/input/policy/flow/candidate independently; f forged session; g nonterminal result; h before/after session failure; i actor policy/acceptance prose; additional malformed assignment types | D-01 invalid-result matrix and raw review roles; D-02 forged session then valid control, nonterminal result and four assignment-type probes; D-04 malformed preflight to implementation reservation | fail — named invalid controls refuse, but bool/int assignment confusions bypass malformed-result refusal and admit readiness (F-01). |
| V-06 | AC-03 | actual disposable tool execution, dependency evaluation, installed-skill read; preflight terminal admission then first implementation | D-01 real prerequisite checks for each model; D-02 original and revised preflight plus work marker; no seeded readiness | pass — terminal current preflight enables real first implementation at count zero; output remains claim. |
| V-07 | AC-03 | a tool absent; b dependency absent; c installed skill absent; d incomplete readiness; e wrong task/role/session separately; f prior input after revision; g malformed/nonterminal/unknown; additional typed malformed envelope | D-01 prerequisite and invalid-output matrices; D-02 forged-session/nonterminal/unknown controls; D-04 malformed envelope | fail — finite named prerequisite/identity controls pass, but schema-invalid numeric/boolean assignment admits current readiness (F-01). |
| V-08 | AC-01/03/05 | real ready state; authorized repair and owner input revision; old/repointed readiness; new actual preflight; count/history/work retention | D-01 repair and revision histories, repointed old readiness and stale output; D-02 distinct revision and repair/re-preflight journey | pass — old readiness ineligible, revised bytes reach actor, repair invalidates readiness, new preflight restores only its current binding. |
| V-09 | AC-04 | a intent before spawn; b spawned before PID publication; c published during collection; d terminal publication before response | D-01 real synchronized killed-controller checkpoints for all four; D-02 separate intent kill, reload, observe/stop/launch replay | pass — no duplicate launch, unknown ownership blocks writer/retry, terminal publication replays preserved outcome. |
| V-10 | AC-04 | waiting actor plus descendant; timeout; coordinator interruption; explicit stop; known-unlaunched cancellation; unknown-liveness stop; repeat observation/stop | D-01 timeout/cancellation/stop and interruption cases; D-02 actual parent/child stop, PID/group absence, unknown stop/replay; D-03 contender pipes released | pass — actual stopped fixture tree disappears; receipts distinguish observed terminality from unknown intent. Custom probes reap supervisors and assert actor/group absence. |
| V-11 | AC-01/05 | cycle zero; shared check_failed/review_findings/environment_repair counts 1/2/3; reload/reservation/launch replay; repair preflight; revision; fourth correction and second free cycle zero | D-01 full history; D-02 distinct reason ordering, seven actual invocations, byte-identical replay, count 3 and refused fourth | pass — only future reason admission is seeded and labeled; no seeded readiness/launch/terminality. |
| V-12 | AC-02/05 | a fresh separate review sessions; b collector acceptance/policy prose raw only; c precise blocker/operation/evidence/action; d unknown relay/response; e observed relay/ack gives no repair/retry/revision/completion; f silence/repeat | D-01 four fresh role sessions, raw claims and persisted event matrix; D-02 real unknown-intent intervention, fixture relay and acknowledgement, refused repair/retry and no relaunch | pass — successor candidate/check/reason prerequisites are labeled fixtures; output grants no acceptance authority; no external message sent. |
| V-13 | AC-02/06 | actual approved sbx/provider preflight, marker, session/process/terminal result | not run — no explicit live approval, owner-approved real sbx/provider configuration or reviewed disposable live inputs | blocked — T-006/live-qualification owner must obtain the prerequisites; no live command authorized and no deferral decided here. |
| V-14 | AC-06 | actual public callables/CLI/files/refusals/replay/admission extension; ART-008 limits; future raw handoffs | D-01 launch/observe CLI; D-02/D-03 public-boundary behavior; static controller-contract/SKILL/operator/architecture/README reconciliation | fail — local interface and truthful live limits reconcile, but exact-assignment/malformed-result refusal claims are contradicted by F-01. No second finding is invented. |
| RF-01 | Supplementary staged foundation authority | same ID in two plans; legacy separate namespace; same-owner repeated entries; cross-owner collision; duplicate refs; invalid ID/path/missing plan; deterministic generation/no partial index writes | D-05 existing focused cases and D-06 independent valid/refusal/repeat probes against both copies | pass — distinct plan identities coexist; exact duplicate owner identity refuses; invalid paths/records preserve prior generated index. |
| RF-02 | Supplementary staged foundation authority | source/standalone validator parity; affected docs and records; recursive installer ownership/resource projection | D-06 installed validator from unrelated cwd; D-09 selected installer tests; source/standalone implementations identical; installer constants and README reviewed | pass — new resources stay under existing selected repo-foundation package; no new selected skill/shared runtime dependency, guide entry or installer ownership needed. |
| RF-03 | Draft 2020-12 boundary | qualified-record schema valid object versus missing plan; generated-index schema valid index versus generated=false | D-13 prepared real current records and deliberately invalid copies; import fails before executing a Draft 2020-12 validator | blocked — validation library unavailable in system and existing native analyzer Python; next evidence owner: fresh discovery with a capable pre-provisioned validator. Stdlib CLI evidence is separate. |
| SCHEMA-actor | AC-02/03 executable schema boundary | real well-typed preflight envelope versus same assignment with correction_count=false | D-13 actor-valid.json and actor-invalid.json retained; validator import fails | blocked — no Draft 2020-12 validation executed; next evidence owner: fresh discovery using a capable pre-provisioned environment. F-01 is independently demonstrated through the controller and does not depend on a claimed schema-validator pass. |
| RF-04 | Native installed-profile drift | current active profile versus selected current source bytes; fresh disposable installed profile versus source | D-12 current profile check; D-06 fresh disposable profile check | fail — active installation differs on six paths; fresh disposable installation matches. Current source development does not imply installed availability. Owner: installation maintainer in a later authorized invocation; never refresh during this run. |
| M-01 | Conditional maintainability consumption | current T-003 five-file I/R versus original eleven-file B; rationale dispositions; whole-scope native policy | maintainability-01.md plus B/I/R JSON/text, independently checked hashes and D-10 | pass for its explicit T-003 scope — complete B/I/R, current five index hashes, original eleven HEAD hashes, matching tools/settings and rationale dispositions; later HEAD change affects only task-flow instructions. Supplemental foundation Python/test paths are outside this report; no scope-wide maintainability conclusion claimed. |
| REG-01 | Current registry synchronization | implemented actor APIs/readiness/raw handoffs/unknown liveness; planned slices and owning-plan identities; generated index | D-11 structural check; current subsystem declarations traced to code/schema/tests and revised records | pass for routing/content reconciliation — 8 subsystems, 32 plan identities; no semantic acceptance, full-loop completion or sbx qualification inferred. |
| SCOPE-01 | Scope, provenance and exact staged bytes | 49 staged paths; package/implementation/supplementary foundation ownership; separate untracked user files; index versus worktree | identity.json plus direct Git index blob/worktree comparisons before probes and before report | pass — all staged/worktree bytes equal; user-owned .DS_Store files excluded, preparation/index identified as pre-existing user work, no reset/restage or production writes. |

## Adversarial checks and cleanup

- Exact one active owner: real contention with two actors in D-01 and three controller CLI contenders in D-03; exactly one actual actor invocation. The real lock, launch boundary and ledger are exercised, not a mocked scheduler.
- Current versus old readiness: D-01 tests old/repointed preflight after repair/revision; D-02 independently runs original/revised input occurrences and fresh post-repair preflight. No successful prior occurrence substitutes for the next real one.
- Terminal parent/child coherence: D-02 and D-03 wait for actual actor/descendant markers, request stop, observe the terminal receipt, reap retained supervisors and verify both PIDs and the actor process group disappear. Contender/controller pipes reach EOF with bounded communicate. Completion of the adapter receipt follows stdout-reader join, so the tested inherited actor pipe is released. Every custom fixture cleans up its owned processes, including on exceptions; no discovery fixture survives. D-01 passes ordinary timeout/interruption cleanup cases but is not used alone to claim independently measured descendant/group cleanup.
- Malformed typed state: F-01 supplies positive evidence of the bool/int confusion. No coherently rewritten-ledger tamper resistance is claimed by the implementation or inferred here.
- Review/acceptance sessions: fresh raw-output sessions remain distinct; seeded successor prerequisites do not establish production semantic admission. Configured model/effort does not prove observed provider identity.

## Exact command records

All commands run from the repository root with system Python unless the command explicitly says otherwise. All test/process inputs are local fixtures; no network, provisioning, live model checks, commits or installation refresh occurred. D-06 installs only into a new disposable target. Raw logs and complete reviewer regression scripts are retained under `/tmp/T-003-discovery.Cb6KSI`; these are evidence files, not an alternate durable report path.

| ID | Exact command | Raw log | Result / limits |
|---|---|---|---|
| D-01 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py` | `/tmp/T-003-discovery.Cb6KSI/actor-tests.log` | 0; 15 tests passed. Real fixture processes, contention and four synchronized publication interruptions. See cleanup qualification below. |
| D-02 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/T-003-discovery.Cb6KSI/probes.py` | `/tmp/T-003-discovery.Cb6KSI/probes.log` | 0; revised authority, first implementation, forged session/valid control, malformed assignment, fresh corrections/shared budget, live descendant stop, killed-coordinator intent, unknown-liveness acknowledgement. |
| D-03 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/T-003-discovery.Cb6KSI/contention-probe.py` | `/tmp/T-003-discovery.Cb6KSI/contention.log` | 0; three synchronized real public CLI contenders: launched/refused/refused, exactly one actor; bounded communicate releases all contender pipes. Also executes D-02 through its helper import, explicitly retained in the log. |
| D-04 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/T-003-discovery.Cb6KSI/F-01-repro.py` | `/tmp/T-003-discovery.Cb6KSI/F-01-repro.log` | 0 reproducer execution; behavioral oracle FAIL: malformed preflight admitted and implementation reserved. This is a finding reproduction, not a successful contract test. |
| D-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_foundation_tools.py` | `/tmp/T-003-discovery.Cb6KSI/foundation-tests.log` | 0; 4 tests passed, including valid/invalid plan identities through both public validators. |
| D-06 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/T-003-discovery.Cb6KSI/registry-probes.py` | `/tmp/T-003-discovery.Cb6KSI/registry-probes.log` | 0; both validators accept distinct-plan reuse and legacy coexistence, reject invalid/duplicate ownership without index replacement, and regenerate deterministically. Fresh disposable installation projects all four changed resources, runs installed validator from /tmp and preserves unmanaged content. |
| D-07 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_codex_worker.py` | `/tmp/T-003-discovery.Cb6KSI/worker-tests.log` | 0; 15 tests passed. |
| D-08 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_state.py` | `/tmp/T-003-discovery.Cb6KSI/state-tests.log` | 0; 45 tests passed. |
| D-09 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_contains_repo_stage_and_bounded_delivery_skills test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_guide_covers_every_installed_skill_and_usage_contract test_install_development_skills.DevelopmentSkillInstallerTests.test_installs_profile_preserves_agents_text_and_final_availability test_install_development_skills.DevelopmentSkillInstallerTests.test_rerun_removes_stale_managed_files_and_preserves_unmanaged_installations` | `/tmp/T-003-discovery.Cb6KSI/installer-tests.log` | 0; 4 tests passed; profile selection/guide, installed bytes and narrow ownership. |
| D-10 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | `/tmp/T-003-discovery.Cb6KSI/architecture.log` | 0; 4 tests passed; canonical whole-repository CLEAN architecture check. |
| D-11 | `python3 tools/check_contracts.py --root .` | `/tmp/T-003-discovery.Cb6KSI/contracts.log` | 0; 8 subsystems, 32 indexed refs; structural evidence only, not actor behavior or JSON Schema validation. |
| D-12 | `python3 scripts/install_development_skills.py --check .` | `/tmp/T-003-discovery.Cb6KSI/profile.log` | 1; six managed files differ. Four belong to staged repo-foundation resources; two are installed review-skill drift against the current HEAD. No refresh performed. |
| D-13 | `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/T-003-discovery.Cb6KSI/schema-probes.py` | `/tmp/T-003-discovery.Cb6KSI/schema-probes.log` | 2; blocked before validator execution: jsonschema absent. Valid/invalid inputs for all three Draft 2020-12 schemas were retained. Neither actor/schema nor foundation/schema row passes. |

Additional identity/static commands: `git status --short`, `git rev-parse HEAD`, `git write-tree`, `git diff --cached --stat`, `git diff --cached --binary --no-ext-diff` (hashed), targeted staged diffs/file ranges and direct `git show :<path>` versus worktree SHA-256 comparisons. `git diff a120de04911d994cfeb3839e82fdaf7fdcba3212 HEAD --stat` attributes the HEAD difference to three task-flow instruction files, not reviewed T-003 Python bytes. These are scope/identity evidence, not behavioral tests.

`git diff --check --cached` exits 2 for trailing spaces on line 1 of `evidence/T-003-mutation.log` and `evidence/T-003-mutation-02.log`. These retained historical unittest logs are whitespace hygiene only; this is not a second functional finding. The submission's earlier `git diff --check` claim concerned a different unstaged/index situation and does not establish staged whitespace cleanliness now.

Schema capability checks: system `/usr/bin/python3` and existing `.quality/envs/Linux-aarch64-cpython-3.14.4-79dbf22b5bc1/bin/python` both fail `import jsonschema` with `ModuleNotFoundError`. No validator was downloaded. `schema-probes.py` retains a real valid actor envelope, its false-count variant, a current qualified registry record/missing-plan variant, and current generated index/generated-false variant; execution must be repeated with a Draft 2020-12 implementation before those rows can pass.

Reviewer harness corrections are retained, not counted as implementation defects or completed evidence: first D-02 setup attempted another preflight after readiness had moved the cursor and raised KeyError on its refused reservation (`probes-first-harness-error.log`); the second attempted to seed an invalid initial preflight cursor (`probes-second-harness-error.log`). The final script uses independent initialized runs for each type case. First D-06 supplied an unmanaged SKILL.md without valid frontmatter, causing staged availability refusal (`registry-first-harness-error.log`); final setup supplies valid frontmatter. Final D-02/D-06 completed with exit 0; F-01 remains the observed contract failure. No reviewed repository test or production file was modified to repair these harnesses.

## Conditional evidence consumed

`reviews/maintainability-01.md` is an independent T-003 review, not this discovery's decision. Its original B, implementer I and independent reviewer R pairs are `.quality/reports/T-003-{start,compare,review}-20261109-01.{json,txt}`. Independent consumption in `maintainability-consumption.json` confirmed all five current reviewed Python SHA-256 values against the index, all eleven original B source hashes against current HEAD, complete reports and matching tool/settings/adapter identities. The report provides current original-B comparisons, the rationale dispositions for affected hotspots and whole-repository native references. Its earlier HEAD a120de0 differs from the current HEAD only in task-flow instruction files; no T-003 source drift is hidden by that difference. D-10 independently supplies current whole-scope architecture proof.

The supplemental foundation validator/schema/test changes were added after that five-file maintainability scope. That earlier report cannot establish their maintainability or their advisory baseline history. No supplemental baseline/comparison or numbered review was submitted. Discovery does not repeat general maintainability review or invent a missing mandatory stage; acceptance must preserve any applicable foundation-stage duty. Registry content is currently synchronized and independently structurally checked by D-11, without treating the absence of another stage report alone as a guided blocker.

## Aggregate-gate record

- Exact gate: `python3 tools/verify.py` — **not run** in this discovery.
- Owner/stage: this independent initial discovery.
- Reason: decisive targeted F-01 failure; aggregate execution is suppressed by the active discovery workflow. Continuing independent safe sibling probes and required targeted architecture/registry/profile checks does not erase the failure.
- Current evidence: targeted local tests pass their existing cases, custom malformed-assignment probe fails the authorized invariant, schema checks are blocked, and D-12 reports installation drift. No all-green claim.
- Submission-only historical aggregate: implementation reports 222 orchestrator tests with 6 failures, 7 errors and 14 skips, plus 310 root tests with 32 skips and no failures; overall gate failed. It attributes legacy failures to the non-macOS sandbox boundary and supplies baseline logs. Those logs were consumed as submitted claims, not independently rerun aggregate evidence. The existing verification-runner/test files are outside this staged diff. The historical passing installed-profile check is stale for the new foundation/source changes; D-12 is the current result.
- Next discovery, after correction: retain this finding and all incomplete rows, rerun focused regressions and finish available schema/native evidence first; only then reconcile authority/scope and own one justified aggregate. Conditional owners keep their duties.

## Residual limits and next route

- `SCHEMA-actor` and `RF-03`: blocked by absent Draft 2020-12 implementation. Fresh discovery evidence owner needs a capable pre-provisioned interpreter; no acceptance of these rows is implied by source inspection or stdlib CLI tests.
- `V-13`: blocked by missing specific live approval/configuration/inputs; T-006 remains the named qualification owner. This report records no approved deferral.
- `RF-04`: current six-file installation drift is observed. Four changed repo-foundation paths follow this staged source change; the two installed task-flow skill copies differ from the current HEAD. Repository rules explicitly prohibit refreshing the active installation during an ongoing run. A later authorized installation-maintenance invocation owns refresh/recheck; discovery does not do it or ask for retroactive permission.
- Supplemental invocation provenance: the staged data provides artifacts and tests but no independent foundation invocation transcript or reviewer/B-I-R packet for its Python changes. The observable contracts were probed; live agent compliance and supplemental advisory history remain unclaimed.
- Historical platform/optional-analyzer skips are retained limits, not passes. No real Codex/provider identity, sbx containment, same-thread recovery, power-loss durability, future collection/acceptance semantics or final workflow completion is qualified.

**Next: separate `task-acceptance-review` decision call** consumes the staged diff, this report, T-003 brief revision 1, verification revision 1, preflight Decision context, successor/predecessor contracts, implementation submission, maintainability report, F-01 regressions and every blocked row. It determines correction/evidence requests; this discovery does not implement, approve a deferral or advance the task. For any correction, complete affected required architecture/maintainability duties, applicable registry synchronization, fresh discovery, then a separate acceptance decision. Preserve M-01's exact scope instead of presenting it as a whole-staged-scope review.

## Reviewer regression reproduction

Full scripts and exact commands are in D-02/D-03/D-04/D-06/D-13. Minimal F-01 reproduction below creates only disposable fixture state, calls real public reserve/launch/observe, records the invalid claim and verifies that it permits implementation. A corrected implementation should block readiness/reservation for this malformed result while keeping the existing valid-control journey successful.

```python
import json,pathlib,sys,time
ROOT=pathlib.Path('/Users/mtrusov/work/skill-sources/personal-skills')
sys.path.insert(0,str(ROOT/'skills/task-orchestrator/tests'))
from test_actor_operations import ActorOperationsTest
out=pathlib.Path(__file__).parent
t=ActorOperationsTest();t.setUp();c,run=t.create_initialized_run();fake=t.actor({'field':'correction_count','value':False})
try:
 r=t.reserve(run);assert r['assignment']['correction_count']==0
 t.launch(c,run,r,fake);result=t.terminal(c,run,r['assignment']['operation_id'])
 raw=json.loads((run/'actors'/r['assignment']['operation_id']/'result.json').read_text())
 (out/'actor-invalid.json').write_text(json.dumps(raw,indent=2)+'\n')
 raw['assignment']['correction_count']=0
 (out/'actor-valid.json').write_text(json.dumps(raw,indent=2)+'\n')
 status=c.status_run(run);implementation=t.reserve(run,'implement','after-malformed-preflight')
 assert result['blocker'] is None and status['readiness_current'] and implementation['status']=='reserved'
 assert c.stop_operation(run,implementation['assignment']['operation_id'])['status']=='terminal'
 handle=next(iter(c._ACTOR_SUPERVISORS.values()),None)
 if handle is not None:handle.wait(timeout=3)
 pid=t.invocations(fake)[0]['pid'];assert c._worker_module.process_liveness(pid)=='absent' and c._worker_module._group_absent(pid)
 print(json.dumps({'false_correction_count_admitted':True,'readiness_current':True,'implementation_reservation':implementation['status'],'actor_pid_and_group_absent':True}))
finally:t.tearDown()
```

## Discovery continuation

- Iteration / byte identity: first independent discovery; HEAD `9a050f034f0ce6929b104698cca425cae870788e`; index tree `0b86f257d2cb57feb5d76f45437bfd7f24b94d33`; staged diff SHA-256 `e61df9f0d783a891213bea34606b5dc435d10fa54d0df4e6ad76b5216d4c2ff7`; all 49 index/worktree paths match.
- Coverage rows: V-01 pass; V-02 fail F-01; V-03 pass; V-04 pass; V-05 fail F-01; V-06 pass; V-07 fail F-01; V-08 pass; V-09 pass; V-10 pass; V-11 pass; V-12 pass; V-13 blocked live approval/environment/inputs; V-14 fail derivative F-01; RF-01 pass; RF-02 pass; RF-03 blocked absent Draft 2020-12 validator; SCHEMA-actor blocked same; RF-04 fail current six-file installation drift; M-01 pass only its explicit five-file scope; REG-01 pass routing/structural evidence; SCOPE-01 pass.
- Finding IDs: F-01 suggested P2, current independently reproduced; no prior discovery finding IDs. Submission's passes for malformed-output/exact-assignment claims are now qualified by F-01; named ordinary controls still pass.
- Continuity / owners: implementer corrects F-01 across typed launch/result/observation sibling surfaces and owns regression submission; affected native/maintainability owners and registry updater retain required correction duties; fresh independent discovery owns current proof and schema rows; T-006 owns authorized live evidence; later installation maintainer owns RF-04 refresh/recheck; separate acceptance owns decisions and route. No failure, incomplete schema row, live gap or scope limit is erased by a prior pass.
- Preparation/context: package brief r1, verification r1, preflight Decision context, implementation-report, controller-contract, cited direction/plan/predecessor decisions and maintainability-01; supplemental staged foundation contracts and user's staged-data request.
- Reviewer regressions: `/tmp/T-003-discovery.Cb6KSI/{F-01-repro.py,probes.py,contention-probe.py,registry-probes.py,schema-probes.py}`; exact D-02/D-03/D-04/D-06/D-13 commands above. For corrected bytes the first four require invariant-aware oracles rather than treating reproduction success as a pass; D-13 must execute a real Draft 2020-12 validator.
- Aggregate: `python3 tools/verify.py` not run, owner initial discovery, suppressed after targeted F-01; historical implementer aggregate failure is separate and not current corroboration.
- Next: separate task-acceptance-review consumes the complete evidence handoff and decides the correction/evidence route; no decision or advancement occurs in discovery.

## Exact Git status before report creation

```text
M  README.md
M  docs/contracts/foundation-tools.json
M  docs/contracts/implementer-feedback.json
M  docs/contracts/index.json
M  docs/contracts/measurement.json
M  docs/contracts/reviewer-feedback.json
M  docs/contracts/task-orchestrator.json
M  docs/development.md
M  skills/repo-foundation/references/contract-index.schema.json
M  skills/repo-foundation/references/contract-registry.md
M  skills/repo-foundation/references/subsystem-contract.schema.json
M  skills/repo-foundation/scripts/check_contracts.py
M  skills/task-orchestrator/SKILL.md
A  skills/task-orchestrator/assets/actor-result.schema.json
A  skills/task-orchestrator/docs/tasks/T-003/brief.md
A  skills/task-orchestrator/docs/tasks/T-003/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-aggregate.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-baseline-legacy.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-controller.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-01.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-02.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-03.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-04.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-05.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-06.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-07.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-final.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-measurement.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-mutation-02.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-mutation.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-orchestrator-final.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-state.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-transport.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/architecture.log
A  skills/task-orchestrator/docs/tasks/T-003/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-003/preflight.md
A  skills/task-orchestrator/docs/tasks/T-003/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-003/verification.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/references/architecture-map.md
M  skills/task-orchestrator/references/index.md
M  skills/task-orchestrator/references/operator-guide.md
M  skills/task-orchestrator/scripts/codex_worker.py
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
A  skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller.py
M  tests/test_foundation_tools.py
M  tools/check_contracts.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
```

## Exact Git status after report creation

```text
M  README.md
M  docs/contracts/foundation-tools.json
M  docs/contracts/implementer-feedback.json
M  docs/contracts/index.json
M  docs/contracts/measurement.json
M  docs/contracts/reviewer-feedback.json
M  docs/contracts/task-orchestrator.json
M  docs/development.md
M  skills/repo-foundation/references/contract-index.schema.json
M  skills/repo-foundation/references/contract-registry.md
M  skills/repo-foundation/references/subsystem-contract.schema.json
M  skills/repo-foundation/scripts/check_contracts.py
M  skills/task-orchestrator/SKILL.md
A  skills/task-orchestrator/assets/actor-result.schema.json
A  skills/task-orchestrator/docs/tasks/T-003/brief.md
A  skills/task-orchestrator/docs/tasks/T-003/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-aggregate.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-baseline-legacy.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-controller.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-01.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-02.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-03.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-04.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-05.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-06.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-07.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-focused-final.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-measurement.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-mutation-02.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-mutation.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-orchestrator-final.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-state.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/T-003-transport.log
A  skills/task-orchestrator/docs/tasks/T-003/evidence/architecture.log
A  skills/task-orchestrator/docs/tasks/T-003/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-003/preflight.md
A  skills/task-orchestrator/docs/tasks/T-003/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-003/verification.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/references/architecture-map.md
M  skills/task-orchestrator/references/index.md
M  skills/task-orchestrator/references/operator-guide.md
M  skills/task-orchestrator/scripts/codex_worker.py
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
A  skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller.py
M  tests/test_foundation_tools.py
M  tools/check_contracts.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-003/reviews/discovery-01.md
```

The new untracked discovery report is the sole status change; no existing staged or untracked state was altered. The index tree and reviewed bytes were checked again after publication.

## External evidence integrity inventory

The following hashes identify retained reviewer evidence bytes, not independent authenticity. Disposable fixture directories were removed after cleanup.

| File under `/tmp/T-003-discovery.Cb6KSI/` | SHA-256 |
|---|---|
| `F-01-repro.log` | `f23a85f0b6002e27d9d47730580aa2c6e1aca2abefbe806623b27db164fef237` |
| `F-01-repro.py` | `5e2f2c28177b62cdb968ea8fad43b71472aeb6bd28dd5f79347ee62abcaed601` |
| `actor-instance-can_change_files.json` | `c93b4ba49a8df3bc182164d1397224aea49e96d772ab96031a27254aae2ef8e9` |
| `actor-instance-can_repair.json` | `1df340fd3d862f110b91bf61c4370936e988a5d42bc97ced2a5bae4acf020f47` |
| `actor-instance-correction_count.json` | `4948871a3231d28784362d4babab71b09fff56af8fe229dfe52b099123471091` |
| `actor-instance-flow_revision.json` | `5c9c6623e72c92918255de96dc96f21778624bdb55b6456c8ca8711f1efe7d0e` |
| `actor-invalid.json` | `8bc4a39ad962acce6adfed3fde96b0bd13f1283ac8846d0100fe737423b4d2ee` |
| `actor-result-schema-invalid.json` | `8bc4a39ad962acce6adfed3fde96b0bd13f1283ac8846d0100fe737423b4d2ee` |
| `actor-result-schema-valid.json` | `78f82b51b15533a16f03c692fcb30a137617639b1a797eb8901ba4286ffa5958` |
| `actor-tests.log` | `2593da271519b5b5f7bfb8cceb5b14b490b4b1af8b8147922e0230f486a29348` |
| `actor-valid.json` | `78f82b51b15533a16f03c692fcb30a137617639b1a797eb8901ba4286ffa5958` |
| `architecture.log` | `61d6e91e129ef2ae810d9c5c34c12ac092fcc9df29c4123c39a99c93b9dcedf3` |
| `contention-probe.py` | `20052064d45af9323a54254cb2db8be625e3e337230d0ce96d184e3e2cd0aaaa` |
| `contention.log` | `7736fe507fd0a0e4886e90a1a633101abf65eee4ed330c4b4cb1f302312b9d32` |
| `contracts.log` | `53a7bb1d174792c5886d5ed21af55fde210659843f7b56cc990d714d9220b0e9` |
| `foundation-tests.log` | `b901762e9c18e54787be5ba6fe2f97ea216633cd01969b50cba14614e2bbcb16` |
| `identity.json` | `705cb0af357cf45c4b33fec18ea52e729ff520a1a85b8d4c55b9f91c3f911603` |
| `installer-tests.log` | `caa9e9da1163a3d9acb48cc9325a7fdf896324d30ba2579e522422d7261d60f5` |
| `ledger-initial.json` | `20b05d606771b7588051b7e4db8bbe587c298684080c26ec083419b03ee0310d` |
| `maintainability-consumption.json` | `290ed46e5a166eb92878fac6fd28a09b64329e0782bf5ab6c8b979ce46ddc76b` |
| `plan-qualified-record-schema-invalid.json` | `037e006c4018cf6a0be71dadd745a15424a229cf5427c4e1d23b6a0d4083e2f7` |
| `plan-qualified-record-schema-valid.json` | `5ffa3d1aed5c490854dcb615be8af53da6616786387e0ba230cbe137536dcf24` |
| `probe-results.json` | `4bacf8163fbd70ba9465a55ddc3542e7f864bd3b77ba1a0af50e23d41b163fd0` |
| `probes-first-harness-error.log` | `3ca9cba85238dc3962909ac52926622b08808356a762be3cca26d42ea89061b5` |
| `probes-second-harness-error.log` | `db36ede7b5cfc89725cb09e08bc1da9d2ad99e4bb228de6361a8deebbfdc87d5` |
| `probes.log` | `cff8a06aaf0c71363ae239dd01a1a8299e0b75c730e7857f5dc6ead7aa48914c` |
| `probes.py` | `11d1cafe0eb63ef977b0a1c30b8b3a252ee6cb03e40df8762938de9e70b26d4a` |
| `profile.log` | `651612a3174b3a11d72695d8649ef53abd73c3b4bb5cbde4bafc9d3d381b5989` |
| `registry-first-harness-error.log` | `713a2a465cfb396db2e0fb68ace7dfd11d62975603845585b220748d5cab3cca` |
| `registry-index-schema-invalid.json` | `1bf8bd1e9b955f30d879566f3c36a8461fe887962fc776af93d8d24bea87da94` |
| `registry-index-schema-valid.json` | `bf1ac639035c0f3169676d15e94eeab893f1bfca6a65b816069f37259c9e7c25` |
| `registry-probes.log` | `68615071f5416bed83643aa9161ea7bc3b43632e9481c0ad2a5cb4fd9b8563e9` |
| `registry-probes.py` | `72206a021b9a890f932a2f51ad48797307d1abab0e78424d7830adc633ce24ff` |
| `schema-probes.log` | `1e599739de81e69797c4282527b5bb06610effd723e2847f70ce1c0383f80977` |
| `schema-probes.py` | `544670e7205a30a12c18e159135faffbffe6acbb8ffe94fa16ceef8ae71b76ad` |
| `state-tests.log` | `a48571e84aad9ae54f27b660c338625323ab0221f7bcad2ce899a28c01acecdb` |
| `status-before.txt` | `f349861c5992ca6e530259281a094c87e62f9c8c555b94412288014aec882bc3` |
| `worker-tests.log` | `69bdd066571df7a4ff51040c35d549708507d84e40ca7828f9b229525dfe33db` |
