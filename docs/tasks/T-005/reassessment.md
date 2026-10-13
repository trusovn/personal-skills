# T-005 remaining-work reassessment — 2026-10-13

This is a planning addendum, not an implementation result or review verdict.
It records the owner's scope revision and the remaining closure contract.
Existing briefs, plans, evidence, review history and structural index stay
unchanged. Read this addendum with the original briefs; it takes precedence
for the remaining T-005 work where their qualification obligations conflict.

## Owner decision and revised outcome

Authority: the owner's 2026-10-13 request to reassess T-005 after partial
T-005.3 progress. The owner builds this flow for personal use, reports using
the skills since T-004 with broadly satisfactory results, accepts the risk of
incomplete qualification, and declines further deep real-oracle work. The
owner also declines a maintainability-review sensitivity evaluation now and
will assess that skill during work elsewhere.

This is the explicit owner scope revision permitted by
[project-plan.md, section 11](../../project-plan.md). No further direction
decision is needed. It changes the assurance required to close T-005; it does
not change the skills' operating contracts or future task review duties.

Revised outcome: preserve the evidence already collected and publish a short
ART-012 closure report that records the owner's accepted risk. Full behavioral
qualification is no longer a completion gate. Personal-use experience is
owner-reported practical confidence, not controlled qualification evidence.

## Progress and remaining disposition

| Child | Existing evidence / state | Remaining disposition |
|---|---|---|
| T-005.1 | [Acceptance](../T-005.1/reviews/acceptance-01.md) is ACCEPT for fixture/setup work, including corrected installation-projection and evaluator-isolation evidence. | Retain and cite. Do not repeat setup or qualification receipts for report closure. |
| T-005.2 | [Acceptance](../T-005.2/reviews/acceptance-01.md) is INCONCLUSIVE. Local/artifact evidence and the claim correction were corroborated; decisive role-chain evidence and historical raw records remain missing. | Retain the verdict. Waive further role qualification and historical recovery as T-005 closure gates; do not relabel the task ACCEPT. |
| T-005.3 | [Results](../T-005.3/results.md) retain 24 fixture snapshots and local probes. [Discovery-01](../T-005.3/reviews/discovery-01.md) corroborates local claims and 53 owner tests; coverage is partial and composed fixture calls remain unrun. No leaf acceptance report is present. | Stop the qualification campaign here. Consume the existing discovery evidence in the final report; no separate acceptance of the old full-qualification contract is needed for revised closure. |
| T-005.4 | Only a brief is present. The [.3 deferral handoff](../T-005.3/evidence/deferral-gap.md) explicitly contains no actual approved deferral. | Waive this qualification child. Do not create a synthetic acceptance, known-issue record or later-preflight replay. |
| T-005.5 | Only a brief is present; it proposes actual correction chains, conditional-stage matrices, finding continuity and aggregate-count proof. | Waive this qualification child. Do not build additional fixtures, oracles or a correction campaign. |
| T-005.6 | Only a brief is present; ART-012 has not been published by this reassessment. | Keep one documentation-only closure task, narrowed below. |

The recorded states above are observations of existing reports, not fresh
acceptance decisions. Prior blocked/unchecked rows retain their original
evidence status. Their new completion-gate disposition is **waived by owner**,
not pass. No runtime status, tracker or dependency advancement is performed.

## Coverage delta

| Parent requirement | Revised closure treatment |
|---|---|
| P-01: Fixtures and qualified installed copies | Cite .1's accepted setup evidence as a point-in-time result. Do not claim that it qualifies every later call or today's active installation. |
| P-02: Preparation and revision recovery | Cite .2's local/artifact evidence and INCONCLUSIVE verdict; waive additional role-chain and raw-history recovery proof. |
| P-03: Independent contextual discovery/decision | Cite .3's corroborated local contrasts; waive composed fixture decisions, prompt behavior and the remaining runtime matrix. |
| P-04: Deferral recorded and consumed by later preflight | Explicitly unproved; waive .4. No actual deferral is inferred from staged history. |
| P-05: Conditional routes, IDs, rows and stops | Retain existing policy/local evidence by reference; waive .5's composed matrix and maintainability blocker-detection qualification. |
| P-06: Correction chain and aggregate ownership | Explicitly unproved at the composed qualification boundary; waive the new .5 campaign. |
| P-07: ART-012 report with truthful evidence limits | Retain as the only remaining deliverable, using the compact contract below. |

These waivers include the additional exporter-resume, ledger-cardinality,
workflow-tamper/replay and process-cleanup probes listed as unrun in .3.
Preserve their case IDs and limits by linking the existing ledger/report;
do not reconstruct or re-grade every inherited row for closure. Outstanding
qualification-related dependency dispositions cited by prior reports do not
require a separate acceptance campaign for this reduced documentation outcome.
This does not retroactively accept those dependencies or release other work.

## Maintainability-review risk

The owner reports that `task-maintainability-review` has always returned OK
in actual use. That may reflect the work reviewed; it does not establish either
a defect in the skill or its ability to detect a material regression. The
unproved property is sensitivity to genuine maintainability problems, including
complete reporting of multiple blockers and finding continuity after correction.

Keep that limitation in ART-012 as an accepted personal-use risk. There is no
seeded-defect benchmark or source repair in the remaining scope. A concrete miss
during later work can justify a focused task then; no follow-up is required now.
Routine applicable independent maintainability review on future implementation
changes remains part of the flow. This reassessment changes neither that skill
nor any persistent instruction.

## T-005.6 contract delta — publish personal-use closure

Status: `ready` (design only; preparation remains required).
Task kind: `executable`. Profile: guided.

This section replaces .6's outcome, dependency gate, execution sizing,
verification obligations and acceptance criteria. Its existing repository,
allowed paths, read-only history, exclusions and separate-review boundaries
remain applicable.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 10 tool calls / 25 minutes / 35k context
```

- Execution sizing: `default@1`; 10 estimated implementation calls; 25 minutes;
  confidence medium; intended `standard / medium`; result `fits`; no triggered
  limits or decomposition override. One report owner avoids duplicate summaries.
- Dependencies: the existing .1 acceptance, .2 results/acceptance and .3
  results/discovery, plus this owner scope revision. Completed .4/.5 outputs,
  new fixture calls and an ACCEPT under .2/.3's original contracts are not needed.
- Direction trace: preserve FLOW-005's ART-012 evidence report and INV-010's
  truthful claims. The owner can see what supports personal use and what remains
  unproved. Why now: useful evidence exists and the owner has ended the additional
  qualification campaign. New direction decisions required: None.
- Output: `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md`,
  beside the unchanged dated proposal, plus `docs/tasks/T-005.6/results.md`.
  Keep the existing report filename; state the reduced assurance in its title/text.
- Readiness route: standalone guided preflight after derived verification,
  limited to report-path ownership and availability of the cited evidence.
- Verification-design recommendation: inline reasoning; the decisive oracle is
  agreement between report claims and their cited sources. Still create compact
  `.6/verification.md` derived from its brief **and this addendum**, then ready
  `.6/preflight.md` before implementation. Do not inherit waived scenarios.

Acceptance criteria:

- **AC-01:** The report accounts for P-01–P-07 and all six child dispositions,
  links the existing evidence/ledgers, and distinguishes local/runtime evidence,
  actual review reports, staged fixture history and owner-reported practical use.
- **AC-02:** The report records the owner scope revision, accepted unrun gaps,
  maintainability sensitivity risk and any cited installation evidence limits.
  It states that personal-use closure does not establish full behavioral
  qualification. Prior ACCEPT/INCONCLUSIVE/partial records remain unchanged.
- **AC-03:** Both output documents agree on the reduced closure outcome.
  Existing plans, briefs, reports, evidence, source skills, installation and
  structural index remain unchanged. No fabricated role result, deferral,
  qualification pass or automatic release is introduced.

Verification: read the cited sources, check report links and the claims above,
then run `git diff --check` and inspect the changed paths. No source behavior
changes, so no code suite, renewed installation receipt, archive replay,
controlled-fault harness, live check or model qualification eval is required.
Discovery owns the report corroboration; acceptance consumes that evidence.
No broader aggregate is justified for this documentation-only change.

Expected contract impact: materialize planned ART-012 with a reduced assurance
claim; preserve IF-008/INV-010. No reusable runtime or ownership contract change,
registry stage or installer update is needed.

Next: compact derived verification → standalone guided preflight → implement
the closure report. Immediately after implementation or correction and any
applicable conditional stages, hand the completed documents to fresh independent
`task-review-discovery`, then its report to a separate `task-acceptance-review`
decision. Those calls judge documentation conformance to this revised scope;
they do not run the waived fixture qualification campaign. No maintainability
stage applies while only documentation changes.

Stop for user-work overlap, unsafe permissions or scope expansion. If a cited
source cannot support a claim, narrow the claim or record the limit; do not
restart the qualification campaign. After .6's revised documentation contract
is accepted, the coordinator may close T-005 as **personal-use scope complete;
full behavioral qualification incomplete, risk accepted by owner**.
