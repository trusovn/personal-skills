# T-004 independent maintainability review 01

VERDICT: CHANGES_REQUESTED
ARCHITECTURE_GATE: PASS

This fresh session authored none of the reviewed implementation, test, fixture or harness bytes. The active authority was project-local `.agents/skills/task-implementation-flow/task-maintainability-review/SKILL.md`, with `.agents/skills/testing-discipline/SKILL.md`. Source T-004 guidance was reviewed as the implementation specification, not substituted for the active installation. The separately authorized independent comparison used sibling `.agents/scripts/measure_maintainability.py`. Review was read-only except fresh reports. Staged brief, verification and task index are pre-existing user work.

## BLOCKERS

1. **MNT-01 — duplicate case identities make later oracle rows unreachable.**
   - Location: `skills/task-implementation-flow/task-maintainability-review/evals/files/review_cases.json:645` through `:688`; dispatch in `review_fixture.py:271`; iteration in `check_review_fixture.py:42`.
   - Problem: the new catalog contains 85 rows but only 82 unique dispatch IDs. `V-11a`, `V-11b` and `V-11c` each appear twice with different situation/oracle text. `prepare(case_id)` selects the first matching row. Thus no caller can select the second row, and the full finite check runs the first state/oracle twice under each duplicate identity.
   - Evidence: independent JSON inspection identified duplicate row pairs 80/81, 82/83 and 84/85. The finite check loops all rows but invokes preparation using only `case['id']` and checks merely that the returned oracle is nonempty; it does not establish that the requested catalog row was selected. The second oracle for each pair is therefore excluded from generated `task-runs/oracle.json` even though traversal counts it.
   - Maintainability impact: case identity is the fixture's selection, output-directory, subtest and grading boundary. A maintainer can change the second V-11b wrong-output oracle and see a green finite run while the generated case remains unchanged. Failure reports and evidence cannot distinguish the two supposed variants. This creates duplicated scenario authority and misleading coverage inventory, with repeated installation/measurement work instead of distinct evidence.
   - Smallest correction direction: consolidate overlapping obligations into one canonical row per ID, preserving all distinct oracle requirements. If a second state is actually needed, give it a unique ID and setup. Make the existing finite check reject duplicate IDs and verify returned case identity/oracle against the requested row. Correct the 85-independent-variants claim to the resulting actual inventory; do not remove distinct requirements merely to deduplicate.
   - Current disposition: confirmed. This is a harness identity/ownership defect, not a metric threshold finding. No other concrete maintainability blocker was found in the bounded scope.

## MEASUREMENT

Status: complete, full-profile, compatible `compared`, format 5.

- Original B, retained: `.quality/reports/T-004-preflight-20261104-01.json` and `.txt`. JSON SHA-256 `031191f9e4e50ff268699c924583351d7e0f8e99032aede1202fa493a9ff2084`. Repository HEAD/project binding matches preflight; this is the original three-package capture, not recaptured edited code.
- Implementer I, retained: `.quality/reports/T-004-implementation-02.json` and `.txt`. Its three Python source hashes match current R.
- Independent R, fresh in this session: `.quality/reports/T-004-maintainability-01.json` and `.txt`.
- Command: `python3 -B .agents/scripts/measure_maintainability.py compare skills/task-implementation-flow/task-maintainability-review skills/task-implementation-flow/task-review-discovery skills/task-implementation-flow/task-acceptance-review --root /Users/mtrusov/work/skill-sources/personal-skills --baseline .quality/reports/T-004-preflight-20261104-01.json --output .quality/reports/T-004-maintainability-01.json`.
- R inventories five eval/harness Python files. Actual affected Python assets are changed `setup_fixture.py` and added `review_fixture.py`/`check_review_fixture.py` in the maintainability package; discovery/acceptance Python helpers are untouched context. The existing setup functions are untouched; its only addition is top-level review dispatch. New helpers are additions, not renames/extractions. Unknown before counts remain absent, not zero.
- Identity: Radon 6.0.1, Ruff 0.14.2, complete complexity/Ruff checks, provisional 10/50/5 targets; settings SHA-256 `f258d0e5a0dc070fc9ec33aa0dc000b1959fba9eebdd5cc20e1cb00178a654fb` and `a95813db8c5666acfbeae7e1734e7f1a16ad674d1798cc710853e0d3bbb2754b`. Full tool/settings/adapter identity is retained in R.
- Markdown and JSON assets received semantic review; Python metrics do not establish their correctness. No supplemental baseline or scope expansion was needed. Shared workspace was used; no isolated receiving root was selected.

## RATIONALE_DISPOSITIONS

All six implementer rationale groups were assessed independently against the actual code and R. New functions have absent before metrics. These dispositions do not waive MNT-01.

- **RAT-01** — `ReviewFixtureTests.test_every_finite_setup_supplies_real_inputs_and_preserves_history`, complexity absent → 12: agree with retaining one finite matrix plus subtests. Preservation rules and subprocess boundary belong together; a test per fault would repeat setup/snapshot authority. MNT-01 requires fixing identity validation within this owner, not a metric-driven split.
- **RAT-02** — `review_fixture.seed`, complexity absent → 18: agree. It adapts two concrete existing fixture families and preserves the actual before/submitted restoration order. Delegating each row to callbacks would scatter the restore/capture invariant. Its local AST read of the existing pricing constant is visible within the same package and serves correction history; no generic fixture framework is justified.
- **RAT-03** — `review_fixture.native_inputs`, complexity absent → 13: agree. It owns native-policy/aggregate evidence variations, with named actual-execution and labeled invalid-claim branches. Tiny mutation callbacks would add navigation without a separate consumer or boundary.
- **RAT-04** — `review_fixture.evidence_fault`, complexity absent → 14: agree. Named evidence prerequisites and fault provenance stay local. A generic field-path interpreter would hide the determining prerequisite and complicate diagnosis.
- **RAT-05** — `review_fixture.route_inputs`, complexity absent → 17: agree. It builds one conditional-history record and the separate consumer requests, keeping byte identities and current/absent/stale transitions visible. A strategy registry would distribute the same route authority across single-use callbacks.
- **RAT-06** — `review_fixture.prepare`, complexity absent → 27 and statements absent → 58: agree with the retained orchestration boundary. Existing helpers own native/evidence/correction/rationale/route groups; the remaining order and permission-bounded request composition form one preparation transaction. Further one-use extraction is not needed to reach numeric targets. The catalog identity fix should stay at its existing selection/test boundary.

The unchanged acceptance fixture's `repeated_review` complexity 13 is untouched debt, not an affected rationale obligation. Below-target new helpers need no individual defense. No missing required rationale remains.

## NATIVE_EVIDENCE

- **Architecture:** reviewer executed `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` on current bytes: 4 tests, PASS, 0.164s. Whole-repository CLEAN policy is owned by `tests/test_architecture.py`, required by AGENTS/development. No new/worsened hard violation.
- **Focused owner:** reviewer executed `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py`: 26 tests PASS, 2.280s. This verifies the current existing scope/fixture contract, not actor compliance or unique new catalog identities.
- **Contracts:** validated saved implementation-stage result `/tmp/T-004-contracts-02.log` and the aggregate constituent: structural PASS, 7 subsystems / 22 plan refs. Registry semantic synchronization remains the designated later owner's duty.
- **Aggregate:** validated saved implementation-stage `python3 tools/verify.py`, `/tmp/T-004-aggregate-unsandboxed-02.log`. Seven checks, one failed: active-profile drift. All maintained suites passed, total 536 tests with 31 optional analyzer skips. No clean aggregate PASS is claimed. Separately pinned measurement suite evidence is recorded in implementation; skipped default analyzer cases remain unqualified by that aggregate.
- **Whole-scope binding:** independently checked `.quality/reports/T-004-native-bytes-03.json`: all 441 recorded file hashes match, no missing files and no additional Git-visible input outside the declared reporting-only implementation result. Digest `3238ea0844c7f3de42601030abd387215d1eb46313fafb1c598a6787834c1b0a`. It covers source, tests, config, skill, eval and docs inputs; this new review is reporting-only. Existing aggregate evidence is therefore applicable to submitted implementation bytes. Aggregate was not rerun merely to populate this report.
- **Drift:** exact failed constituent `python3 scripts/install_development_skills.py --check .`; 112 managed paths, 10 changed/missing source resources. It remains a real required aggregate failure, owned by coordinator/operator for deliberate between-run installation action. Active refresh is forbidden in this invocation. No source-review verdict waives downstream admission or certifies active installation parity.
- There is no additional documented native formatter/lint/typecheck/build/server obligation. Metrics and optional instrumentation add none.

## COVERAGE_AND_GAPS

Reviewed all scoped tracked diffs and new implementation assets, including complete case inventory, opt-in eval definitions, reference protocol, dispatcher, helper/check code, consumer guidance and route README. Traced seed → actual B/I capture → explicit faults/corrections → bounded requests and held-back oracles; evaluated coupling, diagnostic history, fixture ownership, native policy and retained helper cost. Shared runtime, root tests and installer were context only. Installer constants, managed guide and package-copy mechanism show no new membership/dependency obligation; they were not changed.

MNT-01 is the sole confirmed blocker. No maintainability scope remains unreviewed. Implementation's local setup/check claims are retained as local preparation evidence, not independent actor qualification. Live agent compliance and T-005 installed composition remain unrun and outside this review. Active-profile drift remains outstanding as described above. The registry's pending reviewer/disposition delta belongs after a successful fresh maintainability review, not to this read-only reviewer.

WARNINGS: NONE

## NEXT

Correction owner: implementer fixes MNT-01 locally and updates affected evidence while retaining original B and all historical pairs/reports. Fresh independent maintainability review is owed for corrected reviewed bytes, with architecture proof re-entered when affected. This review launches no downstream role. After maintainability acceptance, the existing outstanding route is designated contract-registry synchronization → fresh independent discovery → separate acceptance; the native drift duty remains explicit for its owner and later admission decision.

## REVIEWED byte identities

- `skills/task-implementation-flow/README.md`: `3c9a6d11693b376f559e9548cc598cee3928e0fd574d7f6bfb94c920246629fd`
- `skills/task-implementation-flow/task-acceptance-review/SKILL.md`: `811ac82ab0980acf2b8ab6adc752739557f27c04b4a04563ba8e52df94b57abc`
- `skills/task-implementation-flow/task-maintainability-review/SKILL.md`: `3fba205f2a5d4a0da0bfbc740c55af178d18287770a4643b78d396d2e157f4d1`
- `skills/task-implementation-flow/task-maintainability-review/evals/README.md`: `8c940d7259b330d70ae984eb54ed0f87446402f94b8e176424bdbef26333c14f`
- `skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py`: `408869df38dc7a7f66ca0517fa38fdc1a092760f0f0d2f2c30ced13f52550350`
- `skills/task-implementation-flow/task-maintainability-review/evals/files/review_cases.json`: `dc12fdf88d4ff16b0cfc54f6ca36b722dbb229b83e9772d1e8199d944e94e763`
- `skills/task-implementation-flow/task-maintainability-review/evals/files/review_fixture.py`: `fa48f9b79bb8e74dabfa088af3c2a2c667d29c9759f0d463cd3caa0728dc8b3f`
- `skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py`: `36e97bf52a31e9d13e078b1f9a5c23cbdb16657a68cada94d5a5314f71388484`
- `skills/task-implementation-flow/task-maintainability-review/evals/review-evals.json`: `e4cf657b95e25e4337d609d8fa4d8b37314e93b889df0964293f2e3f9887646c`
- `skills/task-implementation-flow/task-maintainability-review/references/measurement-review.md`: `634909b9b15a3504396a870c1c0f7eea5b0fd99843df6e5bbaf37f8e9574c342`
- `skills/task-implementation-flow/task-review-discovery/SKILL.md`: `cd7554b050f51116688aae287ed08ea96ae5dd8349bfaf054bcdfe02a07ba95f`

Policy/boundary sources: repository AGENTS.md; docs/project-map.md; docs/development.md; tests/test_architecture.py; docs/contracts/index.json and measurement/implementer-feedback/installation records; T-004 brief/verification/preflight/implementation; installed maintainability/testing skills. Source workflow changes are implementation specifications.

## Exact Git status around report write

Before:

```text
A  docs/tasks/T-004/brief.md
A  docs/tasks/T-004/verification.md
M  docs/tasks/index.json
 M skills/task-implementation-flow/README.md
 M skills/task-implementation-flow/task-acceptance-review/SKILL.md
 M skills/task-implementation-flow/task-maintainability-review/SKILL.md
 M skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py
 M skills/task-implementation-flow/task-review-discovery/SKILL.md
?? docs/tasks/T-004/implementation.md
?? docs/tasks/T-004/preflight.md
?? skills/task-implementation-flow/task-maintainability-review/evals/README.md
?? skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py
?? skills/task-implementation-flow/task-maintainability-review/evals/files/review_cases.json
?? skills/task-implementation-flow/task-maintainability-review/evals/files/review_fixture.py
?? skills/task-implementation-flow/task-maintainability-review/evals/review-evals.json
?? skills/task-implementation-flow/task-maintainability-review/references/measurement-review.md
```

After:

```text
A  docs/tasks/T-004/brief.md
A  docs/tasks/T-004/verification.md
M  docs/tasks/index.json
 M skills/task-implementation-flow/README.md
 M skills/task-implementation-flow/task-acceptance-review/SKILL.md
 M skills/task-implementation-flow/task-maintainability-review/SKILL.md
 M skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py
 M skills/task-implementation-flow/task-review-discovery/SKILL.md
?? docs/tasks/T-004/implementation.md
?? docs/tasks/T-004/preflight.md
?? docs/tasks/T-004/reviews/maintainability-01.md
?? skills/task-implementation-flow/task-maintainability-review/evals/README.md
?? skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py
?? skills/task-implementation-flow/task-maintainability-review/evals/files/review_cases.json
?? skills/task-implementation-flow/task-maintainability-review/evals/files/review_fixture.py
?? skills/task-implementation-flow/task-maintainability-review/evals/review-evals.json
?? skills/task-implementation-flow/task-maintainability-review/references/measurement-review.md
```

Only the new durable report entry was added by this write. New independent measurement reports are ignored authorized artifacts. The report does not review itself. Index SHA-256 preserved: `30e5d83da9b771347ae14364755f8cc36d9fd758f9f4bfd8f4b906697b97f7f2`.
