# T-001.1 implementation result

The development profile now supplies a portable measurement launcher, adjacent
runtime helpers, shipped defaults and installation-owned pins. Setup and
measurement select the same target. Each target policy file independently takes
precedence over its corresponding default. Reports retain effective contents and
record settings origins, paths and SHA-256 identities. The F-01 correction now
rejects semantically invalid maintainability policy before scanning or publication;
current correction evidence and the full carried ledger are recorded below.

Implemented: `READY_FOR_REVIEW`

This is implementation evidence. Independent review and acceptance remain owed.

## Authority and context

- Authority: [brief.md](brief.md), SHA-256
  `e38fb7e8e978aa3b16df91fa0b6d10d2b928d08af7bc2119a51fdd48709d5d83`.
- Readiness: [preflight.md](preflight.md).
- Derived guidance: [verification.md](verification.md), revision 1.
- Parent: [T-001 brief](../T-001/brief.md). Reviewed plan/task-map identities still
  match the parent. Approved plans, task map and preparation inputs were not edited.
- Active skill: project-local
  `.agents/skills/task-implementation-flow/bounded-task-implementer/SKILL.md`.
  No active installation refresh, network, dependency download, commit or reviewer
  invocation occurred.

## Deliverables

- `scripts/measure_maintainability.py` resolves its adjacent environment helper.
- `tools/maintainability.py` → `scripts/maintainability.py`.
- `tools/maintainability_env.py` → `scripts/maintainability_env.py`.
- Flat shipped resources: `scripts/maintainability-default.toml`,
  `scripts/maintainability-ruff-default.toml`,
  `scripts/maintainability-requirements.txt`.
- `scripts/install_development_skills.py` explicitly manages all six runtime
  resources under target `.agents/scripts/`; replacement boundaries are unchanged.
- Owning tests: `tests/test_maintainability.py` and
  `tests/test_install_development_skills.py`. The existing disposable-source
  builder is reused as a module-level helper; existing snapshot, exclusion,
  compatibility and installer journeys retain and extend their distinct evidence.
- Updated guidance: `README.md`, `skills/README.md`,
  `scripts/measure-maintainability.md`, `docs/project-map.md`,
  `docs/development.md`.

Actual contract impact:

- Added installed measurement runtime/default/pin membership.
- Added `setup --root <target>` and target-owned native environment selection;
  pins remain installation-owned. Measurement never provisions packages.
- Changed settings resolution to independent target/shipped selection. Added
  `identity.settings` provenance. Effective policy/Ruff bytes still determine
  comparison compatibility; mount paths and origins do not.
- Preserved public baseline/compare/measure, scope, output and native analyzer
  semantics. Neutral labels and empty-baseline extension remain with T-001.2.

Executable contract declarations changed:

- `scripts/install_development_skills.py` (`SHARED_SCRIPT_FILES`).
- `scripts/maintainability_env.py` (setup/root and environment resolution).
- `scripts/maintainability.py` (settings and report identity).
- The launcher and three flat default/pin resources listed above.

Contract registry synchronization belongs to the subsequent designated updater.
No contract record or generated index was edited in this invocation.

## Verification

All commands ran from the source repository root. The final owning runs passed
with no skips:

| Key | Exact command | Result |
|---|---|---|
| M | `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py` | Exit 0; 25 tests; 7.948 s. Real Radon 6.0.1 and Ruff 0.14.2. |
| I | `python3 -B -m unittest discover -s tests -p test_install_development_skills.py` | Exit 0; 36 tests; 24.759 s. |
| A | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Exit 0; 4 tests; no skips. Executed once through the active installation's run-evidence check wrapper. |
| C | `python3 tools/check_contracts.py --root .` | Exit 0; 5 subsystems; 0 indexed plan references. Structural validation only. |
| D | `git diff --check` | Exit 0. Whitespace check only. |

The new independent-settings assertions were run against the original runtime
before implementation using M with `-k settings_select`: they rejected ignored
target policy (expected complexity target 3, observed 10; expected Ruff targets
2/3, observed 5/50) and absent settings provenance. The same targeted command
then passed through the installed launcher after the runtime change.

Setup dispatch was observed at the real `EnvBuilder.create` and pip subprocess
seams without downloading packages. Native-selection evidence seeds a disposable
environment from prepared local dependencies, including the real Ruff binary;
it proves actual adapter execution through that interpreter, not a completed
package installation. Initial fixture issues (temporary-path aliases, incomplete
Ruff environment seeding and invalid unmanaged-skill frontmatter) were corrected
before the final passing runs.

## AC and scenario evidence

Each row below identifies the test within command M or I above. All rows have
passing implementation evidence; these are not independent reviewer statuses.

| Scenario IDs | AC / risk | Test and decisive setup/oracle |
|---|---|---|
| V-01a, V-01b | AC-01; R-01 | M: `test_installed_and_source_launchers_work_without_distribution`. Install from a disposable source, delete that source, clear ambient Python helper paths, run from unrelated cwd. Installed and source baseline/compare/measure use real pins; CC 2→3, delta +1; target-relative JSON/text; baseline bytes unchanged; reported defaults are beside the selected launcher. |
| V-02a, V-02b, V-02c, V-02d | AC-01/02; R-01 | M: `test_settings_select_each_target_file_independently`. All four target-presence states run through the installed CLI. CC stays 5; target is 10 or 3. Ruff counts stay 3/1; targets are 5/50 or 2/3. Origins, paths, hashes and target bytes match each state. |
| V-03a, V-03b | AC-02; R-01 | M: `test_invalid_target_settings_and_unrelated_root_ruff`. Each present malformed family exits 2, names the policy and retains bad bytes; no successful fallback. |
| V-03c | AC-02; R-01 | M: same test. Conflicting root Ruff config has no effect on native records or settings identity, with either target Ruff policy or shipped fallback. Root config bytes remain unchanged. |
| V-04 | AC-03; R-01 | M: `test_missing_pins_recipe_dispatches_setup_for_selected_target`. Parse the diagnostic recipe, replay its setup arguments at provisioning seams, assert target-native destination and installation requirements path. Target policy, reports, source and index remain unchanged; no download. |
| V-05a, V-05b, V-05c, V-05d, V-05e | AC-03; R-01 | M: `test_environment_key_separates_native_runtimes_and_dependency_versions`. Independently change OS, CPU, implementation, patch version and installation pin bytes; each changes the key. Target requirements alone do not change it. |
| V-05f | AC-03; R-01 | M: `test_native_target_environment_reaches_real_adapter`. Unpinned base interpreter selects a locally seeded target environment, ignoring unusable legacy/foreign interpreters. Real report gives CC 3, exact analyzer versions and a Ruff command using the selected target interpreter. |
| V-06a | AC-03; R-01 | M: `test_installed_and_source_launchers_work_without_distribution`. Correctly pinned caller completes real measurements without creating target environments. |
| V-06b | AC-03; R-01 | M: `test_missing_pins_recipe_dispatches_setup_for_selected_target`. Unavailable pins exit 2; quoted launcher/target paths containing spaces parse correctly. Complete target tree, including dirty source, real index, settings and saved evidence, stays byte-identical. Foreign/legacy sentinels remain; no provisioning. |
| V-07 | AC-04; R-02 | M: `test_snapshot_preserves_staged_unstaged_untracked_and_index`. Committed/staged/worktree complexities 2/3/4, untracked complexity 1. Decode captured sources and check hashes; compare 4→5, delta +1. Source bytes, index, staged content and saved JSON/text remain unchanged relative to each invocation. |
| V-08a | AC-04; R-02 | M: `test_real_complexity_boundaries_and_below_target_increase`. Exact 2/10/11/16 values, increase below target, equality/crossing, unchanged legacy, decrease and new breach retain their semantics. Successful breach CLI wiring is also exercised by `test_console_compare_prints_identities_and_deltas_before_top_five`. |
| V-08b | AC-04; R-02 | M: `test_nested_scopes_async_and_duplicate_names_are_not_conflated`, `test_added_and_removed_symbols_need_interpretation_without_guessing_relationships`. Qualified native identities stay distinct; duplicates remain unmatched; no invented rename relationship. |
| V-08c | AC-04; R-02 | M: `test_ruff_real_diagnostics_and_override_exemption`, `test_ruff_statement_changes_keep_advisory_targets`, `test_ruff_native_counts_distinguish_improvement_and_worsening`, `test_ruff_missing_diagnostics_never_become_numeric_zero`. Real argument/statement counts, zero collection limits, advisory targets, noqa and native exemptions remain distinct. |
| V-08d | AC-04; R-02 | M: `test_ruff_missing_diagnostics_never_become_numeric_zero`. Both comparison directions retain unknown values/deltas for zero arguments, return-only bodies and override/overload exemptions. |
| V-08e | AC-04; R-02 | M: `test_directory_exclusions_selected_check_and_empty_scope`. Implementation/test/eval groups remain separate; invalid Python under nested excluded directories is not scanned; explicit excluded scope fails. Installed/runtime evidence paths are also excluded in V-01/V-02. |
| V-09a | AC-04; R-02 | M: `test_directory_exclusions_selected_check_and_empty_scope`. Real complexity-only CLI exits 0 with `full_profile: false`. |
| V-09b | AC-04; R-02 | M: `test_partial_completion_missing_tool_and_invalid_python`. Controlled Ruff discovery absence retains completed Radon observations, marks Ruff unavailable and returns CLI status 2. |
| V-09c | AC-04; R-02 | M: `test_partial_completion_missing_tool_and_invalid_python`, `test_concurrent_input_change_marks_results_incomplete`. Invalid source and changes after capture remain incomplete; actual causes/observations remain visible; CLI status is 2. |
| V-09d | AC-04; R-02 | M: `test_incompatible_scope_tool_configuration_and_failed_baseline`, `test_report_can_be_compared_from_a_different_mount_path`. Independent tool/config/collection/adapter/interpreter changes and incomplete baselines are incompatible; incomplete-baseline CLI exits 2. Mount and Python patch differences remain compatible. |
| V-09e | AC-04; R-02 | M: `test_folder_baseline_can_compare_affected_new_and_deleted_files`, `test_cli_report_handoff_uses_target_root_for_relative_report_paths`. Covered additions/deletions compare; untouched files are not removals; outside coverage is incompatible. |
| V-09f | AC-04; R-02 | M: `test_directory_exclusions_selected_check_and_empty_scope`, `test_cli_file_scope_baseline_comparison_and_no_overwrite`. Relative folder/file scopes and absolute in-root paths work; escaping and symlink scopes fail visibly. |
| V-10a, V-10b | AC-04/05; R-02 | M: `test_cli_file_scope_baseline_comparison_and_no_overwrite`. Baseline and comparison each refuse occupied JSON or sibling-only text, exit 2 and preserve all existing file bytes. |
| V-11 | AC-05; R-02 | I: `test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family`, `test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes`. Fresh/refresh in committed and unborn targets preserve target policy, env/report sentinels, unmanaged content, dirty source/index and outside-marker AGENTS bytes; selected stale files are removed and checks match. |
| V-12a, V-12b | AC-05; R-02 | I: `test_measurement_resources_changed_missing_checks_and_refresh`. Each of all six new resources is separately changed and removed. Two checks report exactly that path/category and preserve the complete tree/index; explicit refresh restores canonical bytes; final check matches. Source projection and target-owned bytes remain unchanged. |
| V-13 | AC-01/05 | I: `test_profile_contains_repo_stage_and_bounded_delivery_skills` and existing install/projection checks establish declared membership. Source/interface review of installer, profile guide, README, measurement guide and map confirms all six resources, old/new paths, independent fallback, target setup and unchanged narrow ownership/native-gate policy. Text review is separate from behavioral proof. |

## Preservation and limits

Exact pre-edit bytes for affected existing source/test/guide files, source target
policy/pins and the real index were captured before implementation in
`/tmp/T-001.1-pre-edit.tar`. The Git-local evidence run also retains the begin
snapshot. The archive is local continuation material, not a committed deliverable.
After verification, `.git/index` and all three source `.quality/` policy/pin files
still matched that archive byte-for-byte. Existing staged planning documents and
untracked task inputs remain separate from this implementation.

Evidence run: `run-20261024T175602Z-86fdbf3a89e8`, under
`.git/personal-skills/run-evidence/runs/`; architecture output is captured there.

No scenario is omitted or blocked in implementation evidence. Actual network
package installation and other operating systems remain unqualified. The final
aggregate `python3 tools/verify.py` is deliberately deferred to T-001.3, its
assigned owner. Architecture/contract validation does not replace behavioral
proof. Independent reviewers must assess this submission's bytes themselves.

## Next owner and complete remaining route

The required architecture gate is complete. The first outstanding stage is fresh
`task-maintainability-review`, followed by `task-contract-registry-updater`, fresh
independent `task-review-discovery`, then a separate fresh
`task-acceptance-review` decision. Start each stage separately; this implementer
invocation does not launch or manage reviewers. Registry work must record the
actual runtime, settings/setup, report-provenance and installation-membership
changes above. T-001.2 may consume these runtime paths and current evidence after
the required review route permits advancement.

## F-01 correction — pre-edit map

Authority: `docs/tasks/T-001.1/brief.md`; preparation: `preflight.md`
and `verification.md` revision 1 in this package. Preceding verdict: none;
`reviews/discovery-01.md` is evidence only, with open F-01 (suggested P2).
The user authorized correction directly before a separate acceptance decision.

F-01 invariant: effective maintainability policy must have valid consumed field
types and supported checks before discovery, analyzer execution or publication.
Numeric thresholds must exclude Boolean coercion; collection fields must not
accept strings or invalid elements. Sibling surfaces: profile, checks, numeric
threshold and directory names. Validate these at settings resolution.

Readiness remains applicable: same brief revision, verification revision, scope,
local pinned interpreter and dependency boundary. Existing task-owned dirty
work is retained. No dependency repair or active installation refresh is needed.
Pre-correction bytes/index/policy captured in `/tmp/T-001.1-correction-before`.
The prepared interpreter will be exercised by the focused real-tool regression.

Plan: add installed CLI valid controls and table-driven invalid fields; run
the regression before and after the correction; run owning measurement and
installer suites, architecture and contract checks. T-001.3 owns the aggregate
`python3 tools/verify.py`; implementation will not run it here.

Every supplied ledger identity occurs once below. Prior passes are navigation
only, not acceptance of corrected bytes. No prior row is blocked or unchecked.
The evidence column is a pre-edit plan; reviewer statuses remain unchanged.

| Row | Prior reviewer status | Pre-edit evidence plan / navigation | Next owner |
|---|---|---|---|
| V-01a | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-01b | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-02a | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-02b | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-02c | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-02d | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-03a | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-03b | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-03c | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-03-semantic | fail — F-01 | New installed CLI regression: valid hidden-source exclusion control; invalid threshold, exclusion, checks and profile rejected with policy-specific exit 2 and no report. Run fail-first then after fix. | Fresh independent discovery, then separate acceptance |
| V-04 | pass — selection only | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-05a | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-05b | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-05c | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-05d | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-05e | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-05f | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-06a | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-06b | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-07 | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-08a | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-08b | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-08c | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-08d | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-08e | pass for valid policy; invalid-type boundary separately fails above | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-09a | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-09b | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-09c | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-09d | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-09e | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-09f | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-10a | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-10b | pass | Prior discovery navigation; rerun owning real-tool measurement suite with existing setup/oracles recorded above. | Fresh independent discovery, then separate acceptance |
| V-11 | pass | Prior discovery navigation; rerun installer suite; V-13 documentary context retained. | Fresh independent discovery, then separate acceptance |
| V-12a | pass | Prior discovery navigation; rerun installer suite; V-13 documentary context retained. | Fresh independent discovery, then separate acceptance |
| V-12b | pass | Prior discovery navigation; rerun installer suite; V-13 documentary context retained. | Fresh independent discovery, then separate acceptance |
| V-13 | pass — documentary/structural, not runtime proof | Prior discovery navigation; rerun installer suite; V-13 documentary context retained. | Fresh independent discovery, then separate acceptance |

Correction owner: this implementer. Evidence/capability owner: fresh independent
discovery; authority owner: separate acceptance. No preparation revision or new
requirement is proposed; semantic-invalid regression implements AC-02/F-01.
Production/test changes re-enter maintainability review, registry updater, fresh
discovery and separate acceptance after implementation architecture evidence.

## F-01 correction result and submission

Invalid effective maintainability policy now fails at the shared settings boundary
with its path and invalid field in the diagnostic. Both target and shipped policy
pass through that boundary. Boolean/non-integer/negative thresholds, invalid
collections/elements, unsupported checks and missing consumed fields are rejected.
Valid custom profiles, zero targets, check subsets and empty exclusions remain
supported. No fallback or report is produced for invalid target policy.

Implemented: READY_FOR_REVIEW

- Authority: `docs/tasks/T-001.1/brief.md`.
- Preflight/context reference: `docs/tasks/T-001.1/preflight.md`, including
  Decision context; `docs/tasks/T-001.1/verification.md` revision 1;
  `docs/tasks/T-001.1/reviews/discovery-01.md` sections 2–3 and 10, Appendices A/B;
  `docs/tasks/T-001.1/reviews/maintainability-01.md` is prior-byte evidence only.
- Preceding verdict: no acceptance verdict was supplied. Discovery reported F-01
  (suggested P2); the user directly authorized its correction. No ACCEPT or
  CHANGES_REQUESTED verdict is invented here.
- Finding/scenario IDs: complete finding inventory is F-01. Complete scenario
  inventory is the 37 individually named rows in the pre-edit map above,
  including the added reviewer row V-03-semantic. All prior reviewer statuses
  remain unchanged; current implementation results are separate evidence below.
- Complete findings and invariant: F-01 — semantic-invalid policy was accepted;
  Boolean targets became numeric thresholds and string exclusions became character
  sets, including excluded `.git` Python. Effective policy must be valid before
  discovery, measurement or publication. TOML syntax validity is insufficient.
- Influenced sibling surfaces: profile must be a non-empty string; checks must be
  a non-empty list containing supported check names; complexity_target must be a
  non-negative integer excluding Boolean values; exclude_directories must be a
  list of non-empty strings. Shared settings validation covers both origins.
  The installed regression exercises 17 invalid/missing-field cases and two valid
  controls, including invalid Python hidden under `.git` with default exclusions.
- Attempts and discarded hypotheses: the initial fail-first test reused an output
  name; the first accepted invalid policy produced a report that masked later
  cases with overwrite errors. The fixture was corrected to use distinct outputs.
  R then failed all 17 invalid subcases against unchanged production for the
  intended wrong-success or missing policy-specific diagnostic oracle. One
  production correction was applied; R passed. No production alternative was
  attempted or discarded. No stopped correction or retained failed hypothesis.
- Current scoped diff: this correction changes only `scripts/maintainability.py`
  (17-line validator plus settings dispatch), `tests/test_maintainability.py`
  (one table-driven installed CLI regression), and this existing implementation
  record. All prior task implementation, registry work and review files remain
  separate. The installer was inspected: membership is unchanged and copies the
  corrected runtime; no installer edit is needed. Approved plans were not edited.
- Coverage ledger: the pre-edit table preserves every supplied identity and prior
  status. Current evidence for V-03-semantic is R: valid default policy excludes
  the invalid `.git/hidden.py`; each invalid case exits 2, names policy/field,
  and preserves the complete target snapshot, including index and saved reports.
  Custom valid policy still completes. Incomplete reason: none for implementation
  regression; independent corroboration remains owed. Next owner/status: fresh
  discovery; prior reviewer fail remains unchanged. For every V-01–V-10 row,
  M reruns the existing tests and setup/oracles mapped in the original AC table
  above; for V-11/V-12 rows, I reruns their actual installer lifecycle assertions.
  V-13 has current I membership assertions and prior documentation navigation;
  fresh discovery owns renewed documentary coherence assessment. Each row's prior
  pass remains navigation, not independent evidence for corrected bytes. No prior
  blocked or unchecked row exists, and none is silently removed.
- Reviewer reproducer: original DISC-07 command was
  `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B /tmp/T-001.1-policy-type-probe.py`.
  Its Appendix B asserts defective success and reads an invalid-policy report;
  it was not rerun unchanged as a passing gate. R is its durable corrected
  equivalent through the installed launcher, with both original triggers,
  hidden-source control and policy-specific exit-2/no-write oracle. R passed.
- Owning suite: M and I below both passed with no skips.
- Broad/aggregate gate: `python3 tools/verify.py` skipped by explicit brief
  ownership; T-001.3 owns final combined proof. A and C below passed as required
  structural checks, not behavioral or acceptance proof.
- Remaining reviewer coverage: fresh discovery must assess all 37 carried rows
  for the corrected bytes, including F-01 and its sibling fields. No row is
  accepted or reclassified by this implementer.
- Next: fresh `task-maintainability-review` →
  `task-contract-registry-updater` → fresh independent `task-review-discovery` →
  separate fresh `task-acceptance-review`. Architecture evidence A is current;
  the correction affects production/test scope previously reviewed for
  maintainability, so that conditional stage is owed again. Registry updater
  checks the strengthened existing invalid-policy contract and affected refs.
  This invocation does not launch or manage these reviews.

Current correction command evidence (repository root):

| Key | Exact command | Implementation result |
|---|---|---|
| R | `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py -k invalid_policy_settings -v` | Fail-first: exit 1, 17 subcase failures after distinct-output fixture fix. After correction: exit 0, 1 test, 1.792 s; no skips. |
| M | `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py` | Exit 0; 26 tests, 9.451 s; real pinned analyzers; no skips. |
| I | `python3 -B -m unittest discover -s tests -p test_install_development_skills.py` | Exit 0; 36 tests, 24.483 s; no skips. |
| A | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Exit 0; 4 tests, 0.162 s; no skips; captured once through active-installation run-evidence check wrapper. |
| C | `python3 tools/check_contracts.py --root .` | Exit 0; 6 subsystems, 7 indexed plan refs; structural only. |
| D | `git diff --check` | Exit 0; whitespace only. |

Deliverables:
- Shared policy validation and installed CLI regression, with this correction
  handoff retaining complete review continuity.

Actual contract impact:
- Strengthened the existing invalid-present-policy failure contract at the common
  settings boundary; no new CLI or report field, managed resource, environment
  behavior, dependency or registry membership. Consumed policy types and supported
  check values are validated before use. Registry wording/current references are
  left to the designated updater.

Executable contract declarations changed:
- `scripts/maintainability.py` effective maintainability-policy validation.

The correction-only diff was compared with `/tmp/T-001.1-correction-before`.
Real index and all three source `.quality/` policy/pin files match captured
pre-correction bytes. Optional evidence run:
`run-20261024T181259Z-4e8bfa85116f`. No dependency downloads, active-installation
refresh, aggregate suite, external reviews, commits or network checks occurred.
Other operating systems and actual package provisioning remain unqualified.
