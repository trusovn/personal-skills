# Task Brief: `T-004.1` — Install the development profile in genuine unborn repositories

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 12 tool calls / 30 minutes / 45k context
```

## Execution sizing

- Sizing policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 12. Estimated implementation duration: 30 minutes.
- Estimate confidence: medium. Intended profile: `standard / high`.
- Policy result: fits. Triggered limits: none. Decomposition override: none.
  Implementation/local verification only; reuse existing Git fixtures.

## Readiness route

standalone guided preflight — confirm reviewed T-001–003 dependencies, current
identity consumers and installed availability commands. Derived `verification.md`,
then ready `preflight.md`, are required before implementation.

## Verification-design recommendation

separate — distinguish a genuine unborn HEAD from Git errors and demonstrate
the repair through staged and final installed availability without changing
fingerprint semantics. Existing Python/Git subprocess fixtures are believed
available; fixture setup is task-local, with no shared harness prerequisite.

## Outcome

The canonical installer and installed availability entry point work in a real
Git repository with no commits, report explicit unborn identity, and retain
committed/detached behavior and genuine-error handling.

## Direction trace

- Contribution: parent P-01/P-05; `CAP-003`, `FLOW-004`, `ART-009/010`,
  `IF-007`, `INV-009`.
- User-observable effect: installation before a project's first commit succeeds.
  Enables .2/.3 qualification and T-005's installed-flow proof.
- Why now: T-001–003 source changes precede distribution; unborn availability
  is required before the final install/check/refresh journey.
- Decisions used: [plan](../../project-plan.md), sections 1–2, IF-007,
  FLOW-004, T-004 integration boundary and section 11's real Git cases;
  [parent](../T-004/brief.md).
- New direction decisions required: None.

## Authority and scope

- Authority: cited plan sections; `T-004` [task-map entry](../../task-map.json).
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: completed/reviewed `T-001`, `T-002`, `T-003`; no readiness claim here.
- Allowed: narrow changes in `scripts/workflow_version.py`,
  `scripts/run_evidence.py`, `scripts/install_development_skills.py` as required
  for installer/identity/availability only; their owning tests
  `tests/test_workflow_version.py`, `tests/test_run_evidence.py`,
  `tests/test_install_development_skills.py`; directly affected install/identity
  guidance in root README, `skills/README.md`, flow README.
- Inspect `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
  `SHARED_SCRIPT_FILES`; synchronize actual dependency/distribution changes.
  No new helper is presumed. Source shared tooling remains under `scripts/`;
  installed tests invoke sibling `.agents/scripts/` in disposable targets.
- Read-only: current `.agents/`, plans, index and historical evidence. Existing
  installer `init_repo` helper commits; unborn coverage must omit that commit.
- Out of scope: profile checker (.2), refresh composition (.3), full collector
  begin/resume lifecycle, fingerprint file selection/framing/hash changes,
  fabricated HEAD, unrelated Git behavior and active installation refresh.
- Assumptions: decisive mechanisms exist (temporary Git repos and subprocess
  CLIs). Exact explicit unborn representation and narrow implementation are local
  design; existing consumer compatibility is a preflight fact, not a new requirement.

## Work and acceptance criteria

1. Reproduce the unborn installation failure at the canonical CLI, then repair
   only its identity/availability path. Use testing-discipline; reuse existing
   setup and preserve distinct installed-layout/fingerprint cases.
2. Extend focused coverage and affected guidance; expose the usable identity
   and installed availability interface for .2/.3.

- **AC-01:** `python3 scripts/install_development_skills.py <target>` succeeds
  after real `git init` without any commit. Final installed
  `run_evidence.py --repo <target> availability` reports available. HEAD remains
  genuinely unborn; no commit or fake object is created.
- **AC-02:** Workflow identity explicitly distinguishes unborn state from a
  resolved commit and from an actual Git failure. Non-unborn Git errors remain
  reported failures, never missing-commit success. Committed and detached HEAD
  keep their actual commit identities and successful install/availability behavior.
- **AC-03:** Fingerprint framing, included/excluded files, ordering and location
  independence remain unchanged. Installed/source equivalent package bytes keep
  equivalent fingerprints; unrelated Git commits do not redefine them.
- **AC-04:** The installer retains its existing managed selection and ownership;
  changed helper bytes are projected from source. Guidance states the exercised
  unborn boundaries and does not claim full collector lifecycle support.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-009: truthful Git identity | Real unborn, committed, detached; non-unborn Git failure | Canonical install and final installed availability; Git HEAD state agrees with identity; genuine errors remain failures | Fail-first unborn CLI; real success fixtures; controlled Git-boundary error only where needed | Independently initialize an unborn target, inspect HEAD before/after, then contrast an actual invalid Git target | .1 implementer: targeted/owning modules; fresh discovery: justified aggregate after clean rows |
| R-02 / INV-009: unchanged fingerprint contract | Source and installed layouts; included-file change; excluded-file change; unrelated commit; deterministic ordering | Existing identity/fingerprint entry point and independent package bytes | Retain existing semantic cases and add only missing unborn boundary evidence | Compare an installed package fingerprint before/after an unrelated first commit | .1 implementer: workflow owning suite; discovery: current aggregate record |

## Verification

- Fail-first: genuine unborn installer fixture must fail for the HEAD/availability
  defect before the repair, not for missing fixture inputs. Record setup/result.
- Targeted changed cases first; then affected owning modules, one command at a time:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`,
  and the same command with `test_workflow_version.py` / `test_run_evidence.py`
  for changed identity/availability behavior. Preflight resolves new case selectors.
- Fresh discovery owns the justified aggregate across affected modules once
  current targeted rows/probes are clean, including after correction (plan IF-004).
  Derived verification resolves its exact command. Acceptance consumes that record.
  Correction implementers run targeted/owning checks; no duplicate broad gate.
- No whole-repo, network or model-budget gate. Record skips and residual gaps.

## Expected contract impact

- Materialize unborn support at `ART-010`'s exercised identity/availability boundary;
  change `ART-009` helper bytes; preserve `IF-007`, `INV-009`, `FLOW-004`.
- Current dependencies: canonical installer and identity/availability functions
  in the named scripts. No `docs/contracts` registry is present.
- Expected delta: genuine unborn installation with explicit identity, consumable
  by .2/.3; no collector lifecycle expansion or fingerprint redefinition.

## Stops and handoff

- Stop for changed authority, user-work overlap, unsafe permission needs, a
  missing decisive capability or scope expansion into collector lifecycle.
- Preserve existing task-specific stops, including two materially different fixes
  failing the same targeted behavior. Budget is a soft checkpoint.
- Next: derive verification, obtain ready standalone guided preflight, then
  implement .1. Submit current scenario evidence and exact interface/gap notes.
- Required follow-on: immediately after implementation or correction and any
  applicable conditional stages (maintainability/architecture, then registry
  synchronization if applicable), hand completed bytes to a fresh independent
  `task-review-discovery` call, then its report to a separate
  `task-acceptance-review` decision. Same-session self-review is not acceptance.
