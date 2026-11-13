# T-005.1 implementation submission

Separate acceptance now admits a current decision through the existing actor
lifecycle, preserves finding dispositions, and authorizes correction or returns
missing proof to its owner. A valid accept exposes eligibility for T-005.2;
completion and tracker recording remain absent.

Submission: **READY_FOR_REVIEW**, not independently accepted. The focused suite
passes 67 tests. The aggregate remains failed on the same 13 inherited legacy
Linux/macOS containment cases; its skips are unqualified. Next owner: fresh
maintainability review → contract registry updater → fresh independent discovery
→ separate fresh acceptance. The required canonical architecture gate has passed.
No reviewer was launched or verdict emitted by this implementation invocation.

## Deliverables and scope

- `scripts/controller.py`: separate acceptance context/admission, exact retained
  proof checks, current eligibility, finding dispositions and recovery routes.
- `scripts/controller_state.py`: decision/disposition/conditional-receipt shape
  validation, frozen required-review inventory and admission-field protection.
- `assets/actor-result.schema.json`: acceptance-only decision envelope;
  `assets/task-manifest.schema.json`: optional frozen `required_reviews`.
- `tests/test_actor_operations.py`: public acceptance/refusal matrices, real code
  correction, mixed correction budget, evidence recovery and interrupted replay.
- `tests/test_controller.py`: two older reservation-only scenarios now reject
  seeded review authority; their check/repair/revision/replay/exhaustion evidence
  remains. Actual review-driven composition belongs to the public actor journey.
- [Controller contract](controller-contract.md): exact T-005.2 consumer seam,
  API/CLI, records, dispositions, replay, eligibility and remaining work.

Paths above are within `skills/task-orchestrator/`. Existing task-index edits,
T-005/T-005.1/T-005.2 authority packages and `.DS_Store` files are owner work and
were preserved. No official plan/index, tracker, installation, dependency,
commit, release or orchestration state was changed by implementation.

Actual contract impact: added ART-009 / IF-003 separate acceptance; extended
ART-002 decision/eligibility/route state and finding provenance; bound verifier
result bytes and independent collection reruns more tightly. Existing
ART-003/005/006 and IF-001/002 accounting remains. Environment repair still uses
explicit upstream authority; no automatic recovery or new budget policy exists.

Executable contract declarations changed: both schemas above and the runtime
validators/records in controller/state. Registry synchronization is deliberately
left to its designated separate stage. That stage must also reconcile stale
capability prose in the source `SKILL.md`, operator guide and architecture map,
which still describe acceptance as a raw claim. Task-orchestrator is absent from
`DEVELOPMENT_SKILL_SOURCES`; the canonical installer was inspected and no profile
or shared-runtime distribution change is needed. Installed skills were not refreshed.

## Entry and retained evidence

Consumed [brief revision 1](brief.md), [verification revision 1](verification.md)
and [ready guided preflight](preflight.md), the parent P-01..03/P-06, current
contract registry, accepted T-004 contract/closure, owner-confirmed sbx direction
and installed contextual disposition policy. Project-local implementer and
`testing-discipline` were selected under `.agents/skills/`; helpers came only
from sibling `.agents/scripts/`. Required installed review roles were available.
No authority, ownership or capability change prevented entry.

All raw logs below live under
[`.quality/reports/T-005.1/`](../../../../../.quality/reports/T-005.1/).
Historical failed attempts are retained, including the corrected supersession
bug, mistaken test reasoning-level assertion and two obsolete seeded-review
expectations. Later successful evidence supersedes those attempts; it does not
make the historical failures passes.

| Current command/evidence, repository-root cwd | Result and meaning |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py` — `focused-final-04.log` | 67 passed, no skips. Current public controller/real local actor/check behavior. |
| `python3 tools/verify.py` — `aggregate-final.log` | 7 checks, 1 failed. Orchestrator constituent: 281 tests, 6 failures, 7 errors, 20 skips. Other suites: 3, 13, 4 and 311 tests pass; root has 32 skips. Registry passes; installer drift matches all 112 managed paths. |
| Aggregate orchestrator constituent: `/usr/bin/python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py' -v` | Current full owning scope; equivalent discovery coverage to preflight's command without explicit default pattern. Reused rather than rerun solely for reporting. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — `architecture-final-02.log` | 4 passed, no skips; canonical whole-repository runtime import gate. Captured once for these current runtime bytes through installed run-evidence. |
| `python3 tools/check_contracts.py --root .` — `contracts-final-02.log` and aggregate | Structural pass, 8 subsystems / 36 indexed refs. Implemented contract delta is still updater-owned. |
| `mutation-01.log` | A disposable copied controller with acceptance admission replaced by the prior raw-claim behavior fails V-01's passed-versus-missing assertion. Mutation rejected for the intended oracle; no working-tree mutation retained. |
| `witnesses.log`, `witnesses/` | Six decisive existing tests pass with complete disposable-run artifacts retained: V-01, V-06, V-08, V-09, V-10a and V-12. Archive-origin records map original temporary roots to retained directories. |
| `reservation-regression.log`, `revision-regression.log` | Each of the two corrected reservation-only tests passes; both also pass in the current aggregate. |

The 13 aggregate failure identities exactly equal the historical independently
reproduced unchanged-baseline set in T-004.2's `baseline-failures.log`; see
`inherited-failure-comparison.log`. No new failures remain. This comparison is
identity reconciliation with retained historical evidence, not a newly executed
baseline or successful host qualification. The full gate is still failed.

Current checked-byte identities for all six changed runtime/schema/test paths
are retained in `checked-bytes-final.json`. They were checked unchanged after the
aggregate and witness executions. Native producer/stage is this implementation
invocation, under `docs/development.md`, repository AGENTS instructions and the
preflight's native-obligation inventory. The aggregate covers current whole-repo
scope; architecture is structural evidence, not behavioral qualification.

## Acceptance evidence map

All tests in this table are methods of `ActorOperationsTest` in
`tests/test_actor_operations.py` unless otherwise stated. The current focused
command above executes them. Every named verification row is accounted for;
policy interpretation remains a fresh independent review obligation. Local
scripted classifications establish mechanical handling of supported/contradictory
claims, not a model's ability to make the right judgment.

| Verification cases | Current setup / oracle and evidence |
|---|---|
| V-01 | `test_acceptance_v01_fresh_current_decision_without_completion`: real public preparation, passing checks and collector rerun; observed distinct session, frozen model/effort, no-edit/no-tracker prompt, exact context/digests, count zero, eligibility without completion. Witness retained. |
| V-02a–i, j–m, o–t | `test_acceptance_v02_identity_terminality_matrix`: otherwise valid current candidate; different run/task/operation/key, actual implementer/collector role, valid but wrong hashes/revision/candidate, absent/mismatched/invented/reused sessions, malformed/missing output, wrong JSON type and failed/non-complete outcome all grant no admission. Fresh control succeeds; recollection then old acceptance-session reuse refuses. |
| V-02n | `test_acceptance_v08_actual_review_driven_code_correction`: the actual correction's observed session is reused as acceptance against corrected current proof and refuses; a fresh reviewer then accepts. |
| V-03a–f | `test_acceptance_v03_retained_artifact_integrity_matrix`: remove, replace or append bytes to current candidate, check, collection, execution/log or collector-rerun proof. Reservations refuse without ledger mutation; after launch, changed execution also denies admission. Missing verifier proof is exposed as stale with verify recovery. |
| V-03g | Real failed frozen checks in V-09 and inherited real failed-rerun scenario, supplemented by the otherwise-valid failed-status acceptance refusal in `test_acceptance_v03_required_status_and_unsupported_claims`. Failed proof cannot satisfy launch/admission prerequisites. |
| V-03h–j | `test_acceptance_v03_required_status_and_unsupported_claims` and `test_acceptance_v03_conditional_stages_cannot_be_omitted_or_weakened`: explicit negative blocked/missing/not-run/omitted states and failed/blocked/not-run/inconclusive conditional receipts refuse. These negative states are guard inputs, not seeded success. |
| V-03k–l | Conditional-stage test: frozen maintainability/registry inventory, actual retained independent receipts and Markdown proof; each missing stage refuses, altered/weaker manifest refuses, supported complete control accepts. |
| V-03m–n | Unsupported-claims and disposition-policy tests: empty rationale, missing evidence map, unknown verdict and unaccounted retained finding refuse; prose cannot erase findings. |
| V-04a–e | `test_acceptance_v04_drift_matrix_and_replay`: independent tracked/untracked/configuration/index/HEAD changes with real Git/files and exact restoration; refusal leaves ledger bytes unchanged. |
| V-04f–g | `test_acceptance_v04_explicit_ignored_input_and_each_task_document`: explicitly evaluated ignored input and separate brief/verification source mutations refuse; restored inputs allow acceptance. |
| V-04h–j | Drift/replay and `test_acceptance_v04_in_review_drift_and_irrelevant_output`: synchronized real live acceptance detects product drift; replay retains admission history but loses current eligibility after drift; irrelevant ignored generated output still accepts. |
| V-05a–c | `test_acceptance_v05_disposition_policy_and_v07_routes`: supported AC violation, material operating risk and contextual maintenance risk yield bounded correction authority; wrong reason preserves bytes/count. |
| V-05d | `test_acceptance_v05_v06_approved_known_issue_continuity`: bounded optional diagnostic context, compatible consumers, follow-up/reassessment and actual acceptance provenance retained; no tracker write. Witness retained. |
| V-05e–f | `test_acceptance_v05_observation_uncertainty_and_prevented_correction`: preference/ordinary uncertainty contexts accept as observations with no correction request or charge. Preference-only correction claim separately refuses. |
| V-05g–h | Evidence-only recovery and prevented-correction tests: missing proof returns to verify/collection; unresolved material context or unavailable correction authority yields no eligibility and retains intervention/unfinished rows. |
| V-05i–j | Disposition-policy test and contradictory-approval control: AC-waiving or material-risk deferrals refuse, including explicit rare catastrophic irreversible-impact context. Existing approval cannot conceal contradictory material-risk flags. |
| V-06a–c, f | Continuity test: same issue, collector omission, unchanged approval reopening attempt and existing default tracker history preserve stable ID, original approval/provenance and history without duplicate issues or writes. |
| V-06d–e | Continuity test: separately changed evidence and changed exposure reopen with reason and prior history; fresh supported reapproval works. |
| V-07a, d | Disposition-policy test and V-08: supported current blocker authorizes review correction; a separate unfinished coverage row remains in the decision while correction takes precedence. Decision charges zero, reservation charges once. |
| V-07b–c | `test_acceptance_v05_observations_and_v07_evidence_only_recovery`: substantive proof gaps from mechanically complete prerequisites; actual new checks/recollection recover the named proof without product edits or correction charge. |
| V-07e | Prevented-correction test: confirmed blocker without authority remains intervention-only; no correction reservation or charge. |
| V-07f | Existing `test_collection_v11b_missing_executable_retains_infrastructure_blocker`: actually remove a previously passing executable; current rerun remains unknown/blocked, with no invented product or repair authority. |
| V-07g | V-09: explicitly upstream-authorized repair charges shared cycle three, invalidates readiness, refuses premature implementation and rejects an old repointed readiness receipt; fresh public preflight restores readiness. Only repair authorization is an upstream seeded fixture. |
| V-07h | Existing `test_v07_missing_each_prerequisite_reaches_specific_blocker` removes the actual installed fixture skill; `test_collection_v11_capability_blocker_and_public_request_refusals` retains unavailable-review coverage/blocker/intervention; conditional-stage tests refuse absent required stage proof. No source/installation substitution. |
| V-07i | Evidence-only recovery test records an actual intervention acknowledgement; it grants no environment-repair reservation or eligibility. |
| V-08 | `test_acceptance_v08_actual_review_driven_code_correction`: frozen task expressly requires `calculate(2)==4`; initial real checks pass while real probe raises AssertionError on `return 0`. Collector finding alone cannot authorize correction. Separate decision enables actual code change to `return x*2`, fresh checks/collector and fresh acceptance. Retained `behavior-probes.jsonl` shows return codes 1 then 0, not a setup/syntax failure. Count one, no completion/tracker. |
| V-09a–b | `test_acceptance_v09_mixed_budget_revision_and_eligibility_at_limit`: actual failed check → check correction one; separate supported review → real product correction two; explicit repair → correction three. Owner-bound input/policy/flow revision preserves count/history. Replay/reload do not double-charge; supported acceptance succeeds at three, then a real required failure makes fourth correction refuse without launch/mutation. Reservation/revision-only tests additionally preserve post-third-revision and legacy-guard cases. Witness retained. |
| V-10a, d | `test_acceptance_v10_replay_ignores_replaced_raw_decision` and publication-interruption test: retained decision survives raw-output replacement and post-publication coordinator death without reinterpretation/version/count change. Missing admitted decision proof loses eligibility but permits a fresh reviewer. |
| V-10b–c | `test_acceptance_v10_real_publication_interruptions`: kill actual coordinator after durable launch intent or after decision-file creation before ledger publication; reload conservatively blocks unknown ownership or admits the same known terminal result once. No relaunch. |
| V-11a–d | Live-owner/invalid-request, policy-route, V-08 and updated reservation-only tests: stale version, conflicting key, collector-only correction and wrong reason preserve state/count/files; no extra actor/charge. |
| V-11e–f | Live-owner test and intent-interruption test: synchronized actual actor may have result bytes but remains sole owner; unknown intent after reload cannot launch a successor or become eligible. |
| V-11g | Existing `test_collection_v10c_live_rerun_serializes_and_unresolved_terminal_blocks`: actual unresolved collector-rerun ownership prevents acceptance/retry. |
| V-11h | `test_acceptance_v11_real_launch_contention_has_one_actor`: competing real coordinator processes produce exactly one acceptance invocation. |
| V-12 | `test_acceptance_v12_documented_cli_and_changed_schema_boundary`: actual reserve/launch/observe/status CLI, current decision bytes/digest and eligibility-only behavior. Runtime valid/invalid decision controls accompany structural schema assertions. This contract and final diff were inspected as implementation evidence, not independent review. Witness retained; registry reconciliation remains its separate owner's gate. |

AC-01 maps to V-01/02/07h/11e–h; AC-02 to V-01/03/04/09/12; AC-03 to
V-05/06/07d–e/10a; AC-04 to V-01/07/08/09/11a–d; AC-05 to V-01/08/09/10/11;
AC-06 to V-01/08/12. No scenario revision or requirement weakening occurred.

## Measurement and retained structure

Original pre-edit actual-worktree pair:
`.quality/reports/T-005.1-before-01.json` and `.txt`. Current comparison:
`.quality/reports/T-005.1-after-05.json` and `.txt`. Both are complete, compatible
complexity/Ruff measurements from the installed helper and already prepared
pinned environment. Earlier comparisons 01–04 remain retained and superseded
where bytes changed; every comparison uses the same original baseline.

Original scope covers `skills/task-orchestrator/scripts` and `tests`, all 12
initial Python files, including relevant harness/fixtures. Final affected Python
scope is controller, state and the two changed test files; no Python path was
added/deleted/moved. `baseline-validation.log` confirms project binding, inventory,
stored source hashes and exact preserved original HEAD bytes. Effective tool,
settings and check identities are in the report pair. No setup or installation
was performed. Schemas/Markdown are unsupported measurement assets, N/A.

The following retained-breach reasoning refers to comparison `after-05` and its
original `before-01`. CC target is 10, statements 50, arguments 5. Unknown/new
symbols are not numeric zero. Untouched sibling hotspots are outside attribution.

| Affected function / known metric | Retention and useful local alternative |
|---|---|
| `controller.init_run`: CC 16→16; statements 66→67 | Required reviews belong beside frozen checks/scope. Extracting generic input freezing could be useful for a broader authority refactor, but here adds navigation for one field and touches unrelated initialization. |
| `_validate_current_collection`: CC 7→11 | Candidate, collector identity, report coverage and retained rerun/log proof form one current-collection boundary. A separate rerun validator would shorten this function but split its single cohesive consumer; shared retained-byte/check helpers already carry reusable logic. |
| `_admit_collection`: CC 25→26 | Adds the rerun digest at publication alongside the report it binds. Extracting a nullable-hash helper buys no new boundary and hides this binding. |
| `_disposition_for_finding`: new CC unknown→13 | Contradictory flags, immutable approvals and fresh provenance are one disposition decision. Table-driven flag dispatch could shorten branching but obscure policy precedence; it is not a classifier. |
| `_acceptance_route`: new CC unknown→17 | The four routes and correction-over-missing-proof precedence must be assessed together. Independent action handlers would duplicate mixed-condition checks or disperse precedence. |
| `_admit_acceptance`: new CC unknown→17 | One admission transaction checks provenance/current context, computes dispositions/routes and publishes one record. Existing dedicated context, validators, dispositions and route helpers separate real boundaries. Another publication helper would add indirection for a single field-write consumer. |
| `status_run`: CC 21→37 | Current candidate/check/collection/acceptance integrity and recovery actions belong to one read-only ledger snapshot. Extracting a status-view builder is a plausible next local cleanup if another consumer emerges; splitting now risks separate snapshots or concealed ordering. No status read mutates authoritative state. |
| `reserve_operation`: CC 33→44; statements 39→52; arguments 7→7 | Current evidence, admitted correction authority, evidence-only recovery, idempotency and charge must precede one locked reservation. A stage-prerequisite helper could reduce the local branch count, but would move ordering-critical checks away from the mutation they guard. The existing public signature remains stable. |
| `launch_operation`: CC 13→14; `_admit_actor_outcome`: CC 11→12 | Adds acceptance context selection and the required admission dispatch at existing extension points. Moving either into transport or an alternate admission path would duplicate authority or cross ownership. |
| `revise_inputs`: CC 29→29; statements 58→58 | Required-review inventory and actual source hash remain inside the existing owner-authorized revision bundle. A separate source-capture helper is feasible but adds a one-consumer wrapper; no unrelated revision refactor was justified. |
| `state._validate_task_manifest_schema`: CC 17→19 | Closed required-review names belong with task manifest field validation. Generic schema dispatch would broaden scope and obscure explicit supported stages. |
| `state.apply_ledger_update`: CC 30→30; statements 54→54; arguments 8→8 | Protects `candidate_path` in the existing admission-owned field set. Extracting the established generic mutation gate for this set member adds unrelated churn and no new responsibility separation. |
| `ActorOperationsTest.producer_run`: arguments 4→6 | Explicit required-review and task-document inputs reuse the existing real Git/actor setup rather than copy a harness. A generic options dictionary would hide these concrete test preconditions; dedicated duplicate builders would increase maintenance. |
| `test_acceptance_v09_mixed_budget_revision_and_eligibility_at_limit`: new statements unknown→65 | One real unseeded history proves mixed charging, revision, repair, third-cycle eligibility and fourth refusal. Splitting into independently seeded phase tests would lose composition evidence; a shared phase object would hide the decisive lifecycle operations. Existing focused helpers handle routine execution. |

The old actor raw-acceptance test is replaced by V-01's real admission oracle.
The old seeded-review actor budget test is replaced by the real mixed public
journey, retaining repair/readiness, replay/revision, exhaustion and occupancy
boundaries. Those renamed symbols have unmatched automatic numeric baselines;
no fabricated deltas are claimed. No production responsibility was extracted to
another module, no metric exclusions/targets changed, and no unrelated cleanup
was performed. Other affected measured functions remain at/below target.

## Report transfer, limits and next owner

All evidence is shared in this workspace. For an isolated reviewer, explicitly
copy the original `T-005.1-before-01.json`/`.txt` and comparisons
`T-005.1-after-01` through `T-005.1-after-05` (both extensions) from this
repository's `.quality/reports/` into the same repository-relative paths in the
receiving checkout. Also copy `.quality/reports/T-005.1/` (raw logs, final byte
identity and witnesses) into that same receiving relative directory. These
ignored artifacts do not travel with commits. Archives retain original path
identities for inspection; they are not relocated runnable controller runs.

Optional run evidence uses
`.git/personal-skills/run-evidence/runs/run-20261112T193831Z-34902050afb4/`.
It records this implementation invocation, not independent task acceptance.

Remaining obligations: fresh maintainability review; registry/current-discovery
synchronization including source capability prose; fresh independent discovery
corroborating the finite cases and current inherited failures/skips; separate
fresh acceptance. The canonical architecture gate is current and passed. No
conditional review or acceptance is claimed by this author. Do not advance to
T-005.2 before that route completes.

Residual limits: aggregate failure and 20/32 skips remain; no live sbx/provider,
model identity, semantic-review judgment, enforced reviewer isolation, tamper
resistance or power-loss recovery was qualified. Conditional review receipts are
trusted coordinator handoffs with exact retained proof, not a new role launcher
or provider-attestation system. Preparation owns truthful required-stage
inventory; natural-language workflow requirements are not automatically parsed.
The default known-issue tracker is supplied when present; nondefault tracker
selection/recording and final recording validation remain completion-owner work.
