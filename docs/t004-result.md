# Plans and reports were tried with supplied evidence

Fresh consumers used a disposable installation to produce small and multi-task
plans, a successful implementation report, an interrupted report, and three
acceptance decisions. The inspected openings explain the practical result and
retain unfinished work, conflicting evidence and review limits. The
missing-direction case asks for the owner's purpose instead of inventing it.

Qualification is **READY_FOR_REVIEW**. The owner approved the clearer examples;
the feedback checkpoint is satisfied. The fresh
task-brief trial is now retained alongside the planning and reporting trials.
These observations are implementation evidence, not independent acceptance of
this task. Fresh independent discovery
and a separate acceptance decision follow.

Authority: [T-004 in the project plan](project-plan.md#t-004--qualify-the-complete-reading-experience),
the direct request to work on task 4, and explicit approval to run focused fresh
consumer trials. The plan and staged T-001–003 work were preserved.

## Candidate and changes

- Planning evals now supply actual synthetic request, foundation and result
  documents through a packaged setup program. Small change, multiple tasks and
  missing direction each include interruption, historical acceptance and an
  unsupported conflicting completion note.
- Existing implementation and acceptance evals retain their executable fixtures;
  their expectations now check the practical opening. An interrupted guided
  implementation case reuses the existing session fixture.
- Two focused fixture tests reuse the repository staging helper. One checks
  supplied authority/evidence inputs; one actually runs the failing expired
  session regression and confirms no source change. These do not certify prose.
- The [reading rubric](../skills/project-delivery-plan/evals/files/reading-rubric.md)
  compares claims with evidence and supplies a planted false completion claim.

Installer inspection covered DEVELOPMENT_SKILL_SOURCES, PROFILE_SKILLS_README,
SHARED_SCRIPT_FILES, focused installer tests and README installation guidance.
Whole-package copying already covers these assets; names and shared dependencies
need no changes. The canonical installer ran only in a disposable unborn Git
repository. Its managed projection matched before and after trials; unrelated
skill and AGENTS text sentinels survived. The active installation was not refreshed.

[Installation identity](t004-evidence/installation.json) records source HEAD,
the disposable target, every installed package/guide/shared-file SHA-256 and
candidate digest `b64aaccd9a3e43d5b15253f7c963f3c38b53f76dc78185edd41ec515adab77ac`.
HEAD alone does not identify this dirty candidate. Before/after installer checks
and the [retained-file manifest](t004-evidence/retained-files.json) bind the
qualification evidence. Retained fixture copies omit Git objects and bytecode;
rerun packaged setup to obtain an executable repository rather than treating
those copies as fresh readiness.

## Actual outputs and author comparison

These are observations from the task author using the rubric, not independent
discovery findings. Consumers did not read the rubric. Five fresh consumer
sessions were used: planning cases shared one session, acceptance cases another,
successful/interrupted implementation each used its own session, and the
task-brief trial used another fresh session.

| Scenario | Retained output | Observation and limit |
|---|---|---|
| Small change | [CSV plan](t004-evidence/trials/small-change/small-change/docs/project-plan.md) | Identifies support staff, column identification and the two-record proof; scope stays planned. Task map validator passed. |
| Several tasks and internal enabling work | [Assignment plan](t004-evidence/trials/multi-task/multi-task/docs/project-plan.md) | Explains storage, CLI and restart-proof contributions with links; preserves reassignment rejection and restart semantics. Task map validator passed. |
| Task contribution and preparation | [Durable-operations brief](t004-evidence/trials/task-brief/docs/tasks/T-001/brief.md) | Opening explains the enabling effect and timing. Missing source paths/commands stay unknown; plan verification, derived verification and ready preflight remain due. No implementation or readiness evidence was invented. |
| Missing purpose | [Consumer response](t004-evidence/trials/missing-direction/missing-direction/consumer-response.md) | Requests owner decision; creates no plan/map. |
| Successful work | [Implementation report](t004-evidence/trials/api-immediate/consumer-response.md) | Actual fail-first followed by targeted and owning-suite passes. States READY_FOR_REVIEW, with independent review still due. [Diff](t004-evidence/trials/api-immediate/implementation.diff) retained. |
| Interrupted work | [Interrupted report](t004-evidence/trials/api-interrupted/consumer-response.md) | Actual targeted failure; V-01 unchecked, token assertion not reached, owning suite unrun, no edits. Next implementer must fix and verify. |
| Rejected work | [Queue decision](t004-evidence/trials/queue-defect-decision/queue-runner/docs/tasks/QR-12/reviews/acceptance-01.md) | Preserves F-01 / QR-RUN1 and routes correction; unit pass does not erase public-flow failure. |
| Supported synthetic disposition | [Exporter decision](t004-evidence/trials/exporter-accept-decision/exporter/docs/tasks/EXP-08/reviews/acceptance-01.md) | Admits supplied independent evidence and separate index/worktree identity; does not re-execute or advance work. |
| Incomplete evidence | [Scheduler decision](t004-evidence/trials/scheduler-inconclusive-decision/scheduler/docs/tasks/SCH-09/reviews/acceptance-01.md) | Missing helper leaves concurrency unproved and verdict INCONCLUSIVE; no invented production defect. |
| Stale/conflicting completion | Both planning outputs and supplied result records | Current inspection-only report conflicts with unsupported handover; historical acceptance cannot certify new scope. Maintainer resolves conflict. |
| Unsupported completion contrast | [Planted opening](t004-evidence/planted-unsupported-opening.md) | Author applied rubric item 3: FAIL. No implementation/checks exist in current-report.md, old acceptance covers old CLI, and handover has no evidence. This is rubric calibration, not another consumer run. |

Acceptance trials used supplied synthetic discovery records and made no new
public probes or suite runs. Their fixture verdicts do not accept this candidate.
The inspected outputs introduce no required parallel overview or status ledger;
planning progress stays linked to its owning report. Owner feedback is recorded
below; no separate comprehension exercise was performed.

## Local verification

Commands ran from the repository root with `PYTHONDONTWRITEBYTECODE=1`:

```sh
PYTHONPATH=tests python3 -m unittest test_bounded_task_implementer.ImplementerContractTest.test_reading_evals_supply_authority_and_conflicting_result_records test_bounded_task_implementer.ImplementerContractTest.test_interrupted_reading_eval_exercises_a_real_failure
python3 -m unittest discover -s tests -p test_bounded_task_implementer.py
python3 -m unittest discover -s tests -p test_task_acceptance_review.py
python3 -m unittest discover -s tests -p test_task_flow_guides.py
python3 -m unittest discover -s tests -p test_task_preparation_contracts.py
python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
```

Results respectively: 2, 17, 25, 14, 13 and 3 checks passed. Focused installer
checks passed for profile selection, guide coverage, acceptance package copying
with unrelated-byte preservation, and matching committed/unborn installations.
One initial selector named the last method under the wrong class and failed
to load; rerunning it under `DevelopmentProfileCheckTests` passed.

`python3 skills/project-delivery-plan/scripts/validate_task_map.py docs/task-map.json`
and `git diff --check` passed. The initial scheduler trial setup used the wrong
scenario name and failed with usage output before generation; the consumer then
used the installed eval's correct `scheduler-inconclusive-decision` setup.

Optional evidence instrumentation reported `git_metadata_unwritable` and was
skipped once under the active implementer skill's fallback. No active-install
refresh, full suite, external reviewer or current-task acceptance was performed.

## Continuation completed and remaining route

On the owner's request to continue, the candidate's installed projection still
matched the source (88 compared paths), and every retained evidence hash
matched. A fifth fresh consumer generated the task brief from the multi-task
plan and all seven supplied inputs. The initial read used the wrong directory;
the exact scenario path was supplied and the consumer then read all inputs.

The brief's outcome and existing direction trace explain T-001's contribution
to T-002/T-003 without claiming a direct CLI change. Scope, acceptance criteria,
technical contracts and required preparation remain below the opening. Actual
source paths and local commands are unknown and remain preparation work; the
brief's designed `ready` status does not establish implementation readiness.
The consumer checked required sections, local links and absence of readiness
artifacts. This is structural output verification, not behavioral or readiness
proof. The author comparison found the requested practical contribution and
limitations visible. Owner feedback was still pending at that point.

The [post-brief installer check](t004-evidence/post-brief-install-check.json)
again reports a matching candidate. No source guidance or executable test changed
in this continuation, so the previously passed suites were not repeated. Final
whitespace, retained-hash and brief-link checks passed.

## Owner feedback and submission

In response to the clarity question summarizing the generated multi-task plan
and interrupted report, the owner said:

> they appeart ot be better now than used to be. so let's accept it

This is explicit approval of the improved explanations and satisfies the owner
feedback checkpoint. No specific confusion or requested correction was raised.
The feedback covers the examples presented in that question; it does not claim
a separate reading of every retained output or a comprehension exercise.

Submission: **READY_FOR_REVIEW**. Next: fresh independent
`task-review-discovery`, followed by a separate fresh `task-acceptance-review`.
No additional conditional review stage is imposed by the current authority.
The owner's clarity approval does not replace those independent stages, and
the current author session supplies neither verdict.

Deliverables: supplied eval inputs, reused reporting scenarios, contrast rubric,
targeted setup tests, disposable-install identity and retained consumer evidence.
Actual contract impact: evaluation inputs/oracles for existing human-readable
outputs; no production workflow or runtime dependency change.
Executable contract declarations changed: none.

## Evidence retention after completion

The owner subsequently requested cleanup. [The cleanup record](t004-evidence/cleanup.md)
identifies reproducible source/test copies removed after byte-for-byte
reconstruction checks. Generated outputs and supplied documents remain;
[the manifest](t004-evidence/retained-files.json) now covers surviving original
evidence. Earlier counts and review identities describe the pre-cleanup snapshot.
