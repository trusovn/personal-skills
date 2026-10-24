# Task Brief: T-001.1 — Install a portable, target-aware measurement runtime

## Outcome

An installed launcher measures a separate target repository with its own policy
or shipped defaults. Runtime files and dependency pins come from the same
installation. Explicit setup selects that target; measurement never installs
packages. T-001.2 can then change report behavior through this stable runtime.

## Direction trace

- Direction contribution: plan section 1's portable measurement capability and
  sections 6–7's preservation and authority boundaries.
- User-observable effect: installed baseline/compare works outside the source
  checkout; missing dependencies identify the selected target's setup command.
- Why now: T-001 is the prerequisite for T-002's starting-code handoff.
- Direction decisions used: plan sections 1–2, 6–7 and T-001 in section 10.
- New direction decisions required: None.

## Authority and scope

- Authority: [parent authority and reviewed identities](../T-001/brief.md#authority-and-scope),
  especially project-plan section 7's installation/settings contract.
- Repository: `personal-skills`; follow `AGENTS.md`, `docs/project-map.md` and
  `docs/development.md`.
- Dependencies: none. The current installer and native measurement adapter exist.
- Allowed changes: `scripts/measure_maintainability.py`; relocation of
  `tools/maintainability.py` and `tools/maintainability_env.py` into `scripts/`;
  flat shared defaults and pinned requirements beside them; relevant
  `tests/test_maintainability.py` and `tests/test_install_development_skills.py`;
  `scripts/install_development_skills.py`, `skills/README.md`, `README.md`,
  `scripts/measure-maintainability.md`, and stale paths in `docs/project-map.md`
  or `docs/development.md` caused by this relocation.
- Out of scope: neutral labels/empty-baseline extension (T-001.2), foundation
  skill guidance/final composition (T-001.3), and parent exclusions.
- Read-only context: existing measurement and installer tests, `.quality/`
  settings/pins, `tests/staging_fixture_support.py`, and the contract records below.
- Assumptions: a prepared pinned analyzer interpreter is believed to exist;
  exact availability is UNKNOWN for preflight. No dependency download is authorized.

Keep the public `baseline`/`compare`/`measure`, `--root`, scope and `--output`
interfaces. Add `setup --root <target>`. Keep one shipped-default source;
the source repository's `.quality/` files remain deliberate target policy.
Select each target settings file independently, with its corresponding shipped
fallback. Invalid present settings fail. Pins remain installation-owned.
Keep environments/reports in target `.quality/`; no global helper fallback,
active-installation refresh, or generic installer extension is allowed.

### Expected contract impact

- Materialize ART-001/IF-001 for CAP-001/FLOW-001; preserve
  INV-001/INV-002/INV-003/INV-006/INV-007/INV-009. Preserve ART-007/IF-004 policy.
- Current dependencies: [installation](../../contracts/installation.json) owns
  `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`
  and narrow replacement; [runtime evidence](../../contracts/runtime-evidence.json)
  supplies optional existing capture, not a new required lifecycle.
- Expected delta: installed runtime/default/pin paths and target-aware resolution
  become discoverable implemented contracts. The designated registry-updater
  stage records only the completed delta, including installation membership.

## Work and acceptance criteria

- **AC-01:** Source and installed public launchers resolve all runtime helpers,
  pins and defaults locally. A disposable installation runs real pinned
  baseline/compare from an unrelated cwd without reading the source checkout.
- **AC-02:** For each of `maintainability.toml` and `ruff.toml`, target presence
  selects target policy and absence selects its shipped default. Mixed origins
  work. Reports record effective settings identity/origin; malformed present
  files fail visibly. Unrelated root Ruff config is not inherited.
- **AC-03:** Setup uses the selected target and installation-owned pins.
  Native environment keys retain platform/interpreter/pin separation; invoking
  a correctly pinned interpreter remains supported. Measurement with unavailable
  pins fails with an executable, target-aware setup instruction and no provisioning.
- **AC-04:** Preserve actual dirty/staged/untracked snapshots, scope compatibility,
  analyzer semantics, native unknowns, separate asset groups and exclusions.
  Breaches alone return execution success; partial/incompatible runs stay explicit.
- **AC-05:** Extend existing install/refresh/read-only drift coverage for every
  new managed file. Preserve unmanaged files, target policy, environments/reports,
  outside-marker AGENTS bytes, source bytes and real index. Synchronize installer
  selections, profile guide, README and relocation map in this child.

### Finite-risk cases

#### R-01 — Wrong policy or runtime origin; AC-01–AC-03

- Invariant: INV-003/INV-006/INV-007; measurement uses the selected target and
  installation, with truthful effective identities.
- Material cases: both settings absent; each independently present; both present;
  malformed present file of either family; conflicting unrelated Ruff config;
  correctly pinned caller; native target environment; unavailable pins.
- Oracle/boundary: actual launcher results and settings identities at a separate
  target; missing-tool runs leave no new environment/packages.
- Implementation evidence: extend settings/launcher cases and a real disposable
  installed invocation. Observe setup's target/pin arguments without network;
  this observation does not claim a completed dependency installation.
- Independent review probe: use a different target setting and unrelated cwd;
  verify reported identity, chosen target environment and no source-path fallback.
- Gate owner/stage: implementer runs targeted and owning suites before submission;
  fresh discovery corroborates the separate-target boundary.

#### R-02 — Relocation or refresh loses evidence/ownership; AC-04–AC-05

- Invariant: INV-002/INV-006/INV-007; only declared installed resources change.
- Material cases: fresh install, managed-file refresh, missing/changed managed
  resource detected by `--check`; staged, unstaged and untracked source;
  target settings, environment/report files, unmanaged skill/helper and outside
  AGENTS block bytes. Preserve saved JSON and sibling text reports.
- Oracle/boundary: before/after byte and real-index identities in disposable Git
  targets; real native values and unknowns retain existing meaning after relocation.
- Implementation evidence: update existing installer preservation/drift and
  snapshot cases rather than copy their setup.
- Independent review probe: remove one shipped resource in a disposable install;
  verify precise drift and read-only behavior, then inspect a refresh's preservation.
- Gate owner/stage: same ownership as R-01; T-001.3 owns final combined broad proof.

## Verification

Verification-design recommendation: separate — independent settings fallback,
installation isolation and real filesystem/index preservation need explicit cases.

First derive `verification.md` using existing coverage, then confirm prerequisites
in preflight. The implementer demonstrates new assertions reject the old
source-dependent behavior where feasible. Run targeted cases first, then
`<pinned-python> -B -m unittest discover -s tests -p test_maintainability.py`,
then `python3 -B -m unittest discover -s tests -p test_install_development_skills.py`.
Missing-analyzer skips do not satisfy AC-01 or AC-04. Run required architecture
and contract checks before handoff. T-001.3 owns the final cross-cutting
`python3 tools/verify.py`; do not duplicate it solely for reporting.

## Execution and handoff

Status: `ready`
Task kind: `executable`

Guided profile. The brief is prepared; execution prerequisites remain required.
Readiness route: standalone guided preflight after derived `verification.md`;
write a ready `preflight.md` before implementation. Confirm analyzer availability,
current paths, install fixture isolation, and exact pre-edit source preservation.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 20 tool calls / 50 minutes / focused runtime and installer context
```

### Execution sizing

- Sizing policy: `default@1`, active project-local `references/task-sizing.yaml`.
- Estimate: 20 agent calls; 50 implementation minutes. Confidence: medium.
- Policy result: `override_cannot_split_safely`.
- `decomposition_override: cannot_split_safely` — calls and duration exceed the
  active maxima. Separating runtime relocation from installer/default registration
  would leave a non-distributable shared dependency and force both agents to
  renegotiate paths, duplicate settings fixtures and edit the same guide/tests.
  Keep this coupled boundary whole; report behavior and foundation work are
  already separate. Residual risk is a longer implementation call; the budget
  is a soft checkpoint, not permission to drop preservation evidence.

### Stops and next action

- Stop for changed owner policy, need for a generic installer, absent decisive
  real-tool evidence, or a required dependency repair/download without approval.
  Do not alter pins/settings to force smaller metrics.
- Capture exact pre-edit bytes before any new-runtime self-check; unavailable
  before evidence must be reported, never replaced by current bytes.
- Next: verification design, then preflight, then implementation. Hand runtime
  paths/settings/setup behavior and current evidence to T-001.2.
- After implementation or correction, run applicable maintainability review,
  then contract-registry synchronization. Immediately hand completed bytes to
  fresh independent `task-review-discovery`, then its report to a separate
  `task-acceptance-review` decision. Retain existing conditional stage order;
  same-session checks do not constitute independent acceptance.
