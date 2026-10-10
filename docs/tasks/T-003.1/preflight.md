# Preflight: T-003.1 — Name the complete ordered submission route

Status: ready
Profile: guided
standalone_preflight_value: material
Checked: 2026-10-10
Source brief: docs/tasks/T-003.1/brief.md
Source brief revision: SHA-256 9693af27578075b1331e39335c185ab226f01a84df2c7718f8e36408e7acd803
Verification design: docs/tasks/T-003.1/verification.md (revision 1)
Verification `Source brief:` resolves to the package brief at the digest above.

## Standalone value

Material because the brief named a genuine entry condition: the T-001/T-002
dependency contracts had to be confirmed from repository state, and T-001 has no
`results.md` (only Git history). Resolved by discovery, not assumption:

- `T-001.4` completed at Git `700654a` (`T-001.4 done`); `T-002.4` completed and
  accepted at Git `0eb7963` (`T-002.4 done (accepted)`, with `results.md`).
- Both dependencies are satisfied; the consuming interfaces (T-001 preparation,
  T-002 discovery/decision) are the current committed contracts.

Remaining facts (paths, selectors, commands) were routine and can be re-checked
cheaply by the implementer.

## Scope and ownership

Executable leaf, `Status: ready`, `Task kind: executable`. The parent `T-003`
is `decomposed` and is never preflighted or launched; this leaf is its
dependency-ready child.

Allowed edit targets all exist and are confirmed present:

- `skills/task-implementation-flow/bounded-task-implementer/SKILL.md`,
  `evals/evals.json`, `evals/files/setup_fixture.py`
- route wording in `skills/task-implementation-flow/README.md`, `skills/README.md`,
  root `README.md`
- focused `tests/test_bounded_task_implementer.py`, `tests/test_task_flow_guides.py`
- inspection-only: `scripts/install_development_skills.py`

Work applicability confirmed: the initial template (SKILL.md:386, 395–397),
correction template (SKILL.md:327–328), machine `next_action` (SKILL.md:423–424)
and completion routing (SKILL.md:432–435) currently hard-code discovery as the
next stage, which is exactly what AC-01/AC-02 repair.

Pre-existing user work (must be preserved; no overlap with edit targets):

- modified `docs/tasks/index.json` (uncommitted T-003 registry block)
- untracked `docs/tasks/T-003/`, `T-003.1/`–`T-003.4/`, `docs/future-work/`,
  `.DS_Store` files and `skills/.DS_Store`

None of these are edit targets for this task. This preflight adds only
`docs/tasks/T-003.1/preflight.md` beside the existing `brief.md`/`verification.md`
in that package.

## Dependencies and capabilities

- Dependencies T-001, T-002: satisfied (above).
- Fixture/helper capability: `evals/files/setup_fixture.py` present; existing
  implementer submission/evidence cases and guide route cases present. No new
  harness or runtime routing mechanism is needed (matches the brief).
- Installer: `scripts/install_development_skills.py` declares
  `bounded-task-implementer` (line 35) and manages `skills/README.md`
  (`PROFILE_SKILLS_README`, line 46). Inspect-only; change a stale declaration
  only if this task causes it.

## Baseline

Both owning test files pass at the current committed tree, confirming a working
environment (not a fail-first state):

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py` → `Ran 9 tests … OK`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py` → `Ran 11 tests … OK`

## Targeted command and oracle

Start with fail-first focused cases, narrowest first, then the owning gates from
the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py
```

Oracle: published initial/correction handoff guidance and the extended route
cases map every supplied policy/stage state to the exact first outstanding owner
and full ordered remainder (AC-01/AC-02), while submission stays a stop at
`READY_FOR_REVIEW` and retains context, every scenario row and remaining
obligations (AC-03). A fail-first result must fail on the route obligation, not
on missing preparation or a broken fixture. All V-01–V-06 scenarios are
exercisable with existing local evidence; no scenario requires the real agent
boundary.

## Warnings

- Assertions prove guidance/fixture contract structure, not an emitted agent
  handoff, role stop or compliance. Preserve the explicit T-005 unrun gap.
- No broad, network, model or agent-eval gate is authorized here; T-003.4 owns
  composition/installed-profile checks.

## Next action

Proceed to bounded implementation of T-003.1 within the allowed paths; run the
fail-first focused cases first, then the two owning gates sequentially. End the
implementer invocation at `READY_FOR_REVIEW` with the first outstanding
conditional stage and complete remaining route. Standalone guided preflight is
recommended again for the next materially similar dependency-gated leaf.
