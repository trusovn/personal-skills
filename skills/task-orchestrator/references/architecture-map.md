# Task Orchestrator Architecture Map

Status: operator reference

Freshness: 2026-07-23

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

## Current limitations

The current public surface does not provide safe stop/recovery, workflow
profiles, semantic review/correction, atomic acceptance/release, automatic
advance, or plan preparation. Their intended ownership is defined in the
current Stage 3 MVP rebaseline; historical stage briefs do not override it.
