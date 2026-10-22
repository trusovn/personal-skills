# ART-008: Local harness contract

Contract version: 1.0 (investigation contract, not an implemented adapter API)
Observed: 2026-10-22
Submission: READY_FOR_REVIEW; independent discovery and acceptance outstanding
Runtime qualification: BLOCKED
Source: [brief.md](brief.md), [verification.md](verification.md) revision 1,
[preflight.md](preflight.md)

The smallest bridge is the existing Python subprocess path to **Codex CLI
0.163.0**, at `/opt/homebrew/bin/codex`. Retain its useful process/output code;
do not build a native-delegation backend. This selects the transport for further
work, not a qualified end-to-end harness. Required permission, recovery, context
and notification proof is missing. No dependent implementation is declared ready.

## Evidence and scope

Evidence levels used below: **observed** means an actual local command/fixture;
**source** means inspected implementation; **documented** means official product
documentation; **proposed** means a downstream contract with no implementation.
Supported at one level does not imply support at another boundary.

| ID | Evidence / reproduction from repository root | Result / limit |
|---|---|---|
| E1 | `command -v codex`; `codex --version`; `codex exec --help` | `/opt/homebrew/bin/codex`; `codex-cli 0.163.0`; exit 0. Sandbox choices, JSONL, schema, model/effort configuration and output-file options exist. PATH-alias permission warning is printed. No model started. |
| E2 | `codex --ask-for-approval never exec resume --json --output-schema skills/task-orchestrator/assets/worker-result.schema.json -o /tmp/t001-unused-result.json -c 'sandbox_mode="read-only"' --help` | Exit 0; exact resume parser accepts this shape. Help creates no actor result; it proves neither effective permissions nor model availability. |
| E3 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py -k test_start_persists_thread_and_structured_result` | 1 test, OK, 0.469 seconds. Existing disposable fake CLI emits a thread event and structured result; wrapper records both. |
| E4 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py` | 15 tests, OK, 4.474 seconds. Includes resume, missing thread, unsafe-CLI refusal, timeout/SIGTERM descendant cleanup, live-PID refusal and malformed/missing result. Real wrapper/process/files; fake runtime, no permission qualification. |
| E5 | `PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_local.py` | Real disposable Git: exact path commit; original index bytes and all worktree bytes preserved; pre-publication HEAD unchanged; post-publication reconciliation; stale ref update refused; exactly 2 commits including fixture base. See script assertions and limits below. |
| E6 | `codex sandbox --help`; `codex app-server --help` | Exit 0. Local sandbox accepts a command directly, `-P/--permission-profile`, and opaque sandbox-state JSON. App server offers stdio and schema generation. Neither was started. |
| E7 | Source references in the following sections | Inspection only. No live run records, production code, installation, project commit or owner notification changed. |

Repository HEAD at investigation: `8efffca9e38855e8229764851d570a72aa7a857b`.
Initial dirty entry was `?? skills/task-orchestrator/docs/tasks/`, containing the
owner's brief. New artifacts are distinct files. Plan SHA-256
`98fab11ed34846bbe7c0596ea293be5908b763573ac8b0b988f3f4f5441452fd`
and map SHA-256
`7e6a0a379c360c373934cfa88ee03dcdf32175aae4cc8ac1286cb7a73f9ad440`
match [the accepted plan review](../../project-plan-review.md).

Official documentation retrieved on the observation date:

- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
  documents script execution, JSONL thread/turn events, structured final output,
  saved-session resume and terminal token usage. These support the selected CLI
  shape; no current-context occupancy measure is established there.
- [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
  describes sandbox enforcement and macOS Seatbelt. This is documentation,
  not a denial observation on this machine. Its platform-subcommand example
  differs from E6; use installed help for this version.
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
  lists `notify` as a command receiving a JSON payload. It does not establish an
  intervention-only delivery receipt usable by this controller.

## Selection and callable boundaries — AC-01

Python can call `subprocess.Popen`/`subprocess.run` on the installed binary.
[`codex_worker.py`](../../../scripts/codex_worker.py) already supplies `start`,
`resume`, `run_turn`, `process_liveness` and `terminate_process_group` internally.
Its operator CLI remains internal; the public entry points are
`controller.py init`, `run-next`, `inspect`, `revise-flow`, as described by the
[operator guide](../../../references/operator-guide.md).

Interactive `collaboration.spawn_agent`, messages, interruption and waiting are
tools supplied to this coordinator session. No Python binding, durable receipt
API or inherited permission contract for them was supplied. Their visibility to
the coordinator is not evidence of controller-callability. App-server help is
an alternative interface inventory only; no second backend is selected or built.

| Interface | Callable today | Proposed spelling for successor work; not callable today |
|---|---|---|
| IF-001: coordinator → controller | Existing public commands above; no atomic operation reservation | `status`, `reserve` |
| IF-002: controller → adapter | Internal subprocess start/resume; synchronous wait; local artifacts | `launch`, `status`, `wait`, `collect`, `cancel`, `reconcile`, `notify_intervention` |
| IF-004: coordinator → controller | `inspect` supplies mechanical eligibility only | `accept`, `recover`, `advance`; controller-owned commit finalization |

Version support is limited to observed parser compatibility at 0.163.0, not all
older/newer versions or successful sessions. T-003 must recheck the resolved
binary/version and fail closed on incompatible CLI or permission settings.

## Identity and recovery — AC-02 / R1

Existing `run_turn` writes `starting` state before Popen, then records PID after
spawn. It reads `thread.started.thread_id` from runtime stdout and writes events
and stderr. It waits synchronously; timeout or handled interruption terminates
the process group and persists a terminal snapshot. `resume` rejects live and
permission-ambiguous PIDs, and running state with no PID. These are source plus
E4 wrapper observations. They are not an exactly-once operation service.

The exact proposed v1 request boundary for each adapter operation is:

- Common envelope: `version=1`, `run_id`, `task_id`, `operation_key`,
  `assignment_sha256`, `expected_state_version`. The controller owns these;
  the actor does not choose them. Launch also carries `role`, `candidate_id`,
  `flow_revision`, immutable `policy_sha256`, resolved `model`, `reasoning`,
  effective permissions, prompt/schema paths and external artifact directory.
- `launch(envelope, assignment)` returns an adapter receipt or an explicit
  `unknown` launch outcome. Under the reserved operation lock, persist intent
  before spawn and the observed PID/process-start identity/thread identity as
  they become available. Receipt fields include adapter version, executable
  identity, argv/policy digest, host boot/process-start identity, observed thread
  ID, timestamps and artifact references. Missing observations remain null/unknown.
- `status(envelope)` returns `live`, `terminal`, or `unknown`, with observed
  process identity and reason. A PID alone cannot prove ownership after reuse.
- `wait(envelope, deadline)` returns that same status shape after bounded waiting.
  A wait timeout is not proof of cancellation or terminality.
- `collect(envelope)` returns `pending`, `invalid`, or `collected`, plus receipt
  reference, process exit, result digest, runtime thread/turn observations and
  diagnostic references. Collection of the same terminal bytes is idempotent.
  Exit zero without a validated structured result is invalid, not completion.
- `cancel(envelope)` signals only an identity-matched owned process group,
  waits, and returns observed terminality or unknown. A signal sent is not proof
  the actor and descendants have stopped.
- `reconcile(envelope)` returns `live`, `terminal`, or `unknown` with evidence
  references. It never launches. Only positive evidence that no old writer can
  remain allows the controller to reserve a new operation.

These names and fields fix the handoff boundary; T-002/003 must implement and
test their record encoding. They do not claim new production declarations.
The adapter owns receipts outside the actor-writable tree, while the controller
owns assignments/reservations. Bind the receipt to the reserved role, task and
candidate, and retain the raw event source. A result's claimed ID or role cannot
create provenance. A fresh review needs a new observed thread distinct from all
implementation and previous review threads; never resume implementation as review.

| Case | Existing observation / limitation | Required disposition |
|---|---|---|
| First launch | Thread event and result persisted in E3/E4 | Wrapper-supported; real CLI launch still unverified |
| Same operation repeated | `start` rejects an existing state path; no controller key or atomic launch/receipt transaction | No idempotent launch support today. Return existing receipt for identical assignment; reject key/payload mismatch; never start twice |
| Live | E4 refuses recorded live PID on resume | Retain ownership and wait/cancel; robust process-start proof still missing |
| Terminal | E4 result and state artifacts | Collect once, validate provenance; terminality alone does not pass acceptance |
| Unknown | Source handles some ambiguous PID cases, not all launch windows | Block launch, finalization and dependency release |
| Spawn without receipt | Popen can succeed before PID persistence; `starting` with null PID/thread does not prove no spawn | Unknown; do not call `start` or `resume` to guess. Require external process ownership proof or owner-controlled stop/reconciliation |
| Replacement coordinator | Existing external artifacts survive handled interruption | Read controller ledger and adapter receipts; chat history and actor claims do not establish liveness |

Current files are `state.json` and per-turn `turn-NNN.prompt.txt`, `.events.jsonl`,
`.stderr.log`, `.result.json`, `.result.state.json` beneath `--run-dir`.
Wrapper writes are atomic replacements or exclusive creation, not authenticated
or power-loss-durable storage. A new adapter must place them beneath the external
run root with access denied to actors. Unknown receipt/liveness must stay unknown.
Concurrent start and SIGKILL/power-loss windows lack qualification; E4's handled
SIGTERM is not a substitute. No launch was attempted in this investigation.

## Permissions and frozen policy — AC-03 / R2

`start` passes `--sandbox read-only|workspace-write` and global approval `never`;
it rejects danger-full-access. Resume passes sandbox through `-c` (E2). This is
configuration/source evidence only. The wrapper records `network=False` and
`writable_roots=[cwd]` without measuring the effective runtime permissions.
It does not isolate user configuration, hooks, external tools or MCP capabilities.
Therefore these recorded values cannot be used as an enforcement receipt.

Required layout: implementation may write its approved candidate workspace;
review may read it but may not write it. Both must be denied writes to external
run records and active controller/skill roots. A project-local skill installation
inside a broadly writable workspace needs demonstrated protection or a separate
approved layout. Post-hoc scope checks and prompt instructions do not enforce
this boundary. Temporary roots, symlinks, Git metadata and inherited tool paths
must be included when qualifying effective access. No assertion of deny coverage
is made for any of them here.

E6 exposes a non-model sandbox command, but this investigation did not execute
write attempts through it. Neither E4 fake argv nor the separate
[`verification_runner.py`](../../../scripts/verification_runner.py) Seatbelt
profile qualifies the selected actor boundary. Missing proof: an allowed task
write, denied reviewer write, and denied run/controller/skill writes under the
same effective policy and all enabled actor write tools. Obtain this locally
first; any required privilege expansion needs owner authorization. A model pilot
is separately authorized, never implied by this report.

[`controller_state.py`](../../../scripts/controller_state.py), `ACTOR_LEVELS`
and `IMPLEMENTATION_SESSION_REUSE_THRESHOLD`, match
[`flow-profile.schema.json`](../../../assets/flow-profile.schema.json):

| Tier | Frozen model | Reasoning |
|---|---|---|
| light | gpt-5.6-sol | low |
| standard | gpt-5.6-sol | medium |
| strong | gpt-5.6-sol | high |

The implementation-session reuse threshold is exactly `0.5`. CLI model/effort
arguments exist, but account availability and observed effective model/effort
have not been tested. Do not substitute the coordinator's model or a newer model.
No current code measures context occupancy or implements the reuse decision.
The documented terminal token counters are turn usage, not an established
current-context numerator plus effective model-window denominator after compaction.
The selected adapter has no qualified measurement source; usage is **unknown**,
never zero. Correction context reuse is blocked until a trustworthy source and
threshold semantics are established, or the owner approves a policy change.
Default correction limit 2 in current code is also not the direction's required
3; the existing schema permits a configured finite limit, but successor workflow
work must explicitly implement the approved three-cycle rule. T-001 changes none
of these policies.

## Commit support — AC-04 / R3

Safe primitive support is **observed at disposable Git boundary only** (E5).
The probe builds a temporary index from HEAD, stages only `task` there, writes
a tree, creates a commit using `git commit-tree TREE -p PARENT`, then publishes
with `git update-ref HEAD COMMIT PARENT`. No user hook or signing command is run.
Unrelated staged, unstaged and mixed staged/unstaged owner content remains byte
identical, including the real index. Failure of the stale expected-parent update
is observed. Existing `controller_git.py` inspects identity/scope; it does not
implement this commit path.

Proposed controller finalization must hold exclusive writer ownership, recheck
accepted candidate/policy/HEAD/index/scope and refuse owner changes on accepted
paths. An accepted-path owner staging overlap is not proved safe by this probe;
refuse rather than overwrite it. Refuse unsupported repository layouts/states
(unmerged index, concurrent writer, ambiguous ref ownership) until qualified.
Persist a durable intent with operation key, parent/ref identity, accepted paths,
candidate/tree digest and original index identity. Persist the exact commit OID
before compare-and-swap publication, then receipt with observed HEAD/tree/parent.
No remote operation is needed or authorized.

Recovery reads intent before doing any new commit: HEAD equal to intended commit
with matching tree/parent permits receipt recovery; HEAD equal to parent permits
publication of the already recorded commit; any other identity is unknown/conflict
and blocks release. Before an OID was recorded, an orphaned commit object is not
a published completion; reconcile HEAD before generating another. Never infer
success from a commit message or retry a high-level commit blindly.

E5 simulates two control-flow interruption points; it does not kill a controller
or prove fsync ordering. Original task index entries remain at baseline after
HEAD moves and can appear staged in reverse. T-005 must qualify safe exact-task
index reconciliation that preserves all owner entries, durable intent/receipt,
crash windows, additions/deletions/renames/modes and repository hooks/signing
policy before completion. Until then commit finalization is **unverified**, and
the public controller has no accept/commit/release path. `off` cannot satisfy the
planned dependency-release boundary.

## Intervention support — AC-04 / R3

No implemented controller notifier or qualified delivery channel was found in
the inspected scripts. Codex's documented `notify` hook does not establish an
intervention-only trigger, recipient routing or acknowledged delivery for Python.
The interactive response channel does not supply a durable controller receipt.
No actual notification was sent and no user configuration was read or changed.

Proposed `notify_intervention(envelope, intervention_id, reason, evidence_refs)`
first persists the intervention. A controller-owned notifier returns `delivered`,
`failed`, or `unknown`, with channel/recipient reference, attempt ID, timestamp,
exit/error and channel receipt. Only an observed channel acknowledgement supports
delivered; command invocation, stdout or a local record alone does not. A timeout
is unknown and retries must follow the channel's idempotency semantics. Failure
or unavailable delivery stays visible in `status` with a manual next action.
No delivery state clears the blocker or releases a dependent task. Emit active
notifications only for required owner intervention, not routine success.

This is **unsupported by the current controller; real delivery unverified**.
Smallest owner action: select/authorize a local delivery channel and a bounded
delivery test. T-003 must expose channel failure and uncertain delivery; T-006
must prove the intervention branch. No live test is authorized by T-001.

## Capability dispositions and consumer handoff — AC-05

| Required capability | Disposition and evidence level | Missing proof / owner |
|---|---|---|
| Python-callable transport and version | Supported parser/source; E1/E2 | T-003/006: actual independent CLI sessions with approved frozen model |
| Result persistence, validation, handled interruption | Supported wrapper fixture; E3/E4 | T-003: adapter receipt binding; T-006: real runtime outputs |
| Exactly-once launch, cancel/status/reconcile across replacement | Unsupported as a public service; partial source mechanics | T-002/003: reservation, lock, process-start identity, spawn-before-receipt and crash probes |
| Independent observed review identity | Unverified real harness | T-003/004/006: fresh observed threads, wrong-thread rejection |
| Role/protected-root permissions and network policy | Unverified; flags/source/docs only | Capability owner: actual allow/deny probes under effective actor policy |
| Frozen model/effort availability | Unverified; E1 parser only | Owner-authorized bounded session for exact gpt-5.6-sol mappings |
| Context reuse at 0.5 | Unverified; no qualified measurement | Capability owner: occupancy source; owner decides any policy change |
| Safe exact-path commit primitives | Supported disposable fixture; E5 | T-005: integrated intent/receipt, index reconciliation and crash qualification |
| Final completion and dependency release | Unsupported current controller | T-005/006: current evidence gate plus proven commit before atomic release |
| Intervention delivery and observable failure | Unsupported current controller, delivery unverified | Owner channel choice/test authorization, then T-003/006 integration |

Q-001: **partially resolved, still blocking qualification**. Select CLI 0.163.0
as the smallest bridge; do not claim it meets the full contract. Permission and
ambiguous-launch proof remain decisive. The owner can authorize bounded missing
probes with concrete fixture scope, or pause affected work. No second backend
or weaker safeguards are silently adopted.

Q-002: **unresolved, affected runtime work blocked**. No model substitution or
threshold change is authorized. Context occupancy is unavailable at the inspected
boundary. Establish it or request an explicit owner decision on the affected rule.

T-002 may use the proposed request/identity contract for planning, but this report
does not open its implementation gate: the brief requires unresolved required
boundaries to keep affected implementation blocked. T-003 needs qualified
permissions, lifecycle and notification support. T-004 additionally needs fresh
review provenance and valid correction-context handling. T-005 needs proven
finalization/index/crash behavior. T-006 needs separately authorized real sessions
and the full correction, review, commit, dependency and intervention loop.
Fake fixtures cannot substitute for that pilot.

## Verification ledger and submission route

| Scenario | Current implementation evidence / remaining boundary |
|---|---|
| V-01 | E1/E2/E6 and source distinguish callable CLI from interactive tools; selection conditional on explicit gaps |
| V-02 / R1 | E3/E4 and source trace first/resume/live/terminal/missing result; duplicate/missing-receipt/unknown cases remain blocked as above |
| V-03 / R2 | E1/E2/E6 plus policy source; all actual permission allow/deny and usage proof remain unverified with capability owner |
| V-04 / R3 | E5 real Git primitive assertions pass; integrated crash/index and accepted-path owner-overlap proof remains T-005 |
| V-05 / R3 | Source/docs establish only hook availability; real delivery success/failure pending channel authorization and T-003/006 |
| V-06 | Disposition table accounts for every AC/risk and Q-001/Q-002; aggregate corroboration belongs to fresh discovery |

Deliverables: this versioned report, verification.md, preflight.md and probe_local.py.
Actual contract impact: adds ART-008 selection/limitations and proposed operation
boundaries for successor tasks. Executable contract declarations changed: none.
No production architecture gate, maintainability or registry update applies to
this task-local report/probe; no contract registry exists for this workflow.
Optional run-evidence writes were omitted under the brief's no-live-run-record
scope; evidence remains task-local. Broad repository suites and live model runs
were not run. No self-acceptance is claimed.

Next owner: fresh independent `task-review-discovery`, including R1 duplicate and
missing-receipt traces, R2 evidence-level check, and R3 commit/delivery assumptions;
then a separate fresh `task-acceptance-review` decision. Acceptance of the truthful
investigation must not waive the unresolved harness qualification gates.
