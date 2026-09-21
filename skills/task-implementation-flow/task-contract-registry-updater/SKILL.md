---
name: task-contract-registry-updater
description: Synchronize the machine-readable current-state contract registry and stale discovery references after a bounded implementation has passed structural and maintainability review. Use before task acceptance when work may have added, changed, or removed durable cross-task contracts.
---

# Task Contract Registry Updater

Keep implemented system contracts cheap for the next agent to discover without turning the implementation agent into a documentation-maintenance agent.

This is a narrow synchronization role. It does not design architecture, repair production code, reinterpret the plan, or approve the task.

## Position in the standard flow

Run after the implementation bytes have survived the repository's deterministic architecture checks and maintainability review, and before `task-acceptance-review`:

```text
task brief
  -> bounded-task-implementer
  -> architecture gate
  -> task-maintainability-review
  -> task-contract-registry-updater
  -> task-acceptance-review
```

If later review changes production, test, or executable-contract bytes, run this synchronization again before fresh acceptance.

## Authority and inputs

Read only what is necessary:

1. task authority / task brief;
2. the relevant `docs/task-map.json` entry when present;
3. the implementer's handoff, treating it as a claim rather than proof;
4. the scoped diff / changed bytes;
5. `docs/contracts/index.json` and relevant subsystem contract records when present;
6. affected module README files;
7. the root and nearest scoped `AGENTS.md` / `CLAUDE.md` files when their routing or rules may be affected;
8. executable declarations only as needed to understand the implemented boundary.

Use the registry model and inclusion threshold defined by `repo-foundation`; do not assume another skill's installed filesystem path.

## What belongs in the registry

Register only durable surfaces that future tasks may legitimately depend on across task boundaries, such as:

- cross-module/application interfaces;
- durable artifacts or event/message contracts;
- state or persistence ownership;
- configuration or lifecycle surfaces;
- reusable test/infrastructure capabilities;
- stable invariants;
- integration boundaries;
- package/public API boundaries.

Do not register private helpers, incidental classes, ordinary internal refactors, algorithms, or transient file organization.

A useful test is:

> If a future task should not rely on this without understanding its implementation, it normally does not belong in the registry.

## Procedure

### 1. Reconstruct the actual contract delta

Determine independently whether the completed implementation added, changed, or removed any durable cross-task contract. Do not copy the implementer's `Actual contract impact` blindly.

Compare the actual bytes with the expected contract impact and stable plan IDs from the task authority.

If implementation materially changed the semantics of a planned cross-task contract, stop with `BLOCKED`. Do not silently redefine the plan ID.

### 2. Update subsystem contract records

Update only the affected `docs/contracts/<subsystem>.json` files.

Preserve stable plan IDs where they materially correspond to the implemented surface.

Do not invent plan IDs for unplanned but legitimate reusable contracts.

### 3. Regenerate and validate the index

Use the repository's canonical contract-registry command. A repo founded from `repo-foundation` should normally expose an equivalent of:

```bash
python3 tools/check_contracts.py --root . --write-index
python3 tools/check_contracts.py --root .
```

`docs/contracts/index.json` is a deterministic discovery index derived from subsystem records. Prefer regeneration over manual index editing.

### 4. Close stale explanatory references

For each actual contract delta, inspect this discovery closure:

```text
contract delta
  -> owning subsystem registry record
  -> module README
  -> scoped AGENTS.md / CLAUDE.md
  -> root README.md
  -> project/architecture map
```

Edit only surfaces whose existing claims became stale.

Typical behavior:

- module README: update when local public entry points, owned data, invariants, commands, or placement guidance changed;
- scoped agent instructions: update only when routing, placement, ownership, commands, or rules changed;
- root README: update only for project-level usage/orientation changes;
- project/architecture map: update only when its high-level topology/boundary statement became stale.

Do not duplicate the detailed registry into Markdown.

### 5. Re-run registry validation

The registry must be structurally valid and all declared repository paths required by the validator must resolve.

## Hard boundaries

You may edit:

- `docs/contracts/**`;
- affected module `README.md` files;
- affected root/scoped `AGENTS.md` / `CLAUDE.md` files;
- root `README.md` when an existing project-level statement is stale;
- project/architecture maps when an existing high-level statement is stale.

You must not edit:

- production code;
- tests;
- OpenAPI, GraphQL, protobuf, JSON Schema, package exports, public types, CLI/config definitions, migrations, or other executable/declarative implementation contracts;
- project or task plans;
- `docs/task-map.json`;
- task acceptance criteria;
- ADRs or architecture decisions;
- foundation intent documents to make them resemble current state.

Executable/declarative contract omissions route back to `bounded-task-implementer`. Planned/current semantic mismatches route to the appropriate planning owner. Missing or unclear contract-registry foundation routes to `repo-foundation`.

## Result contract

Return exactly one status.

### `REFERENCE_UPDATE: UPDATED`

Include:

- reconstructed contract delta;
- registry files changed;
- explanatory/routing references changed;
- validator command and result;
- any plan IDs preserved.

### `REFERENCE_UPDATE: NO_UPDATE_NEEDED`

Include:

- surfaces checked;
- why no durable cross-task contract or stale discovery reference exists;
- validator result when a registry is present.

### `REFERENCE_UPDATE: BLOCKED`

Include:

- the concrete mismatch;
- why synchronization would require changing implementation, architecture, or intended plan semantics;
- required owner: `implementation`, `planning`, or `repo-foundation`.

Do not repair a blocked problem yourself.
