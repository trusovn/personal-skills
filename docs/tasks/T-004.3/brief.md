# Task Brief: `T-004.3` — Prove explicit refresh and distribution closure

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 10 tool calls / 25 minutes / 40k context
```

## Execution sizing

- Sizing policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 10. Estimated implementation duration: 25 minutes.
- Estimate confidence: medium. Intended profile: `standard / high`.
- Policy result: fits. Triggered limits: none. Decomposition override: none.
  Implementation/local verification only; reuse install/rerun and .2 fixtures.

## Readiness route

standalone guided preflight — confirm reviewed .1/.2 outputs, exact check CLI
and current owning test selectors. Derived `verification.md`, then ready
`preflight.md`, are required before implementation.

## Verification-design recommendation

separate — ordered real install/check/drift/refresh occurrences and preservation
require composed evidence beyond isolated comparator tests. Existing reinstall
entry point, disposable Git fixtures and .2 snapshots are believed sufficient;
no new shared helper/harness or agent-role runner is authorized.

## Outcome

In disposable unborn and committed targets, a maintainer can install, detect
drift without mutation, explicitly refresh, and recheck a restored match while
unmanaged state survives; current documentation and evidence expose this flow
for T-005.

## Direction trace

- Contribution: parent P-01–06 closure; `CAP-003`, `FLOW-004`,
  `ART-009/010/011`, `IF-007`, `INV-009`.
- User-observable effect: deliberate refresh repairs managed drift without
  removing local skills/helpers or unrelated project instructions. The qualified
  projection enables T-005's next demonstrable installed-flow behavior proof.
- Why now: .1 supplies unborn installation; .2 supplies the check interface;
  their outputs must compose before T-005 claims an invoked profile is qualified.
- Decisions used: [plan](../../project-plan.md), sections 1–2, ART-009–011,
  IF-007, FLOW-004 and T-004 in sections 10–11; [parent](../T-004/brief.md).
- New direction decisions required: None.

## Authority and scope

- Authority: cited plan sections; `T-004` [task-map entry](../../task-map.json).
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: completed/reviewed [T-004.1](../T-004.1/brief.md) and
  [T-004.2](../T-004.2/brief.md). Consumes their ART-009/010/011 interfaces.
- Allowed: focused lifecycle additions/consolidation in
  `tests/test_install_development_skills.py`; minimal installer repairs required
  for explicit rerun restoration/unmanaged preservation; affected root README,
  `skills/README.md`, flow README; new `docs/tasks/T-004.3/results.md`.
- Inspect/synchronize `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
  `SHARED_SCRIPT_FILES`, focused expectations and guidance. Preserve selection
  unless actual approved dependency changes require synchronization. Reuse
  current rerun tests and .2 snapshots, keeping .1/.2 local cases intact.
- Read-only: current `.agents/`, plans/index, historic results/reviews and .1/.2
  implementations except bounded integration repair. A broader identity/check
  defect returns to its owning leaf rather than widening this task.
- Out of scope: automatic refresh, active installation mutation, collector
  lifecycle, fingerprint changes, expanded managed ownership, retained versions,
  official-plan edits, live/model-budget or role-call qualification.
- Assumptions: existing reinstall is the refresh action. Exact .2 CLI is an
  explicit produced dependency, not a choice to reinvent here.

## Work and acceptance criteria

1. Exercise the full journey through canonical CLI calls in disposable targets.
   Extend/reuse existing distinct tests under testing-discipline.
2. Reconcile distribution guidance and record exact local setup, commands,
   installed identities, results and unrun T-005 boundaries in a new results file.

- **AC-01:** Both genuine unborn and ordinary committed targets complete:
  first install → matching check → deliberate managed drift → read-only drift
  check → explicit installer rerun → matching recheck → second matching check.
  Check calls do not repair drift. Refresh requires a separate explicit call.
  Unborn HEAD stays unborn throughout; .1 retains detached compatibility proof.
- **AC-02:** Refresh restores current source bytes for changed/missing skill,
  reference/eval/setup, guide, shared helper/config/schema and marked block;
  removes an extra owned file. The final independently inspected projection
  agrees with check output. Use finite representative family cases, not a full
  state-by-family Cartesian product or duplicated .2 comparator coverage.
- **AC-03:** Unselected skills/references, non-managed helpers, other project
  files and AGENTS text outside the block survive. For an existing block, compare
  outside-block bytes before/after refresh; for first insertion, retain original
  instruction text. Managed markers remain singular. Keep existing malformed
  marker/refusal coverage and do not repair unsafe targets silently.
- **AC-04:** Installer selection, guide/helpers, focused tests and READMEs agree
  on install, check, result semantics and explicit refresh between invocations.
  Existing install syntax and fingerprint framing remain compatible. No claim
  extends to full unborn collector lifecycle or retained active-run versions.
- **AC-05:** New results contain reproducible starting states, exact CLI/probes,
  observed outputs and installed package/helper identity evidence. Distinguish
  filesystem/Git proof from unrun skill-call/model behavior. T-005 receives the
  qualified projection/check interface and exact remaining qualification gaps.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-009: deliberate restoration | Unborn/committed; first install → match → drift → explicit refresh → match → repeated match; changed/missing/extra owned files across AC-02 families | Real canonical install/check calls; independent source/installed byte comparison; Git state and check snapshots | Extend current rerun case for ordered .2 calls; reuse family coverage, record stage results | Independently remove a managed reference, add an extra owned file, then refresh/recheck | .3 implementer: targeted lifecycle and installer suite; fresh discovery: final justified aggregate |
| R-02 / INV-009: narrow preservation | Unselected skill/reference; non-managed helper; unrelated project file; outside-block text; existing block and first insertion | Before/after bytes and singular markers; existing unsafe/malformed input remains refused | Reuse unmanaged sentinel test, strengthen only distinct missing byte evidence | Add outside-block whitespace and an unmanaged helper, verify they survive refresh exactly | .3 implementer: targeted preservation; discovery: corroboration then aggregate |

## Verification

- Targeted lifecycle/preservation cases first; demonstrate a controlled owned
  deletion/change is detected and restored. If a preservation bug needs repair,
  record its fail-first regression before editing.
- Owning command:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`.
  Preflight resolves focused case selectors using current .1/.2 outputs.
- Fresh discovery owns one justified final aggregate after required targeted
  evidence/probes are clean, including corrections: installer, workflow-version
  and run-evidence modules for distribution closure. Derived verification records
  the exact union command. Acceptance consumes current gate evidence and does
  not duplicate it; conditional owners keep their own applicable duties.
- No whole-repo/network/model-budget tests. Existing .1 fingerprint/detached
  evidence is reused only when still current; no fabricated or stale proof.

## Expected contract impact

- Close `ART-009/010/011`, `IF-007`, `INV-009`, `FLOW-004` composition.
- Current dependencies: reviewed .1/.2 contracts and canonical rerun installer;
  no `docs/contracts` registry. No new registry requirement.
- Delta: synchronized distribution usage and reproducible local lifecycle proof
  consumed by T-005. The results are evidence, not ART-012 agent qualification.

## Stops and handoff

- Stop for changed authority, user-work overlap, unsafe permission needs, missing
  decisive capability or scope expansion; return broader defects to .1/.2.
- Preserve the two-materially-different-failed-fixes stop. Budget is a checkpoint.
- Next: derive verification, obtain ready standalone guided preflight, then
  implement .3 and publish its new results. Never refresh this run's `.agents/`.
- Required follow-on: immediately after implementation or correction and any
  applicable conditional stages (maintainability/architecture, then applicable
  registry synchronization), hand completed bytes to fresh independent
  `task-review-discovery`, then its report to separate `task-acceptance-review`.
  Coordinator advancement and T-005 qualification remain separate authorized work.
