# Idea Brief: Post-project documentation cleanup

## Status

- Source: owner discussion in this Codex session, 2026-10-14.
- Output: `ideas/documentation-consolidation.brief.md`.
- Depth: standard; the discussion already supplies most of the scope and intent.
- Created: 2026-10-14.
- Downstream target: a bounded cleanup task after a focused dependency audit.
- This brief records direction. No archive, deletion, rebase, or dependency migration has been performed.

## Raw Idea

The owner stated:

> основна проблема - я хочу звільнити docs для майбутніх робочих документів.

> зараз я хочу прибрати зайве без втрати архівних даних.

The confirmed scope is tasks, project-plan, and task-map. Keep future-tasks in the active repository. The owner wants completed working documents available for possible future use, without keeping them in the main branch's working tree. The owner also prefers to clean the noisy development commit history before merging.

The initial proposal included a knowledge wiki, documentation lifecycle rules, and simpler planning artifacts. Later discussion narrowed the current work to cleanup. Those broader ideas remain candidates for later work, not current decisions. The owner described existing documents as mostly written by agents for agents; cleanup removes clutter but does not resolve that separate readability problem.

The owner supplied additional wiki discussion in the chat. Its claims about LLM Wiki and the current implementation were not independently verified for this brief. The shared ChatGPT conversation could not be fetched; the pasted material is the available source.

## One-Paragraph Vision

Retire completed delivery documents from the active repository tree while preserving their original content and repository context in a Git archive. Leave room in `docs/` for the next delivery cycle, keep future work visible, and retain a small route to historical evidence. The cleanup should preserve skill behavior and executable assets without redesigning documentation or task workflows.

## Problem And Context

- Problem: completed task details occupy the space intended for current working documents.
- Trigger: the owner wants to clean up after the delivery cycle and prepare for future work.
- Current alternative: keep all historical artifacts beside active documents and rely on readers to distinguish them.
- Why now: that alternative adds noise and makes reuse of the delivery document paths harder.
- Evidence boundary: task completion, verdicts, qualification gaps, and live dependencies have not been audited in this session.

## Users And Stakeholders

| Group | Goal | Friction Today |
| --- | --- | --- |
| Repository owner | Keep a clean workspace and recover history if needed | Too much completed working detail remains active |
| Future agents | Find current work without confusing it with old tasks | Historical task artifacts share the delivery space |
| Maintainers and reviewers | Preserve tests, evidence, and source context | Retirement may break dependencies or historical references |

## Desired Outcomes

- Primary outcome: completed delivery packages no longer occupy the active documentation tree.
- Secondary outcomes: original evidence remains recoverable; future-tasks remains useful; skill and test assets remain available.
- Success signals: new work can reuse the delivery paths, historical documents have a stable archive reference, and active consumers do not depend on retired files.
- Non-goals: rewrite historical evidence, improve all documentation, build a wiki, or redesign planning and review workflows.

## Scope Sketch

### First Useful Version

- Archive the completed material under `docs/tasks/`, plus `docs/project-plan.md` and `docs/task-map.json`, then retire it from the active tree.
- Preserve original statuses, findings, reviews, and results without rewriting them.
- Keep future-tasks active. Repair any references it needs to retired material.
- Retain test inputs or other executable dependencies in suitable owned locations if the audit finds them.
- Leave a short archive pointer in existing active navigation; do not create a documentation system for this purpose.

### Explicitly Out Of Scope

- A knowledge wiki or wiki engine.
- Refactoring skills, templates, or normative contracts for readability or less duplication.
- Changing where future planning artifacts are created.
- Rewriting historical reports as summaries or retroactively changing verdicts.
- Broad cleanup of documents outside the named scope.
- Closing historical qualification gaps as part of retirement.

### Boundary Notes

- Preferred archive approach: a tag pointing to the full repository snapshot before cleanup and before any history rewrite. This preserves document context as well as files.
- Record the tag and exact commit SHA. A tag can be moved, so treat the archive tag as fixed by convention.
- The owner prefers a clean merge history. Rebase changes IDs of rewritten commits; a tag on the original commit preserves access to the original history independently of the development branch.
- Ordinary rebase does not reduce commit count. Interactive rebase with squash/fixup or squash merge are possible later choices; no Git history operation is authorized by this brief alone.
- Archival means removal from the current tree, not erasure from Git history.
- If extracting dependencies requires substantial behavior changes, separate that implementation from documentation retirement.

## Scenario Map

| Scenario Type | Scenario | Why It Matters |
| --- | --- | --- |
| Happy path | Completed delivery artifacts are archived and removed; a new cycle uses the same paths | Frees the intended workspace |
| Edge case | future-tasks links to a retired finding or brief | Keep the backlog usable through an archive reference and only essential local context |
| Failure path | A live test or script reads a retired task artifact | Retirement could break verification or silently weaken its setup |
| Bad input | The archive omits modified, untracked, or ignored evidence that the owner expects to retain | A tag preserves committed content only |
| Operational | The development branch is deleted after rebase or squash | The original archive remains reachable through its tag, even if absent from main's ancestry |
| Recovery | A fresh checkout needs an old report or fixture | The archive must be available beyond one local clone |
| Later correction | A historical finding becomes the basis for new work | New work links to original evidence rather than modifying it |

## Critical Assumptions

| Assumption | Why It Matters | How To Validate | If False |
| --- | --- | --- | --- |
| The named artifacts belong to completed work | Their retirement must not hide an active obligation | Inspect current statuses and unresolved work | Identify active items before retirement |
| The archive can include all intended historical data | No-loss preservation is the owner's main constraint | Inspect tracked and uncommitted state, including relevant ignored assets | Agree what to include before making the snapshot |
| Live dependencies can be retained without redesign | Keeps cleanup bounded | Inspect consumers and existing test setup | Split dependency changes into separate work |
| Keeping future-tasks is enough to preserve pending work | The backlog must survive retirement | Inspect its references and dependence on old context | Add only the missing context or archive links |

## Risk Register

| Risk | Likely Consequence | Early Signal | Mitigation Or Next Check |
| --- | --- | --- | --- |
| Archive created after history rewriting or deletion | Original history or content becomes harder to recover | No fixed reference to the original state | Preserve the original snapshot first |
| Archive exists only locally | A lost clone or fresh checkout cannot recover it reliably | Tag absent from the intended remote | Choose archive destination and verify availability |
| Fixture extraction loses setup or assertions | Passing tests no longer establish the same behavior | Changed inputs or weaker checks | Compare existing behavioral coverage during extraction |
| Historical links resolve against new delivery files | Old evidence appears to support unrelated current work | Relative links reuse task paths | Use the archive commit for historical references |
| Retirement is mistaken for qualification | Readers infer gaps were closed | Archive pointer omits known limits | Preserve verdicts and unresolved gaps in archive metadata |
| Wiki or workflow redesign enters the cleanup | A small retirement task becomes a wider project | New templates, workflow rules, or knowledge pages appear | Keep these as separate future ideas |

## Architecture-Affecting Unknowns

These are boundaries to inspect, not new architecture decisions.

- Source of truth: whether any named artifact still owns a live contract or required input.
- Data lifecycle: the full set of historical files that must be committed before retirement.
- External dependencies: whether tests or scripts load files from the retired paths.
- Audit: how original verdicts and known qualification limits are exposed by the archive pointer.
- Collaboration and recovery: which remote retains the tag and how a fresh clone retrieves it.
- Cost: whether dependency extraction remains a small cleanup or requires separate implementation.
- Permissions: archive publication and history rewriting need an explicit execution decision; this brief does not perform either.

## Open Questions

| Question | Why It Matters | Blocks Or Influences | Owner | Due |
| --- | --- | --- | --- | --- |
| Which exact files and uncommitted assets belong to the snapshot? | Prevents incomplete preservation | Archive creation and deletion scope | Cleanup implementer; owner resolves ambiguity | Before archival |
| What archive tag, remote destination, and existing navigation location should be used? | Makes recovery stable and discoverable | Archive publication and pointer | Owner and cleanup implementer | Before archival |
| Which active consumers depend on the named documents? | Prevents broken or weaker verification | Safe retirement and task size | Cleanup implementer | Before retirement |
| Which pending obligations need to remain visible outside the archive? | Avoids hiding live work or qualification limits | future-tasks and archive pointer | Cleanup implementer; owner confirms disposition | Before retirement |
| Which history-cleaning method fits the current branch and its users? | Rebasing shared history may affect collaborators | Later merge preparation; not initial discovery | Owner | Before history rewrite |

## Planning Handoff

- Recommended next step: focused local dependency and preservation discovery, followed by a bounded cleanup task.
- Rationale: the desired result is settled, but deletion scope and executable dependencies still need repository evidence. A new master plan or wiki is unnecessary.
- Suggested task slug: `documentation-consolidation`.
- Verification direction: establish that the archive contains every retired file, check active references, and run the narrow relevant local behavioral tests if dependencies change. Syntax or link checks alone do not prove preserved behavior.

### Seed For Next Planning Step

Clean up completed delivery documentation in personal-skills so future work can reuse `docs/`. Retire the completed task packages, project-plan, and task-map from the active tree while keeping future-tasks. Preserve their original contents and repository context under a fixed archive tag before cleanup or any rebase, and leave a short archive pointer. Inspect uncommitted data and active consumers first; retain executable assets and repair current references without rewriting historical evidence. Keep wiki development, planning-document redesign, skill refactoring, and closure of old qualification gaps outside this task. The owner prefers a clean merge history, with the original history retained separately through the archive tag.
