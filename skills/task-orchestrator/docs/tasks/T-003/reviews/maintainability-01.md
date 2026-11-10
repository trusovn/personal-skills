# T-003 maintainability review

VERDICT: ACCEPT
ARCHITECTURE_GATE: PASS
MEASUREMENT: complete

## Provenance and scope

Independent reviewer session: this session authored none of the reviewed implementation or test assets. Review targets the staged T-003 change against HEAD `a120de04911d994cfeb3839e82fdaf7fdcba3212`. Reviewed Python hashes were checked against the Git index and implementer/reviewer measurement records. The three unrelated untracked `.DS_Store` files were excluded. This report records the completed review; it does not review itself or establish functional acceptance.

Reviewed implementation: `scripts/controller.py`, `scripts/controller_state.py`, `scripts/codex_worker.py`, `assets/actor-result.schema.json`, `tests/test_actor_operations.py`, and the changed assertions in `tests/test_controller.py`, all under `skills/task-orchestrator/`. Supporting task documents, skill instructions and runtime references supplied boundary context.

## Blockers

NONE. No concrete introduced or materially worsened cohesion, coupling, change-locality, testability, duplicated-authority or speculative-abstraction regression was found.

The controller retains orchestration and admission ownership, state validation remains pure, and the adapter owns process/session observations. Terminal preflight admission has one extension path. The process-handle cache supplements durable receipts rather than replacing durable authority. Tests reuse existing repository setup and exercise the process boundary with a local executable; interruption injection is confined to the test harness.

## Measurement evidence and rationale dispositions

All pairs below are under repository `.quality/reports/`; both JSON and text siblings are retained:

- Original B: `T-003-start-20261109-01.json` / `.txt`.
- Implementer I: `T-003-compare-20261109-01.json` / `.txt`.
- Independent R: `T-003-review-20261109-01.json` / `.txt`.

Reviewer command:

```sh
.quality/envs/Linux-aarch64-cpython-3.14.4-79dbf22b5bc1/bin/python .agents/scripts/measure_maintainability.py compare skills/task-orchestrator/scripts/controller.py skills/task-orchestrator/scripts/controller_state.py skills/task-orchestrator/scripts/codex_worker.py skills/task-orchestrator/tests/test_controller.py skills/task-orchestrator/tests/test_actor_operations.py --root . --baseline .quality/reports/T-003-start-20261109-01.json --output .quality/reports/T-003-review-20261109-01.json
```

Complexity and Ruff capture completed for all five affected Python files. Eleven preserved baseline sources match HEAD, and all five current hashes match staged bytes and I/R. B/I/R share HEAD, adapter, tool versions and settings; Git status differs because implementation and staging occurred between captures. Baseline directory coverage includes the added test. No missing before count is treated as zero. Reports use Radon 6.0.1 and Ruff 0.14.2; targets are advisory CC 10, statements 50 and arguments 5.

The retained-breach rationales in `../implementation-report.md` were independently assessed against the diff and R:

| Affected responsibility | Signal | Disposition |
|---|---|---|
| `codex_worker.run_turn` | CC 23→25; statements 94→96; arguments 8→8 | Agree with retention: new observations belong beside existing cleanup and receipt publication. Polling/classification helpers isolate added mechanics; a second runner would duplicate lifecycle policy. |
| `controller._reservation_options` | CC 20→21 | Agree: reserved-versus-running actions belong with existing ordered admission guards; another forwarding helper would add navigation. |
| `controller.reserve_operation` | CC 30→30 | Agree: diagnostic clearing accompanies readiness invalidation. Broader assignment extraction is unnecessary for this change. |
| `controller.launch_operation` | New CC 12 | Agree: visible guard/intent/spawn/identity ordering under one lock is valuable; publication and prompt helpers already separate cohesive work. |
| `controller._validate_readiness` | New CC 15 | Agree: one compact validator owns the three prerequisite inventories and evidence rules; splitting each denial would scatter the contract. |
| `controller.observe_operation` | New CC 15 | Agree: replay, liveness and publication form one transition; terminal publication is already extracted. |
| `controller.record_intervention` | New CC 14 | Agree: exact event validation, replay/conflict checks and append belong together in one locked history update. |
| `controller_state.validate_actor_transport` | New CC 11 | Agree: one small pure validator owns transport binding and terminal outcome consistency. |
| `controller_state.validate_actor_operations` | CC 54→57; statements 64→66 | Agree: optional transport validation is delegated to its owner; rewriting the older assignment/budget validator would broaden scope. |

Other affected functions remain at or below the applicable targets. Untouched hotspots are context, not blockers. Metrics are not behavioral verification.

## Native evidence and warnings

Reviewer executed the canonical whole-repository architecture command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
```

Result: PASS, 4 tests. CLEAN policy has no debt baseline. Reviewer also ran `python3 tools/check_contracts.py --root .`: PASS, 8 subsystems and 26 indexed plan references; this is structural evidence only.

Policy/boundary sources: repository `AGENTS.md`, `docs/project-map.md`, `docs/development.md`, `tests/test_architecture.py`, `docs/contracts/task-orchestrator.json`, and the orchestrator architecture map and T-003 brief/controller contract. The installed project-local maintainability skill and its measurement protocol governed this review; installed testing-discipline informed test-asset inspection. The development installer was inspected: task-orchestrator is outside its selected profile and introduces no shared runtime dependency.

Warnings carried forward:

- Implementer evidence reports aggregate verification failure: orchestrator 6 failures, 7 errors and 14 skips; root suite 32 skips. The implementation report attributes the failures to the inherited non-macOS legacy containment boundary and supplies baseline comparison evidence. These remain visible functional evidence limitations; this review did not rerun or grant functional acceptance of those suites. Live sbx/provider qualification remains unperformed.
- Registry synchronization is owed for the added actor lifecycle/result/readiness contracts. The designated post-review updater owns that work; it is not a maintainability blocker.

## Outstanding route

First: `task-contract-registry-updater`. Then fresh independent `task-review-discovery`, followed by the separate `task-acceptance-review` decision. This review executed none of those stages. Corrections affecting reviewed assets invalidate the applicable maintainability evidence and require fresh review.

## Git status evidence

Exact status before report creation:

```text
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
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
```

Exact status after report creation:

```text
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
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-003/reviews/maintainability-01.md
```

Only the new report entry was added; existing staged and untracked entries were preserved.
