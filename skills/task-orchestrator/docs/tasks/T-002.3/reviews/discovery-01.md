# Task Review Discovery Report: T-002.3 — Safe approved-input revision

Producing stage: task-review-discovery (project-local installed skill).
Coverage: **partial overall** — all task scenarios V-01..06 and finite risks R1..3 have current targeted evidence; inherited sandbox execution remains unavailable and the aggregate is not green.
Iteration: first discovery, 2026-10-23T18:58:18.947727+00:00.
Repository: `/Users/mtrusov/work/skill-sources/personal-skills`. Report: `skills/task-orchestrator/docs/tasks/T-002.3/reviews/discovery-01.md`.

Evidence only: no acceptance verdict, approved deferral or advancement. This report applies only to the identified bytes, does not review or authenticate itself, and requires a separate acceptance decision.

## 1. Provenance and preparation

This session authored no reviewed production or test bytes; evidence is independent of implementation authorship. The only repository write is this new report. Active skill: `.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`; testing authority: `.agents/skills/testing-discipline/SKILL.md`. No installation refresh, helper-root substitution, delegation or source-workflow substitution occurred.

Authority: this package's brief revision 1; verification.md revision 1; preflight.md including Decision context; implementation-report.md READY_FOR_REVIEW; parent T-002 brief P-01..06; plan IF-001, ART-001/002/004, FLOW-001/003 and INV-001/002/003/005/008. Predecessor acceptance references are T-002.1/reviews/acceptance-02.md and T-002.2/reviews/acceptance-01.md. Their prior findings remain predecessor history, not unresolved findings introduced into this task. Current maintainability-01 reviewed the same four source/test SHA-256 identities below. No prior discovery exists for this leaf.

## 2. Findings

No findings in the scoped implementation. Aggregate limitations below are not qualified as task defects, passing evidence or approved deferrals.

## 3. Completeness ledger

The ledger was selected before the aggregate from V-01..06 and R1..3. Submitted evidence is the implementation report's named eight-method scenario map, not independent proof. DISC identifiers refer to section 5. All fixtures initialize disposable Git repositories and real run files. Direct terminal/readiness/evidence writes explicitly stand in for future T-003/004/005 admission.

| Row | AC/invariant and explicit cases | Setup/oracle and submitted evidence | Current independent probe | Result |
|---|---|---|---|---|
| V-01 | AC-01/R1: idle authorized document-only, policy-only, scope/check revisions; version, identity, history/count | Initialized run, bound owner object; exactly one version increment, new digest, retained old files; submitted authorized-document-policy-scope method | DISC-01 three sequential variants; DISC-03 valid validator + two real revisions + historical replay | pass |
| V-02 | AC-01/03/R1: missing/null authority, ack, actor-result/prose, bad binding/owner/provenance, stale/bool version, malformed policy/documents, missing mandatory stage, wrong task/run/repo, escaping scope, lock, reserved/running/unknown, completed | Valid success control and byte snapshots around public refusal; submitted invalid-request and active/completed methods | DISC-01 all table variants and real lock; DISC-03 mandatory-stage validator rejection | pass |
| V-03 | AC-01/02/R2: brief-only, verification-only, policy-only; old readiness/candidate/implementation/check/collection/acceptance, reload/repoint, new preflight | Seed actual historical evidence files and current readiness; preserve contents/history/findings/count, clear current references and expose stale; submitted invalidation method | DISC-01 all three isolated variants, old-stage reservations refused, new preflight then implementation | pass |
| V-04 | AC-03/R3: before content, content-before-pointer, pointer-before-response; exact retry, conflict, later revision and historical replay | Fault real immutable/atomic writers, reload status then retry; one receipt/version; submitted interruption/replay and process-exit methods | DISC-01 three write faults; DISC-03 sequential replay; DISC-04 abrupt real exits on both commit sides, lock reacquired and pipe/group cleanup observed | pass |
| V-05 | AC-04/R1..3: initialize/freeze, preflight guard, cycle zero, three corrections with check/review/repair reasons, replay/reload, repair re-preflight, revision at count three, fourth refusal, legacy/generic bypasses | Public operations plus labeled successor fixtures; exactly retained charge/history, snapshot-preserving fourth denial and missing-evidence refusals; submitted composed method | DISC-01 composed journey incl. run-next CLI/inspect/revise-flow/update guards; DISC-02 reservation class | pass |
| V-06 | AC-05: actual callable/CLI/validator/identity/count/refusal/handoff contract, repair preflight, truthful unrun runtime proof | Compare parent controller-contract.md with public definitions, canonical serialization and submitted result map | DISC-05 static traces + DISC-01 CLI execution; no runtime admission/completion claim | pass (document/interface evidence) |
| R1 | Authorized safe revision, including count-three and unknown operation | Explicit bound payload + public result/file oracle | V-01/02/05 | pass |
| R2 | No old evidence follows changed authority | Real revision/reload, old references and fresh-preflight guard | V-03/05 | pass |
| R3 | Coherent publication and replay, no budget reset | Observe real persisted old/new identities before legitimate next occurrence | V-04/05 | pass |
| ENV-01 | Seven carried inspection cases requiring sandbox-exec | Implementation report's seven named InspectionIntegrationTest methods; intended semantic oracles remain unreachable on Linux | DISC-06: six errors and one failure, each UnsupportedSandbox before intended assertions | blocked — macOS capability owner must execute; no bypass authorized |
| ENV-02 | Aggregate sandbox suite and isolation integration | Existing verification-runner cases | DISC-06: six additional sandbox nonpasses; 14 platform skips | blocked — macOS capability owner; no successful sandbox evidence |
| BASE-01 | Existing retrieval inventory assertion | Exact expected docs set vs actual; outside task changes | DISC-06 failure; DISC-07 unchanged HEAD reproduces exact six extras | fail (baseline, documentation/retrieval owner) |

ENV-01 methods: test_authorized_gap_cannot_excuse_a_targeted_failure; test_failed_verification_offers_resume_only_when_policy_escalates; test_inspect_keeps_pending_semantic_review_non_accepting; test_repository_gate_authorized_gap_preserves_pending_review; test_verifier_created_content_drift_is_recorded_and_denies_accept; test_verifier_created_drift_replay_reuses_published_records; test_inspect_reuses_execution_after_crash_with_review_pending.

ENV-02 nonpasses in VerificationSandboxFailClosedTests: test_production_builds_the_adopted_sandbox_invocation (error); test_incomplete_permission_envelope_is_rejected, test_missing_writable_root_enforcement_is_rejected, test_substituted_unrestricted_runner_is_rejected, test_unauthorized_danger_full_access_is_rejected_before_launch, test_unsupported_mode_is_rejected (failures caused by earlier UnsupportedSandbox).

## 4. Adversarial evidence

Old current pointers were restored after a real revision: readiness stays ineligible, verify/collection/acceptance reservations refuse stale input evidence. Policy-only changes invalidate input identity too. Active reserved/running/unknown revisions refuse without file changes; historical terminal operations retain original authority. Three legitimately charged corrections survive revision and reload, and no new cycle zero/fourth correction is granted. Exact historical revision replay after a second committed revision preserves current authority byte-for-byte. Mandatory-stage removal is rejected even with recomputed owner binding. No coherent whole-run tamper authentication claim is made. There is no changed JSON Schema boundary: the executable Python request and ledger validators were independently exercised with valid and invalid instances.

## 5. Commands and observations

All commands use repository root, Linux/Python 3.14.4, local disposable state, no network/live actor. No test or production file was edited. Temporary Git/run state was removed by fixture teardown or TemporaryDirectory.

- DISC-01: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py -k ControllerInputRevisionTest` — exit 0, 8 tests in 1.899s. Reviewed each assertion/setup before execution; covers actual public revision library and subprocess CLI.
- DISC-02: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py -k ControllerReservationTest` — exit 0, 11 tests in 12.697s. Existing predecessor ownership/actor/readiness/count regressions are current evidence on changed bytes.
- DISC-03: inline `PYTHONDONTWRITEBYTECODE=1 python3 -` probe reproduced below — request and ledger valid/invalid controls passed; two real revision commits then exact historical replay preserved snapshots. The initial combined command subsequently failed in review instrumentation before its process test setup because Popen received `check`; this was a probe-harness error, not product evidence. DISC-04 corrected it and ran the lifecycle probe fully. No failed product probe was hidden by the aggregate.
- DISC-04: inline command below — exit 0; 1 lifecycle test in 0.273s; 13 real subprocess checks, including both abrupt publication exits. communicate(timeout) observed inherited-pipe EOF; each child reaped and its isolated process group absent via killpg(pid,0). The fixture launches no detached child; Git and revision children are bounded. Original lock was available for retry. No fixture process survived.
- DISC-05: static public loader, revision, reservation/evidence, state validators and CLI traces; parent contract and test diff comparison. `git diff --check` exit 0 (hygiene only). The three-line state-test change supplies real manifest data/digest to existing fixtures, without removing scenarios/assertions.
- DISC-06: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` — exit 1; 206 tests in 23.431s: 178 pass, 7 failures, 7 errors, 14 skipped. Thirteen nonpasses are UnsupportedSandbox-related; one is baseline retrieval inventory. This is not a green gate.
- DISC-07: `git archive HEAD skills/task-orchestrator` exported via Python tarfile into TemporaryDirectory, then `python3 -m unittest discover -s <export>/skills/task-orchestrator/tests -p <pattern> -k <selector>` with timeout=30 for `(test_controller.py, test_inspect_keeps_pending_semantic_review_non_accepting)`, `(test_verification_runner.py, VerificationSandboxFailClosedTests)`, `(test_retrieval_surface.py, test_expected_current_references_exist)`. Respectively 1 error; 7 tests with 5 failures/1 error; 1 failure, matching current causes. Export removed. Unchanged verification_runner.py, its tests, and retrieval test also have no scoped diff. Representative inspection baseline attribution does not claim all intended inspection behavior passed.

DISC-03 reproducible targeted body (run using the inline Python command above):

```python
import sys,json
sys.path.insert(0,'skills/task-orchestrator/tests')
import test_controller as t
case=t.ControllerInputRevisionTest(); case.setUp()
try:
 c,r=case.create_initialized_run(name='independent-validator')
 q=case.revision_request(r)
 c._state_module.validate_input_revision_request(q)
 bad=json.loads(json.dumps(q))
 bad['payload']['policy']['flow']['steps'].pop(); case.bind_owner(bad)
 try: c._state_module.validate_input_revision_request(bad)
 except ValueError: pass
 else: raise AssertionError('invalid mandatory flow accepted')
 assert c.revise_inputs(r,q)['status']=='revised'
 ledger=case.read_ledger(r); c._validate_ledger(ledger)
 bad=json.loads(json.dumps(ledger))
 bad['input_revisions'][-1]['path']='input-revisions/revision-999.json'
 try: c._validate_ledger(bad)
 except ValueError: pass
 else: raise AssertionError('invalid receipt accepted')
 second=case.revision_request(r,key='second-independent')
 assert c.revise_inputs(r,second)['status']=='revised'
 before=case.snapshot(r)
 assert c.revise_inputs(r,q)['status']=='replayed'
 assert before==case.snapshot(r)
finally: case.tearDown()
```

DISC-04 exact successful inline body:

```python
import sys,os,subprocess,unittest
sys.path.insert(0,'skills/task-orchestrator/tests'); import test_controller as t
checks=[]
def observed(*args,**kwargs):
 kwargs['start_new_session']=True
 check=kwargs.pop('check',False)
 if kwargs.pop('capture_output',False): kwargs.update(stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 timeout=kwargs.pop('timeout',10)
 with subprocess.Popen(*args,**kwargs) as p:
  out,err=p.communicate(timeout=timeout)
  assert p.poll() is not None
  try: os.killpg(p.pid,0)
  except ProcessLookupError: pass
  else: raise AssertionError('process group survived')
  checks.append(p.pid)
  if check and p.returncode: raise subprocess.CalledProcessError(p.returncode,p.args,out,err)
  return subprocess.CompletedProcess(p.args,p.returncode,out,err)
subprocess.run=observed
result=unittest.TextTestRunner().run(unittest.TestSuite([t.ControllerInputRevisionTest('test_process_exit_during_publication_preserves_charge_and_releases_lock')]))
assert result.wasSuccessful()
print('bounded process-group disappearance and inherited-pipe EOF:',len(checks),'PASS')
```

## 6. Aggregate ownership

Owner/stage: this independent initial discovery, DISC-06. Exact command above, status failed. Immediately before launch, V-01..06/R1..3 were reconciled to scope and had clean targeted behavioral/static evidence, valid/invalid executable-validator controls, completed lifecycle cleanup, and no selected adversarial probe outstanding. ENV-01's inherited macOS blocker was concrete and did not depend on the gate. The aggregate was justified by the shared controller/state blast radius and explicitly assigned brief command. No aggregate ran after a decisive targeted product failure; the corrected instrumentation error was resolved before launch. No new gate or command is imposed on acceptance. No result waives platform evidence duties.

## 7. Scope and byte identity

HEAD: `c4bfeda33358c5a0a8683099f5263710dec2b991` (matches submission).
Tracked worktree binary diff SHA-256: `1d019f1820212bdf0503b6b6f09157eba150d8d19ce60e1e4b5c0931a801e5de`.
Index file SHA-256: `d66dad4f87a07fd248356f23928097fe35c9211b51eb92f814cc31900b7a609b`. Cached diff is empty: index equals HEAD, distinct from changed worktree bytes. Worktree SHA-256 values match maintainability-01. No unexplained overlap in task-owned paths.

| Task-owned changed path | Index Git blob | Worktree SHA-256 |
|---|---|---|
| `skills/task-orchestrator/scripts/controller.py` | `0a21618a11b192bae891c373f0ae61caf0c0499b` | `ef9460efb6ed54938edb9f3fbb93fb49c7b31d80a2378a83a81fa50d1275cc48` |
| `skills/task-orchestrator/scripts/controller_state.py` | `a27b1367fe7370ee64defc78653c4a6bd88dd49b` | `5552a069d43733896e2676e885bdf7a57ed6342bc524cf6c25d4a8d558884524` |
| `skills/task-orchestrator/tests/test_controller.py` | `6bf2b95a1f6ca9a398f8beccf03c9b9c4997acff` | `5feab396b8034515ffb1ce9457359b0c98ae0f2ad299843657553e1197137bc6` |
| `skills/task-orchestrator/tests/test_controller_state.py` | `038ba6ff3af9a0f4257e589344303d0e719e8657` | `4eb327cca0f35898a48143e131f8df2d2deada26fdfea2944dd8c1bf25bea747` |

Task package preparation/submission and parent controller-contract are authorized task artifacts, pre-existing at discovery start. Prior maintainability report is preserved. Unrelated .DS_Store files and docs/advisory-code-maintainability-signals.md are user state, excluded from task review. No schema/installer/profile/shared-script change exists; no installation synchronization is required. Official brief/plan/trackers are untouched. Snapshot comparisons are scope evidence, not behavior.

Exact ordinary short status before report:

```text
 M skills/task-orchestrator/scripts/controller.py
 M skills/task-orchestrator/scripts/controller_state.py
 M skills/task-orchestrator/tests/test_controller.py
 M skills/task-orchestrator/tests/test_controller_state.py
?? .DS_Store
?? docs/.DS_Store
?? docs/advisory-code-maintainability-signals.md
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-002.3/implementation-report.md
?? skills/task-orchestrator/docs/tasks/T-002.3/preflight.md
?? skills/task-orchestrator/docs/tasks/T-002.3/reviews/
?? skills/task-orchestrator/docs/tasks/T-002.3/verification.md
?? skills/task-orchestrator/docs/tasks/T-002/controller-contract.md
```

Exact expanded status before report (used for precise new-file audit):

```text
 M skills/task-orchestrator/scripts/controller.py
 M skills/task-orchestrator/scripts/controller_state.py
 M skills/task-orchestrator/tests/test_controller.py
 M skills/task-orchestrator/tests/test_controller_state.py
?? .DS_Store
?? docs/.DS_Store
?? docs/advisory-code-maintainability-signals.md
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-002.3/implementation-report.md
?? skills/task-orchestrator/docs/tasks/T-002.3/preflight.md
?? skills/task-orchestrator/docs/tasks/T-002.3/reviews/maintainability-01.md
?? skills/task-orchestrator/docs/tasks/T-002.3/verification.md
?? skills/task-orchestrator/docs/tasks/T-002/controller-contract.md
```

Exact expanded status after report:

```text
 M skills/task-orchestrator/scripts/controller.py
 M skills/task-orchestrator/scripts/controller_state.py
 M skills/task-orchestrator/tests/test_controller.py
 M skills/task-orchestrator/tests/test_controller_state.py
?? .DS_Store
?? docs/.DS_Store
?? docs/advisory-code-maintainability-signals.md
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-002.3/implementation-report.md
?? skills/task-orchestrator/docs/tasks/T-002.3/preflight.md
?? skills/task-orchestrator/docs/tasks/T-002.3/reviews/discovery-01.md
?? skills/task-orchestrator/docs/tasks/T-002.3/reviews/maintainability-01.md
?? skills/task-orchestrator/docs/tasks/T-002.3/verification.md
?? skills/task-orchestrator/docs/tasks/T-002/controller-contract.md
```

Only the new discovery-01.md entry differs. Every pre-existing tracked/untracked file hash, HEAD, tracked diff and index was checked unchanged after writing; the report is excluded from its own reviewed scope.

## 8. Gaps and next route

No task-required V/R row remains unchecked. Overall coverage stays partial because ENV-01/02 intended sandbox behavior cannot run here; owner is a macOS-capable evidence session, using the existing exact aggregate command or recorded seven method names. BASE-01 remains the documentation/retrieval baseline owner's failure; no fix is authorized in this discovery. No acceptance-approved deferral is recorded. Live sbx/model execution, runtime provenance, production readiness/semantic admission and first useful proof remain outside this leaf and unrun, owned by T-003..006.

Next: separate task-acceptance-review call consumes this report, current scoped diff and byte identities, brief revision 1, verification revision 1, preflight Decision context, implementation submission, maintainability-01, parent contract, all ENV/BASE limitations and reviewer probe commands. Discovery does not decide or advance.

## 9. Discovery continuation

- Iteration/current identity: first discovery; HEAD/diff/index and individual identities in section 7.
- Coverage: V-01=pass; V-02=pass; V-03=pass; V-04=pass; V-05=pass; V-06=pass (static/interface); R1=pass; R2=pass; R3=pass; ENV-01=blocked (Linux sandbox); ENV-02=blocked (Linux sandbox/skips); BASE-01=fail (unchanged inventory assertion).
- Finding IDs: none for scoped task. Predecessor findings are historical resolved context, not current leaf findings.
- Scenario continuity: no prior leaf discovery. Producer evidence is implementation-report.md's eight-method map; current evidence is DISC-01..07. Correction owner: no task defect identified; future implementation corrections belong to implementer. Evidence owner: macOS-capable session for ENV-01/02. Baseline owner: documentation/retrieval maintenance. Authority/route owner: coordinator/separate acceptance call. Influenced sibling surfaces: old readiness/implementation/check/collection/acceptance after every input/policy change; all active-operation states; repeated revisions and correction-budget history.
- Preparation/context: brief revision 1; verification revision 1; preflight.md Decision context; parent P-01..06/plan; accepted predecessors and maintainability-01.
- Reviewer regressions: no files added; DISC-03/04 inline bodies and DISC-01/02 focused commands in section 5 are reproducible reviewer probes.
- Aggregate: DISC-06 failed, 206 tests, 178 pass/14 skip/7 fail/7 error; owned by independent initial discovery after clean task-targeted evidence; baseline/environment causes attributed by DISC-07.
- Next: separate task-acceptance-review with all inputs/limitations above; no advancement by discovery.
