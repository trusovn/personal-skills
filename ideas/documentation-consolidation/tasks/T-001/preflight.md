# Task Preflight: `T-001` — Audit preservation and retirement eligibility

Status: `ready`

Focused refresh for verification revision 2 (owner run-evidence clarification) and
brief `94cc2e18…`. Supersedes the revision-1 binding previously recorded here
(prior preflight SHA-256 `9d79cb44aa6d152536563a42928869a781bedd238277cabe48fd09615310612d`).
Unchanged facts are reused from that binding; only revised obligations and
current applicability were re-examined.

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | `ideas/documentation-consolidation/tasks/T-001/brief.md`, `Status: ready`, `Task kind: executable`, `Profile: guided`. Authority: owner request + owner-approved [direction brief](../../documentation-consolidation.brief.md), cleanup-v1 [plan](../../project-plan.md) §§1–2, 4, 8 FLOW-001, 10–12, [task map](../../task-map.json) `T-001`, plus the owner's 2026-10-14 run-evidence clarification now in the brief (§AC-05, §Verification note) and verification revision 2. [Plan review](../../project-plan-review.md) accepts planning, not current eligibility. |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills`; root `AGENTS.md` followed; no matching project-local `.agents/skills/` copy of this skill, so user-global `task-preflight` is active. |
| Dependencies / entry criteria | No predecessor task. Consumed roots exist and are readable: `docs/tasks/` (182 tracked candidates), old `docs/project-plan.md`, `docs/task-map.json`, `docs/project-plan-review.md`, `docs/future-work/` (15 tracked files incl. `stale/`). Tools present: `git` 2.53.0, `rg`, `sha256sum`, `python3`. No `docs/contracts/` registry; no known-issues file in scope. |
| Allowed scope | Write only `ideas/documentation-consolidation/tasks/T-001/results.md` (plus `preflight.md` and later review artifacts in this task directory). Audited inputs are read-only. |
| User-work ownership | Separable, no conflict. Unstaged preparation edits: `brief.md`, `verification.md` (preparation/owner workflow). Untracked task-owned existing work to preserve: `results.md` (SHA-256 `798906e8…`) and `reviews/discovery-0{1,2,3}.md`. `preflight.md` is tracked and currently holds revision-1 bytes. |
| Permission limits | No network, destructive, privileged or staged actions; no commit/push; no `.agents/` refresh; no edits to either plan document. Run-evidence instrumentation (metadata, snapshot objects, begin/recovery/finish refs under `refs/personal-skills/run-evidence/`) is the standard required workflow and is authorized; all other refs, the index and files remain protected. |
| Profile | `guided` |
| Standalone preflight value | `material` — exact uncertainties resolved: (1) the revision-2 run-evidence namespace boundary is real and mechanically distinguishable from protected refs; (2) current HEAD/ownership after repository advancement and preparation edits; (3) rebinding readiness from the stale revision-1 binding. See Decision context. |
| Source brief / revision | `ideas/documentation-consolidation/tasks/T-001/brief.md` — SHA-256 `94cc2e185f1aef939a17d23db629cfef90bd33d6aca7727ad3de1ddaf65a2ebf` (current working-tree bytes). |
| Verification / Verification revision | `ideas/documentation-consolidation/tasks/T-001/verification.md`, revision **2** — SHA-256 `962a9b138d3491eff9ee4d6a372226af8cdbc9f7062d389308c1d8f699d616b1`. `Source brief:` resolves to this package brief and its recorded digest matches current bytes. Scenario IDs V-01–V-06 unchanged; V-05/V-06 revised for the run-evidence namespace. |
| Current applicability | `HEAD` = `b65f900e7515ccfe36335b793b0c058b7b2bfa8c` (advanced from the revision-1 binding's `32edda26…`). Status: two unstaged preparation paths (`brief.md`, `verification.md`) and untracked `results.md` + three `reviews/` reports + four `.DS_Store`. No staged changes; raw index hash `bab2e328…`. The existing `results.md` was authored under revision 1 and its AC-05/overall disposition is stale under revision 2 (see Warnings). No owner answer to Q-002 is recorded; Q-001/Q-003 decisions are supplied (results.md §Authority). No external drift beyond the recorded preparation revision. |

## Decision context

- Intended use: T-001 produces ART-002 (one evidence-backed audit manifest) consumed by T-002 (preservation), T-003 (consumer/verification map) and T-004/T-005 (eligibility, pending work, identity). A blocked audit is a valid result. This refresh authorizes the bounded **correction** of the existing `results.md` under revision 2, not archive execution.
- Failure consequences: a manifest missing untracked/ignored inputs, misclassifying unfinished work as eligible, or mis-attributing authorized instrumentation would later permit archive/retirement on wrong facts (INV-001/003/004/006). Drift invalidates affected facts and is never repaired by editing originals.
- Priorities: record actual evidence; a task index, commit label, future catalog or passing structural check cannot establish completion. Historical verdicts and unrun limits keep their meaning.
- Revised obligation (the focused delta): AC-05 / R-04 / V-05 / V-06 now require protected state (`files`, `index`, and refs **outside** `refs/personal-skills/run-evidence/`) to remain unchanged, while authorized run-evidence instrumentation is recorded **separately** and is not an AC-05 failure.
  - Verified current fact: the namespace is live and distinct — `git for-each-ref refs/personal-skills/run-evidence/` = 92 refs; protected refs outside it = 19 `refs/heads/*`, 18 `refs/remotes/*`, 1 `refs/stash`, and 2 unrelated `refs/codex/turn-diffs/*` (total 40). `git for-each-ref --exclude='refs/personal-skills/run-evidence/**'` is supported by git 2.53.0 and returns exactly those 40 protected refs.
  - Repo workflow confirms this is canonical: `scripts/run_evidence.py` / `scripts/run-evidence.md` / `README.md` define the namespace.
- Reused unchanged facts (re-verified cheaply, still true): 182 tracked candidates all mode `100644`; no `.gitattributes`, no `.gitmodules`, `git-lfs` absent → no symlink/submodule/LFS external-content boundary among tracked candidates; 15 `docs/future-work/` files retained; four `.DS_Store` untracked (one inside `docs/tasks/T-005.3/`) are excluded with reason; whole `ideas/` package is a relevant untracked preservation input.
- Owner gates: Q-001 (exact inclusion) and Q-003 (completion/pending-work dispositions) have supplied owner decisions recorded in `results.md` §Authority; Q-002 (tag/destination/publication/navigation) is a recommendation only and remains an open downstream gate. Archive advancement stays blocked until Q-002 is decided; silence is not approval.
- Assumptions: ordinary unknown candidate dispositions become recorded unknowns or blockers, not silent eligibility. No routine user questions needed; Q-002 is asked only when facts are ready, per brief §Stops.

## Acceptance evidence and commands

| AC / scenario / risk | Authority relationship | Setup / decisive boundary / oracle | Exact command / cwd | Feasibility: dependencies / permissions / ownership | Baseline result / gap |
|---|---|---|---|---|---|
| AC-01 / V-01 / R-01 (INV-001, INV-006) | Brief AC-01; verification V-01 | Reconcile real Git/index/filesystem inventory with manifest membership, identities, modes, Git states; unresolved inclusion blocks affected scope | `git rev-parse HEAD`; `git status --porcelain=v1 --untracked-files=all`; `git ls-files --stage -- <paths>`; `git diff --raw -- <paths>`; `git diff --cached --raw -- <paths>`; `git ls-files --others --ignored --exclude-standard -- <paths>`; `sha256sum <untracked path>` — cwd repo root | Feasible; read-only. External-boundary absence re-verified (182×`100644`, no `.gitattributes`/`.gitmodules`/`git-lfs`) | Not run — the inventory is the task output. **Correction gap (F-02):** existing `results.md` records stale worktree identities for the two changed included preparation paths (`brief.md`, `verification.md`); correct against current bytes. |
| AC-02 / V-02 / R-02 (INV-004, INV-006) | Brief AC-02; verification V-02 | Every candidate maps to original completion/review/qualification evidence or explicit unknown; pending obligations carry evidence, retained context/next owner, disposition or owner gate | Scoped `rg -n` reads of `docs/tasks/**`, old `docs/project-plan.md`, `docs/task-map.json`, `docs/project-plan-review.md`, `docs/future-work/**` | Feasible; reuses prior evidence (V-02 pass) | Reuse — prior binding's V-02 reconciliation stands; Q-003 dispositions recorded. No revision-2 change. |
| AC-03 / V-03 / R-03 (INV-003) | Brief AC-03; verification V-03 | Live readers traced through fixture/setup/input closure; executable deps vs active navigation vs historical mentions distinguished; owners/scenarios/oracles/selectors recorded | Scoped `rg -n` from `tests/test_review_composition.py`, `tests/review_fixture_support.py`, `tests/staging_fixture_support.py`, `tests/README.md`, `docs/tasks/T-005.1/setup_consumer.py`; follow to transitive inputs | Feasible; reuses prior evidence (V-03 pass) | Reuse — consumer closure unchanged. T-003 baseline selector `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` is recorded, not run by T-001. |
| AC-04 / V-02, V-04 / R-02 | Brief AC-04; verification V-04 | Q-001/Q-002/Q-003 each get a sourced decision or a stated question, owner, affected later task; per-candidate + overall `ELIGIBLE`/`BLOCKED` | Read plan §12 and supplied owner decisions in `results.md` §Authority | Feasible; reuses prior evidence (V-04 pass) | Reuse — Q-001/Q-003 supplied, all candidates gated, overall `BLOCKED`. Q-002 recommended only; remains an open owner gate. |
| AC-05 / V-05 / R-04 (INV-006) — **revised** | Brief AC-05 + 2026-10-14 clarification; verification V-05 rev 2 | Protected files/index/refs-outside-namespace unchanged; run-evidence metadata, snapshot objects and begin/recovery/finish refs under `refs/personal-skills/run-evidence/` attributed separately and not an AC-05 failure | `git for-each-ref --format='%(refname) %(objectname)' --exclude='refs/personal-skills/run-evidence/**'` (protected refs); `git for-each-ref --format='%(refname) %(objectname)' refs/personal-skills/run-evidence/` (authorized instrumentation); compare scoped `sha256sum` + `git status` before/after — cwd repo root | Feasible: git 2.53 supports `--exclude`; 40 protected refs vs 92 namespaced refs verified distinct; read-only | Not run — before/after capture is implementation step 1/step N. **Correction gap (F-03):** existing `results.md` declares `NON-COMPLETE` because a namespaced finish ref was written; under revision 2 that instrumentation is authorized, so the AC-05 disposition and handoff must be restated. |
| AC-05 / V-06 / R-04 (INV-006) — **revised** | Brief AC-05 + clarification; verification V-06 rev 2 | Observed drift invalidates affected facts until reinspection; user files never restored/overwritten; changed preparation bytes are protected files | Compare initial/final scoped identities; re-hash changed included inputs and reinspect affected rows, or mark blocked | Feasible; no fault injection required. Current fact: `brief.md`/`verification.md` worktree bytes changed while their index blobs remain old | **Active applicability:** existing `results.md` relies on pre-change identities for those two included paths; affected rows/statements are invalid until reinspected under current bytes (V-06). |

Every scenario V-01–V-06 and risk row R-01–R-04 is covered; no row is dropped or blocked. The decisive oracle is existing Git/filesystem/source inspection; no new harness, live-model eval, network or destructive check belongs to this task.

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| Existing `results.md` (SHA-256 `798906e8…`) authored under revision 1 | Its AC-05 disposition (`NON-COMPLETE` on a namespaced ref) and its stale identities for `brief.md`/`verification.md` do not satisfy revision 2 | T-001 implementer (bounded correction) | Rewrite only within authorized scope: reconcile the current inventory identities (F-02) and restate AC-05/overall per the revision-2 ref rule (F-03); do not touch audited inputs |
| Q-002 (tag/destination/publication/navigation) has only a recommendation | Archive advancement stays gated; overall `BLOCKED` may remain a truthful result | Owner; T-002 downstream | Keep Q-002 as an explicit open owner gate; record supplied decisions with source; silence is not approval |
| `preflight.md` is tracked; writing it makes it the single ` M` packet delta | Non-blocking; expected and attributed | Preflight | Record the attributed delta; preserve all other untracked task work and preparation edits |
| `.DS_Store` untracked (one inside candidate tree `docs/tasks/T-005.3/`) | Must be explicitly excluded with reason | Implementer records | List exclusions with reason (AC-01) |
| Budget: 25 tool calls / 60 min / 80k context (brief) | Soft checkpoint | Implementer | Preserve a truthful partial result and structured continuation; never label unchecked scope complete |

Implementation stops: edit nothing outside the T-001 task directory; never modify audited inputs, the index, or refs outside `refs/personal-skills/run-evidence/`; never edit user work; do not run consumer suites as eligibility evidence; do not refresh `.agents/`; stop affected assessment on inaccessible decisive evidence, conflicting authority, or concurrent drift.

**Next action:** correct `ideas/documentation-consolidation/tasks/T-001/results.md` with `bounded-task-implementer` under this revision-2 binding (F-02 identity refresh and F-03 run-evidence disposition). Then take the corrected bytes through a fresh independent `task-review-discovery` pass followed by a separate `task-acceptance-review` decision (`review: immediate`). No maintainability or registry stage is expected for this evidence-only output.

## Implementer handoff

```text
Correct (do not re-run from scratch): ideas/documentation-consolidation/tasks/T-001/results.md
  existing SHA-256 798906e82414c4c25f16e994a508e63e4eef2806c067ea6953b02347b23407ee
Brief: ideas/documentation-consolidation/tasks/T-001/brief.md (ready, executable, guided)
  SHA-256 94cc2e185f1aef939a17d23db629cfef90bd33d6aca7727ad3de1ddaf65a2ebf
Verification revision 2: SHA-256 962a9b138d3491eff9ee4d6a372226af8cdbc9f7062d389308c1d8f699d616b1
  Scenario IDs V-01..V-06 unchanged; V-05/V-06 revised for run-evidence namespace
HEAD baseline: b65f900e7515ccfe36335b793b0c058b7b2bfa8c
Deltas to fix:
  F-02 (V-01/V-06): refresh exact worktree identities for the two changed INCLUDED
       preparation paths (brief.md 94cc2e18..., verification.md 962a9b13...); keep
       index/worktree versions distinct; preserve other 515 rows
  F-03 (V-05): stop treating the namespaced run-evidence finish ref as an AC-05
       violation; attribute begin/recovery/finish refs + snapshots separately and
       restate the AC-05 / submission disposition under revision 2
Protected state: files, index, and refs OUTSIDE refs/personal-skills/run-evidence/
  protected-ref check: git for-each-ref --format='%(refname) %(objectname)'
    --exclude='refs/personal-skills/run-evidence/**'  -> expect 40 refs
Namespace (authorized): git for-each-ref refs/personal-skills/run-evidence/ -> 92 refs
Scope: read-only audit output; preserve docs/future-work (incl. stale/), old
  docs/project-plan-review.md, unrelated docs; candidates = docs/tasks/ + old
  docs/project-plan.md + old docs/task-map.json
Gates: Q-001/Q-003 supplied (record with source); Q-002 open owner gate -> overall
  BLOCKED may remain truthful; do not delete or publish
Do NOT: modify audited inputs/index/other refs/user work; run consumer suites as proof;
  refresh .agents/
Next: fresh independent task-review-discovery -> separate task-acceptance-review
```

## Current correction readiness — 2026-10-14

Status: `ready`. This focused refresh supersedes the prior current-state rows,
not the brief or verification revision 2. Active preflight skill:
`.agents/skills/task-implementation-flow/task-preflight/SKILL.md`.

The owner now requests completion of cleanup-v1. The existing eight staged
T-001 preparation/output/review files are pre-existing user work; their staging
is not attributable to this correction. Preserve the index and all protected
refs at the current baseline. No overlapping writer is present. Originals,
consumer source, authority and verification revision 2 are unchanged.

Q-002: owner selected `archive/documentation-pre-cleanup-2026-10-14`, `origin`,
and root `README.md` in this session. The owner will commit the snapshot. Tag
publication and fresh recovery follow that commit; no commit is authorized for
the implementer. T-002 remains gated on the owner commit and actual recovery.

V-01/V-06: re-inventory current preparation bytes and all added task outputs,
separating HEAD/index/worktree identities. V-02/V-03: original family and consumer
bytes are unchanged; corroborate mapped source evidence. V-04: record the actual
owner reply and distinguish archive settings from recovery. V-05: capture current
index/protected-ref baseline and compare after correction; separately record
authorized instrumentation. All six scenarios remain feasible with Git and
Python standard library reads; no consumer suite is required for this audit.

Standalone value: material, resolved current staged-state ownership and new
archive authority. Current baseline: HEAD `b65f900e7515ccfe36335b793b0c058b7b2bfa8c`, raw index SHA-256 `fe4a868731cf3517853416b51d84ccf7c64eea4e2944313e6e3499af8ff7e190`,
normalized index SHA-256 `ae8fa311ae523af35146e70b3f63f64f0de9bc8833e6abf27b9b7a06d66428cc`. Exact pre-existing state is recorded in the
corrected result. Allowed write remains audit output and preparation/review
artifacts; audited originals, index and other refs remain protected.

Next: bounded correction -> fresh independent discovery -> separate acceptance
-> owner snapshot commit -> T-002 publication/recovery. No maintainability or
registry stage applies to this evidence-only correction.
