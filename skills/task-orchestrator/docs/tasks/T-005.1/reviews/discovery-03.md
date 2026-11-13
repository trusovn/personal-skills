# Task Review Discovery Report: T-005.1 — separate acceptance and recovery

| Field | Value |
|---|---|
| Producing stage | installed project-local task-review-discovery |
| Coverage completeness | complete — 92 retained ledger rows, all locally required cases corroborated; qualification limits below |
| Discovery iteration | third discovery; correction-04 recovery |
| Created at | 2026-11-13T15:45:21.930763+00:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report path | skills/task-orchestrator/docs/tasks/T-005.1/reviews/discovery-03.md |
| Task brief | ../brief.md, revision 1 |
| Verification / context | ../verification.md revision 1; ready ../preflight.md, Decision context; ../controller-contract.md |
| Current submission | ../correction-04.md plus implementation-report and corrections 02/03 |

This report publishes evidence only, with no acceptance verdict, approved deferral or advancement. Separate acceptance owns the decision. It applies only to the reviewed bytes and does not review or authenticate itself.

## 1. Discovery provenance

Fresh independent session `/root/t0051_discovery`; no reviewed production, schema, test, fixture, setup or authority bytes authored. Only this report is written in the repository. Active installation resolved to `.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`; its report template and same-installation `.agents/skills/testing-discipline/SKILL.md` were read. No source substitution, installation refresh, delegation, install, network or live check.

HEAD `c20300c44f2469f393214ece2752ae417ee072cd`. Staged binary diff SHA-256 `5f66197788fa97cc7ccc56e9964735a9b3710391de8e9676ba4590f372d7c4f4`. All 32 evaluated worktree hashes in `/tmp/T-005.1-schema-byte-identities.json` independently MATCH. Index entries/blob identities and worktree are separately retained in `/tmp/T-005.1-discovery-03/before.json` and `dirty-identities.json`; staged content matches the prior discovery/acceptance identity. The correction intentionally leaves README and two tests different from index and adds runner/setup changes. Matching staged content alone is not treated as matching worktree.

## 2. Findings and continuity

No findings.

Historical F-01 (misleading source/operator/README completion/admission descriptions) was resolved by prior correction-03 and acceptance-01. Current D03-06 traces actual admission/recovery to source skill, operator guide, README, schemas, registry and successor contract; sibling descriptions remain consistent. Historical MNT-01 remains resolved: current shared selection/proof-drift regressions pass (D03-02), and runtime bytes are unchanged. No previous finding ID is recycled; missing evidence was never labeled a production defect.

V-12/G-SCHEMA was blocked by missing validator; now actual Draft 2020-12 +/- validation executes on both schemas. G-REG lacked owner closure; registry-02 now supplies current independent NO_UPDATE_NEEDED. G-NATIVE previously failed 13 Linux/macOS-boundary tests; targeted correction and current native aggregate recover those failures, retaining explicit skips. No authority case/revision was changed to obtain these results.

## 3. Completeness ledger

92 exact retained identities: 86 authority cases plus the six proof/gate rows carried by acceptance-01 and correction-04. Prior passes are navigation, not current proof. Each row below has current independent behavioral execution, static evidence where appropriate, or attributed current conditional-stage/gate evidence. Setup is the existing disposable prepared Git task and external run directory, real local actor/check processes, frozen authority, current candidate, independent collection and fresh acceptance sessions. Refusal matrices vary only the named guard from otherwise valid prerequisites; invalid requests preserve authoritative bytes/count. Negative seeded states prove guards; V-01/V-08 produce the successful evidence through public admission. Scripted policy inputs do not qualify model judgment.

Independent command mapping (all methods in `test_actor_operations.ActorOperationsTest` unless stated):

- V-01: `test_acceptance_v01_fresh_current_decision_without_completion`.
- V-02: `test_acceptance_v02_identity_terminality_matrix; V-08 also checks actual correction-session reuse`.
- V-03: `test_acceptance_v03_retained_artifact_integrity_matrix; test_acceptance_v03_required_status_and_unsupported_claims; test_acceptance_v03_conditional_stages_cannot_be_omitted_or_weakened; V-09 actual failed checks`.
- V-04: `test_acceptance_v04_drift_matrix_and_replay; test_acceptance_v04_in_review_drift_and_irrelevant_output; test_acceptance_v04_explicit_ignored_input_and_each_task_document`.
- V-05: `test_acceptance_v05_disposition_policy_and_v07_routes; test_acceptance_v05_v06_approved_known_issue_continuity; test_acceptance_v05_observations_and_v07_evidence_only_recovery; test_acceptance_v05_observation_uncertainty_and_prevented_correction`.
- V-06: `test_acceptance_v05_v06_approved_known_issue_continuity`.
- V-07: `test_acceptance_v05_disposition_policy_and_v07_routes; test_acceptance_v05_observations_and_v07_evidence_only_recovery; test_acceptance_v05_observation_uncertainty_and_prevented_correction; V-08/V-09; D03-02 inherited capability/infrastructure tests`.
- V-08: `test_acceptance_v08_actual_review_driven_code_correction`.
- V-09: `test_acceptance_v09_mixed_budget_revision_and_eligibility_at_limit`.
- V-10: `test_acceptance_v10_replay_ignores_replaced_raw_decision; test_acceptance_v10_real_publication_interruptions`.
- V-11: `test_acceptance_v11_live_owner_and_invalid_requests; test_acceptance_v11_real_launch_contention_has_one_actor; V-05/V-08 authority refusals; D03-02 collector-rerun ownership`.
- V-12: `test_acceptance_v12_documented_cli_and_changed_schema_boundary (actual CLI, runtime and two executable Draft 2020-12 schema +/- controls)`.


| Row ID | AC / invariant | Explicit material case | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| V-01 | AC-01/02/04/05/06 | Fresh separate acceptance with full frozen context and current independent collection. | Fresh observed reviewer; exact evidence; count zero; eligibility without completion. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02a | AC-01 | Submit a different run identity. | No current acceptance admission. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02b | AC-01 | Submit a different task identity. | No current acceptance admission. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02c | AC-01 | Submit a different operation or assignment key. | No decision admitted for the reserved assignment. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02d | AC-01 | Submit an implementer role/stage. | No acceptance authority or implementation launch. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02e | AC-01 | Submit a collector role/stage or its decision as acceptance. | No acceptance authority; collection remains a separate role. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02f | AC-01 | Submit obsolete input identity. | No decision admitted under obsolete inputs. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02g | AC-01 | Submit another policy identity. | No decision admitted under another policy. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02h | AC-01 | Submit another flow identity/revision. | No decision admitted under another flow. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02i | AC-01 | Submit another candidate identity. | No decision admitted for the current candidate. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02j | AC-01 | Omit explicit session identity. | No acceptance provenance inferred from prose. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02k | AC-01 | Claim a session different from the adapter observation. | No current acceptance admission. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02l | AC-01 | Supply invented provenance without a supporting adapter observation. | Actor-supplied provenance grants no authority. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02m | AC-01 | Have the adapter observe a reused implementation session. | Independence fails even when result and observed session agree. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02n | AC-01 | Have the adapter observe a reused correction session. | Independence fails against correction history. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02o | AC-01 | Have the adapter observe a reused collector session. | Independence fails against collection history. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02p | AC-01 | Launch a new acceptance assignment using an earlier acceptance session. | Fresh-assignment requirement fails. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02q | AC-01 | Submit malformed structured output. | Retain diagnostic output; admit no decision authority. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02r | AC-01 | Produce no required result. | Preserve the missing-result condition; admit no decision authority. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02s | AC-01 | Change an assignment value's JSON type while retaining a similar printed value. | Exact assignment validation fails. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-02t | AC-01 | Claim accept despite a failed adapter/process outcome. | No eligible accept; retain the actual failure. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03a | AC-02 | Remove the actual retained candidate artifact while preserving a passed ledger label. | No eligible accept; identify missing candidate proof. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03b | AC-02 | Remove the retained required check artifact while preserving the pass claim. | No eligible accept; route missing check proof to its owner. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03c | AC-02 | Remove the retained collection artifact while preserving its ledger label. | No eligible accept; route missing collection proof to collection. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03d | AC-02 | Replace a retained candidate artifact behind its existing reference. | Identity/integrity mismatch cannot become current acceptance. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03e | AC-02 | Replace required check evidence or its bound execution/log bytes. | Retained pass labels cannot conceal invalid check proof. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03f | AC-02 | Replace retained collection or its independent rerun proof. | No eligible accept from replaced collection/provenance. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03g | AC-02 | Supply an actual failed required check and an accept claim. | Failure remains failed; no eligible accept or waiver. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03h | AC-02 | Supply blocked required evidence and an accept claim. | Blocked remains distinct from passed. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03i | AC-02 | Leave a required check/stage not run and claim accept. | Not-run remains distinct; route the unfinished obligation. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03j | AC-02 | Supply inconclusive required review evidence and claim accept. | No eligible accept; inconclusive is not a pass. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03k | AC-02 | Omit an applicable required conditional review, such as maintainability, registry or discovery evidence. | Missing required stage remains visible; acceptance cannot absorb its role. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03l | AC-02 | Select or claim a weaker profile that removes a required stage. | No requirement removed and no eligible accept. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03m | AC-02 | Supply a decision without rationale or required evidence references. | No supported decision admitted from an unsupported verdict. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-03n | AC-02 | Claim all findings resolved while retained unresolved findings lack disposition. | Findings remain outstanding; the claim cannot create eligibility. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04a | AC-02 | Change relevant tracked product bytes before acceptance reservation. | Bound evidence is stale; no acceptance launch. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04b | AC-02 | Add or change a relevant untracked file before reservation. | No acceptance based on the former candidate. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04c | AC-02 | Change evaluated configuration before reservation. | Evidence for the prior configuration is stale. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04d | AC-02 | Change the index while keeping worktree bytes equal. | Index identity drift prevents current acceptance. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04e | AC-02 | Change HEAD while keeping evaluated worktree bytes equal. | HEAD identity drift prevents current acceptance. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04f | AC-02 | Change an explicitly evaluated ignored input. | Its prior evidence is stale under inherited relevance rules. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04g | AC-02 | Change frozen task brief or verification source bytes without an authorized revision. | Task-input drift is exposed; old acceptance authority cannot be used. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04h | AC-02 | Synchronize a live acceptance process, then change relevant tracked bytes before terminal observation. | Admission detects in-review drift; the accept claim is not eligible. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-04 bounded lifecycle cleanup | pass — current independent public-boundary execution matches oracle |
| V-04i | AC-02 | Admit valid acceptance, then change an evaluated file and replay observation. | Retained decision history may replay, but current eligibility becomes stale; replay cannot rebind it. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-04j | AC-02 | Change only irrelevant ignored generated output. | Inherited relevance handling remains intact; otherwise valid acceptance still admits. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05a | AC-03 | Demonstrated AC or required-gate violation, within correction authority. | Blocking finding; bounded correction route, never known-issue eligibility. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05b | AC-03 | Confirmed material operating risk despite passing checks/ACs. | Fix-now disposition with contextual exposure/consequence; green checks do not erase it. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05c | AC-03 | Confirmed material maintainability risk with a credible same-kind maintenance consequence. | Fix-now disposition can be justified without a formal future ticket; reviewer preference alone is insufficient. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05d | AC-03 | Bounded non-material defect; required evidence passes; compatible consumers need no hidden workaround. | Acceptance-approved known issue retains bounded rationale, acceptance provenance, evidence, compatible consumers, follow-up and reassessment conditions. No tracker write occurs here. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05e | AC-03 | Preference, polish or speculative improvement only. | Observation; no new correction obligation or charge. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05f | AC-03 | Ordinary uncertainty or unproved minor concern. | Stated reasonable assumption/observation; no invented defect or automatic blocker. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05g | AC-03 | Missing decisive required proof, without a correction-eligible confirmed blocker. | Missing-evidence disposition, not defect deferral; request the evidence owner without an implementation launch. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05h | AC-03 | Credible material risk remains unresolved and current authority cannot settle it. | No eligible accept or bounded known issue; retain the precise blocker and required decision. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05i | AC-03 | Propose a deferral that waives a required AC or check. | No eligible accept from the proposed waiver. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-05j | AC-03 | Propose a deferral of demonstrated material risk, including low-likelihood catastrophic consequences. | No eligible accept; low likelihood cannot erase material impact. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-06a | AC-03 | Report the same finding with unchanged relevant evidence and exposure. | Stable ID and approved disposition survive; history and acceptance provenance are retained without duplicate current findings. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-06b | AC-03 | Omit a retained unresolved finding from the later collector report. | Omission does not resolve or delete it; acceptance still accounts for it. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-06c | AC-03 | Try to reopen an approved disposition with no new relevant evidence or changed exposure. | Existing approval is preserved; repeated review alone grants no correction authority. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-06d | AC-03 | Supply new relevant evidence for the finding. | Reopening records that evidence and reason, with previous disposition/history preserved. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-06e | AC-03 | Change the finding's exposure while preserving its evidence. | Reopening records changed exposure and reason, retaining prior approval/history. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-06f | AC-03 | Repeat the same approved known issue and supply existing known-issue history. | Preserve stable identity and approval provenance; no broadened deferral, duplicate issue or tracker write. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-07a | AC-01/03/04 | Admit a supported blocking review finding within implementation scope. | Authorize bounded `review_findings` correction; no charge until reservation. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-07b | AC-01/03/04 | Admit a missing required check-proof decision without a confirmed blocker. | Route to checks, charge zero, launch no implementation actor. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-07c | AC-01/03/04 | Admit a collection coverage-gap decision without a confirmed blocker. | Route to fresh collection, charge zero, launch no implementation actor. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-07d | AC-01/03/04 | Combine a correction-eligible blocker with another unfinished evidence row. | Correction takes precedence; retain the unfinished row, reason and evidence owner for separate recovery. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-07e | AC-01/03/04 | Combine that blocker with missing authority for its correction. | Preserve blocker and evidence rows; intervene instead of granting correction. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-07f | AC-01/03/04 | Encounter broken check infrastructure without repair authority. | Infrastructure blocker remains distinct from product failure; no invented product-fix or repair authority. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-02 inherited authority/infrastructure/ownership | pass — current independent public-boundary execution matches oracle |
| V-07g | AC-01/03/04 | Perform an explicitly authorized inherited environment repair. | Its correction reservation charges the shared budget; readiness becomes invalid and fresh public preflight is required before ordinary implementation resumes. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-02 inherited authority/infrastructure/ownership | pass — current independent public-boundary execution matches oracle |
| V-07h | AC-01/03/04 | Encounter an unavailable required review capability with no explicit source-guided review authorization. | Profile blocks with exact missing capability/next action; source presence is not installation. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-02 inherited authority/infrastructure/ownership | pass — current independent public-boundary execution matches oracle |
| V-07i | AC-01/03/04 | Record chat acknowledgement of a blocker without a recovery decision. | Retain intervention/response history; acknowledgement grants no repair, policy revision or retry authority. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-08 | AC-04/05/06 | Real initial implementation and passing checks, behavior defect, collector finding, separate correction, actual product edit, fresh checks/collection/acceptance. | calculate(2)==4 fails before correction and passes after; one charge; fresh observed correction and acceptance sessions. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-09a | AC-02/04/05 | Actual check failure, review correction and authorized repair across replay/reload/revision; fourth request. | Charges 1/2/3 once; readiness invalidates; revision preserves history/count; fourth correction refuses. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-09b | AC-02/04/05 | Satisfy requirements after the third authorized correction. | Current separate acceptance remains eligible at count three. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-10a | AC-03/05 | Admit a decision, replace raw actor output with a different verdict, reload and observe again. | Return the retained admitted decision; no reinterpretation, version/count change, new disposition or actor launch. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-10b | AC-03/05 | Interrupt after durable launch intent but before a conclusive terminal observation. | Reload preserves uncertain ownership and evidence; no duplicate launch or successor actor. Expose a precise stop/observation action. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-04 bounded lifecycle cleanup | pass — current independent public-boundary execution matches oracle |
| V-10c | AC-03/05 | Interrupt with complete known terminal result before decision publication. | Reload may admit that same result once, or conservatively block with evidence location and next action. Never relaunch the actor or publish unsupported eligibility. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-04 bounded lifecycle cleanup | pass — current independent public-boundary execution matches oracle |
| V-10d | AC-03/05 | Interrupt after decision publication but before the caller receives acknowledgement. | Reload returns the retained decision once; no duplicated findings, routes, charges or history effects. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-04 bounded lifecycle cleanup | pass — current independent public-boundary execution matches oracle |
| V-11a | AC-01/04/05 | Reserve with stale expected version. | Refuse without authoritative state/version/count or task-file change. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-11b | AC-01/04/05 | Reuse an operation key with a conflicting payload. | Refuse without a second assignment, launch or charge. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-11c | AC-01/04/05 | Request `review_findings` correction before a supported acceptance decision. | Refuse; collection findings alone grant no correction authority. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-11d | AC-01/04/05 | Request a correction reason different from the admitted authorization. | Refuse without charge or launch. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below | pass — current independent public-boundary execution matches oracle |
| V-11e | AC-01/04/05 | Submit result bytes while acceptance remains live, then request progression/retry. | Result bytes do not establish terminality; retain sole owner, no eligible accept or successor actor. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-04 bounded lifecycle cleanup | pass — current independent public-boundary execution matches oracle |
| V-11f | AC-01/04/05 | Leave acceptance terminality unknown, then reload and retry. | Persist blocker, work and evidence; no new actor or eligibility. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-04 bounded lifecycle cleanup | pass — current independent public-boundary execution matches oracle |
| V-11g | AC-01/04/05 | Retain unresolved collector-rerun ownership before acceptance. | Acceptance cannot bypass the inherited unknown-ownership guard. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-02 inherited authority/infrastructure/ownership; D03-04 bounded lifecycle cleanup | pass — current independent public-boundary execution matches oracle |
| V-11h | AC-01/04/05 | Make competing acceptance launch attempts for the same reservation. | Existing serialization permits at most one actor invocation; no second admission route. | implementation-report / correction-04; corresponding V-row | D03-01; method mapping below; D03-04 bounded lifecycle cleanup | pass — current independent public-boundary execution matches oracle |
| V-12 | AC-02/06 | Actual CLI, schemas, successor contract and source references | Truthful supported slice; valid/invalid executable schema controls | implementation-report / correction-04; corresponding V-row | D03-01 real CLI + both schema controls; D03-05 independent validator; D03-06 source/contract trace | pass — historical schema blocker recovered with actual declared-draft +/- validation; behavior and documentation separately corroborated |
| V-12-CLI | AC-02/06 | Public reserve/launch/observe/status | Prepared run with current checks/collection; eligible without completion | correction-04 / current conditional reports | D03-01 V-12 real CLI | pass — current CLI journey |
| V-12-DOC | AC-06 / F-01 sibling trace | Source skill, operator guide, README, controller-contract and registry | Trace callable spellings, paths, digests, recovery and absent completion against runtime | correction-04 / current conditional reports | D03-06 and registry-02 producer closure | pass — historical F-01 correction remains corroborated |
| V-12-SCHEMA / G-SCHEMA | AC-02/06 | Both declared Draft 2020-12 schemas | Valid actor/result and manifest accepted; missing decision / unsupported required-review rejected | correction-04 / current conditional reports | D03-01 V-12 and D03-05 schema.py | pass — prior missing-validator blocker recovered |
| MNT-01 | Maintainability continuity | Shared action selection and retained-proof drift | Status and refusal agree; all four candidate/check/collection/decision proof changes preserve authority | correction-04 / current conditional reports | D03-02 RecoveryDecisionTest + proof-drift regression; maintainability-05 unchanged responsibility confirmation | pass — remains resolved |
| G-REG | Required conditional stage | Independent current registry/reference closure | Owner stage must account for implemented contracts and changed setup references | correction-04 / current conditional reports | registry-02 NO_UPDATE_NEEDED; D03-06 trace; D03-08 canonical validation | pass — prior absent owner result now present, current and attributed |
| G-NATIVE | Native obligations | Prior 13 failure identities and visible skip scope | Corrected deterministic targets pass; full current aggregate zero failures; skip limits explicit | correction-04 / current conditional reports | D03-07 30 tests; D03-09 saved current implementer gate + supplementary analyzer evidence | pass — historical failed gate recovered; macOS skips remain outside local proof |

## 4. Adversarial state, lifecycle and cleanup

D03-01 exercises exact assignment types, independent observed session freshness, zero/one/conflicting owner states, retained evidence/status and tracked/untracked/config/index/HEAD/task-document drift; real failed checks, correction cycles 1/2/3, fourth refusal and successful acceptance at count three; repeated replay retains one decision.

D03-03 independently executes two simultaneous findings: blocking correction plus another unfinished evidence row; actual correction and fresh recollection omitting the second finding; subsequent resolved/known-issue acceptance accounts for both. It then rewrites conditional proof and its receipt digest coherently after acceptance; retained decision anchoring makes eligibility false without mutating the ledger. Digest consistency alone is not described as tamper resistance against actors with controller-record write access.

Old diagnostic sources/controls were preserved. Copies of adversarial.py and lifecycle_cleanup.py differ only in output-directory constants (`/tmp/T-005.1-discovery-03/`). Their assertions and setup were inspected before execution. D03-03 observes all actor PIDs/groups absent and no fixture-path descendants before teardown in both histories. D03-04 runs five lifecycle tests, producing eight teardown records including three independent interruption histories. Bounded four-second polling confirms no observed PID, process group or fixture descendant survives. Terminal worker publication follows bounded stdout-reader join; coordinator `communicate(timeout=5/8)` drains inherited stdout/stderr pipes. Complete terminal receipts and bounded successful communicate/cleanup establish pipe release; no fixture process survives. The synchronization waits observe explicit waiting/checkpoint/gate files, rather than inferring completion from sleep.

## 5. Independent probes and command results

All commands run from repository root; raw logs remain in `/tmp/T-005.1-discovery-03/`. No repository fixture or test was added. Transfer these external sources, inputs and raw logs explicitly if moving workspaces.

| ID | Exact command / probe | Purpose / observation | Result / cleanup |
|---|---|---|---|
| D03-01 | `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k acceptance -v` | Every current acceptance method; real CLI and valid/invalid schema instances included | 19 passed, zero skips, 33.364s; targets.log; disposable state and lifecycle cleanup |
| D03-02 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skills/task-orchestrator/tests .venv/bin/python -m unittest test_actor_operations.RecoveryDecisionTest test_actor_operations.ActorOperationsTest.test_review_correction_proof_drift_requires_consistent_intervention test_actor_operations.ActorOperationsTest.test_collection_v11b_missing_executable_retains_infrastructure_blocker test_actor_operations.ActorOperationsTest.test_v07_missing_each_prerequisite_reaches_specific_blocker test_actor_operations.ActorOperationsTest.test_collection_v10c_live_rerun_serializes_and_unresolved_terminal_blocks test_actor_operations.ActorOperationsTest.test_collection_v11_capability_blocker_and_public_request_refusals -v` | Shared selector/proof drift, missing executable, prerequisites/capability, unresolved rerun ownership | 6 passed, zero skips, 3.583s; regressions.log |
| D03-03 | `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python /tmp/T-005.1-discovery-03/adversarial.py` | Repeated two-finding real lifecycle; coherent receipt tamper; runtime decision +/-; saves current observed result controls | passed; adversarial.log; bounded no-survivor assertions |
| D03-04 | `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python /tmp/T-005.1-discovery-03/lifecycle_cleanup.py` | Interruptions, contention, live owner, in-review drift and collector rerun cleanup | 5 passed, zero skips, 5.815s; lifecycle-cleanup.log/.json; all eight teardown records clean |
| D03-05 | `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python /tmp/T-005.1-discovery-03/schema.py` | Independent Draft202012Validator 4.25.1, declared schema draft checked; positive and deliberate negative for both schemas | both valid ACCEPT; actor missing decision REJECT via required, manifest unsupported discovery stage REJECT via enum; schema.log, retained +/- JSON |
| D03-06 | Targeted reads of controller.py 1945–2168, state validators, schemas; source SKILL.md 90–150, operator-guide.md 50–100, README 450–485; controller-contract; docs/contracts/index.json → task-orchestrator.json and foundation-tools.json; dirty diffs and installer | Expected ART-009/IF-003/ART-002 maps to actual admission/current proof/route; declared and discoverable slice agrees; task authority unchanged | passed static trace; no completion/tracker/provider claim; read-only |
| D03-07 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skills/task-orchestrator/tests .venv/bin/python -m unittest test_verification_runner.VerificationSandboxFailClosedTests test_controller.ControllerInspectionIntegrationTest -v` | Independently rerun corrected deterministic sandbox and real inspection command/record/drift/replay boundaries | 30 passed, zero skips, 4.131s; native-targets.log; disposable state |
| D03-08 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`; `.venv/bin/python tools/check_contracts.py --root .`; `git diff --check` | Canonical CLEAN architecture and registry shape/path/index; whitespace | 4 passed/no skips; 8 subsystems/37 refs; clean diff. architecture.log/contracts.log. Structural evidence only |
| D03-09 | `.venv/bin/python tools/verify.py` — existing implementer-owned gate, consumed, not rerun | Current full native scope reconciled below | seven checks, zero failed; raw /tmp/T-005.1-schema-aggregate.log; independently byte-bound |
| D03-10 | `.venv/bin/python /tmp/T-005.1-discovery-03/measurement-identities.py` (SHA-256/base64 snapshots against original Git/current files) | Maintainability evidence current applicability | original B 12 snapshots match 6a13008d239d22ad48909258e00edd809953973d; I/R three each match current bytes; prior R four snapshots self-consistent and both runtime sources match current; measurement-identities.log |

D03-05 uses real current observed actor output from D03-03; its invalid sibling removes decision. Manifest controls copy retained minimal prepared manifest with explicit maintainability/registry; invalid sibling supplies discovery, forbidden by the schema. D03-01 separately validates the actual CLI-produced actor output and actual prepared run manifest, rejecting missing decision/unsupported. `check_schema` alone is structural; actual acceptance/rejection above is the executable contract evidence. JSON instance and schema hashes are retained in schema.log. No missing-library skip remains: missing jsonschema fails the maintained owning suite, and requirements-dev.txt pins repository-only verification setup.

## 6. Aggregate-gate reconciliation

Gate command: `.venv/bin/python tools/verify.py`. Owner/stage: implementer, as preflight native table and verification design assign; discovery independently reconciles and admits its current recovery evidence. Status: passed for executed local checks; skipped cases remain unqualified. No discovery gate rerun: user/coordinator explicitly directed consumption of existing current gate once identities/provenance are verified and no new changes/failure/gap justify duplication. This is attributed implementation evidence, not a claimed independent full-suite execution. Fresh targeted rows D03-01..07 are clean and complete; no selected adversarial row remains. `/tmp/T-005.1-discovery-03/ledger-reconciliation.json` preserves all 92 rows/results and the gate action.

Independently inspected raw aggregate: project-plan-verification 3, skill-creator 13, task-brief-designer 4; orchestrator 283 with 20 real macOS skips; root 311 with 32 analyzer skips; registry 8 subsystems/37 refs; profile drift 112 compared paths, match=true. Seven checks, zero failed. All 32 evaluated identities independently match current source; no implementation change followed the gate. Historical discovery-02 aggregate (six failures/seven errors) remains historical failure evidence, superseded for current native execution by the recovered gate rather than rewritten. Independent D03-07 specifically executes the 30 corrected deterministic/inspection cases including all 13 former failure identities.

The 32 analyzer skips are separately exercised by coordinator command `PYTHONDONTWRITEBYTECODE=1 .quality/envs/Linux-aarch64-cpython-3.14.4-79dbf22b5bc1/bin/python -m unittest discover -s tests -p test_maintainability.py -v`: 34 passed, zero skips, 7.792s. Raw `/tmp/T-005.1-coordinator-analyzer-tests.log` independently inspected (including skipped-name coverage); this is current coordinator evidence, not this reviewer's execution. The remaining 20 macOS containment skips are explicit host limits outside this task's local sbx/YOLO mechanical proof. Their real tests/host guards are unchanged; supported-host execution denial remains failure. They are not passed behavior, a deferral or live qualification. T-006 owns supported real sbx/provider/model proof.

## 7. Scope, authority and conditional-stage admission

Task production/schema/docs implement the acceptance/recovery slice; parent/successor briefs and task index are owner context, not completed successor work. Current correction scope is three existing tests plus root requirements/setup/docs/.gitignore, authorized by later user instruction for durable recurring schema capability. No runtime/schema bytes changed from discovery-02; no scenarios were removed or authority revised. Unrelated three .DS_Store files are preserved, including byte hashes in before.json. No scope overlap or unexplained production ownership was found.

Controller inspection now isolates only its sandbox invocation builder; real commands/Git/log/record/drift/replay assertions remain. Deterministic sandbox tests explicitly model platform/availability and compare against literal expected argv; actual unsupported-host rejection and real macOS tests remain. No duplicate fixture family or runtime abstraction was added. Installer inspected: orchestrator is outside DEVELOPMENT_SKILL_SOURCES and jsonschema is repository-only, so no development-profile runtime dependency/list/guide edit is owed.

Conditional evidence: maintainability-05 is independent installed-skill execution, current ACCEPT with architecture PASS and complete reviewer-owned original-B comparison R `.quality/reports/T-005.1-review-installed-05.{json,txt}`. Its three reviewed test sources equal I and current bytes, errors empty/full profile. Prior maintainability-04 remains expressly source-guided evidence for unchanged original production/test responsibilities; it is not relabeled installed execution. Preserve original R-01–R-55/H-01–H-08 responsibilities as scoped by maintainability-05; revised R-55 and new R-56/R-57 locally account for V-12 and corrected sandbox/inspection setup. Unknown original matches, embedded subprocess and advisory measurement limits remain explicit. No unresolved applicable maintainability blocker was found; no general rereview performed.

registry-02 is the separate installed updater's current NO_UPDATE_NEEDED result, accounting for later README/setup references and unchanged public runtime contracts; canonical registry validation passes. It did not edit registry/reference bytes. This closes the prior owner-attribution evidence gap without discovery taking over that stage.

Exact pre-write status is below. All existing nonignored files (including owner .DS_Store), HEAD, index entries and staged diff were checked unchanged before creation. Separate index/worktree blob hashes are in dirty-identities.json; before.json binds their pre-review snapshot. Only this report is created. No plan/tracker/production/test/prior report is edited or staged.

Before:

```text
 M .gitignore
MM README.md
M  docs/contracts/index.json
M  docs/contracts/task-orchestrator.json
 M docs/development.md
 M docs/project-map.md
M  skills/task-orchestrator/SKILL.md
M  skills/task-orchestrator/assets/actor-result.schema.json
M  skills/task-orchestrator/assets/task-manifest.schema.json
A  skills/task-orchestrator/docs/tasks/T-005.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-005.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-005.1/correction-02.md
A  skills/task-orchestrator/docs/tasks/T-005.1/correction-03.md
A  skills/task-orchestrator/docs/tasks/T-005.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-005.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-02.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-03.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-04.md
A  skills/task-orchestrator/docs/tasks/T-005.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-005.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-005/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/references/architecture-map.md
M  skills/task-orchestrator/references/operator-guide.md
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
MM skills/task-orchestrator/tests/test_actor_operations.py
MM skills/task-orchestrator/tests/test_controller.py
 M skills/task-orchestrator/tests/test_verification_runner.py
?? .DS_Store
?? docs/.DS_Store
?? requirements-dev.txt
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-005.1/correction-04.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/acceptance-01.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/discovery-02.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-05.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/registry-01.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/registry-02.md
```

After (verified against actual post-creation status):

```text
 M .gitignore
MM README.md
M  docs/contracts/index.json
M  docs/contracts/task-orchestrator.json
 M docs/development.md
 M docs/project-map.md
M  skills/task-orchestrator/SKILL.md
M  skills/task-orchestrator/assets/actor-result.schema.json
M  skills/task-orchestrator/assets/task-manifest.schema.json
A  skills/task-orchestrator/docs/tasks/T-005.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-005.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-005.1/correction-02.md
A  skills/task-orchestrator/docs/tasks/T-005.1/correction-03.md
A  skills/task-orchestrator/docs/tasks/T-005.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-005.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-01.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-02.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-03.md
A  skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-04.md
A  skills/task-orchestrator/docs/tasks/T-005.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-005.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-005/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/references/architecture-map.md
M  skills/task-orchestrator/references/operator-guide.md
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
MM skills/task-orchestrator/tests/test_actor_operations.py
MM skills/task-orchestrator/tests/test_controller.py
 M skills/task-orchestrator/tests/test_verification_runner.py
?? .DS_Store
?? docs/.DS_Store
?? requirements-dev.txt
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-005.1/correction-04.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/acceptance-01.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/discovery-02.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/discovery-03.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-05.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/registry-01.md
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/registry-02.md
```

## 8. Questions, unchecked work and residual risks

No locally required row remains failed, blocked or unchecked. No new question or production correction owner. Real macOS containment, provider/model identity, enforced edit isolation and semantic judgment are unqualified; scripted actors qualify mechanical controller wiring only. Full-access controller-record tamper resistance and power-loss recovery are not established or claimed. Existing qualification boundaries and T-006 ownership remain unchanged; no approved deferral is recorded here.

## 9. Coverage completeness and next route

Complete current local evidence: 92/92 rows pass with their respective independent/producer attribution; no findings. Next owner: separate installed task-acceptance-review. Supply this report, current staged plus unstaged scoped diff, brief/verification rev1, ready preflight Decision context, controller-contract, correction-04, prior acceptance/discovery continuity, maintainability-04/05 and measurement pairs, registry-02, retained raw logs/custom controls. Acceptance owns evidence admission/disposition and any advancement; do not execute T-005.2 here.

## 10. Discovery continuation

- Iteration/current identity: discovery-03 correction-04; HEAD/staged diff and current 32-path worktree map above, unchanged after probes.
- Coverage rows: V-01=pass, V-02a=pass, V-02b=pass, V-02c=pass, V-02d=pass, V-02e=pass, V-02f=pass, V-02g=pass, V-02h=pass, V-02i=pass, V-02j=pass, V-02k=pass, V-02l=pass, V-02m=pass, V-02n=pass, V-02o=pass, V-02p=pass, V-02q=pass, V-02r=pass, V-02s=pass, V-02t=pass, V-03a=pass, V-03b=pass, V-03c=pass, V-03d=pass, V-03e=pass, V-03f=pass, V-03g=pass, V-03h=pass, V-03i=pass, V-03j=pass, V-03k=pass, V-03l=pass, V-03m=pass, V-03n=pass, V-04a=pass, V-04b=pass, V-04c=pass, V-04d=pass, V-04e=pass, V-04f=pass, V-04g=pass, V-04h=pass, V-04i=pass, V-04j=pass, V-05a=pass, V-05b=pass, V-05c=pass, V-05d=pass, V-05e=pass, V-05f=pass, V-05g=pass, V-05h=pass, V-05i=pass, V-05j=pass, V-06a=pass, V-06b=pass, V-06c=pass, V-06d=pass, V-06e=pass, V-06f=pass, V-07a=pass, V-07b=pass, V-07c=pass, V-07d=pass, V-07e=pass, V-07f=pass, V-07g=pass, V-07h=pass, V-07i=pass, V-08=pass, V-09a=pass, V-09b=pass, V-10a=pass, V-10b=pass, V-10c=pass, V-10d=pass, V-11a=pass, V-11b=pass, V-11c=pass, V-11d=pass, V-11e=pass, V-11f=pass, V-11g=pass, V-11h=pass, V-12=pass, V-12-CLI=pass, V-12-DOC=pass, V-12-SCHEMA / G-SCHEMA=pass, MNT-01=pass, G-REG=pass, G-NATIVE=pass.
- Findings: no new findings. F-01 prior open → resolved acceptance-01, current D03-06 sibling trace supports continuity; MNT-01 prior resolved → current D03-02 confirms. Correction owner prior implementer completed; evidence owner fresh discovery; disposition owner separate acceptance. No authority revision.
- Recovered rows: V-12/V-12-SCHEMA/G-SCHEMA prior blocked → current independent +/- validator pass; G-REG prior blocked → registry-02 current producer closure; G-NATIVE prior fail → current implementer aggregate + independent repaired targets pass, explicit skips/limits preserved. Capability/setup owner completed recurring dependency; stage evidence owners remain distinct.
- Preparation: brief rev1, verification rev1, ready preflight Decision context, controller-contract; implementation-report/corrections02–04; maintainability-04 source-guided + maintainability-05 installed, registry-02, prior discovery01/02 and acceptance-01.
- Reviewer regressions: D03-01..07 commands above; /tmp/T-005.1-discovery-03/{adversarial.py,lifecycle_cleanup.py,schema.py}, retained controls/logs; no repository regression files created.
- Aggregate: current implementer `.venv/bin/python tools/verify.py` passed, seven checks/zero failures; discovery reconciles current identities and targeted recovery, no duplicate broad rerun; historical failed gate preserved, 20 macOS skips unqualified; coordinator supplemental analyzer 34 passed/no skips.
- Next: one separate fresh acceptance decision; this report does not advance work.
