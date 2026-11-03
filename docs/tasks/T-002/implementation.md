# T-002 implementation submission

Implemented: READY_FOR_REVIEW

Preflight source now prepares the actual starting Python report and carries native
check duties in both readiness profiles. It retains the original report pair through
corrections, checks applicability before editing, exposes advisory gaps and blocks
only under applicable required-evidence/native-entry policy. T-003 and T-004
consumer execution remains outside this submission.

Authority: `docs/tasks/T-002/brief.md` revision 1.
Context: `docs/tasks/T-002/preflight.md`; `docs/tasks/T-002/verification.md` revision 1.
The staged package and task index predate implementation and remain untouched.

## Deliverables and contract impact

- Changed source preflight instructions and both-profile packet template.
- Preserved eval IDs 1–12; aligned authorized report writes with their policies.
- Added eval 13 and a `starting-evidence` setup mode: 42 independent row inputs,
  source/index/report preservation identities, explicit policies and row oracles.
- Actual contract impact: added preflight producer guidance for original evidence
  and native-check inventory (IF-002 / FLOW-002-S01); consumers are not delivered.
- Executable contract declarations changed: no shared runtime/schema changes;
  eval setup CLI adds `starting-evidence` and requires explicit
  `EVAL_MEASUREMENT_LAUNCHER` plus a prepared analyzer interpreter.
- Installer selection, managed README and runtime dependencies were inspected;
  no additions or ownership-boundary changes are needed. Existing package copying
  includes the changed files. Registry synchronization belongs to the next stage.

## Verification and coverage

Commands ran from the repository root. `PINNED` below denotes exactly
`.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`.

- `PYTHONDONTWRITEBYTECODE=1 PINNED -m unittest discover -s tests -p test_maintainability.py`:
  33 passed, no skips. Real measurement/installed runtime boundaries only.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`:
  36 passed. Projection and preservation boundaries only.
- `PYTHONDONTWRITEBYTECODE=1 EVAL_WORK_ROOT=/tmp/t002-fixtures EVAL_MEASUREMENT_LAUNCHER="$PWD/.agents/scripts/measure_maintainability.py" PINNED skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py starting-evidence`:
  exit 0. Real initial baseline; 42 independent row setups. V-10a/c/d include
  actual Ruff command results and source identities, with a later real source
  change for stale evidence. Partial/incompatible reports are controlled upstream
  fault inputs, not claims of agent capture. Missing capability is a supplied
  absent-launcher path, not a damaged active installation.
- All nine original setup modes ran with `EVAL_WORK_ROOT=/tmp/t002-original-fixtures`:
  exit 0 each. No agent invocation or grading occurred.
- Local input probe checked all 42 source/index/report hash maps, existing empty
  parent, missing parent, missing original and partial status against setup output.
  This checks fixture consistency, not readiness behavior.

| Scenario inventory | Current implementation evidence and oracle | Limit / next owner |
|---|---|---|
| V-01 | Real dirty/staged/untracked/index test and folder/exclusion tests; new fixture covers all five asset folders | Agent folder selection unrun; discovery checks prepared guidance |
| V-02a, V-02b, V-02c, V-02d | Real empty-folder baseline/compare and excluded/missing scope tests; independent empty/missing/vendor inputs | Agent decisions unrun; discovery |
| V-03a, V-03b, V-03c | Real each-report-sibling collision test and successful installed capture control; occupied sentinel inputs | Agent fresh-name choice unrun; discovery |
| V-04a, V-04b | Both template profiles and producer guidance; real report fields and separate guided/high-assurance inputs | Actual readiness output unrun; discovery |
| V-05a, V-05b, V-05c, V-05d, V-05e, V-05f, V-05g, V-05h | Independent unchanged/hash/inventory/project/tool/settings/scope inputs; existing real incompatible identity/settings tests | Producer mismatch decisions unrun; discovery |
| V-06a, V-06b, V-06c | Original pair retained; edited correction, exact preserved added bytes, and untracked unrecoverable-history inputs; existing repeated compare/uncovered scope tests | Recovery choices unrun; discovery |
| V-07 | Exact source pair and receiver paths in prompt; existing real different-mount/target-root handoff tests | Agent transfer unrun; discovery |
| V-08a, V-08b | Explicit docs/JS measurement scope with unchanged other prerequisites; N/A guidance | Agent N/A classification unrun; discovery |
| V-08c-A, V-08c-R, V-08d-A, V-08d-R, V-08e-A, V-08e-R, V-08f-A, V-08f-R | Separate absent-launcher/missing/incompatible/partial inputs with A/R policy and owner; existing real unavailable/partial/incompatible tool tests | Agent ready/blocked decisions unrun; discovery |
| V-09a, V-09b, V-09c | Registry/documented/absent native-policy inputs; explicit inventory template fields | Native discovery behavior unrun; discovery |
| V-10a, V-10b, V-10c, V-10d | Real seeded command evidence/current or changed hashes, missing and omitted coverage inputs; later-owner policy | Evidence-admission decisions unrun; discovery |
| V-10e, V-10f, V-10g | Real F401 input plus existing native-hard-failure/advisory-success test; absent native command with explicit entry policy and unavailable/N/A measurement | Agent blocking decisions unrun; discovery |
| V-11 | Original eval IDs retained, all nine old setup modes run, installer suite passes; explicit report-write authorization | Live compliance unqualified; discovery inspects setup/grading |

All rows have prepared inputs and specified oracles; none has live agent behavioral
qualification. No live eval is required by this brief or authorized in this run.
Schema/metadata checks are not counted as behavioral evidence.

## Gates, limits and next action

- Canonical architecture check: 4 passed.
- `python3 tools/check_contracts.py --root .`: exit 0, 6 subsystems / 12 indexed refs.
- `git diff --check`: passed.
- `python3 scripts/install_development_skills.py --check .`: exit 1, expected drift
  in the four edited preflight source counterparts. Active installation unchanged.
- Aggregate `python3 tools/verify.py` not run: single-skill change, focused owning
  suites suffice; aggregate would also report the intentional active-profile drift.
- Optional run evidence used from the active `.agents` installation.

Next: fresh task-maintainability-review (significant eval/setup changes), then
task-contract-registry-updater, fresh independent task-review-discovery, and a
separate fresh task-acceptance-review decision. Architecture is completed as
implementation evidence. No independent review or acceptance is claimed here.
