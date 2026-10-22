# Task Review Discovery Report: `T-001` — Local runtime support

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery` |
| Coverage completeness | `partial — codex CLI observations (E1/E2/E6) cannot be re-executed on this review host (Linux aarch64; no codex binary); all other rows independently corroborated` |
| Discovery iteration | first discovery pass |
| Created at | 2026-10-22T18:04:09Z |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report path | `skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-01.md` |
| Task brief | `skills/task-orchestrator/docs/tasks/T-001/brief.md` (SHA-256 `3eaa6df3…462c2`, matches recorded revision) |
| Verification design / task context | `…/T-001/verification.md` revision 1; `…/T-001/preflight.md`; `…/T-001/harness-contract.md` (ART-008) |
| Current submission | `harness-contract.md` v1.0, `READY_FOR_REVIEW`, runtime qualification `BLOCKED` |

This report publishes evidence only. It contains no acceptance verdict, no
approved deferral, and no advancement. The separate acceptance decision call
consumes it. It applies only to the reviewed bytes and artifacts identified
below; any correction requires a new discovery report. This report does not
review or authenticate itself.

## 1. Discovery provenance

| Question | Evidence |
|---|---|
| Did this session author any reviewed production bytes? | `no — independent`. This session wrote nothing before this report; the reviewed task package was produced by prior sessions. |
| Independent evidence authority | `yes` |
| Current byte identity | `HEAD 8efffca9e38855e8229764851d570a72aa7a857b`; reviewed diff is untracked `skills/task-orchestrator/docs/tasks/` (see §7). |

## 2. Findings, ordered by suggested severity P0 through P3

No findings.

Every claim in `harness-contract.md` that this environment could independently
reach was corroborated. The report's honest dispositions (unverified permission
enforcement, unsupported idempotent launch, unsupported notifier, blocked
qualification) match the source and the verification design's negative-claim
requirements. Blocked rows below are review-environment limits, not defects.

## 3. Completeness ledger

| Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| V-01 | AC-01: callable, versioned bridge; one selection | interactive tools vs Python-callable API; version; smallest bridge | local executable output + source | E1/E2/E6 + source; selection = Codex CLI 0.163.0 via subprocess | Re-ran source checks: `codex_worker.py` exposes `start/resume/run_turn/process_liveness/terminate_process_group`; operator guide lists `init/run-next/inspect/revise-flow`; `controller_git.py` is inspection-only. CLI re-run: `command -v codex` → 127; `/opt/homebrew/bin/codex` absent (review host is Linux aarch64). | `blocked` for the CLI-observation component — codex binary unavailable on this review host; source-level corroboration passed. |
| V-02 / R1 | AC-02: identity, duplicate handling, missing-receipt recovery | first launch; same key; live/terminal/unknown; spawn without receipt; replacement coordinator | real subprocess/files wrapper + source trace | E3/E4 + source trace | Re-ran `python3 -m unittest …test_codex_worker.py -k test_start_persists_thread_and_structured_result` → 1 test OK. Re-ran full module → 15 tests OK. Source trace: `starting` persisted before Popen; PID recorded after spawn; crash window between spawn and PID persistence is real (`codex_worker.py:244-254`); `start` rejects existing state path (line 352); `resume` rejects live/ambiguous PID (lines 431-439). Report marks duplicate launch unsupported and spawn-without-receipt unknown. | `pass` — report matches source; unknown/unsupported cases are honestly blocked, not claimed supported. |
| V-03 / R2 | AC-03: actual permission enforcement, frozen policy | allowed write; denied reviewer write; denied run/controller/skill writes; 0.5 reuse threshold | real boundary observation; source/configuration labeled separately | E1/E2/E6 + policy source; denial marked unverified | Source: `ACTOR_LEVELS` = gpt-5.6-sol × {low, medium, high} (`controller_state.py:19-23`); `IMPLEMENTATION_SESSION_REUSE_THRESHOLD = 0.5` (line 24); schema `implementation_session_reuse_threshold: {"const": 0.5}` (`flow-profile.schema.json:86`); correction default limit 2 vs direction's three-cycle rule (`direction-local-harness.md:29,56`); no context-occupancy measurement exists in any inspected script. Report labels flags/argv as configuration, never as enforcement, and names the capability owner for the missing allow/deny proof. | `pass` (report honesty and policy facts); the underlying allow/deny capability itself remains `unverified` with owner — recorded as residual, not a report defect. |
| V-04 / R3 | AC-04: safe task-scoped commit; no owner-work loss; no duplicate publication | accepted path + unrelated staged/unstaged; interruption before/after publication; stale CAS | disposable Git repo; byte-identity assertions | E5 | Re-ran `PYTHONDONTWRITEBYTECODE=1 python3 …/T-001/probe_local.py` → exit 0; JSON confirms `exact_paths`, `owner_index_bytes_preserved`, `all_worktree_bytes_preserved`, `pre_publish_head_unchanged`, `post_publish_reconciled`, `stale_update_ref_refused`, `commit_count: 2`; limits list matches report. `controller_git.py` confirmed inspection-only (no commit-tree/update-ref). No surviving `t001-git-*` temp dirs. | `pass` |
| V-05 / R3 | AC-04: notification support with observable delivery; no invented success | delivered / failed / unknown | documented channel boundary; no real message authorized | source/docs | Grep of `scripts/**/*.py` for `notify|notifier|notify_intervention` → no matches; report marks controller notifier unsupported and delivery unverified with smallest owner action. | `pass` (honest unsupported disposition) |
| V-06 | AC-05: every capability dispositioned; Q-001/Q-002 and T-002..006 effects | supported / unsupported / unverified | report-to-source trace | disposition table + Q-001/Q-002 | Disposition table covers all ACs and R1..R3; Q-001 partially resolved/blocking, Q-002 unresolved; consumer effects per successor task stated; no dependent release claimed. | `pass` |
| R1-trace | R1: duplicate and missing-receipt recovery traced from documented observations | duplicate key; missing receipt | source facts, not actor claims | report rows "Same operation repeated", "Spawn without receipt" | Source confirms: no idempotent launch service exists; `start` path-existence refusal is not an idempotency guarantee; crash window between Popen and PID persistence is real. Report traces both cases without claiming support. | `pass` |
| R2-level | R2: denial evidence used the real selected boundary | allowed vs denied writes | actual boundary observation | report labels evidence level per claim | Report consistently separates `observed`/`source`/`documented`/`proposed` and marks permission enforcement unverified; no argv/prompt evidence presented as denial proof. | `pass` |
| R3-assume | R3: commit and delivery assumptions inspected | interruption before/after; delivery failure visibility | disposable Git + channel boundary | E5 + source | Probe assertions re-run; crash/fsync limits explicitly recorded; delivery failure stays visible in proposed `status` contract; no false success path claimed. | `pass` |

## 4. Adversarial state and evidence checks

| Ledger row / invariant | Cases exercised | Result and evidence |
|---|---|---|
| Persisted type strictness | boolean/int confusion at threshold and limit fields | `correction.limit` type-checked as int (`controller_state.py:157`); schema pins threshold via `const: 0.5`. No confusion observed. |
| Coherent tampering | digest stored with mutable evidence | Out of scope: report claims no authentication of receipts; it states receipts are "not authenticated or power-loss-durable". No stronger claim to falsify. |
| Parent/child terminal coherence | stopped parent retaining running child | Wrapper terminates the process group on timeout/SIGTERM (`codex_worker.py:277`; tests 249/278 pass). Report does not claim exactly-once terminality. |
| Exact cardinality | zero/one/two owners of a run | `start` refuses when a run dir exists (one); no controller-level reservation exists (zero/duplicate protection absent) — report marks this unsupported. Consistent. |
| Selected vs non-selected coherence | accepted task path vs unrelated owner paths | E5 asserts real index bytes and all worktree bytes preserved; re-run confirmed. Mixed task-path staging noted as unproved and refused. |

## 5. Independent probes and command results

| ID | Exact command / probe | Working directory / environment | Purpose / ACs | Result and observed signal | Side effects / cleanup | Independence / gap |
|---|---|---|---|---|---|---|
| DISC-01 | `command -v codex; codex --version` | repo root, Linux aarch64 review host | E1 re-run / AC-01 | `command not found`, exit 127 | none | Blocked: implementer observed macOS `/opt/homebrew/bin/codex` 0.163.0; this host has no codex. Not independently re-observable here. |
| DISC-02 | `shasum -a 256 skills/task-orchestrator/docs/tasks/T-001/brief.md` | repo root | brief revision freshness | `3eaa6df3972c254764c1b92992a52dfdbc832f637abb8c89826ea56a994462c2` — matches verification.md and preflight.md recorded revision | none | pass |
| DISC-03 | `shasum -a 256 …/local-harness-orchestration-plan.md …/local-harness-task-map.json` | repo root | authority freshness | `98fab11e…52fd`, `7e6a0a37…ad440` — match `project-plan-review.md:8-9` and `harness-contract.md:36-38` | none | pass |
| DISC-04 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py -k test_start_persists_thread_and_structured_result` | repo root | E3 / AC-02 | 1 test OK | none (bytecode suppressed; fixtures disposable) | pass |
| DISC-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py` | repo root | E4 / AC-02 | 15 tests OK (0.803s in this env vs 4.474s claimed; count matches) | none | pass |
| DISC-06 | `PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_local.py` | repo root | E5 / AC-04, R3 | exit 0; all assertions true; limits listed match report | temp repo removed (`TemporaryDirectory`); `/tmp` shows no surviving `t001-git-*` | pass |
| DISC-07 | Source greps: `ACTOR_LEVELS`, threshold, schema const, worker internals, operator guide, controller_git, notifier search, context-occupancy search | repo root | AC-03/04/05, R2 | All match report claims (see §3 rows) | none | pass |
| DISC-08 | E2/E6 re-run (`codex … --help`, `codex sandbox --help`, `codex app-server --help`) | repo root | AC-01/03 | `not run` — codex binary unavailable on this review host | n/a | Next evidence owner: a discovery/acceptance pass on the macOS host with the observed binary, if re-observation is required. |

## 6. Aggregate-gate decision

| Field | Value |
|---|---|
| Gate / exact command | `not run as a broad suite — verification.md designates the fresh reviewer's ART-008 reconciliation as the aggregate gate for documentation-only work; no repeated full repository suite is authorized` |
| Status | `passed (reconciliation)` |
| Owner and stage | initial discovery, this fresh session |
| Reason | No decisive targeted failure; targeted evidence clean; brief and verification design exclude a full-suite gate for documentation-only work. |
| Current evidence | Ledger §3 rows V-01..V-06 and R1..R3 dispositions; probes DISC-01..08. |

## 7. Scope and baseline comparison

| Item | Recorded baseline | Current reviewed state | Classification / evidence |
|---|---|---|---|
| `HEAD` | `8efffca9e38855e8229764851d570a72aa7a857b` | `8efffca9e38855e8229764851d570a72aa7a857b` | expected — no tracked file modified; matches "production code and live run records stay unchanged" |
| Exact `git status --short` | `?? .DS_Store`, `?? docs/.DS_Store`, `?? skills/.DS_Store`, `?? skills/task-orchestrator/docs/tasks/` | identical at review start | `.DS_Store` entries: environment artifacts, outside task scope, not part of the reviewed diff. Task dir untracked as recorded. |
| Dirty path index/worktree identities | all reviewed paths untracked (no index entries) | unchanged | separability by filename; no index blob comparison applies |
| Task-owned paths | brief allows: `harness-contract.md` (ART-008) + minimal task-local evidence in the task package | `harness-contract.md`, `probe_local.py` (implementation); `verification.md`, `preflight.md` (packet derivation stages); `brief.md` (owner-authored before inspection, per preflight) | in scope; distinct files, no owner content overwritten |
| Durable package artifacts | brief/verification/preflight paths | observed paths present | canonical/current |
| Authority / policy / dependencies | plan/map hashes `98fab11e…`, `7e6a0a37…` | recomputed hashes match | unchanged; plan-review ACCEPT recorded hashes match (2026-10-22) |

Post-report `git status --short`: captured after writing this file — expected to add only
`skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-01.md` inside the already-untracked task directory.

## 8. Questions, unchecked work, and residual risks

| Type / row ID | Evidence or reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| blocked — V-01 CLI observation | E1/E2/E6 produced on macOS implementer host; codex absent on this Linux review host | no for report acceptance; the selection evidence remains environment-bound | acceptance decision may accept source-level corroboration or require a macOS-host re-observation pass |
| residual — permission allow/deny | no real boundary probe exists anywhere; report correctly marks unverified | yes for downstream runtime qualification | capability owner: bounded local allow/deny probes under effective actor policy |
| residual — exactly-once launch | unsupported as public service; crash window between Popen and PID persistence is real | yes for T-002/003 reservation/lock work | T-002/003 |
| residual — context reuse at 0.5 | no occupancy measurement source found in inspected scripts | yes for correction reuse | capability owner / owner policy decision |
| residual — notification delivery | no controller notifier exists; real delivery unverified | yes for intervention support | owner channel choice/test authorization, then T-003/006 |
| residual — commit finalization | disposable-Git primitives only; no fsync/crash/index-reconciliation qualification | yes for dependency release | T-005 |

Failed required behavior would be a finding; none was observed. The report
itself publishes these limitations under AC-05, which is the brief's required
honest disposition.

## 9. Coverage completeness and next route

| Field | Value |
|---|---|
| Coverage completeness | `partial — E1/E2/E6 CLI observations blocked by review-host environment; every other required/material row independently corroborated` |
| Basis | rows V-01..V-06, R1/R2/R3, probes DISC-01..08, source greps, hash checks |
| Next owner | separate `task-acceptance-review` decision call |
| Exact next action | hand this report, the brief, the scoped diff, blocked rows, and reviewer regression commands (DISC-04/05/06) to the acceptance decision call |

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: first discovery pass; HEAD 8efffca9e38855e8229764851d570a72aa7a857b; reviewed diff = untracked skills/task-orchestrator/docs/tasks/
- Coverage rows: V-01 = blocked (codex CLI not re-observable on this Linux review host; source-level pass); V-02/R1 = pass; V-03/R2 = pass (capability unverified with owner); V-04/R3 = pass; V-05/R3 = pass; V-06 = pass; R1-trace = pass; R2-level = pass; R3-assume = pass
- Finding IDs: none
- Finding/scenario continuity: no prior reviews; no findings; blocked rows owned by environment (V-01) and by named capability/T-task owners (residual rows §8)
- Preparation/context: brief.md (SHA-256 3eaa6df3…462c2), verification.md revision 1, preflight.md, harness-contract.md v1.0
- Reviewer regressions: DISC-04 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py -k test_start_persists_thread_and_structured_result`; DISC-05 full `test_codex_worker.py`; DISC-06 `PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_local.py`
- Aggregate gate: not run as broad suite (documentation-only task); reviewer ART-008 reconciliation passed with clean targeted evidence
- Next: separate task-acceptance-review decision call consuming this report, brief, scoped diff, blocked rows, and reviewer regression commands
```
