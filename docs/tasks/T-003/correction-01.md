# T-003 correction 01 — F-01

Implemented: READY_FOR_REVIEW

Authority: user request to fix discovery issues; docs/tasks/T-003/brief.md revision 1, verification.md revision 1 and preflight.md decision context. Prior evidence: reviews/discovery-01.md (no acceptance verdict) and reviews/maintainability-01.md. Registry updater is running separately at the user's direction; this correction does not own its files or claim its completion.

## Correction and evidence

F-01: V-01d must change captured source bytes while preserving the entire Git short status, file inventory, real index and original reports. The fixture now makes logic.py dirty before capture, then changes those dirty bytes after capture. The new focused regression checks each property against actual Git/filesystem state. Existing V-01h index and V-01f effective-identity cases remain unchanged; the full finite check executes those siblings too.

Changed files: measurement_fixture.py (+2 lines) and check_measurement_fixture.py (+14 lines), under skills/task-implementation-flow/bounded-task-implementer/evals/files/. No existing reports, plan documents, staged entries or registry files were edited by this correction.

Commands from repository root:

- `EVAL_MEASUREMENT_PYTHON="$PWD/.quality/venv/bin/python" .quality/venv/bin/python -B skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py MeasurementFixtureTests.test_source_hash_mismatch_preserves_status_and_other_entry_facts` — first failed on original fixture because status gained ` M src/logic.py`; passed after correction (1 test, 0.447s). This implements discovery P2's oracle plus preservation assertions.
- `EVAL_MEASUREMENT_PYTHON="$PWD/.quality/venv/bin/python" .quality/venv/bin/python -B skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py` — passed, 2 tests including all 94 variants, 49.255s.
- `.quality/venv/bin/python -B -m unittest discover -s tests -p test_maintainability.py` — passed, 33 tests, 16.540s, no skips.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — passed, 4 tests, 0.161s; repository CLEAN policy, implementation-produced evidence.
- `python3 tools/check_contracts.py --root .` — passed, 7 subsystems/22 references at execution time. External concurrent registry changes are not owned or behaviorally qualified here.
- `git diff --check` — passed.

Aggregate `python3 tools/verify.py`: not rerun for this narrow fixture correction; fresh discovery retains its aggregate decision. Prior implementation aggregate drift remains historical evidence, not a green result. Installer membership/runtime dependencies are unchanged; canonical installer ownership and previous inspection still apply.

## Measurement

Original baseline remains `.quality/reports/T-003-before-20261103.json` and sibling `.txt`. Prior initial comparison remains `.quality/reports/T-003-after-20261103.json/.txt`. New comparison: `.quality/reports/T-003-correction-01.json/.txt`, complete/compared against the original baseline.

Exact command: `.quality/venv/bin/python -B .agents/scripts/measure_maintainability.py compare skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_fixture.py skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py --root . --baseline .quality/reports/T-003-before-20261103.json --output .quality/reports/T-003-correction-01.json` — exit 0. Covered assets: eval/harness; unchanged setup_fixture.py is included for submission continuity, not newly attributed as affected.

Affected functions: basic and the added regression. In the new report, basic has complexity 16 (15 in initial comparison; unknown in original baseline because it was new), statements 40, arguments 2. Retain the explicit extra branch because it establishes the case's pre-capture dirty state at the same point as other dirty setup. Moving this two-line setup into a helper or mutation descriptor would add navigation and hide capture ordering. The new regression has complexity 3, below target. Existing rationale in results.md for unchanged functions remains context; no cleanup scope or exclusions changed.

For an isolated consumer, explicitly copy original, initial and correction JSON/text pairs from this repository's `.quality/reports/` to those same receiving relative paths. Ignored reports do not travel in commits. The comparison report records current Python source hashes; SHA-256 identities of this correction's two files follow:

- `skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_fixture.py`: `b4df1c31a84a7c317e709829b26602cab0aeb5eeec5e84590c8ba3e9c1740996`
- `skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py`: `6a209245619d9d6c25f4e7523f236053a6c5bb0b0d6acf88ef7ee76fd37fcbc2`

## Complete prior-ledger continuity

These are prior reviewer statuses, not newly issued review results. Implementation evidence is separate. Before editing, failed rows were mapped to the regression/full fixture check, blocked V-11d to its external owner and every other prior pass to navigation plus fresh-review coverage. No finding or scenario is dropped.

| Row ID | Prior status | Correction evidence / next owner |
|---|---|---|
| V-01a | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01b | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01c | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01d | fail | F-01 correction: fail-first regression then focused/full check passed; fresh discovery must corroborate; separate acceptance decides disposition. |
| V-01f-tools | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01f-settings | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01f-checks | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01g | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01h | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-02a | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-02b | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-02c | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-02d | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-03a | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-03b | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-03c-rename | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-03c-move | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-03c-extract | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-03d | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-03e-docs | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-03e-unsupported | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04a-complexity | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04a-statements | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04a-arguments | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04b-complexity | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04b-statements | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04b-arguments | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04c-complexity | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04c-statements | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04c-arguments | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04d-complexity | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04d-statements | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04d-arguments | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04e-complexity | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04e-statements | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04e-arguments | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04f-complexity | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04f-statements | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04f-arguments | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04g-complexity | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04g-statements | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04g-arguments | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04h | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04i | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04j | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-04k | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05a-advisory | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05a-required | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05b-advisory | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05b-required | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05c-advisory | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05c-required | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05d-advisory | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05d-required | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05e-advisory | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05e-required | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05f-advisory | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-05f-required | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-07a | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-07b | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-07c | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-07d | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08a | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08b | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08c | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08d | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08e | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08f | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08g | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08h | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08i | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-08j | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-09a | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-09b | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-09c | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-09d | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-10a | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-10b | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-10c | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-10d-significant | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-10d-trivial | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-10e | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-11a | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-11b | fail | F-01 correction: fail-first regression then focused/full check passed; fresh discovery must corroborate; separate acceptance decides disposition. |
| V-11c | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-11d | blocked | External registry-updater owns synchronization; current structural checker passes but is not proof of semantic completion. Fresh discovery/acceptance own review/disposition. |
| V-06-1 | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-06-2 | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-06-3 | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-06-4 | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-06-5 | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-06-6 | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01e-added | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |
| V-01e-removed | pass | Prior source/preparation evidence remains navigation only; full fixture check passed; fresh discovery owns current corroboration. |

F-01 remains an open reviewer finding until separately assessed. Correction owner: this implementation invocation; evidence owner: fresh independent discovery; authority/decision owner: separate acceptance under the task contract. This session authored the correction and cannot provide independent discovery for these bytes. Live agent behavior remains unqualified.

Next: re-enter affected maintainability review, finish the separately owned registry stage, then fresh independent discovery and separate acceptance. Preserve discovery-01.md and its full scope/ledger/command context; do not overwrite it. Existing staged diff SHA-256 was unchanged at the correction check: a51a27099a8a689f6f262949d02b424f45db31a393491fd9b9db6d941fa7b11a. Fixes are unstaged for review.
