# Task Review Discovery Report: T-001.1 — Portable, target-aware measurement runtime

| Field | Value |
|---|---|
| Producing stage | task-review-discovery, project-local installed skill |
| Coverage completeness | complete — all 37 carried material rows have current targeted evidence |
| Discovery iteration | Correction pass 1; follows discovery-01.md and F-01 correction |
| Created at | 2026-10-24T18:31:53.755406+00:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report | docs/tasks/T-001.1/reviews/discovery-02.md |
| Task brief | docs/tasks/T-001.1/brief.md |
| Verification / context | verification.md revision 1; preflight.md including Decision context; parent T-001/brief.md |
| Current submission | implementation.md, F-01 correction, READY_FOR_REVIEW; producer claims kept separate from independent results |
| Conditional evidence | maintainability-02.md, with unchanged-scope evidence from maintainability-01.md; current registry/reference synchronization |

This report publishes evidence only. It contains no acceptance verdict, approved
deferral or advancement. It applies only to the identified reviewed bytes and
does not review or authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production, test, fixture or harness bytes.
It previously authored maintainability-02.md and the measurement registry summary
in separate user-invoked stages; that documentary authorship is explicit and is
not production authorship. The present discovery invocation writes only this
report in the repository. No implementation, test, prior report, plan or active
installation was edited. Testing-discipline guidance from the same project-local
installation was used for test inspection.

HEAD: `ab9bac8ea13be3ef325750cfc0b00930f5906539`. Actual index SHA-256:
`21d94f36114303731abeaea158b76b1df18f80e5709ec3c13caaa3c0465cdbf7`. The staged diff is empty.
Captured full Git status, worktree SHA-256 identities and separate index entries
before probes. Rechecked all captured files, exact status, index bytes and index
entries before this write. All match. Current source `.quality/` policy and pin
bytes also match the supplied pre-correction manifest. The plan and task-map
hashes match the parent brief. Historical preparation statements about staged
planning documents do not establish today's index state.

## 2. Findings and correction continuity

No current findings.

**F-01 [prior suggested P2] — corrected behavior corroborated.** Prior discovery
observed a Boolean complexity target accepted as numeric and a string exclusion
interpreted as characters, exposing excluded `.git` Python. Current authority is
AC-02/AC-04 and R-01: effective policy must be valid before it controls scanning
or publication. Locations: scripts/maintainability.py:34 (validation) and :51
(settings resolution). R1 repeats both original triggers through an installed
launcher against a distinct target, with an invalid Python sentinel under `.git`.
Nineteen invalid/missing-field cases now exit 2, identify the policy path and
field, publish no report and preserve the whole target tree. The restored valid
control completes and excludes the sentinel. R2 independently executes the
producer's durable installed regression: seventeen invalid/missing cases, default
control and valid custom profile/zero target/subset/empty exclusions control.

Credible sibling surfaces retained from F-01: profile, supported checks,
complexity_target and exclude_directories, including Boolean/integer confusion
and string/list confusion. The common validator covers target and shipped policy;
R1/R2 supply current public-boundary evidence. The original DISC-07 reproducer
asserts defective success, so it is not reused unchanged as a success oracle.
Its corrected equivalent is R1 (source retained below) plus R2's durable test.
No correction, evidence or authority owner is conflated: implementer supplied
the correction and M/I claims; this discovery supplies corroboration; the separate
acceptance call owns disposition and advancement. F-01 is retained, not recycled.

## 3. Completeness ledger

All rows are required/material. Each has the following columns:
AC/invariant, explicit case and setup/oracle, producer evidence, prior discovery
state, current independent probe and result. The cases/oracles below retain the
prior ledger identities; prior passes were navigation only. Producer evidence
refers to implementation.md's scenario map and correction result, not acceptance.
R1–R7 are expanded into exact commands and observations in section 5.

| Row ID | AC / invariant | Explicit cases and setup/oracle | Submitted evidence | Prior state | Current independent evidence | Result |
|---|---|---|---|---|---|---|
| V-01a | AC-01 / local runtime | Disposable distribution installed, then removed; unrelated cwd, no Python helper path; baseline CC 2 then edit and compare CC 3/+1; measure; JSON/text and baseline preservation | Launcher journey | pass | R3 | pass |
| V-01b | AC-01 / local runtime | Disposable distribution installed, then removed; unrelated cwd, no Python helper path; baseline CC 2 then edit and compare CC 3/+1; measure; JSON/text and baseline preservation | Launcher journey | pass | R3 | pass |
| V-02a | AC-01/02 / independent policy | Neither, maintainability only, Ruff only, both; counts remain constant, effective targets/origins/paths/hashes match | Four settings states | pass | R1, R2 | pass |
| V-02b | AC-01/02 / independent policy | Neither, maintainability only, Ruff only, both; counts remain constant, effective targets/origins/paths/hashes match | Four settings states | pass | R1, R2 | pass |
| V-02c | AC-01/02 / independent policy | Neither, maintainability only, Ruff only, both; counts remain constant, effective targets/origins/paths/hashes match | Four settings states | pass | R1, R2 | pass |
| V-02d | AC-01/02 / independent policy | Neither, maintainability only, Ruff only, both; counts remain constant, effective targets/origins/paths/hashes match | Four settings states | pass | R1, R2 | pass |
| V-03a | AC-02 / invalid present syntax | Each family independently contains `[invalid TOML`; exit 2 naming file, no successful fallback; bad bytes preserved | Malformed settings case | pass | R1, R2 | pass |
| V-03b | AC-02 / invalid present syntax | Each family independently contains `[invalid TOML`; exit 2 naming file, no successful fallback; bad bytes preserved | Malformed settings case | pass | R1, R2 | pass |
| V-03c | AC-02 / no root Ruff inheritance | Root Ruff `ignore = ["ALL"]` present/absent with target Ruff and with fallback; unchanged native values/settings identity and root bytes | Same settings case | pass | R1, R2 | pass |
| V-03-semantic | AC-02/04 / typed valid policy | Valid control, Boolean threshold, string exclusion; invalid policy must fail before it can claim a complete report or scan excluded files | F-01 correction: installed regression with 17 invalid/missing inputs and two valid controls; producer R/M/I results | fail — F-01 | R1, R2 | pass |
| V-04 | AC-03 / setup ownership | Replay printed recipe at EnvBuilder/pip seams; target native destination and adjacent installation pin path; no network or actual package installation | Setup dispatch case | pass — selection only | R3 | pass |
| V-05a | AC-03 / native key | Change OS, CPU, implementation, patch version, installation pins separately; key differs. Target pins do not change key | Key-separation case | pass | R3 | pass |
| V-05b | AC-03 / native key | Change OS, CPU, implementation, patch version, installation pins separately; key differs. Target pins do not change key | Key-separation case | pass | R3 | pass |
| V-05c | AC-03 / native key | Change OS, CPU, implementation, patch version, installation pins separately; key differs. Target pins do not change key | Key-separation case | pass | R3 | pass |
| V-05d | AC-03 / native key | Change OS, CPU, implementation, patch version, installation pins separately; key differs. Target pins do not change key | Key-separation case | pass | R3 | pass |
| V-05e | AC-03 / native key | Change OS, CPU, implementation, patch version, installation pins separately; key differs. Target pins do not change key | Key-separation case | pass | R3 | pass |
| V-05f | AC-03 / real interpreter selection | Prepared disposable native environment, unpinned caller, unusable foreign/legacy sentinels; real adapter and exact analyzer versions through target interpreter | Seeded native case | pass | R3 | pass |
| V-06a | AC-03 / pinned caller | Pinned caller completes and creates no target environment | Launcher journey | pass | R3 | pass |
| V-06b | AC-03 / no implicit provisioning | Missing pins under `-S`; exit 2, shell-parsable target-aware recipe with spaces; complete target tree/index unchanged | Missing-pin recipe case | pass | R3 | pass |
| V-07 | AC-04 / actual source and index | Commit CC2, stage CC3, worktree CC4, untracked CC1; decode sources/hashes; edit worktree to CC5 and compare +1; preserve index/staged/saved JSON/text | Dirty snapshot case | pass | R3 | pass |
| V-08a | AC-04 / native/advisory | CC2/10/11/16, below/equal/above target, decrease, unchanged breach, crossing and new breach; breach CLI exits 0 | Native boundary and console cases | pass | R4 | pass |
| V-08b | AC-04 / symbol identity | Nested/local class/async and duplicate names; added/removed/renamed symbols; no guessed identity | Native identity cases | pass | R4 | pass |
| V-08c | AC-04 / Ruff semantics | Real argument/statement counts and native exemptions; collection limits zero and advisory targets distinct; noqa ignored | Ruff real/changes/count cases | pass | R4 | pass |
| V-08d | AC-04 / unknown evidence | Missing→present and present→missing for zero args, return-only, override/overload; missing values/deltas null | Ruff unknown case | pass | R4 | pass |
| V-08e | AC-04 / groups and exclusions | Implementation/test/eval groups; nested invalid Python excluded; explicit excluded scope rejected; installed/runtime resources excluded under valid policy | Directory case and installed journeys | pass for valid policy; invalid-type boundary separately fails above | R4 | pass |
| V-09a | AC-04 / selected checks | Real complexity-only CLI exits 0 with full_profile false | Directory case | pass | R4 partial-profile public CLI | pass |
| V-09b | AC-04 / partial availability | Controlled Ruff discovery absence; completed Radon retained, Ruff unavailable, CLI exit 2 | Partial completion case | pass | R5 | pass |
| V-09c | AC-04 / failed/concurrent source | Invalid Python and source mutation after capture; incomplete observations and exit 2 | Partial/concurrent cases | pass | R5 | pass |
| V-09d | AC-04 / compatibility | Independent tools/policy/Ruff/adapter/collection/interpreter mutations and incomplete baseline rejected; mount/patch compatible | Compatibility and mount cases | pass | R5, R7 effective policy and origin comparison | pass |
| V-09e | AC-04 / scope coverage | Folder baseline; affected new/deleted files; untouched outside subset retained; outside coverage rejected | Folder case | pass | R5 | pass |
| V-09f | AC-04 / path scope | Folder/file and absolute in-root work; escaping/symlink rejected | Directory and CLI handoff cases | pass | R4 escaping/excluded/symlink scopes; R5 valid scope and handoff | pass |
| V-10a | AC-04/05 / saved evidence | Occupied JSON and sibling-only text independently refused, exit 2, all saved bytes preserved | No-overwrite case | pass | R5 | pass |
| V-10b | AC-04/05 / saved evidence | Occupied JSON and sibling-only text independently refused, exit 2, all saved bytes preserved | No-overwrite case | pass | R5 | pass |
| V-11 | AC-05 / narrow ownership | Fresh/refresh committed and unborn targets; staged/dirty/untracked source/index, unmanaged helpers/skills, policy/env/JSON/text sentinels and outside AGENTS bytes preserved | Installer journey and line-ending case | pass | R6 | pass |
| V-12a | AC-05 / exact drift | Every six managed files changed/removed independently; two read-only checks, exact category/path, refresh/recheck, complete tree/index preserved | All-resource lifecycle case | pass | R6 | pass |
| V-12b | AC-05 / exact drift | Every six managed files changed/removed independently; two read-only checks, exact category/path, refresh/recheck, complete tree/index preserved | All-resource lifecycle case | pass | R6 | pass |
| V-13 | AC-01/05 / declaration coherence | Installer six-resource membership, README/profile guide/launcher guide/maps, shipped vs target policy and narrow ownership agree | Membership and documentation trace | pass — documentary/structural, not runtime proof | R6 membership plus current code/registry/README/map/AGENTS trace | pass |

The frozen 37-row ledger was created before probes, then reconciled against brief
AC-01–05, finite risks R-01/R-02, verification revision 1 and the scoped diff
before either owning-suite aggregate. All R1–R7 results were clean; no selected
adversarial probe remained, no required row was blocked/unchecked, and no new
material omission was identified. This is bounded discovery, not exhaustive
input or platform qualification.

## 4. Adversarial and stateful checks

- Separate disposable distribution, installation, measured target and unrelated
  cwd; remove the distribution before execution. R1 uses custom threshold 7 and
  Ruff targets 1/4, independently from the producer's 3 and 2/3 matrix.
- Cross all four target-settings presence states. R2 separately exercises both
  malformed files and conflicting root Ruff configuration under both origins.
- R1 checks original F-01 type confusions, invalid sibling fields and a successful
  restored control. R2 covers valid zero target, subset, empty exclusions and
  custom profile. Full tree snapshots include real index and saved evidence.
- R3 executes baseline, actual source edits and comparison, and observes actual
  staged/unstaged/untracked snapshots with decoded source/hash and saved JSON/text
  preservation. Native interpreter selection reaches the real analyzer process.
- R6 removes/changes each managed resource, checks twice, explicitly refreshes,
  then checks again. Fresh/refresh committed and unborn journeys preserve source,
  index, unmanaged content, policy, environments, reports and outside-marker
  AGENTS line-ending bytes. R1 adds a distinct separate-target refresh probe.
- R7 creates a real baseline, changes effective policy, observes incompatible
  exit 2, restores identical policy bytes at a new origin, edits source and
  observes compatible CC 2→3 (+1), preserving baseline JSON and text.
- There is no changed daemon/process-lifecycle, concurrency scheduler or retry
  contract in this task. Child calls are synchronous; custom probes have 20/30 s
  child timeouts, runner invocations have 120 s bounds, disposable fixtures clean
  up, and no daemon is launched. Custom probes confirm their targets disappear.
  No network, package download, privilege escalation or live model check ran.
- No changed JSON Schema/OpenAPI validation boundary exists. The relevant
  executable policy validator is exercised through real CLI valid/invalid inputs
  in R1/R2; registry shape validation is recorded separately as structural proof.

## 5. Commands and independent results

All runs below were made during this discovery pass. The local runner command
was `python3 -B /tmp/T-001.1-discovery2/run.py <ID>`; it records and executes the
exact child command below, with captured stdout/stderr and a 120 s timeout.
For custom probes, source is included in the appendices. Native analyzer cases
use the prepared interpreter, real Radon 6.0.1 and Ruff 0.14.2. No skip occurred.

### R1

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills`.

```sh
/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B /tmp/T-001.1-discovery2/boundary_probe.py
```

Exit 0; elapsed 2.562 s.

```text
matrix False False PASS
matrix True False PASS
matrix False True PASS
matrix True True PASS
F-01 regression and sibling policy fields: 19 invalid cases rejected; no writes
Restored valid policy control excludes hidden invalid Python: PASS
missing/check/recheck/refresh preservation PASS
temporary targets removed: True
```

### R2

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills`.

```sh
/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py -k settings -v
```

Exit 0; elapsed 3.422 s.

```text
test_invalid_policy_settings_fail_before_measurement (test_maintainability.MeasurementTests.test_invalid_policy_settings_fail_before_measurement) ... ok
test_invalid_target_settings_and_unrelated_root_ruff (test_maintainability.MeasurementTests.test_invalid_target_settings_and_unrelated_root_ruff) ... ok
test_settings_select_each_target_file_independently (test_maintainability.MeasurementTests.test_settings_select_each_target_file_independently) ... ok

----------------------------------------------------------------------
Ran 3 tests in 3.336s

OK
```

### R3

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills/tests`.

```sh
/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest test_maintainability.MeasurementTests.test_installed_and_source_launchers_work_without_distribution test_maintainability.LauncherTests.test_environment_key_separates_native_runtimes_and_dependency_versions test_maintainability.LauncherTests.test_missing_pins_recipe_dispatches_setup_for_selected_target test_maintainability.LauncherTests.test_native_target_environment_reaches_real_adapter test_maintainability.MeasurementTests.test_snapshot_preserves_staged_unstaged_untracked_and_index -v
```

Exit 0; elapsed 2.041 s.

```text
test_installed_and_source_launchers_work_without_distribution (test_maintainability.MeasurementTests.test_installed_and_source_launchers_work_without_distribution) ... ok
test_environment_key_separates_native_runtimes_and_dependency_versions (test_maintainability.LauncherTests.test_environment_key_separates_native_runtimes_and_dependency_versions) ... ok
test_missing_pins_recipe_dispatches_setup_for_selected_target (test_maintainability.LauncherTests.test_missing_pins_recipe_dispatches_setup_for_selected_target) ... ok
test_native_target_environment_reaches_real_adapter (test_maintainability.LauncherTests.test_native_target_environment_reaches_real_adapter) ... ok
test_snapshot_preserves_staged_unstaged_untracked_and_index (test_maintainability.MeasurementTests.test_snapshot_preserves_staged_unstaged_untracked_and_index) ... ok

----------------------------------------------------------------------
Ran 5 tests in 1.955s

OK
```

### R4

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills/tests`.

```sh
/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest test_maintainability.MeasurementTests.test_real_complexity_boundaries_and_below_target_increase test_maintainability.MeasurementTests.test_nested_scopes_async_and_duplicate_names_are_not_conflated test_maintainability.MeasurementTests.test_added_and_removed_symbols_need_interpretation_without_guessing_relationships test_maintainability.MeasurementTests.test_ruff_real_diagnostics_and_override_exemption test_maintainability.MeasurementTests.test_ruff_statement_changes_keep_advisory_targets test_maintainability.MeasurementTests.test_ruff_native_counts_distinguish_improvement_and_worsening test_maintainability.MeasurementTests.test_ruff_missing_diagnostics_never_become_numeric_zero test_maintainability.MeasurementTests.test_directory_exclusions_selected_check_and_empty_scope test_maintainability.MeasurementTests.test_console_compare_prints_identities_and_deltas_before_top_five -v
```

Exit 0; elapsed 2.185 s.

```text
test_real_complexity_boundaries_and_below_target_increase (test_maintainability.MeasurementTests.test_real_complexity_boundaries_and_below_target_increase) ... ok
test_nested_scopes_async_and_duplicate_names_are_not_conflated (test_maintainability.MeasurementTests.test_nested_scopes_async_and_duplicate_names_are_not_conflated) ... ok
test_added_and_removed_symbols_need_interpretation_without_guessing_relationships (test_maintainability.MeasurementTests.test_added_and_removed_symbols_need_interpretation_without_guessing_relationships) ... ok
test_ruff_real_diagnostics_and_override_exemption (test_maintainability.MeasurementTests.test_ruff_real_diagnostics_and_override_exemption) ... ok
test_ruff_statement_changes_keep_advisory_targets (test_maintainability.MeasurementTests.test_ruff_statement_changes_keep_advisory_targets) ... ok
test_ruff_native_counts_distinguish_improvement_and_worsening (test_maintainability.MeasurementTests.test_ruff_native_counts_distinguish_improvement_and_worsening) ... ok
test_ruff_missing_diagnostics_never_become_numeric_zero (test_maintainability.MeasurementTests.test_ruff_missing_diagnostics_never_become_numeric_zero) ... ok
test_directory_exclusions_selected_check_and_empty_scope (test_maintainability.MeasurementTests.test_directory_exclusions_selected_check_and_empty_scope) ... ok
test_console_compare_prints_identities_and_deltas_before_top_five (test_maintainability.MeasurementTests.test_console_compare_prints_identities_and_deltas_before_top_five) ... ok

----------------------------------------------------------------------
Ran 9 tests in 2.099s

OK
```

### R5

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills/tests`.

```sh
/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest test_maintainability.MeasurementTests.test_partial_completion_missing_tool_and_invalid_python test_maintainability.MeasurementTests.test_concurrent_input_change_marks_results_incomplete test_maintainability.MeasurementTests.test_incompatible_scope_tool_configuration_and_failed_baseline test_maintainability.MeasurementTests.test_report_can_be_compared_from_a_different_mount_path test_maintainability.MeasurementTests.test_folder_baseline_can_compare_affected_new_and_deleted_files test_maintainability.MeasurementTests.test_cli_report_handoff_uses_target_root_for_relative_report_paths test_maintainability.MeasurementTests.test_cli_file_scope_baseline_comparison_and_no_overwrite -v
```

Exit 0; elapsed 2.142 s.

```text
test_partial_completion_missing_tool_and_invalid_python (test_maintainability.MeasurementTests.test_partial_completion_missing_tool_and_invalid_python) ... ok
test_concurrent_input_change_marks_results_incomplete (test_maintainability.MeasurementTests.test_concurrent_input_change_marks_results_incomplete) ... ok
test_incompatible_scope_tool_configuration_and_failed_baseline (test_maintainability.MeasurementTests.test_incompatible_scope_tool_configuration_and_failed_baseline) ... ok
test_report_can_be_compared_from_a_different_mount_path (test_maintainability.MeasurementTests.test_report_can_be_compared_from_a_different_mount_path) ... ok
test_folder_baseline_can_compare_affected_new_and_deleted_files (test_maintainability.MeasurementTests.test_folder_baseline_can_compare_affected_new_and_deleted_files) ... ok
test_cli_report_handoff_uses_target_root_for_relative_report_paths (test_maintainability.MeasurementTests.test_cli_report_handoff_uses_target_root_for_relative_report_paths) ... ok
test_cli_file_scope_baseline_comparison_and_no_overwrite (test_maintainability.MeasurementTests.test_cli_file_scope_baseline_comparison_and_no_overwrite) ... ok

----------------------------------------------------------------------
Ran 7 tests in 2.056s

OK
```

### R6

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills/tests`.

```sh
python3 -B -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_measurement_resources_changed_missing_checks_and_refresh test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family test_install_development_skills.DevelopmentProfileCheckTests.test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_contains_repo_stage_and_bounded_delivery_skills -v
```

Exit 0; elapsed 12.307 s.

```text
test_measurement_resources_changed_missing_checks_and_refresh (test_install_development_skills.DevelopmentProfileCheckTests.test_measurement_resources_changed_missing_checks_and_refresh) ... ok
test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family (test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family) ... ok
test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes (test_install_development_skills.DevelopmentProfileCheckTests.test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes) ... ok
test_profile_contains_repo_stage_and_bounded_delivery_skills (test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_contains_repo_stage_and_bounded_delivery_skills) ... ok

----------------------------------------------------------------------
Ran 4 tests in 12.243s

OK
```

### R7

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills`.

```sh
/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B /tmp/T-001.1-discovery2/policy_compare_probe.py
```

Exit 0; elapsed 0.344 s.

```text
Changed effective policy: incompatible exit 2; identical policy from target origin: compatible CC 2->3 (+1); baseline JSON/text preserved.
Disposable comparison target cleaned: True
```

### M

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills`.

```sh
/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py
```

Exit 0; elapsed 9.699 s.

```text
..........................
----------------------------------------------------------------------
Ran 26 tests in 9.612s

OK
```

### I

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills`.

```sh
python3 -B -m unittest discover -s tests -p test_install_development_skills.py
```

Exit 0; elapsed 24.473 s.

```text
....................................
----------------------------------------------------------------------
Ran 36 tests in 24.409s

OK
```

### A

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills`.

```sh
python3 -B -m unittest discover -s tests -p test_architecture.py
```

Exit 0; elapsed 0.208 s.

```text
....
----------------------------------------------------------------------
Ran 4 tests in 0.166s

OK
```

### C

Cwd: `/Users/mtrusov/work/skill-sources/personal-skills`.

```sh
python3 -B tools/check_contracts.py --root .
```

Exit 0; elapsed 0.038 s.

```text
contract registry OK: 6 subsystem(s), 7 indexed plan ref(s)
```

## 6. Aggregate-gate ownership and reconciliation

| Gate | Current result | Owner / stage | Reason |
|---|---|---|---|
| Native Python `-B -m unittest discover -s tests -p test_maintainability.py` (M) | pass; 26 tests, no skips | This correction discovery | Ran after clean targeted R1–R7 and full ledger reconciliation; current corrected bytes, not copied producer or prior results. |
| `python3 -B -m unittest discover -s tests -p test_install_development_skills.py` (I) | pass; 36 tests, no skips | This correction discovery | Owning distribution regression gate after targeted lifecycle proof; follows M. |
| Architecture (A) | pass; 4 tests, no skips | Repository-required handoff check; current discovery | Same architecture policy as the canonical command; `-B` disables bytecode writes. Structural proof only. |
| Registry (C) | pass; 6 subsystems, 7 indexed plan refs | Repository-required contract check; current discovery | Checks current synchronized registry, not functional qualification. |
| `python3 tools/verify.py` | not run | T-001.3 final composition | Explicit leaf brief ownership. No waiver and no copied aggregate pass. |

Initial discovery's aggregate suppression after F-01 remains a truthful prior
record. This correction pass owns fresh M/I results after its clean targeted
probes. No premature aggregate or later omitted material row was identified.

## 7. Scope, conditional evidence and reviewed identities

Implementation scope: public launcher, relocated adapter/environment helpers,
three shipped defaults/pin resources, explicit installer membership, both owning
test modules and the allowed README/guide/map updates. Deleted tools modules
are intentional relocation; current scripts were compared with the old HEAD
modules. Registry-stage files are measurement.json, installation.json, generated
index.json and their existing development-guide explanation. Current registry
summary additionally describes the corrected typed policy boundary. It preserves
ART-001/IF-001 and the existing invariants, and explicitly leaves neutral labels
and valid empty folder baselines to T-001.2. README, guide, maps and AGENTS routing
remain coherent with the implementation; no unexplained production overlap.

maintainability-02.md's 14 reviewed file hashes all still match current bytes;
its current ACCEPT is conditional maintainability evidence only, not functional
acceptance. Registry synchronization has completed and C validates its current
shape. This session's prior registry authorship is disclosed in section 1.
Parent/sibling task packages and existing reports are context, not implementation
attributed to this leaf. No source/test/executable-contract byte changed during
this discovery, so no affected maintainability/registry stage is newly owed.

Authority and submission identities (SHA-256):

```text
e38fb7e8e978aa3b16df91fa0b6d10d2b928d08af7bc2119a51fdd48709d5d83  docs/tasks/T-001.1/brief.md
3f85c174e7aa7822fc285e0f9e09ec8a93454fff2ed154cc3744cd9616b11b0b  docs/tasks/T-001.1/verification.md
e957959683913dda85343c649c8ec9781a6c9a7301fda4394fa1885509cbd7ac  docs/tasks/T-001.1/preflight.md
6bbedfc44a52648f24aa8506bdcbefb8572a6ac6f5082ef62df6609fb71804f2  docs/tasks/T-001.1/implementation.md
9856d3ccfffcd56b4faed20dcf6ea4b49d87c4553292a5ed996cb4e784ca0df7  docs/project-plan.md
952f094d08ad03c5f5dfe18674fdbd710e8851fc8eaff1bdddc6facec2a5c954  docs/task-map.json
f1e8a49d567826e581cc45222d096c0e7f57c00b8b14725a5993cbc00c5e0894  docs/tasks/T-001.1/reviews/maintainability-02.md
```

Current scoped worktree identities (SHA-256):

```text
0c559568b1ec9cf336961222c0855b9b19ce10ddceefb89fac226524b39981de  README.md
60f9b47d36ae5aacf35600ff4bb2775bcd80719fffe199c43aaa25bcc8574659  docs/contracts/index.json
4af6590f6d79bd652d28c4927e82b8e5639da8921a6aefb45878aed0759bb2e9  docs/contracts/installation.json
72e0946a4b2ed0a250d2b8446275f971b9c3b790c7d3d1e1ecc64a8aada31173  docs/contracts/measurement.json
246a3e85d87b1fcc2f2f3ff270128d4f0bc1d6940de5dea575e3e3da9827702e  docs/development.md
e68fb53a19376c37820c1781b474c4972a8b7020b0238d102923ceebd44f4648  docs/project-map.md
a614b7bc21a84f27df588ec150e1c5ccfadd229b562aa3bd967e1e9026a159da  scripts/install_development_skills.py
f258d0e5a0dc070fc9ec33aa0dc000b1959fba9eebdd5cc20e1cb00178a654fb  scripts/maintainability-default.toml
79dbf22b5bc1bc8c10f5746610e937d4f592ebfb3bfc6123d1428cae5e344d44  scripts/maintainability-requirements.txt
a95813db8c5666acfbeae7e1734e7f1a16ad674d1798cc710853e0d3bbb2754b  scripts/maintainability-ruff-default.toml
ef736038b84c35f258f8a1284d1fd9d700de8e2963a0549bd877f8a319b95997  scripts/maintainability.py
54525f713a8865b1a1f26be6c966ffbc5a6c44171ae0727556dbe458c583b9eb  scripts/maintainability_env.py
5dae8e41784b2157fbf91f89d317c5c5ddeb0c432f78551529aadad3d1d38789  scripts/measure-maintainability.md
caa1d0e31fcc04130dd55347f7dc48943a232939156d9fd631f688a0e2fd8b2b  scripts/measure_maintainability.py
bc8930ae9b081c4bf7f030003ebbc7fbe71ae41e54cc27ddce69aa21548eee8d  skills/README.md
a73ea29dbbe97e8070c56247b7e36e2a1147f31e8e12c1a13c688b48aa454f55  tests/test_install_development_skills.py
f37e329e8a5930f015cc25512e01efc7e140817f9b7d270479c1cb53bfdbd5de  tests/test_maintainability.py
DELETED  tools/maintainability.py
DELETED  tools/maintainability_env.py
```

Separate index entries for scoped tracked paths (Git blob IDs):

```text
100644 5873523bb1cddf6a9f4234acd5a76138494a9d7f 0	README.md
100644 be749dcd97b5896a667b94ab3765c11480635007 0	docs/contracts/index.json
100644 7031d1aeb024917cdf8f57de3985be6cf4f84e9d 0	docs/contracts/installation.json
100644 024298eab834138d3f1031c5d37dcb996049cca1 0	docs/development.md
100644 6742fe72de2fc4b94efc1810dea9f673c8bd4f31 0	docs/project-map.md
100644 733660ddf14079482a000e1579254e5cd6dcb08f 0	scripts/install_development_skills.py
100644 4e1ea3a87606acca5f31236af7a2c5971bfc8621 0	scripts/measure-maintainability.md
100644 fcd79ce8b6272de0f3f90ebebaad3b6ac82326d9 0	scripts/measure_maintainability.py
100644 7ca3a9725c632ed8e751785f4a7141cabdee54fe 0	skills/README.md
100644 e99aed8ebdffabff2d2fac1d089e55a66fdf95f4 0	tests/test_install_development_skills.py
100644 9c5dc50ab48b33831fc1b9a77409e0008fe8175b 0	tests/test_maintainability.py
100644 69d15a00278c546364003726ea0d3e6df50514a3 0	tools/maintainability.py
100644 25f8a3aa571772bba82596cb8a6c1f0749531267 0	tools/maintainability_env.py
```

Exact Git status before report write (same as pre-probe capture):

```text
 M README.md
 M docs/contracts/index.json
 M docs/contracts/installation.json
 M docs/development.md
 M docs/project-map.md
 M scripts/install_development_skills.py
 M scripts/measure-maintainability.md
 M scripts/measure_maintainability.py
 M skills/README.md
 M tests/test_install_development_skills.py
 M tests/test_maintainability.py
 D tools/maintainability.py
 D tools/maintainability_env.py
?? docs/contracts/measurement.json
?? docs/tasks/T-001.1/brief.md
?? docs/tasks/T-001.1/implementation.md
?? docs/tasks/T-001.1/preflight.md
?? docs/tasks/T-001.1/reviews/discovery-01.md
?? docs/tasks/T-001.1/reviews/maintainability-01.md
?? docs/tasks/T-001.1/reviews/maintainability-02.md
?? docs/tasks/T-001.1/verification.md
?? docs/tasks/T-001.2/brief.md
?? docs/tasks/T-001.3/brief.md
?? docs/tasks/T-001/brief.md
?? docs/tasks/index.json
?? scripts/maintainability-default.toml
?? scripts/maintainability-requirements.txt
?? scripts/maintainability-ruff-default.toml
?? scripts/maintainability.py
?? scripts/maintainability_env.py
```

Exact Git status after report write (verified):

```text
 M README.md
 M docs/contracts/index.json
 M docs/contracts/installation.json
 M docs/development.md
 M docs/project-map.md
 M scripts/install_development_skills.py
 M scripts/measure-maintainability.md
 M scripts/measure_maintainability.py
 M skills/README.md
 M tests/test_install_development_skills.py
 M tests/test_maintainability.py
 D tools/maintainability.py
 D tools/maintainability_env.py
?? docs/contracts/measurement.json
?? docs/tasks/T-001.1/brief.md
?? docs/tasks/T-001.1/implementation.md
?? docs/tasks/T-001.1/preflight.md
?? docs/tasks/T-001.1/reviews/discovery-01.md
?? docs/tasks/T-001.1/reviews/discovery-02.md
?? docs/tasks/T-001.1/reviews/maintainability-01.md
?? docs/tasks/T-001.1/reviews/maintainability-02.md
?? docs/tasks/T-001.1/verification.md
?? docs/tasks/T-001.2/brief.md
?? docs/tasks/T-001.3/brief.md
?? docs/tasks/T-001/brief.md
?? docs/tasks/index.json
?? scripts/maintainability-default.toml
?? scripts/maintainability-requirements.txt
?? scripts/maintainability-ruff-default.toml
?? scripts/maintainability.py
?? scripts/maintainability_env.py
```

Only the new report entry differs. Worktree hashes and real index bytes/entries
are checked separately, not inferred from short status.

## 8. Questions, unchecked work and residual risks

No required/material row is blocked or unchecked. No unresolved current finding
was confirmed. Actual network dependency provisioning and other operating
systems remain unqualified, as explicitly limited by preflight/brief. Setup
argument observation proves target/pin selection, not package installation.
Schema/registry checks do not establish behavioral success. Metrics remain
advisory; hard checks keep their native authority.

## 9. Coverage completeness and next route

Coverage is complete for the 37 carried rows, with current R1–R7 evidence and
fresh owning-suite M/I results. F-01 corrective behavior is independently
corroborated; this is evidence for a separate decision, not that decision.

Next owner: a separate task-acceptance-review invocation on docs/tasks/T-001.1.
Supply brief.md, current scoped diff, this report, implementation.md,
verification.md revision 1, preflight.md including Decision context, and
maintainability-02.md/current contract records. There are no blocked or unchecked
rows to waive. Do not substitute this report for an acceptance verdict.

## 10. Discovery continuation

```text
Discovery continuation:
- Iteration / identity: correction pass 1; HEAD ab9bac8ea13be3ef325750cfc0b00930f5906539; exact scoped SHA-256 and index identities in section 7.
- Coverage rows: V-01a=pass, V-01b=pass, V-02a=pass, V-02b=pass, V-02c=pass, V-02d=pass, V-03a=pass, V-03b=pass, V-03c=pass, V-03-semantic=pass, V-04=pass, V-05a=pass, V-05b=pass, V-05c=pass, V-05d=pass, V-05e=pass, V-05f=pass, V-06a=pass, V-06b=pass, V-07=pass, V-08a=pass, V-08b=pass, V-08c=pass, V-08d=pass, V-08e=pass, V-09a=pass, V-09b=pass, V-09c=pass, V-09d=pass, V-09e=pass, V-09f=pass, V-10a=pass, V-10b=pass, V-11=pass, V-12a=pass, V-12b=pass, V-13=pass.
- Finding IDs: F-01 (prior suggested P2), original triggers and sibling invalid-field behavior no longer reproduce; no current findings.
- Finding/scenario continuity: prior discovery V-03-semantic failed F-01; all other prior rows passed with stated limits. Producer correction R/M/I claims are separate from current independent R1–R7/M/I. No incomplete reason remains. Correction owner: implementer; evidence owner: this discovery; disposition/advancement owner: separate acceptance call. Sibling fields: profile, checks, complexity_target, exclude_directories.
- Preparation/context: docs/tasks/T-001.1/brief.md; verification.md revision 1; preflight.md including Decision context; implementation.md F-01 correction; discovery-01.md and maintainability-02.md.
- Reviewer regressions: boundary_probe.py source in Appendix A, exact R1 command in section 5; durable test_invalid_policy_settings_fail_before_measurement via R2; original discovery-01 DISC-07 is a defect-asserting oracle, not a corrected-behavior gate.
- Aggregate record: current M (26 tests) and I (36 tests), no skips, after clean targeted reconciliation. A and C passed as structural checks. tools/verify.py not run; T-001.3 owns final composition.
- Next: separate task-acceptance-review on docs/tasks/T-001.1 with the full packet and this report. No downstream stage was launched or delegated.
```

## Appendix A — independent installed-target correction probe

Save as `/tmp/T-001.1-discovery2/boundary_probe.py` and execute R1. Imports use
current reviewed test helpers only for disposable setup/snapshots. Success
assertions are the reviewer's public-boundary expectations.

```python
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
from unittest.mock import patch
ROOT=pathlib.Path.cwd()
sys.path.insert(0,str(ROOT/'tests'))
from test_install_development_skills import build_relocated_source_distribution,init_repo,snapshot_tree
with tempfile.TemporaryDirectory(prefix='t0011-discovery-') as temporary:
 base=pathlib.Path(temporary).resolve()
 source,installer=build_relocated_source_distribution(base)
 installation=base/'installation'; installation.mkdir(); init_repo(installation)
 subprocess.run([sys.executable,str(installer),str(installation)],check=True,capture_output=True,timeout=30)
 shutil.rmtree(source)
 target=base/'other target'; target.mkdir(); init_repo(target)
 quality=target/'.quality'; quality.mkdir()
 cwd=base/'cwd'; cwd.mkdir()
 app=target/'sample.py'; app.write_text('def f(a,b,c):\n    if a: return b\n    return c\n')
 scripts=installation/'.agents/scripts'; launcher=scripts/'measure_maintainability.py'
 policy=(scripts/'maintainability-default.toml').read_text().replace('complexity_target = 10','complexity_target = 7')
 ruff=(scripts/'maintainability-ruff-default.toml').read_text().replace('max-args = 5','max-args = 1').replace('max-statements = 50','max-statements = 4')
 env=dict(os.environ); env.pop('PYTHONPATH',None); env.pop('PYTHONHOME',None); env['PYTHONDONTWRITEBYTECODE']='1'
 def run(output):
  p=subprocess.run([sys.executable,str(launcher),'measure','sample.py','--root',str(target),'--output',output],cwd=cwd,env=env,capture_output=True,text=True,timeout=20)
  return p,json.loads((target/output).read_text()) if (target/output).exists() else None
 for i,(m,r) in enumerate(((False,False),(True,False),(False,True),(True,True))):
  for name,present,text in [('maintainability.toml',m,policy),('ruff.toml',r,ruff)]:
   p=quality/name; p.unlink(missing_ok=True)
   if present: p.write_text(text)
  result,report=run(f'.quality/reports/matrix-{i}.json')
  assert result.returncode==0,result.stderr
  cc=report['checks']['complexity']['values'][0]
  args=next(x for x in report['checks']['ruff']['values'] if x['code']=='PLR0913')
  assert (cc['value'],cc['target'],args['value'],args['target'])==(2,7 if m else 10,3,1 if r else 5)
  for name,present in [('maintainability.toml',m),('ruff.toml',r)]:
   s=report['identity']['settings'][name]
   assert s['origin']==('target' if present else 'shipped')
   path=pathlib.Path(s['path']); assert path.is_relative_to(target if present else scripts)
   assert s['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
  print('matrix',m,r,'PASS',flush=True)
 # F-01 corrected oracle: both original triggers and sibling field classes.
 (target/'.git/hidden.py').write_text('def invalid(:')
 for field,values in {
  'complexity_target':['true','false','"7"','-1','1.5'],
  'exclude_directories':['".git"','[true]','[""]'],
  'checks':['"complexity"','[true]','["unsupported"]','[]'],
  'profile':['true','""','"   "'],
 }.items():
  for i,value in enumerate(values+[None]):
   lines=[line if not line.startswith(field+' =') else field+' = '+value for line in policy.splitlines() if value is not None or not line.startswith(field+' =')]
   (quality/'maintainability.toml').write_text('\n'.join(lines)+'\n')
   before=snapshot_tree(target)
   p,report=run(f'.quality/reports/invalid-{field}-{i}.json')
   assert p.returncode==2 and report is None,(field,value,p.stdout,p.stderr)
   assert 'Invalid settings' in p.stderr and field in p.stderr and str(quality/'maintainability.toml') in p.stderr,p.stderr
   assert before==snapshot_tree(target),(field,value)
 print('F-01 regression and sibling policy fields: 19 invalid cases rejected; no writes',flush=True)
 (quality/'maintainability.toml').write_text(policy)
 p,report=run('.quality/reports/restored-valid.json')
 assert p.returncode==0 and list(report['files'])==['sample.py'],p.stderr
 print('Restored valid policy control excludes hidden invalid Python: PASS',flush=True)
 # Remove a shipped resource, check twice, refresh. Target B and A's unmanaged sentinels are preserved.
 missing=scripts/'maintainability-ruff-default.toml'; missing.unlink()
 sentinel=installation/'.quality/reports/keep.txt'; sentinel.parent.mkdir(parents=True); sentinel.write_bytes(b'keep')
 before=snapshot_tree(installation); other=snapshot_tree(target)
 for n in range(2):
  check=subprocess.run([sys.executable,str(ROOT/'scripts/install_development_skills.py'),'--check',str(installation)],capture_output=True,text=True,timeout=30)
  assert check.returncode==1,check.stderr
  assert json.loads(check.stdout)['differences']==[{'category':'missing','path':'.agents/scripts/maintainability-ruff-default.toml'}]
  assert snapshot_tree(installation)==before
 subprocess.run([sys.executable,str(ROOT/'scripts/install_development_skills.py'),str(installation)],check=True,capture_output=True,timeout=30)
 assert sentinel.read_bytes()==b'keep' and snapshot_tree(target)==other
 assert missing.read_bytes()==(ROOT/'scripts/maintainability-ruff-default.toml').read_bytes()
 print('missing/check/recheck/refresh preservation PASS',flush=True)
print('temporary targets removed:',not base.exists())
```

## Appendix B — effective policy comparison probe

Save as `/tmp/T-001.1-discovery2/policy_compare_probe.py` and execute R7.

```python
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
root=Path.cwd()
with tempfile.TemporaryDirectory(prefix='t0011-corrected-compare-') as temporary:
 base=Path(temporary).resolve(); installation=base/'installation';installation.mkdir()
 target=base/'target';target.mkdir();quality=target/'.quality';quality.mkdir()
 for name in ('measure_maintainability.py','maintainability_env.py','maintainability.py','maintainability-default.toml','maintainability-ruff-default.toml','maintainability-requirements.txt'):
  shutil.copy2(root/'scripts'/name,installation/name)
 policy=(installation/'maintainability-default.toml').read_text()
 source=target/'app.py'; source.write_text('def f(x):\n    if x: pass\n    return x\n')
 def invoke(*args):
  env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
  return subprocess.run([sys.executable,str(installation/'measure_maintainability.py'),*args,'--root',str(target)],cwd=base,env=env,capture_output=True,text=True,timeout=20)
 r=invoke('baseline','.','--output','.quality/before.json');assert r.returncode==0,r.stderr
 saved={p:p.read_bytes() for p in (quality/'before.json',quality/'before.txt')}
 (quality/'maintainability.toml').write_text(policy.replace('complexity_target = 10','complexity_target = 6'))
 r=invoke('compare','.','--baseline','.quality/before.json','--output','.quality/changed.json')
 report=json.loads((quality/'changed.json').read_text());assert r.returncode==2 and report['comparison']['status']=='incompatible',(r.stderr,report)
 # Same effective bytes from a new origin remain compatible, then a real edit is compared.
 (quality/'maintainability.toml').write_text(policy)
 source.write_text('def f(x):\n    if x: pass\n    if x: pass\n    return x\n')
 r=invoke('compare','app.py','--baseline','.quality/before.json','--output','.quality/restored.json')
 report=json.loads((quality/'restored.json').read_text());assert r.returncode==0,r.stderr
 row,=report['comparison']['complexity'];assert (row['before'],row['value'],row['delta'])==(2,3,1),row
 assert report['identity']['settings']['maintainability.toml']['origin']=='target'
 assert saved=={p:p.read_bytes() for p in saved}
 print('Changed effective policy: incompatible exit 2; identical policy from target origin: compatible CC 2->3 (+1); baseline JSON/text preserved.')
print('Disposable comparison target cleaned:',not base.exists())
```
