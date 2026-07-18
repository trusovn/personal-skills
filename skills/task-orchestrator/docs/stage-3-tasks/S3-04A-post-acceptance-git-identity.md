# Task Brief: `S3-04A` — Validate post-acceptance Git identity before repeated selection

## Identity and artifact status

| Field | Value |
|---|---|
| Task ID | `S3-04A` |
| Artifact status | `ready_for_preflight` |
| Producing stage | `task-brief-designer` |
| Created at | `2026-07-17T13:12:59+01:00` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Primary authority | `skills/task-orchestrator/docs/stage-3-tasks/S3-04-acceptance-report.md#1-findings-ordered-p0-through-p3`, third P1 finding, together with `skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md#Legacy-assumption-sweep` and `skills/task-orchestrator/docs/stage-3-plan.md#Settled-decisions-and-constraints` |
| Dependencies | `S3-04` reviewed checkpoint plus its first two P1 corrections — present in the staged index and current unstaged worktree; fresh preflight must fingerprint both views |

## Outcome

A repeated public `run-next` accepts the exact controller-observed Git state of
the most recently accepted task, rejects any later repository drift unchanged,
and launches the next persisted ready task without weakening the initial-run
guard or adding a new evidence field.

## Authoritative inputs and knowledge ledger

| Kind | Path or statement | Relevance |
|---|---|---|
| Authoritative input | Repository `AGENTS.md` instructions supplied for this workspace in the continuation request | Requires explicit assumptions, surgical scope, progressive verification, and preservation of the staged checkpoint and user work. |
| Authoritative input | `/private/tmp/task-orchestrator-preflight/S3-04/correction-handoff.md` | Records the accepted correction state, the unresolved identity contract, verified commands, and explicit prohibitions. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-tasks/S3-04-acceptance-report.md`, third P1 finding and AC-06 row | Requires a real post-acceptance second occurrence and the minimum compatibility change against existing controller-owned accepted evidence. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md`, AC-06, legacy-assumption, risk, and stop sections | Requires repeated public selection without bypassing Git drift checks and routes this contract through brief design. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-plan.md#Settled-decisions-and-constraints` and `#Architecture-assessment-after-S3-01-through-S3-03` | Keeps explicit no-auto-launch acceptance, controller-owned evidence, `controller_git.py` Git observations, and `controller.py` CLI/use-case ownership. |
| Authoritative input | `skills/task-orchestrator/docs/controller-contract.md#Closure-gate` | Existing accepted evidence is controller-observed; pre-existing dirty paths must remain exact and accepted changes must remain within task allowance. |
| Confirmed fact | The current initial-baseline comparison rejects ordinary accepted output before `select_task()`. | Acceptance REV-06 and `skills/task-orchestrator/scripts/controller.py::_cli_run_next`. |
| Confirmed fact | Existing task baselines contain exact HEAD, index tree, and content-hashed canonical status entries; closure evidence contains exact allowed-path binary patch bytes and digests plus HEAD/index and scope observations. | `skills/task-orchestrator/scripts/controller_git.py::capture_task_baseline` and `::capture_closure_evidence`. |
| Confirmed fact | An accepted closure cannot authorize modification or disappearance of a pre-existing dirty path; clean allowed-path output is represented by the exact task patch. | Controller closure gate and current `capture_closure_evidence` observations. |
| Frozen decision | The run-initial HEAD/status/digest guard remains the oracle before any task is accepted. | S3-04 safety contract and continuation prohibition against weakening drift detection. |
| Frozen decision | After acceptance, the trusted comparison source is the latest accepted task's existing controller-owned task baseline and closure evidence, not path membership, current allowed paths alone, worker claims, or a newly added ledger/evidence field. | Acceptance corrective direction plus the user's route and prohibitions. |
| Frozen decision | The accepted-work oracle must bind exact current HEAD, index tree, pre-existing status entries/content hashes, allowed-path patch bytes, and the closure evidence/artifact digests needed to prove those values were the observed accepted state. | Existing Stage 2 evidence contract; this is the minimum exact comparison supported without new fields. |
| Frozen decision | Missing, malformed, mismatched, stale, or tampered accepted evidence fails closed before adapter preflight or durable mutation; there is no fallback to the initial baseline or path-only acceptance once any task is accepted. | Controller authority and drift-safety contracts. |
| Assumption | Existing closure and task-baseline fields are sufficient to reconstruct and compare the exact accepted workspace for every currently accepted S3-04 scenario, including pre-existing dirty paths and allowed untracked files. | Fresh preflight must prove the field coverage and identify the exact read-only helper interface; block if any accepted scenario lacks an exact oracle. |
| Assumption | The existing temporary-Git and fake-worker fixtures can express the two-task public occurrence and same-path content drift without shared infrastructure. | Fresh preflight must confirm exact fixture locations and selectors. |
| Unresolved item | None at design time. If preflight proves the existing evidence is not cryptographically/structurally sufficient, it must return `blocked` rather than authorize a new field or later-record validator. | `task-preflight` owns current executability. |

## Scope and boundaries

| Item | Contract |
|---|---|
| Allowed paths | `skills/task-orchestrator/scripts/controller_git.py` for one read-only exact accepted-workspace comparison; `skills/task-orchestrator/scripts/controller.py` only to select the initial versus post-acceptance guard and call that comparison before preflight/selection/mutation; `skills/task-orchestrator/tests/test_controller_git.py`; `skills/task-orchestrator/tests/test_controller.py`; `skills/task-orchestrator/docs/stage-3-tasks/S3-04-result.md`; `/private/tmp/task-orchestrator-preflight/S3-04/worker-result.json` |
| Read-only context | This brief; original S3-04 brief, acceptance report, handoff, ready packet, Stage 3 plan, controller contract, current staged checkpoint, and current unstaged corrections |
| Prohibited work | New ledger, baseline, closure, decision, operation, or evidence fields; path-only or status-shape drift acceptance; weakening/removing the initial-baseline guard; S3-05/S3-08/S3-11/S3-12 record validation; new CLI commands; acceptance/finalization implementation; broad Git redesign; shared helpers or infrastructure; acceptance-report edits |
| Mutation limits | Standard-library-only; no network, dependency install, live model, server, destructive Git, unstage/reset/commit/push, tracker mutation, `.gitignore` edit, or unrelated cleanup |
| Pre-existing user work | Preserve exactly. The index is the user-staged reviewed S3-04 checkpoint. Current unstaged corrections in `controller.py`, `controller_state.py`, `test_controller_state.py`, and `S3-04-result.md` are task-owned continuation work and must remain unstaged. `.gitignore` is user-owned and byte-invariant. |

## Entry criteria and dependencies

| Criterion | Required evidence | Current claim |
|---|---|---|
| Reviewed checkpoint and first two corrections remain byte-identical | Separate index/worktree digests for every current status entry plus the handoff's ownership statement | preflight must confirm |
| Existing accepted evidence is sufficient for an exact read-only oracle | Field-by-field trace from task baseline and closure packet/artifacts to current HEAD, index, status, and allowed-path patch | preflight must confirm; otherwise block |
| Initial and public fake-worker flows remain executable | Existing focused controller Git and controller test commands | preflight must confirm |
| No forbidden path overlap | Exact Git status and separate index/worktree fingerprints | preflight must confirm |

## Work and acceptance criteria

Required work:

1. Add the smallest read-only Git helper that validates an accepted task's
   current workspace against its existing task baseline, closure packet, and
   evidence artifacts, including exact artifact/evidence digests.
2. Keep the initial-run baseline guard unchanged. When persisted state shows a
   prior accepted task, make `run-next` validate the latest accepted evidence
   before adapter preflight, selection, task-baseline creation, or mutation.
3. Add task-local exact-identity and real two-task public regressions, then
   update the existing S3-04 result and worker result truthfully.

- **AC-01:** With no accepted task, `run-next` retains the exact current
  run-initial HEAD/status/baseline-digest guard and its existing denial behavior.
- **AC-02:** With T1 accepted, its ordinary allowed tracked or untracked output
  unchanged, and dependent T2 persisted `ready`, the second public `run-next`
  validates exact accepted evidence and launches only T2.
- **AC-03:** Any post-acceptance change to HEAD, index, accepted allowed-path
  bytes, pre-existing dirty bytes/presence, path set, or evidence/artifact bytes
  rejects before worker preflight, attempt/baseline creation, or ledger mutation.
- **AC-04:** Missing, malformed, identity-mismatched, or digest-mismatched task
  baseline/closure evidence rejects without falling back to path membership,
  initial baseline, worker claims, or later Stage 3 records.
- **AC-05:** The implementation adds no persisted field, does not mutate
  evidence while validating it, and preserves the staged checkpoint, existing
  unstaged corrections, acceptance report, and `.gitignore`.

## AC execution matrix

| AC | Production invariant | Positive evidence | Negative evidence | Real entry-point path | Repeated or recovery path | Real boundary crossed | Verification dependency |
|---|---|---|---|---|---|---|---|
| AC-01 | Initial selection remains protected by the original exact baseline. | Existing clean initial fake `run-next` passes. | Existing initial HEAD/status/baseline tamper cases reject unchanged. | Public `controller.py run-next`. | First occurrence only; no accepted task exists. | Temporary Git repository, run directory, and local fake process. | Believed-existing controller integration cases. |
| AC-02 | Exact accepted output becomes the next task's legitimate starting state. | Initialize two tasks, run T1, persist a valid acceptance using its real closure evidence, leave accepted bytes unchanged, then invoke public `run-next`; assert T2 attempt/baseline/selection and no T1 relaunch. | A ready T2 with no valid accepted-evidence chain rejects. | Two public `run-next` invocations with the accepted ledger transition between them. | First worker occurrence, legitimate acceptance state change, then second occurrence. | Real Git/filesystem/process/CLI boundary. | Task-local extension of existing fake-worker fixture; no shared harness. |
| AC-03 | Byte-level drift after acceptance cannot launch more work. | Exact accepted state comparison passes before T2. | Independently vary same-path/same-size allowed content, pre-existing dirty content/presence, HEAD, index, untracked path set, and closure artifact bytes; assert exact ledger/run-directory bytes and no adapter invocation. | Public `run-next` plus focused Git helper. | Accepted state, external drift, next occurrence denial. | Real Git index/worktree and immutable run artifacts. | Temporary-Git focused cases plus public denial case. |
| AC-04 | Accepted authority is complete and identity-bound. | Matching run/task/attempt/baseline/closure/artifact identities validate. | Missing field/file, traversal or wrong family where applicable, identity mismatch, and recomputed-content/digest mismatch reject unchanged. | Read-only Git helper called by public `run-next`. | Re-read exact evidence succeeds; altered replay fails. | JSON/file bytes and digest boundary. | Existing canonical JSON/digest helpers and task-local fixtures. |
| AC-05 | Correction remains surgical and status-neutral outside authorized work. | Separate index/worktree fingerprints match before and after implementation except declared unstaged allowed paths. | Any staged-index, report, `.gitignore`, persisted-schema, or later-record change fails scope review. | Git status/diff inspection and JSON/AST hygiene. | N/A — repository preservation invariant, not a lifecycle occurrence. | Git index/worktree boundary. | Existing local Git and parse commands. |

## Legacy-assumption sweep

| Entry point or area | Search term / trace | Risk being tested | Required follow-through |
|---|---|---|---|
| `scripts/controller.py::_cli_run_next` | `initial_baseline`, `since initialization`, guard ordering before `preflight_codex` and `select_task` | Initial-only authority rejects legitimate accepted output or a post-acceptance branch bypasses early denial. | Preserve the initial branch byte-for-byte where feasible; place accepted validation before every side effect. |
| `scripts/controller_git.py` evidence capture | `capture_task_baseline`, `capture_git_status`, `task_patch`, `evidence_digest`, `evidence_artifacts` | A comparison that checks paths/status but not content or trusts unanchored artifact claims can miss later drift. | Trace every accepted-state byte to an existing baseline/closure field and independently recompute all required digests. |
| Accepted task/attempt selection | `accepted`, `last_closure_path`, `selected_task_baseline_ref`, `attempt_ids` | The wrong historical task/attempt could authorize T2 or ambiguous history could be guessed. | Derive one exact latest accepted identity from persisted ledger/history and require every referenced record to match; ambiguity rejects. |
| Public denial ordering | `preflight_codex`, baseline writes, `create_attempt`, `update_ledger` | Detection after an external process or durable write leaves partial state. | Tests spy on preflight and compare run-directory/ledger contents before and after denial. |

## Risk-to-evidence map

| Risk | Impact / escalation trigger | Evidence level and boundary | Scenario and oracle | Residual gap |
|---|---|---|---|---|
| Existing closure evidence cannot reconstruct exact accepted state | Drift could be accepted or valid work permanently blocked; stop before implementation. | Preflight field trace plus focused real-Git fault cases. | Compare same-path/same-size content, index, HEAD, untracked, and pre-existing dirty variants against independently captured expected bytes. | None permitted; missing coverage blocks rather than adding fields. |
| Tampered controller evidence authorizes work | Cross-task or externally rewritten evidence launches T2. | Module plus public integration at file/digest boundary. | Alter each identity/artifact link and assert early rejection/no mutation. | Later cryptographic identity chain remains S3-05/S3-08; this slice uses only already-authorized existing evidence. |
| Initial guard is accidentally relaxed | A dirty initial run launches work. | Existing public regression plus scoped diff inspection. | Rerun initial drift denials and inspect branch selection. | None. |
| Dirty checkpoint is overwritten or staged state changes | Reviewed evidence and correction separation are lost. | Pre/post separate index/worktree SHA-256 inventory. | Compare every status entry and prohibited artifact. | None. |

## Verification-capability inventory

| Needed capability | Disposition | Owner / path | Preflight confirmation |
|---|---|---|---|
| Exact temporary-Git status/patch/index fault fixture | believed existing, extended task-locally | `skills/task-orchestrator/tests/test_controller_git.py` | Confirm helper interfaces cover same-size bytes, staged state, untracked files, and pre-existing dirty paths. |
| Two-task public fake-worker flow | believed existing, extended task-locally | `skills/task-orchestrator/tests/test_controller.py` | Confirm closest init/run-next helper, deterministic fake adapter, and a selector that proves no invocation on denial. |
| Canonical JSON and SHA-256 helpers | believed existing | `skills/task-orchestrator/scripts/controller_state.py` imports used by `controller_git.py` | Confirm exact callable names without changing the state module. |
| Shared harness or new persisted schema | not required and prohibited | N/A | Block if existing task-local fixtures/evidence are insufficient. |

## Verification command candidates

| Class | Candidate command | Working directory | Evidence | Preflight must resolve |
|---|---|---|---|---|
| Fail-first | Exact new two-task post-acceptance public test selector under `skills/task-orchestrator/tests/test_controller.py` | Repository root | Current initial-only guard rejects the legitimate second occurrence for AC-02. | Resolve final test class/method name and confirm assertion-specific failure before production edit. |
| Targeted | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py` | Repository root | AC-03/04 exact Git and artifact comparisons. | Confirm baseline collection and runtime. |
| Targeted | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | Repository root | AC-01 through AC-04 public integration and denial ordering. | Confirm baseline collection and runtime. |
| Regression | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | Repository root | Preserves the already-corrected P1 transition/revision contracts. | Confirm current 18-test baseline. |
| Broader | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | Repository root | Task-orchestrator transitive regression coverage. | Run only after targeted gates pass. |
| Hygiene | Packet-resolved AST parse, JSON parse, `git diff --check`, exact status/digest comparison | Repository root | AC-05 syntax, assets, whitespace, and preservation. | Resolve exact changed-path list and separate index/worktree digest command. |

These are design candidates, not claims that a command exists or passes.

## Effort, budget, and escalation

| Item | Proposal |
|---|---|
| Implementation | `strong` agent; `high` reasoning — the code change should be small, but its identity oracle and early-denial boundary are safety-critical. |
| Review | `immediate` — repeat exact accepted-output success and independent same-path drift/tamper denials before accepting AC-06. |
| Budget checkpoint | At 20 additional tool calls or 60 minutes after a ready packet, reassess; ask before any slow/flaky/live/privileged expansion. |
| Two-strike rule | After two materially different fixes leave the same targeted behavior failing, stop and report evidence, discarded hypotheses, owning contract, and next route. |
| Escalation triggers | Existing evidence cannot bind exact bytes; validation requires a new field or later record; accepted-history identity is ambiguous; a shared helper/schema/wider path is required; initial drift protection would change; staged/index/report/`.gitignore` preservation cannot be proved. |

## Stop conditions and routing

- Stop before edits if preflight cannot prove an exact oracle from existing
  baseline/closure evidence or cannot attribute every dirty index/worktree view.
- Stop if the minimum fix requires a new evidence field, later-record validator,
  path-only allowance, initial-guard weakening, shared infrastructure, or a
  change outside the allowed paths.
- Route missing/ambiguous authority back to `task-brief-designer` or the user.
- Route stale state, invalid commands, missing helpers, dirty overlap, or an
  incomplete existing-evidence oracle to `task-preflight` with `blocked` status.
- Stop after this AC-06 correction; do not implement S3-05 or later acceptance,
  identity-chain, inspection, finalization, recovery, commit, or tracker work.

## Implementation handoff requirements

The implementer must receive a fresh `ready` packet derived from this exact
brief. It must re-fingerprint the staged checkpoint and every unstaged path,
establish the public two-task fail-first regression before production edits,
add the smallest read-only exact comparison, run packet commands progressively,
leave all corrections unstaged, and update the existing worker result only
after AC-01 through AC-05 pass. It must not approve its own work.

## Review handoff requirements

Independent review must receive this brief, its exact fresh packet, the updated
worker result, original S3-04 brief/result, unchanged acceptance report, and the
separate staged/unstaged diff. It must independently reproduce the public
second occurrence and at least one same-path content substitution plus one
evidence-tamper denial, verify no initial-baseline or path-only weakening, and
return a new acceptance verdict without editing reviewed files.

## Handoff summary

Run `task-preflight` on
`skills/task-orchestrator/docs/stage-3-tasks/S3-04A-post-acceptance-git-identity.md`
and write a fresh packet under
`/private/tmp/task-orchestrator-preflight/S3-04A/`; implement only if it is
`ready`.
