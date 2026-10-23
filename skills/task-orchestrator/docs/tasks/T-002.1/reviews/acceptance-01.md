# T-002.1 acceptance review 01

The admitted evidence supports frozen single-task authority, mandatory separate collection and acceptance roles, approved correction policy, and non-destructive refusal of incompatible runs. All functional coverage rows pass on the current reviewed bytes. Advancement remains blocked by one missing conditional record: independent maintainability review of the later F-02 Git-fixture correction. Obtain that focused review, then return to a fresh acceptance decision; no production correction is requested.

Verdict: **INCONCLUSIVE**

Provenance: independent acceptance session; authored no reviewed production or test bytes. Profile: guided. This report is the only intentional repository write. No discovery probe, test suite, aggregate gate, tracker update, commit, or advancement was performed.

## Authority and scope

Read brief.md revision 1, verification.md revision 1, preflight.md including its decision context, parent T-002/brief.md, implementation-handoff.md (historical checkpoint), implementation-report.md (current submission, including MNT-01 and F-02 corrections), controller-contract.md, discovery-01/02/03 and maintainability-01/02. The preparation is applicable to this guided decision: the source-authority protection and stage representation remain this leaf's scope; reservation, whole-input revision, runtime admission/completion and launch-policy application remain successors' work. The Linux preflight limitations are historical environment facts; discovery-03 supplies the missing capable-host evidence.

Task-owned executable scope: controller.py, controller_state.py, four changed schemas, four current examples, test_controller.py, test_controller_state.py, and the bounded F-02 test_controller_git.py correction. The current submission attributes the sibling-fixture correction to separate user authorization; discovery-02/03 corroborate that ownership. Acceptance admits that recorded authorization without inventing further scope. AGENTS.md and planning/task packages/index are separately identified pre-existing user/planning work; they are preserved and excluded from the implementation verdict. No unexplained executable overlap was found. The installer is unaffected; task-orchestrator is outside its managed profile.

Current HEAD: `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`.
Scoped staged binary diff SHA-256: `ec4c8cb191d9ad16940e287d8988ab3f06b38f84b0a5953f8a0b7fe30bf52bc4`.
An empty unstaged diff independently confirms reviewed worktree bytes match the index; the scoped digest exactly matches discovery-03. The discovery report has since been staged; this report-only staging does not change the executable identity. Package contract and preparation contents were read in this decision.

## Findings and conditional evidence

No findings against the reviewed implementation.

- **MNT-01: resolved.** Historical byte-format disagreement is corrected. Current fixture uses the producer serializer; the contract distinguishes exact input/flow bytes from canonical policy/manifest digests. Discovery-03 P1 independently exercises both byte/digest regression methods. Maintainability-02 accepts that correction.
- **F-02: resolved functionally.** Historical policy-incompatible sibling fixture now supplies prepared verification input, current policy and the explicit implementation transport seam. Discovery-03 P2 independently passes all 13 sibling Git tests, including the preserved baseline/patch/digest assertions. No current production/test defect is demonstrated.
- **MNT-F02: blocked evidence row, not a defect finding.** implementation-report.md's final F-02 section explicitly requires fresh maintainability before discovery/acceptance. maintainability-02's REVIEWED section includes only the MNT-01 correction and retained original implementation scope; neither maintainability report includes test_controller_git.py. Discovery-03 tests this file but does not supply the separate maintainability decision. Its green behavioral results cannot replace the required conditional record. Evidence owner: fresh task-maintainability-review; correction owner: none unless that review finds a defect; authority owner: coordinator under the unchanged task contract.

Observations / stated assumptions: the same documented fixture seam is appropriate only for transport testing; it proves no ready/preflight admission. Earlier discovery's suggestions to waive blocked proof are not adopted: discovery-03 now supplies that proof. No owner question is needed.

Approved deferrals: none.

## Admitted discovery and coverage

Admitted current evidence: [discovery-03.md](discovery-03.md), complete ledger and continuation, with current identity corroborated above. Discovery-01/02 remain historical evidence; their incomplete rows are not relabeled as earlier passes. Submitted scenario evidence is implementation-report.md's V-01..V-05 map and correction records. P identifiers below refer to discovery-03, not acceptance-executed checks.

| Stable row | Cases / submitted evidence | Admitted independent evidence and reconciled result |
|---|---|---|
| V-01 | Real initialized brief/verification/scope/check/policy snapshot; source edits and one-task restriction; frozen-source regression and prompt assertion | **pass** — P1 byte/content tests, P4 immutable revision/replay and P6 prompt integration preserve frozen authority. |
| V-02 | Eight omissions, role merge, wrong order/optional stages, task cardinality, repeated pending-ready and actor-completion claims; public-init/state tests | **pass** — P1 public refusal matrix and repeat, P2 state suite, P3 schema/runtime role/result checks; no partial publication or worker launch. |
| V-02a | Mechanical inspection, authorized gate gap and crash replay cannot replace collection/acceptance; three named inspection tests | **pass** — prior Linux runtime gap closed by P5's independent capable-host exact rerun: 3 pass with actual sandbox-exec verification. |
| V-03 | Approved mapping, authorization, occupancy threshold/unknown/totals-only, shared correction budget including repair; state boundary cases | **pass** — P1/P2 validation, P3 invalid policy/examples, P4 13 occupancy cases and sequential cycles 1/2/3 plus fourth denial under stop/escalate. |
| V-03s | Four executable schema contracts and examples; implementer's supplemental script claim | **pass** — prior validator gap closed by P3: 70 paired Draft202012Validator/runtime instances; valid and constraint-targeted invalid cases for every changed schema, local references only. Structural corroboration is kept separate from public behavior. |
| V-04 | Old policy/model/profile/missing snapshot and incompatible flow across four mutation entries; real-file refusal regressions | **pass** — P1 confirms clear new-run action and unchanged persisted bytes before continuation; no migration. |
| V-05 | Implemented contract fields, roles, versions, result families, byte conventions, CLI and explicit missing operations | **pass** — current source/contract reconciliation agrees with discovery-03 static trace and P1/P3/P4/P5 behavior. |
| MNT-01 | Exact input-byte/digest convention and rejected update preservation | **pass** — maintainability-02 plus discovery-03 P1/P2 current regression evidence. |
| F-02 | Sibling Git wiring fixture correction; baseline/closure/patch/digest assertions retained | **pass / resolved** — discovery-03 P2: 13 tests pass; P6 has no task-induced fixture failure. Conditional maintainability coverage is tracked separately in MNT-F02. |
| MNT-F02 | Required independent maintainability of the later test_controller_git.py correction | **blocked** — no report covering these corrected test bytes; owner task-maintainability-review. |

Contract reconciliation: expected ART-001/IF-001 representation matches the actual input snapshot and validation code; declared schemas/examples require current versions, exact ordered roles, policy and single-task cardinality; controller-contract.md describes these implemented semantics and distinguishes missing successor operations. The brief expressly states no contract registry exists and forbids inventing one; no registry-updater or registry validator gate applies. No new routing/module-reference mismatch was demonstrated.

## Aggregate gate (consumed)

Exact command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`.
Owner/stage: discovery-03, fresh completion pass; P6.
Reason: shared controller modules affect sibling suites. Discovery records clean targeted P1..P5 evidence before P6; the initial nested-sandbox P5 failure was resolved by its authorized exact rerun first.
Current result: **failed**, 187 tests, 186 pass, one pre-existing retrieval-inventory assertion; no task-induced failure, errors or skips reported. Acceptance did not rerun it.

Historical F-01 is retained as baseline retrieval drift outside this implementation, not an approved task deferral. Acceptance inspected the HEAD test's exact four-entry directory assertion and HEAD docs tree: the extra entries already exist at HEAD, and the test is unchanged by this diff. Impact: aggregate is red and can obscure later regressions. Exposure: deterministic whenever the full suite is run. Mitigation: discovery names the exact failure and confirms the affected sibling suites independently. Disposition: planning-work owner retains correction outside this leaf; the failure does not demonstrate an AC violation here and no global-green gate is required by the brief. This decision does not call the aggregate green or waive any missing task proof.

## Questions / residual risk / next route

No unresolved authority question or unchecked functional row. The sole missing required evidence is MNT-F02. Retain the documented limits: coherent whole-run tampering is outside source-edit protection; parallel policy declarations need synchronization; seeded transport fixtures do not prove readiness admission; no live sbx, model, launch policy, reservation or completion behavior is qualified.

Next: coordinator obtains a focused fresh **task-maintainability-review of the F-02 test_controller_git.py correction**, preserving the original maintainability coverage, then requests a separate fresh task-acceptance-review with this continuation and discovery-03. If bytes remain unchanged and the review is clean, current discovery need not be rerun solely for the missing report. Any correction follows its affected conditional/discovery route before fresh acceptance. T-002.2 must not advance yet.

## Review continuation

- Iteration/current bytes: acceptance-01; HEAD `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`; scoped staged digest `ec4c8cb191d9ad16940e287d8988ab3f06b38f84b0a5953f8a0b7fe30bf52bc4`; reviewed index and worktree match.
- Coverage: V-01=pass; V-02=pass; V-02a=pass; V-03=pass; V-03s=pass; V-04=pass; V-05=pass; MNT-01=pass; F-02=resolved/pass; MNT-F02=blocked.
- Finding IDs: MNT-01 resolved; F-02 resolved functionally; historical F-01 remains pre-existing retrieval drift. No new implementation finding. MNT-F02 is an evidence-row ID only.
- Continuity/owners: V-02a and V-03s were blocked in discovery-02 and are independently closed by discovery-03 P5/P3. MNT-01 retains maintainability-02 resolution and P1 regressions. F-02 retains authorized sibling fixture correction and P2/P6 behavioral proof. MNT-F02 lacks independent maintainability coverage; evidence owner=fresh maintainability reviewer; correction owner=implementer only if that reviewer requests correction; authority owner=coordinator. Influenced sibling=test_controller_git.py. No other unfinished row.
- Preparation/context: brief.md rev1, verification.md rev1, preflight.md decision context, parent T-002/brief.md owner decision; implementation-report.md; controller-contract.md; discovery-01/02/03; maintainability-01/02. Historical checkpoint=implementation-handoff.md.
- Reviewer regressions: no files or tests added by acceptance. Preserved commands from discovery: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_rejected_controller_update_leaves_persisted_bytes_unchanged skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_frozen_authority_survives_source_edits` (MNT-01); `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_git.ControllerGitWiringTest.test_run_next_uses_controller_git_task_baseline_and_closure_evidence` (F-02). P3 schema recipe and P5 three inspection methods remain in discovery-03 section 5; not rerun here.
- Aggregate consumed: discovery-03 P6 after clean targeted evidence; failed only on established pre-existing retrieval inventory assertion, 186/187 pass; no acceptance gate added.
- Next: focused F-02 maintainability review → fresh separate acceptance against unchanged or newly evidenced bytes. No advancement, tracker write or production correction authorized by this verdict.

## Exact status audit

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
A  skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-03.md
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

After report write (only the new report entry differs):

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
A  skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-03.md
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
?? skills/task-orchestrator/docs/tasks/T-002.1/reviews/acceptance-01.md
```

Acceptance verification: compare actual post-write status to the exact expected snapshot, recheck scoped staged digest and HEAD, and confirm no unstaged tracked changes. These identity/hygiene checks are not behavioral verification. Behavioral results above are consumed from discovery.
