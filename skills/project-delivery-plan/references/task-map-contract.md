# Task Map Contract

`docs/task-map.json` is a compact machine-readable index of the human-readable `docs/project-plan.md`. It exists so downstream task planning/orchestration can reason about dependencies and system handoffs without reparsing the entire plan.

It is **not** a replacement for the project plan and must not contain task-internal implementation recipes.

## Required top-level shape

```json
{
  "schema_version": "1.0",
  "project": "Example",
  "plan_path": "docs/project-plan.md",
  "capabilities": [],
  "artifacts": [],
  "interfaces": [],
  "invariants": [],
  "flows": [],
  "tasks": [],
  "open_system_questions": []
}
```

## ID conventions

- capabilities: `CAP-001`
- artifacts/state: `ART-001`
- interfaces: `IF-001`
- invariants: `INV-001`
- flows: `FLOW-001`
- tasks: `T-001`

IDs are stable references. Renumber only while the plan is still unconsumed; once tasks/reviews refer to them, preserve IDs and supersede content deliberately.

## Capability object

```json
{
  "id": "CAP-001",
  "name": "...",
  "outcome": "...",
  "flows": ["FLOW-001"]
}
```

## Artifact object

```json
{
  "id": "ART-001",
  "name": "...",
  "kind": "persisted|derived|request|response|audit|configuration|other",
  "source_of_truth": "...",
  "producer": "task/system/external source description",
  "consumers": ["..."],
  "lifecycle": "..."
}
```

`producer` may name a pre-existing/external source when the project does not create the artifact. Durable artifacts should normally have at least one consumer or an explicit audit/history purpose in `lifecycle`.

## Interface object

```json
{
  "id": "IF-001",
  "name": "...",
  "owner": "...",
  "consumer": "...",
  "inputs": ["ART-001"],
  "outputs": ["ART-002"],
  "contract": "Behaviorally meaningful success/rejection semantics. Exact local DTO/code shape may be delegated."
}
```

## Invariant object

```json
{
  "id": "INV-001",
  "statement": "...",
  "applies_to": ["ART-001", "FLOW-001", "IF-001"],
  "verification": "..."
}
```

## Flow object

```json
{
  "id": "FLOW-001",
  "name": "...",
  "trigger": "...",
  "terminal_outcome": "...",
  "steps": [
    {
      "id": "FLOW-001-S01",
      "actor": "...",
      "action": "...",
      "consumes": ["ART-001"],
      "produces": ["ART-002"],
      "interfaces": ["IF-001"],
      "invariants": ["INV-001"],
      "state_transition": "optional human-readable transition or empty string"
    }
  ]
}
```

Flow steps should expose cross-boundary semantics. Do not encode every internal function call.

## Task object

```json
{
  "id": "T-001",
  "title": "...",
  "outcome": "Observable product/system outcome",
  "depends_on": [],
  "capabilities": ["CAP-001"],
  "flows": ["FLOW-001"],
  "consumes": ["ART-001"],
  "produces": ["ART-002"],
  "interfaces": ["IF-001"],
  "invariants": ["INV-001"],
  "integration_boundary": "What observable boundary proves this task composes with the system",
  "task_planner_context": "Nuances a later strong-reasoning task planner must preserve; no local implementation recipe."
}
```

Task size is intentionally not encoded. A downstream task planner may split a task while preserving these references and semantics.

## Open system question object

```json
{
  "id": "Q-001",
  "question": "...",
  "blocks": ["FLOW-001", "T-003"],
  "owner": "project owner|planner|other authority"
}
```

## Required consistency

The bundled validator checks:

- unique IDs;
- ID prefixes;
- all references resolve;
- task dependency graph has no cycles;
- flow step IDs are unique;
- every capability points to a flow;
- every task maps to at least one capability or flow;
- every task has an integration boundary and task-planner context.

Semantic producer/consumer correctness, coverage, scope fidelity, and planning depth require independent plan verification.
