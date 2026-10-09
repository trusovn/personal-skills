# Task Brief: `T-002.1` — Publish and distribute independent discovery evidence

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 15 tool calls / 40 minutes / 50k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 15. Duration: 40 minutes. Confidence: medium.
- Intended profile: `standard / high`. Policy result: fits; triggered limits:
  none; decomposition override: none. Equality with a maximum fits.
- Implementation estimate includes new package, fixtures, installer/entry
  synchronization and targeted local checks, excluding separate stages/evals.

## Readiness route

standalone guided preflight — confirm current T-001 inputs, existing disposable
fixtures and installer selectors. Derive `verification.md`, then obtain ready
`preflight.md` before implementation.

## Verification-design recommendation

separate — evidence completeness, inherited real-boundary cases, partial reports
and aggregate ordering can be lost during extraction. Existing review fixtures
and installer tests are believed available; this is command/setup confirmation,
not a new verification mechanism or shared-harness prerequisite.

## Outcome

`task-review-discovery` independently publishes current evidence and confirmed
findings, without deciding acceptance, and installs with its required references.

## Direction trace

- Contribution: `CAP-002`, `FLOW-002/003`, `ART-006/009`, `IF-004`,
  `INV-001/004/005/011`; preserve installer ownership under `INV-009`.
- Effect: reviewers can hand a complete or explicitly partial evidence report
  to a separate decision call; enables .2 admission and `T-005` role proof.
- Why now: consumes T-001's verification/readiness/context contract before .2.
- Decisions: plan sections 4, 6–7, 10 (`T-002`) and 11 evidence ownership.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), cited sections; `T-002`
  in [task-map.json](../../task-map.json); parent [brief](../T-002/brief.md), P-01–03/08.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Depends on completed/reviewed `T-001`; consumes `ART-001/002/003/004/005/009`;
  produces `ART-006` and discovery's part of `ART-009`.
- Allowed: new `skills/task-implementation-flow/task-review-discovery/` package,
  report reference and task-local eval fixtures; discovery-focused additions to
  `tests/test_review_discipline.py`; canonical installer selection, focused
  `tests/test_install_development_skills.py`, and discovery-specific entries in
  root `README.md`, `skills/README.md`, flow README. Inspect/synchronize
  `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`;
  no shared helper addition is expected.
- Read-only: current acceptance skill/report/evals as preservation authority,
  T-001 sources/evidence, plans and installed `.agents/` copies.
- Excluded: acceptance rewrites (.2/.3), final overview reconciliation (.4),
  new schemas/executors, T-003 routing redesign, T-004 installation features,
  active installation refresh, actual agent evals and historical-report edits.
- Assumptions: no new direction choice; exact targeted selectors are preflight
  facts. A direct edit's context may be conversational; ART-003 is explicit for
  prepared packages, without imposing high-assurance inputs on guided review.

## Work and acceptance criteria

1. Extract discovery obligations into a standalone skill, report reference and
   supplied runnable fixtures, preserving the old evidence protections.
2. Add the new skill/references to distribution in this change, with local proof.

- **AC-01:** A fresh session independent of production authorship reads authority,
  verification, explicit ART-003 context, current submission and applicable
  conditional evidence. It publishes facts/suggested severity and complete or
  partial coverage; no acceptance verdict, approved deferral or advancement.
  Author sessions remain self-check-only and route to a fresh discovery call.
- **AC-02:** Stable rows retain current pass/fail/blocked/unchecked evidence,
  concrete reasons, setup/oracle, exact probes and all findings. Findings include
  location, trigger, consequence, affected AC/invariant, bounded credible sibling
  surface and invariant-level direction. Authority omissions cannot vanish behind
  green tests. Context selects bounded decisive material-risk probes.
- **AC-03:** Retain public wiring, first legitimate state change and next real
  occurrence, interacting-state, schema valid/targeted-invalid and real-process
  evidence requirements from current acceptance. Continue independent safe,
  affordable probes after a finding. Reports never claim their own authenticity.
- **AC-04:** Reconcile all material rows before the aggregate. After decisive
  targeted failure, suppress it except for a distinct authorized diagnostic
  purpose. Fresh correction discovery owns one justified aggregate after clean
  targeted evidence, including regressions/unfinished rows. An omitted material
  row makes the old gate premature. Record exact command or not run, owner,
  stage, reason and current evidence; add no gate or command.
- **AC-05:** Ordinary review is read-only except an authorized next-unused
  `reviews/discovery-NN.md`; never edit production, tests, trackers or prior
  reports. Guided output may be inline. Installed bytes include the new skill
  and required references; unrelated files and AGENTS text remain unchanged.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| D-01 / INV-004/005 | Independent/author session; complete/partial; all four row states | Supplied role inputs produce provenance, retained ledger and evidence-only output | New contract/fixture checks rejecting a verdict-bearing or silently clean partial report | Trace an omitted AC and an unfinished sibling row into the output requirements | .1 implementer: local owning checks; actual role behavior T-005 |
| D-02 / INV-005 | Current acceptance evals 1–5, 7–9: repeated queue claim, export/resume/retry, absent concurrency helper, changed index blob, interacting ledger states, coherent tamper/replay/decision, resistant descendant/pipe-holder/race | Real public/filesystem/validator/process boundary with bounded cleanup; inherited cases remain independently exercisable | Preserve supplied starting state, real invocation, expected signal and cleanup in discovery fixtures; do not replace them with wording-only checks | Audit a lifecycle and process fixture for a real second occurrence/observable cleanup; valid and invalid instances for relevant validator | .1 implementer: fixture setup/local probes; T-005: separately authorized calls |
| D-03 / INV-005 | Targeted fail → suppressed aggregate; correction → clean targeted rows → one aggregate; later omitted row → premature gate | Ordered probe/gate record tied to current bytes | Setup and expected records for each transition; local tests distinguish record structure from role compliance | Inspect an unchecked row discovered after a reported aggregate | Discovery: aggregate during initial/correction review; acceptance consumes only |
| D-04 / INV-009 | New install and explicit rerun; selected skill/references/guide/helpers/block versus unrelated bytes | Canonical installer in disposable committed Git target; byte comparison | Extend existing real installer tests, including unmanaged preservation | Add one unrelated target file and inspect it after rerun | .1 implementer: installer suite after targeted pass |

## Verification

- Fail-first: focused new discovery/profile assertions reject absent package or
  missing inherited obligations for the intended reason. Label wording evidence
  as structural; fixture setup alone is not agent behavior proof.
- Targeted selectors: derived verification/preflight resolve new discovery
  fixture checks and focused installer selector. Reuse existing setup/probes;
  do not build a generic harness.
- Owning local suites, implementer after targeted pass, one at a time:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py`
  then the same command with `-p test_install_development_skills.py`.
- Reviewer uses a distinct narrow corroboration, not a routine repeated suite.
  Workflow aggregates obey AC-04. No repository-wide, network or agent-budget
  check here; preserve raw setup/results and unrun role checks for T-005.

## Expected contract impact

- Materialize `ART-006` / `IF-004`; change `ART-009` selection/guidance;
  preserve `INV-001/004/005/011` and installer ownership.
- Dependencies: implemented T-001 `ART-002/003/004`, current conditional sources,
  installer and review fixtures; no current `docs/contracts` registry.
- Delta: independent evidence producer with stable report/continuation boundary
  and managed distribution. .2 consumes it; no machine enforcement is introduced.

## Stops and handoff

Stop for authority ambiguity, predecessor mismatch, user-work overlap, unsafe
permissions, scope expansion or unavailable decisive capability. Preserve user
changes, including pre-existing root AGENTS.md edits. Budget is a soft checkpoint.
Next: derived verification → ready standalone preflight → bounded implementation.
Required follow-on: immediately after implementation or correction, hand completed
bytes to a fresh independent acceptance reviewer, preserving applicable prior
conditional stages; end the implementation invocation. Once reviewed, .2 consumes
this output. New source text does not change the current session's installed skill.
