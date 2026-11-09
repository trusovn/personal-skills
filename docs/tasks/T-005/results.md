# T-005 implementation evidence

Status: READY_FOR_REVIEW; implementation checks complete, independent review remains owed.

## Deliverables and scope

Added `MeasurementTests.test_complete_installed_handoff_retains_original_and_native_history`
in `tests/test_maintainability.py`. It composes the public installed baseline,
implementer comparison, distinct reviewer comparison and correction comparison.
It reuses relocated installation, Git, native-environment and snapshot patterns.
The relocated distribution is deleted before measurement. An unrelated cwd and
the base interpreter force selection of the target's native environment. That
environment receives copies of already pinned packages, without network access.

Only the test and task artifacts are authored here. Existing task index and brief
are user work. No production runtime, skill instructions, plan, task map,
installer-owned resource or active installation was changed.

Readiness: [verification revision 1](verification.md), [preflight](preflight.md).

## Behavioral evidence

Evidence root: `/tmp/T-005-evidence/`. The pinned Python is
`/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`
(Python 3.14.6). Confirmed pins match `scripts/maintainability-requirements.txt`:
Radon 6.0.1, Ruff 0.14.2, mando 0.7.1, colorama 0.4.6, six 1.17.0.

| Verification | Evidence and result |
|---|---|
| V-01 / AC-01 | `journey.log`, `captured-journey.log`: one test passes; B complexity 5, I/R 7, C 6. Separate I/R invocation/output and matching submitted bytes; C differs and still uses B. Complete status, scope, tool/settings identity and installation-local Ruff command asserted. |
| V-02 / AC-02 | Every measurement/native boundary checks source, real index and historical report/evidence bytes. Staged/unstaged/untracked start asserted. `measurement-final.log`: all 34 owning tests pass, no skips; includes empty/add/delete, unknown values, settings, collisions and incompatible/unavailable cases. |
| V-03 / AC-03 | Required whole-project F401 policy, implementer owner. Edited input returns 1 with F401 beside successful comparisons; corrected input returns 0 under identical command/policy. Native records bind checked source hashes, stdout/stderr, result and producer/stage. |
| V-04 / AC-04 | `implementer-fixtures.log`: 2 tests pass. `reviewer-fixtures.log`: 9 tests pass. Existing finite preparations reused without changes; no missing scenario required a new framework. Mapping and qualification route below. |
| V-05 / AC-05 | Focused/structural checks below; aggregate disposition recorded separately. No live actor or independent acceptance claim. |

`fault_control.py` executes an in-memory wrong correction (complexity 5 instead
of 6). `fault-control.log` records the expected assertion failure at the numeric
comparison oracle and a successful control assertion. Repository bytes remain
unchanged. Initial `measurement.log` and initial focused setup errors are retained;
the final passing logs supersede those setup mistakes.

For retained raw journey reports use
`/tmp/T-005-evidence/journey-target/.quality/reports/{B,I,R,C}.{json,txt}`.
`journey-target/I-native.json`, `C-native.json`, `handoff.json`, `AGENTS.md`,
`native-ruff.toml`, source and Git state are copied before fixture cleanup by
`capture_journey.py`. This archive excludes dependency binaries. Paths inside
reports identify the original disposable target; the archive preserves the same
relative paths and exact report bytes. During execution caller handoffs share
the target paths; R is a separate scripted invocation, not independent judgment.
The captured native command and policy remain in the archive, with both failure
and recovery history. The two deliberate edits are the only code changes.

Implementation's own measurement (separate from the target journey):
`/tmp/T-005-evidence/B.{json,txt}` captures tests/ before editing;
`I.{json,txt}` compares tests/test_maintainability.py: complete/compared.
New numeric before/delta values remain unknown. The journey function has 70
statements (target 50), complexity 3; nested capture complexity 10. Retain this
cohesive test because order and immutable shared history are the contract under
proof. Splitting phases into independent tests would lose the composed sequence;
moving its few local helpers into a shared harness would add navigation and
ownership cost without another consumer. No threshold or exclusion was changed.

## Prepared qualification map

I denotes `bounded-task-implementer/evals/files/measurement_cases.json`; R denotes
`task-maintainability-review/evals/files/review_cases.json`, both under
`skills/task-implementation-flow/`. Their existing README files supply executable
setup commands, environment variables, bounded actor requests, read restrictions,
fresh-session requirements and independent grading instructions.

| Plan case | Current owning evidence / prepared cases | Proof limit |
|---|---|---|
| V-001 | Installed journey and full measurement/installer suites | Real local CLI composition only |
| V-002 | Full measurement suite: native boundaries/settings/neutral labels | No agent interpretation proved |
| V-003 | Dirty capture/preservation and empty/add/delete cases; I V-01/V-02/V-03 | Runtime assertions and prepared input only |
| V-004 | New two-edit journey; I V-06; R V-08/V-09 | Correction runtime proved; actor recovery/routing unrun |
| V-005 | I V-04a–k; R V-03a–j, V-04a/b/c, V-05a | Includes 6→8, cohesive breach, materially touched unchanged hotspot, untouched sibling, misleading extraction; judgment unrun |
| V-006 | Runtime missing/incompatible cases; I V-05a–f advisory/required; R V-01 fresh comparison, V-02 faults | Distinct input policies prepared; agent gap handling unrun |
| V-007 | I V-10 including significant/trivial variants; R V-10; existing discovery/acceptance route fixtures | Conditional entry/re-entry prepared, not observed agent choices |
| V-008 | New native failure/recovery journey; I V-08a–j; R V-06a–j | Real failure/recovery and setup histories; missing/unavailable/stale required, aggregate reuse, no-check controls prepared; owner/reuse decisions unrun |

To qualify agents, obtain separate approval for the selected live runtime and
case set, run each independently using its owning setup and fresh actor request,
and preserve raw diff, rationale, disposition, source/report identities, command
and edit order, invocation counts and native history. A separate grader uses
case oracles and withheld input controls. Review actor must run fresh R; setup
R-control or I cannot count. Grade actual artifacts, not keywords or setup exit.
No live agents were executed. Agent compliance remains unqualified.

## Commands and gate ownership

All commands run at repository root. Logs are under the evidence root.

- Pinned Python `-B -m unittest discover -s tests -p test_maintainability.py`:
  34 pass, no skips (`measurement-final.log`). Focused `-k complete_installed`:
  1 pass (`journey.log`).
- With `EVAL_SOURCE_ROOT=$PWD` and `EVAL_MEASUREMENT_PYTHON=<pinned Python>`,
  pinned Python `-B` runs each owning `check_measurement_fixture.py` and
  `check_review_fixture.py`: 2 and 9 pass respectively.
- `python3 -B -m unittest discover -s tests -p test_install_development_skills.py`:
  36 pass (`installer.log`).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`:
  4 pass (`architecture.log`); structural import boundary evidence.
- `python3 tools/check_contracts.py --root .`: 8 subsystems, 26 plan refs pass
  (`contracts.log`); structural registry evidence only.
- `git diff --check`: pass.

## Aggregate result and limits

`python3 tools/verify.py` returned 1 in the sandbox: 7 checks, 2 failed
(`aggregate.log`). Orchestrator containment capability failed (3 failures,
13 errors); the profile drift check also failed. These are failures, not skips.
The exact aggregate command was rerun outside the sandbox with approval.
`aggregate-native.log` returned 1: 7 checks, 1 failed, solely active-profile drift
(112 compared paths, 10 differences: 4 changed, 6 missing). Five suites (537 tests, 32 explicit analyzer skips) and
contracts passed. Default analyzer skips remain unqualified there; the separate
pinned 34-test pass supplies real analyzer proof. Neither aggregate is PASS.

The task explicitly prohibits refreshing this active installation. Report the
drift to independent discovery/acceptance for current contextual admission;
no completion waiver or active-profile qualification is claimed here. All
required implementation commands ran. No dependency repair, live provider or
reviewer-owned gate was executed. Local setup/grading preparation does not prove
agent judgment, check ownership choice, compliance or tamper resistance.

## Contract impact and submission route

Deliverables: installed composition test, preparation/readiness and this evidence.
Actual contract impact: ART-006 gains real complete installed composition authority;
existing measurement/installation/implementer/reviewer records can reference this
test/results while retaining live compliance limits. No executable declarations
changed. Registry synchronization is deliberately left to its designated stage.

Next after implementation checks: fresh maintainability review of the significant
test/harness change → contract-registry updater → fresh independent discovery →
separate acceptance. Architecture proof above is current. Reviewers must admit
aggregate diagnostics and all AC evidence; implementation does not grant acceptance.
