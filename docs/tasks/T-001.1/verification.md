# Verification Design: T-001.1 — Bind packaged verification preparation to task authority

Source brief: docs/tasks/T-001.1/brief.md
Source brief revision: supplied ready brief read on 2026-10-09; no explicit revision label declared
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02 | All six input routes; documentation packages cannot use the conversational exception. |
| AC-02 | V-03, V-04 | Complete derived coverage, source/revision identity, decisive oracles and protected conflicts. |
| AC-03 | V-05, V-06 | Unchanged-authority recovery differs from requirement changes. |
| AC-04 | V-01, V-07 | Compact artifacts, existing sizing/ownership/review contracts and stage-specific guide consistency. |
| D-01 | V-01, V-02, V-07 | Executable leaf, composite, blocked design, legacy direct brief, small direct edit and compact documentation package. |
| D-02 | V-03, V-04, V-05, V-06 | Valid coverage, omission, unjustified scenario, weak oracle, conflicting source and both revision routes. |

This design verifies the leaf's source instructions, references, local regression
contracts and supplied eval inputs. It does not invoke downstream stages or prove
agent compliance. Local deterministic checks prove contract presence; fixture
setup checks prove that evaluators receive the required starting state. Actual
separate skill-call behavior remains the separately authorized T-005 obligation.
T-001 is a decomposed composite and receives no verification artifact here.

## Verification scenarios

### V-01 — Package identity requires both preparation stages

Covers: AC-01, AC-04, D-01

Intent: Reject optional packaged preparation and a direct-edit exception that
silently admits a small documentation package.

Given:
- Supplied inputs distinguish an executable leaf package, a compact executable
  documentation package and a small clear conversational edit without a package.
- Both packages contain a ready executable brief and cited authority, but no
  verification or readiness artifact. The conversational request is sufficient
  for the small edit's inline checks.

When:
- The source entry rules, brief/template/layout references and applicable eval
  expectations are checked against each supplied input.

Then:
- Each package requires a separate `verification.md`, followed by a current
  ready `preflight.md`, before implementation.
- The documentation package follows the same order even though its edit is small.
- The unpackaged conversational edit retains compact inline verification and a
  safety check; packaging it removes that exception.
- Compact guided Markdown artifacts suffice for the packaged route.

Oracle / boundary:
- Check the published contracts in the two allowed source skill packages and
  their preparation references. No entry instruction or generated-brief guidance
  may make either packaged stage optional.
- Inspect supplied eval authority, package state and expected next stage for each
  route. This inspection establishes discriminating inputs, not observed agent
  behavior.

Variants:
- Executable leaf; compact documentation package; small conversational direct edit.

### V-02 — Non-executable and legacy inputs route to their owner

Covers: AC-01, D-01

Intent: Reject apparent preparation success for an ineligible brief or bypass
through treating a legacy brief as an unpackaged direct edit.

Given:
- Separate supplied inputs contain a composite parent with `Status: decomposed`,
  a `blocked_design` brief and a direct legacy brief outside a task package.
- The composite names its executable children; the blocked input identifies its
  unresolved design decision; the legacy input has not been normalized.

When:
- The source preparation entry rules and applicable eval expectations are checked
  against these inputs.

Then:
- The composite is rejected as an execution target and directs the caller to a
  dependency-ready executable leaf.
- Blocked design returns to its task/decision owner for the unresolved decision.
- The legacy brief routes to `task-brief-designer` for package normalization.
- None of these routes claims ready package preparation or invokes the direct-edit
  exception to avoid the required correction.

Oracle / boundary:
- Source entry rules identify the rejection and next owner for each case. Eval
  setup supplies the actual status, location or missing decision that triggers it;
  a prompt merely naming the case is insufficient.

Variants:
- Composite/decomposed; blocked design; direct legacy brief.

### V-03 — Coverage closes in both directions with decisive observations

Covers: AC-02, D-02

Intent: Reject a plausible-looking verification artifact that hides an AC,
invents an obligation or substitutes a green test for the required result.

Given:
- A supplied executable fixture brief and cited authority define at least two
  independently observable material ACs and any finite-risk rows being exercised.
- A valid derived artifact identifies that brief and revision, maps all required
  rows, uses stable scenario IDs and states setup, action and a decisive oracle.
- Contrasting inputs omit one material AC, add an unsupported scenario or replace
  a required result oracle with evidence that cannot distinguish its violation.
- The omission case also supplies green evidence for the remaining covered ACs.

When:
- The source verification contract and supplied eval inputs/expectations are
  checked for AC-to-scenario and scenario-to-authority closure.

Then:
- Valid coverage remains derived from the identified brief and cited authority.
- Every material AC and finite-risk row is covered by a discriminating scenario;
  every scenario obligation is justified by that authority.
- The omitted AC remains an obligation despite green evidence elsewhere.
- An unsupported scenario cannot create a new requirement. An insufficient oracle
  cannot qualify as decisive proof of the result.
- Existing scenario identities remain stable when coverage is maintained or revised.

Oracle / boundary:
- Trace each coverage row to its scenario and each expected result to normative
  authority. Compare the weak oracle with the supplied required result: identify
  a wrong result that could still appear green under that oracle.
- Inspect local regression coverage and fixture contents for all four cases;
  schema validity or text presence alone does not prove agent compliance.

Variants:
- Valid coverage; omitted AC despite green tests; unjustified scenario; weak oracle.

### V-04 — Conflicting verification ownership protects existing work

Covers: AC-02, D-02

Intent: Reject overwriting an existing artifact merely because its filename
matches the requested output.

Given:
- A supplied package contains a brief and an existing `verification.md` with
  recognizable preserved content.
- Its `Source brief:` declaration is absent, malformed, non-singular or resolves
  to a different brief. A control input has one declaration resolving to the
  package's own brief.

When:
- The verification designer's overwrite contract and corresponding supplied
  fixture states/expectations are checked.

Then:
- Conflicting inputs require the artifact to remain unchanged and the conflict
  to be reported.
- The valid same-package declaration clears this ownership check; it does not
  waive authority or revision requirements.

Oracle / boundary:
- Inspect the source overwrite rule and actual pre-existing fixture files. Eval
  expectations must require unchanged file content for the conflict cases, not
  merely an explanatory message. Filesystem behavior itself remains unqualified
  until an authorized behavioral invocation observes it.

Variants:
- Missing, malformed, duplicate or foreign declaration; valid same-package control.

### V-05 — Coverage revision supersedes affected readiness and evidence

Covers: AC-02, AC-03, D-02

Intent: Reject fixing an omitted scenario while silently reusing readiness or
evidence from the previous design.

Given:
- Supplied starting artifacts include an unchanged normative brief, verification
  revision 1 with existing scenario IDs, ready preflight referring to revision 1
  and evidence for those scenarios.
- A material AC already in that authority is later found to lack adequate coverage.

When:
- The source revision contract and eval setup/expectations are traced through
  coverage-gap discovery, reasoned design revision and the next readiness step.

Then:
- The revision records why coverage changed, retains existing scenario IDs and
  supplies the missing discriminating scenario under unchanged authority.
- Affected prior readiness and evidence are superseded; they cannot qualify the
  new revision as ready or prove its new obligation.
- The next owner is focused preflight for the revised coverage. Any renewed ready
  state must refer to that revision; current evidence remains separately required.
- The coverage repair does not change the brief's requirements.

Oracle / boundary:
- The source contract explicitly links reason, revision identity, stable IDs,
  affected invalidation and focused preflight. Fixture setup supplies the actual
  initial brief, verification, readiness and evidence, with their references.
- Inspect expected transitions through renewed readiness. This leaf proves the
  designer's handoff contract, not downstream preflight/entry enforcement or
  composed recovery behavior.

Variants:
- None.

### V-06 — Changed requirements return to task design

Covers: AC-03, D-02

Intent: Reject using scenario revision to introduce or resolve a requirement
change that belongs to the authority owner.

Given:
- Supplied initial brief, verification and readiness identify the same authority.
- A contrasting input changes a required result or needs a product/scope decision
  that this authority does not settle, rather than exposing missing coverage of
  an existing obligation.

When:
- The source revision rules and supplied eval expectations are checked for the
  next permitted owner and action.

Then:
- Changed requirements route to `task-brief-designer` or the decision owner.
- Scenario editing cannot settle the new requirement or present the old
  preparation as current for changed authority.
- The unchanged-authority coverage-repair route in V-05 remains distinct.

Oracle / boundary:
- Compare the actual initial authority with the changed requirement or unresolved
  decision in the fixture. The source contract and expected output must name the
  authority route instead of a purported ready verification repair.

Variants:
- Changed required result; unresolved decision needed to state an expected result.

### V-07 — Binding preparation preserves compact scope and guidance

Covers: AC-04, D-01

Intent: Reject mandatory preparation that also imposes unrequested machinery,
weakens existing task safeguards or leaves the owned guidance contradictory.

Given:
- Existing source contracts define sizing, decomposition, package ownership and
  independent-review handoffs.
- The leaf permits changes only to its two source packages and their stage-specific
  guide entries; downstream enforcement, installer composition and behavioral
  qualification have separate owners.

When:
- The scoped source/reference changes and affected entries in `skills/README.md`,
  `skills/task-implementation-flow/README.md` and root `README.md` are compared with
  the brief and existing contracts.

Then:
- Owned guide entries agree with mandatory packaged preparation and the compact
  conversational exception.
- Existing sizing, decomposition, independent-review handoffs and package
  ownership remain intact.
- Compact guided artifacts do not require digests, machine outputs, controller
  contracts or a new shared helper.
- The canonical installer is inspected for selection, profile-guide and shared
  dependency effects. Any necessary dependency synchronization is handled now;
  installer regression/composition proof otherwise remains with T-001.4.
- Local instruction/fixture results do not claim behavioral qualification or
  trigger installation refresh.

Oracle / boundary:
- Inspect the bounded diff, affected guide entries and recorded installer
  inspection against the leaf's allowed/read-only/excluded surfaces. Requiring
  new high-assurance artifacts on the guided route or changing an excluded stage
  fails this scope check.

Variants:
- None.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  brief. `Status: ready` means design completion, not implementation readiness.
- Next is standalone guided preflight, producing compact `preflight.md` for this
  leaf and confirming the current brief/design revisions and source/profile scope.
- Implement the smallest source and test changes that satisfy the brief and
  exercise these scenarios. Concrete test structure, framework use, helpers and
  file placement remain implementation choices unless authority fixes them.
- Preserve fail-first evidence for the current optional route and inadequate
  coverage/revision contract. Preflight resolves the focused command; exercise
  fixture setup in a disposable `EVAL_WORK_ROOT` and inspect supplied inputs.
- After targeted checks pass, run the owning package suite stated in the brief.
  The projection gate belongs to T-001.4. Agent/model-budget evals are unrun unless
  separately authorized; retain the T-005 qualification gap explicitly.
- If a scenario cannot be exercised at its stated boundary, route the conflict
  to task design/preflight instead of weakening the oracle or widening this leaf.
- After implementation or correction, submit completed bytes for fresh independent
  acceptance through the required route; end the implementer invocation.
