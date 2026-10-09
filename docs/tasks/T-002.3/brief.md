# Task Brief: `T-002.3` — Apply contextual risk and coordinator-owned deferrals

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 15 tool calls / 40 minutes / 50k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 15. Duration: 40 minutes. Confidence: medium.
- Intended profile: `standard / high`. Policy result: fits; triggered limits:
  none; decomposition override: none. Estimate includes rubric, record/consumer
  guidance, contrasting fixture inputs and local checks, excluding separate stages.

## Readiness route

standalone guided preflight — confirm .2 admission fields and T-001's current
context/known-issue consumption. Derive `verification.md`, then ready `preflight.md`.

## Verification-design recommendation

separate — mixed findings, context-dependent materiality, deferral lifecycle and
exceptional escalation admit several plausible wrong decisions. Existing role
fixtures provide a believed-available mechanism; no new harness is authorized.

## Outcome

Acceptance blocks demonstrated material risk, defers justified bounded issues,
continues through ordinary uncertainty and gives the coordinator complete
deferral or correction/evidence/authority routes without routine permission prompts.

## Direction trace

- Contribution: `CAP-002`, `FLOW-002/003`, `ART-007/008/009`, `IF-005/006`,
  `INV-001/006/007/011`; preserve `INV-004/005` role/evidence protections.
- Effect: callers get contextual fix-now/deferral reasons; later affected tasks
  reassess known issues without hidden workarounds. Enables .4 and T-005 proof.
- Why now: consumes .2's stable admitted ledger and separate decision boundary.
- Decisions: plan section 1 user decisions/amendment; sections 4/6 rubric and
  portfolio boundaries; sections 7, 10 (`T-002`), 11 contrasting evidence cases.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), cited sections; `T-002`
  [task-map entry](../../task-map.json); parent [brief](../T-002/brief.md), P-04–07.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Depends on completed/reviewed .2; consumes `ART-001/002/003/004/005/006/008/009`;
  produces contextual `ART-007` and ART-008 recording instructions, plus `ART-009`.
- Allowed: acceptance skill/report/eval fixtures; task-local rubric fixture checks
  in `tests/test_review_discipline.py`; coordinator/deferral guidance in flow
  README and stage-specific root/profile entries. Minimal preflight skill/packet
  reference/eval updates only if its implemented T-001 consumer wording omits an
  approved ART-008 obligation. Preserve adequate context sections by reference.
  Inspect installer constants; no new selected skill/shared helper expected.
- Read-only: discovery contract, unrelated preparation, plans, historical reviews
  and active `.agents/` copies. No real `docs/known-issues.md` record is created
  without an acceptance-approved deferral and coordinator authority.
- Excluded: portfolio prioritization, issue graph/schema/mandatory ontology,
  monetary/probability thresholds, complete context dossiers, routine user prompts,
  new global correction counter, T-003 handoff matrix, active refresh and live evals.

## Work and acceptance criteria

1. Encode the plan's contextual rubric and mixed-condition precedence using .2
   admission, preserving routine decision autonomy and evidence ownership.
2. Define coordinator recording and relevant later-consumer reassessment with
   contrasting supplied fixtures and bounded local checks.

- **AC-01:** Each confirmed finding includes trigger, consequence, affected
  boundary, separate impact and likelihood/exposure, existing mitigation and
  fix-now/deferral rationale tied to supplied operating/business/consumer and
  credible maintenance context. Passing ACs cannot excuse demonstrated material
  operating/business/contract/architecture/refactoring risk. Low likelihood cannot
  erase catastrophic data/security/irreversible consequences. A hard-rule breach
  is sufficient, not necessary; speculative redesign is not a blocker.
- **AC-02:** A bounded non-material defect with required evidence passing may
  receive ACCEPT plus an approved known issue; preferences/polish/unproved minor
  concerns are observations. Ordinary unknowns continue under stated reasonable
  assumptions without invented facts or routine prompts. Resolve serious-delay or
  materially costly-later uncertainty within existing authority first; ask one
  focused question only if that cannot settle it. Required proof is never waived.
- **AC-03:** Confirmed blocker with authorized bounded correction yields
  CHANGES_REQUESTED even beside missing proof or unresolved material-context
  questions. Keep every finding/unfinished row and route correction, evidence and
  necessary authority separately. If authority/scope/permission/dependency prevents
  bounded correction, use INCONCLUSIVE while retaining the blocker. Without such a
  blocker, missing decisive proof or unresolved decision-critical uncertainty is
  INCONCLUSIVE. Neither verdict permits advancement; ordinary uncertainty alone
  does not force either. Evidence requests do not imply production fixes.
- **AC-04:** The coordinator alone records acceptance-approved deferrals before
  authorized advancement. Default `docs/known-issues.md` records stable ID,
  task/review/finding provenance, trigger/consequence/evidence, impact/likelihood,
  affected boundary/consumers, rationale, follow-up owner/action and reassessment
  conditions. No file is required before a deferral. Relevant later preflight
  reassesses compatibility/exposure; unrelated issues trigger no broad search.
- **AC-05:** Optional known context links identify subsystem, stable contracts/
  flows/plans, confirmed versus suspected relations, safeguards/assumptions and
  reassessment triggers, proposed versus committed relevant work. Missing links
  mean unknown relations. Planned work alone is not mitigation. Acceptance has no
  portfolio scheduling/backlog-write authority; priority change alone cannot
  invalidate acceptance, but changed material facts can require focused review.
- **AC-06:** Preserve an accepted disposition while exposure is unchanged; a new
  blocker requires current proof, materiality and its reason (regression, formerly
  blocked evidence, missed existing obligation, changed context/authority or newly
  demonstrated material risk). Optional fixes never restart correction. Do not
  add a global round limit or replace T-003's existing task-specific stop rules.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-006/011 | AC violation with green tests; passing ACs with material operating/business/refactoring risk; required consumer breach; low-likelihood catastrophic risk; bounded minor defect; speculative preference | Same supplied concern under materially different explicit contexts yields justified block/deferral/observation | Contrasting runnable fixture authority/context/implementation/tests/reports, including exposure stated only in ART-003 and a decisive discovery probe | Trace a material refactoring consequence without a hard-rule breach and a genuinely mitigated counterpart | .3 implementer: local fixture/contract checks; T-005: actual role decisions |
| R-02 / INV-005/006 | Confirmed blocker + unrunnable required row with bounded correction allowed/forbidden; missing proof alone; blocker + unresolved context question | Exact verdict with all findings/unfinished rows, reasons and separate next owners | Mixed-condition fixtures reject dropped rows and wrong verdict precedence | Remove correction authority while retaining the demonstrated failure | Acceptance owns disposition; coordinator owns continuation |
| R-03 / INV-011 | Ordinary unknown; unresolved serious-delay/costly-later uncertainty resolvable within authority/not resolvable | Recorded assumption/continued decision versus one necessary focused escalation | Supplied known/unknown facts and permissions; no fabricated context or automatic issue prompt | Audit whether an evidence-owner request was misrouted as user approval | .3 implementer: focused checks; T-005: observed prompts/routes |
| R-04 / INV-007/011 | Deferral approved → coordinator record → relevant next preflight; unrelated next task; stable versus changed exposure; portfolio priority alone versus new material fact | ART-008 provenance and later compatibility disposition; no hidden workaround or reviewer tracker write | Record/consumer fixtures with safeguards, required consumers and explicit exposure changes | Trace a changed consumer requirement and a priority-only change separately | Coordinator: record before advancement; preflight: reassessment; .4: local composition |

## Verification

- Fail-first: new focused contract/fixture assertions reject unconditional
  ACCEPT-on-green-tests, ordinary-unknown prompts and dropped mixed rows.
- Derived verification/preflight resolve targeted selectors and fixture setup.
  Supply legitimate implementations, tests, context, admitted reports and
  expected routes; output text assertions alone prove structure only.
- Owning local gate, .3 implementer after targeted pass:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py`.
  Run a changed preflight fixture's local setup check only if that source changes.
- No repository-wide or live/agent-budget gate. Fresh reviewer checks a distinct
  contextual trace. T-005 owns actual multi-call/risk/next-task behavior evidence;
  preserve prepared fixtures and state all unrun gaps truthfully.

## Expected contract impact

- Change `ART-007` / `IF-005`; materialize coordinator ART-008/`IF-006` recording
  guidance and relevant preflight consumption; preserve role/evidence separation.
- Dependencies: .1 discovery, .2 admission, T-001 compact context/known-issue
  reassessment; no current `docs/contracts` registry.
- Delta: contextual disposition, bounded deferral provenance and later-consumer
  obligations. No formal issue schema, tracker automation or portfolio gate.

## Stops and handoff

Stop for missing material direction, incompatible admission/context interface,
user-work overlap, unavailable decisive capability, unsafe permission or scope
expansion. Do not resolve missing business policy by invention. Budget is soft.
Next: derived verification → ready standalone preflight → bounded implementation.
Required follow-on: immediately after implementation or correction, hand completed
bytes to a fresh independent acceptance reviewer after applicable conditional
stages and discovery; end the implementation invocation. Reviewed .3 supplies .4
with rubric/record fields and reusable fixtures, not real accepted-deferral records.
