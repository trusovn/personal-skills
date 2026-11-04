# Task Preflight: T-004 — Add independent measurement and review decisions

Status: `ready`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | [brief.md](brief.md), executable and ready; project-plan sections 1–7, T-004, FLOW-002/FLOW-003 and V-004–V-008. Guided preparation, not an orchestrator packet. |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills`; HEAD `6b80c8eecad0943c3a9ed9695f1f27ff124df5b2`. |
| Dependencies / entry criteria | T-003 [acceptance-01.md](../T-003/reviews/acceptance-01.md) is ACCEPT following its authorized reevaluation. Measurement, implementer-feedback, installation and runtime-evidence records identify implemented dependencies. Historical acceptance is not current-byte test evidence. |
| Allowed scope | Source maintainability-review package; minimal discovery/acceptance packages and task-flow README changes needed for consumption; designated later contract synchronization. Inspect installer declarations, focused coverage and README installation guidance; synchronize only stale entries. No runtime redesign, new stage, active installation refresh or T-005 closure. |
| User-work ownership | Existing staged `brief.md`, `verification.md` and `docs/tasks/index.json` are user work. No implementation-path overlap. This preflight adds only this readiness file and the authorized ignored baseline pair. Do not stage, reset, stash or edit the existing inputs. |
| Permission limits | Local disposable Git/filesystem/process checks and report writes are feasible. No live/network checks, dependency provisioning, active-install refresh, commits or destructive work. |
| Profile | `guided`; project-local `.agents/skills/task-implementation-flow/task-preflight/SKILL.md` and its packet template govern this invocation. Source instructions remain development specifications. |
| Standalone preflight value | `material`: resolved staged-input ownership, installation-local runtime/pinned dependency availability, existing fixture execution and original-report write feasibility before any implementation edit. |
| Source brief / revision | `docs/tasks/T-004/brief.md`, revision 1; actual SHA-256 matches verification's declaration: `d45b174d7e3a671c1cdc2d0313e7a008683c8a1757446112e6f7a12dd693ac9d`. |
| Verification / revision | [verification.md](verification.md), revision 1, status ready; `Source brief:` resolves to this package's brief. All AC-01–AC-06 and finite child scenarios remain required. No coverage revision. |
| Current applicability | Ready for source guidance and executable eval preparation on the inspected bytes. Check starting-report inventory/source/tool/settings identity before the first edit. Material authority, scope, ownership or capability changes require focused reconsideration. Expected implementation/report writes alone do not invalidate preparation. |

## Decision context

The operating envelope is a fresh bounded maintainability reviewer, with read-only
code access and authorized fresh report writes. It consumes the accepted
implementer handoff and supplies current review evidence to the existing ordered
route. [Project-plan section 5](../../project-plan.md#5-lifecycle-and-decision-rules)
governs proportionality; older every-increase defense rules do not govern this
task. False freshness, lost rationale obligations and advisory/native conflation
can produce an unjustified verdict or omit a required stage. Preserve complete
ledgers, stable findings, original history, explicit owners and honest proof limits.

Current contracts come from [the registry](../../contracts/index.json), specifically
`measurement.json`, `implementer-feedback.json`, `installation.json` and
`runtime-evidence.json`; T-004's reviewer disposition remains a planned delta.
[Project map](../../project-map.md) and [development guide](../../development.md)
confirm source/test ownership and native commands. Existing skill eval setup and
measurement/installer tests provide reusable local mechanisms; no new shared
runner is required. T-005 is the credible next consumer and owns the complete
installed journey. No known-issues file was found under `docs/`; no recorded
deferral is inferred. T-003 records active source/installation drift as a reported
diagnostic, not a requirement to refresh this run. Recheck/report current drift
when the implementation gate runs.

Assumption: task-owned future cases may extend the existing fixture owner; their
absence before implementation is expected. An unavailable indispensable boundary
would instead block and return to its capability owner. None was found. Prepared
actor inputs and local tool checks do not qualify agent compliance.

## Acceptance evidence and commands

All commands below use the repository root unless another cwd is specified.
`V-*` refers to every child row listed, including separately varied inputs within
each row. The brief remains normative; verification supplies the derived setup
and oracle. Future preparation checks have not passed merely because readiness
is ready.

| AC / scenarios / risk | Authority relationship | Setup / decisive boundary / oracle | Exact command / cwd | Feasibility / baseline or gap |
|---|---|---|---|---|
| AC-01; V-01a–e, V-02a–i | Brief independent comparison and provenance; verification V-01/V-02 | Actual B/I/current bytes; fresh independent R, submitted-byte hashes, original/index preservation; missing/incompatible/unavailable/partial/collision/path states isolated from other faults. Same-session and isolated-transfer controls remain distinct. | Installed public `baseline` command below; after editing use `python3 -B .agents/scripts/measure_maintainability.py compare skills/task-implementation-flow/task-maintainability-review skills/task-implementation-flow/task-review-discovery skills/task-implementation-flow/task-acceptance-review --root /Users/mtrusov/work/skill-sources/personal-skills --baseline .quality/reports/T-004-preflight-20261104-01.json --output .quality/reports/T-004-implementation-01.json`. Check both output siblings are unused first. | Installed helpers/pins/settings available; baseline complete. Existing `tests/test_maintainability.py` covers real identities, collisions, partial/tools, relocation and index preservation. Reviewer actor cases are future task-owned preparation, unrun. |
| AC-02; V-03a–j, V-04a–d | Plan section 5 and brief proportionate affected-responsibility rules | Real at/below/above 10/50/5 counts, actual diff, touched/untouched/rename/move/extract variants, unknown counts; inspect each explicit rationale agreement/counterargument, not keyword presence. | `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py` | Existing numeric, symbol, exemption and compatibility tests are reusable. Future reviewer-case preparation must cover every variant and related-metric grouping; no current agent judgment claimed. |
| AC-02; V-05a–e | Brief semantic review, significant test assets and abstraction cost | Actual defect/control diffs with held-back concrete maintenance observations; do not treat smaller metrics or green functional tests as a semantic verdict. | `EVAL_WORK_ROOT=/tmp/T-004-semantic-defects PYTHONDONTWRITEBYTECODE=1 python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py semantic-defects`; use distinct fresh roots with `semantic-control`, `test-assets` and `test-assets-control` for their respective cases. | Existing scenario dispatch/setup inspected. Local four-blockers control setup/gate/suite passed as recorded below; these semantic variants were not run in preflight. Preserve the existing independent oracles. |
| AC-03; V-06a–j, V-10f | Brief native-policy preservation; plan IF-004/INV-009 | Declare real native command/scope/policy/owner; invoke actual pass/fail/recovery commands and record invocation/checked bytes. Keep stale/omitted aggregate coverage, absent commands, policy conflict and optional-wrapper cases separate. | Existing fixture: `python3 scripts/check-architecture`, cwd disposable `maintainability/`; owning measurement suite command above exercises real hard-failure/advisory-success separation. | Python/Git/local subprocesses available. Existing fixture gate passed. Task-owned additional native fault/aggregate-reuse cases remain to prepare and exercise; fabricated PASS fields are not proof. Repo gates remain separately owed below. |
| AC-04; V-07a–c plus V-02e–i, V-03c–j, V-06a–g, V-08c | Brief complete report and uncapped required dispositions | At least four obligations, four stable blockers, evidence gap and more than three optional warnings. Reconcile actual report against the full input ledger; genuine stop retains outstanding work/owners. | `EVAL_WORK_ROOT=/tmp/T-004-four-blockers PYTHONDONTWRITEBYTECODE=1 python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py four-blockers`; use fresh root and `genuine-stop` for its separate incomplete oracle. | Four-blockers setup is executable and passed in a unique disposable root. New disposition-ledger inputs/oracles are in-scope future preparation, not completed review evidence. |
| AC-05; V-08a–d, V-09a–c | Brief original-baseline correction, source preservation and expansion authority | Two actual edits and comparisons to unchanged B; stable surviving/resolved IDs and complete ledger; unchanged-scope control; authorized/exact-preserved/unrecoverable expansion states. | `EVAL_WORK_ROOT=/tmp/T-004-correction-round PYTHONDONTWRITEBYTECODE=1 python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py correction-round`; installed CLI compare and owning suite above. | Existing correction/test-assets-correction and original-baseline/coverage tests support extension. Extra capture outside governed folders requires authorization and verified pre-edit history; no edited-tree baseline. Future correction actor behavior unrun. |
| AC-05; V-10a–f | Brief conditional existing route; IF-003/INV-008 | Prepared current/stale reports, exact byte/scope identity, applicable registry and discovery evidence. Oracle is first outstanding stage plus complete ordered remainder, with separate execution/evidence/decision owners. | Existing consumer setup owners: `skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py` and `skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py`; inspect their case dispatch before extending; run the exact changed fixture/check command recorded by implementation. | Existing standalone Python setup owners captured by B. New finite evidence-consumption variants are feasible within allowed packages. No downstream execution or fresh-agent qualification during preflight. |
| AC-06; V-01–V-10, V-11a–b | Brief eval preparation; verification complete coverage summary | Trace every retained child ID to actual inputs, usable tools/report writes and decisive artifact oracle. Reuse existing setup; exercise claimed CLI/native behavior; reject controlled stale/missing/wrong-route output at its intended oracle. | Run changed fixture/check entry points first; then the pinned owning measurement suite above. Implementation must publish the exact new check commands and raw outputs rather than claim metadata/syntax as behavior. | No missing runtime boundary found. New task-owned executable cases/checks are expected implementation work; none is represented as passed yet. Live model runs are excluded. |
| Scope/distribution; V-11c | Brief installer maintenance; AGENTS installer ownership | Disposable canonical installation, changed package resources/entry points, preserved unrelated target bytes/settings/reports; no source/global fallback. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` | Installer already selects all three packages and shared runtime resources. Constants/profile guide/tests/README were located; implementation must inspect/synchronize stale declarations only. No installed membership/runtime change is inherently required. |

The only executed fixture baseline used a unique root
`/var/folders/58/bqcvz6wx57j2tf732gp9325h0000gn/T/T-004-preflight-2jfmgtwh`.
Raw output is `baseline.log` there. In order: source `setup_fixture.py
four-blockers`, then `python3 scripts/check-architecture`, then `python3 -m
unittest discover -s tests` in its `maintainability/` workspace all exited 0.
This proves local setup/process/native-gate/test feasibility only. It supplies no
maintainability verdict and does not discharge the task's future scenario matrix.

## Starting evidence and native obligations

- Measurement: **complete**, format 5, `full_profile: true`, profile
  `python-initial`; complexity and Ruff checks completed. No implicit setup or
  cross-installation fallback. A temporary report-inspection script initially
  assumed `files` was a list; a corrected dictionary traversal confirmed all
  three source hashes match. This was an inspection error, not measurement failure.
- Original pair, retain both:
  `.quality/reports/T-004-preflight-20261104-01.json` and
  `.quality/reports/T-004-preflight-20261104-01.txt`.
- Executed command: `python3 -B .agents/scripts/measure_maintainability.py baseline skills/task-implementation-flow/task-maintainability-review skills/task-implementation-flow/task-review-discovery skills/task-implementation-flow/task-acceptance-review --root /Users/mtrusov/work/skill-sources/personal-skills --output .quality/reports/T-004-preflight-20261104-01.json`.
- Scope: those three existing package folders include future covered Python
  additions and the three current `evals/files/setup_fixture.py` assets, all
  classified `eval_or_harness`. Actual pre-edit worktree capture includes the
  staged user preparation in repository provenance; the source and real index
  were preserved. Logical project is this repository at the HEAD above; the
  recorded absolute root is provenance, not sufficient project identity alone.
- Report authorities: `files` contains inventory, source snapshots and SHA-256;
  `identity` contains scope directories, checks, adapter/tool/settings identity;
  `excluded_directories` and `skipped_paths` record exclusions. Only an existing
  acceptance-fixture `__pycache__` was skipped. Effective target settings are
  `.quality/maintainability.toml` and `.quality/ruff.toml`, with contents and hashes
  in `identity`; targets remain 10/50/5. Tools: Radon 6.0.1, Ruff 0.14.2,
  CPython 3.14.6. Existing CC 13 `repeated_review` is advisory context, not a
  blocker or cleanup obligation for an untouched function.
- Before first edit, the consumer must check logical project, exact included
  inventory/current hashes, tools/checks/effective settings and intended folder
  coverage against this original report. Changed bytes, added/deleted files,
  incompatible identity or uncovered scope require focused reconsideration with
  cause/owner; equal Git short status is insufficient. Do not silently replace B.
- Corrections retain B and every prior JSON/text pair. A scope expansion needs
  authorization and exact verified preserved pre-edit bytes, or an explicit
  historical gap. Root `tests/` and shared runtime are not captured for editing;
  they are reuse/read-only context under this scoped task. Resolve any needed
  expansion before edits there.
- Clone transfer: source paths are the exact absolute repository root plus the
  two pair paths above. At receiving root `<clone>`, explicitly copy them to
  `<clone>/.quality/reports/T-004-preflight-20261104-01.json` and the same `.txt`
  sibling, then validate project/applicability. Ignored reports do not travel in
  commits. Record the concrete receiving root when one is actually selected.

| Native command | Governed scope | Policy / requiredness | Existing owner / stage | Current evidence | Owed duty / recovery |
|---|---|---|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Whole repository policy; CLEAN | AGENTS/development; required before implementation handoff and under existing maintainability review authority | Implementer, then reviewer run/validation | Not rerun for this readiness-only handoff; no claim of current implementation proof | Run on final implementation bytes; hard failure cannot be waived by metrics. |
| `python3 tools/check_contracts.py --root .` | Whole registry/index | AGENTS/development; required structural check | Implementer/designated registry updater; discovery corroborates | Existing records inspected, not executed in preflight | Run at owning handoff; synchronize actual durable deltas at designated stage and regenerate only explicitly. |
| `python3 tools/verify.py` | All maintained suites, registry and active-profile drift | AGENTS/development; required for cross-cutting implementation after focused checks | Implementer; fresh discovery owns its independent targeted/aggregate record | Not run; no aggregate proof reused from historical T-003 | Run at owning stage. Report skips/failures/drift; no active refresh and no inference of agent qualification. |
| `python3 scripts/install_development_skills.py --check .` | Entire managed active profile | Development diagnostic; aggregate constituent | Implementation/aggregate owner | T-003 documents drift; current parity not claimed | Report current drift when checked; use disposable installs for changed projection proof. |
| No additional formatter/lint/typecheck/build/server command | None documented | Project map/development | No new owner | No such native obligation discovered | Invent no new command or gate; analyzer Ruff remains advisory. |

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| No readiness blocker | Implementation may begin within allowed source scope | Implementer | Validate B against current bytes, read the installed implementer workflow and implement T-004 against verification revision 1. |
| Finite cases and future agent decisions unrun | Readiness is not functional or behavioral qualification | Implementer; fresh discovery; separate acceptance | Prepare/reuse every scenario with real inputs and artifact oracles; publish exact focused commands/results and preserve unrun limits. |
| Active install differs from developing source | Do not switch instructions or refresh this run | Coordinator/implementer | Resolve each role from its available installation; use disposable projection for changed source. |
| Budget 20 calls / 55 implementation minutes | Soft sizing checkpoint, not authority to drop evidence | Implementer/coordinator | Return material scope growth to task design; do not truncate required coverage. |

Stop for material authority/scope change, unresolved ownership overlap, changed
starting-evidence applicability or missing indispensable capability. Keep gaps,
owners and recovery visible. On completion follow the existing conditional route:
fresh maintainability review where required, designated registry synchronization,
fresh discovery and separate acceptance. This preflight performs none of those
later stages.
