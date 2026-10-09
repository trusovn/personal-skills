# Verification Design: T-001.4 — Close preparation guidance and installed profile projection

Source brief: docs/tasks/T-001.4/brief.md
Source revision: Git `700654acc294b1719f6a141f3b7c8243ee406e9a`, clean working tree at design entry
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

This is verification-design readiness, not implementation-entry readiness or
evidence that these scenarios passed. Normative sources are the brief,
`docs/project-plan.md` sections 1, 4, 10–11, the T-001 entry in
`docs/task-map.json`, and `docs/tasks/T-001/brief.md` P-01–08. Predecessor
contracts are read-only inputs; their completion and review status must be
confirmed by preflight.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | All cross-stage surfaces and the packaged-code, packaged-documentation and direct-edit routes. |
| AC-02 | V-02 | Compare guidance against predecessor contracts; no semantic role-call proof. |
| AC-03 | V-03, V-04 | Actual committed-target installation, byte projection and next refresh with unmanaged preservation. |
| AC-04 | V-05 | Installer selection, guide, shared dependencies, tests and installation instructions stay synchronized; evidence limits remain explicit. |
| I-01 / INV-002/003 | V-01, V-02, V-03 | Four skill sources, managed references and guide; source consistency plus installed bytes. |
| I-02 / INV-009 | V-03, V-04, V-05 | Initial install and stale-managed-file refresh stay within existing ownership. |

## Verification scenarios

### V-01 — Every cross-stage route uses the same preparation sequence

Covers: AC-01, I-01

Intent: Reject a correct overview paired with an example, role-table entry or
package layout that still permits skipping packaged preparation.

Given:
- The completed predecessor contracts define packaged preparation and the
  compact direct-request exception.
- The relevant overview, examples, role table and package layout in root
  `README.md`, `skills/README.md` and `skills/task-implementation-flow/README.md`
  are available for comparison.

When:
- Trace each documented route from task input to implementation submission.

Then:
- Executable packages consistently require brief → separate `verification.md`
  → durable ready `preflight.md` → implementation entry validation → mapped
  submission.
- Compact documentation packages use the same sequence. Small clear direct
  edits retain compact checks; a supplied package cannot use that exception.
- Existing stage-specific entries and legitimate optional direct-request routes
  remain intact. Old optional wording cannot authorize skipping packaged stages.
- No mandatory machine sidecar, digest ledger or controller stage is introduced.

Oracle / boundary:
- Compare the full relevant passages across all three source documents against
  the predecessor source contracts. Check obligations and exceptions in context,
  not only the presence of route keywords. Focused source assertions can support
  this review but cannot establish agent compliance.

Variants:
- Packaged code; compact packaged documentation; small clear unpackaged direct edit.

### V-02 — Guidance preserves stage ownership and material distinctions

Covers: AC-02, I-01

Intent: Reject shared terminology that hides contradictory ownership, blanket
readiness invalidation, or permission to drop evidence obligations.

Given:
- The four predecessor skill sources and their relevant references define task
  authority, derived coverage/revision, readiness and submission contracts.
- The cross-stage guidance from V-01 is available with the pre-change
  review-stage policy as a comparison baseline.

When:
- Compare guidance for each material distinction below with the owning source
  contract and follow its named next owner and evidence handoff.

Then:
- The brief and cited authority own requirements. Verification remains derived,
  covers every material AC and uses stable scenario IDs and decisive oracles;
  green tests do not waive omitted coverage.
- A reasoned coverage revision under unchanged authority preserves IDs,
  invalidates affected readiness/evidence and routes to focused preflight.
  Requirement changes return to task design.
- Preflight owns readiness; implementation validates entry and submits current
  per-scenario evidence, or an explicit blocked/unchecked reason and next owner,
  carrying the readiness/context reference and remaining obligations.
- Feasible task-owned future tests are distinct from unavailable indispensable
  capability; the latter blocks with an owned route.
- Relevant known issues and decision context pass through readiness. Unrelated
  issues and ordinary unknowns do not create routine stops or invented policy;
  the existing serious-delay/costly-later exception remains intact.
- Material authority, dependency, ownership, permission or capability changes
  require readiness reconsideration. Expected implementation/report effects
  alone do not force full rediscovery.
- Review-stage policy is unchanged.

Oracle / boundary:
- A source-contract comparison records consistency or the precise contradictory
  passage for each distinction. Inspect the instruction meaning and ownership,
  including relevant references; text-presence checks alone are insufficient.
  A predecessor semantic defect returns to its owning child, not an edit here.

Variants:
- Unchanged-authority coverage revision versus changed requirement.
- Feasible future test versus absent indispensable capability.
- Relevant, unrelated and absent recorded known issues; ordinary unknown versus
  unresolved serious-delay/costly-later uncertainty.
- Material fact change versus expected implementation/report effect.

### V-03 — Canonical installation projects current preparation bytes

Covers: AC-03, I-01, I-02

Intent: Reject source-only success, file-existence checks, or projection that
silently omits references or installs stale preparation instructions.

Given:
- A disposable Git repository has a real baseline commit and user AGENTS text
  outside the installer's marked block; its initial unmanaged bytes are recorded.
- The current four preparation packages and updated profile guide are available
  from the canonical source repository.

When:
- Run `scripts/install_development_skills.py` against that disposable target.
- Compare the installed managed preparation files with their source counterparts.

Then:
- Installation succeeds. All four changed skill sources, their managed references
  and the profile guide have matching source/installed file sets and bytes within
  the corresponding managed projection.
- The installed guidance carries the preparation contract checked in V-01/V-02;
  neither stale installed content nor omitted references can pass.
- User AGENTS text outside the managed block and unrelated target bytes remain
  unchanged. The active repository installation is not refreshed.

Oracle / boundary:
- Observe the actual canonical installer result and resulting disposable-target
  filesystem. Compare bytes for `task-brief-designer`,
  `task-verification-designer`, `task-preflight`, `bounded-task-implementer`,
  their managed references and installed profile guide using canonical mappings.
  Before/after unmanaged bytes establish preservation. Installer success or
  availability alone cannot substitute for these comparisons.

Variants:
- All four skill packages, each package's managed references, and the profile guide.

### V-04 — The next refresh repairs managed state and preserves unmanaged bytes

Covers: AC-03, I-02

Intent: Reject a refresh that retains stale managed files or succeeds by replacing
the whole installation and losing user-owned content.

Given:
- The initial committed-target installation in V-03 succeeded.
- A stale file is added within a profile-managed skill directory and the installed
  guide is made stale.
- An unrelated skill, an unrelated file outside managed ownership and user AGENTS
  text outside the marked block have recorded bytes before refresh.

When:
- Rerun the canonical installer against the same disposable committed target.

Then:
- Refresh succeeds, removes the stale managed file and restores the guide.
- The four preparation packages and their references still match current source
  projection by file set and bytes.
- The unrelated skill and file retain their exact bytes; user AGENTS text outside
  the block remains exact. The marked block is not duplicated.
- The active repository installation is not refreshed.

Oracle / boundary:
- Observe the second real installer invocation and filesystem outputs; compare
  managed outputs with source and unmanaged outputs with their pre-refresh bytes.
  Existence of the unrelated skill alone does not prove its preservation.

Variants:
- Stale managed file and guide; unrelated skill and file; user AGENTS text outside
  the managed block.

### V-05 — Distribution synchronization and proof claims stay within scope

Covers: AC-04, I-02

Intent: Reject unnecessary profile expansion, installation instructions that
disagree with the canonical installer, or claims that local checks qualify skill
behavior.

Given:
- The pre-change canonical installer selection, guide mapping, shared-file list,
  focused tests and README installation guidance are available as a baseline.
- Current guidance changes and deterministic source/installation evidence are
  available for the implementation handoff.

When:
- Inspect `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
  `SHARED_SCRIPT_FILES`, focused installer tests and README installation guidance
  together, and review the reported evidence and limits.

Then:
- The existing profile selection, guide mapping and shared runtime dependencies
  support the changed sources without invented membership or dependency changes.
  Any necessary synchronization stays within the brief's minimal installer scope.
- Focused checks cover the changed route and real projection. Installation
  instructions agree with the canonical installer and its narrow ownership.
- Evidence separates source-contract checks from actual filesystem projection.
  It identifies semantic agent compliance and multi-call composition as unrun
  T-005 qualification, rather than declaring the installed workflow qualified.

Oracle / boundary:
- Inspect the scoped diff and linked deterministic results against the canonical
  constants and task boundary. Require actual fixture setup and observed outputs
  for claimed installation success; source wording/schema checks cannot supply
  that evidence or prove role-call behavior.

Variants:
- Source-contract evidence; real install/refresh evidence; unrun semantic and
  multi-call qualification.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Scenario IDs identify obligations, not prescribed test names.
- Implement the smallest changes that satisfy the brief and exercise these
  scenarios. Concrete test structure, helpers and placement remain implementation
  choices unless already fixed by repository authority.
- Preflight must confirm reviewed predecessor completion and resolve the exact
  targeted installer selector and safe committed-fixture setup. Begin with a
  focused fail-first check that rejects the old contract for the intended reason.
- After targeted evidence is green, the .4 implementer owns the installer suite,
  then the changed preparation package suite, using the commands in the brief.
  No implementation suites or agent evals were run during this design pass.
- This design observes this task's own guidance and distribution boundary only;
  it does not add sibling role-call or parent-level qualification scenarios.
- If a scenario cannot be exercised at its stated boundary, route the conflict
  to task design/preflight rather than silently weakening its oracle.
