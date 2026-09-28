# Execution Evidence Implementation Plan

**Version:** 1.2.1  
**Status:** Draft for implementation  
**Date:** 2026-09-28  
**Authority:** subordinate to `execution-evidence-repo-integration.v1.2.1.md`

## 1. Purpose

This is the lean implementation sequence for Execution Evidence v2.

The plan deliberately minimizes new modules and integrations while preserving the raw evidence needed for later task-difficulty / execution-profile research.

Authority order:

1. `execution-evidence-collection-contract.v1.2.1.md`
2. `execution-evidence-architecture.v1.2.1.md`
3. `execution-evidence-repo-integration.v1.2.1.md`
4. this plan

Do not implement the entire plan as one agent task.

---

## 2. Stage sequence

```text
Task 1  Evidence model + local storage + artifact snapshots
   ↓
Task 2  Run Evidence v2
   ↓
Task 3  Planner/decomposition integration
   ↓
Task 4  Guided execution + acceptance integration
   ↓
Task 5  Documentation, installation, regression closure
```

`task-orchestrator` implementation remains out of scope.

---

# Task 1 — Evidence model, local storage, and artifact snapshots

## Objective

Create the minimal shared persistence/model foundation.

## Expected files

```text
ADD scripts/evidence_store.py
ADD scripts/evidence_records.py
ADD scripts/execution-evidence.schema.v2.json
ADD tests/test_evidence_store.py
ADD tests/test_evidence_records.py
```

Split schema only if one file becomes genuinely unwieldy.

## Implement

### Storage

Use a Git-metadata local backend:

```text
<git-dir>/personal-skills/evidence/v2/
```

Support the small persistence surface needed now:

```text
put_blob
put_immutable_record
create_attempt
update_active_attempt
finalize_attempt
get_record
record_exists
```

`ProjectSnapshot`, `TaskRevision`, `Association`, and blobs use immutable writes. `ExecutionAttempt` is lifecycle-managed until finalization.

### Core records

Implement:

```text
ProjectSnapshot
TaskRevision
ExecutionAttempt
Association
```

Do not create separate top-level models for:

```text
ExecutionConditions
ExecutionTelemetry
CheckObservation
CollectorIdentity
```

Those are sections/fields of ExecutionAttempt.

### Artifact capture helpers

Provide small internal/shared helpers in `evidence_records.py`, for example:

```text
capture_artifact(...)
create_project_snapshot(...)
create_task_revision(...)
```

Inputs are explicit.

Do not recursively discover project documents.

### TaskRevision planning section

Support the small initial structured planner set:

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

plus existing estimates/profile/split facts.

All optional.

### Identity/invariants

Ensure:

- blob deduplication;
- deterministic ProjectSnapshot IDs;
- deterministic TaskRevision IDs covering artifact refs, planning context, planner estimates, decomposition relationships, planning project snapshot ref, and identity-bearing provenance;
- immutable conflicting writes fail;
- logical IDs are independent of absolute local paths;
- knowledge-status distinctions remain possible.

## Non-goals

Do not modify skills.

Do not modify `run_evidence.py` lifecycle yet.

Do not add:

- artifact-capture CLI/module;
- runtime adapter framework;
- S3;
- legacy v1 reader/migration;
- feature extraction.

## Verification

Focused tests prove the storage/model invariants and artifact deduplication.

## Exit criteria

A programmatic caller can create/reuse ProjectSnapshot and TaskRevision records and construct valid Attempt/Association records without any skill integration.

---

# Task 2 — Run Evidence v2

## Objective

Refactor the existing run-evidence lifecycle onto the v2 records/storage while retaining existing workflow/runtime/repository mechanisms.

## Expected files

```text
MOD scripts/run_evidence.py
MOD scripts/run-evidence.md
MOD tests/test_run_evidence.py
```

Reuse:

```text
evidence_store.py
evidence_records.py
workflow_version.py
runtime_context.py
```

## Implement

### PRE-RUN

Accept/reference:

- direct task ref OR TaskRevision;
- execution ProjectSnapshot when applicable;
- PRE-RUN repository snapshot;
- workflow identity;
- trusted actual runtime identity;
- intended execution profile when available;
- assignment provenance when available;
- optional execution-conditions mapping;
- related attempt;
- evidence schema version;
- collector fingerprint.

Freeze PRE-RUN before edits.


### Attempt lifecycle

Implement:

```text
begin
  -> create attempt
  -> freeze PRE-RUN

active
  -> append checks/execution facts

finish/recover
  -> write closure + POST-RUN
  -> finalize

finalized
  -> immutable
```

Tests must prove that PRE-RUN cannot change after `begin` even while execution facts are still being appended.


### EXECUTION

Record:

- start;
- inline deterministic checks;
- failure/interruption facts;
- optional telemetry mapping when naturally supplied.

### POST-RUN

Record:

- factual finish/termination;
- POST-RUN repository snapshot.

### Association

Add generic immutable association support.

### Collector fingerprint

Deterministically fingerprint the evidence implementation files/configuration that materially affect collection semantics.

Do not manually version every helper.

### Recovery

Retain current best-effort recovery behavior without inventing facts across uncertain boundaries.

## Direct task

A direct task must work with no formal task infrastructure.

## Formal task

A formal attempt references TaskRevision/ProjectSnapshot rather than embedding all project/task artifacts.

## Non-goals

No skill integration.

No runner-specific telemetry.

No adapter framework.

No full diff/stat calculation.

No maintainability-review integration.

## Verification

Cover:

- direct task;
- formal TaskRevision;
- ProjectSnapshot;
- PRE-RUN immutability;
- runtime/workflow identity;
- optional conditions present/absent;
- optional telemetry present/absent;
- inline checks;
- finish/interruption/recovery;
- assignment provenance;
- attempt relations;
- association;
- collector fingerprint behavior.

## Exit criteria

A caller can create a complete v2 attempt without knowing physical storage paths and without any runner-specific integration.

---

# Task 3 — Planner and decomposition integration

## Objective

Preserve formal task revisions, planner-produced structured context, estimates, and decomposition history.

## Expected files

Likely:

```text
MOD skills/task-implementation-flow/task-brief-designer/SKILL.md
MOD skills/task-implementation-flow/task-brief-designer/references/task-artifact-layout.md
MOD/ADD task-brief-designer evals/tests
```

Only modify templates if a required planner-produced fact cannot otherwise be emitted.

## Implement

When task artifacts are produced and evidence tooling is available, best-effort:

- capture relevant project artifacts into ProjectSnapshot;
- capture task artifacts into TaskRevision;
- emit the small structured planning set where already known;
- preserve planner estimates;
- preserve intended profile/reasoning;
- preserve split decision;
- preserve parent/child relationships;
- preserve source-plan relationship where available.

### Critical rule

Do not add a later generic parser or LLM whose purpose is to infer missing planner fields from prose.

Raw brief/supporting artifacts remain captured for future derivation.

### Selection history

Composite parents and other produced-but-unexecuted task candidates must remain representable.

Do not invent hypothetical tasks.

## Non-goals

Do not:

- change sizing policy;
- calculate complexity labels;
- add routing;
- write execution attempts;
- require evidence tooling for valid planning.

## Verification

Prove:

- task revision capture/reuse;
- changed task content -> new revision;
- small planner context survives with provenance and producing planner/workflow identity when available;
- missing fields stay missing/unavailable;
- parent task survives without attempt;
- child relations preserved;
- evidence failure does not block brief generation.

## Exit criteria

The evidence layer includes both formal execution candidates and decomposition history without adding new classification logic.

---

# Task 4 — Guided execution and acceptance integration

## Objective

Connect the v2 evidence system to normal bounded implementation and the initial independent acceptance outcome.

## Expected files

Likely:

```text
MOD bounded-task-implementer/SKILL.md
MOD/ADD bounded-task-implementer evals/tests

MOD task-acceptance-review/SKILL.md
MOD acceptance report template only if cleanly useful
MOD/ADD acceptance-review evals/tests
```

Do not change maintainability review.

## Bounded implementer

Before edits:

1. locate optional evidence tooling;
2. determine direct vs formal task;
3. capture/reference exact task input;
4. capture/reference ProjectSnapshot/TaskRevision where applicable;
5. pass known optional execution conditions directly;
6. begin attempt;
7. retain attempt ID.

During execution:

- record canonical deterministic checks;
- pass naturally available telemetry only if already known;
- do not duplicate commands solely for evidence.

At closure:

- finish attempt factually;
- capture POST-RUN repo state;
- preserve attempt ID in acceptance handoff.

### Standalone invariant

Still works with:

- no task ID;
- no brief;
- no project plan;
- no runtime identity;
- no conditions;
- no telemetry;
- missing/broken optional evidence tooling.

## Acceptance review

This is the only review producer that must be automatically integrated in the initial implementation. The generic Association model remains reusable by other review producers later.

When reliable attempt ID is supplied:

- create `acceptance_review` Association;
- capture durable review report by content identity when present;
- preserve factual verdict/status;
- preserve reviewer provenance;
- preserve collection time.

Without attempt ID, do not guess.

Keep execution completion, verification, acceptance review, and final acceptance distinct.

## Non-goals

Do not:

- create task artifacts solely for evidence;
- integrate maintainability review;
- create success score;
- add routing/scoring;
- modify task orchestrator.

## Verification

Cover:

- direct task with evidence;
- direct task without evidence tooling;
- formal task;
- optional conditions/telemetry absent;
- evidence failure non-fatal;
- attempt ID handoff;
- checks not duplicated;
- acceptance association created only with reliable attempt ID;
- review semantics unchanged.

## Exit criteria

Ordinary guided execution records useful evidence when available, and independent acceptance can be linked, without evidence becoming a prerequisite for task completion.

---

# Task 5 — Documentation, installation, and regression closure

## Objective

Make the lean v2 system discoverable/installable and document future integration constraints.

## Expected files

```text
MOD README.md
MOD skills/task-implementation-flow/README.md
MOD scripts/run-evidence.md
MOD task-brief-designer/references/task-artifact-layout.md
MOD skills/task-orchestrator/docs/direction-revised.md
MOD/ADD installation/integration tests
```

## Document installed tooling

Expected:

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

## Document flow

```text
project artifacts
      ↓
ProjectSnapshot
      │
task-brief-designer
      ↓
TaskRevision + small planner context
      │
bounded-task-implementer
      ↓
ExecutionAttempt
      │
      ├── optional conditions/telemetry
      └── acceptance association
```

## Orchestrator direction only

Document that a future redesign must:

- use the same four core record concepts;
- map one worker invocation to one attempt;
- preserve linked retry/resume/correction/replay attempts;
- keep controller state separate from evidence;
- reference ProjectSnapshot/TaskRevision;
- reuse workflow/runtime identity;
- populate existing optional attempt fields rather than introducing a competing telemetry schema;
- use the common storage abstraction;
- avoid dependence on the current controller record layout.

Do not change orchestrator implementation.

## Installation verification

Verify realistic `.agents/` installation including repositories that ignore `.agents/`.

## Regression verification

Run:

- evidence-store tests;
- evidence-record tests;
- run-evidence tests;
- workflow-version tests;
- runtime-context tests;
- task-brief-designer evals/tests;
- bounded-task-implementer evals/tests;
- acceptance-review evals/tests;
- realistic installation test.

## Exit criteria

A fresh agent can discover, install, and use the v2 evidence system without conversation history, and no speculative infrastructure is required.

---

## 3. Explicitly deferred follow-ups

### Remote/object storage

Later:

- `S3EvidenceStore`;
- auth/config;
- remote immutable writes;
- retry/offline policy;
- repository-snapshot portability;
- Git-object/raw-state preservation.

Do not define the detailed S3 object hierarchy now.

### Runner-specific telemetry integration

Later, when a concrete runner exposes reliable telemetry:

- Codex/OpenCode/Bedrock-specific collection;
- normalization into the existing optional telemetry object.

No adapter framework is required before that work exists.

### Additional review associations

Later:

```text
maintainability_review
other verification/review artifacts
```

The generic Association record should already support them.

### Historical v1 evidence

No reader/migration now.

Add a one-off converter later only if historical data is valuable enough to justify it.

### Analytics

Later:

- dataset export;
- repository feature extraction;
- TF-IDF;
- embeddings;
- semantic similarity;
- classical ML;
- calibration;
- learned routing.

---

## 4. Version axes

The design-pack/document version is `1.2.1`; the persisted evidence schema version remains `2` unless actual persisted-record compatibility changes.

---

## 5. Overall completion criteria

The initial implementation series is complete when durable evidence can answer:

### PRE-RUN

- exact task;
- direct vs formal;
- task revision;
- planning project snapshot where formal planning existed;
- execution project snapshot where applicable;
- repository state;
- workflow identity;
- planner-recommended profile where applicable;
- intended execution profile;
- actual runtime profile;
- planner estimates;
- small structured planner context;
- assignment provenance;
- naturally available execution conditions;
- decomposition/attempt relationships;
- evidence schema/collector identity.

### EXECUTION

- start/end;
- completion/termination;
- deterministic checks;
- reliable failure/interruption facts;
- optional naturally available telemetry.

### POST-RUN

- resulting repository state;
- reconstructable delta;
- independent acceptance association where review occurred;
- correction/retry/continuation relations.

### Dataset integrity

- PRE-RUN is not contaminated by POST-RUN facts;
- raw task/planning artifacts remain recoverable;
- project/task artifacts are deduplicated;
- unknown values are not guessed;
- non-executed decomposed tasks remain visible;
- future derived features can be generated from historical raw evidence;
- future remote storage or runner integration can be added without redesigning the core record model.
