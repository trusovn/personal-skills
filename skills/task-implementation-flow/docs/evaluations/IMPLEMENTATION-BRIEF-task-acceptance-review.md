# Implementation brief: make `task-acceptance-review` completeness-first

Status: `ready`

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 26 tool calls / 120 minutes / 80k context
```

This block is intended launch guidance under resolved decision `G-01`; it does
not claim an observed runtime configuration.

This brief is self-contained implementation authority for the
`task-acceptance-review` changes derived from the 2026-07-21 flow evaluation.
An implementer may inspect the repository paths named here, but should not need
to read the source evaluation or this conversation.

## Outcome

Make independent review account for explicit finite risks before broad
regression, report multiple independently demonstrable defects in one pass,
name broken invariants and unchecked areas, and optionally preserve a
deterministic failing test after `CHANGES_REQUESTED` under a tightly bounded
tests-only protocol.

Keep ordinary review read-only. Enter the tests-only protocol only after fixing
`CHANGES_REQUESTED` and confirming both explicit current-invocation
authorization and an exact writable test path or area.

## Why this change is justified

- Independent review was the highest-value role. Across S3-07 and S3-08 it
  found at least eleven material behavioral defects missed by passing focused
  and aggregate suites, including real process, tamper, and crash/recovery
  failures.
- Review also became the dominant S3-08 cost: six review sessions consumed
  51.3% of its uncached-input plus output proxy, compared with 40.8% for three
  S3-07 review sessions.
- Findings were fragmented. S3-07 took three reviews within one cleanup risk
  family. S3-08 took five finding rounds across two risk families already
  explicit in the contract.
- Broad suites were sometimes run before a later decisive adversarial probe,
  and a first finding often ended exploration of independent sibling cases.
- Reviewer-created regressions were effective handoffs: two S3-07 and seven
  S3-08 tests failed for intended reasons, stayed in owning test files, and
  were consumed directly by correction agents.
- That useful write behavior currently violates the skill's read-only rule and
  occurred only after a second user prompt. It needs explicit authority and a
  protocol, not accidental normalization.

The goal is bounded completeness against explicit contract rows and selected
material risk dimensions—not the impossible promise to “find every bug.”

## Authority and scope

| Item | Contract |
|---|---|
| Primary authority | This brief, derived from `skills/task-implementation-flow/docs/evaluations/EVALUATION-2026-07-21.md` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Canonical skill | `skills/task-implementation-flow/task-acceptance-review/` |
| Active mirror | `.agents/skills/task-acceptance-review/`, read-only during this task and updated only by post-acceptance distribution |
| Allowed canonical changes | `SKILL.md`, `references/acceptance-report-template.md`, a focused conditional tests-only reproducer reference under `references/`, `evals/evals.json`, and `evals/files/setup_fixture.py` |
| Post-acceptance distribution | Corresponding active-mirror files, owned by the separate distribution step after the canonical change receives independent `ACCEPT` |
| Read-only context | Other flow skills, their templates/evals, and `skills/task-implementation-flow/README.md` |
| Out of scope | Active-mirror writes, production-code repair by a reviewer, reviewer self-acceptance after writes, official plan/task updates, production task-orchestrator changes, generic fuzzing, live comparative benchmarking, and cross-skill README integration |
| Dependencies | `G-02` and `G-04` are resolved by the 2026-07-23 notes in `GLOBAL-DECISIONS-task-implementation-flow.md` |

The canonical and mirror directories were byte-identical when this brief was
written. Recheck before editing.

## Resolved decisions and repository coordination

### G-02 — reviewer-written tests require explicit invocation authority

The first release uses option 1: the current user or exact review invocation
must authorize `tests_only_reproducer` and name the exact writable test path or
area. An allowed test path proves scope, not permission, and
`review: immediate` proves timing, not write authority. Production repair
remains out of scope.

Keep this as a conditional post-verdict mode of `task-acceptance-review`, not a
separate runtime role. The reviewer can reuse its demonstrated trigger,
invariant, and remaining context to encode the regression. Put the detailed
procedure in a focused reference loaded only after the verdict and
authorization preconditions are satisfied; do not invoke
`bounded-task-implementer` or imply production-write authority.

### G-04 — bounded coverage continues across reviews

Every explicit finite row and selected material invariant ends as `pass`,
`fail`, `blocked`, or `unchecked` with a reason. Continue while remaining
probes are independent, safe, authorized, and affordable. If review stops
earlier, transfer the complete ledger, findings, regressions, broad-gate
decision, and remaining rows. Prior passes guide the next review but do not
prove corrected bytes.

### Repository coordination facts

- Preserve the pre-existing user change to
  `skills/task-implementation-flow/README.md`; it is outside this task.
- Leave the active mirror unchanged. The post-acceptance distribution owner
  resolves the approved canonical-to-mirror sync/install process after the
  canonical change receives independent `ACCEPT`.

## Required work

1. Add a provenance precondition before review.
   - Independence is based on session authorship, not which skill text is
     currently loaded.
   - If the current session authored any production bytes being reviewed, it
     may provide a clearly labeled `SELF_CHECK_ONLY` report but must not issue
     `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE` as an independent verdict.
   - The self-check route is always a fresh reviewer. Do not represent the lack
     of independence as a clean acceptance or as an environment blocker.
   - If this reviewer later writes a tests-only reproducer, the pre-write
     verdict remains final for that session. Corrected bytes always require a
     new review; the same session may not accept them.

2. Add a completeness-first discovery phase before broad suites.
   - Build a concise coverage ledger:
     `AC/invariant → explicit cases → submitted evidence → independent probe → result`.
   - Give rows stable task-derived identities and record `pass`, `fail`,
     `blocked`, or `unchecked` with a reason. Consume a supplied prior ledger
     as continuation context rather than silently reconstructing a different
     set of rows.
   - Start from explicit contract cases and the material dimensions of selected
     high-risk invariants. Do not expand into open-ended repository archaeology.
   - Batch narrow static traces and independent adversarial probes before the
     aggregate gate.
   - Continue after a finding when remaining probes are independent, safe,
     authorized, and affordable within the task budget.
   - If stopping early, list every unchecked required/material row and the
     concrete stop reason. `CHANGES_REQUESTED` must not imply that all other
     areas are clean.
   - A final verdict against corrected bytes requires current evidence for all
     required rows. A prior `pass` may guide probe selection but cannot be
     copied as current acceptance evidence.

3. Change gate order and ownership.
   - Discovery review: targeted adversarial probes first.
   - After any decisive failure in the current review, do not run a broad or
     aggregate gate merely for completeness.
   - A fresh final review after correction reruns all reviewer regressions,
     completes previously blocked/unchecked rows, runs justified owning checks,
     and owns the aggregate gate once after adversarial evidence is clean.
   - A second correction cycle remains legitimate when a correction introduces
     a new defect, an earlier defect blocked downstream evidence, or authority
     changes.

4. Strengthen finding structure.
   - Keep location, demonstrated trigger, consequence, evidence, affected AC,
     and severity.
   - Add the broken invariant and credible sibling surface implied by the same
     contract.
   - Give the smallest invariant-level corrective direction, not a production
     patch and not a demonstrated-field special case.
   - Separate confirmed findings from unproved questions and from unchecked
     rows.

5. Update guided output and `references/acceptance-report-template.md`.
   - Add the completeness ledger or equivalent checked/failed/unchecked
     accounting.
   - Make the broad-gate decision and reason visible.
   - Permit `SELF_CHECK_ONLY` as a labeled non-verdict path outside the three
     independent verdicts; do not add it as an accepting orchestrator status.
   - Keep high-assurance baseline/freshness sections and the rule that only an
     independent `ACCEPT` advances work.
   - Add a compact copyable `Review continuation` block containing review
     iteration/current byte identity when available, all coverage rows and
     results, finding IDs, reviewer regression paths/commands, broad-gate
     status, and the exact next route.
   - A fresh reviewer must receive the brief, current scoped diff, preceding
     verdict and continuation block, reviewer regressions, and all
     unchecked/blocked rows. Keep guided output human-readable; do not invent a
     machine schema before an orchestrator owns it.

6. Add post-verdict `tests_only_reproducer` as a conditional mode of the same
   skill.
   - Keep its trigger and non-negotiable boundaries in `SKILL.md`; place the
     detailed procedure in `references/tests-only-reproducer.md` and read it
     only after the verdict and authorization preconditions are satisfied.
   - Do not load `bounded-task-implementer` or switch into a production-writing
     role. Reuse the demonstrated review trigger and existing owning test
     conventions only.
   - Fix and report `CHANGES_REQUESTED` before any write.
   - Require explicit write authorization and an exact owning/allowed test
     path. Task scope without write authority is insufficient.
   - Change only existing owning test files or a task-authorized new test file;
     do not create shared harnesses, fixtures outside scope, production code,
     dependencies, plans, result files, trackers, or reports inside the repo.
   - Do not stage, commit, or normalize unrelated Git state.
   - Add only deterministic reproducers for demonstrated findings. Prove each
     focused test fails for the intended behavior, not for setup/import errors.
   - Preserve the pre-write verdict, record exact changed paths and before/after
     status, report side effects, and route to correction followed by a fresh
     reviewer.
   - The reviewer may not fix production code or accept corrected bytes in the
     same session.

7. Extend output/template and the focused reference for an optional
   `Post-verdict reproducer` section containing authorization source, exact
   test paths, command/result, intended failure signal, status/diff side
   effects, and next route. Keep the verdict exactly `CHANGES_REQUESTED`; do not
   invent `CHANGES_APPLIED_REVIEW_REQUIRED` for tests-only writes.

8. Add retrospective evals with real fixtures.

   **Provenance/self-check eval**

   - Add an `authored-production-self-check` fixture at
     `/work/authored-production`, have the same eval session make an authorized
     production edit, then ask it to invoke acceptance review on those bytes.
   - Expect `SELF_CHECK_ONLY`, no independent verdict, and a fresh-review route.

   **Multiple-findings matrix eval**

   - Add a `workflow-matrix-defects` fixture at `/work/workflow-runner` with at
     least two independent defects under explicit matrices: coherent prompt and
     model tampering reaching execution;
     execution-only replay failing after verifier drift; and a contradictory
     decision-only artifact reaching execution.
   - Supply real local entry commands and disposable persisted state so each
     defect is independently observable.
   - Expect one review to report every independently reproducible finding,
     identify any blocked row, and skip the aggregate suite after the first
     decisive failure.
   - Add an eval variant with a supplied prior ledger containing pass, fail,
     and unchecked rows. Require stable row identities, completion of remaining
     independent probes, current evidence rather than copied prior passes, and
     a complete continuation block for the next reviewer.

   **Same-risk-family process eval**

   - Add a deterministic `process-cleanup-defects` fixture at
     `/work/process-runner` covering a resistant descendant, an already-exited
     leader with a descendant holding inherited pipes, and a transient
     signal/visibility race.
   - Use observable synchronization and bounded polling/events; no arbitrary
     sleeps or unbounded waits.
   - Expect one review to batch the material lifecycle cases and report the
     cleanup invariant, not stop after the first leak.

   **Tests-only reproducer eval**

   - Reuse a simple deterministic defect such as `queue-defect` where possible.
   - Explicitly authorize only the owning test file in the review prompt.
   - Expect a fixed `CHANGES_REQUESTED` verdict before writes, only that test
     file changed, a focused intended failure, production unchanged, status and
     diff reported, and a mandatory fresh-review route.
   - Preserve every pre-existing eval unless this task explicitly revises its
     expectation. Treat the complete pre-existing-plus-new eval file as the
     owning regression set. If runner availability or paid/live authorization
     prevents execution, list the exact skipped eval IDs and do not claim the
     affected unchanged behavior.

9. Keep the active mirror unchanged during implementation and canonical
   acceptance. After an independent `ACCEPT`, hand the accepted canonical paths
   to the separate distribution owner, who resolves the approved sync/install
   process and proves byte identity.

## Acceptance criteria

- **AC-01 — provenance is enforced.** A session that authored reviewed
  production bytes can emit only `SELF_CHECK_ONLY` and cannot convert itself
  into an independent reviewer by loading another skill.
- **AC-02 — explicit cases are accounted for.** Every required/material row is
  marked pass, fail, blocked, or unchecked with a reason before the review ends.
- **AC-03 — findings are batched when independent.** The matrix and process
  fixtures yield multiple independently reproducible findings in one review
  instead of stopping after the first.
- **AC-04 — findings generalize only to the authorized invariant.** Each finding
  names the broken invariant and credible contract-implied sibling surface
  without inventing generic hardening.
- **AC-05 — broad gates are not duplicated after failure.** A decisive targeted
  failure suppresses the aggregate gate in discovery review; the clean fresh
  final review owns it once.
- **AC-06 — unchecked work is visible.** Early stop or blocked evidence is
  listed explicitly and transferred with stable row identities; a fresh review
  uses prior results as navigation rather than proof for corrected bytes.
  `CHANGES_REQUESTED` does not imply all remaining rows passed.
- **AC-07 — tests-only writes are controlled.** The conditional reference is
  loaded only after explicit current-invocation authorization and a fixed
  `CHANGES_REQUESTED` verdict; only authorized test files change, the
  reproducer fails for the intended reason, production stays unchanged, and
  fresh review remains mandatory.
- **AC-08 — production repair remains prohibited.** No default or implicit
  reviewer production-fix path is added.
- **AC-09 — templates and guided output agree.** Coverage and continuation,
  broad-gate reason, provenance, optional post-verdict writes, and next route
  have consistent semantics.
- **AC-10 — retrospective evals can reject old behavior.** The evals reject
  first-finding termination, hidden unchecked rows, aggregate-after-failure,
  copied stale passes, lost continuation state, same-session verdicts,
  unauthorized writes, or tests that fail for a broken harness.
- **AC-11 — distribution boundary is preserved.** This task changes only the
  canonical skill and leaves the active mirror untouched; the accepted
  canonical paths and post-acceptance distribution route are explicit in the
  handoff.

## Verification

Run one command at a time, starting with the narrowest deterministic check. The
repository does not document a canonical live skill-eval runner; resolve it in
self-preflight and obtain approval before paid/live execution. Process fixtures
must use bounded cleanup and must not leave descendants behind.

| Evidence | Scenario and oracle | Command |
|---|---|---|
| JSON structure | Updated eval definitions parse | `python3 -m json.tool skills/task-implementation-flow/task-acceptance-review/evals/evals.json` |
| Fixture syntax | The setup script parses as Python without filesystem writes | `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py').read_text())"` |
| Matrix fixture | Staged workflow exposes each independent tamper/replay/publication defect through real local entry points | From the canonical skill directory: `python3 evals/files/setup_fixture.py workflow-matrix-defects`, then each documented narrow probe |
| Process fixture | All three cleanup sibling states are deterministic, bounded, and leave no live process/pipe artifacts after fixture cleanup | From the canonical skill directory: `python3 evals/files/setup_fixture.py process-cleanup-defects`, then its focused cleanup tests |
| Reproducer fixture | Authorized test-only review changes only the named test file and the new test fails for the demonstrated defect | Run the reused/new fixture's focused test and inspect `git status --short` plus `git diff -- <authorized-test-path>` |
| Owning skill eval set | Every pre-existing and new eval is run; the revised skill satisfies AC-01–AC-10, while the baseline/current skill is expected to stop early, run a broad gate too soon, remain read-only, or lack provenance handling. Any skipped eval IDs and affected unverified ACs are reported explicitly | Full owning eval-runner command discovered in self-preflight; approval required for paid/live execution |
| Mirror preservation | No task-created change appears under the active mirror relative to the self-preflight baseline | `git status --short -- .agents/skills/task-acceptance-review` |

Syntax checks are not behavioral proof. Do not claim success unless fixture
defects and failure oracles are actually exercised. A reviewer-written test
that merely fails is insufficient; the failure must be the intended contract
violation. The cross-configuration economic benchmark is a separate global
decision.

## Stops and handoff

- Do not infer write permission from test ownership, task scope, or review
  timing.
- Do not enter the conditional tests-only procedure without both explicit
  current-invocation authorization and an exact writable test path or area.
- Do not add production repair or reviewer self-acceptance.
- Do not run or design unbounded process probes.
- Do not edit the shared README, official plans/tasks, or production
  task-orchestrator code.
- Stop on user-work overlap. Do not edit the active mirror; unresolved
  distribution does not block canonical implementation or acceptance.
- After implementation, the authoring session returns `READY_FOR_REVIEW`; a
  fresh acceptance reviewer evaluates these skill bytes.

Next action: guided canonical implementation, fresh acceptance review, then
post-acceptance distribution of accepted bytes.
