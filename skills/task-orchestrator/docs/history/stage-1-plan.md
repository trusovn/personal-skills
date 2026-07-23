# Task Orchestrator: Stage 1 Plan

Status: ready for a fresh implementation session
Parent direction: [direction.md](direction.md)

## Objective

Create an executable safety contract for the future deterministic controller and stabilize the Codex worker transport against the failures already observed.

Stage 1 ends with deterministic local tests passing and a recorded CLI-versus-SDK decision. It does not yet run a real task queue or rewrite `SKILL.md`.

## Working assumptions

- The dedicated `../agent-output.analysis.md` is the evidence source for the prior run. Do not load the full transcript unless a specific unresolved claim cannot be answered otherwise and the user approves.
- No commits are authorized merely by this plan.
- Default verification is local and cheap. Do not install dependencies, use the network, or launch a paid/live Codex task without asking the user first.
- Preserve the current skill and wrapper as the baseline until a test demonstrates each intended behavior.
- Use Python's standard library and the existing test framework unless a concrete contract cannot be proven that way.
- Keep the first controller contract sequential and single-worktree.

## Deliverables

Stage 1 should produce the smallest coherent set of artifacts needed to prove the contracts below:

1. A controller contract document covering authority, state transitions, durable records, and closure gates.
2. A machine-readable run-policy contract or schema with explicit commit, permission, verification, and stop policies.
3. A hardened worker transport or replacement transport spike with capability preflight and safe process lifecycle behavior.
4. Deterministic tests for the risk matrix below.
5. A short transport decision record: corrected CLI selected, SDK selected, or SDK evaluation explicitly deferred with reasons.
6. A Stage 1 handoff recording commands, results, remaining gaps, and the first Stage 2 action.

Do not create speculative queue features, parallelism, plugin packaging, a UI, or generalized configuration beyond these contracts.

## Contracts to define before implementation

### Authority

Define source precedence and reject contradictions:

1. system/repository instructions;
2. explicit persisted user run policy;
3. authoritative task ledger and selected task brief;
4. controller-generated worker prompt;
5. worker result or recommendation.

A lower source cannot grant authority denied or omitted by a higher source. Generated prompts and worker results are never authority sources for commits or permission expansion.

### Worker boundary

- Worker may read and make task-scoped workspace edits within the effective sandbox.
- Worker never commits, updates the orchestration ledger, chooses the next task, patches the installed controller, or broadens permissions.
- Worker reports structured status and evidence claims; the controller independently inspects the worktree.

### State transitions

Specify allowed transitions and rejection behavior for at least:

- initialized, ready, running, awaiting inspection, accepted;
- needs input, blocked, failed, timed out, interrupted, missing result;
- resumable versus terminal attempts;
- active-process and ambiguous-process states.

No transition out of `running` may be inferred only from the supervising shell timing out. No task may move to accepted directly from a worker result.

### Closure gate

Acceptance requires all of the following:

- result status is `complete` and task ID matches;
- expected targeted checks passed;
- required repository gate passed or an explicitly authorized gap is recorded;
- changed and untracked paths are within the task allowance;
- pre-existing dirty paths remain preserved;
- no blocking question or unexplained risk remains;
- commit and tracker actions are valid under the persisted policy.

The gate returns allowed next transitions and reasons. It does not mutate the repository merely because acceptance is possible.

## Risk-to-evidence matrix

| Risk or contract | Lowest reliable evidence | Scenario and oracle | Priority |
|---|---|---|---|
| Safe CLI configuration is rendered incorrectly | Transport command unit test plus local parse smoke | A strict fake rejects flags in invalid positions; generated command contains workspace-write and approval-never without a bypass flag | P0 |
| Installed CLI cannot express the required safe mode | Preflight component test | Unsupported help/capability output stops before process launch or durable run creation; no fallback broadens permissions | P0 |
| Timeout leaves a worker alive | Real local subprocess integration test | A fake worker sleeps and spawns/represents ongoing work; timeout terminates and reaps it, records a terminal reason, and leaves no active PID | P0 |
| Resume overlaps an active worker | State/process integration test | State says running and recorded PID is alive; resume is rejected and no second process starts | P0 |
| Worker status is mistaken for acceptance | Pure closure-gate state test | `complete` without independent closure evidence yields awaiting-inspection/rejected, never accepted | P0 |
| Unexpected files are accepted | Closure-gate unit test with a temporary Git repository | Worker reports allowed files but the worktree has an extra changed/untracked path; acceptance is denied with that path in evidence | P0 |
| Commit authority is invented | Run-policy/state test in a temporary Git repository | `commit_policy: off` rejects commit transition and Git history/index remain unchanged | P0 |
| Worker is asked to commit | Prompt-contract test | Rendered worker prompt explicitly prohibits commits regardless of controller commit policy | P0 |
| Failed evidence is lost or overwritten | Filesystem state test | Retry/resume allocates a new immutable attempt/turn; prior prompt, events, stderr, result, and terminal state remain byte-identical | P1 |
| Task identity is ambiguous during recovery | State-schema test | Every started attempt requires task ID, brief path, prompt hash, baseline reference, and effective permission settings | P1 |
| Missing or malformed result advances the run | Transport/closure integration test | Zero process exit with absent or invalid result becomes `missing_result`; next-task and commit transitions are unavailable | P1 |
| Installed skill self-modification contaminates the run | Allowed-path/policy test | Skill/cache/controller paths outside task scope are reported as violations and block acceptance | P1 |

Use controlled subprocess synchronization and bounded deadlines; do not use arbitrary sleeps as the oracle.

## Execution order

### 1. Re-establish the baseline

Read:

- `../agent-output.analysis.md`;
- `../SKILL.md`;
- `../scripts/codex_worker.py`;
- `../tests/test_codex_worker.py`;
- `../assets/worker-result.schema.json`;
- this plan and `direction.md`.

Then run the current focused suite without creating bytecode artifacts:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/task-orchestrator/tests \
  -p 'test_*.py'
```

Record the baseline, current Codex version, and safe parse-only CLI checks. Do not launch a model.

### 2. Write the controller contract

Document the minimum persisted fields, state transitions, closure inputs, allowed outputs, and authority precedence. Resolve naming only where tests or schemas require it.

Keep transport lifecycle separate from task acceptance so CLI, SDK, or MCP can be substituted later without changing policy behavior.

### 3. Add failure-first tests

Start with the P0 cases. Demonstrate that each test rejects the current behavior or an equivalent controlled fault before changing production code. Confirm the failure is the intended assertion rather than a broken fixture.

Use:

- a strict fake Codex executable that validates argument structure;
- temporary Git repositories for closure and commit-policy tests;
- a controllable subprocess fixture for timeout and active-PID behavior;
- small JSON fixtures for policy and state transitions.

Do not use the real model, network, credentials, or the user's other repositories.

### 4. Implement only enough enforcement to satisfy P0

Expected minimum behavior:

- safe CLI command construction and preflight;
- no dangerous compatibility fallback;
- process ownership, bounded termination, and reaping;
- active-run resume rejection;
- explicit distinction between transport completion, worker status, inspection, and acceptance;
- immutable persisted policy and attempt artifacts;
- closure-gate denial for unexpected paths and unauthorized commits;
- worker prompt contract that always prohibits commits.

Prefer a small pure state/policy core plus the transport boundary. Avoid building the queue loop in Stage 1.

### 5. Complete P1 cases and regression coverage

Add only the P1 cases that protect durable recovery and evidence integrity. Re-run the focused suite after each behavior stabilizes, then the complete task-orchestrator test directory.

### 6. Decide the transport

Choose the corrected CLI unless Stage 1 evidence shows it cannot provide safe cancellation, resumption, structured output, or capability detection.

Consider an SDK spike only if that evidence exists. Before installing or invoking an SDK:

- state the exact missing CLI property;
- ask for dependency/network authorization;
- isolate the spike from production code;
- compare lifecycle behavior, version pinning, structured output, and operational cost;
- record the decision and remove abandoned spike artifacts.

MCP packaging and supervisor tool restriction are not Stage 1 requirements.

### 7. Close Stage 1

Update the contract and transport decision from test evidence. Create a continuation handoff with exact files, commands, results, gaps, and the first Stage 2 task.

Do not rewrite `SKILL.md` yet; Stage 4 will make the prose match the controller that actually exists.

## Verification progression

1. Run the new or changed test that demonstrates one contract.
2. Run the nearest test module.
3. Run all `skills/task-orchestrator/tests`.
4. Run parse-only checks against the locally installed Codex CLI.
5. Offer, but do not automatically run, a real no-network/no-commit Codex smoke test after all local evidence passes.

No full-repository suite is required unless Stage 1 changes shared repository tooling.

## Stop conditions

Stop and ask the user before continuing if:

- the only available configuration requires bypassing approvals or sandboxing;
- completing Stage 1 requires a new dependency, network access, or a paid/live worker run;
- the implementation needs new top-level repository structure or shared tooling;
- process cleanup cannot be made deterministic on the supported platform;
- task-manifest normalization requires a product choice about supported input formats;
- a proposed change would edit installed/cached skill copies or user work outside this skill source.

## Exit criteria

Stage 1 is complete when:

- authority, worker boundaries, states, and closure gates are documented;
- every P0 scenario passes deterministically and was shown capable of failing for the expected reason;
- selected P1 recovery/evidence tests pass;
- current happy-path start/resume behavior remains covered;
- the focused test command passes without network or live model calls;
- the effective safe CLI invocation is proven, or a documented SDK decision replaces it;
- no dangerous fallback, worker commit path, active-process resume, or evidence deletion remains;
- `SKILL.md` and task-queue execution remain intentionally deferred;
- the worktree contains only intended Stage 1 changes and preserved user files.
