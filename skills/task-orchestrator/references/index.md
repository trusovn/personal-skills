# Task Orchestrator Current-Information Index

Status: operator reference

Freshness: 2026-07-23

Use current references first. Treat `docs/history/` as opt-in implementation
evidence, never as ordinary operating authority.

| Need | Read | Avoid initially |
|---|---|---|
| Initialize, launch, or inspect a run | [operator-guide.md](operator-guide.md) | `docs/history/` and direct adapter commands |
| Understand authority and state | [controller contract](../docs/controller-contract.md) | old stage contracts |
| Modify controller behavior | [architecture-map.md](architecture-map.md), then the owning source and test | unrelated modules |
| Diagnose interruption or request recovery | [operator-guide.md](operator-guide.md#interruption-and-recovery) | direct `codex_worker.py resume` |
| Understand remaining MVP work | [Stage 3 MVP rebaseline](../docs/stage-3-mvp-rebaseline.md) and [retrieval follow-up](../docs/stage-3-retrieval-surface-follow-up.md) | completed task briefs |
| Construct current inputs | [minimal run policy](../assets/examples/minimal-run-policy.json), [minimal manifest](../assets/examples/minimal-task-manifest.json), then the schemas | hand-authored fields not in schemas |

Current public entry point:
`python3 scripts/controller.py {init,run-next,inspect}`.

Current limitation: the controller does not yet expose safe recovery, semantic
review/correction, atomic acceptance/release, automatic advance, or
plan-to-manifest preparation.
