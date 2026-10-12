# Verification Design: Q-01 — Review significant changed test assets for maintainability

Source brief: docs/tasks/Q-01/brief.md
Source brief revision: Git blob `be80cdf7c8116ab74d8abdc5f3828de469d2e9c7`
Verification revision: 2
Authority: derived from the task brief and its cited normative sources
Status: ready

Ready describes this verification design. It does not authorize implementation,
establish T-003 ownership clearance, or replace a ready standalone preflight.
The feature map, concept and archived proposal supply context only; their wider
work is not added to Q-01. Existing ART-005, IF-003–006 and INV-004/005/006/008
are compatibility references, with the test-asset extension defined by this brief.

## Owner-approved evidence boundary — 2026-10-12

Revision 2 implements the user's Q-01 scope amendment. Q-01 acceptance requires
inspected instructions, executable fixture facts, distribution evidence and a
complete [Q-01-QUALIFICATION handoff](qualification-handoff.md). Actual role
outputs belong to that later follow-up and are not required for Q-01 acceptance.
V-01–V-09 and all finite-risk cases remain stable. Where a scenario specifies
reviewer behavior below, Q-01 checks the published rule and supplied inputs/oracle;
the follow-up must observe the actual behavior. Do not call these checks proof
that an agent complied. T-005's existing composition scope remains unchanged.
Revision 1 readiness is superseded; obtain focused preflight renewal before
fresh discovery and acceptance under the revised authority.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02, V-03, V-04 | Explicit test-asset scope and significance; consequential defects versus lightweight controls. |
| AC-02 | V-01, V-02, V-03, V-04, V-08 | All named defect classes have review guidance; two distinct runnable defects and non-blocking contrasts supply later detection trials. |
| AC-03 | V-05, V-06 | Authorship follows reviewed assets; corrected bytes need fresh evidence, stable identities and preserved history. |
| AC-04 | V-07, V-08 | Existing verdicts, gate policy, conditional routes, stops, completeness and read-only permissions survive. |
| AC-05 | V-02, V-03, V-04, V-05, V-06 | Real tests-only diffs and probes plus complete follow-up inputs/oracles; actual reviewer outputs remain unrun qualification work. |
| AC-06 | V-09 | Full package/guide projection, independent installed setup, unmanaged preservation and truthful source/run records. |
| R-01 / proportionate detection | V-01, V-02, V-03, V-04 | Duplicated authority, coupled mutable setup/harness, clean assertion edit and valid independent fixtures. |
| R-02 / reviewed-byte provenance | V-05, V-06 | Author versus independent reviewer; report → tests-only correction → next review; unaffected evidence and stale-report substitution. |
| R-03 / ordered obligations | V-07, V-08 | Available/unavailable required gate, affected/unaffected maintainability, applicable/absent registry and authorized trivial exception. |
| R-04 / projection | V-09 | Disposable install and repository disk projection; active sessions unchanged. |

## Evidence boundaries and reuse

Reuse the existing maintainability fixture construction, owning tests and staging
support where appropriate. Preserve the four-production-blocker, genuine-stop,
correction-round, authoring-session and report-path contrasts. Add only missing
test-asset distinctions; scenarios do not require one test function each.
Packaged setup must remain independent of repository-only test helpers.

V-01 uses contract inspection. Fixture execution establishes the defect/control
facts in V-02–06; fresh reviewer output establishes the claimed reviewer
behavior. Keep those evidence types separate. Q-01 discovery corroborates local
contracts, fixture facts and the follow-up handoff. Q-01-QUALIFICATION owns the
fresh role trials, including both defects, clean control, real author self-check,
corrected-byte contrast, unavailable gate and reporting/write boundaries. Later
reviewers receive the changed skill, task authority, Git diff and gate policy,
with expected findings and defect-oracle material withheld. Compare raw outputs
with the held-back oracle afterward; combine compatible cases where appropriate.

## Verification scenarios

### V-01 — The review contract extends to significant test assets

Covers: AC-01, AC-02, R-01

Intent: Reject a token scope addition that leaves the review questions or caller
guidance restricted to production code, or makes every assertion edit mandatory.

Given:
- The changed reviewer contract and only affected scope/routing guides.
- Canonical testing-discipline guidance from the same installation root.

When:
- Inspect the scope, six review questions, guidance reference and caller routing.

Then:
- Tests, evaluations, fixture/setup and harness code are reviewed assets when
  the conditional review applies.
- Significance uses ownership, dependencies, scenario authority, isolation,
  oracle structure or harness behavior; review stays within changed/influenced
  surfaces and necessary immediate neighbors.
- Guidance covers introduced/worsened duplicated scenario authority, fragile
  mutable fixtures, unclear/cross-owner coupling, incidental text/layout
  assertions, harness-internal dependencies and speculative abstraction.
- Size/counts, style, unchanged debt and legitimate separate observation
  boundaries do not alone establish blockers; stable textual contracts remain
  legitimate. Functional conformance remains with discovery/acceptance.

Oracle / boundary:
- Semantic inspection of the changed contract and affected guides against
  AC-01/02, including rejection of the old production-only contract by focused
  checks. This establishes contract coverage, not emitted reviewer behavior.

Variants:
- Each asset category and significance dimension above; no new global threshold.

### V-02 — A green tests-only suite can conceal duplicated scenario authority

Covers: AC-01, AC-02, AC-05, R-01

Intent: Reject acceptance based on unchanged production code or passing tests
when one scenario fact now requires synchronized edits across owners.

Given:
- An executable baseline, tests-only changed bytes, task/scenario authority and
  explicit gate policy; the ordinary submitted suite can pass.
- The changed fixture introduces a second authoritative copy of a scenario
  fact. A held-back probe changes only its intended owner.

When:
- Run the suite and divergence probe against baseline and changed fixtures.
- Check that supplied reviewer inputs exclude the expected verdict and defect
  oracle; actual blind review belongs to Q-01-QUALIFICATION.

Then:
- The baseline has no copy-induced divergence; the changed fixture produces
  observable disagreement for the same scenario after the one-owner change.
- The instructions and held-back oracle require identifying duplicated scenario
  authority as a material blocker
  despite the green ordinary suite, with location, current evidence, concrete
  maintenance consequence and smallest correction direction.

Oracle / boundary:
- Real Git baseline/diff, runnable scenario observations and inspected inputs/oracle.
  Later qualification compares actual raw output with the held-back oracle.
  A missing dependency or
  broken setup is not the intended divergence and cannot satisfy this case.

Variants:
- None; legitimate independent fixtures are the contrast in V-04.

### V-03 — Coupled mutable setup or harness behavior breaks isolation

Covers: AC-01, AC-02, AC-05, R-01

Intent: Reject review that misses a second consequential defect because the
normal execution order happens to hide shared state or harness coupling.

Given:
- A runnable baseline and tests-only diff that introduces coupled mutable
  fixture/setup or harness behavior; production bytes remain unchanged.
- Explicit authority and gate policy, a passing ordinary submitted suite, and
  a held-back probe of the affected scenario's isolation or repeatability.

When:
- Execute the probe against baseline and changed fixtures under the relevant
  independent or repeated occurrence that exposes the introduced coupling.
- Check the supplied blind-review inputs and held-back oracle for the later trial.

Then:
- Baseline observations satisfy the scenario contract; changed observations
  violate isolation or repeatability because of the introduced coupling.
- The instructions and oracle require reporting this distinct material defect
  with its location,
  current evidence, maintenance consequence and smallest correction direction.

Oracle / boundary:
- Actual scenario results/state at the fixture's affected execution boundary,
  baseline/change contrast and inspected inputs/oracle. Actual output comparison
  belongs to Q-01-QUALIFICATION.
  Setup failure does not count as evidence of the intended coupling defect.

Variants:
- Isolation or repeatability, whichever demonstrates the supplied defect;
  no redundant second fixture is required for the same invariant.

### V-04 — Clean assertion edits and independent fixtures remain non-blocking

Covers: AC-01, AC-02, AC-05, R-01

Intent: Reject false blockers based on textual assertions, repeated construction
or file size without a concrete introduced maintenance consequence.

Given:
- A clean small assertion change, with explicit policy showing that this edit
  alone does not require conditional maintainability review.
- Legitimate independent fixtures that protect separate observation boundaries,
  and a stable textual assertion that protects an actual textual contract.

When:
- Run the control observations and examine the conditional-review guidance.
- Inspect the supplied requested-review control and held-back expectations;
  actual reviewer output belongs to Q-01-QUALIFICATION.

Then:
- Control observations satisfy their contracts; instructions/oracle require no
  material blocker merely for separate fixtures or the stable text assertion.
- The small edit alone does not introduce mandatory review or a new gate.
- With required proof available and no material regression, instructions/oracle
  require control acceptance without claiming functional task acceptance.

Oracle / boundary:
- Runnable control results, supplied policy, affected routing guidance and
  held-back non-blocking expectations. Later qualification observes the output.

Variants:
- Clean assertion edit; independent fixtures; stable textual contract.

### V-05 — Test-asset authors cannot issue their own independent verdict

Covers: AC-03, AC-05, R-02

Intent: Reject independence determined only from production-byte authorship.

Given:
- A tests-only submission with concrete reviewed scope and a passing available
  gate when required.
- Provenance identifying a session that authored reviewed test, eval or harness
  bytes, and a contrasting fresh reviewer with no such authorship.

When:
- Inspect the author/fresh-session rules and supplied review prompts. Later
  qualification must obtain both outputs with actual authorship records.

Then:
- The published rule requires the author to yield SELF_CHECK_ONLY and no
  independent ACCEPT,
  CHANGES_REQUESTED or INCONCLUSIVE verdict for those assets.
- The published rule permits an independent evidence-supported existing verdict;
  provenance and reviewed output identify the actual test assets.

Oracle / boundary:
- Q-01 inspects published provenance rules and supplied contrasts. The follow-up
  needs session authorship records bound to reviewed bytes and actual role outputs;
  hypothetical prompt authorship cannot satisfy it. Relabeling or loading the
  skill again does not prove independence.

Variants:
- Reviewed test, eval and harness authorship, reusing existing authoring-session
  coverage rather than duplicating its setup.

### V-06 — Tests-only correction invalidates affected evidence and preserves history

Covers: AC-03, AC-05, R-02

Intent: Reject a prior verdict reused after test-only changes, loss of finding
identity, or unnecessary invalidation of demonstrably unaffected scope.

Given:
- A first independent report with stable finding IDs and concrete reviewed
  test-asset identities; prior reports and applicable unaffected evidence exist.
- A tests-only correction that resolves one finding while another survives,
  with probes that distinguish the corrected defect from the surviving defect.

When:
- Run corrected/surviving probes and compare the prior report's recorded
  identities with corrected/unchanged assets; inspect freshness/history rules.
- Supply stale-report substitution and next-report expectations for the follow-up.

Then:
- The correction probe shows resolution; the surviving defect remains observable.
- The published rule says the prior report cannot complete the affected review
  stage for changed bytes;
  unaffected evidence remains usable only while current and applicable.
- The published rule and oracle require the next report to retain every confirmed
  finding ID and its current
  disposition, including the resolved finding. IDs are not recycled, and any
  newly confirmed finding receives an unused ID.
- Prior report bytes remain unchanged; the published rule and oracle require the
  next numbered report to bind to current scope and evidence.

Oracle / boundary:
- Before/after test-asset identities, real correction probes, preserved supplied
  history and inspected freshness rules/oracles. Actual stale-report refusal and
  next-report output belong to Q-01-QUALIFICATION.

Variants:
- Affected corrected scope; demonstrably unaffected scope; stale-report
  substitution. Preserve existing correction-round identity coverage.

### V-07 — Actual effects retain the ordered applicable obligations

Covers: AC-04, R-03

Intent: Reject tests-only shortcuts, invented registry/gate work, or a handoff
that omits outstanding stages after correction.

Given:
- Test-asset correction inputs with explicit gate policy, reviewed scope,
  current/stale evidence and registry applicability, using existing route cases.

When:
- Establish gate availability and compare the changed review/handoff contract
  and focused route evidence with each supplied policy/effect combination.

Then:
- Required gates apply to current bytes. An unavailable required gate without
  valid fresh proof or an authorized exception yields INCONCLUSIVE with truthful
  NOT_AVAILABLE evidence; passing gates still require applicable semantic review.
- Each handoff names the first outstanding stage and full ordered remainder:
  affected applicable gate/maintainability review, applicable registry sync,
  fresh discovery, then separate acceptance. Current applicable evidence can
  keep an unaffected completed stage out of the outstanding remainder.
- A tests-only label waives no affected required review. Explicit trivial-change
  exceptions apply only to their authorized scope; remaining obligations stay.
- Absent registry work and gates not required by policy are not invented.

Oracle / boundary:
- Supplied policy, real available/unavailable gate facts and the emitted or
  published outstanding route, with scope/current-evidence reasons for each
  included or omitted stage. This checks Q-01 handoffs, not execution of sibling
  stages or whole-flow composition.

Variants:
- Required gate available/unavailable; maintainability affected/unaffected;
  registry applicable/absent; tests-only correction with/without an explicit
  trivial exception. Reuse existing route contrasts for unchanged obligations.

### V-08 — Bounded reporting and reviewer permissions survive the extension

Covers: AC-02, AC-04, R-03

Intent: Reject extension of scope that drops existing safeguards, truncates
confirmed findings or converts incomplete review into clean acceptance.

Given:
- Existing four-production-blocker, genuine-stop and report-path cases, and the
  significant test-asset cases above, with authorized bounded scope.

When:
- Check affected contract and fixture evidence against the existing reporting,
  verdict, stop and permission rules; preserve actual output/write checks in the
  follow-up handoff rather than infer them from instruction tests.

Then:
- Existing ACCEPT, CHANGES_REQUESTED and INCONCLUSIVE semantics remain intact.
- Every confirmed material finding within scope is reported with stable ID,
  location, current evidence, maintenance consequence, correction direction
  and disposition; count or verdict sufficiency never ends bounded discovery.
- A genuine stop retains confirmed findings, outstanding coverage, concrete
  reason and next owner; missing required proof cannot become clean ACCEPT.
- Reviewer actions remain read-only apart from the permitted new durable report.
  Invalid external report paths are rejected and prior reports are preserved.
- The review does not execute downstream stages or decide functional acceptance.

Oracle / boundary:
- Existing discriminating fixture facts and owning checks, affected contract
  inspection and fixture Git before-and-after state. Actual role reports and
  write-side-effect observations belong to Q-01-QUALIFICATION. Text checks show
  contract preservation only; record unexercised role behavior in the handoff.

Variants:
- Complete bounded review; genuine permission/capability/budget stop; canonical
  versus external report path. Preserve existing production contrasts.

### V-09 — Canonical installation projects the complete executable package

Covers: AC-06, R-04

Intent: Reject matching SKILL.md alone while executable assets or guide bytes
are stale, missing or dependent on repository-only helpers.

Given:
- Changed source and the canonical development-profile installer, with its
  selected skills, managed guide and shared-script ownership boundaries.
- A disposable target containing unmanaged sentinel files/text and stale managed
  bytes; the repository disk projection is also available for comparison.

When:
- Install into the disposable target and rerun after stale managed content is
  introduced, using existing installer coverage.
- Project source to repository disk through the canonical installer and compare
  the full managed inventory and bytes, excluding only existing transient patterns.
- Execute installed fixture setup and resulting focused defect/control probes
  without access to repository-only test helpers.

Then:
- The complete managed package, including executable eval assets, and profile
  guide match source in both targets; stale managed content is removed.
- Unmanaged files and text outside the installer-managed AGENTS block survive.
- Installed setup supplies runnable task/baseline/change and gate-policy inputs;
  the resulting probes run independently of repository-only helpers.
- Q-01 results record source identity, commands/results and any unrun behavioral
  proof. Disk projection is not claimed as an active-session refresh or load.

Oracle / boundary:
- Real target filesystem inventory/byte comparison, unmanaged sentinel identity,
  installed setup execution and Q-01 result records; no active session reload.

Variants:
- Disposable initial install/reinstall; repository disk projection.

## Implementation handoff

- Treat this file as derived guidance, not a replacement for the brief.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness/evidence until focused preflight is ready.
- Implement the smallest changes satisfying the brief and these observations.
  Concrete test structure, framework, helpers and placement remain implementation
  choices unless fixed by repository authority. No new runner is authorized.
- Preflight must resolve T-003 overlap and freeze the focused selectors. Use the
  brief's sequential targeted maintainability command, affected guide checks and
  installer checks; no whole-repository suite is required.
- Keep actual independent reviewer detection distinct from deterministic setup
  and text checks. Ask before costly/live-networked model evals unless their exact
  class is authorized. Unrun behavioral qualification is an explicit follow-up
  gap, not a Q-01 acceptance blocker under revision 2.
- If a scenario cannot be exercised at its boundary, route to design/preflight
  rather than weaken its oracle. No cross-task composition proof is added here.
- Source identity for this revision is the brief blob above. The original design
  recorded `M AGENTS.md`, `A docs/tasks/Q-01/brief.md` and `M docs/tasks/index.json`
  before its write. That is historical context, not revision 2's status record;
  this amendment does not edit AGENTS.md or the task index.
