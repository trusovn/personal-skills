# Local Python maintainability experiment

The entry point is `python3 scripts/measure_maintainability.py`. It measures
Python source without importing or executing it. This is a standalone
measurement runtime included in the development installation profile. Its metrics
are advisory and do not change CI or acceptance rules. The design context is in
[`docs/advisory-code-maintainability-signals.md`](../docs/advisory-code-maintainability-signals.md).

## Setup

Use Python 3.11 or later. Select the same target for setup and measurement:

```sh
python3 scripts/measure_maintainability.py setup --root /path/to/target
```

Run setup once in each host or sandbox environment. It creates an environment in
the selected target's `.quality/envs/`, keyed by OS, CPU architecture, Python
implementation and full version, and the pinned requirements hash. macOS and Linux therefore use their
own binaries even when they share the repository. Python with `venv`/`pip` and
Git must be installed in each environment. Setup needs package-index access (or
an offline wheel directory configured through pip). Run one setup at a time per
environment; rerun it to repair an interrupted install.

The launcher selects that native environment, or uses the invoking interpreter
if all pinned dependencies are already installed. It ignores the legacy
`.quality/venv` directory; existing environments may still be invoked explicitly.
Measurement never installs packages. Missing or incorrect dependencies produce
an error with the setup command. Environments and local reports are ignored by
Git. Dependencies are pinned, including Radon's transitive dependencies.
The initial versions are Radon 6.0.1 and Ruff 0.14.2. This setup provisions Python
analyzers only; future language tools can keep their own native runtimes separate
from the shared report directory.

## Installed resources and target policy

Source `scripts/` and installed `.agents/scripts/` contain the same flat runtime:

| Resource | Role |
|---|---|
| `measure_maintainability.py` | Stable public launcher |
| `maintainability_env.py` | Native interpreter selection and explicit setup |
| `maintainability.py` | Measurement adapter |
| `maintainability-default.toml` | Fallback for target `.quality/maintainability.toml` |
| `maintainability-ruff-default.toml` | Fallback for target `.quality/ruff.toml` |
| `maintainability-requirements.txt` | Installation-owned analyzer pins |

Each settings file is selected independently from the target when present, or
from its corresponding shipped default when absent. Invalid present settings
fail visibly. Unrelated root Ruff configuration is ignored. Reports record
effective settings contents, SHA-256 identities, paths and target/shipped origins.
Paths and origins are provenance; effective contents decide compatibility.
The source repository's `.quality/` settings remain its deliberate target policy;
its requirements file cannot select installed packages. Setup uses only the
installation's `maintainability-requirements.txt`.

The helpers moved from `tools/maintainability.py` and
`tools/maintainability_env.py` to `scripts/`. No repo-only or global fallback
exists. In a target repository, use the installed public launcher:

```sh
python3 /path/to/target/.agents/scripts/measure_maintainability.py setup --root /path/to/target
python3 /path/to/target/.agents/scripts/measure_maintainability.py measure . --root /path/to/target
```

Installer refresh manages only declared runtime resources. It preserves target
policy, environments, saved JSON/text reports and unmanaged helpers.

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

Scope, `--output`, and `--baseline` paths are relative to `--root`, which defaults
to the current working directory.
Absolute paths inside that root also work. To measure a different repository,
run this launcher's absolute path with `--root /path/to/repo`. Files must end in
`.py`; an empty or missing scope is an error, except when comparing deleted files preserved in the
baseline. Symlinks are not followed. Explicit excluded scopes
are rejected; excluded directories encountered during traversal are recorded.
Folders are appropriate for a baseline: they also capture functions or files
added later. Include deleted file paths in the after scope to report removals.

## Capture before and compare after

```sh
# Before editing. Do not capture a baseline after the change and call it "before".
python3 scripts/measure_maintainability.py baseline scripts tests --output .quality/reports/before-01.json

# After editing, compare only the affected files within those baseline folders.
python3 scripts/measure_maintainability.py compare scripts/run_evidence.py tests/test_run_evidence.py --baseline .quality/reports/before-01.json --output .quality/reports/after-01.json
```

`measure` and `compare` print the summary to the console by default. Use
`--output` to also save JSON and text reports. `baseline` requires `--output`
because later comparisons need the saved measurement.
Pass that report filename to the next skill. The after scope may be the same
scope or a subset; new files must be under a baseline folder. Baseline records
outside the after scope are not compared or reported as removals. Checks,
tools, and settings must still match.

Each saved report needs a new output path. The runner refuses to overwrite
reports or their sibling `.txt` summaries. A baseline preserves actual worktree
bytes, including relevant untracked files. It does not reset, stash, stage, or
refresh the real index. It cannot reconstruct a missing pre-edit baseline.

## Share reports between host and sandbox

Store reports in the measured repository's `.quality/reports/`, as above. When
the sandbox mounts that repository, both sides see the same JSON and text files,
even if their absolute repository paths differ. Give each run a distinct filename
(for example, a task ID plus `before`/`after` and a run ID). Pass the relative JSON
path to the next agent; there is no mutable "latest" report to confuse runs.
Neither analyzer binaries nor virtual environments need to be shared.

For a separate clone, copy the report files back into the receiving repository's
`.quality/reports/` before comparison. Reports are ignored by Git, so commits do
not transfer them. A local folder cannot synchronize isolated filesystems.
Keep write permissions usable by both environments when sharing a mount.

Comparisons allow different absolute roots, operating systems, architectures,
and Python patch versions. They still require the same Python implementation
and major/minor version, analyzer versions, adapter, and settings, with the
current relative scope covered by the baseline.
The caller must select a baseline from the same logical project; a matching
scope alone cannot establish project identity. Full root and Python version
remain recorded as provenance. Reports now use format 4, with explicit Ruff
collection limits and separate advisory targets. Older reports cannot
serve as format 4 baselines. Capture a new baseline before edits, or remeasure
exact pre-edit source bytes preserved in an older report with the current tool.

Exit **0** means the selected measurements completed and any requested
comparison was compatible. Highlights are observations for agent judgment,
not a quality verdict. Exit
**2** means invalid input, incomplete measurement, analyzer failure, or an
incompatible comparison. Check `full_profile` before treating a subset as the
default profile. No hard architecture or correctness gate is run.

## What is measured

| Check ID | Tool and result | Provisional target | Comparison |
|---|---|---|---|
| `complexity` | Radon score for each named function, async function, method, and nested function, including local-class methods | 10 | Full before/after inventory, including scores below target |
| `ruff` | Native `PLR0915` and `PLR0913` counts collected with zero-limit CLI overrides | 50 statements / 5 arguments | Numeric deltas, including below target, when both sides have a diagnostic; missing values remain unknown |

The Radon adapter visits each function AST with `cc_visit_ast`. It does not
implement its own complexity formula or include class aggregate scores.
Ruff uses `.quality/ruff.toml` explicitly, with no inherited repository config,
fixes, cache, Git-ignore filtering, or `noqa` suppression. Native rule exemptions
still apply; for example, Ruff exempts `@override` methods from `PLR0913`.
The runner overrides `lint.pylint.max-args` and `lint.pylint.max-statements` to
zero on the command line to collect counts below the advisory targets. The
targets still come from `.quality/ruff.toml`; that file is not rewritten.
Ruff analyzes a temporary snapshot containing exactly the captured Python files.
Radon analyzes the captured bytes. Neither executes target project code.

[Radon's API](https://radon.readthedocs.io/en/latest/api.html),
[Ruff configuration](https://docs.astral.sh/ruff/configuration/), and
[PLR0913](https://docs.astral.sh/ruff/rules/too-many-arguments/) describe the
native semantics. The local tests exercise these pinned tools with real input.

`.quality/maintainability.toml` owns scope exclusions, the default profile, and
the Radon target. `.quality/ruff.toml` owns Ruff rules and advisory targets. The experiment
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
  adapter hash, baseline folder scopes, native settings, and `ruff_collection_limits`. Compatibility
  ignores the absolute root and Python patch version, and permits a narrower
  after scope; other measurement-setting differences prevent comparison.
- `repository` and `files`: Git context, source hashes, asset groups, and exact
  source bytes encoded as base64. Reports are self-contained local observations.
- `checks.complexity.values`: qualified symbols, locations, values, and targets.
  `checks.ruff.values` contains native diagnostic messages, locations, reported
  counts, collection thresholds, and advisory targets. A message such as
  `(4 > 0)` describes collection; the record's `target` remains 5 arguments.
  It is not a complete numeric inventory. No diagnostic means no numeric record,
  not an inferred zero.
- `comparison`: compatible per-function deltas and diagnostic changes.
- `highlights`: rows with factual labels, also printed before legacy hotspots.
  A measurement or baseline alone highlights values above target. A compatible
  comparison adds change highlights. No highlight is an automatic rejection.

| Highlight | Meaning |
|---|---|
| `got_worse` | A matched numeric value increased, including below target |
| `crossed_above_threshold` | A matched value moved from within target to above it; also marked `got_worse` |
| `new_above_threshold` | A new complexity symbol exceeds the target |
| `above_threshold` | A standalone hotspot or a newly appearing Ruff count above its advisory target |
| `improved` | A matched numeric value decreased |
| `needs_interpretation` | A symbol was added, removed, or ambiguous, or a Ruff diagnostic appeared or disappeared |

Complexity decreases cannot offset increases elsewhere. Unchanged legacy
hotspots remain in the inventory without creating a change highlight. Symbol
identity uses path, qualified name, and metric, never line number. Added and
removed symbols are reported separately; duplicate identities remain unmatched.
The tool does not guess move, rename, or extraction relationships.
Ruff matching uses symbol and rule rather than diagnostic message, so a change
from 7 arguments to 6 is an improvement. A newly appearing diagnostic has no
known numeric before value. A disappearing diagnostic may reflect an exemption
or removal, so it is not claimed as a numeric improvement. Both transitions
request interpretation; a newly appearing diagnostic is only labeled
`above_threshold` when its count exceeds the advisory target. Native exemptions,
zero counted arguments, and return-only bodies can leave gaps even with zero
collection limits. Absence is never converted to zero. Ruff cannot prove a
complete statement/argument regression policy. Changes during scanning mark the
report incomplete. Measurements collected before a failure remain visible.

Keep explanations and reviewer decisions in separate task/review artifacts
that refer to the report path, symbol, and metric/rule. This experiment does not
accept exceptions, provide move mappings, or orchestrate reviewers. Targets are
provisional; calibration and semantic review remain human/agent work. Coverage,
CRAP, cognitive complexity, and dependency rules are outside this experiment.

## Verify the tooling

```sh
# Use the native environment path printed by setup.
<environment>/bin/python -B -m unittest discover -s tests -p test_maintainability.py -v
```

These tests run real Radon/Ruff measurements and the launcher against disposable
source and Git repositories. They cover threshold boundaries, increases below
target, unchanged debt, independent improvements, nested and ambiguous symbols,
native Ruff exemptions, dirty snapshots/index preservation, partial completion,
input changes, incompatible baselines, and output preservation. Missing tools
are simulated at the package-discovery boundary; other analyzers still run.
Without the tools, the analyzer tests explicitly skip rather than simulate
successful measurements.
Portability cases cover foreign legacy environments, native environment keys,
offline missing-tool failure, and a saved baseline transferred between checkout
paths. These local tests do not replace a live Linux sandbox run.
Additional cases cover folder baselines with affected-file comparisons, new and
deleted files, factual highlights, native Ruff count changes, and console
findings/errors without JSON inspection. Zero-limit cases exercise below-target
increases, advisory crossings, configured targets, native override/overload
exemptions, missing-evidence transitions, and rejection of older collection identities.
