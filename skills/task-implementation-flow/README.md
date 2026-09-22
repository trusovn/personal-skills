# Task implementation flow

These seven task skills provide a reusable implementation discipline without
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
| `task-preflight` | Check readiness, ownership, commands, and decisive evidence when dirty ownership, dependencies, environment, permissions, helpers, fixtures, real-boundary capability, or a durable handoff creates material uncertainty. | A routine guided task can perform the same compact self-check inside the implementer. |
| `task-verification-designer` | Optionally turn one executable brief into a separate task-local verification design with AC coverage, discriminating scenarios, and decisive oracles before implementation. | The task is small and its decisive tests/oracles are already obvious from the brief. |
| `bounded-task-implementer` | Implement one bounded task with risk-based tests, progressive verification, and a useful handoff. | The request is planning, review-only, or too ambiguous to implement safely. |
| `task-maintainability-review` | Independently assess the changed design for concrete maintainability regression after the repo's deterministic architecture gate. | The repo does not require maintainability review and the user/task does not request it. |
| `task-contract-registry-updater` | Synchronize implemented-contract discovery after maintainability review. | The repository does not use implemented-contract discovery, or the task did not change a durable cross-task contract. |
| `task-acceptance-review` | Independently assess scoped functional/specification correctness and return `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`. | The task does not need independent functional review under its metadata or risk. |

`architecture-guardrails` is a foundation/setup skill, not a per-task reviewer. It
materializes the deterministic gate and short repo-local contract that this flow
can consume.

## Workflow identity

When a task run needs to record which implementation workflow was used, obtain
the identity from the repository-level `scripts/workflow_version.py` utility.
It returns machine-readable JSON and is the single canonical fingerprint
implementation. Task skills should not duplicate version calculation or
maintain manual version numbers. Future run-evidence collection should call
that utility rather than infer workflow identity from prose or repository HEAD
alone.

## Task sizing, decomposition, and durable artifact discovery

`task-brief-designer` treats its execution estimate as a decomposition gate.
The authoritative, packaged policy files are intentionally external to the
skill body:

- sizing policy: [`task-brief-designer/references/task-sizing.yaml`](task-brief-designer/references/task-sizing.yaml)
- durable artifact layout: [`task-brief-designer/references/task-artifact-layout.md`](task-brief-designer/references/task-artifact-layout.md)

This keeps calibration editable without rewriting the skill. A task that
matches any active decomposition trigger becomes a non-executable composite
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
    verification.md               # only when separate verification design is used
    preflight.md                  # only when a durable preflight artifact is needed
    reviews/
      maintainability-01.md       # only when a durable report is written
      acceptance-01.md
```

Repository/user authority may choose a different task-package root or directory
name, but every durable task keeps `brief.md` and its optional artifacts inside
one dedicated package directory. `docs/task-map.json` remains the verified
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

## Guided profile: default

Use guided mode for most ordinary bounded tasks, especially when a person is
launching the skill directly.

```text
existing request or brief
        ↓
fill only meaningful contract gaps
        ↓
optional task-verification-designer when the brief recommends it
        ↓
implementer self-preflight
        ↓
implement + risk-based tests + progressive verification
        ↓
human-readable result
        ↓
required architecture gate / maintainability review, if declared by repo
        ↓
fresh-session functional acceptance review when metadata or risk calls for it
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
   functional review is required, end at `READY_FOR_REVIEW` and route the
   completed bytes to the appropriate fresh reviewer.

The implementation agent should not be burdened with a long architecture
rubric. When the repo has maintainability guardrails, follow the short
repo-local contract (normally cohesion, change locality, explicit/narrow
dependencies, testability, and no speculative abstraction) and let the
canonical gate plus `task-maintainability-review` enforce the deeper policy.

The brief designer, verification-design pass, and standalone preflight are
optional in guided mode. Use them when they reduce ambiguity, verification
reasoning load, or readiness risk; do not create artifacts merely to satisfy
the diagram.

### When separate verification design adds value

A ready executable brief explicitly recommends either `inline` verification
design or `separate — <reason>`. Use `task-verification-designer` for the
separate route when task-local semantics are non-obvious enough that asking the
implementation agent to invent the decisive scenarios while coding would add
avoidable cognitive load. The skill writes `verification.md` in the executable
task package and leaves concrete test implementation to
`bounded-task-implementer`.

This recommendation is advisory. Small changes with an obvious regression and
oracle should stay inline. The initial verification-designer contract is
task-local and does not own cross-child or parent-level integration-test design.
### When standalone preflight adds value

Use the implementer's compact self-preflight for routine guided work. Use
standalone `task-preflight` when a separate readiness pass can resolve a named
material uncertainty, such as:

- dirty or multi-writer ownership;
- a required environment, permission, dependency, helper, or fixture;
- real-boundary capability or an unresolved command and observable oracle;
- a required repo gate whose command or prerequisites are not actually ready; or
- a durable handoff between sessions.

A directly requested standalone preflight still returns a truthful readiness
result even when its incremental value is marginal. It should stay compact,
avoid broad baseline work without a named readiness reason, and recommend
implementer self-preflight for the next materially similar task. Explicit
high-assurance and orchestrated flows continue to require standalone
preflight.
## Maintainability-gated profile

Use this profile whenever repo authority declares architecture/maintainability
review required, or when the user explicitly asks for focused maintainability
verification.

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
        │
        └── ACCEPT
                ↓
        functional/spec acceptance review when required
                ├── CHANGES_REQUESTED
                │       ↓
                │   implementation correction
                │       ↓
                │   architecture gate + fresh maintainability review again
                │       ↓
                │   fresh functional acceptance review again
                │
                └── ACCEPT
```

Do not reverse the two semantic reviews merely to save a stage. The first
review asks whether the change introduced or materially worsened concrete
design/maintainability risk. The later acceptance review spends its budget on
whether the code actually satisfies the requested behavior and preserves
required behavior.

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
Maintainability review accepted the current production bytes. Focus review budget
on specification conformance, observable behavior, regressions, edge cases, and
test adequacy. Do not redo general architecture review unless architecture directly
causes an observed functional defect.
```

When the flow already carries a byte/diff digest, attach it to both reviews. In a
lightweight human-driven flow, at minimum confirm the production diff did not change
between maintainability `ACCEPT` and functional-review start.

Every correction changes the bytes under review. Therefore a previous
maintainability verdict and a previous functional verdict are both stale after
production corrections. Rerun the deterministic architecture gate and use a
fresh maintainability reviewer before re-entering functional acceptance.

For a trivial correction that provably cannot affect production architecture
(for example, an authorized tests-only correction), repo policy may allow the
maintainability stage to be skipped; do not infer that exception when the repo
says the gate is required for all changed source bytes.
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
optional task-local verification design when recommended
        ↓
fresh preflight packet (`ready`)
        ↓
bounded implementation + structured worker result
        ↓
required deterministic architecture gate + independent maintainability report
        ↓
independent functional acceptance report
        ↓
orchestrator or human advancement
```

If the repo does not require maintainability review, omit that stage rather than
manufacturing policy for the task.

High-assurance mode may require exact digests, package-contained durable task
artifacts, external runtime policy/schema/result state, and strict entry/exit
statuses. A guided run that
encounters one of these needs should pause and recommend the smallest
escalation rather than silently rebuilding the entire chain.

When a task-local `verification.md` exists, preflight records its path and
digest as a derived input, maps its scenario IDs to packet commands/oracles,
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

- responsibility/cohesion;
- unnecessary or hidden coupling and dependency direction;
- change locality across owning subsystems;
- independently testable important logic;
- duplicated business/domain rules or growing dispatch structures;
- speculative layers/interfaces/abstractions with no concrete boundary,
  variation, or test-seam value;
- deterministic gate failures and architecture warnings that correspond to a
  real design problem.

Do not make maintainability review a second functional review or a style
preference contest.

Independence is based on session authorship. Loading another skill, quoting its
instructions, or changing roles in the same session does not reset provenance.
A session that authored reviewed production bytes may perform a labeled
`SELF_CHECK_ONLY` and fix defects it finds, but it cannot issue an independent
verdict. Only a fresh reviewer may return `ACCEPT`, `CHANGES_REQUESTED`, or
`INCONCLUSIVE` for those bytes.

Every `CHANGES_REQUESTED` correction requires fresh review for the affected
stage, and production corrections invalidate both semantic review verdicts when
both stages are required. A previous verdict never applies to corrected bytes.
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
- Run functional acceptance in a separate, independent reviewer session after maintainability acceptance.
- Feed functional findings back to the implementer; production corrections then re-enter the maintainability stage before fresh functional acceptance.

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
  -> bounded-task-implementer
  -> deterministic architecture gate
  -> task-maintainability-review
  -> task-contract-registry-updater
  -> task-acceptance-review
```

Ownership is intentionally separated:

- planner: intended cross-task contract;
- implementer: executable implementation and executable/declarative contract bytes;
- registry updater: machine-readable current-state discovery plus stale explanatory references;
- acceptance reviewer: independent consistency proof.

Reference-only acceptance failures return to `task-contract-registry-updater` and then fresh acceptance. Implementation defects return through the normal implementation/review path. Planned/current semantic mismatches return to the planning owner rather than being normalized by the updater.
<!-- contract-registry-flow:task-flow-readme:end -->
