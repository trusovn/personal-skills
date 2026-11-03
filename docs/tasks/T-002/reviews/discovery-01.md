# Task Review Discovery Report: T-002 — Starting code handoff

- Producing stage: task-review-discovery; first independent discovery.
- Created: 2026-11-02T23:05:19.459658+00:00.
- Coverage: complete for T-002's guidance and executable-eval preparation boundary. Live agent compliance remains unqualified; it is expressly not a required execution claim in this task.
- Repository: /Users/mtrusov/work/skill-sources/personal-skills.
- Report: docs/tasks/T-002/reviews/discovery-01.md.
- Authority: docs/tasks/T-002/brief.md revision 1, verification.md revision 1, preflight.md, implementation.md (READY_FOR_REVIEW); maintainability-01.md supplies prior structural review context, not functional proof.

Evidence only: no acceptance decision, approved deferral or advancement. This report applies only to the identified staged bytes and does not review or authenticate itself.

## Provenance and scope

This session authored no reviewed production bytes. All staged paths are reviewed; task-package/index preparation is pre-existing user work. Implementation consists of the four preflight source files; README and measurement registry changes document that producer boundary. No unstaged tracked changes existed. Worktree and index bytes match, so local probes exercise the staged implementation. Active project-local discovery/testing skills were used; reviewed source preflight instructions were treated as development specifications. No installation was refreshed.

HEAD: `7b7c71ade301db9ae39b5966de0b1738599f5c8e`. Index tree: `073da7eaafbc2e13d7e69e716c3555d40166bce8`.

Exact staged blob identities:

```text
100644 c401b476d3220e3f2f1b9ac757e36815756d158c 0	docs/contracts/index.json
100644 0e0986ff896729fb0c170e1c3351aee4bc331a92 0	docs/contracts/measurement.json
100644 d1bfb3e78e35bf96941818c3f80b893db5494ce7 0	docs/tasks/T-002/brief.md
100644 5891937a854b86fc468149fa4b9fe1b36325900c 0	docs/tasks/T-002/implementation.md
100644 38708f08216190f54645f0ecd36c72d010beb704 0	docs/tasks/T-002/preflight.md
100644 eb379390891027d5de9cbfd63ded7f0351950ec9 0	docs/tasks/T-002/reviews/maintainability-01.md
100644 e650b5ea3224df92a25c76917fcef1157b4df7e2 0	docs/tasks/T-002/verification.md
100644 cfa8d12ec2cafe5b3c1fe85d631bcf0d5b36dc52 0	docs/tasks/index.json
100644 9c69d31e390b01071f31e8370b3fa61bf091cda5 0	skills/task-implementation-flow/README.md
100644 2ff66a549ea99027cd43dcd0d6158b331aabc969 0	skills/task-implementation-flow/task-preflight/SKILL.md
100644 135f014528140a75e0460d8e5b5667a815f23833 0	skills/task-implementation-flow/task-preflight/evals/evals.json
100644 729322387660a662f504be16a6e12f0c5fd85583 0	skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py
100644 05a3796feed64957d9202f0dc211539405257318 0	skills/task-implementation-flow/task-preflight/references/execution-packet-template.md
```

## Findings

No findings.

## Completeness ledger

Each pass below concerns the task-authorized **prepared outcome**, not an agent readiness decision. Submitted evidence is implementation.md's scenario map and limits. The independent setup supplies each row's actual files/policy; its producer-input.json states the oracle. Static traces checked the new seven-step producer guidance, both-profile template, sequencing with existing high-assurance freshness, and eval 13's grading requirements. DISC-03 corroborates reusable runtime boundaries; it cannot establish agent obedience.

| Row | Authority | Explicit cases / oracle | Setup | Submitted evidence | Independent probe | Result |
|---|---|---|---|---|---|---|
| V-01 | AC-01; AC-05 preparation | Capture all five asset folders, actual dirty/untracked bytes; preserve index/exclusions/unrelated. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-02a | AC-01; AC-05 preparation | Capture existing empty parent; empty inventory, no numeric zero. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-02b | AC-01; AC-05 preparation | Capture empty parent, then permitted probe adds Python; compare as new with unknown before/delta. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-02c | AC-01; AC-05 preparation | Missing parent: evidence gap, no fabricated parent. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-02d | AC-01; AC-05 preparation | Excluded vendor parent: evidence gap, exclusion retained. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-03a | AC-01; AC-05 preparation | JSON-only collision retained; choose fresh pair; successful control. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-03b | AC-01; AC-05 preparation | Text-only collision retained; choose fresh pair; successful control. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-03c | AC-01; AC-05 preparation | Both siblings retained; choose fresh pair; successful control. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-04a | AC-02; AC-05 preparation | Guided exact pair and report facts, compact applicability. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-04b | AC-02; AC-05 preparation | High assurance exact pair and unchanged full freshness duties. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-05a | AC-02; AC-05 preparation | Unchanged project/inventory/identity: original applicable. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-05b | AC-02; AC-05 preparation | Same MM text, changed hash: focused reconsideration. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-05c | AC-02; AC-05 preparation | Added included file: detect inventory mismatch. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-05d | AC-02; AC-05 preparation | Deleted captured file: detect inventory mismatch. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-05e | AC-02; AC-05 preparation | Different logical project: reject original applicability. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-05f | AC-02; AC-05 preparation | Incompatible tools: gap and focused reconsideration. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-05g | AC-02; AC-05 preparation | Incompatible effective settings: gap and focused reconsideration. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-05h | AC-02; AC-05 preparation | Added folder outside coverage: authorized resolution needed. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-06a | AC-02; AC-05 preparation | Correction: retain original, never recapture edited start. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-06b | AC-02; AC-05 preparation | Added scope: exact preserved bytes available; authorization then added evidence. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-06c | AC-02; AC-05 preparation | Added scope: no preserved bytes; explicit before gap. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-07 | AC-02; AC-05 preparation | Separate clone: transfer exact ignored pair; no silent recapture. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08a | AC-03; AC-05 preparation | Docs only: N/A, native duties retained. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08b | AC-03; AC-05 preparation | Unsupported language: N/A, native duties retained. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08c-A | AC-03; AC-05 preparation | Absent launcher: advisory gap, ready otherwise. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08c-R | AC-03; AC-05 preparation | Absent launcher: indispensable entry evidence, blocked; capability owner recovery. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08d-A | AC-03; AC-05 preparation | Missing original: advisory gap, ready otherwise. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08d-R | AC-03; AC-05 preparation | Missing original: indispensable entry evidence, blocked; capability owner recovery. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08e-A | AC-03; AC-05 preparation | Incompatible tools: advisory gap, ready otherwise. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08e-R | AC-03; AC-05 preparation | Incompatible tools: indispensable entry evidence, blocked; capability owner recovery. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08f-A | AC-03; AC-05 preparation | Partial upstream report, Ruff unavailable: advisory gap, ready otherwise. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-08f-R | AC-03; AC-05 preparation | Partial upstream report, Ruff unavailable: indispensable entry evidence, blocked; capability owner recovery. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-09a | AC-04; AC-05 preparation | Registry native command/policy/scope/owner retained. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-09b | AC-04; AC-05 preparation | No registry: documented native command suffices. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-09c | AC-04; AC-05 preparation | No native command: record none, invent no checker. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-10a | AC-04; AC-05 preparation | Current aggregate covers command/scope/policy/bytes: reuse without rerun. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-10b | AC-04; AC-05 preparation | Later-stage missing evidence remains owed; ready otherwise. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-10c | AC-04; AC-05 preparation | Stale byte identity: reject reuse, later owner duty retained. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-10d | AC-04; AC-05 preparation | Aggregate omits native command: reject constituent reuse. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-10e | AC-04; AC-05 preparation | Entry native F401 failure blocks despite advisory success. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-10f | AC-04; AC-05 preparation | Entry native unavailable blocks despite advisory unavailability. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-10g | AC-04; AC-05 preparation | Entry native unavailable blocks despite measurement N/A. | DISC-01/02 supplied row; oracle in producer-input.json | Submission scenario map | DISC-01/02, instruction/template trace; DISC-03 runtime coverage | pass — prepared input/oracle and producer guidance; agent execution unqualified |
| V-11 | AC-05 | Preserve evals 1–12, inputs, write authority, original readiness distinctions | Original nine modes; eval definitions and policies | All setup modes and installer passed (producer claim) | DISC-04/05; original IDs retained; explicit report-write permissions; negative cases retained | pass — setup/projection, not agent qualification |

## Independent probes and command record

All commands ran from repository root; no network or live model calls. Let `P=.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python` (literal executable substituted below). No runtime production file changed.

- DISC-01: `PYTHONDONTWRITEBYTECODE=1 EVAL_WORK_ROOT=/tmp/t002-discovery-fixtures EVAL_MEASUREMENT_LAUNCHER="$PWD/.agents/scripts/measure_maintainability.py" .quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py starting-evidence` — exit 0. Real baseline and Ruff owner evidence generated; 42 independent rows.
- DISC-02: `PYTHONDONTWRITEBYTECODE=1 python3 -` with an independent assertion probe: enumerate `/tmp/t002-discovery-fixtures/starting-evidence/V-*` (exactly 42); for every producer-input.json compare each source/report SHA-256 and `.git/index` SHA-256 with actual bytes; assert V-02a empty exists, V-02c missing absent; absent launchers for V-08c-A/R and V-10f; absent original JSON for V-08d-A/R and V-07; V-10a/c/d aggregate exit 0, checked-source identity equal only for a/d and command coverage present only for a/c. All assertions passed. This independently checks decisive seeded states and preservation maps, not agent behavior.
- DISC-03: `PYTHONDONTWRITEBYTECODE=1 .quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -m unittest discover -s tests -p test_maintainability.py` — 33 passed, no skips. Real analyzers, dirty/index capture, folder additions/deletions, empty baselines, exclusions, both sibling collisions with successful controls, identity/settings rejection, missing/partial measurement, transfer and native-hard-failure/advisory-success boundaries. Test authorities are the named cases in tests/test_maintainability.py; no new tests or fixture infrastructure added.
- DISC-04: `PYTHONDONTWRITEBYTECODE=1 python3 -` loop invoking `python3 skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py <mode>` with EVAL_WORK_ROOT=/tmp/t002-discovery-original, check=True and captured output for each of: readiness-cases, revision-recovery, readiness-context, freshness-change, api-routine, queue-ready, queue-guided, scheduler-missing, api-overlap. All nine exited 0. Prepared inputs only.
- DISC-05: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` — 36 passed. Installer selection, managed guide/shared scripts and copying inspected; existing whole-package projection includes the changes without expanding installer ownership.
- DISC-06: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — 4 passed. Structural evidence only.
- DISC-07: `python3 tools/check_contracts.py --root .` — exit 0, six subsystems / 15 indexed plan references. Registry routes to actual producer declarations and explicitly excludes downstream execution qualification. Structural evidence only; no executable JSON Schema contract changed or claimed.
- DISC-08: `git diff --cached --check` — exit 0.
- DISC-09: `python3 scripts/install_development_skills.py --check .` — exit 1, exactly the four changed source preflight counterparts differ from active installation. Expected recorded development drift; no refresh attempted. It is not a behavioral pass.

Adversarial selection: dirty index versus worktree, unchanged MM with changed source, added/deleted inventory, incompatible project/tool/settings, retained originals versus later corrections, missing/excluded parent, occupied JSON/text independently, advisory versus required entry policy, native later-owner versus entry duties, stale and omitted aggregate coverage. For prepared decision rows the static contract and concrete setup were checked; no agent decisions were inferred from seeded files. No process-lifecycle change or lifecycle qualification is in scope. All invoked subprocess commands completed; no server or persistent fixture process was started. Disposable files remain under the two named /tmp roots only.

## Aggregate gate

`python3 tools/verify.py`: not run. Owner: this initial discovery pass. Reason: localized single-skill guidance/eval preparation plus registry/README documentation; targeted owning measurement and installer suites and required structural checks cover the changed boundary. The full gate also includes known active-profile drift. No decisive targeted failure was found. This record waives no later owner's duties.

## Questions and residual risk

No unresolved scope overlap or missing required preparation input was identified. Live agent invocation/grading is **not run**: separately budgeted runtime approval is absent, and the brief expressly permits honest preparation-only evidence. Agent decisions, report choice, handoff compliance and later T-003/T-004 consumption remain unqualified. They are not passed by these tests. Qualification owner: later authorized eval runner; acceptance owner must retain this limitation.

## Discovery continuation

- Iteration / current byte identity: first discovery; HEAD and index tree above; worktree equals staged bytes before report creation.
- Coverage rows: all 42 V-01–V-10 variants listed individually above = pass for preparation only; V-11 = pass for preparation/projection. No blocked/unchecked required preparation row. Agent execution remains unqualified across all variants.
- Finding IDs: none. No prior discovery finding or regression supplied.
- Finding/scenario continuity: implementation.md is producer-attributed input; current reviewer evidence is DISC-01–09. Correction owner: implementer if future findings arise; evidence owner: discovery for current preparation, authorized eval runner for future live behavior; authority/decision owner: separate acceptance call. Sibling surfaces include both profiles, every advisory/required variant and native later-owner/entry variants.
- Preparation/context: docs/tasks/T-002/brief.md rev 1; verification.md rev 1; preflight.md; implementation.md; reviews/maintainability-01.md; current staged diff including contracts and README. No new requirements or recorded decision-context artifact added.
- Reviewer regressions: none added; reuse DISC-01–05 exact commands and DISC-02 assertions for future corrections.
- Aggregate gate: not run, `python3 tools/verify.py`, initial discovery owner; localized scope and focused evidence as above.
- Next: separate fresh task-acceptance-review call with this report, brief, current scoped diff, verification rev 1, preflight, implementation claims and the explicit live-qualification limit.

## Exact status before report creation

```text
M  docs/contracts/index.json
M  docs/contracts/measurement.json
A  docs/tasks/T-002/brief.md
A  docs/tasks/T-002/implementation.md
A  docs/tasks/T-002/preflight.md
A  docs/tasks/T-002/reviews/maintainability-01.md
A  docs/tasks/T-002/verification.md
M  docs/tasks/index.json
M  skills/task-implementation-flow/README.md
M  skills/task-implementation-flow/task-preflight/SKILL.md
M  skills/task-implementation-flow/task-preflight/evals/evals.json
M  skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py
M  skills/task-implementation-flow/task-preflight/references/execution-packet-template.md
```

## Exact status after report creation

```text
M  docs/contracts/index.json
M  docs/contracts/measurement.json
A  docs/tasks/T-002/brief.md
A  docs/tasks/T-002/implementation.md
A  docs/tasks/T-002/preflight.md
A  docs/tasks/T-002/reviews/maintainability-01.md
A  docs/tasks/T-002/verification.md
M  docs/tasks/index.json
M  skills/task-implementation-flow/README.md
M  skills/task-implementation-flow/task-preflight/SKILL.md
M  skills/task-implementation-flow/task-preflight/evals/evals.json
M  skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py
M  skills/task-implementation-flow/task-preflight/references/execution-packet-template.md
?? docs/tasks/T-002/reviews/discovery-01.md
```

Only this new report entry may differ; staged tree and reviewed files remain unchanged.
