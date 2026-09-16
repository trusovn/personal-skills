# Foundation Plan

## Baseline
- Runtime/build:
- Existing run command:
- Existing focused verification:
- Existing full verification:
- Existing architecture/maintainability gate:
- Existing repo instructions/maps:
- Existing CI:
- Config/state:
- Development diagnostics:
- AI in data/process flow: yes / no / unknown

## Capability decisions

| Capability | Status | Evidence | Minimum change | Verification |
|---|---|---|---|---|
| Bootstrap/runtime | REUSE/REPAIR/ADD/DEFER/N/A | | | |
| Verification | | | | |
| Repo navigation | | | | |
| Development diagnostics | | | | |
| Configuration/state | | | | |
| Automation/CI | | | | |
| AI foundation | | | | |
| Maintainability / architecture guardrails | | | | |

## Authorized foundation changes
1. <bounded change>
   - Why before product planning:
   - Files:
   - DoD:
   - Reversible: yes/no

## Explicitly deferred
- <product/design concern not needed for foundation>

## Materialization handoff
Read:
- `docs/project-charter.md`
- `docs/foundation-plan.md`

Use:
- `repo-foundation`
- `architecture-guardrails` through `repo-foundation` when maintainability / architecture guardrails are `ADD` or `REPAIR`

Do not:
- implement product features
- broaden architecture beyond the authorized foundation
- guess unresolved values
