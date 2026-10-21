# Planning now explains the practical result first

The planning source guidance now leads with who benefits and what improves.
For a plan with several tasks, the opening explains what each task gives the
owner or enables next and links to its detailed scope. An existing readable
task list can stay in place and be linked from the opening. Task briefs reuse their
existing outcome and direction trace before execution metadata.

To limit duplication, the plan template moves its product outcome to the
opening and removes the repeated outcome column from its technical task table.
The table retains dependencies, flow placement, inputs, outputs, interfaces,
invariants, and integration boundaries. The task map keeps its existing JSON
contract. Progress stays in linked work reports.

After the owner raised the risk of adding explanations alongside existing
ones, the guidance was tightened: inspect existing explanations first, retain
clear ones, move or rewrite others while replacing the old occurrence, and add
only missing information. This applies to both plans and task briefs.

This is implementation evidence for T-002 in the
[project plan](project-plan.md#5-implementation-tasks), using the
[approved pilot feedback](t001-pilot.md#owner-feedback-and-resulting-choices).
Next is T-003: apply the same information ownership to work reports.

## Changed source

- [Planning guidance](../skills/project-delivery-plan/SKILL.md) and its
  [template](../skills/project-delivery-plan/references/project-plan-template.md):
  outcome first, readable task contributions, links to authority and progress,
  and explicit treatment of missing or conflicting purpose.
- [Brief guidance](../skills/task-implementation-flow/task-brief-designer/SKILL.md)
  and its [template](../skills/task-implementation-flow/task-brief-designer/references/task-brief-template.md):
  existing outcome and applicable direction trace come first; project purpose,
  scope, and acceptance criteria retain their owning locations.

Compatibility inspection found no required producer/consumer change in
project-direction or project-plan-verification. The plan template retains all
13 headings recognized by the existing verifier. Direction authority and
packaged preparation/review duties remain in their existing guidance.

Installer inspection covered DEVELOPMENT_SKILL_SOURCES, PROFILE_SKILLS_README,
SHARED_SCRIPT_FILES, focused installer tests, and README installation guidance.
The existing whole-package copy mechanism covers these edits. Names, paths,
shared dependencies, and installer ownership need no change. Candidate
installation and consuming-session qualification belong to T-004.

## Illustrative wording checked against the requirements

These are author-written examples, not outputs from a consuming-agent trial.

| Case | Example opening or contribution | What the comparison checks |
|---|---|---|
| Small change | “Make plans easier for the project owner to understand by putting the practical result before workflow details. First, try one example with the owner.” | Purpose, beneficiary, and first useful proof are understandable without IDs. Detailed scope stays below. |
| Several tasks | “Try an example: agree on wording before applying it. Improve plans: explain the result and each task's contribution. Improve reports: explain evidence and next action. Qualify the experience: check accuracy and ask the owner whether it is clear.” Each task name links to its detailed scope. | Each contribution follows the existing four-task plan; the opening does not become another requirements or progress list. |
| Internal work | “Align planning guidance and its template so later plans explain what the owner will gain.” | Internal work names its enabling effect without inventing an end-user feature. |
| Missing direction | “The supplied request does not establish who should benefit or which situation should improve. The owner must settle that purpose before we can define the intended result.” | Unknown purpose stays unknown. A material authority gap follows the existing decision route rather than becoming a ready task under an invented purpose. |

The changed guidance also keeps material uncertainty visible and avoids routine
statements about unchanged areas, as requested in the pilot.

## Verification

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_contains_repo_stage_and_bounded_delivery_skills test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_guide_covers_every_installed_skill_and_usage_contract
```

Results: 3 package-resource checks, 13 preparation-contract checks, and 2
installer profile/guide checks passed. The skill-creator `quick_validate.py`
also passed for both changed skill packages. These are structural/regression
checks, not proof of emitted-document quality.

After the duplication correction, the 3 package-resource and 13 preparation
checks were rerun and passed; the whitespace check also passed.

The examples above and the scoped diff were manually compared with T-002's
acceptance criteria. Actual consuming-session behavior, owner assessment of
integrated outputs, and independent discovery followed by a separate acceptance
decision remain T-004 qualification obligations. Optional evidence sidecar
instrumentation was unavailable because Git metadata is not writable in the
sandbox; task verification used the recorded local checks.

Actual contract impact: changed presentation and information placement for
emitted plans and executable task briefs. No executable schema or JSON task-map
declaration changed.
