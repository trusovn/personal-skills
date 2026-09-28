# Execution Evidence Collection Contract — Current Scope

## Status

**Version:** 1.2.1  
**Change scope:** consistency clarification over v1.2. No new evidence category is introduced. This patch clarifies attempt finalization, project-snapshot roles, execution-profile roles, TaskRevision identity/provenance, initial review integration scope, and document/schema version separation.

**Purpose:** define the evidence that the `personal-skills` workflow should start preserving now for each task execution.

This document defines **what must be available as the result of the evidence-collection work**.

It does **not** define:

- storage format;
- JSON/schema structure;
- APIs or CLI;
- collector implementation;
- runner integration mechanics;
- feature-extraction logic;
- complexity scoring;
- ML models;
- routing policy.

Those belong to separate implementation or future research work.

---

# 1. Required outcome

After this work, a completed workflow execution should leave enough durable evidence to reconstruct:

1. **what task was given to the executor;**
2. **what was known before execution started;**
3. **what repository state the task was executed against;**
4. **which workflow, execution profile, and relevant execution conditions actually applied;**
5. **how that execution profile was selected, when such information exists;**
6. **what happened during execution at the level of reliably observable facts;**
7. **what repository state resulted;**
8. **what verification, review, or acceptance evidence was later associated with the attempt;**
9. **whether the attempt belongs to a retry, correction, decomposition, calibration, or other related sequence;**
10. **where each recorded fact came from and whether it was observed, declared, estimated, unavailable, or not applicable;**
11. **which evidence schema and collector implementation semantics produced the observation.**

The evidence must preserve enough information for future analysis without requiring reconstruction from conversation history, transient agent context, or human memory.

The immediate objective is raw, reproducible evidence collection rather than a learned grader or new task-complexity mechanism.

---

# 2. Observation boundary

The primary observation unit is an **execution attempt**.

A logical task may therefore have multiple observations:

```text
logical task
    ├── execution attempt A
    ├── execution attempt B
    └── execution attempt C
```

Attempts must remain individually identifiable.

Where known, relationships between attempts must also be preservable, including:

- retry;
- corrective rerun;
- continuation;
- execution under another profile;
- experimental/calibration run;
- parent/child task relationship after decomposition.

A task-level summary may be derived later. It must not replace the underlying attempt-level observations.

---

# 3. Evidence lifecycle

Evidence must remain separated into three semantic stages:

```text
PRE-RUN
EXECUTION
POST-RUN
```

The distinction is part of the data contract, not merely documentation convention.

## 3.1 PRE-RUN

PRE-RUN evidence represents facts available **before implementation begins**.

It must be frozen sufficiently to answer:

> What information could legitimately have been used to make an execution-profile or decomposition decision at that moment?

Post-execution discoveries must never be retroactively inserted into the PRE-RUN representation.

## 3.2 EXECUTION

EXECUTION evidence represents externally observable facts about the attempt while it runs.

These facts describe execution behavior.

They do not constitute task-complexity labels.

## 3.3 POST-RUN

POST-RUN evidence represents facts that became available because execution occurred or because subsequent verification/review occurred.

POST-RUN information may later become:

- training outcomes;
- diagnostic metrics;
- evaluation evidence.

It must not become a prediction input for the same execution attempt.

---

# 4. Required PRE-RUN evidence

## 4.1 Original task input

Every execution attempt must preserve a durable representation of the task supplied to the executor.

The contract must support at least:

```text
formal planned task
standalone direct task
```

A formal task brief, master plan, preflight artifact, or acceptance document must **not** be required.

Standalone execution such as:

```text
"Fix this bug..."
```

is a valid first-class workflow case.

The preserved task representation must make it possible to recover:

- the exact effective request;
- its revision/version where applicable;
- the source from which it came.

Where formal supporting artifacts existed before execution, they may be associated with the attempt without becoming mandatory.

---

## 4.2 Repository state

The PRE-RUN evidence must identify the exact repository state against which execution began.

It must preserve enough durable information to support future deterministic extraction of facts such as:

- available files;
- directory structure;
- relevant file identities;
- repository size/structure;
- test presence;
- configuration presence;
- scoped repository characteristics.

The collection contract should preserve **raw repository state**, not prematurely calculate every possible repository metric.

Metrics such as:

```text
file_count
repository_depth
test_file_count
language_distribution
fan_in
fan_out
dependency_complexity
```

are future derived features unless there is a separate demonstrated operational need to collect them directly.

---

## 4.3 Workflow identity

The observation must identify the workflow/scaffold semantics under which the attempt ran.

Existing workflow-version/fingerprint mechanisms should remain the authoritative source.

The evidence-collection work must not create a second competing workflow-version mechanism.

---

## 4.4 Actual execution profile

The observation must preserve the actual execution configuration when it can be obtained from a trusted runtime source.

This includes the relevant identity of:

- runner;
- provider;
- model;
- model variant where applicable;
- reasoning/effort level;
- execution session or equivalent runtime identity where available.

Unavailable runtime information must be represented as unavailable rather than guessed.

The system must not depend on the executing model self-reporting its own identity.

---

## 4.5 PRE-RUN execution conditions

Where reliable launcher/runtime information is naturally available before implementation begins, the observation should preserve relevant execution conditions that may affect outcome or resource use. These conditions may be stored as a compact optional section of the execution attempt; no separate execution-condition subsystem is required.

Examples include:

- operating system and architecture;
- relevant toolchain/runtime identity;
- available tools or capabilities;
- network availability;
- sandbox/restriction mode;
- approval mode;
- execution budget or timeout;
- whether the attempt is fresh, resumed, or continued;
- references to additional context explicitly supplied at launch.

These facts are part of PRE-RUN evidence because they may explain differences between otherwise similar task executions.

They must come from trusted launcher/runtime/adapter sources where available.

The collection work must **not** require expensive environment discovery or runner-specific instrumentation solely to populate speculative fields.

Unavailable conditions must remain unavailable rather than guessed.

---

# 5. Planning and assignment evidence

## 5.1 Existing planner estimates

If planning already produced estimates such as:

- expected calls;
- expected duration;
- confidence;
- intended model tier;
- reasoning effort;
- split/no-split decision;

those values should be preservable alongside the execution observation.

They are **historical predictions**, not ground-truth complexity labels.

This distinction is important because these predictions can later serve as the baseline against which a learned or deterministic replacement is evaluated.

---


## 5.2 Structured planner context

When planning already produced structured judgments or explicit planning facts before execution, those facts should be preservable in addition to the raw planning artifact.

Potential examples include:

- task type;
- intended scope;
- behavioral scope;
- transformation type;
- known implementation precedent or lack of precedent;
- state or compatibility constraints;
- verification work;
- discovery uncertainty;
- other planner-produced constraints or blockers that materially affect execution.

The initial implementation does **not** need to normalize every potentially useful planning dimension.

It should prioritize a small stable subset and retain the raw planning artifact so richer features can be derived later.

This requirement does **not** mandate a new parser that reconstructs structured fields from task prose after the fact.

The preferred source is the planner or planning step that already knows or explicitly produced the value.

Such values remain planner-declared or planner-estimated evidence. They are not ground-truth complexity labels.

If a planning fact was not produced, it should remain unavailable rather than being invented solely to fill the dataset.

---

## 5.3 Assignment provenance

Where known, the observation must preserve why or by what mechanism the execution profile was selected.

Possible conceptual sources include:

```text
manual
default
heuristic
policy
experiment
replay/calibration
```

The exact taxonomy and representation are implementation decisions.

The architectural requirement is that future data must allow the project to distinguish:

```text
the profile succeeded on this task
```

from:

```text
this profile was systematically selected only for a particular class of tasks
```

This is necessary to make later comparisons between execution profiles interpretable.

---

# 6. Execution evidence

The system should preserve reliably observable execution facts where they are available.

The core contract requires:

- execution start;
- execution finish or termination;
- completion/termination state;
- relevant deterministic verification/check evidence produced during the attempt;
- externally observable failure or interruption information where available.

Additional runner telemetry may be captured when naturally available, including:

- tool calls;
- model turns;
- retries;
- token consumption;
- timing breakdown;
- context usage.

However, such detailed telemetry is **not required to make the initial evidence contract useful**.

The system should not require new complex instrumentation solely to obtain speculative metrics.

Execution telemetry must also preserve semantic distinctions where relevant. For example, a model turn, outer tool call, and nested operation are not automatically the same unit.

The evidence model should provide an optional way for callers or future runner/launcher integrations to supply such telemetry when it is already available. A dedicated adapter framework is not required in the initial implementation, and the common collector should not require runner-specific instrumentation in order for ordinary evidence collection to succeed.

---

# 7. POST-RUN repository evidence

The observation must preserve the repository state after the attempt.

Together, PRE-RUN and POST-RUN repository evidence must make it possible to deterministically derive later:

- changed files;
- added/deleted files;
- repository delta;
- patch size;
- line additions/deletions;
- affected areas.

Those derived values do not need to be first-class collection fields now if the underlying state has been preserved.

Most importantly, such POST-RUN facts must never be treated as PRE-RUN features for the same attempt.

---

# 8. Verification, review, and acceptance evidence

Execution completion and implementation success are separate concepts.

The evidence model must therefore distinguish:

```text
executor finished
```

from:

```text
verification passed
```

from:

```text
independent review accepted the result
```

from:

```text
task was ultimately accepted
```

Where independent verification or review occurs, its outcome should be linkable to the relevant execution attempt.

The evidence model must be capable of representing such links generically. The initial implementation is required to integrate the independent acceptance-review path; additional review producers may adopt the same association mechanism later without changing the contract.

Existing review semantics should be reused rather than replaced by a new evidence-specific success grader.

Absence of independent review must remain:

```text
review outcome unavailable
```

rather than being converted into either success or failure.

No new synthetic `task_complexity` or `success_score` should be introduced as part of this work.

Observed outcomes should remain the primary evidence.

---

# 9. Decomposition and selection history

The dataset must not contain only tasks that eventually reached an executor.

Where task planning produces decomposition, the evidence model must be capable of retaining:

- the original candidate task;
- the fact that it was split;
- resulting child tasks;
- known parent/child relationships;
- candidates that were rejected or never executed where such information exists.

This preserves evidence about tasks filtered by the current sizing policy.

Without this history, the future dataset would contain mostly executable leaves and hide the larger tasks that the existing policy removed before execution, creating selection bias.

---

# 10. Provenance and knowledge status

Recorded values must preserve enough provenance to distinguish their origin.

Where applicable, the evidence should allow later analysis to distinguish:

```text
observed
mechanically extracted
planner-declared
planner-estimated
externally supplied
inferred
unknown
not applicable
```

In particular:

```text
unknown ≠ zero
unknown ≠ false
unknown ≠ not applicable
```

Relevant provenance should allow facts to be traced back to their source context, such as:

- task revision;
- repository revision;
- workflow version;
- execution attempt;
- producing artifact/process;
- collection time.

The observation should also preserve the identity of the evidence-collection semantics themselves. At minimum, future analysis should be able to distinguish observations produced under different evidence schema versions or materially different collector implementations. A deterministic collector implementation fingerprint is preferred over manually maintained per-tool semantic versions where practical.

Collector identity is separate from workflow identity: workflow identity describes the executed workflow/scaffold, while collector identity describes the mechanism that recorded the evidence.

Exact schema design is deferred.

---

# 11. Architectural decisions already established

The following decisions are considered part of the contract because they were already evaluated in the preceding research.

## 11.1 Raw evidence before derived features

Collectors should preserve facts.

They should not produce speculative interpretation such as:

```text
complexity_score = 7.4
task_risk = high
```

unless such a value is itself explicitly being preserved as somebody else's historical prediction.

---

## 11.2 PRE-RUN is a hard information boundary

Anything learned only during or after execution is forbidden as a prediction feature for that same attempt.

The evidence structure must make accidental leakage difficult.

---

## 11.3 Planner judgment is not ground truth

Current estimates and routing recommendations are useful historical signals and baselines.

They are not labels describing the true difficulty of a task.

---

## 11.4 Attempt-level observations are preserved

Retries and repeated execution must not be collapsed prematurely into a single task result.

Future models may need to reason about outcome variability across attempts and execution profiles.

---

## 11.5 Existing identity mechanisms are reused

Workflow-version and runtime-context mechanisms already present in the project remain authoritative.

Evidence collection should reference or reuse them rather than duplicate their semantics.

---

## 11.6 Success is not inferred from lifecycle completion

`completed`, `accepted`, `verification passed`, and `review passed` remain distinct observations.

---

## 11.7 Assignment history must remain observable

Future routing analysis will be biased if the project cannot determine how a profile came to receive a task.

The contract therefore preserves routing/assignment provenance where available.

---

## 11.8 Selection/decomposition history must survive

Tasks filtered or split before execution are valuable evidence and must not disappear merely because no executor ran them.

---

## 11.9 Evidence collection remains best-effort

Optional evidence collection must remain subordinate to execution of the actual task.

Ordinary standalone task execution must not fail solely because optional telemetry cannot be collected, unless a separate explicit workflow or repository contract requires it.

---

## 11.10 Structured planning evidence is preserved at its source when possible

If a planner already knows or emits a structured fact, preserving that fact directly is preferable to asking a later parser or model to infer it from prose.

Raw planning artifacts should still be retained where applicable so future feature extraction remains possible.

---

## 11.11 Naturally available runtime telemetry should be accepted, not required

Runner/launcher adapters may contribute richer execution telemetry when it already exists.

The common evidence contract must remain useful when those adapters provide only partial data or no telemetry at all.

---

## 11.12 Initial implementation should prefer the smallest useful representation

The first implementation should preserve required raw evidence with as few new abstractions and integrations as practical.

In particular:

- optional execution conditions may be an inline PRE-RUN object;
- optional telemetry may be an inline EXECUTION object;
- collector identity may be simple schema-version plus deterministic implementation fingerprint fields;
- deterministic checks may remain embedded in the attempt record;
- generic association support does not require integrating every review type immediately.

The collection contract requires the evidence to be preservable. It does not require a distinct subsystem for every evidence category.

---


## 11.13 Execution-attempt lifecycle and finalization

An execution attempt is not required to be physically immutable from the instant `begin` is recorded.

The required lifecycle semantics are:

```text
begin
  -> PRE-RUN frozen before edits
active
  -> execution facts/checks may accumulate
finish/recover
  -> closure + POST-RUN recorded
finalized
  -> the complete attempt record is immutable
```

The hard requirement is that PRE-RUN cannot be changed after implementation begins.

Project snapshots, task revisions, blobs, and post-run associations may remain immutable records from creation.

---


## 11.14 Document version and evidence schema version are separate

The documentation/design-pack version and the persisted evidence schema version are different version axes.

For example:

```text
design pack: 1.2.1
evidence schema: 2
```

A documentation patch does not require a schema-version change unless persisted record semantics or compatibility actually change.

---

# 12. Explicitly outside the current scope

This work must **not** introduce:

- a learned complexity grader;
- `G1/G2/G3/G4` prediction;
- a new routing algorithm;
- execution-profile recommendation logic;
- semantic-similarity calculation;
- TF-IDF features;
- embeddings;
- vector storage;
- RAG;
- Item Response Theory;
- XGBoost or other ML models;
- repository dependency analysis;
- AST analysis;
- fan-in/fan-out calculation;
- code-complexity scoring;
- manually invented success labels;
- aggregate complexity/risk scores;
- training or evaluation pipelines;
- dashboards or statistical reporting.

These remain potential consumers of the evidence collected here.

---

# 13. Completion criteria

This work is complete when the resulting evidence model can support the following questions for an execution attempt without relying on transient agent memory:

## Before execution

- What exactly was the task?
- Which version/revision of the task was used?
- Which project context was used when the task was planned, when formal planning existed?
- Which project context was effective when execution began?
- What repository state existed?
- What workflow semantics applied?
- What profile did planning recommend, where applicable?
- What execution profile was intended at launch?
- What execution profile actually ran?
- What planning estimates existed?
- What structured planner context existed, if any?
- What relevant execution conditions were known before implementation?
- How was this profile selected, if known?
- Was this task produced by decomposition or related to another attempt?

## During execution

- When did execution begin and end?
- Did it complete, terminate, block, or fail?
- What trustworthy execution/check evidence is available?

## After execution

- What repository state resulted?
- What deterministic delta can later be reconstructed?
- What verification evidence exists?
- What independent review or acceptance evidence exists?
- Was another correction/retry/escalation attempt required?

## Dataset integrity

- Which facts were available before execution?
- Which facts became available only afterwards?
- Which values are observed versus estimated or declared?
- Which data is unavailable rather than zero?
- Can the observation be related to retries, decomposition, calibration, or other execution attempts?
- Which evidence schema and collector implementation semantics produced this observation?

If all of these can be answered from durable evidence, the current collection objective has been achieved.

No proof that the data improves task-complexity prediction is required at this stage.
