# Local Python maintainability experiment

The entry point is `python3 scripts/measure_maintainability.py`. It measures
Python source without importing or executing it. This is a standalone
experiment: it does not change skills, installation profiles, CI, or acceptance
rules. The design context is in
[`docs/advisory-code-maintainability-signals.md`](../docs/advisory-code-maintainability-signals.md).

## Setup

Use Python 3.11 or later. From this repository:

```sh
python3 -m venv .quality/venv
.quality/venv/bin/python -m pip install -r .quality/requirements.txt
```

The launcher automatically uses `.quality/venv` when it exists. It never installs
dependencies during measurement. The environment and local reports are ignored
by Git. Dependencies are pinned, including Radon's transitive dependencies.
The initial versions are Radon 6.0.1 and Ruff 0.14.2.

## Measure a folder or files

```sh
# Print to the console without saving reports.
python3 scripts/measure_maintainability.py measure scripts tests

# All Python source in the current repository, including tests and evals.
python3 scripts/measure_maintainability.py measure . --output .quality/reports/scan-01.json

# Selected files and folders; the script expands folders recursively.
python3 scripts/measure_maintainability.py measure scripts/run_evidence.py tests --output .quality/reports/focused-01.json

# Complexity only: explicitly a partial profile.
python3 scripts/measure_maintainability.py measure scripts --checks complexity --output .quality/reports/complexity-01.json
```

Paths are relative to `--root`, which defaults to the current working directory.
Absolute paths inside that root also work. To measure a different repository,
run this launcher's absolute path with `--root /path/to/repo`. The settings and
tools still come from this installation. Files must end in `.py`; an empty or
missing scope is an error. Symlinks are not followed. Explicit excluded scopes
are rejected; excluded directories encountered during traversal are recorded.
Folders are appropriate for a baseline: they also capture functions or files
added later. With explicit file paths, keep those paths present for comparison.

## Capture before and compare after

```sh
# Before editing. Do not capture a baseline after the change and call it "before".
python3 scripts/measure_maintainability.py baseline scripts tests --output .quality/reports/before-01.json

# After editing, using the same roots, checks, tools, and settings.
python3 scripts/measure_maintainability.py compare scripts tests --baseline .quality/reports/before-01.json --output .quality/reports/after-01.json
```

`measure` and `compare` print the summary to the console by default. Use
`--output` to also save JSON and text reports. `baseline` requires `--output`
because later comparisons need the saved measurement.

Each saved report needs a new output path. The runner refuses to overwrite
reports or their sibling `.txt` summaries. A baseline preserves actual worktree
bytes, including relevant untracked files. It does not reset, stash, stage, or
refresh the real index. It cannot reconstruct a missing pre-edit baseline.

Exit **0** means the selected measurements completed and any requested
comparison was compatible. Advisory findings can still require action. Exit
**2** means invalid input, incomplete measurement, analyzer failure, or an
incompatible comparison. Check `full_profile` before treating a subset as the
default profile. No hard architecture or correctness gate is run.

## What is measured

| Check ID | Tool and result | Provisional target | Comparison |
|---|---|---|---|
| `complexity` | Radon score for each named function, async function, method, and nested function, including local-class methods | 10 | Full before/after inventory, including scores below target |
| `ruff` | Native `PLR0915` and `PLR0913` diagnostics | 50 statements / 5 arguments | Supplementary target diagnostics only; below-target no-increase comparison is unavailable |

The Radon adapter visits each function AST with `cc_visit_ast`. It does not
implement its own complexity formula or include class aggregate scores.
Ruff uses `.quality/ruff.toml` explicitly, with no inherited repository config,
fixes, cache, Git-ignore filtering, or `noqa` suppression. Native rule exemptions
still apply; for example, Ruff exempts `@override` methods from `PLR0913`.
Ruff analyzes a temporary snapshot containing exactly the captured Python files.
Radon analyzes the captured bytes. Neither executes target project code.

[Radon's API](https://radon.readthedocs.io/en/latest/api.html),
[Ruff configuration](https://docs.astral.sh/ruff/configuration/), and
[PLR0913](https://docs.astral.sh/ruff/rules/too-many-arguments/) describe the
native semantics. The local tests exercise these pinned tools with real input.

`.quality/maintainability.toml` owns scope exclusions, the default profile, and
the Radon target. `.quality/ruff.toml` owns Ruff rules and limits. The experiment
includes implementation, tests, evals, fixture generators, and harnesses;
asset groups are reported separately. It excludes installed `.agents/` copies,
local environments and reports, caches, and common generated/vendor folders.
These directory-name exclusions apply at every depth and are recorded in JSON.
There are no test or harness target exceptions in this experiment.

## Read the output

With `--output`, a run writes JSON and a short sibling `.txt` summary. The JSON contains:

- `measurement_status`, individual check status, versions, errors, raw Ruff
  output and command, and the Radon API identity.
- `identity`: exact root/scope, selected checks, interpreter/tool versions,
  adapter hash, and native settings. Different identities prevent comparison.
- `repository` and `files`: Git context, source hashes, asset groups, and exact
  source bytes encoded as base64. Reports are self-contained local observations.
- `checks.complexity.values`: qualified symbols, locations, values, and targets.
  `checks.ruff.values` contains native diagnostic messages and locations, not a
  fabricated numeric inventory.
- `comparison`: compatible per-function deltas and diagnostic changes.
- `required_response`: complexity increases, new complexity breaches, new Ruff
  diagnostics, and unmatched symbol relationships that need review. This list
  is evaluated only for a compatible comparison. A measurement or baseline
  alone reports hotspots; an empty response list in such a run is not a pass.

Complexity decreases cannot offset increases elsewhere. Unchanged legacy
hotspots remain in the inventory without creating a new response item. Symbol
identity uses path and qualified name, never line number. Missing or duplicate
symbols remain unmatched. If old symbols disappear, new ones are conservatively
unmatched too; the tool does not guess move, rename, or extraction relationships.
Ruff diagnostic matching also includes symbol and message; it cannot prove a
complete statement/argument regression policy. Changes during scanning mark the
report incomplete. Measurements collected before a failure remain visible.

Keep explanations and reviewer decisions in separate task/review artifacts
that refer to the report path, symbol, and metric/rule. This experiment does not
accept exceptions, provide move mappings, or orchestrate reviewers. Targets are
provisional; calibration and semantic review remain human/agent work. Coverage,
CRAP, cognitive complexity, and dependency rules are outside this experiment.

## Verify the tooling

```sh
.quality/venv/bin/python -B -m unittest discover -s tests -p test_maintainability.py -v
```

These tests run real Radon/Ruff measurements and the launcher against disposable
source and Git repositories. They cover threshold boundaries, increases below
target, unchanged debt, independent improvements, nested and ambiguous symbols,
native Ruff exemptions, dirty snapshots/index preservation, partial completion,
input changes, incompatible baselines, and output preservation. Missing tools
are simulated at the package-discovery boundary; other analyzers still run.
Without the tools, the analyzer tests explicitly skip rather than simulate
successful measurements.
