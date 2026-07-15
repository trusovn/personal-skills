# Task Orchestrator: Controller Contract

Status: Stage 1 executable contract
Date: 2026-07-15

## Authority

Authority is resolved in this order:

1. system and repository instructions;
2. the persisted run policy;
3. the authoritative task ledger and selected task brief;
4. the controller-rendered worker prompt;
5. the worker result and recommendations.

A lower source cannot grant authority denied or omitted by a higher source. In
particular, prompts and worker results cannot authorize commits, permission
expansion, ledger changes, or selection of another task. A contradiction fails
closed and requires the controller to stop or escalate according to the run
policy.

## Ownership boundaries

The controller owns policy validation, task and attempt state, prompt rendering,
worker lifecycle, independent Git inspection, closure decisions, ledger changes,
and any explicitly authorized exact-path commit.

The worker may read and edit the selected task's allowed workspace paths and run
authorized checks. It must not commit, update the orchestration ledger, select a
task, change controller or installed-skill code, or broaden its permissions. Its
structured result contains claims for inspection, not acceptance evidence.

An optional supervisor may interpret a closure packet or phrase a resume prompt.
It cannot mutate controller state directly or choose a transition the controller
did not return as allowed.

## Persisted run policy

`../assets/run-policy.schema.json` defines the version 1 record. It is written
before a run starts and thereafter treated as immutable. The controller records
its SHA-256 digest in every attempt so replacement of the policy is detectable.

The policy explicitly identifies the repository, authorized task IDs, required
verification, permission envelope, commit mode, and stop behavior. Omission is
denial. `danger-full-access` is valid only when the same persisted permission
record explicitly authorizes that exact mode. The dangerous bypass flag is not a
supported transport fallback.

## State model

Task lifecycle states are separate from process exit and worker status:

```text
initialized -> ready -> running -> awaiting_inspection -> accepted
                              |              |
                              |              +-> resumable -> running
                              |              +-> stopped
                              +-> resumable -> running
                              +-> stopped
```

An attempt records one terminal reason: `complete`, `needs_input`, `blocked`,
`failed`, `timed_out`, `interrupted`, `missing_result`, or `failed_to_start`.
`complete` moves a task only to `awaiting_inspection`; it never means accepted.
The other outcomes move the task to `resumable` or `stopped` only after the
recorded process is proven absent. A live or ambiguously owned process rejects a
resume without changing state.

Allowed task transitions are:

| From | To |
|---|---|
| `initialized` | `ready`, `stopped` |
| `ready` | `running`, `stopped` |
| `running` | `awaiting_inspection`, `resumable`, `stopped` |
| `awaiting_inspection` | `accepted`, `resumable`, `stopped` |
| `resumable` | `running`, `stopped` |
| `accepted` | none |
| `stopped` | none |

Any unlisted transition is rejected. Acceptance requires a closure decision that
explicitly includes `accepted` in its allowed next states.

## Durable records

Every started attempt has an immutable directory and includes:

- task ID and authoritative brief path;
- attempt and turn number;
- prompt path and SHA-256 digest;
- thread ID and process identity when available;
- start and end timestamps plus terminal reason;
- effective transport, model, sandbox, approval policy, network policy, and
  writable roots;
- run-policy digest and pre-task Git baseline reference;
- prompt, events, stderr, structured-result, and terminal-state paths.

Creating a retry or resume allocates a new attempt/turn. Existing artifacts are
opened exclusively and never truncated, replaced, or deleted. A process failure
before a thread ID exists is still a terminal attempt and remains auditable.

## Transport contract

The transport exposes preflight, start, wait, cancel, resume, and result
collection without owning task policy or acceptance. Preflight proves the exact
safe command shape before creating a run directory. Unsupported safe options
stop; they never select a broader permission mode.

A timeout triggers bounded process-group termination and reaping, followed by a
durable `timed_out` terminal state with no active process PID. Resume rejects a
live PID and a PID whose ownership/liveness cannot be determined.

## Closure gate

Closure inspection receives the persisted policy, selected task identity,
pre-task Git baseline, current independent Git status, worker result, and
verification evidence. Acceptance requires all of these:

- result status is `complete` and its task ID matches;
- every targeted check required by policy passed;
- the repository gate passed, or the policy explicitly records an authorized
  gap;
- changed and untracked paths are within the task allowance;
- pre-existing dirty paths remain present and are not silently absorbed;
- no blocking question or unexplained risk remains;
- requested tracker and commit actions are valid under the persisted policy.

The output is a closure decision containing `accepted`, reasons, independently
observed changed paths, and allowed next task states. A denial never changes Git,
the index, history, or the ledger. With commit mode `off`, no commit transition is
available. With `controller_exact_paths`, committing remains a separate
controller action limited to accepted paths; workers are prohibited from
committing in either mode.

