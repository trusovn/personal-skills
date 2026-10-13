# Verification Design: T-005.2 — Exercise preparation and readiness recovery

Source brief: docs/tasks/T-005.2/brief.md
Source brief revision: SHA-256 794247bc2477968d6394ce6bdbb9798ab6c06b96ed4d28ab7383da68ab391c77
Verification revision: 1
Authority: derived from the task brief, docs/project-plan.md sections 8 and 10–11, and docs/tasks/T-005/brief.md evidence rules and P-02
Status: ready

This status applies to the verification design only. Execution readiness,
current installed-copy qualification, fixture locations, and concrete role-call
authorization remain for standalone guided preflight. No role calls or
behavioral qualification are claimed by this file.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-04, V-05 | Actual producer bytes, separate consumers, mandatory packaged preparation and current recovery references. |
| AC-02 | V-02, V-03, V-04, V-06 | Preserve each refusal/direct-edit control as evidence or an explicit gap; distinguish deficient preparation from valid planned proof. |
| AC-03 | V-05, V-06 | Retained IDs/reason, rejection of obsolete readiness before and after recovery, current proof/new decision, and requirement-change routing. |
| AC-04 | V-07 | Raw calls, authorization, identities, observations and unrun boundaries remain auditable. |
| P-01 / INV-001/002/003 | V-01, V-02, V-03, V-04, V-07 | Entry and refusal boundaries use actual files/results; staged inputs are not producer outputs. |
| P-02 / INV-003/005/008 | V-05, V-06, V-07 | Recovery cannot reuse stale approval or convert a changed requirement into a coverage repair. |

Reuse the supplied T-005.1 inventory, receipts and valid existing evidence.
The variants below are a coverage obligation, not a mandate to rerun every
isolated case. Record each retained case's evidence level and any role-boundary
gap. Local checks cannot replace required composed producer-to-consumer proof.

## Verification scenarios

### V-01 — Actual packaged preparation reaches implementation in order

Covers: AC-01; P-01 / INV-001/002/003; INV-CASE-19

Intent: Reject a chain that fabricates intermediate reports, uses different
preparation references, or starts implementation before required preparation.

Given:
- a minimal executable package with clear ACs and supplied authority/setup;
- qualified disposable installed copies and separately authorized role calls;
- no staged verification or readiness counted as an observed producer output.

When:
- the installed verification designer produces the package's verification.md;
- a separate preflight invocation reads that output and produces ready readiness;
- a separate implementer invocation reads those exact preparation references
  and submits evidence for the current scenarios.

Then:
- each handoff resolves to the actual preceding producer's bytes and revision;
- ready preflight follows derived verification and precedes implementation;
- the submission identifies current scenario proof rather than planned checks
  or inherited green results presented as new proof;
- a compact documentation package follows the same entry order.

Oracle / boundary:
- trace preserved raw calls, actual package files, consumed references and
  observed entry/submission output across separate invocation boundaries;
- compare the consumed artifact identity with its producer output, not just
  the filename or a staged expected answer.

Variants:
- minimal executable package; compact documentation package.

### V-02 — Invalid verification cannot borrow green evidence or artifact ownership

Covers: AC-02; P-01 / INV-001/002/003

Intent: Reject incomplete or unsupported verification and destructive replacement
of an artifact whose source ownership is not established.

Given:
- the supplied coverage-closure and verification-conflicts controls, with a
  valid same-package design and recognizable invalid artifact contents;
- green evidence for an included AC where another material AC is omitted.

When:
- verification validity and artifact ownership are assessed for each control;
- preflight assesses the corresponding supplied readiness-cases inputs.

Then:
- the omitted AC remains a gap despite other green evidence;
- an unsupported scenario cannot add a requirement, and a weak oracle cannot
  prove the required result;
- missing or foreign verification cannot satisfy packaged readiness;
- missing, malformed, duplicate or foreign Source brief declarations are
  artifact conflicts, with existing verification contents preserved;
- the valid same-package control clears ownership only; coverage and current
  readiness obligations still apply;
- defects route to the appropriate preparation owner without repairing
  requirements or declaring entry ready.

Oracle / boundary:
- compare the supplied brief/authority with scenario coverage and decisive
  observations; inspect readiness/refusal output and artifact bytes before/after;
- a text-presence check alone cannot establish the observed role refusal.

Variants:
- omitted AC; unjustified scenario; weak oracle; missing/foreign verification;
  missing/malformed/duplicate/foreign source declaration; valid controls.

### V-03 — Missing prerequisites differ from task-owned future proof

Covers: AC-02; P-01 / INV-001/002/003; INV-CASE-05/19/20

Intent: Reject readiness that overlooks indispensable prerequisites, and reject
false blocking merely because an authorized future test is not yet written.

Given:
- supplied readiness-cases and inherited scheduler-missing, queue-ready and
  api-overlap controls;
- a valid case whose absent future test is explicitly task-owned and whose
  necessary setup, capability, authority and permissions are available;
- contrasting cases with a missing indispensable fixture/capability, unavailable
  dependency/permission, or ownership overlap.

When:
- readiness is assessed from actual authority, setup, commands and ownership.

Then:
- the valid future-test case may be ready with planned proof; the absent test
  is never reported as executed or passing;
- indispensable unavailable prerequisites block with the concrete gap, next
  owner and smallest recovery action;
- ownership overlap is separated within authority or blocks before implementation;
- task-owned future work is not confused with an unavailable decisive boundary.

Oracle / boundary:
- inspect actual fixture/tool/permission/ownership facts and readiness output;
  trace each result to the prerequisite that permits or prevents its oracle;
- preserve supplied negative inputs instead of creating prerequisites to turn
  an invalid case green.

Variants:
- valid planned test; missing fixture/capability; dependency; permission;
  resolved dirty ownership versus unresolved overlap.

### V-04 — Compact and integration routes retain their authority boundaries

Covers: AC-01, AC-02; P-01 / INV-001/002/003; INV-CASE-21/22; INT-FLOW-001 I-05 / IFQ-02

Intent: Reject bypassing package preparation by relabeling a request, and reject
expanding executable-leaf permission into parent or sibling authority.

Given:
- supplied preparation-routes, integration-leaf and entry-cases controls;
- an unpackaged small conversational direct edit, a compact documentation
  package, a decomposed parent, blocked-design work and a direct legacy brief;
- an executable integration leaf whose own ACs specify supplied producer
  outputs and consumer boundaries, plus its out-of-scope/unavailable contrasts.

When:
- the preparation roles assess those inputs and the implementer assesses
  entry for the documentation package relabeled as a direct request.

Then:
- the unpackaged direct edit retains compact inline readiness/self-preflight;
- relabeling the supplied documentation package does not bypass verification
  and ready preflight; missing readiness refuses entry without repository edits;
- the composite parent routes to an executable leaf, blocked design to its
  decision owner, and the legacy brief to package normalization;
- integration-leaf scenarios derive only that leaf's explicit composition ACs;
  mandatory packaged preparation still applies;
- invented sibling requirements/system-wide strategy stay outside authority;
  unavailable inputs route to their owner, and unresolved expected results to
  task design/decision owner without fabricated reports or readiness.

Oracle / boundary:
- inspect scope/entry outputs against actual brief kinds, status and supplied
  authority; compare refused-input contents before/after;
- for the allowed leaf, trace scenarios to its explicit ACs and stated consumer
  boundary rather than treating any composition request as allowed.

Variants:
- each listed direct/package/refusal control; allowed integration leaf versus
  composite parent, sibling/system scope, unavailable input or unresolved oracle.

### V-05 — Recovery preserves IDs and rejects obsolete readiness twice

Covers: AC-01, AC-03; P-02 / INV-003/005/008; INV-CASE-23; CCR-07; REV-01; INT-FLOW-001 I-04

Intent: Reject revision recovery that discards history, skips focused readiness,
or lets later passing proof rescue obsolete readiness.

Given:
- unchanged task authority, an original verification/readiness chain and a
  material coverage gap, using supplied coverage-revision/revision-recovery inputs;
- preserved original artifacts and IDs, with only an authorized coverage repair;
- authorized separate calls for the affected preparation, proof and decision roles.

When:
- the designer records the coverage reason and revises verification while
  retaining existing scenario IDs and adding the missing justified coverage;
- affected old readiness is offered before focused recovery;
- focused preflight produces readiness for the current revision, followed by
  current revised proof and a separate new decision consuming current evidence;
- old readiness is substituted again after that recovered proof exists.

Then:
- retained IDs and the revision reason survive every affected handoff;
- affected obsolete readiness/evidence is superseded and prior artifacts remain
  available as history;
- old readiness is rejected both before and after recovery for its obsolete
  revision, even when later proof is green;
- current readiness precedes current revised proof and the separate new decision;
- decision-relevant preparation references, revisions and context reach the
  separate decision consumer; missing proof routes to its owner;
- if the revised oracle needs an unavailable indispensable capability, recovery
  remains blocked with reason/owner instead of becoming ready.

Oracle / boundary:
- trace actual revised design, focused preflight, submission, independent
  evidence and decision bytes through preserved separate calls in order;
- use the old-readiness substitution as the wrong-ready contrast and inspect
  the rejection reason, not merely a non-success status;
- accept staged revision inputs as history only, never as actual recovery outputs.

Variants:
- feasible focused recovery; indispensable capability unavailable;
  old readiness reintroduced after current proof.

### V-06 — Requirement changes and material staleness retain distinct owners

Covers: AC-02, AC-03; P-02 / INV-003/005/008; INV-CASE-24; CCR-07; REV-01

Intent: Reject changing requirements through scenario editing, treating expected
report effects as stale approval, or treating equal Git status text as freshness.

Given:
- supplied changed-requirement, revision-recovery transition and freshness-change
  controls, preserved as alternative before/after inputs;
- contrasts for unchanged-authority coverage repair, expected authorized report
  effects, and material authority/dependency/ownership/permission/capability changes;
- a freshness control with unchanged short status but changed non-artifact bytes
  and user-owned index/worktree state.

When:
- the appropriate preparation/entry role assesses each changed state against
  its prior authority and readiness boundary.

Then:
- changed required behavior returns to task design/decision owner rather than
  being settled through a verification revision;
- a coverage repair under unchanged authority takes focused preflight;
- expected authorized report effects alone do not restart task design or force
  broad rediscovery;
- material fact changes force readiness reconsideration with the actual reason
  and owner, rather than silently reusing approval;
- the high-assurance freshness control rejects changed non-artifact identities
  despite identical short status, preserving user work and baseline evidence.

Oracle / boundary:
- compare the authority/result required before and after, the readiness facts,
  actual file/index/worktree identities and observed routing;
- the wrong-authority contrast must reject for the authority change, not for
  unrelated broken setup; transition inputs are not applied or reset.

Variants:
- changed requirements; coverage-only revision; expected effects;
  material prerequisite/ownership/permission/capability changes; equal-status
  changed-byte freshness control.

### V-07 — Evidence records expose both observed calls and unrun boundaries

Covers: AC-04; P-01 / INV-001/002/003; P-02 / INV-003/005/008

Intent: Reject promoting staged readiness, structural checks, expected verdicts
or an unauthorized/unavailable call into observed behavioral success.

Given:
- T-005.1 supplied inventory/receipts and every case claimed by this leaf;
- concrete role-call authorization if available, or an unresolved/unapproved
  method, budget, permission or capability;
- qualification calls restricted to disposable installed copies and matching
  sibling helpers, without refreshing the active installation.

When:
- the leaf records results and retained evidence for its attempted and unrun cases.

Then:
- each claim retains authority/context, starting Git/filesystem state, applicable
  good/wrong implementation and test inputs, setup/probes, expected oracle,
  observed result, output identity and next owner;
- installed identities include source revision, full managed-projection
  comparison and matching canonical check, rechecked before calls;
- raw producer output is preserved before grading; consumer input references
  resolve to that output; setup answers/oracles stay outside reviewer inputs;
- concrete permissions, call identities and limits remain visible; observations
  use pass/fail/blocked/unchecked separately from expected fixture verdicts;
- unapproved/unavailable calls have reproducible setup and explicit unrun
  reason/owner; unrun required boundaries keep behavioral qualification incomplete;
- failures, unfinished rows and stops remain visible; protected authority,
  history, source policy and active installations stay unchanged.

Oracle / boundary:
- audit results against raw calls, artifact bytes, permission records,
  qualification receipts and before/after protected-state evidence;
- local structural/runtime results and staged input history remain distinguishable
  from actual role compliance; a fingerprint alone cannot prove the full projection.

Variants:
- observed authorized call; unapproved call; unavailable decisive capability;
  inherited local/staged evidence with an unrun role boundary.

## Implementation handoff

- Treat this file as derived guidance, not a replacement for the brief.
- Standalone guided preflight must resolve execution method, isolated workspaces,
  raw-output capture, current qualification and the concrete authorization
  envelope. This design does not authorize role calls or a larger campaign.
- Preserve stable scenario IDs across a reasoned coverage revision. A revision
  supersedes affected readiness/evidence until focused preflight is ready for it.
- Reuse existing controls and evidence; add only missing task-local adapters.
  Concrete test structure, helpers and file placement remain implementation
  choices within the brief's scope. No new shared runner or policy fix is owned here.
- Use focused local staging/probes first. Renew the brief's named local owner
  checks sequentially only where affected evidence needs renewal. Discovery owns
  any justified changed-owner aggregate; acceptance consumes it separately.
- If an oracle cannot be exercised, route capability uncertainty to preflight
  and unresolved expected behavior to task design. Keep explicit gaps rather
  than weakening the oracle. Do not invent sibling or parent-level closure.
- The leaf's required fresh discovery and separate acceptance follow implementation;
  this artifact neither performs those reviews nor approves correctness.
