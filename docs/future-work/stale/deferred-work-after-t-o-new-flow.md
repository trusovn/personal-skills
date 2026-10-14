# Deferred ideas and investigations — after `t-o-new-flow`

**Prepared:** 2026-10-09  
**Repository:** `trusovn/personal-skills`  
**Relationship to current work:** Companion to `t-o-new-flow-plan-amendment-handoff.md`. This is a **future-options register**, not a task list to implement in the current branch. The current five-task standalone verification/review refactor and its test scope remain unchanged.

## 1. Boundary: what the current plan is already expected to deliver

The `t-o-new-flow` plan ([docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md), [docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json)) already defines:

- `T-001`–`T-005`, including a separated discovery/acceptance decision, explicit deferral handling, correction handoffs, installation consistency, and qualification.
- `INV-001`–`INV-011`, tied to flows, interfaces, tasks, and intended verification.
- `ART-008`: coordinator-owned accepted-deferral/known-issue records with rationale and reassessment conditions.
- A system verification map specifying existing local and composed evidence obligations.

**Do not count these as future features** and do not duplicate them in a separate implementation framework. Some concepts discussed earlier as “worth doing now” are *already planned*; the amendment only makes a few relationships and decision-authority boundaries clearer.

There are two different classes of future work below:

- **Already anticipated by the code-guided orchestration direction**, but excluded from the current *standalone* refactor.
- **Additional, unvalidated capabilities**, which should be considered independently after focused experiments.

## 2. Already anticipated for the *later* code-guided orchestrator

This work remains important to the executor direction, but should not be slipped into `T-001`–`T-005`.

### 2.1 Structured stage results and evidence admission

**Problem:** Markdown preflight/review reports contain facts required to choose a workflow transition, but free-text parsing is not a sufficiently reliable machine protocol.

**Future direction:** Human-readable report plus **schema-validated machine-consumable outcome/ledger/evidence references**, with a single authoritative source for overlapping fields. Consider structured sidecars or typed envelopes for preflight, discovery, acceptance and correction, aligned with the chosen common invocation/run identity. Trusted tooling must independently capture/validate filesystem/Git/provenance facts; an agent-produced JSON field does not establish truth by itself.

**Already identified:** Orchestration spike `FLOW-01` (typed stage outcomes), `FLOW-04` (canonical freshness/effect records), `FLOW-05` (typed correction ownership), and `LIVE-01` (replayable evidence). Read the spike documents before scoping a new task.

**Format principle:** Markdown for authority/rationale/scenarios; JSON (or JSONL where appropriate) for execution transitions, observed facts and programmatic validation; YAML may be preferable for small human-maintained policy/configuration. Do not mechanically duplicate a full `verification.md` into JSON unless a real consumer needs it. If needed, distinguish a **verification plan** from a **coverage/result ledger** rather than maintaining two independently edited copies of the same truth.

### 2.2 Code-readable, versioned flow policy and resumable execution

**Problem:** The current flow has conditional stages and distinct correction routes that prose alone cannot enforce in an unattended executor. Fingerprints identify contents but are not runnable retained versions.

**Future direction:** Code-owned transitions, permissions and evidence checks; pinned/versioned skill-flow bundles; interruption recovery; compatibility checks for deliberate upgrades; release of eligible dependent tasks only after admitted evidence and authority. Keep AI judgment within its bounded stages.

**Already identified:** `FLOW-03` (flow authority), `FLOW-06` (retained runnable versions), plus interruption and lifecycle requirements in `skills/task-orchestrator/docs/code-guided-orchestration.brief.md`. Treat this as the next **separate orchestrator design/delivery plan**, not as a reason to change the standalone skill policy prematurely.

### 2.3 Execution telemetry and observable process claims

**Problem:** Final written verdicts do not prove that an agent followed its process contract (independent review, avoiding extra broad rediscovery, authorized write scope). Current spike telemetry did not exercise the shared run-evidence lifecycle.

**Future direction:** Reuse available transport events, trusted snapshots, command records, and existing evidence collection with explicit lifecycle ownership. Distinguish actual observed process from narrative explanations and unproved claims. Avoid creating duplicate collectors or an open-ended monitoring framework.

**Already identified:** `TELEMETRY-01` and `LIVE-01`. Do not expand current T-005 coverage as part of the immediate plan amendment; reconsider qualification requirements in the later executor plan under its own authority.

## 3. Optional future capability: system/master verification strategy

**Status:** Valuable idea; **investigate through an optional post-plan experiment before standardizing a skill or required stage**.

### What problem it addresses

In multi-task AI-assisted development, separate implementers can each produce credible tests while the overall project still suffers redundant E2E flows, repeated setup, inconsistent fixtures, and untested cross-task integration boundaries. Tests are easy to generate but potentially expensive to execute, triage and maintain.

### Candidate responsibility

A *system-level verification allocation strategy*, derived from the approved system plan, could decide:

- Which critical requirements, flows, invariants and interfaces need proof, and at what **lowest reliable observation boundary**.
- Which task owns focused proof, and which remaining behavior requires an integration/composed qualification stage.
- Which shared fixtures, data and environments need early ownership rather than being repeatedly reinvented.
- Which higher-level tests add distinct failure detection versus duplicate more focused evidence.
- Which important testability gaps should be returned to the project planner before detailed task implementation.

This is **not** an exhaustive traditional Master Test Plan, complete test case catalogue, another requirements source, or a blanket E2E mandate. It may recommend changes but not invent or approve product requirements.

### Potential placement and reuse

After `project-delivery-plan` and independent `project-plan-verification`, before detailed task planning. The preliminary task map and system verification section already exist; the strategy would be **derived and optional**, rather than a replacement for section 11 or for task-local `task-verification-designer`.

Start with a fresh `testing-discipline` review of one verified multi-task plan. A dedicated skill or `docs/system-verification-strategy.md` convention should be introduced **only if repeat experiments show marginal value** beyond the current `project-delivery-plan` verification map. If overlap is substantial, improve the existing plan template instead.

### Investigation to run later

Compare an approved baseline plan with and without the optional verification-allocation pass. Assess distinct critical gaps, redundant evaluation work avoided, shared prerequisites discovered before coding, effort of the extra planning step, and later correction churn. The prior preliminary `testing-discipline` review found four plausible improvements (process observability, fixture timing, redundant evals, stop/resume and scenario revision), but the user explicitly decided **not to expand current test scope** on that basis. Retain those observations for a later assessment; do not silently import them as accepted requirements.

## 4. Optional future capability: backlog portfolio reasoning

**Status:** Worth exploring **after** stable known-issue records exist and a representative historical backlog can be accessed. This is a separate concern from task acceptance.

### 4.1 Local triage versus portfolio priority

Local acceptance decides whether a task may be accepted under present authority, evidence and material risk. Portfolio review decides whether already deferred/open issues, taken together, justify reprioritization, grouping, root-cause investigation, a targeted refactor, or continued conditional deferral. These can differ without contradiction; only changed material facts/authority should reopen a prior acceptance judgment.

Do **not** make a second broad agent mandatory for every finding, and do not give a portfolio advisor implicit project, issue-tracker, or acceptance-write authority.

### 4.2 Minimal issue history and cross-issue signals

Candidates: common affected subsystem or invariant; confirmed/suspected relation; repeated root causes; issue arrival/maintenance burden; a newly weakened safeguard; planned refactor or migration; deferral conditions that have ceased to hold.

A future deterministic checker can select relevant records and flag **known** invalidated assumptions or known hazardous combinations. It cannot infer all unreported defects or prove safety from silence. `ART-008` by itself includes only accepted deferrals; whole-backlog analysis may require GitHub Issues or an equivalent authoritative tracker.

A “refactor coming soon” assertion should state whether the work is merely proposed or approved/committed, whether it genuinely removes the defective path, whether delay is safe, and what change triggers reconsideration. A concentration of issues is a reason to investigate, not proof of a common cause.

### 4.3 Separate broader-context agent (only if triggered)

A bounded read-only agent could assess cumulative subsystem risk using curated project/backlog context, propose consolidated fixes or refactor investigations, and distinguish confirmed causation from hypotheses. Prefer **fresh, reproducible invocations** with explicit inputs and source references to an indefinitely running implicit-memory agent.

A possible future orchestration shape is one local decision, cheap mechanical related-context retrieval, and one deeper portfolio review *only for meaningful signals*. No recursion of independent agents checking one another.

### 4.4 Subsystem health and thread-branch optimization

Derived subsystem summaries could reduce rereads of unrelated backlog data and show recurring causes, issue trends, and maintenance burden. They are not automatically authoritative health scores.

For batches of related triage cases, a prepared parent context with isolated thread forks might save repeated discovery and benefit from runtime prompt caching. This is **cost optimization, not a correctness rule**: branches are based on the same snapshot and do not automatically observe one another's new decisions. Reconciliation remains necessary. Compare full batch costs (including preparation), latency and decision accuracy against fresh, targeted sessions before implementing forks.

### 4.5 Selective compound-failure rules

A few high-consequence invariants may benefit from explicit failure combinations, e.g., incomplete evidence plus ineffective validation or bypassable acceptance. Such rules can identify known conjunctions and reveal that a previous deferral relied on a now-failing safeguard.

Do **not** immediately build general fault-tree analysis, a hazard graph database, automated probability model, or a universal three-valued reasoning engine. Unknown is distinct from verified false, but not every unknown warrants another agent review. Only investigate formal modeling if lighter deferral-assumption checks materially miss consequential problems.

## 5. Optional future capability: invariants → evidence traceability

The current system plan already defines `INV-*` cross-task guarantees and maps them to tasks and intended verification. It is a useful foundation, **not evidence that every property is mechanically enforced**.

Possible later improvements, only where justified:

- Trace a critical guarantee through its owning task(s), scenario IDs, executable tests, and observed current evidence.
- Distinguish *specified*, *enforced*, *tested*, *observed passing*, *not verified*, and *not applicable*.
- Use invariant-based/property-based or state-machine tests for complicated retries, state transitions, ordering, authorization and side-effect boundaries.
- Capture explicit failed-check, stale-proof, independent-acceptance, and mandatory-versus-best-effort modes without turning advisory guidance into hard policy.

Do not create another global invariant registry or a mandatory test generator by default. Use existing `project-delivery-plan`, `task-map.json`, `task-verification-designer`, `testing-discipline`, and implemented-contract discovery. Add structured detail only when an actual consumer needs it.

## 6. Suggested order and decision gates

| Phase | Possible action | Gate before committing to implementation |
|---|---|---|
| Current standalone work | Finish and qualify `T-001`–`T-005` under present scope | No new stages/tests/cross-issue engine introduced |
| Orchestrator planning | Resolve structured outcomes, flow ownership, version retention and evidence admission already identified by the spike | Coherent code/AI authority boundary, real validation requirements, no duplicated policy |
| Optional test-strategy experiment | Apply `testing-discipline` to an approved multi-task plan after plan verification | Meaningful reduction in duplicate work and/or detection of critical missing integration evidence |
| Optional backlog triage experiment | Replay a modest number of historical issues with and without related-issue/deferral context | Actionable decision changes exceed manual metadata/agent cost and alert noise |
| Possible narrow feature | Add only the proven strategy or portfolio capability to an appropriate existing boundary | Exact ownership, durable inputs, output contract and stop behavior agreed |
| Advanced options | Thread branching, subsystem models, compound-failure rules, property-based/state-machine evidence | Concrete need supported by the preceding experiment |

The two optional experiments need not wait for every orchestrator feature if they can be run independently against stable planning artifacts. They **must not become prerequisites** for completing the standalone flow or the first useful code-guided executor.

## 7. Anti-scope-creep rules for future planners

- No universal second-agent approval for every issue or plan.
- No automatic refactor decision based solely on issue count or co-location.
- No acceptance-policy bypass on the promise of future maintenance.
- No invented new normative requirement in a derived test strategy.
- No blanket increase in test count; measure marginal confidence and total maintenance cost.
- No double maintenance of the same requirement in independently edited Markdown and JSON/YAML.
- No assumption that an agent-produced schema-valid outcome proves action provenance or evidence correctness.
- No merging of a future portfolio advisor into an independent acceptance role without a separately approved scope change.
- No general workflow platform, formal failure-tree program, or persistence infrastructure before demonstrated need.

**North star:** reusable project guarantees and durable decisions; minimal targeted evidence; cheap detection of known contextual changes; deeper reasoning only where it materially changes an engineering decision.
