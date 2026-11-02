# Task Brief: SIDE-001 — Write verification designs as readable test cases

## Outcome

Change `task-verification-designer` so its output helps a person and an
implementation agent understand what to test, what should happen, and why it
matters. Lead with concrete test cases. Keep traceability and document metadata
available without making them the reader's first task.

## Authority and scope

- Authority: the owner's request in this session, following the T-001.2
  verification design: “I like this wording more. Create a separate
  along-the-way task here to do such a change to the skill.” The approved
  presentation is preserved below.
- This is a separate side task, not a child or prerequisite of T-001. It does
  not change the maintainability delivery plan or its acceptance criteria.
- Edit source `skills/task-implementation-flow/task-verification-designer/`.
  Update relevant existing tests/evals and directly affected flow guidance only
  where required for consistency. Follow `testing-discipline` for coverage.
- Inspect `scripts/install_development_skills.py`, its focused tests, profile
  guide and README installation references, as repository policy requires for
  profile skill changes. Synchronize only references made stale by this change.
- Preserve `docs/tasks/T-001.2/verification.md` exactly. Use it as read-only
  context. Do not rewrite other existing verification artifacts or refresh the
  active `.agents/` installation.
- Preserve verification semantics: authority, complete AC/risk coverage, stable
  case IDs, exact expected results, evidence limits, conflict protection and
  task-design/preflight routing. This task changes presentation, not assurance.

Expected contract impact: no runtime or plan-contract change. The skill's output
instructions change; check consumers before changing required headings. Retain
the singular `Source brief:` declaration and required revision information.

## Work and acceptance criteria

- **AC-01:** The output opens with a short explanation of the behavior being
  checked and its main promises. Cases use plain test-case or bug-report
  wording: **Situation**, **Action**, **Expected result**, **Why test this**,
  and **How to check**, or an equally clear table/sequence for related cases.
  Titles name concrete behavior. Avoid abstract process language when an
  example can state the actual failure.
- **AC-02:** Each case gives decisive inputs and observable expected results.
  Explain the test method beside the relevant case; share common setup once.
  Do not require an opening generic “Testing approach” table. Retain distinct
  boundaries, lifecycle checkpoints, unknown values and evidence limitations.
- **AC-03:** Move source/revision metadata and the coverage map to the end.
  Keep stable case IDs and complete traceability. Remove the mandatory
  explanatory “Ready means…” paragraph and similar workflow boilerplate from
  generated documents. Do not change the workflow's readiness rules.
- **AC-04:** Remove the mandatory generic “Implementation handoff” section.
  Include only task-specific constraints, unresolved dependencies or necessary
  next actions when they add information. Do not repeat instructions already
  supplied by the consuming workflow.
- **AC-05:** Skill instructions, output example, completion checks and relevant
  tests/eval expectations agree on the new presentation. Existing coverage and
  safety rules remain effective. The T-001.2 verification artifact is unchanged.

### Approved wording example

This example illustrates style; it does not replace any source task's rules.

> **Report an increase without calling it worse**
>
> **Situation:** A function's complexity increases from 9 to 10. The configured
> target is 10.
>
> **Action:** Capture the function before the edit, make the edit, then run a
> comparison.
>
> **Expected result:** The report shows before 9, current 10, and change +1.
> JSON uses `increased`; text says “Increased.” The report does not say that the
> function crossed the target. A value equal to 10 is still within the target.
> The command exits successfully.
>
> **Why test this:** A caller should see what changed. An increase alone must
> not cause the tool to report failure or call the code worse.
>
> **How to check:** Use the pinned analyzer on actual Python source. Inspect
> the saved JSON, text summary and command exit status.

## Verification

Verification-design recommendation: separate — compare readability and retained
coverage without confusing instruction checks with generated-output behavior.

Use existing preparation-contract tests and verification-designer evals first.
Update relevant expectations instead of adding a parallel harness. Run the
owning focused suite, currently `python3 -B -m unittest discover -s tests -p
test_task_preparation_contracts.py`, after confirming its scope in preflight.
Run installer tests if managed resources/references change, plus the repository's
required architecture and contract checks before handoff.

Review a generated example against AC-01–AC-04 and its source brief. Demonstrate
both readability and preservation of distinct obligations; matching headings
alone is not behavioral qualification. Live/model-based evaluation requires a
separate approved budget. If not run, report generated behavior as unqualified
rather than implying that structural tests prove it.

## Execution

Status: `ready`
Task kind: `executable`

The brief is prepared. Derive `verification.md`, then obtain a ready
`preflight.md` through standalone guided preflight before implementation.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 12 tool calls / 30 minutes / skill presentation and focused coverage
```

Sizing policy: `default@1`. Estimate: 12 implementation-agent calls and 30
minutes; confidence medium. Fits the active policy; no split trigger applies.

Stop and return to the owner if the change would remove a required verification
obligation or require rewriting existing task artifacts. After implementation
and applicable conditional stages, use fresh independent `task-review-discovery`,
then a separate `task-acceptance-review` decision. Do not claim author self-checks
as independent acceptance.
