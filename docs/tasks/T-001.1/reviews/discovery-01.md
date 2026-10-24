# Task Review Discovery Report: T-001.1 — Portable, target-aware measurement runtime

| Field | Value |
|---|---|
| Producing stage | task-review-discovery, project-local installed skill |
| Coverage completeness | complete — all 36 designed cases have current evidence; one additional material invalid-policy row fails |
| Iteration | First independent discovery pass |
| Created | 2026-10-24T18:11:34.533176+00:00 |
| Root | /Users/mtrusov/work/skill-sources/personal-skills |
| Report | docs/tasks/T-001.1/reviews/discovery-01.md |
| Authority | docs/tasks/T-001.1/brief.md; parent docs/tasks/T-001/brief.md; docs/project-plan.md section 7 |
| Preparation | docs/tasks/T-001.1/verification.md revision 1; docs/tasks/T-001.1/preflight.md including Decision context |
| Submission | docs/tasks/T-001.1/implementation.md, READY_FOR_REVIEW; scenario claims are producer evidence |
| Conditional evidence | docs/tasks/T-001.1/reviews/maintainability-01.md; current installation/measurement contract records |

This report publishes evidence only. It gives no acceptance verdict, approved
deferral, or advancement. It applies only to the identified reviewed bytes and
does not review or authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production, test, fixture, or harness bytes.
It independently inspected the task-owned worktree diff and ran the probes below.
The sole repository write is this report. Temporary probes and capture data were
written under `/tmp/`; the active `.agents/` installation was not refreshed.
The project-local testing-discipline skill supplied test-review guidance.

HEAD: `ab9bac8ea13be3ef325750cfc0b00930f5906539`. Index SHA-256: `21d94f36114303731abeaea158b76b1df18f80e5709ec3c13caaa3c0465cdbf7`.
`git diff --cached --name-only` is empty. Index bytes, staged-entry listing,
worktree digests and full status were captured before probes and compared again
before this write. The worktree alone is not used as evidence of index identity.

## 2. Findings

### F-01 [suggested P2] Semantically invalid target policy can produce complete measurements or disable exclusions

| Field | Evidence |
|---|---|
| Location | scripts/maintainability.py:34–47, especially line 41; downstream consumers at build_report and complexity |
| Trigger | Copy the shipped policy into target `.quality/maintainability.toml`, changing only `complexity_target = 10` to `complexity_target = true`; invoke the public launcher with real pinned tools. Separately supply `exclude_directories = ".git"`. |
| Observed consequence | Boolean threshold exits 0 with `measurement_status: complete` and JSON `target: true`, interpreted numerically as 1. A string exclusion is accepted as complete for a file scope; for folder scope it becomes a set of characters, scans `.git/hidden.py`, and reports a source failure for a file that the valid list excludes. Invalid target settings can therefore yield misleading advisory thresholds or scan excluded assets. |
| Evidence | DISC-02 reproduced both types through an installed launcher measuring another target. DISC-07 supplies an independent valid-policy control and an invalid Python sentinel inside `.git`; control excludes it and exits 0, Boolean exits 0/complete, string includes the sentinel and exits 2/incomplete instead of rejecting the policy. Reproduction code is retained below. |
| Affected AC | AC-02 invalid present settings; AC-04 exclusions; R-01 target policy and truthful evidence |
| Broken invariant | Present target settings must be valid policy before they drive measurement; successful TOML parsing alone is insufficient. Python Boolean/integer and string/collection coercions must not cross this configuration boundary. |
| Explicit sibling surface | The demonstrated numeric threshold and directory-list fields share the same unchecked policy boundary. The policy's checks collection and other consumed field types are credible sibling inputs to examine; this report does not claim every sibling was demonstrated broken. Ruff's own validation does not validate maintainability policy. |
| Smallest corrective direction | Validate the effective maintainability policy's required field types and supported values at its shared settings boundary, before discovery/analyzer/report work, and issue a visible policy-specific failure. Cover valid controls and invalid numeric/collection types rather than special-casing these literals. |

No other finding was confirmed. Existing syntax-malformed settings cases pass;
they do not cover this semantic-validation gap. The behavior is in scope because
this task introduces owner-controlled target policy and promises invalid-policy
failure; the old adapter's source-owned policy is not an oracle for valid input.

## 3. Completeness ledger

All rows below are required/material. Stable verification identities are retained.
Each comma-separated ID has the stated result independently. Submitted evidence
for every V-row is the correspondingly named scenario in implementation.md,
not an independent pass. No prior discovery ledger exists.

| Row IDs | AC / invariant | Explicit cases and setup/oracle | Submitted evidence | Independent evidence | Result |
|---|---|---|---|---|---|
| V-01a, V-01b | AC-01 / local runtime | Disposable distribution installed, then removed; unrelated cwd, no Python helper path; baseline CC 2 then edit and compare CC 3/+1; measure; JSON/text and baseline preservation | Launcher journey | DISC-03 real pinned public launchers; DISC-02 also separates installation from measured repository | pass |
| V-02a, V-02b, V-02c, V-02d | AC-01/02 / independent policy | Neither, maintainability only, Ruff only, both; counts remain constant, effective targets/origins/paths/hashes match | Four settings states | DISC-01; DISC-02 independently uses target 7 and Ruff 1/4 in a different target, constant CC 2 and args 3 | pass |
| V-03a, V-03b | AC-02 / invalid present syntax | Each family independently contains `[invalid TOML`; exit 2 naming file, no successful fallback; bad bytes preserved | Malformed settings case | DISC-01 actual installed CLI | pass |
| V-03c | AC-02 / no root Ruff inheritance | Root Ruff `ignore = ["ALL"]` present/absent with target Ruff and with fallback; unchanged native values/settings identity and root bytes | Same settings case | DISC-01 installed CLI with both origins | pass |
| V-03-semantic | AC-02/04 / typed valid policy | Valid control, Boolean threshold, string exclusion; invalid policy must fail before it can claim a complete report or scan excluded files | No submitted semantic-invalid cases | DISC-02 and DISC-07 actual CLI; Boolean and string accepted; sentinel under `.git` becomes included | fail — F-01 |
| V-04 | AC-03 / setup ownership | Replay printed recipe at EnvBuilder/pip seams; target native destination and adjacent installation pin path; no network or actual package installation | Setup dispatch case | DISC-03 observes real setup dispatch with provisioning effects replaced by scoped spies | pass — selection only |
| V-05a, V-05b, V-05c, V-05d, V-05e | AC-03 / native key | Change OS, CPU, implementation, patch version, installation pins separately; key differs. Target pins do not change key | Key-separation case | DISC-03 component probe | pass |
| V-05f | AC-03 / real interpreter selection | Prepared disposable native environment, unpinned caller, unusable foreign/legacy sentinels; real adapter and exact analyzer versions through target interpreter | Seeded native case | DISC-03 real subprocess/adapter; no package download | pass |
| V-06a | AC-03 / pinned caller | Pinned caller completes and creates no target environment | Launcher journey | DISC-03, additionally DISC-02 | pass |
| V-06b | AC-03 / no implicit provisioning | Missing pins under `-S`; exit 2, shell-parsable target-aware recipe with spaces; complete target tree/index unchanged | Missing-pin recipe case | DISC-03 | pass |
| V-07 | AC-04 / actual source and index | Commit CC2, stage CC3, worktree CC4, untracked CC1; decode sources/hashes; edit worktree to CC5 and compare +1; preserve index/staged/saved JSON/text | Dirty snapshot case | DISC-03 actual Git/filesystem plus real public compare | pass |
| V-08a | AC-04 / native/advisory | CC2/10/11/16, below/equal/above target, decrease, unchanged breach, crossing and new breach; breach CLI exits 0 | Native boundary and console cases | DISC-04 | pass |
| V-08b | AC-04 / symbol identity | Nested/local class/async and duplicate names; added/removed/renamed symbols; no guessed identity | Native identity cases | DISC-04 | pass |
| V-08c | AC-04 / Ruff semantics | Real argument/statement counts and native exemptions; collection limits zero and advisory targets distinct; noqa ignored | Ruff real/changes/count cases | DISC-04 | pass |
| V-08d | AC-04 / unknown evidence | Missing→present and present→missing for zero args, return-only, override/overload; missing values/deltas null | Ruff unknown case | DISC-04 | pass |
| V-08e | AC-04 / groups and exclusions | Implementation/test/eval groups; nested invalid Python excluded; explicit excluded scope rejected; installed/runtime resources excluded under valid policy | Directory case and installed journeys | DISC-04; DISC-03 | pass for valid policy; invalid-type boundary separately fails above |
| V-09a | AC-04 / selected checks | Real complexity-only CLI exits 0 with full_profile false | Directory case | DISC-04 | pass |
| V-09b | AC-04 / partial availability | Controlled Ruff discovery absence; completed Radon retained, Ruff unavailable, CLI exit 2 | Partial completion case | DISC-05; discovery absence mocked at dependency seam, real adapter preserved | pass |
| V-09c | AC-04 / failed/concurrent source | Invalid Python and source mutation after capture; incomplete observations and exit 2 | Partial/concurrent cases | DISC-05; controlled mutation at command seam | pass |
| V-09d | AC-04 / compatibility | Independent tools/policy/Ruff/adapter/collection/interpreter mutations and incomplete baseline rejected; mount/patch compatible | Compatibility and mount cases | DISC-05, includes public incompatible-baseline exit 2 | pass |
| V-09e | AC-04 / scope coverage | Folder baseline; affected new/deleted files; untouched outside subset retained; outside coverage rejected | Folder case | DISC-05 | pass |
| V-09f | AC-04 / path scope | Folder/file and absolute in-root work; escaping/symlink rejected | Directory and CLI handoff cases | DISC-04/05 | pass |
| V-10a, V-10b | AC-04/05 / saved evidence | Occupied JSON and sibling-only text independently refused, exit 2, all saved bytes preserved | No-overwrite case | DISC-05 real public CLI | pass |
| V-11 | AC-05 / narrow ownership | Fresh/refresh committed and unborn targets; staged/dirty/untracked source/index, unmanaged helpers/skills, policy/env/JSON/text sentinels and outside AGENTS bytes preserved | Installer journey and line-ending case | DISC-06 executes journey; DISC-08 executes correct line-ending test; DISC-02 extra separate-target refresh | pass |
| V-12a, V-12b | AC-05 / exact drift | Every six managed files changed/removed independently; two read-only checks, exact category/path, refresh/recheck, complete tree/index preserved | All-resource lifecycle case | DISC-06, plus DISC-02 single-resource independent probe | pass |
| V-13 | AC-01/05 / declaration coherence | Installer six-resource membership, README/profile guide/launcher guide/maps, shipped vs target policy and narrow ownership agree | Membership and documentation trace | DISC-06 membership test plus current source/diff review; registry update reviewed separately below | pass — documentary/structural, not runtime proof |

The ledger was reconciled against the brief's AC-01–05, R-01/R-02 and all
verification rows. V-03-semantic remains failed despite passing syntax cases.
No required row is blocked or unchecked. This is complete discovery of selected
contract cases, not exhaustive input or operating-system qualification.

## 4. Adversarial state and evidence checks

- Four independent settings-presence states were exercised twice, including a
  reviewer target distinct from the installation and fixture targets.
- Policy type confusion was exercised at the public boundary, with valid controls
  and a hidden invalid-source sentinel. F-01 is not inferred from static text.
- Missing/changed distribution resources were checked repeatedly, then legitimately
  refreshed and checked again. Real target/index/evidence preservation was observed.
- Dirty source was captured, edited, then compared through a second real occurrence.
- Process lifecycle, retries, cardinality and tamper-proofing are not changed
  contracts here. Probes use synchronous completed children, bounded custom
  subprocess timeouts and temporary-directory cleanup; none launches a daemon.
  Both custom probes confirmed disposable targets no longer existed. No network,
  downloads, provider checks or privileged operations were performed.

## 5. Commands and independent results

Commands run from repository root unless `cwd=tests/` is stated. Native Python is
`.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`, with real Radon
6.0.1 and Ruff 0.14.2 confirmed by the native-selection report. No analyzer skip
was observed. Unittest temporary fixtures clean up their own targets.

### DISC-01 — narrow settings rows

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py -k settings -v
```

Exit 0; 2 tests; 1.687 s; no skips. Installed policy matrix, malformed families
and unrelated root Ruff configuration have decisive assertions.

### DISC-02 — separate installation and target, independent policy matrix and refresh

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B /tmp/T-001.1-discovery-probe.py
```

Exit 0 means reproduction completed, not contract success. Output: all four
presence states PASS; `boolean threshold: 0 complete True`;
`string exclusions: 0 complete '.git'`; missing/check/recheck/refresh preservation
PASS; temporary targets removed True. Exact probe source is in Appendix A.

### DISC-03 — explicit targeted ledger cases

Cwd: `tests/`.

```sh
../.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest test_maintainability.MeasurementTests.test_installed_and_source_launchers_work_without_distribution test_maintainability.LauncherTests.test_environment_key_separates_native_runtimes_and_dependency_versions test_maintainability.LauncherTests.test_missing_pins_recipe_dispatches_setup_for_selected_target test_maintainability.LauncherTests.test_native_target_environment_reaches_real_adapter test_maintainability.MeasurementTests.test_snapshot_preserves_staged_unstaged_untracked_and_index -v
```

Exit 0; 5 tests; 2.030 s; no skips.

### DISC-04 — explicit targeted ledger cases

Cwd: `tests/`.

```sh
../.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest test_maintainability.MeasurementTests.test_real_complexity_boundaries_and_below_target_increase test_maintainability.MeasurementTests.test_nested_scopes_async_and_duplicate_names_are_not_conflated test_maintainability.MeasurementTests.test_added_and_removed_symbols_need_interpretation_without_guessing_relationships test_maintainability.MeasurementTests.test_ruff_real_diagnostics_and_override_exemption test_maintainability.MeasurementTests.test_ruff_statement_changes_keep_advisory_targets test_maintainability.MeasurementTests.test_ruff_native_counts_distinguish_improvement_and_worsening test_maintainability.MeasurementTests.test_ruff_missing_diagnostics_never_become_numeric_zero test_maintainability.MeasurementTests.test_directory_exclusions_selected_check_and_empty_scope test_maintainability.MeasurementTests.test_console_compare_prints_identities_and_deltas_before_top_five -v
```

Exit 0; 9 tests; 1.925 s; no skips.

### DISC-05 — explicit targeted ledger cases

Cwd: `tests/`.

```sh
../.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest test_maintainability.MeasurementTests.test_partial_completion_missing_tool_and_invalid_python test_maintainability.MeasurementTests.test_concurrent_input_change_marks_results_incomplete test_maintainability.MeasurementTests.test_incompatible_scope_tool_configuration_and_failed_baseline test_maintainability.MeasurementTests.test_report_can_be_compared_from_a_different_mount_path test_maintainability.MeasurementTests.test_folder_baseline_can_compare_affected_new_and_deleted_files test_maintainability.MeasurementTests.test_cli_report_handoff_uses_target_root_for_relative_report_paths test_maintainability.MeasurementTests.test_cli_file_scope_baseline_comparison_and_no_overwrite -v
```

Exit 0; 7 tests; 2.174 s; no skips.

### DISC-06 — targeted installer lifecycle and membership

Cwd: `tests/`.

```sh
python3 -B -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_measurement_resources_changed_missing_checks_and_refresh test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family test_install_development_skills.DevelopmentSkillInstallerTests.test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_contains_repo_stage_and_bounded_delivery_skills -v
```

Exit 1: three real tests passed, but the line-ending test selector named the
wrong class and produced one loader error. The resource lifecycle, committed/
unborn journey and membership cases each completed successfully. The loader
error supplies no line-ending evidence; DISC-08 corrects only that selector.

### DISC-07 — valid policy control and semantic-invalid siblings

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B /tmp/T-001.1-policy-type-probe.py
```

Exit 0 means the observed defect reproduced. Output:

```text
control exit 0 status complete files ['a.py'] target 10
boolean exit 0 status complete files ['a.py'] target True
string exit 2 status incomplete files ['.git/hidden.py', 'a.py'] target 10
temporary target removed: True
```

Full source is in Appendix B. Oracle for corrected behavior is policy-specific
exit 2 for both invalid types before measurement, while the valid control remains
successful; current script deliberately asserts observed defective behavior.

### DISC-08 — corrected AGENTS preservation selector

Cwd: `tests/`.

```sh
python3 -B -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes -v
```

Exit 0; 1 test; 5.154 s; no skips. Exact outside-marker CRLF and other line-ending
bytes survive fresh installation and refresh.

### DISC-09 — required structural checks

Each command ran separately from root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 -B tools/check_contracts.py --root .
git diff --check
```

Architecture exit 0, 4 tests, no skips. Registry exit 0, six subsystems and seven
indexed plan refs. Whitespace exit 0. These checks are structural, not behavioral
qualification. Architecture is the repository-mandated handoff check; registry
is the mandated contract check. They do not erase F-01 or act as an aggregate.

### Command corrections and byte reconciliation

- The first DISC-03 launch used `.quality/.../bin/python` while cwd was `tests/`;
  it failed immediately with exit 127, no interpreter started. The recorded
  successful command uses `../.quality/...`.
- An attempted identity assertion against every maintainability-report digest
  stopped at `docs/development.md`. Explicit comparison then found all 13 other
  paths identical, including every implementation/test asset. The changed doc
  adds the current measurement registry and remaining IF-001 explanation. Its
  current bytes were reviewed with the registry delta; the earlier digest is
  not claimed as current evidence. Initial discovery capture itself still
  matched status, index and every pre-existing changed/untracked file.
- `git diff --cached --name-only` is empty; separate current index/HEAD state is
  recorded below. Historic narrative about staged planning work is not used to
  assert current index identity.

## 6. Aggregate-gate record

| Gate | Status | Owner / stage | Reason / current evidence |
|---|---|---|---|
| Native Python `-B -m unittest discover -s tests -p test_maintainability.py` | not run | Initial discovery | F-01 is a decisive targeted failure. Explicit independent ledger probes continued; no full owning suite was run merely for completeness. Producer's 25-test run remains producer evidence. |
| `python3 -B -m unittest discover -s tests -p test_install_development_skills.py` | not run | Initial discovery | Same suppression after F-01; targeted preservation/lifecycle rows above completed. Producer's 36-test run is not current reviewer aggregate evidence. |
| `python3 tools/verify.py` | not run | T-001.3 final composition stage | Brief explicitly assigns the final cross-cutting aggregate to T-001.3. No waiver, premature gate or copied prior pass. |

No selected required probe remains outstanding. The required architecture and
contract structural checks ran for their separate repository-mandated purpose.
A correction discovery must reproduce F-01 against corrected bytes, preserve
sibling coverage and own the task-applicable owning-suite evidence after clean
targeted results. T-001.3 retains the cross-cutting gate.

## 7. Scope and reviewed identities

Task runtime/test/documentation changes align with the brief's allowed paths.
Registry-stage additions are `docs/contracts/measurement.json`, changes to
`installation.json` and generated `index.json`, and the corresponding explanation
in `docs/development.md`. This is the brief's expected contract delta, inspected
against current executable declarations; the registry describes partial IF-001
and does not claim T-001.2/report or T-001.3 guidance work is complete. There is
no unexplained production overlap. Runtime and tests retain all maintainability-
reviewed digests. Only the development guide differs from that review's listed
files, as explained above; it receives current documentary review here.

Existing task packets and `reviews/maintainability-01.md` are authority/submission/
conditional evidence. T-001.2/T-001.3/parent briefs and docs/tasks/index.json are
pre-existing context, not implementation attributed to this task. Deleted
`tools/maintainability.py` and `tools/maintainability_env.py` are intentional
relocations; their old HEAD contents were compared with the new scripts modules.
No user source, active installation, index or previous report was changed.

Authority identities (SHA-256):

```text
e38fb7e8e978aa3b16df91fa0b6d10d2b928d08af7bc2119a51fdd48709d5d83  docs/tasks/T-001.1/brief.md
3f85c174e7aa7822fc285e0f9e09ec8a93454fff2ed154cc3744cd9616b11b0b  docs/tasks/T-001.1/verification.md (revision 1)
9856d3ccfffcd56b4faed20dcf6ea4b49d87c4553292a5ed996cb4e784ca0df7  docs/project-plan.md
952f094d08ad03c5f5dfe18674fdbd710e8851fc8eaff1bdddc6facec2a5c954  docs/task-map.json
```

Current scoped worktree SHA-256 (`DELETED` is absent in worktree):

```text
0c559568b1ec9cf336961222c0855b9b19ce10ddceefb89fac226524b39981de  README.md
60f9b47d36ae5aacf35600ff4bb2775bcd80719fffe199c43aaa25bcc8574659  docs/contracts/index.json
4af6590f6d79bd652d28c4927e82b8e5639da8921a6aefb45878aed0759bb2e9  docs/contracts/installation.json
b09f89e64c465c58c5657e328fdc311be5ea44881508ff72a8a033220b2122cd  docs/contracts/measurement.json
246a3e85d87b1fcc2f2f3ff270128d4f0bc1d6940de5dea575e3e3da9827702e  docs/development.md
e68fb53a19376c37820c1781b474c4972a8b7020b0238d102923ceebd44f4648  docs/project-map.md
a614b7bc21a84f27df588ec150e1c5ccfadd229b562aa3bd967e1e9026a159da  scripts/install_development_skills.py
f258d0e5a0dc070fc9ec33aa0dc000b1959fba9eebdd5cc20e1cb00178a654fb  scripts/maintainability-default.toml
79dbf22b5bc1bc8c10f5746610e937d4f592ebfb3bfc6123d1428cae5e344d44  scripts/maintainability-requirements.txt
a95813db8c5666acfbeae7e1734e7f1a16ad674d1798cc710853e0d3bbb2754b  scripts/maintainability-ruff-default.toml
167ed91678f8e79bae62781715d79760f94c60515ee858f6aab55103ea73567b  scripts/maintainability.py
54525f713a8865b1a1f26be6c966ffbc5a6c44171ae0727556dbe458c583b9eb  scripts/maintainability_env.py
5dae8e41784b2157fbf91f89d317c5c5ddeb0c432f78551529aadad3d1d38789  scripts/measure-maintainability.md
caa1d0e31fcc04130dd55347f7dc48943a232939156d9fd631f688a0e2fd8b2b  scripts/measure_maintainability.py
bc8930ae9b081c4bf7f030003ebbc7fbe71ae41e54cc27ddce69aa21548eee8d  skills/README.md
a73ea29dbbe97e8070c56247b7e36e2a1147f31e8e12c1a13c688b48aa454f55  tests/test_install_development_skills.py
77e40f5f22eda978532ac3d6d08a98e27857d9577ff27a8e9ff5c630383671ab  tests/test_maintainability.py
DELETED  tools/maintainability.py
DELETED  tools/maintainability_env.py
```

Separate index entries for tracked scoped paths (Git blob IDs, unchanged by review):

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

Exact reviewed status immediately before report write:

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
?? docs/tasks/T-001.1/reviews/maintainability-01.md
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

Exact status after report creation (checked against actual Git output):

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

Only the new discovery report entry differs. All pre-existing changed/untracked
file hashes, real index bytes and staged-entry listings remain unchanged.

## 8. Questions, unchecked work and residual risks

No required row is blocked or unchecked; there is no unresolved authority question.
F-01 is a confirmed failed behavior, not a residual risk or approved deferral.
Actual network dependency installation and other operating systems are not
qualified, as already bounded by the brief and preflight. Setup spies prove
selection only. Source-policy semantic validation needs corrected regression
evidence; the acceptance decision call retains all decision authority.

## 9. Coverage completeness and next route

Discovery coverage is complete for this task's selected material cases, with
F-01 open. The next action is a separate `task-acceptance-review` call consuming
this report, the current scoped diff, task brief, verification revision 1,
preflight/Decision context, implementation submission, prior maintainability
report and current contract records. This report does not permit advancement.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / bytes: first independent discovery; HEAD ab9bac8ea13be3ef325750cfc0b00930f5906539; current scoped SHA-256 and separate index identities in section 7.
- Coverage rows: V-01a/b=pass; V-02a/b/c/d=pass; V-03a/b/c=pass; V-03-semantic=fail (Boolean numeric policy and string collection accepted); V-04=pass (dispatch only); V-05a/b/c/d/e/f=pass; V-06a/b=pass; V-07=pass; V-08a/b/c/d/e=pass for valid policy; V-09a/b/c/d/e/f=pass; V-10a/b=pass; V-11=pass; V-12a/b=pass; V-13=pass documentary/structural.
- Finding IDs: F-01 suggested P2, open; invalid target maintainability policy is parsed but not semantically validated.
- Continuity: no prior discovery. Producer claimed every V-row passed; reviewer corroborates designed rows, adds failing V-03-semantic. No blocked/unchecked rows or omitted required scenarios. Correction owner: subsequent bounded implementation; evidence owner: fresh independent discovery after correction; authority owner: separate acceptance decision call. Sibling surfaces: numeric threshold, exclusion/check collections and other consumed policy types at the shared boundary.
- Preparation/context: docs/tasks/T-001.1/brief.md; verification.md revision 1; preflight.md including Decision context; parent T-001 brief and reviewed plan/task-map hashes; implementation.md; reviews/maintainability-01.md; docs/contracts/measurement.json and installation.json.
- Reviewer regressions: Appendix B reproducer and Appendix A installed-origin matrix, retained in this report (temporary executable copies /tmp/T-001.1-policy-type-probe.py and /tmp/T-001.1-discovery-probe.py). Exact commands in DISC-07 and DISC-02. Reproducer asserts current defect; corrected regression must instead assert policy-specific exit 2 for invalid types while valid control succeeds. Existing syntax-only command: native Python -B -m unittest discover -s tests -p test_maintainability.py -k settings -v.
- Aggregate gate: full owning suites not run by initial discovery after F-01; producer results remain producer evidence. python3 tools/verify.py not run, owner T-001.3. Required architecture and registry checks passed independently as structural evidence.
- Next: separate task-acceptance-review on docs/tasks/T-001.1, this report and current scoped bytes; no acceptance verdict or advancement is supplied here.
```

## Appendix A — exact reviewer installed-boundary probe

Run from repository root with the pinned Python in DISC-02. This temporary script
uses existing repository fixture builders; production behavior is exercised by
actual installer and measurement subprocesses. Script exit 0 is not a policy-
validation pass; it prints the defective observations for the finding.

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
 # Semantic invalidity: numeric complexity threshold must not silently become a Boolean.
 (quality/'maintainability.toml').write_text(policy.replace('complexity_target = 7','complexity_target = true'))
 p,report=run('.quality/reports/boolean.json')
 print('boolean threshold:',p.returncode,report['measurement_status'] if report else p.stderr,report['checks']['complexity']['values'][0]['target'] if report else '',flush=True)
 # Independent sibling: collection setting supplied as string must not split into characters.
 (quality/'maintainability.toml').write_text(policy.replace('exclude_directories = [', 'exclude_directories = ['))
 lines=policy.splitlines(); lines=[ 'exclude_directories = ".git"' if x.startswith('exclude_directories') else x for x in lines]
 (quality/'maintainability.toml').write_text('\n'.join(lines)+'\n')
 p,report=run('.quality/reports/string-exclusion.json')
 print('string exclusions:',p.returncode,report['measurement_status'] if report else p.stderr,repr(report['excluded_directories']) if report else '',flush=True)
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

## Appendix B — exact policy-type reproduction

Run from repository root with the pinned Python in DISC-07. Valid/invalid policy
inputs and the independent `.git` sentinel oracle are explicit. No schema text
or deserialization success is substituted for executable behavior.

```python
from pathlib import Path
import json,subprocess,sys,tempfile
root=Path.cwd()
with tempfile.TemporaryDirectory(prefix='t0011-policy-') as temporary:
 target=Path(temporary)
 (target/'.quality').mkdir(); (target/'.git').mkdir()
 (target/'a.py').write_text('def f(x):\n    if x: return 1\n    return 0\n')
 (target/'.git/hidden.py').write_text('def invalid(:')
 default=(root/'scripts/maintainability-default.toml').read_text()
 cli=root/'scripts/measure_maintainability.py'
 for label,policy in [('control',default),('boolean',default.replace('complexity_target = 10','complexity_target = true')),('string', '\n'.join('exclude_directories = ".git"' if s.startswith('exclude_directories =') else s for s in default.splitlines()))]:
  (target/'.quality/maintainability.toml').write_text(policy)
  r=subprocess.run([sys.executable,str(cli),'measure','.', '--root',str(target),'--output',f'.quality/reports/{label}.json'],capture_output=True,text=True,timeout=20)
  report=json.loads((target/f'.quality/reports/{label}.json').read_text())
  print(label, 'exit',r.returncode,'status',report['measurement_status'],'files',list(report['files']),'target',report['checks']['complexity']['values'][0]['target'])
  if label=='control': assert r.returncode==0 and list(report['files'])==['a.py']
  if label=='boolean': assert r.returncode==0 and report['checks']['complexity']['values'][0]['target'] is True
  if label=='string': assert r.returncode==2 and '.git/hidden.py' in report['files'] and report['checks']['complexity']['errors']
print('temporary target removed:',not target.exists())
```
