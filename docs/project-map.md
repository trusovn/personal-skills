# Project map

Verified against the working tree: 2026-10-24.

| Location | Ownership and nearest precedent |
|---|---|
| `skills/<name>/` | Complete skill-owned package: instructions, scripts, references, eval inputs, and local tests. Start at its `SKILL.md`. |
| `skills/task-implementation-flow/` | Nested bounded-task skills; its README owns call-order guidance. |
| `skills/task-orchestrator/` | Current runtime work. Use its [module map](../skills/task-orchestrator/references/architecture-map.md) for source/test ownership and [operator guide](../skills/task-orchestrator/references/operator-guide.md) for supported commands. |
| `scripts/` | Existing shared runtime/installer CLIs. `install_development_skills.py` owns distribution; `run_evidence.py` shows shared dependency resolution. Keep public paths stable. |
| `tools/` | Repository development utilities. `verify.py` composes checks; `check_contracts.py` validates contract discovery. These are not development-profile runtime dependencies. |
| `tests/` | Shared-tool and cross-skill tests; `staging_fixture_support.py` owns reusable repository-only setup. Skill eval setup remains self-contained. |
| `docs/contracts/` | [Generated index](contracts/index.json) routes to implemented reusable contracts and their code/schema/test authorities. Edit subsystem records, regenerate the index. |
| Other `docs/` | Foundation and bounded work results. Existing plans express intended state; historical records do not establish current capability. |
| `.agents/` | Ignored installed skills/helpers. Resolve separately from editable source; never refresh the active installation during a run. |
| `.quality/` | Optional analyzer settings, pinned requirements, native environments, and local reports. Metrics remain advisory. |

## Canonical checks

Run from the repository root unless a command supplies a root explicitly.

```sh
python3 tools/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
python3 scripts/install_development_skills.py --check .
```

Use the owning suite first, then the aggregate gate for cross-cutting changes.
See [development setup and test tiers](development.md). There is no separate
build, mandatory formatter, lint/typecheck gate, server, or migration command.

Keep new single-skill resources inside their skill. Follow existing shared
runtime paths; place new repo-only utilities in `tools/`. Add shared abstractions
only for concrete consumers. Contract registries route discovery; they do not
replace executable authority or imply future interfaces are implemented.
