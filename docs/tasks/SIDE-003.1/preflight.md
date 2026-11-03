# Task Preflight: SIDE-003.1 — Freeze the loading-cost baseline

Status: `ready`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | `docs/tasks/SIDE-003.1/brief.md`, status `ready`, task kind `executable`, guided profile; authority: SIDE-003 plan ("Current source baseline", "Measurement and decision rules" layers 1–2, "Delivery sequence" phase 1) + parent brief; `docs/tasks/index.json` lists SIDE-003.1 as executable with no `depends_on` (dependency-ready leaf) |
| Repository | Repository root; HEAD `2007ca53ef92e94b76719f70ebe6e87c6baa9b6b`, clean before preparation (user-reported) |
| Dependencies / entry criteria | None blocking. All cited sources exist: `docs/development.md`, `docs/project-map.md`, `docs/contracts/index.json`, `tools/verify.py`, `scripts/install_development_skills.py`, `AGENTS.md`, `tests/test_architecture.py` |
| Allowed scope | New `tools/baseline_measure.py`; `docs/tasks/SIDE-003/baseline.md` + one machine-readable record beside the plan. Read-only over `skills/`, `scripts/`, `tests/` |
| User-work ownership | No overlap: `tools/` currently holds only `check_contracts.py`, `verify.py`; `docs/tasks/SIDE-003/` holds only `brief.md`, `plan.md` — all target paths free. Preparation artifacts (`verification.md`, this `preflight.md`) are expected permitted workflow effects |
| Permission limits | All commands local, standard library, no network/privilege/destructive actions. `PYTHONDONTWRITEBYTECODE=1` for the architecture suite |
| Profile | guided |
| Standalone preflight value | material — resolved: counting definitions (plan-explicit), route taxonomy (plan layer 2 matches brief), recording commit (HEAD `2007ca53`, clean; plan table at `aa94e28` → documented-delta path expected), and revealed mixed plain/folded frontmatter scalar shapes pinning the parser and V-02b's representative file |
| Source brief / revision | `docs/tasks/SIDE-003.1/brief.md`, revision 1 (brief declares `Status: ready`) |
| Verification / revision | `docs/tasks/SIDE-003.1/verification.md`, revision 1; `Source brief: brief.md` resolves to the package brief; status `ready` |
| Current applicability | Current tree is the baseline that matters; drift from `aa94e28` is expected and handled by V-02's exact-delta-with-cause path. No skill bytes change in this leaf |

## Decision context

The recorded baseline is the attribution basis for every later SIDE-003 leaf (.2–.18); a wrong counting definition or unreproducible route sum propagates into all per-route deltas. Intended use: repo-only, deterministic, read-only measurement. Counting definitions (plan, "Current source baseline"): body bytes = everything after the closing frontmatter delimiter including its following whitespace; description characters = normalized scalar text of the `description` field only, excluding other frontmatter fields. Route taxonomy (plan, layer 2): direct guided, packaged guided, high-assurance, corrections, optional evidence available/unavailable, representative acceptance path — matching the brief's named routes. Counts are UTF-8 byte/character evidence, never tokens; route sums are static unique-file estimates. No known-issues file applies to this leaf; no recorded deferrals found. Assumptions: route file lists are derived from each skill's current instructions and the read graph (cross-package links confirmed present, e.g., `bounded-task-implementer/SKILL.md` → `../../testing-discipline/SKILL.md`); rendered-catalog observation is environment-dependent and recorded as unobservable locally when it is. Frontmatter shapes: plain scalars (e.g., `task-preflight`) and folded multi-line scalars (e.g., `ask-user-questions`) both exist — normalization must handle both; V-02b should spot-check a folded-scalar file.

## Acceptance evidence and commands

All commands run from the repository root. No commands were executed during preflight (read-only inspection tools only); feasibility is confirmed by inspection, results are **not run**.

| AC / scenario | Authority | Setup / decisive boundary / oracle | Exact command / cwd | Feasibility | Baseline result / gap |
|---|---|---|---|---|---|
| AC-01 / V-01 determinism | Brief §Verification fail-first row; verification V-01 | Two runs on an unchanged tree; byte-identical output incl. route sums | `python3 tools/baseline_measure.py > /tmp/run1.txt && python3 tools/baseline_measure.py > /tmp/run2.txt && cmp /tmp/run1.txt /tmp/run2.txt` (repo root) | Feasible by inspection: script is task-owned new file; standard library; no execution performed | Not run — intended first evidence after implementation |
| AC-01 / V-02 table match or documented delta | Brief work item 4; verification V-02 | Row-by-row diff vs plan table (26 files, 404,992 file bytes, 388,640 body bytes at `aa94e28`); exact delta + cause per diverging file; subset = exactly the 20 plan-marked "yes" skills | `python3 tools/baseline_measure.py` + row diff vs `docs/tasks/SIDE-003/plan.md` table | Feasible: 26 `skills/**/SKILL.md` files confirmed present, names match the plan's 26 rows; 20 profile-yes rows identified; HEAD ≠ `aa94e28`, so the documented-delta outcome is expected and valid | Not run — inspection confirms the comparison is finite and well-defined |
| AC-01 / V-02b counting definitions pinned independently | Verification V-02b | One representative file (prefer folded-scalar, e.g., `skills/ask-user-questions/SKILL.md`); four metrics recomputed without the new script | `sha256sum <file>`; `wc -c <file>`; `awk`/`sed` frontmatter split + manual description normalization (throwaway, not committed) | Feasible: both plain and folded scalar shapes confirmed to exist; definitions plan-explicit | Not run — throwaway check at implementation/review time |
| AC-01 / V-03 route sums reproduce; lists consistent | Brief §Verification targeted row; verification V-03 | Each recorded route sum reproduces via supplied-list mode; list consistency checked separately against read graph + named instructions | `python3 tools/baseline_measure.py --sum <route file list>` per route (repo root) | Feasible: the `--sum` supplied-list mode is brief work item 1's required script capability; cross-package reference links confirmed present for read-graph derivation; route taxonomy confirmed in plan layer 2 | Not run — route lists are implementation output |
| AC-02 / V-04 record completeness | Brief work items 1–3; verification V-04 | Checklist of 8 items (a)–(h) incl. recording commit vs `git rev-parse HEAD` and prerequisites-map commands resolvable in `docs/development.md` / `tools/verify.py` | `git rev-parse HEAD`; checklist review | Feasible: all prerequisite-map sources exist; `tools/verify.py` discovery roots documented in `docs/development.md` (tests/, orchestrator, skill-creator, task-brief-designer); briefs for SIDE-003.9 and .11–.17 all exist for the body-work route lists | Not run — record is implementation output |
| AC-02 / V-05 byte/character labeling, no token claims | Brief AC-02; plan "Measurement and decision rules"; verification V-05 | Text review of record labels | `grep -in token docs/tasks/SIDE-003/baseline*.md` + judgment per hit | Feasible: labeling check on recorded data | Not run — record is implementation output |
| AC-03 / V-06 read-only over `skills/` | Brief AC-03; verification V-06 | Working tree shows only the new script + baseline artifacts (+ expected preparation artifacts); no `skills/` path modified; no `__pycache__` | `git status --porcelain` before and after runs; `git diff --stat` | Feasible: baseline was clean at HEAD `2007ca53` before preparation; expected deltas are exactly `tools/baseline_measure.py`, `docs/tasks/SIDE-003/baseline.md`, one machine-readable record, plus preparation artifacts | Not run — post-implementation observation |
| Owning suite / V-07 architecture policy | Brief §Verification owning-suite row; verification V-07; `AGENTS.md` canonical check | Zero failures attributable to the new script (declared stdlib imports only, CLEAN policy) | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` (repo root) | Feasible by inspection: `tests/test_architecture.py` exists; command is the repository's canonical check per `AGENTS.md`; no execution performed | Not run — no baseline executed in preflight (read-only tools); run at implementation |

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| Warning: tree drift — HEAD `2007ca53` ≠ plan table commit `aa94e28` | Non-blocking: V-02's exact-delta-with-cause path is the expected valid outcome; current tree is the baseline that matters | Implementer | Record the recording commit (`git rev-parse HEAD`) and per-file deltas with cause |
| Warning: folded multi-line description scalars exist (e.g., `skills/ask-user-questions/SKILL.md`) | Non-blocking: parser must normalize folded scalars; pins V-02b's representative file | Implementer | Handle both scalar shapes; spot-check a folded-scalar file in V-02b |
| Warning: no preflight commands were executed (read-only inspection only) | Non-blocking: all feasibility conclusions are inspection-based; no baseline claim is made | Implementer | Run V-01…V-07 progressively at implementation |

No blockers. Implementation stops (from the brief): record and confirm the measuring commit if the tree is dirty with unrelated changes; stop and report if a counting definition or route list cannot be derived from the plan's method or the skills' current instructions; never touch `scripts/`, skill bytes, or build a loader framework.

**Next exact action:** implement `tools/baseline_measure.py` and the baseline artifacts under the recorded scope, then run V-01 through V-07 progressively in the order above.

### Implementer handoff

- Scope: create `tools/baseline_measure.py` (stdlib only, incl. `--sum` supplied-list mode), `docs/tasks/SIDE-003/baseline.md`, one machine-readable record beside the plan. Read-only over `skills/`, `scripts/`, `tests/`.
- Ownership: tree clean at HEAD `2007ca53` before preparation; only preparation artifacts (`verification.md`, `preflight.md`) are pre-existing deltas — preserve them.
- Counting definitions: body bytes = after closing `---` incl. following whitespace; description chars = normalized scalar of `description` only. Handle plain and folded scalars.
- Oracle: plan table at `aa94e28` (26 files / 404,992 / 388,640) — match or document exact per-file delta + cause; current tree is the baseline.
- Commands: V-01 double-run + `cmp`; V-03 `--sum` per route; V-07 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`; V-06 `git status --porcelain` before/after.
- Next action: implement, then run V-01…V-07 progressively; hand completed bytes to fresh `task-review-discovery`, then separate `task-acceptance-review`.


## Focused applicability refresh — resumed implementation

Status remains `ready`; verification revision 1 and task authority are unchanged.
The user authorized resumption after updating `AGENTS.md`; preserve that user-owned
change. Recording HEAD remains `2007ca53ef92e94b76719f70ebe6e87c6baa9b6b`.
The measurement records current working-tree instruction bytes, including
`AGENTS.md` SHA-256 `c53da175135a5e451d06c2f3406c254c1bff15efda76126a462671738b497a17`.
The two preparation files are the only other pre-existing changes. No source
skill, shared script or test bytes changed. All output paths remain free.

Starting code evidence: `python3 .agents/scripts/measure_maintainability.py baseline tools --root . --output /tmp/side0031-code-before.json`
completed with exit 0 before implementation. Its original JSON/text pair covers
the existing `tools/` folder, including future Python additions, using the
installed helper and already prepared pinned environment. No setup ran. Compare
`tools/baseline_measure.py` against that original baseline before submission;
measurement remains advisory. Native duties: targeted V-01–V-06 measurement and
record checks; V-07 architecture command; repository contract check
`python3 tools/check_contracts.py --root .`. No aggregate gate at this leaf.
All scenario feasibility conclusions remain applicable. This refresh establishes
current instruction/ownership facts and starting evidence, not future correctness.
