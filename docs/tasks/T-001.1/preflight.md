# Task Preflight: T-001.1 — Portable, target-aware measurement runtime

Status: `ready`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Profile | Guided; executable brief has status `ready`. |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Source brief / revision | [brief.md](brief.md), SHA-256 `e38fb7e8e978aa3b16df91fa0b6d10d2b928d08af7bc2119a51fdd48709d5d83`. |
| Verification / revision | [verification.md](verification.md), revision 1; its repository-relative Source brief declaration and hash match this brief. |
| Authority | [Parent](../T-001/brief.md), [plan](../../project-plan.md), especially section 7, and [review](../../project-plan-review.md). Current plan and task-map hashes match the parent's reviewed identities. |
| Dependencies | No predecessor. Existing launcher, adapter, installer and disposable Git fixtures are present. All five analyzer pins are available in the native interpreter below. |
| Allowed scope | Exactly the brief's allowed paths: launcher; relocation of the two `tools/maintainability*.py` helpers into `scripts/`; flat runtime defaults/pins; owning measurement/installer tests; installer and listed guides/maps. Registry changes belong to the later designated stage. |
| User-work ownership | Existing staged work is confined to nine planning/proposal/experiment documents. Task briefs and verification are untracked user inputs. No implementation/test/installer path is dirty. Preserve all existing work; this invocation creates only this packet. No declared concurrent writer was found. |
| Permissions | Local disposable files and Git subprocesses are available. No downloads, dependency repair, active installation refresh, commits or live checks are authorized by this result. |
| Standalone preflight value | `material`: resolved the unknown exact-pin interpreter, existing real Git/index proof, and reusable disposable-source installation setup. A durable handoff is also required. Recommend standalone preflight for the next task with these same environment/isolation uncertainties. |
| Current applicability | Decision made 2026-10-24 against the revisions above. Reconsider affected readiness if authority, verification, ownership, pins or capabilities change. Ordinary runtime edits and expected new tests do not alone require full rediscovery. |

## Decision context

This runtime serves T-001.2's report changes and later preflight/implementation/
review callers. It must measure separate repositories while preserving their
actual source, index, policy and saved evidence. Wrong resource origin can produce
plausible measurements under the wrong policy; broad refresh can destroy evidence.
Installation-local resources, independent settings fallback, explicit setup and
byte comparisons mitigate these risks. Metrics remain advisory and cannot waive
native hard checks. Neutral report labels and empty-baseline changes remain with
T-001.2; foundation guidance and final aggregate proof remain with T-001.3.

Current contract discovery: [index](../../contracts/index.json),
[installation](../../contracts/installation.json) and
[runtime evidence](../../contracts/runtime-evidence.json). Installation membership
is explicit and narrowly owned; the current membership does not yet include this
runtime. That is planned work, not an absent prerequisite. Optional evidence
capture is not a new required lifecycle. No repository-level known-issues file
was found; there are no recorded deferrals to waive these obligations.

Assumption: local Python/Git behavior is the qualified operating envelope for
this task. Cross-platform qualification and actual network provisioning are not
claimed. No unresolved product decision was identified.

## Acceptance evidence and commands

Run from the repository root. Exact owning commands:

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py
python3 -B -m unittest discover -s tests -p test_install_development_skills.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
```

All are local, without package provisioning. Run changed cases first, then the
owning suites sequentially, then the structural checks before handoff. The
maintainability command must run real native cases without analyzer skips.
Installer success requires actual matching projections and preservation checks,
not just exit status. Architecture and contract checks are structural evidence.
Do not run the aggregate `tools/verify.py` merely for this leaf's reporting.

| AC / scenarios / risk | Authority and decisive proof | Feasibility and planned command | Current evidence / remaining work |
|---|---|---|---|
| AC-01; V-01a/b; R-01 | Brief and plan section 7: real baseline/compare/measure, target-relative reports, exact 2→3 delta, unchanged baseline, local resource origins. | Measurement suite above. Reuse installer `build_relocated_source_distribution`; install from a disposable source, make that source unavailable before execution, clear ambient helper paths, use unrelated cwd. Prepared native interpreter can remain outside that disposable source. Assert resolved resources belong to installed/source `scripts/` as appropriate. | Source-copy fixture exists. New installed runtime proof has not run; current launcher is source-dependent as expected. Cwd change alone is insufficient isolation. |
| AC-01/02; V-02a–d, V-03a–c; R-01 | Independent presence matrix; native counts 5 and 3/1 with effective targets/origins; each malformed family fails; conflicting root Ruff policy has no effect. | Measurement suite; existing policy generators and configured-target case support distinct TOML inputs. Real pinned tools available. All four settings states and both invalid families remain required. | Feasible task-owned extensions, not yet run. Target settings must remain byte-identical. |
| AC-03; V-04, V-05a–f, V-06a/b; R-01 | Actual setup dispatch uses installation pins and target path; all key dimensions separate; selected native interpreter reaches real adapter; pinned caller works; unavailable pins print a parseable target-aware setup command and create nothing. | Measurement suite. Existing environment-key and foreign-venv tests provide seams. Observe `EnvBuilder`/pip calls without downloads for V-04; seed a disposable native environment from prepared local dependencies for V-05f, independently of disposable source. Use an unpinned caller and foreign/legacy sentinels. Use path with spaces and parse/replay diagnostic dispatch under controlled provisioning. | Exact pins confirmed below. Native seeding and new setup/root dispatch tests are feasible future work, not executed proof. No package install is needed or authorized. |
| AC-04; V-07; R-02 | Actual dirty/staged/untracked bytes, native 4/1 baseline and 4→5 comparison, unchanged saved JSON/text, real index and staged content. | Measurement suite; extend existing dirty-snapshot case with before-action byte captures and comparison sequence. | Focused existing snapshot baseline passed, 1 test, no skips. Extended sequence remains unrun. Capture exact pre-edit implementation bytes before any edit/self-measurement; do not reconstruct them later. |
| AC-04; V-08a–e; R-02 | Preserve native thresholds, symbol identity/duplicates, Ruff collection/exemptions, unknown `null` counts, asset groups and exclusions. | Measurement suite; existing boundary, nested/duplicate, Ruff-native/missing-count and exclusion cases provide reusable scenarios. | Real tools executable; all preserved cases must run after relocation. This preflight did not execute the full suite. |
| AC-04; V-09a–f; R-02 | Partial profile is truthful; missing tool/invalid Python/concurrent change remain incomplete; incompatibilities retain reasons; affected added/deleted scope and valid/escaping paths retain semantics. | Measurement suite; existing partial, compatibility, mount, concurrent-change, scope and CLI cases. Add missing CLI failure assertions within owner tests. | Feasible without external dependencies; future exit 0/2 wiring and retained-record assertions have not run. |
| AC-04/05; V-10a/b; R-02 | Occupied JSON or sibling text refuses publication, exit 2, preserves both formats byte-for-byte. | Measurement suite; extend existing no-overwrite CLI coverage with sibling-only and comparison cases. | Feasible disposable filesystem proof; unrun extensions. |
| AC-05; V-11, V-12a/b; R-02 | Fresh install/refresh in committed and unborn targets; every new resource independently changed/missing; precise repeated read-only drift, explicit repair, complete ownership preservation. | Installer suite above. Existing snapshots, refresh/drift journey, unmanaged AGENTS line-ending and committed/unborn cases are reusable. Enumerate completed distribution membership rather than sampling file families. | Fixtures inspected; no shared helper changes are required. Extend target policy/env/report/source/index sentinels and all-file coverage in allowed test file. New cases not run. |
| AC-01/05; V-13 | Installer constants, guide, README, tool documentation and relocation maps agree; one shipped-default source, target policy separate, pins installation-owned. | Review allowed documents/constants, supported by both owning suites. | Current `SHARED_SCRIPT_FILES` is explicit and narrow. Synchronize declarations and focused expectations; text review alone does not prove portability. |

### Executed readiness probe

The prepared interpreter is:
`/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`.
It reports CPython 3.14.6 and exact versions `radon==6.0.1`, `ruff==0.14.2`,
`mando==0.7.1`, `colorama==0.4.6`, `six==1.17.0`, matching current requirements.
The ordinary caller is unpinned, which supplies the missing-pin/selection fixture.

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py -k snapshot_preserves
```

Result: exit 0; one real-analyzer test passed in 0.155 seconds, no skips.
It exercises real Git staged/unstaged/untracked capture and real index bytes.
No broad baseline was needed. This establishes environment feasibility, not
acceptance of future behavior.

Required handoff checks also passed: architecture, 4 tests with no skips;
contract validator, 5 subsystems and 0 indexed plan references. These establish
current structural consistency only. Re-run affected checks after implementation.

## Warnings, stops and next action

No current blocker. Stop if an indispensable real-tool proof becomes unavailable,
ownership overlaps another writer, authority changes, generic installer behavior
is needed, or dependency repair/download is required. Obtain the applicable
authorization before repair; do not tune pins or settings to reduce metrics.
Never refresh the active `.agents/` installation during this run.

Next action: invoke `bounded-task-implementer` on `docs/tasks/T-001.1`, capture exact
pre-edit source bytes before editing, and implement only this leaf. Preserve the
subsequent maintainability review → registry update → fresh discovery → separate
acceptance decision route. No implementation or independent acceptance occurred
in this preflight.

## Implementer handoff

```text
T-001.1 is ready under guided preflight, brief hash
e38fb7e8e978aa3b16df91fa0b6d10d2b928d08af7bc2119a51fdd48709d5d83,
verification revision 1. Preserve existing staged docs and untracked task inputs.
Implementation paths are currently clean. Use the exact pinned Python and owning
commands above; the real snapshot readiness probe passed with no skips.
Reuse disposable-source installer and byte-snapshot fixtures. Installed runtime
proof must make the disposable source unavailable, keep prepared native tools
independent, exclude ambient helpers, and observe actual origins and native values.
Seed native selection locally; observe setup provisioning calls without downloads.
New V-01–V-13 obligations remain implementation verification, not passed evidence.
Next: bounded-task-implementer on docs/tasks/T-001.1; capture exact pre-edit bytes
first, implement within the brief, then run focused/owning gates sequentially.
Stop on required dependency repair, lost real-tool proof, ownership conflict or
scope expansion. Do not refresh the active installation or run the aggregate gate.
```
