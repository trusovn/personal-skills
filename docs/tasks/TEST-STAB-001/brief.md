# Task Brief: `TEST-STAB-001` — Stabilize test ownership before T-003

Status: `decomposed`

Task kind: `composite`

## Outcome

Agents can locate and extend preparation, review, fixture and composition tests
through explicit owners and focused commands. Existing scenarios, failure
signals and supported evaluation execution remain intact.

## Authority and sequence

- Primary authority: user request of 2026-10-10 for a bounded, behavior-preserving
  test architecture cleanup in `trusovn/personal-skills`, branch `t-o-new-flow`.
- Maintenance authority: root `AGENTS.md` and the active project-local
  `.agents/skills/testing-discipline/SKILL.md`, especially “Maintain the suite,”
  “Assert behavior, not construction,” and the refactor baseline rule.
- Read-only context: [project plan](../../project-plan.md), sections 1, 10–12;
  [task map](../../task-map.json), T-001 through T-005;
  [T-001 package](../T-001/brief.md), its child results/corrections;
  [T-002 package](../T-002/brief.md), its child results/corrections;
  [T-002.4 results](../T-002.4/results.md) and
  [composition inputs](../T-002.4/composition.json).
- This is supplementary maintenance, not a new plan task or T-002 child.
  Finish both leaves and their required
  reviews before T-003 begins. Do not rewrite official dependencies to encode
  this user-imposed sequence.
- Local observation: commit `0eb7963` is titled “T-002.4 done (accepted)”; its
  results document retains its earlier submission status. 

## Problem and smallest worthwhile scope

At authoring HEAD `520476b`, `tests/test_review_discipline.py` has 2,277 lines
and 74 test methods across unrelated responsibilities. The brief designer's
`tests/test_package_resources.py` has 913 lines and 30 test methods, including
preflight, implementer and whole-flow checks. These are source inventories, not
executed test totals; older results report smaller suites.

The discovery and acceptance fixture generators have 1,395 and 2,757 lines.
They are independently shipped setup programs. Their source-parity guard uses
role substitutions, regular expressions and function-text equality. Removing
that guard safely needs a wider scenario proof than this task permits.

This task addresses ownership and locality first. It then consolidates the
same destructive/mitigated export probe duplicated in the composition test,
and removes an incidental newline requirement in a preparation assertion.
Repository-test setup can share a small helper; skill eval setup must remain
self-contained. No test-count or file-size target justifies losing evidence.

## Direction trace

- Contribution: preserve the approved standalone preparation/review flow while
  making its regression evidence easier to maintain.
- User-observable effect: no product or workflow change; enables focused T-003
  correction tests, T-004 installation checks and T-005 reuse of existing
  qualification inputs without further mixed-owner growth.
- Why now: the user's required interval between accepted T-002.4 and T-003.
- Decisions used: user constraints; plan sections 10–11 retain separate task
  evidence purposes, independent packages and truthful qualification claims.
- New direction decisions required: None.

## Scope and exclusions

Allowed: the two named test modules; new owning modules/support under `tests/`;
the remaining brief-designer package tests; a concise `tests/README.md` with
ownership and commands; new evidence within the implementing leaf's package.

Read-only: source `SKILL.md` files and references; all eval JSON/setup programs;
installer, shared runtime scripts and installation documentation; approved
plans/task map; historical reviews/results and existing task packages;
active `.agents/` installation. Inspect installer compatibility without changing
its selection or ownership. Do not refresh the active installation.

Exclude T-003's new correction matrix/cap removal, T-004's unborn/drift feature,
T-005's composed role-call qualification, new scenarios, frameworks, runners,
CI gates, cross-skill fixture dependencies, production contracts and workflow
semantics. Defer shared **eval generator** extraction and replacement of the
inherited fixture source-parity guard. Preserve and clearly label that guard as
structural protection, not observed behavioral equivalence.

## Execution sizing and decomposition

- Policy: `default@1` from the active brief designer's
  `references/task-sizing.yaml` (15 calls / 40 minutes, exclusive maxima).
- Original estimate: **26 implementation-agent calls / 75 minutes**;
  `standard / medium`; confidence medium. Triggers: `max_agent_calls`,
  `max_duration_minutes`.
- Estimates include focused discovery, test/doc edits and local verification;
  exclude verification design, preflight and independent reviews.

| Child | Owned outcome and stable handoff | Depends on | Brief |
|---|---|---|---|
| TEST-STAB-001.1 | Ownership migration with unchanged assertions; old-to-new test map and runnable commands | Accepted T-002.4 | [brief](../TEST-STAB-001.1/brief.md) |
| TEST-STAB-001.2 | Bounded setup/assertion consolidation; delta map and final preservation evidence | Accepted TEST-STAB-001.1 | [brief](../TEST-STAB-001.2/brief.md) |

The split separates a verifiable assertion-preserving migration from changes to
the evidence itself. The second leaf consumes fixed owners and selectors from
the first; it does not renegotiate placement. Shared modules are edited
sequentially. Each leaf can pass its own baseline and acceptance independently.
This makes dropped tests and weakened assertions easier to attribute than a
single large move-and-simplify diff. Arbitrary file halves and a separate
“write tests” task offer no comparable boundary.

## Coverage and closure

| Parent requirement | Owner |
|---|---|
| P-01 Clear owners, local changes and navigable commands | .1 |
| P-02 Safe reduction of repository-test setup duplication | .2 |
| P-03 Consolidate proven redundant evidence and incidental text coupling | .2 |
| P-04 Preserve scenarios, failure detection, permissions and package independence | .1 baseline/migration; .2 baseline/consolidation |
| P-05 Preserve installation projection and truthful evidence categories | Both leaves; .2 owns final closure |

Leaf estimates fit the active policy: .1 **14 calls / 40 minutes**, .2 **12 calls /
35 minutes**. No override. Each leaf owns its new result/map; neither rewrites
the other's preparation or results. No production interface changes or sibling
wiring need a third integration task: .2's aggregate preservation check closes
the composed result after .1's accepted migration.

## Handoff

Prepare dependency-ready leaves using `task-verification-designer`, then
`task-preflight`, then `bounded-task-implementer`. Do not launch this parent.
Both leaves require fresh discovery and a separate acceptance decision after
applicable conditional stages. No refactor is implemented by this package.

Expected contract impact: none. Preserve relevant plan invariants and ART-009
evaluation packaging; do not invent a registry or ART-012 qualification result.
