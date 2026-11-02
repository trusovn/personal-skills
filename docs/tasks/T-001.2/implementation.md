# T-001.2 implementation handoff

Format 5 reports describe numeric changes as `increased` or `decreased`.
The CLI can capture an explicitly selected existing empty folder as a baseline,
then compare files added within that coverage without inventing numeric before
values. Older formats are incompatible. The measurement guide explains safe
pre-edit recovery and fresh report names.

Submission status: **READY_FOR_REVIEW**, not acceptance. The later
[acceptance decision](reviews/acceptance-01.md) is **CHANGES_REQUESTED**:
independent behavioral evidence was admitted, while this handoff, independent
maintainability review, and registry synchronization were missing. This record
supplies the original implementer's available history; it does not resolve
F-01 or claim to perform the missing review.

## Authority and deliverables

- [Brief](brief.md), [verification design](verification.md) revision 1 and
  [ready preflight](preflight.md); dependency: accepted T-001.1.
- `scripts/maintainability.py`: format 5, neutral classifications and highlights,
  and empty capture limited to explicitly selected existing directories.
- `tests/test_maintainability.py`: real-analyzer, CLI, filesystem and Git
  coverage for changed reporting, compatibility, capture and preservation.
- `scripts/measure-maintainability.md`: format transition, empty coverage and
  safe recovery guidance. Installer selections and profile/README references
  were inspected; resource membership and names did not change.

Actual contract impact: ART-001/IF-001's versioned report and the tool portion
of ART-002's empty-start capture changed. The executable contract declaration
is `scripts/maintainability.py`. The current measurement registry remains stale
(F-01); the designated registry updater owns its correction and index review.
No installed composition or later workflow behavior is claimed here.

## Implementer verification

Pinned interpreter `P` was
`.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`.
The following commands ran from the repository root:

- Before changing the adapter, `P -B -m unittest discover -s tests -p
  test_maintainability.py -k test_real_complexity_boundaries_and_below_target_increase`
  failed one assertion: the updated expected highlight `increased` was
  `got_worse`. This is the recorded fail-first evidence for the label change.
- Focused empty-folder, dirty Git snapshot, saved/console label, changed-settings,
  and report-collision tests passed after their changes.
- `P -B -m unittest discover -s tests -p test_maintainability.py` passed
  32 tests, no skips, on the final implementation submission.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`
  passed 4 tests; `python3 tools/check_contracts.py --root .` passed for 6
  subsystems and 7 indexed references; `git diff --check` passed. These are
  structural checks and do not prove semantic registry freshness.
- `python3 tools/verify.py` was not run: the brief assigns final aggregate
  composition proof to T-001.3. No network or dependency installation ran.
- Optional run-evidence availability returned unavailable because the sandbox
  could not write Git metadata. No evidence lifecycle run was created.

## Scenario-to-evidence map

The owning suite command above runs the named tests with real pinned Radon and
Ruff. These are implementer execution claims, not independent acceptance.
The separate [discovery report](reviews/discovery-01.md) records its own
commands and setup; the acceptance decision admits its V-01–V-10 behavioral
coverage. The grouped IDs below retain every identity in verification revision 1.

| Scenario IDs | Implementer setup and observable evidence |
|---|---|
| V-01a–e, V-01q | Real complexity source pairs in `test_real_complexity_boundaries_and_below_target_increase` and `test_complexity_numeric_boundaries`: native before/current counts, signed deltas, neutral labels and crossing highlights. |
| V-01f–j | Real statement-count pairs in `test_ruff_statement_changes_keep_advisory_targets`: counts, signed delta and threshold highlights. |
| V-01k–p | Real argument-count pairs in `test_ruff_native_counts_distinguish_improvement_and_worsening`: counts, classifications and threshold highlights. |
| V-02a–e | New hotspot, removed and renamed/extracted symbols, duplicate names, and shifted nested/local-class/async functions in the complexity, symbol, nested-scope and output tests; unknown deltas and interpretation are retained. |
| V-03a–i | Real Ruff diagnostic transitions in both directions, override/overload exemptions, and identical messages on distinct symbols in the native diagnostic and missing-diagnostic tests; missing counts stay unknown. |
| V-04 | `test_saved_and_console_reports_use_neutral_labels` and console/standalone tests exercise public CLI, saved JSON/text, console, neutral labels, hotspots and successful exits. The fail-first command above establishes sensitivity to the old label. |
| V-05a–j | Compatible and incompatible controls in compatibility, settings, transferred-root and empty-scope tests; CLI rejects old format and changed identities/settings, while comparisons retain original evidence. |
| V-06 | `test_empty_folder_baseline_preserves_absence_across_edits`: explicit empty folder, two edits and fresh comparisons against the original report, including source/index and report preservation. |
| V-07a–d | Empty-folder and exclusion tests: ordinary empty measure, missing or excluded parent, and uncovered addition fail; empty baseline is the success control. |
| V-08 | `test_snapshot_preserves_staged_unstaged_untracked_and_index` and folder subset test: staged/unstaged/untracked source, covered addition, untouched sibling, deletion, original reports and real index. |
| V-09a–f | `test_each_report_sibling_collision_refuses_write`: baseline, compare and measure with JSON-only and text-only occupied destinations, source and index preservation. |
| V-10 | Guide and installer/profile/README inspection: format and migration guidance, empty coverage, unknown values and fresh output names. This is document inspection, not an executed recovery test. |

## Remaining route

The acceptance decision assigns H-01 to the original implementer, H-02 to a
fresh independent maintainability reviewer, and F-01/H-03 to the registry
updater. After this handoff: independent maintainability review → registry
updater → fresh separate acceptance. The acceptance decision permits that
reference-only route only if executable bytes and admitted behavioral proof
remain current; otherwise affected discovery and gates must run first.
T-001.3 owns aggregate installed-composition evidence. SIDE-001 is separate
user work and was not modified by this implementation.
