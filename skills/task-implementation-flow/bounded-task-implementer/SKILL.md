---
name: bounded-task-implementer
description: Implement one bounded task from a clear user request, ready task brief, or high-assurance preflight packet. Use whenever asked to execute, resume, or correct a scoped implementation and the agent should automatically define missing acceptance criteria, add risk-based tests, verify progressively, preserve user work, and report evidence. Default to a lightweight guided flow with a human-readable result; require strict freshness and raw JSON only when an orchestrated packet or machine output contract is supplied.
---

# Bounded Task Implementer

Implement one bounded outcome with enough evidence to trust it. Carry the
routine implementation discipline so the user does not need to repeat “define
ACs, add tests, verify, and report” on every task.

Repository and user instructions outrank this skill. Preserve pre-existing user
work and never claim ownership of it.

## Choose the profile

Use `guided` by default.

Use `high-assurance` when the user requests it or supplies a ready preflight
packet, worker-result schema, orchestrator invocation, or other machine
contract. If guided work discovers security, migration, destructive-state,
concurrency, multi-writer, or audit requirements that the current inputs cannot
safely support, pause and recommend the smallest escalation rather than
silently building the full artifact chain.

### Guided inputs

Require enough to identify the repository, bounded outcome, and authority. A
user request or `ready` task brief is sufficient when it makes the intended
behavior clear. A separate preflight packet, result schema, run directory, and
tracker are not required.

Use focused local discovery to resolve relevant paths, nearby tests, commands,
and current Git state. Ask only when a missing product, architecture,
compatibility, scope, ownership, or permission decision could materially change
the result.

### High-assurance inputs

Require:

- one fresh preflight packet with status `ready`;
- its referenced task brief and run policy;
- the supplied worker-result schema and durable result path; and
- for correction, the acceptance findings and prior checkpoint/result.

Missing or inconsistent high-assurance inputs return the schema-valid
non-complete result required by the caller. Do not downgrade silently to guided
mode.

## Guided workflow

1. Read applicable instructions and the task authority. State a brief
   verification plan before editing.
2. Perform a compact self-preflight:
   - inspect `git status --short` and preserve user-owned work;
   - identify the bounded change area and prohibited adjacent work;
   - inspect the relevant entry point, closest tests, and local conventions;
   - resolve the narrowest meaningful test command; and
   - confirm required permissions and dependencies.
3. If acceptance criteria are absent, derive the smallest observable set from
   the request and state them briefly. Include the positive behavior and the
   most credible failure, unchanged-state, compatibility, or lifecycle case.
   Do not invent a materially ambiguous requirement.
4. Choose the lowest reliable evidence:
   - reproduce a bug before fixing it when feasible;
   - for new behavior, add or update a focused test that could reject the old or
     faulty behavior;
   - cross the real boundary only where lower-level evidence cannot prove
     wiring, persistence, filesystem/database/process behavior, concurrency,
     recovery, authorization, or another material risk.
5. Implement the minimum code and test change. Match local style and do not
   create shared infrastructure, dependencies, or public contracts unless the
   task authorizes them.
6. Verify progressively: run the changed/targeted test first, then the nearest
   owning suite, then only the broader gate justified by blast radius. Ask
   before slow, flaky, privileged, destructive, live, networked, or otherwise
   expensive checks unless already authorized.
7. Inspect the final diff and status. Confirm every changed path belongs to the
   task, user work remains separable, and temporary artifacts created by this
   run are handled safely.
8. Return the guided human-readable result described below. Review is required
   when task metadata says `immediate`, the user requested it, or risk warrants
   independent corroboration.

## High-assurance additions

Before editing, recalculate every packet freshness field exactly: brief bytes,
`HEAD`, short status, separate index/worktree identities for dirty paths,
dependency/instruction/policy digests, and task-specific environment
fingerprints. Any unexplained mismatch routes to fresh `task-preflight`.

Treat the packet as the discovery and permission boundary:

- inspect and change only declared paths and cited context;
- establish the packet's highest-risk fail-first evidence;
- run its exact commands in order and record every attempted or required-but-
  skipped command truthfully;
- save logs and results only at authorized runtime paths; and
- validate the result against the supplied schema.

On a same-thread `CHANGES_REQUESTED` correction, preserve the bounded partial
diff and apply only in-scope findings. Changed contract, scope, helpers,
dependencies, permissions, or authority route through the owning earlier stage.

## Stops and budget behavior

Stop on ambiguous authority, user-work overlap, unsafe permissions, material
scope expansion, missing decisive capability, unexpected changed paths, or a
required check that cannot run within the authorized environment.

After two materially different fixes fail the same targeted behavior, stop
ordinary editing. Record the failure, discarded hypotheses, owning component or
contract, and one recommended next approach.

Treat the brief's tool/time/context budget as a soft checkpoint by default. At
the checkpoint, summarize progress and continue while the task remains bounded
and there is enough context to finish safely. Stop or hand off only when the
user/repository made the limit hard, continued work would cross authority, or a
context boundary prevents reliable completion.

## Output contract

### Guided or ordinary interactive invocation

Return a concise human-readable summary, not raw JSON:

```markdown
Implemented: <outcome or non-complete status>

- Changed: <paths or none>
- Verified: <exact commands and results>
- AC evidence: <concise mapping>
- Residual risks / skipped checks: <none or specifics>
- Next: <review, user decision, fresh preflight, or complete>
```

Omit empty bullets when prose is clearer. Link to created artifacts rather than
embedding their serialized contents.

### Machine-contracted invocation

When the caller explicitly supplies an output schema or requires a machine-only
response, return exactly one schema-conforming JSON object and no prose. When a
conversational caller asks for a JSON artifact at a path, write and validate the
artifact, then return the human summary with a link to it.

Keep the JSON `summary` useful to a human: describe the implemented outcome and
evidence. Do not prefix it with the skill name, timestamp, packet path, or other
transport metadata unless the supplied schema explicitly requires that text.

For the existing worker-result schema:

- `status`: `complete`, `needs_input`, `blocked`, or `failed`; `complete` is a
  submission, not acceptance.
- `files_changed`: task-owned repository-relative paths only.
- `verification`: every run or required-but-unrun command with exact outcome.
- `decisions`: local reversible task choices only.
- `questions`: unresolved input/authority issues and whether they block.
- `risks`: residual gaps or skipped stronger evidence.
- `next_action`: one exact route.

## Boundaries and routing

- Current-state executability failures route to `task-preflight` when a durable
  re-check is needed.
- Missing product/architecture authority or wider scope routes to the user or
  `task-brief-designer`.
- Completed work routes to `task-acceptance-review` when independent review is
  requested or required; otherwise return it to the user.
- Do not approve your own work, update an official plan/tracker, commit/push,
  install dependencies, use the network, launch subagents, or modify
  orchestration state unless explicitly authorized.

## Definition of done

- Outcome and ACs are satisfied with proportionate behavioral evidence.
- Changes are minimal, in scope, and separable from pre-existing user work.
- Targeted and justified broader checks have truthful results.
- Guided output is useful to a person; machine output is emitted only under an
  explicit machine contract.
- The next owner can act without reading the implementation transcript.
