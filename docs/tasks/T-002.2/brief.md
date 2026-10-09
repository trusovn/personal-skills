# Task Brief: `T-002.2` — Make acceptance admit discovery evidence and decide

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 12 tool calls / 32 minutes / 45k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 12. Duration: 32 minutes. Confidence: medium.
- Intended profile: `standard / high`. Policy result: fits; triggered limits:
  none; decomposition override: none. Estimate covers admission extraction,
  associated references/fixtures and local checks only.

## Readiness route

standalone guided preflight — confirm .1's completed evidence interface and
current review fixtures. Required `verification.md` precedes ready `preflight.md`.

## Verification-design recommendation

separate — separate-call provenance, evidence freshness and incomplete ledgers
can be misclassified during extraction. Existing fixtures are believed available;
confirm their commands/setup without inventing a verification harness.

## Outcome

Acceptance independently admits current discovery evidence and decides from it,
without repeating discovery's broad search, public probes or aggregate suite.

## Direction trace

- Contribution: `CAP-002`, `FLOW-002/003`, `ART-007/009`, `IF-005`,
  `INV-001/004/005/006`; consumes `ART-006` from .1.
- Effect: a separate decision call detects unsupported or stale claims and
  routes exact evidence gaps; enables .3's contextual rubric and T-005 proof.
- Why now: .1 provides the stable ledger/report and gate ownership to consume.
- Decisions: plan sections 1, 4–7, 10 (`T-002`), 11 role separation.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), cited sections; `T-002`
  [task-map entry](../../task-map.json); parent [brief](../T-002/brief.md), P-01–05.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Depends on completed/reviewed .1 and T-001; consumes
  `ART-001/002/003/004/005/006/009`; produces admission/decision `ART-007/009`.
- Allowed: acceptance `SKILL.md`, `references/acceptance-report-template.md`,
  existing eval definitions/setup; acceptance/discovery assertions in
  `tests/test_review_discipline.py`; stage-specific guide entries in root README,
  profile guide and flow README. Discovery sources remain read-only; interface
  defects return to .1. Inspect installer constants; no selection/helper change
  expected because acceptance is already installed.
- Excluded: .3 contextual rubric/known-issue expansion, .4 full guidance closure,
  T-003 correction matrix/cap changes, shared machinery, active refresh, live evals
  and official/historical artifact edits.
- Assumptions: guided and high-assurance profiles retain distinct input contracts;
  packaging alone does not require high-assurance digests or machine results.

## Work and acceptance criteria

1. Replace acceptance-owned evidence discovery with bounded admission of .1's
   output; transfer old probe responsibilities without weakening them.
2. Synchronize output/reference/eval contracts for separate calls and owners.

- **AC-01:** Acceptance is a separate call independent of production authorship
  and discovery; loading a role in an authoring session does not reset provenance.
  Self-check labels cannot issue a verdict or advance work. Discovery supplies
  facts; acceptance owns decision accountability. Missing discovery routes to
  that owner rather than silently doing both roles in one call.
- **AC-02:** Admit current authority, scope, verification revision, readiness/context,
  submission, applicable conditional evidence and discovery report. Reconcile
  every required/material row and confirmed finding with current reviewed bytes;
  summaries, old passes, report self-claims or green tests do not substitute for
  decisive evidence. Ordinary guided input gaps do not require an orchestrator
  packet. Explicit omitted AC violations still block.
- **AC-03:** Acceptance consumes discovery's targeted and aggregate records,
  checks adequacy, and requests focused missing/contradictory proof from its owner.
  It does not routinely rerun public probes, broad archaeology or suites.
  Applicable maintainability/registry facts remain inputs; acceptance retains
  authority to identify a demonstrated contract mismatch without becoming a
  second general maintainability reviewer.
- **AC-04:** Retain exactly `ACCEPT`, `CHANGES_REQUESTED`, `INCONCLUSIVE`;
  preserve every stable finding/row and explicit incomplete reason/owner.
  No required unverified boundary can support ACCEPT. Record the consumed
  aggregate's command/not-run, owner/stage, reason and current evidence.
  .3 supplies the full contextual and mixed-condition judgment rules.
- **AC-05:** Guided reports may be inline; durable decisions use the next unused
  `reviews/acceptance-NN.md`, preserve history and authorize no tracker writes or
  advancement. Preserve the existing explicit post-verdict tests-only exception:
  fixed CHANGES_REQUESTED first, exact current authorization/path, distinct status
  records, no production edit and no same-session acceptance of corrected bytes.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| A-01 / INV-004 | Separate independent calls; production author loads role; discovery tries verdict; acceptance tries discovery | Provenance/output constraints at human role boundary | Adapt current author-provenance eval 6 and new separate-call fixtures with supplied inputs | Trace a production-author session and verify no verdict authority is gained | .2 implementer: focused contract suite; T-005: actual calls |
| A-02 / INV-001/005 | Complete/partial; current/stale; omitted AC despite green tests; absent indispensable helper; unexplained index change | Admitted evidence versus authority/current bytes, retained unfinished ledger | Migrate current evals 1–5/7–9 into discovery inputs plus decision expectations; retain original signals | Supply a superficially complete report lacking the decisive second occurrence | Discovery: missing evidence; acceptance: admission/decision; .2: fixture checks |
| A-03 / INV-005 | Suppressed aggregate after failure; clean corrected report; premature aggregate from omitted row | Decision consumes .1's record without executing its command again | Preserve exact owner/order expectations in reports and fixtures | Compare decision request with discovery's command history for duplicate execution obligations | Discovery owns workflow aggregate; acceptance admits it |
| A-04 / INV-004 | No reproducer authorization; authorized exact test path after fixed verdict; corrected production needs fresh reviewer | Existing tests-only exception and write audit | Preserve eval 10 and tests-only reference; distinguish authorization from task scope | Trace verdict-before-write and reject same-session corrected acceptance | .2 implementer: local fixture checks; independent review: scope audit |

## Verification

- Fail-first: focused assertions reject old combined discovery/decision ownership;
  update rather than delete old schema obligations. Assert discovery exercises
  valid/invalid inputs and acceptance refuses missing decisive validator evidence.
- Targeted selectors and local fixture setup commands are resolved by derived
  verification/preflight. Fixtures retain real public/process inputs and outputs.
- Owning structural gate, .2 implementer after focused pass:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py`.
- No broader suite justified for this source/reference slice. Fresh reviewer
  corroborates a distinct admission trace. Actual call compliance remains T-005,
  separately authorized; report unrun checks and do not call text tests behavioral.

## Expected contract impact

- Change `ART-007` / `IF-005` and acceptance's `ART-009`; preserve .1's
  `ART-006` / `IF-004`, normative authority and narrow write ownership.
- Dependencies: .1 discovery source/report, T-001 preparation/context, existing
  conditional sources; no current `docs/contracts` registry.
- Delta: separate decision consumes corroboration and rejects unsupported claims;
  no new machine schema, gate or infrastructure.

## Stops and handoff

Stop for ambiguous authority, incomplete .1, incompatible report contract,
inseparable user work, unsafe permissions, widened scope or missing decisive
capability. Budget is a soft checkpoint. Preserve all prior work and reports.
Next: derived verification → ready standalone preflight → bounded implementation.
Required follow-on: immediately after implementation or correction, hand completed
bytes to a fresh independent acceptance reviewer after applicable conditional
stages; end the implementation invocation. After review, .3 consumes the admission
contract; independent discovery precedes decision when the new flow applies.
