# Task Brief: `T-005.3` — Exercise independent contextual review decisions

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 22 tool calls / 65 minutes / 60k context
```

## Outcome and direction trace

Record whether separate installed discovery and acceptance calls consume actual
current evidence and distinguish blocking risks, bounded deferrals, observations,
ordinary uncertainty and exceptional escalation in the supplied contexts.

- Direction contribution: FLOW-002/003/005; IF-004/005/006/008;
  INV-001/004/005/006/007/010/011; consumes ART-001–006, produces ART-006/007
  observations for ART-012 and a real bounded-deferral decision for T-005.4.
- User-observable effect: the maintainer can assess whether material defects
  block despite green ACs and whether ordinary uncertainty continues.
- Why now: T-005.1 supplies reproducible contexts and qualified installed copies.
- Direction decisions used: plan section 6 contextual rubric/mixed precedence,
  IF-004/005 and section 11.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 6–8, 10–11;
  [parent brief](../T-005/brief.md), evidence rules and P-03/P-04.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`; dependency: T-005.1.
- Allowed: `docs/tasks/T-005.3/results.md`, `evidence/`, missing case-local input
  adapters; disposable fixture changes within supplied correction authority.
- Read-only: T-005.1 inventory/receipts; COMP-01/02/05; existing discovery and
  acceptance fixture/eval families and contextual test owners. Preserve inherited
  public queue/exporter, index/worktree, ledger/workflow, process-cleanup and
  continuation cases with their decisive boundary obligations.
- Excluded: source-policy fixes, a role runner, tracker writes by reviewers,
  portfolio decisions, active installation refresh, old reports/master plans.
- UNKNOWN: role-call authorization/interface. Unapproved calls remain explicit gaps.

## Execution sizing

- Policy: `default@1`; calls: 22; duration: 65 minutes; confidence: medium.
- Intended profile: `standard / high`; policy result: `override_cannot_split_safely`.
- Triggered limits: `max_agent_calls`, `max_duration_minutes`.
- `decomposition_override: cannot_split_safely` — considered splitting discovery
  from decision or material from mitigated context. The first is a layer split
  that loses ownership of the observed handoff; the second duplicates the same
  fixture/context comparator and can substitute a different report/exposure.
  One owner must compare raw reports, prompt behavior and all retained rows in
  each paired call. Coordination/renegotiation costs exceed this bounded reuse.
  Residual risk: model latency/output corrections can exhaust the attempt;
  checkpoint with explicit unfinished cases rather than widen the campaign.

## Readiness route

Standalone guided preflight after derived verification — confirm raw-call isolation,
held-back oracle inputs, current qualification and concrete approved call budget.

## Verification-design recommendation

Separate — contrasting contexts, mixed verdict precedence and prompt behavior
need distinct falsifiable oracles. Derived `verification.md`, then ready
`preflight.md`, are mandatory; neither authorizes model-budget checks.

## Work and acceptance criteria

1. Exercise fresh discovery over supplied current code/tests/preflight context;
   preserve its raw report and feed it to a separate acceptance call. Supply
   existing staged history only as labeled history, never as the new producer.
2. Use contextual-risk, mitigated, mixed-condition and uncertainty contrasts.
   Supply a bounded non-material finding with passing required proof whose
   actual accepted disposition can be consumed by T-005.4.

- **AC-01:** Every claimed composed decision consumes an actual separate
  discovery output with packaged preparation references/current identities.
  Discovery gives evidence, not advancement; acceptance admits it without broad
  rediscovery or duplicate aggregate execution. Authors remain SELF_CHECK_ONLY.
- **AC-02:** Real AC failure despite green tests and missing/weak required proof
  cannot produce clean advancement. Existing public/lifecycle/validator/tamper/
  process/continuation cases are retained in the inventory with current evidence
  or explicit gaps, including valid and targeted invalid validator instances.
- **AC-03:** Passing ACs with preflight-only material operating/business/refactoring
  exposure produce the justified blocking disposition; mitigated/bounded debt
  may defer; speculative redesign is observation. Grade consequence and exposure
  separately; a severity label alone cannot establish the right judgment.
- **AC-04:** Ordinary uncertain concerns continue under stated assumptions
  without routine user prompts. Unresolved serious-delay/costly-later questions
  escalate only when current authority cannot resolve them; resolved contrasts
  continue. Missing required proof routes to its evidence owner.
- **AC-05:** A confirmed eligible blocker plus JOB-PAIR blocked/unchecked proof
  gives CHANGES_REQUESTED under authorized bounded correction, INCONCLUSIVE when
  that route is prevented. Both preserve findings/rows/reasons and separate owners;
  neither advances. Raw deferral decision or its explicit unrun gap feeds .4.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| D-01 / INV-004/005 | Separate producer/consumer; authored self-check; complete/partial/stale report; retained valid/invalid and public-boundary cases | Invocation provenance, actual report identities, current ledgers and unchanged unauthorized files | Existing owned probes plus authorized call outputs; gaps otherwise | Follow one raw report into acceptance inputs; inspect one valid/invalid boundary pair | Qualification implementer: case evidence; fixture discovery: justified aggregate; leaf discovery: changed-owner aggregate |
| D-02 / INV-006/011 | Material operating/business/refactoring exposure; catastrophic/required-consumer risk; mitigation; minor bounded debt; speculative preference; severity-only wrong decision | Supplied context plus decisive probe and reasoned disposition, including exposure present only in preflight | Contextual-risk/mitigated controls; reject permissive and fix-everything judgments | Compare same concern under materially different exposure; locate preflight-only fact | Same owners |
| D-03 / INV-011 | Ordinary unknown; unresolved serious-delay/costly-repair; resolved serious contrasts; missing required proof | Actual prompt/no-prompt behavior and evidence-owner versus authority-owner route | Uncertainty fixtures with recorded prompts, assumptions and next owner | Check that missing proof is not converted to a generic user decision | Same owners |
| D-04 / INV-005/006/008 | Confirmed blocker plus JOB-PAIR unfinished: authorized versus forbidden correction | Separate verdict and complete correction/evidence/authority routes; no advancement | Mixed-condition fixtures; preserve IDs, reasons and all unfinished rows | Trace JOB-PAIR and confirmed finding through actual decision output | Same owners; acceptance consumes aggregate evidence |

## Verification

Target actual selected fixture probes before any aggregate. Current nearest
owners: `test_task_review_discovery.py`, `test_task_acceptance_review.py`,
`test_contextual_export_risks.py`, `test_contextual_uncertainty_inputs.py`.
Use `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <owner>`
sequentially only for affected/renewed local evidence; reuse .1's other valid
results. Separate calls require concrete authorization and preflight-resolved
invocation/raw-output capture. Process cases retain observable synchronization,
bounded cleanup and no surviving fixture processes; no arbitrary sleeps.
Wrong implementations/context controls supply fail-first evidence without source
mutation. Check protected state and `git diff --check`. Discovery owns any justified
aggregate; acceptance never reruns it. No full-suite or live gate by default.

## Expected contract impact

None: observe existing ART-006/007, IF-004/005 and rubric; create task-local ART-012
evidence. Do not create `docs/contracts` or grant reviewers tracker authority.

## Stops and handoff

Apply parent evidence rules. Stop for authority/scope conflict, unsafe permissions,
unavailable decisive capability or shared-tooling expansion. Record unapproved
evals as gaps, retain every row/finding, and checkpoint at the soft budget.
Next: verification design → standalone guided preflight → bounded implementation.
Immediately after implementation/correction and applicable conditional stages,
send completed bytes to fresh independent `task-review-discovery`, then its report
to separate `task-acceptance-review`. End the implementer invocation. Reviewed
decision evidence feeds .4/.5; an unrun deferral cannot seed a claimed real record.
