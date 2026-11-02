# T-001.2 discovery 02 — staged correction evidence

Producing stage: task-review-discovery. Coverage: complete within T-001.2's local qualification envelope. Independent correction discovery; this session authored no reviewed production, tests or harness bytes. No acceptance verdict, approved deferral or advancement is recorded. This report applies only to the identities below and does not review or authenticate itself.

## Authority, submission and scope

Authority: `docs/tasks/T-001.2/brief.md`; `verification.md` revision 1; ready `preflight.md`, including Decision context; parent T-001 brief and accepted T-001.1 dependency. Current submission: `implementation.md` (READY_FOR_REVIEW), with producer-attributed commands, fail-first history and scenario map. Conditional context: `reviews/discovery-01.md`, `reviews/acceptance-01.md`, `reviews/maintainability-01.md`. Prior reports are historical evidence and are not rewritten.

All 11 staged paths below are explained: adapter/guide/tests implement T-001.2; preparation, submission and review files record its stages; measurement registry/index correct prior F-01. No unstaged tracked work is present. SIDE-001 is absent from the current staged diff and is outside qualification. Runtime/test/guide index blobs match discovery-01 exactly; HEAD and total diff differ because the baseline and evidence/reference set changed. Explicit current index identities are recorded below rather than inferred from worktree equality.

Installer selections, skills profile guide and README references were inspected. No resource name, dependency or managed membership changed; no installer modification or conditional installer-suite obligation is introduced. No installation was refreshed.

## Findings

No findings.

Prior F-01 [P2], stale measurement discovery: current record explicitly declares format-5 neutral changes and empty-start capture, separates caller workflow obligations and T-001.3 composition, and supplies ART-002 routing in the generated index. Static comparison to actual adapter/CLI behavior plus C4 confirms current correction evidence for its invariant and sibling surface. This is evidence for the separate decision call, not a finding-closure verdict. H-01/H-02/H-03 remain visible below.

## Completeness ledger

Every row is required. All prior V rows were pass; current results below are independently corroborated on current bytes. Submitted evidence for V-01–V-09 is the implementation scenario map and corresponding staged tests; V-10 uses the submitted guide. C1 is the targeted MeasurementTests execution, C2 the separate adversarial CLI probe, C5 the owning suite. Setups use real pinned Radon/Ruff and disposable filesystem/Git state. Test assertions were inspected before execution; no expected values were derived by calling the comparison algorithm.

| Stable row / AC | Explicit cases, setup and oracle | Current independent evidence | Result |
|---|---|---|---|
| V-01a–q / AC-01 | Complexity 2→3, 9→10, 10→11, 12→11, 11→11, 11→12; statements 20→25, 49→50, 50→51, 51→50, 51→52; arguments 3→4, 4→5, 5→6, 7→6, 6→5, 6→7. Real native values; exact signed delta, neutral classification, crossing only across target. | C1 numeric boundary/native tests | pass |
| V-02a–e / AC-01,04 | Add/remove/rename/extract, duplicate identities, nested/local-class/async line shifts. Unknown values and interpretation remain; distinct stable identities match. | C1 symbol/nested-scope tests and renderer trace | pass |
| V-03a–i / AC-01,04 | Argument unknown↔1; statement unknown↔1; override/overload unknown↔6; identical messages on different symbols. Both directions retain native unknowns, exemptions, and interpretation. | C1 real native missing-diagnostic/exemption tests; noqa coverage retained | pass |
| V-04 / AC-01 | Public baseline/edit/compare, saved JSON/text and console, at/above-target growth, decrease and new hotspot. Complete observations exit 0 with factual labels. | C1 saved/console and standalone tests; static numeric_change/render trace | pass |
| V-05a–j / AC-02 | Valid control; old formats 3/4; incompatible tools, real effective settings, collection identity, adapter, implementation/major-minor runtime, incomplete evidence and uncovered scope. Compatible moved-root/patch controls retained. | C1 public CLI valid/invalid consumer checks; C2 independent format-4 refusal | pass |
| V-06 / AC-03–05 | Explicit empty area capture; add then edit twice against original baseline; known covered absence, unknown numeric before/delta, original reports/source/index preserved. | C1 empty-folder Git journey; C2 separate native complexity 5 then 8 against one original baseline | pass |
| V-07a–d / AC-02,03 | Ordinary empty measure, missing parent, explicit excluded parent, uncovered addition all fail. Existing explicit empty folder is success control. | C1 empty-folder/exclusion tests; static validation order before empty allowance | pass |
| V-08 / AC-04,05 | Staged plus unstaged edits, untracked source, untouched sibling, affected subset/addition/deletion; original reports, actual source/index bytes and staged blob preserved. | C1 Git snapshot/subset tests; C2 independently deletes captured complexity-8 file and observes removed/8/unknown | pass |
| V-09a–f / AC-05 | baseline/compare/measure × JSON-only/text-only occupied destinations; sentinel unchanged and absent sibling stays absent; fresh successes elsewhere. | C1 all six collision cases and both-present case; C2 independent text-only collision | pass |
| V-10 / AC-02 | Format 5, prior-format refusal, safe exact pre-edit recovery, explicit empty-parent capture, fresh output names and unknown values; installer/reference inspection. | Static guide, README/profile and installer inspection | pass; guidance evidence, not executed recovery |
| H-01 / submission | Prior blocked: missing scenario map/fail-first history. Producer now supplies commands and scenario map in implementation.md. | Inspected handoff and matched named scenarios to tests/current C1/C5. Historical fail-first remains producer-attributed, not independently authenticated. | pass for supplied submission evidence |
| H-02 / conditional review | Prior blocked: absent independent maintainability record. | maintainability-01 identifies same runtime/test/guide blobs and independent provenance, architecture result and semantic analysis. C3 corroborates current architecture. | pass for current required review artifact; no new maintainability verdict issued |
| H-03 / registry; F-01 | Prior fail: current capability contradicted by registry; sibling index routing stale. | Current measurement summaries agree with adapter, guide and C1/C2; ART-002 maps to measurement; C4 validates structural agreement. | pass for current correction evidence |

No executable JSON Schema is declared for measurement reports. Compatibility is an executable runtime boundary, exercised with valid and deliberately invalid reports by C1/C2. Registry validation is structural evidence and is not used as proof of measurement behavior. No process-lifecycle contract is changed or qualified.

## Independent commands and probes

CWD: repository root. P = `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`. No dependencies installed, network/live check or privileged probe run.

- C1: `P -B -m unittest discover -s tests -p test_maintainability.py -k MeasurementTests` — exit 0, 29 tests, no skips, 11.661 s. Targeted behavioral coverage across frozen V-01–V-09 ledger before owning-suite gate.
- C2: `P -B -` with independent disposable-root public CLI probe. Exact reproducible procedure: use TemporaryDirectory; create area/; invoke `P scripts/measure_maintainability.py <args> --root <temp>` with capture_output and timeout=20 for every call. `baseline area --output b.json`; save b bytes. Write area/f.py as `def f(x):` plus four `if x: pass` lines; `compare area/f.py --baseline b.json --output c4.json`; repeat with seven branches to c7.json. Assert each parsed single complexity row has (value,before,delta,classification)=(5,None,None,new), then (8,None,None,new). `baseline area --output nonempty.json`; unlink f.py; `compare area/f.py --baseline nonempty.json --output deleted.json`; assert removed row before=8/current=None. Seed occupied.txt=sentinel; compare same deleted path to occupied.json and require exit 2, no JSON and intact text. Restore f.py with return-only body; copy b to old.json with format_version=4; compare area against old and require exit 2 with `report format differs`. Assert b bytes unchanged. All assertions passed. Context cleanup removed fixture; every synchronous child returned with captured pipes closed. This is measurement history evidence, not process-lifecycle qualification.
- C3: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — exit 0, 4 tests, no skips. Structural only.
- C4: `python3 tools/check_contracts.py --root .` — exit 0; 6 subsystems, 8 indexed refs. Structural only; semantics separately traced for H-03.
- C5: `P -B -m unittest discover -s tests -p test_maintainability.py` — exit 0, 32 tests, no skips, 14.256 s. Current reviewer-owned required owning-suite gate, after C1/C2 and full ledger reconciliation; no selected adversarial row left pending.
- Static: `git diff --cached --check` and `git diff --exit-code` — exit 0. Inspected cached diff, task/preparation/review records, runtime, tests, guide, installer/profile/README and registry. Status, HEAD, index blob and diff SHA-256 reads recorded below. An unnecessary `git write-tree` identity attempt was denied creating index.lock; no tree identity was obtained and no state changed. Read-only index blob identities are used instead.

## Aggregate gate

`python3 tools/verify.py`: not run, final aggregate composition owner T-001.3 per explicit brief/verification design. C5 is the T-001.2-required owning-suite gate, owned by this correction discovery after clean targeted evidence. No new gate added. C3/C4 do not waive independent stage duties.

## Residual scope and next route

No blocked/unchecked required row remains. Fail-first history is supplied as an implementer claim; this session does not authenticate past sessions or report provenance. Installed composition, broader host support, workflow enforcement of pre-edit retention and live agent judgment remain outside T-001.2 qualification; T-001.3/later workflow owners retain those duties. Historical reports correctly describe earlier missing evidence and are preserved. The handoff's stale-registry wording records its earlier stage, while current registry bytes are evaluated above.

Next: separate task-acceptance-review consumes the brief, current staged diff, this report, verification revision 1, preflight/Decision context, implementation handoff, prior discovery/acceptance and maintainability report. No reviewer regression file was added; current regression commands are C1/C2/C5.

## Discovery continuation

- Iteration / current byte identity: correction discovery 02; HEAD and cached-diff digest below; worktree equals index; per-path blobs below.
- Coverage rows: V-01a–q, V-02a–e, V-03a–i, V-04, V-05a–j, V-06, V-07a–d, V-08, V-09a–f, V-10 = prior pass → current pass. H-01/H-02 = prior blocked → current pass for supplied evidence; H-03 = prior fail → current pass for correction evidence.
- Finding IDs: prior F-01 [P2], current correction evidence H-03; no new finding. Separate acceptance owns disposition.
- Continuity: producer claims in implementation.md; current independent evidence C1–C5 and static traces. No incomplete required row. Correction owner registry updater for F-01 if further correction needed; evidence owners original implementer H-01, independent maintainability reviewer H-02, registry updater/current discovery H-03; task owner retains authority for all rows. Influenced sibling is generated index ART-002 routing and downstream T-002/T-003 discovery.
- Preparation/context: T-001.2 brief; verification revision 1; ready preflight including Decision context; parent T-001 authority and accepted T-001.1; discovery-01, acceptance-01, maintainability-01, implementation.md.
- Reviewer regressions: no added files; exact focused commands C1/C5 and reproducible C2 above.
- Aggregate: tools/verify.py not run, T-001.3 owner; current C5 owning suite passed after clean targeted reconciliation.
- Next: fresh separate task-acceptance-review with this full packet; no advancement by discovery.

## Reviewed identity and write audit

Created: 2026-11-02T15:02:58.468282+00:00

HEAD: `f5a6ac2a7adee20db534f72319d5f3b1546cfdc2`

Cached-diff SHA-256: `331d6a78e01d92071a8369a1e1c4841b7ae9b4b85d52845d6c4f930d45f83978`

Index blobs:
```text
100644 993275e29b9d650f156921f3dab58d311e6e00c3 0	docs/contracts/index.json
100644 a450062102e33f81ac71d495ec2cc990d2e6dcd9 0	docs/contracts/measurement.json
100644 01c4f9bbbb725ef43ef01a07f61f988acbaec0c0 0	docs/tasks/T-001.2/implementation.md
100644 276ce0a2937d8c010c49bad6b2a4cf4ea42122f6 0	docs/tasks/T-001.2/preflight.md
100644 40750452d77eaad078bef696eb2faff588b666e0 0	docs/tasks/T-001.2/reviews/acceptance-01.md
100644 05815db9110c87f6a958fcbd5e0c9ad0ad7b1d4d 0	docs/tasks/T-001.2/reviews/discovery-01.md
100644 5d9d2feb19b27e08c5fb971405e9af33c966785e 0	docs/tasks/T-001.2/reviews/maintainability-01.md
100644 16033d21ee53cf2181325f65b869aebf798b81b4 0	docs/tasks/T-001.2/verification.md
100644 4c709e412afe2d043767cd6e9dea2eb2f64bb1fa 0	scripts/maintainability.py
100644 37f98743fc11f8e521e613a57e37df0a03ae77b0 0	scripts/measure-maintainability.md
100644 4fad79cd50878726920ec0fe98e15e4cf0dd3140 0	tests/test_maintainability.py
```

Exact status before write:
```text
M  docs/contracts/index.json
M  docs/contracts/measurement.json
A  docs/tasks/T-001.2/implementation.md
A  docs/tasks/T-001.2/preflight.md
A  docs/tasks/T-001.2/reviews/acceptance-01.md
A  docs/tasks/T-001.2/reviews/discovery-01.md
A  docs/tasks/T-001.2/reviews/maintainability-01.md
A  docs/tasks/T-001.2/verification.md
M  scripts/maintainability.py
M  scripts/measure-maintainability.md
M  tests/test_maintainability.py
```

Exact status after write:
```text
M  docs/contracts/index.json
M  docs/contracts/measurement.json
A  docs/tasks/T-001.2/implementation.md
A  docs/tasks/T-001.2/preflight.md
A  docs/tasks/T-001.2/reviews/acceptance-01.md
A  docs/tasks/T-001.2/reviews/discovery-01.md
A  docs/tasks/T-001.2/reviews/maintainability-01.md
A  docs/tasks/T-001.2/verification.md
M  scripts/maintainability.py
M  scripts/measure-maintainability.md
M  tests/test_maintainability.py
?? docs/tasks/T-001.2/reviews/discovery-02.md
```

Only the new report entry may differ.
