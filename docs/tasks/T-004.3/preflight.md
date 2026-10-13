# Task Preflight: `T-004.3` — Prove explicit refresh and distribution closure

Status: `ready`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | `docs/tasks/T-004.3/brief.md`, Status `ready`, kind `executable`; index.json: T-004.3 executable, parent T-004 composite, `depends_on` T-004.1, T-004.2. Authority: `docs/project-plan.md` sections 1–2, 10–11 (ART-009–011, IF-007, FLOW-004), `docs/tasks/T-004/brief.md`, `docs/task-map.json`. Not composite/decomposed — no rerouting needed. |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Dependencies / entry criteria | T-004.1: reviews `discovery-01`, `discovery-02` (complete coverage, no findings). T-004.2: reviews `discovery-01..04` (complete, no findings) and `maintainability-01/02` VERDICT ACCEPT. No `acceptance-*.md` report exists in either package; discovery reports state acceptance decisions are separate calls. Consumed .1/.2 contracts (unborn install; read-only check) have clean current review evidence. Non-blocking noted fact, see warnings. |
| Allowed scope | Additions/consolidation in `tests/test_install_development_skills.py`; minimal installer repairs in `scripts/install_development_skills.py`; root `README.md`, `skills/README.md`, `skills/task-implementation-flow/README.md`; new `docs/tasks/T-004.3/results.md`. Read-only: current `.agents/`, plans/index, historic results/reviews, .1/.2 implementations except bounded integration repair. |
| User-work ownership | Clean. Untracked, out-of-scope: `.DS_Store` at root/`docs/`/`skills/` (incidental macOS artifacts — leave untouched); untracked `docs/tasks/T-004.3/verification.md` (the required derived verification input — preflight does not modify it). No dirty tracked files. `HEAD` = `12c5c4a2901e5e8f3b1fb6bad22e87f69729ffd7`. |
| Permission limits | No network, live, model-budget, role-call or whole-repo checks. Disposable local Git targets only. Never refresh this run's `.agents/` (brief stop). Commit/advance decisions belong to later stages, not this task. |
| Profile | `guided` |
| Standalone preflight value | `material` — resolved the brief-named uncertainties: exact check CLI and exit codes (0 match / 1 drift / 2 failure, read-only, does not repair), current owning test selectors, reviewed .1/.2 outputs, and genuine unborn preservation across the journey. |
| Source brief / revision | `docs/tasks/T-004.3/brief.md`; SHA-256 `bdf0c28a9184c72438b69466046a7eece5971b34b30adf33e28f244adcdc4098` (recomputed, matches the verification design's declared source revision). |
| Verification / Verification revision | `docs/tasks/T-004.3/verification.md`, revision 1, SHA-256 `50bd1ef5fbd1e196ecfa130eea54d2a86daca0366e52a4b91654b51a7f1617d4`. `Source brief:` resolves to the package brief. Scenarios V-01–V-06 cover AC-01–AC-05 and R-01/R-02. |
| Current applicability | Decision bound to the brief revision above and verification revision 1. Current HEAD/status captured; no material authority, prerequisite, ownership, permission or capability changes since. |

## Decision context

- Direction: parent P-01–06 closure; composes `ART-009/010/011`, `IF-007`, `FLOW-004`, `INV-009`. Required consumer is T-005, which receives the qualified ART-010 projection, the ART-011 check interface and explicit remaining qualification gaps.
- Operating envelope: real canonical CLI calls in disposable unborn and committed Git targets; independent source-to-installed byte comparison; no active-installation mutation; no model calls.
- Failure consequences: a checker that repairs drift, a refresh claimed without a prior detected-drift occurrence, or unmanaged bytes lost under refresh would silently invalidate INV-009 and misqualify T-005's installed-flow proof.
- Priorities: narrow ownership, exact byte preservation outside the managed block, singular markers, unchanged refusal boundaries, filesystem/Git proof never presented as skill-call behavior.
- Known issues: no known-issues file found under `docs/` — no recorded deferrals to re-examine.
- Assumptions: existing positional installer rerun is the refresh action (brief assumption, verified as `install()` with exit 0); ordinary unknowns (exact test method naming for new cases) are in-scope implementer choices.
- Stops preserved: changed authority, user-work overlap, unsafe permission needs, missing decisive capability, scope expansion; the two-materially-different-failed-fixes stop; never refresh this run's `.agents/`.

## Acceptance evidence and commands

| AC / scenario / risk | Authority relationship | Setup / decisive boundary / oracle | Exact command / cwd | Feasibility: dependencies / permissions / ownership | Baseline result / gap |
|---|---|---|---|---|---|
| AC-01 / V-01 / R-01 | Brief AC-01; INV-009 via plan | Both Git states, full ordered journey; real CLI exit status + filesystem/Git snapshots; checks cannot repair; unborn stays unborn | `python3 scripts/install_development_skills.py <target>` then `python3 scripts/install_development_skills.py --check <target>` (disposable targets under `/tmp/opencode`) | Feasible. Verified today in a disposable unborn repo: install exit 0; fresh check exit 0 `match=True` (86 paths); drifted check exit 1 with exact `changed` path; repeat check exit 1 and drifted bytes intact; unborn HEAD unresolvable throughout. Committed variant covered by existing fresh-install/check test + .2 evidence. | Passed smoke (disposed). Full journey is future task evidence. |
| AC-02 / V-02 / R-01 | Brief AC-02; ART-009/010 | Representative managed families: skill, reference, eval, setup, guide, shared helper/config/schema, marked block; changed+missing states overall; owned non-transient extra; independent final projection comparison | Extend `test_rerun_removes_stale_managed_files_and_preserves_unmanaged_installations`; reuse `test_check_reports_changed_bytes_for_every_managed_family` / `..._missing_bytes...`; independent enumeration via check JSON + file walk | Feasible. Existing family and owned-extra (`unexpected` category) coverage exists and is reviewed (.2 discovery V-02 pass); no new helper/harness authorized or needed. | Family coverage exists (do not duplicate .2 matrix). .3 adds ordered refresh occurrences. |
| AC-03 / V-03, V-04 / R-02 | Brief AC-03; INV-009 | Unselected skill/reference, non-managed helper, other project files, outside-block prefix/suffix bytes (incl. deliberate whitespace), first insertion vs existing block, singular markers; malformed/unsafe inputs stay refused | Reuse unmanaged sentinel `test_check_ignores_unmanaged_content_and_installer_transient_files`, install preservation `test_installs_profile_preserves_agents_text_and_final_availability`, refusal retention `test_check_failures_retain_existing_refusals_and_stay_distinct_from_drift`, marker `test_check_reports_agents_block_drift_and_precise_marker_failures` | Feasible. `_render_agents` preserves prefix/suffix; refusal/malformed-marker paths raise `InstallError` (exit 2). No silent repair of unsafe targets. | Existing cases pass (in owning suite); keep them intact, strengthen only distinct missing byte evidence. |
| AC-04 / V-05 | Brief AC-04; FLOW-004 | Selection (`DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`), guide, focused tests and three READMEs agree; positional install syntax; `--check` 0/1/2 semantics; refresh = separate rerun | Guides test `test_check_matches_install_from_unrelated_cwd_and_guides_document_semantics`; reconcile root `README.md`, `skills/README.md`, `skills/task-implementation-flow/README.md` | Feasible. Exit codes verified today (0/1/2 observed); installer docstring/help matches V-05 claims. | No gap. |
| AC-05 / V-06 | Brief AC-05; ART-010/011 handoff | New `docs/tasks/T-004.3/results.md` with reproducible starting states, exact CLI/probes, observed outputs, installed identities; filesystem/Git proof distinguished from unrun skill-call/model behavior | Evidence audit from each claim to its runnable setup and observed output | Feasible. All setup mechanics proven runnable today; results file is new, in allowed scope. | Not run (future artifact). |
| R-01 / R-02 (fresh discovery) | Brief finite-risk contract; INV-009 | Independent probes: delete a managed reference + add an owned extra (R-01); outside-block whitespace + unmanaged helper survival (R-02) | Implementer: targeted cases first, then owning suite `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`; fresh discovery: independent probes then one justified union `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence` | Feasible. `tests/` has no `__init__.py` (discover and PYTHONPATH=tests forms are correct). Focused selector `...test_rerun_removes_stale_managed_files_and_preserves_unmanaged_installations` ran today: 1 test OK in 0.247s. | Focused selector passed; owning suite and union are future (implementer/discovery) commands — readiness does not claim future behavior passed. |

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| None — no blockers. | Implementation can begin under the recorded scope and policy. | — | — |
| Warning: no `acceptance-*.md` report files exist for T-004.1/T-004.2 packages. | Non-blocking: current review evidence (complete discovery, no findings; .2 maintainability ACCEPTs) satisfies the brief's "reviewed .1/.2 outputs" for consuming their contracts. | Coordinator / .1–.2 acceptance stages | Confirm .1/.2 acceptance dispositions are recorded before T-005 qualification; not required to start .3. |
| Warning: untracked `docs/tasks/T-004.3/verification.md` is a required input; preflight must not modify it. | Non-blocking. | .3 implementer | Leave untouched; recalculate brief+verification digests before the first edit. |
| Warning: budget `10 tool calls / 25 minutes / 40k context` is an implementation checkpoint. | Non-blocking; preflight work is not part of that budget. | .3 implementer | Stop with a structured handoff at the checkpoint. |

Implementation stops: changed authority, user-work overlap, unsafe permission needs, missing decisive capability, scope expansion, two materially different failed fixes, or any refresh of this run's `.agents/`.

Next exact action: implementer begins targeted lifecycle/preservation cases (controlled owned deletion/change detected then restored; fail-first regression before any preservation repair), then runs the owning installer suite, reconciles distribution guidance, and writes `docs/tasks/T-004.3/results.md`; then hands completed bytes to fresh independent `task-review-discovery` followed by separate `task-acceptance-review`.

## Implementer handoff

```text
T-004.3 preflight: ready (guided, standalone value material — exact check CLI/exit codes
0 match / 1 drift / 2 failure, read-only and non-repairing, verified in a disposable
unborn target today; owning selectors confirmed; .1/.2 reviewed outputs confirmed clean).

Scope: tests/test_install_development_skills.py (extend rerun case; reuse .2 family/sentinel/
refusal cases), minimal installer repairs in scripts/install_development_skills.py, README
reconciliation (root, skills/, skills/task-implementation-flow/), new
docs/tasks/T-004.3/results.md. Read-only: .agents/, plans/index, history, .1/.2 except
bounded integration repair.

Ownership: only untracked files are .DS_Store (leave) and T-004.3/verification.md
(required input, leave). HEAD 12c5c4a2…ffd7. Brief SHA-256 bdf0c28a…c4098,
verification revision 1 SHA-256 50bd1ef5…617d4.

Commands: installer `python3 scripts/install_development_skills.py <target>` (exit 0);
check `python3 scripts/install_development_skills.py --check <target>` (0/1/2).
Targeted first: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest
test_install_development_skills.DevelopmentSkillInstallerTests.<case>;
owning suite: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p
test_install_development_skills.py; fresh discovery union: PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version
test_run_evidence.

Stops: changed authority, user-work overlap, unsafe permissions, missing capability,
scope expansion, two materially different failed fixes, never refresh this run's .agents/.

Next: implement .3, publish results.md, then fresh task-review-discovery → separate
task-acceptance-review.
```
