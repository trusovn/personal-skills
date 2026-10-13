# Task Brief: `T-005.5` — Exercise complete correction handoffs

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 24 tool calls / 65 minutes / 65k context
```

## Outcome and direction trace

Record whether actual installed correction calls retain every finding/unfinished
row, repeat the applicable current stages and reach a fresh decision with one
justified aggregate execution per clean discovery review.

- Direction contribution: FLOW-002/003/005, IF-001–006/008,
  INV-001/003/004/005/006/008/010/011; consumes ART-001–007 and produces corrected
  ART-004/005/006/007 observations for ART-012.
- User-observable effect: the maintainer sees complete correction continuation
  and explicit owned stops rather than lost obligations or repeated optional fixes.
- Why now: .2 supplies preparation/recovery evidence; .3 supplies actual review
  outputs and mixed-condition findings; .1 supplies qualified fixtures/copies.
- Direction decisions used: plan IF-003–006, FLOW-003 and section 11; existing
  same-target failed-fix stop, with no added global correction limit.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 5–8, 10–11;
  [parent brief](../T-005/brief.md), evidence rules and P-05/P-06.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: T-005.2/.3; consume their actual outputs or carry their explicit
  gaps. No gap can stand in for a producer output in a claimed composed run.
- Allowed: `docs/tasks/T-005.5/results.md`, `evidence/`, missing case-local
  adapters; fixture-authorized production/test/reference corrections in disposable
  repositories, never policy-source repairs.
- Inputs: T-003.4 ROUTE/FIND/ROWS/EFF/GATE/DISP records and CCR-01–08;
  implementer `route-cases`/`record-correction`; maintainability `four-blockers`,
  `genuine-stop`, `correction-round`; discovery correction/late-omission/diagnostic
  fixtures; INT-FLOW-001 I-01–04 setup and current eval definitions.
- Excluded: new global counters, arbitrary fixture helper implementation for
  intentionally missing proof, controller/runner integration, active refresh,
  official-plan/old report edits. No registry stage is invented in this repository;
  registry-required cases use their disposable fixture's actual policy/registry.
- UNKNOWN: role-call authorization, applicable conditional stages and gate entry
  point in each fixture; preflight confirms these existing-capability facts.

## Execution sizing

- Policy: `default@1`; calls: 24; duration: 65 minutes; confidence: medium.
- Intended profile: `standard / high`; result: `override_cannot_split_safely`.
- Triggered limits: `max_agent_calls`, `max_duration_minutes`.
- `decomposition_override: cannot_split_safely` — considered separate failure,
  correction and clean-review tasks. They would share one mutable workspace,
  ordered report history, finding IDs and gate-count observation; restaging could
  reset state or fabricate the continuity this task must prove. Splitting route
  controls from that chain repeats the same currentness/oracle reconciliation.
  Keep one bounded owner of the composed history. Residual risk: repeated model
  calls can exceed time/budget; checkpoint unfinished rows and exact next owner
  instead of retrying indefinitely. Separate review stages remain independent calls.

## Readiness route

Standalone guided preflight after derived verification — confirm upstream reports,
fixture-owned conditional capabilities, current qualification and call budget.

## Verification-design recommendation

Separate — stage-currentness matrices, stable identities, aggregate execution
counts and genuine stops are non-obvious lifecycle evidence. Derived
`verification.md`, then ready `preflight.md`, are mandatory.

## Work and acceptance criteria

1. Exercise an actual failure → bounded correction → applicable fresh conditional
   stages → clean discovery → separate acceptance chain, preserving raw outputs.
   Carry .2's revision proof and .3's mixed-condition rows without renaming them.
2. Reuse route/currentness/effect controls and four-blocker/correction-round inputs;
   observe current IDs, all remaining findings and next numbered reports.
3. Observe discovery's aggregate ordering/count and acceptance consumption;
   retain late-omission and separately authorized diagnostic contrasts.

- **AC-01:** Neither/either/both conditional-stage cases name the first outstanding
  stage and full ordered remainder, including architecture when required. Actual
  calls satisfy applicable stages; merely naming them does not. Freshness follows
  affected scope/current proof, with absent registries never invented.
- **AC-02:** Four independently observable blockers survive without truncation;
  one corrected finding keeps its ID/disposition, three survivors keep IDs despite
  reorder, new findings use unused IDs, and prior report bytes remain unchanged.
- **AC-03:** Production/test/reference/clarification/evidence/scenario/authority
  changes follow actual effects and explicit exceptions. Genuine reference-only
  proof can keep the narrow route; executable effects or absent proof repeat owed
  discovery/gates. Corrections retain regressions, unfinished rows and sibling scope.
- **AC-04:** A decisive targeted failure suppresses the ordinary aggregate. After
  clean current targeted proof, discovery executes one justified aggregate in that
  review and records command/owner/stage/reason; acceptance does not duplicate it.
  An omitted material row makes prior aggregate evidence premature; finish its
  targeted proof before a still-justified rerun. Diagnostic authorization is distinct.
- **AC-05:** Mixed correction/evidence/authority routes retain every ID/owner;
  unchanged justified dispositions stay closed unless material facts change.
  Genuine regression/missed obligation stays visible. Two materially different
  failed fixes of one target produce an owned non-complete stop with attempts,
  partial state and unfinished rows; no global counter or advancement is invented.
- **AC-06:** Current observations and unrun gaps are explicit. Prior fixture
  reports/stop records are labeled inputs; no real continuation is claimed from
  fabricated intermediate outputs or unavailable calls.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| C-01 / INV-003/008 | Neither, maintainability only, registry only, both; architecture required/absent; current, stale, missing, inapplicable completion; affected/unaffected scope | First outstanding stage and full remainder match actual fixture policy/current proof | ROUTE-01/CCR-01 controls plus authorized real stage outputs | Trace registry-required correction and unaffected-current contrast | Qualification implementer: case evidence; fixture discovery: justified aggregate; leaf discovery: changed-owner aggregate |
| C-02 / INV-005/008 | MNT-B1–B4 → B2 corrected/three survivors; reordered output; unused new ID; next numbered report; genuine stop | Current probes/dispositions retain IDs and immutable prior history | FIND-01/CCR-04 and correction-round actual reports or gaps | Reproduce one surviving defect and B2 control; compare prior report bytes | Same owners |
| C-03 / INV-003/005/008 | Production, tests with/without policy exception, genuine reference, executable-reference, missing-proof reference, clarification, evidence, scenario, authority | Actual changed bytes and evidence determine route; all four row states/owners survive | EFF-01/ROWS-01/CCR-02/03; .2 revision and .3 mixed outputs | Challenge reference label with executable effect; follow one blocked sibling | Same owners |
| C-04 / INV-005 | Targeted failure → no ordinary aggregate; clean correction → one aggregate → acceptance zero repeats; late omitted fail/clean row; authorized diagnostic | Raw command observations and complete current ledger establish ordering/count/ownership | COMP-03/GATE-01/CCR-06 with actual discovery/decision calls | Inspect command log and late omitted-row ordering independently | Fixture fresh discovery owns aggregate after clean targeted proof; correction implementer runs targeted evidence first; acceptance consumes only |
| C-05 / INV-008/011 | Stable deferral versus changed exposure/regression/missed obligation; two distinct failed fixes of one target; pass/fail/blocked/unchecked rows | Owned stop/current justified disposition, full retained history and no advancement | DISP-01/CCR-08, record-correction and .3 continuation inputs | Trace attempts and next owner; contrast optional fix with demonstrated regression | Qualification implementer: case evidence; leaf fresh discovery: changed-owner aggregate |

## Verification

Selected real fixture probes/current rows first. Reuse current owning evidence;
renew only affected modules via `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
discover -s tests -p <owner>`: `test_bounded_task_implementer.py`,
`test_task_maintainability_review.py`, `test_task_review_discovery.py`,
`test_review_composition.py`. Role calls require separate concrete authorization;
preflight resolves invocation/capture and each fixture's real gate. Controlled
wrong variants must catch lost IDs/stale proof/duplicate aggregate without leaving
mutations. Check protected files and `git diff --check`. Fixture discovery owns
its existing justified aggregate; fresh review of this leaf owns any justified
changed-owner aggregate. Neither is an excuse to duplicate gates in acceptance.
No full-repository, live or model-budget gate is added.

## Expected contract impact

None: preserve ART-004/005/006/007, IF-002–006 and existing stop/routing contracts;
produce task-local ART-012 evidence. Fixture registry work creates no repository registry.

## Stops and handoff

Apply parent evidence rules. Stop for authority conflict, unsafe permissions,
missing decisive mechanism, user overlap or shared-tooling expansion. Record
unapproved calls as gaps. Preserve existing same-target stop and soft budget.
Next: verification design → standalone guided preflight → bounded implementation.
Immediately after implementation/correction and applicable conditional stages,
hand completed bytes to fresh independent `task-review-discovery`, then its report
to separate `task-acceptance-review`. End the implementer invocation. Reviewed
history and current gaps feed T-005.6.
