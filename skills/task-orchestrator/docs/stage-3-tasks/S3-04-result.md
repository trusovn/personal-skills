# S3-04 result — Stage 3 state model

Created at: `2026-07-17T11:26:27Z`; correction updated at:
`2026-07-17T12:29:03Z`; reconciliation updated at:
`2026-07-18T13:06:41Z`

Status: `complete` for reconciled submission to a fresh independent acceptance
review. This is implementation evidence, not an acceptance verdict.

## Reconciliation update

- Only the selected task may retain `running`, `awaiting_inspection`, or
  `resumable`; a stopped run retains none of those ownership-bearing states.
- A running ledger requires its active attempt to be the latest attempt in the
  selected task history. A ready ledger exposes exactly the dependency-ready
  unfinished task set.
- Ledger revisions must be positive non-boolean integers and
  `completed_task_ids` must be an array of unique strings.
- Public `update_ledger()` now owns the per-run lock. Command phases that
  already hold that lock call the private `_update_ledger_locked()` helper.
- The initial and post-acceptance exact Git checks are unchanged. Under the
  user-selected bounded S3-04 threat model, coherent replacement of the whole
  mutable closure/evidence family is an explicit S3-05/S3-08 risk; no evidence
  anchor, field, or later-record validator was added here.

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
| `ready` | No selected task or active attempt; exactly the dependency-ready unfinished tasks are persisted `ready`. |
| `running` | One selected `running` task and one active attempt owned only by that task's append-only history and latest in that history. |
| `awaiting_inspection` | One selected task in the same state, no active attempt, a current attempt in history, closure present, and later references ordered. |
| `resumable` | One selected task in the same state with retained attempt history and no active attempt. |
| `finalizing` | One selected task still `awaiting_inspection`, no active attempt, and closure, verification, decision, and operation references present in order. |
| `stopped` | No selected task, active attempt, or ownership-bearing task state; ordered historical evidence may remain. |

New ledgers initialize dependency-ready task entries and the run as `ready`
without selecting or launching work. Selection considers only persisted
`ready` entries in immutable policy order and derives dependency completion
from immutable `completed_task_ids` plus task entries in `accepted`.

Updates require the caller's exact expected revision. Immutable run authority,
task identity/order/authority, and append-only attempt histories are checked
before atomic replacement; stale and invalid persisted updates preserve the
previous ledger bytes. Revisions reject booleans and non-positive integers;
`completed_task_ids` rejects non-array values and duplicate, empty, or
non-string items.

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

The same `RunCommandLock` owns every public `update_ledger()` call. Internal
`run-next` phases use `_update_ledger_locked()` only while that command already
holds the lock, avoiding nested public lock acquisition while keeping the
atomic update rule in one place.

The deterministic process test uses control files and bounded polling. It
proves a second controller loses the held mutation lock before allocation,
then after release observes `running` and cannot allocate or launch another
worker. While the first worker is controlled in its wait phase, a lock-owning
competing update advances the ledger; the first controller then refuses stale
reconciliation and leaves the competing bytes unchanged.

## Verification

| Command | Final result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | reconciliation fail-first: 24 tests with 14 assertion-specific failures for the missing ledger invariants and unchanged-update oracles; final: passed 24 tests |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerContractTest.test_direct_update_ledger_obeys_run_lock` | corrected fail-first oracle reached ledger validation while another process held the lock; final: passed 1 test |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py` | passed 12 tests, including exact accepted identity and drift/tamper denials |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerContractTest.test_preflight_before_mutation_blocks_on_failed_adapter skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_post_acceptance_run_next_launches_next_ready_task` | passed 2 public-flow tests: initial drift denial; accepted-byte drift denial with no adapter/durable mutation; exact-byte restoration then T2 launch |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | passed 42 tests, including direct/public lock ownership, real contention/stale reconciliation, initial drift denial, and accepted T1 followed by T2 |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | passed 100 tests |
| `PYTHONDONTWRITEBYTECODE=1 python3 -c 'import ast; from pathlib import Path; paths=("skills/task-orchestrator/scripts/controller_state.py","skills/task-orchestrator/scripts/controller.py","skills/task-orchestrator/tests/test_controller_state.py","skills/task-orchestrator/tests/test_controller.py"); [ast.parse(Path(path).read_text(), filename=path) for path in paths]'` | passed |
| `python3 -c 'import json; from pathlib import Path; paths=sorted(Path("skills/task-orchestrator").glob("**/*.json")); [json.loads(path.read_text()) for path in paths]; print("parsed", len(paths), "JSON files")'` | passed; parsed 4 JSON files |
| `git diff --check` | passed |

The fresh reconciliation packet is
`/private/tmp/task-orchestrator-preflight/S3-04-reconciliation/execution-packet.md`.
Its pre-edit baselines passed 18 state tests and 41 controller tests. The first
lock test attempt depended on the not-yet-existing production lock class and
failed at its harness; it was corrected before production edits to hold the
real lock file independently, then produced the intended fail-first signal.
After the validator change, one existing transition fixture was made coherent
with the exact-ready-set rule while preserving its transition oracle.

## Residual risks

- The advisory lock is intentionally local to one host and one run directory;
  distributed exclusion remains out of scope.
- Artifact containment and digest validation for the four references remains
  owned by S3-05.
- This correction relies only on the existing controller-owned task baseline
  and closure evidence. A writer that coherently replaces the closure JSON,
  every evidence artifact, and all internal digests is explicitly outside the
  user-selected S3-04 threat model. The independently anchored identity chain
  remains owned by S3-05/S3-08.
- The original S3-04 checkpoint does not retain its first fail-first output;
  this reconciliation separately retained current fail-first evidence for all
  newly reconciled ledger and lock behaviors.
