# Task Brief: `T-004.2` — Add explicit read-only development-profile checking

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 15 tool calls / 40 minutes / 50k context
```

## Execution sizing

- Sizing policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 15. Estimated implementation duration: 40 minutes.
- Estimate confidence: medium. Intended profile: `standard / high`.
- Policy result: fits (equality fits). Triggered limits: none. Override: none.
  Implementation/local verification only; one comparator and existing fixtures.

## Readiness route

standalone guided preflight — confirm reviewed .1 interface, managed projection
and current source/target validation. Derived `verification.md`, then ready
`preflight.md`, are required before implementation.

## Verification-design recommendation

separate — full projection comparison, three result classes, finite managed
families and absence of writes require discriminating filesystem/Git evidence.
Real local temporary repos and byte snapshots are believed available. No new
shared verification harness or feasibility task is required.

## Outcome

A maintainer can explicitly compare the installed development profile with
its canonical source and distinguish match, precise managed drift and check
failure, without changing files, Git metadata or evidence state.

## Direction trace

- Contribution: parent P-02/P-03/P-05; `CAP-003`, `FLOW-004`,
  `ART-009/010/011`, `IF-007`, `INV-009`.
- User-observable effect: drift is visible before an explicit refresh or new
  invocation. Enables .3 recovery proof and T-005's installed-profile qualification.
- Why now: .1 supplies installable unborn/committed profiles; .3 consumes this
  check interface to demonstrate drift and restoration.
- Decisions used: [plan](../../project-plan.md), ART-009–011, IF-007,
  FLOW-004, T-004 in sections 10–11; [parent](../T-004/brief.md).
- New direction decisions required: None.

## Authority and scope

- Authority: cited plan sections; `T-004` [task-map entry](../../task-map.json).
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependency: completed/reviewed [T-004.1](../T-004.1/brief.md). Consumes the
  canonical ART-009 selection and installed ART-010, produces ART-011.
- Allowed: check CLI/comparison in `scripts/install_development_skills.py`,
  focused `tests/test_install_development_skills.py`, and check usage in root
  README / `skills/README.md`. Exact CLI/result encoding is local design;
  preserve existing positional install invocation. Prefer the canonical installer
  module and constants; no separately distributed checker is presumed.
- Inspect/synchronize `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
  `SHARED_SCRIPT_FILES` if actual dependencies change. Source comes from the
  installer location, not caller CWD, under the existing distribution contract.
- Read-only: `.agents/`, identity/availability code and .1 evidence, flow source
  policy, plans and prior reports. Reuse current installer fixture/setup helpers.
- Excluded: installation/refresh during checking, new managed ownership, blanket
  comparison of `.agents`, runtime fingerprint shortcuts, run start, collector
  repair, retained versions, live/model-budget checks and active refresh.
- Assumptions: byte/path comparison and Git fixtures exist. Exact new CLI and
  selectors remain local design/preflight facts; no missing product decision.

## Work and acceptance criteria

1. Add an explicit check mode using the canonical install projection and narrow
   ownership. Document result/exit semantics for human and subprocess callers.
2. Reuse existing temporary installer fixtures for deliberate drift, failures
   and before/after snapshots. Use testing-discipline; no parallel harness.

- **AC-01:** A freshly installed profile matches in real unborn and committed
  targets. Match, drift/missing and check failure are observably distinct through
  documented output and exit semantics. Unusable source/target or unreadable
  required content cannot be reported as match; diagnostics identify scope/reason.
- **AC-02:** Comparison covers every file copied into each selected skill,
  including references, evals and setup files; the managed guide; each explicitly
  managed shared script/config/schema; and the expected marked AGENTS block.
  Compare complete projection contents and report changed/missing/unexpected
  managed paths. Use the installer's existing transient-copy exclusions; workflow
  fingerprint exclusions do not define profile equivalence.
- **AC-03:** Additional unselected skills, non-selected script files and AGENTS
  text outside the marked block do not cause drift. Extra non-transient files
  inside selected skill directories do cause drift. A missing block is drift;
  malformed/ambiguous markers cannot yield match and get a precise diagnostic.
  Unsafe path shapes retain existing refusal boundaries without traversing them
  as trusted installations.
- **AC-04:** Every check result leaves source/target files, managed and unmanaged
  bytes, Git state/metadata and evidence storage unchanged. Do not call install,
  stage copies, create `.agents`, refresh, or start a run. Existing availability
  probes write under Git metadata and cannot establish read-only checking.
- **AC-05:** Existing install CLI compatibility and ownership remain intact.
  Check guidance documents comparison scope, result semantics, source resolution
  and deliberate between-invocation refresh; no retained-version guarantee.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-009: full managed projection | Skill SKILL.md; reference; eval/setup file; profile guide; helper/config/schema; marked AGENTS block; changed/missing bytes and unexpected selected-directory file | Public check CLI reports exact owned drift against independently enumerated fixture bytes; all selected packages/shared files covered | Table-driven families, not a Cartesian product; include eval/setup drift that leaves workflow fingerprint unchanged | Alter one fingerprint-excluded managed file and one helper in a disposable installed target | .2 implementer: targeted comparison and installer suite; fresh discovery: justified aggregate |
| R-02 / INV-009: precise outcomes and ownership | Match; drift/missing; actual check failure; absent/malformed block; unmanaged skill/script/outside-block text; unsafe existing path shape | Documented output/exit class; unmanaged changes ignored, unsafe/unreadable input never match | Real filesystem CLI cases; controlled boundary failure only if a real failure cannot be made deterministic | Contrast an extra owned file with an extra unselected helper; inspect one failure diagnostic | .2 implementer: targeted and owning suite; discovery: current corroboration |
| R-03 / INV-009: read-only | Match, drift and failure in unborn/committed repos; absent installation; repeated check on unchanged input | Before/after path/type/content and relevant Git/evidence snapshots identical; no created directories or probe artifacts | Snapshot every result class; compare source as well as target; repeated invocation agrees | Run check twice on a missing installation, inspect `.agents` and Git metadata for side effects | .2 implementer: no-write targeted cases; discovery: independent snapshot then aggregate |

## Verification

- Targeted CLI cases must reject the old missing-check behavior and plausible
  incomplete/fingerprint-only comparison. Supply real installed inputs, then
  mutate owned bytes deliberately; leave production mutations absent.
- Targeted selectors are resolved in derived verification/preflight. Owning:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`.
- Fresh discovery owns the justified aggregate after clean targeted rows/probes,
  including after correction; use the installer suite unless actual blast radius
  justifies another affected module. Acceptance consumes its exact command/result
  or not-run record without repeating execution. Conditional gates retain owners.
- No whole-repo/live/model gate. Snapshots prove exercised local behavior,
  not cross-platform enforcement or installed skill-call compliance.

## Expected contract impact

- Materialize `ART-011`; extend ART-009's installer interface; preserve ART-010
  ownership, `IF-007`, `INV-009`, `FLOW-004`.
- Current dependencies: canonical installer constants/copy policy and reviewed
  .1 output; no current `docs/contracts` registry.
- Delta: documented explicit non-mutating match/drift/failure interface consumed
  by .3 and T-005. No new registry, runtime identity algorithm or package manager.

## Stops and handoff

- Stop for changed authority, user-work overlap, unsafe permission needs, missing
  decisive evidence or required scope expansion. Budget is a soft checkpoint;
  preserve the existing two-materially-different-failed-fixes stop.
- Next: derive verification, obtain ready standalone guided preflight, then
  implement .2. Hand off exact CLI/result semantics, projection/exclusions,
  snapshot evidence and remaining gaps to .3.
- Required follow-on: immediately after implementation or correction and any
  applicable conditional stages (maintainability/architecture, then applicable
  registry synchronization), hand completed bytes to fresh independent
  `task-review-discovery`, then its report to separate `task-acceptance-review`.
  Same-session self-review does not fulfill either independent stage.
