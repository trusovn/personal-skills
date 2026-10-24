# Orchestrator maintainability cleanup experiment

Date: 2026-10-23

The selected hotspot now meets the experiment's 10/50/5 limits, together with
all extracted helpers. Behavioral checks passed. This is implementation
evidence; it is not an independent maintainability or acceptance verdict.

## Scope and selection

The starting worktree was clean at commit
`9b32cfa4a4ced8c8258651539468586b33713ac3`. The full default profile measured
the five Python files under `skills/task-orchestrator/scripts` before edits.
`controller_state.validate_ledger` was the largest hotspot: Radon complexity
89, against 87 for `controller._load_inspection_authority`. Ruff reported
103 statements in `validate_ledger`.

The cleanup changes only that validator's implementation, its owning tests,
and this report. The original public function, compatibility alias, messages,
and validation sequence remain. Existing actor-operation and input-revision
validators are still called at the same points. No installed skills were
refreshed. Inspection of `scripts/install_development_skills.py` confirmed that
`task-orchestrator` is outside its selected profile; no installer change was
needed. Tooling, targets, and exclusions were not changed.

## Result and extraction relationship

All rows below came from the original `validate_ledger`; these are extracted
responsibilities, not thirteen unrelated additions. They remain adjacent in
`controller_state.py`. The public function orders the checks and dispatches
state-specific rules. The readiness check now collects actual and expected
ready tasks in one traversal after collecting completed tasks.

| Current symbol | Radon complexity | Ruff statements | Ruff arguments |
|---|---:|---:|---:|
| `validate_ledger` | 10 | 24 | 1 |
| `_validate_ledger_header` | 7 | 9 | 1 |
| `_validate_ledger_flow_reference` | 5 | 5 | 1 |
| `_validate_ledger_cursor_fields` | 5 | 5 | 1 |
| `_validate_ledger_closure_references` | 9 | 11 | 1 |
| `_validate_ledger_tasks` | 9 | 13 | 1 |
| `_ledger_attempt_owners` | 4 | 4 | 1 |
| `_validate_ledger_task_ownership` | 7 | 6 | 2 |
| `_validate_ledger_selection` | 8 | 9 | 1 |
| `_validate_idle_ledger` | 6 | 5 | 1 |
| `_validate_ready_ledger` | 10 | 10 | 1 |
| `_validate_running_ledger` | 6 | 8 | 3 |
| `_validate_closed_attempt_ledger` | 6 | 10 | 2 |
| `_validate_ledger_finalization_references` | 9 | 7 | 2 |

The comparison is complete and compatible: one improved original symbol,
13 new helpers, and 156 unchanged symbols. No existing function's complexity
increased. There are zero required-response items and no target diagnostics
on the changed function or its helpers. Across the requested folder, legacy
complexity breaches fell from 44 to 43; Ruff diagnostics fell from 25 to 24.
Other hotspots remain outside this cleanup.

Statement and argument values in the table come from a separate native Ruff
probe with command-line limits set to zero. Its source hash matches the final
comparison. This exposes native counts for these undecorated functions without
changing repository configuration. It does not upgrade the runner's general
statement/argument comparison capability, including native exemption handling.

The cost is 13 private helpers and 66 extra implementation lines. Most decisions
still exist: summing complexity gives 101 across 14 functions, against 89 in
the original function, because each function contributes a base point. The
useful improvement is the size of each responsibility and its explicit inputs,
not that sum. No runtime performance improvement is claimed.

A concrete maintenance exercise: another running-attempt ownership rule belongs
in `_validate_running_ledger`, which receives the ledger, selected task, and
attempt-owner map. Its behavioral case belongs beside
`test_running_active_attempt_must_be_latest`. A closure-reference pairing rule
belongs in `_validate_ledger_closure_references`, with the existing reference
tests. Neither requires learning transport or inspection implementation.

## Verification

The original owning suite passed 44 tests before edits. The expanded suite
passed 45 tests against the original implementation before the refactor and
again against the final implementation. Existing fixtures and corruption cases
were reused. New cases cover malformed flow/cursor fields and malformed task
identity/history; rejection also checks that input data stays unchanged.

| Command | Result |
|---|---|
| `python3 -B -m unittest skills/task-orchestrator/tests/test_controller_state.py` | 45 passed |
| `python3 -B -m unittest skills.task-orchestrator.tests.test_controller.ControllerContractTest skills.task-orchestrator.tests.test_controller.ControllerReservationTest skills.task-orchestrator.tests.test_controller.ControllerInputRevisionTest` | 57 passed, 8.167 seconds; real local locks, reservations, revisions, and persisted files |
| `python3 -B -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_full_init_and_run_next_flow` | 1 passed; local fake worker and real controller/Git/file flow |
| `.quality/venv/bin/python -B -m unittest discover -s tests -p test_maintainability.py -v` | 11 passed; real Radon and Ruff, no skips |
| `python3 -B .quality/reports/orchestrator-cleanup-differential.py` | 44 reused tests passed; 105 validator calls matched: 34 accepted, 71 rejected |
| `git diff --check` | Passed; hygiene evidence only |

The differential probe loads original source bytes from the pre-edit report,
then compares return values, exception types/messages, and resulting input data
against the refactor for each observed validator call. It is a characterization
check, not an independent contract oracle or exhaustive equivalence proof.
Its first run encountered the direct-import provenance test because the probe
wraps the validator. The probe now excludes that structural test; the normal
45-test suite still runs it against the real implementation. No production or
test assertion was weakened to accommodate the probe.

The full orchestrator suite, live model calls, verification-containment runs,
and independent agent reviews were not run. The selected local evidence
addresses this pure validator refactor; it does not qualify the entire harness.

## Tooling and agent interaction findings

1. **The feedback loop worked.** The first post-edit comparison flagged
   `_validate_ready_ledger` at 11. Sharing a traversal reduced it to 10. The
   second comparison had zero response items. No threshold change or suppression
   was needed. Measurements took less than a second in this environment.
2. **Console feedback needs the changed symbols.** The summary prints only the
   five largest folder hotspots and a response count. These remain unrelated
   legacy functions after this cleanup. JSON inspection was necessary to find
   the new 11-point helper and assess the target's improvement. A useful next
   tooling change is to print required-response identities and changed-symbol
   deltas before the legacy top five.
3. **Extraction attribution is manual.** The original name remains, so the
   runner labels it improved and labels its helpers new. It does not bind the
   family or measure navigation cost. The table above supplies that relationship.
   Zero response items must not be interpreted as semantic approval.
4. **Native count probing looks useful.** The zero-limit Ruff probe returned
   exact counts for all 14 selected functions. This is a candidate for a later
   tested adapter experiment, with exemptions and boundaries proved before
   claiming a full inventory. The adopted runner still truthfully reports its
   below-target comparison gap.
5. **Do not tune targets from one successful sample.** Keep 10/50/5 provisional.
   Ten is achievable here, but helper count is a real cost. For example, inlining
   the five-line flow-reference helper would put the combined header at 11.
   A fresh reviewer should judge whether that split aids maintenance before
   deciding that 10 is the right general calibration. Fifty statements and five
   arguments were not restrictive for the extracted checks.
6. **Skill integration remains manual.** The active project-local implementer
   and testing skills were used with their sibling evidence tooling. The
   standalone metrics command was selected explicitly; it was not automatically
   discovered or invoked by those skills. Optional evidence availability,
   active-run lookup, and begin succeeded. This was one implementer session,
   not a live multi-agent evaluation or proof of automated review routing.

## Evidence and next review

Local machine reports are intentionally ignored by Git:

- `.quality/reports/orchestrator-cleanup-before.json` and sibling `.txt`:
  baseline with exact original source snapshots.
- `.quality/reports/orchestrator-cleanup-after-01.json`: first comparison,
  including the new complexity-11 helper.
- `.quality/reports/orchestrator-cleanup-after-02.json` and sibling `.txt`:
  final comparison under the unchanged default profile.
- `.quality/reports/orchestrator-cleanup-final.json` and sibling `.txt`:
  confirmation after writing this report; identical source measurements.
- `.quality/reports/orchestrator-cleanup-native-counts.json`: separate native
  count probe, exact command, source hash, and raw output.
- `.quality/reports/orchestrator-cleanup-differential.py`: local probe to rerun
  against the preserved baseline.

The baseline and comparison commands were:

```sh
python3 scripts/measure_maintainability.py baseline skills/task-orchestrator/scripts --output .quality/reports/orchestrator-cleanup-before.json
python3 scripts/measure_maintainability.py compare skills/task-orchestrator/scripts --baseline .quality/reports/orchestrator-cleanup-before.json --output .quality/reports/orchestrator-cleanup-after-02.json
```

Reports refuse overwriting; choose a fresh output path for another comparison.
Both reports used Python 3.14.6, Radon 6.0.1, and Ruff 0.14.2. Optional run
evidence belongs to `run-20261023T193146Z-5d1bc7c49bbb` under
`.git/personal-skills/run-evidence/runs/`.

Implemented: READY_FOR_REVIEW. For independent assessment, the next invocation
should run fresh `task-maintainability-review` on this extraction and its
reports, then fresh independent `task-review-discovery`, then a separate
`task-acceptance-review` decision. No repository architecture gate or contract
registry update applies to this internal refactor. The key review question is
whether the new navigation boundaries justify their helper count; the metrics
and this author's reading exercise cannot settle that independently.
