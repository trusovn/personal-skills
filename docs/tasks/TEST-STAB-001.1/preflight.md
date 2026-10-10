# Preflight: TEST-STAB-001.1 — Assign clear test owners without changing evidence

Status: **ready** (guided)

`standalone_preflight_value: material` — resolved real uncertainties: the
brief-named route required confirming accepted T-002.4, the current baseline,
and the disposable copied-package check. The copied-package probe is executable
today and currently red by design (29/30 errors), which is the exact migration
target of AC-04/V-05 and would have been costly to discover mid-implementation.
Standalone preflight is recommended for the next materially similar task.

## Verification-design resolution

`docs/tasks/TEST-STAB-001.1/verification.md` — `Source brief:` resolves to this
package's `brief.md`; declared brief SHA-256
`73471a7e4fdad30a72ee010b9936906f95227bec4a38f8267024efaaa568c100` matches
current brief bytes. Treated as derived guidance under the brief, not as
requirements authority. Scenario IDs V-01–V-07 preserved; none blocked.

## Confirmed scope and ownership

- Authority: parent brief, user request, root `AGENTS.md`, active project-local
  `testing-discipline`. Branch `t-o-new-flow`, remote `trusovn/personal-skills`.
  Leaf is `executable` with `Status: ready`; parent TEST-STAB-001 is decomposed
  and must not be launched.
- Dependency: T-002.4 accepted (commit `0eb7963` "T-002.4 done (accepted)");
  T-001/T-002 sources unchanged. No dependency-ready issue.
- Intended change areas `tests/` and
  `skills/task-implementation-flow/task-brief-designer/tests/` are clean.
  Existing dirty files (staged leaf/parent briefs, modified `docs/tasks/index.json`,
  untracked `verification.md`) are task-planning artifacts owned by the design
  stage — do not modify them; the implementer writes only new evidence inside
  this leaf plus the brief's allowed test/support/doc surfaces.
- The eight repository owner module names are fixed by the brief
  (`test_task_preflight.py`, `test_bounded_task_implementer.py`,
  `test_task_preparation_contracts.py`, `test_task_acceptance_review.py`,
  `test_task_review_discovery.py`, `test_senior_review_discipline.py`,
  `test_task_flow_guides.py`, `test_review_composition.py`). The three fixture
  module names remain implementer choice per the brief; verification.md's
  handoff line asking preflight to resolve them conflicts with brief authority —
  brief wins, names are chosen locally and recorded in the evidence map.

## Baseline and capability evidence

Run from repository root, sequentially, all green today:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py        # 74 OK
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py   # 30 OK
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py                                              # 14 OK
```

Post-move focused selector pattern (one fresh invocation per owning module):
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <module>.py`,
then the mapped union + remaining designer suite, then the unchanged installer
suite, sequentially. Unrelated-cwd invocation uses explicit `-s` paths.

Disposable copied-package probe (V-05 capability) executed against a copy of
`skills/task-implementation-flow/task-brief-designer` in `/tmp/opencode/stab-copy`:
**fails today with 29/30 errors**, concentrated in the cross-skill classes
slated for repository ownership (`ImplementerContractTest` etc.). This is the
intended pre-move fail-first state, not a broken environment — the source-tree
run passes 30/30. AC-04/V-05 require this to pass from the copy without
source-tree or repository-helper fallback after the move.

## Oracles (per AC)

- AC-01 → V-01: dependency/location inspection vs the ten ownership rows, guide,
  executed collection map; no forwarding classes, emptied originals removed.
- AC-02 → V-02/V-03: collection bijection with scenario/subtest distinctions;
  unchanged assertions/inputs; real fixture boundaries (late-omission validator
  contrast: clean rejects boolean revision with exit 2, fail accepts it with
  exit 0 and rejects the other two with exit 2; index/worktree distinctions).
- AC-03 → V-04: fresh isolated runs + documented mapped union + installer suite.
- AC-04 → V-05/V-06: copied-package designer suite and discovery/acceptance
  setup executions; unchanged real installer projection/preservation.
- AC-05 → V-07: scoped diff + truthful evidence labels; parity guard retained.

Real-boundary evidence required where unit/module checks cannot prove it:
fixture subprocess runs, disposable Git repos, installer projection, and the
copied-package execution above.

## Warnings and stops

- Copied-package suite is red pre-move (expected). Implementation must land the
  AC-04 fix; a green repository suite alone is insufficient.
- Local object store is missing the tree for commit `0eb7963` (`git show`
  fails). Do not depend on reading that commit's diff; use worktree status/diff
  and fixture-local repos. Out of scope to repair.
- Do not touch `.DS_Store` files, do not refresh `.agents/`.
- Stop per brief: red baseline, lost/ambiguous scenario ownership, user-work
  overlap, permission need, or any package/runtime contract change.

## Next action

Implement with `bounded-task-implementer` from this leaf's `brief.md`:
record the baseline inventory with subtest/scenario distinctions (V-02 given),
perform the ownership migration, publish `results.md` and the navigation guide,
then hand completed bytes to fresh independent `task-review-discovery` and a
separate fresh `task-acceptance-review`.

## Implementer handoff

```text
Preflight TEST-STAB-001.1: READY (guided, material value).
Scope: relocate tests from tests/test_review_discipline.py and
skills/task-implementation-flow/task-brief-designer/tests/test_package_resources.py
to the brief's fixed repository owners; keep the three fixture module names as
local choice; only imports/paths/class organization change. Dirty files
(docs/tasks/*, index.json, verification.md) are design-stage work — do not edit.
Baseline (repo root, sequential, all green today): the three PYTHONDONTWRITEBYTECODE=1
unittest discover commands above (74/30/14 OK).
Copied-package probe currently fails 29/30 errors by design — AC-04/V-05 target;
make the remaining designer suite pass from a disposable copy with no
source-tree/helper fallback, and keep the unchanged installer suite green.
Oracles: V-01–V-07 as mapped above; fixture validator contrast, index/worktree
distinctions, and real subprocess outcomes are the decisive boundaries.
Warnings: git show 0eb7963 fails locally (missing tree object) — do not rely on
it or repair it; leave .DS_Store files alone; do not refresh .agents/.
Stops: red baseline, lost scenario ownership, user-work overlap, permission or
contract change.
Next action: implement per brief, publish results.md + navigation guide, then
fresh independent task-review-discovery and task-acceptance-review.
```
