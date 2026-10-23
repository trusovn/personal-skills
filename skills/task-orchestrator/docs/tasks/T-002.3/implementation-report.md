# T-002.3 implementation submission

Implemented: READY_FOR_REVIEW

Owner-authorized input revisions now publish a new task/policy identity and
state version together, invalidate old eligibility, require fresh preflight and
retain the shared correction count and historical records. Public controller
composition is proved locally with explicit successor-admission fixtures. The
parent and this leaf still require independent review; no advancement occurred.

## Authority and preparation

- [brief.md](brief.md), revision 1; parent T-002 P-01..06;
  plan IF-001/ART-001/002/FLOW-003.
- [verification.md](verification.md), revision 1, and
  [preflight.md](preflight.md), ready guided preparation created before implementation.
- Accepted dependencies: T-002.1 reviews/acceptance-02.md and
  T-002.2 reviews/acceptance-01.md; their contracts were inspected.
- Active workflows were the matching project-local installed implementer,
  verification designer, preflight and testing-discipline skills. No active
  installation was refreshed. Task-orchestrator source is a development target,
  not an installed orchestrator invocation or runtime qualification.
- Baseline HEAD: `c4bfeda33358c5a0a8683099f5263710dec2b991`.
  Environment: Linux, Python 3.14.4, local Git, no network/model/sbx execution.

## Deliverables and scoped diff

- `scripts/controller.py`: public `revise_inputs` / `revise-inputs` CLI,
  immutable revision preparation, atomic ledger/receipt publication, explicit
  uncertain-publication refusal and exact replay; unified public
  `load_input_authority` resolves initial or revised authority. Status exposes
  revision history. Environment repair requests preflight before prior-initial
  implementation guards; revision cannot grant another free cycle zero.
- `scripts/controller_state.py`: exact revision-request/owner-binding and receipt
  validators, revised authority-path consistency and immutable generic-update
  history. Existing policy validation remains mandatory.
- `tests/test_controller.py`: eight focused real-file methods reusing existing
  initialization/reservation/successor fixtures. Covers isolated brief-only,
  verification-only and policy-only invalidation plus abrupt process exit.
- `tests/test_controller_state.py`: existing persisted-ledger fixture now supplies
  manifest bytes/digest required by the unified authority reader. Existing
  transition/refusal assertions and scenarios are unchanged.
- [../T-002/controller-contract.md](../T-002/controller-contract.md): consolidated
  callable request/result/storage/ownership contract for successors.
- This report and preparation artifacts. No official plan or brief was edited.

Actual contract impact: added the IF-001 owner-authorized input-revision request,
response/replay and immutable bundle format; extended ART-001/002 with revision
receipts, current bundle paths and historical snapshots; added the public
current-authority loader and status revision history. Existing original files
remain historical after revision. Old assignments stay replayable as records,
never renewed launch authority. T-003 must consume the loader/current identities.

Executable contract declarations changed: `scripts/controller_state.py` runtime
request/ledger validators and `scripts/controller.py` CLI/library definitions.
Existing policy/flow/manifest JSON Schemas are reused without changes; there is
no separate ledger/revision-request JSON Schema. No contract registry exists.

## Design and boundaries

The owner decision includes kind, explicit decision, identity, response provenance
and SHA-256 binding of the exact request excluding authorization. Acknowledgement,
actor prose, missing provenance and mismatched binding do not authorize change.
This is a trusted-coordinator API, not an external identity authentication service.

One immutable bundle contains the requested complete policy/manifest/documents
and derived frozen inputs. One atomic ledger replacement publishes its paths,
all identities, incremented version and replay receipt. Earlier files and receipts
remain intact. The prior ledger snapshot (without recursive receipt duplication)
retains readiness/candidate/current references; raw evidence and operation/attempt
history stay available. Old evidence becomes stale through its input identity.
The revision clears readiness, candidate, current mechanical references and old
correction authorization, preserving findings and the correction count.

Exact pending content can be reused. Conflicting prepared content requires
intervention. Publication errors explicitly report an uncertain state version;
readers see old/new coherent authority and exact retry resolves the receipt.
The tests cover process death and released locks, not power loss or an automatic
recovery service. Arbitrary coherent whole-run tampering is not qualified.

A revision cannot create another initial implementation or erase the allowance.
After prior implementation, T-003/004/005 must admit a fresh correction reason
under the revised inputs; another cycle-zero request remains refused. Environment
repair and input revision both require newly admitted current preflight readiness.

## Verification evidence

All commands ran from repository root with `PYTHONDONTWRITEBYTECODE=1`.

1. Fail-first public CLI regression:
   `python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py -k test_cli_revision_uses_explicit_request_file`
   failed at the expected success assertion: CLI did not recognize revise-inputs
   (exit 2). This established that the test rejects the absent feature.
2. Focused final suite:
   `python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py -k ControllerInputRevisionTest`
   **8 tests pass**. The final invalidation method exercises three independent
   brief-only/verification-only/policy-only variants.
3. State suite after completing its existing fixture:
   `python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_state.py`
   **44 tests pass**.
4. Owning gate:
   `python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_controller*.py'`
   **152 tests: 145 pass, 6 errors, 1 failure**. All seven nonpassing methods stop
   at `UnsupportedSandbox: sandbox-exec verification is supported only on macOS`.
   The failure is an expected crash-message assertion encountering that earlier
   sandbox exception. This gate is not green.
5. Baseline attribution: exported unchanged HEAD's `skills/task-orchestrator`
   with `git archive` into a temporary directory and ran
   `python3 -m unittest discover -s <HEAD-export>/skills/task-orchestrator/tests -p test_controller.py -k test_inspect_keeps_pending_semantic_review_non_accepting`.
   **1 error**, same UnsupportedSandbox boundary. Temporary export was removed.
   This corroborates the shared platform cause without claiming macOS behavior.
6. `git diff --check`: passes (format/hygiene only, no behavioral claim).

The initial owning attempt also exposed three state-fixture errors due to absent
manifest setup. The existing shared fixture was completed; its 44 cases and the
subsequent owning run remove those task-induced errors. Early focused failures
were test setup errors (invalid seeded completion run state, duplicate readiness
argument and missing selected-task setup); corrected fixtures reach their intended
guards. No behavioral test was removed, skipped or weakened. The real repair
readiness ordering finding was corrected in the shared status eligibility rule.

### Complete scenario / risk map

All method names below belong to `ControllerInputRevisionTest`; these are
implementation evidence, not independent reviewer pass/acceptance status.

| Scenario / AC / finite risk | Current evidence and result |
|---|---|
| V-01; AC-01; R1 | `test_authorized_document_policy_and_scope_revisions_preserve_old_files`: public revisions, document bytes/hashes, complete policy/manifest projection, scope/check changes, one version increment, retained original files/count and revised flow actor selection. Pass. |
| V-02; AC-01/03; R1 | `test_invalid_revision_requests_are_byte_preserving` and `test_active_and_completed_tasks_refuse_revision`: bound valid controls; malformed, unauthorized/ack/actor/binding/version/task/run/repo/scope/policy refusals; real held lock; reserved/running/unknown and seeded completed task. Snapshot comparisons preserve authoritative and task bytes. Pass. |
| V-03; AC-01/02; R2 | `test_revision_invalidates_evidence_but_preserves_historical_contents`: seed actual referenced evidence files and readiness; independently revise brief, verification or policy; retain original contents/history/findings, clear eligibility, reload/repoint old readiness and candidate/evidence, refuse old-stage work, require new preflight and then permit implementation. Pass. |
| V-04; AC-03; R3 | `test_interrupted_publication_and_exact_replay`: faults before content, before pointer and after pointer; status/reload, pending-content conflict, exact retry/replay, later-revision historical replay and conflicting reused key. `test_process_exit_during_publication_preserves_charge_and_releases_lock`: real bounded subprocess exits on both ledger-commit sides with repair charge/history retained and retry once. Pass. |
| V-05; AC-04; R1/R2/R3 | `test_composed_three_corrections_revision_and_legacy_guards`: public initialization/preflight/readiness guards/cycle-zero/three shared correction reasons/reload/replay/repair re-preflight/revision/fresh preflight/fourth denial. Another cycle-zero request and public run-next/inspect/revise-flow/generic update cannot bypass stages or complete. Existing reservation suite also exercised in owning gate. Pass for local controller composition. |
| V-06; AC-05 | Parent controller contract reconciled with actual callable/CLI names, request validators, canonical byte conventions, result/refusal codes, receipts/version/count rules, repair/revision preflight requirements and owning test outcomes. Source/interface inspection only; no behavioral execution or schema check claimed for this row. |
| CLI wiring; AC-01/03 | `test_cli_revision_uses_explicit_request_file`: public subprocess CLI publishes and replays an explicit owner-bound request without further writes. Pass. |

Test-only direct successor fixture writes supply terminality, readiness and
candidate/check/collection/acceptance records. The controller's guards and
publication are exercised for real; runtime readiness/semantic admission is
not implemented or proved by those fixtures.

### Owning environment failures still requiring capable execution

All are in `ControllerInspectionIntegrationTest`:

- test_authorized_gap_cannot_excuse_a_targeted_failure
- test_failed_verification_offers_resume_only_when_policy_escalates
- test_inspect_keeps_pending_semantic_review_non_accepting
- test_repository_gate_authorized_gap_preserves_pending_review
- test_verifier_created_content_drift_is_recorded_and_denies_accept
- test_verifier_created_drift_replay_reuses_published_records
- test_inspect_reuses_execution_after_crash_with_review_pending

Owner: fresh discovery / macOS capability owner. No sandbox was bypassed and
these results are neither passes nor acceptance-approved deferrals.

## Review handoff and remaining route

First outstanding stage: **fresh independent task-review-discovery**, then a
**separate task-acceptance-review decision**. The installed implementer requires
ending this invocation at the handoff; no review skill, delegate, reviewer or
reviewer-owned aggregate was invoked. Repo policy does not require a canonical
architecture gate or maintainability pass for these bytes; no explicit user
maintainability request or registry stage applies. Existing predecessor reviews
do not impose a new conditional gate.

Discovery must independently corroborate all V-01..06 and R1..3, especially a
revision after the third correction, unknown ownership, stale evidence pointers,
interrupted publication/replay and truthful successor seams. Implementation
claims above do not mark its ledger checked. It owns whether/how to execute:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
```

That aggregate was **not run here**, as assigned by the brief. Carry the seven
platform-limited owning cases into discovery and acceptance. No actual sbx/model
launch or runtime provenance proof occurred; T-003/004/005 admission and T-006
live proof remain unrun. Parent closure and advancement require accepted leaves.

Pre-existing untracked `.DS_Store`, `docs/.DS_Store`, `skills/.DS_Store` and
`docs/advisory-code-maintainability-signals.md` remain outside this submission.
No commit, plan/tracker update, installation change, external message or model
launch occurred. Optional installed evidence instrumentation used run
`run-20261023T183527Z-6e4310f1e104`; it records invocation boundaries, not an
independent acceptance decision.
