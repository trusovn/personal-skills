# W2 Result: Core evidence records and schema

Status: `completed` (W2.3 accepted by independent review)

## Delivered closure

- W2.1 (`6c240f458ffc70012e2e2f2f776346969cd3cf60`) delivered explicit
  artifact capture, canonical identity, `ProjectSnapshot`, and the initial v2
  schema/test surface.
- W2.2 (`4c5e4659bc9ba3292df25f5ad20c86a6134bd42b`) delivered
  `TaskRevision`, planning/provenance/decomposition behavior, and its schema
  and regression coverage.
- W2.3 completed `ExecutionAttempt`, immutable `Association`, deterministic
  collector fingerprints, and the four-record integration closure in the
  three W2-owned files.

The independently reviewed staged W2.3 byte set has diff SHA-256
`99aad97054c41fc45a22594c649776a97f57b1c9d5eb19ff6ebeff6b310490a7`.
It is limited to `scripts/evidence_records.py`,
`scripts/execution-evidence.schema.v2.json`, and
`tests/test_evidence_records.py`.

## Acceptance evidence

- Targeted W2 records suite: `python3 -m unittest tests/test_evidence_records.py -v` — 39 passing tests.
- W1 storage compatibility: `python3 -m unittest tests/test_evidence_store.py -v` — 5 passing tests.
- Final aggregate gate:
  `python3 -m unittest tests/test_evidence_records.py tests/test_evidence_store.py tests/test_run_evidence.py -v`
  — 59 passing tests.
- Independent schema probes accepted a valid attempt and rejected boolean
  schema versions, mixed task modes, and misplaced telemetry.

## Result

The W2 parent outcome is complete: callers can construct the approved four
record concepts through the W1 storage boundary without skill integration or
physical-path knowledge. Lifecycle orchestration and producer integration
remain correctly deferred to W3 and later work.
