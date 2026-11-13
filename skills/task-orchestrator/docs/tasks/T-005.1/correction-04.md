# T-005.1 correction 04 — native/schema evidence recovery

Pre-edit coverage map. Preceding verdict: INCONCLUSIVE, acceptance-01.md.
Authority: brief.md rev1; verification.md rev1; ready preflight.md and Decision
context; controller-contract.md. No requirement or scenario revision.

No unresolved production finding: F-01 and MNT-01 retain resolved disposition.
Broken test invariant: portable controller behavior and sandbox argv/validation
must be observable without requiring the real macOS executable; real containment
must remain separately qualified, with unsupported hosts explicitly skipped.

Planned narrow changes: isolate the existing controller inspection fixture's
sandbox invocation at its existing test seam while retaining real command/file/
Git/log/replay effects; exercise deterministic sandbox construction/refusals with
explicit platform and executable-availability setup. Preserve actual unsupported
host rejection and dedicated real containment tests. No production changes.
Schema dependency provisioning awaits the explicit user exception to brief scope.

Broad-gate owner: implementer, as preflight native table assigns cross-cutting
`python3 tools/verify.py`; fresh discovery separately owns admission of evidence.
Prior reviewer statuses below remain historical, not passes for changed tests.

| Row | Prior reviewer status | Planned evidence/navigation | Next owner |
|---|---|---|---|
| V-01 | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02c | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02d | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02e | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02f | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02g | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02h | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02i | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02j | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02k | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02l | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02m | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02n | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02o | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02p | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02q | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02r | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02s | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-02t | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03c | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03d | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03e | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03f | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03g | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03h | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03i | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03j | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03k | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03l | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03m | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-03n | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04c | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04d | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04e | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04f | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04g | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04h | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04i | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-04j | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05c | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05d | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05e | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05f | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05g | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05h | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05i | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-05j | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-06a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-06b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-06c | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-06d | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-06e | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-06f | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07c | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07d | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07e | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07f | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07g | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07h | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-07i | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-08 | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-09a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-09b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-10a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-10b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-10c | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-10d | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-11a | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-11b | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-11c | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-11d | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-11e | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-11f | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-11g | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-11h | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-12 | blocked (G-SCHEMA) | Available Draft 2020-12 validator on retained valid/invalid actor and manifest inputs; provisioning exception pending | fresh discovery then separate acceptance |
| V-12-CLI | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-12-DOC | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| V-12-SCHEMA/G-SCHEMA | blocked missing validator | Available Draft 2020-12 validator on retained valid/invalid actor and manifest inputs; provisioning exception pending | fresh discovery then separate acceptance |
| MNT-01 | pass | Prior proof is navigation; rerun owning actor suite without changing scenario authority | fresh discovery then separate acceptance |
| G-REG | blocked missing producer result | Installed updater execution recorded separately in reviews/registry-01.md; unchanged registry identities | fresh discovery then separate acceptance |
| G-NATIVE | fail current gate | Reproduce inherited 13 failures; targeted controller/runner regressions, owning suites, aggregate with explicit skips | fresh discovery then separate acceptance |

## Implementation evidence

Implemented test correction: controller inspection's existing fixture now supplies
an explicit test-only invocation seam; commands, Git identities, execution/log
publication, drift detection and crash/replay still run. Deterministic sandbox
construction and validation explicitly model macOS plus executable availability.
The argv success case now asserts a literal expected Seatbelt command rather
than comparing the builder with itself. Real unsupported-Linux rejection is
unchanged; dedicated real sandbox tests and their host gates are unchanged.
No production or executable schema bytes changed. No tests were removed or
added; existing distinct scenarios retain their behavioral assertions.

Reviewer regression before edit:
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skills/task-orchestrator/tests python3 -m unittest test_verification_runner.VerificationSandboxFailClosedTests test_controller.ControllerInspectionIntegrationTest.test_inspect_keeps_pending_semantic_review_non_accepting -v`:
8 tests, 5 failures + 2 errors. Raw: /tmp/T-005.1-blockers-before.log.

After edit:
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skills/task-orchestrator/tests python3 -m unittest test_verification_runner.VerificationSandboxFailClosedTests test_controller.ControllerInspectionIntegrationTest -v`:
30 tests passed, no skips. Raw: /tmp/T-005.1-blockers-targeted.log.

Owning module checks:
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_verification_runner.py`: 40 tests, 20 skipped; all executed tests passed. Raw /tmp/T-005.1-blockers-runner.log.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py`: 95 passed, no skips. Raw /tmp/T-005.1-blockers-controller.log.

Measurement: original B `.quality/reports/T-005.1-before-01.{json,txt}`
preserved; all 12 original snapshots checked against original commit
`6a13008d239d22ad48909258e00edd809953973d`. Runner test pre-edit bytes match B;
controller's supplied task changes remain prior-producer work. Entry comparison
`.quality/reports/T-005.1-correction-04-entry.{json,txt}` and final comparison
`.quality/reports/T-005.1-correction-04-final.{json,txt}` compare both current
changed test files to original B (not to entry). Both complete; full profile;
no errors. Source/setting/tool identities remain those of the existing analyzer.
Reports and raw `/tmp/T-005.1-blockers-measure-{entry,final}.log` share this workspace;
transfer those exact files and B to an isolated reviewer.

The new sandbox helper is CC1, 2 statements and 2 counted arguments; the existing
inspection fixture grows from 21 to 24 statements, below advisory targets.
Its pre-existing signature and untouched hotspots are not newly introduced metric
breaches. Prior controller test increases belong to the supplied implementation
and retain maintainability-04's dispositions. No metric-driven refactoring.

Optional run-evidence sidecar was not used: an initial `status` CLI probe was
invalid; a later `active` query reported no open run. No evidence run was opened;
raw native logs and measurement reports are retained.

Checked correction-byte SHA-256:
- `skills/task-orchestrator/tests/test_controller.py`: `771351e510fde33051a61096b84ba77225563be2b43291f02e7e072aa899b5c3`
- `skills/task-orchestrator/tests/test_verification_runner.py`: `81b21977935ce6ee8a65aecbbe995ad8208a92fa0c5f7a9769e6b7f463c3bfe7`

Owning actor suite:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py`:
69 passed, no skips; raw /tmp/T-005.1-blockers-actors.log. This exercises all
existing acceptance/lifecycle cases under unchanged authority, as implementation
evidence. Fresh discovery must independently decide current row admission.

Full submitted identity manifest: /tmp/T-005.1-blockers-byte-identities.json,
28 staged/unstaged submitted paths. Existing staged binary diff SHA-256 remains
`5f66197788fa97cc7ccc56e9964735a9b3710391de8e9676ba4590f372d7c4f4`;
no index changes were made. This correction adds only the two unstaged test
changes and the new correction/registry reports. Pre-existing untracked files
are preserved. `git diff --check` passes.

Schema proof prepared but not executed: /tmp/T-005.1-blockers-schema.py reads
unchanged retained actor/manifest valid and invalid controls from
/tmp/T-005.1-discovery-02/, checks both declared Draft 2020-12 schemas and asserts
valid acceptance and deliberate-invalid rejection with jsonschema's
Draft202012Validator. Retain/transfer this script and all four exact inputs;
JSON parsing and the script's existence supply no successful schema evidence.
No dependency install, network, live provider or active-installation refresh has
occurred. Explicit provisioning exception requested from user and still pending.

## Correction handoff

Native implementation evidence is now green; schema proof and independent
review are still owed. Historical reviewer row statuses in the pre-edit map are
unchanged. This session has authored test assets and supplies no independent
verdict for them.

Implemented: READY_FOR_REVIEW

- Authority: `skills/task-orchestrator/docs/tasks/T-005.1/brief.md`, revision 1, and current user's request to close acceptance-01 blockers.
- Preflight/context reference: `skills/task-orchestrator/docs/tasks/T-005.1/preflight.md` (Decision context), `verification.md` revision 1, `controller-contract.md`; unchanged requirements/scenarios and production dependencies.
- Preceding verdict: INCONCLUSIVE, `reviews/acceptance-01.md`.
- Finding/scenario IDs: all 92 exact ledger identities in the pre-edit table; F-01 and MNT-01 remain resolved. No new product finding or approved deferral.
- Complete findings and invariant: G-REG lacked its separately attributed stage, now supplied by `reviews/registry-01.md`; G-NATIVE's 13 inherited failures prevented portable verification, corrected in existing test setup; G-SCHEMA still lacks an installed Draft 2020-12 validator. Tests must provide the setup needed to reach their intended boundary; local component proof does not prove host containment.
- Influenced sibling surfaces: unsupported-host denial, deterministic sandbox construction and permission refusals, real host-dependent containment, controller command execution/record publication/drift/replay. Focused and owning evidence above; actual containment and live provider behavior remain unqualified.
- Attempts and discarded hypotheses: 8-test pre-edit reproduction rejected accidental production acceptance defects as the cause of the native failures: traces hit UnsupportedSandbox before the intended oracle. Explicit setup correction passed the 30-test focused regression on its first implementation attempt. No production repair or skips added.
- Current scoped diff: two test files (30 insertions, 10 deletions), plus this report and `reviews/registry-01.md`. Existing staged implementation, schemas, plans, registry and source references preserved.
- Measurement: original B, entry/final comparisons and exact shared transfer paths above; final complete comparison covers both changed Python test files; no unknown value treated as zero.
- Native evidence: `python3 tools/verify.py`, repository-wide scope assigned to implementer by preflight, **7 checks, 0 failed**, exit 0. Raw `/tmp/T-005.1-blockers-aggregate.log`; current identities `/tmp/T-005.1-blockers-byte-identities.json`. Root suite and orchestrator skips remain explicitly unqualified, not passed. All executed suites passed; registry and development-profile drift passed.
- Native architecture command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`, **4 passed**, no skips; current correction bytes, implementer stage, raw `/tmp/T-005.1-blockers-architecture-final.log`.
- Native registry command: `python3 tools/check_contracts.py --root .`, **8 subsystems / 37 references**, passed; structural only, raw `/tmp/T-005.1-blockers-contracts-final.log`.
- Report transfer: shared paths listed above; copy original B JSON/text, entry/final JSON/text, byte manifest, raw logs, schema probe and four retained schema inputs to an isolated reviewer. Ignored /tmp and .quality evidence does not travel with Git commits.
- Coverage ledger: the complete pre-edit table is authoritative for historical reviewer status. Actor suite supplies current implementation evidence for its V-01–V-12 scenarios; no reviewer status is rewritten. G-NATIVE now has passing implementation aggregate evidence; G-REG has updater-owned closure; G-SCHEMA/V-12-SCHEMA has no successful executable proof. Every row's next functional owner remains fresh discovery, then separate acceptance.
- Reviewer reproducer: exact before/after commands and outcomes above.
- Owning suite: actor 69 passed, controller 95 passed, runner 40 tests with 20 skips; exact commands above. No cases removed or added.
- Broad/aggregate gate: `python3 tools/verify.py` run after focused/owning success, required for cross-cutting correction by preflight; implementation evidence only, no acceptance verdict inferred.
- Remaining reviewer coverage: affected test-harness maintainability; independent admission of all current material rows, especially G-NATIVE and V-12/G-SCHEMA; registry closure applicability; separate final acceptance. Provisioning exception remains pending user answer. No task advancement or T-005.2 execution.
- Next: fresh `task-maintainability-review` for the two changed test assets → consume/reconfirm `reviews/registry-01.md` against unchanged contract/reference bytes (repeat updater if that scope changes) → fresh independent `task-review-discovery` for current native and executable schema evidence once capability is available → separate fresh `task-acceptance-review`. Current implementer invocation stops here; no reviewer is launched or managed in this session.

## Authorized durable schema verification follow-up (pre-edit)

User authorized project installation provided it supports recurring verification.
This replaces the pending temporary-only provisioning request: add a pinned
repository development dependency in requirements-dev.txt, use project .venv,
and extend existing V-12 test to execute Draft 2020-12 valid/invalid controls for
both schemas on every owning-suite/aggregate run. No optional skip on a missing
validator. Installed skill/runtime dependencies stay unchanged.

Coverage-map delta before edits: all 92 row identities and historical statuses
above remain intact. V-12 and V-12-SCHEMA/G-SCHEMA now map to the existing CLI
fixture's actual actor result plus a valid manifest with both supported required
review stages; invalid controls omit acceptance decision or request an unsupported
review stage. Oracle: accept valid instances and reject the deliberate violations
using Draft202012Validator. G-NATIVE maps to a new gate run with the project
interpreter; G-REG's existing runtime/reference closure stays unchanged. Remaining
rows reuse current evidence only as navigation for fresh discovery.

Verification: focused V-12 first, owning actor suite, full repository gate,
architecture and registry checks. No live model or containment qualification.

## Durable schema verification implementation

The project environment now contains jsonschema 4.25.1 installed from new
`requirements-dev.txt`. `.venv/` is ignored. README.md, docs/development.md and
docs/project-map.md document recurring setup and the owning test dependency.
No optional skip is used: missing jsonschema fails actor-suite import, so the
canonical aggregate cannot silently omit schema proof. The standard gate still
never installs packages. Installer selection and shared runtime file lists were
inspected again: this is a repository-only verification dependency, not a skill
runtime dependency; no installation profile change is needed.

Updated the existing V-12 CLI/schema test instead of adding a parallel test or
fixture family. It uses its actual observed actor result, removes decision for
the invalid actor control, and uses the prepared task manifest with supported
maintainability/registry review stages plus an unsupported-stage negative.
Both declared Draft 2020-12 schemas receive check_schema plus actual instance
acceptance/rejection; required/enum errors are asserted. The existing runtime
invalid-action and non-completion assertions remain. Removed only redundant
schema-text shape checks now covered by executable validation.

Current implementation evidence:
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skills/task-orchestrator/tests .venv/bin/python -m unittest test_actor_operations.ActorOperationsTest.test_acceptance_v12_documented_cli_and_changed_schema_boundary -v`: 1 passed, no skips; `/tmp/T-005.1-schema-focused.log`.
- `.venv/bin/python /tmp/T-005.1-blockers-schema.py`: passed all four retained reviewer controls: valid actor accepted; missing decision rejected (required); valid manifest accepted; unsupported discovery stage rejected (enum). `/tmp/T-005.1-schema-retained-controls.log` retains exact schema/instance SHA-256 identities and error paths.
- `.venv/bin/python -m pip check`: no broken requirements. Install log `/tmp/T-005.1-jsonschema-install.log`; exact resolved versions `/tmp/T-005.1-schema-installed-packages.txt`.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_architecture.py`: 4 passed; `/tmp/T-005.1-schema-architecture.log`.
- `.venv/bin/python tools/check_contracts.py --root .`: passed, 8 subsystems / 37 references; `/tmp/T-005.1-schema-contracts.log`; structural only.

Measurement preserves original B and every preceding comparison. New entry
`.quality/reports/T-005.1-schema-entry-01.{json,txt}` records supplied actor-test
bytes before edits; final `.quality/reports/T-005.1-schema-final-01.{json,txt}`
compares all three corrected test files to original B. Both complete with empty
errors. V-12 is CC2 and 42 statements, below targets; prior unmatched before
symbol remains unknown. No new threshold rationale or unrelated cleanup needed.
Raw `/tmp/T-005.1-schema-entry-01.log` and
`/tmp/T-005.1-schema-measure-final.log`; current submitted identities are in
`/tmp/T-005.1-schema-byte-identities.json`. Transfer these files and original B
JSON/text explicitly to isolated reviewers.

This supersedes the earlier pending-provisioning limitation for implementation
evidence only. G-SCHEMA and V-12 now have executable implementation proof;
reviewer statuses await fresh independent discovery. The root README setup edit
changes a reference covered by registry-01, so its exact reference-byte closure
must be reconfirmed by the updater after maintainability. Runtime/schema bytes
remain unchanged; no acceptance or successor advancement is claimed.

## Final project-environment verification and next owner

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py`: **69 passed**, no skips; `/tmp/T-005.1-schema-actors.log`.
- `.venv/bin/python tools/verify.py`: **7 checks, 0 failed**, exit 0; `/tmp/T-005.1-schema-aggregate.log`. Orchestrator: 283 tests, 20 skips; root: 311 tests, 32 skips. All executed tests passed. The remaining 3/13/4-test suites passed; registry and development-profile drift passed. Skipped containment/analyzer capabilities remain unqualified.
- `git diff --check`: passed. No production, schema, task-plan, staged-index or active installation edits.

The two requirements files have distinct scope: `.quality/requirements.txt`
pins optional Radon/Ruff measurement tooling and its dependencies;
`requirements-dev.txt` pins required repository test dependencies (jsonschema).
No analyzer requirements or environments were modified.

Implemented: READY_FOR_REVIEW. The schema capability gap has current executable
implementation evidence and durable regression coverage. The earlier native gap
has passing current aggregate evidence. These are not independent verdicts.

Next ordered route: fresh maintainability review of all three corrected test
assets and dependency/setup changes → registry updater reconfirms existing runtime
record and updated root README/setup references → fresh independent discovery
admits current schema/native evidence and reconciles every ledger row → separate
acceptance decision. The installed implementer requires stopping before invoking
or managing those fresh reviewer calls. T-005.2 remains unexecuted.
