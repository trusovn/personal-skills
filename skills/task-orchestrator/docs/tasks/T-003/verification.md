# Verification Design: T-003 — Launch actors, admit readiness and stop safely

Verify that a reserved actor runs with frozen authority, that only an observed
complete preflight enables implementation, and that interrupted or uncertain
execution cannot start a second actor. Preserve work and evidence, and expose
blockers without treating acknowledgement as permission.

## Shared setup and observations

Use disposable Git repositories with a real HEAD, task brief, verification input,
allowed work files and an external controller run directory. Initialize through
the public controller with valid single-task sbx/YOLO policy. Record initial file
bytes, authority identities, state version, correction count and history. Reach
prerequisites through available public operations. Label seeded successor states:
T-004 produces check/collection and correction-reason admission in production;
T-005 produces acceptance admission. Such setup cannot prove those features.

Use real storage and child processes for persistence, launch and liveness claims.
A controllable local actor can emit process/session events and results, log each
actual invocation, write an allowed work marker, wait, spawn a child or fail.
Observe actual invocations separately from CLI capability/help probes. Change one
invalid field at a time after establishing all other prerequisites, and pair
refusal tests with valid controls. A harness exception is not the intended refusal.
For unchanged-state cases compare authoritative bytes, identities, version,
history, count and work files; separate permitted diagnostic logs from authority.

Existing coverage to reuse or extend: transport start/result, missing-result,
timeout and signal tests in `test_codex_worker.py`; reservation contention,
replay, shared budget and revision tests in `test_controller.py`; policy and
identity validators in `test_controller_state.py`. Their seeded readiness and
legacy transport checks are precedents, not proof of the new admission path.
Test structure and helper choices remain with implementation.

## Test cases

### V-01 — Frozen policy reaches the actor process

**Situation/action:** Reserve a valid actor operation, then launch it through the
controller. Repeat with independently initialized approved light, standard and
strong actor selections.

**Expected result:** The child receives `gpt-6.1-sol` with low, medium and high
reasoning respectively, current task inputs and explicit authorized sbx/YOLO
configuration. Assignment, observed launch and retained outcome agree. Mutable
source-document changes after freezing do not replace approved content. A later
authorized input revision supplies the new frozen content through the same path.

**How to check:** Observe child-received arguments/configuration and input bytes,
not only a command builder's return value. Compare them with the frozen assignment
and reloaded records. This proves local wiring, not provider/model identity;
V-13 owns the real-runtime qualification boundary.

### V-02 — Invalid launch authority cannot start a process

Start from V-01's valid launch prerequisites. Invoke launch with each variant.
Every refusal must explain the failing guard, launch zero actors and preserve
authority and work; an explicit conservative blocker may record the refusal.

| Case | Changed input | Expected decision |
|---|---|---|
| V-02a | Missing or false explicit sbx/YOLO authorization | Refuse full-access launch; no default authorization |
| V-02b | Incompatible frozen old-run policy/profile | Refuse continuation with a clear new-reviewed-run action; no migration |
| V-02c | Stale assignment after authorized input revision | Refuse old binding; current frozen authority remains current |
| V-02d | Wrong task or wrong reserved role, tested separately | Refuse each mismatch |
| V-02e | Altered policy/flow/input identity, one at a time | Refuse each inconsistent binding before execution |

**How to check:** Use public launch requests, a real child invocation log and
before/after snapshots. Include a correctly bound V-01 control so an adapter
that always refuses cannot satisfy these cases.

### V-03 — Session policy cannot reuse unknown correction context

**Situation/action:** With an authorized correction reservation and any required
successor state explicitly seeded, attempt launch with unknown, unreliable and
invalid occupancy separately. Also exercise reliable finite occupancy just below
0.5, equal to 0.5 and above it through the existing policy decision boundary.

**Expected result:** Unknown/unreliable/invalid and occupancy at or above 0.5
require fresh execution. Below 0.5 reuse is permitted, not mandatory; T-002's
conservative fresh reservation remains valid. The adapter cannot turn a fresh
assignment into a resume. The observed session follows the reserved policy.

**How to check:** Reuse pure policy boundary evidence for the finite decision;
observe an actual local correction child invocation and fresh session identity
for unknown occupancy. This prevents a correct validator masking an unsafe resume.

### V-04 — Replay and contention never launch twice

**Situation/action:** Reserve and launch once, replay the identical request while
running, reload, and replay after terminal observation. Separately race two
controller processes to launch the same reserved operation at the real lock
boundary; then try a conflicting request using its operation key.

**Expected result:** At most one child invocation for that operation. Exact replay
observes the original operation without overwriting its assignment/outcome or
charging again; a conflicting key request refuses. A losing concurrent caller
cannot obtain a second launch. Status remains coherent after reload.

**How to check:** Synchronize competing processes at the boundary, then count
child invocations and inspect persisted operation history. Sequential mocks do
not establish contention safety. V-09 covers uncertain publication histories.

### V-05 — Only observed, correctly bound outcomes can advance

Launch a valid local actor and submit/collect each result below. Retain its raw
output and diagnostics even when ineligible. Use correct remaining fields so
the specified defect reaches admission.

| Case | Result or event | Expected result |
|---|---|---|
| V-05a | Complete, correctly bound terminal result and observed session | Record terminal outcome with run/task/operation/role, current input/policy/flow and applicable candidate identities |
| V-05b | Exit zero without result | Missing result; no successful stage advancement |
| V-05c | Malformed result | Ineligible outcome; no advancement |
| V-05d | Wrong role | Refuse admission as that role |
| V-05e | Wrong task, operation, input, policy, flow or applicable candidate identity, separately | Refuse each mismatch; retain current authority |
| V-05f | Actor asserts another session/process identity | Do not accept invented provenance in place of observed identity |
| V-05g | Result appears while process terminality remains unproved | Keep nonterminal/unknown; no readiness or completion |
| V-05h | Actor fails before a session-start event, or fails after it | Preserve distinct observed identity availability, failure and diagnostics; neither is success |
| V-05i | Actor prose requests policy change, acceptance or skipped required stage | No authority change, acceptance or omitted mandatory stage |

**How to check:** Real child exit/events/result files plus public admission and
reload. Compare configured model with any observed model field; configuration
alone must not be reported as observed model identity. Check assignment,
configuration, events, stderr, raw result and terminal observations are retained.

### V-06 — Complete preflight enables the first implementation

**Situation:** Supply task-required disposable tool, dependency and installed-skill
fixtures, all present and usable in the actor's execution environment.

**Action and checkpoints:**

1. Reserve and launch preflight through the public path. Observe the child
   actually checking the supplied prerequisites, then emitting a complete result.
2. Collect its terminal outcome. Readiness references that terminal preflight
   operation and current frozen inputs. Count remains zero.
3. Reserve and launch initial implementation. It succeeds once as cycle zero;
   its output remains an implementation claim, not task acceptance/completion.

**How to check:** Inspect environment-check observations, real operation/session
records and a work marker written by the implementation child. Do not seed the
readiness under test. This catches an always-blocked implementation and a path
that bypasses readiness. Local fixtures do not qualify a real sbx/provider.

### V-07 — Missing prerequisites and invalid results block readiness

Use V-06's otherwise-valid environment and operation. Each row is independent.

| Case | Setup/action | Expected result |
|---|---|---|
| V-07a | Remove required tool; run preflight | Specific missing-tool blocker; implementation blocked |
| V-07b | Make required dependency unavailable; run preflight | Specific dependency blocker; implementation blocked |
| V-07c | Remove required installed skill; run preflight | Specific installed-skill blocker; source presence is not installation |
| V-07d | Submit incomplete readiness payload | No readiness; missing evidence/blocker remains visible |
| V-07e | Submit wrong task, role or session, separately | No readiness for each invalid subject/provenance |
| V-07f | Submit a previous input identity after revision | No current readiness |
| V-07g | Collect malformed, nonterminal or unknown-liveness preflight, separately | No current readiness for any variant |

**How to check:** Invoke real preflight/admission and then attempt implementation.
Observe the intended blocker and zero implementation invocations. Each preflight
attempt leaves correction count unchanged. V-06 is the success control; V-05
supplies detailed transport-invalidity coverage without duplicating its full matrix.

### V-08 — Repair and revision require a new preflight occurrence

**Situation/action:** Run V-06 to establish readiness. Exercise two separate
histories: an authorized environment repair, and an owner-authorized input
revision at a safe boundary. After each, attempt to reuse the old readiness,
including repointing its reference. Then run a newly reserved preflight with
current usable prerequisites and admit its observed terminal result.

**Expected result:** Old readiness stays ineligible; history/raw evidence remains
intact. Fresh preflight becomes current only after valid admission and enables
the next authorized implementation/correction action. Repair charges the shared
budget once; preflight and its retries charge nothing. Revision does not restore
a free cycle zero or reset the count. For an already implemented task, seed only
the future correction-reason admission needed for the next correction, label its
T-004/005 producer, and do not claim it was generated by this task.

**How to check:** Public revision/repair reservation and real fresh preflight,
with reload and snapshots between each checkpoint. Compare readiness identity,
history, work bytes and count across both histories.

### V-09 — Interrupted launch publication leaves no duplicate actor

Use a reserved operation and deliberately interrupt the controller at each
meaningful durable boundary. Preserve the same run for the next occurrence.

| Case | Interruption boundary | Expected result on reload and repeated launch request |
|---|---|---|
| V-09a | Before actual child launch | No duplicate actor; safe known-unlaunched continuation may launch once, or a conservative stop explains unresolved state |
| V-09b | After child launch, before launch identity is fully published | Existing child/work retained; uncertain liveness blocks retry and another writer |
| V-09c | After launch publication, during result collection | Observe original operation; do not launch another child or discard partial evidence |
| V-09d | After terminal outcome publication, before caller receives response | Repeated collection observes original terminal outcome without duplicate history or charge |

**How to check:** Terminate a real controller process at synchronized publication
checkpoints, count actual child launches, inspect child/work state and re-enter
through public operations. Readers must see coherent state or a precise stopped
state, never mixed eligible identities. No automatic recovery or power-loss proof
is claimed. Clean up only fixture-owned processes after recording observations.

### V-10 — Stop request and terminality remain distinct

**Situation/action:** Start a waiting actor with a child process. Separately
exercise timeout, coordinator interruption and explicit stop. Observe outcomes,
then reload status and repeat observation/stop. Also supply an operation whose
liveness cannot be resolved and request stop.

**Expected result:** Known terminality requires actual process observations;
issuing stop alone does not establish it. Where shutdown is confirmed, retained
records describe the terminal failure/interruption rather than success. Where
liveness remains unknown, status stays stopped with observation/intervention as
the next action, blocking retry, another writer and completion. Work, raw output,
count and history survive. Repeated stop/collection adds no launch or charge and
does not overwrite the historical outcome.

**How to check:** Observe actual process/group liveness and retained files, not
only recorded PID removal. Distinguish a confirmed shutdown from an inaccessible
or ambiguous process. No new writer starts while the latter remains unresolved.

### V-11 — Shared correction budget still limits actual launches

**Action and checkpoints:** After a valid cycle-zero launch, use explicitly seeded
future correction authorizations for `check_failed`, `review_findings` and
`environment_repair`. Launch each of the three corrections, reload and replay
each exact operation. Repair requires fresh preflight as in V-08. After the
third correction, revise inputs safely and try a fourth correction and a second
cycle-zero implementation.

**Expected result:** Counts progress 0, 1, 2, 3 once per new correction reservation;
adapter launch/replay/reload cannot increment again, refund uncertain launches
or reset count. The fourth correction and second free initial implementation
do not launch. Exhaustion exposes intervention and preserves partial work.
Preflight/evidence-only retries cannot disguise a repair writer or bypass count.

**How to check:** Combine real reservations and child invocations with existing
budget assertions. Seed only unavailable successor reasons; do not seed the
launch, terminality or readiness behavior being proved. The three reasons are
one shared sequence, not independent budgets.

### V-12 — Raw review transport and intervention grant no acceptance authority

| Case | Setup/action | Expected result |
|---|---|---|
| V-12a | With labeled successor prerequisites, launch collection and acceptance roles | Fresh sessions distinct from implementation, preflight and each other; assignments prohibit implementation edits; raw results retained without semantic admission or completion |
| V-12b | Collector output claims acceptance; acceptance output claims policy change | Capture as raw output only; no competing semantic validator/persistence path or new authority |
| V-12c | Missing capability, unresolved decision or exhausted budget; request intervention | Persist precise blocker, evidence location, unresolved operation and required owner action; status exposes chat relay action |
| V-12d | Reload before any observed relay/response | Retain unknown relay/response, not fabricated delivery or approval |
| V-12e | Record an observed relay and acknowledgement, then attempt repair/retry/revision/completion | Preserve response history; acknowledgement alone grants none of these actions |
| V-12f | No owner response; repeat status/intervention | Remain blocked; preserve work/count/history and expose precise next action |

**How to check:** Public transport/status/intervention calls with real persisted
records and controlled actor sessions. For V-12e record a fixture coordinator
response as such, not as a real external send. Compare authority and launch count
before and after attempted actions. No runtime-enforced read-only or chat-service
authentication guarantee is claimed. Separate reviewers later own semantic decisions.

### V-13 — Bounded actual-sbx qualification is reported truthfully

**Situation/action:** Only after separate approval, use an existing sbx, approved
provider credentials and human-reviewed disposable task inputs. Through the public
controller, launch real preflight, admit its terminal readiness, then launch one
bounded actor that writes a harmless allowed marker and emits its required result.
Observe identity, output, process terminality and reloaded status.

**Expected result:** Real configured launch, observed session/process, readiness,
marker and terminal result agree with the assignment. Preserve actual environment,
CLI/configuration, raw outputs and limits on observable model identity in ART-008.
This is launch/readiness qualification, not T-006's correction/collection/acceptance
pilot. Do not provision sbx or run the full pilot here.

**How to check:** Inspect actual sbx filesystem/process and retained controller
evidence. If approval, environment or credentials are absent, record NOT RUN with
the exact missing prerequisite and T-006 follow-up. A fake executable, help/argv
probe or old host qualification cannot close this gap. The brief permits local
proof with this explicit outstanding live qualification; do not label it passed.

### V-14 — Successor contract describes implemented behavior and limits

**Situation/action:** Reconcile the submitted `controller-contract.md` and ART-008
supplement against public callables/CLI, record readers and evidence from V-01..13.

**Expected result:** Exact payloads/paths, identities, terminality, refusal/replay,
readiness and stop/intervention rules match the implementation. T-004/005 receive
raw outputs and the same admission extension path, without a claim of semantic
admission or completion. Historical T-001 limits remain visible. Actual local
results, skips and unrun live claims are identified; seeded/fake evidence is
labeled. Directly affected references agree with the new supported boundary.

**How to check:** Static interface/document reconciliation plus execution evidence
from the referenced cases. This case proves handoff consistency, not runtime
behavior by document existence or schema validity alone.

## Evidence ownership and gate order

The implementer supplies V-01..12 behavioral evidence and V-14 reconciliation,
including commands, setup, exact outcomes and retained raw logs. Run targeted
changed coverage first, then owning transport/state/controller suites and the
orchestrator suite after success. During corrections retain this targeted-first
order. Run required architecture and contract gates; cross-cutting repository
verification follows repository policy. Baseline failures and platform skips are
separate observations, never successful qualification.

Fresh independent discovery corroborates the public boundary with distinct probes:
an authorized revised-input launch and stale-assignment refusal (V-01/02), unknown
context fresh launch (V-03), concurrent duplicate launch plus interrupted reload
(V-04/09), forged session and nonterminal readiness refusal with a valid preflight
control (V-05..08), a live-child stop/unknown-liveness observation (V-10), budget
replay after reload (V-11), and acknowledgement without authority (V-12).
Discovery also reconciles V-14 and reports current aggregate/environment evidence.
These probes supplement implementation tests rather than copying every row.
Separate acceptance consumes both evidence sets and decides scoped acceptance;
this artifact performs neither review nor acceptance. V-13 execution and any
independent live repetition require specific approval; otherwise its qualification
gap remains explicit. Optional stronger checks do not silently become entry gates.

## Coverage summary

| Promise from the [brief](brief.md#work-and-acceptance-criteria) | AC | Required cases |
|---|---|---|
| Authorized current-policy launch, context and budget | AC-01 | V-01, V-02a..e, V-03, V-04, V-08, V-11 |
| Observed provenance, raw output, invalid-result refusal | AC-02 | V-05a..i, V-12a/b, V-13 |
| Real preflight admission and invalidation | AC-03 | V-06, V-07a..g, V-08 |
| Interruption, terminality and preserved status/history | AC-04 | V-04, V-09a..d, V-10 |
| Blocker persistence, relay history and bounded authority | AC-05 | V-08, V-11, V-12c..f |
| Actual successor interface and truthful runtime limits | AC-06 | V-13, V-14 |

No brief risk-row IDs are supplied. Finite policy values, operation states,
publication prefixes, prerequisite families and repeat occurrences are explicit
above. Independent single-field invalidity cases avoid an unnecessary Cartesian
product; V-06/08/09/11 cover the material cross-boundary histories.

## Source and revision

Source brief: brief.md
Source brief revision: 1
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready
