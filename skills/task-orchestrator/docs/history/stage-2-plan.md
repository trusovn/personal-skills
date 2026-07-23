# Task Orchestrator: Stage 2 Implementation Plan

Status: ready for a fresh implementation session
Date: 2026-07-16
Parent direction: [direction.md](direction.md)
Stage 1 evidence: [stage-1-handoff.md](stage-1-handoff.md)

## Objective

Implement the smallest controller path that can initialize one immutable run,
select one dependency-ready task deterministically, launch exactly one worker
through the proven CLI transport, persist controller-owned state, and emit an
independent closure packet.

Stage 2 ends at `awaiting_inspection`. It must not accept a task, resume a
worker, update a human tracker, commit, or select a second task. Those behaviors
remain Stage 3.

## Design judgment

The main value of Stage 2 is moving task choice, prompt provenance, and evidence
collection out of supervisor memory. The main failure mode is building queue
plumbing that appears deterministic while still accepting worker self-report as
proof. Therefore Stage 2 begins with a short Stage 1 closure slice and keeps
worker claims separate from controller-observed evidence throughout the ledger
and closure packet.

Use Python's standard library and the existing unittest style. Keep the
controller sequential and single-worktree. Do not introduce an SDK, JSON Schema
runtime dependency, plugin packaging, parallel worktrees, arbitrary Markdown
normalization, or a general workflow engine.

## Stage 1 review verdict

Verdict: `CHANGES REQUESTED` before relying on Stage 1 as a safety gate. The 21
local tests pass, but they do not cover several contracts claimed by the Stage 1
handoff.

### [P1] Worker claims can satisfy the verification gate

- Location: `../scripts/controller.py:198`
- Impact: a worker can report every required command as passed and receive an
  accepting closure decision without independent verification evidence.
- Evidence: `decide_closure()` builds its verification map exclusively from
  `result["verification"]`; a focused diagnostic returned
  `worker_claim_only_accepted=True` with no controller evidence.
- Required correction: pass controller-owned verification evidence separately.
  Missing evidence must deny acceptance. Keep worker verification only under a
  clearly named claims field.

### [P1] The runtime policy validator does not enforce the policy schema

- Location: `../scripts/controller.py:46`
- Impact: policy objects missing required nested fields or containing invalid
  nested types can be persisted as "validated" authority. Later code can crash
  or, after transport integration, interpret a truthy non-boolean authorization
  as permission.
- Evidence: the validator checks only selected top-level fields and a few enum
  values; it does not enforce required verification, permission, or stop-policy
  fields from `../assets/run-policy.schema.json`.
- Required correction: implement strict standard-library validation equivalent
  to the schema for every field Stage 2 consumes. Reject unknown keys, wrong
  types, duplicates, empty strings, and contradictory permission values before
  writing a run directory.

### [P1] Supervisor interruption can leave the worker alive

- Location: `../scripts/codex_worker.py:190`
- Impact: `SIGINT`, `SIGTERM`, or an exception outside the timeout branch can
  exit the wrapper while its new-session worker continues and `state.json`
  remains `running`, recreating the overlapping-resume hazard Stage 1 was meant
  to remove.
- Evidence: process-group termination occurs only in the
  `subprocess.TimeoutExpired` branch; `main()` does not handle interruption and
  no `finally` path owns the child.
- Required correction: make every wrapper exit path terminate/reap an owned
  process and write a terminal attempt record. Add a real local subprocess test
  for interruption, not only timeout.

### [P2] Resume does not enforce the state machine

- Location: `../scripts/codex_worker.py:319`
- Impact: any record with a thread ID and no live recorded PID can be resumed,
  including `stopped` or `awaiting_inspection`, although those transitions are
  invalid or require a controller decision first.
- Required correction: reject resume unless the durable state is explicitly
  `resumable`, the prior process is proven absent, and the controller authorizes
  the transition. Stage 2 does not call resume, but the gap must remain visible
  for Stage 3.

### [P2] Malformed structured results can reach inspection

- Location: `../scripts/codex_worker.py:53`
- Impact: a result with the expected top-level keys but invalid nested values can
  be labeled `complete`; closure processing may then crash instead of producing
  `missing_result` and failing closed.
- Evidence: a focused diagnostic with integer `summary`, string question
  entries, and null `next_action` returned `malformed_schema_status=complete`.
- Required correction: validate the complete result contract before mapping its
  status. Keep the implementation dependency-free and cover every schema field
  with representative invalid cases.

### [P2] Acceptance trusts only a boolean in the closure object

- Location: `../scripts/controller.py:90`
- Impact: `transition_task()` accepts a closure object whose `accepted` boolean
  is true even when `accepted` is absent from its allowed transitions or the
  decision does not identify the selected task and evidence.
- Evidence: a focused diagnostic accepted
  `{"accepted": true, "allowed_transitions": []}`.
- Required correction: bind a closure decision to run ID, task ID, attempt ID,
  and evidence digest, and require `accepted` in its allowed transitions. The
  full acceptance action remains Stage 3.

## Scope and non-goals

Stage 2 includes:

1. Closing the P1 findings above and adding fail-closed tests for the P2 result
   validation issue.
2. A normalized task-manifest schema and strict validator.
3. Atomic run initialization from an existing run-policy JSON file and an
   existing manifest JSON file.
4. A controller-owned ledger with digests, task states, one selected task, and
   one active attempt at most.
5. Deterministic dependency-ready selection.
6. Prompt construction exclusively from persisted policy, persisted manifest,
   the selected task, and the recorded baseline.
7. One new-worker dispatch through the existing CLI adapter.
8. Independent Git evidence and a durable closure packet.

Stage 2 does not include:

- arbitrary Markdown-to-manifest conversion or implicit task confirmation;
- resuming or retrying a worker;
- acceptance, semantic diff judgment, tracker changes, or commits;
- selection or launch of a second task;
- live Codex/model calls, network use, or dependency installation;
- changes to `SKILL.md` or skill evaluations;
- SDK/MCP transport work, supervisor tool restriction, or parallel worktrees.

## Input contracts

### Run policy

Continue using `../assets/run-policy.schema.json` version 1 for Stage 2. Make the
runtime validator match it exactly before adding initializer behavior. Do not
silently change the meaning of version 1. If implementation proves that a new
required authority field is unavoidable, stop and propose version 2 rather than
weakening validation or adding an undocumented default.

The persisted policy remains the authority for repository, authorized task IDs,
verification requirements, permission envelope, commit mode, and stop behavior.
Operational dispatch inputs such as model, effort, and timeout may be explicit
CLI inputs in Stage 2, but must be copied into the immutable attempt record and
must not override policy-controlled sandbox, approvals, network, writable roots,
or dependency-install settings.

### Task manifest

Add `../assets/task-manifest.schema.json` with this minimal version 1 shape:

```json
{
  "version": 1,
  "manifest_id": "feature-or-plan-id",
  "completed_task_ids": ["T0"],
  "tasks": [
    {
      "id": "T1",
      "title": "Bounded task title",
      "brief_path": "docs/tasks/T1.md",
      "dependencies": ["T0"],
      "allowed_paths": ["src/example.py", "tests/test_example.py"],
      "required_checks": ["python3 -m unittest tests.test_example"]
    }
  ]
}
```

Validation rules:

- reject unknown fields and wrong JSON types;
- require non-empty unique task IDs, titles, brief paths, allowed paths, and
  required checks where present;
- require every dependency and completed task ID to exist in `tasks`;
- reject self-dependencies and dependency cycles;
- require every `policy.task_ids` entry to exist and not already be completed;
- reject an authorized task that depends on an incomplete task outside the
  authorized run, because the immutable run could never make it ready;
- preserve `policy.task_ids` order as the deterministic selection order;
- treat `allowed_paths` as exact repository-relative file paths in version 1;
  reject absolute paths, `..`, empty segments, directory-only entries, and paths
  resolving outside the repository;
- require each brief to be an existing regular file inside the repository;
- do not infer tasks, paths, dependencies, or completion from Markdown.

Exact file paths are intentionally narrower than glob or prefix support. If a
real manifest cannot enumerate expected files, stop and treat broader path-scope
semantics as an explicit product decision rather than inventing glob behavior.

## Durable run layout

Use one run directory outside the repository worktree for Stage 2. Reject an
in-repository run directory rather than adding ignore-file behavior during this
stage.

```text
<run-dir>/
  run-policy.json
  task-manifest.json
  ledger.json
  baselines/
    run-initial.json
    task-001.json
  attempts/
    attempt-001/
      record.json
      prompt.txt
      state.json
      turn-001.events.jsonl
      turn-001.stderr.log
      turn-001.result.json
      turn-001.result.state.json
  closure/
    attempt-001.json
    attempt-001.name-status.txt
    attempt-001.stat.txt
    attempt-001.diff.patch
```

Persist canonical policy and manifest copies with SHA-256 digests in the ledger.
Record source paths for provenance, but never re-read them as authority after
initialization. On every later command, recompute the persisted-copy digests and
fail closed on mismatch.

Write initialization into a sibling temporary directory and atomically rename it
to the final run directory only after policy validation, manifest validation,
repository checks, and baseline capture all succeed. Never replace an existing
run directory.

## Ledger contract

Add `../assets/run-ledger.schema.json` only if it is used by tests and runtime
validation; do not create a decorative schema. The minimum ledger fields are:

- version, run ID, repository canonical path, created/updated timestamps, and a
  monotonic revision;
- persisted policy and manifest paths plus SHA-256 digests;
- initial baseline path and digest;
- run state: `initialized`, `ready`, `running`, `awaiting_inspection`, or
  `stopped`;
- one entry for every authorized task with task state, dependency IDs, and
  attempt IDs;
- selected task ID or null;
- active attempt ID or null;
- last closure packet path or null.

Maintain these invariants in one validator used before and after every ledger
write:

- no more than one selected task or active attempt exists;
- `running` requires both selected task and active attempt;
- `initialized` has neither;
- `awaiting_inspection` has a selected task, no live active process, and a
  closure packet;
- a task cannot become `accepted` in Stage 2;
- persisted task IDs exactly equal the policy-authorized task IDs;
- attempt IDs are append-only and existing attempt directories are immutable;
- ledger writes are atomic and only the controller performs them.

## Deterministic controller flow

### 0. Close the Stage 1 blockers

Write focused failing tests first for strict policy validation, independent
verification evidence, full worker-result validation, and interrupted-process
cleanup. Make only the production changes required for those tests. Also tighten
closure-transition binding while touching that boundary.

Resume state enforcement may be implemented now if the change is small and
isolated; otherwise record it as the first Stage 3 prerequisite. Do not build the
Stage 3 recovery loop in this stage.

### 1. Initialize the run

Add an `init` entry point to `scripts/controller.py`:

```text
python3 skills/task-orchestrator/scripts/controller.py init \
  --run-dir <outside-repository-path> \
  --policy <run-policy.json> \
  --manifest <task-manifest.json>
```

The command must:

1. load both inputs as JSON objects and validate them strictly;
2. resolve the policy repository to the actual Git top level and reject a
   mismatch;
3. validate all manifest paths and graph constraints;
4. capture the initial HEAD OID, index/worktree status with content hashes, and
   untracked paths without modifying the repository;
5. copy canonical policy and manifest records into a temporary run directory;
6. create an `initialized` ledger containing their digests and task entries;
7. atomically publish the run directory;
8. print a small JSON summary with run ID, state, ledger path, and baseline path.

Require an existing HEAD in Stage 2. An unborn repository is a stop condition,
not a reason to invent alternate baseline semantics.

### 2. Select and prepare one task

Implement selection as a pure function. A dependency is satisfied when it is in
the manifest's immutable `completed_task_ids` or the controller ledger marks it
accepted in a later stage. Among ready authorized tasks, select the first ID in
`policy.task_ids` order. Return structured blocking reasons when none is ready.

Before changing the ledger:

- verify persisted policy/manifest digests;
- verify no selected task or active attempt exists;
- compare the current Git status and HEAD with the initial baseline; reject any
  intervening change, including a change to a pre-existing dirty file;
- capture `baselines/task-001.json` and its digest;
- hash the selected brief and record that hash in the attempt.

Render the prompt without accepting free-form supervisor instructions. Include
only:

- run ID, selected task ID/title, and authoritative brief path/hash;
- dependency IDs already satisfied;
- exact allowed paths and required checks;
- pre-existing dirty paths to preserve;
- effective permission summary and explicit worker prohibitions;
- worker-result schema path and the statement that the result is an untrusted
  claim pending independent inspection.

Assert that neighboring task titles, briefs, paths, and future instructions do
not appear in the prompt.

### 3. Preflight and launch through the transport

Add a `run-next` entry point, but permit only one invocation in Stage 2:

```text
python3 skills/task-orchestrator/scripts/controller.py run-next \
  --run-dir <run-dir> \
  --timeout-seconds <positive-number> \
  [--model <model>] [--effort <level>]
```

Use the existing adapter rather than duplicating Codex command rendering. Expose
or call its preflight before allocating the attempt. A failed preflight must not
select a task, create an attempt directory, or mutate the ledger.

After preflight:

1. allocate `attempt-001` exclusively and persist its static record and prompt;
2. transition the selected task and run from `ready` to `running` in one atomic
   ledger update;
3. invoke `codex_worker.py start` with the attempt directory and durable prompt;
4. persist the exact adapter invocation, model, effort, timeout, effective
   permission envelope, policy/manifest/baseline digests, and brief hash;
5. read only the adapter terminal state and structured result on normal
   completion; raw events/stderr remain diagnostic artifacts;
6. never call resume or launch another task.

Local tests must use a strict fake Codex executable. No implementation or
verification step may call the real model.

### 4. Produce independent closure evidence

After the worker process is terminal, collect evidence directly from Git:

- HEAD OID before and after the attempt;
- porcelain status and untracked paths;
- staged and unstaged name/status summaries;
- staged and unstaged diff statistics;
- a task-scoped patch artifact;
- allowed, unexpected, disappeared pre-existing, and modified pre-existing
  paths;
- whether the index or HEAD changed despite the worker commit prohibition.

Write `closure/attempt-001.json` with:

- run/task/attempt identity and policy, manifest, prompt, baseline, and evidence
  digests;
- adapter exit, terminal state, thread ID, and artifact paths;
- worker result under `worker_claims`, including claimed verification;
- Git data under `controller_observations`;
- `controller_verification` explicitly set to `not_collected` in Stage 2;
- mechanical violations and missing-evidence reasons;
- allowed next actions limited to inspection or stop. Do not include acceptance,
  tracker, commit, resume, or next-task actions.

Then atomically set the ledger to `awaiting_inspection`, clear the active attempt,
and reference the closure packet. If the worker never starts or lacks a valid
terminal result, record the terminal attempt and set the ledger to `stopped`;
do not fabricate a closure success state.

The packet may preserve worker verification claims, but the pure closure gate
must reject acceptance until a future Stage 3 caller supplies controller-owned
verification evidence.

### 5. Close Stage 2

Update this plan only for implementation facts that changed. Create a Stage 2
handoff containing exact files, test commands/results, unresolved findings, and
the first Stage 3 action. Do not rewrite `SKILL.md` yet.

## Risk-to-evidence matrix

| Risk or contract | Lowest reliable evidence | Scenario and oracle | Priority |
|---|---|---|---|
| Invalid persisted authority | Validator unit tests | Missing/unknown/wrong-type nested policy fields and truthy non-booleans are rejected before run creation | P0 |
| Worker claim treated as proof | Closure-gate unit test | Claimed passes with absent controller evidence cannot allow acceptance | P0 |
| Interruption leaves a worker alive | Local subprocess integration test | Interrupt the wrapper after thread start; worker group is absent and terminal state is durable | P0 |
| Manifest escapes task/repository scope | Validator unit tests | Absolute, parent-traversal, duplicate, missing-brief, unknown-dependency, and cyclic inputs are rejected | P0 |
| Wrong task is selected | Pure selection tests | Multiple ready tasks choose the first authorized policy ID; incomplete dependencies block candidates | P0 |
| Supervisor text changes authority | Prompt contract test | Prompt is reproduced from persisted inputs and contains no unselected task data or caller-supplied prose | P0 |
| Run state permits overlapping work | Ledger invariant tests | A selected or active attempt blocks another selection/launch and no second attempt directory appears | P0 |
| Repository changes between init and launch | Temporary Git integration test | New, deleted, renamed, staged, untracked, or changed dirty paths block dispatch before selection | P1 |
| Worker commits or stages changes | Temporary Git integration test | Closure packet records changed HEAD/index and reports a mechanical violation | P1 |
| Worker result is malformed | Result-contract unit tests | Invalid nested field types map to `missing_result` and never reach awaiting inspection as complete | P1 |
| Run inputs are replaced after init | Digest/integrity test | Modified persisted policy or manifest causes the next command to stop without ledger mutation | P1 |
| Partial initialization looks valid | Filesystem integration test | Failure before atomic rename leaves no final run directory; re-init never replaces an existing run | P1 |
| Closure evidence omits scope drift | Temporary Git integration test | Allowed, unexpected, untracked, renamed, and modified pre-existing paths appear in the packet with correct classifications | P1 |

Use bounded polling or process events for lifecycle tests. Do not use arbitrary
sleeps as the oracle. Every new behavioral test should first reject the current
implementation or an equivalent controlled fault.

## Expected file changes

Expected Stage 2 scope:

- `assets/task-manifest.schema.json` — new normalized manifest contract.
- `assets/run-ledger.schema.json` — add only if runtime code validates it.
- `scripts/controller.py` — strict validators, initialization, selection,
  prompt/attempt preparation, one-task dispatch, ledger, and closure packet.
- `scripts/codex_worker.py` — only the reviewed lifecycle/result-validation
  corrections and a minimal reusable preflight boundary.
- `tests/test_controller.py` — focused policy, manifest, ledger, selection,
  prompt, initialization, dispatch, and Git-evidence tests.
- `tests/test_codex_worker.py` — interruption and full result-contract tests.
- `docs/stage-2-handoff.md` — created only when implementation is complete.

Do not modify `SKILL.md`, `evals/evals.json`, or
`assets/worker-result.schema.json` unless a proven contradiction makes the
existing result contract impossible to validate. If that occurs, stop and
record the required contract change before editing it.

## Verification progression

Run one command at a time:

1. The single new failing test for the behavior being implemented.
2. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
3. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py`
4. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
5. Parse every JSON schema and fixture with Python's standard library.
6. Parse changed Python files with `ast.parse` without generating bytecode.
7. `git diff --check`
8. Inspect `git status --short` and confirm only intended Stage 1 files,
   Stage 2 files, and the preserved user analysis are present.

No full-repository suite is required unless shared tooling changes. Do not run a
real Codex smoke test, networked check, SDK spike, or dependency installation
without separate user authorization. Parse-only local Codex checks are needed
only if Stage 2 changes the effective CLI command shape.

## Stop conditions

Stop and ask the user if:

- policy version 1 cannot express a required authority decision without a
  breaking semantic change;
- task paths cannot be represented safely as exact repository-relative files;
- a run directory must live inside the repository;
- verification execution must be added before Stage 3, because command
  representation and permission semantics need a separate decision;
- deterministic interruption cleanup cannot be proven on the supported
  platform;
- implementation requires a dependency, network, a live model, a new top-level
  repository structure, or edits to installed/cached skill copies;
- current user changes overlap the intended Stage 2 files.

## Exit criteria

Stage 2 is complete when:

- the P1 Stage 1 findings are closed with deterministic local evidence, and the
  remaining P2 recovery item is explicitly carried to Stage 3 if not fixed;
- strict policy and manifest validation fail before run creation;
- initialization atomically persists immutable inputs, digests, a Git baseline,
  and an `initialized` ledger outside the repository;
- selection is deterministic and launches only the first dependency-ready
  authorized task;
- the prompt is reproducible from persisted selected-task authority only;
- a strict fake transport proves one launch, one attempt, and no overlap;
- worker completion moves only to `awaiting_inspection`, never `accepted`;
- the closure packet independently reports Git scope and integrity evidence and
  labels worker verification as claims;
- no tracker, commit, resume, second-task, skill-rewrite, live-model, network, or
  dependency behavior was added;
- the focused test suite, schema/AST parsing, and diff checks pass without
  generated artifacts.

## First implementation action

Add failing tests that prove `validate_run_policy()` rejects a schema-invalid
nested policy and `decide_closure()` rejects worker-claimed verification when
controller evidence is missing. Make those tests pass before adding the task
manifest or run initializer. This prevents Stage 2 from persisting or dispatching
from an authority model already known to be incomplete.
