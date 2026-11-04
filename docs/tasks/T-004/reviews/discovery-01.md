# T-004 independent discovery 01

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, fresh independent session |
| Coverage completeness | **complete** for source guidance and executable preparation; required failed rows remain failed |
| Iteration | First discovery, after maintainability MNT-01 correction and registry synchronization |
| Created | 2026-11-04T23:22:25.805720+00:00 |
| Root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Report | `docs/tasks/T-004/reviews/discovery-01.md` |
| Preparation | `brief.md` revision 1; `verification.md` revision 1; `preflight.md`, including its Decision context |
| Submission | `implementation.md`, `correction-01.md`; `reviews/maintainability-01.md`, current `maintainability-02.md`; `contract-registry-01.md` |

This report publishes evidence only. It makes no acceptance decision, approved
deferral or advancement, and does not review or authenticate itself. Results
apply only to the identified reviewed bytes. Actor verdict/disposition/route
compliance is unrun and is not a required live check for this task.

## Provenance and scope

This session authored none of the reviewed production, test, fixture, catalog,
harness or registry bytes. It resolved and read the project-local installed
`.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`, its
durable report template and installed sibling `testing-discipline`. Changed
source instructions were reviewed as development specifications. No installation
was refreshed or substituted. This reviewer wrote only this new repository
report; disposable evidence and regression probes are under `/tmp/`.

HEAD is `6b80c8eecad0943c3a9ed9695f1f27ff124df5b2`.
The sorted JSON mapping of 28 relevant package/README/contract paths to SHA-256
has digest `81c87c510dada1140e507ec2f25e91961b7a581dabe3ec531b831f2a293d848c`. Exact 447-path current-worktree identities, real index
entries, index digest, status and 16 historical report siblings are in
`/tmp/T-004-discovery-01-identity.json`. That saved local manifest establishes
observed provenance and consistency, not tamper resistance.

Original B JSON remains SHA-256
`031191f9e4e50ff268699c924583351d7e0f8e99032aede1202fa493a9ff2084` at
`.quality/reports/T-004-preflight-20261104-01.json`, with its text sibling.
All 11 source hashes in maintainability02 match current bytes. Its independent
R remains `.quality/reports/T-004-maintainability-02.json`/`.txt`, and correction I
remains `T-004-correction-01.json`/`.txt`. No recapture, overwrite or measurement
pair was needed by discovery. Current measurement evidence is consumed within
its reviewed scope, without repeating general maintainability review.

The task-owned implementation is the 11 source assets identified by
maintainability02 plus the registry updater's four contract files. The staged
brief, verification and task index are pre-existing user work. Preflight,
implementation/correction and numbered reviews are durable package evidence.
There is no unexplained or inseparable scope overlap. No plan, runtime CLI,
schema, installer, shared dependency or root test changed. The prior native04
manifest differs on the three existing contract files updated by registry01;
the new reviewer record is also a later input. That older manifest is not a
current whole-repository gate identity.

## Confirmed findings

### F-01 [suggested P2] The tests-only independence case is production-only

- Location: `skills/task-implementation-flow/task-maintainability-review/evals/files/review_fixture.py:98–99`; V-01d catalog row.
- Trigger: run `setup_fixture.py review:V-01d` with the documented explicit source distribution and prepared interpreter.
- Observed: `git diff --name-only HEAD -- src tests evals fixtures harness` returns only `src/logic.py`. Every test/eval/fixture/harness sample remains unchanged. The request nevertheless declares that this session authored reviewed tests-only bytes.
- Consequence: the prepared case can never distinguish a reviewer who correctly handles production authorship but incorrectly treats tests-only authorship as independent. Its actor oracle is unsupported by its actual diff. The all-case checker still passes.
- Affected authority: AC-01, AC-06; V-01d and V-11a/b. Broken invariant: prepare the stated authored-byte class while unrelated prerequisites remain valid; a prose label cannot create a tests-only submission.
- Credible sibling surface: V-01c's production-authorship control, V-05d/e significant-test controls and V-10d test/harness correction entry depend on the same real asset-class distinction. Existing legacy test-assets coverage remains distinct and does not substitute for this case.
- Smallest corrective direction: specialize this existing case at its setup owner so production stays at original bytes and a real reviewed test/eval/harness asset changes; bind the preparation assertion and oracle to the actual diff. Preserve the production-only control and existing test-asset cases.
- Evidence: `/tmp/T-004-discovery-regressions.py`, `test_tests_only_case_has_tests_only_diff`; raw failure `/tmp/T-004-discovery-01-regressions.log`.

### F-02 [suggested P2] Partial-evidence variants retain a masking baseline fault

- Location: `.../evals/files/review_cases.json` V-02d-current/profile seeds; `.../evals/files/review_fixture.py:163–170`.
- Trigger: prepare `review:V-02d-current` or `review:V-02d-profile`; both reuse upstream `V-05b-advisory`, which already corrupts B's Ruff status and overall completion before reviewer-specific faults are applied.
- Observed: current variant has **both B and I incomplete**. Profile variant has B `measurement_status=incomplete` plus `full_profile=false`, while I is complete. The required independent current-only and profile-only states are not supplied.
- Consequence: a reviewer that notices only an incomplete baseline can pass these controls without detecting incomplete current evidence or missing selected-profile coverage. The intended guards are masked by an earlier unrelated fault, contrary to V-02's explicit single-prerequisite setup.
- Affected authority: AC-01, AC-04, AC-06; V-02d, V-11a/b. Broken invariant: each independent evidence fault must start from otherwise valid evidence and reach its own guard.
- Credible sibling surface: V-02d-baseline is the separate incomplete-B control; V-02c format/tool/settings/check variants and V-06g constituent/scope/policy/bytes variants likewise require isolated faults. Inspection found those sibling branches separately mutate their named inputs; their passing preparation results do not close these two failed variants.
- Smallest corrective direction: use/recover an intact real B/I preparation for the current and profile variants, then inject only their named fault. Assert B/I completion and coverage preconditions per variant, including the valid side, rather than merely asserting that some evidence is bad.
- Evidence: regression `test_partial_evidence_faults_are_isolated` fails both subtests at the intended baseline-completion assertion, after successful real setup; same raw log.

### F-03 [suggested P2] The isolated receiver lacks submitted source and permission to obtain it

- Location: `.../evals/files/review_fixture.py:98–99`, `:325–326`, `:347–348`, `:362–363` (upstream V-07d creates the receiver before this submission edit).
- Trigger: prepare `review:V-01e`, then follow the supplied isolated-consumer instructions.
- Observed: source `src/logic.py` SHA-256 is `f62ee7573dfa7881e8f46fd74fcf48cf177c85f8cf36d2d050322c91cbcc69d4`; receiver is `da81fd8db37546b0de02c3682a2adf1fdf239ecdf72264f7a18f9fe0b860e36f`. Receiver still contains baseline source. The new request authorizes exact B/I sibling transfer only, permits no source edits, and says submitted source must be transferred separately without supplying that transfer. Review task inputs added after clone are also absent at the receiver.
- Consequence: transferring the ignored reports succeeds in principle but the receiving reviewer cannot compare the actual submitted code within its declared authority. A correct reviewer must stop for missing source/input transfer, so the intended isolated-review success outcome is not executable as prepared.
- Affected authority: AC-01, AC-06; V-01e, V-11a/b. Broken invariant: the isolated receiving workspace must contain the actual submission and review inputs before read-only review, while report transfer stays explicit.
- Credible sibling surface: changed/added/deleted assets and significant test/eval/harness changes in V-01a must all survive any isolated transfer, not just the existing logic file. B/I JSON/text siblings must remain separately transferred and immutable.
- Smallest corrective direction: complete source/task-input staging into the disposable receiver at setup time (or provide an explicitly authorized complete transfer before review), retain the original Git before-state, and assert receiving submitted-byte equality and usable local review inputs. Keep report transfer explicit and source writes outside the read-only reviewer role.
- Evidence: `test_isolated_receiver_contains_submitted_source` fails after successful setup; `/tmp/T-004-discovery-01-V01e/` retains the source, receiver, request and transfer paths.

### F-04 [suggested P2] The policy-conflict case has no concrete native obligation

- Location: `.../evals/files/review_fixture.py:119–121`; V-06i uses a measurement-only seed.
- Trigger: prepare `review:V-06i`.
- Observed: two documents disagree about an unnamed “architecture command”. There is no `docs/native.md`, `tools/native.py`, `tools/aggregate.py` or `scripts/check-architecture`; neither conflicting document gives an exact runnable command or its governed scope. Thus there is no actual existing native obligation whose requiredness can be retained or resolved.
- Consequence: this case checks recognition of generic contradictory prose, rather than the required native command/policy/owner boundary. An actor can route the prose conflict without proving it preserves the real hard/advisory check obligation.
- Affected authority: AC-03, AC-06; V-06i, V-11a/b. Broken invariant: V-06 starts from a real existing static command, governed scope and owner, and changes only its specified policy precondition.
- Credible sibling surface: V-06h-none intentionally has no command and must remain distinct; V-06c/e/f/g retain a real documented native command for missing/unavailable/current/stale evidence. Those variants cannot replace the policy-conflict state.
- Smallest corrective direction: reuse the existing real native fixture owner for V-06i and make the two authority sources conflict about that same exact command/scope, with a named resolution owner and unchanged executable command. Assert that concrete binding in the preparation checker.
- Evidence: `test_policy_conflict_names_real_command` fails after successful setup; raw fixture retained under `/tmp/T-004-discovery-01-V06i/`.

## Completeness ledger

“Pass” below concerns this task's source guidance or **preparation/tool boundary
only**. It never claims an actor obeyed the skill. Each child has a concrete
catalog situation/oracle plus its supplied source/Git/B/I/request/native/rationale
inputs; the current full checker prepared all 82 unique IDs and compared each
returned catalog field exactly. I independently traced the source rule and
reused seed for every matrix row, then probed material setup risks. Metadata
equality does not override the four demonstrated precondition defects.

| Row | AC / invariant and explicit cases | Setup/oracle and current independent evidence | Result |
|---|---|---|---|
| V-01 | AC-01/06; fresh/stale/current assets, both authorship classes, isolated transfer; children a–e | Source protocol requires own R/current hashes and full relevant asset scope; full setup checker plus fresh stale-I real comparison/index preservation; separate d/e probes | **fail**, F-01/F-03; a/b/c preparation passes |
| V-02 | AC-01/04/06; missing B, wrong project, four incompatibilities, three partial variants, optional/indispensable tools, docs/unsupported, JSON/text collisions, external/occupied paths | Required reference covers precise gaps/recovery, N/A and fresh pairs; four compatibility CLI rejects exercised by full checker; real missing/path inputs traced; d-current/profile independently inspected | **fail**, F-02; all other listed preparations pass |
| V-03 | AC-02/04/06; a–j, below/equal/new/cross/worse/equal-hotspot/improved/reached/missing/grouped | Source decision table implements all cases; real complexity inputs/rationale traced; pinned owning suite exercises actual statement/argument boundaries and missing counts | pass — preparation/source; actor dispositions unrun |
| V-04 | AC-02/06; untouched sibling, wrong attribution, rename/move/extract, unknown count | Actual upstream source/diffs, deliberate attribution JSON, move file and Ruff override inputs traced; pinned symbol/exemption tests pass | pass — preparation/source |
| V-05 | AC-02/06; extraction defect, semantic defect/control, test-assets defect/control | Real forwarding/payload helper defect plus retained legacy semantic/test setup and held-back oracles; owning suite 26 PASS includes concrete green-code controls and defect observations | pass — preparation/source |
| V-06 | AC-03/04/06; hard violation, native fail complete/N/A, missing/stale/unavailable, aggregate current/four faults, documented/none, policy conflict, wrapper available/unavailable | Source retains whole scope/policy/owners and no duplicate constituent execution; real native failure/recovery current checker; independent i probe; variants traced to their actual native history | **fail**, F-04; other preparations pass |
| V-07 | AC-04/06; complete multi-blocker, genuine-stop, justified-breach control | Real four CC11 obligations, four original blockers, gap/owner and five optional warning candidates; current checker and owner suite; uncapped required source fields traced | pass — preparation/source |
| V-08 | AC-05/06; first occurrence, second edit, stable findings, unaffected scope | Current checker actually executes two distinct source states with R1/R2 against unchanged B, preserves original reports/index and seeded finding ledger; actor histories explicitly labeled | pass — preparation/tool boundary |
| V-09 | AC-01/05/06; unauthorized, authorized preserved-before, authorized missing-before | Real outside paths, preserved HEAD-verifiable bytes versus new uncovered file, request authorities and current-only recovery protocol traced; pinned coverage/original-before tests pass | pass — preparation/source |
| V-10 | AC-03/05/06; registry owed/absent/current, acceptance-only, significant tests, trivial/unaffected, stale/incomplete/blocker | Seeded numbered upstream history binds current hashes; real stale/test edits; separate discovery/acceptance requests exist for each variant; minimal consumer diff preserves route and role separation | pass — preparation/source; no downstream actor executed |
| V-11 | AC-06/scope; all finite cases, negative output controls, distribution/preservation | Full checker passes but omits decisive precondition assertions F-01–F-04; regression proves failures. Exact 9-file changed package projection and installed new entry independently pass; focused installer preservation test passes | **fail**, a/b; c passes |

### Child and variant matrix

The following is the complete 82-ID selectable inventory, covering all 62
authority child IDs. The exact setup for every entry is the public entry in
DISC-01 with `review:<ID>` and a fresh `EVAL_WORK_ROOT`. Its exact situation and
artifact oracle are `files/review_cases.json` fields `situation`/`oracle`, consumed
with the source traces and observations above. Seeds are actual reused input
owners, not evidence that a reviewer ran. All rows have current setup execution
under DISC-01; failed rows have additional DISC-02 precondition evidence.

| ID | Reused input owner | Current preparation result |
|---|---|---|
| V-01a | measurement:V-03a | pass — preparation only |
| V-01b | measurement:V-05c-advisory | pass — preparation only |
| V-01c | measurement:V-04a-complexity | pass — preparation only |
| V-01d | measurement:V-04a-complexity | fail — F-01 |
| V-01e | measurement:V-07d | fail — F-03 |
| V-02a | measurement:V-05a-advisory | pass — preparation only |
| V-02b | measurement:V-04a-complexity | pass — preparation only |
| V-02c-checks | measurement:V-04a-complexity | pass — preparation only |
| V-02c-format | measurement:V-04a-complexity | pass — preparation only |
| V-02c-settings | measurement:V-04a-complexity | pass — preparation only |
| V-02c-tools | measurement:V-04a-complexity | pass — preparation only |
| V-02d-baseline | measurement:V-05b-advisory | pass — preparation only |
| V-02d-current | measurement:V-05b-advisory | fail — F-02 |
| V-02d-profile | measurement:V-05b-advisory | fail — F-02 |
| V-02e | measurement:V-05f-advisory | pass — preparation only |
| V-02f | measurement:V-05f-required | pass — preparation only |
| V-02g-docs | measurement:V-03e-docs | pass — preparation only |
| V-02g-unsupported | measurement:V-03e-docs | pass — preparation only |
| V-02h-json | measurement:V-07c | pass — preparation only |
| V-02h-text | measurement:V-07c | pass — preparation only |
| V-02i-external | measurement:V-04a-complexity | pass — preparation only |
| V-02i-occupied | measurement:V-04a-complexity | pass — preparation only |
| V-03a | measurement:V-04a-complexity | pass — preparation only |
| V-03b | measurement:V-04b-complexity | pass — preparation only |
| V-03c | measurement:V-04c-complexity | pass — preparation only |
| V-03d | measurement:V-04d-complexity | pass — preparation only |
| V-03e | measurement:V-04e-complexity | pass — preparation only |
| V-03f | measurement:V-04f-complexity | pass — preparation only |
| V-03g | measurement:V-04g-complexity | pass — preparation only |
| V-03h | measurement:V-04h | pass — preparation only |
| V-03i | measurement:V-04k | pass — preparation only |
| V-03j | measurement:V-04e-statements | pass — preparation only |
| V-04a | measurement:V-03b | pass — preparation only |
| V-04b | measurement:V-04f-complexity | pass — preparation only |
| V-04c-extract | measurement:V-03c-extract | pass — preparation only |
| V-04c-move | measurement:V-03c-move | pass — preparation only |
| V-04c-rename | measurement:V-03c-rename | pass — preparation only |
| V-04d | measurement:V-03d | pass — preparation only |
| V-05a | measurement:V-04j | pass — preparation only |
| V-05b | semantic-defects | pass — preparation only |
| V-05c | semantic-control | pass — preparation only |
| V-05d | test-assets | pass — preparation only |
| V-05e | test-assets-control | pass — preparation only |
| V-06a | four-blockers | pass — preparation only |
| V-06b-NA | measurement:V-08h | pass — preparation only |
| V-06b-complete | measurement:V-08h | pass — preparation only |
| V-06c | measurement:V-08b | pass — preparation only |
| V-06d | measurement:V-08f | pass — preparation only |
| V-06e | measurement:V-08g | pass — preparation only |
| V-06f | measurement:V-08d | pass — preparation only |
| V-06g-bytes | measurement:V-08d | pass — preparation only |
| V-06g-constituent | measurement:V-08d | pass — preparation only |
| V-06g-policy | measurement:V-08d | pass — preparation only |
| V-06g-scope | measurement:V-08d | pass — preparation only |
| V-06h-documented | measurement:V-08b | pass — preparation only |
| V-06h-none | measurement:V-08b | pass — preparation only |
| V-06i | measurement:V-04a-complexity | fail — F-04 |
| V-06j-available | measurement:V-09a | pass — preparation only |
| V-06j-unavailable | measurement:V-09a | pass — preparation only |
| V-07a | four-blockers | pass — preparation only |
| V-07b | genuine-stop | pass — preparation only |
| V-07c | measurement:V-04c-complexity | pass — preparation only |
| V-08a | four-blockers | pass — preparation only |
| V-08b | correction-round | pass — preparation only |
| V-08c | correction-round | pass — preparation only |
| V-08d | measurement:V-04a-complexity | pass — preparation only |
| V-09a | measurement:V-05e-advisory | pass — preparation only |
| V-09b | measurement:V-07a | pass — preparation only |
| V-09c | measurement:V-07b | pass — preparation only |
| V-10a | measurement:V-04a-complexity | pass — preparation only |
| V-10b-absent | measurement:V-04a-complexity | pass — preparation only |
| V-10b-current | measurement:V-04a-complexity | pass — preparation only |
| V-10c | measurement:V-04a-complexity | pass — preparation only |
| V-10d | measurement:V-04a-complexity | pass — preparation only |
| V-10e-exception | measurement:V-04a-complexity | pass — preparation only |
| V-10e-unaffected | measurement:V-04a-complexity | pass — preparation only |
| V-10f-blocker | measurement:V-04a-complexity | pass — preparation only |
| V-10f-incomplete | measurement:V-04a-complexity | pass — preparation only |
| V-10f-stale | measurement:V-04a-complexity | pass — preparation only |
| V-11a | measurement:V-04a-complexity | fail — F-01–F-04 |
| V-11b | measurement:V-04a-complexity | fail — F-01–F-04 |
| V-11c | measurement:V-04a-complexity | pass — preparation only |

## Independent probes, commands and limits

All commands ran from the repository root except the explicitly disposable
workspaces. Logs remain authoritative raw evidence at the paths below. No live,
networked or provider checks, new dependencies, daemon, controller or long-lived
process fixture was launched. All bounded setup/check subprocesses exited;
retained disposable directories contain evidence files only.

| ID | Exact command or probe | Observed result / purpose | Evidence |
|---|---|---|---|
| DISC-01 | `env EVAL_SOURCE_ROOT=/Users/mtrusov/work/skill-sources/personal-skills EVAL_MEASUREMENT_PYTHON=/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python PYTHONDONTWRITEBYTECODE=1 python3 skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py` | Exit 0; 5 tests, 60.907s; all 82 setups, exact row identity, stale/current comparison, index/history, native recovery, two correction comparisons and synthetic negative claims. Does not assert all scenario preconditions. | `/tmp/T-004-discovery-01-focused.log` |
| DISC-02 | `python3 -B /tmp/T-004-discovery-regressions.py` | Exit 1; 4 tests, 5 failures, 3.700s. Each public setup succeeds, then authority-derived precondition assertions fail for F-01–F-04. Both F-02 variants fail separately. Retains fresh workspace paths in raw log. | `/tmp/T-004-discovery-01-regressions.log`; regression script retained, no production edits |
| DISC-03 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py` | Exit 0; 26 PASS, 2.292s; distinct legacy semantic/test-asset/multiblocker/genuine-stop/correction coverage retained | `/tmp/T-004-discovery-01-owner.log` |
| DISC-04 | `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py` | Exit 0; 33 PASS, 17.149s, no skips; real numeric, compatibility, unknown counts, projection/relocation, coverage and collision boundaries | `/tmp/T-004-discovery-01-measurement.log` |
| DISC-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k test_install_projects_maintainability_and_registry_updater_families_and_guide_routes` | Exit 0; 1 PASS, 0.923s; managed projection and unrelated-byte preservation | `/tmp/T-004-discovery-01-installer.log` |
| DISC-06 | `env EVAL_SOURCE_ROOT=/Users/mtrusov/work/skill-sources/personal-skills EVAL_MEASUREMENT_PYTHON=/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python EVAL_WORK_ROOT=/tmp/T-004-discovery-01-installed PYTHONDONTWRITEBYTECODE=1 python3 /tmp/T-004-discovery-01-V01d/measurement-fixture/.agents/skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py review:V-01a` | Exit 0; installed new entry produces disposable B/I/current submission. All 9 files of changed maintainability package match source projection exactly. Explicit source distribution is fixture preparation; the generated measurement uses target-local runtime. No active/global fallback. | `/tmp/T-004-discovery-01-installed.log`, generated target |
| DISC-07 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Exit 0; 4 PASS, 0.168s; current whole-repository CLEAN source policy | `/tmp/T-004-discovery-01-architecture.log` |
| DISC-08 | `python3 tools/check_contracts.py --root .` | Exit 0; 8 subsystems / 26 indexed plan refs. Structural registry consistency, not behavior or actor qualification. No runtime schema/validator constraint changed in this task. | `/tmp/T-004-discovery-01-contracts.log` |
| DISC-09 | `python3 scripts/install_development_skills.py --check .` | Exit 1; checked 112 paths, 10 active-profile differences (4 changed, 6 missing). Read-only expected source/install drift; preserved, not waived or refreshed. | `/tmp/T-004-discovery-01-profile.log` |
| DISC-10 | `git diff --check`; exact source/report/index hashing and current-review identity validation | Diff check exit 0. All 11 maintainability02 hashes match; B hash matches; preserved source/index/pair manifest independently recorded. | `/tmp/T-004-discovery-01-identity.json`; report provenance above |

Installer declarations `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
`SHARED_SCRIPT_FILES`, profile guide and README installation instructions were
inspected. Current profile already includes these three packages; new resources
are projected recursively; no membership/runtime declaration became stale.
`evals.json` remains unchanged from HEAD; the six opt-in actor definitions retain
their explicit preparation/budget boundary. No live actor/grader was run.

Required dispositions and native proof in the source protocol are outside the
optional warning cap; source semantics satisfy the intended AC-01–AC-05 rules.
The four findings concern AC-06's decisive preparation contract. They do not
assert that the source decision rules or an unrun actor produced a wrong verdict.

## Aggregate-gate record

| Field | Current record |
|---|---|
| Command | `python3 tools/verify.py` |
| Status | **not run** in this discovery pass |
| Owner/stage | This fresh independent discovery |
| Reason | Decisive targeted preparation failures F-01–F-04. Installed discovery step 6 suppresses aggregate after targeted failure; no separate diagnostic broad run is needed. |
| Current evidence | Focused rows and regressions above; no clean current aggregate is claimed. Prior `/tmp/T-004-aggregate-unsandboxed-02.log` predates corrected harness/catalog and current registry, so remains historical. |

This suppression does not waive any conditional owner's native duty. Canonical
architecture and registry checks ran current; profile drift was independently
reconfirmed and remains a real failed diagnostic. The active installation must
remain unchanged during this run. Deliberate between-run refresh belongs to the
coordinator/operator. No aggregate or constituent is silently relabeled current
from prior logs. New discovery after correction owns its justified aggregate
only after targeted evidence is clean.

## Scope/status preservation

Real index SHA-256 is
`30e5d83da9b771347ae14364755f8cc36d9fd758f9f4bfd8f4b906697b97f7f2`.
Staged user entries remain: brief blob `53fe9be1217307f1aeefff5ba6830a5b16e4dc3c`,
verification blob `b5042d377892da2397073c154c94612e902e5f73`, task-index blob
`efd206b17f26bd066512c081e0d1000e183f4dc7`. Worktree and real index were
observed separately, with no staging/reset or ownership absorption.

Exact reviewed pre-write status (`--untracked-files=all`):

```text
 M docs/contracts/implementer-feedback.json
 M docs/contracts/index.json
 M docs/contracts/measurement.json
A  docs/tasks/T-004/brief.md
A  docs/tasks/T-004/verification.md
M  docs/tasks/index.json
 M skills/task-implementation-flow/README.md
 M skills/task-implementation-flow/task-acceptance-review/SKILL.md
 M skills/task-implementation-flow/task-maintainability-review/SKILL.md
 M skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py
 M skills/task-implementation-flow/task-review-discovery/SKILL.md
?? docs/contracts/reviewer-feedback.json
?? docs/tasks/T-004/correction-01.md
?? docs/tasks/T-004/implementation.md
?? docs/tasks/T-004/preflight.md
?? docs/tasks/T-004/reviews/contract-registry-01.md
?? docs/tasks/T-004/reviews/maintainability-01.md
?? docs/tasks/T-004/reviews/maintainability-02.md
?? skills/task-implementation-flow/task-maintainability-review/evals/README.md
?? skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py
?? skills/task-implementation-flow/task-maintainability-review/evals/files/review_cases.json
?? skills/task-implementation-flow/task-maintainability-review/evals/files/review_fixture.py
?? skills/task-implementation-flow/task-maintainability-review/evals/review-evals.json
?? skills/task-implementation-flow/task-maintainability-review/references/measurement-review.md
```

Post-write status:

```text
 M docs/contracts/implementer-feedback.json
 M docs/contracts/index.json
 M docs/contracts/measurement.json
A  docs/tasks/T-004/brief.md
A  docs/tasks/T-004/verification.md
M  docs/tasks/index.json
 M skills/task-implementation-flow/README.md
 M skills/task-implementation-flow/task-acceptance-review/SKILL.md
 M skills/task-implementation-flow/task-maintainability-review/SKILL.md
 M skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py
 M skills/task-implementation-flow/task-review-discovery/SKILL.md
?? docs/contracts/reviewer-feedback.json
?? docs/tasks/T-004/correction-01.md
?? docs/tasks/T-004/implementation.md
?? docs/tasks/T-004/preflight.md
?? docs/tasks/T-004/reviews/contract-registry-01.md
?? docs/tasks/T-004/reviews/discovery-01.md
?? docs/tasks/T-004/reviews/maintainability-01.md
?? docs/tasks/T-004/reviews/maintainability-02.md
?? skills/task-implementation-flow/task-maintainability-review/evals/README.md
?? skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py
?? skills/task-implementation-flow/task-maintainability-review/evals/files/review_cases.json
?? skills/task-implementation-flow/task-maintainability-review/evals/files/review_fixture.py
?? skills/task-implementation-flow/task-maintainability-review/evals/review-evals.json
?? skills/task-implementation-flow/task-maintainability-review/references/measurement-review.md
```

Only this new report entry differs. Post-write hashing checks the saved 447
worktree files, exact index bytes/entries and all 16 report siblings; this report
is excluded from its own reviewed-byte identity.

## Questions, residual limits and next owner

No required row is blocked or unchecked: preparation/source coverage is complete
with explicit failed rows. Correcting the four findings belongs to the bounded
implementation/correction owner. Existing MNT-01 remains resolved by
maintainability02; its canonical 82 unique IDs and exact returned-row assertions
were independently rerun and remain sound. F-01–F-04 are new independent IDs,
not recycled maintainability IDs.

Live reviewer actions for all V-01–V-11 verdict/disposition/route outcomes remain
unqualified; authorized operator/fresh graders own any later live qualification.
T-005 owns the full installed producer-to-consumer journey. These are explicit
non-required proof limits of T-004, not a discovery-approved deferral. Active
drift remains with the coordinator/operator and downstream admission owners.

Hand this report, scoped diff, brief, verification revision 1, preflight/Decision
context, implementation/correction, current maintainability02, registry01 and
regression script/log to the separate acceptance decision call. That owner judges
whether these findings block advancement; discovery makes no such decision. If
correction is requested, following bounded correction,
re-enter affected architecture/maintainability and registry duties as applicable,
then obtain fresh independent discovery and a separate acceptance decision.
This reviewer executes no downstream stage.

## Discovery continuation

```markdown
Discovery continuation:
- Iteration/current bytes: discovery01; HEAD 6b80c8eecad0943c3a9ed9695f1f27ff124df5b2; 28-path scoped mapping digest 81c87c510dada1140e507ec2f25e91961b7a581dabe3ec531b831f2a293d848c; /tmp/T-004-discovery-01-identity.json.
- Coverage: V-01 fail F-01/F-03; V-02 fail F-02; V-03/04/05 pass preparation/source; V-06 fail F-04; V-07/08/09/10 pass preparation/source/tools; V-11 fail a/b, c pass. All 82 child/variant dispositions are retained above; no blocked/unchecked required rows. Actor compliance unrun, outside required local qualification.
- Finding IDs: F-01 P2 tests-only state absent; F-02 P2 partial faults masked; F-03 P2 receiver submission absent; F-04 P2 concrete native conflict absent. MNT-01 remains resolved; no IDs recycled.
- Continuity/owners: implementation correction owner repairs F-01–F-04 and sibling preconditions without replacing B/history; fresh reviewer/discovery own new evidence; separate acceptance owns decisions. Existing architecture/native owners and coordinator's active-drift duty survive. No approved deferral.
- Preparation/context: docs/tasks/T-004/brief.md revision1, verification.md revision1, preflight.md/Decision context, implementation.md, correction-01.md, reviews/maintainability-02.md and contract-registry-01.md.
- Reviewer regressions: python3 -B /tmp/T-004-discovery-regressions.py; /tmp/T-004-discovery-01-regressions.log; 4 tests / 5 intended precondition failures. Current focused/owner/measurement/installer/architecture/contracts logs use /tmp/T-004-discovery-01-*.
- Aggregate: python3 tools/verify.py not run; discovery01 owns suppression after decisive targeted failures. Prior aggregate historical; active-profile check currently fails ten differences. Fresh corrected discovery owns one justified aggregate after clean targeted evidence.
- Next: separate acceptance decision call consumes this complete report and decides whether findings block advancement. If correction is requested, its owner then follows affected conditional duties/registry, fresh discovery and separate acceptance. This is the first discovery pass; user authority requires stopping the correction loop if a fourth or later discovery still finds issues. No stage advanced by this report.
```
