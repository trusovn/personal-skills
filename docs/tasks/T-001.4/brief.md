# Task Brief: `T-001.4` — Close preparation guidance and installed profile projection

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 12 tool calls / 32 minutes / 40k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 12. Estimated implementation duration: 32 minutes.
- Confidence: medium. Intended profile: `standard / medium`.
- Policy result: fits. Triggered limits: none. Decomposition override: none.
- Estimate includes integration edits, local deterministic tests and projection checks only.

## Readiness route

standalone guided preflight — confirm completed source contracts and disposable
installer fixture boundary. Plan section 1 requires separate verification and
compact durable readiness for this package.

## Verification-design recommendation

separate — distinguish source-contract consistency, actual installation projection
and unrun semantic qualification. Required by the packaged-stage rule. This is a
single local projection task; `T-005` owns actual multi-call workflow proof.

## Outcome and direction trace

Maintainers and installed-profile callers see one consistent preparation route,
and a real disposable installation receives the changed skills, references and
guide while preserving unmanaged state. This enables later qualified installed
skill invocations in `T-005`; it does not prove their semantic compliance.

- Authority: [project-plan.md](../../project-plan.md), sections 1, 4, 10–11;
  `T-001` in [task-map.json](../../task-map.json);
  parent [T-001](../T-001/brief.md), P-01–08 local composition closure.
- Contribution: `CAP-001`, `ART-009`, `FLOW-001/003`, `IF-001/002`,
  `INV-001/002/003/005/007/011`; preserve installer ownership `INV-009`.
- Why now: consumes all three completed/reviewed preparation source slices.
- Decisions used: section 10 T-001 synchronization boundary and section 11
  local proof versus composed installed behavior; no new installation capability.
- New direction decisions required: None.

## Authority and scope

- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Depends on completed/reviewed `T-001.1`, `T-001.2`, `T-001.3`; consumes
  `ART-001/002/003/004/009` source contracts, produces composed `ART-009` guidance
  and local distribution evidence. Disposable installed copies are test outputs,
  not an active-profile refresh or a replacement for `T-004` qualification.
- Allowed: cross-stage sections of root `README.md`, `skills/README.md`,
  `skills/task-implementation-flow/README.md`; focused
  `tests/test_install_development_skills.py` coverage; minimal canonical installer
  synchronization only if required by those changed sources. Preserve its constants'
  semantics and narrow ownership. No selected skill/helper addition is expected.
- Read-only: predecessor source contracts, installed `.agents/`, plans/review.
  A discovered source semantic defect returns to the owning child for correction.
- Excluded: unborn install, drift CLI, refresh redesign, discovery/rubric/correction
  changes, new shared tooling and semantic agent eval execution.
- Unresolved decisions: none; installer baseline is existing committed Git fixtures.

## Work and acceptance criteria

1. Reconcile cross-stage overview/examples with the predecessor contracts while
   preserving their stage-specific entries and optional direct-request routes.
2. Extend the existing installer fixture checks to prove the changed source
   packages/references/guide reach a committed disposable target.

- **AC-01:** Overview, examples, role table and package layout consistently show
  executable brief → separate verification → durable ready preflight → entry
  validation → mapped submission. Compact documentation packages follow it;
  small clear direct edits retain compact checks. No mandatory machine sidecar,
  digest ledger or controller stage appears.
- **AC-02:** Cross-stage guidance agrees on authority/coverage/revision ownership,
  feasible future tests versus absent capability, relevant known issues/context,
  material staleness versus expected effects and evidence handoff. No old optional
  wording authorizes skipping the packaged route. Do not change review-stage policy.
- **AC-03:** A real canonical install into a disposable committed Git fixture
  receives all four changed skill sources, their managed references and updated
  profile guide. Inspect installed bytes against source, not just file existence.
  Rerun refresh of that fixture still preserves unrelated skills/files and user
  AGENTS text outside the managed block. Do not refresh the active repository.
- **AC-04:** Inspect/synchronize `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
  `SHARED_SCRIPT_FILES`, focused tests and README installation guidance. No profile
  membership/runtime dependency change is invented. Record deterministic projection
  and source checks separately from unrun agent compliance/composition proof.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| I-01 / INV-002/003: one preparation route reaches installed callers | Four skills: designer, verification designer, preflight, implementer; their references and profile guide; packaged code/documentation versus direct edit | Installed/source byte comparison at canonical install filesystem boundary plus route consistency review | Targeted committed Git fixture install and source-contract checks | Inspect installed template/packet wording for a contradictory optional route | .4 implementer: targeted then installer suite; fresh reviewer: independent corroboration |
| I-02 / INV-009: distribution stays within managed ownership | Initial committed-target install → rerun after stale managed file; unrelated skill/file; user AGENTS text outside marked block | Actual installer filesystem outputs and before/after unmanaged bytes | Existing real installer preservation/rerun tests plus changed-source projection assertions | Add one unrelated file and verify targeted rerun leaves its bytes intact | .4 implementer: nearest installer suite; fresh reviewer: narrow independent probe |

## Verification

- Fail-first: extend focused installer/guide assertions so the old preparation
  contract fails for the intended reason. This proves projection and required
  wording; it cannot prove skill-call behavior.
- Targeted: preflight resolves the exact changed installer test selector; run it
  first with disposable committed Git setup and byte comparisons.
- Owning/aggregate local projection gate, owned by .4 implementer after targeted
  evidence is green:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`.
- Then run the changed preparation package suite once for composed local consistency:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py`.
  Both commands run from repository root. On correction, run focused regressions
  while red; run these owning gates only after relevant targeted evidence is clean.
- No whole-repository, network or agent/model-budget gate is authorized here.
  Actual role calls/revision recovery are `T-005` proof, needing separate
  authorization and actual preceding stage outputs. Report their unrun status.

## Expected contract impact

- Compose/preserve `ART-001/002/003/004`, `IF-001/002` and relevant T-001 invariants;
  change `ART-009` guidance/projection coverage. Preserve `INV-009` installer ownership.
- Dependencies: .1/.2/.3 source contracts, existing canonical installer and focused
  committed-target fixtures; no current `docs/contracts` registry entries.
- Durable delta: synchronized public/profile guidance and deterministic evidence
  that managed installation distributes it; no new check/refresh capability.

## Stops and handoff

Stop for incomplete predecessors, semantic contract disagreements, unsafe
permissions, user-work overlap, absent decisive installer capability or widened
scope. Return source defects to their owning child; preserve all prior work.
Budget is a soft checkpoint.
Next: separate verification design, standalone guided preflight, then bounded
implementation after .1/.2/.3. Required follow-on: immediately after implementation
or correction, hand completed bytes to a fresh independent acceptance reviewer,
preserving applicable prior conditional stages; end the implementer invocation.
Accepted local composition closes this parent's local source outcome. Continue
the official plan with `T-002`; leave semantic qualification to `T-005`.
