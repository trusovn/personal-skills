# Ruff zero-limit collection experiment

Date: 2026-10-24

Zero-limit collection is useful. It exposes native counts below the advisory
targets and detects both requested changes: 4 → 5 arguments and 20 → 25
statements. On the selected repository sample it adds 331 numeric observations.
It does not produce a complete inventory. Missing diagnostics must remain
unknown, and adopting this approach requires changes to the runner's diagnostic
classification as well as its Ruff invocation.

This experiment leaves the staged runner, tests, documentation, index, and
repository settings unchanged. It does not adopt new behavior or add an analyzer.
The advisory targets remain **50 statements / 5 arguments**. Increases are
observations for agent judgment; they are not automatic rejection criteria.

## Method

Used the existing native environment: Python 3.14.6, Ruff 0.14.2, macOS arm64.
Each run analyzed a disposable snapshot with the repository's explicit
`.quality/ruff.toml`, no fixes or cache, and `--ignore-noqa`. The zero-limit
variant added only these command-line overrides:

```sh
<environment>/bin/python -m ruff check \
  --config /absolute/path/to/personal-skills/.quality/ruff.toml \
  --config 'lint.pylint.max-args=0' \
  --config 'lint.pylint.max-statements=0' \
  --no-cache --no-fix --ignore-noqa --output-format json .
```

Run this from a snapshot containing the Python files to measure. For the
control, omit the two overrides. Ruff exit 1 means diagnostics were returned;
it is expected here. Exit codes other than 0 or 1 fail the probe.

Collection thresholds and advisory targets were kept separate in probe records:
`collection_threshold` comes from Ruff's diagnostic message; `target` is 5 for
PLR0913 or 50 for PLR0915. The current production adapter instead takes `target`
from the message. Passing zero limits to that adapter alone would set its
advisory targets to zero.

Fixtures exercised native exemptions and missing evidence before comparisons.
Then two versions of the same function used four/five named arguments and
20/25 assignment statements. The existing `compare_values` function received
the collected numeric records with the preserved advisory targets. Corpus
measurements used the staged `tools/maintainability.py` and the five Python files
in `skills/task-orchestrator/scripts`: 6 files, 194 function definitions.
Target code was parsed, never imported or executed.

## Below-target changes

| Metric | Default collection | Zero-limit before → after | Delta | Comparison highlight |
|---|---|---|---:|---|
| Arguments | No diagnostic on either side | 4 → 5 | +1 | `got_worse` |
| Statements | No diagnostic on either side | 20 → 25 | +5 | `got_worse` |

Both comparisons retained targets 5/50. Neither received
`crossed_above_threshold`, as neither exceeded its target. These results prove
the proposed collection benefit with real Ruff output and the existing matched
numeric comparison logic. They do not qualify a modified end-to-end runner.

## Exemptions and missing diagnostics

“Missing” below means **no numeric evidence**, not an inferred zero.

| Fixture | Arguments at zero limit | Statements at zero limit |
|---|---:|---:|
| `def zero(): pass` | Missing | 1 |
| `def variadic(*args, **kwargs): pass` | Missing | 1 |
| `def return_only(a): return a` | 1 | Missing |
| Function containing only a docstring | Missing | 1 |
| Function containing only `...`, `raise`, or `yield` | Missing | 1 each |
| `def dummy(_a, _b, c): pass` | 1 | 1 |
| Positional-only, ordinary, and keyword-only argument, one each | 3 | 1 |
| Six-argument function with `# noqa: PLR0913` | 6 | 1 |
| Six-argument `@overload` declaration with `...` | Missing | 1 |
| Corresponding `*args` implementation returning a value | Missing | Missing |
| Instance/class/static method with one counted argument | 1 each | 1 each |
| `@override` method with six named arguments plus `self`, 51 assignments | Missing | 51 |
| Six-argument abstract method or Protocol method with `...` | 6 each | 1 each |
| Nested async function with one argument and only a return | 1 | Missing |

Native counts differ from a naive AST count: dummy names and method receivers
are excluded in these argument fixtures; variadics do not supply a positive
argument count. The abstract and Protocol fixtures were not exempt from PLR0913
in this setup. Native `@override` and `@overload` exemptions remained active even
with zero limits and `--ignore-noqa`. The latter disables comment suppression,
not native exemptions. Return-only statement bodies also yielded no diagnostic.
These are observations for the pinned version and fixtures, not an exhaustive
definition of Ruff's counting rules.

A separate before/after fixture kept a six-argument method but added
`@override`: its argument record changed from 6 to missing. The current matcher
correctly left its numeric delta unknown and requested interpretation. In the
same fixture, changing its return-only body to assignment plus return produced
a statement record of 1 after a missing record. Its numeric delta also stayed
unknown. This directly exercises why absence must not become zero.

## Repository sample

| Metric | Function definitions | Default numeric records | Zero-limit records | Added records at or below advisory target | Still missing |
|---|---:|---:|---:|---:|---:|
| Arguments | 194 | 11 | 181 | 170 | 13 |
| Statements | 194 | 14 | 175 | 161 | 19 |

All 25 default counts remained present with identical values under zero-limit
collection. Numeric coverage rose to 93.3% for arguments and 90.2% for statements
in this sample. These percentages describe single-snapshot collection, not
before/after match coverage or other repositories. The 19 missing statement
records include return wrappers such as `digest`, `capture`, and `symbol_key`
in the tool itself.

The final sample runs took about 29 ms at default limits and 34 ms at zero limits,
excluding snapshot creation and report processing. These single local timings
are observations, not a performance benchmark. Diagnostic volume rose from
25 to 356, so collecting all counts should not mean printing every diagnostic
as an advisory hotspot.

## Adoption recommendation

Proceed with a bounded adapter change as a separate task. Keep these distinctions:

1. Collect using zero-limit CLI overrides. Preserve native counts and raw
   messages, but store collection limits separately from advisory targets.
2. Compute deltas only when both sides have unambiguous numeric evidence.
   Preserve unknowns for absent diagnostics, exemptions, analyzer failures,
   and ambiguous symbol matches. An AST symbol inventory may identify missing
   evidence without implementing a second counting formula.
3. Update threshold-only classifications. The probe exposed a concrete mismatch:
   the current matcher labels a newly observed statement count of **1**, with
   advisory target **50**, `new_diagnostic` / `above_threshold`. That assumption
   is valid for target-filtered diagnostics and false for zero-limit collection.
   A new low count needs interpretation, without an above-target claim.
4. Print matched increases and actual target breaches, rather than all collected
   diagnostics. Keep agent judgment responsible for whether an increase is
   reasonable. Update report limitations and comparison identity so older
   target-filtered baselines cannot masquerade as zero-limit measurements.

The experiment closes much of the numeric evidence gap without another analyzer.
It does not justify treating Ruff as a complete statement/argument inventory or
silently upgrading missing values to zero.

## Verification and local artifacts

The assertion-backed probe passed against real Ruff: subtarget before/after
counts and highlights, native override exemption, ignored `noqa`, missing
argument/return-only evidence, missing-evidence transitions, and preservation
of every default corpus count. It also reproduced the current new-low-count
highlight mismatch described above.

Local evidence is in the ignored directory
`.quality/reports/ruff-zero-collection-20261024/`:

- `probe.py`: fixture generation, disposable snapshots, assertions, and report
  generation. Run from the repository root with the pinned environment.
- `results.json`: exact commands, raw diagnostics, fixture and corpus inventory,
  source snapshots and SHA-256 hashes, settings, transitions, and timings.

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B \
  .quality/reports/ruff-zero-collection-20261024/probe.py
```

This command regenerates the local report from current source. The saved report
preserves the bytes used for this run. These ignored artifacts do not transfer
with a commit; this document contains the findings and the collection command.
The probe's first attempt needed temporary-path canonicalization on macOS; a
later exploratory assertion was corrected after Ruff counted a docstring-only
body as 1. Both corrections are confined to the probe.

No production code changed, so the existing tool suite was not rerun. No live
network checks, full-repository scan, independent review, or cross-platform
qualification was performed. Final `git diff --check` is hygiene evidence only.
