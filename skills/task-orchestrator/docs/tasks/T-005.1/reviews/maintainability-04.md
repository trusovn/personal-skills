# T-005.1 source-guided maintainability review

VERDICT: ACCEPT
ARCHITECTURE_GATE: PASS
MEASUREMENT: complete

This is the user-authorized source-guided reassessment under
`skills/task-implementation-flow/task-maintainability-review/SKILL.md` and its
`references/measurement-review.md`, with source `skills/testing-discipline/SKILL.md`
and sibling source `scripts/` runtime. The older installed skill was not refreshed.
This session authored no reviewed production/schema/test/fixture/harness assets;
it previously wrote only maintainability-03. Reviewer independence from implementation
is retained. This report supersedes maintainability-03 as the current source-guided
assessment, without modifying any historical report. It does not review itself.

## MEASUREMENT

- Original B: `.quality/reports/T-005.1-before-01.json` and `.txt`.
- Implementer I: `.quality/reports/T-005.1-correction-02-final.json` and `.txt`.
- Independent R: `.quality/reports/T-005.1-review-source-04.json` and `.txt`.
- B captures both original orchestrator Python folders, all 12 source files,
  at original commit `6a13008d239d22ad48909258e00edd809953973d`, an ancestor of
  current HEAD. All 12 base64 source snapshots independently match their hashes
  and that commit's exact bytes. This validates logical project and preserved
  pre-edit state, not merely matching roots/status text.
- I's four measured file hashes match current staged and worktree bytes. R was
  independently run against those actual bytes and the same original B, not I.
  Measurement is complete, comparison is `compared`, errors are empty. Both
  checks, full profile, format 5, CPython 3.14.4, Radon 6.0.1, Ruff 0.14.2,
  adapter SHA-256 `c24932c841189b72725b50c86f20a2814c50a7a8903921a2ceb8b167b0f285df`,
  effective target policy/settings and zero-limit Ruff collection are compatible.
  Existing tools were used; no setup, installation, exclusions or target edits.
- Scope: the four changed Python files under original scripts/tests coverage.
  No Python path was added, deleted or moved. Two tests were renamed/replaced:
  `test_v03_v08_v11_shared_corrections_repair_and_fresh_preflight` becomes
  `test_acceptance_v09_mixed_budget_revision_and_eligibility_at_limit`, and
  `test_v12_acceptance_role_remains_fresh_raw_claim_without_admission` becomes
  `test_acceptance_v01_fresh_current_decision_without_completion`.
  Their unmatched numeric before-values remain unknown. No cross-symbol delta
  or missing native count was interpreted as zero.
- Schema/Markdown/task-index changes are unsupported measurement formats (N/A)
  but relevant schema and ownership changes received semantic inspection.
  The embedded fake actor and launch interception programs are string literals;
  their changed decisions are not measured by outer-function CC and were
  inspected manually. No attribution analyzer was created.
- R command: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/measure_maintainability.py compare skills/task-orchestrator/scripts/controller.py skills/task-orchestrator/scripts/controller_state.py skills/task-orchestrator/tests/test_actor_operations.py skills/task-orchestrator/tests/test_controller.py --root . --baseline .quality/reports/T-005.1-before-01.json --output .quality/reports/T-005.1-review-source-04.json`.
  Raw launcher output: `/tmp/source-review-measure.log`.

## RATIONALE_DISPOSITIONS

Targets 10 CC / 50 statements / 5 arguments are advisory. The following inventory
covers every measured CC increase and every newly introduced/unmatched function
in the affected files, including below-target changes. Each row names the
function rather than treating untouched symbols in the same file as affected.
`Unknown` is not numeric zero. These are independent inspection dispositions;
retention rationale in implementation-report/correction-02 is agreed with except
for obsolete intermediate values, which R replaces below.

| ID | File / function | CC before → after | Disposition |
|---|---|---|---|
| R-01 | `controller.py:_validate_current_collection` | 7 → 11 | Retain: one collection-proof boundary checks admitted assignment, coverage and collector-owned rerun. It delegates byte/hash and check closure policy to existing helpers; another one-consumer rerun wrapper adds navigation without localizing new policy. |
| R-02 | `controller.py:_admit_collection` | 25 → 26 | Retain: the one added branch hashes an optional rerun alongside its admitted report. Collection provenance, report status and publication retain their existing owner; extracting nullable hashing alone conceals the binding. |
| R-03 | `controller.py:_retained_bytes` | unknown → 5 | Retain: shared run-relative containment and exact-byte digest validation has concrete check, collection and acceptance consumers; filesystem I/O is its intended boundary. |
| R-04 | `controller.py:_retained_json` | unknown → 1 | Retain: a small reusable composition of retained-byte validation and JSON decoding; it prevents callers from accidentally skipping the integrity boundary. |
| R-05 | `controller.py:_current_checks` | unknown → 6 | Retain: current verifier identity and closure are checked here for collection, acceptance and reservation; these consumers reuse one determining rule. |
| R-06 | `controller.py:_conditional_reviews` | unknown → 10 | Retain: closed required-review stages, independent producer identity and referenced byte checks form one conditional-evidence boundary. Generic plug-in machinery is unnecessary for the two supported stages. |
| R-07 | `controller.py:_acceptance_context` | unknown → 10 | Retain: collects the exact candidate, checks, collection, conditional reviews and tracker snapshot for launch, admission and current-decision checks; those consumers intentionally use the same boundary. |
| R-08 | `controller.py:_acceptance_launch_context` | unknown → 1 | Retain: the launch-qualified helper persists the exact context used later for admission. Persistence is a real lifecycle boundary rather than a generic forwarding layer. |
| R-09 | `controller.py:_disposition_for_finding` | unknown → 13 | Retain: contradictory flags and preservation of an approved disposition are deterministic decisions over one finding. The collector owns reopening on changed evidence/exposure; acceptance owns approving the resulting disposition. A rule table would add a second representation for overlapping guards. |
| R-10 | `controller.py:_acceptance_dispositions` | unknown → 6 | Retain: one complete finding inventory applies the single-finding rule and appends history on a copy; callers do not each implement omission or approval continuity. |
| R-11 | `controller.py:_acceptance_route` | unknown → 17 | Retain: correction precedence, unresolved dispositions and unfinished proof jointly determine one admitted decision route. Separate per-action handlers would need coordinated checks for authorized blockers; the direct pure function keeps that rule visible. |
| R-12 | `controller.py:_admit_acceptance` | unknown → 17 | Retain: one admission transaction binds observed session, current launch context, validated decision and published authority. Context, validation, disposition and routing have concrete helpers already; another thin publication layer would disperse the transaction order without an additional consumer. |
| R-13 | `controller.py:_current_acceptance` | unknown → 8 | Retain: exact retained decision and current context are checked together. Subsequent evidence operations explicitly supersede the old decision before freshness validation, keeping recovery independent of old proof. |
| R-14 | `controller.py:_reservation_options` | 29 → 40 | Retain: one pure ordered decision owns active-operation, budget, correction authority, preflight and freshness precedence for both status and reservation/refusal. A table could encode terminal rules but would still need ordered guards. The current 40-point structure is substantial, but the shared facts and nine-case decision table avoid the demonstrated duplicated action authority; no new dispatcher is warranted. |
| R-15 | `controller.py:_reservation_evidence` | unknown → 11 | Retain: reads proof and prepares a copied projection for both status and locked reservation without choosing actions or writing authority. Four artifact-specific exception boundaries expose the dependency set. Splitting each into generic catch-and-mark wrappers would hide stage dependencies and add navigation. |
| R-16 | `controller.py:reserve_operation` | 33 → 34 | Retain: one locked transaction owns replay, authorization, charge and publication. It now consumes shared proof facts/actions; admission freshness checks here protect the mutation boundary rather than independently select recovery routes. A request object would hide stable call inputs and not remove transactional ordering. |
| R-17 | `controller.py:reserve_operation.refuse` | 3 → 5 | Retain: when normal selection has not run, refusal derives the same current facts and actions; otherwise it reuses the selected result. Its closure is local to one transaction and avoids a second refusal-policy authority. |
| R-18 | `controller.py:_actor_prompt` | 1 → 2 | Retain: adds role-specific acceptance instructions at the existing prompt owner. The transport remains unaware of disposition policy; a separate prompt registry for one added role adds coordination. |
| R-19 | `controller.py:launch_operation` | 13 → 14 | Retain: acceptance launch context joins collection context at the existing launch boundary. Context preparation stays in role-specific helpers; routing it through transport would reverse ownership. |
| R-20 | `controller.py:_validate_observed_result` | 8 → 9 | Retain: the acceptance-only decision envelope belongs with existing stage-dependent actor envelope checks, separate from semantic decision admission. |
| R-21 | `controller.py:_admit_actor_outcome` | 11 → 12 | Retain: acceptance uses the existing single admission dispatch and preserves diagnostic exceptions. A second acceptance entry path would duplicate authority. |
| R-22 | `controller.py:_publish_actor_outcome` | 8 → 9 | Retain: failed acceptance gets a blocked evidence projection alongside existing preflight/collection failures. The operation receipt and intervention retain the cause and identity; the projection is a distinct failure boundary, not a second decision engine. |
| R-23 | `controller_state.py:_validate_task_manifest_schema` | 17 → 19 | Retain: the optional required-review inventory and closed supported values belong to manifest validation. Runtime prerequisite validation deliberately rechecks passed/current stage proof at its separate trust boundary. |
| R-24 | `controller_state.py:validate_conditional_review` | unknown → 3 | Retain: pure record-shape/hash validation; controller current-stage and independence policy remains outside state validation. |
| R-25 | `controller_state.py:validate_evidence_references` | unknown → 4 | Retain: shared pure validation of relative references and digests supports multiple record validators without runtime I/O. |
| R-26 | `controller_state.py:validate_finding_disposition` | unknown → 4 | Retain: validates the structured decision data; material-risk and approval policy remains in the controller disposition owner. |
| R-27 | `controller_state.py:validate_acceptance_decision` | unknown → 8 | Retain: exact action/inventory/unfinished shapes, uniqueness and owner names are one pure decision-envelope contract; it does not grant acceptance. |
| R-28 | `test_actor_operations.py:RecoveryDecisionTest.test_correction_ownership_and_budget_precede_evidence_recovery` | unknown → 5 | Retain: a local nine-row fact table directly exercises the pure selector and nonmutation; it complements the public lifecycle regression rather than recreating admission setup. |
| R-29 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v09_mixed_budget_revision_and_eligibility_at_limit` | unknown → 6 | Retain: one history spans check/review/repair charging, revision, third-cycle eligibility, replay and fourth refusal. The unmatched old seeded-budget test is replaced, not assigned a fabricated numeric baseline. Splitting into separately seeded tests would remove composition evidence; extracting opaque phases would hide the decisive state transitions. Statements 66 exceed 50, but existing helpers already own routine launch/check mechanics. |
| R-30 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v01_fresh_current_decision_without_completion` | unknown → 3 | Retain: replaces the raw-claim predecessor with one real acceptance-admission journey; unmatched numeric before remains unknown. |
| R-31 | `test_actor_operations.py:ActorOperationsTest.producer_run.initialize` | 2 → 9 | Retain: optional scope, review inventory and task documents are installed before the real initialization freezes them. The bounded patch adapts the existing shared fixture; it neither substitutes admission logic nor adds a production test hook. Extending the shared fixture API would touch unrelated suites for this local need. |
| R-32 | `test_actor_operations.py:ActorOperationsTest.acceptance_ready` | unknown → 2 | Retain: names the concrete checked-and-collected lifecycle prerequisite while retaining real controller calls in existing helpers. |
| R-33 | `test_actor_operations.py:ActorOperationsTest.accept` | unknown → 1 | Retain: reservation, launch and terminal observation are the repeated acceptance lifecycle boundary, not a second policy implementation. |
| R-34 | `test_actor_operations.py:ActorOperationsTest.finding` | unknown → 1 | Retain: one local default finding shape, with decisive evidence/exposure overridable at each scenario. These are scripted claims, not an independent behavioral probe. |
| R-35 | `test_actor_operations.py:ActorOperationsTest.disposition` | unknown → 1 | Retain: one local structured-claim builder exposes kind and overrides. Its defaults do not decide production acceptance; controller validation remains real. |
| R-36 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v02_identity_terminality_matrix` | unknown → 6 | Retain: one identity/terminal-result matrix reuses a prepared public lifecycle; invalid decisions do not grant correction or eligibility. |
| R-37 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v03_retained_artifact_integrity_matrix` | unknown → 5 | Retain: missing/replaced/appended evidence variants share one local path inventory and exact restoration; admission-time tampering has an explicit separate wait boundary. |
| R-38 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v03_required_status_and_unsupported_claims` | unknown → 3 | Retain: ledger-status refusal cases are explicitly negative controls, then restored before actual malformed actor claims; no seeded acceptance success is asserted. |
| R-39 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v04_drift_matrix_and_replay` | unknown → 4 | Retain: each row keeps mutation and restoration beside its named source of drift; scope is one disposable repository, with restoration in finally. |
| R-40 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v04_in_review_drift_and_irrelevant_output` | unknown → 1 | Retain: review-time product drift and a restored, excluded generated output distinguish relevant input from incidental files without global setup. |
| R-41 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v05_disposition_policy_and_v07_routes` | unknown → 5 | Retain: related disposition claims use a local matrix and real correction/recollection between admitted decisions, preserving separate histories rather than resetting authority. |
| R-42 | `test_actor_operations.py:ActorOperationsTest.correct_and_recheck` | unknown → 1 | Retain: repeated real correction/inspection/check sequence has a named helper; reservation reason and actual edits remain explicit at callers. |
| R-43 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v05_v06_approved_known_issue_continuity` | unknown → 3 | Retain: one finding history traces retained approval, collector omission and new relevant evidence; tracker assertions verify the review boundary does not write it. |
| R-44 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v05_observations_and_v07_evidence_only_recovery` | unknown → 4 | Retain: explicit verify/collection/intervention owners drive one evidence-only route family; real recovery calls and ledger count assertions stay visible. |
| R-45 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v08_actual_review_driven_code_correction` | unknown → 1 | Retain: actual defective/corrected product code, task authority and independent assertion are visible in the same test. Independent prose and executable observations appropriately repeat the contract instead of deriving expectations from production routing. |
| R-46 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v08_actual_review_driven_code_correction.probe` | unknown → 1 | Retain: a bounded real subprocess assertion supplies the before/after behavior oracle without mocking the controller. |
| R-47 | `test_actor_operations.py:ActorOperationsTest.test_review_correction_proof_drift_requires_consistent_intervention` | unknown → 4 | Retain: each retained-proof variant follows actual admitted correction authority and asserts public status/refusal agreement, unchanged ledger/version/count and restoration. |
| R-48 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v10_replay_ignores_replaced_raw_decision` | unknown → 1 | Retain: keeps raw claims distinct from admitted records and explicitly checks recovery after losing the retained decision. |
| R-49 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v11_live_owner_and_invalid_requests` | unknown → 2 | Retain: active process lifetime has a finish marker in finally; public refusals and invocation counts assert sole actor ownership. |
| R-50 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v03_conditional_stages_cannot_be_omitted_or_weakened` | unknown → 4 | Retain: externally supplied conditional-review records are explicit fixtures for that boundary, not invented controller acceptance success. The closed stage matrix and references remain local to this contract test. |
| R-51 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v05_observation_uncertainty_and_prevented_correction` | unknown → 5 | Retain: independent_case gives each disposition scenario its own workspace; no fixture history leaks between the matrix rows. |
| R-52 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v04_explicit_ignored_input_and_each_task_document` | unknown → 2 | Retain: relevant ignored-path and frozen-document mutations are explicit and restored beside each refusal assertion. |
| R-53 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v10_real_publication_interruptions` | unknown → 3 | Retain: real child termination at existing publication seams tests replay ownership; phase-specific expectations stay beside each boundary. |
| R-54 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v11_real_launch_contention_has_one_actor` | unknown → 5 | Retain: marker synchronization and bounded communicate observe actual competing processes without replacing locking or admission. |
| R-55 | `test_actor_operations.py:ActorOperationsTest.test_acceptance_v12_documented_cli_and_changed_schema_boundary` | unknown → 1 | Retain: real CLI reservation/launch/observe/status supplies behavioral wiring evidence; its schema comparison is explicitly structural, not a substitute for the journey. |

### Other materially edited retained hotspots and current counts

- H-01 `controller.init_run`: CC 16→16, statements 66→67. One frozen
  required-review field remains beside scope/check authority. General input
  freezing extraction would touch initialization and revision authorities for
  one added field, with no necessary new collaborator. Retain existing owner.
- H-02 `controller.status_run`: CC 21→15, statements 21→7. The earlier staged
  CC 37 belongs to the pre-correction comparison, not these bytes. Shared facts
  and selection now own policy; status remains the response projection. Its
  completion-eligibility expression does not replace admission or reservation.
  Another response wrapper would add navigation without reducing authority.
- H-03 `controller.revise_inputs`: CC 29→29, statements 58→58. Review inventory
  and actual task-source identity belong to the existing owner-authorized
  revision bundle. A source-capture helper is feasible but one-consumer forwarding
  here would not reduce existing transaction complexity. Prior correction count
  and implementation history remain in the same transaction.
- H-04 `state.apply_ledger_update`: CC 30→30, statements 54→54,
  arguments 8→8. Adding candidate_path to the existing protected set strengthens
  the generic mutation boundary. Reworking its interface or mutation structure
  for that set member would be unrelated architecture churn.
- H-05 `reserve_operation`: CC 33→34, statements 39→48, arguments 7→7;
  its nested refusal CC 3→5. The supplied correction rationale's current CCs
  are independently confirmed. `_reservation_options` CC 29→40 and new
  `_reservation_evidence` CC 11 retain the real shared-policy/facts boundary,
  not mere metric redistribution: both status and locked reservation/refusals
  use them. Validation under the lock is a separate trust boundary; there is no
  second action selector. The current statement count is below target.
- H-06 `ActorOperationsTest.producer_run`: arguments 4→6, statements 19→24;
  nested initialize CC 2→9. Explicit task documents/reviews let the caller state
  frozen prerequisites. A generic options dict hides them, and copying the
  producer fixture would duplicate lifecycle authority. The bounded initializer
  patch installs data before real freezing; existing actor/check logic stays real.
  `checked_collection_run` adds the same explicit forwarding inputs (3→5 args,
  CC 1→1), a legitimate successive lifecycle boundary, not another policy owner.
- H-07 Mixed-budget test: unmatched-before CC→6 and statements→66. The
  implementer report's earlier 65 is superseded by R's actual 66. The one-history
  rationale in its R row is retained: separate seeded phases would lose the
  composition this test must exercise, and current launch/correction helpers
  already localize repetition. A standalone fixture DSL would hide transitions.
- H-08 `launch_operation` CC 13→14, `_admit_actor_outcome` 11→12,
  `_admit_collection` 25→26, `_validate_current_collection` 7→11 and
  manifest validator 17→19 retain their accumulated existing boundary roles
  described in their individual R rows; none acquires an unrelated lifecycle
  collaborator. Their useful alternatives were inspected rather than rejected
  solely because branch movement lowers a score.

### Shared-policy and test/harness consumer tracing

- Recovery facts originate in `_reservation_evidence`; selection is solely in
  `_reservation_options`. `status_run`, `reserve_operation` and its early/refusal
  path consume that pair. Active actor ownership and exhausted budget precede
  recovery; current review-correction authority precedes evidence-only retries.
  Reservation preserves separate request validation and mutation under its lock.
- `_acceptance_route` decides admission of the reviewer's claim;
  `_reservation_options` later decides executable next work with current occupancy,
  budget/readiness/freshness. These are intentional different boundaries, not
  duplicated recovery selectors. `_current_acceptance` invalidates old decision
  applicability after later evidence operations, so renewed evidence is not
  hostage to an older decision.
- `_merge_collection_findings` remains collection-owned reopening authority for
  changed evidence/exposure; `_disposition_for_finding` and
  `_acceptance_dispositions` approve and retain current dispositions. Context
  preparation and current-acceptance checks consume the same retained artifacts.
  Decision publication, invalid-result publication, correction reservation and
  explicit input revision are separate state transitions; no consumer invents
  acceptance from a ledger label or raw result. Generic ledger updates continue
  to reject controller-owned fields.
- State validators own data shape. Actor-result/task-manifest schemas describe
  the public serialized envelope; controller validators own current evidence,
  provenance and disposition policy. Separate validation at these boundaries is
  deliberate and does not justify a new schema-driven policy engine.
- The changed fake actor uses its existing mode file for scripted acceptance
  claims and authorized product edits; policy admission is never mocked. Each
  independent_case has its own disposable root. Within one lifecycle, overwriting
  the mode file is intentional sequential scenario setup, completed through real
  terminal observation before the next actor. Review-time waits have explicit
  finish markers. Interruption tests use the existing child launch helper and
  private publication hooks to reach real crash boundaries, then observe through
  public calls. The added acceptance-record seam reuses that harness instead of
  creating a second controller or launcher.
- Task prose, finding claims, supplied code and independent calculate(2)==4
  assertions are legitimate separate observation boundaries. The executable
  oracle is not computed by the production router. Generic finding/disposition
  defaults remain visible claims, not evidence of a model's semantic judgment.
- Existing reservation/revision tests now reject a seeded review label and retain
  check/repair/count invariants. The removed seeded review-budget journey is
  replaced by the real mixed-budget public history; no separate scenario family
  was dropped solely to remove a failure. Identical added negative controls in
  the existing two fixture classes do not create a new harness owner.
- Diagnostics: failed admission retains exception cause in the operation receipt,
  raw result/terminal paths and intervention. Freshness views intentionally mark
  stale proof without mutating the ledger; detailed rejection remains available
  at the admission/reservation boundary. No introduced high-impact cause-loss
  regression was established. This is not an assertion of globally ideal errors.

## BLOCKERS

NONE currently confirmed.

### Historical finding reconciliation

MNT-01 (stable alias for `maintainability-02.md`, blocker 1): **resolved for the
reviewed bytes**. The prior report used no producer ID; this report assigns this
alias without changing history or recycling an existing ID. The duplicated
status/reservation recovery decision was replaced by shared facts and one selector.
The reviewer reran the public lifecycle regression after actual separate acceptance
correction admission, tampering each retained candidate/check/collection/decision
artifact. Status and reservation consistently require intervention; refusals retain
ledger bytes, version and correction count. The pure selector table separately
checks active writer/verifier, budget, repair, readiness and authority precedence.
This is current correction evidence, not relying on the older ACCEPT label.

## NATIVE_EVIDENCE

Policies/owners: AGENTS.md, docs/development.md, preflight.md native inventory;
`tests/test_architecture.py` is CLEAN with no debt baseline. Metrics do not replace
any native obligation and this review does not change a gate's policy.

Whole repository snapshot before execution: 543 tracked/untracked nonignored files, canonical sorted path/SHA-256 map digest `e0d0fecc415402ba0a8f7038d2dbcec28ac35303d4abaa982eb5a07c557af887`; full map, exact index and pre-write status retained in `/tmp/T-005.1-source-review-before.json`. Every recorded file and the exact index were rechecked unchanged after execution. The Python measurement scope is only four files; it does not narrow native whole-project scope.

| Command / producer and owner | Governed scope and evidence | Result / applicability |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` / reviewer, required before handoff | All runtime scripts covered by executable CLEAN policy; `/tmp/source-review-architecture.log` | Fresh PASS: 4 tests, no skips. Structural architecture evidence only. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skills/task-orchestrator/tests python3 -m unittest test_actor_operations.RecoveryDecisionTest test_actor_operations.ActorOperationsTest.test_review_correction_proof_drift_requires_consistent_intervention` / reviewer focused reproduction | Corrected recovery selector plus real disposable public actor lifecycle; `/tmp/source-review-recovery.log` | Fresh PASS: 2 tests, no skips. Direct evidence for MNT-01 and precedence, not full functional acceptance. |
| `python3 tools/verify.py` / reviewer authorized native recovery; implementer/discovery own functional disposition | Whole documented aggregate: all discovered maintained suite roots, registry and installer drift. `/tmp/T-005.1-source-review-aggregate.log`; source inventory above binds current bytes. | Verification: 7 checks, 1 failed; see verbatim constituent outcomes below. No failed or skipped result is promoted to a pass. |

The fresh aggregate was justified by an applicability gap: the implementer's
`correction-02-checked-bytes.json` binds six affected files, not a complete
whole-project inventory. It was not rerun simply to populate report sections.
Its orchestrator constituent covers the whole owning suite; registry, root
architecture and profile constituents are not rerun again merely for sections.
The separately required reviewer architecture gate and focused correction
reproduction preceded the aggregate.

Historical native evidence is preserved: correction-02 actor suite reported
69 passes/no skips, aggregate reported 7 checks/1 failed, orchestrator 283 tests
with 6 failures/7 errors/20 skips, root 311 tests with 32 skips. The historical
failure-identity comparison reports no new identities against prior implementation,
which is not a newly executed baseline or successful supported-host qualification.
The current aggregate remains a separately recorded outcome, not an inferred pass.

Aggregate concise outcome, retained verbatim from the current raw log:

```text
CHECK: /usr/bin/python3 -m unittest discover -s skills/project-plan-verification/tests -p 'test_*.py' -v
Ran 3 tests in 0.100s
OK
CHECK: /usr/bin/python3 -m unittest discover -s skills/skill-creator/tests -p 'test_*.py' -v
Ran 13 tests in 0.675s
OK
CHECK: /usr/bin/python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p 'test_*.py' -v
Ran 4 tests in 0.001s
OK
CHECK: /usr/bin/python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py' -v
Ran 283 tests in 112.555s
FAILED (failures=6, errors=7, skipped=20)
CHECK: /usr/bin/python3 -m unittest discover -s tests -p 'test_*.py' -v
Ran 311 tests in 20.273s
OK (skipped=32)
CHECK: /usr/bin/python3 tools/check_contracts.py --root .
contract registry OK: 8 subsystem(s), 36 indexed plan ref(s)
CHECK: /usr/bin/python3 scripts/install_development_skills.py --check .
FAILED: /usr/bin/python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py' -v
Verification: 7 checks, 1 failed
```

## COVERAGE_AND_GAPS

- Completed: staged production/state/schema design, significant changed tests,
  embedded actor/interruption harness behavior, immediate collaborators and
  determining-rule consumers, all measured growth/new-function obligations,
  materially edited retained hotspots, historical finding reconciliation,
  current required architecture evidence and independent original-B comparison.
- Native non-passes/skips remain with their implementer/discovery owner; this
  maintainability ACCEPT neither waives them nor grants overall task acceptance.
  Discovery must assess current failure/skip exposure and supported-host proof,
  then the separate acceptance owner decides functional disposition. No unrelated
  platform repair is prescribed by this read-only maintainability review.
- Measurement gap: native Ruff omissions and unmatched symbols are unknown;
  embedded programs are inspected, not assigned invented function counts. Neither
  gap prevents this bounded semantic verdict. No rationale row is deferred.
- No permission/capability/budget stop curtailed bounded semantic coverage.
  No live sbx/provider/model execution, enforced edit isolation or reviewer
  semantic-judgment qualification was attempted or claimed.

## WARNINGS

- NONE beyond the explicit native evidence and scope limitations above. Those
  obligations are not hidden inside the optional warning cap.

## NEXT

First outstanding stage: `task-contract-registry-updater` for implemented acceptance
admission, decision/disposition artifacts, required-review inputs and shared recovery
routes. Then fresh independent `task-review-discovery`, including native failure/skip
assessment, then the separate `task-acceptance-review` decision. These stages remain
owed for these submitted bytes; this review does not execute, delegate or wait for
them. Corrected implementation/test bytes would re-enter affected conditional
stages before fresh discovery and acceptance.

Evidence is in the shared repository, so no isolated transfer occurred. For a
separate receiver, copy both siblings of B, I and R from this repository's
`.quality/reports/T-005.1-before-01.{json,txt}`,
`.quality/reports/T-005.1-correction-02-final.{json,txt}` and
`.quality/reports/T-005.1-review-source-04.{json,txt}` to those exact relative paths
in the receiving checkout; validate applicability there. Also explicitly transfer
the native raw logs and snapshot named above from `/tmp/` to the same named `/tmp/`
paths at the receiver, or retain an explicitly documented receiver evidence path.
Ignored evidence does not travel in a commit.

## REVIEWED

Staged implementation scope (current SHA-256 identities):

- `skills/task-orchestrator/scripts/controller.py`: `fa52547d9ccd578c26b5863d8136ba6c7643742927a4dbd9a4efcca53384fb85`.
- `skills/task-orchestrator/scripts/controller_state.py`: `7ab6e6aa48228a441a737b26803e2e303e6d79dacf63db739853502ec180d762`.
- `skills/task-orchestrator/tests/test_actor_operations.py`: `7fe7d492247be9d63ac4d6af467693c8fb013138f638705bb8e5283ff1b1d4e2`.
- `skills/task-orchestrator/tests/test_controller.py`: `c25037fcfc52ac84b3d3cfaee41bbe2027cb38bc8bb6846ae3a8716ce65a804b`.
- `skills/task-orchestrator/assets/actor-result.schema.json`: `97dd82508fbf718a26e8fc5aae0ae10778d66507bd1ba1b4899c526984828825`.
- `skills/task-orchestrator/assets/task-manifest.schema.json`: `12b99cb5c3b42c8e7b8c68585fcd9bb82f6997d29b2c6af1394e2e41b45fcf76`.

Immediate context: controller collection/check/publication/revision collaborators,
state validators and record consumers, `test_controller` fixture setup and its
reservation/revision cases. Task docs/index changes supplied context; earlier
reports and unrelated `.DS_Store` files were not attributed as implementation.
Boundary/policy sources: root AGENTS.md, docs/project-map.md,
docs/development.md, docs/contracts/index.json and task-orchestrator.json,
skills/task-orchestrator/references/architecture-map.md,
T-005.1 brief/verification/preflight/controller-contract/implementation-report/
correction-02, and tests/test_architecture.py. Existing references describing
acceptance as future work remain designated registry/reference-updater duties,
not a blocker in this pre-sync review.

## Exact Git status before report creation

```text
M  skills/task-orchestrator/assets/actor-result.schema.json
M  skills/task-orchestrator/assets/task-manifest.schema.json
A  skills/task-orchestrator/docs/tasks/T-005.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-005.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-005.1/correction-02.md
A  skills/task-orchestrator/docs/tasks/T-005.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-005.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-02.md
A  skills/task-orchestrator/docs/tasks/T-005.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-005.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-005/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-03.md
```

## Exact Git status after report creation

```text
M  skills/task-orchestrator/assets/actor-result.schema.json
M  skills/task-orchestrator/assets/task-manifest.schema.json
A  skills/task-orchestrator/docs/tasks/T-005.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-005.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-005.1/correction-02.md
A  skills/task-orchestrator/docs/tasks/T-005.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-005.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-02.md
A  skills/task-orchestrator/docs/tasks/T-005.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-005.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-005/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-03.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-04.md
```

Only this new report entry was added to Git status. The real index, all prior reports and implementation bytes were preserved. The only other repository writes were the fresh ignored R JSON/text pair, whose two paths were checked absent before execution.
