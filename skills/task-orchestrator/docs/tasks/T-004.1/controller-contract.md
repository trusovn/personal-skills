# T-004.1 candidate/check producer contract

Status: implementation submission; independent review pending.

Consume the accepted [T-003 lifecycle](../T-003/controller-contract.md). This
producer adds inspection and verification to that lifecycle. Collection,
acceptance and completion remain unavailable.

## Public calls and CLI

| Library operation | CLI | Inputs / result |
|---|---|---|
| `inspect_candidate(run_dir, operation_id)` | `controller.py inspect-candidate --run-dir RUN --operation-id OPERATION` | An admitted terminal implementation/correction operation. Returns `passed`, candidate SHA-256 and run-relative record path; scope/owner violation returns `blocked`; invalid authority or active operation returns `refused`. |
| `check_candidate(run_dir, assignment, timeout_seconds=N)` | `controller.py check-candidate --run-dir RUN --request ASSIGNMENT_JSON --timeout-seconds N` | Exact assignment from the existing `reserve` operation with stage `verify`, role `verifier`. Returns durable check result, or `refused`, `stale`, or an uncertainty/infrastructure `blocked` result. |

Use `status_run` to obtain the current task, stage, state version and next actions.
After inspection, reserve the verifier through the existing public operation:

```text
reserve_operation(RUN, expected_version=STATUS['state_version'], task_id=TASK,
                  stage='verify', role='verifier', operation_key='first-check')
check_candidate(RUN, RESERVATION['assignment'], timeout_seconds=30)
```

The request file contains the assignment object itself. CLI exit 0 means the
operation returned a recorded passed/failed/stale observation; callers must
inspect its status. Refusal/blocked CLI results exit 1. A failed check authorizes
only the inherited bounded `check_failed` correction route. Evidence production
adds no correction charge. A fresh correction reservation owns its charge.

## Candidate record and eligibility

`candidates/<sha256>.json` is an exclusively published canonical JSON object:

- `operation_id` and complete terminal producer `assignment` bind run/task,
  input/policy/flow identities and correction count;
- `baseline_sha256` binds the initial owner-work baseline, including its index tree;
- `workspace` contains HEAD, index tree, visible Git status and per-file identities.

The candidate SHA-256 hashes canonical JSON without a trailing newline; the
serialized record has the controller's canonical trailing newline. The workspace
hashes every tracked file, visible untracked file and explicitly allowed path,
including an ignored allowed input. It records missing files, executable bits,
symlink spelling and file referent bytes. Relevant evaluated ignored inputs must
be explicit allowed paths; this interface does not discover arbitrary reads by
a command. Other ignored generated output retains Git's existing exclusion.

Inspection verifies the actual terminal outcome and complete assignment. Actor
summaries and claimed digests are not candidate authority. It rejects changed
pre-existing dirty files (even within scope), new changes outside the allowed
path list and changed HEAD. It compares staged paths against the initial index
tree, so identical status text and worktree bytes cannot conceal a staging change.
Runs without the initial index identity require a newly reviewed run. No
inspection restores or overwrites task files.
Historical candidates remain on disk. Only the latest terminal producer can
become current. Reinspection of unchanged bytes reuses the candidate record.

Check admission compares the complete current workspace with the inspected
workspace and verifies frozen authority. It compares again after execution. Drift
can never produce a current pass, including a zero-exit check with side effects.
`status` calculates stale eligibility without rewriting historical check records.
Source documents are workspace inputs when visible to Git; approved task content
continues to come from the frozen input bundle, never from source replacements.

## Check identity, mechanism and evidence

Each check uses the same operation ledger and command lock as actors. No separate
runner or correction counter exists. Before execution it publishes
`checks/operation-NNN.intent.json`, then persists the operation as `unknown`.
Another actor/check/inspection cannot overlap its command lock or active owner.

The existing verification planner parses all commands before launch, rejects
prohibited syntax and enforces dependency-install planning rules. Required checks
are never excused by a known-issue gap. In targeted-only flow, a repository-only
gate is explicitly listed in `policy_omissions`; required task checks remain.

The existing runner now accepts an optional `execution_authorization` parameter.
Only the exact frozen `{"transport":"sbx","yolo":true,"intervention":"active_chat"}`
object selects direct shell-free argv and records `execution_mechanism: sbx_yolo`.
This selection claims no filesystem or network enforcement. An absent object
retains the exact legacy macOS sandbox-exec path. Invalid objects fail; neither
platform detection nor sandbox-launch failure selects unrestricted execution.
Existing permission-envelope validation and executable preflight remain active.

Execution uses the existing artifact convention:

```text
verification/operation-NNN.turn-001.execution.json
verification/operation-NNN.turn-001.command-MMM.stdout.log
verification/operation-NNN.turn-001.command-MMM.stderr.log
checks/operation-NNN.json
```

The existing execution-record validator owns command order, exits, binary log
paths/hashes and closure identity; its optional mechanism field accepts only
`sbx_yolo`. The legacy closure subject's `attempt_id` carries the verifier
operation ID, `turn` is 1, `prompt_sha256` carries frozen inputs SHA-256, and
`stage2_git_evidence_sha256` carries the candidate SHA-256. These are compatibility
field names, not a second legacy attempt admission.

The check receipt contains exact assignment, timeout, setup/frozen inputs,
environment cwd/platform, execution path/hash, post-workspace, explicit policy
omissions, mechanism limits and status. A failure stops later commands; their
absence from outcomes means not-run. Required-executable/planning/infrastructure
errors are blocked, not product success. Partial logs and intent are retained.
An unresolved runner failure leaves the operation unknown and requires explicit
inspection/intervention; no automatic installation, repair or relaunch exists.

## Replay, interruption and collector reruns

Repeating the exact assignment and timeout after completion returns the original
receipt without changing the ledger revision, correction count or execution.
Reload checks execution-record and log hashes before accepting replay. Different
configuration refuses. Historical or drifted candidates cannot restore current
eligibility. An unknown operation without a complete check receipt remains
stopped. Partial evidence/collisions cannot be overwritten into a success.

A complete check receipt published before ledger completion can be reconciled
under the same lock by replaying that assignment. A completed execution record
without a check receipt remains uncertain; the controller does not rerun it.
This is process-interruption handling, not power-loss recovery or tamper resistance.

A future collector requests its own fresh rerun by reserving a new `verify`
operation with a distinct operation key and current state version, then calling
this same runner. It receives a new operation identity and new logs; replay of
an old completed operation is never a fresh independent rerun. Collection
admission and its final stage transitions remain T-004.2 work.

## Local evidence and limits

See [implementation-report.md](implementation-report.md) for exact commands,
results and coverage gaps. The producer tests execute local actor fixtures and
real subprocess/file checks. They do not qualify real sbx, Codex, provider/model
identity or outer containment. T-006 retains that work. Registry synchronization
belongs to the designated stage after maintainability review; this submission
does not register future collection or acceptance as implemented.
