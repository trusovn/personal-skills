# Task Brief: `W2.2` — Implement task revisions and planning history

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: strong
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / 36k context
```

## Execution sizing

- Sizing policy: `default@1`
- Estimated agent calls: `15`
- Estimated implementation duration: `40 minutes`
- Estimate confidence: `medium`
- Policy result: `fits`
- Triggered limits: `none`
- Decomposition override: `none`

The estimate covers implementation work only and excludes W2.1 acceptance
evidence and the required fresh W2.2 acceptance review.

## Readiness route

`implementer self-preflight`

Confirm W2.1 was accepted, inspect its public record/artifact conventions, and
run `python3 -m unittest tests/test_evidence_records.py -v` before editing.
Stop rather than repair W2.1 within this leaf.

## Verification-design recommendation

`separate — TaskRevision identity must change for each of six finite semantic
dimensions while remaining stable for representational noise, and parent/child
history plus optional planning/provenance fields admit several plausible but
selection-biased implementations`

This is advisory. If skipped, the implementer must preserve every case and
oracle below in the task-owned focused suite.

## Outcome

A programmatic caller can construct, validate, persist, and reuse an immutable
schema-v2 `TaskRevision` whose ID covers every approved semantic revision
dimension, preserves supplied planner facts and provenance without backfill,
and represents decomposed parents and children even when no attempt exists.

## Direction trace

- Direction contribution: Preserve formal task state, planner predictions, and
  decomposition/selection history at their source.
- User-observable effect: No direct workflow effect; enables W3 formal attempts
  to reference exact task state and W4 to retain parent/child revisions,
  including unexecuted parents.
- Why now: W2.1 provides accepted artifact and ProjectSnapshot references;
  TaskRevision is the next dependency before runtime records can reference
  formal tasks.
- Direction decisions used: collection contract §§4.1, 5, 9–10 and
  11.2/11.3/11.7/11.8/11.10; architecture §§7–9 and 21; repo integration §§4–5
  and 20; implementation-plan Task 1; work-breakdown W2; verification refs
  S-09–S-11, S-14–S-16 and P-02–P-07.
- New direction decisions required: `None`

## Authority and scope

| Item | Contract |
|---|---|
| Authority | The v1.2.1 four-document authority chain, refined by W0/W2 and the verification matrix. |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Dependencies | Accepted W2.1 behavior and files; accepted W1 immutable `task_revision` namespace. |
| Consumes | W2.1 artifact descriptors, canonical identity/validation conventions, optional planning ProjectSnapshot ref, and explicit caller-supplied planning/provenance/decomposition values. |
| Produces | TaskRevision constructor/validator/persistence behavior plus schema and tests in the same three W2 files; W2.1 behavior remains unchanged. |
| Allowed changes | Only `scripts/evidence_records.py`, `scripts/execution-evidence.schema.v2.json`, and `tests/test_evidence_records.py`. |
| Read-only context | Design pack, accepted W2.1 result/review when present, W1 store, and existing W2.1 tests. |
| Out of scope | Parsing Markdown or planner prose; manufacturing missing fields; ExecutionAttempt/Association; skill integration; task-index mutation; lifecycle execution; changing sizing policy; altering accepted W2.1 semantics. |
| Assumptions / unresolved decisions | Exact Python signature and compact representation of provenance/decomposition links are bounded implementation choices, but their approved meanings and identity participation are not. No unresolved product or architecture decision blocks W2.2. |

## Work and acceptance criteria

Required work:

1. Extend the module/schema with TaskRevision construction and validation using
   explicit artifact refs, optional planning ProjectSnapshot ref, optional
   structured planning facts/estimates, identity-bearing producer provenance,
   and decomposition/source-plan relationships.
2. Make revision identity cover all semantically relevant supplied content,
   persist through W1's `(task_id, revision_id)` namespace, and support records
   that never receive an ExecutionAttempt.
3. Extend tests without weakening or changing accepted W2.1 behavior.

- **AC-01:** Equivalent TaskRevision inputs produce the same revision ID and
  canonical record despite object-key order or insignificant JSON formatting;
  absolute task-package/source paths do not participate in identity.
- **AC-02:** Holding the same task brief ref constant, changing any one of
  artifact refs, structured planning context, planner estimates/profile/split
  facts, decomposition/source-plan relationships, planning ProjectSnapshot
  ref, or identity-bearing producer provenance changes the revision ID.
- **AC-03:** The initial optional planner set can preserve `task_type`,
  `intended_scope`, `behavioral_scope`, `transformation_type`,
  `implementation_precedent`, `state_or_compatibility_constraints`,
  `verification_work`, and `discovery_uncertainty`, plus expected calls,
  expected duration, confidence, recommended profile/reasoning, and split
  decision, exactly when supplied and with provenance.
- **AC-04:** Omitted planner values stay absent; `unknown`, zero, false,
  `not_applicable`, and explicit null remain distinguishable according to the
  approved canonical rules. No parser, model, or default manufactures a value.
- **AC-05:** Decomposed parent and child revisions preserve stable task IDs,
  parent/child relationships, split decision, and source-plan relationship;
  the parent revision is valid and persistable without an attempt.
- **AC-06:** Invalid task IDs/refs, malformed relationships, unsupported schema
  versions, unrecognized provenance/knowledge-status values, and conflicting
  immutable persistence fail without replacing an existing revision.
- **AC-07:** Only the three scoped files change; W2.1 behavior remains green
  and the implementation remains standard-library-only.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| Revision identity covers every approved semantic dimension | artifact refs; planning context; planner estimates/profile/split; decomposition/source-plan relations; planning ProjectSnapshot ref; identity-bearing producer provenance | Public constructor IDs and W1 immutable TaskRevision readback | Parameterized/subtest matrix changes exactly one dimension while brief ref stays fixed | Fresh reviewer changes two easily omitted dimensions independently: split relation and producer identity | Implementer owns targeted matrix; fresh reviewer owns probe |
| Missing planning data is not backfilled or collapsed | omitted; explicit null; unknown; zero; false; not_applicable for applicable field types | Constructed record and schema validation | Focused cases inspect exact keys/values and provenance; no prose parser invoked | Supply a sparse planning object and verify no extra planner fields appear | Implementer owns targeted suite; fresh reviewer owns probe |
| Decomposition history survives without execution | unsplit leaf; decomposed parent with children; child with parent; parent with no attempt | Persisted TaskRevision records in real W1 store, with no attempt namespace entry | Focused tests persist and reload each state and assert relations | Persist parent/child revisions, execute no attempt, and retrieve both | Implementer owns targeted suite; fresh reviewer owns probe |

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first / regression | Add identity and sparse/decomposition cases before implementation; they fail because TaskRevision behavior is absent, for that reason. | `python3 -m unittest tests/test_evidence_records.py -v` |
| Targeted | All ProjectSnapshot regressions and TaskRevision identity, optionality, provenance, decomposition, invalid-input, and persistence cases pass. | `python3 -m unittest tests/test_evidence_records.py -v` |
| Owning suite | W1 immutable tuple-ID persistence remains compatible. | `python3 -m unittest tests/test_evidence_store.py -v` |
| Broader gate | N/A until W2.3 integrates all four records; fresh reviewer owns scoped diff, standard-library, and no-parser/no-extra-file inspection. | `git diff --check` |

## Expected contract impact

- Plan refs: architecture §§7–9/21; repo integration §§4–5;
  implementation-plan Task 1; work-breakdown W2; S-09–S-11/S-14–S-16 and
  P-02–P-07 — `materialize`; accepted W2.1 contracts — `preserve`.
- Current contract dependencies: no `docs/contracts/` registry exists; consume
  accepted W2.1 module/schema conventions and W1's `task_revision` namespace.
- Expected durable delta: reusable TaskRevision shape, full semantic revision
  identity, sparse planner/provenance representation, and decomposition history
  contract consumed by W3/W4.

## Stops and handoff

- Stop if W2.1 is not accepted/green, its API cannot express TaskRevision
  without a material redesign, user work overlaps scoped files, authority is
  ambiguous, or implementation pressure introduces parsing/backfill, a new
  planning model, or later-record behavior.
- Treat the budget as a checkpoint and preserve all pre-existing work.
- Do not edit authority/master-plan documents or `docs/tasks/index.json`.
- Next action: guided implementation after implementer self-preflight (with the
  optional focused verification-design pass recommended above).
- Required follow-on: immediately after implementation or correction, hand
  the completed bytes to a fresh independent acceptance reviewer.
