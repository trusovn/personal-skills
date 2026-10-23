# Task Review Discovery Report: `T-002.1` — Freeze the approved one-task policy

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery` |
| Coverage completeness | `complete` for authority rows; two bounded sub-boundaries `blocked` on this host (schema validator, inspection runtime) — see ledger |
| Discovery iteration | 1 (first discovery pass after MNT-01 correction) |
| Created at | 2026-10-23T15:30:00Z |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report path | `skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-01.md` |
| Task brief | `skills/task-orchestrator/docs/tasks/T-002.1/brief.md` (revision 1) |
| Verification design / task context | `verification.md` (revision 1), `preflight.md`, `implementation-report.md` (MNT-01 correction), `controller-contract.md`, `reviews/maintainability-01.md`, `reviews/maintainability-02.md` |
| Current submission | Implementer: `READY_FOR_REVIEW`; maintainability-02: `ACCEPT` (maintainability only); all V-01..V-05 rows pending independent review |

This report publishes evidence only. It contains no acceptance verdict, no
approved deferral, and no advancement. The separate acceptance decision call
consumes it. It applies only to the reviewed bytes and artifacts identified
below; any correction requires a new discovery report. This report does not
review or authenticate itself.

## 1. Discovery provenance

| Question | Evidence |
|---|---|
| Did this session author any reviewed production bytes? | `no — independent` (fresh session; staged T-002.1 bytes authored by the implementer run, per `implementation-report.md`) |
| Independent evidence authority | `yes` |
| Current byte identity | HEAD `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`; 26 staged entries + 3 untracked `.DS_Store`; worktree == index for all reviewed paths (`git diff` unstaged: empty); full pre-report status captured at `/tmp/opencode/discovery-status-before.txt` |

## 2. Findings, ordered by suggested severity P0 through P3

### F-02 [suggested P2] Sibling-suite fixture broke: aggregate gate fails on the new required policy fields

| Field | Evidence |
|---|---|
| Finding ID | `F-02` |
| Suggested severity | `P2` (no production defect, no data risk; breaks the repository aggregate-gate signal and the preflight's "add no new failures" contract at aggregate level) |
| Current location | `skills/task-orchestrator/tests/test_controller_git.py:635` (policy fixture, `"version": 1`, no `execution_authorization`, no `flow`) exercised at `:681` via `controller.persist_run_policy` |
| Triggering state/input | Run the aggregate suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` with the current staged bytes on any host |
| Consequence | `test_controller_git.ControllerGitWiringTest.test_run_next_uses_controller_git_task_baseline_and_closure_evidence` errors with `ValueError: Run policy is missing: execution_authorization` before exercising its wiring assertions. The full local orchestrator suite is red on every host due to this fixture, beyond the documented macOS-only environmental baseline. Successors (T-002.2) running the aggregate will see a failure they did not cause |
| Evidence | Aggregate gate (DISC-05): 187 tests, 7 failures + 8 errors + 14 skipped; this error is the only non-environmental, non-pre-existing one. Production `validate_run_policy` (`controller_state.py:908-923`) now requires `version: 2`, `flow`, `execution_authorization` and exactly one `task_ids`; the fixture at HEAD/worktree is unchanged (`git diff` shows no edits to `test_controller_git.py`) and outside the brief's named test files |
| Affected AC | AC-03 (synchronize runtime constants, validation, schemas and current examples), AC-04 (compatibility and handoff) |
| Broken invariant | Repository aggregate gate green modulo the documented environmental baseline; preflight instruction "Your work must add zero new failures" |
| Credible sibling surface | Explicitly bounded: `test_codex_worker.py` constructs a `"version": 1` policy but never passes it to the changed validators (`validate_run_policy`/`persist_run_policy`/`resolve_flow_profile` absent) and its suite passes. No other suite constructs run-policy dicts for the changed validators. The four `assets/examples/*` provide canonical policy shapes |
| Smallest corrective direction | Synchronize every run-policy fixture in the repository with the frozen policy contract (version 2, `execution_authorization`, explicit flow, exactly one task), keeping the test's wiring assertions intact. Because `test_controller_git.py` is not in the brief's listed test files, the acceptance call must route the ownership decision (brief-scope widening vs. task-authority-owned fixture update); discovery does not decide |

Note: the retrieval-surface aggregate failure (`test_retrieval_surface.test_expected_current_references_exist`) is **pre-existing at HEAD** (planning docs already in `skills/task-orchestrator/docs/` at HEAD exceed the test's expected 4-entry set) and is not a finding against these reviewed bytes; recorded in sections 7 and 8.

## 3. Completeness ledger

| Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| V-01 | AC-01, R2 — frozen authority cannot silently adopt source edits | brief/verification/policy/manifest edits; reopened run; multiple active tasks refused | Real disposable repo + `init_run`; before/after byte comparison of every run file; `load_frozen_inputs` + `_load_flow_authority` | `test_frozen_authority_survives_source_edits` (controller suite, green on this host); MNT-02 digest assertions | DISC-03 probes B1–B4, C (frozen content unchanged after each source edit; no records written; prompt source is frozen) | pass |
| V-02 | AC-02, R1 — required stages/roles/single-task authority; no actor completion | each of 8 stages omitted; roles merged; reordered; optional mode; 2 task ids; actor results at controller stages; run-next pending at `ready` without worker launch | Runtime validator + public CLI init/run-next; no partial run publication; oracle: refusal + byte comparison | `test_init_refuses_weakened_authority_without_partial_publication`, `test_pending_ready_persists_cursor_without_launching_worker`, state matrix (all green on this host) | DISC-03 probes F (5 public-CLI variants), H, I, J | pass |
| V-02a | AC-02, R1 — inspection cannot grant acceptance (runtime) | inspect after mechanical verify stops pending `semantic_review`; repository-gate gap preserves pending review; crash replay non-accepting | `inspect_run` with real verification execution | `test_inspect_keeps_pending_semantic_review_non_accepting`, `test_repository_gate_authorized_gap_preserves_pending_review`, `test_inspect_reuses_execution_after_crash_with_review_pending` (implementer reports macOS pass of all 76) | Static: `controller.py:1178-1212` — `accepted = mechanically_eligible and current_step == "accept"`; the 8-stage flow never reaches `accept` from inspection; `semantic_review: "not_collected"` published | blocked on this Linux host — macOS-only `sandbox-exec` in `verification_runner.py` (out of scope); static decision-path confirmation only; macOS results are submitted evidence, not independent |
| V-03 | AC-03, R2 — approved mapping and correction-session rules (runtime/persisted) | `gpt-6.1-sol` low/medium/high; stale model/effort/budget refused; missing/malformed sbx/YOLO/intervention refused; occupancy 0.0/0.49 reuse, 0.5/0.51/unknown/unreliable/NaN/inf/bool/totals-only fresh; 3 shared corrections incl. repair, 4th stop/escalate; examples ↔ runtime agreement | `validate_run_policy`, `validate_flow_profile`, `correction_session_policy`, `transition_flow_cursor`; examples loaded through runtime validation (state suite `flow()` helper reads example JSON) | State tests `test_required_stages_roles_policy_and_context_boundaries`, `test_corrections_share_budget_including_environment_repair`, `test_policy_never_defaults_missing_or_malformed_authorization` (green) | DISC-03 probes G (10 occupancy cases), L (4 type confusions), I; state suite 44/44 | pass (runtime part) |
| V-03s | AC-03, R2 — schema/example structural agreement (Draft 2020-12 validator boundary) | four changed schemas + four current examples; 12 invalid policies / 4 actor claims rejected by schema | Execute a Draft 2020-12 validator (`jsonschema`) with ≥1 valid and ≥1 deliberately invalid instance per changed schema | Implementer's `/tmp/t0021-schema-check.py` (macOS host, `jsonschema` installed there): "four schemas and four examples valid; 12 invalid policies and four actor claims refused" — submitted-only | Not executable on this Linux host: `jsonschema` not installed (`ModuleNotFoundError`); installing requires network, which the brief forbids | blocked — concrete non-gate blocker (no Draft 2020-12 validator on this host); cannot be reported as passed |
| V-04 | AC-04, R2 — incompatible frozen old runs refused before mutation | old policy version; old model mapping; optional profile missing mandatory stage; missing `inputs_sha256` reference; all four mutation entries (run-next, inspect, revise-flow, update-ledger) | Real run files; public CLI continuation + byte comparison of every persisted file | `test_old_run_continuation_refuses_without_mutation`, `test_old_flow_refuses_all_mutation_entries_without_touching_run` (both green on this host) | DISC-03 probes D (3 families via public CLI), E (missing snapshot ref); refusal message contains "Initialize a new run using reviewed current inputs"; bytes unchanged | pass |
| V-05 | AC-04 — published contract matches executable declarations | CLI commands; library-only `update_ledger`; eight stages/roles/modes; `execution_authorization`; correction dict; session policy; envelope families/`evidence_status`; record byte conventions; revise-flow boundary; missing operations explicit | Static comparison of `controller-contract.md` against `controller.py`, `controller_state.py`, staged schemas/examples | Contract note + MNT-01 correction (reviewed by maintainability-02) | Static check: CLI subparsers = init/run-next/inspect/revise-flow only; `update_ledger` has no subparser; `FLOW_STEP_ORDER`/`FLOW_STEP_ROLES`/`FLOW_STEP_MODES` match the 8-stage table; `validate_step_outcome` result families and `evidence_status == "reported"` match (staged `step-outcome.schema.json` `const: "reported"`); handoff envelope stays version 1; `correction_session_policy` matches `[0, 0.5)` reuse rule; `revise_flow` preconditions match (ready, no selection/attempt/operation/cursor, cycle 0); `minimal-run-policy.json` = version 2 + exact authorization + single task + explicit flow | pass (static) |
| MNT-01 | Prior review continuation — one persisted `inputs.json` byte convention across production/contract/fixture | fixture no longer appends `\n`; real init asserts no trailing newline + digest binding | Exact reviewer reproducer (maintainability-01) | MNT-01 correction report; maintainability-02 ACCEPT | DISC-04 exact reproducer pair on current bytes: 2 tests, `OK` | pass |

## 4. Adversarial state and evidence checks

| Ledger row / invariant | Cases exercised | Result and evidence |
|---|---|---|
| Selected versus non-selected state coherence | Non-selected ready task not authorized (`test_select_task_returns_only_authorized_task`, green); two-task policy refused at init (probe F-two-tasks) | pass |
| Exact cardinality | zero (probe K), one (probe A/B init), two (probe F-two-tasks; state test) `task_ids` | pass — only exactly one accepted |
| Latest/current ordering | `kinds != list(FLOW_STEP_ORDER)` rejected; reversed steps refused (probe F-reorder); cursor advance follows the 8-stage order (state tests green) | pass |
| Exact ready/eligible set | `select_task` returns only the authorized task; incomplete-dependency blocking retained (`test_select_task_blocks_on_incomplete_deps`, green) | pass |
| Parent/child terminal coherence | `advance` refused from `accept`/`completed`; `complete_correction` refused without active cycle; `begin_correction` requires cycle ≥ 1 and current stage in checks/collection/acceptance (probes H, I) | pass |
| Persisted type strictness | `yolo: 1`, `limit: 3.0`, `enabled: 1`, `includes_environment_repair: 1` all refused (probes L); dict-equality bypass confirmed rejected (`controller_state.py:121-128`, `:919-923`) | pass |
| Coherent tampering | `test_tampered_flow_fails_before_worker_preflight_or_run_mutation` green on this host; digest-binding is per-run self-consistent — a writer with run-dir access could recompute ledger digests coherently; no independent anchor is claimed by the task (its claim is source-input edits, probes B/C confirm) | pass with documented residual risk (section 8) |

## 5. Independent probes and command results

| ID | Exact command / probe | Working directory / environment | Purpose / ACs | Result and observed signal | Side effects / cleanup | Independence / gap |
|---|---|---|---|---|---|---|
| DISC-01 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | repo root, Linux host | V-01..V-03 owning state suite | 44 tests, `OK` (0.393s) | none | independent run of current bytes |
| DISC-02 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | repo root, Linux host | V-01..V-05 owning controller suite | 76 tests: 6 errors + 1 failure, all rooted in `UnsupportedSandbox: sandbox-exec verification is supported only on macOS` in `ControllerInspectionIntegrationTest` (pre-existing, documented in `preflight.md`; `verification_runner.py` out of scope). All changed/new task tests pass on this host | none | environmental gap only; macOS-host pass (76/76) is implementer-submitted evidence |
| DISC-03 | `/tmp/opencode/t0021-discovery-probe.py` (37 adversarial probes against public CLI + state module in a disposable temp repo/run; two initial probe bugs fixed and re-run clean) | disposable `tempfile` under `/tmp/opencode`, run dirs outside repo; read-only w.r.t. real repository | independent corroboration of V-01..V-04, R1, R2 | 37/37 probes pass (frozen identity, old-run refusal via CLI, weakened-authority refusal without publication, occupancy boundaries, cursor terminal states, type strictness) | `shutil.rmtree` of the disposable root; repository `git status` unchanged after all probes | independent; not a copy of the implementer's suites |
| DISC-04 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_rejected_controller_update_leaves_persisted_bytes_unchanged skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_frozen_authority_survives_source_edits` | repo root, Linux host | MNT-01 reviewer regression | 2 tests, `OK` (0.079s) | none | exact maintainability-01 reproducer on current bytes |
| DISC-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | repo root, Linux host | aggregate-gate decision (brief assigns to fresh discovery) | 187 tests: 7 failures + 8 errors + 14 skipped. 12 environmental (macOS-only sandbox-exec, pre-existing), 1 pre-existing retrieval-surface docs drift, **1 task-induced: F-02** (`test_controller_git` fixture rejected by new required policy fields) | none; no surviving fixture processes (checked) | run by discovery, not implementer; environmental baseline from `preflight.md` |
| DISC-06 | `git diff --check`; `ps` scan for fixture processes; pre/post `git status --porcelain` diff | repo root | hygiene | diff-check clean (rc 0); zero controller/fake-codex processes; status identical before and after all probes | none | — |

Required-but-unrun: none beyond the two blocked rows (V-02a runtime inspection on this host; V-03s schema validator on this host), each with a concrete non-gate blocker and owner in section 8.

## 6. Aggregate-gate decision

| Field | Value |
|---|---|
| Gate / exact command | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` |
| Status | `failed` — 12 environmental (macOS-only sandbox, pre-existing/out-of-scope), 1 pre-existing retrieval drift (F-01 in section 7/8), 1 task-induced `test_controller_git` fixture break (finding F-02) |
| Owner and stage | initial discovery (this pass), as the brief assigns the aggregate decision to fresh discovery |
| Reason | Blast radius justified it: production changes to the shared `controller_state`/`controller` modules are consumed by sibling suites. All safely runnable required rows had current targeted evidence before the gate; the two blocked rows have concrete non-gate blockers (no Draft 2020-12 validator; macOS-only sandbox). No decisive targeted failure of reviewed bytes preceded the gate |
| Current evidence | DISC-01..DISC-05; the gate itself produced F-02, which targeted runs had not reached because the brief's targeted commands exclude `test_controller_git.py` |

## 7. Scope and baseline comparison

| Item | Recorded baseline | Current reviewed state | Classification / evidence |
|---|---|---|---|
| `HEAD` | `4449a3f373af9fabdcfe0c4d4b661988c4640c7f` (preflight, implementation report) | `4449a3f373af9fabdcfe0c4d4b661988c4640c7f` | expected, unchanged |
| Exact `git status --short` | 26 staged + 3 untracked `.DS_Store` at review start (`/tmp/opencode/discovery-status-before.txt`) | identical before and after all probes; the only addition from this review is this report file | task/packet state preserved; no user state touched |
| Dirty path index/worktree identities | — | worktree == index for all reviewed paths (`git diff` unstaged: empty); no unstaged drift | clean separability |
| Task-owned paths | brief allows `scripts/controller.py`, `scripts/controller_state.py`, `assets/` schemas/examples, their focused tests (`test_controller.py`, `test_controller_state.py`), package report/contract | staged diff matches exactly those paths; `test_controller_git.py` is not in the brief's list and is unchanged | in scope, except F-02's affected sibling fixture sits outside the named test files |
| Durable package artifacts | brief/verification revision 1, preflight, implementation-report, contract, maintainability reviews | all present and consistent; superseded `implementation-handoff.md` kept as history | canonical |
| Staged non-task entries | `M AGENTS.md` (one-line governance deletion), planning packages (`docs/tasks/T-002*`, `T-002.2`, `T-002.3`, `index.json`), 3 `.DS_Store` | still staged/untracked as at review start | pre-existing user/planning work, not attributed to this implementation (consistent with maintainability-01/02); not reviewed as task bytes |
| Pre-existing aggregate failures | `preflight.md` recorded 6 environmental failures in `test_controller.py` on Linux | aggregate shows 12 environmental (controller inspection 7 + verification_runner 5) plus the retrieval-surface docs drift (F-01) | pre-existing at HEAD: `git ls-tree HEAD` shows `skills/task-orchestrator/docs/` already contains 10 entries while the test expects exactly 4; not caused by these reviewed bytes |

Post-report state: `git status --short` after this write adds exactly `?? skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-01.md`; no other change (verified in section 1).

## 8. Questions, unchecked work, and residual risks

| Type / row ID | Evidence or reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| finding | F-02: sibling-suite fixture unsynchronized with the frozen policy contract (section 2) | yes | acceptance decision call routes ownership: brief-scope widening or task-authority-owned fixture update; implementer owns the correction if authorized |
| blocked | V-02a runtime inspection non-acceptance cannot execute on this Linux host (`sandbox-exec` macOS-only in out-of-scope `verification_runner.py`); static decision-path confirmation only; implementer's macOS 76/76 is submitted evidence | no | macOS-capable verification owner, or acceptance call may weigh the static evidence |
| blocked | V-03s Draft 2020-12 schema-validator boundary cannot execute on this Linux host (`jsonschema` not installed; network install forbidden by the brief); implementer's macOS schema script is submitted-only | no | evidence owner on a host with `jsonschema`, or acceptance call may treat schema text + runtime/example agreement as the available evidence |
| residual risk | Per-run digests are self-consistent; a writer with run-dir write access could recompute ledger digests coherently. The task claims source-input-edit protection (confirmed), not an independently anchored tamper barrier; no finding | no | successor work (evidence admission / T-002.3) |
| residual risk | Parallel-authority stage/role policy (runtime constants, 4 schemas, 4 examples, contract note) must be synchronized deliberately by successors (carried from maintainability-01/02) | no | T-002.2/T-003 owners |
| residual risk | `stage_transport_fixture` in `test_controller.py` mutates persisted ledger bytes to bypass not-yet-implemented ready/preflight admission; must migrate to the real path when T-002.2 lands admission | no | T-002.2 implementation |
| pre-existing | Retrieval-surface docs-drift failure at HEAD (planning docs added without updating the test's 4-entry expectation) | no | planning-work owner; outside this task's scope |

## 9. Coverage completeness and next route

| Field | Value |
|---|---|
| Coverage completeness | `complete` for all authority rows on this host with the two bounded blockers above (V-02a runtime, V-03s schema validator); no omitted material row; no hidden green behind refusals |
| Basis | Ledger rows V-01..V-05 (+ V-02a, V-03s, MNT-01), findings F-02 (+ pre-existing F-01 excluded from findings), probes DISC-01..DISC-06, aggregate gate record |
| Next owner | separate acceptance decision call (fresh `task-acceptance-review`) |
| Exact next action | Hand the brief, scoped diff, this report, finding F-02, blocked rows V-02a/V-03s, and the packaged preparation references (verification revision 1, preflight, maintainability reviews) to a fresh acceptance decision call |

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: 1; HEAD 4449a3f373af9fabdcfe0c4d4b661988c4640c7f; 26 staged + 3 untracked .DS_Store; worktree == index for reviewed paths
- Coverage rows: V-01=pass; V-02=pass; V-02a=blocked (Linux lacks macOS sandbox-exec; static decision-path confirmation; macOS suite evidence submitted-only); V-03=pass (runtime); V-03s=blocked (no Draft 2020-12 validator on this host; implementer macOS schema script submitted-only); V-04=pass; V-05=pass (static); MNT-01=pass (reproducer pair OK)
- Finding IDs: F-02 [suggested P2] test_controller_git policy fixture rejects under the new required fields (execution_authorization/flow/version 2/single task) -> aggregate gate red beyond environmental baseline; sibling surface explicitly bounded to test_controller_git.py (test_codex_worker passes, never calls changed validators)
- Finding/scenario continuity: MNT-01 (maintainability-01 CHANGES_REQUESTED -> maintainability-02 ACCEPT) remains resolved on current bytes; V-02a/V-03s keep concrete non-gate blockers with owners above; no prior discovery ledger existed (first discovery pass)
- Preparation/context: brief.md rev 1; verification.md rev 1; preflight.md; implementation-report.md (MNT-01 correction); controller-contract.md; reviews/maintainability-01.md, maintainability-02.md
- Reviewer regressions: exact maintainability-01 reproducer pair (DISC-04): PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_rejected_controller_update_leaves_persisted_bytes_unchanged skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_frozen_authority_survives_source_edits -> OK
- Aggregate gate: failed, run by initial discovery (DISC-05): PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py' -> 187 tests, 12 environmental + 1 pre-existing retrieval drift + 1 task-induced (F-02)
- Next: separate fresh task-acceptance-review consuming this report, with F-02 ownership decided (brief-scope widening vs task-authority-owned fixture update)
```
