# T-002.1 controller contract

Status: implemented; submitted for independent review. This contract does not
constitute acceptance of T-002.1 or unblock T-002.2.

## Frozen authority

`init_run(run_dir, policy_path, manifest_path, repository)` validates one
selected prepared task. The repository must be a Git top-level directory; the
run directory must be outside it. The selected manifest task must have a real
brief and a real `verification.md` beside that brief. Invalid policy or missing
prepared input is refused before run publication.

The initializer preserves these separate authority records:

- `run-policy.json`: immutable policy version `2`, including execution
  authorization, permissions, checks, commit/stop policy and the initial flow.
- `task-manifest.json`: copied manifest, version `1`. Other manifest tasks do
  not become authorized. Exactly one ID is allowed in policy `task_ids`.
- `flows/flow-001.json`: immutable initial flow format version `2`.
- `inputs.json`: frozen task input format version `1`:

```json
{
  "version": 1,
  "task_id": "T1",
  "documents": {
    "brief": {
      "source_path": "tasks/T1/brief.md",
      "content": "<approved UTF-8 content>",
      "sha256": "<SHA-256 of original UTF-8 bytes>"
    },
    "verification": {
      "source_path": "tasks/T1/verification.md",
      "content": "<approved UTF-8 content>",
      "sha256": "<SHA-256 of original UTF-8 bytes>"
    }
  },
  "allowed_paths": ["allowed.txt"],
  "required_checks": ["make test"]
}
```

Paths in `documents` are repository-relative provenance. Loading approved
inputs does not read those source files. The ledger binds exact `inputs.json`
bytes through immutable `inputs_sha256`. Input JSON uses sorted keys, compact
separators and no trailing newline. Policy and manifest digests also bind
canonical JSON without a trailing newline; flow digests bind canonical JSON
with a trailing newline.
Together these ledger references identify the approved initial input revision.
Ledger format remains version `1`; its mutation `revision` and `flow_revision`
are separate counters. There is no whole-input revision API in this leaf.

`load_frozen_inputs(run_dir, ledger)` validates current policy compatibility,
the frozen policy digest, input-file digest and selected task identity, and
returns the snapshot. `_load_flow_authority` additionally validates immutable
flow history, its current digest and cursor. Source edits cannot replace frozen
brief, verification, scope, checks or policy. A launched implementation prompt
includes the frozen document content; repository drift checks can still refuse
a launch after source edits.

## Policy and sequence

`execution_authorization` must equal:

```json
{"transport":"sbx","yolo":true,"intervention":"active_chat"}
```

This records approval. It does not configure adapter launch flags. The initial
`flow` is required explicitly; no default profile is inserted. Profile names
are labels. Every profile must contain exactly these eight ordered stages:

| Kind | Role | Allowed modes |
|---|---|---|
| `ready` | `controller` | `off` |
| `preflight` | `preflight` | `light`, `standard`, `strong` |
| `implement` | `implementer` | `light`, `standard`, `strong` |
| `verify` | `verifier` | `targeted`, `targeted_plus_repository_gate` |
| `semantic_review` | `review_collector` | `standard`, `strong` |
| `acceptance` | `acceptance_reviewer` | `standard`, `strong` |
| `accept` | `controller` | `off` |
| `completed` | `controller` | `off` |

`off` is the representation for controller-owned stages; it does not remove
them. Collection and acceptance are different roles. Runtime validation and
schemas reject omissions, role merging, reordered stages and optional checks.
The actor mapping is exactly `gpt-6.1-sol`: `light` = `low`, `standard` =
`medium`, `strong` = `high` reasoning.

Correction policy must equal
`{"enabled":true,"limit":3,"includes_environment_repair":true}`.
The pure cursor accepts `begin_correction` from checks, collection or acceptance
with `findings`, `CHANGES_REQUESTED` or `environment_repair`. All causes share
`correction_cycle`; a fourth correction returns the configured
`corrections_exhausted` stop/escalate action without advancing the cycle.
`complete_correction` returns to `verify`. This represents policy; durable
reservation and evidence admission remain successor work.

`correction_session_policy(occupancy=..., reliable=...)` returns `reuse` only
for reliable, finite numeric occupancy in `[0, 0.5)`. At or above `0.5`, unknown,
unreliable, invalid or totals-only information returns `fresh`. Terminal token
totals are not occupancy and are not a separate input to this API.

Handoff and actor-result envelopes remain format version `1`, with subjects
bound to run/task, flow revision/digest, step, correction cycle and actor role.
Actor results require `evidence_status: "reported"` and these result families:

| Step | Results |
|---|---|
| `preflight` | `ready`, `blocked`, `needs_input` |
| `implement`, `correction` | `complete`, `needs_input`, `failed` |
| `verify` | `mechanically_eligible`, `findings` |
| `semantic_review` | `collected`, `findings`, `INCONCLUSIVE` |
| `acceptance` | `ACCEPT`, `CHANGES_REQUESTED`, `INCONCLUSIVE` |

Controller-owned stages have no valid actor result. Collection cannot submit
`ACCEPT`. These validators do not admit evidence, advance a live task or grant
completion. Pure `advance` also cannot advance from `accept` or `completed`;
a controller completion operation is not implemented in this leaf.

## Supported operations and limits

The CLI still provides `init`, `run-next`, `inspect`, and `revise-flow`.

- `run-next` selects `ready`, persists a pending cursor and launches no worker.
  There is no new adapter or CLI to admit `ready` or `preflight`.
- The historical implementation transport path remains available when the
  persisted cursor already names `implement`. Its tests use an explicit
  transport-boundary fixture. That fixture proves no readiness admission.
- `inspect` retains mechanical verification and durable replay checks. Successful
  mechanical inspection stops at pending `semantic_review`; it cannot replace
  collection or acceptance and cannot grant task acceptance.
- `revise-flow` retains immutable flow-only revisions at the exact safe boundary:
  ready run, no selected task, active attempt, active operation or cursor, and
  correction cycle zero. It does not revise frozen documents or run policy and
  is not the T-002.3 whole-input revision operation.
- Public `update_ledger` checks frozen authority before mutation and under its
  command lock. It is a library operation, not a new CLI command.

Incompatible policy versions, model mappings, required-stage profiles or runs
without a frozen-input reference are refused before continuation. Incompatible
persisted flow history is also refused. The response includes:
`Initialize a new run using reviewed current inputs.` No old policy, flow,
input, history or state bytes are migrated. Ordinary input loading writes no
records. Inspection still requires an applicable inspection state.

Reservation/replay ownership, whole-input revision, live preflight/collection/
acceptance admission, completion, intervention handling and applying sbx/YOLO
launch policy remain outside this leaf. No live model, network, sbx pilot or
installation refresh is qualified here. See [implementation report](implementation-report.md)
for local evidence and the remaining independent review route.
