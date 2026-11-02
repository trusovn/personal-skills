# T-001.2 discovery report — neutral reports and empty-start baselines

Created: 2026-11-02T13:06:52.244397+00:00

Producing stage: task-review-discovery. First independent pass.
Coverage: complete for T-001.2 behavioral rows; preparation-stage and submission gaps remain below. No acceptance verdict, approved deferral or advancement is recorded.

## Provenance and reviewed identity

This session authored no reviewed production bytes. The user identified staged data as the scope. HEAD: `aa82c406d17f6a0edb8a0473aa4416e97cb245dd`. SHA-256 of `git diff --cached`: `252e6a20bb6b60b6f0960311a59d76992e5d2e6ce0c36c7786ab3b0a94d96811`.
`git diff --exit-code` passed: tracked worktree bytes equal index bytes. Separate index blob identities follow. No index changes were made.

```text
100644 5479d9745f1e0191aaa1cfc547eb2c8e1dd09539 0	docs/tasks/SIDE-001/brief.md
100644 276ce0a2937d8c010c49bad6b2a4cf4ea42122f6 0	docs/tasks/T-001.2/preflight.md
100644 16033d21ee53cf2181325f65b869aebf798b81b4 0	docs/tasks/T-001.2/verification.md
100644 4c709e412afe2d043767cd6e9dea2eb2f64bb1fa 0	scripts/maintainability.py
100644 37f98743fc11f8e521e613a57e37df0a03ae77b0 0	scripts/measure-maintainability.md
100644 4fad79cd50878726920ec0fe98e15e4cf0dd3140 0	tests/test_maintainability.py
```

Authority: `docs/tasks/T-001.2/brief.md`, `verification.md` revision 1 (brief hash recorded there), `preflight.md` including its Decision context, parent `docs/tasks/T-001/brief.md` and measurement contract. No prior discovery report exists. No implementation summary, fail-first record, scenario map, maintainability review or registry-updater result was supplied or present in this task package. Tests are submitted assets, not prior passing claims. Current evidence below was executed by this reviewer.

## Findings

No findings. No demonstrated runtime violation was found in T-001.2's scoped implementation.

## Completeness ledger

All rows are required. Commands D1–D6 and setup are recorded below. Existing staged tests were inspected before execution. Case IDs preserve verification revision 1's identities.

| Row / AC | Explicit cases and setup / oracle | Submitted assets | Independent current evidence / result |
|---|---|---|---|
| V-01a–q / AC-01 | Real source with complexity 2→3, 9→10, 10→11, 12→11, 11→11, 11→12; statements 20→25, 49→50, 50→51, 51→50, 51→52; arguments 3→4, 4→5, 5→6, 7→6, 6→5, 6→7. Signed deltas, equality within target, crossings only on transition. | Numeric boundary tests | D2 real pinned analyzer tests; pass. |
| V-02a–e / AC-01,04 | Add/remove/rename/extract; duplicate qualified names; nested/local-class/async identities after line shifts. Unknown deltas and interpretation for unmatched identities. | Symbol and console tests | D2 symbol traces and assertions; pass. |
| V-03a–i / AC-01,04 | Argument count unknown↔1; statements unknown↔1; override/overload exemptions unknown↔6; identical messages on distinct symbols. No fabricated zero; interpretation retained. | Native missing-diagnostic and exemption tests | D2 runs both real source states; comparison checks both directions. Pass. Native noqa/exemption coverage retained. |
| V-04 / AC-01 | Real CLI baseline and edit with at-target increase, above-target increase, decrease and new hotspot. JSON, saved text and console neutral; standalone breach exits 0. | saved_and_console_reports_use_neutral_labels, console tests | D2 CLI assertions and numeric_change/summary static trace; pass. |
| V-05a–j / AC-02 | Compatible control; formats 3/4; changed tools, settings, collection limits, adapter, runtime; incomplete report; uncovered scope. Real settings edits; compatible moved-root/patch controls. | Compatibility tests | D2 CLI rejection and component cases pass; D3 separately rejects format 4. Missing collection identity additionally checked at comparison boundary. No executable JSON Schema contract is declared; JSON is consumed by runtime compatibility checks. |
| V-06 / AC-03–05 | Explicit empty area baseline; add file then edit again; compare twice against original. Known absence, unknown numeric before/delta; unchanged original reports/source/index. | empty_folder_baseline test | D1 and D2 pass; D3 separately uses complexity 4 then 9 and confirms original baseline unchanged. |
| V-07a–d / AC-02,03 | Ordinary empty measure, missing parent, excluded parent, uncovered new file. Exit 2 with no successful comparison. | Empty-folder and exclusion tests | D1/D2 pass; static discover trace confirms checks precede empty allowance. |
| V-08 / AC-04,05 | Real Git staged edit plus later unstaged edit and untracked file; untouched sibling excluded from subset; covered addition; delete captured file; compare again against original. | snapshot and folder comparison tests | D2 pass: real index bytes, staged blob, source snapshots and earlier report pairs preserved. D3 additionally deletes captured complexity-9 file and observes removed/9/unknown. |
| V-09a–f / AC-05 | Baseline/compare/measure × JSON-only/text-only sentinels; absent sibling remains absent; source/index unchanged. Fresh success controls in V-04,06,08. | each_report_sibling_collision_refuses_write and existing collision test | D2 passes all six and both-present cases; D3 separately verifies text-only collision. |
| V-10 / AC-02 | Format 5 and neutral fields; old-format refusal; safe pre-edit recovery; explicit existing empty folder coverage; original baseline and fresh comparison filenames; native unknowns. | scripts/measure-maintainability.md | Static review pass. Installer SHARED_SCRIPT_FILES already includes adapter; no names/dependencies changed. README links guide; installer/profile selection needs no change. This is guidance evidence, not executed recovery qualification. |

## Probe and command record

CWD for all commands: repository root. Pinned Python (`P` below): `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`. No packages installed or network probes run.

- D1: `P -B -m unittest discover -s tests -p test_maintainability.py -k empty_folder` — exit 0, 1 test, no skips.
- D2: `P -B -m unittest discover -s tests -p test_maintainability.py -k MeasurementTests` — exit 0, 29 tests, no skips. Targeted behavioral coverage, not a repository aggregate.
- D3: independent `P -B -` CLI probe with `TemporaryDirectory`, public `scripts/measure_maintainability.py`, `--root <temp>`, each subprocess timeout 20 seconds. Reproduce: create `area/`; baseline to `b.json`; write `area/f.py` with `def f(x):` and 3 then 8 `if x: pass` lines; compare each against b to c3/c8; assert unknown before/delta and native complexity 4/9. Seed `occupied.txt` with sentinel; compare output occupied.json must exit 2 with no JSON and unchanged text. Capture nonempty.json; delete f.py; compare deleted path to deleted.json; assert removed/9/unknown. Copy b.json to old.json with format_version=4, restore valid f.py, compare area against old.json; assert exit 2 and format diagnostic. Assert b.json byte-identical. All assertions passed. Temporary state removed by context manager; synchronous CLI subprocesses returned. No process-lifecycle contract is changed or claimed.
- D4: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — exit 0, 4 tests. Structural evidence only.
- D5: `python3 tools/check_contracts.py --root .` — exit 0, 6 subsystems, 7 indexed refs. Structural agreement does not establish semantic registry freshness.
- D6: `P -B -m unittest discover -s tests -p test_maintainability.py` — exit 0, 32 tests, no skips, after targeted reconciliation. Owning-suite gate, reviewer-owned; all selected targeted cases clean before launch.
- Static commands: `git diff --cached --check` and `git diff --exit-code` — exit 0; staged adapter, guide, test diff and package documents inspected; installer selections and README references inspected. Neither command is behavioral evidence.

## Aggregate gate

`python3 tools/verify.py`: not run. T-001.3 owns final aggregate composition proof per brief. No additional aggregate introduced. D6 is the task-required owning suite, owned by this initial discovery pass after clean targeted evidence. Architecture/contract structural checks passed independently; they waive no review-stage duties.

## Scope and unresolved handoff evidence

The six staged paths are the user-selected scope. Adapter, measurement guide, tests and T-001.2 preparation artifacts map to this task. `docs/tasks/SIDE-001/brief.md` defines a separate skill-presentation task. It is preserved and explicitly outside T-001.2 behavioral qualification; no SIDE-001 implementation is present or reviewed. User scope authorization does not make its separate task criteria T-001.2 criteria.

The measurement registry still says neutral labels and empty capture remain future work. The task assigns synchronization to a separate registry-updater stage; this report does not change it or treat structural validation as synchronization. No maintainability review result is in the package. Evidence owners: implementer supplies scenario/evidence and fail-first records; maintainability reviewer owns its separate review; registry updater owns current contract synchronization; acceptance caller verifies required stage order. These are handoff gaps, not demonstrated runtime defects or approved deferrals. Installed composition remains T-001.3's obligation. No live agent behavior is qualified.

## Status preservation

Exact status before report write:
```text
A  docs/tasks/SIDE-001/brief.md
A  docs/tasks/T-001.2/preflight.md
A  docs/tasks/T-001.2/verification.md
M  scripts/maintainability.py
M  scripts/measure-maintainability.md
M  tests/test_maintainability.py

```
Exact status after report write:
```text
A  docs/tasks/SIDE-001/brief.md
A  docs/tasks/T-001.2/preflight.md
A  docs/tasks/T-001.2/verification.md
M  scripts/maintainability.py
M  scripts/measure-maintainability.md
M  tests/test_maintainability.py
?? docs/tasks/T-001.2/reviews/discovery-01.md
```
Only the new report entry may differ. Report applies to the bytes above and does not review or authenticate itself.

## Discovery continuation

- Iteration / identity: first independent pass; HEAD and staged-diff SHA-256 above; separate index blobs recorded; tracked worktree equals index.
- Coverage: V-01a–q, V-02a–e, V-03a–i, V-04, V-05a–j, V-06, V-07a–d, V-08, V-09a–f, V-10 = pass under the stated boundaries. No blocked/unchecked T-001.2 behavioral row.
- Finding IDs: none; no prior finding/scenario continuation supplied.
- Continuity: current reviewer evidence D1–D6; no producer passing record supplied. Separate correction owner: implementer if corrections arise; evidence owners: maintainability reviewer and registry updater for missing stages; authority owner: task owner. SIDE-001 is not qualified. No sibling runtime defect confirmed.
- Preparation/context: brief; verification revision 1; preflight and its Decision context; current staged diff; this report. Missing submission and conditional-stage results remain explicit above.
- Reviewer regressions: no new test files; D1–D3 reproduce decisive behavior; D6 is exact owning-suite command with P expanded above.
- Aggregate: repository aggregate not run; T-001.3 owns it. D6 owning suite passed, initial discovery reviewer owned, targeted reconciliation clean.
- Next: separate task-acceptance-review call with this report, brief, current staged diff, verification revision 1, preflight/context, command records and the missing-stage/submission gaps. That caller decides the route; discovery does not advance work.
