# Task Brief: `T-003.2` — Report every confirmed bounded maintainability blocker

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 10 tool calls / 25 minutes / 35k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 10. Duration: 25 minutes. Confidence: medium.
- Intended profile: `standard / medium`. Policy result: fits; triggered limits:
  none; decomposition override: none. Implementation work only.

## Readiness route

standalone guided preflight — confirm maintainability policy and task-local
fixture setup. Derived `verification.md`, then ready `preflight.md`, are required.

## Verification-design recommendation

separate — removal of a cap must preserve bounded review, actionable materiality
and truthful partial coverage. Existing eval format and local stdlib fixture
patterns support a task-owned setup; no shared harness is authorized.

## Outcome and direction trace

Maintainability guidance requires every confirmed blocker found within its safe,
authorized review scope to be reported, without a three-blocker cap or stopping
because enough blockers already justify a verdict.

- Contribution: `CAP-002`, `FLOW-002/003`, `ART-005/009`, `IF-003`, `INV-008`;
  preserve `INV-004/005/006/011` and downstream IF-004/005/006.
- Effect: callers receive the complete bounded correction set; the next review
  can address sibling defects together. Enables .4/T-005 qualification.
- Why now: T-002's complete discovery/decision ledger needs complete conditional
  findings from its maintainability producer.
- Decisions: plan sections 1, 7 IF-003, 10 T-003 and 11; parent P-02/P-07.
- New direction decisions required: None.

## Authority and scope

- Authority: [plan](../../project-plan.md), cited sections;
  `T-003` [task-map entry](../../task-map.json); [parent](../T-003/brief.md).
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: completed/reviewed T-001/T-002. Consumes
  `ART-001/002/003/004/005/006/007/009`; produces complete ART-005 and ART-009.
- Allowed: source `skills/task-implementation-flow/task-maintainability-review/`
  skill and eval cases, task-local `evals/files/setup_fixture.py` if needed;
  focused `tests/test_task_maintainability_review.py` if no existing owner covers
  the distinct cases. Update only stale maintainability entries in flow/profile
  guides. Inspect installer selection/guide/helpers; preserve existing selection.
- Read-only: existing reviewer test owners, staging helpers, discovery and
  acceptance contracts, plans/history and active `.agents/` copies.
- Excluded: wider review scope, exhaustive repo review, style/preference blockers,
  new gate/schema/runner, automated role invocation and global round limits.
- No unresolved direction decision. Fixture paths/selectors are preflight facts.

## Work and acceptance criteria

1. Remove the reporting cap and enough-blockers stop while retaining scope,
   safe-budget stops, evidence fields and architectural-impact ordering.
2. Supply one small runnable changed-production fixture with four distinct
   independently observable maintainability blockers, legitimate task/policy,
   baseline/diff, and a non-blocking preference control. Reuse existing setup
   conventions and coverage rather than cloning a runner.

- **AC-01:** All confirmed blockers from the bounded review are reported with
  stable identity/location, introduced or worsened problem, evidence, concrete
  maintenance consequence and smallest correction direction. Four supplied
  blockers remain four; finding count alone cannot end discovery or truncate output.
- **AC-02:** Review stays within authorized changed/influenced surfaces and
  affordable safe probes. Genuine permission/capability/budget stops preserve
  outstanding coverage with reasons/next owner; incomplete required proof is not
  a clean result. Keep current gate, verdict, independence and materiality rules.
- **AC-03:** No preference or speculative redesign becomes a blocker to fill
  a quota. Existing self-check, unavailable-gate and report-path cases retain
  their distinct expectations. Supplied setup proves defects exist, not that an
  agent reported them; T-005 owns observed role compliance.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / IF-003 / INV-008 | Four distinct confirmed blockers; non-material preference; complete bounded inspection versus genuine interrupted coverage | Each blocker is independently observable in supplied changed production; report contract cannot truncate at three or stop merely on verdict sufficiency | Fail-first policy checks plus runnable fixture with four locations/consequences, non-blocking control and legitimate policy/gate inputs | Trace the fourth blocker and verify it is distinct; audit interrupted coverage reason against scope/budget | .2 implementer: local contract/setup checks; T-005: actual complete/partial reporting |

## Verification

- Targeted changed tests first, then the owning focused module:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py`
  if created; preflight resolves any existing equivalent owner first.
- Exercise setup in a disposable Git workspace with actual changed bytes and
  inspect every blocker/control. Text/eval metadata assertions are structural
  evidence only. Live agent evals require separate authorization and stay unrun.
- .4 owns composed guide/installer checks; no repository-wide gate here.

## Expected contract impact

- Change ART-005 / IF-003 completeness; preserve bounded review and contextual
  materiality. T-002 downstream ledgers remain consumers of the complete set.
- No current `docs/contracts` registry; no registry foundation work.
- Delta: removal of arbitrary truncation/early stop, with reusable four-blocker
  qualification inputs. Installer package projection must include task-owned setup.

## Stops and handoff

Stop for missing authority, user-work overlap, unsafe scope/permissions or a
decisive capability requiring shared infrastructure. Budget is soft.
Next: derived verification → ready standalone preflight → bounded implementation.
Required follow-on: immediately after implementation or correction, hand completed
bytes to a fresh independent acceptance reviewer through applicable conditional
stages and fresh discovery. End the implementer invocation. Supply .4/T-005
with exact fixture inputs, independent defect oracles and explicit unrun gaps.
