# Execution Evidence Architecture

**Version:** 1.2.1  
**Status:** Draft for implementation  
**Date:** 2026-09-28  
**Authority:** subordinate to `execution-evidence-collection-contract.v1.2.1.md`

## 1. Purpose

This document defines the smallest architecture that satisfies the Execution Evidence Collection Contract while remaining suitable for later analysis and remote storage.

The design is intentionally biased toward:

- raw evidence;
- reproducibility;
- low routine collection cost;
- few new abstractions;
- future derivation rather than premature feature extraction.

It does not define scoring, routing, ML, semantic similarity, S3 implementation, or runner-specific instrumentation.

---

## 2. Core model

The initial architecture has only four first-class record concepts:

```text
ProjectSnapshot
TaskRevision
ExecutionAttempt
Association
```

Relationships:

```text
ProjectSnapshot
      │
      ▼
TaskRevision
      │
      ▼
ExecutionAttempt
      │
      └── Association(s)
```

Additional facts such as planning context, execution conditions, telemetry, checks, and collector identity are sections **inside** these records rather than separate top-level entities.

This keeps the evidence model small without losing information.

---

## 3. Repository authority versus historical evidence

Repository documents remain authoritative for planning and workflow use.

Examples:

```text
docs/project-plan.md
docs/task-map.json
docs/project-plan-review.md

docs/tasks/TASK-017/brief.md
docs/tasks/TASK-017/verification.md
docs/tasks/TASK-017/preflight.md
docs/tasks/TASK-017/reviews/acceptance-01.md
```

The evidence layer captures exact historical bytes and references.

```text
repository artifact
      ↓
content-addressed blob
      ↓
ProjectSnapshot / TaskRevision / Association
```

Evidence storage does not replace repository artifacts.

---

## 4. Local storage

Initial local evidence storage remains outside the worktree:

```text
<git-dir>/personal-skills/evidence/v2/
```

Logical layout:

```text
evidence/v2/
├── project/
│   └── snapshots/
│       └── <project-snapshot-id>.json
├── tasks/
│   └── <task-id>/
│       └── revisions/
│           └── <task-revision-id>.json
├── attempts/
│   └── <attempt-id>/
│       ├── attempt.json
│       └── associations/
└── blobs/
    └── sha256/
        └── <prefix>/<hash>
```

There is no separate `checks/` namespace in the initial design. Checks belong to the attempt.

The physical mapping is owned by the local storage implementation; producers should use logical references.

---

## 5. Content-addressed blobs

Store exact artifact bytes once by SHA-256 identity.

Use blobs for:

- project plans and task maps;
- task briefs;
- verification/preflight artifacts;
- exact direct request text;
- durable acceptance-review reports;
- other explicit context artifacts that materially affected planning/execution.

Do not copy the same project or task documents into every attempt.

Logical IDs must not depend on absolute local filesystem paths.

---

## 6. ProjectSnapshot

A `ProjectSnapshot` captures the exact reusable project-level authority/context artifacts relevant to task design or execution.

Example:

```text
ProjectSnapshot P1
├── project-plan.md        -> sha256:A
├── task-map.json          -> sha256:B
└── project-plan-review.md -> sha256:C
```

Rules:

- capture only explicitly relevant artifacts;
- do not recursively snapshot all of `docs/`;
- unchanged artifact manifests should produce the same snapshot identity;
- tasks/attempts reference the snapshot rather than copying its content.

---

## 7. TaskRevision

A `TaskRevision` represents one exact formal task state.

Example:

```text
TaskRevision T17-R2
├── raw artifact refs
│   ├── brief.md
│   ├── verification.md?
│   └── preflight.md?
├── planning_project_snapshot_ref?
├── planning
│   ├── small structured context
│   ├── planner estimates
│   └── producer provenance
└── decomposition relationships
```

### 7.1 Small initial structured planning set

The initial implementation should prioritize:

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

plus existing planner outputs such as:

```text
expected_calls
expected_duration
confidence
intended_profile
reasoning_effort
split_decision
```

Rules:

- fields are optional;
- preserve only facts the planner already produced;
- retain provenance;
- preserve the producing planner/workflow identity or fingerprint when available;
- do not run a later parser/LLM to fill missing values;
- retain the raw planning artifact so additional features can be derived later.

`TaskRevision` identity must cover all semantically relevant revision content, including artifact refs, planning context, planner estimates, decomposition relationships, planning project snapshot ref, and identity-bearing provenance. It must not be derived from the brief bytes alone.

A `TaskRevision` may exist even when no executor ever runs it.

This preserves decomposition/selection history.

---


## 8. Execution-profile semantics

Three distinct profile facts may exist and must not overwrite one another:

```text
TaskRevision.planning.planner_recommended_profile
ExecutionAttempt.pre_run.intended_execution_profile
ExecutionAttempt.pre_run.actual_runtime_identity
```

Meaning:

- `planner_recommended_profile` — what planning recommended;
- `intended_execution_profile` — what the caller/policy intended to launch;
- `actual_runtime_identity` — what trusted runtime context reports actually ran.

These values may differ and are analytically useful precisely because they may differ.

---

## 9. Direct standalone tasks

A direct request is a valid first-class execution input.

Example:

```text
"Fix this bug in parser.py"
```

Preserve the exact effective request as an immutable blob/reference.

Do not manufacture:

- task ID;
- brief;
- task package;
- project plan;
- verification/preflight artifacts.

---


## 9. Project-snapshot roles

The same `ProjectSnapshot` record type is used in two different roles:

```text
TaskRevision.planning_project_snapshot_ref
ExecutionAttempt.execution_project_snapshot_ref
```

`planning_project_snapshot_ref` means the project context under which the formal task revision was produced.

`execution_project_snapshot_ref` means the project context effectively available when execution began.

They may refer to the same snapshot, but they are not required to.

This distinction preserves cases where a task is planned under one project context and executed later after project-level authority changes.

---

## 10. ExecutionAttempt

One `ExecutionAttempt` represents one actual executor invocation.

Conceptual shape:

```text
ExecutionAttempt
├── task
│   └── direct_input_ref OR task_revision_ref
├── execution_project_snapshot_ref?
├── pre_run
│   ├── repository_state
│   ├── workflow_identity
│   ├── actual_runtime_identity
│   ├── intended_execution_profile?
│   ├── assignment_provenance?
│   └── execution_conditions?
├── execution
│   ├── started_at
│   ├── finished_at / terminated_at
│   ├── termination_state
│   ├── checks[]
│   └── telemetry?
├── post_run
│   └── repository_state
├── related_attempts[]
└── evidence
    ├── schema_version
    └── collector_fingerprint
```

PRE-RUN must be frozen before edits begin.


### ExecutionAttempt lifecycle

`ExecutionAttempt` is lifecycle-managed until finalization:

```text
begin
  -> create attempt + freeze PRE-RUN
active
  -> append execution/check facts
finish/recover
  -> record closure + POST-RUN
finalized
  -> whole attempt becomes immutable
```

This is the only core record allowed to change during its active lifecycle.

`ProjectSnapshot`, `TaskRevision`, `Association`, and blobs are immutable once created.



---

## 11. Optional PRE-RUN execution conditions

Execution conditions remain useful because the same task can behave differently under different constraints.

Keep them as one optional PRE-RUN object, for example:

```text
os
architecture
toolchain
available_tools
network_access
sandbox_mode
approval_mode
budget
timeout
fresh_or_resumed
supplied_context_refs
```

Rules:

- collect only naturally available trusted facts;
- no expensive environment discovery;
- no dedicated adapter framework required now;
- callers may supply fields directly;
- missing values remain unavailable.

---

## 12. Optional execution telemetry

Keep telemetry as one optional EXECUTION object.

Potential values:

```text
model_turns
outer_tool_calls
nested_operations
retries
tokens
context_usage
timing_breakdown
human_interventions
```

Rules:

- record only when naturally available;
- no mandatory Codex/OpenCode/runner instrumentation;
- no telemetry value is required for a valid attempt;
- preserve distinct units where they differ;
- no complexity score is derived during collection.

A future runner integration may populate this object without changing the evidence model.

---

## 13. Deterministic checks

Deterministic checks are part of the execution attempt.

Store them inline:

```text
execution.checks[]
```

Each check may preserve facts such as:

```text
command
started_at
finished_at
exit_code
status
relevant raw/result refs when useful
```

Do not create a first-class `CheckObservation` model or separate check namespace unless future operational requirements justify it.

---

## 14. Repository state

Reuse the existing Git-based before/after snapshot mechanism.

PRE-RUN and POST-RUN states must permit future deterministic derivation of:

- changed files;
- added/deleted files;
- diff/patch size;
- line additions/deletions;
- affected areas;
- future repository features.

Do not calculate all of those values during collection.

### Remote-storage limitation

A local Git tree/ref is not automatically portable to S3.

For now, document that limitation only.

The future remote-storage task must solve reconstructable repository-state portability.

---

## 15. Workflow identity

Reuse the existing workflow fingerprint/version mechanism.

Do not create another one.

---

## 16. Runtime identity

Reuse provider-neutral runtime context as the canonical source for actual execution identity.

Examples:

```text
runner
provider
model
variant
effort
session_id
identity_source
```

Do not rely on model self-reporting.

---

## 17. Assignment provenance

Where known, preserve how the execution profile was selected.

Examples:

```text
manual
default
heuristic
policy
experiment
replay/calibration
```

Unknown remains unknown.

---

## 18. Attempt relationships

Support simple links such as:

```text
retry_of
correction_of
continuation_of
profile_replay_of
calibration_of
```

Attempts remain separate observations.

Task parent/child decomposition relationships remain on task revisions.

---

## 19. Association

An `Association` attaches later evidence to an execution attempt without mutating PRE-RUN history.

Initial important use:

```text
acceptance_review
```

Generic association shape may also support future:

```text
maintainability_review
verification
other review/evaluation artifacts
```

An association can preserve:

- type;
- attempt ref;
- producer;
- durable artifact ref when available;
- factual outcome/status;
- provenance;
- collection time.

The initial implementation only needs to automatically integrate acceptance review. The generic Association model remains capable of representing other review producers later.

No synthetic success score is introduced.

---

## 20. Collector identity

Collector identity remains simple inline metadata:

```text
evidence:
  schema_version: 2
  collector_fingerprint: sha256:...
```

The fingerprint should deterministically cover files/configuration that materially affect evidence semantics.

This is separate from workflow identity.

No first-class `CollectorIdentity` record is required.

---

## 21. Provenance and knowledge status

Preserve meaningful distinctions such as:

```text
observed
mechanically_extracted
planner_declared
planner_estimated
externally_supplied
inferred
unknown
not_applicable
```

Apply provenance where interpretation depends on it.

Do not wrap every scalar in a large provenance structure.

---

## 22. Storage abstraction

Use one small persistence boundary:

```text
EvidenceStore
```

Conceptually sufficient operations are:

```text
put_blob(...)
put_immutable_record(...)
create_attempt(...)
update_active_attempt(...)
finalize_attempt(...)
get_record(...)
record_exists(...)
```

`ProjectSnapshot`, `TaskRevision`, `Association`, and blobs use immutable writes. `ExecutionAttempt` uses the lifecycle-managed operations until finalization.

Initial backend:

```text
GitMetadataEvidenceStore
```

Future:

```text
object-storage backend
```

S3 is a likely implementation target, but the current architecture does not require that class name or provider.

Do not build query/index/database abstractions now.

---

## 23. Artifact capture implementation boundary

Artifact capture is required behavior but does not need its own public module or CLI.

The shared record layer may provide small helpers such as:

```text
capture_artifact(...)
create_project_snapshot(...)
create_task_revision(...)
```

This keeps `run_evidence.py` from owning project/task artifact logic without creating another subsystem prematurely.

If this behavior grows substantially later, it can be extracted then.

---

## 24. Future object storage

Current requirements are only:

- logical IDs independent of absolute paths;
- content-addressed artifact refs;
- immutable records;
- storage behind `EvidenceStore`;
- known repository-snapshot portability limitation.

Do not specify bucket hierarchy, authentication, retry/sync policy, or Git-object transport in this implementation.

Those belong to the future remote-storage task.

---

## 25. Legacy evidence

Existing v1 evidence remains untouched.

Current work does not require:

- migration;
- compatibility reader;
- backfill;
- conversion tests.

If historical v1 data later becomes valuable, a one-off converter may be built then.

---

## 26. Explicit non-goals

Do not implement now:

- S3;
- remote sync;
- database/query indexes;
- dataset export;
- semantic similarity;
- TF-IDF;
- embeddings;
- RAG;
- ML models;
- complexity scoring;
- routing;
- AST/dependency/fan-in/fan-out analysis;
- patch metrics calculated at collection time;
- dedicated runtime adapter framework;
- mandatory runner telemetry;
- task-orchestrator redesign;
- maintainability-review integration;
- legacy v1 migration/reader.

---

## 27. Version axes

Document/design-pack version and persisted evidence schema version are separate. A patch such as `1.2.1` does not imply a schema bump beyond `2` unless persisted record compatibility changes.

---

## 28. Architectural invariants

The implementation conforms only if:

1. project artifacts are not copied into every task/attempt;
2. exact historical artifact content remains recoverable;
3. direct tasks work without formal planning artifacts;
4. task revisions can exist without execution attempts;
5. planner-produced structured facts can be preserved without later inference;
6. PRE-RUN cannot be backfilled with POST-RUN knowledge;
7. optional execution conditions remain PRE-RUN;
8. optional telemetry remains non-mandatory;
9. deterministic checks remain raw execution facts;
10. multiple attempts remain separate;
11. acceptance review can attach after execution;
12. workflow/runtime identity reuse existing mechanisms;
13. collector/schema identity is reproducible;
14. evidence collection remains best-effort;
15. future storage migration does not require redesigning ProjectSnapshot, TaskRevision, ExecutionAttempt, or Association.
