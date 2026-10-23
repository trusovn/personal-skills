# T-002 controller contract for successors

Current implementation submission: T-002.3, READY_FOR_REVIEW. This consolidates
the accepted [T-002.1 contract](../T-002.1/controller-contract.md) and
[T-002.2 contract](../T-002.2/controller-contract.md), extending them with input
revision. It does not accept T-002.3, close the parent or advance T-003.

## Public controller boundary

Import `skills/task-orchestrator/scripts/controller.py`. Library paths are
`pathlib.Path` objects; request/response objects are JSON-compatible dictionaries.

| Callable | Request / result |
|---|---|
| `init_run(run_dir, policy_path, manifest_path, repository)` | Validate one prepared task and publish a run outside the Git repository; return run/state/ledger/baseline paths. |
| `status_run(run_dir)` | Read one ledger snapshot and immutable authority; return status, identities, version, stage, correction count, evidence, operation/history and next actions. No selection, lock or mutation. |
| `reserve_operation(run_dir, *, expected_version, task_id, stage, role, operation_key, reason="initial")` | Return `reserved`, exact-request `replayed`, or `refused`; no actor launch. |
| `revise_inputs(run_dir, request)` | Publish an explicitly owner-authorized revision, return `revised`, exact-request `replayed`, or `refused`. |
| `load_input_authority(run_dir, ledger)` | Return `(policy, manifest, frozen_inputs)` for the supplied ledger snapshot, verifying their current identities. Use this after revision instead of opening the initial policy/manifest files. |
| `load_frozen_inputs(run_dir, ledger)` | Return the frozen document/scope/check projection from that same authority. |

CLI examples, from repository root:

```sh
python3 skills/task-orchestrator/scripts/controller.py init --run-dir /tmp/run --policy /tmp/policy.json --manifest /tmp/manifest.json --repository /tmp/repo
python3 skills/task-orchestrator/scripts/controller.py status --run-dir /tmp/run
python3 skills/task-orchestrator/scripts/controller.py reserve --run-dir /tmp/run --expected-version 1 --task-id T1 --stage preflight --role preflight --operation-key preflight-1 --reason initial
python3 skills/task-orchestrator/scripts/controller.py revise-inputs --run-dir /tmp/run --request /tmp/owner-revision.json
```

Reserve/revision CLI results are JSON on stdout; success/replay exits 0 and
refusal exits 1. Unhandled CLI input/file exceptions use the existing main
handler's structured stderr refusal and exit 2.

## Formats, policy and identities

Executable declarations are `scripts/controller_state.py`'s
`validate_run_policy`, `validate_flow_profile`, `validate_ledger`,
`validate_actor_operations`, `validate_input_revision_request` and
`validate_input_revisions`. There is no separate JSON Schema for the ledger,
assignment or revision request. Existing JSON Schemas remain:

- `assets/run-policy.schema.json`: policy version 2, explicit single-task
  sbx/YOLO authorization and active-chat intervention, permissions/checks and flow.
- `assets/flow-profile.schema.json`: flow version 2, all eight ordered stages.
- `assets/task-manifest.schema.json`: manifest version 1.
- `assets/handoff.schema.json` and `assets/step-outcome.schema.json`: role-bound
  version-1 envelopes; reported actor outcomes do not admit semantic evidence.

The eight stages are ready/controller, preflight/preflight,
implement/implementer, verify/verifier, semantic_review/review_collector,
acceptance/acceptance_reviewer, accept/controller and completed/controller.
Controller stages use mode `off` but remain mandatory. Collection and acceptance
cannot merge. Actor mapping is exactly `gpt-6.1-sol`: light/low,
standard/medium, strong/high reasoning. Correction limit is exactly three shared
cycles including environment repair. Session reuse policy permits `reuse` only
for reliable finite occupancy in [0, 0.5); unknown/unreliable/invalid occupancy
requires `fresh`. Reservations conservatively assign fresh correction sessions.
No adapter flags or model execution are qualified by these declarations.

Initialization freezes `run-policy.json`, `task-manifest.json`, `inputs.json`,
`flows/flow-001.json` and initial Git baseline. Frozen input version 1 contains
task ID, brief/verification source paths, UTF-8 content and byte SHA-256, allowed
paths and required checks. Source paths are provenance; readers do not substitute
mutable repository text. Inputs use canonical JSON without a trailing newline.
Policy and manifest SHA-256 use sorted compact JSON without a newline; flow
SHA-256 uses canonical JSON with one trailing newline. The implementation uses
Python `json.dumps(..., sort_keys=True, separators=(",", ":"))` defaults,
including ASCII escaping. Digests establish consistency, not external identity
or protection against coherent whole-run tampering.

Ledger format remains version 1. `revision` is the state version; reservation
and admitted revision increment it once. `flow_revision` is a separate counter.
Existing compatible runs are read without an installation or state migration;
incompatible frozen policy/flow/inputs require a new reviewed run.

## Status and reservations

Status includes `run_id`, `task_id`, input/policy/flow identities, `state`,
`state_version`, `stage`, `attempts`, `correction_count`, candidate, current
references, five required evidence stages, policy omissions, outstanding
findings, readiness, active operation, operation history, input revision history,
next actions and blocker. It exposes missing, passed, failed, stale, blocked and
not_run distinctly. Input/candidate mismatches make evidence stale; omission of
a mandatory role is blocked. Targeted verification omits only the repository
gate, never required actor stages.

Both mutations hold the existing nonblocking `RunCommandLock`. Embedded
assignments/charges and revision receipts publish through atomic replacement
of `ledger.json`. Status uses its one ledger snapshot and immutable files, so
concurrent publication cannot expose a mixed eligible authority.

Reservation request fields are expected_version (positive integer), task_id,
stage, role, operation_key (nonempty), and reason. Supported pairs are:

| Stage / role | Prerequisites |
|---|---|
| preflight / preflight | Initial/preflight cursor or fresh readiness needed. |
| implement / implementer | Implementation cursor, current terminal preflight readiness, no prior cycle-zero implementation for this task. |
| correction / implementer | Admitted matching reason (`check_failed`, `review_findings`, `environment_repair`) and count below three; ordinary corrections need readiness. |
| verify / verifier | Current candidate and passed current implementation evidence. |
| semantic_review / review_collector | Current candidate and passed current check evidence. |
| acceptance / acceptance_reviewer | Current candidate and passed current collection evidence. |

Assignments contain run/task/operation/key/stage/role/reason, input/policy/flow
identities, flow revision, candidate, correction_count, can_change_files,
can_repair, actor and session_policy. Verify has actor null. Other actor
profiles resolve from the frozen flow. Each operation is embedded with
operation_id `operation-NNN`, request, assignment and state
reserved/running/unknown/terminal. Only the latest may be active; its task,
stage, authority, candidate and actor must match current state. Its active
pointer is `actor_operations/operation-NNN`, an embedded reference.
Unknown ownership permits observation/intervention, never another actor.

Exact reservation replay requires the original key, payload and expected
version, and is resolved before staleness. It returns the original assignment
and current version without writing or granting a second launch. Conflicting
requests refuse. Cycle zero is free once per task. Each new correction charges
one immediately, with no automatic uncertain-launch refund; replay, preflight
and evidence-only retries charge nothing. A revision cannot authorize another
free cycle zero or a fourth correction. **Environment repair invalidates
readiness and requires fresh preflight**, even before initial implementation.

## Authorized revision request

The request has this exact shape. `policy` and `manifest` below are complete
valid objects, for example the values returned by `load_input_authority`.
Document text and owner/provenance values come from the actual approved change
and owner response. This example assembles the JSON-compatible request:

```python
request = {
    "expected_version": 9,
    "task_id": "T1",
    "revision_key": "owner-change-17",
    "payload": {
        "policy": policy,
        "manifest": manifest,
        "documents": {"brief": approved_brief_text,
                      "verification": approved_verification_text},
    },
}
binding = controller.sha256_text(controller.canonical_json(request))
request["authorization"] = {
    "kind": "owner_response",
    "decision": "authorize_input_revision",
    "owner": owner_identity,
    "provenance": owner_response_reference,
    "request_sha256": binding,
}
```

Hash the canonical JSON object
containing expected_version, task_id, revision_key and payload, without
`authorization` and without a trailing newline. The digest binds the owner
response to the exact change and expected version. The API requires an explicit
owner decision, nonempty owner/provenance and a matching binding.
Acknowledgement, actor-result authorization or prose is insufficient. The
trusted coordinator must obtain and accurately record that response; this API
does not authenticate a chat service, sign the record or infer consent.

Policy must still pass every mandatory rule. Run ID, repository and selected
task cannot change; completed-task history cannot be replaced. Manifest scope,
checks, title/brief provenance and dependencies are revalidated under existing
rules. Revision consumes the supplied document content, never edits repository
files, and cannot make invalid policy valid through owner authority.

A new revision requires the current expected version, no reserved/running/
unknown actor or legacy active attempt/finalization, and a noncompleted task.
A pending interrupted legacy flow revision must be resolved first.

## Revision persistence, invalidation and replay

Prepare immutable `input-revisions/revision-NNN.json` containing version 1,
request and frozen inputs. Revised inputs additionally contain revision_key,
policy_sha256 and manifest_sha256, so even policy-only change or returning to
old document text has a distinct input identity. Bundle/input digests bind
canonical bytes without a newline. The bundle includes the policy, manifest
and flow through request.payload; after publication ledger policy_path,
manifest_path and flow_path all reference that bundle. Consumers must use the
loader above, not assume these paths each contain a standalone policy or flow.
The flow counter increments only when the resolved flow's digest changes.

One ledger replacement publishes all new identities, paths, task projection,
version and `input_revisions` receipt together. Each receipt contains request,
path, sha256, inputs_sha256, state_version and `previous`, the preceding ledger
snapshot without its input_revisions list. Earlier receipts remain in the
outer history. Initial files and earlier bundles remain untouched.

Revision sets ready state with selected task and preflight cursor, clears
readiness/candidate/correction authorization and current closure/check/decision
references, and preserves correction count, attempt/operation history,
outstanding findings and raw evidence. Old references/readiness remain in the
previous snapshot; old raw evidence displays stale through its old input
identity. Historical files are unchanged. Fresh preflight must be admitted
before implementation; a task already implemented needs successor admission of
an appropriate correction reason instead of another initial implementation.
T-003/004/005 own that admission and must not restore old input-bound evidence.

Success returns status revised, state_version, revision_state_version,
inputs_sha256 and revision_path. Exact historical replay returns status replayed,
the current state_version and original revision_state_version/identity/path;
it does not restore historical authority. Changed requests with a reused key
are revision_key_conflict. A stale new key is stale_version.

Before ledger publication, prepared content is ineligible and readers see the
old coherent authority. Exact retry may reuse identical prepared bytes;
different pending bytes cause pending_revision_conflict. After ledger
publication, readers see the new coherent authority and exact retry replays.
A caught publication failure returns revision_publication_uncertain, null
state_version and intervention: read status and retry the exact original
request. A new operation that advances old state before retry makes the old
request stale; a conflicting prepared bundle requires explicit intervention.
No recovery service, automatic orphan deletion or power-loss qualification is
provided. Real process-exit tests cover OS lock release and both commit sides.

Example refusal reasons: invalid_revision_request (missing authority, ack,
binding mismatch or invalid policy), task_mismatch,
run_task_or_repository_mismatch, task_completed, operation_reserved/running/
unknown, operation_active_or_unknown, stale_version, completion_history_mismatch,
pending_flow_revision, pending_revision_conflict, revision_key_conflict and
authority_or_lock_unavailable. Invalid requests preserve authoritative version,
identities, count, history and task files. A diagnostic controller.lock file may
be created; it has no authority.

## Successor ownership and local evidence

T-003 owns sbx launches, observed actor/session/terminal identity, outcome and
preflight readiness admission, interruption/stop/intervention and chat relay.
Readiness must reference a terminal current-authority preflight operation.
T-004 owns candidate/check/collection semantic admission; T-005 owns independent
acceptance admission and completion publication. Missing successor evidence
cannot be replaced by actor claims, pure cursor transitions or mechanical checks.

Public run-next reports pending work without launch. Inspect refuses active
ownership or reports successor inspection pending for actor history. Legacy
flow-only revision requires the original exact unselected cycle-zero boundary;
a revised task cannot use it. Generic ledger mutation cannot inject admission,
change authority/revision history or reset reservation counting. Private legacy
transport is unavailable after input revision. No public completion operation
exists in T-002.

Exact implementation evidence is in
[T-002.3 implementation-report.md](../T-002.3/implementation-report.md).
Focused revision suite: 8/8 pass. Owning controller/state/Git suite: 152 tests,
145 pass, 6 errors and 1 failure at the unavailable macOS sandbox boundary on
Linux/Python 3.14.4. A representative unchanged HEAD test reproduces that
UnsupportedSandbox error. State suite: 44/44 pass. No schema/syntax check is
counted as behavioral evidence. Independent discovery owns the final aggregate
gate and corroboration, followed by a separate acceptance decision.

No live sbx actor/model launch, runtime provenance proof or first useful sbx
proof was run or completed. The seeded terminal/readiness/check/review records
in the composed tests are explicitly future-admission setup, not its proof.
