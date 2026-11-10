# T-003 implementation submission

Implemented: **READY_FOR_REVIEW**. The controller can launch reserved actors,
admit terminal current preflight readiness, launch the first implementation,
and conservatively preserve uncertain operations. Independent review is owed;
this report makes implementation claims, not an acceptance decision.

Consumed preparation: [brief.md](brief.md) revision 1,
[verification.md](verification.md) revision 1, [preflight.md](preflight.md), and
the accepted [predecessor contract](../T-002/controller-contract.md). Preflight's
current applicability held: same authority/scope/dependencies and no overlapping
production edits. Measurement's exact pre-edit inventory/hashes/project binding
were validated before editing. Original reports use the active installation's
pinned tools/settings and cover future Python within the two selected parents.

## Deliverables and contract impact

- Fresh actor bridge in codex_worker.py; process/session/terminal observations,
  stop-request handling and separate actor result protocol.
- Controller launch/observe/stop/intervention callables and CLI, one semantic
  admission extension path, blocked/unknown intervention records and status.
- State validation for optional transport observations; existing correction,
  immutable authority and owner-revision boundaries retained.
- actor-result.schema.json; real-process public-boundary tests in
  test_actor_operations.py, and updated existing status-action assertions.
- Updated directly affected SKILL.md/operator/index/architecture references and
  [controller-contract.md](controller-contract.md), including ART-008 supplement.

Actual contract impact: added actor transport launch/observation/stop/intervention
APIs/CLI and result schema; extended embedded operations with transport/outcome,
status with chat history/action, and preflight evidence/readiness admission.
Raw implementation/collection/acceptance records are handoffs, not semantic admission.
Executable contract declarations changed: controller.py, controller_state.py,
codex_worker.py and assets/actor-result.schema.json. Registry synchronization is
owed to the later registry updater; docs/contracts was deliberately not edited.
The canonical installer was inspected: task-orchestrator is not in the development
profile, and no selected skill/shared runtime dependency changed. No installer or
active installation refresh is needed or performed.

Pre-existing user changes to tasks/index.json, brief.md and verification.md were
preserved. No official plan/tracker, Git index, commit or dependency was changed.
No external messages, live model checks or provisioning were performed.

## Current implementation evidence

All commands ran from the repository root. Raw logs are retained in
[evidence/](evidence/); early attempts remain historical, not current passes.

| Command | Current result / raw record |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py` | **15 passed**, evidence/T-003-focused-final.log; real filesystem/Git/child processes, fake Codex |
| Same discovery, `-p test_codex_worker.py` | **15 passed**, evidence/T-003-transport.log; also current aggregate |
| Same discovery, `-p test_controller_state.py` | **45 passed**, evidence/T-003-state.log; also current aggregate |
| Same discovery, `-p test_controller.py` | 95 tests, 1 failure/6 errors at legacy sandbox boundary; evidence/T-003-controller.log and current aggregate |
| Same discovery, `-p 'test_*.py'` | **222 tests: 195 passed, 6 failed, 7 errors, 14 skipped**, evidence/T-003-orchestrator-final.log |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | **4 passed**, evidence/architecture.log; executed once via active run-evidence wrapper, also covered by aggregate root suite |
| `python3 tools/check_contracts.py --root .` | **passed**, 8 subsystems/26 refs; structural only, also current aggregate |
| `python3 tools/verify.py` | **failed**, 7 checks/1 failed (orchestrator). Root suite **310 tests, 32 skipped, no failures**; other suites 3/13/4 passed; registry and 112-path installed-profile drift checks passed. evidence/T-003-aggregate.log |
| `git diff --check` | passed; whitespace only, not behavioral qualification |

The 13 orchestrator nonpasses arise before intended legacy macOS sandbox
assertions on this non-macOS host. Seven belong to legacy controller inspection;
they reproduce identically on an untouched HEAD extraction in
`evidence/T-003-baseline-legacy.log` (95 tests, same 1 failure/6 errors). Six belong
to the unchanged verification runner/tests and fail at its same platform guard.
Those two files were verified unchanged against HEAD. This matches the inherited
boundary documented by predecessor acceptance, not a new actor regression.
The 14 skips are platform containment scenarios. Root's 32 skips require optional
real analyzer tools in the test interpreter; the separate pinned measurement
launcher did produce complete actual evidence. These skips are not passes.
No sandbox restoration or optional-tool provisioning was authorized/imposed.

Test sensitivity: evidence/T-003-mutation-02.log records a controlled injected
no-op readiness validator. The missing-tool/dependency/skill scenario rejects it
with **three expected assertion failures and no harness errors**, without editing
production bytes. The first fault probe reached TypeError assertions; that
historical log is retained and the assertions were corrected before the valid
fault probe. The initial 14-case run exposed an invalid seeded correction cursor
at cycle zero; the fixture now seeds only future reason authorization at a valid
implement cursor. No production behavior was changed to accommodate that fixture.
Early focused logs remain retained; final 15-case and aggregate records govern.

## AC and scenario accounting

Every row uses the focused command above unless another source is named. Test
names below are methods of ActorOperationsTest. Subcases keep independent invalid
fields and valid controls; no schema-only claim establishes execution.

| Scenarios / AC | Inputs, decisive observation, current evidence |
|---|---|
| V-01 / AC-01 | `test_v01_v06_frozen_models_readiness_and_first_implementation`: independently approved light/standard/strong flows; actual child argv low/medium/high, frozen document bytes despite mutable replacement. `test_v08_revision_rejects_stale_launch_and_repointed_readiness` observes approved revised text reaching the new actor. Pass. |
| V-02a/b / AC-01 | `test_v02_authorization_and_old_policy_are_refused_at_launch`: incompatible persisted policy fixtures (missing auth, false YOLO, old version) refuse public launch, preserve ledger and produce zero actor invocations. Valid launch controls are V-01. Pass. |
| V-02c/d/e / AC-01 | `test_v02_invalid_assignment_guards_do_not_launch_or_mutate` independently changes task/role/input/policy/flow bindings, snapshots ledger and counts zero launches; V-08 refuses historical assignment after authorized revision. Pass. |
| V-03 / AC-01 | `test_v03_v08_v11_shared_corrections_repair_and_fresh_preflight`: actual correction sessions differ from initial session and argv has no resume. Pure policy checks cover unknown, unreliable, invalid, 0.499, 0.5, 0.501. Reuse below threshold remains optional. Pass. |
| V-04 / AC-01/04 | `test_v04_replay_retains_outcome_and_configuration`, `test_v04_real_launch_contention_has_one_invocation`: replay while running/after reload/after terminal, conflicting config refusal, two gate-synchronized controller processes contend at real lock; exactly one actual child invocation. Pass. |
| V-05a/b/c/d/e/f/h / AC-02 | Valid V-01 terminal control; `test_v05_v07_invalid_results_retain_raw_evidence_without_readiness` independently exercises missing/malformed result, wrong role/task/operation/input/policy/flow/candidate, invented session, pre-session and post-session failure. Retained assignment/config/events/stderr/terminal record, distinct observed session availability, configured model vs null observed model, no readiness or implementation. Pass. |
| V-05g / AC-02 | `test_v05g_v10_nonterminal_result_cannot_admit_and_stop_is_observed`: result exists while actual process waits; observation stays running, readiness false and competing reservation refuses. Pass. |
| V-05i / AC-02 | `test_v12_review_roles_are_fresh_raw_claims_without_semantic_admission`: actor prose requests acceptance/policy change/skipped stages; implementation/collection/acceptance remain raw, no acceptance/completion authority. Pass. |
| V-06 / AC-03 | V-01/V-06 method actually runs disposable tool, evaluates dependency and reads installed skill, then admits readiness without seeding it and launches an implementation writing allowed.txt; count stays zero. Pass. |
| V-07a/b/c / AC-03 | `test_v07_missing_each_prerequisite_reaches_specific_blocker` independently removes tool, dependency, installed skill; actual actor checks report precise blockers and implementation cannot reserve. Counts stay zero. Pass. |
| V-07d/e/f/g / AC-03 | Invalid-result matrix covers incomplete inventory, wrong task/role/session and malformed output; revision test supplies old input identity in a new terminal output; V-05g and V-09 cover nonterminal/unknown liveness. No current readiness. Pass. |
| V-08 / AC-01/03/05 | Repair/revision history methods: real readiness before repair, charged authorized repair (only successor reason seeded), rejected old readiness even when repointed, actual fresh preflight; separately authorized input revision, stale launch/output rejection, fresh readiness and next valid implementation. Work/history/count retained; already-implemented correction authorization remains successor-owned. Pass. |
| V-09a/b/c/d / AC-04 | `test_v09_publication_interruption_never_relaunches`: SIGKILL real controllers after durable intent before spawn, after spawn before PID publication, after launch publication with result/actor waiting, and after terminal publication before response. Reload/replay never duplicates; unknown prevents another actor; observed terminal replay retains readiness/outcome. Pass. |
| V-10 / AC-04 | V-05g/V-10 method starts real actor plus child; group stop/reap observed, process absent, repeated stop/observe preserve ledger. `test_v10_timeout_is_failure_and_before_launch_stop_is_terminal` covers timeout and known-unlaunched cancellation; V-09 unknown stop retains unknown, never infers terminality. Coordinator interruption is exercised in V-09. Pass. |
| V-11 / AC-01/05 | Shared-history test launches cycle zero and three different correction reasons in one sequence, replays reservations/launches after reload, repairs then re-preflights, revises inputs without resetting count, refuses fourth correction and second free implementation. Seven actual actor invocations; no extra replay charge. Pass. |
| V-12a/b / AC-02 | Raw-review method seeds only unavailable successor candidate/check/collection prerequisites. Preflight, implementation, collection and acceptance have four distinct observed sessions; reviewer assignments prohibit edits, raw claims do not admit semantic evidence/completion. Pass. |
| V-12c/d/e/f / AC-05 | `test_v12_intervention_history_does_not_authorize_work` persists/reloads opened, relayed and acknowledgement events; rejects repair/retry and acknowledgement as input-revision decision; count unchanged and no completion. Missing prerequisites and unknown publication also persist precise opened records with evidence/action. Silence/repeated observation leaves unresolved work blocked; relay/response are never fabricated. Pass. |
| V-13 / AC-02/06 | **NOT RUN**: live approval, approved sbx/provider configuration and reviewed disposable inputs absent for this invocation. Brief explicitly permits this open qualification gap. T-006 owns approved actual-sbx launch/readiness/marker/terminality check and full pilot. |
| V-14 / AC-06 | `test_v14_public_cli_launch_and_observe` executes launch/observe CLI with real local child and replay; contract/reference reconciliation names implemented payloads/files/refusals/admission and unproved runtime claims. Pass for local interface reconciliation; no live-runtime claim. |

## Measurement and retained structure

Original pair (retained):
`.quality/reports/T-003-start-20261109-01.json` and `.txt`.
Current comparison: `.quality/reports/T-003-compare-20261109-01.json` and `.txt`.
Both have complete complexity/Ruff capture. Original scope is
`skills/task-orchestrator/scripts` and `skills/task-orchestrator/tests` (11
pre-edit files, real worktree bytes). Final affected set is controller.py,
controller_state.py, codex_worker.py, test_controller.py, test_actor_operations.py;
all five final source hashes match the comparison report. Identity, effective
settings, full_profile and files/source hashes in the reports remain authoritative.
There is no missing before-state or scope expansion. New symbols have absent
before counts, not invented zeros. Untouched legacy hotspots are context only.
No renames/extractions across files occurred. Terminal publication was extracted
locally into `_publish_actor_outcome`; the result classifier, stop polling and
group observation are cohesive adapter helpers, assessed with run_turn.

Retained-breach rationale (all figures from compare-20261109-01; CC target 10,
statements 50, arguments 5):

- `codex_worker.run_turn`: CC **23→25**, statements **94→96**, arguments
  **8→8**. New observed terminal/group fields and actor result classification
  belong beside the existing wait/finally/receipt lifecycle. Polling and result
  classification were extracted into focused helpers. A separate actor runner
  would duplicate signal/timeout/cleanup semantics; a wider lifecycle rewrite
  would expose unrelated legacy behavior. Retain this small increase.
- `controller._reservation_options`: CC **20→21**. Reserved launch vs launched
  observation/stop actions belong with the ordered stage/budget/readiness guards.
  A separate one-call active-action helper adds navigation without isolating a
  new responsibility. `reserve_operation` remains a materially edited legacy
  hotspot (CC **30→30**): clearing a previous diagnostic accompanies existing
  readiness invalidation; assignment-construction extraction was considered but
  would widen this bounded lifecycle change without simplifying that decision.
- New `launch_operation`: CC **12** (no before value). Its guards, intent commit,
  spawn and identity commit must be readable in one locked transaction. Prompt,
  immutable byte publication and ledger save already have separate ownership.
  Splitting the remaining transaction would hide its publication ordering.
- New `_validate_readiness`: CC **15** (no before). Its 13 statements validate
  three prerequisite inventories and their exact item evidence together.
  A per-item helper is possible but adds navigation for one compact consumer;
  retaining explicit denial checks makes missing-family evidence visible.
- New `observe_operation`: CC **15** (no before). Its 30 statements coordinate
  replay, unknown liveness, supervisor cleanup and publication under one lock;
  terminal admission/publication was extracted. A separate unfinished-observation
  helper is plausible but would spread the remaining single transition across
  more mutable-ledger helpers. Retained for visible ordering.
- New `record_intervention`: CC **14** (no before). Its 20 statements validate one
  exact event/subject and append/replay it atomically. A standalone payload
  validator could be extracted for another consumer; none exists, and separating
  key-conflict checks would obscure append-only history semantics.
- New `validate_actor_transport`: CC **11** (no before), 18 statements; validates
  one transport's configuration/process/terminal binding together. Splitting
  outcome checks adds navigation across a small pure record validator.
  `validate_actor_operations`: CC **54→57**, statements **64→66**. The added
  optional transport validation belongs at the operation boundary; nested
  transport rules were already extracted. Rewriting the older assignment/budget
  validator would expand scope and risk weakening its coupled invariants.

All other affected functions remain at/below effective targets. These advisory
metrics do not establish maintainability acceptance or override native failures.

## Native evidence, transfer and next owners

Native policy: repository AGENTS.md/docs/development.md and task verification.
The command table above records implementation-owned focused/whole-project
checks; no reviewer-owned check or verdict was run. The final measurement's file
hashes bind the five affected Python files; schema/reference reconciliation is
against this submission. Evidence logs record exact commands/outcomes, and the
run-evidence manifest retains the canonical architecture command/result.
Required native commands ran; aggregate remains failed and skips remain unproved.
No all-green release claim is made. Registry update remains owed to its proper
stage and must keep structural validation current afterward.

Run-evidence ID: `run-20261109T132715Z-7b10587a90ef` under
`.git/personal-skills/run-evidence/runs/`; closure is completed for the implementer
invocation, not task acceptance. Shared-worktree reviewers can use the exact
measurement/log paths above. Isolated consumers must copy both original
JSON/text files to the same `.quality/reports/T-003-start-20261109-01.*` paths,
both comparison files to `.quality/reports/T-003-compare-20261109-01.*`, and this
task's evidence directory; ignored reports do not travel with commits.

**Next owner and complete ordered remainder:** fresh
`task-maintainability-review` (significant state/process boundary change), then
`task-contract-registry-updater`, fresh independent `task-review-discovery`,
and the separate fresh `task-acceptance-review` decision. The required architecture
gate already passed for these submitted bytes. Discovery should use the distinct
probes required by verification.md and explicitly retain aggregate/platform and
V-13 limits. This implementation invocation ends here; no reviewers were launched
and no independent verdict is invented. Accepted contract/advancement remains
with those owners and the coordinator.
