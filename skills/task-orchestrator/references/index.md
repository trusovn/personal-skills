# Task Orchestrator Current-Information Index

Status: operator reference

Freshness: 2026-10-22

Use the operator guide for existing behavior, the architecture map for code and
constraints, and the development index for intended changes.

| Need | Read | Avoid initially |
|---|---|---|
| Initialize, launch, or inspect a run | [operator-guide.md](operator-guide.md) | direct adapter commands |
| Understand authority and state | [architecture map](architecture-map.md#authority-and-existing-records) | unrelated modules |
| Modify controller behavior | [architecture-map.md](architecture-map.md), then the owning source and test | unrelated modules |
| Diagnose interruption or request recovery | [operator-guide.md](operator-guide.md#interruption-and-recovery) | direct `codex_worker.py resume` |
| Plan future work | [current development documents](../docs/README.md), starting with the confirmed direction | completed task paperwork |
| Construct current inputs | [minimal run policy](../assets/examples/minimal-run-policy.json), [minimal manifest](../assets/examples/minimal-task-manifest.json), then the schemas | hand-authored fields not in schemas |

Current public entry point:
`python3 scripts/controller.py {init,run-next,inspect,revise-flow}`.

Current limitation: the controller does not yet expose safe recovery, semantic
review/correction, atomic acceptance/release, automatic advance, or
plan-to-manifest preparation.
