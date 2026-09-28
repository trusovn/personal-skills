# Task Brief: `W2.1` — Capture artifacts and project snapshots

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 11 tool calls / 35 minutes / 28k context
```

## Execution sizing

- Sizing policy: `default@1`
- Estimated agent calls: `11`
- Estimated implementation duration: `35 minutes`
- Estimate confidence: `medium`
- Policy result: `fits`
- Triggered limits: `none`
- Decomposition override: `none`

The estimate covers implementation-agent discovery, production/schema/test
edits, and targeted verification only. Independent review is excluded.

## Readiness route

`implementer self-preflight`

Confirm the accepted W1 files are present and run
`python3 -m unittest tests/test_evidence_store.py -v` before editing. Stop on a
pre-existing failure rather than absorbing it into W2.1.

## Verification-design recommendation

`inline`

The decisive artifact-byte, manifest, path-independence, and identity-change
oracles are finite and explicit below; a separate design artifact would add
little beyond the task-owned focused tests.

## Outcome

A programmatic caller can capture explicitly selected artifact bytes into W1,
construct and validate a schema-v2 `ProjectSnapshot`, obtain the same logical
identity for semantically equivalent inputs independent of absolute paths, and
persist/reuse that immutable snapshot through the W1 namespace.

## Direction trace

- Direction contribution: Materialize the approved reusable project-context
  record and explicit-input artifact boundary.
- User-observable effect: No direct workflow effect; enables W2.2 task
  revisions and later producers to reference exact project artifacts instead
  of copying them or crawling `docs/`.
- Why now: W1 provides accepted blob and immutable-record persistence; W2.1 is
  the first dependency in the decomposed W2 record layer.
- Direction decisions used: collection contract §§4.1–4.2, 10 and
  11.1/11.9/11.12; architecture §§3, 5–6, 20–22; repo integration §§4–5 and
  20; implementation-plan Task 1; work-breakdown W0/W2; verification refs
  S-07, S-08, S-13–S-16, P-01.
- New direction decisions required: `None`

## Authority and scope

| Item | Contract |
|---|---|
| Authority | The v1.2.1 four-document authority chain, refined by work-breakdown W0/W2 and the verification matrix without changing their scope. |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Dependencies | W1 accepted; consume `scripts/evidence_store.py` exactly through its seven public operations. |
| Consumes | Explicit artifact inputs supplied by the caller: stable logical role/path plus bytes or a caller-selected file; W1 `put_blob` and `put_immutable_record`. |
| Produces | Initial `scripts/evidence_records.py`, `scripts/execution-evidence.schema.v2.json`, and `tests/test_evidence_records.py`, containing the shared canonical identity/validation foundation, explicit artifact helper, and complete ProjectSnapshot behavior. |
| Allowed changes | Only those three W2 files. |
| Read-only context | The execution-evidence design pack; `scripts/evidence_store.py`; `tests/test_evidence_store.py`; runtime-context schema/helper only as local schema-validation precedent. |
| Out of scope | TaskRevision, ExecutionAttempt, and Association constructors; lifecycle orchestration; recursive discovery; deciding which artifacts matter; planner parsing; skill/CLI integration; changes to W1 or existing workflow/runtime helpers. |
| Assumptions / unresolved decisions | Exact Python names/signatures and compact schema factoring are bounded implementation choices. Artifact identity must use a stable caller-supplied logical name/role plus content ref, never an absolute source path. No unresolved product or architecture decision blocks W2.1. |

## Work and acceptance criteria

Required work:

1. Add the minimal shared constants, canonical UTF-8 JSON identity helper, and
   validation/error conventions needed by ProjectSnapshot and later W2 leaves.
2. Add an explicit-input artifact helper that stores exact bytes with W1 and
   returns a stable artifact descriptor; it must not discover or infer inputs.
3. Add ProjectSnapshot construction/validation, deterministic identity, W1
   immutable persistence/reuse, the corresponding schema definition, and
   focused behavioral tests.
4. Keep `schema_version: 2` and deterministic collector-fingerprint fields
   representable in the shared evidence envelope; W2.3 owns final fingerprint
   construction and whole-schema closure.

- **AC-01:** Capturing exact artifact bytes stores/reuses the W1 content blob
  and returns a descriptor from which the bytes and stable logical artifact
  role can be recovered; no absolute source path appears in the descriptor or
  any logical ID.
- **AC-02:** The same explicitly supplied artifact manifest produces the same
  ProjectSnapshot ID and canonical record regardless of mapping/key order,
  insignificant JSON formatting, temporary repository root, or source-file
  absolute path.
- **AC-03:** Changing an artifact's bytes/ref or changing its stable logical
  role changes the ProjectSnapshot identity; list order is preserved, and
  omitted versus explicit `null` remains distinct unless the constructor
  deliberately documents normalization for a field.
- **AC-04:** ProjectSnapshot accepts only explicit relevant artifacts, validates
  its schema-v2 record shape, persists through W1's `project_snapshot`
  namespace, and an identical recreation is idempotently reusable.
- **AC-05:** Missing files, non-file inputs, malformed artifact descriptors,
  unsupported schema versions, duplicate/ambiguous logical artifact entries,
  and store failures are reported without crawling for substitutes or writing
  a false ProjectSnapshot.
- **AC-06:** Only the three scoped W2 files change; the implementation remains
  standard-library-only and introduces no later-record or producer behavior.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| Snapshot identity represents the explicit manifest, not local layout | same manifest with reordered object keys; same bytes under different absolute roots/names; changed bytes/ref; changed stable logical role | Public constructor plus W1 blob/snapshot readback in temporary Git repositories | Focused tests compare IDs and persisted records for every named case | Recreate one manifest in a second temp root, then alter only content and only logical role | Implementer owns targeted suite; fresh reviewer owns probe |
| Canonical identity preserves approved distinctions | equivalent object key order; ordered list reversal; omitted optional field; explicit null | Canonical identity helper and public ProjectSnapshot constructor | Focused test rejects key-order instability and proves the other three inputs remain distinct when semantically present | Independently compute records for omitted/null and reversed-list cases | Implementer owns targeted suite; fresh reviewer owns probe |
| Failed capture cannot create false complete evidence | missing/non-file input; blob-store failure; malformed descriptor; duplicate logical artifact | Public capture/snapshot helpers with real temporary filesystem and controlled store failure | Negative tests assert exception and absence of immutable snapshot record | Force one store failure after input validation and inspect namespaces | Implementer owns targeted suite; fresh reviewer owns probe |

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first / regression | Before production implementation, focused imports/behavior tests fail because `evidence_records.py` and the v2 schema do not exist. Record the expected failure without weakening assertions. | `python3 -m unittest tests/test_evidence_records.py -v` |
| Targeted | Explicit capture and all ProjectSnapshot positive/negative/identity cases pass against real temporary Git metadata storage. | `python3 -m unittest tests/test_evidence_records.py -v` |
| Owning suite | W1 blob/immutable namespace behavior remains green and supplies the real persistence boundary. | `python3 -m unittest tests/test_evidence_store.py -v` |
| Broader gate | N/A at this leaf: no existing producer imports the new module. W2.3 owns the aggregate four-record suite; reviewer performs scoped diff and stdlib checks now. | `git diff --check` |

## Expected contract impact

- Plan refs: architecture §§3, 5–6 and 20–22; repo integration §§4–5;
  implementation-plan Task 1; work-breakdown W2; S-07/S-08/S-13–S-16 and
  P-01 — `materialize` for the ProjectSnapshot slice.
- Current contract dependencies: no `docs/contracts/` registry exists;
  consume W1's `EvidenceStore`/`GitMetadataEvidenceStore` and namespaces from
  `scripts/evidence_store.py` and `docs/tasks/W1/W1-result.md`.
- Expected durable delta: explicit artifact descriptors, canonical record-ID
  semantics, a ProjectSnapshot constructor/validator/persistence helper, and
  the initial v2 schema envelope used by W2.2/W2.3.

## Stops and handoff

- Stop for a W1 baseline failure, ambiguous authority, overlap with user work,
  required third-party dependency, need to modify W1, or pressure to discover
  artifacts implicitly or define later-record semantics.
- Treat the metadata budget as a checkpoint; return to brief design rather
  than broadening scope.
- Preserve all pre-existing work and do not update the authority/master-plan
  documents.
- Next action: guided implementation after implementer self-preflight.
- Required follow-on: immediately after implementation or correction, hand
  the completed bytes to a fresh independent acceptance reviewer.
