# T-004.1 discovery-01 correction

Authority: brief.md r1, verification.md r1, preflight.md, controller-contract.md; preceding discovery is partial evidence, no acceptance verdict.

F-01 invariant: pre-existing dirty owner work must retain its evaluated filesystem identity, regardless of allowed-path membership. Siblings: executable regular files and symlink target/referent identity, inside/outside scope. Preserve initial content/status/index checks.

Pre-edit ledger mapping (prior statuses remain unchanged; implementation results are separate):

| Row | Prior status | Planned evidence / next owner |
|---|---|---|
| V-01 | pass | Navigation only; fresh discovery re-establishes applicability |
| V-02a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-02b | fail | Fail-first public owner identity matrix, then corrected run; fresh discovery owns row disposition |
| V-02c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-02d | pass | Navigation only; fresh discovery re-establishes applicability |
| V-03a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-03b | pass | Navigation only; fresh discovery re-establishes applicability |
| V-03c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-03d | pass | Navigation only; fresh discovery re-establishes applicability |
| V-03e | pass | Navigation only; fresh discovery re-establishes applicability |
| V-03f | pass | Navigation only; fresh discovery re-establishes applicability |
| V-04a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-04b | pass | Navigation only; fresh discovery re-establishes applicability |
| V-04c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-04d | pass | Navigation only; fresh discovery re-establishes applicability |
| V-04e | pass | Navigation only; fresh discovery re-establishes applicability |
| V-05a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-05b | pass | Navigation only; fresh discovery re-establishes applicability |
| V-05c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-06 | pass | Navigation only; fresh discovery re-establishes applicability |
| V-07a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-07b | pass | Navigation only; fresh discovery re-establishes applicability |
| V-07c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-07d | blocked | Fresh supported-host reviewer: launch failure and containment proof |
| V-07e | blocked | Fresh supported-host reviewer: launch failure and containment proof |
| V-08a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-08b | pass | Navigation only; fresh discovery re-establishes applicability |
| V-08c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-08d | pass | Navigation only; fresh discovery re-establishes applicability |
| V-09a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-09b | pass | Navigation only; fresh discovery re-establishes applicability |
| V-09c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-09d | pass | Navigation only; fresh discovery re-establishes applicability |
| V-09e | pass | Navigation only; fresh discovery re-establishes applicability |
| V-09f | unchecked | Fresh discovery: direct portable failure/later-marker or publication-failure control |
| V-10a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-10b | pass | Navigation only; fresh discovery re-establishes applicability |
| V-10c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-10d | pass | Navigation only; fresh discovery re-establishes applicability |
| V-10e | pass | Navigation only; fresh discovery re-establishes applicability |
| V-11a | pass | Navigation only; fresh discovery re-establishes applicability |
| V-11b | pass | Navigation only; fresh discovery re-establishes applicability |
| V-11c | pass | Navigation only; fresh discovery re-establishes applicability |
| V-11d | pass | Navigation only; fresh discovery re-establishes applicability |
| V-11e | unchecked | Fresh discovery: direct portable failure/later-marker or publication-failure control |
| V-12 | pass | Navigation only; fresh discovery re-establishes applicability |
| V-13 | pass | Navigation only; fresh discovery re-establishes applicability |
| G-01 | blocked | Maintainability reviewer: original-B comparison, limits and rationale dispositions |

Aggregate gate ownership: fresh discovery reviewer, per correction protocol. Implementer runs owning suite and required architecture/contract checks; no implementation aggregate claim.

Original baseline: `.quality/reports/T-004.1-preflight-20261110-01.json` and `.txt`; preserve prior implementation comparisons. Seven current Python hashes checked against implementation-20261110-02 before correction. No scope, authority, dependency or permission change. Existing pinned interpreter is a broken symlink on this host; attempt current comparison without provisioning and report limits. No live/provider checks.

## Implementation evidence (reviewer row statuses above unchanged)

Five public-boundary regressions: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k dirty_owner`. All five fail on the old implementation with unexpected `passed` inspection (`/tmp/T-004.1-correction-01-before-02.log`), all five pass corrected (`/tmp/T-004.1-correction-01-after.log`). An initial fixture attempt used external allowed symlinks and failed manifest validation; corrected to an ignored in-repository referent for allowed paths before the valid fail-first run. No invalid setup counted as behavior proof.

Changed: `scripts/controller_git.py` captures dirty-file identity at initialization using the same helper as candidates (content, executable metadata, symlink spelling and evaluated referent). `scripts/controller.py` compares that identity before publishing and refuses missing dirty-owner identity in older frozen runs. The legacy accepted-baseline shape admits the additional field while retaining older shapes; no frozen record is rewritten. `tests/test_actor_operations.py` reuses terminal actor setup and checks inside/outside scope, unchanged-owner positive control, same-status mutation refusal, unchanged ledger and absent check invocation.

Native implementation checks:
- Actor suite: 37 tests pass; `/tmp/T-004.1-correction-01-actors.log`.
- Git suite: 14 tests pass; `/tmp/T-004.1-correction-01-git-02.log`. First run exposed strict accepted-baseline shape rejection; fixed locally, original failure retained in `/tmp/T-004.1-correction-01-git.log`.
- Whole repository CLEAN architecture: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`, 4 tests pass; `/tmp/T-004.1-correction-01-architecture.log`.
- `python3 tools/check_contracts.py --root .`: 8 subsystems / 35 references valid; structural only. Designated updater still owns affected contract synchronization.
- `git diff --check`: pass. No index/staging/installation edits.

Measurement: original B retained at `.quality/reports/T-004.1-preflight-20261110-01.{json,txt}`; final current I at `.quality/reports/T-004.1-correction-20261111-02.{json,txt}`; intermediate correction `-01` retained. `python3 .agents/scripts/measure_maintainability.py compare` over the same seven Python paths against original B succeeds complete/compared, both checks completed. The broken `.quality/venv` was not used or repaired; launcher found available pinned tools. Reports share this workspace; transfer all exact JSON/text pairs if moved.

Rationale for materially edited retained hotspot `controller.inspect_candidate`: new against B, CC 26 (prior submission 24), 41 statements. Dirty identity validation and comparison stay with existing scope/owner admission under the same lock. A separate admission function would duplicate or scatter precedence; extracting file identity to Git removes hashing duplication without creating a second authority path. Other original-B rationale obligations remain in implementation-report.md's table for fresh independent disposition, especially G-01. `validate_accepted_workspace` retains its existing above-target structure: only the allowed frozen-baseline field inventory changes to accept enriched new baselines while preserving legacy reads; splitting the shape guard would add indirection to one schema check. New helper CC 5 and regression helper CC 6 / 41 statements stay below advisory targets.

Checked Python hashes for current I:
- `skills/task-orchestrator/scripts/controller.py`: `b5441597ce376035e735192fed2e052caa143258fb3ebcb4c6644fcf0732c021`
- `skills/task-orchestrator/scripts/controller_git.py`: `746ab7fa695b15ff2b9f68eb9198b4d9cb41a2802836c0e7a7736251d2bc553a`
- `skills/task-orchestrator/scripts/controller_state.py`: `a30ab322e417a62b936d5198e8297d41214a0c106a43c3dfdf262f5a6bac97a4`
- `skills/task-orchestrator/scripts/verification_runner.py`: `d7b7b19672fd4cfbca87e7400f7ee8fe51f66207f20c332dd5c6868f0c80fb2a`
- `skills/task-orchestrator/tests/test_actor_operations.py`: `2a38d65634701a51a8e9e198eb05b6b739bd5b927111ac8e87b5bc385e6a7d14`
- `skills/task-orchestrator/tests/test_controller_git.py`: `70db0929b22c6f821666ec090bed0b1736e355c496621a830c6004b718359cbd`
- `skills/task-orchestrator/tests/test_verification_runner.py`: `deb48747c12f518d7f0774b5c0c1cdc2d24d14aa3e6af5f7f93ff1f687ddbf44`

Final implementation addendum: the owning suite exposed a second strict baseline-shape consumer in `controller._load_inspection_authority`; both legacy consumers now accept original or enriched field sets. No migration or field rewriting. Its retained CC 87 hotspot changes only the schema guard, keeping all authority checks together rather than extracting a single inventory predicate. Final I supersedes -02 at `.quality/reports/T-004.1-correction-20261111-03.{json,txt}` (complete/compared, 7 files); original B and all prior comparisons retained. Final architecture4 passes in `/tmp/T-004.1-correction-01-architecture-02.log`. Earlier suite failures retained in `/tmp/T-004.1-correction-01-suite.log`; rerun `/tmp/T-004.1-correction-01-suite-02.log` owns final outcome. See I-03 for final exact file hashes, superseding controller hash printed above.

Final owning-suite result: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests` ran 251 tests, 6 failures, 7 errors, 20 skips; raw log `/tmp/T-004.1-correction-01-suite-02.log`. All failure/error traces reach `UnsupportedSandbox: sandbox-exec verification is supported only on macOS` (legacy inspection/fail-closed controls). These are not successful behavioral qualification; fresh discovery owns independent baseline attribution and supported-host gaps V-07d/e. No macOS/provider proof claimed.

## Correction submission

Implemented: READY_FOR_REVIEW

- Authority: `skills/task-orchestrator/docs/tasks/T-004.1/brief.md` r1.
- Preflight/context reference: sibling `preflight.md`, `verification.md` r1, `controller-contract.md`; parent `../T-004/brief.md` and `../../direction-single-task-sbx.md`.
- Preceding verdict: discovery-01 partial evidence, no acceptance verdict.
- Finding/scenario IDs: F-01, G-01; complete 48-row V/G inventory and prior statuses in the pre-edit ledger above.
- Complete findings and invariant: F-01 dirty-owner evaluated identity must remain unchanged regardless of scope; G-01 missing independent original-B comparison/limits/rationale. Correction and review evidence documented above and in maintainability-02.md.
- Influenced sibling surfaces: inside/outside scope executable regular files and symlink referents; 5 public regressions and unchanged-owner positive controls. Fresh discovery owns final row dispositions.
- Attempts and discarded hypotheses: exact fail-first/final regression logs and initial invalid fixture attempt preserved above; no discarded production workaround.
- Current scoped diff: controller.py, controller_git.py, test_actor_operations.py plus docs/contracts/task-orchestrator.json; details above. Pre-existing staged task implementation preserved.
- Measurement: original B preflight20261110-01 JSON/text, current I correction20261111-03 JSON/text, independent R maintainability20261111-03 JSON/text under `.quality/reports/`; complete/compared. All prior comparisons retained; affected-function rationale above and independent dispositions in maintainability-02.md.
- Native evidence: actor37/Git14/architecture4 pass; owning suite251 / 6 failures / 7 errors / 20 skips, host errors detailed above. Registry35 refs and profile112 match pass; these are structural evidence.
- Report transfer: shared workspace holds all exact `.quality/reports/` JSON/text pairs; ignored files require explicit transfer if moving to another checkout.
- Coverage ledger: complete pre-edit table above, prior row statuses unchanged; implementation outcomes separately documented, independent current evidence belongs in discovery-02.md.
- Reviewer reproducer: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k dirty_owner` — old5 fail, corrected5 pass; independent embedded exact P1 probe owned by fresh discovery.
- Owning suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests` — final result and exact log above, no all-green claim.
- Broad/aggregate gate: `python3 tools/verify.py` — final correction gate belongs to fresh discovery, not replaced by implementation checks.
- Remaining reviewer coverage at submission: G-01 original evidence supplied by maintainability-02; fresh discovery re-evaluates F-01/V-02b, unfinished V-09f/V-11e and supported-host V-07d/e; full current ledger remains its responsibility.
- Next: registry synchronization completed as contract-registry-02.md; fresh independent task-review-discovery, then separate task-acceptance-review decision. Do not advance T-004.2 without acceptance.

Review continuation: maintainability-02 ACCEPT (independent original-B R complete, all11 rationale dispositions); registry-02 UPDATED; independent discovery reports no new defect and current F-01/G-01 correction evidence, with portable V-09f/V-11e exercised. Discovery-owned aggregate `python3 tools/verify.py`: 7 checks,1failed. Orchestrator251 /6fail /7error /20skip; original pre-correction legacy subset independently reproduces the same host failures. Root311 /32skip; other suites, registry and profile pass. Full raw aggregate `/tmp/t0041-correction-discovery-aggregate.log`. Supported-host V-07d/e remain blocked; no live qualification. Optional run-evidence `run-20261111T063232Z-22ff86e37162` closed completed for this correction invocation. Separate acceptance disposition remains owned by its fresh reviewer after discovery publication.

Final review disposition: discovery-02.md independently corroborates F-01 corrected, G-01 supplied and V-09f/V-11e completed;46 of48 rows pass, V-07d/e remain host-blocked. Separate acceptance-01.md is INCONCLUSIVE solely for those required supported-host evidence gaps; F-01/G-01 resolved, no new correction-eligible defect. This completes the requested finding correction; it does not advance T-004.2. Next remaining route: supported-capability verifier supplies real launch-failure and restrictive containment evidence → fresh discovery admits it → new separate acceptance decision. No source/code correction requested by acceptance. All report pairs and original staged work retained.
