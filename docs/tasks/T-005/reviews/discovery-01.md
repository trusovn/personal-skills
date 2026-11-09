# T-005 discovery report — installed handoff

Producing stage: task-review-discovery. First independent discovery, 2026-11-05.
Coverage: complete for the bounded task; the aggregate failed as detailed below.
No acceptance verdict, approved deferral or advancement is recorded.

## Provenance and reviewed scope

This session authored none of the reviewed bytes. It independently inspected
and executed the staged submission. HEAD is
`9883a7966308ff9cd556dd9edf99530d39cee0d2`; index tree is
`1038977b7494af481130cc0fd44977ed05f9809d`.
The worktree matched the index before probes and immediately before this write.
The tree identity binds all ten staged paths, including their index blobs;
worktree equality was checked separately with `git diff --quiet`.

Authority: `docs/tasks/T-005/brief.md`; verification design
`docs/tasks/T-005/verification.md`, revision 1; readiness and recorded decision
context: `docs/tasks/T-005/preflight.md`. Submission:
`docs/tasks/T-005/results.md`, READY_FOR_REVIEW. The user reports maintainability
passed; this report does not independently authenticate that stage.
The project plan section 11 and contract index/subsystem records supplied context.

Ownership: brief and task-index changes are pre-existing user preparation;
verification/preflight/results are packaged context. The added measurement test
is the implementation. Three contract summaries and the task-flow README update
route to the new evidence and retain live-compliance limits. These are within
the task's registry/evidence scope. No production runtime, official plan or task
map was changed. No unexplained overlap was found. Installer membership, managed
script list and guide remain applicable: the changed nested flow README is not
the installer's managed `skills/README.md`. Installer tests passed.

## Findings

No findings.

The active installation drift is an observed required aggregate failure, not a
new defect introduced by this staged change. Its disposition remains with the
acceptance/authority owner; this report grants no waiver.

## Completeness ledger

The ledger was selected before aggregate execution. Each row uses the submitted
results map as claims, then the independent probes below as current evidence.
No material row remains blocked or unchecked.

| Row | AC / cases and oracle | Submitted evidence | Independent evidence | Result |
|---|---|---|---|---|
| V-01 | AC-01: disposable installation, removed distribution, unrelated cwd, installation-local tools; B→I→R→C, separate I/R and current hashes, complexity 5→7→6, original B and exact report pairs/settings/scope | journey.log, captured-journey.log | P1; static trace of installed_launcher/capture; P2 | pass: actual public installed CLI journey, distinct invocations and corrected bytes |
| V-02 | AC-02: staged/unstaged/untracked start; source and actual index bytes unchanged at CLI/native boundaries; immutable B and historical pairs; empty/add/delete, settings, unknown values, collisions, incompatible/unavailable variants | measurement-final.log | P1/P2; preservation assertions inspect actual files/index; P5 | pass: all 34 owning cases and 36 installer cases, no skips |
| V-03 | AC-03: required whole-project Ruff F401 command and policy; actual edited failure alongside successful comparison, corrected success; retained output/hash/producer/stage and failure history | journey reports/native JSON, journey.log | P1/P2; static trace check_native and shared preservation guard | pass: real native exit 1/F401 then 0 under unchanged command/policy |
| V-04 | AC-04: plan V-001–V-008 preparation, actual inputs, finite controls and independent grading route; distinguish setup from agent behavior | implementer-fixtures.log, reviewer-fixtures.log and results map | P3/P4 plus catalog/README trace | pass for preparation only: 2 and 9 tests, including all finite setups; no live agent claim |
| V-05 | AC-05: truthful interpreter/pins, focused/structural/aggregate outcomes, raw evidence and qualification limits | results.md and /tmp/T-005-evidence logs | P1–P9; pins queried; prior aggregate-native.log compared with current P9 | pass for truthful publication; required aggregate itself FAILED, no completion waiver |

### Plan-case allocation and bounded adversarial checks

- V-001: V-01 and installer tests prove public distribution wiring.
- V-002: V-02 owning suite exercises target/default settings, neutral labels,
  numeric boundaries, unknown values and incompatible old inputs.
- V-003: V-02 dirty index/source and empty/add/delete preservation cases.
- V-004: V-01 two actual edits against immutable B; preparation checkers cover
  conditional correction/re-entry. P6 deliberately supplies wrong correction
  complexity and is rejected at the intended assertion.
- V-005: V-04 catalog inspection and finite preparation execution preserve 6→8,
  cohesive breach, materially touched unchanged hotspot with untouched sibling,
  and misleading extraction; implementer V-04a–k and reviewer V-03/V-04/V-05.
- V-006: V-02 deterministic missing/incompatible cases and V-04 advisory/required
  variants (implementer V-05a–f; reviewer V-01/V-02) retain fresh R obligations.
- V-007: V-04 implementer/reviewer V-10 includes significant/trivial test changes
  and conditional entry/re-entry; grading checks ordered remaining route.
- V-008: V-03 actual failure/recovery plus V-04 implementer V-08a–j and reviewer
  V-06a–j prepare missing/unavailable/stale evidence, aggregate reuse and no-check
  cases. The owning README requires grading actual diff, rationale, identities,
  native history and command/edit order, rather than setup success or keywords.

No executable schema or lifecycle implementation changed. Registry checks are
structural evidence, not behavioral proof. CLI/native subprocess completion and
fixture cleanup ran through the existing disposable setup; no service or fixture
process was intentionally retained. No independent process-containment or
anti-tamper qualification is claimed for this measurement task.

## Independent command record

All commands ran from the repository root. Define `P` as
`.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python` below.
For P3/P4 the exact environment prefix was `EVAL_SOURCE_ROOT="$PWD"
EVAL_MEASUREMENT_PYTHON="$PWD/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python"`.
These installed dependencies were already present; nothing was downloaded.

| Probe | Command | Current result |
|---|---|---|
| P1 | `P -B -m unittest discover -s tests -p test_maintainability.py -k complete_installed` | 1 pass, 1.947s |
| P2 | `P -B -m unittest discover -s tests -p test_maintainability.py` | 34 pass, no skips, 18.187s |
| P3 | `P -B skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py` with prefix above | 2 pass, 52.515s |
| P4 | `P -B skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py` with prefix above | 9 pass, 72.186s |
| P5 | `python3 -B -m unittest discover -s tests -p test_install_development_skills.py` | 36 pass, 34.317s |
| P6 | `P -B /tmp/T-005-evidence/fault_control.py` | exit 0; expected single assertion failure `(5,6,1) != (5,5,0)`, no errors; wrong correction rejected; in-memory mutation only |
| P7 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | 4 pass |
| P8 | `python3 tools/check_contracts.py --root .` | pass, 8 subsystems / 26 refs |
| P9 | `python3 tools/verify.py > /tmp/T-005-discovery-aggregate.log 2>&1` | exit 1; 7 checks, 1 failed, solely active-profile drift |

Additional read-only checks: `git diff --cached --check` passed; `git diff
--quiet` passed; `git status --short --untracked-files=all`, index blobs and tree
identity recorded. Pinned interpreter metadata: Radon 6.0.1, Ruff 0.14.2,
mando 0.7.1, colorama 0.4.6, six 1.17.0, matching requirements. P6's worker-supplied
script was inspected before independent execution. It compiles current test bytes
with only the wrong-correction substitution; no repository files are modified.
Focused raw outcomes are in this discovery session's command records. Submitted
raw archives remain under `/tmp/T-005-evidence/`; those are producer evidence,
not a substitute for the current independent runs.

## Aggregate-gate record

Owner/stage: this independent initial discovery. Before P9, all safely runnable
material rows had clean current targeted evidence, finite-risk probes were done,
and no selected adversarial probe remained. User explicitly approved P9's cost
and execution outside the sandbox; no unapproved network/provider check ran.
Exact command and raw log: P9 above. Result: FAILED. Five suites ran 537 tests
with 32 analyzer skips under the default Python. Contracts passed. The sole
failed check was active-profile drift: 112 compared paths, 10 differences
(4 changed, 6 missing), matching the submission's reported limitation.
Separate P2 supplies real analyzer evidence without skips; it does not turn P9
into a pass. No installation was refreshed. No gate was added or waived.

## Scope/status preservation

Exact status immediately before writing this report:

```text
M  docs/contracts/implementer-feedback.json
M  docs/contracts/measurement.json
M  docs/contracts/reviewer-feedback.json
A  docs/tasks/T-005/brief.md
A  docs/tasks/T-005/preflight.md
A  docs/tasks/T-005/results.md
A  docs/tasks/T-005/verification.md
M  docs/tasks/index.json
M  skills/task-implementation-flow/README.md
M  tests/test_maintainability.py
```

Exact status after writing adds only:

```text
?? docs/tasks/T-005/reviews/discovery-01.md
```

All preceding status lines remain identical. The report is untracked and was
not staged. The reviewed index tree remains unchanged. This report applies
only to the identified reviewed bytes; it neither reviews nor authenticates itself.

## Residual risks and next route

Live actor behavior, independent semantic judgment and agent owner/routing
choices remain unqualified by design. Separate approval, selected runtime/cases,
fresh actor sessions and independent grading are needed for that optional work.
Temporary raw archives are local evidence, not guaranteed durable storage.
Acceptance owns disposition of the failed active-profile aggregate; discovery
has no authority to approve a deferral or advance the task.

Next: separate `task-acceptance-review` call with brief, staged diff at the tree
above, this report, verification revision 1, preflight/decision context, results,
and the user-reported maintainability evidence. No reviewer regression files
were added; P6 is the explicit current mutation control.

## Discovery continuation

- Iteration/bytes: initial independent discovery; HEAD and index tree above.
- Rows: V-01 pass; V-02 pass; V-03 pass; V-04 pass for preparation;
  V-05 pass for truthful evidence, aggregate FAILED.
- Finding IDs: none. No prior discovery ledger supplied.
- Continuity: worker results are submitted claims; P1–P9 are current independent
  evidence. No incomplete material scenario. Correction owner: implementer if
  needed; evidence owner: discovery; aggregate disposition authority: acceptance.
- Preparation: T-005 brief, verification revision 1, preflight decision context.
- Reviewer regressions: no repository paths; P6 command above.
- Aggregate: P9 failed, discovery-owned, active-profile drift only; no waiver.
- Next: separate acceptance decision with the full package and failed-gate record.
