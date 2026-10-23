# Task Review Discovery Report: `T-002.1` — Freeze the approved one-task policy

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery` |
| Coverage completeness | `complete` for authority rows; two bounded sub-boundaries `blocked` on this host (schema validator, inspection runtime) — see ledger |
| Discovery iteration | 2 (fresh correction pass after F-02 fix; consumes `reviews/discovery-01.md` as continuation context) |
| Created at | 2026-10-23T16:20:00Z |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report path | `skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-02.md` |
| Task brief | `skills/task-orchestrator/docs/tasks/T-002.1/brief.md` (revision 1) |
| Verification design / task context | `verification.md` (revision 1), `preflight.md`, `implementation-report.md` (MNT-01 and F-02 corrections), `controller-contract.md`, `reviews/maintainability-01.md`, `reviews/maintainability-02.md`, `reviews/discovery-01.md` |
| Current submission | Implementer: `READY_FOR_REVIEW`; maintainability-02: `ACCEPT` (maintainability only); all V-01..V-05 rows pending independent review |

This report publishes evidence only. It contains no acceptance verdict, no
approved deferral, and no advancement. The separate acceptance decision call
consumes it. It applies only to the reviewed bytes and artifacts identified
below; any correction requires a new discovery report. This report does not
review or authenticate itself.

## 1. Discovery provenance

| Question | Evidence |
|---|---|
| Did this session author any reviewed production bytes? | `no — independent` (fresh session; staged T-002.1 bytes authored by the implementer runs, per `implementation-report.md`) |
| Independent evidence authority | `yes` |
| Current byte identity | HEAD `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`; 28 staged entries + 3 untracked `.DS_Store`; worktree == index for all reviewed paths (`git diff` unstaged: empty); full pre-report status captured at `/tmp/opencode/t0021-d2-status-before.txt` |

## 2. Findings

**No findings against the reviewed bytes.** The prior finding F-02 is resolved
on current bytes (section 3), the MNT-01 byte-convention regression holds
(section 3), and all 70 independent adversarial probes plus the owning suites
behaved per the frozen contract. No defect was manufactured; pre-existing
environmental and retrieval-surface aggregate noise is recorded in sections 7
and 8 and is not attributed to these bytes.

## 3. Completeness ledger

| Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| V-01 | AC-01, R2 — frozen authority cannot silently adopt source edits | brief/verification/policy/manifest edits; reopened run; multiple active tasks refused; missing `verification.md` refused; tampered persisted bytes refused | Real disposable repo + `init_run` via public CLI; before/after byte comparison of every run file; `load_frozen_inputs` | `test_frozen_authority_survives_source_edits` (controller suite, passes on this host); MNT-01 digest assertions | DISC-05 probes: frozen brief/verification content, `allowed_paths`/`required_checks`, source-path provenance after source edits; `inputs.json + \n` → digest refusal; semantic policy tamper → digest refusal; two-task policy refused with no partial run; missing `verification.md` refused | pass |
| V-02 | AC-02, R1 — required stages/roles/single-task authority; no actor completion | each of 8 stages omitted; roles merged; reordered; duplicated/optional stage; policy without `flow`; 2 task ids; actor results at controller stages; collection ACCEPT; run-next pending at `ready` without worker launch | Runtime validator + public CLI init/run-next; no partial run publication; oracle: refusal + byte comparison | `test_init_refuses_weakened_authority_without_partial_publication`, `test_pending_ready_persists_cursor_without_launching_worker`, state matrix (green on this host) | DISC-05 probes: all 8 stage omissions refused; merged roles refused; reorder refused; duplicate refused; flow-less policy refused at init without publication; actor completion at `accept` refused; collection `ACCEPT` refused; acceptance with `collected` refused; run-next exits 0 with `pending`/`ready` cursor, no `attempts/` dir, no worker process | pass |
| V-02a | AC-02, R1 — inspection cannot grant acceptance (runtime) | inspect after mechanical verify stops pending `semantic_review`; repository-gate gap preserves pending review; crash replay non-accepting | `inspect_run` with real verification execution | `test_inspect_keeps_pending_semantic_review_non_accepting`, `test_repository_gate_authorized_gap_preserves_pending_review`, `test_inspect_reuses_execution_after_crash_with_review_pending` (implementer reports macOS pass of all 76) | Static: `controller.py:1178-1212` — `accepted = mechanically_eligible and current_step == "accept"`; the 8-stage flow never reaches `accept` from inspection; `semantic_review: "not_collected"` published | blocked on this Linux host — macOS-only `sandbox-exec` in `verification_runner.py` (out of scope); static decision-path confirmation only; macOS results are submitted evidence, not independent |
| V-03 | AC-03, R2 — approved mapping and correction-session rules (runtime/persisted) | `gpt-6.1-sol` low/medium/high; stale model/effort/budget refused; missing/malformed sbx/YOLO/intervention refused; occupancy 0.0/0.49 reuse, 0.5/0.51/unknown/unreliable/NaN/inf/bool/string/totals-only fresh; 3 shared corrections incl. repair, 4th stop/escalate; examples ↔ runtime agreement | `validate_run_policy`, `validate_flow_profile`, `correction_session_policy`, `transition_flow_cursor`; examples loaded from `assets/examples/` | State tests `test_required_stages_roles_policy_and_context_boundaries`, `test_corrections_share_budget_including_environment_repair`, `test_policy_never_defaults_missing_or_malformed_authorization` (green) | DISC-05 probes: actor mapping exact; 11 occupancy boundary cases; type confusions `yolo=1`, `limit=3.0`, `enabled=1`, `includes_environment_repair=1` refused; correction cycle 1→2→3 with `environment_repair` consuming the shared budget, 4th returns `corrections_exhausted` without advancing; invalid begin_correction result refused; state suite 44/44 | pass (runtime part) |
| V-03s | AC-03, R2 — schema/example structural agreement (Draft 2020-12 validator boundary) | four changed schemas + four current examples; invalid policies / actor claims rejected by schema | Execute a Draft 2020-12 validator (`jsonschema`) with ≥1 valid and ≥1 deliberately invalid instance per changed schema | Implementer's `/tmp/t0021-schema-check.py` (macOS host, `jsonschema` installed there): "four schemas and four examples valid; 12 invalid policies and four actor claims refused" — submitted-only | Not executable on this Linux host: Python has no `jsonschema` (`ModuleNotFoundError`), no pip cache, and global Node modules contain no JSON Schema validator; installing one requires network, which the brief and discovery boundaries forbid | blocked — concrete non-gate blocker (no Draft 2020-12 validator on this host); cannot be reported as passed |
| V-04 | AC-04, R2 — incompatible frozen old runs refused before mutation | old policy version; old model mapping; optional profile missing mandatory stage; missing `inputs_sha256` reference; mutation entries (run-next, inspect, revise-flow, update-ledger) | Real-file old-run fixtures (structurally valid as persisted by the old controller: `ready` and `awaiting_inspection` shapes); public CLI continuation + byte comparison of every persisted file | `test_old_run_continuation_refuses_without_mutation`, `test_old_flow_refuses_all_mutation_entries_without_touching_run` (green on this host) | DISC-05 probes: run-next, revise-flow (valid v2 requested flow) and inspect on realistic old fixtures all refuse with `Initialize a new run using reviewed current inputs.` and unchanged tree digests; `update_ledger` library path refuses with the same action and unchanged bytes; stale `gpt-5.6-sol` mapping refused; missing `inputs_sha256` refused | pass |
| V-05 | AC-04 — published contract matches executable declarations | CLI commands; eight stages/roles/modes; `execution_authorization`; correction dict; session policy; result families/`evidence_status`; record byte conventions; missing operations explicit | Static comparison of `controller-contract.md` against `controller.py`, `controller_state.py`, staged schemas/examples | Contract note + MNT-01/F-02 correction reports (reviewed by maintainability-02) | Static check on current bytes: CLI subparsers = init/run-next/inspect/revise-flow only; `FLOW_STEP_ORDER`/`FLOW_STEP_ROLES`/`FLOW_STEP_MODES` match the 8-stage table; `validate_step_outcome` families and `evidence_status == "reported"` match the contract table; `_canonical_record_bytes` = compact, sorted, no trailing newline (confirmed behaviorally by the V-01 newline-tamper refusal); `correction_session_policy` matches `[0, 0.5)` reuse; `revise_flow` preconditions match (ready, no selection/attempt/operation/cursor, cycle 0); `minimal-run-policy.json` = version 2 + exact authorization + single task + explicit flow | pass (static) |
| MNT-01 | Prior review continuation — one persisted `inputs.json` byte convention across production/contract/fixture | fixture no longer appends `\n`; real init asserts no trailing newline + digest binding | Exact reviewer reproducer (maintainability-01) | MNT-01 correction report; maintainability-02 ACCEPT | DISC-04 exact reproducer pair on current bytes: 2 tests, `OK` (0.071s) | pass |
| F-02 | Prior finding — sibling-suite policy fixture unsynchronized with the frozen policy contract | `test_controller_git.py` fixture now supplies version 2, explicit `execution_authorization`, prepared verification document, transport-boundary ledger seed | Sibling suite + aggregate gate | F-02 correction report; focused reproducer (green on this host per report) | DISC-03: `test_controller_git.py` 13/13 `OK` (0.346s); DISC-06 aggregate shows no task-induced failure | resolved on current bytes |

## 4. Adversarial state and evidence checks

| Ledger row / invariant | Cases exercised | Result and evidence |
|---|---|---|
| Selected versus non-selected state coherence | Two-task policy refused at init; `select_task` reads ledger entries built only from the single authorized `task_ids` entry | pass |
| Exact cardinality | zero/one/two `task_ids` — exactly one accepted (two-task CLI init refused, no partial run) | pass |
| Latest/current ordering | `kinds != list(FLOW_STEP_ORDER)` rejected; reordered and duplicated stages refused; cursor advance follows the 8-stage order | pass |
| Exact ready/eligible set | run-next at `ready` persists pending cursor at `ready` without worker launch; no attempt dir or process | pass |
| Parent/child terminal coherence | `advance` refused from `accept` and `completed`; `begin_correction` refused from `implement`; `complete_correction` refused without an active cycle | pass |
| Persisted type strictness | `yolo: 1`, `limit: 3.0`, `enabled: 1`, `includes_environment_repair: 1` all refused (dict-equality bypass for `1 == True` closed by explicit `is not True` check) | pass |
| Coherent tampering | `inputs.json` newline/byte tamper refused by digest; semantic policy tamper refused by digest; source-input edits never adopted | pass with documented residual risk (section 8): per-run digests are self-consistent, not an independent tamper anchor — the task claims source-input-edit protection, which is confirmed |

## 5. Independent probes and command results

| ID | Exact command / probe | Working directory / environment | Purpose / ACs | Result and observed signal | Side effects / cleanup | Independence / gap |
|---|---|---|---|---|---|---|
| DISC-01 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | repo root, Linux host | V-01..V-03 owning state suite | 44 tests, `OK` (0.400s) | none | independent run of current bytes |
| DISC-02 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | repo root, Linux host | V-01..V-05 owning controller suite | 76 tests: 6 errors + 1 failure, all `UnsupportedSandbox: sandbox-exec verification is supported only on macOS` in `ControllerInspectionIntegrationTest` (pre-existing, documented in `preflight.md`; `verification_runner.py` out of scope). All runnable task tests pass | none | environmental gap only; macOS-host pass (76/76) is implementer-submitted evidence |
| DISC-03 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py` | repo root, Linux host | F-02 sibling-suite corroboration | 13 tests, `OK` (0.346s) | none | independent confirmation the F-02 correction is on current bytes |
| DISC-04 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_rejected_controller_update_leaves_persisted_bytes_unchanged skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_frozen_authority_survives_source_edits` | repo root, Linux host | MNT-01 reviewer regression | 2 tests, `OK` (0.071s) | none | exact maintainability-01 reproducer on current bytes |
| DISC-05 | `/tmp/opencode/t0021-d2-probe.py` (70 fresh adversarial probes: public CLI init/run-next/revise-flow/inspect subprocesses plus validator-level boundary cases; three probe-script bugs found and fixed, re-run clean — no production bytes touched) | disposable `tempfile` under `/tmp/opencode`, run dirs outside repo; read-only w.r.t. real repository | independent corroboration of V-01..V-04, R1, R2, terminal coherence, type strictness | 70/70 probes pass (frozen identity and digest refusals, weakened-authority refusals without publication, occupancy boundaries, correction budget incl. environment repair, old-run refusals with unchanged bytes, actor-result and terminal-state refusals) | `shutil.rmtree` of the disposable root; repository `git status` identical after all probes | independent; a fresh script, not a copy of prior or implementer probes |
| DISC-06 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | repo root, Linux host | aggregate-gate decision (brief assigns to fresh discovery) | 187 tests: 7 failures + 7 errors + 14 skipped. 13 environmental (macOS-only sandbox-exec: 7 in `ControllerInspectionIntegrationTest`, 6 in `VerificationSandboxFailClosedTests`; pre-existing, out-of-scope files untouched by this diff), 1 pre-existing retrieval-surface docs drift. No task-induced failure; F-02 absent | none; no surviving fixture processes (checked) | run by discovery, not implementer; environmental baseline from `preflight.md` |
| DISC-07 | `git diff --check`; `ps` scan for controller/codex/fake-codex processes; pre/post `git status --porcelain` diff | repo root | hygiene | diff-check clean; zero fixture processes; status identical before and after all probes | none | — |

Required-but-unrun: none beyond the two blocked rows (V-02a runtime inspection on this host; V-03s schema validator on this host), each with a concrete non-gate blocker and owner in section 8.

## 6. Aggregate-gate decision

| Field | Value |
|---|---|
| Gate / exact command | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` |
| Status | `failed` — 13 environmental (macOS-only sandbox-exec, pre-existing/out-of-scope), 1 pre-existing retrieval drift (F-01). No task-induced failure |
| Owner and stage | discovery-02 (this pass), as the brief assigns the aggregate decision to fresh discovery |
| Reason | Fresh correction discovery: targeted evidence was clean before the gate (DISC-01..DISC-05, 70/70 probes), the prior gate failure F-02 had a focused correction corroborated by its sibling suite, and the two blocked rows have concrete non-gate blockers (no Draft 2020-12 validator; macOS-only sandbox). The gate confirms F-02 is resolved at aggregate level and no new task-induced failure exists |
| Current evidence | DISC-01..DISC-07 |

## 7. Scope and baseline comparison

| Item | Recorded baseline | Current reviewed state | Classification / evidence |
|---|---|---|---|
| `HEAD` | `4449a3f373af9fabdcfe0c4d4b661988c4640c7f` (preflight, implementation report) | `4449a3f373af9fabdcfe0c4d4b661988c4640c7f` | expected, unchanged |
| Exact `git status --short` | 28 staged + 3 untracked `.DS_Store` at review start (`/tmp/opencode/t0021-d2-status-before.txt`) | identical before and after all probes; the only addition from this review is this report file | task/packet state preserved; no user state touched |
| Dirty path index/worktree identities | — | worktree == index for all reviewed paths (`git diff` unstaged: empty); no unstaged drift | clean separability |
| Task-owned paths | brief allows `scripts/controller.py`, `scripts/controller_state.py`, `assets/` schemas/examples, their focused tests, package report/contract | staged diff covers exactly those paths plus `tests/test_controller_git.py` (the F-02 sibling-fixture correction, authorized by the user's explicit request recorded in the implementation report) | in scope; the F-02 path sits outside the brief's named test files and was authorized separately — the acceptance call weighs that authorization |
| Durable package artifacts | brief/verification revision 1, preflight, implementation-report, contract, maintainability reviews, discovery-01 | all present and consistent; superseded `implementation-handoff.md` kept as history; discovery-01 remains the historical first pass | canonical |
| Staged non-task entries | `M AGENTS.md` (one-line governance deletion), planning packages (`docs/tasks/T-002*`, `T-002.2`, `T-002.3`, `index.json`), 3 `.DS_Store` | still staged/untracked as at review start | pre-existing user/planning work, not attributed to this implementation (consistent with maintainability-01/02 and discovery-01); not reviewed as task bytes |
| Pre-existing aggregate failures | `preflight.md` recorded 6 environmental failures in `test_controller.py` on Linux | aggregate shows 13 environmental (controller inspection 7 + verification_runner 6) plus the retrieval-surface docs drift (F-01) | pre-existing at HEAD; `test_retrieval_surface.py` and `test_verification_runner.py` are untouched by this diff; not caused by these reviewed bytes |

Post-report state: `git status --short` after this write adds exactly `?? skills/task-orchestrator/docs/tasks/T-002.1/reviews/discovery-02.md`; no other change (verified in section 1).

## 8. Questions, unchecked work, and residual risks

| Type / row ID | Evidence or reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| blocked | V-02a runtime inspection non-acceptance cannot execute on this Linux host (`sandbox-exec` macOS-only in out-of-scope `verification_runner.py`); static decision-path confirmation only; implementer's macOS 76/76 is submitted evidence | no | macOS-capable verification owner, or acceptance call may weigh the static evidence |
| blocked | V-03s Draft 2020-12 schema-validator boundary cannot execute on this Linux host (no `jsonschema`, no pip cache, no global Node validator; network install forbidden by the brief); implementer's macOS schema script is submitted-only | no | evidence owner on a host with `jsonschema`, or acceptance call may treat schema text + runtime/example agreement as the available evidence |
| residual risk | Per-run digests are self-consistent; a writer with run-dir write access could recompute ledger digests coherently. The task claims source-input-edit protection (confirmed), not an independently anchored tamper barrier; no finding | no | successor work (evidence admission / T-002.3) |
| residual risk | Documented byte-binding asymmetry: `inputs.json` and flow bytes are bound exactly (byte-level digests, newline-sensitive), while policy and manifest digests bind canonical JSON (newline-insensitive, semantic). The contract states this distinction; behavior matches it. Successors must not assume byte-level binding for policy/manifest | no | T-002.2/T-003 owners |
| residual risk | Parallel-authority stage/role policy (runtime constants, 4 schemas, 4 examples, contract note) must be synchronized deliberately by successors (carried from maintainability-01/02) | no | T-002.2/T-003 owners |
| residual risk | `stage_transport_fixture` in `test_controller.py` and the F-02 fixture seed mutate persisted ledger bytes to bypass not-yet-implemented ready/preflight admission; must migrate to the real path when T-002.2 lands admission | no | T-002.2 implementation |
| pre-existing | Retrieval-surface docs-drift failure at HEAD (planning docs added without updating the test's 4-entry expectation) | no | planning-work owner; outside this task's scope |

## 9. Coverage completeness and next route

| Field | Value |
|---|---|
| Coverage completeness | `complete` for all authority rows on this host with the two bounded blockers above (V-02a runtime, V-03s schema validator); no omitted material row; no hidden green behind refusals; prior finding F-02 resolved on current bytes |
| Basis | Ledger rows V-01..V-05 (+ V-02a, V-03s, MNT-01, F-02), no findings against the reviewed bytes, probes DISC-01..DISC-07, aggregate gate record |
| Next owner | separate acceptance decision call (fresh `task-acceptance-review`) |
| Exact next action | Hand the brief, scoped diff, this report, prior finding F-02 (resolved), blocked rows V-02a/V-03s, and the packaged preparation references (verification revision 1, preflight, maintainability reviews, discovery-01) to a fresh acceptance decision call |

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: 2; HEAD 4449a3f373af9fabdcfe0c4d4b661988c4640c7f; 28 staged + 3 untracked .DS_Store; worktree == index for reviewed paths
- Coverage rows: V-01=pass; V-02=pass; V-02a=blocked (Linux lacks macOS sandbox-exec; static decision-path confirmation; macOS suite evidence submitted-only); V-03=pass (runtime); V-03s=blocked (no Draft 2020-12 validator on this host; implementer macOS schema script submitted-only); V-04=pass; V-05=pass (static); MNT-01=pass (reproducer pair OK); F-02=resolved (sibling suite 13/13 OK; aggregate shows no task-induced failure)
- Finding IDs: none against the reviewed bytes (no invented defect; F-02 resolved, F-01 pre-existing retrieval drift remains outside findings)
- Finding/scenario continuity: MNT-01 (maintainability-01 CHANGES_REQUESTED -> maintainability-02 ACCEPT) remains resolved on current bytes; F-02 (discovery-01 suggested P2) resolved by the authorized test_controller_git.py fixture correction; V-02a/V-03s keep concrete non-gate blockers with owners above
- Preparation/context: brief.md rev 1; verification.md rev 1; preflight.md; implementation-report.md (MNT-01 + F-02 corrections); controller-contract.md; reviews/maintainability-01.md, maintainability-02.md, discovery-01.md
- Reviewer regressions: exact maintainability-01 reproducer pair (DISC-04): PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_rejected_controller_update_leaves_persisted_bytes_unchanged skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_frozen_authority_survives_source_edits -> OK
- Aggregate gate: failed (environmental + pre-existing only), run by discovery-02 (DISC-06): PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py' -> 187 tests, 13 environmental sandbox-exec + 1 pre-existing retrieval drift, no task-induced failure
- Next: separate fresh task-acceptance-review consuming this report, with blocked rows V-02a/V-03s and the F-02 authorization weighed there
```
