# Task Orchestrator: Direction

Status: agreed direction for the next design iteration
Date: 2026-07-15
MVP rebaseline: 2026-07-21

## Purpose

Evolve `task-orchestrator` from a prompt-heavy supervisor around a thin process wrapper into a deterministic controller with a thin skill. Correctness and safety should not depend on a supervisor model remembering a long procedural checklist across many tasks.

The original goal remains: let an inexpensive supervisor coordinate stronger Codex implementation workers through an approved task ledger without routine babysitting. The change is that the supervisor will no longer be the authority for policy, process state, acceptance gates, or commits.

## Why the current shape is insufficient

The current skill describes useful policies, but most are not enforced by code. The wrapper starts or resumes Codex and records output; the supervisor must independently remember permission boundaries, task authority, recovery rules, Git inspection, acceptance, tracker ownership, and commit policy.

The analyzed run exposed the consequences:

- an invalid CLI argument position was misdiagnosed as a missing safe capability;
- the installed adapter was changed to bypass approvals and sandboxing;
- generated worker prompts invented commit authority;
- worker claims were accepted without the required Git closure evidence;
- timed-out processes were resumed without proving the old process had stopped;
- failed-attempt evidence and tracker ownership were not preserved reliably.

These are not best addressed by adding more warnings to `SKILL.md`. They identify responsibilities that belong in an enforceable protocol.

## Decision

Build a deterministic controller and make the skill a compact operator and judgment guide.

The controller owns:

- immutable run policy;
- task selection from a machine-readable ledger;
- prompt construction from the selected task only;
- worker start, resume, timeout, cancellation, and process reaping;
- durable attempt state and evidence;
- Git baseline and closure inspection;
- acceptance-state transitions;
- tracker updates;
- task-scoped commits when explicitly authorized.

The Codex worker owns:

- implementation inside the selected task boundary;
- targeted and authorized repository verification;
- a structured result with decisions, risks, questions, and claimed evidence;
- no commits and no orchestration-ledger changes.

The inexpensive supervisor is optional and bounded. It may interpret a closure packet, make a locally reversible decision already entailed by authoritative constraints, or phrase a resume request. It must not create authority, mutate controller state directly, patch the controller, broaden permissions, commit, or select an action the controller says is invalid.

## Target operating model

```text
approved task ledger + immutable run policy
                    |
                    v
        deterministic controller
        - selects one ready task
        - snapshots Git state
        - renders bounded prompt
                    |
                    v
             Codex worker
        - implements and verifies
        - never commits
                    |
                    v
        structured result + closure evidence
                    |
                    v
        mechanical acceptance gate
          |         |          |
        accept     resume     escalate/stop
          |
          v
 tracker update + optional controller-owned commit
```

## Enforceable invariants

These are controller contracts, not reminders:

1. A run starts only from an explicit, persisted policy covering task range, verification, permissions, commit behavior, and stop behavior.
2. The effective worker command and permission envelope are validated and recorded before launch. Unsupported safe configurations fail closed.
3. `danger-full-access` and approval/sandbox bypass flags are rejected unless the run policy contains explicit authorization for that exact mode.
4. Workers never commit. The controller may commit exact accepted paths only when the persisted policy allows it.
5. One task and one active worker attempt may own the working tree at a time.
6. Resume is rejected while the recorded process is alive or its state is ambiguous.
7. Timeout or interruption causes bounded termination, process reaping, and a durable terminal attempt state before recovery is considered.
8. Attempts are immutable. A retry or resume creates new turn artifacts; failed evidence is never deleted or overwritten.
9. A worker result is a claim, not acceptance. Closure evidence is gathered independently from the worktree.
10. Unexpected changed paths, missing required verification, blocking questions, unexplained risks, or a non-`complete` result prevent acceptance.
11. The controller alone changes the orchestration ledger. Repository plan notes may be task artifacts, but they are not the acceptance ledger.
12. Installed or cached skill copies are never patched during a run. Compatibility failure stops before task execution.

## Controller state model

Exact names may change during Stage 1, but allowed transitions must be explicit and tested.

```text
initialized -> ready -> running -> awaiting_inspection
                                      |       |       |
                                  accepted  resumable  stopped
                                                |
                                             running
```

`blocked`, `failed`, `needs_input`, `timed_out`, and `missing_result` are distinct outcomes. A successful wrapper process exit must not imply task acceptance.

Each attempt should identify at least:

- task ID and brief path;
- attempt/turn number and prompt hash;
- thread ID and process identity;
- start/end timestamps and terminal reason;
- effective transport, model, sandbox, approval, network, and writable-root settings;
- pre-task Git baseline reference;
- result and diagnostic artifact paths.

## Durable artifacts

Names are provisional until Stage 1 fixes the contract:

- run policy: immutable user authority and operational constraints;
- task manifest: IDs, dependencies, brief references, expected paths, and required checks;
- run ledger: controller-owned task and attempt states;
- attempt directory: prompt, events, stderr, structured result, and terminal state;
- closure packet: status, name/status diff, statistics, untracked paths, allowed-path comparison, verification, questions, risks, and proposed next transitions.

The normal supervisor context should contain the selected task, run policy summary, and closure packet—not full worker transcripts or every future task brief.

## Transport boundary

The controller should depend on a narrow worker transport interface: preflight, start, poll/wait, cancel, resume, and collect result. Transport choice does not own task policy or acceptance.

The corrected Codex CLI is the default first implementation because it has the smallest dependency footprint. The known argument failure is positional: `--ask-for-approval` is a global option when expressed as a flag, while a scoped config override is also accepted by the current CLI. Stage 1 must prove the chosen invocation rather than relying on remembered syntax.

The Codex SDK remains an alternative if a bounded spike demonstrates materially safer lifecycle control or version compatibility. Adopting the SDK must not be mistaken for implementing the controller state machine. Codex-as-MCP is a later packaging/integration option if the supervisor should receive typed tools instead of general shell access.

## Delivery stages

### Stage 1: Contract, failure harness, and transport decision

- Define controller authority, state transitions, durable records, and closure gates.
- Turn the observed failures into deterministic tests.
- Correct and preflight the safe CLI invocation.
- Prove timeout cleanup and active-process resume rejection with local fake processes.
- Record whether the CLI is sufficient or an SDK spike is justified.

Stage 1 does not orchestrate a real task list, rewrite the skill, launch paid/live model runs, or add a new dependency by default.

### Stage 2: Controller core

- Initialize a run from policy and a normalized task manifest.
- Select one dependency-ready task.
- Snapshot baseline state, render the prompt, and launch through the transport.
- Persist the ledger and produce a closure packet.

### Stage 3: Acceptance, recovery, tracker, and commits

- Enforce closure gates and allowed transitions.
- Implement resume, interruption recovery, and immutable attempts.
- Update the controller ledger and any approved human tracker.
- Add exact-path controller-owned commits under explicit policy.

### Stage 4: Thin skill and constrained supervisor interface

- Rewrite `SKILL.md` around the controller commands and bounded judgment.
- Decide whether Qwen receives typed MCP tools, a restricted command surface, or remains an advisory reviewer.
- Remove prose that duplicates enforced controller behavior.
- Build skill evaluations for normal progress, decision escalation, recovery, and policy denial.

### Stage 5: Pilot and iterate

- Run a small synthetic multi-task repository first.
- After user approval, run one real Codex task without network or commits.
- Compare closure evidence with the original skill baseline.
- Expand to a short real task sequence only after the first pilot is accepted.

## MVP rebaseline: local configurable task flow

The Stage 3 mid-review showed that the controller has built useful mechanical
boundaries but has not yet delivered the unattended implementation and
correction loop that motivated the project. The remaining work is therefore
reordered around an early local MVP. This section supersedes the Stage 3–5
delivery order above where they conflict; the earlier sections remain as the
design history and source of the invariants worth preserving.

The governing high-level plan is
[stage-3-mvp-rebaseline.md](stage-3-mvp-rebaseline.md). The evidence that led to
the change is recorded in
[stage-3-mid-review.md](history/stage-3-mid-review.md). Deferred
information-architecture work that should inform later task actualization is
recorded in
[stage-3-retrieval-surface-follow-up.md](stage-3-retrieval-surface-follow-up.md).

### Revised product goal

On one local development machine, accept an approved task document or manifest
and execute a configurable sequential flow across its tasks with minimal
babysitting. A normal reviewed flow should be able to:

```text
prepare task -> optional preflight -> implement -> verify -> optional review
     ^                                                   |
     +---------------- correct and resume <--------------+
                                                         |
                                             accept -> next task
```

Preflight, verification, and semantic review are selectable steps rather than
hardcoded requirements. Their modes and actors are run configuration. The
controller keeps the non-configurable safety invariants; a thin workflow runner
interprets the configured step sequence and invokes the appropriate actor.

### Local trust and safety model

- The operator, local machine, repository, and external run directory are
  trusted. Malicious third-party mutation is not a design target.
- The relevant failures are LLM hallucination, accidental scope expansion,
  overlapping workers, stale state, crashes, and incomplete recovery.
- A real sandbox boundary, such as the current supported local mechanism or a
  later Docker-backed sandbox, is the primary containment for worker commands.
- Digests and immutable artifacts detect stale, contradictory, or accidentally
  corrupted evidence. They are not a cryptographic security boundary and do
  not require an externally anchored chain for the MVP.
- The controller must not duplicate a general sandbox, package-manager policy,
  or adversarial audit system in application code.

### Revised architecture boundary

Keep the deterministic controller for task ownership, persisted run state,
process lifecycle, repository observations, and acceptance transitions. Add a
small workflow layer with a closed set of supported step kinds and structured
outcomes. A run profile may add, remove, reorder where valid, or change the
level/actor of supported steps without a code change. Arbitrary plugins,
unrestricted jumps, and a general workflow engine are beyond the MVP.

The chosen workflow is persisted at run start so an implementation or review
agent cannot silently alter its own process. The operator may change the flow
between runs, or explicitly revise it at a safe task boundary. Such a revision
is authority from the operator, not a worker recommendation.

### Revised delivery order

1. Close the bounded S3-08 correctness gap under the local trust model.
2. Freeze the configurable flow-step and outcome contract.
3. Complete safe recovery and same-thread correction/resume.
4. Add optional preflight and semantic-review actors plus the review/fix loop.
5. Add simple side-effect-free acceptance, dependency release, and an
   `advance` loop that proceeds until completion or a genuine escalation.
6. Add plan-to-manifest preparation and rewrite the skill around the runnable
   controller/workflow interface.
7. Run synthetic and real local pilots before implementing controller-owned
   commits, tracker mutation, or more assurance machinery.

Exact-path commits, tracker adapters, prepared external-side-effect journals,
parallel worktrees, distributed coordination, malicious-tamper resistance, and
a custom step plugin system are post-MVP work. They should be pulled forward
only when a pilot demonstrates that they block practical use.

## Deferred decisions

Do not silently decide these during Stage 1:

- whether semantic diff review is performed by Qwen, a separate read-only Codex reviewer, or a human for higher-risk tasks;
- whether Qwen can be technically denied general shell/write access;
- whether arbitrary Markdown task lists must be normalized and confirmed before a run;
- whether the long-term transport is CLI, SDK, or MCP-backed;
- whether parallel worktrees are ever worth supporting.
- adding metrics geathering as per templates [execution-brief-pilot-measurement.md](execution-brief-pilot-measurement.md) and [execution-brief-template.md](execution-brief-template.md)

## Rejected shortcuts

- Adding more emphatic prose while leaving enforcement with the supervisor.
- Treating a structured worker result as independent proof.
- Letting workers commit under `workspace-write`.
- Broadening permissions after a failed non-interactive action.
- Editing an installed skill or adapter during a task run.
- Treating SDK or MCP adoption as a substitute for controller policy and state.
- Loading the full 3,829-line transcript during this redesign when the dedicated analysis is sufficient.

## Evidence used for this direction

- `../agent-output.analysis.md` — dedicated execution/process analysis; the full transcript was intentionally not loaded.
- `../SKILL.md` — current prompt-level operating policy.
- `../scripts/codex_worker.py` — current transport wrapper.
- `../tests/test_codex_worker.py` — current happy-path wrapper tests.
- `../assets/worker-result.schema.json` — current worker self-report contract.
- Current local Codex CLI parsing checks and the official Codex manual fetched on 2026-07-15.
