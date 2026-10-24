# Development

## Setup and scope

Use Python 3 and Git. The foundation was exercised with Python 3.14.6 and Git
2.54.0; minimum versions and a full host support matrix remain unqualified.
The existing optional analyzer launcher explicitly requires Python 3.11 or later.
There is no application build or server to start.

The default local checks use the standard library and disposable filesystem/Git
fixtures. They use fake Codex executables and mocked Ollama responses. No
provider account is needed. See the [project map](project-map.md) for placement
and the [contract index](contracts/index.json) for implemented reusable surfaces.

| Tier | Prerequisites and limits |
|---|---|
| Default local verification | Python and Git available in `PATH`; permission to create temporary directories, local child processes, and disposable Git repositories. |
| Real containment tests | macOS and `/usr/bin/sandbox-exec`, with host permission to run it. Unsupported hosts report skips; execution denial on a supported host is a failure, not a skip. Loopback fixtures do not contact external services. |
| Skill frontmatter/package validation | Optional PyYAML, imported by `skills/skill-creator/scripts/quick_validate.py`; separate from behavioral tests. |
| Analyzer evidence | Pinned Radon/Ruff environment under the selected target; installation pins are `scripts/maintainability-requirements.txt` (installed under `.agents/scripts/`). See [analyzer setup](../scripts/measure-maintainability.md). Tests requiring real tools report skips when absent. |
| Live model evals/qualification | Explicit approval for the selected check, runtime/provider authentication and supported configuration. Excluded from the default gate. |

For optional frontmatter validation, use a separate virtual environment and
install PyYAML there, then invoke the source validator:

```sh
python3 -m venv /tmp/personal-skills-validation
/tmp/personal-skills-validation/bin/python -m pip install PyYAML
/tmp/personal-skills-validation/bin/python skills/skill-creator/scripts/quick_validate.py skills/task-orchestrator
```

This is an optional setup recipe, not a qualified dependency lock. Review
dependency updates deliberately. The aggregate gate never downloads or installs
packages and does not select or repair an analyzer environment automatically.

## Verification commands

```sh
# Focus on the owning root or module first; root tests use local helper imports.
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_state.py

# All maintained local suites, architecture policy, registry, and profile drift.
python3 tools/verify.py
```

`tools/verify.py` finds directories containing `test_*.py` under root `tests/`
and source `skills/`, excluding `fixtures/`, `evals/`, and bytecode directories.
Each directory is an independent `unittest` discovery process so local test
helper imports and duplicate module names do not collide. Current roots are
`tests/`, orchestrator tests, skill-creator tests, and task-brief-designer tests.
Use this directory convention for new maintained suites; eval fixtures are not
automatically executed. Keep nested discovery roots separate rather than adding
package markers that cause duplicate recursive discovery.

The command prints every invocation, unittest's skipped cases and reasons, and
an aggregate failure count. It returns nonzero if any check fails. Empty test
scope is an error. A passing run with skips proves only the checks that ran.
The architecture policy is part of the root suite. The contract check runs
separately. If `.agents/skills/` exists, a read-only profile drift check runs;
an incomplete installed profile fails that check. Without that directory, drift
checking is explicitly skipped. Neither case refreshes installed skills.

For stronger analyzer evidence, first use the documented setup command, then
invoke `tools/verify.py` with the native environment's Python printed by setup.
Do not add live providers to the default gate. Behavioral eval execution also
requires scenario setup and grading; metadata or an execution exit code alone
does not prove skill quality.

## Architecture policy

Canonical command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
```

Mode: **CLEAN**, no baseline. The executable policy is
`tests/test_architecture.py`. It checks declared static imports and literal
dynamic loads in root runtime scripts/tools and skill-owned runtime scripts:

- Runtime code does not import test-only modules or fixture support.
- Shared runtime does not import skill packages.
- Existing orchestrator dependencies follow the explicit sibling allow-list:
  controller composes the modules, Git/verification may use state, and state
  and transport do not depend on controller or each other.

This is a narrow source check, not a Python dependency resolver. Computed loads,
filesystem paths, transitive dependencies, permissions, and semantic ownership
still need review. No baseline exceptions or automatic baseline refresh exist.
Complexity/size measurements remain advisory. No new mandatory semantic-review
stage is imposed by this command; existing task/repository review requirements
still apply.

## Contract discovery maintenance

Edit `docs/contracts/<subsystem>.json` when an implemented reusable surface or
its authority changes. Keep records sparse and do not register planned features.
Then run:

```sh
python3 tools/check_contracts.py --root . --write-index
python3 tools/check_contracts.py --root .
```

The validator was copied from the active project-local repo-foundation package.
`tools/check_contracts.py` is this repository's standalone validator; it has no
installed-skill dependency. It checks the core v1 shape, local paths, subsystem
references, and generated-index agreement. These are structural checks, not
semantic acceptance of the described runtime. Records omit plan IDs where
today's revised plan does not match the older implemented capability. The
measurement record maps T-001.1's implemented surfaces to their plan IDs and
explicitly identifies the remaining IF-001 work.

## AI boundary diagnostics

Orchestrator attempts retain process/thread identity, events, stderr, state and
structured result paths in the controller-owned external run directory. Start
with the [operator guide](../skills/task-orchestrator/references/operator-guide.md);
an absent result or ambiguous process does not authorize another writer.
Delegation returns bounded tool metadata, configured model/endpoint and duration.
Configured model names are not observed identity. Treat captured prompts/events
as repository content and inspect them before sharing; automatic redaction is
not established. Recovery, automatic retries and complete semantic acceptance
remain feature work. See [AI foundation](ai-foundation.md) for boundary decisions.
