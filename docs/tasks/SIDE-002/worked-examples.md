# SIDE-002 illustrative source-guided worked outputs

These pairs are manually authored examples under the changed source instructions.
They are not executed skill evals, runnable task packages, or evidence that a model
follows the skill. No implementation, observer or hypothetical command was run.
Paths inside an example refer to its isolated fixture repository. The embedded
brief and verification texts show separate artifact contents; they do not replace
existing tasks. Sizing below is an illustrative implementation estimate, not a
change to policy or a claimed execution measurement.

## Source authority

- Brief fixtures: [setup_fixture.py](../../../skills/task-implementation-flow/task-brief-designer/evals/files/setup_fixture.py), SHA-256 `e5e2e0e7130b8690d7f86b646e2ec13014e4f97d1f7d84e043ddcc067a13daea`.
- Verification fixtures: [setup_fixture.py](../../../skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py), SHA-256 `139affd0986b2a33a7d7414db02fd4c2dcb2b9f9894275b228c77d1a55b45ac2`.
- Functions `small_explicit`, `finite_risk_matrix`, `sizing_decomposition`,
  `queue_runner` and `ambiguous` supply the comparisons below.

## API-5 — Reject blank display names

### Illustrative `API-5/brief.md`

# Task Brief: API-5 — Reject blank display names

## Outcome

Callers can submit a nonblank display name and receive it. Blank names leave the stored name intact.

## Authority and scope

Authority: verification fixture `small_explicit`, `docs/tasks/API-5/brief.md`.
Scope: this submission behavior only; the fixture supplies no mandated implementation paths.

## Acceptance

**AC-01 — Return an accepted name.** Submitting a nonblank name succeeds and returns it.

**AC-02 — Refuse a blank name without changing storage.**

- Empty and whitespace-only text return `blank_display_name`.
- The stored name remains unchanged.

## Execution

Status: `ready` — brief prepared; prerequisites pending.
Task kind: `executable`.
Next: derive verification, then obtain ready guided preflight.
Workflow: [submission route](../../../skills/README.md#submission-route).

```yaml
agent_tier: standard
reasoning: low
review: immediate
budget: 6 calls / 20 minutes / fixture-local work
```

Sizing: `default@1`; 6 implementation calls / 20 minutes;
confidence medium; fits.

### Illustrative `API-5/verification.md`

# Verification Design: API-5 — Reject blank display names

## Shared setup

Use the named fixture authority. Establish valid prerequisites before each refusal.
Implementation owns fail-first where feasible, targeted cases, then the owning suite.
Fresh independent discovery corroborates the named cases with distinct inputs;
the separate acceptance call consumes that report. Use the shared route for
conditional stages and corrections; broader gates need justified authority.

## Test cases

### V-01 — Nonblank submission succeeds

**Situation:** Stored name is `Old`; input is `Ada`.
**Action:** Submit the name through the name-submission boundary.
**Expected result:** Success returns `Ada`.
**How to check:** Observe the returned value and success decision; do not invent
normalization or persistence semantics for successful submission.

### V-02a / V-02b — Empty and whitespace-only submissions preserve the name

**Situation:** Stored name is `Old`; inputs are respectively empty text and `   `.
**Action:** Submit each input independently.
**Expected result:** `blank_display_name`; storage still contains `Old`.
**How to check:** Read the stored name before and after each refusal and observe
the exact validation error. V-01 rejects an always-refusing implementation.

## Coverage summary

| Promise | AC | Cases |
|---|---|---|
| Accepted input | AC-01 | V-01 |
| Blank refusal and preservation | AC-02 | V-02a, V-02b |

## Source and revision

Source brief: docs/tasks/API-5/brief.md
Source brief revision: illustrative pair revision 1
Verification revision: 1
Authority: derived from the brief and cited fixture authority
Status: ready (illustrative design only)

## EVD-12 — Resume only valid publication state

### Illustrative `EVD-12/brief.md`

# Task Brief: EVD-12 — Resume only valid publication state

## Outcome

Operators resume valid evidence publication without rewriting prior evidence; invalid state is refused before effects.

## Authority and scope

Authority: brief fixture `finite_risk_matrix`, `docs/evidence-plan.md#EVD-12`.
Allowed implementation: `src/evidence_flow.py`, `tests/test_evidence_flow.py`. No shared harness, dependency, unrelated corruption, fuzz, platform or performance work.

## Acceptance

**AC-01 — Validate every persisted evidence family before effects.**

- Validate policy, manifest, attempt record, structured result and closure.
- Reject tampering in each family before filesystem mutation or subprocess start.

**AC-02 — Continue the legal publication sequence.**

- Order: execution, verification, decision, ledger.
- Legal prefixes: none; execution; execution + verification;
  execution + verification + decision; execution + verification + decision + ledger.
- Reuse existing bytes and publish only the next missing stage.

**AC-03 — Refuse contradictory orphan states before effects.**

- Structured result without an attempt record.
- Closure without a decision publication.
- Ledger without a verification publication.
- Manifest referencing a missing attempt record.

## Evidence boundary

Verification-design recommendation: separate — finite publication and refusal rules.
Standalone guided preflight must resolve the unconfirmed deterministic observer
for pre-write and pre-process rejection. Stop if that capability requires a new
shared harness or authority decision. EVD-12's evidence paragraph governs
implementation/review separation and final-reviewer aggregate ownership.

## Execution

Status: `ready` — brief prepared; prerequisites pending.
Task kind: `executable`.
Next: derive verification, then obtain ready guided preflight.
Workflow: [submission route](../../../skills/README.md#submission-route).

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 12 calls / 35 minutes / fixture-local work
```

Sizing: `default@1`; 12 implementation calls / 35 minutes;
confidence medium; fits.

### Illustrative `EVD-12/verification.md`

# Verification Design: EVD-12 — Resume only valid publication state

## Shared setup

Use the named fixture authority. Establish valid prerequisites before each refusal.
Implementation owns fail-first where feasible, targeted cases, then the owning suite.
Fresh independent discovery corroborates the named cases with distinct inputs;
the separate acceptance call consumes that report. Use the shared route for
conditional stages and corrections; broader gates need justified authority.

## Test cases

All cases use public `evidence-runner resume --state <path>`. The observer must
be confirmed by preflight before claiming pre-write and pre-process evidence.
Capture file bytes and process starts across the operation; exit status alone
cannot prove absence of side effects. Implementation owns fail-first and targeted
public-command evidence. EVD-12 assigns the aggregate after corrections to the
fresh final reviewer, after targeted evidence is green; correction implementers
do not run it while targeted checks are red.

### V-01a–e — Each tampered family is refused

**Situation:** Independently tamper policy (a), manifest (b), attempt record (c),
structured result (d), or closure (e), with all other prerequisites valid.
**Action:** Resume each state.
**Expected result:** Refusal before file mutation or subprocess start.
**How to check:** Compare complete pre/post file snapshots and the deterministic
process-start observation. Establish that the intended family guard is reached.
Fresh discovery uses distinct family tampering, not implementation's exact inputs.

### V-02a–e — Every legal prefix reuses bytes and advances one stage

| Case | Starting publications | Result |
|---|---|---|
| V-02a | none | execution only |
| V-02b | execution | add verification only |
| V-02c | execution + verification | add decision only |
| V-02d | execution + verification + decision | add ledger only |
| V-02e | execution + verification + decision + ledger | reuse complete bytes; no missing stage to publish |

**Action:** Invoke resume for each valid starting state. For lifecycle proof,
also invoke from none, observe execution persisted, then invoke again from that
actual state and observe verification only.
**Expected result:** Existing bytes remain identical; each partial prefix adds
only its next stage. The full prefix adds nothing.
**How to check:** Read durable publications after each public invocation and
compare prior bytes. These are success controls for V-01 and V-03. Fresh discovery
uses a separate valid recovery history and verifies reload across invocations.

### V-03a–d — Each named orphan is refused

**Situation:** Independently seed structured result without attempt record (a),
closure without decision (b), ledger without verification (c), and a manifest
referencing a missing attempt record (d). Keep unrelated guards satisfied.
**Action:** Resume each contradictory state.
**Expected result:** Refusal before filesystem mutation or subprocess start.
**How to check:** Use the same real observer as V-01 with pre/post byte snapshots.
Fresh discovery independently constructs each orphan, checking the intended
contradiction rather than passing via malformed setup.

## Coverage summary

| Promise | AC | Cases |
|---|---|---|
| Family validation | AC-01 | V-01a–e |
| Legal reuse and next-stage publication | AC-02 | V-02a–e |
| Contradictory refusal | AC-03 | V-03a–d |

## Source and revision

Source brief: docs/tasks/EVD-12/brief.md
Source brief revision: illustrative pair revision 1
Verification revision: 1
Authority: derived from the brief and cited fixture authority
Status: ready (illustrative design only)

## TASK-40 — Illustrative composite `brief.md`

# Task Brief: TASK-40 — Import a local bundle

## Outcome

Users import a valid local bundle once and retrieve it unchanged. Invalid input
has no persisted side effect. Authority: brief fixture `sizing_decomposition`,
`docs/project-plan.md#TASK-40`; stable refs FLOW-40, ART-40, IF-40, INV-40.

## Acceptance and ownership

**AC-01 — Parse and normalize the bundle.** TASK-40.1 owns ART-40 through IF-40.
**AC-02 — Persist without partial effects.** TASK-40.2 owns transactional persistence and INV-40.
**AC-03 — Demonstrate public import.** TASK-40.3 owns public wiring and FLOW-40 integration proof.

| Child | Consumer and owned output | Depends on | Brief |
|---|---|---|---|
| TASK-40.1 | ART-40 / IF-40 for persistence and CLI | none | TASK-40.1/brief.md |
| TASK-40.2 | persisted ART-40 / INV-40 for public import | TASK-40.1 | TASK-40.2/brief.md |
| TASK-40.3 | public FLOW-40 and final integration proof | TASK-40.1, TASK-40.2 | TASK-40.3/brief.md |

## Execution

Status: `decomposed`; Task kind: `composite`. Only prepared dependency-ready
leaves execute. `default@1`: original estimate 24 calls / 65 minutes, standard/
medium, confidence medium; both size limits trigger boundary evaluation.
Stable parse output and transactional persistence allow independent ownership
and proof with a final integration leaf; no shared mutable output owner exists.
Child sizes below fit. No parent launch metadata or implementation permission.

## TASK-40.1 — Normalize the import artifact

### Illustrative `TASK-40.1/brief.md`

# Task Brief: TASK-40.1 — Normalize the import artifact

## Outcome

Persistence and public import consume normalized ART-40 through IF-40.

## Authority and scope

Authority: brief fixture `sizing_decomposition`, `docs/project-plan.md#TASK-40`, parent AC-01.
Scope: parse and normalize one local bundle; persistence and CLI belong to dependent children.

## Acceptance

**AC-01 — Produce the approved normalized artifact.** Parse the local bundle into ART-40 through IF-40.

**AC-02 — Respect the shared boundary.** Keep the artifact consumable by TASK-40.2 and TASK-40.3; publish no destination state.

## Execution

Status: `ready` — brief prepared; prerequisites pending.
Task kind: `executable`.
Next: derive verification, then obtain ready guided preflight.
Workflow: [submission route](../../../skills/README.md#submission-route).

```yaml
agent_tier: standard
reasoning: low
review: immediate
budget: 8 calls / 20 minutes / fixture-local work
```

Sizing: `default@1`; 8 implementation calls / 20 minutes;
confidence medium; fits.

### Illustrative `TASK-40.1/verification.md`

# Verification Design: TASK-40.1 — Normalize the import artifact

## Shared setup

Use the named fixture authority. Establish valid prerequisites before each refusal.
Implementation owns fail-first where feasible, targeted cases, then the owning suite.
Fresh independent discovery corroborates the named cases with distinct inputs;
the separate acceptance call consumes that report. Use the shared route for
conditional stages and corrections; broader gates need justified authority.

## Test cases

### V-01 — Producer output matches the consumer contract

**Situation:** Approved local bundle and IF-40 contract, supplied before readiness.
**Action:** Parse and normalize it.
**Expected result:** ART-40 carries the approved items without loss or alteration.
**How to check:** Compare values against the supplied input and IF-40; independently
review consumer compatibility. No storage or CLI proof is claimed here.

### V-02 — Producer has no destination effect

**Action:** Parse with an existing destination snapshot.
**Expected result:** No persisted import state changes.
**How to check:** Compare destination bytes. Missing IF-40 field/invalid-input
semantics route to the authority owner; verification must not invent them.

## Coverage summary

| Promise | AC | Cases |
|---|---|---|
| Parse / normalize | AC-01 | V-01 |
| Consumer boundary and no persistence | AC-02 | V-01, V-02 |

## Source and revision

Source brief: docs/tasks/TASK-40.1/brief.md
Source brief revision: illustrative pair revision 1
Verification revision: 1
Authority: derived from the brief and cited fixture authority
Status: ready (illustrative design only)

## TASK-40.2 — Persist normalized import atomically

### Illustrative `TASK-40.2/brief.md`

# Task Brief: TASK-40.2 — Persist normalized import atomically

## Outcome

Public import can persist ART-40 transactionally while preserving INV-40.

## Authority and scope

Authority: brief fixture `sizing_decomposition`, `docs/project-plan.md#TASK-40`, parent AC-02. Depends on TASK-40.1 ART-40 / IF-40.
Scope: persistence only; consume approved producer output. TASK-40.3 owns CLI composition.

## Acceptance

**AC-01 — Persist ART-40 transactionally.** Preserve INV-40 from the approved contract.

**AC-02 — Refuse invalid input without partial persistence.** Invalid input leaves destination state unchanged.

## Execution

Status: `ready` — brief prepared; prerequisites pending.
Task kind: `executable`.
Next: derive verification, then obtain ready guided preflight.
Workflow: [submission route](../../../skills/README.md#submission-route).

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 8 calls / 25 minutes / fixture-local work
```

Sizing: `default@1`; 8 implementation calls / 25 minutes;
confidence medium; fits.

### Illustrative `TASK-40.2/verification.md`

# Verification Design: TASK-40.2 — Persist normalized import atomically

## Shared setup

Use the named fixture authority. Establish valid prerequisites before each refusal.
Implementation owns fail-first where feasible, targeted cases, then the owning suite.
Fresh independent discovery corroborates the named cases with distinct inputs;
the separate acceptance call consumes that report. Use the shared route for
conditional stages and corrections; broader gates need justified authority.

## Test cases

### V-01 — Valid producer output is persisted unchanged

**Situation:** Supplied ART-40 and authoritative INV-40; real disposable storage.
**Action:** Persist and read back the artifact.
**Expected result:** Stored values match ART-40 and INV-40 holds.
**How to check:** Read durable storage independently of the write return value.

### V-02 — Invalid input has no persisted effect

**Situation:** Invalid ART-40 according to IF-40, with other prerequisites valid.
**Action:** Attempt persistence.
**Expected result:** Refusal; no partial destination change.
**How to check:** Compare durable pre/post state. V-01 is the success control.
Preflight must confirm the actual IF-40 / INV-40 definitions; this example does
not invent an invalid field or transaction implementation.

## Coverage summary

| Promise | AC | Cases |
|---|---|---|
| Transaction and invariant | AC-01 | V-01 |
| No partial persistence | AC-02 | V-02 |

## Source and revision

Source brief: docs/tasks/TASK-40.2/brief.md
Source brief revision: illustrative pair revision 1
Verification revision: 1
Authority: derived from the brief and cited fixture authority
Status: ready (illustrative design only)

## TASK-40.3 — Prove public bundle import

### Illustrative `TASK-40.3/brief.md`

# Task Brief: TASK-40.3 — Prove public bundle import

## Outcome

Users run `bundle import`, then retrieve the imported bundle unchanged.

## Authority and scope

Authority: brief fixture `sizing_decomposition`, `docs/project-plan.md#TASK-40`, parent AC-03. Depends on both producer children.
Scope: public wiring and FLOW-40 integration proof; do not re-own producer contracts.

## Acceptance

**AC-01 — Import once and retrieve unchanged.** Compose IF-40, ART-40 and persistence through public `bundle import`.

**AC-02 — Preserve destination on invalid input.** The public command leaves no persisted side effect for invalid input.

## Execution

Status: `ready` — brief prepared; prerequisites pending.
Task kind: `executable`.
Next: derive verification, then obtain ready guided preflight.
Workflow: [submission route](../../../skills/README.md#submission-route).

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 8 calls / 20 minutes / fixture-local work
```

Sizing: `default@1`; 8 implementation calls / 20 minutes;
confidence medium; fits.

### Illustrative `TASK-40.3/verification.md`

# Verification Design: TASK-40.3 — Prove public bundle import

## Shared setup

Use the named fixture authority. Establish valid prerequisites before each refusal.
Implementation owns fail-first where feasible, targeted cases, then the owning suite.
Fresh independent discovery corroborates the named cases with distinct inputs;
the separate acceptance call consumes that report. Use the shared route for
conditional stages and corrections; broader gates need justified authority.

## Test cases

### V-01 — Public producer/consumer composition imports once

**Situation:** Prepared TASK-40.1 and TASK-40.2 outputs, approved valid bundle,
real disposable destination storage.
**Action:** Invoke `bundle import`, then retrieve the imported items.
**Expected result:** One imported bundle; names and bytes match the source.
**How to check:** Count imported records and inspect retrieval via the actual
consumer. This is the final FLOW-40 integration proof, not a stubbed producer test.

### V-02 — Public invalid import leaves storage intact

**Situation:** Authority-defined invalid input; valid environment and sentinel state.
**Action:** Invoke `bundle import`.
**Expected result:** Refusal and unchanged destination state.
**How to check:** Compare persisted pre/post records and bytes. V-01 is the control.
Independent discovery repeats both at the public boundary using different approved
input values. No unspecified repeated-import/idempotency policy is added.

## Coverage summary

| Promise | AC | Cases |
|---|---|---|
| FLOW-40 composition | AC-01 | V-01 |
| Public refusal | AC-02 | V-02 |

## Source and revision

Source brief: docs/tasks/TASK-40.3/brief.md
Source brief revision: illustrative pair revision 1
Verification revision: 1
Authority: derived from the brief and cited fixture authority
Status: ready (illustrative design only)

## S3-04 — Continue queue execution

### Illustrative `S3-04/brief.md`

# Task Brief: S3-04 — Continue queue execution

## Outcome

Queue operators call `runner run-next` repeatedly to select remaining ready tasks.

## Authority and scope

Authority: brief fixture `queue_runner`, `docs/stage-3-plan.md#S3-04`.
Scope: public `runner run-next`, `.runner/state.json`, selection and command tests. Preserve existing empty-queue behavior; do not implement unrelated runner features.

## Acceptance

**AC-01 — Select and persist the next ready task.**

- Return its task ID and persist that task as running in `.runner/state.json`.
- Later invocations select remaining ready tasks.

**AC-02 — Preserve excluded state and empty behavior.**

- Never reclaim a running task.
- Preserve existing empty-queue behavior.

## Audit and evidence boundaries

Artifact identity: S3-04, producing stage `task-brief-designer`, example timestamp
2026-11-02T19:10:00Z; primary authority `docs/stage-3-plan.md#S3-04` in the exact
fixture-script revision recorded above. Sizing policy: `default@1`.
Confirmed: command, state path and repeated-selection rules come from that section.
No governing direction or machine schema was supplied; do not invent either.
Provisional: existing empty-queue outcome, exact command, repository baseline,
policy and capability identities require high-assurance preflight confirmation.
Task-local public lifecycle tests may be implemented; the existing static
selection test is not public persistence evidence.
Verification-design recommendation: separate — first/change/next lifecycle.
Detailed AC/evidence and capability disposition belong to verification and preflight.
Use exact freshness and machine/audit obligations from
[high-assurance implementer inputs](../../../skills/task-implementation-flow/bounded-task-implementer/SKILL.md#high-assurance-additions)
and [packet template](../../../skills/task-implementation-flow/task-preflight/references/execution-packet-template.md).
Retain a caller-supplied result schema/path and run policy verbatim when supplied;
their absence must not be replaced by invented paths. Stop for unresolved empty
semantics, authority or packet identity mismatch.

## Execution

Status: `ready_for_preflight` — brief prepared; prerequisites pending.
Task kind: `executable`.
Next: derive verification, then obtain ready high-assurance preflight.
Workflow: [submission route](../../../skills/README.md#submission-route).

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 12 calls / 35 minutes / fixture-local work
```

Sizing: `default@1`; 12 implementation calls / 35 minutes;
confidence medium; fits.

### Illustrative `S3-04/verification.md`

# Verification Design: S3-04 — Continue queue execution

## Shared setup

Use the named fixture authority. Establish valid prerequisites before each refusal.
Implementation owns fail-first where feasible, targeted cases, then the owning suite.
Fresh independent discovery corroborates the named cases with distinct inputs;
the separate acceptance call consumes that report. Use the shared route for
conditional stages and corrections; broader gates need justified authority.

## Test cases

### V-01 — First invocation and reload select different ready tasks

**Situation:** Two ready tasks A then B, and running task R; actual state file.
**Action:** Invoke `runner run-next`; inspect durable state; invoke again in a new
process loading that state.
**Expected result:** First returns A and persists A running. Next returns B and
persists B running; R remains running and is never returned.
**How to check:** Observe public output and reload `.runner/state.json` after each
invocation. Static `select_next` success alone is insufficient. Fresh discovery
uses different task IDs and independently checks the two-process history.

### V-02 — No ready task preserves the existing empty outcome

**Situation:** Only running tasks, then independently an empty queue.
**Action:** Invoke the public command for each.
**Expected result:** Existing empty-queue outcome; no running task reclaimed.
**How to check:** Compare with the documented/characterized baseline and pre/post
state; preflight must establish that baseline before readiness. V-01 supplies a
success control. Search first/only-task assumptions in selection, CLI and tests;
verify any found assumption against this lifecycle instead of widening scope.

### V-03 — Freshness and result handoff remain exact

**Situation:** A high-assurance packet and supplied machine-result contract, if
required by the actual caller.
**Action:** Recalculate packet brief/verification digests, HEAD, post-packet status,
separate dirty index/worktree identities and recorded policy/environment identities.
**Expected result:** Exact agreement before edits; unexplained mismatch routes to
fresh preflight. Required structured result validates against its supplied schema.
**How to check:** Follow the high-assurance implementer packet rules; this example
contains no packet and claims no successful freshness check or machine result.

## Coverage summary

| Promise | AC | Cases |
|---|---|---|
| Persist and continue | AC-01 | V-01 |
| Running exclusion and empty baseline | AC-02 | V-01, V-02 |
| Audit/freshness obligations | Audit addendum | V-03 |

## Source and revision

Source brief: docs/tasks/S3-04/brief.md
Source brief revision: illustrative pair revision 1
Verification revision: 1
Authority: derived from the brief and cited fixture authority
Status: ready (illustrative design only)

## V-05 — Ambiguous retention contrast

Verification fixture `ambiguous` supplies RET-8: bounded storage, but
no approved retention count, deletion set or automatic/confirmed deletion policy.
Source-guided outcome: `needs_brief_revision`; owner: product owner. Ask for the
smallest retention/deletion decision. Leave `verification.md` absent or unchanged
and preserve `existing-marker.txt`. API-5 above has complete expected behavior
without risk rows and permits derived cases; RET-8 lacks expected behavior and
cannot be made ready by inventing a three-backup rule.

## Requirement comparison and consumer map

| Source obligation | Contract home | Detailed proof home |
|---|---|---|
| API success; blank refusal; empty/whitespace; stored name | API-5 AC-01/02 | V-01, V-02a/b |
| Five exact evidence families and tampering | EVD-12 AC-01 | V-01a–e |
| Four publications, all five legal prefixes, byte reuse, next stage | EVD-12 AC-02 | V-02a–e plus first/change/next sequence |
| All four exact orphan states; refusal before both effect types | EVD-12 AC-01/03 | V-01, V-03a–d and real observer |
| Fail-first/targeted implementation, distinct fresh probe, final-reviewer aggregate | Precise EVD-12 evidence authority in brief | Shared verification setup and each case method |
| Observer uncertainty and no shared harness | EVD-12 evidence boundary/scope | Preflight confirms before V-01/03 proof |
| ART-40 / IF-40, INV-40, FLOW-40 and unchanged retrieval | TASK-40 parent AC mapping and child contracts | Each child verification; TASK-40.3 owns final composition |
| Queue public command, persisted running state, later selection | S3-04 AC-01 | V-01 across real reload |
| Empty behavior and never reclaim running | S3-04 AC-02 | V-01/02, baseline confirmed by preflight |
| Exact provenance, provisional knowledge, freshness and supplied machine obligations | S3-04 audit addendum, exact shared rules | V-03, packet-owned identities |

| Consumer | Input location and responsibility |
|---|---|
| Preflight | Each brief authority/scope, evidence uncertainty and execution; matching verification revision/cases. Confirm capabilities and precise scope without fixed risk headings. |
| Implementer | Each titled AC plus derived scenario IDs; map every case before editing, establish task-owned evidence, preserve blocked/unchecked gaps. |
| Discovery | Brief requirements and exact authority plus complete verification cases and producer-attributed implementation evidence; corroborate independently and retain all obligations. |
| Acceptance | Same complete AC/scenario map plus fresh discovery and applicable conditional reports; separate decision, no author self-acceptance. |
| Split coordinator | TASK-40 requirement-to-child map, single output ownership, dependency order and TASK-40.3 closure; parent never executes. |

Shared route links resolve to the shipped profile guide (source skills/README.md). Each executable retains
status/task kind, first preparation action, four launch keys and sizing once.
No R section is needed. Case setup and observation appear only in verification.
Finite value lists in EVD-12 are requirements, not removable test detail.
The TASK-40 source names ART/IF/INV contracts without field definitions; these
examples preserve that limitation explicitly rather than inventing a schema.
They do not certify those hypothetical leaves ready for implementation.
