# Execution Evidence Repository Integration

**Version:** 1.2.1  
**Status:** Draft for implementation  
**Date:** 2026-09-28  
**Authority:** subordinate to `execution-evidence-architecture.v1.2.1.md`

## 1. Purpose

This document maps the lean v1.2 evidence architecture onto the current `personal-skills` repository.

It defines ownership and expected repository changes, while avoiding speculative modules and integrations.

---

## 2. Responsibility map

| Component | Responsibility | Change |
|---|---|---:|
| `scripts/workflow_version.py` | canonical workflow identity | none |
| `scripts/runtime_context.py` | canonical trusted runtime identity | none/minimal adapter use |
| `scripts/evidence_store.py` | persistence + local backend + blobs | new |
| `scripts/evidence_records.py` | ProjectSnapshot, TaskRevision, Attempt, Association, capture helpers | new |
| `scripts/run_evidence.py` | attempt lifecycle producer | major |
| `task-brief-designer` | task revision + small planner context + decomposition | medium |
| `bounded-task-implementer` | guided execution integration | medium |
| `task-acceptance-review` | initial post-run review association | small |
| maintainability review | future generic association consumer | no change now |
| verification/preflight skills | task artifact sources | no redesign |
| project-planning skills | project artifact sources | no evidence-writing change |
| `task-orchestrator` | future producer of common evidence | documentation only |

No standalone `evidence_capture.py` or `execution_adapter.py` is planned in v1.2.

---

## 3. `scripts/evidence_store.py`

Own:

- Git-metadata evidence root;
- content-addressed blobs;
- immutable persistence for blobs, ProjectSnapshot, TaskRevision, and Association;
- lifecycle-managed create/update/finalize operations for active ExecutionAttempt records;
- basic record lookup/existence operations;
- atomic local writes.

Initial root:

```text
<git-dir>/personal-skills/evidence/v2/
```

Must not own task planning, review semantics, runtime discovery, complexity, or runner telemetry.

---

## 4. `scripts/evidence_records.py`

Own:

- ProjectSnapshot construction/validation;
- TaskRevision construction/validation;
- ExecutionAttempt construction/validation;
- Association construction/validation;
- deterministic record IDs;
- TaskRevision identity over all semantically relevant revision content, not only artifact bytes;
- content hashes;
- artifact-capture helpers;
- provenance/knowledge status;
- collector fingerprint helper or canonical input definition.

Potential helpers:

```text
capture_artifact(...)
create_project_snapshot(...)
create_task_revision(...)
```

These helpers accept explicit inputs.

They must not:

- recursively crawl project docs;
- infer which files matter;
- parse planner prose to manufacture fields;
- run attempt lifecycle.

---

## 5. Schema

Add one or a small number of v2 evidence schemas.

Prefer schema organization around the four core record concepts:

```text
ProjectSnapshot
TaskRevision
ExecutionAttempt
Association
```

Do not create standalone schema families for checks, telemetry, execution conditions, or collector identity unless implementation pressure later requires them.

Those are sections of existing records.

---

## 6. `scripts/run_evidence.py`

Keep lifecycle behavior equivalent to:

```text
begin
check
finish
recover
associate
```

### PRE-RUN

Accept/reference:

- direct input ref OR TaskRevision;
- execution ProjectSnapshot where relevant;
- repository snapshot;
- workflow identity;
- trusted actual runtime identity;
- intended execution profile where available;
- assignment provenance where available;
- optional execution-conditions object;
- related attempt;
- schema version + collector fingerprint.

### EXECUTION

Record:

- start/end/termination;
- deterministic checks inline;
- externally observable failure/interruption;
- optional caller-supplied telemetry object.

### POST-RUN

Record repository state after execution.

### Associations

Support a generic immutable association mechanism.

Initial skill integration only needs acceptance review.

### Must not

`run_evidence.py` must not:

- crawl planning artifacts;
- infer planning context;
- implement Codex/OpenCode-specific telemetry;
- calculate complexity/features;
- infer acceptance;
- contain task-orchestrator-specific branches.

---


## 7. ExecutionAttempt lifecycle

The storage and collector integration must treat an attempt as active until finish/recovery finalization.

Required behavior:

```text
begin
  create attempt
  freeze PRE-RUN

check / execution updates
  append execution facts only

finish / recover
  write closure + POST-RUN
  finalize attempt
```

After finalization the complete attempt is immutable.

This avoids conflicting with the immutable-record semantics used for ProjectSnapshot, TaskRevision, Association, and blobs.

---

## 8. Optional execution conditions and telemetry

Do not add a dedicated adapter framework now.

`run_evidence.py` may accept normalized optional mappings/objects from its caller.

Example conceptual inputs:

```text
execution_conditions = {...} | unavailable
telemetry = {...} | unavailable
```

When a future runner integration exists, it can populate those fields without changing the evidence schema.

---

## 9. Collector fingerprint

Persist:

```text
schema_version
collector_fingerprint
```

Use a deterministic fingerprint over the collection implementation files/configuration that materially affect evidence semantics.

Prefer reusing/generalizing the existing workflow-fingerprint approach.

Do not introduce manually maintained versions for every evidence helper.

---

## 10. `task-brief-designer`

Best-effort preserve:

- raw task artifact refs;
- ProjectSnapshot when relevant;
- TaskRevision;
- parent/child relationships;
- split/decomposition fact;
- planner estimates;
- small structured planning context;
- planner/workflow producer provenance;
- planner-recommended profile/reasoning;
- source-plan relationship when available.

### Initial structured context

Prioritize:

```text
task_type
intended_scope
behavioral_scope
transformation_type
implementation_precedent
state_or_compatibility_constraints
verification_work
discovery_uncertainty
```

Do not force every field.

Do not add a second parser/LLM to fill missing fields.

Raw task artifacts remain retained for future derivation.

---

## 11. Task artifact layout documentation

Update the task artifact layout reference to clarify:

- repository task packages remain authoritative;
- evidence is historical/immutable and stored separately;
- `docs/tasks/index.json` remains structural, not a runtime ledger;
- runtime evidence does not belong under task package runtime folders;
- task/project artifacts may be captured by content reference without moving them.

---

## 12. `bounded-task-implementer`

When evidence tooling exists, best-effort:

1. identify direct versus formal task;
2. capture/reference the exact task input;
3. capture/reference ProjectSnapshot/TaskRevision when applicable;
4. begin the attempt before edits;
5. pass optional known execution conditions directly;
7. retain attempt ID;
8. record canonical deterministic checks;
9. accept optional naturally available telemetry;
10. finish factually;
11. carry attempt ID into acceptance-review handoff.

Standalone execution must remain valid with:

- no task ID;
- no brief;
- no project plan;
- unavailable runtime identity;
- no execution-condition data;
- no telemetry;
- missing/broken optional evidence tooling.

---

## 13. `task-acceptance-review`

This is the only review skill that must be automatically integrated in the initial scope. Other review producers remain representable through the generic Association record but are deferred.

When an attempt ID is supplied:

- create an `acceptance_review` Association;
- capture the durable review artifact when one exists;
- preserve factual verdict/status;
- preserve reviewer provenance;
- preserve collection time.

When no reliable attempt ID exists, do not guess.

Keep separate:

```text
executor completed
verification passed
acceptance review result
ultimate task acceptance
```

No synthetic success score.

---

## 14. Maintainability review

Do not integrate it in this implementation.

The generic Association record must be capable of supporting future:

```text
maintainability_review
```

without schema redesign.

That future integration should be a small follow-up.

---

## 15. Verification/preflight skills

No redesign.

If their artifacts exist before execution, include them in TaskRevision capture.

Do not require them for standalone tasks.

---

## 16. Project-planning skills

Do not add evidence-writing behavior across project planning.

Relevant project artifacts are captured explicitly when task design/execution needs them.

---

## 17. Documentation

Update:

```text
README.md
skills/task-implementation-flow/README.md
scripts/run-evidence.md
task-brief-designer/references/task-artifact-layout.md
skills/task-orchestrator/docs/direction-revised.md
```

Document:

- ProjectSnapshot / TaskRevision / ExecutionAttempt / Association;
- small structured planner context;
- optional inline execution conditions;
- optional inline telemetry;
- collector fingerprint;
- Git-local storage;
- future S3 direction only at a high level;
- best-effort semantics.

---

## 18. Project-local installation

Expected shared tooling:

```text
.agents/scripts/
├── run_evidence.py
├── evidence_store.py
├── evidence_records.py
├── execution-evidence.schema.v2.json
├── workflow_version.py
├── runtime_context.py
└── runtime-context.schema.v1.json
```

Adjust only if v2 schema is split.

The rule remains:

```text
missing optional evidence tooling
!=
failed bounded task
```

unless another explicit contract makes evidence mandatory.

---

## 19. `task-orchestrator`: documentation only

No implementation changes.

Update only its future direction:

1. one worker invocation maps to one ExecutionAttempt;
2. retry/resume/correction/replay create linked attempts;
3. controller state remains separate from evidence;
4. orchestrator uses ProjectSnapshot/TaskRevision refs instead of copying planning docs;
5. existing workflow/runtime identity remains authoritative;
6. richer conditions/telemetry populate existing optional attempt sections;
7. orchestrator uses the common storage abstraction;
8. no competing evidence schema/store;
9. no dependency on the current legacy controller record layout.

---

## 20. Tests

### `tests/test_evidence_store.py`

Cover:

- blob deduplication;
- deterministic refs;
- immutable writes;
- overwrite conflict rejection;
- atomic writes;
- namespace separation;
- logical path independence.

### `tests/test_evidence_records.py`

Cover:

- ProjectSnapshot identity;
- TaskRevision identity;
- artifact capture helpers;
- small planner context/provenance;
- ExecutionAttempt structure;
- optional conditions/telemetry;
- attempt relationships;
- Association;
- collector fingerprint fields;
- unknown/unavailable/N/A distinctions.

### `tests/test_run_evidence.py`

Cover:

- direct task;
- formal TaskRevision;
- ProjectSnapshot;
- PRE-RUN immutability;
- workflow/runtime identity;
- conditions present/absent;
- telemetry present/absent;
- checks inline;
- finish/interruption/recovery;
- attempt relations;
- association;
- collector fingerprint.

### Skill evals

Cover:

- planner/decomposition capture;
- standalone implementer path;
- formal-task implementer path;
- evidence failure remains non-fatal;
- attempt ID handoff;
- acceptance association.

### Installation

Retain realistic `.agents/` installation testing, including application repositories that ignore `.agents/`.

---

## 21. Explicitly deferred

Do not implement in this scope:

- standalone artifact-capture CLI/module;
- execution adapter framework;
- runner-specific telemetry scraping;
- maintainability-review evidence integration;
- S3 backend;
- S3 key hierarchy/auth/retry design;
- legacy v1 migration/compatibility reader;
- dataset export;
- derived repository metrics;
- embeddings/similarity;
- ML/scoring/routing;
- task-orchestrator implementation changes.

---

## 22. Version axes

The design-pack/document version (`1.2.1`) and persisted evidence schema version (`2`) are separate. Do not bump the schema merely because this documentation patch changed wording or clarified lifecycle semantics.

---

## 23. Integration success condition

The initial repository integration is complete when:

- direct tasks produce reproducible attempts;
- formal tasks produce reusable task revisions;
- project/task artifacts are deduplicated;
- small planner context and estimates survive;
- decomposition history can survive without execution;
- optional execution conditions/telemetry can be stored but are not required;
- deterministic checks remain inline raw evidence;
- acceptance results can attach after execution;
- collector semantics are identifiable;
- no unnecessary public tool surface was introduced;
- ordinary task execution remains independent of evidence infrastructure.
