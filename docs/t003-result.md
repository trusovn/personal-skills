# Reports now explain the practical result before workflow details

The reporting source guidance now asks implementation and acceptance reports to
open with what the work means, what the evidence supports, what remains
unfinished, and who acts next. Correction and interrupted-work reports carry
the same explanation. Existing clear prose is reused or moved; detailed facts
remain with their owning evidence and decision records.

The repository and development-profile guides now point readers from intended
work to the current report. Implementation reports its changes and checks;
discovery supplies independent evidence; acceptance decides what may advance.
Missing or stale evidence stays visible. These are source changes checked
locally; actual consuming-session output quality remains to be qualified.

This is T-003 implementation evidence for the
[project plan](project-plan.md#5-implementation-tasks), following the
[pilot feedback](t001-pilot.md#owner-feedback-and-resulting-choices) and
[planning changes](t002-result.md). Authority for this continuation is the
owner's request to continue work on `docs/project-plan.md`.

## Changed source and compatibility

- [Implementation output guidance](../skills/task-implementation-flow/bounded-task-implementer/SKILL.md#output-contract)
  and its correction handoff: practical result first, with checked scope,
  interruption limits, next actor, and owner decisions where needed.
- [Acceptance output guidance](../skills/task-implementation-flow/task-acceptance-review/SKILL.md#output-contract)
  and its [report template](../skills/task-implementation-flow/task-acceptance-review/references/acceptance-report-template.md):
  explain the supported disposition before dense identity fields, deriving the
  opening from the existing verdict and evidence.
- [Root guide](../README.md), [profile guide](../skills/README.md), and
  [flow guide](../skills/task-implementation-flow/README.md#reading-plans-and-work-reports):
  explain the reading path and preserve each record's scope and age. Profile
  links target installed skill packages rather than the source-only flow guide.

Discovery inspection found that its current findings, coverage, command records,
and continuation already supply the necessary inputs. No producer gap required
a change. Required preparation, identity, verdict, coverage, correction, and
independent-review fields remain in place. Machine-only output contracts retain
their existing format.

Installer inspection covered `DEVELOPMENT_SKILL_SOURCES`,
`PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`, focused installer tests, and
README installation guidance. Existing package copying and the managed profile
guide cover these edits; skill names and shared runtime dependencies need no
change. The active installation was not refreshed.

## Wording comparison against supplied situations

These are author-written illustrations checked against T-003's requirements,
not outputs from fresh consumers or independent review findings.

| Supplied situation | Illustrative opening | Evidence boundary preserved |
|---|---|---|
| Source edits and local checks completed; no consumer trial | “Reports now start with their practical result. Local checks passed; a fresh consumer trial is still needed. The qualifier runs that trial next.” | Implementation claims its own checks without independent acceptance. |
| Work interrupted after editing; checks not run | “The report wording is drafted, but its checks have not run. The next implementer must check the draft before submitting it.” | Last checked scope and unfinished work remain visible. |
| Discovery confirms an unsupported completion claim | “The report describes unfinished work as complete. It cannot advance until the implementer corrects that claim and fresh review checks it.” | Rejection retains the finding and correction route. |
| Required discovery evidence missing | “The intended improvement is clearer reporting, but current independent evidence is missing. The discovery reviewer must supply it before acceptance can decide.” | Missing proof does not become success or a production defect claim. |
| Earlier acceptance predates changed report bytes | “The earlier report was accepted before these edits. That decision does not establish whether this version is accurate; fresh discovery and a separate decision are needed.” | Historical acceptance cannot certify new bytes. |

These comparisons do not prove owner comprehension or installed behavior.
T-004 owns fresh outputs, contrast evaluation, and the integrated owner check.

## Verification and next action

Commands run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_acceptance_review.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_contains_repo_stage_and_bounded_delivery_skills test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_guide_covers_every_installed_skill_and_usage_contract
```

Results: 15 implementer, 25 acceptance, 14 guide, and 2 installer checks passed.
Guide and installer checks passed again after the profile-link adjustment.
The skill-creator `quick_validate.py` passed for both changed skill packages.
Whitespace and changed-document local-link checks passed. These establish
structural/regression compatibility, not emitted-document quality. Existing
coverage was inspected; behavioral eval changes remain in T-004 rather than
adding tests that match the new prose.

Optional evidence instrumentation reported `git_metadata_unwritable` at its
availability probe and was skipped for this invocation. No model-consuming,
networked, or installed qualification run was performed.

Actual contract impact: changed human-readable report presentation and guide
navigation. Executable contract declarations changed: none.

Next: T-004 qualifies the integrated candidate in a disposable installation
using fresh consumers and supplied evidence, then obtains owner clarity feedback.
Its required review route remains fresh independent `task-review-discovery`
evidence followed by a separate fresh `task-acceptance-review` decision. This
record is implementation evidence and does not supply that verdict.
