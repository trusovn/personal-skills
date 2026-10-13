# T-005.2 unrun role boundaries and evidence-record discipline

Covers AC-04 / V-07. Every claim in this package's evidence separates:

- **observed** — raw local staging/probe results from this invocation
  (`run-log.md`, `preparation-and-recovery-observations.md`): commands,
  exit codes, Git identities (HEAD + dirty state per root), the retained
  freshness-probe values, and regenerable staged control bytes (the
  claimed capture was not retained — discovery-01 F-01). Raw observation
  preceded grading;
  no staged readiness, expected fixture verdict, structural check or
  planned route is presented as an observed role output.
- **structural** — current green owner-test modules over the fixture
  oracles (renewed green at completion; see `results.md`).
- **unrun** — role-call boundaries below; observations use
  pass/fail/blocked/unchecked separately from expected fixture verdicts.

## Evidence-run and identity record

- Sidecar: `scripts/run_evidence.py` (installation root = this repository;
  availability probe `available: true` with workflow fingerprint
  `sha256:a11a7689…` recorded as workflow-identity evidence only). No prior
  open run existed (`active: null`); one run
  `run-20261013T143605Z-d20d1908061f` was begun at entry with
  `--task-id T-005.2 --task-brief docs/tasks/T-005.2/brief.md` and finished
  with outcome `completed` at the end of the invocation (manifest under the
  Git-metadata evidence storage; nothing written into the worktree).
- Starting/ending repository state, consumed preparation references
  (brief/verification/preflight SHA-256s, verification revision 1) and all
  staging identities are recorded in `run-log.md`. The three pre-existing
  untracked user-owned `.DS_Store` files (root, `docs/`, `skills/`) were not
  touched; no active `.agents/` installation, source skill, installer
  declaration, protected history or `docs/tasks/index.json` byte changed.
- Permissions: local disposable workspaces under `/tmp/opencode/t0052` only;
  no network, model-budget, live eval, dependency installation, commit or
  push was performed or is claimed. Disposable workspaces and raw capture
  directories were removed; the receipts retained the staging identities and
  probe values but **not** the staged control bytes (discovery-01 F-01;
  correction recorded in `evidence/correction-discovery-01.md`).

## Unrun role-call ledger (reproducible setup retained for each)

| # | Unrun boundary | Reproducible setup (from repo root) | Reason not run | Next owner |
|---|---|---|---|---|
| 1 | Actual `task-verification-designer` + `task-preflight` calls over the staged QR-12 package inputs (the T-005.1 handoff-manifest placeholder replacement; staged `docs/tasks/QR-12/preflight.md` is supplied history until replaced by raw actual output) | `EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py queue-defect` (current identities: `run-log.md`) | The coordinator launched only this package's designer→preflight→implementer chain; no further role-call authorization exists (parent rule 4; brief UNKNOWN fallback: setup + explicit unrun records) | Coordinator to launch; T-005.2 role calls |
| 2 | Actual `task-verification-designer` call over the INT-9 integration leaf (IFQ-02 / I-05) | `EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py integration-leaf` | same | Coordinator |
| 3 | Actual designer coverage-revision call over REV-1 (coverage gap with unchanged authority) | `EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py coverage-revision` | same | Coordinator |
| 4 | Actual focused `task-preflight` for verification revision 2, then the current revised-proof implementer submission, then the separate new acceptance decision (FEASIBLE/UNAVAILABLE; INV-CASE-23 / CCR-07 / REV-01) | `EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py revision-recovery` | same | Coordinator; decision owner: separate fresh `task-acceptance-review` |
| 5 | Actual preflight/implementer refusal behavior over the readiness-cases, preparation-routes, verification-conflicts, coverage-closure and entry-cases controls | staging commands per `run-log.md` | same | Coordinator |
| 6 | Actual discovery-side prepared/direct-route role calls (COMP-05 staged inputs; INT-FLOW-001 I-04 preparation-reference handoff parity is supplied to T-005.3 via IFQ-03) | `EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py discovery-prepared-ledger`; `… authored-production-self-check` | same | Coordinator (T-005.3 consumes the IFQ-03 parity inputs) |
| 7 | Any live/network/model-budget eval or new role-call campaign | — | Prohibited by parent evidence rule 4 without concrete case/method/cost/permission authorization | Coordinator authorization required |

Every unrun required boundary keeps behavioral qualification incomplete;
local structural/runtime results and staged input history remain
distinguishable from actual role compliance, and no unrun call is relabeled
green anywhere in this package's evidence.

## Protected state (before/after)

- Before: HEAD `9127e59`, dirty set = three untracked `.DS_Store` user files
  only; `git diff --check` clean.
- After: same pre-existing bytes untouched; this task added only
  `docs/tasks/T-005.2/results.md` and `docs/tasks/T-005.2/evidence/`
  (allowed paths). Completion checks: `results.md`.
- Carried warning (from T-005.1 acceptance-01 §8 and this package's
  preflight): dependency acceptance dispositions for T-001.4, T-002.4,
  T-003.4, T-004.1–.3, INT-FLOW-001, TEST-STAB-001.1/.2 remain owed to the
  coordinator + per-package fresh `task-acceptance-review` calls before
  T-005.6's ART-012 audit; commit-message "(accepted)" labels are not
  decision artifacts.