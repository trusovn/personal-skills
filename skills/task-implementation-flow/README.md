# Task implementation flow

These eight task skills provide a reusable implementation discipline without
making every task carry an orchestration-grade artifact chain. The default is a
lightweight guided flow. Repositories that enable maintainability guardrails can
insert a focused architecture gate before functional acceptance. A
high-assurance profile remains available for work that benefits from durable
handoffs, exact freshness evidence, and machine-readable results.
## Goals

- Make bounded implementation more consistent without repeatedly prompting an
  agent to define acceptance criteria, add tests, verify progressively, preserve
  user work, and report evidence.
- Spend tokens on the task and its highest-risk behavior rather than repeated
  stage paperwork.
- Let cheap/small agents carry a short implementation contract while deterministic
  gates and focused reviewers carry the deeper architecture/quality policy.
- Separate maintainability judgment from functional/specification acceptance so
  each reviewer can spend its context on one question.
- Scale assurance with risk instead of treating every task as mission-critical.
- Preserve an orchestrator-compatible path for unattended or audited work.
## Skills
| Skill | Use it for | Skip it when |
|---|---|---|
| `task-brief-designer` | Create or tighten a bounded task contract. It defaults to a delta check when a useful brief already exists. | The user request already gives an unambiguous outcome, scope, and acceptance criteria for a small task. |
| `task-preflight` | Check readiness, ownership, commands, and decisive evidence when dirty ownership, dependencies, environment, permissions, helpers, fixtures, real-boundary capability, or a durable handoff creates material uncertainty. | Every executable package requires derived verification and compact canonical readiness; an unpackaged direct request may use implementer self-preflight. |
| `task-verification-designer` | Turn an executable brief into a separate task-local verification design with AC coverage, discriminating scenarios, and decisive oracles before implementation. It is required for a supplied executable task package. | An unpackaged small direct edit has obvious decisive tests/oracles and does not need a separate design. |
| `bounded-task-implementer` | Implement one bounded task with risk-based tests, progressive verification, and a useful handoff; on packaged entry the implementer verifies current applicable readiness and its submission maps every verification scenario ID to current evidence. | The request is planning, review-only, or too ambiguous to implement safely. |
| `task-maintainability-review` | Independently assess the changed design for concrete maintainability regression after the repo's deterministic architecture gate. | The repo does not require maintainability review and the user/task does not request it. |
| `task-contract-registry-updater` | Synchronize implemented-contract discovery after maintainability review. | The repository does not use implemented-contract discovery, or the task did not change a durable cross-task contract. |
| `task-review-discovery` | Independently publish current evidence and confirmed findings as a complete or explicitly partial report for a separate acceptance decision call, without deciding acceptance. | The task requires no independent functional review at all; discovery is never optional whenever the separate acceptance decision runs. |
| `task-acceptance-review` | Independently decide scoped functional/specification correctness by admitting the current discovery evidence and deciding every finding; returns `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`. | The task does not need independent functional review under its metadata or risk. |

`architecture-guardrails` is a foundation/setup skill, not a per-task reviewer. It
materializes the deterministic gate and short repo-local contract that this flow
can consume.

## Workflow identity

When a task run records which implementation workflow was used, obtain the
identity from the canonical shared `workflow_version.py` installed alongside the
active skill installation. In this source repository the shared tooling lives under
`scripts/`; in the preferred project-local installation it lives under
`.agents/scripts/` beside `.agents/skills/`, as defined by the root README.

`bounded-task-implementer` currently uses the shared `run_evidence.py` integration
best-effort in ordinary guided execution. That collector consumes
`workflow_version.py` and the generic runtime-context helper/schema; task skills do
not duplicate fingerprint calculation or maintain manual version numbers. Missing
optional evidence tooling does not make a standalone bounded task fail unless an
explicit repository/user/machine contract makes instrumentation mandatory.

## Task sizing, decomposition, and durable artifact discovery

`task-brief-designer` treats its execution estimate as a boundary-quality
gate. The authoritative, packaged policy files are intentionally external to
the skill body:

- sizing policy: [`task-brief-designer/references/task-sizing.yaml`](task-brief-designer/references/task-sizing.yaml)
- durable artifact layout: [`task-brief-designer/references/task-artifact-layout.md`](task-brief-designer/references/task-artifact-layout.md)

This keeps calibration editable without rewriting the skill. A matched
decomposition trigger forces a boundary decision rather than an automatic
split: before committing to a split, assess clear ownership, stable handoffs,
independent implementation and verification, shared edit/test surfaces,
likely contract renegotiation, and net delivery benefit. Prefer a split when
settled boundaries produce independently verifiable outcomes with cheaper
coordination than keeping the work whole; a triggered task may remain one
executable leaf when concrete coupling or coordination/rework costs favor
keeping it whole, recorded with the triggered rules, the candidate boundary
considered, the concrete reason, and residual execution risk. When splitting,
the original becomes a non-executable composite
parent plus full executable child briefs. Children are re-estimated
recursively; only leaf briefs are implementation launch targets. If an
end-to-end criterion requires work after siblings compose, model that as a
final executable integration child rather than a special parent-review stage.

The default project-level discovery layout keeps planning truth, task execution
contracts, and review evidence separate:

```text
docs/project-plan.md
docs/task-map.json
docs/project-plan-review.md

docs/tasks/
  index.json
  <TASK-ID>/
    brief.md
    verification.md               # required before packaged implementation
    preflight.md                  # required ready preflight before implementation
    reviews/
      maintainability-01.md       # only when a durable report is written
      discovery-01.md             # only when discovery publishes durably
      acceptance-01.md
```

Repository/user authority may choose a different task-package root or directory
name, but every durable task keeps `brief.md`, required preparation artifacts,
and reviews inside one dedicated package directory. `docs/task-map.json` remains the verified
project-planning graph; `docs/tasks/index.json` is only the structural
execution/decomposition index. Review artifacts never rewrite the brief or
master plan, and numbered durable reviews preserve prior verdict provenance
across correction cycles.

This package rule also applies to high-assurance work. Its durable preflight is
the package's `preflight.md`, and durable semantic reviews use the next unused
numbered file under `reviews/`. Creating one of those files is an expected,
attributed repository-status change: freshness compares the exact pre-write and
post-write states and permits only that artifact delta. External run policy,
schema, disposable probe state, and machine worker-result locations may remain
runtime inputs/outputs; they are not substitutes for the canonical durable task
artifacts above.

### Reading plans and work reports

For the project owner, start with the plan's intended result and task
contributions, then follow the current implementation result or acceptance
report for progress. Their openings explain the practical change, checked scope,
material gaps, and next actor or owner decision. Implementation reports changes
and checks; discovery supplies independent evidence; acceptance decides what may
advance. When maintaining navigation in an existing project guide, link to the
plan and the latest identified report instead of copying their status. If the
current report cannot be established or sources conflict, say so and name who
must resolve it. Keep each report's scope and age visible.

## Guided profile: default

Use guided mode for most ordinary bounded tasks, especially when a person is
launching the skill directly.

```text
existing request or brief
        ↓
fill only meaningful contract gaps
        ↓
required task-verification-designer for an executable task package
        ↓
ready packaged preflight
        ↓
implement + risk-based tests + progressive verification
        ↓
human-readable result
        ↓
required architecture gate / maintainability review, if declared by repo
        ↓
required contract-registry stage, if the repository uses implemented-contract
discovery and the task changed a durable cross-task contract
        ↓
fresh independent task-review-discovery evidence whenever independent functional review is required
        ↓
separate fresh-session functional acceptance decision consuming that discovery report
        ↓
coordinator recording of approved deferrals, then authorized continuation
```

Guided mode carries these defaults so the user does not need to repeat them:
1. State or infer the smallest testable outcome and bounded scope. Ask only
   when a missing decision could materially change the implementation.
2. Define concise acceptance criteria when they are absent. Include positive
   behavior and the most credible negative, unchanged-state, or lifecycle case.
3. Preserve pre-existing user work and stop on ownership overlap.
4. Add or update the lowest-level reliable tests. For a bug, establish
   fail-first evidence when feasible. Cross the real boundary when lower-level
   tests cannot prove wiring, persistence, concurrency, recovery, or another
   material risk.
5. Run the targeted check first, then the nearest owning suite, then only the
   broader gate justified by blast radius and authorization. If repo authority
   declares a required architecture gate, run its canonical command before
   maintainability handoff.
6. Finish with a concise human summary: outcome, changed files, verification,
   residual risks, and next action. When independent maintainability or
   functional review is required, end at `READY_FOR_REVIEW` and name the first
   outstanding applicable stage and the complete ordered remainder: the
   architecture gate only when policy requires it, fresh maintainability review
   when applicable, the contract-registry updater when applicable, then fresh
   discovery evidence and the separate fresh acceptance decision.

The implementation agent should not be burdened with a long architecture
rubric. When the repo has maintainability guardrails, follow the short
repo-local contract (normally cohesion, change locality, explicit/narrow
dependencies, testability, and no speculative abstraction) and let the
canonical gate plus `task-maintainability-review` enforce the deeper policy.

The brief designer is optional in guided mode. Once an executable task package
is supplied, verification design and a durable ready preflight are binding
preparation before implementation. A small clear conversational direct edit may
use compact inline checks only while it is not a supplied task package.

### When separate verification design adds value

A ready executable brief may classify its verification reasoning as `inline` or
`separate — <reason>`, but a supplied executable task package always runs
`task-verification-designer`. That classification only explains the needed
scenario depth; it does not permit skipping the required `verification.md` and
ready preflight route. An unpackaged direct edit may use inline checks when its
decisive scenarios are obvious. The skill writes `verification.md` in the
executable task package and leaves concrete test implementation to
`bounded-task-implementer`.

For a supplied executable task package, this preparation is required even for a
small change. An unpackaged conversational direct edit with an obvious oracle
may stay inline. The verification-designer contract remains task-local and does
not own cross-child or parent-level integration-test design.

Packaged guided readiness uses canonical `preflight.md`, bound to the brief,
scope and verification revision. Record complete per-AC/scenario authority and
proof feasibility plus referenced decision context, relevant known issues and
ordinary assumptions. Feasible future tests may be absent; missing indispensable
capabilities block with their owner. Coverage revisions retain IDs and need
focused current readiness; material fact changes need reconsideration, expected
implementation/report effects alone do not force rediscovery, and requirements
return to task design. Direct requests may stay inline; package presence alone
requires no digest ledger or machine schema. Strict high-assurance checks remain.

### When standalone preflight adds value

Use ready standalone `task-preflight` for an executable task package. An
unpackaged direct edit may use the implementer's compact self-preflight. The
standalone pass resolves readiness facts such as:

- dirty or multi-writer ownership;
- a required environment, permission, dependency, helper, or fixture;
- real-boundary capability or an unresolved command and observable oracle;
- a required repo gate whose command or prerequisites are not actually ready; or
- a durable handoff between sessions.

A directly requested standalone preflight still returns a truthful readiness
result even when its incremental value is marginal. It should stay compact,
avoid broad baseline work without a named readiness reason, and recommend
implementer self-preflight for similar unpackaged direct requests. Explicit
high-assurance and orchestrated flows continue to require standalone
preflight.
## Maintainability-gated profile

Use this profile whenever repo authority declares architecture/maintainability
review required, or when the user explicitly asks for focused maintainability
verification.

Significant changed tests, evaluations, fixture/setup and harness code are
reviewed implementation assets, including tests-only submissions. Changed
ownership, dependencies, scenario authority, isolation, oracle structure or
harness behavior can justify this conditional review. An ordinary assertion
edit alone does not require it. Use canonical `testing-discipline` guidance
from the same installation root; leave functional conformance to discovery
and acceptance.

The order is intentional:

```text
bounded implementation
        ↓
canonical deterministic architecture gate
        ↓
fresh task-maintainability-review
        ├── CHANGES_REQUESTED
        │       ↓
        │   implementation correction
        │       ↓
        │   architecture gate + fresh maintainability review again
        │       ↓
        │   contract-registry stage again, if the repository uses implemented-contract
        │   discovery and the correction changed a durable cross-task contract
        │
        └── ACCEPT
                ↓
        contract-registry stage, if the repository uses implemented-contract
        discovery and the task changed a durable cross-task contract
                ↓
        fresh task-review-discovery evidence whenever independent functional acceptance is required
                ↓
        separate functional/spec acceptance review consuming that discovery report
                ├── CHANGES_REQUESTED
                │       ↓
                │   implementation correction
                │       ↓
                │   architecture gate + fresh maintainability review again
                │   when the correction affected their reviewed scope
                │       ↓
                │   contract-registry stage again, if the repository uses implemented-contract
                │   discovery and the correction changed a durable cross-task contract
                │       ↓
                │   fresh discovery evidence + fresh functional acceptance again
                │
                └── ACCEPT
```

Do not reverse the two semantic reviews merely to save a stage. The first
review asks whether the change introduced or materially worsened concrete
design/maintainability risk. The later acceptance decision admits the
discovery evidence and spends its budget on whether the code actually
satisfies the requested behavior and preserves required behavior.

The deterministic architecture command is evidence, not the semantic verdict:

- a hard gate failure is an implementation failure and normally yields
  `CHANGES_REQUESTED` without requiring a broad subjective review;
- advisory size/complexity/fan-out/duplication signals are leads for the
  maintainability reviewer, not automatic blockers;
- a passing gate does not prove cohesion, change locality, useful test seams, or
  absence of speculative abstraction;
- a maintainability `ACCEPT` does not prove the task specification is satisfied.

When launching `task-acceptance-review` after maintainability acceptance, carry a
short routing note rather than asking the acceptance reviewer to infer the stage:

```text
Maintainability review accepted the current reviewed implementation assets. Focus review budget
on specification conformance, observable behavior, regressions, edge cases, and
test adequacy. Do not redo general architecture review unless architecture directly
causes an observed functional defect.
```

Whenever independent functional review is required, launch `task-review-discovery`
as a fresh separate call whose session did not author the reviewed implementation
assets, and hand its report to the acceptance decision call; the decision call
never runs without that discovery evidence. When functional review itself is
not required, neither stage runs. The acceptance call
then admits that evidence and decides: it does not routinely rerun discovery's
public probes, broad searches, or aggregate suites, and it requests focused
missing proof from the discovery owner rather than merging the roles. A high
reasoning tier is recommended for discovery, and an equally high tier is
recommended for the separate acceptance decision, whose budget goes to
contextual judgment and finding dispositions rather than re-search; launch
tooling enforces neither the separate-call roles nor the reasoning
recommendations.

When the flow already carries a byte/diff digest, attach it to both reviews. In a
lightweight human-driven flow, at minimum confirm the reviewed implementation diff did not change
between maintainability `ACCEPT` and functional-review start.

Every implementation correction, including a tests-only correction, changes the
bytes under review and stales the prior acceptance verdict for the corrected bytes. The next submission re-enters
every conditional stage whose reviewed scope the correction affected, before
re-entering fresh discovery evidence and functional acceptance: the required
deterministic architecture gate and a fresh maintainability reviewer when the
correction affected their reviewed scope, and the contract-registry stage when
it applied and the correction affected its scope. Current applicable evidence
for the corrected bytes keeps an unaffected stage out of the route — when gate
and maintainability evidence is current for the corrected scope, the remaining
route is the registry updater, then discovery, then acceptance.

For a trivial correction that provably cannot affect reviewed implementation
architecture, repo policy may explicitly allow the maintainability stage to be
skipped. A tests-only label alone never waives an affected required review;
apply authorized exceptions only within their stated scope. Do not invent a
gate or registry work for every test change.
## High-assurance profile

Use high-assurance mode when explicitly requested, when an orchestrator or
machine output schema is supplied, or when durable evidence is proportionate
to the risk. Typical signals include:
- security, authorization, privacy, or credential boundaries;
- migrations, irreversible writes, recovery, or destructive state;
- concurrency or multi-process coordination;
- multiple independent writers or agents in one worktree;
- complex staged/unstaged user work that must remain separable;
- audited or unattended execution requiring resumable machine contracts.

High-assurance mode uses the complete chain:
```text
task brief (`ready_for_preflight`)
        ↓
required task-local verification design for a supplied executable task package
        ↓
fresh preflight packet (`ready`)
        ↓
bounded implementation + structured worker result
        ↓
required deterministic architecture gate + independent maintainability report
        ↓
contract-registry stage, if the repository uses implemented-contract discovery
and the task changed a durable cross-task contract
        ↓
independent discovery report + separate functional acceptance decision
        ↓
orchestrator or human advancement
```

If the repo does not require maintainability review, omit that stage rather than
manufacturing policy for the task. If the repository does not use
implemented-contract discovery or the task changed no durable cross-task
contract, omit the contract-registry stage.

High-assurance mode may require exact digests, package-contained durable task
artifacts, external runtime policy/schema/result state, and strict entry/exit
statuses. A guided run that
encounters one of these needs should pause and recommend the smallest
escalation rather than silently rebuilding the entire chain.

For high-assurance work, preflight records required packaged `verification.md`
with its path and digest as a derived input, maps its scenario IDs to packet
commands/oracles,
and the implementer revalidates those bytes before editing. The task brief
remains normative; carrying the artifact through the packet must not promote it
into a second requirements source.
## Task metadata

Durable briefs put this compact block near the top:

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 30 tool calls / 90 minutes / 100k context
```

- `agent_tier`: `mechanical`, `standard`, or `strong`.
- `reasoning`: `low`, `medium`, or `high`.
- `review`: `mechanical`, `milestone`, or `immediate`.
- `budget`: a soft checkpoint unless the user or repository explicitly calls it
  a hard limit.

`agent_tier`, `reasoning`, and `review` are intended launch guidance, not claims
about the eventual runtime configuration. Authors should choose the economical
values the task actually calls for. `review: immediate` means an immediate
handoff after implementation or correction to a fresh independent reviewer; it
never instructs the implementer to accept its own work. When repo policy also
requires maintainability review, that focused review comes before functional
acceptance. Metadata does not replace the task's outcome, scope, acceptance
criteria, or verification commands.
## Review rules worth keeping

Independent functional review should spend effort where implementation evidence
is most likely to be misleading:
- account for every explicit finite task row and selected material risk
  dimension, keeping blocked or unchecked areas visible without promising to
  find every latent defect;
- exercise the real public path when unit evidence can miss wiring;
- for repeated or recovered behavior, perform the first state change and the
  next real occurrence;
- test interacting state rules across selected and non-selected entities;
- check exact cardinality with zero, one, and two owners where “exactly one” is
  an invariant;
- check exact ready sets and latest/current ordering rather than only presence;
- test coherent tampering when evidence files can be rewritten together.

A digest stored beside mutable bytes proves internal consistency, not
immutability. Claims of immutability require an independently protected anchor
or an explicitly narrower threat model.

Maintainability review has a different ledger. Keep it focused on concrete
regression introduced or materially worsened by the current change:

- responsibility/cohesion and truthful names for behavior, state and units;
- unnecessary or hidden coupling, mutations, indirection and dependency direction;
- change locality and invariant/state ownership across subsystems;
- independently testable important logic and usable failure context;
- duplicated business/domain rules or growing dispatch structures;
- speculative layers/interfaces/abstractions with no concrete boundary,
  variation, or test-seam value;
- deterministic gate failures and architecture warnings that correspond to a
  real design problem.

Do not make maintainability review a second functional review or a style
preference contest.

Independence is based on session authorship. Loading another skill, quoting its
instructions, or changing roles in the same session does not reset provenance.
A session that authored reviewed implementation assets may perform a labeled
`SELF_CHECK_ONLY` and fix defects it finds, but it cannot issue an independent
verdict. Only a fresh reviewer may return `ACCEPT`, `CHANGES_REQUESTED`, or
`INCONCLUSIVE` for those bytes.

Every `CHANGES_REQUESTED` correction requires fresh review for the affected
stage, and a previous verdict never applies to corrected bytes. An implementation
correction, including a tests-only correction, stales the prior acceptance verdict and re-enters every conditional
stage whose reviewed scope the correction affected; current applicable evidence
for the corrected bytes keeps an unaffected stage in force.

Correction continuation retains all finding/scenario IDs, prior row statuses,
current producer-attributed evidence, incomplete reasons and separate correction,
evidence/capability and authority owners. Carry preflight/context and verification
revision references, the scoped diff, invariant, attempts/discarded hypotheses,
influenced siblings, exact probes and the gate record. A green corrected target
does not close unfinished siblings or certify changed bytes with an old pass.
Neither non-success verdict permits advancement.

Route by actual effects and current proof: clarification returns to its artifact
owner; evidence recovery to discovery/capability ownership, then a separate
decision. Tests-only exceptions require explicit policy and retain the rest of
the ordered route. Genuine reference-only updater → fresh acceptance requires
unchanged executable/behavioral effects and current behavioral proof; otherwise
repeat affected discovery/gates. A reasoned coverage revision under unchanged
requirements retains IDs and supersedes affected readiness/evidence: verification
designer → focused ready preflight → current revised-scenario proof → new decision.
New proof cannot excuse old readiness or its substitution after recovery.
Changed requirements return to task design; ordinary corrections/clarifications
do not restart design, and expected task/report effects alone do not stale readiness.

Correction discovery reconciles authority, diff and the complete ledger before
aggregate selection. Safely runnable material rows and selected probes need
current targeted evidence; unfinished rows retain concrete non-gate reasons and
owners. Decisive failure suppresses the ordinary aggregate absent a distinct
authorized diagnostic purpose. Clean evidence permits one justified current gate,
with command/not-run, owner/stage, reason and evidence. A later omitted row makes
the earlier gate premature: targeted recovery precedes any justified rerun.
Acceptance consumes without duplication; conditional gate duties remain intact.
### Deferrals, known issues, and the human coordinator

Acceptance may approve bounded non-material deferrals, but the human
coordinator alone records them, before authorized advancement, by default in
`docs/known-issues.md` (or the repository's declared path). The record
carries a stable issue ID, task/review/finding provenance,
trigger/consequence/evidence, impact/likelihood, affected
boundary/consumers, deferral rationale, follow-up owner/action, and
reassessment conditions; optional proportional context links may relate it
to a subsystem, stable contracts/flows/plans, confirmed versus suspected
related issues, safeguards/assumptions with reassessment triggers, and
proposed versus committed relevant work. Discovery and acceptance never
write the tracker or acquire backlog/portfolio scheduling authority, and no
known-issues file is required before a deferral exists.

A relevant later preflight or acceptance reassesses recorded known issues
against that task's exposure and obligations: unchanged compatible exposure
preserves the accepted deferral, changed exposure or a changed consumer
requirement is routed through the record's follow-up owner for focused
resolution or review, and unrelated issues never trigger a broad issue
search. A later priority change alone does not reopen an accepted
deferral; changed material facts that invalidate an acceptance assumption
can require focused review under existing authority. A new correction
blocker needs current proof, materiality, and an explicit reason
(regression, formerly blocked evidence, a missed existing obligation,
changed context/authority, or newly demonstrated material risk); optional
improvements never restart correction, and no global correction-round limit
is added.

### Verification gate ownership
- Initial implementer: fail-first evidence, targeted checks, the nearest owning
  suite, the canonical architecture gate when required, and a broader gate only
  when authority or blast radius justifies it.
- Maintainability reviewer: rerun or validate the canonical architecture gate,
  inspect its warnings plus the changed design and immediate neighbors, and
  avoid spending budget on full functional acceptance.
- Functional discovery reviewer: targeted adversarial probes first; after a
  decisive failure, skip the broad gate unless it has a distinct authorized
  diagnostic purpose. When maintainability review is required, do not redo
  general architecture review unless architecture directly causes the
  functional defect.
- Correction implementer: reviewer regressions followed by the nearest owning
  suite and required architecture gate; leave an assigned final reviewer's
  aggregate functional gate untouched.
- Fresh final functional reviewer: rerun reviewer regressions, complete the
  finite review ledger against corrected bytes, and run one justified aggregate
  gate after adversarial evidence is clean.
### Optional tests-only reproducer

After fixing and reporting an independent `CHANGES_REQUESTED` verdict, the
reviewer may add a failing test only when the current user or exact review
invocation explicitly authorizes `tests_only_reproducer` and names the exact
writable test file or bounded test area. Task scope, `review: immediate`, or an
allowed test path is not write permission.

The reviewer must not change production code, shared test infrastructure,
dependencies, plans, architecture policy/baselines, or result artifacts, and
must not stage or commit the test. It must prove the focused intended failure
and report status and diff side effects. The verdict remains
`CHANGES_REQUESTED`, and corrected production bytes always require a fresh
reviewer; the reproducer-writing session cannot accept them.
## Recommended agent session usage for context reuse

- Keep the implementer session alive.
- When maintainability review is required, run it in a separate, independent session first.
- Feed maintainability findings back to the implementer and repeat that stage until accepted.
- Run fresh `task-review-discovery` in a separate session that did not author
  the bytes, then run functional acceptance in a separate, independent
  reviewer session; hand the fresh discovery report to the decision call
  instead of re-probing.
- Feed functional findings back to the implementer; implementation corrections, including tests-only corrections, then re-enter every conditional stage whose reviewed scope the correction affected — the architecture gate and fresh maintainability review when their reviewed scope changed, and the contract-registry stage when it applied and the correction affected it — and re-enter fresh discovery before fresh functional acceptance. Current evidence for the corrected scope keeps an unaffected stage out of the route.

If the implementer session becomes very long or confused, start a fresh
correction session using the reviewer's concise findings and tests. Context
reuse is an optimization, not a requirement.
### A practical heuristic for the implementer context

  - Below 50%: normally resume the implementer.
  - 50–70%: resume for one focused correction if the session stayed clean.
  - Above 70%: prefer a fresh correction session with the findings and tests.
  - At any percentage: restart if the agent repeats work, relies on stale state, confuses roles, or loses track of findings.


<!-- contract-registry-flow:task-flow-readme:begin -->
## Contract-aware standard sequence

For repositories with implemented-contract discovery enabled, the standard bounded-task sequence is:

```text
task brief
  -> task-verification-designer      (required for a supplied executable task package)
  -> task-preflight                  (required ready preflight for that package)
  -> bounded-task-implementer
  -> deterministic architecture gate
  -> task-maintainability-review
  -> task-contract-registry-updater
  -> task-review-discovery
  -> task-acceptance-review
```

Ownership is intentionally separated:

- planner: intended cross-task contract;
- implementer: executable implementation and executable/declarative contract bytes;
- registry updater: machine-readable current-state discovery plus stale explanatory references;
- acceptance reviewer: independent consistency proof.

Reference-only acceptance failures return to `task-contract-registry-updater` and then fresh acceptance. Implementation defects return through the normal implementation/review path. Planned/current semantic mismatches return to the planning owner rather than being normalized by the updater.
<!-- contract-registry-flow:task-flow-readme:end -->
