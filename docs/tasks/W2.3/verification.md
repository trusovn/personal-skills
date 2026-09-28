# Verification Design: W2.3 — Complete attempt and association records

Source brief: docs/tasks/W2.3/brief.md
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02 | Covers both valid task modes, both invalid cardinalities, and distinct snapshot roles. |
| AC-02 | V-03 | Covers section placement, presence/absence, empty checks, and sparse values. |
| AC-03 | V-04 | Uses deliberately different values to prove all three profile roles survive. |
| AC-04 | V-05 | Covers all five attempt relations and excludes task parent/child links. |
| AC-05 | V-06 | Covers association variants, immutability, and unchanged attempt bytes. |
| AC-06 | V-07 | Covers fingerprint stability/change dimensions and workflow separation. |
| AC-07 | V-08 | Maps every named invalid family to rejection and absence of false persistence. |
| AC-08 | V-09 | Proves the final top-level model and namespace boundary. |
| AC-09 | V-10 | Exercises the complete task-local four-record graph through real W1 operations. |
| AC-10 | V-11 | Protects predecessors, producer/lifecycle scope, dependencies, and changed files. |
| Finite risk: task/snapshot roles | V-01, V-02 | Valid/invalid input modes and unequal planning/execution snapshots are explicit. |
| Finite risk: optional inline evidence | V-03 | Present/absent/empty and unknown/falsy/N/A values share an exact-record oracle. |
| Finite risk: profile/relation semantics | V-04, V-05 | Profile roles and every approved attempt relation can fail independently. |
| Finite risk: append-only association | V-06 | With/without artifact, factual metadata, conflict, and unchanged attempt are covered. |
| Finite risk: collector semantics | V-07 | Reorder/relocation stability and byte/config changes are paired with workflow-only change. |

## Verification scenarios

### V-01 — Exactly one task input mode is valid

Covers: AC-01

Intent: Reject attempts that accept ambiguous mixed task inputs, require formal tasks, or permit no recoverable task input.

Given:
- valid direct-input and TaskRevision references

When:
- an ExecutionAttempt is constructed with each permitted and forbidden task-input combination

Then:
- direct input alone produces a valid attempt without manufactured formal artifacts
- TaskRevision input alone produces a valid formal attempt
- supplying both or neither is rejected

Oracle / boundary:
- observe public constructor/schema validation and absence of a persisted record for rejected cases

Variants:
- direct ref only; TaskRevision ref only; both; neither

### V-02 — Planning and execution snapshots retain independent roles

Covers: AC-01, T-04

Intent: Reject a graph that overwrites the TaskRevision's planning context with the attempt's execution context or collapses the two references.

Given:
- a persisted TaskRevision referring to planning ProjectSnapshot A
- a formal attempt referring to execution ProjectSnapshot B, where A and B differ

When:
- the linked records are constructed and retrieved

Then:
- the TaskRevision still refers to A
- the attempt independently refers to B
- either snapshot role may be absent where its owning record permits absence

Oracle / boundary:
- inspect the linked public records through real W1 readback

Variants:
- equal refs; different refs; optional execution ref absent

### V-03 — Optional evidence stays sparse, inline, and correctly staged

Covers: AC-02, A-06, A-08, A-09, A-10, A-11

Intent: Reject guessed values, lost falsy observations, stage leakage, or standalone models for conditions, telemetry, and checks.

Given:
- valid attempt inputs with distinct PRE-RUN, EXECUTION, and POST-RUN values

When:
- attempts are constructed with each optional section present and absent

Then:
- execution conditions appear only as an optional PRE-RUN object
- telemetry and checks appear only inline under EXECUTION
- absent conditions and telemetry remain absent and valid
- empty checks remain valid
- explicit unknown, zero, false, and `not_applicable` values remain distinguishable where permitted
- no missing observation is guessed or defaulted

Oracle / boundary:
- inspect the exact constructed record and final schema validation result

Variants:
- conditions present/absent; telemetry present/absent; checks present/empty; unknown/zero/false/not_applicable

### V-04 — Recommended, intended, and actual profiles never overwrite one another

Covers: AC-03, T-05, T-06, T-07

Intent: Reject validation or construction that collapses three analytically distinct profile facts.

Given:
- a TaskRevision with planner-recommended profile A
- an attempt with intended execution profile B and trusted actual runtime identity C
- A, B, and C deliberately differ

When:
- the records are constructed, validated, persisted, and retrieved

Then:
- A remains on TaskRevision planning
- B remains in attempt PRE-RUN as the intended launch
- C remains separately in attempt PRE-RUN as trusted actual runtime identity
- none of the three values is copied over another

Oracle / boundary:
- inspect the linked records through real W1 readback

Variants:
- all values different; optional intended profile absent

### V-05 — Attempt relations link but never collapse observations

Covers: AC-04, T-09

Intent: Reject relation handling that merges attempts, loses relation meaning, or moves task decomposition onto attempts.

Given:
- separately identified valid attempts and TaskRevisions with unchanged parent/child data

When:
- each approved attempt relation is recorded from one attempt to another

Then:
- both attempt IDs remain separate and retrievable
- the exact relation meaning and target attempt ID are preserved
- TaskRevision parent/child relationships remain unchanged
- task parent/child relation values are not accepted as attempt-relation types

Oracle / boundary:
- inspect the linked attempt and TaskRevision graph through public records/W1 readback

Variants:
- retry_of; correction_of; continuation_of; profile_replay_of; calibration_of

### V-06 — Association adds immutable evidence beside an unchanged attempt

Covers: AC-05, S-12

Intent: Reject associations that mutate the referenced attempt, lose factual metadata, require an artifact, or permit conflicting replacement.

Given:
- a persisted attempt and its exact pre-association bytes/value

When:
- generic associations are constructed and persisted with each permitted artifact variant, followed by an attempted conflicting write to the same association ID

Then:
- type, attempt ref, producer/provenance, factual outcome/status, and collection time are preserved
- an optional durable artifact ref is preserved when supplied and absence remains valid
- the association is retrievable from the W1 association namespace
- the referenced attempt remains byte-for-byte unchanged
- the conflicting association write is rejected and the original remains unchanged

Oracle / boundary:
- compare W1 association readback and attempt readback before and after the operation

Variants:
- durable artifact present/absent; factual status variants; conflicting same-ID write

### V-07 — Collector fingerprint tracks semantics, not location or workflow

Covers: AC-06, S-13

Intent: Reject fingerprints that are order/path dependent, insensitive to semantic input changes, or aliases for workflow identity.

Given:
- explicit collector-semantic file bytes/config and an unrelated workflow identity

When:
- the fingerprint is computed for equivalent reordered/relocated inputs and for one-at-a-time changes

Then:
- equivalent selected inputs yield the same deterministic fingerprint regardless of ordering or absolute location
- changing any selected file bytes or semantic config changes the fingerprint
- changing workflow identity alone does not change the collector fingerprint
- collector metadata contains schema version 2 and the fingerprint as distinct fields

Oracle / boundary:
- compare public fingerprint-helper output and constructed attempt evidence metadata

Variants:
- reordered inputs; relocated inputs; one file-byte change; one config change; workflow-only change

### V-08 — Invalid records fail before false persistence

Covers: AC-07

Intent: Reject permissive schema or constructor paths that persist malformed or misplaced evidence.

Given:
- a baseline real W1 store state

When:
- attempt or association construction/persistence receives one named invalid family

Then:
- the public operation reports failure
- no false attempt or association record is added
- no valid existing immutable record is replaced

Oracle / boundary:
- compare relevant W1 namespace state before and after the public operation

Variants:
- mixed task input; missing task input; misplaced standalone conditions/telemetry/check/collector model; malformed attempt relation; malformed association ref; unsupported knowledge status; unsupported schema version; invalid nested optional section

### V-09 — The final schema has exactly four first-class record concepts

Covers: AC-08

Intent: Reject a schema-valid implementation that expands nested evidence into unauthorized top-level models or storage namespaces.

Given:
- the completed schema and public persistence surface

When:
- top-level record definitions and W1 namespace use are inspected

Then:
- only ProjectSnapshot, TaskRevision, ExecutionAttempt, and Association are exposed as first-class records
- conditions, telemetry, checks, and collector identity remain nested definitions or fields
- no standalone namespace or first-class persistence API exists for those nested concepts

Oracle / boundary:
- observe the final schema's public model surface and actual W1 namespace operations

Variants:
- none

### V-10 — All four records compose through the real storage boundary

Covers: AC-09

Intent: Reject individually valid constructors that cannot form and retrieve the approved linked graph through W1.

Given:
- explicit artifact bytes/logical roles and a real temporary W1 evidence store

When:
- a ProjectSnapshot and TaskRevision are created or reused, a valid attempt and association are constructed, and attempt/association persistence uses the corresponding W1 operations

Then:
- every record is retrievable with its links intact
- identical immutable project/task inputs are reusable
- persistence uses logical references without caller knowledge of physical storage paths
- no skill import or integration is required

Oracle / boundary:
- traverse the complete linked graph using only the public record and W1 store interfaces

Variants:
- formal TaskRevision input; direct task input where the graph permits it

### V-11 — W2 closes without crossing into W3

Covers: AC-10

Intent: Reject regressions, extra dependencies/files, or lifecycle/producer behavior introduced during record-model completion.

Given:
- accepted W2.1/W2.2 behavior, accepted W1 behavior, the untouched v1 producer, and the completed W2.3 change set

When:
- owning behavioral regressions and the scoped repository diff/public surfaces are inspected

Then:
- all accepted W2 and W1 behaviors remain green
- the existing v1 run-evidence behavior remains green
- only the three W2-owned files changed for this leaf
- runtime dependencies remain standard-library-only apart from accepted local modules
- no run lifecycle, PRE-RUN timing, check execution, recovery, producer, runner adapter, skill/review integration, or synthetic grading behavior was added

Oracle / boundary:
- observe behavioral regression outcomes plus the repository diff, imports, schema, and public module surface

Variants:
- none

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the task brief.
- Implement the smallest production and test changes that satisfy the brief and exercise these scenarios.
- Concrete test structure, framework usage, helpers, and file placement remain implementation choices unless already fixed by repository authority.
- If implementation discovery shows that a scenario cannot be exercised at its stated boundary, route the conflict back to task design/preflight rather than silently weakening the oracle.
