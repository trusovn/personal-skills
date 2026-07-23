# Stage 3 Tasks 04–08 Planning Review

| Field | Value |
|---|---|
| Status / owner | `complete` / Codex planning review |
| Dependencies | S3-01 through S3-03 results and corrected S3-03 boundary |
| Execution | `strong` agent; `high` reasoning |
| Review | `immediate` |
| Budget | `30 tool calls / 90 minutes / 100k context` |

## Outcome

Review S3-04 through S3-08 against the completed S3-01 through S3-03 results,
challenge their architecture and ordering, add execution metadata, and make the
required positive, negative, and integration evidence explicit.

## Pre-edit verdict

Verdict: `CHANGES REQUESTED`.

### [P0] Stage 2 closure evidence cannot prove exact pre-verification worktree identity

`capture_closure_evidence()` computes the evidence digest from name/status,
statistics, allowed-path patch data, and selected classifications, but does not
bind the canonical `capture_git_status()` mapping. An unexpected or
pre-existing dirty file can change content while retaining the same path and
similar summary/statistics. S3-08 therefore could not reliably prove that the
worktree still matched the terminal worker closure before running verification.

The revised plan makes an exact HEAD/index/canonical-status identity a required
new closure field, tests same-path/same-size substitution, and fails closed for
older closure records rather than rewriting them.

### [P0] Atomic ledger replacement does not serialize controller processes

The prior plan relied on coherent state and compare-and-swap language without a
real conditional filesystem write or controller lock. Two CLI processes could
read the same revision and each perform an authorized-looking side effect.

S3-04 now owns a local per-run mutation lock plus expected-revision checks.
`run-next` may release the lock only after its running attempt is durable so a
later `stop` can act; terminal reconciliation must reacquire and reject a stale
state rather than overwriting it.

### [P1] The proposed identity was cyclic and mixed pure validation with I/O

S3-05 asked for one identity containing a verification digest while also using
that identity inside the verification record. It also called validators pure
while requiring file existence and digest reads, and asked the task to enforce
publication while prohibiting publication.

The revised contract is acyclic: attempt/turn -> closure -> command execution
-> final verification -> decision -> operation. Structural validation remains
pure; each writer owns containment, bytes, digest, exclusive-create, and replay
integration evidence.

### [P1] Executor and inspector ownership made post-Git evidence impossible

S3-07 was expected to publish a complete verification record but was forbidden
to inspect Git; S3-08 was expected to add post-verification drift afterward.
That either required an unnecessary callback abstraction or an incomplete
record.

The executor now publishes a command-execution record and logs. `inspect`
captures Git before/after and publishes the final verification record that
references the execution digest.

### [P1] Multi-file publication was incorrectly described as atomic

A verification record, decision record, and ledger update cannot be one atomic
filesystem operation. A crash could leave any prefix of those effects and a
naive rerun could execute checks twice or publish contradictory evidence.

S3-08 now uses ordered exclusive writes with exact reuse: execution, final
verification, decision, then locked ledger references. Tests inject a stop
after every boundary and prove that commands are not rerun.

### [P1] State and selection contracts did not cover recovery or a second task

The prior run-state list omitted `resumable`, although later tasks require it,
and `select_task()` currently accepts only the initial state. The plan did not
separate immutable manifest-completed IDs from tasks accepted during the run.

S3-04 now defines exhaustive run/task transitions, coherent fixtures for every
state, initial and post-acceptance readiness/selection, immutable manifest
completion authority, and append-only attempt/task identity.

### [P1] Dependency-install denial overclaimed argv inspection

An argv denylist cannot prove that arbitrary test code will not install a
dependency. The prior wording risked treating a heuristic as a sandbox.

S3-06 now requires a closed, reviewable top-level explicit-install rule and
states its limitation. The filesystem/network boundary and post-verification
Git drift remain separate controls. If an exact version 1 rule cannot be
stated, the stage stops instead of silently weakening policy.

### [P2] S3-06 was unnecessarily serialized behind S3-05

Command planning needs the completed S3-01 sandbox decision and S3-02 module
boundary, not Stage 3 record validators. The revised graph makes S3-04 and
S3-06 independently ready; S3-05 and S3-06 converge at S3-07.

## Architecture decision

Keep the current functional modules. Do not add a record package, storage
layer, workflow engine, or separate command-plan module.

- `controller_state.py`: pure state, identity, and record contracts.
- `controller_git.py`: observation and later exact-path commit mechanics,
  without policy interpretation.
- `verification_runner.py`: pure plan construction plus sandboxed command
  execution.
- `controller.py`: locked CLI use cases, ordered publication, and policy
  decisions.
- `codex_worker.py`: worker transport/process lifecycle.

This is smaller than introducing generalized persistence or callbacks while
still making crash and concurrency boundaries explicit.

## Test-planning result

Each revised brief now distinguishes positive and negative evidence. The real
boundaries are assigned as follows:

| Task | Lowest decisive evidence | Required integration boundary |
|---|---|---|
| S3-04 | exhaustive pure transition/coherence tables | two local controller processes contend for one run lock; stale reconciliation cannot overwrite |
| S3-05 | strict pure record/identity fixtures | intentionally deferred to each record writer; no mocked filesystem proof |
| S3-06 | pure command normalization/provenance and deny-rule tables | none; existing S3-01 capability tests remain green |
| S3-07 | command plan/execution outcomes and immutable byte logs | real local subprocess groups plus production `sandbox-exec` write/network controls |
| S3-08 | decision matrix and replay state machine | temporary Git run through closure, executor, final verification, decision, and ledger references |

## Files changed

- `docs/stage-3-plan.md`
- `docs/stage-3-tasks/S3-04-stage-3-state-model.md`
- `docs/stage-3-tasks/S3-05-record-and-identity-contracts.md`
- `docs/stage-3-tasks/S3-06-verification-command-plan.md`
- `docs/stage-3-tasks/S3-07-verification-executor.md`
- `docs/stage-3-tasks/S3-08-inspect-and-decide.md`
- this review record

No production code, tests, schemas, completed result, direction, or later task
brief was changed.

## Verification

- `rg` confirmed that each S3-04 through S3-08 brief has exactly the requested
  `agent_tier`, `reasoning`, `review`, and `budget` keys.
- `rg` confirmed a positive and negative evidence section in every reviewed
  brief and the revised dependency headers match the master task table.
- The task-scoped diff contains only the master plan, five reviewed briefs, and
  this review record. Pre-existing untracked `AGENTS.md` and
  `agent-output.analysis.md` were preserved and not edited.
- `git diff --check` passed for tracked changes. The no-index whitespace check
  for this new review record emitted no error; its exit status is nonzero only
  because the file is new.
- Runtime tests were not run because this change edits planning documents only.
  Each future task now names its narrow behavioral test, owning suite,
  integration boundary where applicable, aggregate suite, and diff check.

## Post-edit verdict

Verdict: `APPROVE` for implementation in dependency order.

S3-04 and S3-06 are independently ready. With one shared worktree, prefer
S3-04 first because its state, revision, and mutation-lock contract protects
every later CLI side effect; S3-06 can follow without waiting for S3-05.

Residual risks are explicit rather than silently resolved: the exact top-level
dependency-install table still needs immediate review in S3-06, older closure
records without a canonical status digest are not inspectable, and the local
run lock is single-host rather than distributed. The briefs require a stop if
any of those narrower contracts cannot be met.
