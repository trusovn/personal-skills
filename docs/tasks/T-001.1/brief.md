# Task Brief: `T-001.1` — Bind packaged verification preparation to task authority

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 12 tool calls / 35 minutes / 45k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 12. Estimated implementation duration: 35 minutes.
- Confidence: medium. Intended profile: `standard / high`.
- Policy result: fits. Triggered limits: none. Decomposition override: none.
- Includes source, local fixtures/tests and implementation checks; excludes separate stages.

## Readiness route

standalone guided preflight — confirm the derived scenario coverage and source/profile
edit boundaries. The approved plan requires separate verification design and a
durable compact `preflight.md` for this executable package even if current facts
are routine; it does not require high-assurance instrumentation.

## Verification-design recommendation

separate — authority closure and revision semantics have plausible wrong routes.
Required by plan section 1 for executable packages; write this leaf's
`verification.md` before preflight. No preparation artifact is produced here.

## Outcome and direction trace

Package callers are directed to separate verification and preflight, with a
derived verification revision that covers every material AC without adding
requirements. This enables justified ready entry in `T-001.2`/`T-001.3` and
the installed workflow proof in `T-005`.

- Authority: [project-plan.md](../../project-plan.md), sections 1, 4–7, 10–11,
  and `T-001` in [task-map.json](../../task-map.json);
  parent [T-001](../T-001/brief.md), P-01/02/05/07/08.
- Contribution: `CAP-001`, `FLOW-001/003`, `IF-001`, `INV-001/002/003/005`.
- Why now: no prerequisites; downstream preflight consumes this contract.
- Direction decisions used: mandatory packaged stages, normative brief authority,
  compact direct edits and reasoned scenario revisions in plan sections 1 and 5–7.
- New direction decisions required: None.

## Authority and scope

- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: none. Consumes `ART-001`, baseline `ART-009`.
  Produces the source contract for `ART-002` and its part of `ART-009`.
- Allowed: `skills/task-implementation-flow/task-brief-designer/` and
  `task-verification-designer/` (under the same flow root), including their
  references, package tests and existing eval definitions/fixtures.
  Update only their stage-specific guidance in `skills/README.md`,
  `skills/task-implementation-flow/README.md` and root `README.md`.
- Inspect `scripts/install_development_skills.py`, including selection,
  `PROFILE_SKILLS_README` and `SHARED_SCRIPT_FILES`; no selection/helper change is
  expected. Necessary installer coverage goes to .4 unless a changed source
  dependency requires synchronization now; do not postpone a required dependency.
- Read-only: official plans/review, other stage sources and installed `.agents/`.
- Excluded: preflight/implementer changes, review redesign, new shared harness,
  controller contracts, behavioral eval execution and installation refresh.
- Unresolved decisions: none. Exact new targeted test names are UNKNOWN for preflight.

## Work and acceptance criteria

1. Replace optional packaged preparation routes in the two source skills and
   brief/template/layout references. Keep a direct-edit exception that cannot
   be used to bypass a supplied task package.
2. Make derived verification coverage, authority closure and revision recovery
   explicit; supply discriminating eval cases with real fixture inputs.

- **AC-01:** Executable package guidance requires `verification.md`, then ready
  `preflight.md`; composite/blocked work and direct legacy briefs route to their
  proper owner. Small clear conversational direct edits retain inline checks.
- **AC-02:** `verification.md` identifies its source brief and revision, maps every
  material AC to discriminating scenarios with setup/action/oracle, and preserves
  stable scenario IDs. Unsupported scenarios cannot add requirements; omitted ACs
  cannot be waived by green tests. Existing artifact conflicts remain protected.
- **AC-03:** A coverage gap under unchanged authority gets a reasoned revision
  retaining existing IDs, invalidates affected readiness/evidence and requests
  focused preflight. Changed requirements route to task design, not scenario editing.
- **AC-04:** Compact guided artifacts remain sufficient. Preserve sizing,
  decomposition, independent-review handoffs and package ownership. Affected guide
  entries match the changed source; do not require machine outputs or digests.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| D-01 / INV-001/002: authority and package identity control preparation | Executable leaf; composite; blocked design; legacy direct brief; small direct edit; compact documentation package | Source entry rules and supplied eval inputs distinguish all six routes; actual skill behavior belongs to T-005 | Source regression rejects old optional route; eval cases supply actual authority and package state | Inspect a documentation package for a hidden direct-edit bypass | Implementer: targeted/package suite; .4: projection gate |
| D-02 / INV-001/003/005: revision cannot alter requirements or hide gaps | Valid coverage; omitted AC; unjustified scenario; weak oracle; conflicting Source brief; initial ready revision → coverage-gap revision → renewed preflight; changed requirement | Derived artifact contract names authority/revision, stable IDs and next owner | Supplied brief/verification/readiness starting states and expected transitions; deterministic checks prove contract presence only | Trace an added AC scenario and verify old readiness cannot be reused | Implementer: targeted/package suite; T-005: separately authorized invocation proof |

## Verification

- Fail-first: add a focused source-contract regression rejecting the current
  optional packaged route and inadequate revision/coverage rules. It proves
  instruction coverage, not semantic agent compliance.
- Targeted: preflight resolves the new focused test command; exercise any new
  fixture setup in a disposable `EVAL_WORK_ROOT`, inspecting supplied inputs.
- Owning suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py`.
  Run from repository root after targeted checks pass.
- Broader local projection gate: owned once by .4 after all source leaves compose.
  No whole-repository suite is justified here.
- Agent/model-budget evals are unrun unless separately authorized. Extend existing
  skill-local fixtures, not a shared harness. Preserve that residual qualification
  gap explicitly for `T-005`; wording/schema tests do not close it.

## Expected contract impact

- Change `ART-001/002/009`, `IF-001`, `INV-001/002/003/005`; preserve `FLOW-001/003`
  and direct-edit scope. Materialize the binding source preparation contract.
- Current dependencies: existing source package/layout and skill-local eval
  fixtures; no current `docs/contracts` registry entries are available.
- Durable delta: separate mandatory packaged design with authority-bound revision
  and coverage ownership. This predicts implementation, not acceptance evidence.

## Stops and handoff

Stop on authority ambiguity, inseparable user-work overlap, unsafe permissions,
scope expansion or missing decisive capability. Do not implement a new helper
as a workaround. Treat the budget as a soft checkpoint; preserve user work.
Next: separate leaf verification design, standalone guided preflight, then bounded
implementation. Required follow-on: immediately after implementation or correction,
hand the completed bytes to a fresh independent acceptance reviewer, preserving
any applicable prior conditional stages. End the implementer invocation; no
same-session acceptance. Completed source contracts feed `T-001.2`.
