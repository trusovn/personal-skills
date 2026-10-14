# Task Preflight: `T-001` — Audit preservation and retirement eligibility

Status: `ready`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | `ideas/documentation-consolidation/tasks/T-001/brief.md`, `Status: ready`, `Task kind: executable`. Authority: owner request + owner-approved [direction brief](../../documentation-consolidation.brief.md), cleanup-v1 [plan](../../project-plan.md) §§1–2, 4, 8 FLOW-001, 10–12, [task map](../../task-map.json) `T-001` (depends_on: [], consumes ART-001/ART-005, produces ART-002). [Plan review](../../project-plan-review.md) accepts planning, not current eligibility. |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills`; root `AGENTS.md` followed; `.agents/skills/` holds no matching copy of this skill, so the user-global `task-preflight` is the active installation. |
| Dependencies / entry criteria | No predecessor task. Consumed roots exist and are readable: `docs/tasks/` (180 tracked files), old `docs/project-plan.md`, `docs/task-map.json`, `docs/project-plan-review.md`, `docs/future-work/` (15 tracked files: `FEATURE-MAP.md`, `concepts/`, `stale/`). Tools present: `git`, `rg` 15.1.0, `sha256sum`, `python3` 3.14.4. |
| Allowed scope | Write only `ideas/documentation-consolidation/tasks/T-001/results.md` (plus this `preflight.md` and review artifacts in the same task directory). Everything audited is read-only. |
| User-work ownership | No overlap. The write path directory currently holds only `brief.md` and `verification.md`; no `results.md` exists. Entire `ideas/` package is untracked planning-package work; the implementer records, never edits, it. |
| Permission limits | No network, no destructive/privileged/staged actions, no commit/push, no `.agents/` refresh, no edits to either old or new plan documents. Running consumer suites is not required for this audit. |
| Profile | `guided` |
| Standalone preflight value | `material` — exact uncertainties resolved: (1) verification-brief freshness binding; (2) untracked/ignored input surface inside and outside the candidate boundary; (3) absence of submodule/LFS/symlink external-content boundaries among tracked candidates; (4) feasibility of the read-only command surface. See Decision context. |
| Source brief / revision | `ideas/documentation-consolidation/tasks/T-001/brief.md` — SHA-256 `5f417e6d157800711d6d763592c4173932118c9dec7c18190dec947ac0404d42` (untracked working-tree bytes) |
| Verification / Verification revision | `ideas/documentation-consolidation/tasks/T-001/verification.md`, revision 1 — SHA-256 `bbeafc7a85d7ef5f3c3974f5b178a0e2cf35efb9dbfa82d35faa21d3dc17f105`. `Source brief:` resolves to the package brief and the recorded brief digest matches current bytes. |
| Current applicability | `HEAD` = `32edda26bf82b0a494993afc17e564722e51808d` ("docs(future-work): add Jev-neutral decision-model benchmark proposal"). Status: only untracked paths — `ideas/` package (4 files) and four `.DS_Store` files (repo root, `docs/`, `docs/tasks/T-005.3/`, `skills/`). No `docs/contracts/` registry; no known-issues file discovered in scope. No owner answers to Q-001–Q-003 are recorded anywhere in the package or plan; they remain open execution questions (plan §12). |

## Decision context

- Intended use: T-001 produces ART-002 (one evidence-backed audit manifest) that T-002 (preservation), T-003 (consumer/verification map), and T-004/T-005 (eligibility, pending work, identity) consume. A blocked audit is a valid, expected result.
- Failure consequences: a manifest missing untracked/ignored inputs or misclassifying unfinished work as eligible would later permit archive/retirement decisions on wrong facts (INV-001/003/004/006). Drift must invalidate affected facts, never be repaired by editing originals.
- Priorities: record actual evidence; task index, commit label, future catalog, or a passing structural check cannot establish completion. Preserve historical verdicts and unrun limits.
- Known state facts for the implementer (all re-verified at audit time):
  - Tracked candidates: `docs/tasks/` + old `docs/project-plan.md` + old `docs/task-map.json` = 182 index entries, all mode `100644` (no symlinks). No `.gitmodules` (no submodules), no `.gitattributes` (no LFS filter config), `git-lfs` command absent — current tracked scope has no external-content boundary; the implementer must still verify and record this absence with scoped commands.
  - Untracked, unignored: the whole `ideas/` planning package (a relevant preservation input, per brief); four `.DS_Store` files, one inside the candidate tree (`docs/tasks/T-005.3/.DS_Store`) — unrelated, must be explicitly excluded with reason.
  - Ignored/other: `.agents/`, `.handoff/` (contains one session-handoff file, unrelated), `__pycache__/`, `*.py[cod]` via root `.gitignore`; `.pytest_cache/` excluded by its nested `.gitignore`; `.tmp-targeted-cv-template/` is an empty directory (git reports nothing).
  - Terminology: plan line 301 already interprets the owner's "future-tasks" as `docs/future-work/`; the audit confirms or records a contradiction (AC-02).
- Assumptions: ordinary unknown candidate dispositions become recorded unknowns or blockers, not silent eligibility. No routine user questions are needed; ask the owner for Q-001–Q-003 only when facts are ready, per brief.

## Acceptance evidence and commands

| AC / scenario / risk | Authority relationship | Setup / decisive boundary / oracle | Exact command / cwd | Feasibility: dependencies / permissions / ownership | Baseline result / gap |
|---|---|---|---|---|---|
| AC-01 / V-01 / R-01 (INV-001, INV-006) | Brief AC-01; verification V-01 | Reconcile real Git/index/filesystem inventory (tracked, staged, unstaged, untracked, ignored) with manifest membership, identities, modes, Git states; unresolved inclusion blocks affected scope | `git rev-parse HEAD`; `git status --porcelain=v1 --untracked-files=all`; `git ls-files --stage -- <paths>`; `git diff --raw -- <paths>`; `git diff --cached --raw -- <paths>`; `git ls-files --others --ignored --exclude-standard -- <paths>`; `sha256sum <untracked path>` — cwd repo root | Feasible: all tools present; read-only. External-boundary absence verified (182×`100644`, no `.gitmodules`/`.gitattributes`); implementer re-verifies and records | Not run — the inventory itself is the task output (T-001) |
| AC-02 / V-02 / R-02 (INV-004, INV-006) | Brief AC-02; verification V-02 | Every candidate maps to original completion/review/qualification evidence or explicit unknown; pending obligations carry evidence, retained context/next owner, disposition or owner gate | Scoped `rg -n` searches plus reads of `docs/tasks/**`, old `docs/project-plan.md`, `docs/task-map.json`, `docs/project-plan-review.md`, `docs/future-work/**`; implementer records roots/patterns | Feasible: evidence roots exist and are readable; `rg` present | Not run — reconciliation is the task output |
| AC-03 / V-03 / R-03 (INV-003) | Brief AC-03; verification V-03 | Live readers traced through fixture/setup/input closure; executable dependencies vs active navigation vs historical mentions distinguished; existing owners/scenarios/oracles/selectors recorded | Scoped `rg -n` from known starts: `tests/test_review_composition.py`, `tests/review_fixture_support.py`, `tests/staging_fixture_support.py`, `tests/README.md`, `docs/tasks/T-005.1/setup_consumer.py`; follow to transitive inputs | Feasible: all known starts exist. Known T-003 baseline selector `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` is recorded, not run by T-001 | Not run — consumer map is the task output |
| AC-04 / V-02, V-04 / R-02 | Brief AC-04; verification V-04 | Q-001 (exact archive inclusion), Q-002 (tag/destination/publication/navigation), Q-003 (completion/pending dispositions) each get a sourced decision or a stated question, owner, affected later task; per-candidate + overall `ELIGIBLE`/`BLOCKED` | Read plan §12 definitions and any supplied owner decisions; record unresolved gates | Feasible. Current fact: no owner answers recorded in package/plan; expected overall `BLOCKED` for archive advancement unless decisions are supplied during the audit — a valid T-001 result | Not run — gate reconciliation is the task output |
| AC-05 / V-05 / R-04 (INV-006) | Brief AC-05; verification V-05 | Before/after scoped identities, index and refs agree except attributed task artifacts; no staging/deletion/migration/navigation or report edits | Record baseline at audit start; re-check `git status`, scoped hashes, `HEAD` after writing `results.md` | Feasible: write path empty of user work; read-only commands only | Not run — baseline capture is implementation step 1 |
| AC-05 / V-06 / R-04 (INV-006) | Brief AC-05; verification V-06 | Observed drift invalidates affected facts until reinspection; user files never restored/overwritten | Compare initial/final identities; record drift and re-inspect affected rows or mark blocked | Feasible: no fault injection required; absence of drift is recorded under V-05 | Not run — drift check is implementation step |

Every verification scenario (V-01–V-06) and risk row (R-01–R-04) is covered above; no row is dropped or blocked. The decisive oracle is existing Git/filesystem/source inspection; no new harness, no live-model eval, no network or destructive check belongs to this task.

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| Whole `ideas/` package is untracked | Manifest must record the planning package (including `preflight.md`, `results.md`) as a relevant untracked preservation input with filesystem hashes; never treat it as Git-tracked | Implementer records; no action needed now | Enumerate via `sha256sum`/`git ls-files --others`; attribute audit outputs distinctly (V-05) |
| `.DS_Store` files untracked, one inside candidate tree (`docs/tasks/T-005.3/`) | Must be explicitly excluded with reason; do not silently ignore or indiscriminately collect | Implementer records exclusion with reason | List in manifest exclusions (AC-01) |
| No owner answers to Q-001–Q-003 exist | Archive advancement and affected retirement stay gated; overall assessment expected `BLOCKED` until owner decides | Owner; T-001 records the gates | Ask the owner when facts are ready; silence is not approval (brief §Stops) |
| Budget: 25 tool calls / 60 min / 80k context (brief) | Soft checkpoint; preserve a truthful partial result and structured continuation if reached | Implementer | Stop with structured handoff instead of labeling unchecked scope complete |

Implementation stops: edit nothing outside the T-001 task directory; never modify audited inputs, index, refs, or user work; do not run consumer suites as eligibility evidence; do not refresh `.agents/`; stop affected assessment on inaccessible decisive evidence, conflicting authority, or concurrent drift.

**Next action:** implement the audit with `bounded-task-implementer` writing only `ideas/documentation-consolidation/tasks/T-001/results.md`. After implementation/correction, the brief requires a fresh independent `task-review-discovery` pass, then a separate `task-acceptance-review` decision (`review: immediate`). No maintainability or registry stage is expected for this evidence-only output.

## Implementer handoff

```text
Implement: ideas/documentation-consolidation/tasks/T-001/brief.md (ready, executable)
Write only: ideas/documentation-consolidation/tasks/T-001/results.md
Bind: brief SHA-256 5f417e6d157800711d6d763592c4173932118c9dec7c18190dec947ac0404d42;
      verification revision 1 (bbeafc7a85d7ef5f3c3974f5b178a0e2cf35efb9dbfa82d35faa21d3dc17f105);
      HEAD 32edda26bf82b0a494993afc17e564722e51808d
Scope: read-only audit; preserve docs/future-work (incl. stale/), old docs/project-plan-review.md,
      unrelated docs; candidates = docs/tasks/ + old docs/project-plan.md + old docs/task-map.json
Known state: 182 tracked candidates all mode 100644 (no symlink/submodule/LFS boundary);
      untracked: ideas/ package + 4x .DS_Store (one at docs/tasks/T-005.3/ — exclude with reason);
      ignored: .agents/, .handoff/, __pycache__/, *.py[cod], .pytest_cache/ (nested .gitignore)
Gates: Q-001..Q-003 open (plan §12); record as unresolved owner gates; expected overall BLOCKED
Commands: git rev-parse/status/ls-files(--stage,--others --ignored)/diff(--raw,--cached --raw),
      sha256sum for untracked bytes, scoped rg for consumers; do NOT run consumer suites
Verification: map every V-01..V-06 scenario and R-01..R-04 row to manifest evidence;
      record initial/final identities and any drift (V-05/V-06)
Next: fresh independent task-review-discovery -> separate task-acceptance-review
```
