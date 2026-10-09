# Verification Design: T-002.2 — Make acceptance admit discovery evidence and decide

Source brief: docs/tasks/T-002.2/brief.md
Source brief revision: SHA-256 `2913f3e8d0b1fe76bdc6ace2e8a9004cd47fa676701e2de29fe4cc08775bb700`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | Separate calls, persistent authorship provenance, facts versus decisions, missing discovery. |
| AC-02 | V-02, V-03, V-04, V-05, V-06 | Complete current inputs; weak, stale and omitted proof; conditional evidence; guided versus high-assurance contracts. |
| AC-03 | V-03, V-05, V-06, V-07 | Focused evidence-owner requests and bounded reconciliation, without repeated discovery or general maintainability review. |
| AC-04 | V-02, V-03, V-04, V-05, V-07, V-08 | Three verdicts, current aggregate record and complete findings/unfinished rows; no acceptance with required proof missing. |
| AC-05 | V-09, V-10 | Inline/numbered output, immutable history, no advancement or tracker writes, exact tests-only exception. |
| A-01 / INV-004 | V-01 | Independent calls; author loads role; discovery attempts a verdict; acceptance attempts discovery. |
| A-02 / INV-001/005 | V-02, V-03, V-04, V-05, V-08 | Complete/partial and current/stale evidence; omitted AC despite green tests; missing helper; changed index; unfinished ledger. |
| A-03 / INV-005 | V-07 | Suppressed aggregate, clean corrected record and premature aggregate after an omitted row. |
| A-04 / INV-004 | V-10 | Absent authorization, authorized exact test path after fixed verdict, distinct write audit and fresh review of corrected production. |

### Evidence limits

This task changes source instructions, references and supplied eval contracts.
Local assertions can prove that those contracts and fixture expectations agree;
they cannot prove that an agent follows them. Use supplied fixture inputs and
real public/process observations to support evidence examples. Do not label
text, schema or setup checks as successful acceptance-call behavior. Actual
separate-call and write compliance remains the separately authorized T-005
qualification. These scenarios consume T-002.1's interface; they do not qualify
sibling composition or T-002.3's contextual/mixed-condition rubric.

## Verification scenarios

### V-01 — Loading a role does not create independent decision authority

Covers: AC-01, A-01

Intent: Reject combined discovery/decision calls and provenance reset by a
skill switch.

Given:
- Supplied cases distinguish a production-author session, an independent
  discovery call and a third, independent acceptance call.
- The author case includes the production edit before loading acceptance
  (retain eval 6's trigger). Another case supplies no independent discovery.

When:
- Check the role/output contracts and separate-call fixture expectations for
  each attempted review, including discovery attempting a verdict and acceptance
  attempting to perform the missing discovery itself.

Then:
- The author remains `SELF_CHECK_ONLY`, emits no verdict and cannot advance work;
  current bytes route through fresh independent discovery and separate acceptance.
- Discovery supplies facts without verdict authority. Acceptance owns decision
  accountability in its separate call and does not treat suggested severity or
  a discovery self-claim as a decision.
- Missing discovery routes to its owner with the exact gap; acceptance does not
  merge roles. A guided gap does not trigger an orchestrator-packet requirement.

Oracle / boundary:
- Provenance, role permissions and expected output at the human call boundary,
  checked across skill, reference and fixture contracts. Live role compliance is
  an unrun T-005 obligation, not a result of these local checks.

Variants:
- Independent calls; author switches role; discovery tries verdict; acceptance
  tries discovery; guided input lacks discovery.

### V-02 — Complete current evidence can support a clean decision in either profile

Covers: AC-02, AC-04, A-02

Intent: Reject mandatory machine packets for guided review or acceptance based
only on a report's clean label.

Given:
- A clean supplied case retains eval 2's scoped exporter changes, separate
  index/worktree user-state records and decisive public resume/retry observations.
- Its discovery input identifies current authority, scope, verification revision,
  readiness/context, submission, applicable conditional evidence and every
  required/material row, with current observations and the aggregate record.
- Guided input uses the guided contract; high-assurance input supplies its
  existing required identity and packet records.

When:
- Check admission and clean-decision expectations against the supplied evidence,
  rather than only its summary or passing unit tests.

Then:
- Acceptance reconciles each input, row and finding with the reviewed bytes and
  can return `ACCEPT` with `No findings.` when required evidence is decisive.
- Guided review does not demand high-assurance digests or machine results merely
  because a brief is packaged. High-assurance admission retains its own checks.
- The consumed aggregate's command/not-run, owner/stage, reason and current
  evidence remain visible in the decision.

Oracle / boundary:
- Compare the decision contract/expected output with the supplied scope records,
  public observations and complete ledger. A report marked complete or an exit
  code alone is insufficient proof of the clean case.

Variants:
- Guided inputs; high-assurance inputs.

### V-03 — A complete-looking report cannot replace decisive boundary proof

Covers: AC-02, AC-03, AC-04, A-02

Intent: Reject unsupported pass rows and broad reruns as a substitute for an
exact missing-evidence request.

Given:
- A report labels all rows passing, but evidence lacks a required boundary
  observation; no independent confirmed blocker exists in this case.
- Repeated-flow setup retains eval 1's persisted first state change but omits
  the required second public invocation's observation.
- Validator setup supplies a relevant valid instance and a deliberately invalid
  instance targeting the required constraint, but omits decisive validator
  execution/results for one or both.

When:
- Compare each pass claim with authority, supplied inputs, setup and raw evidence.

Then:
- The unsupported row remains blocked/unchecked with its exact missing proof
  and owner, despite green tests, static schema checks or producer self-validation.
- Missing indispensable proof yields `INCONCLUSIVE`, not `ACCEPT`; acceptance
  requests the second occurrence or missing valid/invalid validator evidence
  from discovery/the capability owner.
- Acceptance does not routinely repeat public probes, broad searches or suites
  to repair the report within the decision call.

Oracle / boundary:
- Compare the actual supplied boundary evidence with the authority's oracle and
  expected decision/request. Validator evidence must show both acceptance of the
  valid instance and rejection of the constraint-targeting invalid instance.

Variants:
- Missing second occurrence; absent valid-validator evidence; absent
  invalid-validator evidence; static/producer-only substitutes.

### V-04 — Stale evidence cannot admit changed bytes or lost capability

Covers: AC-02, AC-04, A-02

Intent: Reject old passes, matching short status or report self-claims as proof
that admission is current.

Given:
- Supplied cases retain eval 3's removed indispensable concurrency helper,
  eval 4's changed user-path index blob with unchanged worktree/status text,
  and eval 8's prior passing row against now-changed reviewed bytes.
- A revision case supplies discovery/readiness evidence for an affected older
  verification revision rather than the current one.

When:
- Reconcile current authority/revision, scope and capability records with the
  evidence identities and preserved continuation.

Then:
- None of these cases supports `ACCEPT`. Old row IDs remain, but stale passes
  cannot count as current proof.
- Missing capability or unexplained high-assurance index state yields
  `INCONCLUSIVE` and routes to preflight/prerequisite ownership; acceptance
  neither invents the forbidden helper nor absorbs/resets user work.
- Affected obsolete readiness/evidence routes to focused preflight and current
  evidence ownership. Acceptance does not revise requirements or scenarios.

Oracle / boundary:
- Supplied filesystem/capability observations, separate index/worktree identities,
  revision records and current byte-bound evidence, compared with the expected
  decision and exact next owner. Matching summary text is not the oracle.

Variants:
- Removed helper; index-only change; stale continuation pass; affected old
  verification/readiness revision.

### V-05 — Real AC violations survive extraction and green-test omissions

Covers: AC-02, AC-03, AC-04, A-02

Intent: Reject loss of the existing public/lifecycle/state signals when acceptance
stops executing discovery's probes.

Given:
- Migrated evals 1–5 and 7–9 retain their original public/process inputs and
  observations in discovery evidence supplied to decision expectations.
- An omission case has green submitted tests/scenarios but current decisive
  evidence of a material AC violation absent from their coverage.

When:
- Compare acceptance's admission/decision expectations with each discovery
  finding, raw signal and normative AC, including the omitted violation.

Then:
- Explicit AC violations block and yield `CHANGES_REQUESTED` in these cases
  with authorized bounded correction; green tests and omitted scenarios do not
  waive them. Finding/row IDs and exact correction ownership are retained.
- Acceptance admits the boundary proof without becoming its probe runner.
- Inherited evidence retains repeat/resume/retry, interacting-state/type checks,
  and each process-lifecycle failure and cleanup observation; partial signals
  cannot stand in for unexercised material cases.

Oracle / boundary:
- Fixture public/process inputs and raw observations tied to stable AC/row IDs,
  plus the derived decision expectations. Preserve these material cases:

| Evidence family | Material cases retained |
|---|---|
| Repeated/persisted flow | First state change and required second invocation; public resume and retry. |
| Ledger/state validator | Selected/non-selected state; zero/one/two active owners; latest ordering; exact ready set; stopped parent/running child; boolean revisions; string completed IDs. |
| Workflow | All three inherited independently observable defects and continuation rows. |
| Process lifecycle | Resistant descendant; exited leader with pipe holder; transient visibility; bounded cleanup observations. |

Variants:
- Each inherited evidence family; demonstrated omitted AC despite green tests.

### V-06 — Conditional facts inform admission without a second general review

Covers: AC-02, AC-03

Intent: Reject ignoring applicable conditional evidence or replacing it with
unbounded maintainability/registry rediscovery.

Given:
- Authority identifies applicable maintainability/registry evidence, supplied
  alongside current discovery and submission.
- One case is consistent; another lacks an applicable record; another contains
  a demonstrated mismatch between the required contract and reviewed bytes.

When:
- Check the conditional-input and bounded mismatch expectations.

Then:
- Acceptance consumes the applicable facts and reconciles contradictions.
- Missing/contradictory proof receives a focused request to its owning stage,
  rather than a general second maintainability review or broad archaeology.
- A demonstrated contract mismatch remains actionable; an earlier conditional
  pass cannot erase it. No registry infrastructure or .3 rubric is added here.

Oracle / boundary:
- Compare authority, conditional records and demonstrated byte/contract evidence
  with the exact admission gap or finding and named owner.

Variants:
- Consistent applicable record; missing record; demonstrated contract mismatch.

### V-07 — Acceptance consumes aggregate history without executing it again

Covers: AC-03, AC-04, A-03

Intent: Reject transferred gate ownership, copied stale passes and premature
aggregate evidence after an omitted row.

Given:
- Supplied discovery records include a targeted failure with aggregate suppression,
  a clean corrected report with current regressions/targeted proof followed by
  one justified aggregate, and an aggregate made premature by an omitted row.
- Each has an ordered command history and command/not-run, owner/stage, reason
  and current evidence. The omission has passing and failing targeted variants.

When:
- Compare the decision contract and expected evidence requests with that history.

Then:
- Acceptance records the consumed gate fields and does not repeat its command.
- Suppression after decisive failure is retained; a copied pre-correction pass
  cannot replace the clean corrected discovery record.
- A premature gate does not clear the omitted row. Focused proof returns to
  discovery; after clean targeted evidence, only discovery owns a still-justified
  rerun. A failing omitted row keeps the ordinary aggregate suppressed.
- No gate or command is added. Missing required proof cannot support `ACCEPT`.

Oracle / boundary:
- Ordered discovery command records versus decision expectations and requested
  owners. Distinguish the .2 implementer's local contract suite from the workflow
  aggregate modeled in these records; neither proves live role compliance.

Variants:
- Suppressed after failure; clean correction; late omitted row passes; late
  omitted row fails.

### V-08 — Partial decisions preserve every finding and unfinished row

Covers: AC-04, A-02

Intent: Reject first-finding truncation, renamed rows or treating unlisted work
as clean after a non-accepting decision.

Given:
- A supplied partial ledger contains stable pass/fail/blocked/unchecked rows,
  multiple confirmed finding IDs and concrete missing-proof reasons/owners.
- A continuation supplies the prior ledger plus current evidence.

When:
- Check decision and continuation outputs against the full input ledger.

Then:
- Every stable finding/row remains visible with its current result and evidence
  or incomplete reason and owner, separately from questions/residual risk.
- Verdicts remain exactly `ACCEPT`, `CHANGES_REQUESTED`, `INCONCLUSIVE`;
  `SELF_CHECK_ONLY` remains a non-verdict provenance label.
- No required unverified boundary supports `ACCEPT`. A non-accepting result does
  not imply that omitted areas passed or permit advancement.
- Full contextual and mixed-condition precedence remains T-002.3's work; this
  scenario establishes ledger preservation, not that later rubric.

Oracle / boundary:
- Compare complete input/output ID sets, row states, concrete reasons/owners
  and continuation records. A top-level verdict alone cannot satisfy this case.

Variants:
- Initial partial report; continuation with prior and current evidence.

### V-09 — Decision output preserves numbered history and narrow write scope

Covers: AC-05

Intent: Reject mandatory guided report files, historical overwrite, tracker
writes or automatic advancement.

Given:
- Guided inline inputs and a durable case with occupied acceptance report
  numbers, existing user bytes and trackers are supplied.
- Durable mode supplies its existing required reviewed-state/write records.

When:
- Check output permissions, report references and fixture path/audit expectations.

Then:
- Guided output may remain inline. Durable output uses the next unused
  `reviews/acceptance-NN.md` in the task package and preserves earlier reports.
- Before/after records attribute only the new report during the verdict phase;
  user bytes, trackers and production/tests remain unchanged.
- Even `ACCEPT` records a decision/route without authorizing tracker mutation or
  performing advancement.

Oracle / boundary:
- Output-path and permission contracts plus supplied prior report identities
  and before/after write expectations. Actual agent write compliance is T-005.

Variants:
- Inline guided output; durable output with prior numbers occupied.

### V-10 — Tests-only authorization is a post-verdict exception

Covers: AC-05, A-04

Intent: Reject test writes inferred from task scope, production repair or
same-session acceptance of corrected bytes.

Given:
- Retain eval 10's confirmed repeated-flow finding and owning test trigger.
- Cases distinguish no authorization, authorization without an exact test area,
  authorization before a fixed verdict, and current explicit
  `tests_only_reproducer` authorization naming exactly
  `tests/integration/test_run_next.py` after a fixed `CHANGES_REQUESTED` verdict.
- A follow-up supplies corrected production bytes to that same reviewer session.

When:
- Check the exception reference and fixture expectations for verdict-before-write,
  permitted paths, intended failure signal and subsequent review routing.

Then:
- Without all preconditions, acceptance remains read-only; allowed task paths
  and `review: immediate` are not reproducer permission.
- Authorized mode preserves the fixed verdict, changes only the exact allowed
  test area, and records a contract-reproducing assertion failure rather than a
  setup/import failure. It does not edit production or broaden write ownership.
- Authorization source/path, pre-write status, post-write status and diff effects
  are distinct records compared in the final audit.
- Production correction routes to its authorized owner; corrected bytes need a
  fresh independent reviewer. This session cannot replace its verdict or accept
  those corrected bytes.

Oracle / boundary:
- Exact authorization and ordered verdict/write records, owning-test failure
  observation and before/after path identities in the supplied fixture contract.
  Local checks do not assert that a live reviewer performed these actions.

Variants:
- No authorization; missing exact path; no fixed verdict yet; all preconditions
  satisfied; corrected production offered for same-session acceptance.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Status ready means design complete, not preflight ready or accepted.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios. Concrete test structure, framework usage, helpers
  and file placement remain implementation choices unless authority fixes them.
- Obtain standalone ready preflight first. Confirm completed/reviewed T-002.1's
  evidence interface and resolve targeted selectors and disposable fixture setup
  there; do not create a new generic harness or refresh active installed skills.
- Preserve original eval signals while moving public/process probing expectations
  to discovery inputs and decision expectations to acceptance. Update old schema
  obligations rather than deleting them; fail-first checks must reject combined
  ownership and missing decisive validator evidence.
- After focused local checks pass, the .2 implementer runs the brief's owning
  gate from repository root:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py`.
  No broader suite or live eval is authorized by this design.
- Inspect installer constants and synchronize only the affected stage entries
  required by the brief; no selection/helper change is expected. Full guidance
  composition and installed projection remain T-002.4's work.
- Record local structural results, real fixture observations and unrun actual-call
  checks separately. Independent review corroborates a distinct admission trace;
  do not present source assertions as behavioral qualification.
- If implementation discovery cannot exercise a scenario at its stated boundary,
  route the conflict to task design/preflight rather than weaken the oracle.
- After implementation or correction, follow applicable conditional stages and
  hand completed bytes to fresh independent acceptance review; end the
  implementation invocation. Actual role qualification remains T-005.
