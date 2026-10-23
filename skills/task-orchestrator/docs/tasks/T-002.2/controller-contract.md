# T-002.2 controller status and reservation contract

Implemented and submitted for independent review. This note extends
[T-002.1](../T-002.1/controller-contract.md); it does not claim acceptance or
production actor/readiness admission.

## Public requests

Run from the repository root. The run directory remains outside the evaluated
repository. Python callers import `scripts/controller.py` from the skill.

```sh
python3 skills/task-orchestrator/scripts/controller.py status --run-dir /tmp/run
python3 skills/task-orchestrator/scripts/controller.py reserve --run-dir /tmp/run --expected-version 1 --task-id T1 --stage preflight --role preflight --operation-key preflight-1 --reason initial
```

Equivalent library requests:

```python
status_run(run_dir)
reserve_operation(run_dir, expected_version=1, task_id="T1", stage="preflight",
                  role="preflight", operation_key="preflight-1", reason="initial")
```

`run_dir` is a `Path`. Status reads one ledger snapshot, validates frozen
policy/input/flow and manifest authority, and never selects a task, writes a
lock, advances a stage, increments a version or consumes a correction.
Reservations hold the existing nonblocking `RunCommandLock` throughout
validation and publication. The embedded assignment and its charge are
published in one atomic `ledger.json` replacement. There is no separately
published assignment file or receipt-dependent commit point.

A new reservation returns:

```json
{"status":"reserved","state_version":2,"assignment":{"run_id":"run-1","task_id":"T1","operation_id":"operation-001","operation_key":"preflight-1","stage":"preflight","role":"preflight","reason":"initial","inputs_sha256":"<input digest>","policy_sha256":"<policy digest>","flow_sha256":"<flow digest>","flow_revision":1,"candidate_sha256":null,"correction_count":0,"can_repair":false,"can_change_files":false,"actor":{"model":"gpt-6.1-sol","reasoning":"low"},"session_policy":null}}
```

The actor profile above is the supplied `fast-local` preflight example; the
actual assignment resolves the stage mode through the frozen flow. `verify`
has `actor: null` and is controller-executed check work. Corrections use the
implementation profile and `session_policy: "fresh"`; this conservative leaf
does not implement session reuse.

## Status and refusal results

Status returns `status: "ok"`, `run_id`, `task_id`, `inputs_sha256`,
`policy_sha256`, `flow_revision`, `flow_sha256`, `state`, `state_version`,
`stage`, `attempts`, `correction_count`, `candidate_sha256`, `references`,
`evidence`, `policy_omissions`, `required_evidence`, `outstanding_findings`,
`operation`, `operation_history`, `readiness_current`, `next_actions` and
`blocker`. An unselected initial cursor is displayed as `ready`, with
`reserve:preflight` permitted; reading it does not select the task.

- `references` contains the legacy closure, verification, decision and active
  operation references, each nullable.
- `evidence` has preflight/implementation/check/collection/acceptance entries
  under `preflight`, `implement`, `verify`, `semantic_review`, `acceptance`.
  An absent entry is `missing`. Passed, failed, stale, blocked and not-run
  remain distinct (`not_run` is the exact stored spelling). Input or candidate
  mismatch displays `stale`. A required-role `omitted_by_policy` displays
  `blocked`. References and historical fields remain visible.
- All five evidence stages remain required. `policy_omissions` lists only
  `repository_gate` when the verification mode is `targeted`; it never removes
  a required role. These are policy facts, not successful execution claims.
- `operation` is the possibly active actor record or null. History retains
  terminal records and original assignments. An active reservation reports
  `observe_operation` and `intervene`; it never infers terminality from an
  absent process or receipt. Legacy finalization references remain in
  `references`, with successor admission blocked by run state.

A refusal returns `status: "refused"`, `reason`, `next_actions` and
`state_version`. Known valid state supplies the current version/actions;
authority or lock failure supplies null version, `intervene` and a `detail`.
Reasons include `invalid_request`, `stale_version`, `task_or_role_mismatch`,
`operation_key_conflict`, `stage_mismatch`, `reason_not_authorized`,
`operation_reserved/running/unknown`, `current_preflight_readiness_required`,
`corrections_exhausted`, `successor_admission_pending`,
`correction_authorization_pending`, `successor_evidence_required`,
`successor_completion_pending`, `initial_implementation_already_reserved` and
`authority_or_lock_unavailable`. A refusal preserves ledger/version, authority,
count and task files. Creating the diagnostic `controller.lock` file is allowed;
it contains no authority. CLI reserve exits 0 for reservation/replay and 1 for
refusal. Other CLI exceptions emit a structured refusal on stderr and exit 2;
ordinary reserve results are on stdout.

Replay requires the same key and the exact original request, including its
original expected version. It returns `status: "replayed"`, the original
`assignment`, and the current `state_version`, without writing anything. Replay
is resolved before the stale-version check, after frozen-authority validation.
Reusing the key with a changed request is a conflict. Competing new keys against
one expected version yield one winner; a loser gets lock-unavailable or stale
version. Replay is an assignment lookup, never launch permission for a second
actor; T-003 must enforce launch identity and terminal-result handling.

## Persisted fields and successor seams

Ledger format remains version 1. Initialization adds `actor_operations: []`,
`readiness: null`, `correction_request: null`, `candidate_sha256: null`,
`evidence: {}` and `outstanding_findings: []`. Compatible T-002.1 ledgers without
these fields read as absent/default state; there is no automatic file rewrite.

Each `actor_operations` item has `operation_id`, `state`, `request`, and
`assignment`. IDs are sequential `operation-NNN`. Request fields are
`expected_version`, `task_id`, `stage`, `role`, `operation_key`, `reason`.
The assignment fields are shown above. States are `reserved`, `running`,
`unknown`, `terminal`. Only the latest record may be active, and its assignment
must match current authority. A live record is referenced by
`active_operation_path: "actor_operations/operation-NNN"`; this is an embedded
ledger reference, not a filesystem path. The pre-existing finalization path
meaning remains unchanged for legacy mechanical records.

T-003 must extend the controller's locked admission boundary to validate observed
identity and terminality, retain history, mark an operation terminal and clear
its active pointer atomically. No public outcome/state injection API is added
here. Tests label direct fixture writes as successor setup.

T-003 readiness is an admitted object with `status: "ready"`, `task_id`,
`operation_id`, `inputs_sha256`, `policy_sha256`, `flow_sha256`. The referenced
operation must be terminal preflight work for this task/current authority.
A missing, failed, stale, nonterminal, wrong-role or wrong-operation object
cannot permit implementation. A later environment-repair assignment invalidates
that readiness. Reserving preflight also clears it until new admission.
Ordinary implementation/correction does not erase the initial readiness.

T-003/004/005 admission owns stage progression and the appropriate `ready` or
`resumable` run state. This leaf never derives progression from actor claims.
A permitted reservation sets the selected task, current stage, active pointer,
revision and assignment together. Stage/role pairs are:

| Stage | Role | Required reservation prerequisites |
|---|---|---|
| preflight | preflight | Initial ready/preflight cursor, or fresh readiness required |
| implement | implementer | Implementation cursor, current admitted readiness, no initial implementation already reserved for current inputs |
| correction | implementer | Admitted matching correction reason and available shared allowance; ordinary corrections also require readiness |
| verify | verifier | Verify cursor, current candidate and passed implementation evidence |
| semantic_review | review_collector | Collection cursor, current candidate and passed check evidence |
| acceptance | acceptance_reviewer | Acceptance cursor, current candidate and passed collection evidence |

Later evidence entries carry `status`, `inputs_sha256`, `candidate_sha256`, and
optional `reference`/historical fields. Their actual production admission and
semantic validation belong to T-004/005, not this reservation eligibility check.
Missing prerequisites expose intervention/successor work rather than success.
There is no reserve action for completion or acceptance publication.

`correction_request` is an admitted reason: `check_failed`, `review_findings`,
or `environment_repair`. It is consumed by reservation, not supplied as new
authority by the request. T-003/004/005 own admission of that reason. A repair may
be needed before initial implementation and does not require prior readiness.

## Shared correction accounting and legacy guards

The first initial implementation adds no correction charge. Each newly reserved
correction adds exactly one, up to three, regardless of reason. Counts equal the
number of correction assignments in history. Replay, preflight and evidence-only
retry add none. No automatic refund exists for an uncertain/failed launch.
`can_change_files` is true only for implementation/correction; `can_repair` is
true only for an authorized environment-repair correction. Free retries cannot
request that reason. A repair requires preflight again. Positive counts are
valid at preflight/implementation cursors, so initial implementation never resets
a repair charge. A pending fourth correction returns `corrections_exhausted`
and requires intervention without writing state.

Public `run-next` now reports pending successor launch work, including permitted
actions, without launching or selecting. The former private mechanics are named
`_legacy_run_next` only for existing transport/Git regression coverage; no CLI
route calls them. `inspect_run` refuses active actor ownership and reports
successor inspection pending for terminal actor history. Historical mechanical
inspection remains non-accepting under T-002.1 policy. `revise-flow` retains its
safe-boundary guard and cannot bypass selected/active work or retained charges.
The generic legacy ledger updater rejects actor-admission fields and reservation
cursor changes and cannot mutate during active ownership, including under its
mutation lock. T-002.3 owns safe input revision and must retain this history and
count; this leaf adds no input-revision or completion command.
