# Maintainability tool: affected-file comparisons and highlights

Date: 2026-10-24

Implemented the small report-based flow: a skill captures a named folder
baseline, implementation changes code, and another skill compares affected
files against that baseline. The tool reports observations; agents decide
whether the code needs correction.

## Changes

- A comparison may select a subset of the baseline folders. New files inside
  those folders are supported. Baseline records outside the selected after
  scope are not treated as removals.
- Explicit deleted file paths preserved in the baseline are supported,
  including a comparison with no remaining Python files.
- JSON `highlights` replaces `required_response`. Rows carry factual labels:
  `got_worse`, `crossed_above_threshold`, `new_above_threshold`,
  `above_threshold`, `improved`, and `needs_interpretation`.
- Added and removed symbols remain separate facts. A removal no longer makes
  unrelated additions unmatched. Duplicate identities remain ambiguous; the
  tool does not infer rename or extraction relationships.
- Ruff comparisons match path, qualified symbol, and rule. Native counts in
  diagnostics are compared numerically when both reports contain them. For
  example, 7 arguments to 6 is an improvement, not a new diagnostic.
- Ruff remains threshold-only. Growth from 4 arguments to 5 is unavailable
  as comparison evidence. A newly appearing diagnostic has no numeric before
  value; a disappearing diagnostic needs interpretation because exemptions
  or source removal can also explain it.
- Console output shows highlights before legacy hotspots, including standalone
  Ruff findings and per-check errors. Exit 0 still means successful execution
  and compatible comparison, not maintainability acceptance.

Reports use format 3. Older reports are incompatible. Capture a new baseline
before editing, or remeasure preserved exact pre-edit source with the current
adapter. The launcher and pinned analyzer dependencies are unchanged.

The usage guide is updated at `scripts/measure-maintainability.md`. Skill
integration and installation remain a later task. Inspection of
`scripts/install_development_skills.py` confirmed that this tool is not part
of its managed shared-script set, so no installer change was needed.

## Verification

The new affected-file comparison test failed against the original code because
the folder baseline was rejected as incompatible. It passes after the change.
The owning suite passed all 19 tests, with real Radon 6.0.1 and Ruff 0.14.2 and
no skips:

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py -v
```

Existing cases were updated rather than duplicated. Evidence covers threshold
crossings, increases below the complexity target, unchanged debt, added and
removed symbols, duplicate identities, native Ruff counts and exemptions,
folder-to-file scope reduction, out-of-scope rejection, new files, deleted-only
CLI comparison, standalone findings, analyzer errors, portability, source
snapshots, and report overwrite protection.

## Tool self-check

Before edits, the original tool captured `tools` and `tests` in:

`.quality/reports/maintainability-highlights-before-original.json`

After the adapter changed, its exact preserved source bytes were restored into
a temporary folder and remeasured with the final adapter. This produced the
compatible baseline below; it did not use post-edit source as the before state.
The final command then selected only the affected files:

```sh
python3 scripts/measure_maintainability.py compare tools/maintainability.py tests/test_maintainability.py --baseline .quality/reports/maintainability-highlights-before.json --output .quality/reports/maintainability-highlights-after.json
```

Both measurements completed; comparison was compatible. It produced 22
highlight rows, including informational additions/removals and improvements.
The reports and their sibling text summaries are local ignored artifacts.

Selected numeric observations:

| Symbol | Before → after complexity | Assessment by the implementing agent |
|---|---:|---|
| `discover` | 16 → 18 | Retained two branches for accepting known deleted files while rejecting unknown missing scopes. |
| `run_ruff` | 9 → 11 | Retained native-count parsing and its explicit unsupported-message error near the diagnostic normalization. |
| `comparison` | 15 → 13 | One numeric comparison path now serves complexity and Ruff. |
| `summary_change` | 3 → 4 | One label choice supports both Radon and Ruff values. |
| `summarize` | 10 → 12 | Retained local iteration for highlights and individual check errors. |
| `build_report` | 9 → 12 | Retained baseline-file handling and folder-scope recording beside source capture. |
| `main` | 29 → 26 | Report highlight assembly moved to its owning helper; Ruff statements also fell from 57 to 53. |

`compare_values` replaces `compare_complexity`, both at complexity 11. The new
`numeric_change` helper (6) separates delta calculation from symbol matching;
`report_highlights` (9) replaces the previous response-summary assembly.
The renamed symbol relationships are described here rather than guessed by
the tool. No test function exceeds the complexity target; one existing native
Ruff test rose from 3 to 5 after adding assertions on reported numeric counts.

The retained increases implement distinct requested behavior in the existing
owners. Further splitting would add navigation for short local operations;
these numbers alone do not establish a design defect. This is implementation
self-check evidence, not an independent maintainability verdict. No thresholds
or exclusions were changed. Broader suites and live agent evaluations were not
needed for this standalone tool change.
