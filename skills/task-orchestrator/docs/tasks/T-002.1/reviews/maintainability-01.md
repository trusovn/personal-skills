# T-002.1 maintainability review 01

Reviewer: fresh independent session (did not author any reviewed bytes).
Date: 2026-10-23. Base: staged working tree at HEAD `4449a3f`.
Skill: task-maintainability-review (project-local flow). Read-only except this report.

```text
VERDICT: CHANGES_REQUESTED
ARCHITECTURE_GATE: NOT_AVAILABLE

BLOCKERS:
1. MNT-01 — skills/task-orchestrator/scripts/controller.py :438-439 and :421,
   skills/task-orchestrator/docs/tasks/T-002.1/controller-contract.md :46-48,
   skills/task-orchestrator/tests/test_controller_state.py :645-652
   - Problem: The persisted `inputs.json` byte convention is now three
     authorities that disagree. Production `init_run` writes
     `_canonical_record_bytes(inputs)` = `canonical_json(inputs).encode()`
     (canonical JSON, no trailing newline). The new contract note states
     "Input JSON uses sorted keys, compact separators and a final newline",
     and the new `persist_ledger_fixture` test helper writes
     `(controller.canonical_json(inputs) + "\n").encode()` (trailing newline).
   - Evidence: controller.py `_canonical_record_bytes` returns
     `canonical_json(record).encode()`; `init_run` writes that to `inputs.json`
     and binds `inputs_sha256` to its raw bytes. Contract note line 46-48
     claims a final newline. Fixture line 651 appends `+ "\n"` and computes its
     digest from its own bytes, so its tests stay green while exercising a
     layout production never emits.
   - Maintainability impact: the contract note is the frozen implemented
     contract consumed by T-002.2 via IF-001; a wrong persisted-byte statement
     misleads reservation/revision successors. The fixture becomes a second,
     unchecked authority for the input-record layout that R2 (frozen input
     identity) protects, and will silently drift when T-002.3 revises
     inputs.json. Digest binding is per-run self-consistent, so the divergence
     does not fail today but guarantees future coordinated edits across three
     owners.
   - Smallest correction direction: pick one convention and align all three —
     either append the trailing newline in production (`_canonical_record_bytes`
     or the `inputs.json` write), or drop the newline from the fixture and the
     contract sentence. Do not change digest semantics; keep raw-byte binding.
   - Current disposition: confirmed.

WARNINGS:
- The frozen eight-stage policy is now encoded in six parallel authorities:
  runtime constants (`controller_state.py`), four schemas, four example JSONs,
  and the contract note. This is the intended freeze (AC-03) and is
  cross-checked by tests that load examples through runtime validation, but
  successors have no single source of truth for stage/role/mode policy and must
  deliberately synchronize all of them.
- `stage_transport_fixture` in test_controller.py mutates persisted ledger
  bytes (`selected_task_id`, `current_step`) to bypass the not-yet-implemented
  ready/preflight admission. The seam is documented and the real pending-stage
  path is tested separately, but when T-002.2 implements admission these tests
  must migrate to the real path or they will mask admission regressions.
- Redundant validation clauses add noise without effect: the correction dict
  check in `validate_flow_profile` and the `execution_authorization` check in
  `validate_run_policy` each carry a second condition that can never evaluate
  differently from the first; `if "flow" in policy:` in `validate_run_policy`
  is always true after the missing-field check. Not defects; clean up when the
  files are next touched.

REVIEWED:
- changed implementation scope: skills/task-orchestrator/scripts/controller.py,
  skills/task-orchestrator/scripts/controller_state.py,
  skills/task-orchestrator/assets/{flow-profile,run-policy,handoff,step-outcome}.schema.json,
  skills/task-orchestrator/assets/examples/{fast-local-flow,reviewed-flow,strong-local-flow,minimal-run-policy}.json,
  skills/task-orchestrator/tests/test_controller.py,
  skills/task-orchestrator/tests/test_controller_state.py,
  skills/task-orchestrator/docs/tasks/T-002.1/controller-contract.md
  (all as staged at HEAD 4449a3f; package planning docs, the staged AGENTS.md
  one-line governance deletion, and untracked planning packages are not
  attributed to this implementation and were not reviewed as task bytes).
- architecture command: NONE. No `.quality/gates.yaml`, no canonical gate in
  AGENTS.md or repo docs; `architecture-guardrails` provides only an unused
  template. Repo policy requires no gate for these bytes, so none was created.
- policy/boundary sources: skills/task-orchestrator/docs/tasks/T-002.1/brief.md
  (rev 1), verification.md (rev 1), preflight.md, implementation-report.md,
  controller-contract.md; AGENTS.md.

ENVIRONMENT NOTES:
- On this Linux host `python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  passes (44 tests). `.../test_controller.py` runs 76 tests with 6 errors and 1
  failure, all rooted in the pre-existing macOS-only
  `UnsupportedSandbox: sandbox-exec verification is supported only on macOS`
  limitation documented in preflight.md (which recorded 6 environmental
  failures; the crash-replay case now surfaces as a failure of the same root
  cause). This is functional evidence for discovery, not a maintainability
  finding; `verification_runner.py` is out of this leaf's scope.
- `jsonschema` is not installed on this host, so the supplemental schema/example
  structural check from the implementation report could not be reproduced here.
- Exact git status before this write: 27 porcelain lines (captured in
  /tmp/opencode/status-before-review.txt). After this write the only added path
  is this report file.
