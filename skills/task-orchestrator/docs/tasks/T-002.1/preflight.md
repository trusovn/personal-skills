# Task Preflight: T-002.1 — Freeze the approved one-task policy

Status: `ready`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | Packaged leaf T-002.1 of decomposed composite T-002; brief revision 1, status `ready`, kind `executable`; verification revision 1 with `Source brief: brief.md` resolving to this package. Authority: parent P-01/P-05/P-06, approved plan + r2 review, owner-confirmed direction. |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills` (HEAD `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`) |
| Dependencies / entry criteria | Confirmed. T-001 historical evidence present and preserved: `harness-contract.md`, `capability-follow-up.md`, `reviews/discovery-03.md`, `reviews/acceptance-02.md`. Parent reconciled T-001 under the revised direction; obsolete isolation/commit gates are not entry gates. T-002.2/T-002.3 depend on this leaf, not vice versa. |
| Allowed scope | `skills/task-orchestrator/scripts/controller_state.py`, `scripts/controller.py` (relative to `skills/task-orchestrator/`), affected `assets/` schemas/examples, their existing focused tests, this package's implementation report/contract note. |
| User-work ownership | Tracked tree clean. Only untracked items: planning packages `docs/tasks/T-002*` + `index.json` (pre-existing planning work, preserve as-is) and `.DS_Store` noise. No overlap with implementation paths. |
| Permission limits | Local unittest only; no live model/network/sbx pilot; no commits; preserve old runs and active installations; installer untouched; `verification_runner.py` and `codex_worker.py` out of scope. |
| Profile | `guided` |
| Standalone preflight value | `material`. Resolved: (1) authority freshness — plan SHA-256 `9e32bc96…4a811e2` and task-map SHA-256 `a669e740…aed7b9082` exactly match the parent's preparation-time records; (2) T-001 evidence presence; (3) ownership/fixture reuse — clean implementation area, temp-dir run fixtures and immutable run storage confirmed; (4) a fact the brief did not name: `test_controller.py` baseline on this Linux host carries 6 pre-existing failures/errors from macOS-only `sandbox-exec` paths — costly to discover during implementation, and it defines the honest oracle for the targeted command. |
| Source brief / revision | `skills/task-orchestrator/docs/tasks/T-002.1/brief.md`, revision 1 |
| Verification / Verification revision | `skills/task-orchestrator/docs/tasks/T-002.1/verification.md`, revision 1; scenarios V-01..V-05 cover AC-01..AC-04 and R1/R2 completely |
| Current applicability | No `preflight.md` existed (planning stated; directory listing confirms). No material authority change since preparation (digests match). No contract registry exists under `docs/contracts` or `skills/task-orchestrator/docs/contracts` — brief's claim is current; publish the package contract note, do not invent a registry. |

## Decision context

- This leaf materializes frozen ART-001 and the required stage/role declarations consumed by T-002.2 via IF-001; T-003 later applies the resolved policy at launch. Failure consequence: silent adoption of source-input edits or silent old-run migration would corrupt task authority for the whole one-task sbx loop — refusals must be exact and non-destructive.
- Owner decision (parent brief, 2026-10-23): environment repair consumes the shared three-correction budget (resolves F-001 for this task and successors). AC-03 must encode limit 3 including repair; preflight/evidence-only retries consume none.
- Premise confirmed against current code: `ACTOR_LEVELS` still maps `gpt-5.6-sol` low/medium/high; `FLOW_STEP_ORDER` is the 5-step `preflight/implement/verify/semantic_review/accept` flow with merged `semantic_reviewer` role and correction limit 2; `IMPLEMENTATION_SESSION_REUSE_THRESHOLD = 0.5` already exists. The approved `gpt-6.1-sol` mapping, 8-stage required sequence with separate collection/acceptance roles and controller-owned completion gate, and fresh-session rule for unknown occupancy are genuine deltas in allowed paths.
- Reuse confirmed: flow/cursor validation, immutable policy storage (`persist_run_policy`, `xb` exclusive writes, digests), run initialization (`init_run`), ledger validation, `assets/*.schema.json` + `assets/examples/*` all present. Existing coverage lives in `test_controller_state.py` (41 tests) and `test_controller.py` (72 tests, 6 environment failures).
- Known issues: no recorded-deferrals file; T-001 capability follow-up records historical transport limits that stay preserved, not gating. The macOS-only sandbox failures are a current environment fact, not a task blocker (see warnings).
- Ordinary assumptions (no owner question needed): exact stage names/layout remain delegated to the implementer per AC-02; `controller-contract.md` will be created in this package during implementation (explicitly allowed scope).

## Acceptance evidence and commands

| AC / scenario / risk | Authority relationship | Setup / decisive boundary / oracle | Exact command / cwd | Feasibility: dependencies / permissions / ownership | Baseline result / gap |
|---|---|---|---|---|---|
| V-01 — AC-01, AC-03, R2 | Brief AC-01; parent P-01; plan ART-001 | Disposable repo/run: real brief/verification/policy files, init a run, edit each source input, reopen; oracle = real initialization/loading plus before/after bytes of input/run files, original frozen records preserved. Rejected old permissive behavior demonstrated where feasible. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` (repo root), then the controller test file | Feasible: `tempfile.TemporaryDirectory()` fixture patterns already in both test files; `init_run` persists policy/flow/manifest immutably outside the repo. No network/model needed. | Baseline ran: 41 tests OK (0.03s). New focused cases are the intended fail-first work; not run yet. |
| V-02 — AC-02, R1 | Brief AC-02; parent P-01/P-05; plan INV-004/IF-003 | Runtime validator + public init: each required stage removed, roles merged, stages reordered, actor result presented as completion; refuse without adopting. Weak/optional profile rejected. Schema checks supplement. | Same targeted commands as V-01 | Feasible: `validate_flow_profile`/constants in `controller_state.py` are the change site; current optional-profile/merged-role behavior is exactly the delta to reject. | Baseline green pre-change; new cases not run yet (fail-first intended). |
| V-03 — AC-03, R2 | Brief AC-03; owner decision in parent (F-001); direction doc | Policy resolution across low/medium/high, known/unknown occupancy, 0.5 boundary, terminal-totals-only; wrong model/effort/limit/missing authorization fail validation. Persisted policy checked against schemas/current examples. | Same targeted commands; plus JSON/schema structure checks for `assets/` | Feasible: mapping/threshold constants exist; `run-policy.schema.json`/`flow-profile.schema.json` + examples (`reviewed-flow.json`, `fast-local-flow.json`, `strong-local-flow.json`, `minimal-run-policy.json`) in scope to synchronize. Does not prove adapter launch (T-003). | Baseline green; new cases not run yet. |
| V-04 — AC-04, R2 | Brief AC-04; plan T-002 section ("preserve already frozen runs; refuse incompatible old-run continuation with a clear next action instead of silently migrating it") | Real old-format/model/profile run fixture bytes; request continuation through an applicable public controller path; oracle = controller response + byte comparison of persisted fixture files. Refusal must occur before continuation/mutation; no actor launch needed. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` (repo root) | Feasible on Linux: old-run fixture bytes writable from the current pre-change run layout (`run-policy.json`, `flows/flow-001.json`, `task-manifest.json`, `baselines/`); refusal at load/compatibility boundary happens before verification execution, so the macOS-only sandbox limitation does not apply. | Baseline ran: 72 tests, 66 pass, 6 pre-existing failures/errors — all `UnsupportedSandbox: sandbox-exec verification is supported only on macOS` in `ControllerInspectionIntegrationTest`. Treat those 6 as the environmental baseline; this task must add no failures and must not "fix" them (`verification_runner.py` out of scope). New cases not run yet. |
| V-05 — AC-04 | Brief AC-04 | Compare published `controller-contract.md` field/role/version/compatibility examples with actual declarations and focused behavioral results; explicit missing runtime stages and supported commands; no sbx/install-refresh claims. | Source/declaration review plus the targeted commands above | Feasible: contract note in this package is allowed scope; document check supplements, never replaces, V-01..V-04. | Not applicable pre-implementation; created during implementation. |

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| Warning: 6 pre-existing failures/errors in `test_controller.py` on this Linux host, all from macOS-only `sandbox-exec` paths in `ControllerInspectionIntegrationTest` | Non-blocking. The targeted command's aggregate signal is contaminated; the implementer must compare results against the recorded baseline (66 pass / 6 environmental failures) rather than expecting a fully green file, and must not modify `verification_runner.py` to mask them. | Implementer | Run the targeted commands; treat the 6 as environmental constants; add no new failures. |
| Warning: planning packages (`docs/tasks/T-002*`, `index.json`) are untracked pre-existing work | Non-blocking. Preserve without edits/commits; the only new artifact in this package besides the report/contract note is this `preflight.md`. | Implementer | Leave untouched. |
| None other — no blockers | Implementation can begin under the recorded scope and policy. | — | — |

Implementation stops (per brief): reservation behavior (T-002.2), input revision (T-002.3), `codex_worker.py` launch behavior, evidence admission, actual sbx checks, official plan/review edits, installation changes, and any `verification_runner.py` change for the environmental failures.

Next action: begin implementation with the owning method selected by the implementer, then run both targeted commands from the brief; immediately after implementation/correction and any applicable architecture/maintainability/registry stages, obtain fresh `task-review-discovery` evidence and a separate `task-acceptance-review` decision; hand the implemented contract and review references to T-002.2 only after acceptance.

---

## Implementer handoff

```text
Task: T-002.1 — freeze approved one-task policy (brief rev 1, verification rev 1). Status: READY.
Repo: /Users/mtrusov/work/skill-sources/personal-skills (HEAD 4449a3f, tracked tree clean).
Scope (only): skills/task-orchestrator/scripts/controller_state.py, skills/task-orchestrator/scripts/controller.py,
  affected skills/task-orchestrator/assets/ schemas+examples, their existing focused tests
  (tests/test_controller_state.py, tests/test_controller.py), this package's report + controller-contract.md.
Confirmed current-state deltas to build: ACTOR_LEVELS is gpt-5.6-sol (make gpt-6.1-sol low/medium/high);
  FLOW_STEP_ORDER has 5 steps with merged semantic_reviewer role and correction limit 2 (make 8 required
  stages: ready/preflight/implementation/checks/collection/acceptance/completion-gate/completed + bounded
  correction, separate collection and acceptance roles, controller-owned completion gate, shared limit 3
  including environment repair); IMPLEMENTATION_SESSION_REUSE_THRESHOLD = 0.5 already exists (reuse it).
  Old runs: preserve bytes; refuse incompatible continuation before mutation with a new-run next action.
Baseline (ran, local, authorized):
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
    -> 41 tests OK.
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
    -> 72 tests: 66 pass, 6 pre-existing failures/errors, ALL caused by
       "UnsupportedSandbox: sandbox-exec verification is supported only on macOS"
       (ControllerInspectionIntegrationTest). Environment condition, not your regression and NOT yours to
       fix: verification_runner.py is out of scope. Your work must add zero new failures and keep the 6
       unchanged.
Commands (cwd = repo root): the two above, targeted-first; full local orchestrator suite only if blast
  radius requires it. No live model/network/sbx; no commits; preserve untracked planning packages.
Stops: T-002.2 reservation, T-002.3 revision, codex_worker.py launch, evidence admission, actual sbx
  checks, plan/review doc edits, installation changes.
Next: implement per brief "Verification and readiness"; after implementation/correction + any applicable
  architecture/maintainability/registry stages, fresh task-review-discovery then separate
  task-acceptance-review; hand contract + review references to T-002.2 only after acceptance.
```