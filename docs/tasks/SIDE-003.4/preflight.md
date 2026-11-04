# Task Preflight: SIDE-003.4

Status: ready
Profile: guided
standalone_preflight_value: marginal

## Readiness summary

Source brief: docs/tasks/SIDE-003.4/brief.md (`Status: ready`, `Task kind:
executable`, guided profile, `review: immediate`), HEAD b7b3337 "S-003.3 done"
(unchanged task brief). Verification: docs/tasks/SIDE-003.4/verification.md,
revision 1, `Status: ready`; its `Source brief:` declaration resolves to
docs/tasks/SIDE-003.4/brief.md. Repository:
/Users/mtrusov/work/skill-sources/personal-skills.

Initial `git status --short` shows only untracked
`docs/tasks/SIDE-003.4/verification.md` (this task's preparation artifact) and
pre-existing unrelated untracked `.DS_Store` files (`.DS_Store`,
`docs/.DS_Store`, `skills/.DS_Store`). No other description leaf is active; no
concurrent description writer.

Baseline currency re-verified: `python3 tools/baseline_measure.py` (saved at
/tmp/side0034-preflight-check.json) reproduces all-26 = 11,815 and profile-20 =
8,176 description characters with body totals 388,640 / 320,123, and all five
target rows equal the frozen SIDE-003.1 record
(docs/tasks/SIDE-003/baseline-measurements.json) exactly — description
characters 515 (bounded-task-implementer), 640 (task-maintainability-review),
279 (task-contract-registry-updater), 494 (task-review-discovery), 599
(task-acceptance-review), with matching `file_bytes` and `sha256`. The running
totals match the post-SIDE-003.3 state recorded in
docs/tasks/SIDE-003/description-results.md (11,815 / 8,176); the .2/.3 deltas
on the other 11 skills are expected and recorded. The saved baseline is current
for the five unchanged target packages.

Scope: only the `description` frontmatter scalar of the five named
`skills/task-implementation-flow/` packages, this leaf's appended section in
docs/tasks/SIDE-003/description-results.md, and description-quoting assertion
sync if truly needed. Bodies, names, folder paths, invocation identities, the
saved baseline record, and the measurement tool stay fixed.

## Decision context and current applicability

Authority: brief AC-01–03, SIDE-003 plan "Description design" boundary-group
table rows 5–6, parent brief, and the SIDE-003.1 baseline. Priority: preserve
every activation route and each group's nearest-neighbor distinction over the
150–300-character advisory range; the implementer's supplied-machine-contract
high-assurance route must remain explicitly visible (AC-02, V-01a-M). Group 5
distinction: authoring scoped implementation vs independent structural review
when policy or the user requires it. Group 6 distinction: synchronizing current
contracts vs independent evidence without a verdict vs a separate acceptance
decision after discovery.

The consumer is the source discovery catalog; installed copies are deliberately
not refreshed in this phase. No registered contract authority touches a
description scalar (the contract index holds no description as authority), so
no registry stage applies; the brief's expected contract impact is none. No
maintainability stage applies (metadata-only edits, no implementation assets).
Conditional stages: inapplicable. Aggregate `python3 tools/verify.py` and live
fresh-model routing are owned by SIDE-003.18 / separately approved budget; this
leaf never runs them and reports them pending.

Owning-consumer scan (performed for this family; implementer re-verifies
editorially): ~450 asserted string literals across
tests/test_bounded_task_implementer.py, tests/test_task_maintainability_review.py,
tests/test_review_composition.py, tests/test_task_review_discovery.py,
tests/review_fixture_support.py, tests/test_run_evidence_availability.py,
tests/test_task_acceptance_review.py — no literal is description-only;
"preflight" (implementer) and "acceptance decision call" (discovery) overlap a
description but also appear in the unchanged bodies. No assertion sync is
expected.

One of the five scalars (task-maintainability-review) uses folded `>`
frontmatter; edits, sentinel masks, and measurements must treat the whole folded
block as the scalar.

The standalone stage was routine: paths, commands, oracles, baseline currency,
and text consumers are all checkable with cheap local commands, and every fact
the coordinator supplied reproduced except one environment detail resolved
below (PyYAML). Routine basis: no ownership conflict, no ambiguous or expensive
command/oracle, no real-boundary capability is required.

## Acceptance evidence and feasibility

| Cases / AC | Setup and oracle | Command / feasibility |
|---|---|---|
| V-01a–e E/P/N/B, V-01a-M, V-01a–e-FULL; AC-01/02 | Compare full old descriptions clause by clause against plan rows 5–6 and the verification's prompts; every trigger, input, and exclusion must remain discoverable; removed procedural detail must be in the body or kept and flagged; implementer's machine-contract route must stay visible (wording limited to "explicitly requested high-assurance" fails V-01a-M) | Local editorial review with results checklist; all authorities (plan rows, five SKILL.md files, bodies) available. Live fresh-model routing designed but pending separate budget approval; pending cases are not behavioral passes. |
| V-02; AC-03 | Git HEAD b7b3337 originals; replace only each package's description scalar with a sentinel (mask the entire folded `>` block for task-maintainability-review); expect byte-identical remainders, exactly five changed skill paths under `skills/`, unchanged names/paths/identities | `git diff --stat` plus targeted `git diff` per file, plus Python byte comparison after sentinel masking; local and feasible. This is the decisive negative oracle (fail-first infeasible for editorial compression). |
| V-03; AC-01/03 | Before JSON is /tmp/side0034-before.json (family convention); expect 26 source / 20 profile entries, body bytes 388,640 / 320,123 unchanged, all-26 and profile-20 reductions each equal the sum of the five per-skill reductions, other 21 rows unchanged including accepted .2/.3 descriptions | `python3 tools/baseline_measure.py` before and after; reproduced successfully in this preflight (five target rows match the frozen baseline exactly, totals 11,815 / 8,176). Feasible. |
| V-04; AC-03 | Owning-consumer suites; no assertion quotes changed description text (prior ~450-literal scan; implementer re-verifies editorially before and after edits) | 13 focused suites each as `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <pattern>` — all files confirmed present under tests/ (test_bounded_task_implementer.py, test_run_evidence.py, test_run_evidence_availability.py, test_maintainability.py, test_review_composition.py, test_task_preparation_contracts.py, test_task_flow_guides.py, test_task_maintainability_review.py, test_task_review_discovery.py, test_task_acceptance_review.py, test_contextual_export_risks.py, test_contextual_known_issues.py, test_contextual_uncertainty_inputs.py). Local; feasible. |
| V-04 (optional); AC-03 | Five package frontmatters via quick_validate.py | **PyYAML is NOT available in this environment** (`python3 -c "import yaml"` → ModuleNotFoundError; contrary to the expected fact). AC-03/V-04 explicitly authorize recording the skip when unavailable. Implementer must record the skip; do not install dependencies. |
| Required final checks (AGENTS.md); AC-03 | Architecture gate and contract check | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` and `python3 tools/check_contracts.py --root .`; local and feasible; the implementer runs them. |
| Broader gate; AC-03 | Aggregate gate and live routing qualification | `python3 tools/verify.py` and live fresh-model routing owned by SIDE-003.18 / separately approved budget; this leaf reports them pending and never runs them. |

## Limits, stops, and next action

No blocker. One judgment call: quick_validate.py is infeasible here (no
PyYAML); the brief and verification both pre-authorize recording the skip, so
it does not affect readiness.

Stops (from the brief): do not narrow activation to hit the 150–300-character
range (especially the implementer's supplied-machine-contract route); do not
touch bodies; do not run concurrently with another active description leaf; a
missing or stale SIDE-003.1 baseline stops work (re-verified current here).
Expected description edits and this leaf's results section do not invalidate
this readiness.

Next: the implementer implements the five description scalars, records this
leaf's results section, runs the local checks, and ends at READY_FOR_REVIEW
naming the route (architecture gate → fresh independent task-review-discovery →
separate fresh task-acceptance-review); it never launches reviewers.

---

## Implementer handoff

Confirmed scope and ownership: change only the `description` frontmatter scalar
of the five packages — bounded-task-implementer, task-maintainability-review,
task-contract-registry-updater, task-review-discovery, task-acceptance-review
(all under `skills/task-implementation-flow/`); append this leaf's section to
docs/tasks/SIDE-003/description-results.md; sync an assertion only if it truly
quotes changed description text (none expected). Bodies, names, paths,
invocation identities, the saved baseline, and the measurement tool are out of
scope. No other writer is active; working tree contains only this task's
preparation artifacts and unrelated `.DS_Store` files.

Exact targeted commands, in order:

1. `python3 tools/baseline_measure.py > /tmp/side0034-before.json` — confirm
   five target rows still equal the frozen SIDE-003.1 record (515 / 640 / 279 /
   494 / 599 characters, matching `file_bytes` and `sha256`) and totals
   11,815 / 8,176; a mismatch stops work.
2. Edit the five description scalars (folded `>` block treated as one scalar
   for task-maintainability-review).
3. V-02 sentinel-mask guard: for each changed package, compare the worktree
   file to the HEAD b7b3337 original after replacing only the description
   scalar (the entire folded block for task-maintainability-review) with a
   sentinel in both; expect byte-identical remainders. Then `git diff --stat`
   plus targeted `git diff` per file: exactly five changed skill paths,
   description-line-only changes, everything else unchanged.
4. `python3 tools/baseline_measure.py > /tmp/side0034-after.json` — record
   per-skill old/new counts and catalog deltas in the results section.
5. Run the 13 focused suites, each as
   `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <pattern>`
   (patterns listed in the feasibility table above).
6. `python3 skills/skill-creator/scripts/quick_validate.py <package>` for the
   five packages — **PyYAML is unavailable here; record the skip instead of
   running it; do not install anything.**
7. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`
8. `python3 tools/check_contracts.py --root .`

Machine-contract route preservation (AC-02 / V-01a-M): the compressed
bounded-task-implementer description must keep the supplied-machine-contract
high-assurance route visible by naming supplied machine contracts (or
equivalent); wording limited to "explicitly requested high-assurance" fails.
A per-skill light edit or no-op is acceptable where current wording already
preserves routing (task-contract-registry-updater at 279 is already in range);
never narrow activation to hit the range. Removed procedural detail must be
already in the body or kept and flagged in the results.

Exact next action: implement the five scalars, record this leaf's section in
docs/tasks/SIDE-003/description-results.md (old/new wording, character counts,
preserved boundaries, catalog measurement delta), run commands 3–8 above, then
end at READY_FOR_REVIEW naming the route: architecture gate → fresh
independent task-review-discovery → separate fresh task-acceptance-review. Do
not launch reviewers.