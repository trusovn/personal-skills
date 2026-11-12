# T-004.2 implementation report

Stage: READY_FOR_REVIEW. Profile: guided. Brief/verification revision: 1/1.
Implementation evidence, not independent review or task acceptance.

Collection now admits current independent controller-run reruns and explicit
requirements/behavior/code-quality coverage, gaps and findings. Failed checks
feed the inherited bounded correction route; terminal collection enables a
separate acceptance assignment without admitting acceptance or completion.

## Scope and authority

Changed runtime: `scripts/controller.py`, `scripts/controller_state.py`;
contract: `assets/actor-result.schema.json`; evidence:
`tests/test_actor_operations.py`; current instructions: `SKILL.md`; consolidated
T-005 handoff: [parent controller-contract](../T-004/controller-contract.md).
All paths are under `skills/task-orchestrator/`. New `preflight.md` belongs to the
preparation stage. Staged `verification.md` and the pre-existing untracked
.DS_Store files are preserved. No official plan, active installation, shared
runtime, installer, tracker or completion implementation changed. Source
orchestrator is outside the development-profile installer selection; no installer
synchronization is needed. Design and implementation reuse the existing actor,
producer, Git, command-runner and state fixtures.

Public addition: `check_collection(run_dir, assignment, *, timeout_seconds)` and
`check-collection`. One full frozen rerun belongs to the active collector and its
adapter-observed session, with a distinct `<collector>.rerun` execution identity,
exclusive intent/result and fresh logs. Existing ordinary `check_candidate`
execution/replay semantics remain intact. Only `observe_operation` →
`_admit_actor_outcome` → `_publish_actor_outcome` admits collection.

The prompt supplies frozen task/policy/candidate/check evidence, finding history,
project-local skill-resolution instructions and separate maintainability,
registry, discovery and acceptance roles. Capability attestations do not prove
review skill quality or runtime-enforced read-only behavior. Current structured
coverage is mechanical evidence admission; semantic ART-009 decisions remain
T-005 work. A collection observation never creates review_findings correction or
new deferral authority.

## Retained implementation evidence

All paths below are repository-relative under
`.quality/reports/T-004.2-implementation-20261112/` unless otherwise stated.
Raw logs are retained, including earlier failed controls and setup corrections.
No failure was discarded or reclassified as successful qualification.

| Evidence | Outcome / meaning |
|---|---|
| `actors-submission.log` | Final owning actor suite, 50 tests, all pass, no skips; covers the current submitted runtime/test bytes. |
| `state-final.log` | 45 state tests pass, no skips. State bytes remain unchanged since this check. |
| `architecture-current.log` | Canonical repository architecture gate: 4 pass, no skips; final runtime import scope unchanged. |
| `orchestrator-final.log` | Full orchestrator: 264 tests, 6 failures, 7 errors, 20 skips. Failing cases all reach unsupported legacy macOS sandbox behavior on Linux. This is not a passing full gate. |
| `baseline-failures.log` | All 13 exact failing cases reproduced on unmodified HEAD `9afc120029ed85e10e56d4ac2fcce926db129d01` in an archived disposable tree: same 6 failures and 7 errors. No task-source substitution. |
| `aggregate-final.log` | `python3 tools/verify.py`: 7 checks, 1 failed (the same orchestrator boundary). Other suites: 3, 13, 4 and 311 pass; root suite has 32 skips. Registry passes 8 subsystems/35 refs, profile drift matches 112 managed paths. |
| `contracts-pre-registry.log` | Structural registry validation passes, 8 subsystems/35 indexed references. Implemented collection deltas are still owed to the designated registry-updater stage. |
| `admission-mutation.log` | Controlled omission of collection admission makes V-01 fail its behavioral `passed` versus `missing` assertion after real actor/check setup. No temporary source edit retained. This is sensitivity evidence, not a production pass. |
| `composed-proof-02.log`, `composed-proof-02/` | Retained real V-05/V-09 task: actual failed product, correction, passing checks, independent rerun, acceptance handoff, then later drift; final status has stale checks/collection and count 1. |

Exact native commands from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py
```

Run changed methods first via the owning command plus `-k collection` or the
specific method suffix, then owning modules and broader gates. Current final
finite-role/exposure controls additionally have focused logs
`identity-exact-roles.log` and `findings-isolated-exposure.log`. Aggregate execution
preceded those test-input refinements; final owning suite reruns all 50 cases.
Production/state bytes did not change after the aggregate run. Schema/document
checks establish structure only and are not counted as behavioral verification.

The retained proof tree was copied from `/tmp/tmpn6tp9xtm` before normal fixture
cleanup. Its records deliberately retain original absolute provenance; do not
rebind identities to the copy. Inspect copied relative paths under
`composed-proof-02/runs/run-flow/`: `checks/operation-003.json` and command stderr
show the initial real assertion failure; `checks/operation-005.json` shows the
corrected check; `collection-checks/operation-008.rerun.json`, execution logs and
`collections/operation-008.json` show the fresh independent rerun/admission.
`proof-current-status.json` records later stale evidence and count 1. The copied
actor invocation log and candidates retain observed sessions and before/after
product identity. This is local proof, not a portable runnable run directory.

## Complete scenario mapping

Test names below are methods of `ActorOperationsTest` in
`tests/test_actor_operations.py`; names omit the `test_` prefix. Every material
subrow uses actual public operations/storage and production admission, with
scripted actors controlling only responses/session events/edits.

| Verification rows | Behavioral evidence and oracle |
|---|---|
| V-01 | `collection_v01_current_independent_rerun_and_handoff`: public preflight/implementation/checks/collector; assignment/prompt inputs and local workflow; distinct rerun ID/logs/session; execution counter 2; product unchanged; count 0; current passed collection enables separate acceptance, whose evidence remains missing. |
| V-02a,b,c | `collection_v02_identity_and_authority_matrix`: wrong task, operation, explicit implementer role and explicit acceptance_reviewer role independently refused at terminal admission. |
| V-02d,e,f | Same matrix: claimed session mismatch, candidate mismatch, and each input/policy/flow digest mismatch (valid-shaped different digests). No successful coverage or acceptance progression. |
| V-02g | Same matrix: actor-invented observed provenance extra field cannot establish transport identity. Inherited `f01_malformed_observation_binding_cannot_admit_readiness` separately protects actual receipt assignment types. |
| V-02h | Same matrix reuses actual implementation session; `collection_v05_real_failed_code_correction_and_v09_evidence_retry` separately reuses actual correction session. Both fail independence. |
| V-02i | Matrix separately supplies malformed JSON and missing required result; diagnostic raw/absence retained, no pass. |
| V-02j | `collection_v08_drift_during_live_collection`: real actor publishes result then waits; observation remains running. `collection_v10_publication_interruptions_replay_once` intent branch establishes actual unknown ownership and no relaunch/acceptance. |
| V-02k | Identity matrix adds structured final decision ACCEPT; collector envelope rejects it and grants no acceptance/completion authority. |
| V-03a | `collection_v03_missing_replayed_wrong_bound_and_incomplete_coverage`: only ordinary implementer-era passed-check reference; no new execution or independent coverage. |
| V-03b | Same test actually replays completed ordinary verify while collector is active; replay returns old pass, counter unchanged, collection cannot use it as fresh rerun. |
| V-03c | Same test makes separate wrong-candidate and wrong-input public rerun requests; both refuse without executing or providing current coverage. |
| V-03d | Same test separately omits rerun and supplies required gap; truthful missing/not_run coverage, count unchanged. |
| V-03e | `collection_v03e_real_failed_rerun_overrides_pass_claim`: actual rerun assertion fails under controlled external flag without candidate drift; real failure overrides reported pass and grants only inherited check_failed. |
| V-03f | Missing-coverage test separately omits coverage, gaps and findings; malformed ART-006 cannot pass. |
| V-04a,b | `collection_v04_finding_history_preserves_and_reopens_approval`: successive admissions/reload keep one stable ID and append history; unchanged evidence/exposure preserves explicitly seeded upstream-approved disposition. |
| V-04c | Same test independently changes evidence with exposure fixed, then exposure with evidence fixed; each starts from approved upstream disposition and reopens with previous decision/history retained. |
| V-04d,e | Same test retains observation without correction_request/charge; new collector disposition/deferral claim refuses and leaves existing findings unchanged. No tracker written. |
| V-05 | `collection_v05_real_failed_code_correction_and_v09_evidence_retry`: no seeded candidate/check/collection; actor creates actual defect, required behavioral check fails, real correction changes code, new candidate/check pass, distinct collector reruns and admits, then later relevant edit makes old checks/collection stale in the same task. Failure artifacts/counters/count retained. |
| V-06 | Updated `v03_v08_v11_shared_corrections_repair_and_fresh_preflight`: first reason comes from real failed check; only future ART-009 review decision and authorized repair state use labeled upstream seam. Three reservations/launches/reloads/replays charge exactly 1/2/3; repair needs fresh public preflight; revision retains 3; fourth refuses exhaustion after valid prerequisites. Intervention and acknowledgement persist without authority. Existing context-policy boundary controls remain exercised. |
| V-07a | `collection_v07_files_configuration_index_head_and_repointing`: actual tracked same-size edit invalidates current collection/checks; retained report/log bytes unchanged. |
| V-07b | Same matrix separately adds visible untracked input, modifies existing untracked input, removes it; each invalidates coverage. |
| V-07c | Same matrix separately changes evaluated configuration and explicitly allowed ignored configuration. Inherited `ControllerGitTest.test_candidate_workspace_ignored_evaluated_input_and_visible_drift` supplies the irrelevant ignored-generated-output control. |
| V-07d | `collection_v07d_revision_bindings_cannot_restore_old_reports`: separate task-input, policy-only and flow-only owner-authorized revisions invalidate old collection/readiness and preserve count/history. |
| V-07e | File matrix separately changes index while worktree bytes stay fixed, and HEAD. Old evidence cannot enable acceptance. |
| V-07f | File matrix challenges old report path and candidate-digest repointing after drift; revision test repoints old report reference after revision. Status stays stale, acceptance refuses, observe replay never restores eligibility or rewrites history. |
| V-08 | `collection_v08_drift_during_live_collection`: separate product/configuration/approved-source edits at synchronized live process checkpoint; old passing rerun/report cannot admit stale collection. Actual edits retained, no acceptance. Also exercises exact active rerun replay through library and CLI without executing again. |
| V-09 | Real correction journey reaches count 1; missing evidence leads to fresh collector/rerun with distinct IDs and no additional implementer or charge. Earlier failed/gap evidence remains. |
| V-10a | Positive and publication tests replace raw claim after admission; replay keeps identical ledger bytes/version/count and findings/history/logs. Publication controls use nonzero correction count and nonempty finding. |
| V-10b | Publication test kills coordinator after durable launch intent, before launch certainty: replacement controller reports unknown, intervenes and refuses overlapping actor/relaunch. Count/work retained. |
| V-10c | Publication test kills coordinator while collector remains live. `collection_v10c_live_rerun_serializes_and_unresolved_terminal_blocks` also kills actual collector coordinator during real running rerun; command-lock contention refuses overlap; unresolved rerun survives actor terminal receipt as unknown ownership with blocked evidence, intervention and no retry. |
| V-10d | Publication test interrupts after exclusive admitted-report artifact but before ledger publication; replacement controller consumes existing terminal proof once without another actor/check or duplicate finding. |
| V-10e | Publication test interrupts after ledger admission before caller success; replacement observe replays identical outcome/findings/count and execution counter. |
| V-11a | Real failed-code journey and failed-independent-rerun test persist product-failure records/logs and bounded check_failed route. |
| V-11b | `collection_v11b_missing_executable_retains_infrastructure_blocker`: required executable passes initial checks then actually disappears outside candidate; rerun records infrastructure blocker/unknown ownership, no product pass or invented repair permission. |
| V-11c | Identity missing-result and coverage missing-rerun/gap controls expose missing/not_run coverage and specific fresh-evidence next action. |
| V-11d | Drift/revision matrices and composed late edit expose stale evidence and new inspection/check/collection actions. |
| V-11e | `collection_v11_capability_blocker_and_public_request_refusals`: unavailable required review capability attestation blocks collection with persisted intervention/active-chat action. Prompt explicitly prohibits source substitution and preserves separate stages. It proves honest handling, not external authentication of skill availability. |
| V-12 | Parent controller contract compared with callable/CLI/schema/artifact behavior above. `v12_acceptance_role_remains_fresh_raw_claim_without_admission` now uses real collection admission before acceptance transport (old seeded collection setup removed). No semantic acceptance/completion. |

The inherited receipt-type test is supplementary to the complete collector
controls, not a substitute for them.
Only the labeled future ART-009 disposition/review-decision and environment-repair
fixtures seed upstream authority. No production bypass for acceptance was added.

## Original baseline, comparison and maintainability rationale

Original B remains exactly:

- `.quality/reports/T-004.2-preflight-20261112T165634690085Z/starting.json`
- `.quality/reports/T-004.2-preflight-20261112T165634690085Z/starting.txt`

Before edits, exact 12-file inventory/current hashes, logical root, Python,
installed adapter/settings and scripts/tests/evals folder coverage matched B.
Final I is `comparison-05.json` / `comparison-05.txt`: complete,
full_profile=true, comparison=compared, same CPython 3.14.4/Radon 6.0.1/Ruff
0.14.2 and effective settings. It compares three affected Python paths against
original B; all originals/prior comparisons remain retained. No new/extracted
module, renamed symbol or unsupported folder was introduced. Unmatched new
symbols have unknown before counts, never invented zeros. Measurement is advisory;
required architecture/native duties retain their own results above.

Exact submitted Python SHA-256 (also `changed-python-final.json`):

```text
scripts/controller.py          508c8a81c755c8d0195ac882d2072e2e7c378e9478920b74088308f610fcdf79
scripts/controller_state.py    58cc1d2b61bb97e9c594303f57f57da7a2b8074a599c0e750b9d6610fbd20226
tests/test_actor_operations.py  47fd170d8e6939655fd426151a79f168ad3a54960ac2ac53a1c19d7d6643ff53
```

All rationale rows reference `comparison-05` and original B. CC is cyclomatic
complexity; statements and arguments use collected native Ruff counts.

| Affected function / metric B → I | Retained structure and useful local alternative |
|---|---|
| `check_collection`, CC unknown → 18 | One locked transaction validates ownership/current candidate, replays exclusive results or records intent/execution. Context and artifact verification are already separate helpers. Further splitting replay/launch would pass the same authority tuple across helpers without another consumer; retain the visible no-relaunch ordering. |
| `_admit_collection`, CC unknown → 25 | Identity/independence, actual rerun status, coverage and publication form one semantic admission decision. Report validation and finding merging are separate pure helpers. A further rerun-disposition helper is plausible, but would distribute the failure-precedence rules between callers; retain them together for review. |
| `_reservation_options`, CC 25 → 29 | Ordered guards preserve active-owner, exhaustion, readiness and candidate/collection prerequisite precedence. A data-driven transition table would need exceptional guards for these same priorities and obscure safe next-action decisions. |
| `status_run`, CC 15 → 21 | One read-only snapshot evaluates candidate and admitted-report freshness, preserving exhaustion precedence and unknown-owner diagnostics. Artifact validation is already extracted; another view helper would mostly move cloning/precedence branches without a reusable boundary. |
| `reserve_operation`, CC 32 → 33; arguments 7 → 7 | Adds current collection validation at existing locked acceptance prerequisite. Request validation/replay and exact one-charge publication stay atomic. A request-object API would change the inherited public contract and hide arguments; helper validation is reused instead. |
| `launch_operation`, CC 12 → 13 | Adds collector input context before publishing no-relaunch launch intent. Launch ownership/configuration/replay ordering belongs together. Moving context into the transport would duplicate controller-owned authority validation and cross the module boundary. |
| `_admit_actor_outcome`, CC 10 → 11 | One stage dispatch delegates collection semantics and retains preflight plus raw acceptance handling. A dispatch registry adds indirection for one additional branch and risks multiple admission owners. |
| `observe_operation`, CC 15 → 18 | Rerun uncertainty must gate terminal actor admission at the existing observed-ownership boundary. Path/unresolved detection is extracted. A second observer would duplicate lock/liveness/publication policy, so retain the short explicit branch here. |
| `test_collection_v07_files_configuration_index_head_and_repointing`, CC unknown → 11 | Finite named rows keep the decisive real filesystem/Git mutations visible beside one shared stale oracle. Callback/action factories would hide which input actually changed and add fixture abstraction for one consumer. |
| `build_parser`, statements 53 → 53 | Registers one additional producer command through the existing loop. A parser module extraction would expand ownership and add navigation cost without reducing this bounded change. |

No affected function has another above-target native statement/argument metric.
Untouched legacy hotspots, including `check_candidate`, retain their existing
numbers and are context only. Numeric equality below or at target needs no defense.

## Handoff and limits

First outstanding stage: fresh `task-maintainability-review`. Complete ordered
route: required architecture gate (passed for final runtime scope) → fresh
maintainability review → designated `task-contract-registry-updater` → fresh
independent `task-review-discovery` → separate fresh `task-acceptance-review`.
The registry stage must update current reusable contracts and stale discovery
references, then regenerate the index. Independent reviewers must corroborate
current finite admission/drift/correction/reload evidence and inspect retained
proof logs; this report is not their verdict.

Optional installation-local run-evidence sidecar:
`.git/personal-skills/run-evidence/runs/run-20261112T165856Z-1175386f00d7/manifest.json`.
Sidecar outcome: completed (implementation handed off for independent review);
`run-evidence-finish.log` retains closure. It does not replace behavioral or
independent review evidence. Initial
architecture wrapper argument parsing failed before executing a check; corrected
canonical checks ran and their raw logs are retained.

No live/model/network/sbx/provider qualification, enforced collector filesystem
isolation, semantic review-quality qualification, automatic recovery, ART-009,
completion, commit, tracker update or dependency release was performed. The 20
orchestrator and 32 root skips are unqualified checks. Historical unsupported
legacy Linux sandbox boundaries remain failures, reproduced on unchanged HEAD;
no skip or configuration check is counted as a behavioral pass. T-006 retains
the authorized live pilot, while T-005 owns independent acceptance/completion.
