# T-004 implementation result

Status: `READY_FOR_REVIEW` after MNT-01 correction; see `correction-01.md` for current comparison/native evidence and the unchanged reviewer finding status.

The source maintainability workflow now requires a fresh reviewer comparison against the original baseline, verifies actual affected responsibilities, records every required rationale disposition, and carries current native evidence and the applicable ordered route. The source discovery and acceptance skills consume that evidence without repeating general maintainability review.

## Preparation and ownership

- Active execution: project-local installed `.agents/skills/task-implementation-flow/bounded-task-implementer/SKILL.md` and `.agents/skills/testing-discipline/SKILL.md`. Changed source skills are development specifications; the active installation was not refreshed.
- Consumed `docs/tasks/T-004/brief.md` revision 1, `verification.md` revision 1 and `preflight.md`. Preserved staged user brief/verification/task index and the supplied preflight.
- Before edits, validated original B against exact HEAD `6b80c8eecad0943c3a9ed9695f1f27ff124df5b2`, logical repository, complete three-file Python inventory and actual source hashes, installed adapter hash, settings hashes, selected checks and governed folders. Pinned environment confirmed CPython 3.14.6, Radon 6.0.1 and Ruff 0.14.2.
- Inspected installer constants `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`, the profile guide, focused installer tests and README installation instructions. Membership/dependencies/ownership remain unchanged; existing package projection copies the new resources. No installer or guide declaration became stale.
- Optional run-evidence availability passed, but an attempted lifecycle query used unsupported `status` instead of `active`. Per installed skip-once policy, invocation instrumentation was abandoned with no setup/repair or replacement lifecycle. This does not supply or replace measurement/native evidence.

## Deliverables and actual contract impact

- Required reviewer reference `references/measurement-review.md` plus updated inputs/protocol/report/correction guidance.
- Local review-case catalog and fixture/check commands reuse existing author-measurement and maintainability semantic/test/multi-blocker setup. Existing evals 1–10 are preserved; six new representative opt-in actor evals in `review-evals.json` reference the finite catalog; legacy `evals.json` is byte-identical to HEAD.
- Minimal consumer guidance in discovery, acceptance and task-flow README.
- Added/changed durable source guidance: reviewer-owned original-baseline comparison, full rationale disposition and native-evidence handoff (CAP-004/ART-005/IF-003; ART-003/006/008). No runtime CLI/schema/architecture policy was changed.
- Executable/declarative contract declarations changed: task-owned `task-maintainability-review/evals/review-evals.json` opt-in setup invocations. No shared runtime CLI/schema changed. Registry synchronization remains with the designated updater.

## Current correction

Fresh review `reviews/maintainability-01.md` found MNT-01: the former 85 catalog
rows had 82 selectable identities, with V-11a/b/c each duplicated. The catalog
now has **82 canonical selectable cases**. Both former situation/oracle texts
are retained verbatim in their respective canonical row. The existing matrix
rejects duplicate IDs before setup and checks every returned case field against
the requested row. Current correction checks: five tests passed over all 82
cases; owning reviewer suite 26 passed; architecture four passed; contracts
passed. Current original-B comparison is `.quality/reports/T-004-correction-01.json`
and `.txt`, with fresh native input identity04. All previous pairs/reviews/logs
remain history. The former independent-85-case claim was wrong and is corrected
below. Fresh maintainability review must determine MNT-01 disposition; the
implementer does not self-clear it. Full correction ledger, commands, rationale,
proof limits and first outstanding route are in [correction-01.md](correction-01.md).

## Scenario evidence map

All IDs below use the exact local setup entry `python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py review:<ID>` in a unique disposable `EVAL_WORK_ROOT`, explicit `EVAL_SOURCE_ROOT` and already pinned `EVAL_MEASUREMENT_PYTHON`. `files/review_cases.json` supplies each exact situation and artifact oracle. The corrected focused `check_review_fixture.py` command exercises every listed setup and selected real CLI/native boundaries, rejects duplicate selection IDs and verifies the full returned requested row. Prepared histories and R-control reports are labeled fixture evidence. Actor decisions and full independent grading remain unrun.

| Verification case / variant | Reused seed / concrete boundary | Submission evidence and limit |
|---|---|---|
| V-01a | `measurement:V-03a`; Fresh session; I matches current bytes | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-01b | `measurement:V-05c-advisory`; Edit submitted code after I, without changing its short-status text | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-01c | `measurement:V-04a-complexity`; This session authored reviewed production bytes | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-01d | `measurement:V-04a-complexity`; Production unchanged; this session authored only reviewed test/eval/harness bytes | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-01e | `measurement:V-07d`; Reviewer uses an isolated clone with another absolute root | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02a | `measurement:V-05a-advisory`; B is missing; current measurement is available | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02b | `measurement:V-04a-complexity`; B comes from another logical project with matching relative paths | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02c-checks | `measurement:V-04a-complexity`; B has an incompatible format, tool version, effective settings or selected checks, varied separately | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02c-format | `measurement:V-04a-complexity`; B has an incompatible format, tool version, effective settings or selected checks, varied separately | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02c-settings | `measurement:V-04a-complexity`; B has an incompatible format, tool version, effective settings or selected checks, varied separately | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02c-tools | `measurement:V-04a-complexity`; B has an incompatible format, tool version, effective settings or selected checks, varied separately | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02d-baseline | `measurement:V-05b-advisory`; B or current report is incomplete, or omits required selected-profile coverage | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02d-current | `measurement:V-05b-advisory`; B or current report is incomplete, or omits required selected-profile coverage | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02d-profile | `measurement:V-05b-advisory`; B or current report is incomplete, or omits required selected-profile coverage | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02e | `measurement:V-05f-advisory`; Runtime or pinned analyzer unavailable; advisory evidence is not indispensable | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02f | `measurement:V-05f-required`; Same unavailable evidence, with explicit task/repo authority making it indispensable | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02g-docs | `measurement:V-03e-docs`; Docs-only scope; separately unsupported-language scope | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02g-unsupported | `measurement:V-03e-docs`; Docs-only scope; separately unsupported-language scope | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02h-json | `measurement:V-07c`; Proposed output collides with existing JSON; separately only its text sibling exists | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02h-text | `measurement:V-07c`; Proposed output collides with existing JSON; separately only its text sibling exists | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02i-external | `measurement:V-04a-complexity`; Caller requests an external durable review path or an already occupied numbered path | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-02i-occupied | `measurement:V-04a-complexity`; Caller requests an external durable review path or an already occupied numbered path | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03a | `measurement:V-04a-complexity`; Complexity 6 → 8; statements 40 → 49; arguments 3 → 4 | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03b | `measurement:V-04b-complexity`; Complexity 9 → 10; statements 49 → 50; arguments 4 → 5 | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03c | `measurement:V-04c-complexity`; New function at 11 complexity, 51 statements or 6 arguments | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03d | `measurement:V-04d-complexity`; Existing function crosses 10 → 11, 50 → 51 or 5 → 6 | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03e | `measurement:V-04e-complexity`; Existing breach worsens 11 → 12, 51 → 52 or 6 → 7 | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03f | `measurement:V-04f-complexity`; Materially edited hotspot stays 11 → 11, 51 → 51 or 6 → 6 | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03g | `measurement:V-04g-complexity`; Materially edited hotspot improves 12 → 11, 52 → 51 or 7 → 6 | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03h | `measurement:V-04h`; Materially edited hotspot reaches 11 → 10, 51 → 50 or 6 → 5 | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03i | `measurement:V-04k`; A required rationale is missing or omits its plausible alternative's cost | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-03j | `measurement:V-04e-statements`; One cohesive design explanation covers related breached metrics | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-04a | `measurement:V-03b`; Another function changes; legacy sibling only shifts lines or receives formatting | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-04b | `measurement:V-04f-complexity`; Implementer labels a behaviorally or structurally edited hotspot untouched | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-04c-extract | `measurement:V-03c-extract`; Function renamed; separately moved; separately extracted into helpers | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-04c-move | `measurement:V-03c-move`; Function renamed; separately moved; separately extracted into helpers | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-04c-rename | `measurement:V-03c-rename`; Function renamed; separately moved; separately extracted into helpers | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-04d | `measurement:V-03d`; A native count is absent on one side, such as an exempt override method | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-05a | `measurement:V-04j`; Extraction lowers a metric but adds misleading names/navigation, opaque argument containers or speculative forwarding layers | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-05b | `semantic-defects`; Existing `semantic-defects` reservation/recovery variant | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-05c | `semantic-control`; Existing `semantic-control` variant with explicit protocol branches, caller-locked mutation and documented legacy wire name | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-05d | `test-assets`; Existing `test-assets` defect variant; production unchanged and ordinary suite green | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-05e | `test-assets-control`; Existing `test-assets-control` with independent observations and stable text assertion | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06a | `four-blockers`; New/worsened required hard architecture violation; comparison completes successfully | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06b-NA | `measurement:V-08h`; Required native correctness check fails; metrics complete, then separately metrics N/A | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06b-complete | `measurement:V-08h`; Required native correctness check fails; metrics complete, then separately metrics N/A | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06c | `measurement:V-08b`; Required proof missing; owner can supply it | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06d | `measurement:V-08f`; Saved pass has stale checked bytes; an authorized focused run is available | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06e | `measurement:V-08g`; Required gate unavailable; no valid current evidence or documented exception | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06f | `measurement:V-08d`; Current aggregate establishes included commands, whole-project scope, policy and checked bytes | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06g-bytes | `measurement:V-08d`; Aggregate omits a required constituent, narrows whole-project scope, lacks policy coverage or has stale bytes, varied separately | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06g-constituent | `measurement:V-08d`; Aggregate omits a required constituent, narrows whole-project scope, lacks policy coverage or has stale bytes, varied separately | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06g-policy | `measurement:V-08d`; Aggregate omits a required constituent, narrows whole-project scope, lacks policy coverage or has stale bytes, varied separately | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06g-scope | `measurement:V-08d`; Aggregate omits a required constituent, narrows whole-project scope, lacks policy coverage or has stale bytes, varied separately | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06h-documented | `measurement:V-08b`; Commands documented without a registry; separately no native commands exist | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06h-none | `measurement:V-08b`; Commands documented without a registry; separately no native commands exist | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06i | `measurement:V-04a-complexity`; Policy sources conflict on requiredness or hard/advisory semantics | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06j-available | `measurement:V-09a`; Optional run-evidence wrapper captures a real comparison; separately wrapper unavailable | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-06j-unavailable | `measurement:V-09a`; Optional run-evidence wrapper captures a real comparison; separately wrapper unavailable | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-07a | `four-blockers`; Full bounded scope is available; an early blocker already decides the verdict | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-07b | `genuine-stop`; Genuine permission/capability/budget stop prevents completing coverage | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-07c | `measurement:V-04c-complexity`; All proof current, no semantic/hard blocker, justified retained breaches | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-08a | `four-blockers`; First submitted edit with B/I1/R1 | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-08b | `correction-round`; Second real edit correcting one same-responsibility finding | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-08c | `correction-round`; Surviving and corrected finding ledger | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-08d | `measurement:V-04a-complexity`; Separate change outside reviewed scope | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-09a | `measurement:V-05e-advisory`; Expansion not yet authorized | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-09b | `measurement:V-07a`; Authorized expansion; exact preserved pre-edit bytes are verifiable | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-09c | `measurement:V-07b`; Authorized expansion; exact pre-edit evidence unavailable | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10a | `measurement:V-04a-complexity`; Maintainability accepted; registry stage applies and changed durable contracts require sync | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10b-absent | `measurement:V-04a-complexity`; No registry stage exists; separately registry evidence is already current | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10b-current | `measurement:V-04a-complexity`; No registry stage exists; separately registry evidence is already current | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10c | `measurement:V-04a-complexity`; Maintainability, applicable registry and discovery already current | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10d | `measurement:V-04a-complexity`; Functional correction changes significantly reviewed test/eval/harness responsibilities | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10e-exception | `measurement:V-04a-complexity`; Ordinary assertion correction fits an explicit trivial-change exception, or earlier reviewed scope is demonstrably unaffected | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10e-unaffected | `measurement:V-04a-complexity`; Ordinary assertion correction fits an explicit trivial-change exception, or earlier reviewed scope is demonstrably unaffected | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10f-blocker | `measurement:V-04a-complexity`; Maintainability report is stale, incomplete or has an unresolved applicable blocker | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10f-incomplete | `measurement:V-04a-complexity`; Maintainability report is stale, incomplete or has an unresolved applicable blocker | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-10f-stale | `measurement:V-04a-complexity`; Maintainability report is stale, incomplete or has an unresolved applicable blocker | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-11a | `measurement:V-04a-complexity`; Reconcile V-01–V-10 with eval definitions/setup and retained existing scenarios All case inputs and report-write boundaries | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-11b | `measurement:V-04a-complexity`; Run changed fixture checks and relevant measurement coverage Wrong/stale/missing output controls | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |
| V-11c | `measurement:V-04a-complexity`; Inspect installer/profile/shared-file declarations, focused installer coverage and README installation guidance; project changed packages into a disposable target Disposable installed resources | Prepared; local setup/tool checks below. Fresh actor behavior unqualified. |

The catalog covers every V-01a–e, V-02a–i, V-03a–j, V-04a–d, V-05a–e, V-06a–j, V-07a–c, V-08a–d, V-09a–c, V-10a–f and V-11a–c. Separate format/tool/settings/check, report sibling, relationship, native-coverage and route variants preserve their distinct controls. V-03 complexity decision inputs reuse the owning suite’s real statement/argument boundary evidence; no Cartesian product is added.

## Verification and proof limits

- Historical finite fixture suite: 5 tests passed in 63.494s while iterating 85 catalog rows, which represented only 82 unique selectable IDs; the three duplicate V-11 IDs made later oracle rows unreachable. This was not evidence of 85 independent variants. Log `/tmp/T-004-focused-corrected.log`; MNT-01 correction evidence supersedes the affected identity/selection claim. Command: `EVAL_SOURCE_ROOT=/Users/mtrusov/work/skill-sources/personal-skills EVAL_MEASUREMENT_PYTHON=/Users/mtrusov/work/skill-sources/personal-skills/.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python PYTHONDONTWRITEBYTECODE=1 python3 skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py`. It exercises actual fresh R/stale I hashes, original/index/history preservation, native whole-scope failure/recovery, two real correction comparisons against B and four real complexity-11 obligations. Synthetic candidate claims reject omitted disposition, stale hash and skipped registry/discovery route against exact independent input facts; no general semantic grader or actor run is claimed.
- Owning existing reviewer suite after the legacy-fixture correction: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py`: 26 passed in 2.509s, `/tmp/T-004-owner-01.log`. This covers preserved four-blocker, genuine-stop, semantic and test-asset behavior, as well as contract safeguards. The earlier focused suite omitted this existing owner; the aggregate exposed that gap and its failures were corrected before handoff.
- Real pinned measurement suite: `.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py`: 33 passed in 16.325s, `/tmp/T-004-measurement-01.log`; includes at/below/above numeric boundaries, unknown counts, compatibility, collisions, original-baseline/installed CLI and native separation.
- Installer suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`: 36 passed in 29.648s, `/tmp/T-004-installer-01.log`. Final aggregate reruns this owning coverage after source corrections.
- Canonical architecture: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`: 4 passed after correction, `/tmp/T-004-architecture-02.log`.
- Contracts: `python3 tools/check_contracts.py --root .`: passed after correction, 7 subsystems / 22 plan refs, `/tmp/T-004-contracts-02.log`. Structural consistency does not certify the source guidance or registry semantic currency; updater remains outstanding.
- Explicit current hard-gate control: `setup_fixture.py review:V-06a` in `/tmp/T-004-hard-gate-final`, same explicit source/interpreter environment, produced completed metrics and actual `src.billing.receipts imports src.billing.service` gate failure (exit 1, no traceback). Raw commands/oracle remain in its `task-runs/` directory. This distinguishes a real rule violation from the earlier broken embedded gate.
- Installed new-entry proof after correction: invoked `/tmp/T-004-hard-gate-final/maintainability/.agents/skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py review:V-01a` with explicit distribution, pinned interpreter and fresh root `/tmp/T-004-installed-review-corrected`; actual disposable install/B/I succeeded, `/tmp/T-004-installed-entry-02.log`. Setup explicitly consumes the source distribution for fixture reuse/installation; agent measurement uses the target installation, with no global/active fallback.

Historical failures remain available: `/tmp/T-004-focused-01.log` records wrong test expectations for incompatible exit status and baseline-path location; corrected by focused-02/03/final. `/tmp/T-004-aggregate-01.log` records sandbox containment/loopback denial plus source-local legacy fixture integration failures. The latter were an accidental dispatch insertion inside the embedded gate string, analyzer-dependent new evals mixed into dependency-free legacy eval execution, and one omitted warning safeguard sentence. The gate string was restored, new definitions moved to opt-in `review-evals.json`, and the safeguard retained. No root test was edited. `/tmp/T-004-aggregate-unsandboxed-01.log` began before those source corrections and is historical, not current byte proof.

Local setup/tool and synthetic candidate-oracle checks never prove fresh agent compliance. Live model evals, independently graded actor reports and T-005 installed composition were not run. Actor-level expected verdicts/dispositions/routes for every matrix row remain prepared, not behaviorally qualified.

## Original measurement and native evidence

Original B (retain both): `.quality/reports/T-004-preflight-20261104-01.json` and `.quality/reports/T-004-preflight-20261104-01.txt`. Governed folders: source maintainability, discovery and acceptance packages. Included three pre-edit eval fixture Python assets; new Python files stay in the captured maintainability package. Root tests/shared runtime were read/reused, not edited.

Pre-correction comparison pair (retained history): `.quality/reports/T-004-implementation-02.json` and
`.quality/reports/T-004-implementation-02.txt`. Executed:

```sh
python3 -B .agents/scripts/measure_maintainability.py compare skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py skills/task-implementation-flow/task-maintainability-review/evals/files/review_fixture.py skills/task-implementation-flow/task-maintainability-review/evals/files/check_review_fixture.py --root /Users/mtrusov/work/skill-sources/personal-skills --baseline .quality/reports/T-004-preflight-20261104-01.json --output .quality/reports/T-004-implementation-02.json
```

Result: complete, full-profile, compatible `compared`; all three affected Python
paths are `eval_or_harness`. Original inventory/settings and B remain unchanged. Comparison-01 and native-bytes-01 are retained historical pre-correction artifacts; they are superseded only for the repaired setup bytes, not deleted or relabeled.
`setup_fixture.py` only adds a top-level dispatch; its existing functions are
untouched. The two new files are task-local fixture/check responsibilities, not
renames/extractions of existing source functions. Their before counts are absent,
not zero. Discovery/acceptance source changes are Markdown only; their existing
Python helpers stay untouched.

Historical initial-submission retained-structure rationale (the affected matrix is updated in correction-01.md; other accepted groups are unchanged):

| Function | Metric; known before → after | Cohesion and useful alternative cost |
|---|---|---|
| `ReviewFixtureTests.test_every_finite_setup_supplies_real_inputs_and_preserves_history` | complexity absent → 12 | One finite setup matrix checks common preservation plus the distinct fault oracle reached by each case. Splitting one test per seeded fault repeats the same subprocess/snapshot authority and obscures complete catalog traversal; subtests retain case identity. |
| `review_fixture.seed` | complexity absent → 18 | Owns the two existing fixture families and exact before/submitted restoration for real B. Reusing their subprocess setup avoids copying infrastructure. Separate per-case seed callbacks would duplicate distribution/restore ordering or require a registry for one caller. |
| `review_fixture.native_inputs` | complexity absent → 13 | Native policy/evidence variants share one whole-scope command/aggregate boundary. Named branches make real failures and intentionally edited claims visible together. Splitting into tiny mutators adds navigation and hides which claims remain seeded versus executed. |
| `review_fixture.evidence_fault` | complexity absent → 14 | One owner varies exactly one evidence prerequisite at a time and labels forged consumer claims. A generic field-path mutation framework would hide decisive facts and increase configuration interpretation; local named branches are easier to audit. |
| `review_fixture.route_inputs` | complexity absent → 17 | Builds one cohesive upstream conditional-history input with actual reviewed-byte identity and separate consumer requests. A dispatch/strategy layer would spread current/stale/absent stage policy over callbacks, with no second consumer of those builders. |
| `review_fixture.prepare` | complexity absent → 27; statements absent → 58 | Keeps the authorized preparation order visible: reuse seed, create real author evidence, inject named faults, stage rationale/correction/route inputs, then publish permission-bounded request and held-back oracle. Local helpers already own native/evidence/correction/report/route groups. Further splitting the short case-specific source changes or request clauses into single-use callbacks would scatter setup ordering and permission authority. A future independent fixture family could justify another local helper; no analyzer/settings changes or metric-only split was made. |

Report transfer uses shared workspace paths now. If an isolated root `<clone>` is
selected, explicitly copy each original/final JSON and text sibling from
`/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/<name>` to
`<clone>/.quality/reports/<same-name>`, then validate logical project/applicability.
The names are `T-004-preflight-20261104-01.json/.txt` and
`T-004-implementation-02.json/.txt`. Ignored reports do not travel with commits.
Also transfer `T-004-native-bytes-03.json` if consuming the native identity below.
No receiving clone was selected during this invocation.

Pre-correction native checks bind to the then-current complete Git-visible input inventory (441
paths) in `.quality/reports/T-004-native-bytes-03.json`, digest
`3238ea0844c7f3de42601030abd387215d1eb46313fafb1c598a6787834c1b0a`.
This includes new/untracked code, skill/config/eval/docs inputs and all governed
repository inputs; only this reporting result is excluded to avoid self-reference.
Earlier native-bytes-01/02 Python-only manifests are preserved history, not a
claim that the full aggregate scope is only Python. Producer/stage: this installed implementer invocation.
Native policy: AGENTS.md and docs/development.md, whole-repository CLEAN architecture,
contract consistency and cross-cutting aggregate before handoff. Historical command
results and raw logs are recorded below. Corrected native evidence is recorded in correction-01.md; the aggregate below is not current proof for changed harness/data bytes.
No additional formatter/lint/typecheck/build/server obligation exists. Metrics
and optional instrumentation do not waive native failures or missing proof.


## Current aggregate result and remaining duties

`python3 tools/verify.py`, approved outside the sandbox for the real macOS
containment/loopback tests, completed on the initial submission, before MNT-01 correction. Raw output:
`/tmp/T-004-aggregate-unsandboxed-02.log`. Seven composed checks ran; **one failed**:
active installation profile drift. All maintained suites passed: 3 + 13 + 4 +
207 + 309 = 536 tests, with 31 optional analyzer skips in the default root suite (30 need real Radon/Ruff; one needs real pinned dependencies).
The separately pinned 33-test owning measurement run supplies its actual tool
coverage; skips are not treated as behavioral qualification. The aggregate's
contract constituent passed. Existing containment failures from the sandboxed
attempt were cleared in the approved run; no hard rule was weakened.

The failed constituent is exactly `python3 scripts/install_development_skills.py
--check .`: 112 managed paths compared, 10 changed/missing current source resources
across the three source review packages. This is a real nonzero required
aggregate result, **not a clean aggregate pass**. The brief/repository forbid
refreshing the active installation during this invocation, so it remains
unresolved as an environment/distribution duty. Disposable installation and
projection tests demonstrate the developing source package separately. Owner:
coordinator/operator, deliberate between-run installation update when permitted;
reviewers must use their actual resolved installation, or explicitly authorized
fresh source-guided review for source changes, without claiming live installed
qualification. Source T-004 review can assess this recorded limit; the implementer
waives no gate or downstream admission requirement.

Exact shared raw logs remain at the paths above, including historical failures.
For an isolated consumer, copy those named logs to the receiving root's existing
`.quality/reports/` with their same basename, in addition to both measurement
pairs and native manifest03. No receiving clone was selected. Source/index and
staged user preparation remain separable; `git diff --check` passed. No runtime,
root tests, installer, registry records, plan documents or active installation
were edited by this implementer.

First outstanding stage: fresh `task-maintainability-review`. It must assess all
significant eval/harness additions, the retained-structure rationales above and
current native evidence. Then `task-contract-registry-updater` records actual
reviewer/disposition/consumer guidance and proof limits; fresh independent
`task-review-discovery` corroborates preparation and current evidence; separate
`task-acceptance-review` decides advancement. Fresh correction-stage native evidence is required; historical CLEAN architecture
proof is supplied as context, with the reviewer's existing run/validation duty preserved.
No independent verdict is issued here. No live agent compliance, current active
installation parity or T-005 end-to-end composition is claimed.

## Outstanding route

Fresh maintainability review → designated task-contract-registry-updater synchronization → fresh independent task-review-discovery → separate fresh task-acceptance-review. The implementer performs no independent review, registry update or acceptance. The canonical architecture gate is required before handoff; reviewers retain their own run/validation authority.
