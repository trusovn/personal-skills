# Contract Registry Reference

Use this reference when a repository needs cheap, machine-readable discovery of **currently implemented** reusable system contracts.

## Purpose

The registry answers:

- what reusable capability exists now;
- which subsystem owns it;
- which stable plan IDs it materializes;
- what state or artifact it owns;
- what durable invariants apply;
- where the executable/declarative authority and local module documentation live.

It is a routing and durable-contract memory layer, not an architecture encyclopedia.

## Planned truth vs implemented truth

Keep these authorities separate:

```text
project-plan.md / task-map.json
  = intended coordinated system, including future contracts

docs/contracts/*.json
  = currently implemented reusable contracts

OpenAPI / schemas / package APIs / migrations / code / tests
  = executable/declarative authority and behavioral truth
```

A registry entry must not claim a planned capability exists before it is implemented.

A material semantic mismatch between a planned stable ID and implementation is a planning/implementation defect; do not normalize it by rewriting the registry meaning.

## Files

```text
docs/contracts/
  index.json                # generated discovery router
  <subsystem>.json          # canonical current-state subsystem records
```

`index.json` should be deterministically regenerated from subsystem records. This avoids asking an agent to synchronize the same facts twice.

## Subsystem records

Keep records sparse. Recommended top-level fields are:

- `schema_version`;
- `id`;
- `summary` when useful;
- `owner_paths`;
- `provides`;
- `artifacts`;
- `state_owned`;
- `invariants`;
- `depends_on`;
- `module_docs`.

Contract-bearing entries may include:

- `name`;
- `kind`;
- short `summary`;
- `plan_refs`;
- local repository `declarations`.

Descriptions should identify observable/reusable semantics, not implementation design.

## Inclusion threshold

Record a surface when later work may legitimately depend on it without first reverse-engineering its implementation.

Good candidates:

- public/cross-module service interfaces;
- durable domain artifacts;
- events/messages;
- persisted state ownership;
- reusable configuration surfaces;
- reusable test/infrastructure seams;
- lifecycle/state-machine contracts;
- integration boundaries;
- stable invariants.

Exclude:

- private helpers;
- incidental implementation classes;
- algorithms;
- ordinary internal refactors;
- transient file structure;
- historical rationale.

## Stable plan references

When a contract materializes an ID already assigned by project planning, preserve it in `plan_refs`, for example:

```json
{
  "name": "AnalysisResultReader",
  "kind": "service",
  "plan_refs": ["IF-004"],
  "declarations": ["src/analysis/AnalysisResultReader.ts"]
}
```

This creates a cheap join:

```text
task-map consumes IF-004
  -> index.json plan_refs[IF-004]
  -> analysis.json
  -> declaration / module README
```

Unplanned but legitimate contracts may be registered without fabricated plan IDs.

## Discovery hierarchy

The intended agent path is:

```text
AGENTS.md / CLAUDE.md
  -> docs/contracts/index.json
  -> relevant subsystem record
  -> module README and/or executable declaration
  -> source/tests only as needed
```

Root/project architecture maps remain useful for high-level orientation but should not duplicate the detailed contract registry.

Module READMEs remain useful for local workflow, commands, layout, operational notes, closest precedents, and explanation that does not belong in structured contract data.

## Ownership

During the standard bounded-task flow:

- planner owns intended cross-task contract identity and semantics;
- implementer owns code, tests, and executable/declarative contract bytes;
- `task-contract-registry-updater` owns post-implementation registry/reference synchronization;
- acceptance independently proves expected, actual, declared, and discoverable state agree.

Outside that flow, use the repository's normal stale-document ownership rule.
