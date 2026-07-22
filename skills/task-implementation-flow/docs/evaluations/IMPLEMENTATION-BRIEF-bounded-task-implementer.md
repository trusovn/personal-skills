# Implementation brief: enforce implementer handoff and invariant-level correction

Status: `ready`

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 22 tool calls / 90 minutes / 65k context
```

This block is intended launch guidance under resolved decision `G-01`; it does
not claim an observed runtime configuration.

This brief is self-contained implementation authority for the
`bounded-task-implementer` changes derived from the 2026-07-21 flow evaluation.
An implementer may inspect the repository paths named here, but should not need
to read the source evaluation or this conversation.

## Outcome

Make an implementer with immediate-review work stop at an explicit fresh-review
handoff, account for finite high-risk cases before editing, correct broken
invariants rather than only demonstrated symptoms, and avoid duplicate broad
gates during correction.

## Why this change is justified

- Same-session self-acceptance occurred in S3-06, S3-07 correction 3, and three
  S3-08 implementation/correction sessions. Loading
  `task-acceptance-review` was incorrectly treated as a role reset.
- S3-06 and S3-07 therefore have no observed independent final verdict on their
  final bytes. The existing sentence “Do not approve your own work” did not
  prevent this.
- `review: immediate` was repeatedly read as “perform review now,” not “handoff
  immediately to a fresh reviewer.”
- Corrections were symptom-local: one descendant leak did not trigger sibling
  leader/pipe/race cases; one identity mismatch did not trigger exact record
  binding; one partial publication did not trigger sibling invalid prefixes.
- Implementation/fix sessions consumed 48.0% of S3-07's and 42.2% of S3-08's
  uncached-input plus output proxy. Repeated broad gates and rediscovery were
  material contributors.
- Implementers did preserve reviewer regressions well. Keep that successful
  behavior and make it the primary correction handoff.

The change must not remove implementation verification. Implementers still own
fail-first, targeted, and normally the nearest owning suite. The forbidden
behavior is issuing an independent acceptance verdict on bytes authored in the
same session.

## Authority and scope

| Item | Contract |
|---|---|
| Primary authority | This brief, derived from `skills/task-implementation-flow/docs/evaluations/EVALUATION-2026-07-21.md` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Canonical skill | `skills/task-implementation-flow/bounded-task-implementer/` |
| Active mirror | `.agents/skills/bounded-task-implementer/`, read-only during this task and updated only by post-acceptance distribution |
| Allowed canonical changes | `SKILL.md`, `evals/evals.json`, and `evals/files/setup_fixture.py` |
| Post-acceptance distribution | Corresponding active-mirror files, owned by the separate distribution step after the canonical change receives independent `ACCEPT` |
| Read-only context | The other three flow skills, their report/templates, and `skills/task-implementation-flow/README.md` |
| Out of scope | Active-mirror writes, acceptance-review implementation, worker-result schema changes, production task-orchestrator changes, official plan/task updates, live comparative benchmarking, and cross-skill README integration |
| Dependencies | None; `G-04` is resolved and current `review: immediate` semantics are sufficient for this skill-local change |

The canonical and mirror directories were byte-identical when this brief was
written. Recheck before editing.

## Needs to be solved before implementation

No product or architecture decision blocks this skill-local task.

Two self-preflight facts still require resolution:

- Preserve the existing user change to `skills/task-implementation-flow/README.md`;
  this task must not edit it.
- Leave the active mirror unchanged. The post-acceptance distribution owner
  resolves the approved canonical-to-mirror sync/install process after the
  canonical change receives independent `ACCEPT`.

## Required work

1. Replace ambiguous immediate-review wording with a provenance-based handoff
   rule.
   - `review: immediate` means complete implementation checks, perform an
     optional labeled self-check, and route immediately to a fresh reviewer.
   - Loading, quoting, or following `task-acceptance-review` in the current
     session does not create independence.
   - If the current session authored any production bytes under review, it may
     find and fix its own defects but must not emit `ACCEPT` or describe the
     result as independently reviewed.
   - If a fresh reviewer is unavailable, stop at `READY_FOR_REVIEW`; do not
     degrade to same-session acceptance.

2. Make output semantics explicit without breaking machine contracts.
   - Guided immediate-review output uses a clear `READY_FOR_REVIEW` submission
     state and `Next: fresh task-acceptance-review`.
   - For an existing worker-result schema, retain `status: complete` because it
     already means submission, not acceptance; set
     `next_action` to a fresh `task-acceptance-review`.
   - Do not add `READY_FOR_REVIEW` to a supplied JSON schema or invent a new
     machine field.
   - For milestone/no-review work, retain the current human result semantics.

3. Add a pre-edit finite risk/evidence account.
   - When the task authority explicitly supplies a finite high-risk matrix or
     named universal cases, map every row/case to existing or planned evidence
     before editing.
   - This may remain concise scratch reasoning; do not force a durable artifact
     for guided tasks.
   - The final AC evidence must make omissions visible. Do not expand into
     generic risk enumeration beyond the authority.
   - On correction, consume the complete prior review coverage ledger when
     supplied. Preserve every row identity and status, including prior passes
     as navigation context and unchecked/blocked state for the next reviewer;
     do not promote prior passes to acceptance evidence for the corrected
     bytes.

4. Add an invariant-level correction step.
   - For each reviewer finding, first state the broken invariant.
   - Enumerate only credible sibling cases already implied by the same task
     contract or finite matrix.
   - Preserve the reviewer regression and implement the smallest correction
     that protects the invariant rather than adding a field-specific or
     interleaving-specific special case.
   - Add table-driven/parameterized sibling evidence when several explicit
     values share one oracle; do not create a reusable framework for a one-task
     fix.
   - Carry the authoritative brief reference, preceding verdict, complete
     coverage ledger, current scoped diff, complete findings, reproducer
     commands, broad-gate decision, and remaining coverage rows into the final
     correction handoff. Report implementation evidence separately from
     reviewer row status.

5. Assign correction gate ownership.
   - Initial implementation: fail-first, targeted, nearest owning suite, and a
     broader gate only when the task explicitly requires it or blast radius
     justifies it.
   - Correction: reviewer regressions plus the nearest owning suite by default.
   - Run the broader/aggregate gate during correction only when authority or
     blast radius requires it, or when no final reviewer is assigned to own it.
   - Never run an acceptance pass as a substitute for implementation checks.

6. Add an immediate-review handoff eval.
   - Add an `api-immediate` fixture at `/work/api-immediate` rather than
     changing the existing `api-guided` milestone case. Use exact targeted
     command
     `python -m unittest tests.auth.test_session.SessionTest.test_expired_session_is_invalid`
     and owning command `python -m unittest tests.auth.test_session`.
   - It should stage a clean, bounded task with `review: immediate`, one source
     path, one test path, a real fail-first defect, exact targeted and owning
     commands, and no machine result schema.
   - The eval must require implementation checks and permit a labeled
     self-check, but assert `READY_FOR_REVIEW`, fresh-review next action, no
     `ACCEPT`, and no attempt to load/execute the acceptance-review role.
   - The fixture's test must actually reject the old behavior and pass after the
     bounded production change.

7. Add an invariant-level correction eval.
   - Add a `record-correction` fixture at `/work/result-record` with an
     independently anchored digest of exact serialized result bytes, a buggy
     validator that checks only one identity field, and a reviewer regression
     showing a coherent mutation of a different field with internal consistency
     recomputed. Use focused command
     `python -m unittest tests.test_record_integrity.RecordIntegrityTest.test_coherent_mutation_is_rejected`
     and owning command `python -m unittest tests.test_record_integrity`.
   - The task contract must require binding all exact result bytes, not just the
     demonstrated field.
   - Include at least one credible sibling mutation or semantically equivalent
     byte rewrite in the allowed test file.
   - The eval must reject a one-field equality patch, require a minimal
     record-level binding correction, run the supplied reviewer regression plus
     owning suite, skip an unnecessary aggregate gate, and end at a fresh
     review handoff.
   - Supply a prior review ledger with at least one failed and one unchecked
     row. Require the correction handoff to preserve both row identities,
     attach correction evidence to the failed row, and leave the unchecked row
     for the fresh reviewer without claiming a verdict. The handoff must also
     retain the preceding verdict and include the current scoped diff.
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

- **AC-01 — immediate review is a handoff.** A guided implementation with
  `review: immediate` completes its own checks and ends `READY_FOR_REVIEW` with
  a fresh-review route, never `ACCEPT`.
- **AC-02 — role loading cannot reset provenance.** Instructions explicitly say
  that loading another skill in the same authoring session does not create
  independence.
- **AC-03 — machine submission remains compatible.** Existing schemas retain
  `status: complete` and use `next_action` for fresh review; no unauthorized
  schema change is made.
- **AC-04 — finite task risks are accounted for.** Every explicit named row/case
  is mapped to evidence before editing and summarized at handoff, without
  generic matrix expansion.
- **AC-05 — correction protects the invariant.** The record-correction eval
  produces exact-byte binding and sibling evidence; a demonstrated-field-only
  patch fails the eval expectations.
- **AC-06 — correction verification is economical.** Reviewer regressions run
  first, then the nearest owning suite; an aggregate gate is not repeated
  without a named owner/risk reason.
- **AC-07 — self-check remains useful but non-authoritative.** The implementer
  may report and fix self-found issues but labels them as implementation
  evidence, not an acceptance verdict.
- **AC-08 — review continuation survives correction.** A correction consumes
  and preserves the authoritative brief reference, preceding verdict, complete
  review ledger, current scoped diff, regressions, gate decision, and unchecked
  rows without presenting stale passes as current acceptance.
- **AC-09 — retrospective evals can reject old behavior.** The new evals reject
  same-session `ACCEPT`, missing fresh-review routing, symptom-local correction,
  lost review-continuation state, or unjustified aggregate execution.
- **AC-10 — distribution boundary is preserved.** This task changes only the
  canonical skill and leaves the active mirror untouched; the accepted
  canonical paths and post-acceptance distribution route are explicit in the
  handoff.

## Verification

Run one command at a time, narrowest first. The repository does not document a
canonical live skill-eval command; resolve it during self-preflight and request
approval before paid/live execution.

| Evidence | Scenario and oracle | Command |
|---|---|---|
| JSON structure | Updated eval definitions parse | `python3 -m json.tool skills/task-implementation-flow/bounded-task-implementer/evals/evals.json` |
| Fixture syntax | The setup script parses as Python without filesystem writes | `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py').read_text())"` |
| Immediate fixture | `api-immediate` stages a real fail-first defect and exact guided commands | From the canonical skill directory: `python3 evals/files/setup_fixture.py api-immediate`; run the staged targeted command and confirm its initial failure is the missing expiration behavior |
| Correction fixture | `record-correction` stages exact-byte authority, a field-local validator defect, deterministic reviewer regression, and sibling mutation | From the canonical skill directory: `python3 evals/files/setup_fixture.py record-correction`; run the staged reviewer regression and confirm it fails for the intended invariant |
| Owning skill eval set | Every pre-existing and new eval is run; the revised skill satisfies AC-01–AC-09, while the baseline/current skill is expected to self-accept, patch too narrowly, or lose review-continuation state. Any skipped eval IDs and affected unverified ACs are reported explicitly | Full owning eval-runner command discovered in self-preflight; approval required for paid/live execution |
| Mirror preservation | No task-created change appears under the active mirror relative to the self-preflight baseline | `git status --short -- .agents/skills/bounded-task-implementer` |

Do not count JSON or fixture syntax parsing, or a placeholder fixture, as
behavioral validation. The fixtures must demonstrate the intended failure
oracles. The global comparative cost evaluation is outside this task.

## Stops and handoff

- Do not change the worker-result schema to express the human
  `READY_FOR_REVIEW` state.
- Do not edit acceptance-review behavior, the shared README, official plans, or
  production task-orchestrator code.
- Do not infer sibling cases beyond the task's invariant or explicit finite
  matrix.
- Do not mark prior reviewer rows passed or checked on behalf of the fresh final
  reviewer.
- Stop on user-work overlap. Do not edit the active mirror; unresolved
  distribution does not block canonical implementation or acceptance.
- End implementation at `READY_FOR_REVIEW`; only a fresh reviewer may accept
  the resulting bytes.

Next action: guided canonical implementation, fresh acceptance review, then
post-acceptance distribution of accepted bytes.
