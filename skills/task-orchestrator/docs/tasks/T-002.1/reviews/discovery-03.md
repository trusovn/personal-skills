# Task Review Discovery Report: T-002.1 — complete prior missing evidence

| Field | Value |
|---|---|
| Producing stage | task-review-discovery; project-local installed skill |
| Coverage completeness | complete — both previously blocked material rows now have independent evidence |
| Discovery iteration | 3; continuation of discovery-02, preserved unchanged |
| Created at | 2026-10-23T16:21:22.543465+01:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report | skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-03.md |
| Task authority | brief.md revision 1; verification.md revision 1; parent T-002/brief.md owner decision |
| Preparation | preflight.md; controller-contract.md; implementation-report.md including MNT-01 and F-02 corrections |
| Prior evidence | reviews/discovery-01.md, discovery-02.md, maintainability-01.md, maintainability-02.md |

This report publishes evidence only. It makes no acceptance decision, approves no deferral, and advances no work. It applies only to the reviewed bytes below. It does not review or authenticate itself.

## 1. Provenance and scope

This session authored no production or test bytes. All behavioral evidence below was gathered independently in this session. Prior reports and implementation claims were navigation context, not current proof. The only repository write is this new report. No subagents, live model, network check, sbx pilot, installation refresh, fix, commit, or plan edit occurred.

HEAD: `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`. SHA-256 of `git diff --cached --binary skills/task-orchestrator/scripts skills/task-orchestrator/assets skills/task-orchestrator/tests`: `ec4c8cb191d9ad16940e287d8988ab3f06b38f84b0a5953f8a0b7fe30bf52bc4`. The unstaged diff is empty; current index and worktree identities match. Separate index blobs are recorded below. Prior reports supplied HEAD/status but no matching scoped digest; they do not establish byte identity by themselves.

Task-owned executable changes: controller.py, controller_state.py; four schemas (run-policy, flow-profile, handoff, step-outcome); four current examples (minimal-run-policy and three flows); test_controller.py, test_controller_state.py, and the F-02 correction in test_controller_git.py. All are under skills/task-orchestrator. The last correction is explicitly attributed to separate user authorization in implementation-report.md; discovery-02 carries that context. This session corroborates the bytes and regression, without inventing an additional authorization or widening scope.

AGENTS.md, the planning/task packages and index are pre-existing user/planning state. This report does not attribute them to implementation or review them as production changes. The stale implementation-handoff is historical; implementation-report is the current submission. No unexplained executable overlap was found. The development installer is outside this diff; no installer-managed dependency was changed.

## 2. Findings

No findings against the reviewed task implementation.

Prior F-02 (suggested P2, sibling Git fixture rejected by the new policy) remains resolved: the affected sibling suite now passes on current bytes. Historical F-01 denotes the pre-existing retrieval inventory drift, not a new task finding. MNT-01 remains resolved by current real-input byte/digest assertions.

## 3. Completeness ledger

Commands and reproducible probe definitions are in section 5. Each pass below refers to current independent evidence, not the prior report's pass label.

| Row | AC / risk | Explicit cases and setup / oracle | Submitted evidence | Independent current evidence | Result |
|---|---|---|---|---|---|
| V-01 | AC-01/03, R2 | Initialize real disposable Git repository/run with brief, verification, scope, checks and policy. Edit each source family separately, reopen, compare frozen content and every persisted run file; exactly one selected task. | test_frozen_authority_survives_source_edits; prompt transport assertion | P1 frozen-source test and byte/digest assertions; P4 immutable revision/replay; P6 controller integration tests include frozen content in prompt. No mutable source adoption. | pass |
| V-02 | AC-02, R1 | Remove each of eight stages, merge roles, reverse order, disable preflight, select two tasks. Public init must refuse without partial publication or source/run writes. Valid run-next twice must remain pending at ready without worker/attempt creation or second mutation. Actor result cannot complete controller stages or turn collection into acceptance. | public-init refusal matrix; pending-ready repeat; state outcome cases | P1 real CLI matrix and repeated pending-ready; P3 schema/runtime stage/role/result cases; P2 state suite. | pass |
| V-02a | AC-02, R1 | Real inspect after successful mechanical verification cannot accept; authorized repository-gate gap cannot bypass pending review; publish execution, inject crash, then inspect again and reuse legitimate execution while review remains pending. | three named inspection tests, previously submitted-only on macOS | P5: all three pass independently on macOS with actual sandbox-exec verifier; pending semantic_review, not_collected, no acceptance action. Nested outer sandbox failure was rerun through approved escalation. | pass — prior runtime blocker closed |
| V-03 | AC-03, R2 | Exact gpt-6.1-sol low/medium/high, wrong mapping/budget/authorization refused; reliable occupancy below/at/above 0.5, unknown/unreliable/nonfinite/bool/string/totals-only; shared corrections including environment repair, fourth denial. | state boundary and shared-budget tests | P1/P2 runtime validators; P3 examples and invalid policy matrix; P4 13 occupancy/reliability cases and sequential correction cycles for both stop/escalate. | pass |
| V-03s | AC-03, R2 | All four changed schemas executed by declared Draft 2020-12 validator; valid and relevant deliberately invalid instance per schema; local cross-schema references; all four examples. Structural evidence supplements behavior only. | implementer temporary schema script; prior independent blocker | P3: installed jsonschema 4.26.0, Draft202012Validator, referencing registry with local resources only. 70 paired schema/runtime instances pass. Includes eight omissions in flow and policy, roles, result families, missing authorization and multiple tasks. | pass — prior validator blocker closed |
| V-04 | AC-04, R2 | Old version/model/optional profile/missing snapshot; run-next refusal, plus incompatible persisted flow through run-next/inspect/revise-flow/update-ledger; exact next action and every persisted file unchanged. | two old-run regression methods | P1 real temporary files and public CLI/library mutation boundaries all pass; no worker used to continue an incompatible run. | pass |
| V-05 | AC-04 | Contract fields/versions, eight roles/modes, envelope result families, byte conventions, supported CLI and missing runtime operations compared to implementation. | controller-contract.md | Static trace of controller.py:114-197, init_run, update_ledger, revise_flow, inspect_run and CLI parser; controller_state constants and validators. P1/P3/P4/P5 support the documented boundaries. | pass (static plus behavioral corroboration) |
| MNT-01 | Prior maintainability regression | inputs.json uses compact sorted JSON with no newline, exact byte digest; rejected update preserves all bytes. | correction recorded in report and maintainability-02 | P1 includes both exact reviewer regression methods; P2 retains owning coverage. | pass |
| F-02 | Prior discovery regression | Real prepared inputs and v2 policy in sibling Git wiring fixture; fake transport baseline/patch/digest evidence retained. | authorized correction in implementation-report | P2: full test_controller_git suite, 13 tests pass; P6 includes it and has no policy-fixture error. | resolved |

## 4. Adversarial and state coverage

Required authority rows R1 and R2 reconcile to V-01..V-05; none is omitted. Zero/one/two selected tasks are covered by runtime tests and P3. All eight stage omissions and each envelope stage-role pairing receive valid/invalid checks. P4 uses sequential correction transitions (not independent synthetic cycle assertions): each completion returns to verify, then collection and separate acceptance precede the next correction. Cycles 1/2/3 share causes and the fourth is denied for both configured exhaustion routes. Both terminal stages refuse pure advance.

P1 repeats the real run-next call after its first persisted pending selection. P4's existing revision test performs real first revision, unchanged repeat, interrupted publication and recovery against immutable history. P5's replay test executes the first inspection occurrence, preserves its legitimate published execution, injects the crash and invokes the next inspection. These establish repeated behavior at the applicable public boundary; they do not qualify future admission APIs.

The task's frozen-authority claim concerns source edits, not a hostile writer who can rewrite ledger digests and all run artifacts coherently. No independent tamper anchor is claimed. Adversarial lifecycle work is not added to this policy task. The existing aggregate lifecycle cases run locally; bounded communicate/cleanup assertions complete, and a post-run process scan found no fake worker, signal.pause, time.sleep(60), controller/worker fixture or unittest process remaining. Successful bounded subprocess returns provide pipe-release evidence for the selected public probes; no process-isolation qualification is inferred.

## 5. Commands and current results

All commands run from repository root with `PYTHONDONTWRITEBYTECODE=1`; Python is /opt/homebrew/opt/python@3.14/bin/python3.14 on Darwin. Existing fixtures create disposable real repositories/runs and clean their temporary directories.

| ID | Exact invocation / reproducible probe | Outcome / purpose |
|---|---|---|
| P1 | `python3 -m unittest` with the nine fully qualified methods listed below | 9 tests pass, 2.375s; targeted authority, compatibility, repeated ready state and reviewer regressions |
| P2 | `python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py skills/task-orchestrator/tests/test_controller_git.py` | 57 tests pass, 2.730s (44 state + 13 Git); F-02 corroborated |
| P3 | `python3 -` with the deterministic schema/runtime recipe below | 70 paired instances pass; schema validity checks for all four changed schemas; no fetching/installing dependencies |
| P4 | `python3 -` with occupancy/correction recipe below; then `python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_flow_revision_is_immutable_noop_and_rejected_during_owned_work skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_tampered_flow_fails_before_worker_preflight_or_run_mutation` | 13 occupancy cases and sequential budget checks pass; 2 integration tests pass, 0.298s |
| P5 | `python3 -m unittest` with the three inspection methods below | First sandboxed run: 2 errors + 1 failure due to nested sandbox-exec preflight denial, not the target behavior. Approved escalated exact rerun: 3 pass, 2.170s; verifier remains sandboxed. |
| P6 | `python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | Approved escalated local aggregate: 187 tests, 34.586s, exactly 1 failure (pre-existing retrieval drift), no errors/skips reported. 186 pass. |
| P7 | `git diff --check`; `git diff --cached --check`; `git diff --name-only`; `git status --short`; `git ls-files -s` for reviewed paths; scoped staged binary diff SHA-256 | Both whitespace checks pass, unstaged diff empty; identities/status recorded here. |
| P8 | `ps -axo pid=,ppid=,pgid=,state=,command=` | Sandbox initially denied ps; approved escalation succeeded. Filtering the full returned inventory found no matching review fixtures; no user processes changed. |

P1 methods (prefix `skills.task-orchestrator.tests.`):

```text
test_controller_state.ControllerStateContractTest.test_required_stages_roles_policy_and_context_boundaries
test_controller_state.ControllerStateContractTest.test_corrections_share_budget_including_environment_repair
test_controller_state.ControllerStateContractTest.test_policy_never_defaults_missing_or_malformed_authorization
test_controller_state.ControllerStateContractTest.test_rejected_controller_update_leaves_persisted_bytes_unchanged
test_controller.ControllerIntegrationTest.test_frozen_authority_survives_source_edits
test_controller.ControllerIntegrationTest.test_init_refuses_weakened_authority_without_partial_publication
test_controller.ControllerIntegrationTest.test_old_run_continuation_refuses_without_mutation
test_controller.ControllerIntegrationTest.test_old_flow_refuses_all_mutation_entries_without_touching_run
test_controller.ControllerIntegrationTest.test_pending_ready_persists_cursor_without_launching_worker
```

P5 methods (prefix `skills.task-orchestrator.tests.test_controller.ControllerInspectionIntegrationTest.`):

```text
test_inspect_keeps_pending_semantic_review_non_accepting
test_repository_gate_authorized_gap_preserves_pending_review
test_inspect_reuses_execution_after_crash_with_review_pending
```

P3 reproducible recipe: import controller_state.py via importlib; load assets/*.schema.json into Draft202012Validator, with a referencing.Registry registering each local filename, file URI and $id. Call check_schema for the four changed schemas. For every following instance assert validator.is_valid equals the expected result, then call the corresponding runtime validator and require identical acceptance/refusal (ValueError). Instances:

- Valid minimal-run-policy and each of fast-local/reviewed/strong-local-flow (4).
- For each of 8 stages, remove that stage from fast-local-flow and from the policy's flow (16 invalid).
- Flow mutations: reverse steps, merge collection role into acceptance_reviewer, preflight mode off, light model gpt-5.6-sol, limit 4, includes_environment_repair false (6 invalid).
- Remove each transport/yolo/intervention authorization key from policy (3 invalid); task_ids empty and [T1,T2] (2 invalid).
- For each ready/preflight/implement/verify/semantic_review/acceptance/accept/completed/correction, build subject run_id=r, task_id=T1, flow_revision=1, flow_sha256=a repeated 64, correction_cycle=1 only for correction else 0, and the declared role (correction=implementer). Handoff version=1, summary=review, changed_paths=[], evidence_refs=[], transcript_ref=transcript.txt must validate; change role to implementer (or controller if already implementer) and require refusal (18).
- For each of those 9 subjects build outcome version=1, evidence_status=reported, artifact_refs=[], payload={version:1,reference:null}. Expected results: preflight=ready, implement/correction=complete, verify=mechanically_eligible, semantic_review=collected, acceptance=ACCEPT; valid only for those six actor steps; controller steps use complete and must refuse (9). For each valid actor step, separately change evidence_status to omitted_by_policy, and result to ACCEPT (acceptance instead to collected); both must refuse (12). Total=70. This is structural corroboration only; public behavior comes from P1/P4/P5.

P4 pure-boundary recipe: assert correction_session_policy on (occupancy,reliable,expected): (0,true,reuse), (.499999,true,reuse), (.5,true,fresh), (.500001,true,fresh), (null,true,fresh), (.1,false,fresh), (.1,1,fresh), (true,true,fresh), ('0.1',true,fresh), (-.01,true,fresh), (NaN,true,fresh), (infinity,true,fresh), ({input_tokens:100,output_tokens:10},true,fresh). For each exhaustion route stop/escalate, start verify/cycle0, call begin_correction with findings, complete_correction, advance twice, then repeat with environment_repair and CHANGES_REQUESTED; assert cycles1/2/3, verify return and semantic_review/acceptance sequence. Fourth environment_repair must preserve acceptance/cycle3 plus stop_action. advance at accept and completed must raise ValueError. No persisted run or process is claimed by this pure-boundary recipe.

## 6. Aggregate record

Owner: discovery-03, fresh continuation/completion stage. Exact command: P6. Status: **failed**, one pre-existing retrieval inventory assertion. Immediately before P6, V-01/02/02a/03/03s/04/05, MNT-01 and F-02 all had current clean targeted evidence; no selected adversarial case remained. Scope was reconciled and the ledger frozen before launch. Shared controller modules justify the existing aggregate. No new gate or command was added. No decisive target failure preceded it: P5's initial capability failure was resolved by the authorized exact rerun.

The prior discovery-02 aggregate remains historical and cannot close current rows. Its 13 environment errors/failures are absent here. Its missing V-03s validator evidence and V-02a runtime evidence are now supplied before this aggregate. The single current failure is test_retrieval_surface.RetrievalSurfaceTest.test_expected_current_references_exist, line 45: it expects four docs entries, but six additional entries already exist at HEAD. `git show HEAD:skills/task-orchestrator/tests/test_retrieval_surface.py` and `git ls-tree --name-only HEAD:skills/task-orchestrator/docs` confirm both stale expectation and extra entries predate the reviewed diff. This is not a green aggregate and is not an approved deferral. Planning-work owner retains the issue; the separate acceptance call weighs the record.

## 7. Exact reviewed state

Before report write:

```text
M  AGENTS.md
M  skills/task-orchestrator/assets/examples/fast-local-flow.json
M  skills/task-orchestrator/assets/examples/minimal-run-policy.json
M  skills/task-orchestrator/assets/examples/reviewed-flow.json
M  skills/task-orchestrator/assets/examples/strong-local-flow.json
M  skills/task-orchestrator/assets/flow-profile.schema.json
M  skills/task-orchestrator/assets/handoff.schema.json
M  skills/task-orchestrator/assets/run-policy.schema.json
M  skills/task-orchestrator/assets/step-outcome.schema.json
A  skills/task-orchestrator/docs/tasks/T-002.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-002.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.1/implementation-handoff.md
A  skills/task-orchestrator/docs/tasks/T-002.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-02.md
A  skills/task-orchestrator/docs/tasks/T-002.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-002.1/reviews/maintainability-02.md
A  skills/task-orchestrator/docs/tasks/T-002.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-002.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-002.2/verification.md
A  skills/task-orchestrator/docs/tasks/T-002.3/brief.md
A  skills/task-orchestrator/docs/tasks/T-002/brief.md
A  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
```

Index identities (worktree matches index, established independently by empty unstaged diff):

```text
100644 3801ca829fbefc7b181368420e1a2a745583a2d1 0	skills/task-orchestrator/assets/examples/fast-local-flow.json
100644 84b267aa1f8ba5a1cc1e98811ef030464d4ba09b 0	skills/task-orchestrator/assets/examples/minimal-run-policy.json
100644 331ddaa34c137f3758e23ed11d8ff462ebec3a50 0	skills/task-orchestrator/assets/examples/minimal-task-manifest.json
100644 daf80d1ff0ab5cf585785cd475274ff0501282d7 0	skills/task-orchestrator/assets/examples/reviewed-flow.json
100644 b17ff4a185f7f16b15d828f474831a1f2c6c7c19 0	skills/task-orchestrator/assets/examples/strong-local-flow.json
100644 3d913dbc8128ef8cfffd0283195fd0f31c349ff6 0	skills/task-orchestrator/assets/flow-profile.schema.json
100644 20bbc4775ce23ae489d2968d511607003f9dda90 0	skills/task-orchestrator/assets/handoff.schema.json
100644 43996a25a600fdb600d6d2c00342e71a3814bd61 0	skills/task-orchestrator/assets/run-policy.schema.json
100644 d561442b0e10a86bc1e0c4760fdf7da1728f9aea 0	skills/task-orchestrator/assets/step-outcome.schema.json
100644 b5c0e937159527eec19bfc7702bd08006bfa30b5 0	skills/task-orchestrator/assets/task-manifest.schema.json
100644 b0c6f2120fe38c7232cdc8a9a20a4c42b06020e4 0	skills/task-orchestrator/assets/worker-result.schema.json
100644 3e82085176ccda509c7e57c3ab06575f7d120b21 0	skills/task-orchestrator/scripts/controller.py
100644 fc59ecfcccb033816b5cabe7dfd47fecef436350 0	skills/task-orchestrator/scripts/controller_state.py
100644 114e74e1f348b641402aa6b9eff09f6ba323c4b8 0	skills/task-orchestrator/tests/test_controller.py
100644 68ad1b3815928a8ffaffd793802311d24c2cf09a 0	skills/task-orchestrator/tests/test_controller_git.py
100644 21a3dfa8466544dd6d3b2da6d06963ad889ffe0f 0	skills/task-orchestrator/tests/test_controller_state.py
```

Post-write status is the exact before snapshot plus only:

```text
?? skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-03.md
```

The writing command immediately compares actual post-write status with that expected set, rechecks HEAD and the scoped staged-diff SHA-256, and checks that no unstaged tracked path appeared. Its observed verification is reported to the user; this statement is not a claim of report authenticity.

## 8. Questions and residual limits

No required material row remains blocked or unchecked. No new authority question was found. The old report's classification of coverage as complete while two material boundaries remained blocked is superseded by the actual execution here; those old results are not relabeled as passes.

Residual limits retained: no independent anchor against coherent whole-run tampering; policy/manifest bind canonical JSON while inputs/flow bind exact bytes using their documented newline conventions; parallel runtime/schema/example declarations require synchronization; transport fixtures seed the implement cursor rather than prove readiness admission. T-002.2/T-003 and later admission work own those future capabilities. No live sbx launch-policy behavior is qualified here. Missing runtime stages and CLI limits are explicitly stated in controller-contract.md.

## 9. Continuation

```text
Discovery continuation:
- Iteration/current bytes: 3; HEAD 4449a3f373af9fabdcfe0c4d4b661988c4640c7f; scoped staged diff SHA-256 ec4c8cb191d9ad16940e287d8988ab3f06b38f84b0a5953f8a0b7fe30bf52bc4; index=worktree for reviewed paths.
- Coverage rows: V-01=pass; V-02=pass; V-02a=pass (previous macOS runtime gap closed by P5); V-03=pass; V-03s=pass (previous validator gap closed by P3); V-04=pass; V-05=pass; MNT-01=pass; F-02=resolved.
- Finding IDs: none new against reviewed implementation; historical F-02 remains resolved; historical F-01 is pre-existing retrieval drift outside task findings.
- Finding/scenario continuity: prior passes independently corroborated; producer's MNT-01 and F-02 correction claims confirmed by P1/P2/P6; no incomplete material evidence. Correction owner remains implementer if future corrections are requested; evidence owner is fresh discovery; authority/acceptance owner is a separate decision call. Sibling surface test_controller_git is exercised; no scope expansion/fix performed here.
- Preparation/context: brief.md rev1; verification.md rev1; preflight.md; parent T-002/brief.md environment-repair decision; controller-contract.md; implementation-report.md; reviews/discovery-01.md and discovery-02.md; maintainability-01.md and maintainability-02.md. Paths relative to this package unless parent given.
- Reviewer regressions: P1 exact frozen-authority and rejected-update pair (MNT-01); P2 test_controller_git.py including ControllerGitWiringTest.test_run_next_uses_controller_git_task_baseline_and_closure_evidence (F-02); P5 inspection and replay methods; P3 schema recipe. No repository regression files added.
- Aggregate: P6, discovery-03 owner, failed with exactly one established pre-existing retrieval inventory assertion; no environment or task-induced failures; 187 tests/34.586s.
- Next: separate fresh task-acceptance-review consuming brief, current scoped diff, this report, all packaged preparation/context and prior review records, exact reviewer commands/recipes, and the aggregate baseline exception. Discovery makes no advancement decision.
```
