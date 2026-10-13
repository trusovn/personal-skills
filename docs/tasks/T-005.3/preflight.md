# Task Preflight: `T-005.3` — Exercise independent contextual review decisions

Status: `ready`

Created at: 2026-10-13T15:41:30Z

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | `docs/tasks/T-005.3/brief.md`, Status `ready`, Task kind `executable` (index.json: executable leaf, depends_on `T-005.1` — completed). Authority: `docs/project-plan.md` sections 6–8, 10–11; `docs/tasks/T-005/brief.md` evidence rules 1–7 and P-03/P-04. |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Dependencies / entry criteria | T-005.1 inventory/receipts present and read-only (`fixtures.md`, `results.md`, `evidence/` receipts); all four named test owners current-green (see commands); contextual/mixed/uncertainty fixture scenario commands exist in source `setup_fixture.py` registries; role-call interface confirmed by coordinator this session. |
| Allowed scope | `docs/tasks/T-005.3/results.md`, `evidence/`, missing case-local input adapters, disposable fixture changes within supplied correction authority. Read-only: T-005.1 inventory/receipts, COMP-01/02/05, existing discovery/acceptance fixture/eval families and contextual test owners, inherited public queue/exporter, index/worktree, ledger/workflow, process-cleanup and continuation cases. Excluded: source-policy fixes, role runner, reviewer tracker writes, portfolio decisions, active installation refresh, old reports/master plans. |
| User-work ownership | Clean for the task area. Pre-existing untracked user-owned `.DS_Store`, `docs/.DS_Store`, `skills/.DS_Store` are preserved untouched. `docs/tasks/T-005.3/verification.md` is this package's own uncommitted preparation work (revision 1). No ownership overlap or multi-writer signal. |
| Permission limits | Local disposable workspaces under `/tmp/opencode` only; no network, dependency installation, commit/push, live gate, or full-suite run. The only model-budget role calls are the two coordinator-launched fresh discovery/acceptance sessions over the implementer's finished submission. |
| Profile | `guided` (brief routes: "Standalone guided preflight after derived verification"). |
| Standalone preflight value | `material` — resolved the brief's declared UNKNOWN (role-call authorization/interface), current installation qualification, held-back oracle input supply, and the concrete approved call budget. |
| Source brief / revision | `docs/tasks/T-005.3/brief.md`, SHA-256 `0f577d56b18fe48368d6b096a6ef625ca5b64c54e7a4c5db46037fb1d0169fe0` (matches verification's declared `Source brief revision`). |
| Verification / Verification revision | `docs/tasks/T-005.3/verification.md` revision 1, SHA-256 `2f30d900abb09d337d273dfed738e69fd8205a556551279969510be72ec06190`. `Source brief:` declaration resolves to this package's brief. Scenarios V-01–V-09 map to AC-01–AC-05 and D-01–D-04 (coverage table complete; every AC has at least one scenario). |
| Current applicability | HEAD `f105a7b2755e005d1cf1131c4d325cf83e6ac2c2`; no tracked modifications; untracked set = 3 user `.DS_Store` files + this package's `verification.md`; `git diff --check` clean. No known-issues/tracker file exists → no recorded deferrals. Role-call authorization confirmed by the coordinator during this preflight, so the UNKNOWN in the brief is resolved. |

## Decision context

- Direction: FLOW-002/003/005; IF-004/005/006/008; INV-001/004/005/006/007/010/011.
  Consumes ART-001–006; produces ART-006/007 observations for ART-012 and a real
  bounded-deferral decision (or its explicit unrun gap) for T-005.4. Plan
  section 6 contextual rubric / mixed precedence governs verdicts.
- Intended use and envelope: implementer bounded to 22 tool calls / 65 minutes /
  60k context (policy `default@1`, `decomposition_override: cannot_split_safely`).
  Implementer ends its invocation after submission; the coordinator then launches
  a fresh `task-review-discovery` session (project-local installed skill), then a
  separate fresh `task-acceptance-review` session consuming the raw report —
  same interface as T-005.2 (`reviews/discovery-01.md` → `reviews/acceptance-01.md`).
  Discovery supplies evidence only; acceptance admits it; implementer authors
  remain `SELF_CHECK_ONLY`.
- Failure consequences: unrun role boundaries keep behavioral qualification
  incomplete and feed only an explicit gap to T-005.4; a staged or fabricated
  deferral must never seed a real known-issue record (V-09). Wrong-green or
  weak/stale proof cannot advance (AC-02); material exposure found only in
  preflight context still blocks despite green tests (AC-03).
- Required consumers: T-005.4 (raw accepted deferral decision or explicit unrun
  gap), T-005.5, T-005.6 audit. Reviewers write no tracker/known-issues record.
- Credible changes: none known. Active-installation refresh is excluded from
  this task's scope; see Warning 1.
- Assumptions recorded as ordinary: staged Git identities change per staging
  run and must be re-recorded; optional context links may be absent (V-05) and
  do not affect eligibility; timezone/consumer-tolerance facts resolve locally
  per the fixtures' own contracts.

## Acceptance evidence and commands

| AC / scenario / risk | Authority relationship | Setup / decisive boundary / oracle | Exact command / cwd | Feasibility: dependencies / permissions / ownership | Baseline result / gap |
|---|---|---|---|---|---|
| AC-01; V-01, V-02, V-09; D-01 / INV-004/005 | Brief AC-01; parent evidence rule 3; P-03 | Actual separate fresh discovery report bytes and identities fed to a separate acceptance call; raw outputs preserved before grading; evaluator answers held outside reviewer inputs (`fixtures.md` held-back contract) | Coordinator-launched fresh sessions: `task-review-discovery` → `docs/tasks/T-005.3/reviews/discovery-01.md`, then `task-acceptance-review` → `reviews/acceptance-01.md` (T-005.2 precedent) | Confirmed: coordinator authorizes/launches both calls (resolved this session). Interface = project-local `.agents/skills/task-implementation-flow/` installed skills | Not run: post-implementation role calls. Readiness claims no future pass |
| AC-02; V-02, V-03, V-08; D-01 / INV-004/005 | Brief AC-02; parent rules 1, 6; T-005.1 inventory | Wrong-green vs clean contrasts; public queue/exporter, index/worktree, validator exit codes, process cleanup, continuation cases retain decisive boundaries | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_review_discovery.py` (cwd repo root) | Green: 17 tests OK (run today). Fixture scenarios (`queue-defect`, `exporter-accept`, `process-cleanup-defects`, `ledger-defects`, `workflow-matrix-defects`) exist in discovery `setup_fixture.py` registry | Passed now; renew affected probes before any justified aggregate |
| AC-02 continuation; V-02, V-03 | Brief AC-02 | Acceptance-side retained rows and verdict routes | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_acceptance_review.py` (cwd repo root) | Green: 25 tests OK (run today) | Passed now |
| AC-03; V-04, V-05, V-08; D-02 / INV-006/011 | Brief AC-03; plan section 6 rubric; P-03 | Material operating/business/refactoring exposure blocks despite green tests; mitigated debt defers; preferences stay observations; preflight-only fact traced into actual probe | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_contextual_export_risks.py` (cwd repo root); staging: `EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py contextual-risk-blockers-decision` and `contextual-risk-mitigated-decision` | Green: 6 tests OK (run today). Both scenario commands exist in the acceptance fixture registry | Passed now; actual role-call evidence is the decisive oracle |
| AC-04; V-02, V-05, V-06; D-03 / INV-011 | Brief AC-04; INV-011 | Ordinary uncertainty continues under assumptions; serious unresolved facts escalate through the coordinator only when current authority fails; missing proof routes to its evidence owner | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_contextual_uncertainty_inputs.py` (cwd repo root); scenarios `consequential-uncertainty-decision`, `serious-delay-uncertainty-decision`, `-resolved` variants | Green: 5 tests OK (run today). Scenario commands exist in the acceptance fixture registry | Passed now |
| AC-05; V-05, V-07, V-09; D-04 / INV-005/006/008 | Brief AC-05; parent rules 3, 5; P-03/P-04 | Confirmed eligible blocker F-01 + JOB-PAIR blocked/unchecked proof: authorized correction → `CHANGES_REQUESTED`, prevented → `INCONCLUSIVE`; both preserve all IDs/rows/reasons; neither advances; raw deferral or explicit unrun gap feeds T-005.4 | Scenarios `mixed-conditions-authorized-decision`, `mixed-conditions-forbidden-decision` (staged `local-review-mixed.json` run policies) | Scenario commands and policy files exist in the acceptance fixture registry | Not run: role-call evidence post-implementation |

Notes: sequential owner-module runs were the named targeted command
(`-p <owner>` per the brief's Verification section); no full suite was run.
Discovery owns any justified aggregate; acceptance consumes it without rerun
(parent rule 7). Staging runs from repo root with `PYTHONDONTWRITEBYTECODE=1`
and disposable `EVAL_WORK_ROOT`; staged identities must be re-recorded per run.

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| None (blockers) | — | — | — |
| Warning 1: active `.agents/` installation has 2-path drift vs canonical source (`python3 scripts/install_development_skills.py --check .` → `match=false`, compared 86: `.agents/scripts/workflow_version.py` missing later-added unborn-HEAD handling; `.agents/skills/README.md` docs-only additions; both source changes postdate the installation) | Non-blocking here: the two role skills and all other managed files byte-match source; the drift covers only unborn-HEAD repositories, which this leaf's staged contexts do not use; active-installation refresh is excluded from scope; T-005.1's disposable-projection receipts (C2, `match=True` over current source) remain the qualification basis | Coordinator / installer maintenance (outside this task) | Implementer must not claim the active installation is fully byte-qualified; record the 2-path drift in results; re-run `--check` before role calls and route any NEW drift to fresh preflight |
| Warning 2: staged fixture Git identities change on every staging | Receipts from one run do not identify the next | Implementer | Re-record fresh HEAD/dirty state per staging run |
| Warning 3: user-owned untracked `.DS_Store` files (root, `docs/`, `skills/`) | Preserved; not task evidence | User / implementer | Leave untouched |

For `ready`: implementation stops — no source/skill/test/installer/plan edits
beyond task-local adapters and authorized disposable corrections; no reviewer
tracker writes; no installation refresh; no network, commit, push, live gate,
or full-suite run; checkpoint at the soft budget (22 calls / 65 min / 60k
context) with explicit unfinished cases. Next exact action: launch
`bounded-task-implementer` for T-005.3 using this package; after submission the
implementer invocation ends and the coordinator launches the fresh separate
discovery then acceptance sessions (confirmed).

## Implementer handoff

- Brief: `docs/tasks/T-005.3/brief.md` (SHA-256 `0f577d56…9fe0`); verification
  revision 1 (SHA-256 `2f30d900…6190`); this `preflight.md`.
- Scope: only `docs/tasks/T-005.3/results.md`, `evidence/`, missing case-local
  input adapters, disposable fixture corrections within supplied authority.
  Preserve T-005.1 inventory/receipts, COMP-01/02/05, existing fixture/eval
  families, inherited public/lifecycle/validator/tamper/process/continuation
  cases and the three user `.DS_Store` files.
- Commands: run the four named owners sequentially first
  (`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <owner>`:
  `test_task_review_discovery.py`, `test_task_acceptance_review.py`,
  `test_contextual_export_risks.py`, `test_contextual_uncertainty_inputs.py`);
  stage each contrast via
  `EVAL_WORK_ROOT=/tmp/opencode/t0053/<case> python3 skills/task-implementation-flow/task-<skill>/evals/files/setup_fixture.py <scenario>`
  and record fresh identities per run; `git diff --check` before finishing.
- Role calls: do NOT self-launch. End the implementer invocation after the
  submission; the coordinator launches fresh `task-review-discovery`, then
  separate `task-acceptance-review`, over the completed bytes
  (`reviews/discovery-01.md` → `reviews/acceptance-01.md`). If a call cannot
  happen, record an explicit unrun gap with owner — never a staged pass.
- Record the active-installation 2-path drift (Warning 1) in results; claim no
  byte-qualification of the active `.agents/` installation.
- Output: `results.md` distinguishing observed role outputs, structural test
  results, and unrun boundaries; raw discovery output preserved before grading;
  the actual accepted deferral decision (or explicit unrun gap) retained for
  T-005.4.
