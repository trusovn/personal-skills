# Task Brief: `T-005.4` — Carry an accepted issue into later readiness

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 13 tool calls / 35 minutes / 45k context
```

## Outcome and direction trace

Record whether the coordinator's actual accepted-deferral record reaches later
installed preflight with the right provenance and exposure-sensitive disposition.

- Direction contribution: FLOW-001/002/003/005, IF-001/005/006/008,
  INV-006/007/010/011; consumes ART-007, produces/consumes fixture ART-008 and
  later ART-003 observations for ART-012.
- User-observable effect: a later task sees a relevant accepted issue without
  hidden consumer workarounds or unrelated-task obligations.
- Why now: T-005.3 owns the actual acceptance output; this task consumes it.
- Direction decisions used: plan ART-008 ownership, section 6 rubric, IF-006,
  section 11 additional-proof table and optional context-link amendment.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 4, 6–8, 10–11;
  [parent brief](../T-005/brief.md), evidence rules and P-04.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`; dependency: T-005.3.
- Allowed: `docs/tasks/T-005.4/results.md`, `evidence/`, case-local adapters and
  coordinator-owned `docs/known-issues.md` only inside disposable fixtures.
- Inputs: .1 qualification receipts; .3 raw accepted-deferral output; COMP-04,
  DISP-01/CCR-08, known-issue consumption/proposed-work/committed-work/priority-only/
  no-links and correction-regression setup; existing contextual known-issue tests.
- Excluded: repository backlog edits, reviewer tracker writes, portfolio priority
  changes, hidden consumer fixes, source-policy changes, active refresh and history.
- UNKNOWN: actual accepted-deferral output and role-call permission at execution.
  If absent, prepare reproducible consumption inputs and report the composed gap;
  never fabricate a real acceptance or treat a fixture task as advanced.

## Execution sizing

- Policy: `default@1`; calls: 13; duration: 35 minutes; confidence: medium.
- Intended profile: `standard / medium`; result: `fits`; triggered limits: none.
- Decomposition override: none.

## Readiness route

Standalone guided preflight after derived verification — confirm .3's actual
decision or explicit gap, known-issue writer and qualified call permissions.

## Verification-design recommendation

Separate — provenance, changed exposure and similarly numbered records can be
confused. Derived `verification.md`, then ready `preflight.md`, are required.

## Work and acceptance criteria

1. Have the coordinator record the bounded deferral from .3's actual decision
   before any authorized fixture advancement; preserve task/review/finding IDs,
   trigger/consequence/evidence, impact/exposure, boundary/consumers, rationale,
   follow-up owner/action and reassessment conditions.
2. Feed that actual record to separate later preflight calls with relevant
   unchanged, relevant changed and unrelated exposure; preserve optional-link
   and priority-only controls without expanding tracker scope.

- **AC-01:** A claimed real record derives from actual current acceptance, is
  written by the coordinator and retains provenance; reviewers write only their
  artifacts. Staged seed records remain labeled fixture data.
- **AC-02:** Relevant unchanged exposure keeps the justified deferral; changed
  required-consumer exposure routes reassessment to the named owner. An unrelated
  task inherits no defect obligation and triggers no broad issue archaeology.
- **AC-03:** Proposed/committed future work alone does not justify deferral;
  priority-only change does not reopen acceptance; missing optional links mean
  unknown relationships. Distinct KI-001 examples remain scoped by provenance.
- **AC-04:** Each claim preserves actual producer/consumer identities, raw
  readiness output and current context or names its unrun/blocked gap. No hidden
  compatibility fix, automatic release or complete-backlog claim is introduced.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| K-01 / INV-007/010 | Actual decision → coordinator record → next preflight; staged seed contrast | Writer/provenance and actual record bytes consumed by later invocation | .3 output plus authorized coordinator/preflight observations; explicit gap otherwise | Trace one issue to raw decision/finding and its later reader | Qualification implementer: case evidence; fresh discovery: justified changed-owner aggregate |
| K-02 / INV-006/007/011 | Relevant unchanged, relevant changed, unrelated, priority-only, proposed/committed follow-up, optional links absent, separately scoped KI-001 | Readiness rationale follows actual boundary/exposure, never a label or hypothetical workaround | COMP-04/CCR-08 controls and current consumer probes | Contrast RPT-12A/RPT-12B/WEB-02 and the ORD-04 provenance | Same owner; fixture/leaf acceptance consumes discovery gate evidence |

## Verification

Reuse current .1/.3 evidence; selected record/consumer probes first. Nearest
owner: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p
test_contextual_known_issues.py`; `test_review_composition.py` only for changed
composition setup. A changed-exposure and an unrelated-task control must reject
the wrong blanket disposition. Actual preflight calls need separate concrete
authorization and preflight-resolved launch/capture. Check `git diff --check`,
prior-report and tracker ownership snapshots. Fresh discovery owns any justified
changed-owner aggregate; acceptance consumes it. No whole-repo/live gate.

## Expected contract impact

None: preserve ART-008/IF-006 ownership and optional context semantics; add only
task-local ART-012 observations. No formal issue schema or registry is added.

## Stops and handoff

Apply parent evidence rules. Stop for authority conflict, unsafe permissions,
user-work overlap, missing decisive capability or scope expansion. Missing real
upstream output/authorization leaves a gap, never apparent acceptance. Budget is
a soft checkpoint. Next: verification design → standalone guided preflight →
bounded implementation. Immediately after implementation/correction and applicable
conditional stages, fresh independent `task-review-discovery` receives completed
bytes, then separate `task-acceptance-review` receives its report. End the
implementer invocation. Reviewed evidence feeds T-005.6.
