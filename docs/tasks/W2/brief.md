# Task Brief: `W2` — Implement core evidence records and schema

Status: `decomposed`

Task kind: `composite`

## Outcome

A programmatic caller can use one standard-library-only record module and the
v2 schema to capture explicit artifacts, create or reuse deterministic
`ProjectSnapshot` and `TaskRevision` records, and construct valid
`ExecutionAttempt` and `Association` records without skill integration or
knowledge of physical storage paths.

## Direction trace

- Direction contribution: Materialize the approved four-record evidence model
  and explicit-input artifact boundary consumed by W3–W6.
- User-observable effect: No direct workflow effect; enables W3 to produce a
  complete v2 attempt and W4–W6 to emit planning and review evidence without
  inventing another schema.
- Why now: W1 is implemented and accepted; the approved branch sequence places
  W2 before every producer migration or skill integration.
- Direction decisions used:
  `docs/execution-evidence/execution-evidence-collection-contract.v1.2.1.md`;
  `docs/execution-evidence/execution-evidence-architecture.v1.2.1.md`
  §§2, 5–13 and 17–22;
  `docs/execution-evidence/execution-evidence-repo-integration.v1.2.1.md`
  §§2, 4–5 and 20;
  `docs/execution-evidence/execution-evidence-implementation-plan.v1.2.1.md`
  Task 1;
  `docs/execution-evidence/execution-evidence-work-breakdown.v1.2.1.md`
  W0 decisions and W2;
  `docs/execution-evidence/execution-evidence-verification-matrix.v1.2.1.md`
  S-08–S-16 and the record-model portions of A/T/P.
- New direction decisions required: `None`

## Authority and scope

- Authority: the four-document authority chain named by the work breakdown, in
  its stated order; W0, the work breakdown, verification matrix, and accepted
  W1 result refine execution without overriding it.
- Parent plan task / stable refs: implementation-plan Task 1 / Core records,
  artifact capture, TaskRevision planning section, and identity/invariants;
  work-breakdown W2; verification refs S-08–S-16, A-06/A-08–A-11,
  T-04/T-05/T-09, and P-01–P-07.
- Original scope: add `scripts/evidence_records.py`,
  `scripts/execution-evidence.schema.v2.json`, and
  `tests/test_evidence_records.py`; implement only the four approved core
  records, explicit-input artifact helpers, deterministic identities,
  provenance/knowledge status, and collector fingerprint support.
- Out of scope: W3 attempt lifecycle orchestration and `run_evidence.py`
  migration; skill integrations; recursive discovery; planner-prose parsing;
  runner instrumentation; new first-class condition/telemetry/check/collector
  models; third-party dependencies; remote storage; legacy migration;
  derived features, scoring, query layers, and authority-plan edits.

## Execution sizing

- Sizing policy: `default@1`
- Original estimated agent calls: `34`
- Original estimated implementation duration: `105 minutes`
- Original required execution profile: `strong/medium`
- Estimate confidence: `medium`
- Triggered decomposition rules: `max_agent_calls`, `max_duration_minutes`

The estimate covers focused repository discovery, production/schema edits,
task-owned behavioral tests, and implementation verification. It excludes
independent acceptance review and orchestration.

## Decomposition

| Child | Responsibility / owned output | Depends on | Brief |
|---|---|---|---|
| `W2.1` | Explicit artifact capture, canonical identity foundation, `ProjectSnapshot`, and the initial v2 schema/test surface | accepted `W1` | `docs/tasks/W2.1/brief.md` |
| `W2.2` | `TaskRevision`, planning/provenance/decomposition semantics, and corresponding schema/tests | accepted `W2.1` | `docs/tasks/W2.2/brief.md` |
| `W2.3` | `ExecutionAttempt`, `Association`, collector fingerprint closure, and full four-record schema/test integration | accepted `W2.2` | `docs/tasks/W2.3/brief.md` |

## Coverage and closure

- Parent requirement / AC coverage: W2.1 owns ProjectSnapshot identity,
  explicit artifact capture, path independence, canonical serialization, and
  schema/module foundations; W2.2 owns complete TaskRevision identity, optional
  planning fields, provenance, and parent/child history; W2.3 owns attempt and
  association shapes, inline optional sections, attempt relationships,
  collector identity, full-schema closure, and the parent exit criterion.
- Shared artifacts/interfaces/invariants: W2.1 owns the initial public module
  conventions, canonical identity helper, artifact-reference shape, and schema
  envelope. W2.2 and W2.3 may extend those three W2 files only without changing
  already accepted behavior. W2.3 owns the final integrated schema and full
  regression pass.
- Integration closure: W2.3 is the final executable integration child. Its
  verification must exercise all four records together and prove that a caller
  can construct them without physical-path knowledge or skill integration.
- Leaf sizing: W2.1 (`11` calls / `35` minutes), W2.2 (`15` / `40`), and W2.3
  (`15` / `40`) each fit `default@1`; no override applies.

## Expected contract impact

- Plan refs: architecture §§2, 5–13 and 17–22; repo integration §§4–5;
  implementation-plan Task 1; work-breakdown W2 — `materialize`.
- Current contract dependencies: no `docs/contracts/` registry exists. The
  accepted W1 surface is `scripts/evidence_store.py`, with durable execution
  evidence in `docs/tasks/W1/W1-result.md`.
- Expected durable delta: one reusable four-record construction/validation API,
  explicit artifact helpers, deterministic identity semantics, collector
  fingerprint input semantics, and evidence schema v2 for W3–W6.

## Handoff

Implement dependency-ready executable leaves only, in numeric order. Never
hand this composite parent to `bounded-task-implementer`. W2 is complete only
after W2.1, W2.2, and W2.3 each complete their immediate independent
acceptance-review route, with W2.3 providing integration closure.
