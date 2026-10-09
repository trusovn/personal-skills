# Task Brief: `T-001.3` — Validate packaged implementation entry and map evidence

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 13 tool calls / 35 minutes / 45k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 13. Estimated implementation duration: 35 minutes.
- Confidence: medium. Intended profile: `standard / high`.
- Policy result: fits. Triggered limits: none. Decomposition override: none.
- Estimate covers focused source edits, task-owned tests/fixtures and local checks.

## Readiness route

standalone guided preflight — confirm predecessor source interfaces, entry
fixtures and profile boundaries. This package requires separate verification
and compact durable readiness under plan section 1.

## Verification-design recommendation

separate — applicability and evidence omission can falsely admit packaged work;
separate design is also required by the packaged-stage rule.

## Outcome and direction trace

Implementer callers can enter a package only with current applicable ready
preflight and its justified verification revision, then submit evidence for every
scenario without recomputing readiness. Direct edits retain compact self-checks.
This supplies the implementation boundary exercised in the installed `T-005` proof.

- Authority: [project-plan.md](../../project-plan.md), sections 1, 4–7, 10–11;
  `T-001` in [task-map.json](../../task-map.json);
  parent [T-001](../T-001/brief.md), P-01/02/03/04/05/06/07/08.
- Contribution: `FLOW-001/003`, `IF-002`, `INV-001/002/003/005/007/011`.
- Why now: consumes reviewed .1 verification and .2 readiness/context contracts.
- Decisions used: plan section 5 applicability; IF-002 entry/submission ownership;
  section 10 T-001 compact direct-edit and no-rediscovery boundaries.
- New direction decisions required: None.

## Authority and scope

- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Depends on completed/reviewed `T-001.1`, `T-001.2`. Consumes `ART-001/002/003/008/009`;
  produces `ART-004` source contract and its `ART-009` slice.
- Allowed: `skills/task-implementation-flow/bounded-task-implementer/`, its
  eval definitions/setup, and focused entry/evidence tests in the flow package
  test area. Update only implementer-specific guide entries in profile/flow/root READMEs.
- Inspect canonical installer constants in the same change; synchronize a real
  changed dependency immediately. No new shared helper or installer selection is expected.
- Read-only: .1/.2 source contracts, other review roles, installed `.agents/` and plans.
- Excluded: high-assurance fingerprint or worker-result redesign, controller
  enforcement, reviewer launch, discovery split and complete correction routes
  owned by `T-002`/`T-003`. Preserve existing review/provenance and optional evidence rules.
- Unresolved decisions: none. New targeted command names are UNKNOWN for preflight.

## Work and acceptance criteria

1. Replace optional packaged prerequisites with entry applicability checks;
   preserve the distinct direct-edit and strict high-assurance routes.
2. Preserve stable scenario identity and current evidence/context in the submission;
   supply valid/invalid entry fixtures and focused source regressions.

- **AC-01:** Before package edits, verify executable leaf identity, matching
  authority/scope/verification revision and ready preflight. Missing/blocked/stale
  readiness, mismatched verification, composite/blocked task or direct legacy brief
  prevents entry and names the correct earlier owner. A package cannot be relabeled
  a conversational request to bypass these conditions.
- **AC-02:** Entry checks current material dependency/ownership/permission/capability
  and authority facts within the bounded context. The implementer does not become
  the readiness owner or perform broad discovery again. Expected implementation
  and report effects alone do not stale ready; a scenario revision cannot reuse
  affected obsolete readiness. Feasible task-owned future tests can be implemented.
- **AC-03:** Submission maps every verification scenario ID to current commands,
  setup/oracle and result or an explicit blocked/unchecked reason and next owner;
  carries the preflight/context reference and remaining obligations. Green tests
  cannot excuse an omitted AC or scenario. Implementer claims remain submission
  evidence, not independent acceptance.
- **AC-04:** Small clear direct edits retain compact verification/self-preflight.
  Packaged guided work gains no worker schema, exact digest chain or mandatory
  optional instrumentation. Existing high-assurance checks and review stops remain.
  Source-specific guide entries and supplied eval inputs agree with these rules.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| E-01 / INV-002/003: only applicable ready package enters | Valid ready; missing verification/readiness; blocked readiness; mismatched source/revision; composite/blocked/legacy brief; valid direct edit | Source entry decision and supplied real package starting states; actual agent edit/no-edit behavior later in T-005 | Regression rejects optional prerequisites; fixture setup supplies correct and faulty inputs | Attempt bypass by treating a documentation package as a direct edit | Implementer: targeted/package suite; T-005: authorized edit/no-edit calls |
| E-02 / INV-003: next occurrence respects material changes | First ready entry → expected implementation/report effect → next legitimate continuation; material dependency/ownership/permission/capability/authority change; revised verification with old then refreshed ready | Applicability rules name current revisions and earlier owner; fixture distinguishes expected and material changes | Supplied snapshots/revisions and source checks rejecting unconditional rediscovery | Use refreshed readiness for revised scenario, then substitute old revision | Implementer: targeted; T-005: actual continuation proof |
| E-03 / INV-001/005: submission retains coverage | Complete pass/fail evidence; blocked row; unchecked row; omitted AC/scenario despite green test; current versus obsolete evidence | Submission contract accounts for each ID and reason/context reference, without acceptance claims | Explicit fixture scenario ledger and expected submission; source regression | Trace one missing negative scenario through otherwise green output | Implementer: targeted; .4: cross-stage source/projection gate |

## Verification

- Fail-first: source-contract checks reject current optional package entry and
  incomplete evidence mapping. Preserve existing legacy-brief and provenance tests.
- Targeted: preflight resolves the exact new checks and safe fixture setup commands;
  supplied fixture starting states must include legitimate ready and rejected entry.
- Owning suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py`
  from root, after targeted checks pass.
- Broader local projection is .4-owned after composition. Actual edit/no-edit and
  handoff compliance are `T-005` agent proofs, not inferred from wording/fixture
  assertions; record unrun evals and obtain authorization before budgeted calls.

## Expected contract impact

- Change/materialize `ART-004/009`, `IF-002`, `INV-002/003/005`; preserve
  `ART-001/002/003/008`, `INV-001/007/011` and `FLOW-001/003`.
- Dependencies: .1/.2 source contracts and existing optional evidence/provenance
  rules; no current `docs/contracts` registry entries.
- Durable delta: implementation entry checks applicability instead of replacing
  readiness; submission carries current complete scenario evidence and context.

## Stops and handoff

Stop for invalid entry, ambiguous authority, user-work overlap, unsafe permission,
scope growth or absent decisive capability; route to the owning earlier stage.
Preserve user work, strict high-assurance checks and targeted-fix stops. Budget
is a soft checkpoint.
Next: separate verification design, standalone guided preflight, then bounded
implementation after .1/.2. Required follow-on: immediately after implementation
or correction, hand completed bytes to a fresh independent acceptance reviewer,
preserving applicable prior conditional stages; end the implementer invocation.
Completed source entry/evidence contracts feed `T-001.4`.
