# Verification Design: W2.1 — Capture artifacts and project snapshots

Source brief: docs/tasks/W2.1/brief.md
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02 | Proves exact-byte recovery, stable logical roles, reuse, and path exclusion. |
| AC-02 | V-03 | Covers every required representational-noise and relocation case. |
| AC-03 | V-04 | Covers content/ref, role, list-order, and omitted/null distinctions. |
| AC-04 | V-05 | Proves validation and real W1 namespace persistence/reuse. |
| AC-05 | V-06, V-07 | Separates capture failures from descriptor/manifest/store failures and proves no false snapshot. |
| AC-06 | V-08 | Provides the scoped-file, standard-library, and no-later-record boundary. |
| Finite risk: explicit-manifest identity | V-03, V-04 | Stable equivalents and each identity-changing dimension are observed through the public constructor. |
| Finite risk: canonical distinctions | V-03, V-04 | Key order is normalized while list order and omitted/null remain distinct. |
| Finite risk: failed capture | V-06, V-07 | Every named failure class is paired with absence of a persisted snapshot. |

## Verification scenarios

### V-01 — Exact bytes and logical role survive capture

Covers: AC-01, P-01

Intent: Reject descriptors that lose the selected bytes or logical role, or that substitute source-location identity for content identity.

Given:
- explicit artifact bytes and a stable caller-supplied logical role
- a real temporary W1 evidence store

When:
- the artifact is captured through the public helper

Then:
- reading the returned content reference yields the exact supplied bytes
- the descriptor preserves the supplied logical role
- neither the descriptor nor its logical identifiers contains the absolute source path

Oracle / boundary:
- observe the public descriptor and W1 blob readback

Variants:
- bytes supplied directly; caller-selected regular file

### V-02 — Repeated capture reuses content without path leakage

Covers: AC-01

Intent: Reject a helper that keys identical content by filename or absolute location and creates location-specific blobs or descriptors.

Given:
- identical bytes available from different absolute roots or filenames
- the same stable logical role

When:
- both artifacts are captured into the same W1 store

Then:
- both captures resolve to the same content reference
- the recovered bytes and logical role are identical
- no absolute location appears in either result

Oracle / boundary:
- compare public capture results and W1 blob state

Variants:
- none

### V-03 — Equivalent manifests have one canonical snapshot identity

Covers: AC-02, S-07, S-08, S-15

Intent: Reject identities that depend on mapping order, JSON whitespace, temporary repository roots, filenames, or source-file absolute paths.

Given:
- one explicit artifact manifest represented with reordered object keys and insignificant JSON formatting differences
- equivalent artifact bytes and logical roles located under two different absolute roots and source filenames

When:
- a ProjectSnapshot is constructed for each representation

Then:
- every construction has the same ProjectSnapshot ID
- every canonical record is byte-for-byte equivalent

Oracle / boundary:
- compare public constructor outputs before persistence

Variants:
- reordered mapping keys; reformatted JSON input; relocated/renamed source files

### V-04 — Every approved semantic distinction changes identity

Covers: AC-03, S-08, S-16

Intent: Reject identity payloads that omit artifact content, logical role, list order, or the omitted-versus-null distinction.

Given:
- a valid baseline manifest and ProjectSnapshot

When:
- exactly one of the following changes at a time: artifact bytes/content ref, stable logical role, ordered-list position, or an optional field from omitted to explicit null

Then:
- the changed input produces a different ProjectSnapshot ID and canonical record
- reversing an ordered list remains observable
- omitted and explicit null remain distinct unless the public constructor explicitly documents normalization for that field

Oracle / boundary:
- compare public constructor IDs and canonical records for the baseline and each single-dimension variant

Variants:
- changed bytes/ref; changed role; reversed list; omitted versus explicit null

### V-05 — Valid snapshots persist and recreate idempotently

Covers: AC-04, S-05, P-01

Intent: Reject schema-only construction that is not wired to W1's immutable ProjectSnapshot boundary, or that cannot reuse identical records.

Given:
- a valid explicit artifact manifest and a real temporary W1 evidence store

When:
- the snapshot is validated and persisted twice from identical inputs

Then:
- the record validates as schema version 2
- it is stored in the `project_snapshot` namespace
- W1 readback equals the constructed canonical record
- the second write reuses the same immutable record without conflict or duplication

Oracle / boundary:
- observe public validation/persistence results and W1 namespace readback

Variants:
- none

### V-06 — Invalid filesystem inputs do not trigger discovery or a snapshot

Covers: AC-05

Intent: Reject fallback behavior that crawls for a substitute or emits complete-looking evidence when explicit capture fails.

Given:
- an explicit input that is missing or is not a regular file
- a real temporary repository containing other potentially discoverable files

When:
- capture is requested

Then:
- the operation reports failure
- no substitute artifact is selected
- no ProjectSnapshot is written

Oracle / boundary:
- observe the public failure and absence of a new ProjectSnapshot in W1

Variants:
- missing path; directory or other non-file input

### V-07 — Malformed or failed manifests never become false snapshots

Covers: AC-05

Intent: Reject validation or persistence paths that accept ambiguous manifests, unsupported versions, malformed descriptors, or partial store success.

Given:
- a baseline W1 store state

When:
- snapshot construction or persistence receives one named invalid case, or the blob store fails during capture

Then:
- the operation reports failure
- no false ProjectSnapshot record is added or replaces an existing immutable record
- no recursive search for replacement inputs occurs

Oracle / boundary:
- compare W1 ProjectSnapshot namespace state before and after the public operation

Variants:
- malformed artifact descriptor; unsupported schema version; duplicate or ambiguous logical entry; controlled blob-store failure

### V-08 — The leaf remains within its architectural boundary

Covers: AC-06

Intent: Reject an otherwise functional implementation that expands into later records, producers, dependencies, or unrelated files.

Given:
- the completed W2.1 change set

When:
- its changed paths, imports, public schema definitions, and callable behavior are inspected

Then:
- only `scripts/evidence_records.py`, `scripts/execution-evidence.schema.v2.json`, and `tests/test_evidence_records.py` changed for this leaf
- runtime imports are standard-library or accepted W1 modules only
- no TaskRevision, ExecutionAttempt, Association, discovery, parser, skill, CLI, or lifecycle behavior was introduced

Oracle / boundary:
- observe the repository diff, import surface, final schema, and public module surface

Variants:
- none

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the task brief.
- Implement the smallest production and test changes that satisfy the brief and exercise these scenarios.
- Concrete test structure, framework usage, helpers, and file placement remain implementation choices unless already fixed by repository authority.
- If implementation discovery shows that a scenario cannot be exercised at its stated boundary, route the conflict back to task design/preflight rather than silently weakening the oracle.
