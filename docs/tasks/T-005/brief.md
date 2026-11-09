# Task Brief: T-005 — Verify the complete installed handoff

## Outcome

Demonstrate that the installed measurement runtime composes across the complete
task journey: original baseline, actual edit, implementer comparison, separate
review comparison, and correction against the original baseline. Include a real
required native static-check failure and recovery. The owner and downstream
reviewers can then distinguish demonstrated tool behavior from prepared but
unrun agent behavior.

This is the final composition proof in the accepted project plan. It connects
the installed runtime and source workflow contracts delivered by T-001–T-004.
Scripted caller roles demonstrate composition, not independent agent judgment.
Prepare the remaining agent qualification inputs and grading route; executing
live agents requires separate approval and is not a completion prerequisite.

## Authority and scope

- Authority: [project plan, T-005](../../project-plan.md#t-005--verify-the-complete-installed-handoff),
  sections 1–7 and 11, and [task-map entry T-005](../../task-map.json).
  The [independent plan review](../../project-plan-review.md) accepted the plan.
  The plan persists owner-confirmed direction: one baseline, proportionate
  implementer feedback, independent reviewer comparison, and advisory metrics.
- Repository: `personal-skills`; follow [project map](../../project-map.md),
  [development guide](../../development.md) and repository instructions.
- Dependency: [T-004 acceptance](../T-004/reviews/acceptance-01.md) admits its
  corrected source workflow and eval preparation, and routes to T-005. It does
  not establish current readiness or installed end-to-end qualification. Its
  aggregate check failed because of active-installation drift; retain that
  limitation rather than treating acceptance as an aggregate pass.
- Allowed changes: owning measurement/installer tests and their existing fixture
  helpers; task-flow eval definitions, setup/check helpers and eval documentation
  only where composition or section 11 preparation evidence is missing; this
  task's results. Reuse before extending. Contract-record synchronization belongs
  to the designated registry-updater stage.
- Read-only context: `tests/test_maintainability.py`, especially
  `test_installed_and_source_launchers_work_without_distribution` and
  `test_native_hard_failure_remains_separate_from_installed_advisory_success`;
  `tests/test_install_development_skills.py` and its relocated-distribution
  helpers; implementer `evals/files/measurement_cases.json` and
  `check_measurement_fixture.py`; maintainability-review
  `evals/files/review_cases.json`, `check_review_fixture.py`, `review-evals.json`
  and eval README; existing preflight and discovery/acceptance route fixtures.
- Out of scope: production runtime or workflow redesign, new analyzers, runners,
  shared harnesses, policy registries, review stages, controller changes,
  automatic refactoring, live model execution, and active-installation refresh.
  A discovered production defect returns to the task owner for a bounded repair;
  do not weaken an oracle or expand this verification task silently.
- Inspect the canonical installer, `DEVELOPMENT_SKILL_SOURCES`,
  `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`, focused installer coverage and
  README installation instructions when changing profile-owned resources.
  Synchronize affected entries only. Preserve its narrow ownership boundary.

Use disposable installations, never refresh this run's active skills. Source
skills are development specifications, not substitutes for installed instructions.
Keep provisional advisory targets at 10/50/5. Preserve existing native-check
policy, scope, requiredness and stage owners. Below-target growth and untouched
legacy debt require no individual metric defense; retained affected breaches
follow plan section 5. No measurement result waives a hard native failure.

### Expected contract impact

- Produce composition and preparation evidence (`ART-006`) for all capabilities
  `CAP-001`–`CAP-005`, flows `FLOW-001`–`FLOW-003`, interfaces `IF-001`–`IF-004`
  and invariants `INV-001`–`INV-009`. Preserve the contracts of consumed
  `ART-001`–`ART-005`, `ART-007` and `ART-008`.
- Current dependencies: [measurement](../../contracts/measurement.json) owns
  portable CLI, report/baseline and preflight contracts;
  [installation](../../contracts/installation.json) owns managed projection;
  [implementer feedback](../../contracts/implementer-feedback.json) and
  [reviewer feedback](../../contracts/reviewer-feedback.json) own source caller
  guidance and prepared evals. [Runtime evidence](../../contracts/runtime-evidence.json)
  remains optional capture tooling.
- Expected durable delta: those records can point to the actual installed
  composition test/evidence and prepared qualification cases, narrowing only
  demonstrated proof limits. Do not remove live-compliance limits. The owner's
  handoff is `docs/tasks/T-005/results.md`, with exact evidence references and
  the remaining qualification work.

## Work and acceptance criteria

**AC-01 — Complete installed journey**

Exercise a disposable target installation with real pinned analyzers, from an
unrelated working directory and without access to its original source
distribution. Capture original baseline B before editing actual target code;
make an edit; invoke implementer comparison I; invoke a separate reviewer
comparison R on the same submitted bytes; make a second actual correction;
compare corrected bytes against unchanged B. Use the public installed CLI and
installation-local dependencies at each measurement step, not internal adapter
calls or a global/source helper fallback.

Each step supplies and checks the exact report pair, scope, tool/settings
identity, measurement status and actual source identity. R must be a distinct
invocation and output, not a copy of I. The correction must identify different
current bytes and still reference B. Carry usable baseline, comparison and native
evidence references across caller handoffs rather than merely naming CLI steps.

**AC-02 — Preserve source, index and historical reports**

At each measurement/check boundary, assert source and real Git-index preservation;
allow only the two deliberate edits and authorized report/evidence writes.
Include staged, unstaged and untracked starting code using existing fixture
support. Preserve original B and every earlier JSON/text report pair through
correction. Verify neutral labels and actual before/current values where known;
unknown values must remain unknown. Reuse owning evidence for added/deleted
paths, empty starts, settings, collisions and unavailable/incompatible runs
under V-001–V-004; rerun affected coverage rather than copying historical passes.

**AC-03 — Native failure and recovery remain effective**

Declare a real existing native static command and its whole governed scope,
policy, requiredness and owner in the disposable target. In the installed
journey, execute it on the edited input and observe an actual hard failure beside
successful advisory comparison. Correct the input, retain the failure history,
and recover passing evidence bound to corrected bytes without changing policy.
Carry command, checked bytes, result and producer/stage in the handoff.

For V-008, retain prepared cases for missing/unavailable/stale required evidence,
current aggregate coverage reuse without reporting-only duplicate runs, and
absence of native checks without inventing commands. Setup and command history
must exercise each claimed deterministic outcome. Scripted reuse does not prove
an agent chose the correct check owner or recovery route.

**AC-04 — Prepare decisive agent evals**

Map section 11's V-001–V-008 to current owning evidence, with explicit proof
limits. Reuse existing independently runnable scenario inputs and controls;
extend only distinct gaps. Preserve the full approved V-005 set: 6 -> 8 growth,
a justified cohesive breach, a materially touched unchanged legacy hotspot with
an untouched sibling, and extraction with misleading names/navigation. Preserve
V-006 missing-tool and incompatible-baseline cases with distinct advisory versus
required outcomes and a fresh reviewer comparison requirement. Preserve V-008's
native-policy, evidence-recovery, aggregate-reuse and no-checks cases.

Prepared cases supply executable setup, actual code/report/native-evidence
states, bounded actor requests, fresh-session requirements and independent
grading instructions. Grade actual diff, rationale, disposition, source/report
identity, edit/command order and invocation history, not keywords or setup exit
status alone. Retain V-004 correction and V-007 conditional entry/re-entry
coverage, including significant test/harness changes versus trivial tests-only
changes. Do not replace these with a new generic eval framework.

**AC-05 — Publish truthful final evidence**

Create `results.md` beside this brief, not completion edits to the official plan
or task map. Identify commands, interpreter/pins, setup, actual results, retained
raw evidence paths, skips, failures and their owners. Separate structural checks,
deterministic runtime composition, eval preparation and agent-behavior results.
Run focused suites, required architecture/contracts checks and the aggregate as
specified below. Native-analyzer skips do not qualify the installed journey;
unexecuted or failed required behavior is not complete.

Do not claim a live model result without separately authorized execution and
independent grading. With live evals unrun, state that agent compliance remains
unqualified and name the prepared cases and approval/runtime needed next.
Report active-profile drift as a failed diagnostic; do not refresh the active
installation or label the aggregate passed. Any unresolved completion gate needs
an explicit disposition from its authority owner.

## Evidence boundaries

Verification-design recommendation: separate — two edits, immutable original
reports, independent invocation, real native failure/recovery and finite eval
cases require derived scenarios and evidence allocation. Existing pinned-tool
tests and local fixture checkers provide the mechanism; this is composition of
available capabilities, not an unresolved feasibility proof.

Implementation must follow `testing-discipline` and inspect existing coverage
before adding tests. Extend the nearest installed journey/native-failure cases
and reusable setup rather than copying fixture infrastructure. Fresh agent
execution and independent semantic grading remain separate from scripted roles.

Start implementation verification with `tests/test_maintainability.py` using an
already prepared pinned interpreter; confirm versions against
`scripts/maintainability-requirements.txt`. Then run affected fixture checkers and
installer coverage, followed by the canonical architecture check,
`python3 tools/check_contracts.py --root .`, and `python3 tools/verify.py` for the
cross-cutting integration. Retain failures and truthful skips. Dependency repair,
live evals and other expensive checks require their applicable approval; this
brief grants none. Do not run these implementation checks merely to design it.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Profile: `guided`

Next: derive `verification.md` with `task-verification-designer`, then obtain a
ready `preflight.md` through standalone guided preflight. The brief is prepared;
these execution prerequisites remain required before implementation. Preflight
confirms the pinned interpreter and disposable-installation capability, source
dependency applicability, and current native-check obligations. It reports
active-profile drift without trying to repair this active installation.

Follow the active installation's [submission route](../../../.agents/skills/README.md#submission-route):
applicable architecture and independent maintainability review, contract-registry
synchronization, fresh discovery, then separate acceptance. Corrections re-enter
affected stages. Same-session self-check is not independent acceptance.

Launch guidance (intended settings; soft budget checkpoint):

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / focused context
```

### Execution sizing

- Sizing policy: installed `task-brief-designer/references/task-sizing.yaml`,
  `default` profile, version 1.
- Estimate: 15 agent calls; 40 implementation minutes; confidence: medium.
- Pair: `standard` / `medium`. Policy result: `fits`; equality fits the active
  numeric maxima.
- Basis: existing installed tests, real native-failure fixture and finite actor
  catalogs already provide the mechanisms and most cases. Work is the missing
  composed sequence, small fixture/oracle deltas and a current evidence map.
  No independent stage or live run is included in the estimate. If this requires
  a new shared harness or production repair, return to design instead of
  silently expanding scope.
