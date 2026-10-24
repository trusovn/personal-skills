# Zero-limit collection update and self-check

Date: 2026-10-24

The runner now collects native Ruff argument and statement counts with zero-limit
command-line overrides. Advisory targets still come from `.quality/ruff.toml`:
5 arguments and 50 statements. The repository settings were not changed.

`tools/maintainability.py` now stores `collection_threshold` separately from
`target`. Matched counts produce numeric deltas below the targets, including
4 → 5 arguments and 20 → 25 statements. A newly appearing diagnostic requests
interpretation and receives `above_threshold` only if its count exceeds the
advisory target. A missing diagnostic never becomes numeric zero. Native
exemptions remain active; deltas stay unknown when either side lacks evidence.
Standalone output continues to highlight only counts above the advisory targets.

Reports now use format 4 and record `ruff_collection_limits` in comparison
identity. Older reports require a fresh baseline or remeasurement of exact
preserved source bytes with the current adapter. The usage guide was updated
in `scripts/measure-maintainability.md`.

## Behavioral verification

Command:

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B \
  -m unittest discover -s tests -p test_maintainability.py -v
```

Result: **22 tests passed, no skips**, using real Ruff 0.14.2 and Radon 6.0.1.
The statement comparison test first failed against the pre-update runner:
20 → 25 had no records, and 50 → 51 had an unknown before value. It passed after
the update. Existing cases were updated to reflect the additional native counts;
three new tests cover statement deltas, missing-evidence transitions, and
configured advisory targets.

Evidence includes:

- Argument and statement increases below target, advisory crossings, and decreases.
- Native `@override` and `@overload` exemptions; `noqa` remains ignored.
- Unknown-to-count and count-to-unknown transitions, including zero-argument
  and return-only functions; no invented numeric delta.
- New low counts requesting interpretation without a false above-target label.
- Duplicate identities remaining unmatched and standalone low counts staying
  out of highlights.
- Changed advisory settings remaining separate from zero collection thresholds.
- Old report formats and absent or changed collection identities being rejected.
- CLI output, saved reports, index preservation, incomplete measurements,
  compatible mount changes, and launcher behavior in the existing suite.

## Self-check with the updated tool

The updated CLI measured its own code and tests:
`tools/maintainability.py` and `tests/test_maintainability.py`.
Result: **measurement complete; comparison compatible**. Both analyzers completed:
51 complexity records and 70 native Ruff count records in the final files.

The before report is a **remeasurement**, not a baseline captured before editing.
It uses exact source bytes from the unchanged Git index. Both files had no
unstaged changes at the start of this update, so those staged bytes are the
pre-edit sources for this invocation. They were copied into a disposable root
and analyzed with the updated adapter. The comparison then analyzed the final
worktree files with the same adapter and settings. Source bytes and hashes are
preserved in the reports; an additional provenance file records the commands
and confirms that the real index did not change.

The comparison produced 21 highlights: 13 increases, 2 improvements, and 6
interpretation items. There were no crossings above an advisory target and no
new above-target functions. The interpretation items are the three new test
methods, each observed by complexity and statement count.

| Changed production function | Complexity before → after | Statements before → after | Judgment |
|---|---:|---:|---|
| `run_ruff` | 11 → 13 | 27 → 31 | Retained: reads advisory targets, adds collection overrides, and selects the target for each native rule. Complexity was already above 10. |
| `compare_values` | 11 → 12 | 19 → 20 | Retained: checks the advisory target before highlighting a newly observed count. Complexity was already above 10. |

The other increases belong to expanded test assertions and CLI evidence. Their
functions remain within the targets. The updated argument-delta test improved
from complexity 9 to 7 and statements 14 to 9 after removing the obsolete
below-target-unavailable branch. These improvements do not offset the production
increases; each increase was assessed on its purpose. No helper extraction or
threshold change was introduced to make the report appear clean.

Local reports are ignored by Git:

- `.quality/reports/ruff-zero-update-before.json` and sibling `.txt`:
  remeasured pre-edit staged sources.
- `.quality/reports/ruff-zero-update-after.json` and sibling `.txt`:
  final worktree comparison.
- `.quality/reports/ruff-zero-update-provenance.json`:
  source hashes, exact CLI commands, and index-preservation result.
- `.quality/reports/ruff-zero-update-self-check.py`:
  the disposable-snapshot and CLI procedure. Reports refuse overwrite; choose
  fresh output names before repeating it.

The installer was inspected. This standalone tool is not a development-profile
skill or managed shared script, so no installer or active skill refresh applies.
Existing staged changes were preserved, with this update left unstaged.
`git diff --check` passed as hygiene evidence. No full-repository scan, live
network check, cross-platform run, or independent review was performed.
