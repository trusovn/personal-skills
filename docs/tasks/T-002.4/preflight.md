# Preflight: T-002.4 — Close review-flow guidance and local composition

Status: `ready`
Profile: standalone guided
Brief: `docs/tasks/T-002.4/brief.md` (SHA-256 `8593563b…25240`)
Verification design: `docs/tasks/T-002.4/verification.md`, revision 1
  (SHA-256 `d12ab546…96942`; `Source brief:` resolves to the package brief;
  recorded source-brief digest `8593563b…25240` matches current brief bytes)

## Standalone preflight value

`standalone_preflight_value: material`

The brief's named uncertainties — completed/reviewed .1–.3 interfaces, the
existing installer fixture, and exact local selectors — are now resolved:

- .1–.3 are completed and accepted: `4a4b771 "T-002.1 done (accepted)"`,
  `2a71e4c "task T-002.2 done (accepted)"`, `6f7b8b9 "T-002.3 task done
  (accepted)"` (HEAD). T-002.3's correction results are committed; the tracked
  tree is clean. Settled child contracts are in the source tree under
  `skills/task-implementation-flow/` (task-review-discovery, task-acceptance-review,
  task-preflight consumer wording).
- Installer fixture exists and is real-behavior: disposable committed-target
  install/rerun/unmanaged-preservation tests at
  `tests/test_install_development_skills.py:287,360,413`, including .1's
  discovery-projection test. Installer constants
  (`DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`)
  present in `scripts/install_development_skills.py:23,46,48`.
- Exact selectors: root `README.md`, `skills/README.md` (profile guide),
  `skills/task-implementation-flow/README.md` (flow README), affected child-skill
  handoffs/layout references, `tests/test_review_discipline.py`,
  `tests/test_install_development_skills.py`, task-local fixture/results under
  `docs/tasks/T-002.4/`.
- A further material fact surfaced: `.agents/skills/task-implementation-flow/`
  is stale versus `skills/` source — 12 files differ or are absent (e.g.
  acceptance-report-template.md lacks the .2 admitted-ledger bytes). Active
  installation stays read-only for this task; the disposable committed-target
  fixture is the only valid AC-03 oracle (see Warnings).

Residual facts are routine; no further standalone preflight is needed.

## Scope and ownership

- Confirmed scope: cross-stage root README, `skills/README.md`, flow README;
  minimal functional-review stage-name/reference substitutions in affected
  source skill handoffs/layout references where omission contradicts .1/.2;
  focused tests in `tests/test_review_discipline.py` and
  `tests/test_install_development_skills.py`; task-owned eval/fixture
  composition and results in `docs/tasks/T-002.4/`.
- Ownership clean: no tracked modifications at preflight. Untracked:
  `.DS_Store` files (root/docs/skills, user junk — do not touch) and
  `docs/tasks/T-002.4/verification.md` (pipeline input — keep, do not rewrite).
  No user work overlaps the edit area.
- Read-only: settled child semantics, plans and historical reviews, active
  `.agents/` installation. Inspect installer constants only if predecessors
  require synchronization; no new selected skill or shared helper expected.
- Dependency: T-002.4 leaf `executable`, depends on accepted T-002.1/.2/.3
  (`docs/tasks/index.json`).

## Command and oracle

Targeted owning gates (from repository root, sequentially, after targeted
evidence is clean — per the brief, these are the implementer's gates, not
preflight's):

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

- Ran both at preflight as a cheap environment baseline: OK — 54 tests (1.77s)
  and 13 tests (0.74s). This is behavioral evidence that the current suite and
  environment are healthy, not evidence for any T-002.4 outcome: the fail-first
  composition/projection assertions do not exist yet and must be added and made
  to fail first by the implementer.
- Oracle: verification.md scenarios V-01–V-09 map every AC-01–05 and C-01–03
  row to contract/fixture assertions:
  - V-01/V-02 → structural route/role-agreement assertions in
    `tests/test_review_discipline.py` over source/guide bytes.
  - V-03 → real installer behavior via the disposable committed-target fixture
    in `tests/test_install_development_skills.py` (exact source/target byte
    comparison, rerun preservation of an unrelated file; extend for new
    report/guide contents).
  - V-04–V-08 → supplied legitimate setup/fixture-composition assertions
    (preflight-only exposure, mixed blocker/missing-proof, corrected evidence,
    coordinator deferral examples, inherited cases) — constructed records are
    explicitly labeled fixture data.
  - V-09 → task results document distinguishing structural tests, actual
    installer/probe behavior, semantic contract inspection, and unrun agent
    compliance; fixture commands/setup and source identities carried to T-005.
- Local assertions prove structural agreement and real installer/probe behavior
  only; actual separate producing/consuming agent calls remain T-005's
  ownership and must stay visible as unrun, never as a passing local check.
  No scenario is blocked locally.

## Warnings

- `.agents/skills/task-implementation-flow/` is stale versus `skills/` source
  (12 differing/absent files). Do not edit, use, or refresh it in this task:
  active refresh is excluded. A fresh reviewer must read `skills/` source
  bytes; the disposable committed-target fixture projects from source and is
  unaffected by the stale installation.
- Budget 10 tool calls / 28 minutes / 40k context is a soft checkpoint; this
  brief composes three predecessors — plan focused edits before starting.
- No behavioral qualification or completion claim for the installed flow;
  T-005 owns actual role calls and final qualification under separate
  authorization.
- No whole-repo, network, or agent-budget gate is authorized.

## Implementation stops

Stop for incomplete predecessors (resolved — accepted), semantic
disagreement with settled .1–.3 contracts (return defects to the owning
child, no silent integration redesign), user-work overlap, unsafe
permissions, missing decisive capability, or scope expansion (T-003
conditional/correction matrices, T-004 unborn/drift, T-005 actual calls, new
shared infrastructure, active refresh are all out of scope). Preserve
history and user AGENTS.md changes. Budget is a soft checkpoint.

## Next action

Hand this ready preflight to bounded implementation: fail-first
composition/projection assertions first (missing-discovery guide check, lost
context/unfinished rows, absent installed reference, new report/guide
projection bytes), then minimal guide/reference reconciliations, then the two
owning gates sequentially. Immediately after implementation or correction,
hand completed bytes to a fresh independent acceptance reviewer after
applicable conditional stages and discovery, and end the implementation
invocation. Reviewed .4 closes T-002's local composition only; continue with
T-003 and leave actual installed multi-call qualification to T-005.

## Implementer handoff

```text
Task: T-002.4 — Close review-flow guidance and local composition.
Status: preflight READY (guided). Brief SHA-256 8593563b…25240 matches verification.md
revision 1 (d12ab546…96942). Predecessors .1/.2/.3 accepted (4a4b771/2a71e4c/6f7b8b9).

Edit scope (confirmed, ownership clean):
- Root README.md, skills/README.md, skills/task-implementation-flow/README.md
- Minimal stage-name/reference substitutions in affected skills/task-implementation-flow/
  child-skill handoffs/layout references (task-review-discovery, task-acceptance-review,
  task-preflight consumer wording) where omission of discovery contradicts .1/.2
- tests/test_review_discipline.py, tests/test_install_development_skills.py (focused additions)
- Task-local eval/fixture composition and results under docs/tasks/T-002.4/
Read-only: settled child semantics, plans, historical reviews, .agents/ active installation
(12 files stale vs source — do not use, edit, or refresh), scripts/install_development_skills.py
constants (inspect only if predecessors require), docs/tasks/T-002.4/verification.md, .DS_Store.

Commands (repo root, sequentially, after targeted evidence is clean):
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
Preflight baseline: 54 tests OK (1.77s); 13 tests OK (0.74s). Fail-first: new assertions must
reject missing discovery in an affected guide, lost context/unfinished rows, absent installed
reference, and missing new report/guide projection bytes before the guides/fixture are completed.

Oracle: verification.md V-01–V-09 cover AC-01–05 and C-01–03. V-03 uses the existing disposable
committed-target installer fixture (byte comparison, not existence; add unrelated target file
before rerun). V-04–V-08 fixtures are constructed data, labeled as such. Local checks prove
structural agreement and real installer/probe behavior only; actual agent compliance and
installed-flow qualification are T-005, unrun and explicitly recorded. Carry fixture
commands/setup and source identities to T-005.

Stops: semantic defects return to the owning child; no T-003/T-004/T-005 scope, no new shared
infrastructure, no .agents/ refresh, no whole-repo/network/agent-budget gate. Budget
(10 calls/28 min/40k) is a soft checkpoint. After implementation/correction: hand bytes to a
fresh independent acceptance reviewer after applicable conditional stages and discovery; end
the implementation invocation. Continue with T-003; T-005 owns actual multi-call qualification.
```