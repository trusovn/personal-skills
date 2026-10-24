# Task Brief: T-001 — Distribute usable measurement tooling

## Outcome

An installed command captures a separate repository's actual starting Python
code, compares a later edit, and preserves source bytes and the real Git index.
The command works without this source checkout. This is the first useful proof
in [the project plan](../../project-plan.md#product-outcome). It gives T-002 a
usable measurement interface for preflight capture.

## Child outcomes and sequence

| Child | Outcome / owned output | Depends on | Brief |
|---|---|---|---|
| T-001.1 | Portable installed runtime, target settings and explicit setup | None | [Runtime brief](../T-001.1/brief.md) |
| T-001.2 | Neutral versioned reports and valid empty-folder baselines | T-001.1 | [Report brief](../T-001.2/brief.md) |
| T-001.3 | Foundation discovery guidance and complete installed composition proof | T-001.1, T-001.2 | [Integration brief](../T-001.3/brief.md) |

Runtime distribution must precede report changes so one child owns relocation,
resource resolution and installer membership together. Report semantics then
have their own observable boundary. The final child connects the documented
foundation discovery route to the installed command and proves the combined
result. Work is serial because the children share the adapter, tests and guide.

## Authority and scope

- Authority: [project plan](../../project-plan.md), sections 1–2, 4–8,
  T-001 in section 10, V-001/V-002/V-003/V-008 in section 11, and delegated
  choices in section 12; [task map](../../task-map.json), T-001.
- Reviewed baseline: plan version `2026-10-24 / 1`; plan SHA-256
  `9856d3ccfffcd56b4faed20dcf6ea4b49d87c4553292a5ed996cb4e784ca0df7`;
  task-map SHA-256
  `952f094d08ad03c5f5dfe18674fdbd710e8851fc8eaff1bdddc6facec2a5c954`.
  [Independent plan review](../../project-plan-review.md) accepts these bytes.
  The plan's retained `READY_FOR_PLAN_VERIFICATION` label is not a new review gap.
- Stable refs: CAP-001/CAP-005; FLOW-001 and the measurement boundary of
  FLOW-002; ART-001/ART-006/ART-007; IF-001/IF-004;
  INV-001/INV-002/INV-003/INV-006/INV-007/INV-009.
- Original scope: shared runtime/defaults/pins, target settings/setup, neutral
  output, empty folder baseline, installer maintenance, minimal foundation
  discovery guidance, local evidence and implemented-contract handoff.
- Out of scope: T-002–T-005 skill-flow behavior, controller changes, new analyzers,
  generic resource/check runners, mandatory registries, automatic refactoring,
  new hard metric gates, and live agent evaluation.
- Governing direction: the owner-confirmed policy persisted in plan section 1
  and its sections 5–7. Metrics remain advisory; native checks retain their
  authority. No new direction decision is required.

## Coverage and closure

| Parent obligation | Owning child |
|---|---|
| Installation-local runtime, default resources, target precedence, setup and dependency pins | T-001.1 |
| Installer selections/profile guide/README and path relocation map | T-001.1; T-001.3 updates only additions from its own guidance |
| Neutral JSON/text labels, incompatible old reports and empty-start capture | T-001.2 |
| Existing native metrics, dirty snapshots, affected added/deleted files, source/index and report preservation | T-001.1 preserves; T-001.2 extends capture; T-001.3 proves installed composition |
| Foundation discovery, native policy separation, bootstrap/readiness conflict inspection | T-001.3 |
| Real installed CLI, unrelated cwd, source independence, settings/format failures and target preservation | T-001.1 targeted proof; T-001.3 combined acceptance proof |
| Current contract records and installation references | Each child's designated registry stage, limited to its implemented delta |

ART-001/IF-001 runtime and installation ownership belongs to T-001.1; T-001.2
owns its report-format and empty-baseline extensions. T-001.3 owns final
ART-006 composition evidence and ART-007/IF-004 discovery guidance. T-002 owns
the later preflight handoff; these briefs do not implement it.

All parent acceptance obligations close through the three executable leaves,
including T-001.3's integration proof. Each leaf follows its own preparation and
review route. T-001.1 carries a permitted sizing override; the other leaves fit.

## Execution and handoff

Status: `decomposed`
Task kind: `composite`

This parent is not an implementation target. Start preparation with T-001.1.
Do not update the official plan, task map or existing plan review to track work.

### Execution sizing

- Sizing policy: `default@1`, from the active project-local skill's
  `references/task-sizing.yaml`.
- Original estimate: 38 agent calls; 100 implementation minutes.
- Original execution profile: `standard` / `high`.
- Estimate confidence: medium.
- Triggered rules: `max_agent_calls` and `max_duration_minutes`.
- Boundary decision: split runtime distribution, report behavior, and final
  foundation/integration closure. Each produces a concrete interface or evidence
  consumed by the next; no child exists solely to write another child's tests.
