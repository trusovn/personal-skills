# T-004.1 implementation handoff — correction round

Implemented: READY_FOR_REVIEW

- Authority: `docs/tasks/T-004.1/brief.md` (blob `0744c01b6db8ece290e7dcdc527821de7ca144a2`).
- Preparation/context: `docs/tasks/T-004.1/preflight.md`,
  `docs/tasks/T-004.1/verification.md` revision 1,
  `docs/project-plan.md` (sections 1–2, IF-004, IF-007, FLOW-004, T-004
  integration boundary, section 11), `docs/tasks/T-004/brief.md`.
- Preceding review: `docs/tasks/T-004.1/reviews/discovery-01.md` — first
  independent `task-review-discovery` report, evidence only, no verdict. One
  confirmed finding F-01 (suggested P2); ledger rows V-03 and V-08 fail, all
  other V rows pass; no blocked or unchecked rows.
- Correction evidence run: `run-20261012T160101Z-11ff08a7052a`
  (fail-first, reviewer regression, targeted checks, and all three owning
  suites recorded in its manifest). First-round run:
  `run-20261012T150815Z-86087759ea56`.
- Provenance: this session authored the corrected production and test bytes.
  They are not independently reviewed here; everything below is submission
  evidence.

## Finding and invariant

- F-01 broken invariant: unborn success requires evidence that the branch
  ref is absent. `_git_succeeded` collapsed every nonzero exit code to
  "ref absent", and `_head_commit` treated that as unborn, so a fatal
  ref lookup (`show-ref --verify` exit 128) on a committed target produced
  successful identity with `repository_commit: null` and successful
  availability with `available: true`.
- Correction: the ref lookup now keeps its exit status. Status 0 (the branch
  ref verifies as existing) re-raises the original HEAD-resolution error;
  status 1 (Git's dedicated not-found status, confirmed empirically) is the
  only path that classifies HEAD as unborn; any other status means the ref
  database could not be read and raises a `WorkflowVersionError` carrying
  the `show-ref` diagnostic. Genuine errors propagate unchanged through
  every identity/availability consumer that imports the helper.
- Credible sibling cases covered by this invariant: the single-failure
  control (rev-parse fails, `show-ref` resolves the existing branch →
  error), genuine unborn success (status 1 → unborn, preserved), and fatal
  lookup failures (any status other than 0/1 → error; 128 is the reviewer's
  representative value). `symbolic-ref` failure already re-raises (existing
  malformed-HEAD case, unchanged).
- Influenced sibling surfaces: source and copied installed identity, and
  the staged and final installer availability gates, all consume the same
  helper bytes; the installer projects the corrected
  `scripts/workflow_version.py` through its existing `SHARED_SCRIPT_FILES`
  copy, so no installer change was needed.

## Deliverables

First round (as reviewed by discovery-01): unborn-aware workflow identity
(`repository_commit: null` on a genuine unborn branch), eight unborn-boundary
test cases across the three owning modules, and affected install/identity
guidance in root `README.md` and `skills/README.md`.

Correction round (this submission):

- `scripts/workflow_version.py`: `_git_succeeded` replaced by `_git_check`
  (returns the raw completed Git result); `_head_commit` distinguishes
  confirmed-absent branch refs from failed ref lookups as described above.
- `tests/test_workflow_version.py`: two classification tests through the
  real unborn fallback path (real failed HEAD resolution and real
  `symbolic-ref`), controlling only the ref-lookup outcome — fatal status
  128 must raise, existing-ref status 0 must keep the original error.
- `tests/test_run_evidence.py`: one availability regression at the real CLI
  boundary — a committed target whose `rev-parse HEAD`/`show-ref` fail
  fatally through a PATH shim (every other Git command runs for real) must
  report `available: false` with `reason: workflow_unavailable` and exit 2,
  with the genuine controlled failure cause preserved in `error`.

Actual contract impact: ART-010's exercised identity/availability boundary
now distinguishes confirmed-absent branch refs from failed ref lookups;
unborn representation (`repository_commit: null` plus the real branch in
`repository_branch`) and all fingerprint semantics (framing, selection,
ordering, location independence) are unchanged; ART-009 shared helper bytes
changed and are projected by the installer's existing manifest. IF-007,
INV-009, FLOW-004 preserved. Executable contract declarations changed:
`scripts/workflow_version.py` (identity helper contract). No
`docs/contracts` registry exists.

## Commands and results

All run from the repository root. First-round commands (fail-first unborn
CLI record F and targeted/owning T1–T3, W 17, R 17, I 17) remain recorded in
the first-round handoff below and in the first-round evidence run; discovery
independently corroborated them.

Correction round, all recorded in `run-20261012T160101Z-11ff08a7052a`:

| ID | Exact command | Result |
|---|---|---|
| C-F | `python3 /tmp/opencode/t0041-correction-regression.py` (fail-first, kind `fail-first-f01-fatal-ref-lookup`) | exit 1 at the intended assertion: fatal-lookup mode reproduced F-01 — installed `workflow_version.py` rc 0 with `repository_commit: null`; single-failure control already rc 2 |
| C-R | same probe (reviewer regression, kind `reviewer-regression-f01-disc05`) | exit 0: both fatal-lookup CLI outcomes rc 2 (identity error; availability `available: false`, `reason: workflow_unavailable`, controlled cause in `error`); single-failure control rc 2 for both CLIs; genuine unborn target still installs canonically with null identity and final `available: true`, HEAD left unborn |
| C-TW | `python3 -m unittest discover -s tests -p test_workflow_version.py -k branch_ref` | 2 tests OK |
| C-TR | `python3 -m unittest discover -s tests -p test_run_evidence.py -k fatal_ref` | 1 test OK |
| C-W | `python3 -m unittest discover -s tests -p test_workflow_version.py` | 19 tests OK |
| C-R2 | `python3 -m unittest discover -s tests -p test_run_evidence.py` | 18 tests OK |
| C-I | `python3 -m unittest discover -s tests -p test_install_development_skills.py` | 17 tests OK |

The probe in C-R is the DISC-05 reproducer rerun with the corrected oracle
required by the report (reject both fatal-lookup CLI outcomes while
preserving the single-failure control and genuine unborn success). The
affected-module aggregate
(`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest
test_install_development_skills test_workflow_version test_run_evidence`)
remains deliberately not run by the implementer: verification revision 1 and
plan IF-004 assign it to fresh discovery once targeted rows are clean. No
whole-repo, network, or model-budget gate exists for this task.

## Scenario and finite-risk evidence

Implementation checks, not independent acceptance evidence. Prior discovery
dispositions are navigation context for the corrected bytes; V-03 and V-08
stay failed rows until fresh discovery reconciles them.

| Scenario | Correction evidence | Prior discovery status |
|---|---|---|
| V-01 | Unchanged behavior preserved: unborn cases in W/R/I suites green (C-W/C-R2/C-I); C-R asserts canonical unborn install, null identity, final `available: true`, no commit created | pass |
| V-02 | Unchanged behavior preserved: attached/detached identity cases green; C-R single-failure control keeps a committed target's failed HEAD resolution an error, never unborn | pass |
| V-03 | Corrected: new W classification tests (fatal status 128 raises; existing-ref status 0 re-raises the original error), new R fatal-ref-lookup availability regression (rc 2, `available: false`, `workflow_unavailable`, cause preserved), C-F fail-first reproduced the defect, C-R reruns the reviewer reproducer clean | **fail (F-01)** — correction evidence attached |
| V-04 | No fingerprint code touched; all W framing/selection/ordering cases green; fingerprint algorithm bytes unchanged | pass |
| V-05 | No selection/layout code touched; W copied-layout cases green; I byte-projection cases carry the corrected helper bytes automatically | pass |
| V-06 | No transition logic touched; W transition case green (unborn → first → later commit identities, stable fingerprint) | pass |
| V-07 | Installer manifest/ownership untouched; I projection/preservation cases green, including shared-script byte comparison against the corrected helper | pass |
| V-08 | Corrected behavior now satisfies the documented guarantee (root `README.md`: an actual Git failure remains a reported error and is never reported as a missing first commit); no guidance text change was needed — discovery confirmed the remaining unborn-scope and collector-exclusion wording accurate — and the guarantee is now pinned by the new W/R regression tests | **fail (F-01)** — correction evidence attached |

Risk coverage: R-01 / INV-009 → V-01, V-02, V-03; R-02 / INV-009 → V-04,
V-05, V-06. Every ledger row is accounted for; none omitted.

Interface notes for .2/.3 are unchanged: `workflow_version.py <id>` (and
`get_workflow_version`) report unborn as `repository_commit: null` with the
real branch in `repository_branch`; `run_evidence.py --repo <target>
availability` reports `available: true` on a genuine unborn target; the
canonical installer accepts unborn targets. Gap: the run-evidence collector's
`begin`/`finish`/`recover` lifecycle still requires a resolved HEAD and is
not unborn-qualified (out of scope; documented in the root README).

## Scope and next owners

Changed paths across both rounds (all task-authorized):
`scripts/workflow_version.py`, `tests/test_workflow_version.py`,
`tests/test_run_evidence.py`, `tests/test_install_development_skills.py`,
root `README.md`, `skills/README.md`. The correction touched only the first
three; `scripts/run_evidence.py` and
`scripts/install_development_skills.py` still needed no changes. Plans,
index, `.agents/`, historical evidence and `reviews/discovery-01.md` were
not modified.

Skipped: the discovery-owned affected-module aggregate (see above);
profile checker (.2), refresh composition (.3), and unborn collector
lifecycle qualification (out of scope). The brief's soft budget was already
exceeded in the first round; the correction stayed bounded and closed
safely.

Next: fresh independent `task-review-discovery` call on the corrected staged
bytes — it must corroborate the corrected bytes, rerun the DISC-05 reviewer
regression with an oracle requiring both fatal-lookup outcomes to fail,
check the influenced identity/availability surfaces, reconcile all V rows,
and own the justified affected-module aggregate — then its report to a
separate fresh `task-acceptance-review` decision. No repository policy
requires a conditional architecture or maintainability gate for these bytes,
and no contract registry exists to synchronize. No conditional stage is
outstanding ahead of discovery. End the implementer invocation here; no
self-acceptance, reviewer launch, or advancement.

## First-round submission record (superseded by the correction above)

Implemented: READY_FOR_REVIEW (original bytes as reviewed by discovery-01).

Authority: `docs/tasks/T-004.1/brief.md`; preparation: `preflight.md`,
`verification.md` revision 1; context: `docs/project-plan.md` (sections 1–2,
IF-007, FLOW-004, T-004 integration boundary, section 11),
`docs/tasks/T-004/brief.md`. Guided invocation at HEAD `9712879` with only
`.DS_Store` noise untracked. Evidence run
`run-20261012T150815Z-86087759ea56` (begin/finish facts, fail-first check,
owning-module checks).

Deliverables: unborn-aware workflow identity in `scripts/workflow_version.py`
(`_git_succeeded` helper and `_head_commit()`; `repository_commit` is `null`
when HEAD names a branch with no commits yet); eight unborn-boundary test
cases across the three owning modules (the `init_repo` installer fixture
gained a `commit=True` parameter; workflow-version tests gained a shared
`write_skill_fixture` helper); affected guidance in root `README.md` and
`skills/README.md` stating the exercised unborn boundary without claiming
collector lifecycle support.

| ID | Exact command | Final result |
|---|---|---|
| F | `python3 scripts/install_development_skills.py <unborn-target>` (fail-first) | exit 2: `staged run-evidence availability failed`, `reason: workflow_unavailable` — the HEAD/availability defect on a properly supplied unborn target |
| T1 | `python3 -m unittest discover -s tests -p test_workflow_version.py -k Unborn` | 4 tests OK |
| T2 | `python3 -m unittest discover -s tests -p test_run_evidence.py -k unborn -k invalid_git_target` | 2 tests OK |
| T3 | `python3 -m unittest discover -s tests -p test_install_development_skills.py -k unborn -k invalid_git_target` | 2 tests OK |
| W | `python3 -m unittest discover -s tests -p test_workflow_version.py` | 17 tests OK |
| R | `python3 -m unittest discover -s tests -p test_run_evidence.py` | 17 tests OK |
| I | `python3 -m unittest discover -s tests -p test_install_development_skills.py` | 17 tests OK |

The first round claimed all V rows pass; discovery-01 contradicted V-03 and
V-08 (F-01) and independently corroborated the rest. Those claims are
superseded by this correction round's evidence.