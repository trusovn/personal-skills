---
name: foundation-readiness-review
description: >
  Use after repo-level foundation changes are materialized and BEFORE detailed product planning or
  implementation. Independently verify that an unfamiliar agent can navigate, bootstrap, run, test,
  inspect failures, and follow repo rules from persisted artifacts. Also recommend the cheapest safe
  next delivery route: PERSONAL_FLOW, SDD_QUICK, SDD_STANDARD, or SDD_FULL. Produces
  docs/foundation-review.md. Do not review product functionality here.
---
# Foundation Readiness Review

Perform a clean-context review of the project foundation.

The question is:

> Can another capable coding agent enter this repository now and plan/implement the product without
> rediscovering the environment or relying on this conversation?

This review evaluates the **engineering substrate**, not product completeness.
## Inputs

Read:

- `docs/project-charter.md`
- `docs/foundation-plan.md`
- repo-local `AGENTS.md` / `CLAUDE.md` / `README.md`
- project/architecture map
- relevant ADRs
- build/package/CI configuration
- `.quality/gates.yaml` or an equivalent gate registry when present
- architecture-policy configuration/tests when the foundation claims maintainability guardrails
- `docs/ai-foundation.md` when present

Inspect the actual repo state and git diff/status.

## Output

Create:

- `docs/foundation-review.md`

Verdict:

- `READY`
- `READY_WITH_NOTES`
- `BLOCKED`

Also emit one delivery-route recommendation:

- `PERSONAL_FLOW`
- `SDD_QUICK`
- `SDD_STANDARD`
- `SDD_FULL`
## Protocol
### 1. Assume zero conversation memory

Do not rely on prior chat decisions unless they are persisted in the repo.

Try to determine from the repo alone:
1. what the project is
2. what the current scaffold already provides
3. how to install/bootstrap it
4. how to run it
5. how to run the narrowest meaningful check
6. how to run the normal/full verification gate
7. where new product code/tests/tools/docs belong
8. what must not be modified
9. where architecture decisions and constraints live
10. how to diagnose a failed run/test
11. whether a canonical architecture/maintainability gate is required and how to run it
12. whether hard architecture rules, advisory signals, and legacy exceptions are distinguishable

For an AI-heavy project also determine:
13. where provider/model calls are isolated
14. how tests substitute deterministic model output
15. where output validation occurs
16. how model-dependent quality is evaluated, if required
17. what trace/log data exists for AI failures
### 2. Execute the documented commands

Actually run the commands that foundation claims are canonical, subject to project safety constraints.

At minimum, where applicable:

- bootstrap/install sanity
- build/typecheck
- focused or smoke test
- normal/full test/verify
- lint/static check
- architecture/maintainability gate
- run/boot smoke
- migration apply/revert smoke
- AI boundary fake/fixture test
- eval smoke if an eval runner is claimed

A documented command that does not work is a blocker until corrected or explicitly marked unavailable with a valid reason.

If the repo claims required maintainability/architecture guardrails:

- verify the canonical command runs against the current tree
- verify its policy location and `clean` / no-regression mode are discoverable
- verify hard failures are distinct from advisory warnings/signals
- if semantic maintainability review is declared required, verify `task-maintainability-review` or the repo's explicit equivalent is actually available to the delivery flow
- verify any legacy baseline/exceptions are explicit and narrow enough that feature work cannot silently expand them
- require evidence that at least one representative hard rule was proven capable of failing during materialization; if that evidence is absent, safely prove the sentinel only in a disposable fixture/worktree when feasible, never by risking unrelated user work
- after any sentinel exercise, verify the repo returns to the intended clean state and the canonical gate passes

A gate that is documented but cannot be shown to reject a representative prohibited case is not trustworthy merely because it exits zero on the current tree.
### 3. Check agent legibility

Fail or note problems when:
- the only way to know a command is to infer it from package files
- two docs disagree on canonical commands
- `AGENTS.md` is a long duplicate of architecture docs instead of a router
- placement rules are absent where the repo has multiple plausible homes
- generated/editable files are not distinguished
- important constraints exist only in ephemeral chat/history
- architecture maps contain guessed or stale claims
- a required architecture gate exists but the agent-facing instructions do not name its canonical command
- maintainability policy is expressed only as abstract doctrine such as "follow SOLID" with no repo-specific executable invariant or focused review contract
- foundation created empty/unused abstractions that increase search space
### 4. Check verification quality

Foundation verification should be:

- executable
- local where practical
- deterministic for deterministic behavior
- narrow enough for fast iteration
- broad enough to catch structural breakage before handoff

For architecture/maintainability enforcement, also check:

- deterministic hard rules have low enough ambiguity to block safely
- heuristic metrics such as size, complexity, fan-out, or naming are warnings/reviewer evidence unless the project explicitly has a justified hard threshold
- no-regression baselines preserve existing debt without permitting new or worsened violations
- baseline refresh is a deliberate foundation/architecture change, not a normal feature-work escape hatch

Do not require heavyweight infrastructure merely to improve a checklist score.
### 5. Check AI foundation when applicable

Block on material issues such as:

- domain/business code coupled directly to provider SDK with no test seam
- raw model output used for side effects without validation
- ordinary tests requiring a live model/provider
- retries capable of duplicating side effects with no idempotency semantics
- no way to distinguish provider failure from parse/validation failure

Do not block merely because a prompt, model, or final eval dataset has not yet been designed;
those may properly belong to feature design.
### 6. Determine the cheapest safe delivery route

Use `references/delivery-routing.md`.

Default to `PERSONAL_FLOW`.

Escalate only when the cost buys real risk reduction.

When the repo requires maintainability review, preserve that gate inside whichever bounded delivery route is selected; do not treat it as a reason by itself to escalate to SDD.
### 7. Write the review

Use `templates/foundation-review.md`.

Every blocker must include:

- evidence
- why it blocks downstream work
- smallest repair
- verification after repair

Do not generate speculative improvements.
## Definition of Done

- Canonical commands were actually exercised where feasible.
- Another agent can navigate the repo from persisted artifacts.
- Foundation docs and real repo state agree.
- If maintainability guardrails are claimed, the architecture gate runs, its policy/mode is discoverable, hard failures are distinguishable from warnings, representative failure capability has evidence where feasible, and any required semantic-review entry point is available.
- Any AI boundary is independently testable without a live model for deterministic cases.
- Blockers are concrete and minimal.
- A next delivery route is recommended with explicit reasons.
- No product feature review or detailed task planning was performed.
## Anti-patterns

- Rating the foundation by document count.
- Recommending full SDD simply because the project is important.
- Treating every uncertainty as a blocker.
- Trusting a never-negative architecture gate without any evidence that a hard rule can actually fail.
- Turning advisory maintainability metrics into arbitrary universal failure thresholds.
- Running expensive full integration checks when a documented external dependency makes them impossible.
- Turning the readiness review into a product architecture review.
- Using `SDD_FULL` as a prestige/default choice.


<!-- contract-registry-flow:foundation-readiness-review:begin -->
## Implemented-contract discovery readiness

When the foundation requires a contract registry, independently verify that a zero-context agent can:

- discover the canonical current-state contract entry point from repository instructions;
- find an existing reusable contract without reconstructing the subsystem from source;
- resolve a materialized stable plan ID to the owning subsystem where such IDs exist;
- follow a registry record to real module/executable declaration paths;
- distinguish planned/future contracts from currently implemented contracts;
- run the canonical registry validator successfully.

Treat missing, stale, or ambiguous discovery foundation as a readiness defect rather than relying on later task agents to compensate through broad repository exploration.
<!-- contract-registry-flow:foundation-readiness-review:end -->
