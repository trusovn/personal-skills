# Project Plan Review

Verdict: `ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE`
Review date/session: `<...>`

## Reviewed bytes

- `docs/project-plan.md` SHA-256: `<digest>`
- `docs/task-map.json` SHA-256: `<digest>`
- Repository revision/worktree note: `<commit / dirty-state note if material>`

## Authoritative sources reviewed

- `<approved proposal / project charter / AI foundation / readiness report / repo rules>`

## Independent reconstruction

### Product outcome
<Reviewer reconstruction from upstream authority, not copied from plan.>

### Required capabilities / critical journeys
- `<...>`

### Explicit non-goals / constraints
- `<...>`

## Structural checks

- Bundled verifier: `PASS | FAIL`
- Reference integrity: `PASS | FAIL`
- Task dependency graph: `PASS | FAIL`

## Coverage summary

| Area | Result | Notes |
|---|---|---|
| Scope fidelity | PASS / FAIL | ... |
| End-to-end flow completeness | PASS / FAIL | ... |
| Artifact producer/consumer closure | PASS / FAIL | ... |
| State/lifecycle semantics | PASS / FAIL | ... |
| Interface contracts | PASS / FAIL | ... |
| Cross-task invariants | PASS / FAIL | ... |
| Capability/task coverage | PASS / FAIL | ... |
| Dependency/order composition | PASS / FAIL | ... |
| Verification coverage | PASS / FAIL | ... |
| Planning abstraction | PASS / FAIL | ... |

## Findings

### F-001 — `<short title>`

Severity: `BLOCKER | MAJOR | MINOR | NOTE`  
Affected IDs: `<FLOW-..., ART-..., IF-..., INV-..., T-...>`

**Gap / contradiction**  
...

**Why it matters / failure scenario**  
...

**Smallest plan-level correction**  
...

Repeat as needed. If there are no findings, write `None`.

## Producer/consumer exceptions checked

List any apparently terminal artifacts and why they are legitimate (for example immutable audit history), plus any external/pre-existing producers that are intentionally outside project tasks.

## Open system questions

- `<question and whether it blocks ACCEPT>`

## Verdict rationale

<Concise explanation tied to the severity rules.>

## Next action

- `ACCEPT`: feed the verified plan/task map into downstream task planning.
- `CHANGES_REQUESTED`: return findings to the project planner; rerun this review on corrected bytes with a fresh reviewer.
- `INCONCLUSIVE`: obtain the missing authority/evidence or a truly independent reviewer, then rerun.
