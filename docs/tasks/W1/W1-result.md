# W1 result — Local evidence storage

Status: `completed` (accepted by independent acceptance review)

## Scope delivered

Exactly the allowed files, no others changed:

- `scripts/evidence_store.py` — `EvidenceStore` boundary + `GitMetadataEvidenceStore` backend
- `tests/test_evidence_store.py` — focused real-filesystem tests
- `scripts/evidence-store.md` — module README (registry-updater reference update)

## Interface and decisions

- The seven approved operations only: `put_blob`, `put_immutable_record`,
  `create_attempt`, `update_active_attempt`, `finalize_attempt`,
  `get_record`, `record_exists`; errors via `EvidenceStoreError`.
- Root: `<absolute-git-dir>/personal-skills/evidence/v2/` (AC-01), resolved
  via `git rev-parse --absolute-git-dir`.
- Blobs: SHA-256 content address at `blobs/sha256/<prefix>/<hash>`; filename
  and source path never affect the reference (AC-02).
- Namespaces: `blob`, `project_snapshot`, `task_revision` (tuple ID),
  `association` (tuple ID), `attempt` — distinct on-disk paths, no aliasing
  of equal logical IDs (AC-06).
- Immutable writes: canonical sorted-key JSON comparison; identical repeat
  idempotent, conflict raises `EvidenceStoreError` and preserves the stored
  value, including for nested JSON with different serialization order (AC-03).
- Attempt lifecycle: create once → update while active → finalize exactly
  once; update, conflicting re-finalization, and identical re-finalization all
  rejected after finalization; distinct attempt IDs may be active
  concurrently; attempts addressed by ID only (AC-04/AC-05).
- Atomic writes: temp file + fsync + `os.replace`; a forced failure before
  replacement leaves the prior target byte-for-byte unchanged or a new target
  absent, with no temp leftovers (AC-07).
- Standard library only; no W2 record semantics, no W3 producer migration
  (AC-08).

## Verification results

Pre-edit baseline (implementer self-preflight, all green):

- `python3 -m unittest tests/test_run_evidence.py -v` — OK
- `python3 -m unittest tests/test_runtime_context.py -v` — OK
- `python3 -m unittest tests/test_workflow_version.py -v` — OK

Fail-first: the new focused tests initially failed because
`scripts/evidence_store.py` did not yet exist (expected red, no weakened
assertions).

Post-edit results (all green):

- `python3 -m unittest tests/test_evidence_store.py -v` — 5 tests OK
- `python3 -m unittest tests/test_run_evidence.py -v` — 15 tests OK
- `python3 -m unittest tests/test_runtime_context.py tests/test_workflow_version.py -v` — 24 tests OK

## Independent acceptance review (fresh reviewer)

Verdict: `ACCEPT`. Targeted adversarial probes independently corroborated:
nested-JSON conflict with differing serialization order, identical
re-finalization rejection, namespace non-aliasing with equal IDs, atomic
failure forced at the real `os.fsync` boundary, and stdlib/scope inspection.
Broad gate (all three existing suites) run after targeted evidence was clean.

## Contract delta for later tasks

- Durable surface: `EvidenceStore` / `GitMetadataEvidenceStore` API and the
  on-disk namespace/lifecycle contract at
  `<git-dir>/personal-skills/evidence/v2/`, consumed by W2 (record layer) and
  W3 (run-evidence migration).
- Plan IDs preserved: architecture §§4–5/22, repo integration §3,
  implementation plan Task 1 / Storage, work-breakdown W1 — materialized as
  planned; no semantic drift.
- No `docs/contracts/` registry exists in this repository; module README
  (`scripts/evidence-store.md`) is the discovery record.