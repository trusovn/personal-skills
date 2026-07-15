---
name: task-orchestrator
description: Supervise an approved long-running implementation task list by delegating one bounded task at a time to resumable external coding-agent sessions, inspecting structured handoffs and diffs, applying policy-bounded judgment, and maintaining durable progress. Use whenever the user wants an agent to execute a multi-task plan unattended, work through a task ledger without babysitting, coordinate `codex exec` workers from a cheaper local model, resume interrupted worker sessions, or use SDD task artifacts as an external-worker queue. Do not use to invent the plan or replace feature specification and task-breakdown skills.
compatibility: Requires a durable task list and repository access. The bundled Codex adapter requires Python 3 and a Codex CLI with exec resume, JSONL, and output-schema support.
---

# Task Orchestrator

Act as a low-cost control plane around stronger implementation workers. Keep the orchestration context small: plan constraints, task state, worker summaries, diffs, and verification evidence. Do not ingest full worker transcripts during normal operation.

This skill executes an already-approved plan. If requirements, architecture, or task decomposition are still being designed, finish those artifacts first.

## Operating model

Use this v1 shape:

```text
approved plan + durable tracker
            ↓
select one ready task
            ↓
start or resume one worker thread
            ↓
structured handoff + task-scoped diff
            ↓
accept, resume, escalate, or reject
            ↓
update tracker and select the next task
```

Run sequentially in one working tree. Parallel writes require isolated worktrees, merge ordering, and conflict recovery; do not add them merely because the task graph has parallel width.

## Preconditions

Before launching a worker:

1. Identify the authoritative plan, task index, task briefs, and tracker. Prefer an existing machine-readable ledger such as `tasks.json` plus a human tracker.
2. Confirm that product and architecture decisions are settled enough for implementation. A task must have a bounded outcome, dependencies, verification, and a stop condition.
3. Read applicable `AGENTS.md` files and repository instructions.
4. Inspect `git status --short`. Record pre-existing changes so worker output cannot be confused with user work.
5. Establish the run policy with the user or reuse an explicit policy already attached to the plan:
   - working repository and task range;
   - verification command and whether expensive/live checks are allowed;
   - commit policy: `off`, `per-task`, or another explicit rule;
   - permission envelope, including dependency installation, network, external writes, and destructive commands;
   - stop policy for failures and unresolved decisions.
6. Choose a durable run directory that survives terminal or OS restarts. Keep it out of task commits. If the repository has no ignored local-state location, tell the user before creating or ignoring one.

Do not silently infer commit permission, network use, dependency installation, destructive actions, credential access, or writes outside the declared workspace.

## Build the queue

- Read the index and dependency data first; load only the current task brief and the upstream sections it cites.
- Select exactly one task whose dependencies are complete.
- Never combine adjacent tasks because the worker appears to have spare context.
- If the current task requires a second subsystem, a new architectural decision, or broad prerequisite work, stop and report that the task boundary is wrong.
- Treat the tracker as orchestration-owned. Workers return structured results; the orchestrator records accepted progress.

For SDD artifacts, read `docs/features/<slug>/tasks.json`, `tasks/tracker.md`, the selected task file, and its cited AC/design/test-plan sections. Preserve the SDD task's RED → GREEN → REFACTOR → GATE contract. Do not run the whole-feature `sdd-implement` inside this skill; choose one orchestration engine for the run.

## Launch a worker

Give the worker a fresh, bounded prompt containing:

- task ID, title, and authoritative brief paths;
- required plan/spec/design sections to read directly;
- relevant dependencies already completed;
- pre-existing dirty paths to preserve;
- exact scope and prohibited adjacent work;
- targeted and repository verification commands;
- permission and commit policy;
- the requirement to return the structured status described by `assets/worker-result.schema.json`.

Do not paste the orchestrator transcript or previous workers' raw output into the prompt. Let the worker read repository artifacts directly.

Use the bundled adapter when Codex is the worker:

```bash
python3 <skill-dir>/scripts/codex_worker.py start \
  --run-dir <durable-task-run-dir> \
  --cwd <repository> \
  --prompt-file <task-prompt-file> \
  --model <model> \
  --effort medium
```

The adapter starts Codex with a workspace-write sandbox and `approval=never`, captures JSONL in the run directory, records the thread ID as soon as Codex emits it, and writes only a structured result path to normal stdout. Use `danger-full-access` only after the user explicitly authorizes that exact risk.

## Inspect the result, not the transcript

On a normal worker exit, read:

1. the latest `turn-NNN.result.json`;
2. `git status --short`;
3. diff names/statistics and the task-scoped diff;
4. untracked files created by the task;
5. verification commands and outcomes from the structured result.

Check that every changed line traces to the task, expected behavior has evidence, unrelated dirty files remain untouched, and the repository is in an acceptable state. Re-run a targeted gate when evidence is missing or risk warrants it. Do not duplicate an expensive or live verification run without authorization.

Open `turn-NNN.events.jsonl` or the stderr log only when the structured result is missing, contradictory, or insufficient to diagnose a failure. Full transcripts are diagnostic artifacts, not routine orchestration context.

## Make bounded decisions

The orchestrator may decide and resume without asking the user only when all of these are true:

- the choice is directly entailed by an explicit plan constraint or established repository pattern;
- the worker gives a recommendation with concrete reasoning;
- the choice is local to the current task and reversible before dependent tasks start;
- it does not change a public contract, architecture boundary, persistence meaning, security/privacy posture, user-visible product rule, cost commitment, or permission envelope;
- no comparably valid option remains after applying the authoritative constraints.

Example: if the plan explicitly requires a transport-independent domain value, choosing canonical before/after values over a presentation-specific unified diff is within the decision budget.

Escalate to the user when any condition fails. State the options, worker recommendation, authoritative constraints, impact, and your recommendation. Do not ask the worker to guess a product decision repeatedly.

## Permissions

Treat permission policy separately from design judgment:

- Proceed with reads, task-scoped workspace edits, and local commands already inside the declared envelope.
- A failed non-interactive approval is a blocked action, not permission to broaden the sandbox.
- Resume with expanded access only after the user explicitly authorizes the command class and scope.
- Never grant access to credentials, unrelated repositories, arbitrary network destinations, destructive commands, or `danger-full-access` based only on a worker request.
- If recurring tasks need the same safe capability, ask once for a narrow reusable authorization before the run rather than interrupting every task.

## Resume instead of relaunching

When the worker returns `needs_input`, crashes, times out, or is interrupted after a thread ID was recorded:

1. Verify that no old worker process is still active.
2. Inspect the current diff and structured result if present.
3. Decide within the policy above or obtain user input.
4. Put only the decision and any changed constraints in a follow-up prompt file.
5. Resume the recorded thread:

```bash
python3 <skill-dir>/scripts/codex_worker.py resume \
  --run-dir <durable-task-run-dir> \
  --prompt-file <follow-up-prompt-file>
```

Do not start the task from scratch while a resumable thread and partial diff exist. Avoid `codex exec resume --last` in orchestration because another session may be newer; use the recorded thread ID.

If no thread ID was recorded, inspect the diff before launching anything else. Start a replacement worker only with an explicit recovery brief describing existing partial changes and requiring it to preserve or complete them.

## Close a task

Accept a task only when:

- the structured status is `complete`;
- the diff stays within the task boundary;
- required targeted checks pass;
- the repository-wide gate passes when the plan requires it;
- no blocking question or unexplained risk remains.

Then:

1. Update the authoritative tracker with status, concise summary, changed files, verification, decisions, and residual risks.
2. Commit only if the run policy explicitly allows it. Stage task-scoped paths; do not use blanket staging in a dirty worktree.
3. Record the commit ID when applicable.
4. Re-read the task index and select the next dependency-ready task.

For `blocked` or `failed`, record the exact reason and apply the stop policy. Never mark a task complete merely because a worker process exited successfully.

## End-of-run report

Report:

- completed, blocked, and remaining task IDs;
- accepted decisions and escalations;
- commits, if authorized;
- checks run and gaps not verified;
- current dirty state and durable run/tracker paths;
- the next ready task or the reason the run stopped.

## Anti-patterns

- Reading every task brief and every worker transcript into the orchestrator context.
- Relaunching a fresh worker after a clarification instead of resuming its thread.
- Letting the worker update orchestration state or choose the next task.
- Treating a plausible summary as proof without inspecting the diff.
- Making a novel product or architecture decision because it avoids waking the user.
- Expanding permissions after a non-interactive failure without explicit authorization.
- Combining tasks, blanket-staging a dirty tree, or committing orchestration logs.
- Nesting this supervisor around another whole-plan implementation orchestrator.
