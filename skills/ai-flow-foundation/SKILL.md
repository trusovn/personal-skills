---
name: ai-flow-foundation
description: >
  Use during pre-planning foundation work when AI/LLM behavior will participate in the application's
  data or process flow. Establish testable boundaries, deterministic validation, fake/provider seams,
  eval/trace locations, retry/idempotency constraints, and safe side-effect boundaries BEFORE detailed
  prompt/workflow/feature design. Produces docs/ai-foundation.md. Do not use to optimize prompts or
  design detailed agent behavior.
---

# AI Flow Foundation

Create the minimum engineering substrate needed to build and verify software whose behavior includes
LLM/agent/model-dependent steps.

This is a **foundation skill**, not an AI feature-design skill.

## Core stance

- Nondeterministic AI behavior belongs inside a deterministic engineering shell.
- Business correctness around AI boundaries must be testable without calling a live model.
- Model output is untrusted external input until parsed and validated.
- Side effects occur only after deterministic validation/policy checks.
- Persisted state and retries must have explicit semantics.
- Evals and traces are first-class development infrastructure when model quality matters.
- Do not prematurely design the final prompts, agent graph, routing policy, or model choice.

## Inputs

Required:

- `docs/project-charter.md`
- current scaffold/repo

Preferred:

- `docs/foundation-plan.md`
- existing AI/provider client code, if any
- project-provided provider/model constraints

## Output

Create or update:

- `docs/ai-foundation.md`

Optionally add bounded AI-foundation items to `docs/foundation-plan.md`.

This skill records the foundation decisions and prepares their materialization handoff. It does not
implement the adapter, validation, test, retry, or observability seams itself.

## Protocol

### 1. Locate the AI boundary at high level

Describe only the expected structural path:

```text
input
-> deterministic preprocessing
-> AI boundary
-> structured/raw result
-> parser/schema validation
-> deterministic policy/business logic
-> side effect/output
```

If more than one materially different AI boundary is already implied by the high-level goal, list them.
Do not invent future agents/components merely for symmetry.

### 2. Establish provider/model isolation

Choose or confirm a single replaceable boundary for model/provider access.

Foundation should make it possible to:

- call the real provider in integration/manual runs
- substitute a deterministic fake/fixture in tests
- capture model/provider metadata without leaking secrets

Do not lock the application domain directly to one SDK when a small adapter seam is sufficient.

### 3. Establish input/output contracts

For every AI boundary define at foundation level:

- input carrier/type location
- expected output representation
- parser/schema location
- validation failure behavior
- whether free text is actually required

Prefer structured output when downstream code depends on fields/enums/identifiers.

The exact feature schema may remain TBD; the **place and mechanism** for validation must be clear.

### 4. Establish deterministic test seams

The test harness must be able to exercise:

- valid model fixture
- malformed response
- missing required field
- unexpected enum/value
- empty response
- provider error/timeout
- retry/duplicate response where relevant

Do not require live-provider calls for unit tests.

Record:

- fixture/fake location
- injection/override mechanism
- focused AI-boundary test command

### 5. Establish eval infrastructure only when quality is model-dependent

If the project requires judging model output quality rather than only software behavior, define:

- `evals/` or repo-conventional equivalent
- small versioned eval dataset/fixtures
- one eval runner command
- result format
- model/prompt/version metadata captured with results

Do not build a large benchmark harness before the project requires it.

If model quality is not an acceptance dimension, mark eval runner `N/A`; deterministic boundary tests are still required.

### 6. Establish tracing/observability

For AI calls, capture enough structured data to debug failures:

- correlation/run ID
- boundary/operation name
- model/provider identifier
- latency
- status/error class
- parse/validation outcome
- retry count when applicable

Prompt/response capture must respect secrets and project constraints.

Prefer a small structured log/trace seam over a full observability stack unless the scaffold already has one.

### 7. Establish retry, state, and side-effect invariants

Record only what is foundational:

- retryable vs non-retryable provider failures
- idempotency requirement when a retry can repeat downstream work
- persisted state owner, if the AI process is multi-step
- rule that external side effects happen only after validated output/policy checks
- human approval boundary if the project explicitly requires one

Do not design the complete workflow graph here.

### 8. Write `docs/ai-foundation.md`

Use the template.

Mark each item:

- `ESTABLISHED`
- `REUSE`
- `TBD-BY-FEATURE`
- `N/A`

These statuses describe decisions or existing scaffold evidence, not completion of planned
materialization. Anything `TBD-BY-FEATURE` must still identify the safe engineering seam that
`repo-foundation` will materialize.

### 9. Hand off to `repo-foundation`

Complete the template's `Repo-foundation handoff` section.

Prepare a bounded handoff authorizing `repo-foundation` to materialize, as applicable:

- provider adapter/fake seam
- schema/validation package location
- fixture/eval directories
- test command
- minimal logging/trace support
- env/example configuration

Name the affected files, required verification, non-goals, and unresolved values that must remain
unknown. The handoff must not authorize detailed AI product behavior.

Stop after producing the handoff. Do not invoke `repo-foundation` or claim that planned seams have
been implemented or verified; those are responsibilities of the materialization step.

## Definition of Done

- `docs/ai-foundation.md` identifies the provider boundary and the intended adapter location.
- The document defines the output-validation mechanism and its failure behavior.
- The document defines how tests will inject deterministic outputs and where required failure cases
  will be exercised without a live provider.
- Side-effect gates and retry/idempotency expectations are documented where relevant.
- Eval infrastructure is planned only if model quality is actually part of the problem.
- Required debugging metadata and its capture policy are documented.
- The `repo-foundation` handoff bounds the authorized materialization work and its verification.
- No planned seam is represented as implemented or verified without materialization evidence.
- Detailed prompts/workflows remain product-design concerns.

## Anti-patterns

- Calling the provider SDK directly from arbitrary domain code.
- Treating successful JSON parsing as semantic validation.
- Live LLM calls in ordinary unit tests.
- Building a multi-agent framework because the goal mentions AI.
- Adding vector DB/RAG/queue/state machinery before the use case requires it.
- Hiding deterministic business rules inside prompts.
- Retrying a call that can repeat a side effect without idempotency semantics.


<!-- contract-registry-flow:ai-flow-foundation:begin -->
## Contract-discovery handoff

`docs/ai-foundation.md` remains an intended AI-foundation authority, not a live inventory of implemented repository state.

When handing materialization to `repo-foundation`, identify AI seams that should become discoverable through the implemented-contract registry once they actually exist. Typical candidates are provider boundaries, input/output validation boundaries, deterministic fake/substitution seams, persisted-state ownership, side-effect gates, and retry/idempotency semantics when later tasks may depend on them.

Do not register planned AI seams before materialization. Preserve stable project-plan IDs where a materialized AI seam corresponds to one.
<!-- contract-registry-flow:ai-flow-foundation:end -->
