# T-002.2 implementation report

The controller now exposes read-only status and reserves one operation against
an expected version. Assignment, ownership and any correction charge are stored
in one atomic ledger update. Reload/replay does not duplicate work or charges;
unknown ownership stops further reservations. Environment repair shares the
three-correction allowance, including repair before initial implementation.

Implemented: **READY_FOR_REVIEW**. These are implementation checks, not an
independent review or acceptance decision.

Authority: [brief.md](brief.md), revision 1; [verification.md](verification.md),
revision 1; [preflight.md](preflight.md), guided ready at HEAD `1c1aff8`.
Dependency: T-002.1 [controller contract](../T-002.1/controller-contract.md) and
[acceptance-02](../T-002.1/reviews/acceptance-02.md). The only initial untracked
file was this task's preflight; it remains unchanged and is not implementation
work. No other writer or material authority/capability change was found.

## Deliverables and scope

- `skills/task-orchestrator/scripts/controller.py`: status/reserve library and
  CLI, atomic embedded assignments, eligibility/readiness guards and pending
  public legacy launch path.
- `skills/task-orchestrator/scripts/controller_state.py`: assignment/history,
  one-owner and charge validation; actor-admission fields/cursor remain
  controller-owned. Positive retained counts at preflight/implementation are
  valid so repairs cannot reset the allowance.
- `skills/task-orchestrator/tests/test_controller.py`: nine reservation tests
  reusing initialized real Git/run fixtures; historical transport regressions
  explicitly dispatch the private legacy launch helper. Their original Git,
  timeout, frozen-input and inspection oracles remain intact.
- `skills/task-orchestrator/tests/test_controller_state.py`: replace the obsolete
  positive-count rejection with valid retained-count preflight/implementation
  cases; preserve zero-cycle correction and over-limit rejection coverage.
- `skills/task-orchestrator/tests/test_controller_git.py`: one reused wiring
  fixture call follows the private helper rename; its baseline/closure assertions
  are unchanged. This is fixture maintenance for the guarded public boundary.
- [controller-contract.md](controller-contract.md): exact requests, outputs,
  persisted fields, replay/refusal behavior and successor admission seams.

Actual contract impact: added IF-001 status/reserve and the ART-002/004 embedded
actor-assignment history, active pointer and accounting contract. Public
`run-next` reports pending successor launch work without selecting or launching.
Actor history cannot use legacy inspection for completion. No launch, generic
state-injection, input-revision or completion command was added.

Executable contract declarations changed:
`skills/task-orchestrator/scripts/controller.py` (CLI/library definitions) and
`skills/task-orchestrator/scripts/controller_state.py` (record validators).
No separate ledger JSON schema exists or was added.

The development installer was inspected. Task-orchestrator is outside its
selected profile and no shared dependency changed. No installer, active skill,
policy example/schema, worker adapter, verification runner, approved plan,
tracker, AGENTS.md or orchestration state was changed. No commit, network,
dependency install, subagent, model or sbx launch was used.

## Verification results

Commands ran from the repository root, one gate at a time.

| Exact command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest.test_reserve_replay_survives_reload` | Before implementation: failed with missing `reserve_operation`, confirming absent API. After implementation: 1 passed. This is an absence check, not proof against a faulty existing replay implementation. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest` | Final targeted run: 9 passed, 3.224 seconds. Exercises actual policy, lock, filesystem publication and independent controller processes. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_impossible_correction_cycle_fails_before_worker_preflight skills.task-orchestrator.tests.test_controller.ControllerReservationTest` | 9 passed at that point, after updating the obsolete cycle rejection. The later public CLI case brought the reservation class to nine tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | Final: 44 passed, 0.516 seconds. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | Initial: 84 tests with two failures in one obsolete positive-cycle rejection test. After its contract-aligned correction and the added CLI case: 85 passed, 28.208 seconds. No skips. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_git.ControllerGitWiringTest.test_run_next_uses_controller_git_task_baseline_and_closure_evidence` | 1 passed, 0.576 seconds; preserved real Git baseline/closure wiring under the renamed private helper. |
| `git diff --check` | Passed; hygiene only, not behavioral proof. |

No nested-sandbox failure occurred in the owning controller suite on this run.
The broader command `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
was intentionally not run: fresh discovery owns its aggregate decision under the
brief. Preflight records an existing retrieval-inventory aggregate failure;
this invocation neither requalifies nor fixes it.

## AC, scenario and finite-risk evidence

Each row below is submitted implementation evidence. All reviewer statuses
remain unassigned; fresh independent discovery must corroborate them.
The command for the nine named methods is the final reservation-class command
above. Their setup writes successor outcomes only in the labelled
`seed_successor` test fixture, with real controller reservation/count logic.
No production admission or launch is claimed.

| Scenario / AC / risk | Current setup, oracle and evidence |
|---|---|
| V-01 / AC-01 | `test_status_is_read_only_and_preserves_evidence_distinctions` seeds actual ledger evidence, candidate/reference and open finding records. Reloaded public status preserves identity/count/actions and all run/task bytes; passed/failed/stale/blocked/missing/not_run are distinct, required omission is blocked, input mismatch is stale and a targeted-only repository-gate omission remains explicit. `test_public_cli_contract_and_weakened_authority_refusal` also exercises the real status CLI. |
| V-02 / AC-02/03 / R1 | `test_reserve_replay_survives_reload` checks first assignment and exact original-key replay with unchanged bytes. `test_active_states_and_conflicts_preserve_files_and_charge` covers competing keys, changed-key requests, reserved/running/unknown records without receipts, inspect/update/revise-flow guard paths, reload, and explicit terminal state permitting the next reservation. `test_separate_process_reservations_have_one_winner` synchronizes two actual processes through stdin/stdout, then proves exactly one durable assignment and zero charge. The CLI contract case exercises reservation, replay and stale-version refusal. |
| V-03 / AC-04 / R2 | `test_shared_budget_repair_replay_restart_and_fourth_refusal` reserves initial implementation at zero, then mixed failed-check/review/repair corrections at 1/2/3. Each request reloads state; replay/uncertainty preserves the charge/files, and a fourth mixed-route request preserves bytes and requires intervention. `test_repair_before_initial_implementation_does_not_reset_count` charges a pre-implementation repair, refuses implementation without fresh preflight, admits test-seeded new readiness, starts initial implementation at retained count 1, allows only corrections 2/3 and refuses the fourth. `test_free_evidence_and_preflight_retries_never_authorize_repair` reserves repeated check/collection/acceptance work and preflight without charges/write authority, refusing disguised repair unchanged. |
| V-04 / AC-03/05 / R3 | `test_invalid_requests_readiness_and_public_legacy_guards` compares real run/task bytes across invalid/stale version, task, role, stage, empty key and unauthorized-reason requests. Missing/failed/old-input/wrong-operation/wrong-task/old-flow readiness fails; unknown preflight and terminal non-preflight records cannot grant readiness. Real public run-next stays pending with valid or unknown test-seeded ownership/readiness. Generic updater injection is rejected. The active-state test covers inspect/revise-flow ownership guards. The CLI contract test refuses a weakened frozen profile unchanged. Existing owning-suite old-authority tests remain passing through the explicitly private mechanics. |
| V-05 / AC-05 | Source and [controller-contract.md](controller-contract.md) reconciled against the public CLI status/reserve/replay/stale-refusal test and V-01..04 results. Assignment fields are the actual validator/producer fields; no public outcome setter exists. Readiness/observed terminality remain T-003, semantic eligibility T-004/005, input revision T-002.3, completion T-005. Documentation is supporting evidence, not reservation proof. |

R1's first/replay/competing versions, all three active states, terminal and
reload/process cases map to V-02. R2's cycle-zero/1/2/3/fourth, mixed reasons,
pre-initial repair, route changes, replay/restart/free retries and uncertain
charge map to V-03. R3's wrong/stale authority, weak profile, all readiness
variants and legacy paths map to V-04. No verification scenario or finite-risk
row is omitted from implementation evidence.

## Limits and next owner

Assignments remain reserved in production until T-003 implements outcome and
readiness admission. Future evidence/correction reasons are consumed through
persisted controller-owned seams, not admitted by this leaf. Test-written
successor states prove reservation behavior only. Coherent out-of-band rewriting
of an entire run is not an authenticated-admission guarantee. Private legacy
transport regressions qualify mechanics, not sbx launches or the new public
workflow. Green tests do not constitute independent acceptance.

No repository-mandated architecture gate, maintainability stage or contract
registry applies to this submission. There is no current contract registry;
the package contract is the requested handoff. Do not infer another mandatory
stage from a previous task's chosen review route.

First outstanding stage and complete ordered route:
**fresh independent `task-review-discovery` → separate fresh
`task-acceptance-review`**. Discovery owns corroboration of V-01..V-05/R1..R3 and
the aggregate-gate decision. The caller/coordinator starts these separate
invocations. No reviewer was launched or managed by this implementer.
