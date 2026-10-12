# Preflight: INT-FLOW-001 — Close preparation and review integration gaps

Source brief: docs/tasks/INT-FLOW-001/brief.md (revision 1, status `ready`, kind `executable`)
Verification design: docs/tasks/INT-FLOW-001/verification.md (revision 1, `Source brief:` resolves to this package's `brief.md`; read as derived guidance)
Profile: guided standalone preflight (per brief readiness route)
Status: `ready`
Standalone preflight value: `marginal`

## Classification rationale

The brief named standalone preflight to confirm source ownership, affected test
owners, existing fixture capability and command scope. Focused discovery resolved
all four cheaply, so no material uncertainty remained: change areas are tracked
and clean, all seven focus test modules exist, fixtures pass, and the candidate
command runs in ~3 seconds. Reclassified `marginal`; implementer self-preflight
is recommended for the next materially similar task.

## Ownership and current state

- Intended change areas are tracked and clean: `skills/task-implementation-flow/`
  `{task-maintainability-review, task-review-discovery, task-acceptance-review,
  task-verification-designer}/`, `README.md`, `skills/README.md`,
  `skills/task-implementation-flow/README.md`, the seven focus test files under
  `tests/`, and `scripts/install_development_skills.py` (inspection).
- Pre-existing user work, outside implementer scope, do not touch:
  - `M docs/tasks/index.json` — INT-FLOW-001 registry entry added by brief design.
  - Untracked `docs/tasks/INT-FLOW-001/` package (brief + verification).
- Junk untracked `.DS_Store` files at repo root, `docs/`, `skills/`: ignore.
- `git diff --check` is clean on current state.

## Dependencies and capabilities

- T-001, T-002, T-003 completed (per git history and `index.json` `depends_on`).
- Installer and disposable-commit-target projection fixtures exist and pass.
- `docs/contracts/` correctly absent — do not create one (brief excludes it).
- Active `.agents/` installation is read-only for this task.

## Targeted command and oracle

Verified from repo root (baseline run: 110 tests OK in ~2.9s):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_task_maintainability_review test_task_review_discovery test_task_acceptance_review test_task_preparation_contracts test_task_flow_guides test_review_composition test_install_development_skills
```

Oracle for acceptance: run new/changed focused checks first (fail-first rejection
of the old instruction or a controlled relevant fault where feasible, fault
removed afterward), then the nearest owning modules sequentially; `git diff
--check` clean; installer projections only on disposable committed Git targets.
Structural text checks, staged fixture reports and constructed comparisons are
labeled as such; actual role calls remain unrun (T-005 boundary).

## Warnings and stops

- Do not refresh the active `.agents/` installation or run T-005 roles.
- No live-network, model-budget or whole-repository gates required.
- Stop for authority conflict, inseparable user work, unsafe permissions, a
  missing decisive local capability, new shared tooling or scope expansion.
- Do not update official plans, old task history, or the task tracker.

## Implementer handoff

- Scope: correct the five findings (I-01..I-05) per brief ACs 1–6 and
  verification scenarios V-01–V-11, within the named skill instructions,
  templates, eval expectations and task-local fixtures; synchronize only
  affected README claims; reuse existing staging helpers and coverage.
- Ownership: all target files are clean; pre-existing dirty state above belongs
  to other stages and is disjoint from the change scope.
- Command: as above; oracle: focused checks first, then owner modules, clean
  `git diff --check`, disposable-target installer projections only.
- Evidence limits: state structural vs. real filesystem/Git observations vs.
  unrun role boundaries; prepare exact T-005 setup, producers/consumers,
  expected contrasts and unrun boundaries without adding a role runner.
- Next action: implement the corrections, then hand completed bytes and the
  finding/scenario inventory to fresh independent review: maintainability
  review → applicable registry synchronization → fresh discovery → separate
  acceptance. End the implementer invocation naming the first outstanding owner
  and the complete remaining route.
