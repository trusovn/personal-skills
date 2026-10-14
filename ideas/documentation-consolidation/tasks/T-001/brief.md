# Task Brief: `T-001` — Audit preservation and retirement eligibility

Status: `ready`  
Task kind: `executable`  
Profile: `guided`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 25 tool calls / 60 minutes / 80k context
```

## Outcome

Produce one evidence-backed audit manifest that identifies the exact preservation
set, retirement eligibility, live consumers, pending obligations and owner gates
for the documentation cleanup, without changing the audited repository inputs.
An audit with explicit blockers is a valid result; it does not authorize cleanup.

## Direction trace

- Direction contribution: establish safe scope for freeing completed delivery
  paths while preserving originals, active work and executable dependencies.
- User-observable effect: the owner can inspect what may be retired and what
  still needs a decision. Enables T-002 to preserve the intended original
  repository context before T-003 migration and T-004 retirement.
- Why now: cleanup-v1 places this audit before every archive or cleanup task.
- Direction decisions used: [owner-approved brief](../../../documentation-consolidation.brief.md),
  “Desired Outcomes,” “Scope Sketch,” “Boundary Notes” and “Open Questions”;
  [cleanup plan](../../project-plan.md), §§1–2, 8 FLOW-001, 10–12.
- New direction decisions required: None. Discover and record execution choices;
  do not make unresolved owner decisions on the owner's behalf.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | User request: design task 1 as one task, with task documents under `ideas/documentation-consolidation/tasks/`; cleanup-v1 plan §§4, 8, 10–12 and its [task map](../../task-map.json), `T-001`. The separate [plan review](../../project-plan-review.md) accepts the gated plan, not current retirement eligibility. |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills`; follow root `AGENTS.md` and active project-local skill resolution. |
| Dependencies | No predecessor task. Consume existing ART-001 originals/context and ART-005 active backlog/navigation. |
| Allowed changes | Audit output only: `ideas/documentation-consolidation/tasks/T-001/results.md`, containing ART-002 as one document. Required preparation and later review artifacts also stay in this task directory. |
| Read-only context | `docs/tasks/`, old `docs/project-plan.md`, old `docs/task-map.json`, `docs/project-plan-review.md`, `docs/future-work/`, existing navigation, and discovered consumer source/tests/fixtures/installer declarations. Read only the evidence and dependency closure needed for the audit. |
| Out of scope | Archive commits/tags, fetch/push or publication, staging files, deletion, dependency migration, navigation/backlog edits, rewriting reports/verdicts, closing qualification gaps, skill/tooling changes, installation refresh, history rewriting and running live-model evals. Do not edit either old or cleanup planning documents. |
| Known unknowns | Exact preservation membership, current completion evidence, full consumer closure, relevant ignored assets and owner choices Q-001–Q-003 are audit subjects, not assumptions of completion. |

The retirement candidate boundary is completed material within `docs/tasks/`,
plus the old `docs/project-plan.md` and `docs/task-map.json`. Preserve
`docs/future-work/` including `stale/`, the old plan review and unrelated docs.
Confirm that the owner's “future-tasks” means `docs/future-work/`; record any
contradiction for the owner. Preservation may include relevant assets outside
retirement candidates, including the currently untracked planning package;
preservation membership never implies deletion permission.

## Work and acceptance criteria

Create `results.md` with the following evidence, commands, observations and
limits. Use compact tables rather than copying historical reports.

- **AC-01 — Reproducible preservation scope.** Record HEAD and scoped Git state;
  enumerate each candidate and other relevant preservation asset with exact
  path, byte identity/hash, file type/mode, tracked/index/worktree state and
  proposed inclusion or exclusion with reason. Distinguish index and worktree
  versions when they differ. Record relevant untracked/ignored inputs explicitly;
  do not indiscriminately collect unrelated files or secret contents. Identify
  any LFS, submodule or external-content boundary that ordinary Git objects
  cannot preserve alone. Inaccessible/unresolved assets block affected scope.
- **AC-02 — Evidence-backed eligibility and obligations.** For every candidate,
  cite actual completion, review/result and qualification evidence, or mark it
  unknown. Record pending obligations with original evidence, proposed retained
  active context/next owner and confirmed disposition or unresolved owner gate.
  A task index, commit label, future catalog or passing structural check alone
  cannot establish completion. Preserve historical verdicts and unrun limits.
- **AC-03 — Consumer and verification map.** Trace live readers and relevant
  reference carriers of candidate paths, including transitive fixture/setup
  inputs. Distinguish executable dependencies, active navigation and historical
  mentions. Record source locations, necessary input closure, existing owner,
  decisive scenarios/oracles and the narrow existing verification selectors for
  T-003. Inspect existing coverage/helpers before proposing retained inputs;
  identify installer coupling if managed inputs would change. Do not migrate
  assets or claim behavioral equivalence from this audit.
- **AC-04 — Explicit owner gates and handoff.** Reconcile Q-001 inclusion,
  Q-002 unused tag/destination/publication authorization/navigation location,
  and Q-003 completion/pending-work dispositions. Record supplied owner decisions
  with their source; otherwise identify the question, owner and affected later
  task. Give per-candidate eligibility and an overall `ELIGIBLE` or `BLOCKED`
  assessment. Unresolved global preservation/archive choices block archive
  advancement; unresolved candidate dispositions block affected retirement.
  Even an eligible assessment is not archive execution or deletion permission.
- **AC-05 — Read-only and current.** Audited inputs, Git index, refs outside the
  run-evidence namespace and existing user work remain unchanged. Standard
  run-evidence instrumentation is required; its metadata, snapshot objects and
  refs under `refs/personal-skills/run-evidence/` are authorized task artifacts,
  not audit failures. Record their changes separately from protected state.
  Record initial/final scoped identities and any
  drift. Drift invalidates affected facts until re-inspected; never resolve it
  by restoring or overwriting user files. Attribute the new audit output and
  keep all preparation/review files distinct from original preservation inputs.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-001, INV-006: intended originals have explicit identity and inclusion | Tracked unchanged, staged, unstaged, untracked and relevant ignored assets; index/worktree divergence; ordinary files versus any discovered external-content boundary | ART-002 reconciles actual Git/index/filesystem inventory with exact scoped paths, versions and modes; unresolved inclusion is blocked | Enumerate real inputs using Git and filesystem reads; compare inventory to manifest and explain each exclusion | Independently rebuild scoped inventory and compare membership; inspect divergent or nontracked inputs when present, otherwise verify their recorded absence | Audit implementer before submission; fresh discovery reviewer corroborates current output |
| R-02 / INV-004, INV-006: eligibility does not hide unfinished work | Candidate families: `docs/tasks/`, old project plan, old task map; completed, unfinished and unknown dispositions where present; retained future-work including `stale/` and old plan review | Every candidate maps to source evidence/disposition; unresolved cases remain blockers, retained families stay outside deletion scope | Reconcile candidate rows against reports and backlog; list Q-001–Q-003 decisions or gates | Challenge a completion inference against its original evidence and follow pending-work references; verify unknowns cannot appear eligible | Audit implementer; fresh discovery reviewer owns final aggregate reconciliation after corrections |
| R-03 / INV-003: live input dependencies are visible | Executable reads, fixture/setup closure, active navigation and historical-only references | Each discovered live consumer has its full necessary input mapping and existing evidence owner/selector; historical mentions alone do not require migration | Search path carriers and inspect actual reader/setup code and existing tests; trace known composition consumers to their input closure | Trace a real reader through fixture/setup inputs independently and compare with ART-002; inspect reference-search coverage | Audit implementer before submission; fresh discovery reviewer corroborates closure |
| R-04 / INV-006: discovery cannot change originals or advance on stale facts | Audit start -> output write -> final identity check; stable inputs versus observed drift | Before/after content, scoped status, index and refs outside the run-evidence namespace agree; task output and authorized run-evidence artifacts are attributed separately; changed protected inputs invalidate affected assessment | Capture and compare identities; report drift/blockers rather than modifying inputs | Compare final scoped identities and change set with the recorded baseline; check any drift disposition | Audit implementer at submission/correction; fresh discovery reviewer checks final bytes |

## Verification

Verification-design recommendation: `separate` — inventory completeness across
Git states, evidence-based eligibility and transitive consumer closure allow
plausible incomplete audits that still look successful. Derive
`verification.md` with `task-verification-designer`, then obtain a ready
`preflight.md` with `task-preflight` before implementation. These are later
preparation stages, not subtasks or extra outputs of this brief-design request.

Readiness route: `standalone guided preflight` — confirm current inputs,
read-only command scope and audit output ownership after derived verification.
The decisive oracle uses existing Git/filesystem/source inspection; no new
verification harness or feasibility prerequisite is needed.

| Evidence | Scenario and oracle | Command / owner |
|---|---|---|
| Targeted inventory | Real candidate tree and relevant preservation inputs match manifest membership, identities, modes and Git states; omissions cannot be reported as complete | Implementer resolves scoped commands during preparation; existing entry points include `git rev-parse HEAD`, `git status --porcelain=v1 --untracked-files=all`, `git ls-files --stage`, `git diff --raw`, `git diff --cached --raw`, and scoped `git ls-files --others --ignored --exclude-standard -- <paths>`. Use filesystem hashing and account for deletion/type/symlink cases. |
| Targeted evidence/consumer reconciliation | Original reports contradict unsupported completion claims; each live reader's required inputs appear in the consumer map | Scoped `rg -n` searches plus source/report reads; record actual search roots, patterns and traced closure. Known starting points: `tests/test_review_composition.py`, `tests/review_fixture_support.py`, `tests/staging_fixture_support.py` and `tests/README.md`. |
| Negative / unchanged state | Unknown inclusion, unfinished work, absent owner choices or protected-state drift yield explicit blockers; existing inputs/index/refs outside the run-evidence namespace remain unchanged | Check actual cases against the manifest; compare initial/final identities and attribute authorized run-evidence changes separately. No destructive fault injection or new test harness. |
| Owning suite selection | Document the existing consumer suite and further selectors discovered by the audit; a passing suite would not prove eligibility | Known T-003 baseline selector: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py`. T-001 selects commands; it need not run consumer suites merely to produce the audit. |
| Broader gate | Full manifest, obligation and consumer reconciliation against current repository facts | Fresh independent discovery reviewer after implementation/correction. No broad test suite, network recovery or live-model run belongs to this audit. |

Fail-first regression: N/A; this task creates an audit record, not executable
behavior. Verification must reject unsupported/missing rows through source
reconciliation. A schema, path search or syntax check alone is insufficient.
No archive recovery, migration equivalence or agent compliance is proved here.

Owner clarification, 2026-10-14: run-evidence is the standard required workflow.
Its authorized instrumentation effects alone are not a failure of AC-05.
Historical reports retain their original findings; renewed review uses this
clarified boundary. The prior preflight bindings require a focused refresh.

## Expected contract impact

- Cleanup-v1 refs: materialize ART-002 and IF-001 for CAP-001,
  FLOW-001-S01/S02; preserve INV-001/003/004/006. IDs are scoped to
  `ideas/documentation-consolidation/task-map.json`, not the old task map.
- T-002 consumes preservation scope and owner gates; T-003 consumes consumer
  closure/verification selection; T-004/T-005 consume eligibility, pending-work
  and identity facts. Each must revalidate affected facts on drift.
- Current contract dependencies: existing ART-001/005 and repository sources;
  no `docs/contracts/` registry is present at brief design. No reusable software
  contract or registry infrastructure is introduced by this audit.

## Execution sizing

- Sizing policy: project-local `references/task-sizing.yaml`, `default@1`.
- Estimated agent calls: **22**; implementation duration: **55 minutes**.
- Estimate confidence: **medium**; consumer closure and evidence volume remain
  audit subjects. Intended launch pair: **standard / medium**.
- Policy result: `override_cannot_split_safely`.
- Triggered limits: `max_agent_calls` (22 > 15) and
  `max_duration_minutes` (55 > 40); no execution-profile trigger.
- `decomposition_override: cannot_split_safely`. Considered separating file
  inventory, completion/disposition and consumer discovery. They all reconcile
  the same preservation set at one repository state: consumer findings change
  inclusion, and pending obligations change eligibility. Separate ownership
  would force repeated scans and renegotiation of the same manifest before it
  could serve T-002. Keep one audit and one owned output, consistent with the
  user's no-subtasks instruction and the policy's permitted override.
- Residual risk: unexpected consumer breadth may exceed the estimate. At the
  repository's 25–35-call or 80–100k-context checkpoint, preserve a truthful
  partial result and structured continuation; never label unchecked scope
  complete. Estimates exclude separate preparation and review stages.

## Stops and handoff

- Ask the owner for unresolved inclusion/disposition/archive choices when facts
  are ready. Continue independent read-only audit work; leave dependent later
  work blocked until an actual answer is recorded. Silence is not approval.
- Stop affected assessment for inaccessible decisive evidence, conflicting
  authority or concurrent drift. Report substantial migration/redesign needs
  for later task planning; do not implement around them.
- Preserve existing user work and both plan packages. Do not refresh `.agents/`.
  New shared tooling, changed behavior or permission expansion needs new scope.
- Next: derive task-local `verification.md`, obtain ready `preflight.md`, then
  implement this audit with `bounded-task-implementer`, writing only its owned
  `results.md`. No child tasks or structural task index are needed.
- Required follow-on: immediately after implementation or correction and any
  applicable conditional stages, hand the completed bytes to a **fresh
  independent `task-review-discovery` call**, then hand its report to a
  **separate `task-acceptance-review` decision**. Same-session self-review is
  insufficient. No maintainability or registry stage is expected for an
  evidence-only output; reassess if the authorized scope changes.
- Audit acceptance confirms evidence quality, not archive recovery, historical
  qualification or permission to delete. T-002 starts only after its own gates.
