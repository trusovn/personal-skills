# T-003.3 implementation handoff

Implemented: READY_FOR_REVIEW

Authority: `docs/tasks/T-003.3/brief.md`.
Preparation: `docs/tasks/T-003.3/preflight.md` and
`docs/tasks/T-003.3/verification.md`, verification revision 1.
Context: `docs/project-plan.md`, `docs/tasks/T-003/brief.md` and the read-only
ordered route in `docs/tasks/T-003.1/brief.md`. Guided invocation; initial
worktree clean. No pre-existing user changes were absorbed.

Deliverables:
- Source implementer correction guidance, eval 6 and existing record/route fixture
  extensions preserve all four row states, current evidence and separate owners.
- Acceptance and registry-updater source guidance closes the reference-only
  shortcut by actual effects and applicable proof.
- Discovery and acceptance report templates preserve continuation owners;
  discovery records current gate evidence and late-omission recovery order.
- Flow README and three existing owning test modules cover the affected contracts.

Actual contract impact: changed ART-004 / IF-002/006 correction continuation and
ART-005/006/007 consumption under IF-003/004/005. No new verdict, stage executor,
counter, shared helper or registry foundation. Executable contract declarations
changed: none. Existing fixture inputs and eval expectations changed.

## Commands and results

Run separately from the repository root with `PYTHONDONTWRITEBYTECODE=1`:

| ID | Exact command | Final result |
|---|---|---|
| I | `python3 -m unittest discover -s tests -p test_bounded_task_implementer.py` | 15 tests OK |
| A | `python3 -m unittest discover -s tests -p test_task_acceptance_review.py` | 23 tests OK |
| D | `python3 -m unittest discover -s tests -p test_task_review_discovery.py` | 15 tests OK |
| P | `python3 -m unittest discover -s tests -p test_task_preflight.py` | 7 tests OK; inherited readiness evidence |

Fail-first contract checks rejected missing continuation fields, missing prior-pass
fixture rows, missing template evidence and effect-bound routing. New fixture
setup initially lacked the added contrast files; those setup errors alone are not
behavioral evidence. The final probes execute the intended boundaries below.
A discovery test used the wrong folder and an insufficient first-invocation unit
check; it was corrected to run the public entry twice. No aggregate gate was run.

## Scenario and finite-risk evidence

These are implementation checks, not independent acceptance or observed agent compliance.

| Scenario | Current evidence, setup and oracle | Result |
|---|---|---|
| V-01 | I: `record-correction` supplies F-01, ROW-ORIGINAL/EXACT-BYTES/REMOTE-ANCHOR/REPLAY-BOUNDARY and V-01…V-04. Existing record suite fails on coherent mutation, passes after a disposable exact-byte correction; equivalent rewrite and files_changed mutation are rejected. Prior report remains unchanged; missing remote helper and unfinished replay row remain visible. Source handoff fields retain context, siblings, attempts, reasons and owners. | Local contract and fixture checks pass. |
| V-02 | A: authorized/forbidden mixed fixtures execute `python -m src.jobs.claim STATE` twice: JOB-1, then no claim. The pair helper is absent; policy allows or denies correction separately. Existing precedence checks retain blocked/unchecked and material-question owners; no-eligible-blocker INCONCLUSIVE is audited in source. | Public defect/capability facts and contract checks pass; no role verdict executed. |
| V-03 | I/A: existing .1 conditional policy/currentness matrix retained. `route-cases/change-effects/cases.json` supplies clarification, evidence, production, tests exception, genuine/disguised/missing-proof reference, scenario and authority contrasts with actual before/after files. `docs.contract.accepts` accepts 1 and rejects True for the genuine reference; the executable reference admits True. Missing-proof state denotes absent submitted proof, regardless of the test's later probe. Updater, source and consumer routes audited. | Diff, probe and route-contract checks pass. |
| V-04 | I/P/A: existing entry/revision-recovery fixtures retain IDs, revision-1 ready versus revision-2 scenarios, focused recovery and old-ready substitution. Available clock/session boundaries run; unavailable helper and changed authority remain distinct. Source rejects obsolete readiness even with new proof; ordinary expected effects do not restart design. | Fixture/setup and revision-contract checks pass; no preflight role executed. |
| V-05 | D/A: corrected queue public entry claims TASK-1 then TASK-2; defective diagnostic fixture claims only TASK-1. Diagnostic authorization remains separate. Source/template tests audit reconciliation, failure suppression, current record, no acceptance rerun and conditional duties. | Boundary and gate-contract checks pass; aggregate execution deliberately unrun. |
| V-06 | D: existing late-omission public validator accepts valid input. Clean fixture rejects boolean revision, older active attempt and second running task with exit 2. Defective fixture admits boolean revision but rejects the other two. Recovery order marks earlier gate premature. | All distinct public validator contrasts pass. |
| V-07 | A: existing stable-disposition/rubric checks preserved. Repeated retry probes show duplicate output under regression, formerly blocked proof, missed obligation, changed context/authority and newly material risk contrasts; settlement consumer observes 20. Informational KI-001 log exposure remains unchanged. Six reason branches and optional improvement controls audited. | Current fixture facts and disposition-contract checks pass; actual decisions unrun. |
| V-08 | I/A/P: two distinct record-binding hypotheses both accept an equivalent byte rewrite and fail the same exact-byte oracle. Stop input retains all four prior states, F-01, partial attempts and unfinished rows. Source tests audit non-complete stop, owned next approach, ordinary uncertainty, serious-delay/costly-later exception and task/user/capability stops without a global counter. Existing uncertainty context contrasts retained. | Failed-fix probes and stop-contract checks pass. |

Risk coverage: R-01 → V-01/02/03/08; R-02 → V-04;
R-03 → V-03; R-04 → V-01/05/06/07/08. No row omitted from this local map.
The two-failed-fixes contrast uses the existing record fixture; no scheduler
recovery fixture with two failed attempts existed in the scoped setup files.
This changes fixture placement, not the stop invariant or required evidence.

## Scope and next owners

Inspected `scripts/install_development_skills.py` selection, profile guide and
shared helper declarations. Skill paths and helper dependencies did not change;
no installer declaration needs synchronization. Active `.agents/` copies,
authority/preparation documents and official plans remain unchanged.

Skipped: whole-repository gate, composed sibling-output checks, installed
projection refresh and agent/model evals. The brief assigns composition and
installed projection to T-003.4; T-005 owns actual stage-output consumption and
separately authorized role calls. These remain unrun; fixture reports are
qualification inputs, not evidence that intermediate roles actually executed.

Next: fresh independent `task-review-discovery` evidence → separate fresh
`task-acceptance-review` decision. No repository policy was found requiring a
conditional architecture/maintainability gate for this submission; no current
contract registry exists to synchronize. Any newly applicable policy must retain
its conditional stages in the .1 order. End this implementer invocation here;
no self-acceptance, reviewer launch or advancement.
