# S3-02: Extract Pure Controller State

Status: ready after Stage 2
Depends on: Stage 2 exit contract
Blocks: S3-03, S3-04

```yaml
agent_tier: standard
reasoning: medium
review: milestone
estimated_budget: 30 tool calls / 90 minutes / 100k context
```

## Outcome

Move the already-pure validation, transition, digest, and ledger-record logic
from `controller.py` into `controller_state.py` without changing observable
behavior or persisted formats. Keep compatibility imports in `controller.py` so
existing callers and tests do not break merely because code moved.

## Required context

Read:

- `docs/stage-3-plan.md` — architecture assessment and execution contract
- `scripts/controller.py` — pure helpers, validators, state transitions, ledger
- `tests/test_controller.py` — tests that directly import those functions

Do not read later Stage 3 task briefs.

## Entry criteria

- The focused controller suite passes before the refactor.
- Stage 2 behavior and record bytes are treated as fixed.
- No pre-existing user edit overlaps the functions being moved.

## Allowed changes

- `scripts/controller.py`
- new `scripts/controller_state.py`
- new `tests/test_controller_state.py`
- `tests/test_controller.py` only to preserve/reduce duplicate coverage

Do not change CLI flags, Git commands, transport calls, JSON shapes, or error
semantics. Do not create classes or a package hierarchy.

## Work

1. Establish the passing controller-test baseline.
2. Before moving code, characterize representative successful outputs and
   rejected inputs for every boundary being moved. Record exact canonical
   JSON/digest outputs and exception type/message where those are part of the
   current behavior.
3. Extract canonical JSON/digest helpers, run-policy and manifest validation,
   pure transition/selection rules, attempt-record validation, and ledger
   validation/update rules that do not execute Git or a worker.
4. Keep atomic persistence ownership explicit; do not create a generalized
   storage abstraction.
5. Re-export names from `controller.py` where existing tests/callers use them.
6. Move focused pure tests into `test_controller_state.py`; keep command-flow
   integration tests in `test_controller.py`.

## Required test evidence

Positive cases:

- Representative valid policy and manifest fixtures validate through
  `controller_state.py` and through retained `controller.py` compatibility
  names.
- Valid selection and transition cases return the same values as the
  pre-extraction characterization.
- Canonical JSON, digest, attempt-record, and ledger fixtures retain exact
  expected values or bytes where persistence depends on them.

Negative cases:

- Representative missing, unknown, duplicate, and wrong-type policy/manifest
  fields remain rejected.
- Invalid graph/path inputs, unavailable task selection, invalid transitions,
  stale closure identity, malformed attempt records, and incoherent ledger
  updates retain the characterized exception type/message; rejected ledger
  updates leave persisted ledger bytes unchanged.
- A direct-import test must fail if `controller_state.py` falls back to the old
  implementations in `controller.py`; compatibility imports may point from
  `controller.py` to `controller_state.py`, never the reverse.

Structural non-duplication in AC-03 is confirmed by task-scoped diff inspection;
do not replace it with a brittle line-count assertion.

## Acceptance criteria

- **AC-01:** Existing Stage 2 controller behavior and public CLI output remain
  unchanged.
- **AC-02:** Pure state tests import `controller_state.py` directly.
- **AC-03:** `controller.py` contains orchestration, not duplicate validator or
  transition implementations.
- **AC-04:** Existing persisted JSON and digest values are byte/semantically
  compatible as applicable.
- **AC-05:** No speculative abstraction or adjacent cleanup is introduced.
- **AC-06:** Positive and negative characterization cases produce the same
  observable results before and after extraction.

## Verification

Before editing, establish the baseline with the existing owning suite:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
```

After extraction, run the new focused suite first, then the unchanged command
and integration coverage:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
```

Then run the aggregate task-orchestrator suite and `git diff --check`.

## Exit and handoff

Report the exact functions moved and compatibility names retained. Stop before
adding any Stage 3 state or record field; S3-04 and S3-05 own those changes.
