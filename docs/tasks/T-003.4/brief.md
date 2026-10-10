# Task Brief: `T-003.4` — Verify composed handoffs and installed source projection

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 12 tool calls / 30 minutes / 45k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 12. Duration: 30 minutes. Confidence: medium.
- Intended profile: `standard / high`. Policy result: fits; triggered limits:
  none; decomposition override: none. Implementation/local proof only;
  existing composition and installer patterns avoid a new harness.

## Readiness route

standalone guided preflight — confirm reviewed .1–.3 outputs and current test
ownership. Derived `verification.md`, then ready `preflight.md`, are required.

## Verification-design recommendation

separate — producer/consumer continuity across conditional stages, revised
readiness and mixed conditions needs integration closure beyond child-local text
checks. Existing fixture staging and disposable committed-target installer tests
are believed available. No new profile checker or role runner is authorized.

## Outcome and direction trace

Source/profile guidance and supplied integration inputs preserve the full T-003
route, with observed local fixture/installation evidence and explicit unrun
agent-call qualification gaps for T-005.

- Contribution: `CAP-002`, `FLOW-002/003`, all T-003 ART/IF/INV refs in the parent.
- Effect: callers discover one consistent route and installed packages contain
  its current contract/fixtures. Enables T-004 distribution and T-005 role proof.
- Why now: .1–.3 supply the protocol, complete conditional findings and recovery
  inputs that must compose before later qualification.
- Decisions: plan sections 1, 4–8, 10 T-003 and 11; parent P-01–07.
- New direction decisions required: None.

## Authority and scope

- Authority: [plan](../../project-plan.md), cited sections;
  `T-003` [task-map entry](../../task-map.json); [parent](../T-003/brief.md).
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Depends on completed/reviewed .1/.2/.3. Consumes
  `ART-001/002/003/004/005/006/007/009`; produces composed source ART-009 and
  reusable ART-004/005/006/007 fixture inputs, never observed agent reports.
- Allowed: stale route/usage entries in root README, `skills/README.md`, flow
  README; focused existing guide/composition/installer tests; new task-owned
  `docs/tasks/T-003.4/composition.json` and `results.md` for setup/evidence.
  Inspect installer `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
  `SHARED_SCRIPT_FILES`; synchronize only changes demanded by .1–.3 outputs.
  Minimal missing child-owned fixture wiring may be repaired here; broader
  production/policy defects return to the owning child.
- Read-only: old composition/results/reviews, plans/task-map/index, current
  `.agents/` copies. Reuse `tests/staging_fixture_support.py` without extending
  it into a framework or importing it from installed skills.
- Excluded: T-004 unborn/drift/check CLI, source fingerprint changes, wider
  installer ownership, new shared infrastructure, agent/model-budget evals,
  real known-issue writes or active installation refresh.

## Work and acceptance criteria

1. Reconcile affected overview routes with reviewed child contracts. Build a
   compact new composition record referencing child-owned cases rather than
   copying all their setup or rewriting T-002.4 history.
2. Exercise current fixture probes and package projection in disposable committed
   Git targets; preserve exact commands, state/oracles and qualification gaps.

- **AC-01:** Overview routes, source templates and installed guide agree on all
  four conditional combinations, first outstanding stage/full remainder and
  production correction re-entry. More than three confirmed maintainability
  findings reach the supplied correction input without loss or extra review scope.
- **AC-02:** Composed inputs retain stable findings/rows, sibling surfaces,
  incomplete reasons/owners, revision recovery with old-ready rejection and new
  focused readiness, and distinct changed-requirement routing. Preserve mixed
  correction/evidence/authority routes and actual-effect reference-only contrast.
  Stable deferral/optional improvement does not erase a real regression.
- **AC-03:** Failure → correction → clean discovery → acceptance inputs preserve
  current targeted evidence and the discovery-owned aggregate command/reason/
  owner/stage record. Late omitted coverage invalidates premature aggregate proof;
  acceptance does not duplicate execution. Existing task-specific stops survive.
- **AC-04:** The canonical installer projects each changed package, including
  task-local references/eval/setup files, plus guide/helpers, into a disposable
  committed target. Rerun preserves unmanaged files/text and removes stale managed
  bytes under existing ownership. Selection/helper declarations stay unchanged
  unless actual child output requires synchronization. No active refresh occurs.
- **AC-05:** Results distinguish contract structure, real fixture/filesystem/Git
  observations and unrun agent behavior. T-005 receives exact setup, package
  identities, intended producers/consumers and every unrun separate-call boundary.
  Constructed intermediate artifacts are labeled fixture data, never role outputs.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-003/004/005/006/008/011 | Parent P-01–06; initial failure → correction → fresh evidence → new decision; scenario revision versus authority change; four conditional combinations; four maintainability findings | Supplied producer output fields are compatible with downstream inputs; actual fixture probes exercise stated current bytes/oracles | Reuse child setup, inspect IDs/revisions/owners and probe real defects; reject dropped row/stale-ready/copied gate record | Trace one mixed-condition corrected submission with an unfinished sibling and revised readiness | .4 implementer: targeted local composition; fresh discovery: justified owning union; T-005: actual role calls |
| R-02 / ART-009 / IF-003 | All packages changed by .1–.3; package files/guide/helpers; first install → stale managed file + unmanaged sentinel → reinstall | Real committed-target bytes equal source projection, stale managed file disappears, unmanaged bytes/AGENTS text survive | Extend current installer projection test only for missing package-family evidence; do not duplicate existing families | Inspect installed maintainability setup and implementer correction template, then unmanaged sentinel | .4 implementer: targeted installer case and owning installer suite; no T-004 drift claim |

## Verification

- Targeted composition/installer changes first. Local owning commands from root:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py`
  and `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`.
  Extend existing cases only for distinct missing proof; preserve predecessor cases.
- Fresh discovery owns one justified composed union of affected modules after
  required targeted rows/probes are clean, under plan IF-004. Derived verification
  names the exact union using current child owners (guide, implementer,
  maintainability, discovery/acceptance/preflight only as affected). Acceptance
  consumes its record. Conditional gate owners retain their separate duties.
- No whole-repo, live-network or model-budget gate. Report every unrun stronger
  check and its owner; fixture execution cannot prove semantic role compliance.

## Expected contract impact

- Preserve/close `ART-004/005/006/007/009`, `IF-002/003/004/005/006`,
  `INV-003/004/005/006/008/011` and `FLOW-002/003` across child outputs.
- Dependencies: reviewed .1–.3 source contracts and existing canonical installer;
  no current `docs/contracts` registry. No new registry/foundation requirement.
- Delta: consistent discovery guidance, complete projected packages and reusable
  composition evidence for later qualification; no enforcement or runtime ledger.

## Stops and handoff

Stop for unresolved child contract mismatch, changed authority, user-work overlap,
unsafe permissions, scope expansion or missing decisive shared capability. Route
policy defects to the owning child; budget is soft.
Next: derived verification → ready standalone preflight → bounded implementation.
Required follow-on: immediately after implementation or correction, hand completed
bytes to a fresh independent acceptance reviewer through applicable conditional
stages, fresh discovery and separate acceptance; end the implementer invocation.
Reviewed .4 closes the parent only with all reviewed leaves; send exact setup and
unrun behavior gaps to T-005 without claiming behavioral qualification complete.
