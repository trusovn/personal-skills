# T-004 correction 01 — canonical finite case identities

Status: `READY_FOR_REVIEW`; current implementation evidence supplied, no independent verdict.

- Authority: `docs/tasks/T-004/brief.md` revision 1.
- Preflight/context: `docs/tasks/T-004/preflight.md`; `docs/tasks/T-004/verification.md` revision 1; original implementation result and `reviews/maintainability-01.md`.
- Preceding verdict: `CHANGES_REQUESTED` from fresh maintainability review 01.
- Broken invariant: each dispatch ID must identify exactly one selectable catalog row, and the generated oracle must retain that requested row's exact case fields. Iterating duplicated IDs cannot count as distinct preparation evidence.

## Complete pre-edit row-to-evidence map

| Supplied identity | Prior reviewer status | Planned implementation evidence / navigation | Next owner and unchanged reviewer status |
|---|---|---|---|
| MNT-01 | Confirmed blocker | Add duplicate-ID and exact returned-row assertions to existing finite matrix; demonstrate duplicate rejection before data correction; consolidate V-11a/b/c each into one canonical row with both original oracle requirements; rerun all finite cases. | Correction owner: implementer; fresh maintainability reviewer must determine disposition. Prior confirmed status is not self-cleared. |
| RAT-01 | Agreement, subject to MNT-01 | Navigation context; retain the single finite matrix owner. Compare current metric and explain any worsened over-target value. | Fresh maintainability reviewer validates affected test rationale. |
| RAT-02 | Agreement | Navigation context; seed unchanged. | Fresh reviewer retains only current applicable evidence. |
| RAT-03 | Agreement | Navigation context; native_inputs unchanged. | Fresh reviewer retains only current applicable evidence. |
| RAT-04 | Agreement | Navigation context; evidence_fault unchanged. | Fresh reviewer retains only current applicable evidence. |
| RAT-05 | Agreement | Navigation context; route_inputs unchanged. | Fresh reviewer retains only current applicable evidence. |
| RAT-06 | Agreement | Navigation context; prepare unchanged; unique catalog removes ambiguous next-match selection without a dispatcher redesign. | Fresh reviewer retains only current applicable evidence. |

Complete finding inventory: MNT-01 only. The review reports no unreviewed
maintainability scope and no other blocker. All V-01–V-11 scenario IDs and
existing distinct variants remain coverage obligations; V-11a/b/c overlapping
rows are consolidated, not discarded. All actor verdict/route compliance and
T-005 installed composition remain unqualified. Active-profile drift stays a
coordinator/operator duty and cannot be waived by this correction.

Influenced siblings: every catalog ID uses the same selection, subtest, output
and grading boundary. The existing all-case matrix will validate uniqueness for
all IDs and exact generated case fields for every selection. No new shared
framework or runtime dependency is needed.

Broad-gate decision: run the reviewer regression and complete local finite
matrix, then owning reviewer suite and required canonical architecture/contracts.
Do not rerun the aggregate during this bounded correction: fresh discovery owns
its separate targeted/aggregate record under the task flow; prior aggregate is
historical for changed harness/data inputs, and active-profile drift remains
explicit. Original B and every comparison/review pair remain immutable. Fresh
comparison and native identity will record corrected bytes before handoff.

## Correction evidence

Completed as implementation evidence below. Reviewer row status remains confirmed until a fresh review.

## Current correction handoff

Implemented: `READY_FOR_REVIEW`

- Authority: `docs/tasks/T-004/brief.md`, revision 1.
- Preflight/context reference: `docs/tasks/T-004/preflight.md`; `docs/tasks/T-004/verification.md`, revision 1; `docs/tasks/T-004/implementation.md`; `docs/tasks/T-004/reviews/maintainability-01.md`.
- Preceding verdict: `CHANGES_REQUESTED`, MNT-01 confirmed. This implementation evidence does not change the reviewer's status.
- Finding/scenario IDs: MNT-01 only; RAT-01–RAT-06 disposition identities retained. All 62 V-01–V-11 child scenario IDs and 82 distinct selectable variants remain. The initial 85 rows represented only 82 selectable IDs; the earlier 85-independent-variants claim was incorrect.
- Complete findings and invariant: each dispatch ID selects exactly one canonical case and generated oracle case fields match the requested catalog row. Consolidated duplicate V-11a/b/c rows only, keeping both original situation and oracle strings verbatim under each stable canonical ID. No distinct requirement, seed, variant or permission was dropped.
- Influenced sibling surfaces: all IDs share the dispatch/subtest/output/grading boundary. The existing matrix now rejects duplicate IDs before any setup and checks every original row field against the returned oracle. `review_fixture.prepare` stays unchanged; no dispatcher/framework redesign or new dependency was introduced.
- Attempts and discarded hypotheses: duplicate-ID reproducer confirmed 85 rows / 82 IDs before edits. Added the invariant assertions first; the reviewer regression failed in 0.001s with `85 != 82: dispatch IDs must be unique`, at the intended assertion (`/tmp/T-004-correction-01-red.log`). After canonical consolidation the same matrix and full suite passed. No unsuccessful correction or discarded alternative hypothesis; no unrelated changes.
- Current scoped diff: source `evals/files/review_cases.json` consolidates three overlapping pairs into three canonical rows; `evals/files/check_review_fixture.py` adds uniqueness and exact returned-row assertions. `implementation.md` corrects counts, removes duplicate display rows and labels superseded evidence; this new correction record carries the pre-edit ledger and current handoff. No other source, runtime, root test, installer/profile, registry, plan or active installation changes.

### Measurement and rationale

Original B remains `.quality/reports/T-004-preflight-20261104-01.json` and
`.quality/reports/T-004-preflight-20261104-01.txt`; JSON SHA-256 remains
`031191f9e4e50ff268699c924583351d7e0f8e99032aede1202fa493a9ff2084`.
All prior implementer/reviewer JSON/text pairs remain unchanged. Fresh pair:
`.quality/reports/T-004-correction-01.json` and
`.quality/reports/T-004-correction-01.txt`.

```sh
python3 -B .agents/scripts/measure_maintainability.py compare skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py --root /Users/mtrusov/work/skill-sources/personal-skills --baseline .quality/reports/T-004-preflight-20261104-01.json --output .quality/reports/T-004-correction-01.json
```

Result: complete, full-profile, compatible `compared`. Current affected Python
scope is the existing matrix test method; catalog JSON receives semantic/identity
verification, not Python metrics. No expansion beyond original package coverage.
Runtime fixture functions, seed/correction/native/route helpers and all other
Python bytes remain unchanged from review 01. No rename/extraction relationship
is claimed. Original B has no before function count for this newly added test;
that value remains absent, not zero.

RAT-01 current rationale: in the fresh pair above,
`ReviewFixtureTests.test_every_finite_setup_supplies_real_inputs_and_preserves_history`
has complexity absent → 14 against B, versus 12 in the previous submission and
reviewer R. The two added comprehensions enumerate all IDs and reconstruct exact
requested fields; the associated assertions enforce the shared selection/grading
invariant at the owner that already traverses every case. Keeping them beside
the matrix exposes duplicate/truncated selection before setup and binds every
actual generated oracle to its requested row. A separate single-use validator
would scatter this owner or add a helper only for these two assertions; one test
per identity would duplicate setup and miss complete catalog traversal. This
bounded growth directly repairs MNT-01; no metric-driven split, settings change
or threshold compliance claim is made. RAT-02–RAT-06 code and rationale remain
unchanged navigation context; fresh review owns their applicability.

### Current evidence and coverage ledger

Reviewer reproducer (local equivalent of the supplied JSON inspection):

```sh
python3 -c 'import json; from collections import Counter; rows=json.load(open("skills/task-implementation-flow/task-maintainability-review/evals/files/review_cases.json")); counts=Counter(row["id"] for row in rows); print(len(rows), "rows", len(counts), "unique IDs", {key:value for key,value in counts.items() if value>1}); assert len(rows)==len(counts)'
```

Result: `82 rows 82 unique IDs {}`; exit 0;
`/tmp/T-004-correction-01-reproducer.log`. Before consolidation, the exact full
case strings were checked to remain substrings of each merged situation/oracle;
all original distinct requirements are retained.

Focused reviewer regression/full finite suite:

```sh
EVAL_SOURCE_ROOT=/Users/mtrusov/work/skill-sources/personal-skills EVAL_MEASUREMENT_PYTHON=/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python PYTHONDONTWRITEBYTECODE=1 python3 skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py
```

Result: **5 tests passed in 66.352s**, including actual preparation and exact
returned-row verification for all 82 unique selectable cases; log
`/tmp/T-004-correction-01-focused.log`. This is local tool/fixture evidence, not
fresh actor compliance or a maintainability verdict.

| Ledger row | Prior reviewer status | Current implementation evidence | Incomplete reason / next owner |
|---|---|---|---|
| MNT-01 | Confirmed blocker | Red duplicate-ID assertion rejects old data; reproducer shows 82/82; complete matrix prepares every unique ID and compares all requested fields exactly; all old situations/oracles retained. | Fresh maintainability reviewer must decide disposition; implementer does not self-clear. |
| RAT-01 | Agreement subject to MNT-01 | Fresh original-B comparison records CC14; explicit retention rationale above covers prior-submission CC12 → CC14. | Fresh reviewer validates current rationale for affected test. |
| RAT-02 | Agreement | Seed code/rationale unchanged; current native inventory preserves its hash. | Fresh reviewer checks continued applicability; no new implementation check substitutes for review. |
| RAT-03 | Agreement | Native-input code/rationale unchanged; current native inventory preserves its hash. | Same fresh reviewer ownership. |
| RAT-04 | Agreement | Evidence-fault code/rationale unchanged; current native inventory preserves its hash. | Same fresh reviewer ownership. |
| RAT-05 | Agreement | Route-input code/rationale unchanged; current native inventory preserves its hash. | Same fresh reviewer ownership. |
| RAT-06 | Agreement | Prepare code/rationale unchanged; canonical catalog now makes its existing unique-ID lookup unambiguous. | Same fresh reviewer ownership. |

### Native evidence and broad-gate ownership

Native checked-byte identity:
`.quality/reports/T-004-native-bytes-04.json`, 441 Git-visible input paths,
digest `bcfc70896533925dacf3ee3fb87d81b37be05863997450f03dfab32b9ce7a0cc`.
Explicit exclusions are reporting-only implementation/correction/review records;
all source, test, configuration, skill/eval and authoritative package inputs are
included. Only the catalog JSON and matrix checker differ from native identity03.
Producer/stage: this installed implementer correction invocation.

| Exact command | Scope / policy / owner | Current result and raw evidence |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py` | Existing owning source review/fixture contract; implementer targeted verification | 26 passed, 2.484s; `/tmp/T-004-correction-01-owner.log`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Required whole-repository CLEAN policy, AGENTS/development; implementer before handoff, reviewer retains run/validation duty | 4 passed, 0.173s; `/tmp/T-004-correction-01-architecture.log`. |
| `python3 tools/check_contracts.py --root .` | Required whole registry/index structural check, AGENTS/development; implementer/updater ownership | PASS, 7 subsystems / 22 plan refs; `/tmp/T-004-correction-01-contracts.log`. Semantic registry update remains after accepted maintainability review. |
| `python3 tools/verify.py` | Broad correction/discovery decision under installed correction protocol and existing task flow | Not rerun during this bounded correction. Changed only task-owned case data and checker assertions; current focused + owning evidence supplies this implementation scope. Fresh discovery owns its separate aggregate decision/evidence. Earlier aggregate is historical for changed inputs, never relabeled current. Active-profile drift remains a real required-check failure and coordinator/operator duty; no waiver. |

The pinned measurement suite/runtime and installer membership/dependencies were
unchanged. The current finite suite performs disposable profile installation as
part of its real preparation. No broad installer/runtime suite was repeated
solely to fill report sections. No setup/provisioning, live/networked eval,
active refresh or independent review was performed.

### Transfer, remaining coverage and route

Shared paths above are concrete for the coordinator. If an isolated root
`<clone>` is selected, copy both original B siblings from
`/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/T-004-preflight-20261104-01.json`
and `.txt` to the identical relative paths at `<clone>`, and likewise both fresh
`T-004-correction-01.json`/`.txt` siblings and native identity04. Transfer retained
historical pairs when consuming their comparisons, plus the exact `/tmp/T-004-correction-01-*.log`
files to `<clone>/.quality/reports/` with unchanged basenames. Validate logical
project/applicability; ignored reports do not travel in commits. No receiving
clone was selected.

Remaining reviewer coverage: the complete corrected submission awaits fresh
maintainability review; MNT-01 remains the sole confirmed finding until that
review. No additional blocked/unchecked review ledger rows were supplied. Actor
verdict/disposition/route behavior for all V-01–V-11 cases and T-005 installed
composition stay unqualified. Native active-profile drift remains explicit for
its coordinator/operator and downstream admission owners.

First outstanding stage and complete ordered remainder: **fresh
`task-maintainability-review` → designated `task-contract-registry-updater` → fresh
independent `task-review-discovery` → separate fresh `task-acceptance-review`**.
Current canonical architecture proof is supplied; reviewer run/validation duty
is preserved. No downstream stage is invoked by this handoff.
