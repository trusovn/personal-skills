# Task Orchestrator Architecture Map

Status: operator reference

Freshness: 2026-10-22

Read only the row that owns the requested behavior, then inspect its primary
test. Use `controller.py` integration coverage when a public command or
cross-module flow changes.

| Concern | Source | Primary tests |
|---|---|---|
| CLI and controller use cases | `scripts/controller.py` | `tests/test_controller.py` |
| State, validation, and durable record contracts | `scripts/controller_state.py` | `tests/test_controller_state.py` |
| Git status, identity, scope, and drift evidence | `scripts/controller_git.py` | `tests/test_controller_git.py` |
| Verification command planning and execution | `scripts/verification_runner.py` | `tests/test_verification_runner.py` |
| Codex CLI transport and thread records | `scripts/codex_worker.py` | `tests/test_codex_worker.py` |
| Current retrieval surface and examples | `SKILL.md`, `references/`, `assets/examples/` | `tests/test_retrieval_surface.py` |

## Public entry points

```text
controller.py init
controller.py run-next
controller.py inspect
controller.py revise-flow
```

`codex_worker.py` is an internal adapter. A new operator action belongs in the
controller or the future workflow runner, not in prompt-level calls to the
adapter.

## Verification commands

Run the owning module first:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_retrieval_surface.py
```

After targeted checks pass, run the full local suite when the change crosses
modules or affects the skill's public guidance:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/task-orchestrator/tests -p 'test_*.py'
```

## Authority and existing records

Repository and system instructions bound the explicit persisted run policy,
manifest and task brief. Actor prompts, results and recommendations cannot grant
permissions, commit authority or ownership of the ledger. A worker reports claims;
`inspect` independently checks records, repository identity, task scope, existing
owner changes and configured verification before recording mechanical eligibility.
It does not complete semantic acceptance or release dependencies.

The controller owns policy validation, task/attempt state, prompt rendering,
Git inspection and verification. The internal transport owns process/session
mechanics. Workers edit only authorized task paths; they cannot commit, select
another task, edit controller records or broaden permissions. Keep the run
directory and active controller/skill installation outside worker-writable scope.

Run inputs and attempt artifacts bind policy, task identity, process/session,
effective permissions, Git baseline, results and diagnostics. Preserve prior
attempts when retrying. Missing results, process failure and an ambiguous/live
worker do not prove completion or authorize a new writer. Consult
`controller_state.py` and the JSON schemas for exact record/state contracts.

Flow/cursor validation, closed profiles, handoff/outcome envelopes and safe-boundary
`revise-flow` exist. Actor-level mappings and the 0.5 implementation-context reuse
threshold are currently fixed in `controller_state.py` and `flow-profile.schema.json`;
these are implementation constraints to investigate, not new owner requirements.
A profile or cursor record alone does not provide a runnable reviewed workflow.

## Verification containment

`verification_runner.py` currently requires macOS and the exact executable
`/usr/bin/sandbox-exec`. It builds argv directly, enforces configured filesystem
and network restrictions, and rejects unsupported configurations before launch;
there is no unrestricted fallback. The mechanism is deprecated and its profile
interface is private, so capability must be checked on the target host.

Writes are restricted by accessed pathname, not by inode. The operator must
supply writable roots without hard links that alias files outside those roots;
the runner does not scan for them. Canonical writable roots must be existing
absolute directories other than `/`. `danger-full-access` requires separate
explicit policy authorization, and approval policy must be `never`. Command
planning separately enforces dependency-install policy. Current containment does
not establish permissions or lifecycle support for a future harness adapter.

## Current limitations

The public controller does not yet provide safe stop/recovery, the complete
semantic review/correction loop, task commit finalization, atomic completion and
dependency release, automatic advance, or plan preparation. See the
[current development documents](../docs/README.md) for the desired behavior and
proposed delivery. Inspect current code and useful tests before extending it.
