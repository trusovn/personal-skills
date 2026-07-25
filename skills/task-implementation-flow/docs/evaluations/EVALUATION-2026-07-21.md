# Task implementation flow effectiveness evaluation — 2026-07-21

## Executive conclusion

The four-skill set is producing valuable quality pressure, but the observed
guided flow is not token-efficient enough in its current form.

The strongest result is the independent acceptance-review role. Across S3-07
and S3-08 it found at least eleven material behavioral defects that passing
focused and aggregate suites had missed. Several involved real process,
tamper, or crash/recovery boundaries. Removing independent review would save
tokens by accepting weaker results, not by making the flow more efficient.

The main failure is that the review/fix loop discovers one slice of an already
named risk family at a time. S3-07 needed three correction rounds, all in the
same process-group-cleanup area. S3-08 needed five correction rounds before a
fresh independent `ACCEPT`; most findings belonged to two risk families that
the task brief already specified: persisted-evidence tampering and
publication-boundary recovery.

The second major failure is role leakage. Several implementer sessions loaded
or emulated `task-acceptance-review` and issued `ACCEPT` on their own work.
This happened even though `bounded-task-implementer` already says not to
approve its own work. The phrase `review: immediate` was repeatedly interpreted
as “perform the review now,” rather than “hand off immediately to a fresh
reviewer.” S3-06 and S3-07 therefore have no observed independent final verdict
on their final bytes. S3-08 does, but only after six review sessions.

The recommended direction is to keep three default roles and make the fourth
conditional:

```text
brief design for complex work
        ↓
implementer self-preflight + explicit risk/evidence matrix
        ↓
fresh completeness-first acceptance review
        ↓
one batched correction, then one fresh final review
```

Standalone preflight should be an exception for meaningful readiness
uncertainty, not a routine stage. A reviewer should normally be allowed to add
an executable failing regression after issuing `CHANGES_REQUESTED`, under a
tests-only protocol. A reviewer should not fix production code or accept its
own corrected bytes by default.

For the original “lower reasoning, good-enough quality” goal, the best lever is
not a longer prompt asking the model to think harder. It is deterministic
scaffolding: enumerate the finite risk dimensions in the task brief, require
the implementer and reviewer to account for them, batch probes before broad
suites, and preserve failing reviewer tests for correction. A high-reasoning
reviewer might still reduce total cost, but these sessions do not provide a
controlled comparison and do not justify making that the default yet.

## Evaluation questions

This evaluation asks:

1. Did each skill perform its intended role?
2. Did the flow produce trustworthy quality evidence?
3. Where were tokens and tool calls spent?
4. Why did review discover defects over multiple passes instead of one pass?
5. Did standalone preflight materially improve implementation?
6. Should acceptance review create tests or apply simple fixes?
7. What should change before the remaining Stage 3 tasks are defined and run?

## Evidence and method

### Reviewed skill sources

- `README.md`
- `task-brief-designer/SKILL.md` and its eval set
- `task-preflight/SKILL.md` and its eval set
- `bounded-task-implementer/SKILL.md` and its eval set
- `task-acceptance-review/SKILL.md` and its eval set

The copies under `.agents/skills/` were byte-identical to the corresponding
sources under `skills/task-implementation-flow/` at evaluation time.

### Reviewed task authority

- `S3-05-record-and-identity-contracts.md`
- `S3-06-verification-command-plan.md`
- `S3-07-verification-executor.md`
- `S3-08-inspect-and-decide.md`
- relevant result files, code, and tests when needed to interpret a finding

### Reviewed session exports

- `/Users/mtrusov/work/tmp/task06/*.jsonl`
- `/Users/mtrusov/work/tmp/task07/*.jsonl`
- `/Users/mtrusov/work/tmp/task08/*`
- `/Users/mtrusov/work/tmp/task05/guided-preflight.jsonl` as limited supporting
  evidence

S3-05's only supplied session is a preflight from July 18, not July 21, and no
matching implementation session was supplied. It is excluded from outcome and
loop comparisons.

`task07/review2.jsonl` and `task07/review2-wTest.jsonl` have the same session
ID. The latter extends the former with the user's test-creation follow-up. Only
the extended export is counted. This avoids double-counting one session as two.

### Measurement method

`/Users/mtrusov/work/tmp/get_measurements` was run on every supplied session.
Its measurements are:

- custom tool-call count;
- final-turn input-context size;
- primary-quota percentage at the beginning and end of the session.

The session token counters were also read to separate cached input, uncached
input, and output. These numbers are useful for relative comparison, not an
invoice:

- cumulative input counts repeat context on every model call;
- cached input is cheaper but not free;
- quota percentages are coarse and one quota reset occurred during S3-08;
- final context is a size snapshot, not total consumption;
- no price table or model-rate conversion was applied.

The `uncached input + output` column below is therefore labeled a cost proxy,
not billable tokens.

## Quantitative results

### End-to-end session cost

| Task | Unique sessions | Tool calls | Sum of final-context input | Summed quota delta | Cumulative tokens, cached included | Uncached-input + output proxy |
|---|---:|---:|---:|---:|---:|---:|
| S3-06 | 2 | 45 | 133,375 | 2 points | 2,457,536 | 238,016 |
| S3-07 | 8 | 190 | 575,228 | 6 points | 11,851,647 | 764,543 |
| S3-08 | 13 | 354 | 1,046,817 | 20 points | 28,165,404 | 1,447,452 |

S3-06 includes preflight plus implementation. Its “acceptance review” occurred
inside the implementation session and was not independent.

S3-07 includes one preflight, four implementation/correction sessions, and
three independent review sessions. Its last `ACCEPT` was issued by the final
implementer, so the final corrected bytes did not receive a fresh independent
review in the supplied evidence.

S3-08 includes one preflight, six implementation/correction sessions, and six
review sessions. The sixth review finally returned an independent `ACCEPT`.

### Cost by role

| Task and role | Sessions | Tool calls | Cumulative tokens | Uncached-input + output proxy | Share of task proxy |
|---|---:|---:|---:|---:|---:|
| S3-07 preflight | 1 | 12 | 623,468 | 86,124 | 11.3% |
| S3-07 implementation/fix | 4 | 102 | 6,637,420 | 366,700 | 48.0% |
| S3-07 review | 3 | 76 | 4,590,759 | 311,719 | 40.8% |
| S3-08 preflight | 1 | 17 | 841,357 | 94,349 | 6.5% |
| S3-08 implementation/fix | 6 | 178 | 15,300,396 | 610,860 | 42.2% |
| S3-08 review | 6 | 159 | 12,023,651 | 742,243 | 51.3% |

On S3-08, review sessions consumed more of the uncached-input-plus-output proxy
than all implementation and correction sessions combined. This does not mean
review is wasteful. It means repeated reviewer bootstrapping, repository
rereading, broad-suite execution, and one-finding-at-a-time probing became the
dominant cost.

Standalone preflight is not the dominant problem. It accounts for 6.5% of the
S3-08 proxy and 11.3% of S3-07's proxy. It is still a candidate for removal
from the default path because its observed incremental value was small, but
fixing preflight alone will not solve the token problem.

### Reasoning setting mismatch

S3-06, S3-07, and S3-08 all declared:

```yaml
agent_tier: strong
reasoning: high
review: immediate
```

The sampled implementation and review sessions used `gpt-5.6-sol` with
`reasoning_effort: medium`. Neither preflight nor the skills treated this as a
warning or a blocker.

This is not necessarily wrong—the stated product idea is to obtain good-enough
quality without always using high reasoning—but it makes the metadata
ambiguous. It currently describes neither an enforced launch configuration nor
the economical strategy actually used.

## What happened in S3-07

| Stage | Result | Risk family |
|---|---|---|
| Initial implementation | 31 runner tests, 36 state tests, 136 aggregate tests passed | Implementer correctly stopped short of self-approval |
| Review 1 | Signal-resistant grandchild survived after group leader exited | AC-03 process-group cleanup |
| Correction 1 | Added resistant-grandchild regression and cleanup escalation | Same family |
| Review 2 | Grandchild holding inherited pipes survived when leader had exited | Same family |
| Reviewer follow-up | Added an intentionally failing inherited-pipe regression | Same family |
| Correction 2 | Cleaned process group before collector rejoin | Same family |
| Review 3 | Transient `PermissionError` race escaped cleanup; pipes could remain unclosed | Same family |
| Reviewer follow-up | Added a deterministic failing signal-race regression | Same family |
| Correction 3 | Added bounded existence polling and reader-owned pipe cleanup | Same family |
| Final status | Implementer issued same-agent guided `ACCEPT` | No fresh independent verdict on corrected bytes |

The S3-07 brief already required the runner to terminate and reap the complete
owned process group on timeout, interruption, or collection failure and warned
not to infer cleanup from wrapper exit. The review behavior was effective but
incremental. Once Review 1 exposed the lifecycle invariant, a compact state
matrix could have covered the meaningful siblings in one pass:

| Dimension | Cases worth batching |
|---|---|
| Group leader | still running; already exited |
| Descendant | normal termination; ignores `SIGTERM`; holds inherited pipes |
| Failure trigger | timeout; interruption; collection failure |
| Signal race | success; already gone; transient permission/visibility race |
| Oracle | group absent; collectors joined; pipes closed; one terminal record |

The correction workflow also patched the demonstrated case too narrowly. After
the first cleanup defect, it did not sweep the neighboring states of the same
invariant. This is a joint implementer/reviewer problem, not only a reviewer
problem.

## What happened in S3-08

| Review | Material behavioral findings | Existing contract family |
|---|---|---|
| 1 | Coherent result `task_id` tamper reached verification; replay after verifier drift failed | AC-02 tamper; AC-08/09 replay |
| 2 | Attempt prompt tamper; crash after execution publication plus verifier drift; non-finite timeout on replay | AC-02 tamper; AC-08/09 crash boundaries; input validation |
| 3 | Coherently changed result/closure bytes lacked an independent anchor | AC-02 tamper/integrity |
| 4 | Contradictory decision-only artifact reached execution before collision detection | AC-08/09 publication order |
| 5 | Attempt-record model tamper reached verification | AC-02 tamper |
| 6 | No findings; final independent `ACCEPT` | Final corrected bytes |

The S3-08 task brief was unusually explicit. Before implementation it already
required:

- validation of policy, manifest, baseline, selected task, attempt/turn,
  prompt, adapter state, structured result, closure artifacts, and digests;
- tampering each persisted evidence family to stop before execution;
- replay after execution-only, verification-only, and decision-without-ledger
  publication boundaries;
- rejection of mismatched existing execution, verification, or decision bytes
  without supplementing them;
- real Git repositories and real harmless local verification commands.

The later reviews did not discover missing product requirements. They
discovered unimplemented or untested members of an already required finite
matrix.

The repeated field-specific fixes also show why findings and corrections should
be stated at the invariant level. Fixing only result `task_id` did not bind the
result bytes. Fixing one prompt copy did not bind the entire attempt record.
The robust direction was exact immutable-byte binding to an independently
anchored digest, which emerged only in Review 3 and was completed for the
attempt record after Review 5.

## Findings

### 1. Implementer and reviewer independence is not enforced

Confidence: high.

Observed examples:

- S3-06 implementation explicitly switched to `task-acceptance-review` and
  returned `ACCEPT`.
- S3-07 correction 3 did the same.
- S3-08 initial implementation, correction 1, and correction 5 performed
  same-agent acceptance passes and returned `ACCEPT`.
- The original S3-07 implementation behaved correctly: it said implementation
  was complete but not self-approved.
- The user had to explicitly tell one S3-07 and one S3-08 correction session not
  to run acceptance review.

The existing sentence “Do not approve your own work” is insufficient because
the agent treats loading a second skill as a role reset. `review: immediate`
amplifies the problem.

Required semantic change:

- `review: immediate` means “return `READY_FOR_REVIEW` and name a fresh review
  as the next action.”
- Loading or following another skill does not create independence.
- If the current session authored any production bytes under review, it may run
  a self-check and fix its own findings, but it cannot issue `ACCEPT`.
- When a fresh reviewer is unavailable, stop at `READY_FOR_REVIEW`; do not
  degrade silently to same-agent acceptance.

### 2. Review is adversarial, but not completeness-first

Confidence: high.

The reviewer found serious defects, so its adversarial stance works. The
problem is sequencing and coverage accounting:

- related probes were split across sessions;
- some review sessions ran broad suites before later discovering a decisive
  adversarial failure;
- a first finding often ended the risk-family investigation;
- findings named the demonstrated field or interleaving more strongly than the
  broken invariant and its sibling surface.

“Find all defects” is not a realistic contract. “Cover every explicit task
case and every material dimension of the selected high-risk invariants before
returning” is realistic and bounded.

The reviewer should build a small in-memory coverage ledger before executing
probes:

```text
AC / invariant → explicit cases → existing evidence → independent probe → result
```

It should continue after a finding when remaining probes are independent and
within budget. If it stops early, the report must say which risk areas remain
unchecked and why. A `CHANGES_REQUESTED` verdict should not imply that no more
findings are likely.

### 3. Implementer corrections are symptom-local rather than invariant-local

Confidence: high.

The implementer appropriately preserved reviewer tests and made surgical
changes. It did not consistently generalize from the failing example:

- resistant descendants did not prompt an already-exited-leader/open-pipe case;
- one result identity mismatch did not prompt complete result-byte binding;
- one attempt field mismatch did not prompt complete attempt-record binding;
- one replay boundary did not prompt all invalid partial-publication states.

A correction should begin by naming the broken invariant and enumerating a few
credible sibling cases. The implementation remains minimal, but the evidence
must reject the family of faulty behavior that the task contract names.

### 4. Reviewer-created failing tests are a successful handoff mechanism

Confidence: high.

After explicit user follow-ups, review sessions added:

- two S3-07 cleanup regressions;
- seven S3-08 regressions across the first four review rounds.

The tests failed for the intended reasons, stayed within owning test files, and
were then used directly by correction agents. This reduced ambiguity and
avoided having each new implementer reconstruct a complex process or crash
probe from prose.

In the one session where both snapshots are available, extending S3-07 Review
2 to add the reproducer increased the uncached-input-plus-output proxy by about
43,000 tokens. That is material, but it reused the reviewer's already-loaded
context and produced an executable handoff. A fresh correction agent would
otherwise have spent part of a new session rediscovering the trigger.

The current review skill prohibits this write, so the useful behavior occurs
only after a second user prompt. It should become an explicit post-verdict
mode, not an accidental boundary violation.

### 5. Full-suite ownership is duplicated

Confidence: high.

Implementers and reviewers repeatedly ran controller, state, runner, and
aggregate suites during the same correction cycle. Passing these suites did
not discover the next defect; targeted adversarial probes did.

Recommended gate ownership for guided immediate-review tasks:

- initial implementer: fail-first, targeted, owning suite, and one broader gate
  if the task explicitly requires it;
- reviewer discovery phase: static/targeted independent adversarial probes
  first; do not run a broad gate after any decisive failure;
- correction implementer: reviewer regressions plus nearest owning suite;
  skip the aggregate unless blast radius or task authority requires it;
- final fresh reviewer: all reviewer regressions, justified owning checks, and
  the aggregate gate once after adversarial evidence is clean.

This preserves regression confidence without paying for the same broad signal
before each newly discovered defect.

### 6. Standalone preflight had little observable incremental value

Confidence: medium because there is no no-preflight control.

The supplied preflights correctly checked ownership, dependencies, command
paths, baselines, sandbox availability, and the first oracle. None returned a
blocker. No ownership accident or missing-command failure occurred later.

Transfer was also weak:

- S3-06's implementer was told only that preflight returned `Ready`; it did not
  receive the recommendations.
- S3-07's preflight output was not included in the implementation prompt.
- S3-08's complete output was pasted into the implementer prompt, but it did
  not reduce the number of correction rounds.

This is consistent with the skill's actual purpose. Preflight answers “can work
start safely, and what exact command/oracle is available?” It is not an
acceptance design or adversarial review. Expecting it to reduce semantic defect
iterations assigns it the wrong metric.

Use standalone preflight when at least one of these is true:

- dirty or multi-writer ownership is meaningfully ambiguous;
- an environment, permission, dependency, helper, or real-boundary capability
  might be absent;
- exact commands are difficult or expensive to resolve;
- a separate agent/process needs a durable freshness handoff;
- high-assurance or unattended execution requires it.

Otherwise let the implementer perform its existing compact self-preflight.

If a separate guided preflight is run, its output must be consumed. Return a
short implementer handoff containing only newly resolved facts, not a repeated
task summary. The output should also state whether standalone preflight added
enough value to recommend using it for the next similar task.

### 7. The task briefs were strong, but prose did not become a finite matrix

Confidence: high for S3-07/S3-08; not generalized beyond this sample.

The task-definition skill should be kept for the remaining complex Stage 3
refactor. S3-07 and especially S3-08 demonstrate that it can produce clear
outcomes, scope, negative evidence, lifecycle behavior, and real-boundary
requirements.

For lower-reasoning executors, phrases such as “each persisted artifact,”
“every publication boundary,” and “complete process-group cleanup” should be
expanded into compact rows or dimensions. The brief should not become a huge
test specification. It should enumerate only finite, material cases whose
omission would allow a false success.

Recommended brief pattern for risky tasks:

| Invariant | Material dimensions/cases | Decisive oracle | Gate owner |
|---|---|---|---|
| Evidence is immutable | exact artifact families or bytes that must be bound; coherent mutation | reject before execution and mutation | implementer + reviewer probe |
| Publication is recoverable | each legal prefix; each contradictory orphan | reuse legal prefix; reject orphan before side effects | reviewer |
| Process group is gone | leader/descendant/pipe/signal cases | no group, joined readers, closed pipes | implementer + reviewer |

This makes quality less dependent on open-ended reasoning effort.

### 8. Current evals do not exercise the observed failure modes

Confidence: high.

The current evals cover useful behavior: freshness, dirty ownership,
high-assurance artifacts, fail-first tests, public repeated flows, adversarial
state validation, and exact verdicts. They do not test:

- an implementer with `review: immediate` refusing to self-accept;
- a reviewer returning multiple independent defects from one explicit risk
  matrix;
- a reviewer continuing through sibling states after finding the first defect;
- tests-only reproducer creation after `CHANGES_REQUESTED`;
- correction at the invariant level rather than one demonstrated field;
- gate ownership that prevents repeated aggregate runs;
- a routine preflight recommending implementer self-preflight instead;
- metadata mismatch between requested and actual reasoning settings.

Without these evals, a textual edit may sound correct while the observed
behavior remains unchanged.

## Answers to the original observations

### “Implementer attempts to run the full verification skill”

Confirmed, with an important distinction.

The implementer should run implementation verification. It should not run the
acceptance-review role or issue an acceptance verdict. In these sessions it did
both. The fix is a hard provenance rule, not removal of targeted or owning test
verification from implementation.

### “Multiple implement → verify → fix iterations; discover most in one pass”

Confirmed and achievable relative to the explicit contract.

No reviewer can promise every latent bug in one pass. Here, however, many later
findings were siblings under already written requirements. The reviewer should
batch the explicit tamper/publication/process-lifecycle matrix, continue after
independent findings, and postpone broad suites until that discovery sweep is
clean. The correction agent should sweep the same invariant's neighboring
states before handoff.

### “Verification session is well positioned to create tests”

Confirmed. This was one of the most effective observed behaviors.

Recommended default: allow tests-only reproducer creation after the verdict
when the task authorizes it, the defect is deterministic, the test is in an
owned path, and the reviewer proves that it fails for the intended reason.
Production code remains unchanged. The report must preserve the pre-write
verdict and state that the next review must evaluate corrected bytes.

### “Can verification fix trivial issues on the spot?”

Possible, but not recommended as the default.

There are three options:

1. **Read-only review plus tests-only reproducer — recommended default.** It
   preserves clean role separation and creates an executable handoff.
2. **Opt-in bounded repair mode — reasonable experiment.** After
   `CHANGES_REQUESTED`, the reviewer may apply an unambiguous local correction
   when no contract, dependency, public schema, persistence, concurrency,
   recovery, or architecture decision is involved. It must return
   `CHANGES_APPLIED_REVIEW_REQUIRED`, not `ACCEPT`; a fresh reviewer still owns
   acceptance.
3. **Reviewer fixes and accepts — reject.** It recreates the same-agent
   acceptance problem already observed.

A one-line change is not automatically trivial. The eligibility test is
whether the authority leaves exactly one local correction and the change does
not alter a material boundary. This option saves one implementer bootstrap but
still requires a fresh final reviewer. It should be evaluated before becoming
default behavior.

### “Is preflight useful?”

Yes for readiness uncertainty; no as a mandatory quality stage.

In this sample, preflight was accurate but not decisive, disconnected from two
implementer sessions, and unable by design to prevent later semantic defects.
Use implementer self-preflight by default. Run standalone preflight only under
the criteria in Finding 6, and judge it by prevented unsafe starts, resolved
commands/capabilities, and useful handoff deltas—not by eventual reviewer defect
count.

## Recommended economical flow

### 1. Define the task

For complex Stage 3 work, continue using `task-brief-designer`.

- Keep outcome, scope, stops, and public-boundary evidence.
- Turn finite high-risk words (`every`, `each`, `exactly one`, retry, recovery,
  tamper, cleanup) into a compact dimension table.
- Assign gate ownership so implementer and reviewer know who runs the broad
  suite and when.
- Make the intended launch policy truthful. Do not write `reasoning: high` if
  the chosen economical profile deliberately uses medium reasoning.

### 2. Decide whether standalone preflight adds value

Default to the implementer's self-preflight. Use standalone preflight only for
ownership, dependency, environment, permission, helper, command, or durable
freshness uncertainty. If run in a separate session, pass its compact delta
handoff to the implementer.

### 3. Implement against the finite matrix

Before editing, the implementer maps each explicit high-risk row to existing or
new evidence. This may be scratch reasoning; it need not create a durable
artifact.

- Establish the task's required fail-first case.
- Add table-driven/parameterized cases when one invariant has several explicit
  values.
- Run targeted and owning checks progressively.
- Perform a self-check, fix any self-found issues, and report them as
  implementation evidence.
- End with `READY_FOR_REVIEW` when review is immediate. Never load the review
  skill to produce `ACCEPT` for bytes authored in the session.

### 4. Review for completeness before regression

The fresh reviewer first reconstructs the explicit coverage matrix and traces
the high-risk boundaries. It then batches the narrow adversarial probes.

- Continue after a finding when remaining probes are independent.
- Generalize each finding to the broken invariant and likely sibling surface.
- Do not run the aggregate gate after a decisive adversarial failure.
- Return all currently demonstrated independent findings plus unchecked areas.
- When authorized, add failing tests only after preserving the verdict.

### 5. Correct the batch

The correction implementer consumes the complete finding batch and failing
tests. For each finding it states the invariant, applies the smallest
invariant-level correction, and checks credible sibling states. It normally
runs the regressions and nearest owning suite, not another full acceptance
pass.

### 6. Run one fresh final review

The fresh reviewer reruns all finding regressions, completes any previously
blocked risk rows, and runs the justified broader/aggregate gate once. Only
this reviewer may return `ACCEPT`.

This flow targets one initial review, one correction batch, and one final
review. More cycles remain legitimate when the correction introduces a new
defect, a prior defect blocked downstream evidence, or the contract itself
changes.

## Implementation-ready skill changes

### `README.md`

1. Define independence as reviewer non-authorship of the production bytes, not
   merely use of a different skill.
2. Change the guided diagram to show an explicit fresh-session review handoff.
3. Add the standalone-preflight decision criteria from Finding 6.
4. Add gate ownership for initial implementation, failed review, correction,
   and final review.
5. Add the economical flow and tests-only reproducer option.
6. Clarify that a self-check can find and fix issues but cannot issue a verdict.

### `bounded-task-implementer/SKILL.md`

1. Replace “Review is required” wording with “route to a fresh reviewer.”
2. Add an explicit rule: loading `task-acceptance-review` does not create
   independence; never issue `ACCEPT` for production bytes authored in the
   current session.
3. Return `READY_FOR_REVIEW` or the existing complete-submission status with
   `next_action: fresh task-acceptance-review`.
4. Before implementation, convert explicit finite risk requirements into a
   concise evidence matrix.
5. On correction, identify the invariant behind each finding and inspect
   credible sibling cases before handing off.
6. For correction cycles, default to reviewer regressions plus the owning suite;
   run the broad gate only when task authority/blast radius requires it or no
   final reviewer will own it.

### `task-acceptance-review/SKILL.md`

1. Add a provenance precondition. If the current session authored production
   bytes, provide only a labeled self-check; do not issue an acceptance verdict.
2. Add a completeness-first phase that maps explicit contract cases and
   material risk dimensions before broad suites.
3. Continue after the first finding when other probes are independent and
   affordable; otherwise report unchecked areas and the stop reason.
4. Put adversarial discovery before broad regression gates. A decisive failure
   ends broad-gate execution for that review.
5. Change finding guidance from symptom-only direction to broken invariant,
   demonstrated trigger, credible sibling surface, and smallest invariant-level
   correction.
6. Add an authorized post-verdict `tests_only_reproducer` mode:
   - verdict is fixed before writes;
   - only owning test files may change;
   - production code and result/plan files remain untouched;
   - the focused test must fail for the intended reason;
   - repository diff/status and side effects are reported;
   - fresh review remains mandatory after correction.
7. Keep production repair out of the default skill. If added later, define a
   separate opt-in non-accepting repair result.

### `task-preflight/SKILL.md`

1. Add an upfront standalone-value check. If all uncertainty is routine and an
   implementer self-preflight is sufficient, say so and avoid a long preflight.
2. For guided mode, return only resolved deltas: ownership exception, exact
   command/oracle, capability result, and stops.
3. Include a copyable implementer handoff when another session will consume the
   result.
4. Avoid broad baselines unless they distinguish environment readiness or are a
   named entry criterion whose freshness matters before editing.
5. Report `standalone_preflight_value: material | marginal` (human-readable,
   not necessarily a schema field) and explain the basis.

### `task-brief-designer/SKILL.md`

1. For finite high-risk requirements, produce a compact invariant/dimension/
   oracle/owner table.
2. Expand universal quantifiers only when the cases are finite and material;
   do not create an exhaustive generic matrix.
3. Separate implementation evidence from independent-review probes.
4. Record who owns the broad gate after correction.
5. Resolve the metadata design described below before generating more Stage 3
   tasks with `reasoning: high` that will actually run at medium.

### Source mirrors

Apply edits to `skills/task-implementation-flow/` first, then update the
byte-identical copies under `.agents/skills/` using the repository's normal
sync/install process. Do not edit one side and leave the active catalog stale.

## Required regression evals for the skill changes

Do not judge the rewrite only by rereading `SKILL.md`. Add retrospective evals
derived from the observed failures.

### Implementer eval: immediate review is a handoff

Give the implementer a completed task with `review: immediate`. Assert that it
runs implementation checks, may perform a labeled self-check, returns
`READY_FOR_REVIEW`, and does not load the review skill or emit `ACCEPT`.

### Implementer eval: invariant-level correction

Provide a failing regression for one coherently mutated result field and a task
contract requiring all exact result bytes to be bound. Assert that the
correction binds the record invariant rather than adding a one-field equality
check, and that it checks at least one semantically identical byte rewrite or
sibling mutation.

### Reviewer eval: multiple findings in one pass

Create a fixture with several independent defects under two explicit matrices,
for example:

- prompt and model tampering both reach execution;
- execution-only replay fails after verifier drift;
- decision-only collision reaches execution.

Assert one review reports all independently reproducible findings, names any
unverified rows, and does not run the aggregate suite after the first decisive
failure.

### Reviewer eval: same risk family

Create process cleanup with a resistant descendant, an already-exited leader
holding pipes, and a transient signal race. Assert one review batches the
meaningful lifecycle cases instead of returning after the first leak.

### Reviewer eval: tests-only reproducer

Authorize post-verdict test writes. Assert the reviewer first fixes the verdict
as `CHANGES_REQUESTED`, edits only the owning test file, proves the new test fails
for the intended behavior, leaves production unchanged, and requires fresh
review.

### Preflight eval: skip standalone ceremony

Provide a clean routine guided task with obvious paths and commands. Assert the
preflight returns a compact marginal-value result recommending implementer
self-preflight rather than running broad baselines or recreating the task
brief.

### Brief-designer eval: explicit finite dimensions

Provide an authority requiring tamper denial across named artifact families and
recovery across ordered publications. Assert the brief emits the finite matrix,
real-boundary oracle, and gate owner without expanding unrelated generic cases.

### Comparative evaluation

After the skill edits, run at least two configurations on fresh fixtures or
repository snapshots:

1. current skills at medium reasoning;
2. revised skills at medium reasoning.

Measure:

- material defects present after initial implementation;
- defects reported in the first review;
- independent review rounds to `ACCEPT`;
- fresh-session count and tool calls;
- uncached input, cached input, output, and quota delta;
- number of broad-suite executions;
- false findings and unnecessary test changes.

Only after that comparison should the team test a third configuration with a
higher-reasoning reviewer. The hypothesis is that a more expensive single
review may be cheaper than five medium-reasoning reviews, but the current data
cannot prove it.

## Decisions that affect the future shape of the flow

### Decision 1: reasoning metadata

Current state is internally inconsistent: briefs request high reasoning while
the economical usage uses medium.

Recommended choice: split execution and review launch guidance, for example:

```yaml
execution:
  agent_tier: strong
  reasoning: medium
review:
  timing: immediate
  reasoning: medium
budget: 30 tool calls / 90 minutes / 100k context
```

Start with medium for both under the revised deterministic matrix. Evaluate
high reasoning only for the reviewer as a controlled third configuration. If
the metadata cannot be consumed or checked by the launcher, simplify or remove
it rather than keeping decorative requirements.

Alternative: keep the current four-key block, but make preflight warn when the
actual session does not match it. This is simpler but does not express the
lower-reasoning implementer/stronger-reviewer strategy.

### Decision 2: reviewer writes

Recommended choice: tests-only after `CHANGES_REQUESTED`, authorized by task
metadata or user instruction. This directly captures a behavior that worked in
the observed sessions.

Keep production repair experimental and opt-in. Never let the repairing
reviewer accept the corrected bytes.

### Decision 3: preflight's place

Recommended choice: remove standalone preflight from the ordinary default
chain. Keep it as a separately invocable readiness specialist and retain it in
high-assurance orchestration.

This does not mean deleting `task-preflight`. It means evaluating it by whether
it resolves a real readiness uncertainty, not by how many tasks receive a
`ready` label.

### Decision 4: one-pass review ambition

Recommended choice: promise completeness against explicit finite contract rows
and selected material risk families, not “find every bug.” Require unchecked
areas to be visible. This is ambitious enough to reduce the observed loops
without driving unbounded repository archaeology or generic fuzzing.

## Risks of the recommendations

- A larger first review may spend more tokens before returning the first useful
  finding. The mitigation is to batch only explicit and material dimensions,
  and to stop broad gates after a decisive failure.
- Reviewer-written tests modify the worktree and can complicate staged versus
  unstaged ownership. The tests-only protocol must preserve the pre-write
  verdict, record exact paths/status, and avoid staging.
- Invariant-level correction can become overengineering. The authority and
  finite risk matrix bound the sibling sweep; do not invent generic framework
  abstractions or unrelated hardening.
- Skipping standalone preflight may expose environment problems during the
  implementer's first calls. That is acceptable for routine guided work because
  the implementer already performs the same compact check. Use standalone
  preflight when the cost or risk of discovering the problem late is material.
- A medium-reasoning-only strategy may still require more iterations on highly
  stateful or concurrent work. Measure it against a high-reviewer variant
  rather than assuming prompt structure eliminates model capability limits.

## Final assessment

| Skill | Effectiveness | Efficiency | Recommended future role |
|---|---|---|---|
| `task-brief-designer` | Strong on S3-07/S3-08 contract quality | Good, session cost not evaluated here | Keep for complex Stage 3 tasks; add finite risk matrices and truthful launch metadata |
| `task-preflight` | Accurate readiness checks; no blocker found | Small share of total but often redundant/disconnected | Conditional specialist; implementer self-preflight by default |
| `bounded-task-implementer` | Produced working increments and used reviewer regressions well | Too much self-review, broad-gate duplication, symptom-local fixes | Keep; enforce handoff, risk matrix, and invariant-level correction |
| `task-acceptance-review` | Highest quality value; found serious real-boundary defects | Dominant S3-08 cost because discovery was fragmented | Keep and strengthen; completeness-first, batch probes, tests-only reproducer mode |

The skill set should be reshaped, not discarded. Its quality mechanism works:
independent review found defects that ordinary implementation verification did
not. The economical version needs fewer role transitions, stronger
independence, finite evidence matrices, reviewer-owned reproducer tests, and a
single broad final gate after adversarial discovery is clean.
