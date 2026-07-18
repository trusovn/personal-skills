# S3-04 result — Stage 3 state model

Created at: `2026-07-17T11:26:27Z`; correction updated at:
`2026-07-17T12:29:03Z`

Status: `complete` for corrected submission to independent acceptance review.
All three acceptance findings are corrected and verified; this is implementation
evidence, not an acceptance verdict.

## Acceptance correction

- Ledger updates reject caller ownership of `revision` and derive `N + 1`
  exclusively from the validated persisted revision.
- The pure and persisted update boundary enforces every changed run/task state
  through the frozen transition tables. Acceptance additionally requires an
  accepting closure decision whose identity matches the run, task, and latest
  attempt.
- A repeated `run-next` keeps the original initial-baseline guard until a task
  is accepted. After acceptance it validates the latest accepted task's exact
  controller-owned baseline and closure evidence before adapter preflight,
  selection, baseline creation, or ledger mutation. The comparison binds HEAD,
  index tree, content-hashed pre-existing status, exact allowed-path binary
  patch bytes, untracked paths, artifact digests, and the closure evidence
  digest. No field or later-record validator was added.
- A real two-task public regression now accepts T1's unchanged ordinary output
  and launches persisted-ready T2. Focused temporary-Git cases reject same-path
  same-size content substitution, pre-existing dirty changes, unexpected paths,
  index/HEAD changes, and closure artifact tampering.

## Transition contracts

| Run state | Allowed next states |
|---|---|
| `initialized` | `ready`, `stopped` |
| `ready` | `running`, `stopped` |
| `running` | `awaiting_inspection`, `resumable`, `stopped` |
| `awaiting_inspection` | `resumable`, `finalizing`, `stopped` |
| `resumable` | `running`, `stopped` |
| `finalizing` | `ready`, `stopped` |
| `stopped` | none |

| Task state | Allowed next states |
|---|---|
| `initialized` | `ready`, `stopped` |
| `ready` | `running`, `stopped` |
| `running` | `awaiting_inspection`, `resumable`, `stopped` |
| `awaiting_inspection` | `accepted`, `resumable`, `stopped` |
| `resumable` | `running`, `stopped` |
| `accepted` | none |
| `stopped` | none |

Both tables are executable through the pure state module and retained
controller compatibility names. Task-local tests iterate every listed and
unlisted edge, including both terminal task states and terminal run state.

## Ledger coherence and selection

| Run state | Enforced coherence |
|---|---|
| `initialized` | No selected task or active attempt; all four Stage 3 references are null. |
| `ready` | No selected task or active attempt; at least one persisted task is `ready`. |
| `running` | One selected `running` task and one active attempt owned only by that task's append-only history. |
| `awaiting_inspection` | One selected task in the same state, no active attempt, a current attempt in history, closure present, and later references ordered. |
| `resumable` | One selected task in the same state with retained attempt history and no active attempt. |
| `finalizing` | One selected task still `awaiting_inspection`, no active attempt, and closure, verification, decision, and operation references present in order. |
| `stopped` | No selected task or active attempt; ordered historical evidence may remain. |

New ledgers initialize dependency-ready task entries and the run as `ready`
without selecting or launching work. Selection considers only persisted
`ready` entries in immutable policy order and derives dependency completion
from immutable `completed_task_ids` plus task entries in `accepted`.

Updates require the caller's exact expected revision. Immutable run authority,
task identity/order/authority, and append-only attempt histories are checked
before atomic replacement; stale and invalid persisted updates preserve the
previous ledger bytes.

## Reference compatibility

New ledgers contain exactly the four authorized nullable references:
`last_closure_path`, `last_verification_path`, `last_decision_path`, and
`active_operation_path`. Existing compatibility imports remain in
`controller.py`. This task does not migrate or rewrite existing ledgers and
does not validate the referenced artifact bytes owned by S3-05.

## Lock ownership and lifetime

`run-next` opens the run-contained `controller.lock` and takes an exclusive,
non-blocking `fcntl.flock`. The descriptor remains held through ledger and
authority validation, task selection, baseline/artifact creation, attempt
allocation, and the durable `running` revision. The lock is released only
while the owned worker runs. Before terminal reconciliation the controller
reacquires the same lock, rereads the ledger, and compares the exact running
revision, run state, selected task, and active attempt. A mismatch refuses
stale reconciliation without writing.

The deterministic process test uses control files and bounded polling. It
proves a second controller loses the held mutation lock before allocation,
then after release observes `running` and cannot allocate or launch another
worker. While the first worker is controlled in its wait phase, a lock-owning
competing update advances the ledger; the first controller then refuses stale
reconciliation and leaves the competing bytes unchanged.

## Verification

| Command | Final result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | fail-first: 41 tests with the intended second-occurrence initial-baseline failure; final: passed 41 tests |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py` | passed 12 tests, including exact accepted identity and drift/tamper denials |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | first-correction fail-first: 18 tests with 3 expected failures; final: passed 18 tests |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | passed 93 tests |
| `PYTHONDONTWRITEBYTECODE=1 python3 -c 'import ast; from pathlib import Path; paths=("skills/task-orchestrator/scripts/controller_state.py","skills/task-orchestrator/scripts/controller.py","skills/task-orchestrator/tests/test_controller_state.py","skills/task-orchestrator/tests/test_controller.py"); [ast.parse(Path(path).read_text(), filename=path) for path in paths]'` | passed |
| `python3 -c 'import json; from pathlib import Path; paths=sorted(Path("skills/task-orchestrator").glob("**/*.json")); [json.loads(path.read_text()) for path in paths]; print("parsed", len(paths), "JSON files")'` | passed; parsed 4 JSON files |
| `git diff --check` | passed |

The preflight packet already recorded passing baselines for CMD-01 and CMD-05;
the resumed implementation order began with CMD-02 as directed. The prior
checkpoint preserves the earlier partial-thread gate state. During this
resumed segment CMD-03 first exposed three obsolete Stage 2 expectations, then
one assertion failure and one fixture error; both were corrected in the
task-local tests before the passing sequence above.

## Residual risks

- The advisory lock is intentionally local to one host and one run directory;
  distributed exclusion remains out of scope.
- Artifact containment and digest validation for the four references remains
  owned by S3-05.
- This correction relies only on the existing controller-owned task baseline
  and closure evidence. The stronger cross-record identity chain remains owned
  by S3-05/S3-08 and was not pulled into S3-04A.
- The checkpoint does not retain the original fail-first output text, so this
  resumed segment preserves but cannot independently reproduce that pre-change
  evidence without reverting the authorized same-thread production diff.
