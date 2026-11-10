# T-003 successor controller contract

Implementation submission: READY_FOR_REVIEW, not independent acceptance.
Authority: brief revision 1 and verification revision 1. Consume the accepted
[T-002 contract](../T-002/controller-contract.md) for init/status/reserve,
owner-bound revision, immutable authority loading and correction accounting.
This supplement extends those operations; it does not implement the full loop.

## Public boundary and payloads

Library: `skills/task-orchestrator/scripts/controller.py`, Path arguments and
JSON-compatible dictionaries. The new callables are:

| Callable | Inputs / returned statuses |
|---|---|
| `launch_operation(run_dir, assignment, *, codex_bin="codex", timeout_seconds=300)` | Exact reserved assignment from `reserve_operation`; positive finite timeout; launched/replayed/refused. Starts a detached adapter supervisor. |
| `observe_operation(run_dir, operation_id)` | reserved/running/unknown/terminal/replayed/refused; the sole public outcome collection/admission path. |
| `stop_operation(run_dir, operation_id)` | Persist stop request and observe; terminal for known-unlaunched cancellation, otherwise running/unknown/terminal/replayed/refused. |
| `record_intervention(run_dir, request)` | recorded/replayed/refused; appends observed active-chat history without changing execution authority. |

CLI uses `controller.py launch --run-dir RUN --request ASSIGNMENT.json
--codex-bin codex --timeout-seconds 300`, `observe` / `stop --run-dir RUN
--operation-id operation-NNN`, and `intervene --run-dir RUN --request REQUEST.json`.
`--request` for launch contains the assignment object itself, not a reservation
response. These commands emit JSON; refused exits 1, other statuses exit 0;
outer CLI parsing/file errors retain the existing exit-2 behavior. Library
refusals carry reason/detail. No commit, finalization, completion or automatic
advance command is added. `run-next` remains its older refusal/reporting stub.

`status_run` adds `interventions` and `chat_relay_action`. Its operation history
now includes optional `transport` with configuration SHA-256, supervisor PID
(or null if publication was interrupted), and a once-published outcome. The run
state can remain ready while its embedded operation is running or unknown;
operation state and active pointer govern writer exclusion. State revision
increments on each ledger mutation, not on replay or passive observation.

## Launch authority and records

Launch reloads the current policy/manifest/frozen inputs through T-002 loaders,
validates the active assignment and actor selection, and rejects stale input,
policy or flow bindings. It uses the explicit frozen sbx/YOLO/active-chat policy.
An incompatible old policy/run requires a new reviewed run; no migration exists.
A verifier assignment is refused: the check pipeline belongs to T-004.

`actors/operation-NNN/` contains:

- `launch.json`: immutable assignment, execution authorization, cwd, CLI and timeout;
- `prompt.txt`: assignment, frozen documents/scope/checks and full frozen run policy;
- `state.json`: adapter observations (atomic replacement while running);
- `events.jsonl`, `stderr.log`: raw child observations;
- `result.json`: raw actor output if produced;
- `result.state.json`: exclusive terminal adapter receipt;
- `supervisor.stdout.log`, `supervisor.stderr.log`: bridge diagnostics;
- `stop.request.json`: optional idempotent stop request.

The controller publishes `unknown` and the configuration digest in the ledger
before spawning the supervisor. It then publishes supervisor PID/running state.
Any interrupted interval retains no-relaunch intent. Repeating the same launch
returns the original operation; changing its CLI/timeout is a configuration
conflict. A stale assignment refuses even if it was historically launched.
Reservation replay still uses the original request/version/key and never launches.

The adapter runs fresh `codex --ask-for-approval never exec --json --sandbox
danger-full-access --model gpt-6.1-sol --config
'model_reasoning_effort="low|medium|high"' --output-schema ACTOR_SCHEMA -o RESULT
PROMPT`. The frozen flow maps light/standard/strong to low/medium/high. Every
actor starts fresh, including correction and separate collection/acceptance.
There is no resume operation in this path. Below-threshold reliable context reuse
is permitted by policy but not required; unknown context always stays fresh.
Legacy adapter start/resume retains its full-access refusal. The actor bridge
accepts full access only with the explicit authorization object.

## Observed outcome and admission

`assets/actor-result.schema.json` declares exactly `assignment`, `session_id`,
`status`, `summary`, `readiness`. Assignment echoes the complete reserved object.
Status is complete/blocked/failed/needs_input. `session_id` is the observed
thread ID if known to the actor, otherwise null; an invented nonnull ID refuses.
The adapter obtains session identity from `thread.started`, process identity
from Popen and exit from wait. Actor prose is not process/session provenance.
`configured_model` is explicit; `observed_model` remains null because this bridge
does not establish provider model identity.

The adapter must have recorded a reaped actor (`terminal_observed`) and absent
process group (`group_absent`) in its terminal receipt. A result file, exit
claim, missing PID, stop request or live supervisor alone cannot establish this.
Observation validates receipt assignment and configuration binding before
terminal admission. Raw malformed/missing/wrong-binding results are retained or
identified as absent. Their terminal outcome has a blocker; they never advance.
Repeated terminal observation replays the embedded outcome without reading a
replacement actor claim or overwriting history. No tamper-resistance against
coherently rewritten controller records or YOLO actors is claimed.

Single semantic extension point: `observe_operation` reads observed terminal
records and calls `_admit_actor_outcome`; `_publish_actor_outcome` publishes the
resulting ledger snapshot under the same command lock. T-004 and T-005 must
extend that path, not admit actor output through a competing writer/API.

Only preflight semantics are currently admitted. Its result must be complete and
bound to the current terminal preflight operation and observed session.
`readiness` has exactly `status: ready`, `requirements_complete: true`, and
`tools`, `dependencies`, `skills` arrays. Each item is `{name, status, evidence}`
with nonempty name/evidence and status passed. Empty arrays attest no requirements
in that family. The preflight actor checks the frozen task's prerequisites in
its execution environment. The controller checks the structured attestation;
it does not extract a complete dependency manifest from prose or independently
re-execute all claimed checks. False/missing reported requirements block. A
trusted coordinator and independent review remain necessary for semantic truth.

Successful admission records input/policy/flow/task/operation-bound readiness,
passed preflight evidence and implement cursor. It enables one initial
implementation. Failed preflight records blocked evidence and precise blocker.
Preflight/retries do not charge correction count. Revision and environment repair
invalidate readiness; a prior operation cannot restore it by repointing its
reference. Existing shared three-correction accounting is unchanged.

Implementation, collection and acceptance outcomes undergo envelope/provenance
validation and raw capture only. They do not establish a candidate, passed
checks, collected findings, acceptance, repair authority or completion. T-004
consumes the implementation/collection raw paths and bound adapter observations;
T-005 consumes separately launched acceptance raw output and the same observations.
Tests seed only unavailable successor candidate/check/reason prerequisites and
label those fixtures. They do not demonstrate production successor admission.

## Stop, intervention and replay

Stop writes a request for the supervisor; it never sends a signal to a stored
PID. The supervisor terminates the child group and observes exit. A surviving
or ambiguous group, missing supervisor receipt or uncertain launch publication
leaves the operation running/unknown. Unknown ownership permits observation,
stop request and intervention, never retry or a second writer. If uncertainty
cannot be resolved from existing receipts, an owner must inspect/resolve it;
there is no automatic recovery service, refund or power-loss guarantee.

Blocked terminal/unknown observations persist opened intervention records with
blocker, evidence location, unresolved operation and required action. Explicit
`record_intervention` requests have string fields `key`, `blocker`, `evidence`,
`operation_id`, `required_action`, `event`, `text`; events are opened/relayed/response.
Empty operation_id is allowed for a blocker without a reservation. Exact events
replay; changed subject fields under an existing key refuse. Relay and response
are unknown until observed events are recorded. No message is sent externally.
Acknowledgement and silence authorize no repair, revision, retry or completion.
Budget exhaustion remains a reservation refusal and status blocker; the
coordinator can persist its precise intervention using this same interface.

Examples: wrong role in launch assignment → launch_refused and zero actors;
missing tool in preflight → terminal blocked readiness, no implementation;
identical launch while running → replayed, same operation; interrupted launch
publication → unknown, no relaunch; repeated stop after terminal → replayed;
fourth correction → corrections_exhausted with count/history/work preserved.

## ART-008 runtime supplement and proof limits

Selected bridge: existing Codex CLI inside existing owner-supplied Docker sbx,
with fresh sessions and approval-never/full-access argv above. The coordinator
runs inside sbx on a separate branch; no containment detection/provisioning is
implemented. Task scope and frozen permissions remain actor instructions;
runtime tool exclusion/reviewer read-only enforcement is outside this direction.

Local evidence uses stdlib Python, real Git/filesystem/child processes and a
local fake Codex. It observes actual invocations, prerequisite probes, input
bytes, session events, implementation marker, stop/timeout, lock contention and
SIGKILL of controllers at four publication checkpoints. These establish local
wiring and conservative persistence, not sbx/provider/model qualification.
Exact commands/results and every V-01..14 row are in implementation-report.md.

V-13: **NOT RUN**. Separate live approval, an existing approved sbx, usable real
Codex/provider configuration and reviewed disposable task inputs are required.
T-006 owns the approved follow-up: public preflight launch/admission, one bounded
implementation marker/result, observed terminality and reloaded status. This is
separate from T-006's full correction/collection/acceptance pilot. Historical
T-001 INCONCLUSIVE/isolation limits are preserved; no old host containment result
or fake executable closes real-runtime proof. No live check was attempted.
