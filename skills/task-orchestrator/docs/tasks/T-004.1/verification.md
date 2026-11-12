# Verification Design: T-004.1 — Produce candidate-bound scope and check evidence

The controller must inspect the actual implementation files and execute approved
checks against that candidate. A candidate is the evaluated file and authority
identity, not an actor's summary. Drift must remove current eligibility without
erasing history. Explicit frozen sbx/YOLO authority permits the new execution
path; it does not prove filesystem or network containment.

## Shared setup

Use disposable Git repositories and external run directories. Freeze one prepared
task, its scope, required checks and explicit execution policy through the public
controller. Complete T-003 preflight and a terminal implementation through its
existing local actor fixture and admission path. That fixture represents the
upstream actor; it does not prove real Codex, sbx or provider behavior. Do not seed
candidate/check success in cases that claim producer behavior.

Use a small real product file and an approved portable local command that reads
it, emits recognizable stdout/stderr and exits nonzero for incorrect content.
Provide correct content as the success control. Keep check logs and invocation
counters outside evaluated task files, except in explicit side-effect cases.
Record independent before/after snapshots of task bytes, Git baseline, ledger
version, correction count, operation history and evidence bytes. Observe results
again after loading the controller in a replacement process.

Reuse the existing Git, controller, actor and runner setup in
`test_controller_git.py`, `test_controller.py`, `test_actor_operations.py` and
`test_verification_runner.py`. In particular, retain unusual paths, dirty owner
baselines, same-size drift, timeout descendants and publication failures. Extend
coverage only where the new public boundary adds an obligation. The local runner
tests currently substitute the sandbox invocation for process mechanics; the new
authorized-path proof must execute the production policy selection and runner.
Mocked argv alone is not proof of execution.

For V-01–V-12, implementation owns focused deterministic evidence, then the
owning orchestrator suite after focused checks pass. Fresh independent discovery
must corroborate the public candidate/check boundary with its own disposable
real-file pass/fail and drift probes (V-01, V-04, V-06, V-09), and inspect current
raw evidence for the remaining cases. Separate acceptance decides whether that
evidence is sufficient. V-13 is producer-contract/document review, corroborated
by discovery against actual interfaces. No live/model/networked run is part of
this design. T-004.2 owns collection/correction composition; T-006 owns real sbx
and provider qualification.

## Test cases

### V-01 — Inspection identifies real files after terminal implementation

**Situation:** The admitted terminal implementation changed one allowed tracked
file and added an allowed untracked file. Include a filename with spaces and
literal shell metacharacters. Its summary claims different bytes or a check pass.

**Action:** Request candidate inspection through the public controller, then read
ART-003 and reloaded status.

**Expected result:** ART-003 describes the actual files and binds run/task,
terminal implementation operation, approved inputs/policy/flow, baseline and
configuration. Actor claims do not supply candidate identity or check success.
Task files and correction count are unchanged. Check evidence is still missing
or not-run; collection, acceptance and completion have not been granted.

**Why test this:** Accepting a summary could admit work the controller never saw.

**How to check:** Use real Git/filesystem observations and independently recorded
file bytes. Compare published bindings and status to the known fixture, including
the literal path. Do not compute the entire oracle with the candidate algorithm.

### V-02 — Dirty owner work is preserved and scope violations cannot pass

Start with owner changes captured in the baseline, both inside and outside task
scope. For each row, execute terminal implementation and inspect real files.

| Case | Implementation change | Expected result |
|---|---|---|
| V-02a | Only clean-baseline allowed files change | Candidate can become current; unchanged dirty owner bytes remain intact and are not absorbed into the task patch. |
| V-02b | A pre-existing dirty file changes again, including one inside allowed scope | Owner-work violation; no eligible candidate/pass; retain both baseline evidence and observed work without repair or overwrite. |
| V-02c | A new tracked change outside allowed scope | Scope violation; no eligible candidate/pass; preserve files. |
| V-02d | A new untracked file outside allowed scope | Scope violation; no eligible candidate/pass; preserve files. |

**Why test this:** Scope membership alone must not authorize overwriting owner
work, and untracked files must not escape inspection.

**How to check:** Compare baseline and actual file/patch observations, refusal or
blocker and current eligibility. Real rename/delete observations in existing Git
coverage remain required; reuse them rather than duplicating their fixtures.
Operational inspection may record truthful violations; it must not undo work.

### V-03 — Invalid ownership and unstable operations cannot authorize checks

Use otherwise valid requests and authority. Change one prerequisite at a time.
Request the relevant inspection/check operation at the public boundary.

| Case | Starting condition | Expected result |
|---|---|---|
| V-03a | No admitted terminal implementation/correction outcome, or wrong-stage outcome | No candidate/check admission or subprocess launch. A raw result file is insufficient. |
| V-03b | Wrong run, task or operation reference, each separately | Refusal; no launch or eligibility. |
| V-03c | Mismatched approved input, policy, flow or baseline binding, each separately | Refusal; no launch or replacement authority. |
| V-03d | Actor operation live | No stable candidate or overlapping check. |
| V-03e | Actor operation unknown | Remain stopped; observation/stop/intervention only, with no overlapping check. |
| V-03f | Check is already active; a second controller attempts inspection/check under the real command lock | No second operation or subprocess; original ownership remains authoritative. |

**How to check:** Use actual controller records and lock contention. In invalid
request rows, ledger bytes/version, count and task files remain unchanged;
diagnostics are separate. Check launch counters stay zero. V-01 and V-06 provide
success controls, so an always-refusing implementation cannot satisfy coverage.
V-03d/e may use explicitly labeled upstream live/unknown states; V-11 exercises
uncertainty caused by the new check path itself.

### V-04 — Relevant drift supersedes candidate and checks

**Situation:** V-06 has produced a current candidate and passed checks. Save their
records. Apply one change per independent row and request status/check admission.

| Case | Relevant change | Expected result |
|---|---|---|
| V-04a | Same-size tracked file byte change with unchanged HEAD/index | Candidate and dependent check eligibility become stale; no current pass. |
| V-04b | Untracked evaluated file byte change, addition or removal, each separately | Same stale outcome; status-only or tracked-only identity is insufficient. |
| V-04c | Index or HEAD/baseline identity change without relying on a worktree byte difference | Old candidate/check identity cannot remain current. |
| V-04d | Evaluated configuration bytes change | Old candidate/check evidence is stale. |
| V-04e | Approved safe-boundary task-input, policy or flow revision, each separately | Old bindings lose eligibility; inherited revision/readiness rules apply. No previous check satisfies the revised task. |

**How to check:** Compare raw file/authority identities, reloaded status and
attempted admission. Historical ART-003/005 bytes remain available and unchanged;
stale is distinguishable from failed or missing. A request against the stale
candidate launches nothing and preserves authoritative state/version, count and
task files; passive status does not mutate them. Direct tampering with frozen
authority is instead a validation refusal, as in V-03c, not an authorized revision.
Use V-12 to show that new evidence can be produced at the next permitted boundary.

### V-05 — Generated output does not hide evaluated input drift

**Situation:** A check creates a Git-ignored generated output that is not an
evaluated input. In a separate case, a generated/ignored file is explicitly an
input read by the configured check. Freeze that input/configuration as part of
the evaluated task. Existing Git exclusion behavior is not authority to ignore
evaluated inputs ([AC-02](brief.md#work-and-acceptance-criteria)).

| Case | Action | Expected result |
|---|---|---|
| V-05a | Run the check that creates only the irrelevant ignored output | Preserve existing generated-file treatment; this output alone does not make an otherwise unchanged candidate stale. |
| V-05b | Change the generated/ignored evaluated input after inspection, before checking | Reject old eligibility; no current pass for the old candidate. |
| V-05c | Change that evaluated input during the real check | Terminal exit zero still cannot establish a current pass. |

**How to check:** Use actual ignore rules, real reads/writes and synchronized
execution for V-05c. Observe pre/post identities and durable eligibility, not just
Git status. This does not authorize new blanket generated-path exclusions.

### V-06 — Approved checks actually execute and publish bound evidence

**Situation:** Current inspected candidate with correct product content and a
frozen explicit sbx/YOLO execution authorization. All required commands resolve.

**Action:** Invoke the public check operation using production policy selection
and the existing planner/runner. Reload the published ART-005.

**Expected result:** Actual shell-free argv executes in the target repository in
approved order. ART-005 identifies the commands, setup/inputs, environment,
candidate and authority, effective execution mechanism, raw outputs and exact
exits. Required checks pass only when executed successfully. Logs survive reload
with their recorded identities. YOLO evidence states its lack of filesystem and
network enforcement. Correction count and task content are unchanged.

**How to check:** Commands read the real product and emit distinctive binary
stdout/stderr; inspect their invocation counter, outputs and log hashes outside
the task tree. Include quoted/literal arguments and multiple commands using the
existing runner precedents. Execute without substituting the sandbox builder.
This proves portable local subprocess wiring, not execution inside real sbx.

### V-07 — Execution authority selects the mechanism without fallback

Use a harmless marker command and otherwise valid candidate/check inputs. Freeze
each authorized envelope through its supported entry point; invalid envelopes
must be refused before launch, not forced into valid runs.

| Case | Policy/environment | Expected result |
|---|---|---|
| V-07a | Explicit supported frozen sbx/YOLO authorization | New path can execute without macOS sandbox-exec; record that actual mechanism. V-06 supplies real-process proof. |
| V-07b | Absent, incomplete or unauthorized execution authority, each separately | New path unavailable; no unrestricted launch. Incompatible frozen runs require reviewed replacement, not migration. |
| V-07c | Restrictive legacy policy on an unsupported host or with missing sandbox-exec | Existing refusal; no platform-selected YOLO path. |
| V-07d | Restrictive legacy sandbox capability launch fails | Failure/refusal remains explicit; no unrestricted fallback and no marker execution. |
| V-07e | Supported restrictive legacy invocation | Retain exact sandbox mechanism and permission validation; real containment evidence is valid only if its existing host capability test actually runs. |

**How to check:** Component checks can control platform/capability responses to
prove selection and pre-launch refusal. Pair them with V-06's real execution and
existing supported-host containment tests. A substituted invocation proves no
enforcement; platform skips or denied host execution must be reported as limits.

### V-08 — The new path retains command and dependency restrictions

**Situation/action:** Request checks through frozen policies that exercise the
existing closed parser and install rules, with all unrelated prerequisites valid.

| Case | Input | Expected result |
|---|---|---|
| V-08a | Existing prohibited shell syntax/launcher families and malformed commands | Refuse before any command executes; no shell side effect. |
| V-08b | Recognized dependency install with installation forbidden | Refuse before execution; no download/install or repair. |
| V-08c | Same recognized command with explicit install permission | Planner permits it under existing rules; no real package installation is needed to prove planning. |
| V-08d | Valid quoted argv and near-miss non-install command | Preserve accepted parsing; harmless local command actually runs. |

**How to check:** Reuse parser/install table coverage and add public-path wiring
evidence that the selected runner applies it. Planner acceptance in V-08c does
not establish installation success or authorize a live check. A later invalid
command must fail planning before an earlier marker command executes, following
the existing all-command preflight behavior.

### V-09 — Check failures have distinct, actionable outcomes

Use a current candidate and vary only the indicated condition. Run public checks
and inspect ART-005 and status after reload.

| Case | Condition | Expected result |
|---|---|---|
| V-09a | Product content is incorrect; actual check exits nonzero | Failed with output/exit and current evaluated candidate; bounded correction may be requested through inherited policy. No correction count charged by checking. |
| V-09b | Required executable missing or test infrastructure broken | Blocked with the precise missing/broken prerequisite and authorized repair or intervention action; no automatic install/repair or product-success claim. |
| V-09c | Required checks not yet run or required evidence missing | Missing/not-run, never passed. Next action requests evidence. |
| V-09d | Required check fails and is offered as a known issue/authorized gap | Required check remains unsatisfied; no waived pass or premature advance. |
| V-09e | Approved targeted-only mode omits a repository-only extra gate | Omission is explicit under frozen policy, not passed or failed; all required task checks and actor stages remain required. |
| V-09f | Targeted check fails before a later approved gate | Actual failure retained; later command is not-run and its marker absent. |

**How to check:** Real product failures and broken local prerequisite controls
prove classification; a fixture infrastructure probe must reach the intended
failure, not fail accidentally during setup. Existing planner gap behavior may
remain a legacy contract, but cannot waive required checks in this new slice.
Status retains the distinction between failure, stale (V-04), blocked, missing,
not-run and policy omission. No result grants collection admission, acceptance or
completion; available next actions remain within the T-004.1 producer slice.

### V-10 — Check side effects and timeout cannot publish false success

| Case | Setup/action | Expected result |
|---|---|---|
| V-10a | Real command waits at a checkpoint; change tracked evaluated bytes, then let it exit zero | Post-execution identity differs; no current pass; retain execution and drift evidence. |
| V-10b | Same sequence with an untracked evaluated file | Same result, catching tracked-only postchecks. |
| V-10c | Check itself edits an evaluated configuration/input and exits zero | Side effect invalidates eligibility; do not silently adopt new bytes as the evaluated candidate. |
| V-10d | Command and descendant exceed a positive finite timeout | Record timeout/failure and logs; establish owned process-group termination before another operation. If terminality remains uncertain, stop with blocker. |
| V-10e | Invalid zero, negative, nonfinite or nonnumeric timeout | Refuse before launch with state/version/count/task files unchanged. |

**How to check:** Use real subprocess/file synchronization, not arbitrary sleeps.
Observe descendant liveness, invocation counts, pre/post identities and published
records. Reuse the runner's exited-parent/open-pipe and SIGTERM-resistant child
controls; a parent's exit alone does not establish group terminality.

### V-11 — Replay and interruption preserve one execution and its evidence

For each history, use a command that appends one external invocation marker.
Interrupt a separate controller process at a controlled durable boundary, then
reload and repeat the same operation request. Keep task bytes and count snapshots.

| Case | Interruption/history | Expected checkpoints after reload/replay |
|---|---|---|
| V-11a | Completed check, ordinary replay | Same operation and immutable logs/record; exactly one execution; no state/version/count increment from replay. |
| V-11b | Durable no-relaunch intent, before launch outcome is certain | No second launch; unresolved ownership remains stopped with operation/evidence and precise intervention action. |
| V-11c | During real command execution | No overlapping check or actor. Retain partial logs/work and known/unknown status; resolve only from supported terminal observations. |
| V-11d | Execution evidence published, before ledger result publication | Reuse original durable execution if completion/identity can be established; otherwise stop with a useful blocker. Never rerun under that identity or overwrite evidence. |
| V-11e | Existing log/record collision or injected log/publication write failure | No overwrite or fabricated complete pass. Preserve existing/partial evidence; report truthful failure/uncertainty and next action. |

**How to check:** Observe actual child invocation counts and retained bytes across
replacement processes. Injection may control the I/O failure or interruption,
but must not replace execution or persistence. After stale replay, the old result
can remain historical and cannot become current. No automatic recovery service,
power-loss durability or coherent-record tamper resistance is claimed.

### V-12 — A terminal correction produces new evidence without erasing history

**Situation:** V-09a produced a real failure. An upstream correction is reserved
and admitted through T-003's existing path and writes correct real product bytes.
This is a producer-boundary exercise, not independent collection admission.

1. Inspect the corrected terminal outcome. Expect a new current candidate bound
   to that operation; old failed candidate/check records remain historical.
2. Run the same approved check through the public runner. Expect an actual pass
   for the new candidate, distinct execution identity/logs and no extra
   correction charge from inspection/checking.
3. Reload and request the old failed operation's check evidence. Expect history
   only, no rerun and no replacement of current evidence with the old candidate.

**Why test this:** Producing a second result must neither reuse the old pass/fail
identity nor reset the inherited correction accounting.

**How to check:** Compare observed failure/pass exits against actual product
content, operation/candidate identities, history and count checkpoints. The
correction reservation owns any inherited charge. Full failure → collection →
correction → recollection composition and budget-limit proof belong to T-004.2.

### V-13 — The producer contract is sufficient for the future collector

**Situation/action:** Inspect the delivered `controller-contract.md`, affected
schemas/validators and implementation report against actual public operations
and V-01–V-12 evidence.

**Expected result:** The contract gives actual library/CLI names, payloads,
evidence paths, identity inputs, generated-file treatment, approved check
invocation and replay rules. It explains how a future collector requests its own
new rerun through this same runner, with distinct execution identity and retained
history. It neither reuses completed-operation replay as a fresh rerun nor needs
a second runner, ledger or actor-admission path. Exact local commands/results,
skips and failures are recorded; real sbx/provider proof is explicitly unrun here.

**How to check:** Compare the documented requests/responses to actual producer
calls and read raw local evidence for failing/passing, drift/refusal and replay
controls. Review schema/validator consistency separately from behavior. Confirm
maintainability and registry updates follow their assigned stages; do not register
unimplemented collection or acceptance. This is interface/document proof, not a
claim that T-004.2's collector has executed.

## Coverage summary

All AC references below resolve to [Work and acceptance criteria](brief.md#work-and-acceptance-criteria).
The brief supplies no separate risk-row IDs.

| Promise from the brief | AC / risk row | Required cases |
|---|---|---|
| Inspect actual terminal implementation/correction, bind all identities, distrust actor claims | AC-01 | V-01, V-03a–c, V-12 |
| Preserve owner work, scope and single-operation exclusion | AC-01 | V-02a–d, V-03d–f |
| Reject relevant drift, honor generated treatment and check before/after execution | AC-02 | V-04a–e, V-05a–c, V-10a–c |
| Preserve authoritative state on invalid/stale requests; keep stale history distinct | AC-02 | V-03a–f, V-04a–e, V-10e, V-11a–e, V-12 |
| Replay/reload cannot rerun, overwrite evidence or bypass uncertain ownership | AC-02 | V-11a–e |
| Execute real checks with explicit frozen mechanism authority, preserve legacy restrictions | AC-03 | V-06, V-07a–e, V-08a–d |
| Retain timeouts, terminality and durable log publication | AC-03 | V-06, V-10d–e, V-11b–e |
| Record truthful setup, environment, outputs, exits and current candidate | AC-04 | V-06, V-09a–f, V-10a–d |
| Distinguish outcomes; require checks; route failures/repair and expose permitted next actions | AC-04 | V-03d–f, V-04a–e, V-09a–f, V-11b–e |
| Evidence-only work is free; no premature collection/acceptance/completion | AC-04 | V-01, V-06, V-09a–f, V-12 |
| Usable actual producer contract and collector rerun boundary with honest proof limits | AC-05 | V-13, corroborated by V-01–V-12 |

## Source and revision

Source brief: skills/task-orchestrator/docs/tasks/T-004.1/brief.md
Source brief revision: 1
Verification revision: 1
Authority: derived from the task brief, its parent P-01/02/06, cited plan ART-003/005,
IF-003, INV-001/002/003/007/008, FLOW-001 steps 2–4, owner-confirmed single-task sbx
direction and the accepted T-003 successor contract (including inherited T-002 rules)
Status: ready

Preflight must confirm the exact frozen policy projection and available local
fixtures before implementation. The cases specify required decisions, not new
API names or an execution-enforcement design. A material authority/enforcement
gap returns to task design; it cannot be filled by a fallback in implementation.
