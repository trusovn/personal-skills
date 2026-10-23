# T-002.1 acceptance review 02 — corrected conditional-stage applicability

The reviewed implementation satisfies this leaf's frozen-authority and policy contract. Current independent discovery closes all required functional and validator rows. The minor subsequent Git-fixture alignment does not require another maintainability review under the governing task/repository authority. The coordinator may hand the implemented contract and review references to T-002.2; this report performs no advancement.

Verdict: **ACCEPT**

Provenance: independent acceptance session; no reviewed production or test bytes authored. Guided profile. This is a correction of acceptance-01's conditional-stage interpretation, not new evidence for changed implementation bytes. acceptance-01 remains unchanged as history.

## Corrected applicability decision

acceptance-01 treated the implementer's request for a fresh maintainability pass as a mandatory gate. That was too strict. The brief requires applicable required conditional stages; repository authority does not mandate a maintainability rerun for every test-fixture correction. The installed maintainability skill's applicability is conditional on repository policy or an explicit user request. An implementation handoff does not itself establish such policy.

maintainability-01/02 cover the substantive implementation and the MNT-01 correction. The subsequent F-02 delta in test_controller_git.py adds the prepared verification file, current policy version/authorization, and the same documented transport-stage setup already reviewed in the controller tests. It preserves the existing worker/Git/patch/digest assertions and adds no production behavior, abstraction or new fixture framework. Its functional effect is independently corroborated by discovery-03 P2 and P6. Therefore MNT-F02, introduced only by acceptance-01, is **closed as not applicable**, not waived required proof. No new review gate is justified for this bounded delta.

## Authority, scope and evidence

The complete authority, preparation/context, current submission and scope reconciliation in [acceptance-01.md](acceptance-01.md) remain applicable: brief revision 1, verification revision 1, preflight decision context, parent owner decision, implementation-report corrections, controller-contract and all preceding discovery/maintainability records. No authority or reviewed implementation bytes changed. Pre-existing AGENTS.md/planning work remains separate and untouched. The sibling-fixture correction retains the separately recorded user authorization. No contract registry or architecture gate applies; the required package contract matches the implemented and declared policy/input/stage interfaces.

HEAD: `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`.
Scoped staged binary diff SHA-256: `ec4c8cb191d9ad16940e287d8988ab3f06b38f84b0a5953f8a0b7fe30bf52bc4`, identical to discovery-03 and acceptance-01. Empty unstaged diff establishes worktree/index equality for reviewed tracked bytes. Changes in report staging do not change the executable scope identity.

No findings.

Approved deferrals: none. No authority questions or unchecked required work remain.

## Reconciled coverage

Submitted evidence remains implementation-report.md's scenario map and correction records. Admitted independent evidence remains [discovery-03.md](discovery-03.md), complete ledger and continuation; earlier publications remain historical. P identifiers below refer to that report, not tests rerun by acceptance.

| Row | Cases / submitted evidence | Independent current evidence / disposition |
|---|---|---|
| V-01 | Frozen real brief/verification/scope/check/policy inputs, separate source edits, one-task restriction and prompt content | **pass** — P1 real-file byte/content regression, P4 revision/replay, P6 prompt integration. |
| V-02 | Eight mandatory stages, role separation/order, optional-profile/cardinality refusal, repeated pending-ready and actor-result limits | **pass** — P1 public initialization/repeat matrix, P2 state suite, P3 paired schema/runtime checks. |
| V-02a | Successful mechanical inspection, authorized gate gap and crash replay cannot grant acceptance | **pass** — P5 independent macOS three-test exact rerun, with actual sandbox-exec verifier; closes prior Linux evidence gap. |
| V-03 | Model mapping, execution authorization, threshold/unknown/totals-only occupancy, three shared corrections including repair and fourth denial | **pass** — P1/P2 validators, P3 policy/examples, P4 occupancy cases and sequential correction budgets for stop/escalate. |
| V-03s | Four schema contracts, local references and examples, relevant invalid cases | **pass** — P3 independently executes Draft202012Validator and runtime on 70 paired instances, including valid and constraint-targeted invalid cases for every changed schema. Structural proof supplements public behavior. |
| V-04 | Old version/model/profile/missing snapshot and incompatible flow through continuation/mutation entries | **pass** — P1 real-file refusal/next-action checks and unchanged persisted bytes. |
| V-05 | Implemented contract fields, roles, versions, byte conventions, result families, supported CLI and missing successor APIs | **pass** — source/contract reconciliation plus discovery's static trace and P1/P3/P4/P5. |
| MNT-01 | Historical input-byte convention mismatch | **pass / resolved** — maintainability-02 and discovery P1/P2 exact byte/digest regressions. |
| F-02 | Historical sibling policy-fixture failure | **pass / resolved** — P2 full Git suite 13/13 and P6 no task-induced fixture failure; assertions preserved. |
| MNT-F02 | acceptance-01's proposed additional maintainability gate | **closed / not applicable** — conditional applicability corrected above; no missing required evidence. |

## Aggregate gate (consumed)

Command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`.
Owner/stage: discovery-03 P6, after clean targeted P1..P5 evidence; shared-module blast radius justified the aggregate. Result: **failed**, 187 tests, 186 pass, one independently established pre-existing retrieval-directory inventory assertion; no task-induced failure/errors/skips. The initial P5 nested-sandbox failure was resolved by its authorized exact rerun before P6. Acceptance adds no command or gate and did not rerun this suite.

Historical F-01 remains baseline retrieval drift outside this task, as independently reconciled against the HEAD test and docs tree in acceptance-01. Impact: persistent red aggregate can obscure later regressions. Exposure: deterministic on aggregate execution. Mitigation: exact failure identified and affected task/sibling behavior independently tested. Planning-work owner retains correction; it is not an acceptance-approved task deferral. No global-green requirement or task AC is waived, and the aggregate is not described as passing.

## Residual limits and next route

Source-edit protection is qualified; coherent whole-run tampering is not. Canonical policy/manifest digests differ from exact input/flow byte binding as documented. Parallel declarations require synchronization. Seeded transport fixtures prove no ready/preflight admission. Reservation, input revision, live actor admission, completion and sbx/model launch policy remain successor work. These are existing scope boundaries, not defects or new deferrals.

Next: coordinator hands controller-contract.md, this decision and discovery-03 to T-002.2 for its own preparation/execution route. No tracker, plan, production or orchestration advancement was performed here.

## Review continuation

- Current bytes: HEAD `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`; scoped digest `ec4c8cb191d9ad16940e287d8988ab3f06b38f84b0a5953f8a0b7fe30bf52bc4`; reviewed worktree/index match.
- Rows: V-01/V-02/V-02a/V-03/V-03s/V-04/V-05/MNT-01=pass; F-02=resolved/pass; MNT-F02=closed/not applicable.
- Finding IDs: MNT-01 and F-02 resolved; historical F-01 remains pre-existing external baseline drift. No new finding or reviewer regression.
- Continuity: acceptance-01's INCONCLUSIVE concerned only MNT-F02; this decision corrects applicability without altering proof or bytes. V-02a/V-03s retain discovery-03 closure of prior blocked rows. Correction owner=none; evidence owner=discovery-03 for admitted proof; authority/next-route owner=coordinator. Sibling surface=test_controller_git.py.
- Preparation/context: same references and revisions listed in acceptance-01, including all prior review reports and current implementation-report/controller-contract.
- Reviewer regressions: no files/tests added; exact MNT-01 pair, F-02 Git regression, schema recipe and three inspection methods remain recorded in acceptance-01 and discovery-03 section 5; not rerun.
- Aggregate consumed: discovery-03 P6, 186/187, one established pre-existing failure; targeted-before-aggregate order preserved.
- Next: coordinator handoff to T-002.2; no additional maintainability or discovery rerun required for unchanged bytes.

## Exact status audit

Before this report:

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

After this report (only this new report entry differs):

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
?? skills/task-orchestrator/docs/tasks/T-002.1/reviews/acceptance-02.md
```

Verification: actual status compared with the exact expected snapshot; HEAD, scoped staged digest and empty unstaged tracked diff rechecked. These are identity/hygiene checks; behavioral evidence is consumed from discovery.
