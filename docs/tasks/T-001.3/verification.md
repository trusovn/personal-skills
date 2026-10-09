# Verification Design: T-001.3 — Validate packaged implementation entry and map evidence

Source brief: docs/tasks/T-001.3/brief.md
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02, V-04 | Applicable ready entry, all rejected input classes, package-bypass attempt and obsolete verification revision. |
| AC-02 | V-01, V-03, V-04 | Bounded applicability, expected versus material changes, feasible future tests and focused renewed readiness. |
| AC-03 | V-05, V-06 | Current complete scenario evidence, explicit unfinished rows, context and submission-only claims; green tests cannot hide omissions. |
| AC-04 | V-07, V-08 | Compact direct edits, guided versus strict high-assurance routes, preserved stops, optional evidence and matching guides/eval inputs. |
| E-01 | V-01, V-02, V-07 | Valid ready, every invalid entry variant and valid direct edit. |
| E-02 | V-03, V-04 | Next continuation after expected effects, each material fact change and old/refreshed readiness after scenario revision. |
| E-03 | V-05, V-06 | Pass/fail, blocked/unchecked, omitted AC/scenario and current/obsolete evidence. |

These scenarios verify this leaf's source entry/submission contract and supplied
fixture states. Source regressions and fixture assertions do not prove an agent
obeyed the contract. Actual edit/no-edit and continuation behavior remains the
separately authorized `T-005` proof; cross-stage projection remains `T-001.4` work.

## Verification scenarios

### V-01 — Applicable ready package permits bounded implementation

Covers: AC-01, AC-02, E-01

Intent: Reject optional prerequisites and unnecessary readiness recomputation,
while avoiding rejection merely because a task-owned future test is absent.

Given:
- An executable leaf package has normative authority, allowed scope, a justified
  verification revision and ready preflight bound to those same inputs.
- Current material ownership, dependency, permission, capability and authority
  facts match the bounded preflight context.
- One task-owned future test does not yet exist, but its setup, tools and
  observation boundary are feasible within scope.

When:
- The implementer evaluates entry before any package implementation edit.

Then:
- The source contract permits entry after checking applicability of the supplied
  ready decision, without making the implementer the readiness owner or requiring
  broad discovery again.
- The feasible future test may be implemented; its absence is not equated with
  missing indispensable capability.

Oracle / boundary:
- Compare the source entry rules with the fully supplied legitimate fixture:
  brief, verification, ready preflight, current bounded facts and feasible test
  setup. Require an explicit permitted route, not just absence of rejection text.

Variants:
- None; invalid prerequisites are isolated in V-02 and V-03.

### V-02 — Invalid preparation stops entry and names the earlier owner

Covers: AC-01, E-01

Intent: Reject implementations that admit incomplete preparation or let a caller
rename packaged documentation work as a conversational direct edit.

Given:
- The V-01 valid starting state is supplied, with exactly one invalid condition
  substituted from the variants below.

When:
- Entry is evaluated before package implementation edits, including an attempt
  to call the invalid documentation package a small conversational request.

Then:
- Entry is prevented; relabeling does not bypass package prerequisites.
- Missing/mismatched derived verification routes to verification design and then
  current preflight; missing, blocked or stale readiness routes to preflight.
- Composite, blocked-design, legacy direct brief, or invalid task authority/scope
  routes to task design or the authority owner, followed by affected preparation.
- The blocker and smallest earlier-stage action are stated rather than silently
  repairing authority or issuing a new ready decision in implementation.

Oracle / boundary:
- Source rules and supplied invalid package fixtures identify rejection before
  implementation and the applicable owner. Each fixture must actually supply its
  faulty state; a fixture name or keyword assertion alone is insufficient.

Variants:
- Missing verification; missing preflight; blocked preflight; stale readiness.
- Verification names another source brief; verification revision differs from
  the ready reference; ready names another task/authority revision or scope.
- Composite/decomposed task; blocked-design task; direct legacy brief outside the
  required package layout.
- Apply the conversational-relabel attempt to the invalid documentation package.

### V-03 — Continuation distinguishes expected effects from material change

Covers: AC-02, E-02

Intent: Reject both unconditional rediscovery after task edits and unconditional
reuse of ready after a material prerequisite changes.

Given:
- V-01 entry was valid and the first bounded implementation occurrence produced
  expected in-scope edits and report effects.
- The next legitimate continuation has either only those expected effects or
  one material fact change from the variants below.

When:
- The implementer checks ready applicability for that continuation.

Then:
- Expected implementation/report effects alone do not stale guided readiness or
  require broad rediscovery.
- A material change prevents use of the affected old ready decision and names
  preflight as owner of reconsideration; changed requirements return to task
  design or the decision owner rather than being settled by derived scenarios.
- The implementer checks bounded current facts without replacing preflight's
  readiness decision. Missing decisive capability is not waived as a future test.

Oracle / boundary:
- Supplied before/after snapshots distinguish attributed expected effects from
  each changed fact. Source applicability rules must produce the corresponding
  continuation or earlier-owner route. Exact high-assurance freshness is checked
  separately in V-07.

Variants:
- Expected implementation effects; expected report effects.
- Material dependency/prerequisite, ownership, permission, required capability,
  or authority change, each exercised separately.

### V-04 — Revised scenarios require readiness for that revision

Covers: AC-01, AC-02, E-02

Intent: Reject comparison of scenario IDs alone and reuse of affected obsolete
readiness after verification changes.

Given:
- Under unchanged authority, verification receives a reasoned coverage revision
  retaining existing scenario IDs.
- The supplied old ready reference still binds the affected earlier revision;
  a second supplied ready decision binds the revised obligations after focused
  preflight, reusing unchanged relevant facts.

When:
- Entry is evaluated with old ready, then with refreshed ready, and the old
  reference is substituted again.

Then:
- Old ready is rejected on both occurrences despite unchanged scenario IDs;
  the next owner is focused preflight for the revised obligations.
- Refreshed applicable ready permits entry without a requirement to restart task
  design or full discovery under unchanged authority.

Oracle / boundary:
- Observe the source applicability contract against explicit verification
  revisions, reasons and old/current ready references. Refreshed readiness is a
  supplied preflight output, not an implementer-authored approval.

Variants:
- None.

### V-05 — Submission preserves complete current evidence and unfinished work

Covers: AC-03, E-03

Intent: Reject a green-only summary, lost scenario identity or a submission that
claims independent acceptance.

Given:
- A valid package has multiple stable scenario IDs and their AC relationships.
- Current observations include passed and failed checks, a blocked scenario and
  an unchecked scenario. Setup, commands, decisive oracles and results are
  supplied for exercised rows; reasons and next owners are supplied for the rest.
- The preflight/context reference and remaining task obligations are available.

When:
- The implementer submits its current scoped work and verification evidence.

Then:
- Every scenario ID and material AC is accounted for; exercised rows carry current
  commands, setup/oracle and actual results, including failures.
- Blocked and unchecked rows retain explicit reasons and next owners, without
  being converted to passes or silently dropped.
- The submission carries the current preflight/context reference and remaining
  obligations, preserving relevant optional evidence/provenance rules.
- Claims remain implementation submission evidence. Required review stops and
  independent-review provenance remain intact.

Oracle / boundary:
- Trace each authoritative scenario/AC through the supplied evidence ledger to
  the expected submission contract, including unfinished rows and references.
  Compare claims with actual supplied outcomes rather than aggregate exit status.

Variants:
- Complete pass/fail evidence; mixed exercised, blocked and unchecked rows.

### V-06 — Green or obsolete evidence cannot conceal a coverage gap

Covers: AC-03, E-03

Intent: Reject a report that treats successful tests as coverage of an omitted
negative scenario, omitted AC or changed obligation.

Given:
- A package has green results for some current scenarios, including enough setup
  to establish what those checks actually exercised.
- Its candidate evidence has one defect from the variants below.

When:
- The implementer reconciles the evidence with current authority and verification
  before submission.

Then:
- The missing or obsolete obligation remains explicit rather than being inferred
  passed from green checks.
- Current evidence is supplied, or the row is retained as blocked/unchecked with
  its reason and next owner; a missing authoritative AC cannot be excused by its
  omission from derived verification.
- Evidence tied to an affected obsolete revision or changed implementation bytes
  is not presented as current proof.

Oracle / boundary:
- Compare current ACs, scenario IDs/revisions and scoped bytes with the candidate
  evidence and expected submission. The source contract must require complete
  reconciliation, not merely a test command or total pass count.

Variants:
- Omitted required negative scenario despite other green tests.
- Material AC absent from the evidence/derived scenario mapping.
- Affected evidence from an obsolete verification revision; affected evidence
  collected before implementation bytes changed.

### V-07 — Direct, guided packaged and high-assurance routes retain their limits

Covers: AC-04, E-01

Intent: Reject formal package overhead for a valid small direct edit, mandatory
instrumentation for guided work, and relaxation of strict high-assurance checks.

Given:
- Supplied entry states distinguish a small clear direct request without a task
  package, a valid guided package and a strict high-assurance invocation.
- Existing high-assurance freshness/result/provenance obligations and review
  stops are available as the comparison baseline.

When:
- Each route is evaluated with the variants below.

Then:
- The small direct request retains compact self-preflight and verification.
- A guided package still requires V-01 preparation but gains no worker-result
  schema, exact digest chain or mandatory optional instrumentation.
- Unavailable best-effort evidence does not alone block guided work; explicitly
  required evidence remains strict.
- High-assurance missing inputs or exact freshness mismatches stop under existing
  rules; it cannot silently downgrade to guided mode. Existing review/provenance
  and targeted-fix stops remain in force.

Oracle / boundary:
- Compare the revised source's route-specific obligations with supplied route
  inputs and existing strict checks/stops. A permissive guided example alone
  cannot establish preservation of high-assurance behavior.

Variants:
- Valid direct edit; valid guided package with optional evidence available or
  unavailable; guided input with explicitly mandatory instrumentation absent.
- Valid high-assurance input; missing required high-assurance input; unexplained
  exact freshness mismatch.

### V-08 — Guides and runnable eval inputs describe the same contract

Covers: AC-04

Intent: Reject corrected skill text distributed with stale optional-prerequisite
guidance or eval inputs that cannot exercise their claimed outcomes.

Given:
- Revised implementer source, implementer-specific flow/profile/root guide
  entries, eval definitions/setup and focused regressions are available.
- Canonical installer constants and managed dependencies have been inspected.

When:
- Task-local checks compare these surfaces and prepare the supplied valid and
  invalid entry/evidence fixture states.

Then:
- Guides and eval expectations agree with mandatory applicable package preparation,
  complete current submission evidence and distinct direct/high-assurance routes.
- Setup supplies the actual authority, verification, readiness, revision/context
  and evidence needed for each claimed success or rejection.
- Any real changed installer dependency is synchronized within its narrow managed
  boundary; no new helper or profile selection is required merely by this task.
- Unrun agent evals are recorded as unrun; source/fixture checks are not reported
  as actual edit/no-edit compliance or installed composition proof.

Oracle / boundary:
- Inspect the stage-specific source/guide contracts and prepared fixture contents
  against V-01 through V-07. Observe local setup results and focused regressions;
  schema/syntax checks alone cannot substantiate behavior claims. Leave full
  projection and agent-call evidence with their named later owners.

Variants:
- Valid and invalid entry fixtures; complete and faulty scenario evidence inputs.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios.
- Concrete test structure, framework usage, helpers and file placement remain
  implementation choices unless already fixed by repository authority.
- If implementation discovery shows that a scenario cannot be exercised at its
  stated boundary, route the conflict back to task design/preflight rather than
  silently weakening the oracle.
- Preflight resolves new targeted checks and safe fixture setup commands. Run
  targeted checks before the brief's owning package-resource suite; preserve
  existing legacy-brief and provenance regressions. Do not infer behavioral
  qualification from source assertions, or launch budgeted agent evals here.
- Full correction routes, cross-stage projection and installed agent compliance
  remain with `T-003`, `T-001.4` and `T-005` respectively. This design neither
  composes those tasks nor approves implementation correctness.
