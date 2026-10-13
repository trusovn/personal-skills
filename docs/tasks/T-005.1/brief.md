# Task Brief: `T-005.1` — Supply reproducible qualification inputs

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 14 tool calls / 35 minutes / 45k context
```

## Outcome and direction trace

Supply a case inventory, reproducible disposable setup and current installed
projection receipts that later T-005 leaves can consume without inventing inputs.

- Direction contribution: `CAP-004`, `FLOW-004/005`, `IF-007/008`, `INV-009/010`.
- User-observable effect: no direct flow change; enables demonstrable installed
  preparation, decisions and correction handoffs in T-005.2–.5.
- Why now: T-001–004 and applicable INT-FLOW-001 contracts precede FLOW-005.
- Direction decisions used: plan sections 1–2, FLOW-005 and section 11.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), T-005 in sections 10–11;
  [parent brief](../T-005/brief.md), including its evidence rules and P-01/P-07.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: T-001–004 and applicable INT-FLOW-001 corrections. Preflight
  confirms completion/current contracts; absence of accepted dependencies
  blocks execution, not a new design decision.
- Consumes ART-001–011 setup/handoffs; produces task-local inputs to ART-012.
- Allowed: `docs/tasks/T-005.1/fixtures.md`, `results.md`, `evidence/`; only
  missing task-local composition setup in this package and focused checks in
  `tests/test_review_composition.py`. Reuse existing setup rather than copying it.
- Read-only: T-002.4/T-003.4 composition/results, INT-FLOW-001 results, T-004.3
  results; `tests/README.md`, existing fixture helpers and source eval packages;
  canonical installer declarations and installation READMEs.
- Excluded: source-policy/helper/installer repairs, active `.agents/` refresh,
  role/model evals, new reusable harness, old task history and master plans.
- UNKNOWN for preflight: current dependency acceptance and exact disposable
  paths. No unresolved product or architecture decision is delegated.

## Execution sizing

- Policy: `default@1`; estimated calls: 14; duration: 35 minutes; confidence: medium.
- Intended profile: `standard / medium`; policy result: `fits`.
- Triggered limits: none. Decomposition override: none.

## Readiness route

Standalone guided preflight after derived verification — confirm dependency
acceptance, current fixture selectors and installer ownership/permissions.

## Verification-design recommendation

Separate — inventory completeness, projection identity and supplied-versus-observed
evidence can otherwise yield false qualification. Write derived `verification.md`,
then obtain ready `preflight.md`, before implementation.

## Work and acceptance criteria

1. Build `fixtures.md` with setup command/environment, workspace, authority,
   expected oracle, inherited IDs, producer/consumer, owning leaf and evidence
   level for each claimed case. Enumerate the 24 inherited INV-CASE IDs and
   all COMP/CCR/composition records; retain public, lifecycle, tamper, validator,
   process-cleanup and continuation obligations by reference to their owners.
2. Identify current focused test owners after TEST-STAB-001 maintenance. Reuse
   existing staging and result inputs; add only missing composition setup.
3. Install into disposable Git targets and retain receipts. Reproduce canonical
   `--check`, independent full managed-byte comparison and target-local helper
   availability; keep workflow identity distinct from full projection identity.

- **AC-01:** Every parent requirement and inherited case has a setup/oracle,
  owner and existing evidence or explicit gap; no stale test selector or staged
  report is represented as a current role output.
- **AC-02:** A fresh disposable installation matches the canonical managed
  projection and uses sibling helpers. Receipts identify source/target and full
  comparison; the active installation and unmanaged repository bytes are unchanged.
- **AC-03:** The supplied local checks distinguish good/wrong fixture behavior
  at the existing real boundaries. No agent behavior or unrun check is claimed.
- **AC-04:** Later leaves can reproduce setup and identify how to replace staged
  producer placeholders with actual outputs while keeping evaluator oracles out
  of the consuming role's inputs. No runner or new policy is introduced.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| S-01 / INV-010 | COMP-01–05; INV-CASE-01–24; CCR-01–08; ROUTE/FIND/ROWS/REV/EFF/GATE/DISP records; applicable INT-FLOW inputs | Every inherited identity resolves to setup, oracle, owner and truthful evidence level | Targeted inventory/link audit and existing composition checks | Pick one inherited public-boundary case and one unrun handoff; reconstruct both from supplied setup | Implementer: targeted/owning; fresh discovery: justified changed-owner aggregate |
| S-02 / INV-009/010 | Selected skill packages incl. references/evals/setup; guide; shared scripts/config/schema; marked AGENTS block | Full source-to-target byte projection and matching read-only CLI check; active/unmanaged state unchanged | Canonical disposable install/check, independent comparison and snapshots | Change a copied eval/setup file: fingerprint may match while full check must report drift | Same owners; no role or whole-repo aggregate |

## Verification

Run changed/new inventory checks first; then
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py`.
Only when installation evidence needs renewal, run the owning
`test_install_development_skills.py` module, sequentially; do not duplicate all
T-004 journeys. Canonical commands: `python3 scripts/install_development_skills.py
<target>` then `python3 scripts/install_development_skills.py --check <target>`.
Use explicit disposable `EVAL_WORK_ROOT` with existing `setup_fixture.py
<scenario>` entry points. Preflight resolves selectors for any newly added check.
Reject a missing inventory mapping or wrong fixture control when feasible.
`git diff --check` and protected-file snapshots are structural/preservation
checks. Fresh discovery owns any justified aggregate of changed test owners;
acceptance consumes it. No live, model-budget or whole-repository check.

## Expected contract impact

None: preserve ART-009/010/011 and existing fixture contracts; provide task-local
inputs for ART-012. No `docs/contracts` registry or registry stage is created.

## Stops and handoff

Stop for unmet dependencies, authority conflict, inseparable user work, unsafe
permissions, missing decisive capability or production/shared-tooling expansion.
The budget is a soft checkpoint; preserve user work and incomplete evidence.
Next: verification design → standalone guided preflight → bounded implementation.
Immediately after implementation or correction and applicable conditional stages,
hand completed bytes to fresh independent `task-review-discovery`, then its report
to a separate `task-acceptance-review` decision. End the implementer invocation;
naming a route does not execute it. Reviewed outputs feed T-005.2/.3.
