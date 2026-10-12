# Task Review Discovery Report: `INT-FLOW-001` — Close preparation and review integration gaps

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery` |
| Coverage completeness | `complete — all material rows have current targeted evidence; role-call boundaries are authority-excluded (T-005), not blocked` |
| Discovery iteration | `first discovery pass` |
| Created at | `2026-10-12T12:55:00+01:00` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report path | `docs/tasks/INT-FLOW-001/reviews/discovery-01.md` |
| Task brief | `docs/tasks/INT-FLOW-001/brief.md` (revision 1) |
| Verification design / task context | `docs/tasks/INT-FLOW-001/verification.md` (revision 1), `docs/tasks/INT-FLOW-001/preflight.md` (ready), recorded ART-003-style decision context lives in the brief's audit table (I-01..I-05) and finite-risk contract |
| Current submission | `docs/tasks/INT-FLOW-001/results.md`, state `READY_FOR_REVIEW`, evidence run `run-20261012T112053Z-f6a83b5a1b72`, commit `199d14d` (`INT-FLOW-001 initial version`) |

This report publishes evidence only. It contains no acceptance verdict, no
approved deferral, and no advancement. The separate acceptance decision call
consumes it. It applies only to the reviewed bytes and artifacts identified
below; any correction requires a new discovery report. This report does not
review or authenticate itself.

## 1. Discovery provenance

| Question | Evidence |
|---|---|
| Did this session author any reviewed production bytes? | `no — independent`. This session wrote none of the 15 files in commit `199d14d`; all reviewed bytes predate this session's first write. |
| Independent evidence authority | `yes` |
| Current byte identity | `HEAD 199d14d11cadcafa6dd6c44aed587f8547d01c16`; scoped diff = `git diff HEAD~1 HEAD` (827 insertions, 29 deletions across 15 files) |

Route-order context: `results.md` names a fresh `task-maintainability-review`
as the first outstanding owner, with discovery after it. This discovery pass
ran on explicit user request ahead of that stage. Discovery records evidence
only; the owed maintainability evidence remains outstanding for the separate
acceptance decision call (recorded in section 8/9, not as a finding).

## 2. Findings, ordered by suggested severity P0 through P3

No findings.

## 3. Completeness ledger

Stable row IDs are derived from the brief's authority rows. Submitted evidence
is implementer-attributed; the independent probe column is this session's
current-bytes evidence.

| Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| L-01 | AC-01 / R-01: registry stage applicable versus absent; first outstanding stage + full ordered remainder | architecture gate; registry applicable; registry absent; maintainability owed versus completed; clean post-review handoff | Read `task-maintainability-review/SKILL.md` correction loop + appended contract-registry boundary; compare with brief order `architecture gate → maintainability → registry → discovery → acceptance` | Results.md correction map I-01; focused tests; 118-test run | Current bytes: correction loop step 5 names conditional registry stage, ordered before discovery and acceptance; "Naming the route … without executing any named stage"; "applicable registry work cannot be dropped, and an absent registry stage cannot be invented"; appended registry boundary says review runs before registry sync and does not fail merely for pending sync. Old shortcut text absent from every live source (grep sweep DISC-05); `docs/contracts/` correctly absent; focused test `test_clean_review_hands_off_the_complete_conditional_route` passes | `pass` |
| L-02 | AC-02 / R-02: affected scope owes fresh review; unaffected scope with applicable current proof retains evidence; stale/missing/inapplicable proof never completes | affected scope; unaffected/current scope; unaffected with stale, missing, inapplicable proof | Read `Independence` section of maintainability SKILL and flow guide; contrast against implementer route wording in `bounded-task-implementer/SKILL.md` "Name the complete ordered submission route" | Results.md correction map I-02; focused tests | Current bytes: blanket sentence "Every production correction invalidates the previous maintainability verdict" removed everywhere except spike-history archive and test `assertNotIn` strings; replacement states invalidation applies "for the corrected bytes", unaffected scope retains "while that evidence stays applicable to the submitted bytes", and "a prior verdict's label alone is not current evidence"; focused tests `test_correction_reentry_follows_affected_scope_and_current_evidence` and flow-guide re-entry assertion pass | `pass` |
| L-03 | AC-02 / R-02 / V-03: tests-only and reference-only route conditions preserved by authority, not label | tests-only with/without authorized exception; reference-only with current proof, missing proof, changed executable effects | Read acceptance SKILL tests-only/reference-only conditions and flow guide; existing executable-reference probes | Results.md claims preserved-and-asserted | Current bytes: flow-guide README contains "Route by actual effects and current proof" and trivial-correction condition (file last touched in commit `3f3d7ab`, unchanged by this diff); acceptance tests-only/reference-only tests and `test_task_flow_guides` pass unchanged | `pass` |
| L-04 | AC-03 / R-03: stable finding ID independent of display order; four findings → one corrected → three survive; new finding gets unused ID; genuine stop keeps IDs | reorder of three survivors; one corrected with current disposition; one new finding; genuine stop before completion | Read producer contract (`Report every confirmed blocker`, Output, `SELF_CHECK_ONLY`, Genuine stops) and eval case 4; run `correction-round` fixture in disposable Git target | Results.md correction map I-03; fixture test | Current bytes: producer requires "a **stable finding ID** such as `MNT-01`, independent of display order", "Identity is a producer obligation, not a fixture convention", "a resolved ID is never recycled", Output form carries `1. MNT-01 — <file/location>` and "Current disposition"; genuine stop retains IDs/dispositions; no finding cap. Real boundary: `correction-round` repo observed — `fee(100)=2.0`, `surcharge(100,10)=1.5`, no `billing.db` created, seeded sqlite rates ignored, divergence still reproduces; prior report contains `MNT-B1..MNT-B4` with dispositions; facts file carries MNT-B5/unrecycled/`maintainability-02.md` inputs. Eval case 4 expectations match | `pass` |
| L-05 | AC-04 / R-04 / V-05: packaged handoffs carry verification revision, readiness, decision context for complete AND partial evidence | complete clean guided report; explicitly partial report | Read discovery SKILL final handoff + durable template section 9 + acceptance guided inputs and workflow step 1 | Results.md correction map I-04; focused tests | Current bytes: discovery handoff lists "the applicable packaged preparation references — the verification design with its revision, the readiness/preflight reference, and the recorded decision context — for complete, clean guided reports as well as explicitly partial ones"; unpackaged direct edit hands off conversational context; acceptance inputs require identifying and reading the applicable references and routing a missing one to its owner with a focused request; focused tests `test_final_handoff_carries_packaged_preparation_references` and `test_guided_inputs_identify_and_read_packaged_preparation_references` pass | `pass` |
| L-06 | AC-04 / R-04 / V-06: current scenario proof cannot rescue obsolete readiness; recovery goes to owning stage | old readiness with new proof; current readiness after recovery; old readiness substituted again; missing decision-relevant proof | Read existing revision-recovery/old-readiness rules in verification-designer and acceptance skills | Results.md claims "already present and asserted unchanged" | Current bytes: verification-designer retains "Authority, coverage, and revision" section (present at both HEAD~1 and HEAD); acceptance readiness rules unchanged; unchanged tests pass within owning module | `pass` |
| L-07 | AC-04 / R-04 / V-07: preflight-only material exposure reaches contextual disposition; bounded compatible contrast not auto-blocked | confirmed material risk with preflight-only exposure; bounded compatible risk | Existing contextual/disposition fixtures and tests | Results.md claims asserted-unchanged | Current bytes: unchanged contextual-disposition rules; owning-module tests pass; no new text contradicts them | `pass` |
| L-08 | AC-04 / R-04 / V-08: unpackaged direct requests stay compact, no mandatory packet or routine prompt | direct edit with sufficient supplied context | Read acceptance "Do not return `INCONCLUSIVE` merely because no preflight packet…" paragraph | Results.md claims compactness preserved | Current bytes: the no-packet paragraph is preserved; guided inputs add the packaged-references clause with explicit direct-edit exception; focused acceptance test asserts the direct-edit and missing-reference routing strings | `pass` |
| L-09 | AC-05 / R-05 / V-09: executable integration leaf may derive own composition AC scenarios; composite parent, sibling/system scope, unavailable oracle stay refused | leaf with supplied producer outputs; composite parent; sibling requirement; system-wide strategy; unavailable input/capability; authority cannot settle oracle | Read verification-designer "Cross-task integration boundary"; run `integration-leaf` fixture | Results.md correction map I-05; fixture test | Current bytes: boundary section derives task-local scenarios "for exactly those composition ACs" while refusing composite parents (route to dependency-ready leaf), invented sibling/system scope, and unavailable oracles (report to owner; never fabricate; no fabricated readiness); "Packaged preparation remains mandatory for that leaf". Old blanket refusal sentence absent from live bytes. Real boundary: `integration-leaf` fixture stages INT-9 brief (`Task kind: executable`, AC-01/AC-02, producer outputs + consumer boundary), INT-PARENT (`Task kind: composite`, `Status: decomposed`), and contrast request (sibling/system-wide/unavailable). Eval case 9 setup/expectations match | `pass` |
| L-10 | AC-06 / V-10: canonical installer projects corrected bytes; ownership boundaries preserved; protected history/active installation intact | initial committed-target install; managed replacement with unmanaged state; no active refresh | Run `test_install_development_skills.py` (disposable committed targets); compare diff paths with brief scope; check `docs/tasks/index.json` and prior history untouched | Results.md unchanged-declarations claim; aggregate run | Changed paths (14 + results.md) are exactly the brief's allowed areas; installer script not in diff (declarations unchanged); `docs/contracts/` absent; `git diff --check` clean; no leftover fixture processes; installer module passes in aggregate run | `pass` |
| L-11 | AC-06 / V-11: evidence limits separated; T-005 inputs usable; fail-first rejection feasible; whitespace/protected-file preservation | structural check; real filesystem/Git observation; unrun role call; feasible rejection demonstration | Focused tests first, then owning modules; worktree-based old-bytes rejection; `git diff --check` | Results.md evidence sections 1–4 and T-005 inputs | Independent fail-first reproduction: new checks against `HEAD~1` bytes in a disposable detached worktree → 7 failures + 1 error (8 rejection signals; fixture staging excluded), worktree removed, user state untouched. T-005 setup commands run standalone and produce the claimed inputs; referenced eval ids exist (maintainability case 4, verification-designer case 9, discovery case 11). Focused tests (12) and aggregate (118) pass; `git diff --check` clean | `pass` |

## 4. Adversarial state and evidence checks

The reviewed bytes are policy/skill text, templates, eval expectations, and
fixture inputs — no persisted state machine, so the stateful adversarial
matrix (selected/non-selected, cardinality, ordering, parent/child, type
strictness, coherent tampering) does not apply. Applied instead:

| Ledger row / invariant | Cases exercised | Result and evidence |
|---|---|---|
| Cross-source contradiction sweep (L-01, L-02, L-05, L-09) | Searched every live source under `skills/`, `tests/`, `docs/tasks/INT-FLOW-001/` for the four removed instruction fragments | Only matches: test `assertNotIn` strings, the pre-existing spike evidence archive `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/`, and results.md's description of the removed sentence. No live instruction retains the old text |
| Coherent multi-file continuity (L-01) | Maintainability correction loop ↔ appended registry boundary ↔ discovery/acceptance handoffs | Agree: registry stage conditional and ordered after review, before discovery/acceptance; naming never executes |
| Fixture/report identity round-trip (L-04) | `correction-round` prior report vs facts file vs eval case 4 expectations | Prior report bytes preserved; MNT-B1..B4 identities, corrected disposition, MNT-B5 next identity, `maintainability-02.md` next path all consistent |

## 5. Independent probes and command results

| ID | Exact command / probe | Working directory / environment | Purpose / ACs | Result and observed signal | Side effects / cleanup | Independence / gap |
|---|---|---|---|---|---|---|
| DISC-01 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_task_maintainability_review.MaintainabilityIntegrationGapContractTest test_task_maintainability_review.MaintainabilityReportingContractTest test_task_maintainability_review.MaintainabilityFixtureTest.test_correction_round_fixes_one_finding_and_supplies_identity_inputs test_task_acceptance_review.ReviewerDisciplineTests.test_guided_inputs_identify_and_read_packaged_preparation_references test_task_review_discovery.ReviewDiscoveryDisciplineTests.test_final_handoff_carries_packaged_preparation_references test_task_preparation_contracts.TaskBriefDesignerPackageTest.test_integration_leaf_composition_permission_keeps_refusal_boundaries test_task_preparation_contracts.TaskBriefDesignerPackageTest.test_integration_leaf_fixture_supplies_qualification_inputs -v` | repo root | Changed/new focused checks; AC-01..AC-05 | `Ran 12 tests … OK` (0.129s) | none | Independent run on current bytes |
| DISC-02 | `python3 -c` JSON load + duplicate-id assertion over all four changed/related evals files | repo root | Eval JSON validity, stable ids | All valid; maintainability ids [1,2,3,4], verification-designer [1..9], discovery [1..9,11..15], acceptance [1..28]; no duplicate ids | none | Independent |
| DISC-03 | `EVAL_WORK_ROOT=/tmp/opencode/disc-fixtures python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py correction-round` + import-boundary probe (`fee(100)`, `surcharge(100,10)`, `billing.db` existence) | disposable temp root | AC-03 / R-03 real fixture boundary | Real Git repo: `pricing.py`, `receipts.py`, `service.py`, `tests/test_billing.py` modified; `fee(100)=2.0`, `surcharge(100,10)=1.5`, `billing.db` absent; prior review dir staged | temp dir under `/tmp/opencode`; no surviving processes | Independent real-boundary observation |
| DISC-04 | `EVAL_WORK_ROOT=/tmp/opencode/disc-fixtures2 python3 skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py integration-leaf` + read of INT-9/INT-PARENT/contrasts | disposable temp root | AC-05 / R-05 real fixture boundary | INT-9 brief: `Task kind: executable`, AC-01/AC-02 with producer outputs and consumer boundary; INT-PARENT: `Task kind: composite`, `Status: decomposed`; contrasts cover sibling/system-wide/unavailable | temp dir; no surviving processes | Independent real-boundary observation |
| DISC-05 | Grep sweep for removed fragments (`Every production correction invalidates`, `proceed to fresh independent`, `repeat architecture gate + fresh maintainability review`, `report that limitation to the caller`) across `skills/`, `tests/`, `docs/tasks/INT-FLOW-001/` | repo root | No live instruction retains old policy | Matches only in tests (assertions), pre-existing spike archive, and results.md prose | none | Independent contradiction sweep |
| DISC-06 | `git worktree add --detach /tmp/opencode/old-bytes HEAD~1` + copy new test files + run focused contract tests, then `git worktree remove --force` | disposable detached worktree | V-11 fail-first rejection feasibility | `Ran 11 tests … FAILED (failures=7, errors=1)` — 8 rejection signals against old bytes; worktree removed | worktree removed; working tree untouched | Independent old-bytes reproduction |
| DISC-07 | `git diff --check`; `ls docs/contracts`; process scan for fixture leftovers | repo root | AC-06 whitespace/protection; no registry creation; no leaked processes | diff-check exit 0; `docs/contracts` absent; no fixture processes | none | Independent |
| DISC-08 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_task_maintainability_review test_task_review_discovery test_task_acceptance_review test_task_preparation_contracts test_task_flow_guides test_review_composition test_install_development_skills` | repo root | Owning-module aggregate gate | `Ran 118 tests in 3.054s — OK` | none | Independent aggregate run |

No required check was left unrun for the reviewed local evidence boundary.

## 6. Aggregate-gate decision

| Field | Value |
|---|---|
| Gate / exact command | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_task_maintainability_review test_task_review_discovery test_task_acceptance_review test_task_preparation_contracts test_task_flow_guides test_review_composition test_install_development_skills` |
| Status | `passed` |
| Owner and stage | `initial discovery` (targeted reconciliation completed before launch; no decisive targeted failure) |
| Reason | Targeted adversarial evidence (DISC-01..DISC-07) was clean and every required/material ledger row had current evidence with no unselected probe remaining, so the justified affected-module aggregate ran |
| Current evidence | `Ran 118 tests in 3.054s — OK`; post-run `git status --short` identical to the reviewed state (three pre-existing untracked `.DS_Store` entries only) |

## 7. Scope and baseline comparison

| Item | Recorded baseline | Current reviewed state | Classification / evidence |
|---|---|---|---|
| `HEAD` | `199d14d11cadcafa6dd6c44aed587f8547d01c16` | same | expected |
| Exact `git status --short` | `?? .DS_Store`, `?? docs/.DS_Store`, `?? skills/.DS_Store` (pre-existing junk, preflight-noted) | identical before this report write | pre-existing user-side untracked junk, outside task scope; untouched |
| Dirty path index/worktree identities | none tracked-and-dirty; worktree matches HEAD | same | expected; no index/worktree divergence |
| Task-owned paths | brief: the four flow skills, affected READMEs, seven focus test files, installer inspection | diff = 14 files (four skills' SKILL.md/evals/fixtures + discovery template + five test files) + `docs/tasks/INT-FLOW-001/results.md` | in scope; READMEs and installer unchanged because already consistent (READMEs last touched in older commits; flow-guide tests assert current semantics) |
| Durable package artifacts | `brief.md`, `verification.md`, `preflight.md`, `results.md` | all present in `docs/tasks/INT-FLOW-001/`; no `reviews/` dir before this report | canonical/current |
| Authority / policy / dependencies | brief revision 1, verification revision 1, preflight ready | unchanged | no invalidation |

After completing the report: recorded post-report `git status --short` — the
only difference from the reviewed state is the new untracked
`docs/tasks/INT-FLOW-001/reviews/discovery-01.md`.

## 8. Questions, unchecked work, and residual risks

| Type / row ID | Evidence or reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| question | Actual role compliance — producer finding-ID generation, reference reading, routing behavior — is unrun by design; staged reports are supplied fixture inputs, not real producer outputs | no (authority-excluded) | T-005 role calls; results.md qualification inputs supply setup/contrasts |
| question | Route order: `results.md` names a fresh `task-maintainability-review` as first outstanding owner; this discovery pass ran first on explicit user request | no (evidence-only) | separate `task-acceptance-review` decision call must consume the owed fresh maintainability evidence |
| question | Implementer's split of the fail-first rejection (8 assertion failures + 2 staging errors) | no | Independently reproduced 8 rejection signals (7 failures + 1 error) on contract classes; fixture staging not re-run against old bytes |
| question | Discovery evals ids skip 10 (`1..9, 11..15`) | no | pre-existing, outside the reviewed diff; eval case 11 referenced by results.md exists and matches |
| residual risk | Structural text checks prove contract bytes, not that a role follows them | no | accepted by brief/verification design as the local evidence boundary |

## 9. Coverage completeness and next route

| Field | Value |
|---|---|
| Coverage completeness | `complete — every material ledger row (L-01..L-11) has current targeted evidence; role-call boundaries are authority-excluded (T-005), not blocked` |
| Basis | 11 ledger rows, 8 independent probes, 1 passed aggregate gate, 0 findings |
| Next owner | `separate acceptance decision call` (fresh `task-acceptance-review`) |
| Exact next action | Route these bytes, this report, the owed fresh `task-maintainability-review` evidence (first outstanding owner per `results.md`), the task brief, verification design revision 1, ready preflight, and results.md to the separate acceptance decision call |

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: first discovery pass; HEAD 199d14d11cadcafa6dd6c44aed587f8547d01c16
- Coverage rows: L-01 pass, L-02 pass, L-03 pass, L-04 pass, L-05 pass, L-06 pass, L-07 pass, L-08 pass, L-09 pass, L-10 pass, L-11 pass
- Finding IDs: none
- Finding/scenario continuity: no prior findings; scenarios V-01..V-11 map to ledger rows L-01..L-11; implementer-attributed evidence = results.md run run-20261012T112053Z-f6a83b5a1b72 (118 tests OK); incomplete: none for the reviewed bytes; owed correction/evidence owner: fresh task-maintainability-review (first outstanding stage per results.md route), T-005 role calls for compliance
- Preparation/context: docs/tasks/INT-FLOW-001/brief.md rev 1; verification.md rev 1; preflight.md ready; decision context = brief audit I-01..I-05 and finite-risk contract R-01..R-05
- Reviewer regressions: tests/test_task_maintainability_review.py, tests/test_task_review_discovery.py, tests/test_task_acceptance_review.py, tests/test_task_preparation_contracts.py, tests/test_task_flow_guides.py, tests/test_review_composition.py, tests/test_install_development_skills.py — command: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_task_maintainability_review test_task_review_discovery test_task_acceptance_review test_task_preparation_contracts test_task_flow_guides test_review_composition test_install_development_skills
- Aggregate gate: passed — 118 tests OK (3.054s); owner: initial discovery; reason: clean targeted reconciliation
- Next: separate task-acceptance-review decision call, which must consume the owed fresh maintainability evidence
```
