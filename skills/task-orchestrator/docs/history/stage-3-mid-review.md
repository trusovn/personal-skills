Verdict: `CHANGES REQUESTED` to the remaining Stage 3 plan. Your instinct is right: the project has produced a strong mechanical-control foundation, but it is overengineered relative to the original unattended task-flow goal—and it still does not automate the repetitive review/fix loop you described.

## What exists now

The controller has solid foundations:

- Immutable policy/manifest inputs and deterministic task selection.
- Single-worktree ownership with a local process lock and ledger revisions.
- Bounded Codex worker launch and durable attempt evidence.
- Independent Git inspection instead of trusting worker claims.
- Sandboxed, shell-free verification with timeout/process cleanup.
- Replay-aware verification and mechanical closure decisions.

The responsibility split—state, Git observation, verification, transport—is sensible and worth keeping. It directly addresses the concrete failures that motivated the redesign in [direction.md](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/docs/direction.md:8).

But the public controller currently exposes only `init`, `run-next`, and `inspect` ([controller.py](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/scripts/controller.py:1076)).

| Desired workflow | Current state |
|---|---|
| Feed it a planning document | Not supported; policy and normalized JSON manifest must be prepared manually |
| Preflight each task | Not integrated as an agent phase |
| Implement task | Implemented by `run-next` |
| Run mechanical checks | Implemented by `inspect` |
| Semantic review finding A/B/C | Not implemented; explicitly `semantic_review: not_collected` |
| Resume worker to fix findings | Planned in S3-09/S3-10 |
| Accept task and release dependencies | Planned in S3-11/S3-12 |
| Continue unattended | Explicitly deferred to a future supervisor/interface |
| Commit accepted work | Planned through four additional tasks |

Even the current two-task test manually fabricates the acceptance transition before launching task two; it is not an end-to-end controller flow ([test_controller.py](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/tests/test_controller.py:1332)).

## Main findings

### 1. S3-08 is not actually complete

Its own result has `CHANGES_REQUESTED`: modifying the immutable attempt record’s `model` field still allows verification execution ([S3-08-result.md](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/docs/stage-3-tasks/S3-08-result.md:105)).

The root is visible in `validate_attempt_record()`: it checks only that required fields exist, not exact shape, types, or values ([controller_state.py](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/scripts/controller_state.py:659)).

This blocks S3-11 under the existing dependency contract. S3-08 needs a bounded correction and fresh acceptance review before downstream acceptance work.

### 2. Mechanical acceptance is being confused with task acceptance

Stage 3 deliberately performs no semantic review ([stage-3-plan.md](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/docs/stage-3-plan.md:48)), yet a clean mechanical decision is represented as `accepted: true` and offers `accept`.

That is too strong a name. Passing commands and remaining inside allowed paths does not show that the implementation satisfies the task. Your current manual “review finds issues A/B/C” phase is exactly the missing semantic layer.

Until a reviewer exists, the result should mean `mechanically_eligible`, not accepted.

### 3. The architecture is robust for a narrower purpose than yours

It is reasonably robust for:

> “Execute one tightly scoped task on one trusted Mac, preserve evidence, prevent overlapping workers, and independently run predefined commands.”

It is not yet robust for:

> “Take a plan document and independently work through preflight → implementation → review → corrections → acceptance → next task.”

The missing pieces are not minor UX polish; they are the actual orchestration loop.

### 4. Complexity is growing faster than demonstrated value

Since the Stage 2 boundary, roughly 3.1k production lines and 4.2k test lines were added. `controller.py`, previously described as approximately 691 lines, is now about 1,450. S3-08 alone added 631 production and 719 test lines.

The correction history—S3-03A/B, S3-04A, several S3-08 review corrections, and a remaining gap after 157 tests—shows that the assurance protocol is itself becoming a major defect surface.

Some of that complexity is justified. The process ownership, independent Git evidence, and same-thread recovery contracts are valuable. The cryptographic-style record chain and multi-step commit finalization are much harder to justify before a usable pilot.

### 5. S3-11/S3-12 are overbuilt for commit/tracker mode off

S3-11 proposes an immutable prepared operation, a `finalizing` state, and an effects-complete record when both optional side effects are explicitly off ([S3-11](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/docs/stage-3-tasks/S3-11-acceptance-operation.md:9)). S3-12 then performs the actual atomic ledger acceptance and later completes the operation ([S3-12](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/docs/stage-3-tasks/S3-12-release-dependencies.md:9)).

With no commit or tracker effect, the atomic ledger write is the transaction. The operation journal is solving a problem that does not yet exist.

## Recommended rebaseline

1. **Correct S3-08 first.** Strictly validate the full attempt record and bind its exact bytes or canonical digest to independently persisted evidence. Then rerun acceptance review.

2. **Keep S3-09 and S3-10.** Safe recovery and same-thread resume directly serve your repetitive correction workflow.

3. **Add the missing semantic-review loop before acceptance.** A read-only reviewer should return `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`. Task-local findings can automatically become the resume prompt; architecture/product findings escalate to you.

4. **Collapse S3-11/S3-12 for the MVP.** For commit/tracker mode off, one `accept` command should revalidate evidence and atomically accept/release dependencies. Reserve the prepared-operation protocol for actual external side effects.

5. **Move a pilot forward.** Before exact-path commit work, prove this sequence:

   `plan/manifest → implement → mechanical inspect → semantic review → resume with findings → review again → accept → next task`

   Use one synthetic two-task run with an injected review failure, then one real task. Measure operator interventions, false stops, elapsed time, and context/token cost.

6. **Defer S3-13A/B, S3-14, and S3-15.** Exact-path commit construction, compare-and-swap publication, and interrupted finalization recovery are optional operational hardening. They are not required to prove the orchestrator’s core value.

7. **Bring part of Stage 4 forward.** The current [SKILL.md](/Users/mtrusov/work/skill-sources/personal-skills/skills/task-orchestrator/SKILL.md:13) still describes the old prompt-driven/manual flow. Add a thin `advance`/supervisor loop and explicit plan-to-manifest normalization before calling the system usable.

8. **State the threat model plainly.** For the personal MVP, treat the external run directory as trusted and use hashes for corruption/stale-evidence detection. If malicious tamper resistance is genuinely required, the ledger itself needs an external trust anchor; more internal digest links alone will not provide that guarantee.

## Bottom line

Do not discard the controller. Its core boundaries are good. But stop building assurance infrastructure ahead of the user workflow.

I would preserve:

- Sequential single-worktree ownership.
- Immutable policy and manifest.
- Worker commit prohibition.
- Process cleanup and same-thread resume.
- Independent Git/status inspection.
- Independent targeted verification.
- Explicit escalation boundaries.

I would defer or simplify:

- Multi-stage mode-off finalization.
- Exact-path commit machinery.
- Tracker integration.
- Further dependency-installer rule expansion.
- Additional identity-chain fields not tied to a demonstrated crash/recovery failure.

Verification performed: 36 state tests and 59 controller tests passed. The broader host-sensitive sandbox suite was not rerun. No files were changed; the pre-existing untracked `.gitignore` remains untouched.