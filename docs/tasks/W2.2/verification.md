# Verification Design: W2.2 — Implement task revisions and planning history

Source brief: docs/tasks/W2.2/brief.md
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | Stable equivalence includes canonical JSON and absolute-path exclusion. |
| AC-02 | V-02 | Each of the six finite semantic dimensions changes independently. |
| AC-03 | V-03 | Covers the complete approved initial planner and estimate set with provenance. |
| AC-04 | V-04 | Sparse inputs and all named non-equivalent values are observed exactly. |
| AC-05 | V-05 | Covers leaf, decomposed parent, child, and unexecuted-parent persistence. |
| AC-06 | V-06 | Invalid values and immutable conflict preserve prior W1 state. |
| AC-07 | V-07 | Protects W2.1 behavior, scope, dependencies, and later-record boundary. |
| Finite risk: revision identity dimensions | V-01, V-02 | Stability and every required single-dimension mutation are paired. |
| Finite risk: no backfill/collapse | V-03, V-04 | Exact supplied data and sparse/knowledge-status distinctions share a record-level oracle. |
| Finite risk: decomposition without execution | V-05 | All three required decomposition states persist without an attempt. |

## Verification scenarios

### V-01 — Equivalent revision inputs remain canonically identical

Covers: AC-01, S-07, S-09, S-15

Intent: Reject revision identity derived from mapping order, JSON whitespace, task-package location, or source path.

Given:
- semantically equivalent TaskRevision inputs with the same stable task ID and artifact refs
- reordered object keys, insignificant JSON formatting differences, and different absolute task-package/source roots

When:
- a TaskRevision is constructed for each representation

Then:
- every result has the same revision ID
- every canonical record is byte-for-byte equivalent
- no absolute task-package or source path participates in the record or ID

Oracle / boundary:
- compare public constructor outputs

Variants:
- key reordering; JSON reformatting; absolute-root relocation

### V-02 — Every semantic revision dimension participates in identity

Covers: AC-02, S-09, S-10

Intent: Reject a brief-only or incomplete identity payload that overlooks one approved source of semantic revision.

Given:
- one valid baseline TaskRevision with a fixed task brief reference

When:
- exactly one approved dimension changes while every other input remains fixed

Then:
- each variant receives a different revision ID
- W1 readback preserves the changed value in the corresponding immutable revision

Oracle / boundary:
- compare public constructor IDs and W1 `task_revision` readback

Variants:
- artifact refs; structured planning context; planner estimates/profile/split facts; decomposition/source-plan relationships; planning ProjectSnapshot ref; identity-bearing producer provenance

### V-03 — Supplied planner facts and provenance survive exactly

Covers: AC-03, P-03, P-05

Intent: Reject partial planning models or validation that overwrites planner predictions, loses provenance, or promotes them to ground truth.

Given:
- a TaskRevision input containing the full approved optional planner set, estimates/profile/split facts, and their supplied provenance

When:
- the revision is constructed, validated, persisted, and reloaded

Then:
- every supplied planner field and estimate is preserved exactly
- producer provenance remains associated with the supplied planning evidence
- no supplied prediction is rewritten as an observed or ground-truth fact

Oracle / boundary:
- inspect the public record and W1 immutable readback

Variants:
- the eight structured context fields; expected calls/duration; confidence; recommended profile/reasoning; split decision

### V-04 — Sparse planning remains sparse and distinctions survive

Covers: AC-04, S-14, S-16, P-04

Intent: Reject defaulting, prose inference, falsy-value loss, or collapse of distinct knowledge states.

Given:
- valid sparse TaskRevision inputs with only explicitly supplied planner values

When:
- revisions are constructed for omitted and explicitly supplied boundary values

Then:
- omitted planner keys remain absent
- explicit null, `unknown`, zero, false, and `not_applicable` remain observably distinct where their field types permit them
- no parser, model, or default manufactures another value

Oracle / boundary:
- inspect exact keys and values in the public canonical records and their validated readback

Variants:
- omitted; explicit null; unknown; zero; false; not_applicable

### V-05 — Decomposition history persists without an attempt

Covers: AC-05, S-11, P-06, P-07

Intent: Reject an execution-selected-only model that loses composite parents or conflates task decomposition with attempt relations.

Given:
- an unsplit leaf revision
- a decomposed parent revision with child links and split/source-plan facts
- a child revision with its parent link
- no ExecutionAttempt for the parent

When:
- all revisions are validated, persisted, and retrieved through W1

Then:
- each stable task ID and relation is preserved in its TaskRevision
- both parent and child records are retrievable
- the parent remains valid and persistable without any attempt record
- the unsplit leaf remains representable without manufactured decomposition links

Oracle / boundary:
- observe the public TaskRevision records and real W1 namespace state

Variants:
- unsplit leaf; decomposed parent; child with parent; parent without attempt

### V-06 — Invalid revisions fail without damaging immutable history

Covers: AC-06

Intent: Reject permissive validation or conflict handling that admits invalid semantics or replaces an existing revision.

Given:
- a real W1 store containing a valid immutable TaskRevision

When:
- construction or persistence receives one invalid case, including a conflicting payload for an existing immutable identity

Then:
- the operation reports failure
- the previously stored revision remains byte-for-byte unchanged
- no invalid revision is persisted

Oracle / boundary:
- compare W1 TaskRevision namespace state before and after the public operation

Variants:
- invalid task ID/ref; malformed relationship; unsupported schema version; unrecognized provenance; unrecognized knowledge status; conflicting immutable write

### V-07 — W2.2 extends only the accepted record surface

Covers: AC-07

Intent: Reject regressions or scope expansion hidden behind correct TaskRevision behavior.

Given:
- accepted W2.1 behavior and the completed W2.2 change set

When:
- W2.1 behavior, changed paths, imports, schema models, and module behavior are inspected

Then:
- every accepted W2.1 behavior remains unchanged and green
- only the three W2-owned files changed for this leaf
- runtime dependencies remain standard-library-only apart from accepted local modules
- no prose parser, inferred backfill, ExecutionAttempt, Association, skill integration, lifecycle, or sizing-policy behavior was added

Oracle / boundary:
- observe the W2.1 behavioral regression results and scoped repository diff/public surfaces

Variants:
- none

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the task brief.
- Implement the smallest production and test changes that satisfy the brief and exercise these scenarios.
- Concrete test structure, framework usage, helpers, and file placement remain implementation choices unless already fixed by repository authority.
- If implementation discovery shows that a scenario cannot be exercised at its stated boundary, route the conflict back to task design/preflight rather than silently weakening the oracle.
