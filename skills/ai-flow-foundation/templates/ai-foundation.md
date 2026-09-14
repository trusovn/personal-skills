# AI Flow Foundation

## AI boundaries

| Boundary | Purpose | Provider seam | Input contract | Output validation | Status |
|---|---|---|---|---|---|
| | | | | | ESTABLISHED/REUSE/TBD-BY-FEATURE/N/A |

## Deterministic shell

```text
input
-> deterministic preprocessing
-> AI boundary
-> parse/schema validation
-> deterministic policy/business logic
-> side effect/output
```

## Provider/model access
- Adapter/interface:
- Real-provider implementation:
- Test fake/fixture implementation:
- Configuration source:
- Secret handling:

## Validation
- Structured-output mechanism:
- Schema/parser location:
- Invalid-output behavior:

## Test seams
- Fixtures/fakes:
- Injection mechanism:
- Focused test command:
- Required failure fixtures:
  - malformed
  - missing field
  - unexpected value
  - empty
  - provider error/timeout
  - retry/duplicate, if applicable

## Evals
- Needed for acceptance: yes/no
- Eval dataset:
- Eval command:
- Result format:
- Captured version metadata:

## Observability
- Correlation/run ID:
- Operation/boundary:
- Provider/model:
- Latency/status:
- Validation result:
- Retry count:
- Prompt/response capture policy:

## Retry/state/side effects
- Retry policy:
- Idempotency boundary:
- Persisted state owner:
- Side-effect gate:
- Human approval: N/A / <boundary>

## Repo-foundation handoff

- Status: READY / BLOCKED
- Authority artifacts: <project charter, foundation plan, or approved equivalents>

### Established or reused behavior

| Concern | Evidence | Status |
|---|---|---|
| <provider runner, validation, tests, tracing, etc.> | <path and observed behavior> | ESTABLISHED/REUSE |

### Gaps requiring materialization

| Authorized change | Files likely affected | Verification |
|---|---|---|
| <smallest required foundation change> | <paths> | <command or observable DoD> |

### Handoff constraints

- Non-goals:
- Values that must remain unknown:
- Blockers: N/A / <missing authority or prerequisite>

## Deferred to feature design
- <prompt contents, detailed routing, workflow graph, feature schemas, etc.>
