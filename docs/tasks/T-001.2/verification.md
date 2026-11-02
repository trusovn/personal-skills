# Verification Design: T-001.2 — Neutral reports and empty-start baselines

Protect factual metric reporting and genuine pre-edit evidence. A successful
measurement must not imply design acceptance. An empty baseline must prove
absence inside captured coverage, and later comparisons must retain that
original evidence.

## Testing approach

| Checks | Level and real boundary | Why this evidence is sufficient |
|---|---|---|
| Numeric and symbol decisions, V-01–V-03 | Component checks with real pinned Radon/Ruff measurements of source bytes | Proves native counts, matching and unknown values. Do not substitute fabricated analyzer success. |
| Output and compatibility, V-04–V-05 | Real public CLI, saved JSON/text and console; controlled incompatible baseline copies | Exercises serialization, presentation and exit status. Seeded incompatible identities test consumer refusal, not execution of an old analyzer. |
| Capture, repeated edits and preservation, V-06–V-09 | CLI against disposable folders and a real Git repository; real saved reports and index | Exercises coverage, durable history and filesystem refusal. Source/index claims require byte comparisons, not mocked writes. |
| Migration and ownership guidance, V-10 | Document/interface review | Establishes instructions and reference consistency. This is not behavioral proof of recovery or installed composition. |

Reuse the relevant boundary, native-exemption, compatibility, folder-baseline,
snapshot and no-overwrite coverage in `tests/test_maintainability.py`. Extend
these cases where evidence is missing; retain their distinct scenarios. These
checks do not prove agent judgment or T-001.3's aggregate installed composition.

## Source and revision

Source brief: docs/tasks/T-001.2/brief.md
Source brief revision: SHA-256 `4163de695ba4b43c16f15ba3ef7b1de4e37068c5956331c7f0a08d6068451f38`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

Ready means the verification design is complete. Execution and implementation
readiness are established by later stages. The exact new format number remains
delegated to implementation by plan section 12.

## Coverage summary

| Promise from the brief | AC / risk row | Required cases |
|---|---|---|
| [Neutral changes, distinct threshold information and advisory success](brief.md#work-and-acceptance-criteria) | AC-01; R-03 numeric/boundary cases | V-01a–V-01q, V-02a–V-02e, V-04 |
| [Versioned evidence and visible compatibility refusal](brief.md#work-and-acceptance-criteria) | AC-02; R-03 old format, tools/settings/scope, incomplete baseline | V-05a–V-05j, V-10 |
| [Valid empty parent capture and covered additions only](brief.md#work-and-acceptance-criteria) | AC-03; R-04 empty, missing, excluded and uncovered scopes | V-06, V-07a–V-07d |
| [Non-empty captures, native unknowns and symbol identity remain correct](brief.md#work-and-acceptance-criteria) | AC-04; R-03 symbols, diagnostic transitions and exemptions | V-02a–V-02e, V-03a–V-03i, V-08, V-09 |
| [Original evidence survives repeated edits and deletion](brief.md#r-04--empty-capture-or-repeated-comparison-fabricates-before-state-ac-03ac-05) | AC-04–AC-05; R-04 repeated comparison, deleted file | V-06, V-08, V-09 |
| [Source, real index and reports remain unchanged by commands](brief.md#work-and-acceptance-criteria) | AC-05; R-04 staged/unstaged/untracked preservation and collisions | V-06, V-08, V-09a–V-09f |

## Shared setup

- Use disposable target directories and the accepted T-001.1 runtime. Preflight
  confirms the pinned interpreter and analyzer availability. Measurement must
  not install dependencies. Missing analyzers or skipped analyzer tests cannot
  qualify AC-01–AC-04.
- Use advisory targets of complexity 10, statements 50 and arguments 5, with
  native Ruff collection limits of zero. Construct small source examples with
  independently known counts, using the existing fixture conventions. Do not
  compute expected results with the comparison implementation.
- Unless a case changes it, keep settings, tools, selected checks and scope
  compatible. Give each run a fresh explicit path under target
  `.quality/reports/`. Inspect parsed JSON, sibling text and console output
  where specified. Match output labels rather than arbitrary occurrences in
  captured source or raw diagnostic messages.
- Before each CLI action, retain source bytes, the real index bytes where Git
  exists, and prior report bytes. Intentional edits/deletions between actions
  are setup; commands themselves must not change those inputs.

## Verification scenarios

### V-01 — Numeric changes stay factual at each target boundary

Covers: AC-01; R-03.

Why: evaluative labels or a strict threshold gate would turn observations into
a false verdict. Equality must remain within target.

Given a matched function with both native values available, measure the before
source, apply the indicated source edit, then compare the real measurements:

| Case | Metric (target) | Before → current | Exact change result |
|---|---|---|---|
| V-01a | Complexity (10) | 2 → 3 | delta +1, `increased`, no crossing |
| V-01b | Complexity (10) | 9 → 10 | delta +1, `increased`, no crossing |
| V-01c | Complexity (10) | 10 → 11 | delta +1, `increased`, `crossed_above_threshold` |
| V-01d | Complexity (10) | 12 → 11 | delta -1, `decreased`, no crossing |
| V-01e | Complexity (10) | 11 → 11 | delta 0, `unchanged`, no change highlight |
| V-01f | Statements (50) | 20 → 25 | delta +5, `increased`, no crossing |
| V-01g | Statements (50) | 49 → 50 | delta +1, `increased`, no crossing |
| V-01h | Statements (50) | 50 → 51 | delta +1, `increased`, `crossed_above_threshold` |
| V-01i | Statements (50) | 51 → 50 | delta -1, `decreased`, no crossing |
| V-01j | Statements (50) | 51 → 52 | delta +1, `increased`, no new crossing |
| V-01k | Arguments (5) | 3 → 4 | delta +1, `increased`, no crossing |
| V-01l | Arguments (5) | 4 → 5 | delta +1, `increased`, no crossing |
| V-01m | Arguments (5) | 5 → 6 | delta +1, `increased`, `crossed_above_threshold` |
| V-01n | Arguments (5) | 7 → 6 | delta -1, `decreased`, no crossing |
| V-01o | Arguments (5) | 6 → 5 | delta -1, `decreased`, no crossing |
| V-01p | Arguments (5) | 6 → 7 | delta +1, `increased`, no new crossing |
| V-01q | Complexity (10) | 11 → 12 | delta +1, `increased`, no new crossing |

Check the exact before/current values, signed deltas and highlights. Any
evaluative change classification also uses `increased`/`decreased`, including
the former `worsened` classification. A decrease in another function does not
cancel an increase. Real output and CLI success are checked in V-04; these
component cases isolate native numeric decisions without repeating every CLI
journey.

### V-02 — Symbol changes preserve identity and interpretation

Covers: AC-01, AC-04; R-03.

Why: matching by line, message or guessed rename can invent a numeric history.

Given real before/current source inventories, perform each action and inspect
the comparison rows and highlights:

| Case | Setup and action | Expected result |
|---|---|---|
| V-02a | Add a new complexity-11 function in captured coverage | `new`, unknown before/delta, `new_above_threshold` and `needs_interpretation` |
| V-02b | Remove a captured function | `removed`, known before, unknown current/delta, `needs_interpretation` |
| V-02c | Rename a function and extract a helper | Separate new and removed identities with unknown deltas and `needs_interpretation`; no guessed relationship |
| V-02d | Retain duplicate qualified names on both sides | Ambiguous rows remain `unmatched`, with unknown deltas and interpretation information; no arbitrary pairing for complexity or Ruff |
| V-02e | Shift lines around distinct nested, local-class and async functions without changing their metrics | Qualified identities remain separate and matched; unchanged values have delta 0, without invented additions/removals |

For V-02a–V-02d, inspect human interpretation labels as well as JSON. Existing
native-count cases supply the success control for matching numeric identities.

### V-03 — Missing native evidence stays unknown

Covers: AC-01, AC-04; R-03.

Why: no diagnostic can mean a native exemption or no count. It does not prove
zero or a numeric decrease. The pinned Ruff analyzer must produce these states.

Use the existing native examples. Each row below specifies one comparison
direction; the same qualified symbol exists on both sides.

| Case | Before → current source | Expected Ruff result |
|---|---|---|
| V-03a | `def f(): pass` → `def f(a): pass` | PLR0913: unknown → 1, unknown delta, `new_diagnostic` |
| V-03b | Reverse V-03a | PLR0913: 1 → unknown, unknown delta, `diagnostic_resolved` |
| V-03c | Return-only body → assignment plus return | PLR0915: unknown → 1, unknown delta, `new_diagnostic` |
| V-03d | Reverse V-03c | PLR0915: 1 → unknown, unknown delta, `diagnostic_resolved` |
| V-03e | Six-argument method with `@override` → same method without decorator | PLR0913: unknown → 6, unknown delta, `new_diagnostic` and `above_threshold` |
| V-03f | Reverse V-03e | PLR0913: 6 → unknown, unknown delta, `diagnostic_resolved` |
| V-03g | Six-argument `@overload` method → same method without decorator | Same numeric and highlight outcome as V-03e |
| V-03h | Reverse V-03g | Same outcome as V-03f |
| V-03i | Retain one six-argument function, add another with an identical diagnostic message | Original diagnostic remains unchanged; added identity is `new_diagnostic`, unknown before/delta, `above_threshold` |

All transition rows retain `needs_interpretation`. Unknown is not zero, and a
resolved diagnostic is not `decreased`. Appearance below target has no
`above_threshold` label. Inspect raw native observations and comparison values.
Retain existing proof that zero collection limits preserve native exemptions
and that `noqa` does not suppress this measurement profile.

### V-04 — Saved reports and console expose neutral observations with exit 0

Covers: AC-01; R-03.

Given valid sources that include an at-target increase, an over-target
increase, a decrease and V-02's new hotspot, capture a baseline and compare to
a fresh output path. Also run a standalone measurement containing a breach.

Then all complete commands exit 0. JSON classifications/highlights and sibling
text/console use `increased`/`decreased` (human capitalization is permitted).
No `got_worse`, `improved`, `worsened`, or corresponding evaluative human label
remains in report labels. Values, deltas, distinct crossing/new-hotspot labels,
symbol locations and interpretation information survive. Standalone breaches
remain visible without a design rejection or required-response verdict.

Check the actual saved pair and console, not only the formatter function.
Show that changed label assertions reject the pre-change implementation for
the intended label mismatch before correcting it (R-03 evidence obligation).

### V-05 — Incompatible evidence cannot become a successful comparison

Covers: AC-02; R-03.

Given a real current-format baseline and valid current source, provide each
baseline variant below independently. Keep all other prerequisites compatible
and use a fresh output name so no unrelated guard masks the result.

| Case | Baseline input or changed comparison input | Expected result |
|---|---|---|
| V-05a | Compatible unchanged current-format evidence | Exit 0 and `compared`; baseline bytes preserved |
| V-05b | Prior format-4 report with its old labels; retain earlier-format rejection coverage | Exit 2, visible format incompatibility; no successful comparison |
| V-05c | Different analyzer version identity | Exit 2, visible tool incompatibility |
| V-05d | Different effective maintainability settings | Exit 2, visible settings incompatibility |
| V-05e | Different effective Ruff settings | Exit 2, visible settings incompatibility |
| V-05f | Different or absent Ruff collection limits | Exit 2, visible incompatible collection identity |
| V-05g | Different adapter hash | Exit 2, visible adapter incompatibility |
| V-05h | Different Python implementation or major/minor version, as separately exercised variants | Exit 2, visible runtime incompatibility |
| V-05i | Baseline marked incomplete | Exit 2, visible incompatible/incomplete baseline; not clean evidence |
| V-05j | Scope outside captured coverage (V-07d) | Exit 2, visible scope incompatibility |

Check CLI status and diagnostic; inspect comparison status in any emitted
report. Controlled copies may seed incompatible identities; these are consumer
guard tests. Use actual settings changes for V-05d/e. Keep the original baseline
unchanged. Retain compatible transferred-root/Python-patch and equal-effective-
settings controls so provenance differences alone do not cause refusal.

### V-06 — Empty capture retains known absence across two real edits

Covers: AC-03–AC-05; R-04.

Why: allowing an empty scan without folder coverage, or silently rebasing after
the first edit, fabricates before state.

Given an explicitly selected existing, non-excluded folder `area/` with no
included Python files, real pinned tools and valid settings:

1. Run `baseline area --output .quality/reports/empty-before.json`.
   Expect exit 0, complete measurement, empty Python inventory and recorded
   `area/` folder coverage. Retain both saved files byte for byte.
2. Add `area/new.py` containing a named function, then compare that file with
   the saved baseline into `empty-after-01.json`. Expect exit 0 and `compared`.
   The new complexity symbol has unknown numeric before/delta and `new`
   classification. Folder coverage establishes prior file absence; it does
   not supply numeric zero. Retain the new report pair.
3. Edit the same function to a different known complexity and compare into
   `empty-after-02.json`, still using `empty-before.json`. Expect exit 0 with
   fresh current source identity/count. The symbol is still new against the
   original baseline; it is not a delta against after-01.

At each checkpoint verify saved source bytes/hashes, folder coverage, report
status and output. All prior report bytes remain intact; source/index bytes
match their immediate pre-command values. This is a tool history proof, not
proof that later agents will retain the baseline reference.

### V-07 — Empty success cannot bypass scope validation

Covers: AC-02–AC-03; R-04.

Given valid settings and tools, exercise each guard independently:

| Case | Starting state and action | Expected result |
|---|---|---|
| V-07a | Existing included folder without Python files; ordinary `measure` | Exit 2, empty-inventory error; no successful measurement |
| V-07b | Missing selected parent; `baseline` with fresh output | Exit 2, missing-scope error; no valid absence capture |
| V-07c | Existing explicitly excluded parent; `baseline` with fresh output | Exit 2, exclusion error; no valid absence capture |
| V-07d | Capture `area/`, then add/select `outside/new.py` outside it | Exit 2, uncovered-scope error; no successful comparison or claimed known absence |

Check the intended diagnostic and absence of a complete successful artifact,
with source/index/prior reports unchanged. V-06 is the empty-baseline success
control. Preserve the existing required-output guard for `baseline`.

### V-08 — Non-empty dirty capture survives subset edits and deletion

Covers: AC-04–AC-05; R-04.

Why: reporting changes must not replace worktree evidence with HEAD/index
contents, mark untouched files removed, or consume a comparison as baseline.

Given a real Git repository with a committed function, stage a first edit,
make a further unstaged edit to the same file, and add an untracked Python
file. Include a separate untouched file under the captured folder.

1. Capture the non-empty folder baseline to a new saved pair. Expect actual
   unstaged and untracked source bytes/counts in the baseline, not staged or
   HEAD bytes. Repository status retains staged/unstaged/untracked distinctions.
2. Edit the affected captured function and add a covered Python file. Compare
   only affected files with the original baseline. Expect exact native numeric
   deltas for matched values and new identities for additions. The untouched
   baseline file is neither compared nor reported as removed.
3. Delete the originally captured affected file. Compare its deleted path
   into a second fresh report using the original baseline. Expect exit 0 and
   complete comparison, removed complexity identities with original before
   values and unknown current/deltas. Missing Ruff counts retain interpretation,
   not a zero or numeric decrease.

Check real saved files, source snapshots/hashes, current identities and native
counts at each checkpoint. Baseline and earlier comparison pairs stay byte
identical. Each command preserves immediate pre-command source bytes, real
`.git/index` bytes and staged blob contents. Intentional edits/deletion are the
only source changes. This journey complements V-06's empty history.

### V-09 — Either occupied report path prevents overwrite

Covers: AC-05; R-04.

Given a valid non-empty target, compatible baseline for comparison, and a saved
sentinel at the indicated destination, invoke each operation with `--output`:

| Case | Operation | Occupied destination |
|---|---|---|
| V-09a | `baseline` | JSON exists; sibling text absent |
| V-09b | `baseline` | Only sibling text exists |
| V-09c | `compare` | JSON exists; sibling text absent |
| V-09d | `compare` | Only sibling text exists |
| V-09e | `measure` | JSON exists; sibling text absent |
| V-09f | `measure` | Only sibling text exists |

Then exit 2 identifies the collision. Existing bytes stay unchanged and the
absent sibling is not created. Source, real index and all earlier reports are
unchanged. Retain existing both-files-present refusal evidence. V-04, V-06
and V-08 provide fresh-path success controls; a writer that always refuses
cannot pass the design.

### V-10 — Guidance describes the format transition and safe recovery

Covers: AC-02; scope maintenance obligations.

Given the implemented new format, review `scripts/measure-maintainability.md`
and inspect installer selections/tests, profile guide and README references.

Then guidance names the actual new format, neutral fields and old-format
refusal. It describes explicit existing empty-parent capture, covered additions,
fresh comparison filenames and unknown native values. Migration requires a
fresh baseline before edits or remeasurement of verified exact preserved
pre-edit bytes. It never directs a caller to use the edited tree as replacement
before evidence. Do not require a new automatic migration interface.

Only references made stale by this change need synchronization. Record whether
installer-managed resources/references changed. Documentation review supports
the migration promise; V-05 proves runtime format rejection. Reviewers must not
report documentation or syntax checks as executed recovery behavior.

## Implementation handoff

- Implement under the brief's authority, reusing relevant tests and fixtures.
  Test names, placement, parameterization and helpers remain implementation
  choices within repository rules.
- Obtain a ready `preflight.md` for this verification revision before
  implementation. Confirm T-001.1's accepted contract, pinned tools and commands.
  A reasoned verification revision preserves IDs and supersedes affected
  readiness/evidence until focused preflight is ready for that revision.
- Run changed cases first, then `<pinned-python> -B -m unittest discover -s
  tests -p test_maintainability.py`. Analyzer skips are gaps, not qualification.
  Run installer tests only if managed resources/references change, and required
  architecture/contract checks before handoff. T-001.3 owns the aggregate gate.
- Route unresolved expected results to task design/the decision owner; route
  unavailable tools, fixtures or boundaries to preflight without reducing
  coverage. No live/network check or dependency installation is authorized by
  this design alone.
- Hand the chosen format revision, compatibility behavior and empty-capture
  interface to T-001.3 and later T-002. Keep independent discovery and acceptance
  separate under the brief's required review route. This artifact establishes
  design readiness, not implementation correctness or behavioral qualification.
