# Preflight: T-003.2 — Report every confirmed bounded maintainability blocker

- Status: `ready`
- Mode: standalone guided (brief's readiness route named it; value classification below)
- `standalone_preflight_value`: `material`
- Brief digest: `9ef8e1459b99fab8deca899d21bf20215f9c5942ac6a081f5e93b3f51c98d88c`
- Verification design: `docs/tasks/T-003.2/verification.md` (revision 1); its `Source brief:` resolves to this package's `brief.md` and its digest matches the current brief bytes. Read as derived guidance; brief remains requirements authority.

## Uncertainties the named route asked to confirm

1. Maintainability policy location/state — resolved:
   - Source skill `skills/task-implementation-flow/task-maintainability-review/SKILL.md`
     line 208 has the three-blocker cap ("Report at most **3 blockers**..."),
     line 248 has the enough-blockers stop ("Do not keep searching for minor
     issues after enough decisive blockers are established"). These two lines
     are the edit targets.
   - Flow/profile guides (`skills/README.md`, `skills/task-implementation-flow/README.md`)
     contain no stale cap/stop wording. No guide edits needed.
   - `skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md`
     line 246 mentions the stop, but that file is plans/history and read-only
     for this task.
   - `.agents/` installed copies are read-only; installer projection owns them.
2. Task-local fixture setup — resolved:
   - Sibling convention is `<skill>/evals/files/setup_fixture.py`; this skill has
     no `files/` dir yet. Create the fixture at
     `skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py`.
   - Installer `scripts/install_development_skills.py` uses `shutil.copytree` per
     skill dir, so the fixture is projected automatically. No installer code or
     selection change is needed or authorized.
3. Focused test owner — resolved: no `tests/test_task_maintainability_review.py`
   exists. Closest owners `tests/test_task_flow_guides.py` (composed flow-guide
   wording) and `tests/test_task_preparation_contracts.py` (report-path
   `reviews/maintainability-NN.md`) do not cover cap/stop completeness cases.
   Creating the new focused module is within authorized scope.

## Ownership and state

- `git status --short`: only untracked `.DS_Store` (root, docs/, skills/) and
  this package's untracked `verification.md`. No dirty tracked files, no
  user-owned work overlapping the change area
  (`skills/task-implementation-flow/task-maintainability-review/`,
  `tests/test_task_maintainability_review.py`, `docs/tasks/T-003.2/`).
  Do not commit `.DS_Store` files.
- Dependencies: T-001/T-002 complete; T-003.1 committed as accepted
  (`9faec6c T-003.1 done (accepted)`). T-003.2 is an executable leaf in
  `docs/tasks/index.json`; authority (plan sections, task-map T-003, parent
  brief P-02/P-07) resolves.
- Existing evals 1–3 (`evals/evals.json`) match V-05's retained cases; keep
  them distinct.

## Command and oracle

- Environment: python 3.14.4; full local suite green before changes
  (`python3 -m unittest discover -s tests` → 177 tests OK, 4.6s).
- Targeted command (after creating the focused module):
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py`
  from repo root.
- Oracles by scenario (from verification.md):
  - V-01/V-02/V-03/V-04: fail-first policy checks reject both shortcuts
    (cap at three, stop on verdict sufficiency) semantically, and the runnable
    four-defect fixture shows four independently observable introduced/worsened
    blockers, a non-blocking preference control, and complete-vs-interrupted
    stop handling with outstanding coverage.
  - V-05: retained eval 1–3 outcomes and report-path checks stay green.
- Real boundary: fixture must stage a disposable Git workspace with actual
  changed production bytes and observable probes; text/metadata assertions
  alone are structural evidence only.
- Unrun by design: live agent evals (T-005 owns), composed guide/installer
  checks (T-003.4 owns).

## Stops for the implementer

- Do not edit `.agents/` copies, the policy-plan history doc, installer code or
  selection, or any gate/schema/runner. Do not refresh installed copies.
- Stop and route to task design if a verification scenario cannot be exercised
  at its stated boundary.

## Next action

Begin bounded implementation: edit the two source-skill lines (cap and stop),
add the focused test module and the skill-local `evals/files/setup_fixture.py`
with the four-blocker qualification inputs, run the targeted command, then hand
completed bytes to a fresh independent acceptance reviewer.

## Implementer handoff

```text
PREFLIGHT: T-003.2 — ready
Value: material (resolved policy location, fixture setup, focused-test owner)

Edit targets (authorized source only):
- skills/task-implementation-flow/task-maintainability-review/SKILL.md
  line 208 (three-blocker cap) and line 248 (enough-blockers stop)
- new tests/test_task_maintainability_review.py (no existing owner for these cases)
- new skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py
  (sibling convention; installer projects it automatically — no installer edits)

Read-only: .agents/ copies, flow/profile guides (no stale entries), policy-plan
history doc, installer code/selection, existing evals 1–3 and existing test owners.

Command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py
Baseline: 177 tests OK (python 3.14.4); git tree clean of user work (.DS_Store untracked, ignore).

Oracle: V-01..V-05 — fail-first checks reject cap-at-three and verdict-sufficiency
stop semantically; runnable fixture proves 4 distinct introduced/worsened blockers,
non-blocking preference control, genuine-stop partial coverage; existing eval
1–3 expectations retained.

Next action: implement → targeted command → fresh independent acceptance reviewer.
```
