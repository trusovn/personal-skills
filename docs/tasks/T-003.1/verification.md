# Verification Design: T-003.1 — Name the complete ordered submission route

Source brief: docs/tasks/T-003.1/brief.md
Source brief revision: SHA-256 9693af27578075b1331e39335c185ab226f01a84df2c7718f8e36408e7acd803
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

The source brief has no declared revision number; its digest identifies the
bytes used for this design. Normative sources are `docs/project-plan.md`
(sections 1, 5, 7, 10/T-003 and 11), `docs/task-map.json` (T-003), and
`docs/tasks/T-003/brief.md` (P-01, P-04 and P-07, within this leaf's scope).
Ready describes this design, not repository executability or passing behavior.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02, V-03 | All four policies, policy-dependent architecture gate, and ordered remainder after current stages or correction. |
| AC-02 | V-02, V-03 | First outstanding owner depends on applicable current evidence; stale evidence and an unsupported tests-only shortcut cannot skip required stages. |
| AC-03 | V-04, V-05, V-06 | Submission stop, independent roles, preparation/context and complete evidence, with milestone/no-review semantics preserved. |
| R-01 / INV-008 | V-01, V-02, V-03 | Initial submission, current/stale conditional evidence, and next submission after production correction. |
| R-02 / INV-004/005 | V-04, V-05, V-06 | Immediate review, milestone/no-review, and incomplete evidence retain truthful claims and owners without a verdict. |

## Evidence boundary and setup

This leaf changes human handoff guidance and supplied evaluation inputs. Its
local evidence is a contract audit of the implementer skill, initial/correction
templates, provenance/output instructions, affected root/profile/flow guide
routes, and existing eval prompts, expectations and generated fixture state.
Check the route's meaning and order, not merely the presence of stage names.
Extend existing preparation and fixture coverage; retain its distinct entry,
lifecycle, provenance and correction evidence cases.

Every route case must supply an executable brief, bound verification design,
applicable ready preflight/context, explicit conditional-stage policy, and stage
evidence whose scope/currentness is stated. Correction cases also supply the
preceding verdict and changed scope. A route expectation alone is insufficient
setup. These local checks prove guidance and fixture contracts, not an actual
agent's emitted handoff, role stop or compliance. T-005 owns that unrun behavior
proof; T-003.4 owns cross-child composition and installed projection. Neither
is a scenario or execution gate for this design.

## Verification scenarios

### V-01 — Initial routes include every applicable stage in order

Covers: AC-01, R-01

Intent: Reject unconditional discovery-next guidance, an omitted conditional
stage, reversed conditional order, or an architecture gate invented by default.

Given:
- Complete supplied preparation and an initial required-review submission.
- No applicable conditional stage has current completion evidence.
- Each policy in the table below, with architecture-gate applicability stated.

When:
- Inspect the prescribed first owner and full remaining route for each case
  in the public handoff guidance and its supplied fixture/eval expectations.

Then:
- The first owner is the leftmost stage in the applicable route below, and
  every remaining stage is named in that order.
- Discovery is fresh independent `task-review-discovery`; acceptance is a
  separate fresh `task-acceptance-review` decision.

| Conditional policy | Full outstanding route |
|---|---|
| Neither | Discovery → acceptance |
| Maintainability only; gate required | Architecture gate → fresh maintainability → discovery → acceptance |
| Maintainability only; gate not required | Fresh maintainability → discovery → acceptance |
| Registry only | Registry updater → discovery → acceptance |
| Both; gate required | Architecture gate → fresh maintainability → registry updater → discovery → acceptance |
| Both; gate not required | Fresh maintainability → registry updater → discovery → acceptance |

Oracle / boundary:
- Compare the published initial template, provenance/output guidance, affected
  overview routes and supplied case expectations against this policy table.
  Discovery/acceptance wording cannot override an earlier outstanding owner.
- Inspect generated fixture preparation and policy facts to ensure every
  expectation has an exercisable starting state.

Variants:
- All four conditional policies; required/absent architecture gate for each
  policy that includes maintainability.

### V-02 — Only applicable current evidence removes a stage

Covers: AC-01, AC-02, R-01

Intent: Reject always restarting completed stages, skipping a required stage
because a report exists, or skipping everything before discovery after one
conditional stage completes.

Given:
- The same explicit policy and prepared submission boundary as V-01.
- Supplied completion evidence identifies the stage, reviewed scope and
  applicability to the current submission; contrast it with stale or missing
  evidence for that same required stage.

When:
- Determine the first outstanding owner and full remainder from each supplied
  stage state using the published handoff contract.

Then:
- Only a stage with applicable current completion evidence is removed from
  the outstanding route. Stale or missing evidence leaves that stage owed.
- The remaining stages retain V-01's order and both fresh functional roles.
- The following discriminating states produce these exact remainders:

| Policy and supplied current completion | Outstanding route |
|---|---|
| Maintainability only; required architecture gate complete, maintainability outstanding | Fresh maintainability → discovery → acceptance |
| Maintainability only; all applicable conditional obligations complete | Discovery → acceptance |
| Registry only; updater complete | Discovery → acceptance |
| Both; required gate and maintainability complete, updater outstanding | Registry updater → discovery → acceptance |
| Both; updater current and applicable, gate/maintainability outstanding | Required architecture gate → fresh maintainability → discovery → acceptance |
| Both; all applicable conditional obligations complete | Discovery → acceptance |

Oracle / boundary:
- Audit route instructions and supplied case evidence against the table.
  Replace a credited completion with stale or missing evidence: the affected
  stage must return to the route, with its proper owner and successors.
- Inspect evidence applicability, not just report names or prior pass labels.

Variants:
- Current versus stale versus absent evidence for applicable gate,
  maintainability and registry obligations; omit the gate where policy does
  not require it. Neither-policy behavior is covered by V-01.

### V-03 — The next submission re-enters stages affected by correction

Covers: AC-01, AC-02, R-01

Intent: Reject carrying a prior acceptance or conditional pass across changed
production bytes, restarting unaffected current stages, or inventing a
tests-only exemption.

Given:
- A prepared task with an initial submission under each V-01 policy and a
  preceding review verdict requiring a bounded production correction.
- The next submission identifies corrected scope and affected prior evidence.
  Prior acceptance is stale; affected conditional evidence is stale.
- For the mixed both-stage case, gate/maintainability evidence is explicitly
  current for the corrected scope, while registry evidence remains stale.

When:
- Inspect the correction template and route guidance for the next submission,
  using the supplied policy and evidence state.

Then:
- Each affected applicable conditional obligation precedes fresh discovery
  and separate fresh acceptance; no old verdict accepts the corrected bytes.
- If all applicable conditional evidence is stale, the route equals V-01's
  full route for that policy.
- In the mixed both-stage case, the next owner is the registry updater and
  the remainder is discovery → acceptance. Current gate/maintainability proof
  is retained; stale acceptance cannot erase the remaining obligations.
- A tests-only correction with applicable conditional obligations and no
  repository-authorized exception cannot skip them merely because only tests
  changed. Stage completion still requires applicable current evidence.

Oracle / boundary:
- Trace initial state → production correction → next submission in supplied
  fixture facts and expected routes. Compare the correction template and
  provenance/output instructions with that trace, including evidence validity.
- This proves the correction route contract; it does not execute recovery
  policy, reviewers or a cross-task workflow.

Variants:
- All four conditional policies; mixed both-stage current/stale evidence;
  tests-only correction without an authorized policy exception.

### V-04 — Immediate review is a submission stop

Covers: AC-03, R-02

Intent: Reject guidance that treats naming a route as permission to launch
reviewers, wait for their verdict, or accept the author's work in the same session.

Given:
- A guided task with `review: immediate`, applicable ready preparation and
  completed implementation checks.
- Initial and production-correction submission forms, with any V-01 route.

When:
- Inspect the prescribed result and role/provenance rules at submission.

Then:
- The implementer ends at `READY_FOR_REVIEW`, names the first outstanding
  owner and complete remainder, and leaves stage launches to the caller.
- Naming conditional stages, discovery and acceptance does not launch,
  delegate to or wait for those roles in the implementer invocation.
- A same-session self-check remains labeled implementation evidence. Loading
  a review skill does not establish independent provenance or permit `ACCEPT`.

Oracle / boundary:
- Inspect both submission templates, provenance/output rules and matching
  eval expectations for the stop and separate-role obligations. Reject
  contradictory guidance elsewhere in these task-owned route surfaces.
- Local assertions cannot prove that an agent actually stopped; retain that
  explicit T-005 unrun gap.

Variants:
- Initial and correction submissions; conditional owner outstanding versus
  all conditional evidence current, so discovery is the next owner.

### V-05 — Submission retains context and every incomplete evidence row

Covers: AC-03, R-02

Intent: Reject an apparently clean submission that drops a scenario, hides an
unfinished obligation, loses preparation/context, or promotes implementation
claims into independent acceptance.

Given:
- Supplied bound preparation/context and a scenario ledger with current
  implementation evidence, plus failed, blocked and unchecked rows.
- Each unresolved row has a concrete result or reason and next owner.
- A contrasting ledger reports green tests while omitting a required scenario.

When:
- Inspect initial and correction output guidance and the supplied evidence
  cases at their submission boundary.

Then:
- The submission carries consumed preparation/context references and accounts
  for every scenario ID with current command, setup/oracle and result, or an
  explicit incomplete reason and owner.
- Remaining obligations retain every unresolved row and its owner, alongside
  the complete remaining review route. An omitted required scenario cannot
  be excused by other green tests.
- Failed or incomplete evidence stays visible and the reported state remains
  truthful; it is not called independently accepted or clean.
- Correction implementation outcomes remain separate from prior reviewer row
  status; unresolved reviewer coverage remains owed to its named owner.

Oracle / boundary:
- Reconcile supplied ledger IDs with the published output fields and fixture
  expectations. Inspect actual supplied commands/setup/results for evidenced
  rows and reasons/owners for incomplete rows; a populated heading alone
  proves neither completeness nor behavior.
- Reuse the existing complete/defective ledger and correction preparation
  cases; preserve their distinct failure and unchanged-status evidence.

Variants:
- Complete ledger; mixed failed/blocked/unchecked ledger; green-test ledger
  with an omitted required scenario; initial and correction forms.

### V-06 — Route repairs preserve milestone and no-review semantics

Covers: AC-03, R-02

Intent: Reject making every implementation an immediate-review stop or allowing
non-immediate metadata to bypass an independently required functional review.

Given:
- Prepared milestone and no-review work whose supplied metadata, user request
  and risk/policy do not require independent functional review at this invocation.
- A contrast where milestone metadata accompanies an explicit requirement for
  independent functional review.

When:
- Compare prescribed output and follow-on guidance before and after the route
  repair, using each supplied review condition.

Then:
- Milestone/no-review work retains its existing human result semantics; the
  route repair does not impose `READY_FOR_REVIEW` solely by default.
- Required proof remains accounted for as in V-05, with no self-acceptance claim.
- Where functional review is required, applicable conditional stages precede
  fresh discovery and separate acceptance under V-01/V-02; metadata cannot
  authorize acceptance without discovery.

Oracle / boundary:
- Compare the unchanged milestone/no-review contract with affected output and
  provenance guidance and supplied case metadata. Verify both the legitimate
  absence of an immediate-review requirement and the explicit-review contrast.

Variants:
- Milestone; no independent review required; milestone with explicit required
  functional review. Do not invent a new metadata value or result schema.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  brief. Preflight confirms current dependency contracts, setup and selectors.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief
  and exercise these scenarios. Concrete framework usage, helpers and file
  placement remain implementation choices within the brief's allowed scope.
- Start with fail-first changed contract cases that reject hard-coded
  discovery-next or a skipped conditional obligation. Existing local selector
  anchors include implementer submission/evidence cases and guide child-handoff
  and implementer-eval route cases; confirm narrower selectors at preflight.
  A fail-first result must fail on the intended route obligation, not missing
  preparation or a broken fixture.
- After targeted cases pass, run the brief's owning gates sequentially from
  the repository root:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py
  ```

- Check affected source/guide/fixture wording together and inspect the canonical
  installer selection, guide and helper declarations as required by the brief.
  Leave unrelated declarations and active `.agents/` copies unchanged.
- Report local guidance/fixture proof separately from unrun T-005 emitted-route
  and role-stop behavior. No broad, network, model or agent-eval gate is assigned
  here; T-003.4 retains composition/installed-profile checks.
- If discovery shows that a scenario cannot be exercised at its stated
  boundary, route the conflict to task design/preflight; do not weaken the
  oracle or invent a requirement. This design does not approve implementation.
