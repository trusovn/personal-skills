# Verification Design: T-002.3 — Safe input revision

Protect owner authority, coherent publication, evidence freshness and the shared
correction allowance at the public controller boundary.

## Source and revision

Source brief: brief.md
Source brief revision: 1
Verification revision: 1
Authority: derived from the brief, parent P-01..06 and plan IF-001/ART-001/002/FLOW-003
Status: ready

Ready describes this design, not implementation or execution readiness.

## Testing approach and shared setup

Use disposable Git repositories and real run files with the existing controller
initialization/reservation fixtures. Compare file bytes on refusal, reload the
controller between requests, and inspect the persisted authority and history.
Use controlled faults at actual durable publication boundaries; do not replace
revision decisions or filesystem persistence with doubles. Reuse the existing
terminal/readiness fixture: direct writes represent future T-003/004/005
admission, and prove neither actual admission nor actor/model provenance.

## Coverage summary

| Promise | AC / risk | Cases |
|---|---|---|
| Explicit authority, mandatory policy, version and safe boundary | AC-01/03, R1 | V-01, V-02 |
| Clear eligibility, retain historical contents/count | AC-01/02, R2 | V-01, V-03 |
| Coherent interrupted publication and idempotent replay | AC-03, R3 | V-04 |
| Composed controller lifecycle and no bypass/completion | AC-04, R1/R2/R3 | V-05 |
| Callable successor contract and truthful evidence | AC-05 | V-06 |

## Verification scenarios

### V-01 — Authorized idle revision changes authority once

Given an initialized noncompleted idle task, request explicit changed brief,
verification, scope/checks or policy with owner identity, response provenance and
a decision bound to the exact requested change and expected version. Admit it
through the public revision operation. Expect a new input identity and one state
version increment, revised valid policy/task projection, retained previous
input/operation/evidence history and correction count. Include policy-only and
document-only changes and a success control for every refusal family.

### V-02 — Unsafe or invalid requests preserve files

From otherwise valid fixtures independently try: missing/unauthorized authority,
acknowledgement-only response, actor prose, mismatched change binding, stale
version, malformed request/policy, mandatory-stage removal, wrong task/run/repo,
reserved/running/unknown ownership and completed task. Expect the applicable
refusal, byte-identical authority/state/history/count and task files. Also hold
the actual controller lock and require a refusal without authoritative writes.

### V-03 — Historical evidence cannot follow revised authority

Seed explicitly current readiness, candidate and passed implementation/check/
collection/acceptance records and referenced files. Revise brief, verification
and policy through the public operation. Expect readiness/candidate/current
references cleared, all old eligibility removed and old record contents intact.
Reload; old readiness and evidence pointers (test-only successor fixture) must
remain stale, and implementation must require newly admitted preflight. Reset
to the actual postrevision state, reserve new preflight, seed its terminal ready
result and show implementation can resume without resetting task corrections.

### V-04 — Interrupted publication and replay remain coherent

Interrupt before immutable content publication, after content publication but
before the ledger replacement, and after ledger publication before the caller
receives success. Read/reload at each checkpoint. Expect coherent old or new
identity/version, or an explicit conservative stop; never mixed eligible
identities. Retry the exact original revision, including its original version:
only one revision commits, old history/count persist. Changed payload with the
same revision key is refused. Retrying a historical committed revision after a
later revision must never restore its authority or readiness.

### V-05 — Public composed journey preserves controller guards

Initialize frozen inputs; reserve preflight; refuse implementation before valid
terminal readiness; seed readiness; reserve cycle-zero implementation. Reserve
three corrections spanning check failure, review findings and environment
repair, reloading and replaying requests. Repair requires preflight again.
Seed terminality, revise after the third correction and require fresh preflight;
then a fourth correction remains refused, with count/history/files preserved.
Exercise stale evidence at successor stage reservations after revision. Public
run-next, inspect, revise-flow and generic ledger mutation must not skip required
stages or produce completion while successor evidence is missing. Direct setup
of terminality/readiness/check/review records is explicitly test-only.

### V-06 — Successor contract matches actual public surfaces

Inspect the final parent controller-contract.md against library/CLI requests,
validators and actual test results. Include revision payload/authority binding,
identity/byte conventions, safe boundaries, replay/count/history rules, refusals,
required re-preflight after repair, and T-003/004/005 admission/completion seams.
Keep structural validation separate from behavioral evidence. State unrun
sbx/model proof and no first useful proof completion.

## Implementation handoff

Reuse existing owning tests and fixtures; tests can group variants in tables.
Run focused revision/composition tests then owning controller/state modules.
Independent discovery owns the aggregate gate specified in the brief. No live
checks, installation changes or plan edits. Every case remains owed until its
execution evidence or explicit limitation is recorded by its owning stage.
