# Development skills

This guide describes the project-local development profile installed by
`scripts/install_development_skills.py`. Invoke a skill by name when its stage
or specialty is needed; optional stages should not be called only because they
are available.

## Recommended flow

For a new repository:

```text
project-direction
  -> project-bootstrap
  -> ai-flow-foundation                 (only when the product/runtime calls a model)
  -> repo-foundation
       + architecture-guardrails        (when the foundation plan requires them)
  -> foundation-readiness-review
  -> project-delivery-plan              (for a multi-task lightweight plan)
  -> project-plan-verification          (in a fresh reviewer session)
```

For one implementation task:

```text
task-brief-designer
  -> task-verification-designer         (required for an executable task package)
  -> task-preflight                     (required ready preflight for that package)
  -> bounded-task-implementer
  -> task-maintainability-review        (when policy or risk requires it; fresh reviewer)
  -> task-contract-registry-updater     (when durable cross-task contracts changed)
  -> task-review-discovery              (fresh session; publishes the evidence acceptance admits)
  -> task-acceptance-review             (when policy or risk requires it; fresh reviewer;
                                        consumes the discovery report and decides)
  -> coordinator recording of approved deferrals
                                        (human coordinator alone, before authorized advancement)
```

Use `senior-code-review`, `ollama-delegate`, `testing-discipline`, and
`session-handoff` on demand rather than as mandatory stages in either flow.

## Skill reference

| Skill | What it does | Requires | Produces |
| --- | --- | --- | --- |
| `project-direction` | Sets owner-readable goals, priorities, scope, and boundaries. | A project objective, notes, or existing plans to extract/audit. | A direction document, normally `docs/direction-<name>.md`, or a direction delta. |
| `project-bootstrap` | Defines the minimum charter and engineering-foundation work before product planning. | A high-level objective and an existing repository or scaffold. | `docs/project-charter.md` and `docs/foundation-plan.md`. |
| `ai-flow-foundation` | Defines deterministic seams and safety boundaries for model-dependent product/runtime behavior; coding-agent maintenance alone does not trigger it. | The charter/foundation plan and the intended model role in the system flow. | `docs/ai-foundation.md`. |
| `repo-foundation` | Materializes the approved repository layout, commands, guidance, and foundation tooling. | The repository plus `docs/project-charter.md`, `docs/foundation-plan.md`, and `docs/ai-foundation.md` when applicable. | The planned repository foundation changes and their verification evidence. |
| `architecture-guardrails` | Adds or repairs deterministic dependency, boundary, or maintainability checks. | Explicit architecture invariants and the repository/tooling they govern. | A canonical architecture gate, its rules/configuration, and concise usage guidance. |
| `foundation-readiness-review` | Checks that a new agent can navigate, run, test, and safely change the repository. | The materialized foundation and its authoritative documents/commands. | `docs/foundation-review.md` with findings and the recommended delivery route. |
| `project-delivery-plan` | Maps end-to-end flows, artifacts, interfaces, invariants, and composing tasks. | A ready foundation, project authority, and applicable foundation artifacts. | `docs/project-plan.md` and `docs/task-map.json`. |
| `project-plan-verification` | Independently checks that the delivery plan is coherent and executable. | The project plan, task map, repository, and upstream authority; use a fresh reviewer. | `docs/project-plan-review.md` with `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`. |
| `task-brief-designer` | Turns one bounded request or plan item into an implementation-ready contract. | A user request, issue, approved plan item, specification, or existing brief. | A concise gap check or `<task-package>/brief.md`; oversized work may be decomposed. |
| `task-verification-designer` | Defines falsifiable verification scenarios before implementation. | An executable task `brief.md` with clear acceptance criteria. | Required derived `<task-package>/verification.md` before packaged implementation. |
| `task-preflight` | Confirms complete authority-derived coverage, feasible proof and current relevant facts. | A bounded request or executable packaged brief with source-matched verification, plus relevant recorded known issues for reassessment against the task's exposure and obligations. | Compact canonical `<task-package>/preflight.md` bound to brief/scope/verification revision, with decision context; inline for unpackaged direct edits. |
| `bounded-task-implementer` | Implements one bounded task with risk-based tests and progressive verification. | A clear bounded unpackaged request, or an executable package; the implementer verifies current applicable readiness (bound preflight and verification revision). High-assurance packets stay strict. | The scoped code/test/doc changes plus a verification and review handoff result; submission maps every verification scenario ID to current evidence or an explicit blocked/unchecked reason and next owner. |
| `task-maintainability-review` | Independently reviews changed production code for concrete architecture and maintainability regressions. | The task authority, current diff, repository rules, and architecture gate; use a fresh reviewer. | `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`, with focused findings. |
| `task-contract-registry-updater` | Synchronizes discoverable current-state contracts after implementation. | Task authority, scoped diff, task-map entry when present, and existing contract records. | Updated contract registry/discovery references and a synchronization result. |
| `task-acceptance-review` | Decides a bounded implementation against its contract by admitting the current independent discovery evidence and deciding every finding. | The request/brief, current diff, submission claims, the independent discovery report, and applicable conditional evidence; use a fresh reviewer. | `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`, with admitted coverage status and the consumed aggregate-gate record; accepted bounded deferrals are routed to the human coordinator, who alone records them (default `docs/known-issues.md`) before authorized advancement. |
| `task-review-discovery` | Independently publishes current evidence and confirmed findings for a bounded implementation as a complete or explicitly partial report, without deciding acceptance. | The request/brief, verification/context inputs, current diff, and submission claims; use a fresh session that did not author the reviewed bytes. | An evidence report with facts, suggested severities, coverage rows, an aggregate-gate record, and a continuation block for a separate acceptance decision call; no verdict. |
| `senior-code-review` | Performs a rigorous read-only merge-readiness review. | A PR, commit, branch range, working-tree diff, patch, or named files plus their intent. | Prioritized findings and a merge-readiness assessment. |
| `ollama-delegate` | Delegates a bounded read-only repository task to an Ollama-backed cloud model using another installed skill. | Ollama HTTP access, a configured model alias, the target repository, and a selected installed skill. | The delegated model's final report plus bounded tool-call metadata. |
| `testing-discipline` | Designs, adds, or reviews the smallest risk-based test evidence that proves behavior. | The behavior contract, relevant code/tests, and repository test conventions. | Tests and verification evidence, or a focused test strategy/review when requested. |
| `session-handoff` | Preserves actionable context so work can continue in a new session. | The current goal, decisions, changed files, commands, results, and open issues. | A copy/paste-ready handoff packet and, when useful, a companion Markdown file. |
