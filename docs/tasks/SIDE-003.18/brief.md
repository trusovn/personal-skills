# Task Brief: SIDE-003.18 — Validate distribution and publish SIDE-003 results

## Outcome

The restructured packages are proven installable and readable in disposable
targets: every reference recorded by the leaves resolves either in a fresh
disposable installer installation (profile packages) or in disposable
package copies (skill-creator, idea-brief, task-orchestrator), including
nested flow paths, and unmanaged sentinels survive the installer
installation. Aggregate source gates pass; the deliberately-unrefreshed
active installation's expected profile drift is reported separately and is
not counted against this work. `docs/tasks/SIDE-003/results.md` publishes the
measured savings per layer and per skill, gaps and failures, and the
live-qualification status honestly. No rollback machinery is built (owner,
2026-11-03 — Git history is the revert path).

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Delivery sequence" phase 5, "Measurement and decision rules", "Verification strategy" (rows "Missing installed reference", "Apparent savings only"), "Completion and rollback" (completion side only), "Verification strategy" closing command block; [parent brief](../SIDE-003/brief.md) |
| Dependencies | SIDE-003.1–.17 complete: `baseline.md` plus measurements and route inventories, `description-results.md` (groups 1–10), `rollout-results.md` (all restructuring and conditional-loading sections) |
| Allowed changes | `docs/tasks/SIDE-003/results.md`; disposable installer installations and disposable package copies under an approved temporary directory (prefer `/tmp/opencode`); registry updates through the designated `task-contract-registry-updater` stage with the explicit `--write-index` command, only if authority paths actually moved; nothing else |
| Read-only context | All prior leaves' results sections; `scripts/install_development_skills.py` (its profile selection is not modified); `tests/test_install_development_skills.py`; the three non-profile packages touched by the leaves: skill-creator (SIDE-003.13), idea-brief and task-orchestrator (SIDE-003.17); [docs/development.md](../../development.md) |
| Out of scope | Refreshing or repairing this repository's active `.agents/` installation or its expected drift (never — report separately); provider spending without separately approved budget; touching skill bytes (defects route back to the owning leaf); rollback units in results; changing the installer's profile or skill selection to cover non-profile packages |
| Assumptions / unresolved | Which references moved is fully enumerated by the leaves' results sections; live qualification status is `pending` unless a separately approved budget was used |

## Work and acceptance criteria

Required work:

1. Validate the changed packages in disposable targets, never the active
   installation: (a) install the 20-skill development profile into a
   disposable Git repository using the canonical installer, with the profile
   unchanged, and resolve there every reference recorded as moved, new, or
   conditional by the leaves for profile packages (SIDE-003.7–.12 and
   .14–.16, plus the profile members of .17), including nested flow paths;
   confirm unmanaged sentinels survive; (b) validate the three non-profile
   packages — skill-creator, idea-brief, task-orchestrator — through
   disposable package copies: copy each package to a disposable location and
   resolve its recorded references there.
2. Run the aggregate gates and classify the results: `python3
   tools/verify.py`, the architecture check, `python3
   tools/check_contracts.py --root .`, and `python3
   scripts/install_development_skills.py --check .`. The active installation
   is deliberately unrefreshed, so its expected profile drift (including the
   read-only drift check's outcome) is reported separately as expected: it
   neither blocks this work nor substitutes for validation — the fresh
   disposable targets are the validation surface. Every other failure is a
   real regression with an owning leaf. Synchronize the registry only for
   actual authority-path moves recorded by the leaves (.7, .10, .14, and
   .16 if needed).
3. Write `results.md` beside the plan: layer-1 catalog savings (description
   characters, all-26 and profile-20, before/after), layer-2
   loaded-instruction savings per skill and route (entry-only and
   cumulative, from the leaves' records and the SIDE-003.1 route
   inventories), the per-skill extraction/no-op decisions, gaps and anything
   that did not shrink, the separately-reported expected drift of the active
   installation, the session-use layer status (unknown without live budget),
   and the explicit record of what was not built (pilot experiment framing,
   rollback machinery) per the owner's adjustments.

- **AC-01:** In the disposable targets, every recorded reference resolves on
  its stated route — profile packages through the fresh disposable installer
  installation, and skill-creator, idea-brief, and task-orchestrator through
  disposable package copies; a deliberately broken link in a scratch copy is
  detected by the resolution walk or the relevant check (fail-first for the
  walk itself).
- **AC-02:** Aggregate source gates pass, with the deliberately-unrefreshed
  active installation's expected drift classified and reported separately;
  the fresh disposable validation is the installation proof. A real
  regression — a source gate failure beyond that expected drift, an
  unresolved reference, a damaged sentinel, or a suite failure — blocks
  completion; reporting it does not satisfy this criterion.
- **AC-03:** `results.md` reports both savings layers with the leaves'
  numbers, separates source accounting from rendered-catalog claims
  (unobservable locally — labeled), and marks live behavioral, routing, and
  session qualification pending unless a separately approved budget was used.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Remove or break one recorded reference link in a scratch disposable copy; the resolution walk (or the relevant check) detects it | the leaf's resolution walk over the scratch copy |
| Targeted | Installer suite with disposable-target fixtures (unmanaged sentinels, whole-package copying) for the profile tier; package-copy reference resolution for the non-profile tier | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` |
| Owning suite | Aggregate gates; the read-only drift outcome for the deliberately-unrefreshed active installation is classified as expected and reported separately, not as a failure of this work | `python3 tools/verify.py`; `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`; `python3 tools/check_contracts.py --root .`; `python3 scripts/install_development_skills.py --check .` |
| Broader gate | Live paired session comparison only with separately approved budget (plan "Apparent savings only" row); otherwise reported pending | approval-gated |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm all prior leaves' results sections exist, are current, and enumerate
their references before installing.
Verification-design recommendation: inline — the checks are enumerable from
the leaves' recorded references and the existing suites; no novel oracle
design.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 14 tool calls / 45 minutes / disposable install and package copies, gates, results
```

Sizing: `default@1`; estimate 13 implementation calls / 40 minutes;
confidence medium; fits.

Stops: a prior leaf's results missing or contradictory (route to that leaf's
owner); a broken reference in a disposable target (route to the owning leaf);
any need to refresh the active installation or to repair its expected drift
mid-session (never); missing live-eval budget (finish local work and report
live qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: this leaf performs the registry synchronization
that SIDE-003.7/.10/.14 recorded as needed and .16 recorded conditionally
(if any), via the designated `task-contract-registry-updater` stage with the
explicit `--write-index` command; otherwise none.