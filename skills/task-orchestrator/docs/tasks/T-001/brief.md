# Task Brief: `T-001` — Check what the local agent runtime can safely do

## Outcome

Find out how the local agent runtime (the harness) can start agents, limit their
permissions, collect results and recover after an interruption. Also check how
it can safely commit task changes and notify the owner when help is needed.

Record one supported way to connect the controller to the runtime. Show the
evidence for each required capability. If a capability is missing or unproven,
state what blocks further work and what must happen next.

The next implementer will use this report to build the connection, called the
adapter. T-001 produces the report; later tasks build the adapter and workflow.

## Direction trace

- What this supports: the owner approves a task once. Agents then implement,
  check, independently review and correct it within the approved permissions.
- What the owner gets from T-001: a report of what the runtime supports and what
  still needs proof. This enables the
  [first useful proof](../../direction-local-harness.md#direction-at-a-glance):
  correct a task, check it again, obtain a fresh independent review, then commit
  it before the next dependent task can start.
- Why this comes first: T-002 needs this report, identified in the plan as
  ART-008. Later tasks also need it to start agents, recover interrupted work
  and complete tasks safely.
- Approved choices: [the direction](../../direction-local-harness.md), sections
  “Scope”, “Boundaries” and “Direction ledger”, permits choosing the connection
  method. Changes to owner authority or required safeguards need owner approval.
- New direction decisions required: None.

Status: `ready`

Task kind: `executable`

Profile: `guided` — investigate capabilities and write the report. Production
code and live run records stay unchanged.

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 25 tool calls / 60 minutes / 80k context
```

## Execution sizing

- Sizing policy: `default@1`, from the active project-local
  `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 22.
- Estimated implementation duration: 60 minutes.
- Estimate confidence: medium; installed interfaces and permission evidence need inspection.
- Intended execution profile: `strong/high`; launch guidance, not an observed runtime setting.
- Policy result: `override_cannot_split_safely`.
- Triggered limits: calls greater than 15; duration greater than 40 minutes;
  `strong/high` execution-profile trigger.
- `decomposition_override: cannot_split_safely` — considered separate lifecycle,
  permissions and commit/notification investigations. Each would select or constrain
  the same transport and version, forcing the final selector to repeat inspection
  and renegotiate their handoffs if one capability fails. One investigator owns
  the selection and ART-008; no production code or full workflow pilot is included.
  Residual risk: a missing runtime capability may consume the checkpoint. Report
  the evidence gap and stop rather than expand into another backend or harness.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [Local harness orchestration plan](../../local-harness-orchestration-plan.md), “T-001 scope and decisions”, artifact/interface catalogs and Q-001/Q-002; [task map](../../local-harness-task-map.json), T-001 |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Dependencies | No implementation prerequisite. [Independent plan review](../../project-plan-review.md) is `ACCEPT`; its recorded plan/map hashes matched at brief creation. Recheck current authority during preflight. |
| Allowed changes | This task package: publish `harness-contract.md` as ART-008 and minimal task-local evidence needed to reproduce its conclusions. Use disposable local fixtures for approved non-billable probes. |
| Read-only context | `skills/task-orchestrator/references/architecture-map.md`, `references/operator-guide.md`, `scripts/codex_worker.py`, `scripts/controller_state.py`, `scripts/controller_git.py`, `scripts/verification_runner.py`, owning schemas/tests, and actual installed harness interfaces |
| Out of scope | Production adapter/controller/schema changes, shared harness infrastructure, multiple backends, run-state edits, installation/profile changes, active-install refresh, real project commits, remote publication and the T-006 model-driven pilot |
| Discovery facts | Installed API/version, callable operations and enforceable permission support are UNKNOWN; this task resolves them. No unsupported capability is assumed. |

Do not modify the official plan, map or existing review. Inspect installer ownership
only if a proposed dependency/profile change arises; such a change is outside T-001.
Use the available installed `openai-docs` workflow when investigating Codex product
interfaces; check local evidence first and official documentation when needed.
Networked smoke tests and billable model runs require explicit authorization.
Do not interpret this brief as that authorization or send a real notification.

## Work and acceptance criteria

1. Inspect current transport and existing tests before designing probes. Distinguish
   interactive coordinator tools from APIs actually callable by the Python controller.
2. Select the smallest supported bridge. Prefer the existing safe adapter where
   adequate; native delegation is preferred only if it satisfies the same contract.
3. Publish a versioned ART-008 with source references, dated local observations,
   commands/setup, observed results, limitations, and consumer handoffs. Clearly
   distinguish existing runtime calls from proposed controller/adapter operation names.

- **AC-01 — Concrete selection:** ART-008 names one selected transport/API and
  supported version, or identifies the exact missing capability and owner options.
  It explains why that choice is the smallest supported bridge and identifies
  which functions are callable from each side of IF-001/002/004. No second backend
  is built to hide a capability gap.
- **AC-02 — Identity and recovery:** The contract fixes exact operation names and
  request/result boundaries for launch, wait/status, collect, cancel and reconcile;
  operation/session identity, duplicate handling, durable output location, and
  adapter-owned receipt provenance are concrete. It explains coordinator replacement
  and the ambiguous launch-without-receipt case. Actor-authored identifiers cannot
  substitute for observed provenance; unknown liveness never permits relaunch.
- **AC-03 — Permissions and policy:** ART-008 identifies actual enforcement for
  implementation writes, read-only review, and protected run/controller/skill roots.
  Session identity or prompt instructions alone are insufficient. Check the existing
  frozen actor model/reasoning mappings and `0.5` implementation-context reuse rule
  in `controller_state.py` and `flow-profile.schema.json`. Identify the context
  measurement source; unavailable measurement is unknown, never zero. Any required
  policy change is an owner decision and blocks affected dependent implementation.
- **AC-04 — Commit and intervention support:** Specify the mechanism for safe
  task-scoped local commits, preservation of unrelated staged/unstaged owner work,
  durable intent/receipt and crash reconciliation without duplicate commits. Specify
  intervention delivery and observable delivery failure. These are support contracts,
  not T-005 finalization or T-003 notifier implementation; unavailable/uncertain
  support is explicit and cannot authorize dependency release.
- **AC-05 — Honest disposition:** Every required capability is marked supported
  with its evidence level, unsupported, or unverified with the exact missing proof.
  Record Q-001/Q-002 disposition and effects on T-002..006. A complete investigation
  can report a blocker; that does not make the harness qualified or successors ready.
  Unapproved live probes stay pending, with the smallest owner action stated.

### Finite-risk coverage contract

These rows scope the investigation; they do not require implementing downstream
guards. Each conclusion must be corroborated at the boundary it claims to cover.

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R1: identity and recovery preserve one active operation | First launch; repeated same operation key; live, terminal and unknown status; launch with missing receipt; replacement coordinator | Selected API/process and persisted receipt distinguish these cases; unknown blocks a new launch | Exact protocol/observations and safe local probe output where available; explicit gaps otherwise | Trace one duplicate and missing-receipt recovery from documented observations, without trusting actor claims | T-001 investigator gathers evidence; fresh reviewer owns aggregate corroboration |
| R2: role and protected-root permissions are enforced | Implementation allowed writes; review denied writes; worker denied writes to run records and active controller/skill roots | Actual permission boundary allows the intended fixture write and denies protected writes | Existing enforcement/code evidence plus safe boundary probes where available; flags/fake argv alone are configuration evidence | Check whether denial evidence used the real selected boundary; mark unverified if it did not | T-001 investigator; fresh reviewer corroborates claims |
| R3: commits and notifications cannot become false success | Accepted paths plus unrelated staged/unstaged changes; interruption before/after commit; unavailable/unknown commit; intervention delivery success/failure | Disposable Git repository preserves owner content and reconciles one commit, or limitation is recorded; notifier has observable delivery status | Reproducible local mechanism evidence; no real owner notification or project commit; unavailable real notifier proof remains pending | Inspect exact-path and crash assumptions and failure reporting against the chosen mechanism | T-001 investigator; fresh reviewer owns aggregate contract check; runtime integration belongs to T-003/005/006 |

## Expected contract impact

- Preserve plan refs CAP-001/002, FLOW-001/002, IF-001/002/004 and
  INV-001/002/004/007. Commit support also constrains INV-006 without implementing it.
- Materialize ART-008 at `skills/task-orchestrator/docs/tasks/T-001/harness-contract.md`.
  It is the single selection/limitation handoff to T-002..006, not a second state ledger.
- No current `docs/contracts` registry exists at brief creation. Reuse the cited
  source/schema/test contracts as evidence, without claiming the proposed operations
  are already implemented. Do not create a registry as part of this proof task.

## Verification

Verification reasoning: **separate —** role enforcement, ambiguous launch recovery,
receipt provenance, and safe commit support admit plausible but unsafe conclusions.
Derive `verification.md` with the installed `task-verification-designer`, then obtain
ready `preflight.md` with `task-preflight` before executing this packaged task.

Readiness route: **standalone guided preflight** — confirm installed tooling,
permission envelope, authority freshness, task-owned output paths and cheap probe
commands. Capability feasibility itself is T-001's output, not a preflight assumption.

| Evidence | Scenario and oracle | Command / ownership |
|---|---|---|
| Targeted investigation | Reproduce selected-interface claims with explicit inputs, setup and observable outputs; mark documentation/configuration evidence separately | Verification designer specifies bounded non-billable local probes after focused interface discovery; no live actor launch by default |
| Existing transport coverage | Existing fake-CLI cases cover result persistence, resume, missing/invalid output, safe argv, live-process rejection and interruption; they cannot qualify the real harness | If needed for a reuse claim: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py`; investigator runs targeted methods first |
| Negative claim check | An unavailable receipt, denied-write proof, usage meter, commit or delivery mechanism must produce a limitation, not a support claim | Investigator traces AC-02..05 and R1..R3; no fail-first production regression required because no runtime changes |
| Aggregate gate | All ACs and finite-risk rows have evidence or explicit blockers; downstream readiness follows those dispositions | Fresh independent reviewer checks completed ART-008 and evidence, including corrections; no repeated full repository suite for documentation-only work |
| Stronger qualification | Model-driven independent sessions and full correction loop | T-006 owns the separately authorized real pilot; report pending here |

## Stops and handoff

- Stop for conflicting authority, overlap with owner work, permission expansion,
  production/shared-tool changes, or billable/networked smoke probes without approval.
- If the decisive support cannot be established safely, finish the investigation
  with the exact blocker and smallest next owner action. Do not implement around it.
- Treat the budget as a checkpoint and preserve existing work. Do not refresh the
  active skill/controller installation during this run.
- Next: derive verification, obtain ready standalone preflight, then execute T-001
  through `bounded-task-implementer` as a proof-only task.
- Required follow-on: immediately after implementation or correction and any
  applicable conditional stages, hand the completed bytes to a fresh independent
  `task-review-discovery` call; hand its report to a separate `task-acceptance-review`
  decision. Resolve actual installed roles; do not substitute source-only workflows
  without explicit authorization. Self-review does not satisfy this handoff.
- Hand ART-008 to successors only with its capability dispositions. Any unsupported
  or unverified required boundary keeps affected implementation blocked; acceptance
  of a truthful investigation does not waive that gate.
