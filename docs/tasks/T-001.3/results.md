# T-001.3 implementation evidence

Implemented: READY_FOR_REVIEW. Independent review and acceptance are still owed.
Authority: [brief.md](brief.md). Preparation: [verification.md](verification.md)
revision 1 and [preflight.md](preflight.md). Alternative briefs were not used.

## Changes and dispositions

- `skills/repo-foundation/SKILL.md`: discover installed advisory measurement
  beside native commands; carry native scope, policy, requiredness and stage
  owner, aggregate reuse and missing/stale proof duties.
- `skills/architecture-guardrails/SKILL.md` and `templates/gates.yaml`: same
  discovery boundary, explicit target setup, independent target/default settings;
  optional template has no thresholds or new review requirement. Existing
  conditional semantic-review duties remain intact.
- `skills/README.md`: synchronize the managed profile guide's discovery route.
- `tests/test_maintainability.py`: reuse existing cases at the installed boundary;
  add one real native-hard/advisory composition case. No production runtime change.
- `tests/test_install_development_skills.py`: extend existing all-measurement-file
  drift/refresh case to both changed source skills, the template and profile guide.
- `project-bootstrap` inspected: no change. It plans a capability and delegates
  placement/enforcement to foundation skills; it selects no conflicting runtime.
- `foundation-readiness-review` inspected: no change. Optional registry input and
  separate hard/advisory policy remain compatible; existing conditional review
  availability checks are retained.
- Installer inspected: no membership or ownership change needed. Both skills,
  all six measurement files and `PROFILE_SKILLS_README` are already explicit
  managed selections. README and tool guide already document the installed
  launcher, target/default settings and explicit setup accurately; no change.
  Project-map paths remain accurate. Active `.agents/` was not refreshed.

## Structural discovery handoffs (V-01, R-05)

These are concrete policy traces through the changed source guidance, not live
agent execution. For examples a/b/d/e/f/g, the fixture's native obligation is:
command `python -m ruff check --no-cache --config <target>/native-ruff.toml <target>`;
scope whole project; policy `<target>/native-ruff.toml`, rule F401; required true;
stage owner implementer. Advisory command is
`python <target>/.agents/scripts/measure_maintainability.py measure sample.py
--root <target> --output advisory.json`; scope sample.py; policy independently
selected target/default settings, recorded in report identity; advisory result;
owner implementer. Native and advisory policy are separate.

| Case | Concrete discovery/evidence input | Handoff under changed guidance |
|---|---|---|
| V-01a | Existing registry lists that native obligation and advisory reference | Carry both commands and each scope/policy/requiredness/owner; retain native F401 as blocking. No second registry. |
| V-01b | No registry; AGENTS documents the same five native fields | The documented command suffices. Discover through instructions/map/native config as needed; retain the same native obligation. |
| V-01c | Instructions/map/native task config declare no applicable native check | Record native command/scope/policy/requiredness/owner as absent. Publish enabled advisory command and its own policy/owner. Select no new linter/typechecker. |
| V-01d | Current `verify` result includes the named native check for identical relevant bytes, full scope and policy | Carry that aggregate evidence reference for the native obligation, preserving owner and requiredness; do not rerun the constituent merely for a report. |
| V-01e | No result exists for required F401 check | Keep native proof missing, owner implementer; recover by authorized whole-project native command. Advisory completion supplies no native evidence. |
| V-01f | F401 result predates the new unused import | Mark required native proof stale; retain native policy/owner and authorized rerun route. No waiver from advisory completion. |
| V-01g | Native whole-project check versus sample.py advisory scope | Handoff retains whole-project required native scope and implementer owner; measured paths do not narrow it. |

## Real installed proof and coverage

Interpreter, relative to repository root:
`P=.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`.
Confirmed pins: Radon 6.0.1, Ruff 0.14.2, mando 0.7.1, colorama 0.4.6,
six 1.17.0. All CLI launches remove PYTHONPATH/PYTHONHOME, use an unrelated cwd
and a separate Git target. `installed_launcher()` reuses the relocated complete
distribution helper, installs into that target, then deletes the disposable
distribution before invoking the installed CLI. The actual checkout is never
modified for isolation. The prepared interpreter supplies pinned packages;
installed helpers/defaults/pins resolve beside the target launcher, with no
source-distribution or user-global helper fallback. This is the specified
distribution-removal isolation proof, not an OS access-control qualification.

| Cases / acceptance | Current executable evidence and oracle |
|---|---|
| V-02, AC-01/02 | Source dispositions above; disposable fresh-install package byte equality and expanded resource drift/refresh case. Structural guidance inspection is separate from runtime evidence. |
| V-03, AC-03, R-06 | `test_snapshot_preserves_staged_unstaged_untracked_and_index`: installed baseline of `.` captures committed Python, staged CC 3, different worktree CC 5, untracked code and untouched sibling. Source snapshots decode to actual worktree bytes and hashes. Actual edit raises CC 5→7 (+2), adds a symbol (new, before/delta null), then deletes captured sample.py (removed, before 5, current/delta null). Compare scopes omit untouched sibling. Source, real index bytes, staged content and original JSON/text reports remain exact at asserted checkpoints; fresh after/removed pairs coexist. |
| V-04, AC-03 | `test_empty_folder_baseline_preserves_absence_across_edits`: installed baseline captures empty `area`, later file has real CC 2 then 3, new classification and null before/delta. Reports/source/index survive; outside/missing/excluded scopes and ordinary empty measure refuse. |
| V-05a–d, AC-04 | Existing installed `test_settings_select_each_target_file_independently`: neither/each/both target files; CC remains 5, three-argument count remains 3, targets vary independently; exact origin/path/hash and target bytes asserted. |
| V-06a/b, AC-04 | Existing installed `test_invalid_target_settings_and_unrelated_root_ruff`: each malformed target TOML refuses with exit 2, no complete measurement; valid controls and unrelated root config isolation. |
| V-06c, AC-04 | Existing installed `test_invalid_policy_settings_fail_before_measurement`: full typed-field matrix including Boolean complexity target/string exclusions, whole-tree equality and valid controls. |
| V-07, AC-04 | Existing `test_missing_pins_recipe_dispatches_setup_for_selected_target`: missing-pins installed-resource launcher under `-S`, exit 2, executable target-aware recipe; replay recipe at mocked provisioning seam proves target environment and same-install pin selection, without downloads. Whole target preserved. |
| V-08a, AC-04 | Installed `test_saved_and_console_reports_use_neutral_labels`: real numeric increases/decreases, breached CC and measure/compare exit 0, neutral saved/console labels; existing boundary cases retain numeric/threshold semantics. |
| V-08b, AC-03/04 | `test_ruff_missing_diagnostics_never_become_numeric_zero` now obtains real installed Ruff reports for zero-count/overload/override cases. Both comparison directions retain null unknowns and deltas; comparison semantics remain tested directly through the runtime module. |
| V-08c/d, AC-04 | Installed `test_cli_rejects_incompatible_baseline_identities` rejects formats 3 and 4 with explicit incompatible result and unchanged original report. |
| V-08e, AC-03/04 | Installed empty-folder and dirty journeys retain original report pairs and multiple fresh comparison pairs. |
| V-08f/g, AC-04 | Installed `test_each_report_sibling_collision_refuses_write`: baseline/measure/compare × JSON/text-only collision; exit 2, sentinel unchanged, absent sibling stays absent, source/index preserved. |
| V-09, AC-05 | Expanded `test_measurement_and_discovery_resources_changed_missing_checks_and_refresh`: all six shared measurement files, both changed skills, template and guide; fresh equality, changed/missing read-only checks twice each, explicit refresh then match; target policy/environments/reports, index and AGENTS survive. Existing whole-family committed/unborn journeys cover unrelated ownership and marked-block bytes. |
| V-10, AC-06 | New `test_native_hard_failure_remains_separate_from_installed_advisory_success`: declared whole-project F401 policy, clean source passes (0). Add unused `import os` before a function with four unconditional if statements: native command fails (1) and names F401/sample.py; installed measure of those source bytes completes (0), CC 5. Tree snapshot proves native check changes nothing; all prior target entries survive advisory output publication. |

For V-10 the target's AGENTS names the exact executable command, whole-project
scope, `native-ruff.toml` policy, required true and implementer owner. Native
diagnostic is F401 for the seeded unused import in sample.py. That native result
is **failed**, while the separately reported advisory result is **complete**.
The native obligation remains failed under its own policy; CC 5 does not waive it.
The clean control establishes that this is a rule violation, not missing tools.

## Verification execution

Commands use repository-root cwd and `PYTHONDONTWRITEBYTECODE=1`:

- `$P -m unittest discover -s tests -p test_maintainability.py -k installed`:
  2 passed, including the real mixed hard/advisory outcome.
- Targeted `-k snapshot`, `-k sibling`, `-k empty_folder`: each passed.
- `$P -m unittest discover -s tests -p test_maintainability.py`:
  33 passed, no skips (17.390 seconds).
- Installer resource case `-k measurement_and_discovery`: passed, no skips.
- `$P -m unittest discover -s tests -p test_install_development_skills.py`:
  36 passed, no skips (27.119 seconds).
- `$P tools/verify.py > /tmp/t0013-verify.log 2>&1`: seven checks,
  two failed. The orchestrator suite had 3 failures/13 errors under sandbox
  process restrictions; the read-only active-profile check reported four changed
  paths (guide, repo-foundation, architecture-guardrails and gates template).
  The 305-test root suite, including architecture policy, passed with no skips;
  contract validation passed. No profile refresh was performed.
- Approved host rerun `$P tools/verify.py > /tmp/t0013-verify-host.log 2>&1`:
  all five suites passed: 3 + 10 + 3 + 207 + 305 = 528 tests, no skips.
  Root suite took 68.184 seconds; orchestrator suite took 36.981 seconds.
  Contract validation passed (6 subsystems, 8 indexed plan refs). Seven checks,
  one failed: only the same four-path active-profile drift. Exit 1 is retained
  truthfully; this is not an all-green aggregate result. Architecture is covered
  by the current root suite's `test_architecture.py`; the contract command ran
  explicitly in the aggregate. No duplicate run was needed for reporting.
- `git diff --check`: passed. Final status retains the pre-existing staged
  alternative briefs, verification design and task-index changes separately.
  They were not changed by implementation.

The first full measurement run failed two fixture cases because installation
setup occurred after their index snapshot. Move installation before snapshot;
targeted collision/empty cases and the full measurement suite then passed. No
runtime preservation defect was observed. Optional run-evidence sidecar was
unavailable (`git_metadata_unwritable`), so it was not retried.

## Ordered handoff

First outstanding stage: fresh `task-maintainability-review`, because the
submission changes significant installed-boundary tests/fixtures. Then
`task-contract-registry-updater` must synchronize actual ART-007/IF-004 discovery
and ART-006 composition authority in the current records/index; no new registry
requirement is introduced. Then fresh independent `task-review-discovery`, then
a separate `task-acceptance-review` decision. The implementer does not launch
those stages or certify acceptance in this invocation.

Discovery must corroborate R-05's mixed hard/advisory result and R-06's unrelated
cwd plus one preservation/refusal probe on fresh disposable targets. Carry all
V-01a–g, V-02, V-03, V-04, V-05a–d, V-06a–c, V-07, V-08a–g, V-09 and V-10 rows
above as implementation evidence, with reviewer status unchecked. No live model,
package-download or agent-compliance qualification was run or claimed. T-005's
full reviewer/correction journey remains outside scope.
