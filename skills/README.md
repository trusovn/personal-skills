# Development skills

This guide describes the project-local development profile installed by
`scripts/install_development_skills.py`. Invoke a skill by name when its stage
or specialty is needed; optional stages should not be called only because they
are available. Installation also works in a target repository that has no
commit yet: installed workflow identity and the availability check explicitly
represent that unborn state without creating a commit.

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
                                        (human or authorized AI coordinator, before advancement)
```

Use `senior-code-review`, `ollama-delegate`, `testing-discipline`, and
`session-handoff` on demand rather than as mandatory stages in either flow.

To understand intended work and progress, read the project plan's opening,
then the current implementation result or acceptance report. See the
[implementation output contract](task-implementation-flow/bounded-task-implementer/SKILL.md#output-contract)
and [acceptance output contract](task-implementation-flow/task-acceptance-review/SKILL.md#output-contract)
for their different evidence and decision roles.

A required-review submission names the first outstanding applicable stage and
the complete ordered remainder: the architecture gate only when policy requires
it, fresh maintainability review when applicable, the contract-registry
updater when applicable, then fresh discovery evidence and the separate fresh
acceptance decision. A conditional stage counts only with evidence current for
the submitted bytes; implementation corrections, including tests-only corrections,
re-enter the stages they affected before fresh discovery and acceptance.

Significant changed tests, evaluations, fixtures and harness code are a risk
reason for the existing conditional maintainability review. Significance follows
ownership, dependencies, scenario authority, isolation, oracle structure or
harness behavior. An ordinary assertion edit alone does not require this review;
a tests-only label never waives an affected required review.

## Checking the installed profile

The profile also installs the portable measurement runtime under `.agents/scripts/`:
`measure_maintainability.py`, `maintainability.py`, `maintainability_env.py`,
`maintainability-default.toml`, `maintainability-ruff-default.toml`, and
`maintainability-requirements.txt`. These are explicit managed files, alongside
the existing workflow/evidence and Ollama helpers. Setup selects the measured
repository with `setup --root <target>` and uses installation-owned pins.
Each target `.quality/maintainability.toml` and `.quality/ruff.toml` independently
replaces its shipped default when present; invalid settings fail. Refresh preserves
target policy, environments/reports and unmanaged helpers. Measurement does not
install dependencies or replace native hard checks. The source repository's
`scripts/measure-maintainability.md` documents the public interface.

The installer also supports a read-only `--check` comparison of the installed
profile with its canonical source:

```bash
python3 /path/to/personal-skills/scripts/install_development_skills.py \
  --check /path/to/this-repository
```

The check compares every file in each selected skill package (references,
evals, and setup files included), the installed profile guide, every
explicitly managed shared script/config/schema, and the marked `AGENTS.md`
block, using the same transient exclusions as installation. Source-side
enumeration follows directory symlinks exactly as install-time copying
does, so content linked into a selected source package is compared like any
other file the installer copies; installed trees are never traversed
through inner symlinks. Acyclic directory aliases — several links to one
directory, or a link to an existing sibling directory — are copied by the
installer and therefore compared at every linked path; only a link that
closes a directory cycle back to one of its own ancestors fails with
`cannot enumerate source skill directory: <path>: directory cycle` and
exit 2. Unmanaged bytes —
unselected skills, non-selected scripts, other `.agents` content, and
`AGENTS.md` text outside the marked block — never cause drift. It never
installs, stages copies, refreshes, writes files or Git metadata, or starts an
evidence run.

It prints one JSON object with `match`, `compared_paths`, and the changed,
missing, and unexpected managed paths in `differences`: exit 0 means the
managed projection matches, exit 1 means managed drift (including a missing
installation), and exit 2 means the check itself failed — unusable source or
target, required content that cannot be read or whose directory cannot be
enumerated, or malformed/ambiguous `AGENTS.md` markers — and a failure never
reports a match. Source is resolved relative to
the installer's own location, not the caller's working directory. The check
compares only current bytes and retains no versions: refresh deliberately by
rerunning the installer between check invocations.

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
| `task-maintainability-review` | Independently reviews changed implementation assets, including significant tests/evals/fixtures/harness code, for concrete architecture and maintainability regressions. | The task authority, current diff, repository rules, and architecture gate; use a fresh reviewer. | `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`, with focused findings. |
| `task-contract-registry-updater` | Synchronizes discoverable current-state contracts after implementation. | Task authority, scoped diff, task-map entry when present, and existing contract records. | Updated contract registry/discovery references and a synchronization result. |
| `task-acceptance-review` | Decides a bounded implementation against its contract by admitting the current independent discovery evidence and deciding every finding. | The request/brief, current diff, submission claims, the independent discovery report, and applicable conditional evidence; use a fresh reviewer. | `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`, with admitted coverage status and the consumed aggregate-gate record; accepted bounded deferrals are routed to the human or authorized AI coordinator for recording (default `docs/known-issues.md`, or the declared tracker/format) before advancement. AI recording needs no new human confirmation; requirement/proof waivers and unresolved material risk remain with the owner. |
| `task-review-discovery` | Independently publishes current evidence and confirmed findings for a bounded implementation as a complete or explicitly partial report, without deciding acceptance. | The request/brief, verification/context inputs, current diff, and submission claims; use a fresh session that did not author the reviewed bytes. | An evidence report with facts, suggested severities, coverage rows, an aggregate-gate record, and a continuation block for a separate acceptance decision call; no verdict. |
| `senior-code-review` | Performs a rigorous read-only merge-readiness review. | A PR, commit, branch range, working-tree diff, patch, or named files plus their intent. | Prioritized findings and a merge-readiness assessment. |
| `ollama-delegate` | Delegates a bounded read-only repository task to an Ollama-backed cloud model using another installed skill. | Ollama HTTP access, a configured model alias, the target repository, and a selected installed skill. | The delegated model's final report plus bounded tool-call metadata. |
| `testing-discipline` | Designs, adds, or reviews the smallest risk-based test evidence that proves behavior. | The behavior contract, relevant code/tests, and repository test conventions. | Tests and verification evidence, or a focused test strategy/review when requested. |
| `session-handoff` | Preserves actionable context so work can continue in a new session. | The current goal, decisions, changed files, commands, results, and open issues. | A copy/paste-ready handoff packet and, when useful, a companion Markdown file. |
