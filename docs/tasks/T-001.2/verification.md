# Verification Design: T-001.2 — Own compact packaged readiness and revision recovery

Source brief: docs/tasks/T-001.2/brief.md
Source brief revision: repository commit b1b257f65931f9e6cf82164666805b93af361477 (clean worktree at design)
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02, V-03 | Complete justified coverage and feasible proof; readiness is not a behavior pass. |
| AC-02 | V-03, V-07 | Future tests versus indispensable capability; strict high-assurance freshness retained. |
| AC-03 | V-01, V-04 | Revision-bound context, relevant issues, ordinary assumptions and exceptional escalation. |
| AC-04 | V-05, V-06 | Focused scenario recovery, material changes, expected effects and requirement routing. |
| AC-05 | V-01, V-08 | Durable compact packages, inline direct requests and consistent supplied guidance/fixtures. |
| R-01 | V-01, V-02, V-03 | Valid verification; omitted AC; unjustified scenario; weak oracle; future test; unavailable capability; wrong source brief. |
| R-02 | V-05, V-06, V-07 | Both readiness versions, stable IDs, changed facts, expected effects and non-artifact preservation. |
| R-03 | V-04 | Relevant/unrelated/no recorded issue; ordinary unknown; unresolved serious-delay/costly-later uncertainty. |

## Observation scope

This leaf changes instructions, references, guidance and supplied eval inputs.
Its local evidence is focused source-contract regression plus disposable fixture
setup audit: check that actual authority, Git state, context and capability
inputs support each expected result. Text presence or successful setup alone
does not prove semantic skill compliance. Actual separately authorized role-call
proof belongs to T-005; broader source/profile composition belongs to T-001.4.
The scenarios below define this leaf's contract and fixture oracles without
adding downstream implementation, review or installation scenarios.

## Verification scenarios

### V-01 — A valid package yields durable readiness without claiming behavior passed

Covers: AC-01, AC-03, AC-05, R-01

Intent: Reject optional packaged verification, inline-only packaged readiness,
incomplete feasibility checks and readiness presented as implementation success.

Given:
- An executable ready package has normative authority and a source-matched
  verification revision covering every material AC with justified scenarios.
- Setup, decisive boundaries, commands, dependencies, permissions and ownership
  are feasible; relevant decision context has supplied references.
- Task behavior has not yet been implemented or verified.

When:
- Guided preflight assesses the package, including when current facts are routine.

Then:
- The contract requires a compact canonical `preflight.md` beside `brief.md`,
  identifying the brief, allowed scope and scenario revision it assesses.
- Every material AC/scenario has an authority relationship and feasible
  setup/boundary/command/dependency/permission/ownership conclusion.
- Readiness includes commands/oracles, referenced decision context, meaningful
  assumptions/stops and the next action; it does not claim future behavior passed.
- A package alone requires no digest ledger, tracker, machine schema,
  instrumentation or separate context artifact.

Oracle / boundary:
- Compare source skill/packet obligations and supplied fixture expectations with
  the fixture's actual package, authority and available prerequisites. Verify
  that canonical durable output and all readiness fields are required.

Variants:
- Routine compact documentation package; package with material readiness uncertainty.

### V-02 — Defective verification cannot be made ready by other green evidence

Covers: AC-01, R-01

Intent: Reject treating verification as optional paperwork or as independent
authority, and reject waiving omitted proof because other tests pass.

Given:
- An otherwise feasible executable package has one verification defect.
- Existing passing evidence, if supplied, does not resolve that defect.

When:
- Packaged readiness checks source identity, AC coverage, scenario justification
  and decisive boundaries against the brief and cited authority.

Then:
- The defective package cannot receive ready readiness.
- The gap remains visible with its evidence, owner and smallest correction route;
  preflight neither invents requirements nor silently drops the affected AC/scenario.

Oracle / boundary:
- Inspect the source refusal/routing rules and contrasting supplied inputs. Each
  defect must be concrete enough to falsify a ready expectation independently.

Variants:
- Missing verification; verification naming another source brief; omitted material
  AC; scenario unsupported by authority; oracle that cannot decide required behavior.

### V-03 — Future test absence and missing indispensable capability have different outcomes

Covers: AC-01, AC-02, R-01

Intent: Reject both requiring finished tests before implementation and assigning
an unavailable prerequisite to implementation without authority.

Given:
- Source-matched justified verification requires a task-owned test not yet written.
- One supplied state has feasible in-scope setup, tooling and a decisive boundary;
  a contrasting state lacks an indispensable capability.
- Other readiness facts are equivalent and acceptable.

When:
- Preflight evaluates whether the required proof can be produced within scope.

Then:
- The feasible future-test state can be ready, naming the planned proof and
  command feasibility without claiming that the absent test ran or passed.
- The unavailable-capability state is blocked with concrete evidence, owner and
  smallest route; it is not silently made new implementation scope.
- Missing required dependencies, unauthorized required permissions or unresolved
  user-work ownership similarly prevent ready when they make execution infeasible.

Oracle / boundary:
- Audit actual supplied tools/helpers, allowed scope, permission policy and Git
  ownership inputs against the source distinctions and expected ready/blocked
  outputs. A placeholder assertion cannot establish capability feasibility.

Variants:
- Absent task-owned future test with feasible setup; absent indispensable
  capability; unavailable required dependency; unavailable required permission;
  inseparable user-work overlap.

### V-04 — Relevant context informs readiness without turning ordinary unknowns into blockers

Covers: AC-03, R-03

Intent: Reject invented business policy, blanket issue rediscovery, routine
questions and omission of required proof under contextual uncertainty.

Given:
- Supplied context identifies intended use/operating envelope, important
  consequences, relevant priorities/consumers/planned maintenance, mitigations
  and decision-relevant unknowns, with references where available.
- Issue and uncertainty variants below retain the same task proof obligations.

When:
- Preflight records context and reassesses relevant recorded known issues.

Then:
- Relevant issues are assessed against this task's exposure and existing
  obligations; unrelated issues do not trigger broad rediscovery.
- No known-issues file means no recorded deferrals, not a preparation blocker.
- Ordinary unknowns become stated reasonable assumptions without routine user
  questions or automatic blockers; required proof rows remain binding.
- For credible serious consequences of delay or materially costly later repair,
  current authority is used first. Only a still unresolved decision-critical fact
  calls for one focused question explaining the consequence and needed fact.
- The result records supplied facts and unknowns without inventing business policy
  or waiving capability, permission or ownership requirements.

Oracle / boundary:
- Compare source context/routing rules and fixture expected outputs with actual
  contextual and issue inputs. Serious-risk variants must supply the concrete
  consequence and whether existing authority can resolve it.

Variants:
- Relevant known issue; unrelated known issue; no recorded issue/file; ordinary
  unknown; serious-delay uncertainty; costly-later uncertainty. For the last two,
  contrast authority-resolved and still-unresolved facts.

### V-05 — A reasoned scenario revision needs a focused current readiness decision

Covers: AC-04, R-02

Intent: Reject reusing obsolete readiness when scenario IDs remain stable, or
restarting task design/full rediscovery for a justified coverage revision.

Given:
- Unchanged authority, scope and prerequisites have an initial verification
  revision and ready readiness bound to that revision.
- A discovered coverage gap leads to a reasoned verification revision retaining
  existing IDs and adding the needed authority-justified scenario.
- Both revisions and the old readiness are supplied, not inferred.

When:
- Focused new preflight considers the revised coverage and affected feasibility.

Then:
- Old affected readiness is obsolete even when existing scenario IDs are unchanged.
- Preflight assesses the added/revised obligations and records a current decision
  tied to the new revision; ready requires their feasibility.
- Unchanged relevant facts can be reused without full rediscovery or requirement
  redesign. Non-artifact repository files remain unchanged.

Oracle / boundary:
- Trace explicit revision/source references, reason and changed coverage through
  supplied starting states and expected decisions. Check source recovery rules
  and fixture inputs; actual role-call recovery remains unrun here.

Variants:
- Newly added scenario feasible; its indispensable capability unavailable.

### V-06 — Material fact changes and expected task effects follow different routes

Covers: AC-04, R-02

Intent: Reject indiscriminate staleness after expected edits, stale readiness
reuse after material changes and requirement changes hidden as scenario edits.

Given:
- Ready readiness identifies its brief/scope/scenario revision and relevant facts.
- A subsequent supplied state changes one of the dimensions below.

When:
- The preflight contract determines whether readiness remains applicable or needs
  reconsideration, and identifies the next owner.

Then:
- Expected implementation or report effects alone do not force full rediscovery.
- Material authority/prerequisite/ownership/permission/capability changes require
  reconsideration and a current readiness decision on affected facts.
- Changed requirements return to task design; preflight cannot settle them by
  editing derived scenarios or assuming old authority still applies.
- Inputs preserve the changed facts and non-artifact files; no fixture resets the
  contrast away before its oracle can inspect it.

Oracle / boundary:
- Inspect source applicability/routing rules against explicit before/after fixture
  facts and expected decisions. Distinguish applicability from later behavior proof.

Variants:
- Expected implementation effect; expected report effect; material authority,
  prerequisite, ownership, permission or capability change; requirement change.

### V-07 — Compact guided policy does not weaken exact high-assurance freshness

Covers: AC-02, AC-04, R-02

Intent: Reject applying guided allowances to strict high-assurance identity checks.

Given:
- An explicitly high-assurance package supplies its required identity, policy and
  ownership inputs and a canonical packet path.

When:
- High-assurance preflight compares baseline and final identities around its
  permitted packet write.

Then:
- Exact existing freshness checks remain strict, including separate index and
  worktree identities and attributed pre/post packet status.
- Only the attributed canonical `preflight.md` delta with unchanged non-packet
  identities can support ready; an unexplained mismatch blocks with a route.
- A future test allowance does not waive freshness or required capabilities.

Oracle / boundary:
- Compare the changed source skill/packet contract with existing strict obligations;
  audit real supplied Git/status/content inputs. Equal short-status text alone
  must not justify accepting changed non-packet bytes.

Variants:
- Packet-only delta; changed non-packet identity despite unchanged short-status text.

### V-08 — Direct requests stay compact while guidance and fixture prompts honor packages

Covers: AC-05

Intent: Reject a universal durable-packet requirement, a packaged inline bypass,
or stale eval expectations contradicting the changed source contract.

Given:
- A small clear bounded conversational request has feasible authority, scope and
  proof, with no supplied durable package.
- A contrasting request supplies an executable package, and preflight-specific
  guide entries and supplied eval prompts describe the supported routes.

When:
- The source contracts and supplied prompt/fixture expectations are compared.

Then:
- The direct request may receive compact inline readiness without forced durable
  artifacts or high-assurance machinery.
- The packaged request requires source-matched verification and canonical durable
  readiness, including for small/routine work; calling it direct cannot bypass that.
- Preflight-specific guides and supplied eval prompts agree with these routes and
  the coverage/capability/context/revision rules above.
- Fixture setup supplies actual prerequisites and negative states needed by its
  expectations and retains safe disposable `EVAL_WORK_ROOT` support.

Oracle / boundary:
- Focused source-contract checks and disposable setup audit compare source,
  preflight-specific guidance, eval prompts and generated inputs. Successful setup
  or wording assertions alone must not be reported as semantic agent compliance.

Variants:
- Small clear direct request; supplied routine executable package.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the brief.
- Preserve stable scenario IDs across reasoned revisions; revised coverage
  supersedes affected readiness/evidence until focused preflight records current ready.
- Implement the smallest source and local test/fixture changes satisfying the brief.
  Concrete test structure, helpers and placement remain implementation choices.
- Preflight resolves exact targeted checks and safe disposable fixture commands.
  After they pass, run the brief's owning package suite from the repository root:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py`.
- Inspect canonical installer selections/guide/shared-file constants in the change;
  synchronize only a required dependency if one changes, as the brief requires.
- Record local source/fixture results separately from unrun agent behavior proof.
  T-001.4 owns broader projection checks; T-005 owns authorized actual role calls.
- If a scenario cannot be exercised at its stated boundary, route the conflict to
  task design/preflight instead of weakening the oracle or expanding this leaf.
