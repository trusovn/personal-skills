# T-002.1 maintainability review 02

Reviewer: fresh independent session (did not author any reviewed bytes).
Re-entry review of the corrected bytes after the `maintainability-01.md`
`CHANGES_REQUESTED` verdict. Date: 2026-10-23. Base: staged working tree at
HEAD `4449a3f` (same base as review 01). Read-only except this report.

```text
VERDICT: ACCEPT
ARCHITECTURE_GATE: NOT_AVAILABLE

BLOCKERS: NONE
```

ACCEPT covers maintainability of the submitted bytes only. It is not a
functional or specification verdict; T-002.1 remains unaccepted and T-002.2
remains blocked until the ordered review route completes.

## Finding disposition

1. MNT-01 (from review 01) — three disagreeing authorities for the persisted
   `inputs.json` byte convention (production, contract note, fixture).
   - Current disposition: **resolved/corrected**, verified in the current
     staged bytes.
   - Correction evidence:
     - Production remains the single authority:
       `controller.py` `init_run` writes `inputs.json` through
       `_canonical_record_bytes(inputs)` (`canonical_json(record).encode()`,
       sorted keys, compact separators, no trailing newline) and binds the
       ledger `inputs_sha256` to those exact stored bytes.
     - `persist_ledger_fixture` (`test_controller_state.py:651-655`) now
       writes `controller._canonical_record_bytes(inputs)` and binds
       `inputs_sha256` to the same bytes. The fixture's separate
       serialization rule is removed. All three fixture consumers
       (`:679`, `:840`, `:1241`) exercise the production digest validation
       through `update_ledger` -> `_load_flow_authority` ->
       `load_frozen_inputs`, so any future divergence fails loudly instead
       of passing self-consistently.
     - `controller-contract.md` (Frozen authority, "no trailing newline"
       sentence) now matches production and distinguishes the three
       record-family conventions exactly as production implements them:
       inputs/policy/manifest digests bind canonical JSON without a
       trailing newline (`persist_run_policy` returns
       `sha256_text(canonical_json(policy))`); flow digests bind canonical
       JSON with a trailing newline (`_canonical_flow_bytes`).
     - Byte-convention and digest-binding assertions were added on both a
       real initialized run
       (`test_controller.py:1426-1428` in
       `test_frozen_authority_survives_source_edits`) and on
       fixture-persisted bytes
       (`test_controller_state.py:681-686` in
       `test_rejected_controller_update_leaves_persisted_bytes_unchanged`).
       The digest oracle is computed independently of production.
   - Maintainability effect of the correction: the persisted input-record
     layout now has one producer-owned definition; the next same-kind
     change (for example the T-002.3 input revision) edits one function
     and the fixture follows automatically, instead of requiring
     synchronized edits across three owners.
   - Fresh evidence: the correction's focused pair
     (`test_rejected_controller_update_leaves_persisted_bytes_unchanged`,
     `test_frozen_authority_survives_source_edits`) passes; the owning
     state suite passes 44/44; see environment notes for the controller
     suite.

Review 01's corrected scope retains its evidence: the production scripts,
schemas and examples are unchanged by the correction (the correction
report declares a tests-and-docs-only diff, and the production bytes at the
MNT-01 evidence points match review 01's citations byte-for-byte in
behavior). No new blocker was introduced by the correction: it removed a
duplicated authority, added no abstraction, and its reach into
`controller._canonical_record_bytes` matches the test file's established
direct-module style (`controller._load_flow_authority` is already used at
five sites) while avoiding the inline layout re-derivation that MNT-01
condemned.

## Retraction of review-01 warning content

Review 01 warned that the explicit correction/authorization type clauses
were redundant. That claim is factually wrong for two of the three
sub-items and is retracted: Python dict equality admits `1` for `True` and
`3.0` for `3` (verified live: `{'enabled': 1} == {'enabled': True}` is
`True`; `{'limit': 3.0} == {'limit': 3}` is `True`), so the explicit
`is not True` / `type(...) is not int` clauses at `controller_state.py:125-128`
and `:923-925` do reject inputs that plain dict equality would admit.
They are deliberate validation, not noise. The third sub-item stands (see
warnings).

## WARNINGS

- The frozen eight-stage policy remains encoded in parallel authorities
  (runtime constants, four schemas, four example JSONs, the contract
  note). This is the intended freeze (AC-03) and is cross-checked by tests
  that load examples through runtime validation; successors must still
  synchronize all of them deliberately. (Carried from review 01.)
- `stage_transport_fixture` in `test_controller.py` mutates persisted
  ledger bytes (`selected_task_id`, `current_step`) to bypass the
  not-yet-implemented ready/preflight admission. The seam is documented;
  when T-002.2 implements admission these tests must migrate to the real
  path or they will mask admission regressions. (Carried from review 01.)
- `if "flow" in policy:` at `controller_state.py:931` is always true after
  the missing-field check at `:913-915`. Conceded optional cleanup; validly
  left out of this tests-only correction. Clean up when the file is next
  touched. (Carried from review 01, scope-corrected.)

## REVIEWED

- changed implementation scope (re-entry, corrected bytes):
  `skills/task-orchestrator/tests/test_controller_state.py`
  (`persist_ledger_fixture`; `test_rejected_controller_update_leaves_persisted_bytes_unchanged`),
  `skills/task-orchestrator/tests/test_controller.py`
  (`test_frozen_authority_survives_source_edits` byte/digest assertions),
  `skills/task-orchestrator/docs/tasks/T-002.1/controller-contract.md`
  (byte-convention statements),
  `skills/task-orchestrator/docs/tasks/T-002.1/implementation-report.md`
  (correction record; documentation).
  Unaffected staged scope retains review 01 as current evidence:
  `scripts/controller.py`, `scripts/controller_state.py`, the four changed
  schemas and four current examples. Package planning documents, the
  staged one-line `AGENTS.md` governance deletion, and untracked
  `.DS_Store` files are not attributed to this implementation and were
  not reviewed as task bytes.
- architecture command: NONE. No `.quality/gates.yaml` and no canonical
  gate exist in repository authority; repository policy requires no gate
  for these bytes, so none was created.
- policy/boundary sources: `skills/task-orchestrator/docs/tasks/T-002.1/brief.md`
  (revision 1), `verification.md` (revision 1), `preflight.md`,
  `implementation-report.md` (MNT-01 correction section),
  `controller-contract.md`, `reviews/maintainability-01.md`; `AGENTS.md`;
  testing-discipline guidance (same installation root) for the test assets.

## Environment notes

- Focused correction pair: 2 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`:
  44 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`:
  76 tests, 6 errors and 1 failure, all rooted in the pre-existing
  macOS-only `UnsupportedSandbox: sandbox-exec verification is supported
  only on macOS` limitation (same Linux-host pattern review 01 recorded;
  the implementation report's macOS run passed all 76). Environmental
  functional evidence for discovery, not a maintainability finding.
- Exact git status before this write: 28 porcelain lines (25 staged
  entries plus 3 untracked `.DS_Store`), captured at
  `/tmp/opencode/status-before-mnt02.txt`. After this write the only
  added path is this report file.

## Remaining submission route (named, not executed)

First outstanding stage: fresh independent `task-review-discovery`
evidence. Then the separate fresh `task-acceptance-review` decision.
No `task-contract-registry-updater` stage applies: no contract registry
exists, the brief forbids inventing one, and the correction changed no
executable contract declaration.