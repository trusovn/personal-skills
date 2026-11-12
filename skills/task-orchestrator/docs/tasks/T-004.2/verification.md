# Verification Design: T-004.2 — Admit independent collection and prove bounded correction

Collection must describe the current checked candidate and include its own check
reruns. It must retain findings without deciding acceptance. A real failed check
must lead to bounded correction, new checks and fresh collection. Drift, uncertain
ownership and budget exhaustion must leave retained evidence and a safe next action.

## Shared setup and evidence boundaries

Use a disposable Git repository, an external controller run directory and one
prepared task with frozen brief, verification, scope, checks and explicit sbx/YOLO
authority. Supply a small product with a deterministic behavioral check that can
fail and pass as its code changes. Keep an independent execution counter outside
candidate inputs. Keep owner work present and unchanged. Required review roles
must be available under the applicable project-local workflow; source presence
alone does not establish installation or permission to substitute a role.

Reuse the actor-operation setup and producer precedents in
`tests/test_actor_operations.py`, including `producer_run`, actual subprocess
checks, public preflight, terminal observation and correction accounting. Reuse
state-policy coverage in `tests/test_controller_state.py`. Extend those fixtures
only where distinct evidence below is missing. This identifies existing setup,
not required new test names, file placement or implementation structure.

For V-01–V-11, exercise public controller operations, real storage and reload.
Scripted local actors may control responses, session events and product edits;
they must not seed candidate, check or collection success. Compare ledger bytes,
state version, correction count, product/owner bytes, retained records, logs and
invocation counters at the relevant checkpoints. Invalid requests must preserve
authoritative state and task files; valid operational failures may persist
failure evidence, blockers and next actions. Diagnostics are not authoritative
progress. V-01 is the valid admission control for refusal cases.

The implementer owns execution evidence for V-01–V-12. Fresh independent discovery
must corroborate those cases against the submitted bytes, inspect decisive logs
and independently exercise the admission, drift, correction and reload boundaries;
an implementation report alone is insufficient. Separate acceptance reconciles
that discovery and the applicable maintainability/registry evidence. This design
does not perform any of those reviews or decide implementation acceptance.

Local actors prove controller wiring and observed local sessions, not semantic
review quality, actual sbx containment or provider/model identity. T-006 retains
the live pilot. No live, model or network check is authorized here. Schema and
document checks are structural evidence only.

## Test cases

### V-01 — Fresh collection admits current evidence, not acceptance

**Situation:** Public preflight and implementation have completed. Controller
inspection and actual required checks pass for the current candidate.

**Action:** Reserve and launch a fresh collector using the existing actor bridge.
Capture its assignment. Have it request new check executions through T-004.1's
controller runner, inspect the supplied task/product and submit terminal collection.
Observe through `observe_operation`.

**Expected result:** The assignment supplies frozen authority, candidate, current
check evidence, prior findings/dispositions and applicable review requirements.
It prohibits implementation edits. The report binds to adapter-observed task,
operation, role, session, inputs and candidate. Its reruns have new operation
identities and logs, not replayed implementation checks. ART-006 and ART-002 expose
explicit coverage, gaps and findings. Valid complete coverage enables the handoff
to separate acceptance, without acceptance, completion, commit or dependency release.
Collection/check production does not charge a correction.

**Why test this:** A plausible report or copied pass could otherwise substitute
for independent current evidence.

**How to check:** Integrate real local actor transport and command execution.
Inspect captured assignment, observed session receipts, execution counter, check
records/logs, admitted report and reloaded status. Compare the collector session
with implementation/correction sessions. Assert product/owner bytes unchanged.
This proves supplied inputs and enforced bindings, not a model's judgment quality.

### V-02 — Report identity and terminality cannot be invented

**Situation:** Use V-01 prerequisites. Change only the named dimension for each
case; other fields, reruns and authority remain valid.

| Case | Action / decisive input | Expected result |
|---|---|---|
| V-02a | Submit another task ID. | No current collection admission. |
| V-02b | Submit another operation ID. | No current collection admission. |
| V-02c | Submit an implementation or acceptance role. | No collection or acceptance authority admitted. |
| V-02d | Claim a session different from adapter observation. | No current collection admission; actor prose is not provenance. |
| V-02e | Bind the report to another candidate. | No current collection admission. |
| V-02f | Use obsolete input, policy or flow binding, each separately. | No current collection admission under obsolete authority. |
| V-02g | Supply invented observed provenance. | No current collection admission from invented identity. |
| V-02h | Reuse an observed implementation session; repeat with a correction session. | Both histories fail independence admission. |
| V-02i | Supply malformed report; separately omit the required result. | Retain raw output or its absence diagnostically; no successful coverage. |
| V-02j | Publish result bytes while the collector is still live; separately leave terminality unknown. | Neither establishes terminal collection; ownership blocks another actor and acceptance progression. |
| V-02k | Put a final acceptance decision in the collector result. | Collector cannot supply acceptance authority or complete the task. |

**Why test this:** Each binding is an independent route to admitting somebody
else's result or an unfinished review.

**How to check:** Exercise actual observation/admission with controlled actor
outputs and observed receipts. Do not replace the admission function with a mock.
Inspect diagnostic retention, current coverage and status after reload. For invalid
API requests assert unchanged authoritative bytes; malformed terminal outcomes may
record a blocked outcome. V-02j needs a synchronized real process, not just a
nonterminal string. The matrix varies one binding at a time to expose each guard.

### V-03 — Coverage requires fresh, current reruns

**Situation:** The implementer's checks pass and a collector is otherwise valid.

| Case | Action / input | Expected result |
|---|---|---|
| V-03a | Reference only the implementer's pass. | No successful collection coverage; expose missing independent reruns. |
| V-03b | Replay an earlier completed verify assignment and cite it as a fresh rerun. | Replay executes nothing and cannot satisfy fresh independent coverage. |
| V-03c | Run a fresh check for a different candidate or frozen input identity. | It cannot cover the current collection. |
| V-03d | Omit required rerun evidence or report a required coverage gap. | Preserve the gap and missing coverage; do not promote it to passed. |
| V-03e | Execute a required rerun that actually fails, while the report claims pass. | Retain the real failed result; no successful coverage or acceptance progression. |
| V-03f | Supply current reruns but omit explicit coverage, gaps or findings fields, each separately. | Incomplete ART-006 cannot establish successful coverage. |

**Why test this:** Independent collection must detect failures rather than echo
an earlier success or hide required omissions.

**How to check:** Use the real controller runner and persisted command outcomes.
For V-03e induce a deterministic command failure without unrelated candidate drift;
V-07 separately covers drift. Inspect execution counts, candidate/input bindings,
coverage, gaps and truthful next actions. Pair with V-01's new successful reruns.
These cases prove mechanical evidence admission, not semantic completeness of prose.

### V-04 — Findings retain identity, disposition and history

**Situation:** First collection reports a finding with a stable ID, evidence and
requirement/context. Later collection receives that history. Where an approved
disposition is needed, seed it explicitly as upstream acceptance-owned state;
this task must not manufacture its approval.

| Case | Action / history | Expected result |
|---|---|---|
| V-04a | Recollect the same finding with unchanged exposure. | Retain stable ID, evidence/context, disposition and history; no duplicate or lost finding. |
| V-04b | Recollect an approved disposition with no new relevant evidence. | Preserve approval; do not reopen it merely because collection repeated. |
| V-04c | Supply new relevant evidence; separately change the finding's exposure. | Reopening is justified only by that evidence/exposure, with prior disposition/history retained. |
| V-04d | Report an observation without an authorized correction decision. | Retain the observation; do not turn it automatically into correction authority or a charged implementation launch. |
| V-04e | Claim a new deferral authority in the collector report. | Do not grant that authority, waive required behavior or write a tracker. |

**Why test this:** Repeated review must not erase decisions, create new policy or
turn all observations into mandatory changes.

**How to check:** Run successive real collection admissions and reload between
them. Compare stable IDs and append-only historical evidence with the supplied
prior dispositions. Review the report's requirements/behavior/code-quality
coverage as well as its schema. Seeded approval tests preservation only; it does
not prove the future ART-009 decision or tracker recording.

### V-05 — A real failed product is corrected and collected again

**Situation:** One disposable prepared task starts without seeded successful
candidate/check/collection records. The scripted implementation leaves a real
product defect that its required behavioral check detects.

**Action and expected checkpoints:**

1. Execute public preflight and initial implementation. Inspect the actual
   product, then run its required check. It fails for the defect, not a missing
   tool. Cycle zero remains zero; failure records and logs exist.
2. Use the admitted `check_failed` route to authorize/reserve and launch correction.
   The actor edits the failing product code. Charge exactly one correction and
   use a fresh session when occupancy is unknown.
3. Capture the corrected candidate and run required checks. New actual command
   execution passes; previous failure, logs and candidate remain historical.
4. Launch a distinct fresh collector. It reruns the checks through the controller
   runner and admits current collection evidence. Prior coverage cannot cover the
   corrected product; finding history remains available.
5. Reload status and expose the acceptance-stage handoff. No ART-009 decision,
   completion or final task acceptance is admitted.

**Why test this:** A seeded ledger or a correction that changes no code cannot
prove the composed loop required by AC-05.

**How to check:** Observe public calls, actual product diff, assertion failure and
later pass, command counters/logs, new candidate identities and distinct observed
sessions. Keep this proof entirely separate from V-06's future-decision fixture.
This case owns the composed AC-05 journey; focused cases cover the other histories.

### V-06 — Three correction routes share one durable budget

**Situation:** Initial implementation has occurred at cycle zero. Use the inherited
test-only successor-decision seam for the not-yet-implemented ART-009 review-driven
correction request, clearly labeled as seeded upstream state. Do not add a
production acceptance bypass. Establish valid readiness and reason prerequisites
before each reservation.

**Action and expected checkpoints:**

1. Admit a real failed-check reason and reserve its correction: count becomes 1.
2. Use the explicitly labeled future review-decision fixture and reserve a
   `review_findings` correction: count becomes 2.
3. Use inherited authorized `environment_repair` state and reserve repair:
   count becomes 3. Actual repair invalidates readiness; implementation cannot
   resume until fresh public preflight is admitted. Preflight does not charge.
4. At each correction, replay reservation, launch and terminal observation, then
   reload. Count remains exactly that step's value and no duplicate actor starts.
   Unknown occupancy selects a fresh correction session.
5. Apply an owner-authorized safe input revision. Count/history stay 3, old evidence
   is not restored, and a second free cycle-zero implementation remains forbidden.
   Meet fresh-preflight and correction-reason prerequisites under revised inputs.
6. Request a fourth correction. Refuse for exhaustion, launch no actor, retain
   partial product/evidence/history/count, and expose a precise active-chat blocker
   and required owner action. Persist it through the existing intervention path;
   acknowledgement alone does not authorize retry or acceptance.

**Why test this:** Separate check/review/repair counters, restart or revision could
otherwise allow unlimited corrections.

**How to check:** Real reservations, launches, observed outcomes and storage reload
prove accounting. Capture invocation counts and authoritative snapshots before
duplicates and fourth refusal. The reason for fourth refusal must be exhaustion,
not missing readiness. Supplement with the inherited context-policy boundary
controls if changed: reliable occupancy 0 and just below 0.5 permit reuse; equality
0.5 and unknown/unreliable occupancy require fresh. Fresh-only launching remains
permitted. Seeded review/repair authority proves consumption/accounting, not
ART-009 semantic admission or automatic authorization of repair.

### V-07 — Relevant drift invalidates collection and cannot be repointed away

**Situation:** V-01 has produced a current collection. Run each row independently
from that valid state. Evaluated ignored inputs are explicitly in allowed paths.

| Case | Relevant change after collection | Expected result on status and attempted old admission |
|---|---|---|
| V-07a | Change tracked product bytes, including same-size content. | Old check/collection evidence cannot remain current. |
| V-07b | Add, modify or remove a visible untracked candidate input, each separately. | Old check/collection evidence cannot remain current. |
| V-07c | Change evaluated configuration, including an explicitly allowed ignored input. | Old check/collection evidence cannot remain current. |
| V-07d | Make an authorized task-input revision; repeat for policy and flow bindings. | Affected evidence/readiness become ineligible; history and correction count persist. |
| V-07e | Change index identity without changing worktree bytes; separately change HEAD. | Prior candidate-bound evidence cannot restore eligibility. |
| V-07f | Repoint a prior digest/report reference after relevant drift or revision. | No restoration of current coverage/readiness or acceptance progression. |

**Why test this:** Correct evidence for an old product is unsafe evidence for its
replacement. Path equality and unchanged status text do not establish identity.

**How to check:** Make actual filesystem/Git changes and public authorized revisions;
then inspect status and attempt reuse through admission. For V-07f an explicit
test-only record mutation challenges the guard; it does not claim coherent whole-run
tamper resistance. Retain historical report/log bytes. Use V-01 as unchanged-state
control and the inherited irrelevant ignored-generated-output control to avoid
mistaking all filesystem output for candidate drift.

### V-08 — A change during collection prevents stale admission

**Situation:** A fresh collector has started for a checked candidate. Synchronize
at a real process checkpoint before terminal collection admission.

**Action:** Change a relevant product input while collection is in progress;
separately repeat with evaluated configuration and approved-input source bytes.
Let the collector finish with the old identity and even passing rerun claims.

**Expected result:** No stale report becomes current coverage. Frozen authority
is not replaced by changed source text. Retain old evidence and the actual edits;
status names stale evidence and the required new inspection/check/collection work.
No acceptance progression follows.

**Why test this:** A start-only freshness check misses changes made during review.

**How to check:** Real subprocess synchronization and file edits exercise the
admission boundary; inspect before/after candidate identities and durable status.
This is sequential ownership safety, not a parallel-writer framework or enforced
collector filesystem isolation.

### V-09 — Evidence-only retries do not spend correction cycles

**Situation:** A current candidate needs missing rerun/collection evidence, without
implementation changes. Establish a nonzero correction count to detect reset.

**Action:** Perform a fresh evidence-only rerun, then fresh recollection. Reload.

**Expected result:** New operation identities and evidence are retained, count is
unchanged, and earlier failure/gap history is not erased. No implementation actor
is launched. If implementation changes are launched instead, they require the
inherited correction authorization and charge; evidence retry is not a bypass.

**Why test this:** Charging observation wastes the budget; disguising edits as
observation evades it.

**How to check:** Use actual check and collector execution, invocation roles,
product bytes and persisted count. Inspect the assignment's read-only instruction.
Runtime-enforced filesystem isolation is outside the contract.

### V-10 — Replay and interrupted collection preserve one outcome

**Situation:** Use a real collection operation at each publication checkpoint.
Keep partial product work and a nonzero correction count present.

| Case | Action / interruption boundary | Expected result after reload |
|---|---|---|
| V-10a | Observe an already admitted terminal collection again; replace raw claim bytes before replay. | Replay the same admitted outcome without replacing findings/logs or changing count/version. |
| V-10b | Interrupt after durable launch intent but before launch certainty. | Unknown ownership stops relaunch; retain records/work/count and precise intervention. |
| V-10c | Interrupt while collector is live, including while its rerun is unresolved. | No overlapping actor/check outside the authorized rerun protocol; no acceptance progression. Preserve partial logs and ownership. |
| V-10d | Interrupt after terminal evidence exists but before admission publication. | Reload may admit known complete terminal evidence once, or conservatively stop if authority/terminality is unresolved; never relaunch or manufacture success. |
| V-10e | Interrupt after admitted report publication before caller receives success. | Reload/observation returns the admitted outcome once; no duplicate findings, charge or execution. |

**Why test this:** Coordinator replacement must neither lose findings nor launch
another actor while the first may still own the task.

**How to check:** Use controlled process interruption at durable boundaries, real
storage and replacement controller reads, reusing existing interruption fixtures.
Demonstrate the single-operation guard at the actual command-lock/ownership
boundary with synchronized contention. Assert retained evidence, count, work,
next action and intervention when unresolved. Conservative stop must identify the
operation/evidence to inspect, not just return a generic error. This proves process
interruption behavior, not power-loss recovery or automatic repair.

### V-11 — Persisted failure categories give truthful next actions

**Situation:** Establish all other prerequisites so each fault reaches its intended
boundary, rather than failing setup.

| Case | Action / cause | Expected persisted observation |
|---|---|---|
| V-11a | Real product assertion fails. | Failed product check, retained logs and bounded authorized correction route. |
| V-11b | Required executable/environment is unavailable. | Infrastructure blocker, no product pass; authorized repair/fresh preflight or intervention, without invented permission. |
| V-11c | Required report or rerun evidence is absent. | Missing/not-run coverage and specific evidence-collection next action; no pass. |
| V-11d | Evidence refers to superseded work. | Stale coverage and new current-evidence next action. |
| V-11e | Required review capability or authority cannot be established. | Persisted blocker and precise active-chat action; no silent source-skill substitution or acceptance. |

**Why test this:** One generic failure or success flag prevents safe recovery and
can hide missing evidence as a product result.

**How to check:** Reuse the actual faults in V-02/V-03/V-05/V-07 where possible;
inspect returned and reloaded ART-002/ART-007, not just exceptions. These rows are
category oracles, not duplicate full journeys. Known issues/policy omissions cannot
waive required checks or role stages. No external message send is required.

### V-12 — T-005 receives an exact contract and honest proof limits

**Situation:** Implementation and local evidence are available for this leaf.

**Action:** Compare the consolidated `../T-004/controller-contract.md` with actual
public call/CLI responses, schemas, retained artifacts and proof results.

**Expected result:** The handoff lists callable/CLI names, payloads, artifact paths,
collector rerun requests, finding/disposition rules, replay/refusal behavior and
correction transitions. It names `observe_operation` → `_admit_actor_outcome` →
`_publish_actor_outcome` as the single semantic extension path, raw acceptance
transport inputs and missing-evidence/correction seams. Current contracts describe
implemented deltas, not ART-009 semantics or completion. Exact local commands,
results, baseline failures/skips and qualification limits remain visible; fake
actors do not qualify real sbx/provider/model execution. T-005 owns acceptance;
T-006 owns the live pilot. No official plan or installed skill is refreshed.

**Why test this:** A successor must consume the delivered boundary rather than
infer an API or assume future acceptance capability exists.

**How to check:** Document/interface review cross-references exercised public
requests and retained output from V-01/V-05/V-06/V-10/V-11. Check affected registry
claims through the designated registry-updater stage. This is contract/document
evidence, not a behavioral loop or a new acceptance decision.

## Coverage summary

| Promise from the brief | AC / parent promise | Required cases |
|---|---|---|
| [Fresh bound independent collection](brief.md#work-and-acceptance-criteria) | AC-01 / P-03 | V-01, V-02a–k, V-11e |
| [Independent reruns and explicit coverage](brief.md#work-and-acceptance-criteria) | AC-02 / P-03 | V-01, V-03a–f |
| [Stable findings and preserved dispositions](brief.md#work-and-acceptance-criteria) | AC-02 / P-03 | V-04a–e, V-10a |
| [Real bounded correction and fresh evidence](brief.md#work-and-acceptance-criteria) | AC-03 / P-04, P-05 | V-05, V-06, V-09 |
| [Reject drift; preserve replay and interruption](brief.md#work-and-acceptance-criteria) | AC-04 / P-04 | V-02a–k, V-07a–f, V-08, V-10a–e |
| [Composed loop, exhaustion and truthful status](brief.md#work-and-acceptance-criteria) | AC-05 / P-04, P-05 | V-05, V-06, V-07a–f, V-11a–e |
| [Exact successor handoff and limits](brief.md#work-and-acceptance-criteria) | AC-06 / P-06 | V-01, V-05, V-12 |

No risk-row IDs are supplied. The finite identity, freshness, disposition,
interruption and failure variants above derive from the ACs and cited authority.
The parent assigns composed T-004 proof to this leaf; there is no unowned
parent-only integration gate. T-005 retains acceptance/completion proof.

## Source and revision

Source brief: skills/task-orchestrator/docs/tasks/T-004.2/brief.md
Source brief revision: 1
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

Normative references: [parent P-03–06](../T-004/brief.md),
[plan ART-006, IF-003, FLOW-001–003, INV-001–008](../../local-harness-orchestration-plan.md),
[owner direction](../../direction-single-task-sbx.md),
[T-004.1 producer contract](../T-004.1/controller-contract.md),
[T-003 observed-outcome contract](../T-003/controller-contract.md) and
[T-002 accounting contract](../T-002/controller-contract.md).
T-004.1 advancement is supported by [acceptance-02](../T-004.1/reviews/acceptance-02.md).
