# T-004.2 contract/reference synchronization

REFERENCE_UPDATE: UPDATED

Owner: coordinator in the designated project-local
`task-contract-registry-updater` stage, after independent
[maintainability-01](maintainability-01.md) ACCEPT. This synchronization does not
decide functional acceptance.

Reconstructed delta from the submitted controller/state/schema/test bytes and
the consolidated [T-004 contract](../../T-004/controller-contract.md):

- `check_collection` / `check-collection` executes the active observed collector's
  full frozen check plan with separate rerun identity, logs and exclusive replay.
- Existing `observe_operation` admission now binds current independent collection,
  coverage, gaps and findings. It preserves stable finding history/upstream
  dispositions and uses inherited failed-check correction accounting.
- ART-002 exposes collection evidence and truthful drift, ownership, missing
  evidence and exhaustion actions. ART-006 reports evidence without final
  acceptance authority. ART-009 acceptance and completion remain unimplemented.

Changed registry: `docs/contracts/task-orchestrator.json` and regenerated
`docs/contracts/index.json`. Preserved qualified plan identity IF-003 and existing
ART-002; added implemented ART-006 under the same orchestration plan. No intended
plan meaning, official plan, task index or executable contract was changed.

Discovery closure inspected the subsystem record, source skill/current operator
guide, root README/AGENTS, project map and owning architecture map. Updated stale
root README status and architecture-map commands/lifecycle/limitations. No module
README exists. Root AGENTS and project map routing remain accurate. The
implementer separately corrected the operator guide; this stage did not modify
runtime, tests, schema, skill instructions or that guide. Orchestrator is not in
`DEVELOPMENT_SKILL_SOURCES`; shared dependencies are unchanged, so no installer or
active-install refresh is needed.

Validation from repository root, both exit 0:

```text
python3 tools/check_contracts.py --root . --write-index
contract registry OK: 8 subsystem(s), 36 indexed plan ref(s)
python3 tools/check_contracts.py --root .
contract registry OK: 8 subsystem(s), 36 indexed plan ref(s)
git diff --check
```

These are structural/reference checks, not behavioral qualification. Original
B, I05 and reviewer R remain applicable to unchanged implementation bytes.
The existing Linux aggregate failures/skips remain explicit in the implementation
and maintainability reports; synchronization does not waive them.

First outstanding stage: fresh independent `task-review-discovery`, followed by
the separate fresh `task-acceptance-review`. Discovery must corroborate the actual
finite scenarios, inspect decisive logs and record the current aggregate gate.
