# T-005.1 receipt — V-02 setup reconstruction

Scenario: one inherited public-boundary case and one unrun handoff reconstructed
from the supplied setup in fresh disposable workspaces (verification `V-02`;
brief AC-01/AC-03/AC-04; S-01). No role call was launched; the unrun handoff
stays unrun with its reason and owner. Commands ran from the repository root
with `python3`; both workspaces lived under `/tmp/opencode` and were disposable.

## Public-boundary case: INV-CASE-01 (`queue-defect`)

Setup command and environment:

```text
EVAL_WORK_ROOT=/tmp/opencode/t0051-v02-public python3 \
  skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py queue-defect
```

Observed staging result: exit 0; a real disposable Git workspace at
`$EVAL_WORK_ROOT/queue-runner` (HEAD `4fd34e16f0fa27869b09fbcc85d7bad930c39982`)
with the staged `docs/tasks/QR-12/brief.md`, the staged public CLI
`src/queue/run_next.py`, its integration test, and the QR-12 preflight packet
(`?? docs/tasks/QR-12/preflight.md` in the staged status). Staged workspace
status before the probe: ` M src/queue/run_next.py`, ` M tests/integration/test_run_next.py`,
`?? docs/tasks/QR-12/preflight.md`.

Public probe (real public CLI boundary; disposable probe state outside the
staged repository, exactly as the fixture's own rules require):

```text
python3 $EVAL_WORK_ROOT/queue-runner/src/queue/run_next.py $EVAL_WORK_ROOT/probe-state.json
```

with `probe-state.json` = `{"tasks": [{"id": "TASK-1", "status": "ready"},
{"id": "TASK-2", "status": "ready"}]}`, invoked twice consecutively.

Observed results:

```text
first invocation  stdout "TASK-1", exit 0
second invocation stdout "",       exit 0   (no claim: TASK-2 stays ready)
state after both invocations: {"tasks": [{"id": "TASK-1", "status": "running"},
                                        {"id": "TASK-2", "status": "ready"}]}
staged workspace status after probe: unchanged (the probe wrote no repository bytes)
```

Oracle and boundary: INV-CASE-01's inherited signal is the public `run-next`
entry point exercised for the first occurrence and the next real occurrence.
The staged implementation reproduces the QR-12 defect at that public
boundary: the first invocation claims and persists `TASK-1`; the second
invocation — the "next real occurrence" with `TASK-2` ready — claims nothing
because a task is already running. The observable is the staged defective
behavior the discovery case is built on, observed at the real CLI/process
boundary; it is not a claim that any agent reviewed it. This probe is
implementation evidence only; the actual discovery/decision role calls belong
to T-005.3.

## Unrun handoff: IFQ-01 (`correction-round`)

Setup command and environment:

```text
EVAL_WORK_ROOT=/tmp/opencode/t0051-v02-handoff python3 \
  skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py correction-round
```

Observed staging result: exit 0; 57 staged files reconstructing the full
input set for the maintainability finding-identity continuity role call:

- `maintainability-correction/` — a real disposable Git workspace with
  `docs/tasks/MNT-42/brief.md`, the prior durable report
  `docs/tasks/MNT-42/reviews/maintainability-01.md` (mentions `MNT-B1`
  through `MNT-B4` and `CHANGES_REQUESTED`; fixture-supplied history, not an
  actual review output), corrected `src/billing/pricing.py`, the remaining
  billing sources/tests, `AGENTS.md`, `.quality/gates.yaml`, and
  `scripts/check-architecture`;
- `task-runs/MNT-42/correction-round-facts.md` — the correction facts the
  next review must preserve finding identity against.

Unrun boundary retained: no `task-maintainability-review` role call was
launched. Reason: the actual role call (maintainability eval case 4 style —
stable finding IDs across a correction round) requires a separately
authorized agent invocation. Owner: T-005.5. The staged prior report and
oracle records are qualification inputs, not durable review reports; the
held-back grading oracle stays outside the reviewer workspace per the
fixture's own contract.

## Evidence limits

Both reconstructions are filesystem/Git proof of supplied setup. No agent
behavior is claimed; no staged record is relabeled as an observed role
output; actual role compliance for both cases remains unrun and owned by
the consuming leaves (T-005.3 for INV-CASE-01, T-005.5 for IFQ-01).