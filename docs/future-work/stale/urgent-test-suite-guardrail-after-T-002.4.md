# Immediate test-suite growth guardrail — execute after T-002.4

**Repository:** [`trusovn/personal-skills`](https://github.com/trusovn/personal-skills)  
**Working branch:** `t-o-new-flow`  
**Prepared:** 2026-10-10; inspected branch HEAD `529c24a4face580fa7fd6c7032e0994a30a251c5`  
**Status:** **Small, implementation-ready change proposal**, not yet executed or approved in the repository  
**Related longer-term proposal:** `test-suite-maintainability-integration-proposal.md` (separate document)  
**Scheduling:** **After T-002.4 is independently accepted, before preparing/implementing T-003**

## Decision in one paragraph

**Do a two-file prevention patch now; keep reviewer-side scope expansion out of T-003.** Add a short repository-specific test-maintenance rule to root `AGENTS.md` and a matching pre-edit decision to `bounded-task-implementer/SKILL.md`. Do **not** refactor existing tests or fixtures, add a new stage, modify `testing-discipline`, or reopen T-002.4. The accepted project plan explicitly tells T-003 to **remove the maintainability review's blocker cap without widening its review scope**. Therefore a test/eval-architecture reviewer expansion must be a **separately authorized follow-up**, ideally after T-003 and before T-004 if worthwhile, not a silently added T-003 requirement. This makes prevention effective during ongoing work without disrupting the reviewed task contracts.

## 1. Why this small intervention is justified

Current evidence shows substantial test/eval fixture growth, replicated synthetic scenarios, and large tests enforcing implementation text and fixture structure. Some new scenarios are justified; the preventable problem is that routine agents tend to **append evidence** without first checking existing tests for reuse, replacement, or redundancy.

The core policy already exists in [`testing-discipline/SKILL.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/testing-discipline/SKILL.md): preserve meaningful regression coverage, avoid duplicate evidence, maintain legible fixtures, and remove obsolete/redundant tests only after demonstrating retained protection. The routine implementation flow does not reliably apply that policy, and current maintainability review focuses on changed *production* bytes.

**T-002.4 status at inspection:** `docs/tasks/T-002.4/results.md` says implementation is complete and **submitted for fresh independent review**. Treat this as pending, not completed/accepted. Its local composition and installation checks are not T-005's actual agent-compliance qualification. Do not touch T-002.4's owned source, fixtures, or review records while acceptance is outstanding.

## 2. Precondition and handoff boundary

Start only when all of these hold:

1. T-002.4 has a **current independent acceptance decision** and the required coordinator continuation has authorized the next work. If it has findings, complete its correction/re-review first.
2. Confirm the latest HEAD, `git status`, active worktrees/agents, and current skill copies. The cited HEAD is a reference point, **not** an instruction to assume those bytes remain current.
3. Check whether T-003 has already been briefed/started. If its scope is already frozen or the same files have concurrent owners, merge this delta into the authorized owner rather than creating competing edits.
4. Use **source** `skills/...` as authoritative. T-002.4 reported `.agents/skills` to be stale; never validate the change using a mixed old installation without labeling it as such.

Do not revise `docs/project-plan.md`, `docs/task-map.json`, an existing accepted review, or T-002.4's historical results merely to implement this guardrail. Follow the repository rule to record new outputs separately.

## 3. Immediate patch: strictly two source files

### Edit A — root `AGENTS.md` (outside installer-managed markers)

Add one short, repository-specific rule near the existing verification guidance. Suggested meaning (adapt phrasing to current text):

> **Test/eval maintenance for changes in this repository:** Before adding or expanding tests, skill evals, or fixture builders, inspect the closest existing evidence and the owning fixture/module. Decide whether to retain, update/extend, add, or safely supersede a test. Add a separate case only for a distinct behavior, credible failure mode, or observation boundary; preserve required AC/scenario coverage and reviewer regressions. Reuse existing setup before duplicating cross-skill fixture construction. Do not reorganize unrelated suites within a bounded feature task. A passing structural/text assertion is not proof of agent behavior. For material test-harness changes, apply `testing-discipline` from the selected skill installation when available.

Keep `AGENTS.md` short; point to the canonical skill instead of copying its full policy. **Do not alter `<!-- personal-skills:development-install:* -->` content by hand**; the installer owns that block.

### Edit B — `skills/task-implementation-flow/bounded-task-implementer/SKILL.md`

Add a **compact pre-edit test decision** to both guided and high-assurance work through their common rules or consistently placed equivalent instructions. Suggested requirement:

> When adding or materially changing tests/evals, first locate relevant existing test coverage and fixture ownership. For each needed behavior, choose **reuse / update or parameterize / add independent case / retire obsolete overlap with retained proof**. Maintain the complete task verification-scenario-to-evidence mapping; IDs do **not** imply one physical test function per scenario. Reuse present helpers and prefer the smallest local change; do not introduce cross-task shared infrastructure without authority. Consult the installed `testing-discipline` guidance for substantial testing-infrastructure changes, without adding a mandatory extra agent stage.

Keep this inside existing discovery/verification/implement/handoff steps. No new machine status, schema field, artifact, mandatory plan, prompt, or review stage. Report a brief test-evidence decision only if it explains a material non-obvious test replacement/removal or shared-fixture decision; otherwise the existing AC evidence/handoff is sufficient.

**Files deliberately left untouched now:** `testing-discipline/SKILL.md`, `task-verification-designer`, `task-preflight`, `task-maintainability-review`, `skill-creator`, installer manifest, large existing test modules, and all review fixture generators. Existing policy and semantic-scenario ownership remain intact.

## 4. Reviewer-side follow-up: outside T-003's authorized scope

T-003 already owns conditional-stage handoffs, correction/review semantics, and removal of the maintainability review's three-blocker cap. **The accepted `docs/project-plan.md` (T-003 integration boundary) explicitly says not to widen maintainability review scope.** Do not add this proposal to T-003's ACs, verification design, or preflight as though it were part of that task.

If the need remains after T-003 acceptance, request authorization for a **separate small reviewer-side follow-up**, preferably before T-004 starts so that T-004 can qualify and project the final changed skill source. That follow-up's narrow contract would be:

> `task-maintainability-review` assesses material **introduced/worsened design regressions in changed maintainable test/eval/fixture/harness source**, as well as changed production source. Look for unnecessary duplicated scenario setup, cross-owner coupling, unclear ownership, and test-maintenance change locality. Do not block merely for file size, number of cases, intentional independent discovery/acceptance evidence, or mechanical duplication without a demonstrated consequence. Do not redo functional discovery or acceptance. Keep independent authorship, changed-byte freshness, correction invalidation, output fields, and routing coherent for test-only changes.

For that **separate** follow-up, add at most a few **discriminating** verification scenarios rather than dozens of wording assertions:

- **Catch:** a tests-only diff introduces a second cross-skill fixture copy and forces synchronized edits without a justified packaging boundary; reviewer notices the concrete cost.
- **Allow:** a small independent negative boundary case uses local setup or appropriate existing helpers; reviewer does not request speculative abstraction or file splitting.
- **Preserve:** a correction modifies only test/eval source; downstream review uses the current relevant bytes and does not treat a previous decision as current merely because production code is unchanged.

If that separate reviewer patch is not authorized or its timing conflicts with T-004/T-005, defer it transparently. The immediate two-file guardrail remains useful on its own. Do **not** describe current production-focused maintainability reviews as having checked the architecture of test-only diffs.

## 5. Implementation and proof: keep it cheap

For the two-file patch:

1. Read current `AGENTS.md`, the implementer skill, `testing-discipline`, and affected tests; capture the current status and edit ownership. Apply only the two changes above.
2. Run `git diff --check`; manually verify that no generated installer block, review verdict, or machine output schema changed. Trace guided and packaged/high-assurance paths to confirm the rule is discoverable in both.
3. Run the **existing focused local suites** if available and applicable:

   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
   ```

   Adapt to current documented commands if the workflow changes before execution. These checks primarily prove repository/instruction/package consistency; **they do not prove model compliance**. Prefer repairing a now-stale existing assertion over appending another broad exact-wording test. Do not grow `test_review_discipline.py` just to count the policy as tested.
4. Inspect the resulting diff against the two-file limit and provide a concise implementation result, commands/outcomes, skipped behavioral check, and next owner. Apply whichever **existing** independent review route current authority requires; do not invent an additional one.
5. **Before the next agent invocation using installed skills**, schedule a deliberate development-profile refresh from the accepted source, only when no workers are relying on the old installation. The current installer accepts a target repo path: `python3 scripts/install_development_skills.py <target-repo-root>`. Its projection affects managed skills, shared helpers, guide, and marked AGENTS block; verify unmanaged text/files remain intact. Prefer a disposable committed Git target for initial projection proof and inspect status/diff before refreshing the active `.agents` location. Record source versus installed versions; do not assume a source edit updates installed skills automatically. This operational refresh does not claim completion of T-004's future drift/refresh qualification.

A single **authorized**, disposable agent trial can later verify behavior: present an already-covered invariant plus one genuinely missing variant and inspect whether the implementer updates existing evidence instead of duplicating it. **Optional now**; if not run, report policy wiring as verified but behavioral effect as unverified. Do not silently spend model-eval budget or claim T-005 qualification.

## 6. Should verification/preparation skills be rerun?

| When | Skill/check | Decision and reason |
| --- | --- | --- |
| Immediately after T-002.4 acceptance, before patch | `testing-discipline` | **Optional focused consultation only**. The canonical maintenance policy already exists; another broad test strategy is unnecessary. |
| Immediately after patch | Existing focused tests + source/installed projection check | **Yes.** These validate the two affected sources and guard against stale `.agents` skill use. They are checks, not a new lifecycle stage. |
| When preparing T-003 | `task-brief-designer` → `task-verification-designer` → `task-preflight` | **Yes, follow the already-planned packaged preparation path, with T-003's original scope unchanged.** Record this issue as non-blocking follow-up context only; do not revise T-003 ACs to expand reviewer scope. |
| After T-003 implementation | `task-maintainability-review` followed by existing discovery/acceptance route where required | **Yes, under T-003's existing scope.** It must not claim to inspect test-only architecture until a separately authorized extension is implemented. |
| After T-003 acceptance, ideally before T-004 | Separate **reviewer-scope follow-up**, if authorized | **Consider**, rather than silently integrating into T-003. Broaden `task-maintainability-review` to maintainable test/eval/harness source with independent test-only provenance and targeted verification; if timing is poor, defer beyond T-005. |
| Now | `repo-foundation` / `architecture-guardrails` | **No full rerun.** No new repository foundation, command, CI gate, or deterministic invariant is needed. File-size heuristics should remain advisory. |
| Now | `foundation-readiness-review` | **No full rerun.** It is a repository-foundation, pre-planning review and writes its own report; it is disproportionate for two policy paragraphs. Use a narrow installed-skill routing/projection smoke check instead. Revisit after T-004 only if actual onboarding/routing problems remain and the needed foundation inputs exist. |
| Now | `project-plan-verification` | **No.** `docs/project-plan.md` and `docs/task-map.json` already have an accepted review and are not being revised. Re-run only for a material plan/flow authority change. |
| After T-004 / during T-005 | Installed-flow behavior qualification | **Keep T-005's planned role.** Its independently authorized tests can reveal whether agents act on the policy; local text tests cannot substitute. |

## 7. Explicit exclusions: do not let the patch grow

- **No fixture refactor now:** don't extract discovery/acceptance builders, split `test_review_discipline.py`, shrink orchestrator tests, or reorganize `task-brief-designer/tests/test_package_resources.py` while upstream flow contracts are changing.
- **No test deletion quota or LOC threshold:** growing files are leads, not verdicts. Do not reduce meaningful coverage to improve metrics.
- **No new orchestration states, reviewer role, mandatory testing call, CI/lint tool, eval platform, schema, registry ownership, or history rewrites.**
- **No change to review authority:** discovery gathers current evidence, acceptance decides, coordinator controls continuation, maintainability reviews architecture when applicable.
- **No simultaneous T-002.4 correction and guardrail edits** in the same changed bytes without explicit coordinated authority.

## 8. Completion conditions and next action

**Immediate patch complete when:**

- T-002.4 is independently accepted, and the follow-up patch has explicit ownership and a cleanly separable diff.
- Both source files contain the compact existing-test maintenance rule, with no overwritten installer-managed content.
- The implementer can choose reuse/update/safe replacement rather than automatically adding another test, while preserving task scenario and reviewer evidence obligations.
- Existing targeted checks and a version-consistent installation check are reported truthfully (or limitations are explicit).
- No existing fixture/eval corpus has been rewritten, and no new full skill-stage requirement has been invented.
- The reviewer-side scope expansion is explicitly **outside T-003** and is recorded as a separately authorizable follow-up or a conscious deferral; T-003 remains bound to the approved no-scope-widening rule.

**Not yet proven by this patch:** that agents consistently behave differently, that the current maintainability reviewer catches test-only regressions, or that existing fixture debt is removed. Test-only reviewer coverage belongs to the separately authorized follow-up; actual agent compliance belongs to separately authorized behavioral qualification (e.g. T-005); fixture cleanup is later bounded work.

**Next after patch:** prepare T-003 using the refreshed authoritative source/installed skills **without expanding T-003's ACs**. After T-003 acceptance, decide whether a separate narrow reviewer enhancement is worth fitting before T-004 or should be deferred. Keep the broader test-suite-maintainability proposal as design context, not as license to expand existing tasks.
