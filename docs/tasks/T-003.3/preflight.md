# Preflight: T-003.3 — Preserve correction obligations and current evidence

Status: `ready` (guided standalone)

`standalone_preflight_value`: `marginal` — the brief named standalone guided
preflight for specific uncertainties (`.1` route fields, record-correction and
mixed-condition fixture availability, verification digest binding). Focused
discovery resolved every named uncertainty with cheap checks, so the standalone
stage added little beyond implementer self-preflight and is not recommended
again for the next materially similar task.

## Checks performed

- Brief `Status: ready`, `Task kind: executable`; not a decomposed composite.
  Dependency T-003.1 done/accepted in `git log`; `docs/tasks/index.json`
  T-003.3 `depends_on: [T-003.1]`, consistent.
- `docs/tasks/T-003.3/verification.md` `Source brief:` resolves to the package
  `brief.md`; declared SHA-256 `1b9e712a…` matches current brief bytes. All
  scenario IDs V-01…V-08 map to AC-01…AC-05 and R-01…R-04 with concrete
  oracles.
- Ownership: worktree has no tracked modifications. Untracked: three `.DS_Store`
  files (unrelated, leave alone) and `docs/tasks/T-003.3/verification.md`
  (prior-stage derived artifact; implementation must not edit it). No overlap
  with implementation paths.
- Resolved uncertainties:
  - `.1` route fields present in `docs/tasks/T-003.1/brief.md` (AC-01 route
    wording, flow README ownership).
  - `record-correction` eval fixture exists at
    `skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py`
    (function `record_correction`, registered as `record-correction`).
  - Mixed-condition fixtures in `tests/test_task_acceptance_review.py` (6);
    revision/expected-effect fixtures in `tests/test_task_preflight.py` (11);
    late-omission/aggregate/diagnostic fixtures in
    `tests/test_task_review_discovery.py` (15).
  - All four owning test modules collect: `test_bounded_task_implementer.py`
    (11), `test_task_preflight.py` (7), `test_task_review_discovery.py` (14),
    `test_task_acceptance_review.py` (21).
- Targeted command executes: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
  discover -s tests -p test_task_preflight.py` → 7 tests OK in 0.35s. Green
  baseline confirms environment; expect intended fail-first only on changed
  cases.

## Scope and ownership

- Confirmed scope: source correction guidance/evals/setup under
  `skills/task-implementation-flow/` (bounded-task-implementer,
  task-review-discovery, task-acceptance-review, task-contract-registry-updater,
  task-preflight only if an approved revision obligation is absent, flow
  README); task-owned focused extensions to the four owning test modules under
  `tests/`.
- No user-work overlap; no permission or scope conflict found.

## Command and oracle

From repo root, fail-first changed cases, then each changed owning module
sequentially:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <owning-module>.py
```

Owning modules: `test_bounded_task_implementer.py`, `test_task_review_discovery.py`,
`test_task_acceptance_review.py`, `test_task_preflight.py`.

Oracle: verification.md scenarios V-01…V-08 (fixture-based contract assertions
per AC-01…AC-05 / R-01…R-04); behavioral probes via `setup_fixture.py
record-correction` in a disposable workspace. No whole-repo gate.

## Warnings

None material. `docs/tasks/T-003.3/verification.md` is untracked derived
guidance: treat as read-only input, not requirements authority.

## Implementation stops

Changed requirements, contradictory stage authority, unsafe permissions,
user-work overlap, scope expansion, or decisive capability requiring
infrastructure.

## Implementer handoff

```text
Task: docs/tasks/T-003.3/brief.md (Status: ready, executable)
Scope: source correction guidance/evals/setup in skills/task-implementation-flow/
  (bounded-task-implementer, task-review-discovery, task-acceptance-review,
  task-contract-registry-updater, task-preflight only if approved revision
  obligation absent, flow README); task-owned extensions to the 4 owning test
  modules under tests/.
Ownership: no dirty overlap; do NOT edit docs/tasks/T-003.3/verification.md or
  the untracked .DS_Store files.
Command (fail-first changed cases, then each owning module sequentially, from root):
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <owning-module>.py
  Owned modules: test_bounded_task_implementer.py, test_task_review_discovery.py,
  test_task_acceptance_review.py, test_task_preflight.py
Oracle: verification.md scenarios V-01..V-08 (fixture contract assertions per
  AC-01..AC-05 / R-01..R-04); behavioral probes via setup_fixture.py
  record-correction in a disposable workspace; no whole-repo gate.
Baseline: green (test_task_preflight 7/7 OK); expect intended fail-first on
  changed cases only.
Stops: changed requirements, contradictory stage authority, unsafe permissions,
  user-work overlap, scope expansion, infrastructure-requiring capability.
Next: bounded implementation, then hand to fresh acceptance reviewer via .1's
  ordered conditional stages; end invocation after handoff.
```

Next action: begin bounded implementation under the recorded scope.
