# Preflight: T-003.4 — Verify composed handoffs and installed source projection

Status: `ready`
Mode: guided, standalone
`standalone_preflight_value`: `marginal` — the named uncertainty (reviewed
.1–.3 outputs, current test ownership) resolved from committed history and a
cheap local command check; no material late-discovery risk remained.

## Facts

- Brief: `docs/tasks/T-003.4/brief.md`, status `ready`, kind `executable`.
  SHA-256 `5834ac29048b28f5cc22e62adf8cbcd2ed0c7b6e104af48cc5aa5e2e90445313`
  matches `verification.md` `Source brief revision:`. `Source brief:` resolves
  to the package brief; scenario IDs V-01–V-10 preserved as derived guidance.
- Dependencies: T-003.1 / .2 / .3 all committed and accepted
  (`9faec6c`, `6bf933c`, `bcd0ad6`). No decomposed-parent condition applies.
- Ownership: tracked worktree clean. Untracked, non-conflicting: `.DS_Store`
  at root / `docs/` / `skills/` (leave untouched) and
  `docs/tasks/T-003.4/verification.md` (derived artifact, read-only here).
- Capabilities: `tests/staging_fixture_support.py`,
  `scripts/install_development_skills.py`, and project-local `.agents/skills/`
  copies all present. Aggregate-union modules named by verification.md all
  exist under `tests/`.

## Targeted commands (both execute and pass now)

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py   # 9 tests OK
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py  # 14 tests OK
```

Oracle per AC: composition/oracle comparisons (AC-01–03, AC-05) and real
disposable committed-target installer projection with stale-managed-removal /
unmanaged-preservation (AC-04); scenario mapping as per verification.md
coverage table.

## Warnings / stops

- No blockers. Do not touch the untracked `.DS_Store` files or edit
  `verification.md`.
- Stop for unresolved child contract mismatch, changed authority, user-work
  overlap, unsafe permissions, scope expansion, missing decisive capability
  (brief "Stops and handoff"). Budget is soft.

## Implementer handoff

- Scope: brief "Authority and scope" paths only (root/flow/skills README route
  entries, existing guide/composition/installer tests, new
  `docs/tasks/T-003.4/composition.json` + `results.md`).
- Run the two targeted commands first; extend existing cases only for distinct
  missing proof; preserve predecessor cases.
- Next action: bounded implementation of the brief; then immediately hand
  completed bytes to a fresh independent acceptance reviewer; do not claim
  T-005 role qualification.
