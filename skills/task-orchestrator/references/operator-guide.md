# Task Orchestrator Operator Guide

Status: operator reference

Freshness: 2026-07-23

This guide covers only the public controller behavior implemented today.

## Prepare confirmed inputs

Start from:

- [minimal-run-policy.json](../assets/examples/minimal-run-policy.json);
- [minimal-task-manifest.json](../assets/examples/minimal-task-manifest.json);
- [run-policy.schema.json](../assets/run-policy.schema.json); and
- [task-manifest.schema.json](../assets/task-manifest.schema.json).

Replace the example repository with its absolute Git top-level and use the same
absolute path in `permissions.writable_roots`. Ensure every brief exists and
every `allowed_paths` entry is repository-relative. Confirm the policy and
manifest with the operator before initialization.

The supported commit modes are `off` and `controller_exact_paths`. Workers do
not commit. Because the current public commands do not complete controller-owned
finalization, use `off` for the present controller-only flow.

## Initialize

Place the run directory outside the repository, then run:

```bash
python3 <skill-dir>/scripts/controller.py init \
  --run-dir <external-run-dir> \
  --policy <run-policy.json> \
  --manifest <task-manifest.json> \
  --repository <repository>
```

Initialization validates the inputs, requires the repository to be a Git
top-level with a `HEAD`, records the initial Git state, and publishes immutable
run inputs plus the controller ledger.

## Launch one task

Confirm that the repository still matches the controller baseline:

```bash
python3 <skill-dir>/scripts/controller.py run-next \
  --run-dir <external-run-dir> \
  --timeout-seconds <seconds>
```

The controller selects one dependency-ready task and invokes the internal Codex
transport. Do not call `scripts/codex_worker.py` directly.

## Inspect one completed attempt

After `run-next` leaves the task in `awaiting_inspection`, run:

```bash
python3 <skill-dir>/scripts/controller.py inspect \
  --run-dir <external-run-dir> \
  --timeout-seconds <seconds>
```

Inspection validates controller-owned records, repository identity, allowed
scope, structured worker results, and configured verification. A positive
decision is mechanical eligibility, not semantic acceptance. The current CLI
does not yet atomically accept the task, release dependencies, or advance.

## Interruption and recovery

The current public controller has no safe-stop or resume command. On an
interrupted, timed-out, or ambiguous attempt:

1. Do not launch another worker.
2. Inspect the ledger, attempt record, stored process identity, current Git
   state, and structured result if present.
3. Determine whether the recorded process is live, absent, or ambiguous.
4. Stop and report the evidence.
5. Route implementation of safe reconciliation or same-thread continuation to
   MVP-3 in the current Stage 3 rebaseline.

Do not use direct `codex_worker.py resume` to bypass missing controller
reconciliation. That older route cannot provide the controller-owned process
and state guarantees required by the current design.

## Current stop report

Report the run/task/attempt identifiers, ledger state, process evidence, Git
state, structured result and verification paths, semantic-review status, and
the next available controller command. If the required command does not exist,
name the owning MVP increment instead of inventing an operational workaround.
