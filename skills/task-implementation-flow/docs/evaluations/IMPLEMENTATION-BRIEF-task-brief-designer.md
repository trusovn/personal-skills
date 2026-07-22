# Implementation brief: strengthen `task-brief-designer`

Status: `ready`

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 20 tool calls / 90 minutes / 60k context
```

This block is intended launch guidance under resolved decision `G-01`; it does
not claim that the authoring skill can observe the actual runtime launch
configuration.

This brief is self-contained implementation authority for the
`task-brief-designer` changes derived from the 2026-07-21 flow evaluation. An
implementer may inspect the repository paths named here, but should not need to
read the source evaluation or this conversation.

## Outcome

Make task briefs turn finite, material high-risk requirements into a compact
coverage contract that separates implementation evidence from independent
review and assigns the broad gate, without turning ordinary guided briefs into
exhaustive test specifications.

Keep the existing four-key metadata schema as intended launch guidance and make
each brief recommend its readiness route without inventing an unconsumed
machine field.

## Why this change is justified

- The evaluated S3-07 and S3-08 briefs already named the decisive risk
  families, so missing requirements were not the main failure.
- S3-07 still took three correction rounds in one process-cleanup family.
- S3-08 took five correction rounds before a sixth independent review accepted
  the result; most defects were unimplemented members of already-required
  tamper and publication-recovery families.
- Phrases such as “each persisted artifact,” “every publication boundary,”
  and “complete process-group cleanup” did not reliably become finite evidence
  plans for medium-reasoning agents.
- The skill was otherwise effective: it produced strong outcomes, scope,
  negative evidence, lifecycle requirements, and real-boundary requirements.
  Preserve those strengths.

The smallest useful response is deterministic scaffolding around explicit
finite risks. A generic matrix for every task would add ceremony and recreate
the token problem this change is meant to reduce.

## Authority and scope

| Item | Contract |
|---|---|
| Primary authority | This brief, derived from `skills/task-implementation-flow/docs/evaluations/EVALUATION-2026-07-21.md` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Canonical skill | `skills/task-implementation-flow/task-brief-designer/` |
| Active mirror | `.agents/skills/task-brief-designer/`, read-only during this task and updated only by post-acceptance distribution |
| Allowed canonical changes | `SKILL.md`, `references/task-brief-template.md`, `evals/evals.json`, and `evals/files/setup_fixture.py` under the canonical skill directory |
| Post-acceptance distribution | Corresponding active-mirror files, owned by the separate distribution step after the canonical change receives independent `ACCEPT` |
| Read-only context | `skills/task-implementation-flow/README.md`, the other three flow skills, and existing task-orchestrator task briefs |
| Out of scope | Active-mirror writes, production task-orchestrator behavior, existing official plans/tasks, unrelated skill cleanup, live comparative benchmarking, and cross-skill README integration |
| Dependencies | `G-01`, `G-03`, and `G-04` are resolved by the 2026-07-23 notes in `GLOBAL-DECISIONS-task-implementation-flow.md` |

The canonical and mirror directories were byte-identical when this brief was
written. Recheck before editing. If they have diverged, record the ownership or
distribution drift for the post-acceptance distribution owner; do not overwrite
either side as part of this canonical task.

## Resolved decisions and repository coordination

### G-01 — metadata describes intended launch guidance

Keep `agent_tier`, `reasoning`, `review`, and `budget`. The first three express
the launch profile the task author actually intends for future automated or
manual routing; `budget` is a soft checkpoint unless authority makes it hard.
The skill does not claim to observe actual runtime configuration. Do not add
nested execution/review fields until a named launcher consumes and enforces
them.

### G-03 — briefs recommend the readiness route

For each durable brief, state one human-readable route:

- `implementer self-preflight` for routine guided work;
- `standalone guided preflight — <material uncertainty>` when brief-time
  authority identifies a meaningful readiness uncertainty; or
- `high-assurance preflight` when the profile requires it.

This is guidance, not a new metadata/schema field. Current repository state can
still require the implementer or future orchestrator to escalate the route at
execution time. Machine parsing and precedence belong to the later
orchestrator contract.

### G-04 — review coverage is transferable

Finite-risk rows must be stable enough for later reviews to carry them forward
as `pass`, `fail`, `blocked`, or `unchecked`. The brief defines the rows and
oracles; it does not treat a prior reviewer result as proof for corrected
bytes.

### Repository coordination facts

- `skills/task-implementation-flow/README.md` already had user changes when
  this brief was created. It is not part of this task; preserve it.
- No repository-local sync command was found in the relevant README files.
  This does not block canonical implementation and review. The post-acceptance
  distribution owner must resolve the approved process before changing the
  mirror.

## Required work

1. Add a finite-risk expansion step to `SKILL.md`.
   - Trigger it only when authority contains a universal or lifecycle claim
     whose cases are both finite and material, such as named artifact families,
     ordered publication prefixes, exact cardinality, retries, recovery,
     tampering, or bounded cleanup states.
   - Do not expand open-ended quality words, speculative abuse cases, or generic
     test catalogs.
   - Preserve the existing rule to keep guided work compact.

2. Define one compact optional table with these semantics:

   | Field | Meaning |
   |---|---|
   | Invariant | The contract property that must remain true |
   | Material dimensions/cases | Exact finite values or state transitions whose omission could permit false success |
   | Decisive oracle/boundary | Observable outcome and the real boundary needed to prove it |
   | Implementation evidence | Fail-first, targeted, or owning evidence the implementer must establish |
   | Independent review probe | Distinct corroboration or adversarial probe; `N/A` only with a reason |
   | Gate owner | Who runs the owning/broad gate and at which stage |

   Rows may combine cases only when they share one invariant and oracle. The
   table is a coverage contract, not a requirement to generate a Cartesian
   product.

3. Make gate ownership explicit.
   - Separate implementation evidence from independent-review probes.
   - For an immediate-review correction flow, record whether the correction
     implementer or the final fresh reviewer owns the broader/aggregate gate.
   - Avoid requiring the same broad gate after every failed review when
     targeted evidence remains red.

4. Update `references/task-brief-template.md` minimally.
   - Add the finite-risk table as an optional core subsection, with an explicit
     omission rule for tasks without finite material dimensions.
   - Keep the existing high-assurance addendum conditional.
   - Do not duplicate the existing AC execution matrix; the new table should
     clarify finite case coverage and gate ownership, while the high-assurance
     matrix continues to record durable execution details.

5. Update the metadata guidance in `SKILL.md` and the template to implement
   resolved `G-01` exactly.
   - Define the values as truthful intended launch guidance usable by future
     automated or current manual routing.
   - Keep the current four scalar keys.
   - Do not claim the skill can observe a runtime reasoning setting unless that
     setting is supplied to it.

6. Make the per-task readiness route explicit in `SKILL.md` and the template.
   - Use the three human-readable routes defined under `G-03`.
   - Require a concrete material-uncertainty reason for standalone guided
     preflight.
   - Keep the routine default as implementer self-preflight and allow
     execution-time escalation when current facts require it.
   - Do not add a launch-metadata key or machine schema for the route.

7. Add or revise eval coverage in `evals/evals.json` and
   `evals/files/setup_fixture.py`.
   - Add a `finite-risk-matrix` fixture at `/work/evidence-flow` containing
     approved authority that names: policy, manifest, attempt record, structured
     result, and closure as persisted evidence families; ordered execution,
     verification, decision, and ledger publications; legal prefixes; and
     contradictory orphan states.
   - Include an existing happy-path test in the fixture that is insufficient to
     prove tamper denial or recovery, so the expected matrix is behaviorally
     motivated rather than a formatting exercise.
   - Add an eval requiring a guided implementation brief that enumerates the
     named evidence families and publication states, uses pre-side-effect
     rejection/reuse as the real-boundary oracle, separates implementer and
     reviewer evidence, and names the broad-gate owner.
   - Assert that unrelated generic corruption, fuzz, platform, and performance
     cases are not invented.
   - Update the existing metadata eval only as required by `G-01`; preserve its
     surgical gap-check purpose.
   - Add or revise one metadata expectation whose authority explicitly calls
     for the economical medium-reasoning profile and immediate fresh review.
     It must reject generic `reasoning: high` output and same-session review
     semantics. This tests truthful task authoring without pretending the skill
     can inspect hidden runtime configuration.
   - Add or revise routing expectations so routine guided authority recommends
     implementer self-preflight, while authority naming a material readiness
     uncertainty recommends standalone guided preflight with the reason.
     Reject a new route metadata key and unconditional standalone ceremony.
   - Preserve every pre-existing eval unless this task explicitly revises its
     expectation. Treat the complete pre-existing-plus-new eval file as the
     owning regression set. If runner availability or paid/live authorization
     prevents execution, list the exact skipped eval IDs and do not claim the
     affected unchanged behavior.

8. Keep the active mirror unchanged during implementation and canonical
   acceptance. After an independent `ACCEPT`, hand the accepted canonical paths
   to the separate distribution owner, who resolves the approved sync/install
   process and proves byte identity.

## Acceptance criteria

- **AC-01 — finite material cases become explicit.** Given authority naming
  persisted artifact families and ordered publication states, the produced
  brief lists every named material family/state and a decisive oracle instead
  of collapsing them into “each” or “every.”
- **AC-02 — expansion remains bounded.** A routine guided task without finite
  high-risk dimensions does not gain a generic matrix, high-assurance ledger,
  or speculative cases.
- **AC-03 — evidence roles are distinct.** The table identifies implementation
  evidence separately from an independent-review probe and does not treat an
  implementer self-check as acceptance.
- **AC-04 — gate ownership is unambiguous.** Immediate-review briefs say who
  owns the broad gate after correction; they do not require duplicate aggregate
  runs at every stage by default.
- **AC-05 — template and skill agree.** The optional template section and
  `SKILL.md` use the same fields, trigger, and omission rule without duplicating
  the high-assurance matrix.
- **AC-06 — metadata is truthful.** Generated metadata follows resolved `G-01`;
  the skill neither invents an actual runtime setting nor emits
  known-inaccurate launch guidance. Authority that explicitly requests the
  medium-reasoning economical profile produces medium guidance.
- **AC-07 — readiness routing is explicit and proportionate.** A brief names
  implementer self-preflight by default, standalone guided preflight only with
  a material reason, or required high-assurance preflight; it adds no
  unconsumed route metadata field.
- **AC-08 — retrospective eval can reject the old behavior.** The new fixture
  and expectations fail an output that retains only universal prose, omits a
  named family/publication state, conflates implementation and review evidence,
  leaves the broad gate owner unstated, or recommends the wrong readiness
  route.
- **AC-09 — distribution boundary is preserved.** This task changes only the
  canonical skill and leaves the active mirror untouched; the accepted
  canonical paths and post-acceptance distribution route are explicit in the
  handoff.

## Verification

Run one command at a time, narrowest first. Exact live skill-eval tooling is not
documented in this repository and must be resolved during self-preflight.

| Evidence | Scenario and oracle | Command |
|---|---|---|
| JSON structure | The updated eval file parses | `python3 -m json.tool skills/task-implementation-flow/task-brief-designer/evals/evals.json` |
| Fixture syntax | The setup script parses as Python without filesystem writes | `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('skills/task-implementation-flow/task-brief-designer/evals/files/setup_fixture.py').read_text())"` |
| Fixture behavior | `finite-risk-matrix` stages the named authority, inadequate happy-path evidence, and no implementation | From the canonical skill directory: `python3 evals/files/setup_fixture.py finite-risk-matrix` |
| Owning skill eval set | Every pre-existing and new eval is run; the revised skill satisfies AC-01–AC-08, while an unchanged/baseline output is expected to miss at least the finite matrix, gate owner, or explicit readiness route. Any skipped eval IDs and affected unverified ACs are reported explicitly | Full owning eval-runner command discovered in self-preflight; obtain approval first if it invokes a paid/live model |
| Mirror preservation | No task-created change appears under the active mirror relative to the self-preflight baseline | `git status --short -- .agents/skills/task-brief-designer` |

Schema and fixture syntax parsing are not behavioral proof. Do not report
the skill change as behaviorally validated unless the fixture is staged and the
focused skill eval is actually run. The multi-configuration cost comparison is
a separate, approval-gated global evaluation, not part of this task.

## Stops and handoff

- Stop on overlap with user-owned changes, especially the shared README.
- Do not edit the active mirror; unresolved distribution does not block
  canonical implementation or acceptance.
- Do not edit official task-orchestrator plans or completed task briefs.
- Do not broaden the fixture into a shared test harness.
- Do not invent a machine-readable readiness-route field; a future orchestrator
  owns that interface.
- When implementation is complete, return `READY_FOR_REVIEW`; loading the
  acceptance-review skill in the same authoring session does not create an
  independent verdict.

Next action: guided canonical implementation, fresh acceptance review, then
post-acceptance distribution of accepted bytes.
