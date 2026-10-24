# Verification Design: T-001.1 — Install a portable, target-aware measurement runtime

Protect the boundary between an installation and the repository it measures.
The launcher must use local runtime resources and pins, select each target policy
independently, and preserve source, index and saved evidence. The main risks are
hidden source-checkout dependencies, silent policy fallback and destructive refresh.

## Testing approach

| Checks | Level and real boundary | Why this evidence is sufficient |
|---|---|---|
| Portable launch and settings, V-01–V-03 | Public CLI subprocesses, disposable installation and target filesystem, real pinned Radon/Ruff | Proves installed wiring and effective policy through actual measurements. A copied helper or mocked analyzer alone cannot prove portability. |
| Setup and interpreter selection, V-04–V-06 | Component checks at environment selection and provisioning calls; real launch where available | Proves target/pin arguments without network. Call observation does not prove dependency installation. Native selection must reach the actual adapter, not just calculate a path. |
| Measurement preservation, V-07–V-10 | Existing native measurement cases plus public CLI and real disposable Git/filesystem operations | Proves snapshot bytes, native values, compatibility and report preservation after relocation. Retain distinct existing cases rather than duplicate their setup. |
| Installation lifecycle, V-11–V-12 | Actual installer and read-only checker against disposable Git targets | Proves fresh install, drift detection and refresh at the ownership boundary for every new managed file. |
| Distribution documentation, V-13 | Source/interface review, separate from behavioral checks | Proves declared membership and documented paths agree. Does not establish executable behavior. |

No live provider or dependency download is required. Real analyzer skips leave
AC-01 and AC-04 unproved. Local evidence does not qualify another operating
system or actual network provisioning.

## Source and revision

Source brief: docs/tasks/T-001.1/brief.md
Source brief revision: SHA-256 e38fb7e8e978aa3b16df91fa0b6d10d2b928d08af7bc2119a51fdd48709d5d83
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

Initial design. Parent reviewed plan identity matches the current plan and task
map. The installation/settings rules are in [plan section 7](../../project-plan.md#installation-and-settings-contract).
Ready means the design is complete; preflight must establish execution readiness.

## Coverage summary

| Promise from the brief | AC / risk row | Required cases |
|---|---|---|
| [Local runtime, pins and defaults; real installed baseline/compare](brief.md#work-and-acceptance-criteria) | AC-01; R-01 | V-01a, V-01b, V-02a–V-02d, V-13 |
| [Independent policy selection and truthful identities](brief.md#work-and-acceptance-criteria) | AC-02; R-01 | V-02a–V-02d, V-03a–V-03c |
| [Target setup, native separation and no measurement provisioning](brief.md#work-and-acceptance-criteria) | AC-03; R-01 | V-04, V-05a–V-05f, V-06a, V-06b |
| [Actual snapshots and unchanged source/index](brief.md#r-02--relocation-or-refresh-loses-evidenceownership-ac-04ac-05) | AC-04; R-02 | V-07 |
| [Scope, native semantics, unknowns, groups and exclusions](brief.md#work-and-acceptance-criteria) | AC-04; R-02 | V-08a–V-08e, V-09a–V-09f |
| [Saved JSON/text and advisory execution outcomes](brief.md#work-and-acceptance-criteria) | AC-04, AC-05; R-02 | V-01a, V-09a–V-09d, V-10a, V-10b |
| [Fresh install, refresh and precise read-only drift](brief.md#r-02--relocation-or-refresh-loses-evidenceownership-ac-04ac-05) | AC-05; R-02 | V-11, V-12a, V-12b |
| [Installer and relocation documentation agree](brief.md#authority-and-scope) | AC-05 | V-13 |

## Shared setup

- Use disposable Git targets, a separate installation source fixture and an
  unrelated cwd. Never refresh this session's active `.agents/` installation.
- Reuse the existing measurement suite's native source generators and dirty Git
  setup, and the installer suite's install/check, managed-path and byte-snapshot
  setup. Existing coverage is in `tests/test_maintainability.py` and
  `tests/test_install_development_skills.py`; test structure remains the
  implementer's choice.
- Use a prepared interpreter with the installation's exact pins for real native
  cases. Pin availability is UNKNOWN until preflight. Do not install or change
  dependencies to satisfy this design.
- Capture source bytes, real index bytes and staged entries before each relevant
  action. Also capture target settings, environment/report sentinels, unmanaged
  skill/helper bytes and AGENTS bytes outside its managed block for install cases.
  Compare against these captured values, never a post-action reconstruction.
- New output paths are relative to the selected target, normally under
  `.quality/reports/`. Record JSON and sibling text bytes separately.
- For policy cases, use valid target settings distinct from shipped defaults:
  complexity target 3, Ruff argument/statement targets 2/3. Inputs include
  `def f(a,b,c): pass` (native argument/statement counts 3/1) and a function with
  four independent `if` statements (Radon complexity 5). Retain valid remaining
  policy fields. Determine default expectations from the one shipped source;
  current provisional targets are 10/5/50. Do not alter target policy for scores.

## Verification scenarios

### V-01 — Public launchers use their own complete runtime

Covers: AC-01; R-01.

Why: help output or a source-relative import can conceal an incomplete installation.

| Case | Given and action | Exact expected result |
|---|---|---|
| V-01a | Install into a separate Git target. Make the disposable source checkout unavailable to execution and exclude ambient/global helper paths. From an unrelated cwd, run the installed public launcher with explicit `--root`: baseline a folder, edit one function, then compare that file against the saved baseline. Run `measure` on the same target. | All three operations complete with exit 0 and real pinned analyzer results. Baseline and compare JSON/text files are under the selected target. A one-branch addition changes Radon complexity from 2 to 3, delta +1. Baseline bytes remain unchanged. Runtime, defaults and pins resolve inside this installation; execution reads no original-source resource. |
| V-01b | Run the source public launcher from the unrelated cwd against the separate target with the same native inputs and explicit root. | The same native results and target-relative output behavior hold. Helpers, pins and fallback defaults come from source `scripts/`, not repo-only `tools/` or source `.quality/`. |

Check: inspect real process outcomes, report contents and filesystem changes.
Establish source unavailability through isolation or denied reads, not cwd alone.
Keep the prepared analyzer interpreter accessible independently of the disposable
source. A successful mocked adapter does not satisfy V-01a.

### V-02 — Each settings family selects its own origin

Covers: AC-01, AC-02; R-01.

Why: selecting both files from one directory loses valid mixed-origin policy.

Given the shared policy inputs and no unrelated configuration, invoke the
installed launcher with explicit target root for each independent row:

| Case | Target maintainability / Ruff presence | Expected policy and report identity/origin |
|---|---|---|
| V-02a | Neither | Both shipped defaults; no source `.quality/` dependency. |
| V-02b | Maintainability only | Complexity target 3 from target; Ruff targets from shipped default. |
| V-02c | Ruff only | Complexity target from shipped default; Ruff targets 2/3 from target. |
| V-02d | Both | Complexity target 3 and Ruff targets 2/3, both from target. |

Then: each run completes; native counts stay 5 for the branch function and 3/1
for `f`. Reported targets, effective settings content/identity and origin agree
with that row. Target files remain byte-identical. Check both actual observations
and identities; a correct origin label with ignored policy fails. All four rows
are required because two independently optional files have four material states.

### V-03 — Invalid target policy fails; unrelated Ruff policy is ignored

Covers: AC-02; R-01.

Why: fallback or inherited Ruff rules can report plausible but wrong measurements.

| Case | Given | When | Then |
|---|---|---|---|
| V-03a | Malformed present target `maintainability.toml`; valid Ruff policy and available pins | Invoke measurement against target | Exit 2 with a visible settings failure identifying the affected policy; no successful default-based measurement. Bad file remains unchanged. |
| V-03b | Valid maintainability policy; malformed present target `ruff.toml`; available pins | Invoke measurement against target | Exit 2 with a visible failure for Ruff policy; no silent shipped fallback or claim of complete measurement. Bad file remains unchanged. |
| V-03c | Valid effective settings, plus conflicting root Ruff config which disables the measurement rules or sets different limits | Measure native inputs with the root config present and absent | Both runs use only the effective `.quality/ruff.toml` or shipped fallback, with the same counts, targets and effective settings identity. Root Ruff bytes remain unchanged. |

Check process diagnostics and report status where produced. Exercise V-03c with
both target Ruff and shipped fallback; this rules out configuration inheritance
on either path. Valid V-02 rows supply controls against an always-failing launcher.

### V-04 — Explicit setup provisions the selected target from local pins

Covers: AC-03; R-01.

Given: a separate target, unrelated cwd, distinguishable installation and target
requirements bytes, and no native target environment.

When: invoke `setup --root <target>` and observe environment creation and package
installation requests without allowing package downloads.

Then: the environment destination is under that target's `.quality/envs/`, using
the installation pin identity. The install request uses the installation's pinned
requirements, never the target's requirements. No environment is requested under
the installation or cwd. Target policy and existing reports remain unchanged.

Check: observe the actual setup dispatch and its provisioning arguments. This
controlled provisioning boundary proves selection, not completed package setup.

### V-05 — Native environment identity and selection remain separated

Covers: AC-03; R-01.

Why: a shared path can launch foreign binaries or reuse incompatible dependencies.

| Case | Input/action | Expected result |
|---|---|---|
| V-05a | Change OS identity only | Different environment key. |
| V-05b | Change CPU architecture only | Different environment key. |
| V-05c | Change Python implementation only | Different environment key. |
| V-05d | Change full Python version only | Different environment key, including a patch-version change. |
| V-05e | Change installation pin bytes only | Different environment key. Target requirements changes alone do not change it. |
| V-05f | Seed a prepared, correctly pinned native target environment at the selected key; invoke from an unpinned caller. Also place unusable legacy `.quality/venv` and foreign-key environments in the target. | Launcher reaches the real adapter through the selected native target interpreter and completes measurement; it executes neither legacy nor foreign environments. |

Check key separation with controlled identities at component level. For V-05f,
observe actual process selection and real report versions/result. The seeded
environment represents output normally created by setup; it does not prove setup
installation. Exact seeded interpreter availability belongs to preflight.

### V-06 — Pinned callers work; missing pins never trigger provisioning

Covers: AC-03; R-01.

| Case | Given and action | Expected result |
|---|---|---|
| V-06a | No target environment; invoke measurement with a correctly pinned interpreter | Real measurement completes with exit 0 using that interpreter. No environment is created and no package installation is attempted. |
| V-06b | Neither caller nor selected target environment supplies the pins; invoke against a valid target from an unrelated cwd | Exit 2 identifies unavailable pinned tools and gives an executable setup instruction selecting this launcher and this target. No new environment/packages or provisioning request. Source, index, settings and saved reports remain unchanged. |

Check before/after environment trees and provisioning boundary observations.
Use a target path containing spaces for V-06b: the printed instruction must parse
to the intended launcher, `setup`, and `--root <target>`. Exercise its setup dispatch
under V-04's no-download observation to rule out an unusable diagnostic recipe.

### V-07 — Capture actual dirty bytes without changing source or index

Covers: AC-04; R-02.

Why: a clean-HEAD or staged snapshot can erase the real task starting point.

Given: a committed file with complexity 2; stage a version with complexity 3;
leave worktree complexity 4; add an untracked Python function with complexity 1.

When:
1. Capture a folder baseline through the relocated runtime.
2. Edit the tracked worktree function to complexity 5, then compare it.

Then: the baseline stores exact pre-edit worktree bytes and hashes for both
tracked and untracked files, complexity 4/1, and truthful dirty Git context.
Comparison reports 4 to 5, delta +1. Baseline JSON/text do not change. At each
checkpoint, runtime execution preserves source bytes, real index bytes and staged
content relative to the state immediately before that invocation.

Check: reuse the existing dirty-snapshot case and extend its observable sequence;
compare decoded report sources and actual index bytes, not status text alone.

### V-08 — Existing scope and native observations survive relocation

Covers: AC-04; R-02.

Run the existing native cases at the relocated boundary. Keep these obligations
identifiable; passing one does not cover the others.

| Case | Setup/action | Expected result |
|---|---|---|
| V-08a | Baseline function complexities 2, 10, 11 and 16; later change 2 to 3, leave 10/11 unchanged, reduce 16 to 2, and add a function at 11. Separately move 10 to 11. | Native values and deltas are exact; equality at 10 is within target, 11 exceeds it. Untouched over-target inventory creates no change increase; crossing and new breach stay visible. |
| V-08b | Measure nested methods, local classes, async functions and duplicate qualified names | Existing qualified identities and native values remain distinct; duplicates remain unmatched instead of invented deltas. Renamed/added/removed symbols need interpretation. |
| V-08c | Measure real Ruff five/six-argument functions, 51 statements, and native override/overload exemptions | Collection limits remain zero, advisory targets remain separate; native counts and exemptions retain their existing meaning. `noqa` does not suppress collection. |
| V-08d | Compare missing-to-present and present-to-missing Ruff observations for zero arguments, return-only bodies and exempt methods | Missing numeric values and deltas remain unknown (`null`), never zero or asserted improvement. Known native values remain exact. |
| V-08e | Measure implementation, test and eval/fixture/harness files; include invalid Python under excluded directories | All included asset families are measured in separate existing groups. Nested excluded directories are skipped and recorded; explicit excluded scope is refused. Installed copies, environments and reports are excluded. |

Check native records and comparison results, reusing existing assertions. This
child preserves current report semantics; neutral-label and empty-baseline
extensions belong to T-001.2.

### V-09 — Scope compatibility and incomplete results remain explicit

Covers: AC-04; R-02.

| Case | Setup/action | Expected result |
|---|---|---|
| V-09a | Measure only complexity with otherwise valid inputs | Selected check completes, exit 0; `full_profile` is false, not a claim of full analyzer coverage. |
| V-09b | Make Ruff unavailable at adapter discovery with Radon available | Report is incomplete; Radon observations remain visible and Ruff is unavailable. CLI reports execution failure (exit 2), not clean evidence. |
| V-09c | Measure invalid Python; separately change source during scanning after capture | Each reports incomplete/failed evidence with its actual cause, exit 2. Captured observations are retained where available; no complete claim. |
| V-09d | Compare with an incomplete baseline or independently changed tool, effective settings, adapter, collection or incompatible interpreter identity | Comparison is incompatible with a reason, exit 2. Absolute root/mount or Python patch-only differences remain compatible under existing rules when other identities and logical scope match. |
| V-09e | Folder baseline, then compare an affected subset including new files within that folder and a captured file now deleted | Comparison completes; new/removal observations appear. Untouched files outside the after scope are not removals. Scope outside baseline coverage is incompatible. |
| V-09f | Invoke existing folder/file scopes and absolute paths inside explicit root; separately invoke an escaping or symlink scope | Valid paths select the intended target files; escaping/symlink scopes fail visibly under existing scope rules. |

Check status/reasons and retained records through existing component cases;
include CLI outcomes for failure and partial-profile wiring. V-01 and V-08a
supply successful measurements even with increases/breaches: advisory values
alone must not cause execution failure or waive a native hard gate.

### V-10 — Saved JSON and sibling text cannot be overwritten

Covers: AC-04, AC-05; R-02.

Why: preserving one report format alone can still destroy starting evidence.

| Case | Given/action | Expected result |
|---|---|---|
| V-10a | Existing JSON at the requested output; attempt baseline or comparison there | Exit 2 for occupied output; original JSON and any sibling text remain byte-identical. |
| V-10b | Only sibling `.txt` exists; request its matching JSON output | Exit 2; text remains byte-identical and no replacement JSON is published. |

Use a new output path as the successful control (V-01). Check filesystem bytes
and visible refusal, not exit code alone.

### V-11 — Fresh install and refresh preserve target ownership

Covers: AC-05; R-02.

Given: disposable committed and unborn Git targets with target settings,
environment/report sentinels (both JSON and text), unmanaged skills/helpers,
outside-marker AGENTS bytes, and staged/unstaged/untracked source. Seeded
environments/reports represent prior setup/measurement outputs.

When:
1. Install the profile, then run read-only `--check`.
2. Change a managed runtime resource and add a stale file inside a selected skill
   directory, then explicitly refresh and run `--check` again.

Then: fresh install supplies every declared runtime/helper/default/pin resource;
refresh restores managed bytes and selected-package cleanup under existing rules.
Both checks return match (exit 0). Unmanaged helpers/skills, target policies,
environments/reports, source and real index retain exact bytes. AGENTS prefix and
suffix bytes, including existing line endings, are unchanged. Committed HEAD or
unborn state is unchanged; installation does not fabricate a commit.

Check actual before/after trees and index identities. Extend existing refresh
and AGENTS preservation coverage; never infer preservation from matching status.

### V-12 — Every new managed resource has precise, read-only drift evidence

Covers: AC-05; R-02.

Given a matching disposable installation and the preservation sentinels of V-11,
exercise each newly managed runtime, helper, default and pin file independently:

| Case | Action | Expected result |
|---|---|---|
| V-12a | Change only that managed file; run `--check` twice, then explicit refresh and check | Each pre-refresh check exits 1 and reports exactly that path as changed. Checks write nothing. Refresh restores canonical bytes; final check exits 0 with no differences. |
| V-12b | Remove only that managed file; run `--check` twice, then explicit refresh and check | Each pre-refresh check exits 1 and reports exactly that path as missing. Checks leave it absent and write nothing. Refresh restores it; final check exits 0 with no differences. |

Check complete filesystem and index snapshots around read-only checks and the
V-11 preservation set around refresh. Do not reduce file coverage to one example
per family. Enumerate resources from the completed distribution membership.

### V-13 — Distribution declarations and public guidance agree

Covers: AC-01, AC-05.

Given the completed runtime relocation, review installer selections,
`SHARED_SCRIPT_FILES`, `PROFILE_SKILLS_README`, focused installer expectations,
profile guide, README, tool guide and relocation entries in the project map or
development guide.

Then: all required runtime/default/pin files are explicitly managed under the
existing narrow installer boundary. Helpers resolve beside the public launcher
in source `scripts/` and installed `.agents/scripts/`. One shipped-default source
exists; source `.quality/` remains deliberate target policy. Guidance describes
effective target settings, installation-owned pins and `setup --root <target>`,
and maps old repo-only helper paths to their new locations. No global fallback,
generic installer, active refresh or changed native hard-check policy is added.

Check by interface/document review, supported by V-01 and V-11–V-12 behavioral
evidence. Text agreement alone does not qualify the runtime.

## Implementation handoff

- Reuse existing cases and fixtures; add only missing behavioral assertions.
  Choose concrete tests and production design under the brief's authority.
  Show that new origin/isolation assertions reject old source-dependent behavior
  where feasible, with failure at the intended assertion rather than setup.
- Obtain a ready `preflight.md` for this brief hash and verification revision
  before implementation. Confirm pinned interpreter and native-environment fixture
  availability, source isolation and exact pre-edit preservation. Missing real
  evidence must remain blocked/unchecked; skips do not close required cases.
- Run changed cases first, then the pinned-interpreter maintainability suite,
  then the installer suite, sequentially as required by the brief. Before handoff,
  run the canonical architecture check and contract validator. They provide
  structural evidence, not replacement behavioral proof. T-001.3 owns the final
  aggregate `tools/verify.py` composition check.
- A reasoned revision retains case IDs and supersedes affected readiness/evidence
  until focused preflight is ready. Route unresolved expected behavior to task
  design/decision owner; route unavailable tools, isolation or fixtures to preflight.
- T-001.2 owns neutral labels and empty-baseline behavior; T-001.3 owns foundation
  discovery and final composition. Do not expand this leaf to those obligations.
  Preserve the brief's subsequent maintainability review, registry update, fresh
  discovery and separate acceptance route. This design claims no test execution,
  implementation correctness or independent acceptance.
