# Project Plan — <project>

## Product outcome

<In plain language: who benefits and which concrete situation improves.
Use short sentences and concrete verbs. Explain unfamiliar terms when first
needed. Include the first useful proof or next owner decision when relevant. Cite the
authority below; keep detailed scope in section 2.>

For a multi-task plan, use one readable task-outcome list or table. Reuse an
existing one by linking to it, or place it here:

- [<Readable task name>](#t-001--task-title): <what this gives the owner, who
  needs it next and what it lets them do within the approved sequence>.

Use a title and task names the owner can understand without decoding plan IDs
or workflow jargon. Keep exact IDs and technical detail in the scope, contracts
and evidence below. Preserve required references and task boundaries.
Move or rewrite existing explanations instead of adding another version.
The detailed task map below adds technical placement without repeating outcomes.
Do not create another requirements list or status table. For a small
plan, fold the sequence into the outcome paragraph when that is clearer.
Link to an identified current work report when available; progress belongs in
that report. Retain material unknowns and source conflicts without inventing
purpose, approval, or demonstrated results.

Status: `DRAFT | READY_FOR_PLAN_VERIFICATION | VERIFIED`
Plan version: `<version/date/commit or other project convention>`

## 1. Planning authority

### Authoritative inputs
- `<project charter / approved proposal / foundation review / AI foundation / repo rules>`

### Settled decisions
- `<decision downstream tasks must not reopen>`

## 2. Scope

### In scope
- `<capability/outcome>`

### Non-goals
- `<explicitly excluded behavior>`

## 3. Actors and capabilities

| ID | Actor / capability | Outcome | Critical flows |
|---|---|---|---|
| CAP-001 | ... | ... | FLOW-001 |

## 4. Artifact and state catalog

| ID | Artifact/state | Kind | Source of truth / owner | Produced by | Consumed by | Lifecycle / invalidation |
|---|---|---|---|---|---|---|
| ART-001 | ... | persisted / derived / request / output / audit | ... | ... | ... | ... |

## 5. Lifecycle and decision rules

### <stateful artifact/process>

```text
STATE_A -> STATE_B -> STATE_C
           |-> FAILED
```

Rules:
- `INV-001` ...
- `INV-002` ...

## 6. Cross-task invariants

| ID | Invariant | Applies to artifacts/flows/interfaces | Intended verification |
|---|---|---|---|
| INV-001 | ... | ART-001 / FLOW-001 | ... |

## 7. System interface map

| ID | Boundary / purpose | Owner / producer | Consumer | Inputs | Outputs | Important success + rejection semantics |
|---|---|---|---|---|---|---|
| IF-001 | ... | ... | ... | ART-... | ART-... | ... |

Record authorization, idempotency, concurrency, staleness, validation, or exact-version semantics here when they affect independent work.

## 8. End-to-end flows

### FLOW-001 — <name>

**Trigger:** ...  
**Terminal observable outcome:** ...

| Step | Actor/owner | Process/action | Consumes/reads | Produces/writes | Interface | State transition | Invariants / failure semantics |
|---|---|---|---|---|---|---|---|
| 1 | ... | ... | ART-... | ... | IF-... | ... | INV-... |

**Failure/rejection branches that matter across tasks:**
- ...

Repeat for every critical journey.

## 9. Capability-to-flow coverage

| Capability | Flows | Artifacts | Interfaces | Invariants | Observable completion |
|---|---|---|---|---|---|
| CAP-001 | FLOW-001 | ART-001 | IF-001 | INV-001 | ... |

## 10. Implementation task map

The machine-readable authoritative task map is `docs/task-map.json`. This section is the human-readable view.

Link to the single readable task-outcome view. Keep cross-task placement here.

| Task | Depends on | Flow placement | Consumes | Produces/changes | Interfaces | Invariants | Integration boundary |
|---|---|---|---|---|---|---|---|
| T-001 | ... | FLOW-001 steps 1–3 | ART-... | ART-... | IF-... | INV-... | ... |

### Task-planning handoff notes

For each task, preserve only nuances needed to keep it compatible with the system plan. Leave task-local design/decomposition to the downstream task planner.

### T-001 — <task title>

<Detailed scope and cross-task handoff nuances. Reference the single task
outcome; do not repeat it as another requirement or progress claim.>

## 11. System verification map

| Flow / invariant / interface | Risk | Intended evidence/oracle | Owning task(s) / final integration |
|---|---|---|---|
| FLOW-001 | ... | ... | ... |

## 12. Risks, assumptions and delegated choices

### Blocking/open system questions
- `<question that must be resolved before implementation or verification>`

### Risks
- `<composition / semantic / delivery risk>`

### Intentionally delegated task-local choices
- `DELEGATED:` `<choice safe for owning task to make locally>`

## 13. Plan-verification handoff

Review these artifacts together:
- `docs/project-plan.md`
- `docs/task-map.json`
- authoritative upstream documents listed in section 1

The verifier should independently reconstruct the required end-to-end flows and check the plan rather than trusting this document's own claims of completeness.
