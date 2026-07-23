# Task Orchestrator: Stage 2 Handoff

Status: complete; repeat closure review approved
Date: 2026-07-16
Parent direction: [direction.md](direction.md)
Stage 2 plan: [stage-2-plan.md](stage-2-plan.md)
Next plan: [stage-3-plan.md](stage-3-plan.md)

## Summary

Stage 2 is complete. The deterministic controller can initialize one immutable
run outside the repository, select the first dependency-ready authorized task,
preflight and launch exactly one fake-backed Codex worker, maintain coherent
controller-owned task and attempt state, and atomically publish an independent
closure packet at `awaiting_inspection`.

The repeat closure review verdict is `APPROVE`. The earlier validation,
preflight, interruption, closure-evidence, task-history, atomic-publication, and
decision-binding findings are closed with deterministic local evidence.

Stage 3 production behavior has not started. Stage 2 does not run controller
verification, accept a task, resume or retry a worker, update a tracker, commit,
or launch a second task.

## Completed Contracts

- Runtime run-policy and task-manifest validation matches the version 1 schema
  fields consumed by the controller, including required fields, types, unknown
  fields, unique arrays, exact task IDs, dependency existence, self-dependency,
  cycles, and repository-relative path constraints.
- `init` requires the actual Git top level, an existing HEAD, an outside-repo
  run directory, valid briefs, an unchanged source of authority, and atomic
  publication of canonical policy, manifest, baseline, and ledger records.
- `run-next` validates the ledger and persisted policy, manifest, and baseline
  digests; compares HEAD and content-aware status; rejects non-positive
  timeouts; and runs the reusable exact Codex command preflight before any task
  baseline, attempt, or ledger mutation.
- The reusable preflight mirrors the adapter's unsupported
  `danger-full-access` boundary, so an unlaunchable envelope fails before
  selection or artifact allocation.
- Attempts live under `attempts/attempt-001`, retain the exact adapter
  invocation and permission envelope, and are appended to task history before
  launch. Task state moves coherently from `initialized` to `running` to
  `awaiting_inspection` or `stopped`.
- SIGTERM interruption and exceptional cleanup terminate and reap the worker
  process group, serialize state writes with the stdout reader, clear PID
  ownership, and persist one matching terminal state record.
- Adapter output, terminal state, terminal-result record, prompt digest,
  contained artifact paths, and fully validated worker result must agree before
  closure. Missing or invalid terminal evidence durably stops the run.
- Closure evidence records task-baseline and final HEAD/index identities,
  staged and unstaged name/status and statistics, tracked and newly created
  untracked allowed-file patches, untracked paths, allowed/unexpected and
  pre-existing-path classifications, unauthorized HEAD/index violations, and
  adapter terminal evidence.
- Every closure artifact has a digest. The combined evidence digest binds
  policy, manifest, task baseline, prompt, Git identities, untracked paths,
  artifact digests, and adapter state.
- The complete closure packet is atomically written once, then referenced by
  one atomic ledger transition to `awaiting_inspection`.
- Stage 2 closure always reports `accepted: false` and offers only `inspect`
  and `stop` actions. The future acceptance transition requires a literal
  boolean, `accepted` in a real transition list, and an exact current
  run/task/attempt/prompt/evidence identity match.

## Files

- `../assets/task-manifest.schema.json` — normalized version 1 manifest
  contract.
- `../scripts/controller.py` — strict validation, atomic initialization,
  deterministic selection, preflight, one-attempt dispatch, ledger history,
  Git evidence, closure publication, and identity binding.
- `../scripts/codex_worker.py` — reusable exact preflight, full result
  validation, process ownership, timeout/interruption cleanup, and durable
  terminal state.
- `../tests/test_controller.py` — controller contracts and temporary-Git/fake
  transport integration evidence.
- `../tests/test_codex_worker.py` — adapter contract, timeout, signal, process
  group, result, and resume-denial evidence.

`../SKILL.md`, `../evals/evals.json`, `../assets/worker-result.schema.json`, and
`../assets/run-policy.schema.json` were not changed by the Stage 2 closure
slice.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed, 39 tests in 3.399 seconds.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py`
  — passed, 15 tests in 3.960 seconds.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — passed, 54 tests in 7.052 seconds.
- All four task-orchestrator JSON assets/evals parse with `jq`.
- The two changed scripts and two changed test modules parse with `ast.parse`
  without bytecode generation.
- `git diff --check` and `git diff --cached --check` pass.
- The repeat read-only Stage 2 closure review found no actionable findings and
  returned `APPROVE`.

Not run: live Codex/model execution, network checks, dependency installation,
SDK/MCP work, controller verification commands, full-repository tests, commits,
tracker updates, resume/retry, or a second task launch.

## Preserved Workspace State

- The pre-existing staged `skills/testing-discipline/SKILL.md` change remains
  untouched.
- The untracked `../agent-output.analysis.md` remains untouched.
- No reset, clean, broad staging, commit, network call, dependency install, or
  live model call was performed.

## Residual Risks And Stage 3 Boundary

- Real Codex CLI compatibility remains unproved by design; Stage 2 uses strict
  local fake executables and parse-only command-shape evidence.
- Controller-owned verification, recovery, immutable resume turns, acceptance,
  tracker integration, exact-path commits, and finalization reconciliation are
  Stage 3 contracts, not implied by this approval.
- Human tracker mode remains off until a versioned tracker contract is approved.
- Semantic diff review remains `not_collected` until its actor/interface is
  chosen.

## First Stage 3 Action

Run the local verification-sandbox proof from `stage-3-plan.md`. It must show
that a non-model verification runner can enforce the persisted network,
writable-root, dependency-install, and sandbox limits before any Stage 3
verification or acceptance implementation is added.
