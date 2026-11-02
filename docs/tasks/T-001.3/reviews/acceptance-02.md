# T-001.3 acceptance decision 02

The staged foundation guidance and installed-composition proof satisfy the bounded task. Independent discovery supports every required scenario. The staged focused preflight resolves prior H-01: the aggregate was run and its exit 1 is retained, while the four expected active-profile differences must remain untouched during this invocation. This is not an all-green aggregate claim. The coordinator may advance the accepted T-001.3 contract to T-002; no advancement is performed here.

Verdict: **ACCEPT**

Provenance: independent session; no reviewed production, test, fixture or harness bytes authored. Guided profile. Only this new numbered report is written.

Findings: No findings.

Observations / stated assumptions: the user's current clarification supplies completed, passing maintainability and registry stages. This is user-attributed conditional-stage evidence, not a new maintainability verdict. The historical outstanding-stage language in results.md does not override that clarification. No changed implementation bytes invalidate those stages. Distribution-removal isolation proves the stated installed boundary; OS containment, downloads, cross-platform support and live agent compliance remain unqualified and outside this task.

Approved deferrals: none. Resolving H-01 is interpretation of existing authority, not a known-issue deferral or gate waiver.

## Admission, preparation and current scope

Authority: [brief.md](../brief.md), its parent authority, AC-01–AC-06 and R-05/R-06. Preparation: [verification.md](../verification.md) revision 1 and [preflight.md](../preflight.md), including its focused H-01 reconciliation. Submission: [results.md](../results.md). Prior decision: [acceptance-01.md](acceptance-01.md), historical INCONCLUSIVE. Admitted independent publication: [discovery-01.md](discovery-01.md), complete V-01–V-10 with continuation and D1–D7 plus validator evidence.

HEAD: `0f747fa30e96aca7a72f86469d276cda901cf23f`. Current staged binary-diff SHA-256: `9030b3e42e77d2823dc3f3978ca8fc1f3503eee7956f938d65ced537d01de9cc`. Worktree matches index. All 11 discovery-recorded index blobs other than preflight match exactly. The changed preflight blob contains the explicit H-01 readiness delta, not changed implementation/scenarios. Discovery and acceptance-01 are additional staged evidence artifacts; all 14 staged paths are safely task-owned. No unrelated overlap or active installation refresh is present. Brief digest matches preparation. Scope remains guidance, installed-boundary tests, registry/reference synchronization and evidence.

Contract reconciliation: EXPECTED ART-007/IF-004 preserves native scope/policy/requiredness/owner alongside advisory discovery. ACTUAL foundation guidance implements those obligations and preserves aggregate reuse and missing/stale proof recovery. DECLARED optional gates template carries commands and references without copied thresholds or a new required stage. DISCOVERABLE measurement.json/index, skills guide and development guide identify current authority and qualify ART-006 as installed test capability, not live compliance. Existing installer selections already manage both skills/template/profile guide and six measurement resources. No semantic drift or stale routing was demonstrated. Discovery D6 establishes current canonical registry validation; its valid-record and deliberately invalid missing-declaration probe supplies both validator outcomes. D2 independently exercises valid and invalid settings. These checks do not substitute for behavioral composition evidence.

## Reconciled coverage

Every row below is admitted as pass against the unchanged implementation bytes and verification revision 1. Submission remains producer-attributed; the independent evidence column supplies the decisive proof. Guidance cases prove documented obligations, not agent obedience. All stable row IDs and cases are retained from discovery.

| Row | AC / risk | Material cases | Setup / oracle | Submission | Current independent evidence | Result |
|---|---|---|---|---|---|---|
| V-01a | AC-01/06; R-05 | Existing registry | Carry command/scope/policy/requiredness/owner | results.md claims passing evidence | Static trace: repo-foundation 186–213; architecture-guardrails 225–253; results handoff a | pass |
| V-01b | AC-01/06; R-05 | Documented commands without registry | No new mandatory registry/runner | results.md claims passing evidence | Same guidance; results handoff b retains all five fields | pass |
| V-01c | AC-01/06; R-05 | No applicable native command | Record absence; invent no check | results.md claims passing evidence | Same guidance; results handoff c | pass |
| V-01d | AC-01/06; R-05 | Current aggregate covers constituents | Reuse only matching scope/policy/bytes | results.md claims passing evidence | Same guidance; results handoff d | pass |
| V-01e | AC-01/06; R-05 | Missing required evidence | Native owner/recovery route remains | results.md claims passing evidence | Same guidance; results handoff e | pass |
| V-01f | AC-01/06; R-05 | Stale required evidence | No waiver from advisory success | results.md claims passing evidence | Same guidance; results handoff f | pass |
| V-01g | AC-01/06; R-05 | Whole-project native, affected-path metrics | Do not narrow native scope | results.md claims passing evidence | Same guidance; results handoff g | pass |
| V-02 | AC-01/02/05 | Four source skills, template, installer/profile/README | No conflicting route; installer already selects changed resources | results.md claims passing evidence | Static inspection plus D3/D4; bootstrap/readiness no-change dispositions corroborated | pass |
| V-03 | AC-03; R-06 | Dirty/staged/untracked baseline; edit/add/delete; sibling exclusion | CC 5→7; captured worktree hashes; immutable baseline/source/index | results.md claims passing evidence | D2: test_snapshot_preserves_staged_unstaged_untracked_and_index; D7 independent CC 4→6 probe | pass |
| V-04 | AC-03; R-06 | Empty parent then new file; repeated comparison | CC 2 then 3; null before/delta; original/index preserved | results.md claims passing evidence | D2: test_empty_folder_baseline_preserves_absence_across_edits | pass |
| V-05a | AC-04; R-06 | Neither target file | Constant native values; independent targets, origin/path/hash; no policy writes | results.md claims passing evidence | D2: test_settings_select_each_target_file_independently | pass |
| V-05b | AC-04; R-06 | Maintainability only | Constant native values; independent targets, origin/path/hash; no policy writes | results.md claims passing evidence | D2: test_settings_select_each_target_file_independently | pass |
| V-05c | AC-04; R-06 | Ruff only | Constant native values; independent targets, origin/path/hash; no policy writes | results.md claims passing evidence | D2: test_settings_select_each_target_file_independently | pass |
| V-05d | AC-04; R-06 | Both target files | Constant native values; independent targets, origin/path/hash; no policy writes | results.md claims passing evidence | D2: test_settings_select_each_target_file_independently | pass |
| V-06a | AC-04; R-06 | Malformed maintainability TOML | Valid controls; exit 2, no fallback/output, target preservation | results.md claims passing evidence | D2: test_invalid_target_settings_and_unrelated_root_ruff | pass |
| V-06b | AC-04; R-06 | Malformed Ruff TOML | Valid controls; exit 2, no fallback/output, target preservation | results.md claims passing evidence | D2: test_invalid_target_settings_and_unrelated_root_ruff | pass |
| V-06c | AC-04; R-06 | Boolean target/string exclusions and typed-field matrix | Valid controls; exit 2, no fallback/output, target preservation | results.md claims passing evidence | D2: test_invalid_policy_settings_fail_before_measurement | pass |
| V-07 | AC-04; R-06 | Missing pinned tools; executable setup recipe | -S refusal; target-aware recipe; mock only package provisioning seam | results.md claims passing evidence | D2: test_missing_pins_recipe_dispatches_setup_for_selected_target; no download qualification | pass |
| V-08a | AC-03/04; R-06 | Neutral increases/decreases and successful breach | Actual values/deltas, neutral saved/console labels; exit 0 | results.md claims passing evidence | D2: test_saved_and_console_reports_use_neutral_labels | pass |
| V-08b | AC-03/04; R-06 | Native unknown count in both directions | null count/delta rather than zero; actual installed Ruff reports | results.md claims passing evidence | D2: test_ruff_missing_diagnostics_never_become_numeric_zero | pass |
| V-08c | AC-03/04; R-06 | Format 3 baseline | Explicit incompatible exit 2; original preserved | results.md claims passing evidence | D2: test_cli_rejects_incompatible_baseline_identities | pass |
| V-08d | AC-03/04; R-06 | Format 4 baseline | Explicit incompatible exit 2; original preserved | results.md claims passing evidence | D2: test_cli_rejects_incompatible_baseline_identities | pass |
| V-08e | AC-03/04; R-06 | Repeat against original with fresh names | Original and successive JSON/text pairs survive | results.md claims passing evidence | D2: test_empty_folder_baseline_preserves_absence_across_edits; test_snapshot_preserves_staged_unstaged_untracked_and_index | pass |
| V-08f | AC-03/04; R-06 | JSON-only collision for all three operations | Exit 2; sentinel survives; absent sibling stays absent; index/source intact | results.md claims passing evidence | D2: test_each_report_sibling_collision_refuses_write | pass |
| V-08g | AC-03/04; R-06 | Text-only collision for all three operations | Same refusal and preservation oracle | results.md claims passing evidence | D2: test_each_report_sibling_collision_refuses_write | pass |
| V-09 | AC-02/05; R-06 | Fresh install; changed/missing all six shared files, both skills, template, guide; repeated check/refresh | Drift exit 1 without repair; refreshed match; unrelated policy/env/reports/index/AGENTS preserved | results.md claims passing evidence | D3 focused resource journey; D4 all 36 installer tests, including all-family ownership journeys | pass |
| V-10 | AC-06; R-05 | Native whole-project F401 vs installed advisory success | Clean native 0; unused import native 1 with F401/sample.py; measure 0 CC 5; preserve prior tree | results.md claims passing evidence | D1 independently executed real subprocess case; repeated in D2; handoff retains failed native obligation | pass |

## Aggregate admission and H-01 disposition

Consumed exact aggregate command: `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python tools/verify.py`. Initial owner/stage: implementer, after focused checks. Producer-attributed approved host execution: 528 tests passed, no skips; exit 1 solely for four active-profile differences. Earlier sandbox containment failures remain historical and were superseded by the authorized host test execution, not silently counted as passes.

Discovery aggregate: **not run**. Discovery owns its decision not to duplicate the expensive run after clean targeted evidence; no targeted failure suppressed the aggregate. Consumed order: D1 mixed native/advisory → D2 measurement → D3 resource journey → D4 installer → D5 architecture → D6 contracts → D7 installed preservation probe, plus the independent validator probe. D5 passes the canonical architecture command; D6 passes `python3 tools/check_contracts.py --root .` for the current registry. Acceptance executes no behavioral probe, architecture/registry gate or aggregate.

**H-01 — resolved.** Prior status: blocked evidence/policy gap, not a confirmed defect. Current evidence: staged preflight's focused `python3 scripts/install_development_skills.py --check .`, exit 1, 95 paths compared, exactly four changed paths: profile README, repo-foundation, architecture-guardrails and its gates template; no missing/unrelated managed paths. The brief requires aggregate execution and truthful drift reporting while explicitly forbidding active refresh; it does not require the preserved active installation to equal edited source. V-09 independently proves disposable installation/refresh/drift behavior. Thus the failed constituent remains reported as failed and has no unfulfilled task-specific repair obligation. Neither advisory success nor this disposition waives a native hard failure. Existing preservation policy, current unchanged behavioral evidence and the focused readiness delta resolve the prior uncertainty without a repeat aggregate or production correction.

H-01 impact was inability to decide gate applicability, not demonstrated runtime damage; exposure is limited to the four intentionally preserved installed resources. Mitigation is explicit separate reporting plus independently qualified disposable targets. Correction owner: none. Evidence owner: discovery (behavioral evidence) and focused preflight (current drift comparison); authority owner: brief/coordinator. Reopen if missing/unrelated drift, changed behavioral bytes or a non-drift gate failure appears.

Questions / unchecked work: none within the bounded task. No required row remains blocked or unchecked.

Scope / residual risk: only the admitted installed composition and documented foundation guidance are accepted. The aggregate is not green; its expected active-profile mismatch is retained under existing task authority. Live compliance and later T-002–T-005 integration are not qualified.

Next: coordinator may advance T-001.3 and pass the accepted installed contract and these evidence records to T-002. No tracker mutation, commit or advancement is performed by this review.

## Review continuation

- Iteration/current identity: acceptance 02; HEAD and index digest above; discovery implementation blobs unchanged, focused preflight delta admitted separately.
- Coverage rows: V-01a/b/c/d/e/f/g, V-02, V-03, V-04, V-05a/b/c/d, V-06a/b/c, V-07, V-08a/b/c/d/e/f/g, V-09, V-10 = pass. Prior discovery/acceptance-01 scenario statuses were pass and remain pass.
- Finding IDs: none. Evidence-gap H-01: prior blocked → resolved by focused readiness evidence and existing task authority. No correction owner or defective sibling surface. Evidence owners: discovery/preflight; authority owner: brief/coordinator.
- Preparation/context: brief; verification revision 1; current preflight with H-01 delta; R-05/R-06; results; discovery-01; acceptance-01; current user clarification that maintainability and registry stages passed.
- Reviewer regressions: none. No added tests, probe files or behavioral commands.
- Aggregate consumed: implementer host exit 1 for four expected drift paths; discovery not rerun; current D5/D6 pass; no all-green claim. H-01 resolved as above.
- Next: coordinator → T-002 with accepted installed contract and bounded evidence; reopen only for changed material facts or bytes.

## Identity and write audit

Read-only identity checks: compared discovery's scoped index blobs, verified brief SHA-256 and worktree/index equality; `git diff --cached --check` passed. These checks prove identity/format only. Behavioral and architecture/registry evidence is consumed, not rerun.

Exact status before write:

```text
M  docs/contracts/index.json
M  docs/contracts/measurement.json
M  docs/development.md
A  docs/tasks/T-001.3/preflight.md
A  docs/tasks/T-001.3/results.md
A  docs/tasks/T-001.3/reviews/acceptance-01.md
A  docs/tasks/T-001.3/reviews/discovery-01.md
A  docs/tasks/T-001.3/verification.md
M  skills/README.md
M  skills/architecture-guardrails/SKILL.md
M  skills/architecture-guardrails/templates/gates.yaml
M  skills/repo-foundation/SKILL.md
M  tests/test_install_development_skills.py
M  tests/test_maintainability.py
```

Exact status after write (verified):

```text
M  docs/contracts/index.json
M  docs/contracts/measurement.json
M  docs/development.md
A  docs/tasks/T-001.3/preflight.md
A  docs/tasks/T-001.3/results.md
A  docs/tasks/T-001.3/reviews/acceptance-01.md
A  docs/tasks/T-001.3/reviews/discovery-01.md
A  docs/tasks/T-001.3/verification.md
M  skills/README.md
M  skills/architecture-guardrails/SKILL.md
M  skills/architecture-guardrails/templates/gates.yaml
M  skills/repo-foundation/SKILL.md
M  tests/test_install_development_skills.py
M  tests/test_maintainability.py
?? docs/tasks/T-001.3/reviews/acceptance-02.md
```

Only the new untracked acceptance-02 report differs. Index content is unchanged.
