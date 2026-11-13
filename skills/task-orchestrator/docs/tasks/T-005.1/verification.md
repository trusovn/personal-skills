# Verification Design: T-005.1 — Admit separate acceptance and route recovery

Acceptance must come from a fresh reviewer and cover the exact current candidate
and required evidence. Its decision can authorize correction, return missing
proof to its owner, expose a blocker, or make the candidate eligible for the
completion consumer. It must preserve findings, history and the shared correction
budget. It must not complete the task or record known issues.

## Shared setup and evidence boundaries

Use one disposable Git repository, a prepared task and an external controller run
directory. Freeze the brief, verification, scope, checks, policy and flow through
the public lifecycle. Use the approved single-task sbx/YOLO authority and frozen
`gpt-6.1-sol` low/medium/high mapping. Keep existing owner work present. Use real
files, Git identity, command execution, local actor processes and storage reload.
Place invocation and execution counters outside evaluated candidate inputs.

Existing actor-operation coverage provides `producer_run`,
`checked_collection_run`, `collect`, public preflight, observed actor transport,
real check execution, drift and interruption setup. Existing state coverage owns
pure policy and reservation rules. Reuse or extend this setup where distinct
evidence is missing. The old raw-acceptance test must change with the contract;
the test-only successor decision and seeded approved-disposition fixtures cannot
prove T-005.1 admission. Test names, placement and helpers remain implementation
choices under repository authority.

For V-01–V-11, exercise the public controller boundary, including its single
observe → admit → publish path. Scripted actors may supply outputs, observed
session events and authorized product edits. Do not seed successful acceptance,
its admission, or review-driven correction authority. Start refusal rows from
otherwise valid prerequisites; vary only the named guard. V-01 supplies the
successful control. Snapshot authoritative state/version/count, task and owner
files, retained artifacts and invocation counters at each decisive boundary.
Invalid requests preserve them. Valid operational failures may retain failure
evidence and interventions; separate diagnostics do not grant progress.

The implementer supplies execution evidence for V-01–V-12. Fresh independent
discovery corroborates those cases against submitted bytes, independently
exercises acceptance, correction, drift, disposition continuity and replay, and
inspects the decisive records/logs for the remaining rows. Separate acceptance
decides whether that evidence is sufficient. Applicable maintainability and
registry stages retain their own gates; the aggregate belongs to the implementer,
with discovery reconciling failures and skips. Run the owning focused gate first,
then the orchestrator suite; apply architecture/contract checks and the repository
aggregate when cross-cutting. Correct through the focused gate before broadening.

Local scripts prove controller decisions, retained provenance and wiring. They
do not establish real sbx containment, provider/model identity, edit isolation or
semantic review quality. Policy cases below require review of the supplied
context and dispositions as well as executable admission controls; no automated
defect classifier is required. Live qualification remains T-006-owned. No live,
networked or expensive checks are authorized by this design. Schema/document
checks are structural evidence, separate from behavioral execution.

## Test cases

### V-01 — Fresh acceptance admits an eligible decision without completing

**Situation:** Public preflight and implementation are terminal. Real required
checks pass. A fresh independent collector has rerun the checks and supplied
complete current collection. Applicable conditional review evidence is present.

**Action:** Reserve acceptance/acceptance_reviewer, launch through the existing
adapter, submit a supported terminal accept decision and observe it. Reload status.

**Expected result:** The assignment prohibits implementation, correction,
collection takeover and tracker writes. It supplies frozen task/verification
authority, current candidate/check/collection records, runtime limits, applicable
conditional reviews, findings/dispositions and known-issue history when present.
The role uses the frozen model mapping and an explicitly adapter-observed fresh
session, distinct from implementation and collection. ART-009 is admitted with
rationale and evidence references. ART-002 exposes the current decision and
eligibility for T-005.2. Count remains zero; no extra corrections are required.
No task completion, tracker write, commit or dependency release occurs.

**Why test this:** An implementation that always refuses or treats collection as
acceptance must not satisfy the negative cases.

**How to check:** Capture the real launch prompt/assignment, observed session and
terminal receipt, retained decision path/digest and reloaded status. Inspect
referenced evidence bytes, execution counters and unchanged task/owner files.
This proves supplied context and mechanical admission, not reviewer judgment.

### V-02 — Identity, independence and terminality cannot come from actor claims

**Situation:** Establish V-01 prerequisites for each row. All unmodified result
fields, observations and evidence remain valid.

| Case | Action / decisive change | Expected result |
|---|---|---|
| V-02a | Submit a different run identity. | No current acceptance admission. |
| V-02b | Submit a different task identity. | No current acceptance admission. |
| V-02c | Submit a different operation or assignment key. | No decision admitted for the reserved assignment. |
| V-02d | Submit an implementer role/stage. | No acceptance authority or implementation launch. |
| V-02e | Submit a collector role/stage or its decision as acceptance. | No acceptance authority; collection remains a separate role. |
| V-02f | Submit obsolete input identity. | No decision admitted under obsolete inputs. |
| V-02g | Submit another policy identity. | No decision admitted under another policy. |
| V-02h | Submit another flow identity/revision. | No decision admitted under another flow. |
| V-02i | Submit another candidate identity. | No decision admitted for the current candidate. |
| V-02j | Omit explicit session identity. | No acceptance provenance inferred from prose. |
| V-02k | Claim a session different from the adapter observation. | No current acceptance admission. |
| V-02l | Supply invented provenance without a supporting adapter observation. | Actor-supplied provenance grants no authority. |
| V-02m | Have the adapter observe a reused implementation session. | Independence fails even when result and observed session agree. |
| V-02n | Have the adapter observe a reused correction session. | Independence fails against correction history. |
| V-02o | Have the adapter observe a reused collector session. | Independence fails against collection history. |
| V-02p | Launch a new acceptance assignment using an earlier acceptance session. | Fresh-assignment requirement fails. |
| V-02q | Submit malformed structured output. | Retain diagnostic output; admit no decision authority. |
| V-02r | Produce no required result. | Preserve the missing-result condition; admit no decision authority. |
| V-02s | Change an assignment value's JSON type while retaining a similar printed value. | Exact assignment validation fails. |
| V-02t | Claim accept despite a failed adapter/process outcome. | No eligible accept; retain the actual failure. |

**Why test this:** Each binding prevents an unrelated actor, prior session or
failed process from accepting the candidate.

**How to check:** Drive actual observation/admission with controlled local actor
outputs and adapter session events. Do not mock the admission decision. Inspect
retained diagnostics, operation outcome and reloaded status. Keep all earlier
sessions in history for V-02m–V-02p. Live and unknown terminality use V-11.

### V-03 — An accept claim cannot replace required retained evidence

**Situation:** Start from V-01's current evidence. For each row leave every other
prerequisite valid. Where a state is seeded, label it as a negative evidence input;
normal producers are controller inspection, checks, collection and review stages.

| Case | Action / evidence condition | Expected result |
|---|---|---|
| V-03a | Remove the actual retained candidate artifact while preserving a passed ledger label. | No eligible accept; identify missing candidate proof. |
| V-03b | Remove the retained required check artifact while preserving the pass claim. | No eligible accept; route missing check proof to its owner. |
| V-03c | Remove the retained collection artifact while preserving its ledger label. | No eligible accept; route missing collection proof to collection. |
| V-03d | Replace a retained candidate artifact behind its existing reference. | Identity/integrity mismatch cannot become current acceptance. |
| V-03e | Replace required check evidence or its bound execution/log bytes. | Retained pass labels cannot conceal invalid check proof. |
| V-03f | Replace retained collection or its independent rerun proof. | No eligible accept from replaced collection/provenance. |
| V-03g | Supply an actual failed required check and an accept claim. | Failure remains failed; no eligible accept or waiver. |
| V-03h | Supply blocked required evidence and an accept claim. | Blocked remains distinct from passed. |
| V-03i | Leave a required check/stage not run and claim accept. | Not-run remains distinct; route the unfinished obligation. |
| V-03j | Supply inconclusive required review evidence and claim accept. | No eligible accept; inconclusive is not a pass. |
| V-03k | Omit an applicable required conditional review, such as maintainability, registry or discovery evidence. | Missing required stage remains visible; acceptance cannot absorb its role. |
| V-03l | Select or claim a weaker profile that removes a required stage. | No requirement removed and no eligible accept. |
| V-03m | Supply a decision without rationale or required evidence references. | No supported decision admitted from an unsupported verdict. |
| V-03n | Claim all findings resolved while retained unresolved findings lack disposition. | Findings remain outstanding; the claim cannot create eligibility. |

**Why test this:** Reviewer prose and ledger labels must not launder absent,
failed or replaced proof.

**How to check:** Exercise reservation and terminal admission as applicable.
Rows blocked before launch must prove that refusal and zero actor invocations;
reach admission separately by changing evidence after a valid launch. Inspect
actual retained files, digests/provenance and truthful status, not just the result
schema. For V-03g execute a real failing check. Negative seeded states prove guard
behavior only; V-01 and V-08 prove normal evidence production. Conditional rows
apply only when the frozen task workflow requires the stage.

### V-04 — Relevant drift invalidates acceptance before, during and after review

**Situation:** Complete current collection for a valid candidate. Use separate
histories for the following changes; do not combine dimensions unnecessarily.

| Case | Action / change | Expected result |
|---|---|---|
| V-04a | Change relevant tracked product bytes before acceptance reservation. | Bound evidence is stale; no acceptance launch. |
| V-04b | Add or change a relevant untracked file before reservation. | No acceptance based on the former candidate. |
| V-04c | Change evaluated configuration before reservation. | Evidence for the prior configuration is stale. |
| V-04d | Change the index while keeping worktree bytes equal. | Index identity drift prevents current acceptance. |
| V-04e | Change HEAD while keeping evaluated worktree bytes equal. | HEAD identity drift prevents current acceptance. |
| V-04f | Change an explicitly evaluated ignored input. | Its prior evidence is stale under inherited relevance rules. |
| V-04g | Change frozen task brief or verification source bytes without an authorized revision. | Task-input drift is exposed; old acceptance authority cannot be used. |
| V-04h | Synchronize a live acceptance process, then change relevant tracked bytes before terminal observation. | Admission detects in-review drift; the accept claim is not eligible. |
| V-04i | Admit valid acceptance, then change an evaluated file and replay observation. | Retained decision history may replay, but current eligibility becomes stale; replay cannot rebind it. |
| V-04j | Change only irrelevant ignored generated output. | Inherited relevance handling remains intact; otherwise valid acceptance still admits. |

**Why test this:** Valid evidence for yesterday's state must not accept today's
candidate, and irrelevant outputs must not force needless correction.

**How to check:** Use real Git/filesystem mutations and reload status. Separate
brief and verification mutations within V-04g. Use process synchronization for
V-04h, not a seeded stale label. Retain old records and prove no accidental check
rerun or correction charge. The independent dimensions plus one synchronized
in-review case prove identity coverage and admission timing without their full
Cartesian product. Authorized input/policy/flow revision is covered in V-09.

### V-05 — Dispositions follow supplied context without waiving obligations

**Situation:** Supply findings with stable IDs and evidence, requirements,
trigger/consequence, affected boundary, separate impact and exposure, mitigations
and relevant consumer/maintenance context. Required evidence passes except where
the row explicitly states otherwise.

**Action:** Supply a supported separate reviewer decision for each row and inspect
its admission, retained disposition and permitted next action.

| Case | Finding / decision context | Expected result |
|---|---|---|
| V-05a | Demonstrated AC or required-gate violation, within correction authority. | Blocking finding; bounded correction route, never known-issue eligibility. |
| V-05b | Confirmed material operating risk despite passing checks/ACs. | Fix-now disposition with contextual exposure/consequence; green checks do not erase it. |
| V-05c | Confirmed material maintainability risk with a credible same-kind maintenance consequence. | Fix-now disposition can be justified without a formal future ticket; reviewer preference alone is insufficient. |
| V-05d | Bounded non-material defect; required evidence passes; compatible consumers need no hidden workaround. | Acceptance-approved known issue retains bounded rationale, acceptance provenance, evidence, compatible consumers, follow-up and reassessment conditions. No tracker write occurs here. |
| V-05e | Preference, polish or speculative improvement only. | Observation; no new correction obligation or charge. |
| V-05f | Ordinary uncertainty or unproved minor concern. | Stated reasonable assumption/observation; no invented defect or automatic blocker. |
| V-05g | Missing decisive required proof, without a correction-eligible confirmed blocker. | Missing-evidence disposition, not defect deferral; request the evidence owner without an implementation launch. |
| V-05h | Credible material risk remains unresolved and current authority cannot settle it. | No eligible accept or bounded known issue; retain the precise blocker and required decision. |
| V-05i | Propose a deferral that waives a required AC or check. | No eligible accept from the proposed waiver. |
| V-05j | Propose a deferral of demonstrated material risk, including low-likelihood catastrophic consequences. | No eligible accept; low likelihood cannot erase material impact. |

**Why test this:** A preference must not consume correction budget, and a known
issue must not hide a failure, proof gap or material risk.

**How to check:** Use the cited installed acceptance policy's disposition table
and mixed-condition precedence as the review oracle. Check structured consistency
and retained evidence through real admission. Independently inspect that prompts,
documents and disposition examples preserve the policy. These checks prove
mechanical handling of supplied supported/contradictory decisions; scripted
reviewers do not prove that a live model classifies defects correctly. Reuse the
admitted V-05d decision as the starting history for V-06, rather than seeding approval.

### V-06 — Repeated review preserves findings and justified dispositions

**Situation:** Produce a finding through collection and its approved disposition
through separate acceptance. Use public evidence-only recollection and fresh
acceptance for each later history. Retain prior records throughout.

| Case | Action / later history | Expected result |
|---|---|---|
| V-06a | Report the same finding with unchanged relevant evidence and exposure. | Stable ID and approved disposition survive; history and acceptance provenance are retained without duplicate current findings. |
| V-06b | Omit a retained unresolved finding from the later collector report. | Omission does not resolve or delete it; acceptance still accounts for it. |
| V-06c | Try to reopen an approved disposition with no new relevant evidence or changed exposure. | Existing approval is preserved; repeated review alone grants no correction authority. |
| V-06d | Supply new relevant evidence for the finding. | Reopening records that evidence and reason, with previous disposition/history preserved. |
| V-06e | Change the finding's exposure while preserving its evidence. | Reopening records changed exposure and reason, retaining prior approval/history. |
| V-06f | Repeat the same approved known issue and supply existing known-issue history. | Preserve stable identity and approval provenance; no broadened deferral, duplicate issue or tracker write. |

**Why test this:** Review repetition or omission must not silently erase findings
or create endless correction for an unchanged approved issue.

**How to check:** Compare current findings and historical snapshots after reload,
including supplied context in subsequent collector and acceptance prompts. Keep
evidence/exposure constant for preservation rows; change only the named dimension
for reopening rows. Do not use the older test-only disposition seed as proof of
acceptance authority. Semantic justification remains separately reviewed.

### V-07 — Recovery goes to the authorized owner and preserves unfinished work

**Situation:** Start from supported current evidence and a separate acceptance
decision. Establish each route's required authority; remove it only in refusal rows.
For V-07b/V-07c, the reviewer identifies a substantive proof gap in evidence that
met the mechanical launch prerequisites. Do not bypass reservation with an
already missing check or incomplete collection record.

| Case | Action / condition | Expected result |
|---|---|---|
| V-07a | Admit a supported blocking review finding within implementation scope. | Authorize bounded `review_findings` correction; no charge until reservation. |
| V-07b | Admit a missing required check-proof decision without a confirmed blocker. | Route to checks, charge zero, launch no implementation actor. |
| V-07c | Admit a collection coverage-gap decision without a confirmed blocker. | Route to fresh collection, charge zero, launch no implementation actor. |
| V-07d | Combine a correction-eligible blocker with another unfinished evidence row. | Correction takes precedence; retain the unfinished row, reason and evidence owner for separate recovery. |
| V-07e | Combine that blocker with missing authority for its correction. | Preserve blocker and evidence rows; intervene instead of granting correction. |
| V-07f | Encounter broken check infrastructure without repair authority. | Infrastructure blocker remains distinct from product failure; no invented product-fix or repair authority. |
| V-07g | Perform an explicitly authorized inherited environment repair. | Its correction reservation charges the shared budget; readiness becomes invalid and fresh public preflight is required before ordinary implementation resumes. |
| V-07h | Encounter an unavailable required review capability with no explicit source-guided review authorization. | Profile blocks with exact missing capability/next action; source presence is not installation. |
| V-07i | Record chat acknowledgement of a blocker without a recovery decision. | Retain intervention/response history; acknowledgement grants no repair, policy revision or retry authority. |

**Why test this:** Evidence recovery must not consume product corrections, and
operational failures or chat responses must not create permissions.

**How to check:** Exercise actual reservation/status routing and evidence-only
rerun/recollection, not only output labels. Show V-07b/V-07c recover the named
proof with unchanged product bytes and count. Induce an actual local tool failure
for V-07f. V-07g may supply explicit upstream repair authority through its inherited
contract; this setup proves consumption of that authority, not automatic diagnosis
or authority creation. Observe invalid readiness, refused premature implementation
and successful fresh preflight. V-07i uses the existing intervention API and no
external send. Stale evidence recovery has its separate identity oracle in V-04.

### V-08 — A review decision causes actual correction and fresh acceptance

**Situation:** Initialize a prepared task whose small product has a deterministic
behavioral defect outside the initial passing check's coverage. Task authority
also requires the behavior that collection will examine. No owned acceptance or
correction authority is seeded.

**Action and expected checkpoints:**

1. Run real implementation through public preflight/reservation/launch/observation.
   Inspect its candidate and execute the frozen checks: they really pass. Execute
   the uncovered behavior to show the defect, then have fresh collection rerun
   the frozen checks and publish a supported finding against the task requirement.
2. Launch a distinct fresh acceptance reviewer. Admit a correction decision tied
   to that finding and current candidate. Only this decision authorizes
   `review_findings`; collection alone has not done so. Count is still zero.
3. Reserve correction: count becomes one exactly once. With unknown occupancy,
   launch a fresh correction session. The actor changes actual product code.
   Observe the previously defective behavior now pass, in addition to changed
   file bytes. Retain the original finding, decision and check records.
4. Inspect the new candidate, execute new required checks and launch fresh
   collection with its own reruns and history. Prior candidate evidence cannot
   establish current coverage. Collection documents the finding's resolution.
5. Launch fresh separate acceptance and admit a supported accept. Current
   evidence refers to the corrected candidate; the finding's history remains.
   Stop at eligibility with count one, without completing or recording a tracker.

**Why test this:** Seeded successor state, file markers or canned passing labels
could otherwise conceal a disconnected correction path.

**How to check:** Preserve public lifecycle inputs/outputs, session receipts,
execution logs/counters and before/after behavior observations. The defect probe
must fail for the specified behavior, not harness setup, and pass after correction.
Scripted actors can execute the edits and return controlled reviews; controller
admission, storage and check execution remain real. V-02–V-07 cover the remaining
finite guards; this journey proves their central producer/consumer interaction.

### V-09 — All correction routes share three cycles across replay and revision

**Situation:** Start cycle-zero work through the public lifecycle. Use actual
failed checks and admitted separate review decisions for their correction routes.
Explicit inherited authority may set up repair; it must not seed ART-009 success.

**V-09a — Mixed routes reach exhaustion:**

1. A real failed required check permits `check_failed` reservation. It charges
   correction one. Correct, then inspect and produce fresh evidence.
2. A supported separate review decision permits `review_findings` reservation.
   It charges correction two. Perform actual correction and fresh evidence work.
3. An authorized `environment_repair` reservation charges correction three.
   Repair invalidates readiness; run fresh preflight before resuming ordinary work.
4. Across these checkpoints replay each reservation, launch and observation;
   reload from disk. No duplicate actor, correction charge or count reset occurs.
   Evidence-only checks, collection and acceptance charge nothing.
5. At a safe boundary admit an explicitly authorized input/policy/flow revision
   through the inherited revision path. Verify each affected identity is invalidated,
   readiness clears, history/count remain, and fresh preflight is needed. Revision
   cannot create a second cycle zero or resurrect old acceptance by repointing it.
6. Execute a required check that fails at count three, then request a fourth
   correction. Refuse `corrections_exhausted` without launch or count change.
   Retain work/evidence/history and a precise active-chat intervention next action.

**V-09b — Passing at the limit remains eligible:** In a separate history, satisfy
the requirements after the third authorized correction, then produce fresh checks,
collection and separate accept. Eligibility is allowed at count three. Exhaustion
is a limit on further corrections, not an obligation to reject passing work.

**Why test this:** Separate counters, reset-on-revision or unconditional
exhaustion blockers would violate the shared budget and early-accept policy.

**How to check:** Count durable reservations and actual actor invocations, not
loop iterations. Reload after reservation and terminal admission. Exercise stale
pre-revision assignments and old bound evidence against current state. Use public
admission for review authority; the historical test-only successor seed does not
prove this route. V-01 and V-08 cover acceptance before budget exhaustion. Pure
state-policy checks may supplement but cannot replace this lifecycle evidence.

### V-10 — Admission replay retains one decision and conservative ownership

**Situation:** Reach acceptance using current evidence and a real local actor.

| Case | Action / interruption | Expected result |
|---|---|---|
| V-10a | Admit a decision, replace raw actor output with a different verdict, reload and observe again. | Return the retained admitted decision; no reinterpretation, version/count change, new disposition or actor launch. |
| V-10b | Interrupt after durable launch intent but before a conclusive terminal observation. | Reload preserves uncertain ownership and evidence; no duplicate launch or successor actor. Expose a precise stop/observation action. |
| V-10c | Interrupt with complete known terminal result before decision publication. | Reload may admit that same result once, or conservatively block with evidence location and next action. Never relaunch the actor or publish unsupported eligibility. |
| V-10d | Interrupt after decision publication but before the caller receives acknowledgement. | Reload returns the retained decision once; no duplicated findings, routes, charges or history effects. |

**Why test this:** A retry must not decide again from altered raw claims or lose
track of an actor that might still own the task.

**How to check:** Interrupt a real local coordinator at meaningful existing
durable boundaries and reload storage with another controller instance. Inspect
decision records, ledger/version/count, operation ownership, diagnostics and
invocation counters. Preserve raw and admitted artifacts separately. This proves
process interruption handling, not power-loss recovery or a tamper-resistant run
directory. Current eligibility after later task drift is separately checked by
V-04i; retained historical admission never overrides current identity checks.

### V-11 — Invalid requests and live or unknown owners cannot advance

**Situation:** Establish valid frozen authority and the prerequisites for the
requested operation. Use a synchronized real actor for live-ownership rows.

| Case | Action / condition | Expected result |
|---|---|---|
| V-11a | Reserve with stale expected version. | Refuse without authoritative state/version/count or task-file change. |
| V-11b | Reuse an operation key with a conflicting payload. | Refuse without a second assignment, launch or charge. |
| V-11c | Request `review_findings` correction before a supported acceptance decision. | Refuse; collection findings alone grant no correction authority. |
| V-11d | Request a correction reason different from the admitted authorization. | Refuse without charge or launch. |
| V-11e | Submit result bytes while acceptance remains live, then request progression/retry. | Result bytes do not establish terminality; retain sole owner, no eligible accept or successor actor. |
| V-11f | Leave acceptance terminality unknown, then reload and retry. | Persist blocker, work and evidence; no new actor or eligibility. |
| V-11g | Retain unresolved collector-rerun ownership before acceptance. | Acceptance cannot bypass the inherited unknown-ownership guard. |
| V-11h | Make competing acceptance launch attempts for the same reservation. | Existing serialization permits at most one actor invocation; no second admission route. |

**Why test this:** A plausible result, duplicate request or claimed review reason
must not bypass authority and exclusive operation ownership.

**How to check:** Compare exact authoritative bytes, task/owner files, count and
invocations for invalid API requests. For live/unknown rows inspect real process
observations and persisted ownership after reload; operational blockers may be
retained. Coordinate V-11h at the actual controller locking boundary. No new
parallel-coordination feature is required. V-01/V-08 provide successful controls.

### V-12 — The successor contract describes the implemented acceptance slice

**Situation:** Implementation and its focused evidence are available for review.

**Action:** Compare the task-local `controller-contract.md`, actual API/CLI,
assignment/result schemas, artifacts and reports with the cases above.

**Expected result:** The contract identifies actual callable and CLI spelling,
decision/disposition paths and digests, exact identity/eligibility checks,
correction and evidence-owner routes, replay/refusal behavior and T-005.2's
consumer seam. It distinguishes admitted eligibility from completion and names
remaining coordinator recording, recording validation and final completion work.
Reports give local results, skips/failures and inherited limits. Registry-stage
evidence records only the implemented ART-009/IF-003 and ART-002 delta, preserving
ART-003/005/006 and IF-001/002 accounting without claiming completion.

**Why test this:** T-005.2 must consume an exact implemented boundary, not infer
capabilities from a passed collection, planned schema or report label.

**How to check:** Replay the documented public spellings on a disposable prepared
run; compare real outputs and artifacts with the contract. Check representative
valid and invalid assignment/results against both runtime and changed schemas.
Schema acceptance alone proves no behavioral outcome. Independently reconcile
the handoff and registered slice with V-01–V-11 evidence. Preserve inherited
aggregate failures/skips truthfully; live sbx/provider/model execution and semantic
review quality remain unqualified and T-006-owned. Do not execute T-005.2 here.

## Coverage summary

All links below refer to [the brief's acceptance criteria](brief.md#work-and-acceptance-criteria).
The brief supplies no risk-row IDs. Child IDs in each table are separate required
cases; ranges include every listed child.

| Promise from the brief | AC | Required cases |
|---|---|---|
| [Fresh separate role, complete context, exact observed provenance](brief.md#work-and-acceptance-criteria) | AC-01 | V-01; V-02a–V-02t; V-07h; V-11e–V-11h |
| [Only current retained required evidence can support admission](brief.md#work-and-acceptance-criteria) | AC-02 | V-01; V-03a–V-03n; V-04a–V-04j; V-09a; V-12 |
| [Contextual dispositions preserve findings and waive no obligation](brief.md#work-and-acceptance-criteria) | AC-03 | V-05a–V-05j; V-06a–V-06f; V-07d–V-07e; V-10a |
| [Correction, evidence recovery, repair and intervention retain their authority and shared budget](brief.md#work-and-acceptance-criteria) | AC-04 | V-01; V-07a–V-07i; V-08; V-09a–V-09b; V-11a–V-11d |
| [Real review-driven correction, replay, exhaustion and unchanged-state refusals](brief.md#work-and-acceptance-criteria) | AC-05 | V-08; V-09a–V-09b; V-10a–V-10d; V-11a–V-11h; V-01 |
| [Exact completion-consumer interface and truthful qualification limits](brief.md#work-and-acceptance-criteria) | AC-06 | V-12; V-01; V-08 |

## Source and revision

Source brief: skills/task-orchestrator/docs/tasks/T-005.1/brief.md
Source brief revision: 1
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

Normative detail: [parent P-01–03/P-06 and ownership](../T-005/brief.md#coverage-and-closure),
[ART-009 / IF-003 / FLOW-001–003 / INV-001–008](../../local-harness-orchestration-plan.md),
[owner-confirmed direction](../../direction-single-task-sbx.md),
[approved disposition authority](../../correction-and-disposition-options.md#existing-skill-and-approved-source-update),
[installed acceptance policy](../../../../../.agents/skills/task-implementation-flow/task-acceptance-review/SKILL.md#contextual-disposition-and-coordinator-owned-deferrals),
and [accepted T-004 lifecycle/identity/replay contract](../T-004/controller-contract.md).
The current installed policy governs disposition details; historical installation
wording in the disposition notes does not replace the available installation.
