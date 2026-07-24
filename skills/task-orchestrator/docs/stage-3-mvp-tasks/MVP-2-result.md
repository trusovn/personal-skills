# MVP-2 Result: Frozen Configurable Flow Contract

Status: `READY_FOR_REVIEW`
Date: 2026-07-24

## Outcome

Implemented the closed, versioned MVP flow contract with controller-owned flow
revisions, one atomic current-flow pointer in run state, a persisted cursor,
finite correction transitions, strict handoff/outcome envelopes, and
cursor-gated existing commands.

The approved threat model trusts the local user, controller process, and
controller-owned run directory. LLM/actor outputs and requested transitions
remain fallible, untrusted data. Deliberate coherent same-user rewriting of all
controller state, controller-source compromise, and host compromise are out of
scope.

The earlier external `.task-orchestrator-authority` head and internal
`flow-anchors` chain have been removed. No signature, key, protected store, or
second authority layer replaces them.

No preflight, semantic-review, correction, acceptance, recovery, or general
workflow adapter was added.

## Flow serialization and authority

The selected profile is resolved from `run-policy.json`, validated, and
serialized as canonical compact JSON with sorted keys and one trailing newline.
Revision files are stored at `flows/flow-NNN.json`.

The run ledger is the single current-flow pointer. Its atomic JSON record
contains:

- `flow_revision`
- `flow_path`
- `flow_sha256`

Initialization writes `flows/flow-001.json` and those three pointer fields in
the ledger inside the temporary run directory, then publishes the complete run
directory by rename.

Every public load validates the ledger, requires `flow_path` to match
`flow_revision`, validates the canonical revision sequence, and requires the
current revision bytes to match `flow_sha256`. At most one canonical
next-revision file may exist as an interrupted publication candidate. Missing,
non-canonical, stale, extra, path-mismatched, or digest-mismatched current-flow
state fails before worker preflight or inspection mutation.

Flow pointer fields are immutable through the general ledger-update path.
Actor handoff and outcome records remain closed objects and reject embedded
flow, permission, task-range, or other authority changes.

Revision files are created exclusively by supported controller operations and
are never overwritten. Prior revision bytes remain present after later
revisions. The trusted local user coherently rewriting controller state is not a
supported detection case.

## Revision publication sequence

At the exact safe task boundary (`ready`, no selected task, active attempt,
active operation, current step, or correction cycle), `revise-flow`:

1. validates and canonicalizes the requested profile;
2. validates the ledger pointer, current revision, and exact revision-file set;
3. returns a byte-identical no-op without a revision or ledger write when the
   requested digest is already current;
4. durably creates the next write-once `flows/flow-NNN.json`; and
5. atomically replaces the ledger once with the new revision, path, and digest.

An interruption before the ledger replacement leaves the old pointer valid and
at most one prepared next revision. Retrying the same flow reuses that exact
candidate and completes publication; requesting a different flow is rejected.
If ledger replacement committed before a later exception was observed,
`revise-flow` reloads the pointer and returns the committed revision instead of
rolling it back.

The focused integration evidence preserves revision 1 bytes, publishes later
revisions, proves the no-op leaves ledger bytes unchanged, rejects revision
during owned work, exercises a real child-process exit before pointer commit,
and verifies current-revision-bound actor selection.

## Cursor and pending-step decisions

- With no selected task, `current_step` is null and `correction_cycle` is zero.
- Selection persists the first enabled step at cycle zero.
- `run-next` launches the existing implementation worker only when the current
  step is `implement`; an unowned pending step returns `pending` without worker
  preflight or launch.
- `inspect` always performs the S3-08 mechanical boundary. It executes
  configured verification only when `verify` is enabled and otherwise records
  `omitted_by_policy`.
- After inspection, the controller advances only across the behavior it owns.
  The persisted decision is derived from the resulting cursor.
- Mechanical eligibility permits `accept`/`accepted` only when that cursor is
  exactly `accept`. A pending `semantic_review` records and returns
  `accepted: false`, exposes no `accept` action or `accepted` transition, and
  retains `semantic_review: not_collected`.
- The same cursor rule denies premature acceptance for every other unowned
  pending step.
- `CHANGES_REQUESTED` begins correction only when configured and below the
  finite limit, increments the cycle exactly once, and returns to fresh
  semantic review without another increment. Exact exhaustion follows the
  persisted stop/escalation route.

## Structured records

Version 1 handoff and outcome validators require exact run, task, flow
revision/digest, step, correction cycle, and actor-role identity. Evidence and
transcript values are safe run-relative references. Raw transcript content and
embedded authority changes are rejected.

The frozen normal outcome spellings are:

- preflight: `ready`, `blocked`, `needs_input`
- implementation/correction: `complete`, `needs_input`, `failed`
- verification: `mechanically_eligible`, `findings`
- semantic review: `ACCEPT`, `CHANGES_REQUESTED`, `INCONCLUSIVE`
- acceptance: `task_accepted`

## Changed files

- `assets/examples/minimal-run-policy.json`
- `assets/examples/fast-local-flow.json`
- `assets/examples/reviewed-flow.json`
- `assets/examples/strong-local-flow.json`
- `assets/run-policy.schema.json`
- `assets/flow-profile.schema.json`
- `assets/handoff.schema.json`
- `assets/step-outcome.schema.json`
- `scripts/controller.py`
- `scripts/controller_state.py`
- `tests/test_controller.py`
- `tests/test_controller_git.py`
- `tests/test_controller_state.py`
- `tests/test_retrieval_surface.py`
- `docs/stage-3-mvp-tasks/MVP-2-flow-contract.md`
- `docs/stage-3-mvp-tasks/MVP-2-result.md`

The pre-existing untracked `.gitignore` is user-owned and was not read, edited,
removed, or added.

## Correction evidence

Fail-first:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerInspectionIntegrationTest.test_inspect_keeps_pending_semantic_review_non_accepting`
  — failed before correction because `inspect` returned `accepted: true` while
  the cursor was `semantic_review`.

Corrected focused and owning evidence:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerInspectionIntegrationTest.test_inspect_keeps_pending_semantic_review_non_accepting`
  — passed, 1 test.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — passed, 40 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_flow_revision_publication_is_atomic_across_process_exit`
  — passed, 1 test after correcting the fault injector to accept the pointer
  helper's keyword arguments.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed, 69 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py`
  — passed, 13 tests; the approved Git fixture scope remains intact.
- `git diff --check`
  — passed.

The first post-correction controller-suite run exposed only the fault-injector
signature mismatch described above; it did not expose a production failure.

### Follow-up correction evidence: F-01 and F-02

F-01 established that persisted verification mode was not controlling the
effective plan. Inspection now derives that plan from the persisted flow step:
`targeted` excludes repository-gate authority even when the run policy contains
a gate, while `targeted_plus_repository_gate` requires and includes the
persisted gate. A missing required gate fails before executor invocation or
record publication.

F-02 established that non-negative but impossible correction cycles passed
ledger validation. One flow-aware cursor validator now rejects steps outside
the selected flow, cycles above its finite limit, disabled or cycle-zero
correction cursors, and nonzero cycles on preflight, implementation, or
verification. The same validator runs at persisted flow-authority loads, pure
cursor transitions, and flow-bound ledger updates. Semantic review and
acceptance may retain a legitimate completed correction cycle through the
configured limit.

Fail-first:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_flow_cursor_rejects_step_cycle_incoherence`
  — failed because no flow-aware cursor validator existed and an over-limit
  pure correction transition did not raise.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_impossible_correction_cycle_fails_before_worker_preflight`
  — failed because `run-next` returned success and launched the worker path for
  cycle 3 under limit 2.
- The preceding reviewer probe is the fail-first evidence for F-01. The new
  inspection tests place an independent assertion at the executor boundary so
  either inclusion of an unauthorized gate or omission of a required gate
  rejects the implementation.

Corrected focused and owning evidence:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_flow_cursor_rejects_step_cycle_incoherence`
  — passed, 1 test.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_impossible_correction_cycle_fails_before_worker_preflight`
  — passed, 1 test, including public authority probes for implementation,
  correction, semantic-review, and acceptance cursors plus zero worker launch.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerInspectionIntegrationTest.test_targeted_verification_excludes_configured_repository_gate`
  — passed, 1 test.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerInspectionIntegrationTest.test_repository_gate_mode_requires_persisted_repository_gate`
  — passed, 1 test with no executor call or run-directory mutation.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — passed, 41 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed, 72 tests.

`skills/task-orchestrator/tests/test_retrieval_surface.py` was not rerun because
this correction changed no schema, example, or retrieval-surface behavior.

The aggregate discovery gate was intentionally not run. The task assigns final
aggregate evidence to the fresh acceptance reviewer.

## Acceptance-criteria disposition

- **AC-01 / AC-02:** Data-defined profiles, frozen mappings, strict runtime
  validation, and profile-owned verification-plan scope remain covered by the
  state and controller suites.
- **AC-03:** Current-flow digest/path/revision inconsistency, impossible
  step/cycle state, and actor authority injection fail closed before public
  adapter work. Coherent full-state same-user rewriting is excluded.
- **AC-04:** The controller preserves write-once revision files, prior bytes,
  safe-boundary publication, atomic pointer commit, interruption retry,
  byte-identical no-op, owned-work denial, and current-revision actor binding.
- **AC-05:** Cursor and correction-cycle transition coverage rejects nonzero
  initial-phase cycles, inactive correction, and every over-limit sibling
  cursor while preserving legitimate fresh-review and acceptance cycles.
- **AC-06:** Pending preflight, verify-off mechanical inspection, and pending
  semantic-review non-acceptance pass.
- **AC-07:** Exact identity, safe references, omitted-by-policy semantics,
  normal result families, and embedded-authority rejection remain passing.
- **AC-08:** Focused owning suites pass. The fresh reviewer owns independent
  corroboration and the aggregate gate.

## Residual risks and next owner

General crash recovery outside the bounded revision publication case,
initialization interruption recovery, migration of pre-MVP run directories,
deliberate coherent same-user state rewriting, controller-source compromise,
and host compromise remain out of scope.

Next: fresh `task-acceptance-review` against the completed working-tree bytes.
