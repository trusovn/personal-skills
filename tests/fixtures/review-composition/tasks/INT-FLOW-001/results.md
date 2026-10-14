# Implementation results: INT-FLOW-001

Submission state: `READY_FOR_REVIEW` (brief metadata `review: immediate`).
Evidence run: `run-20261012T112053Z-f6a83b5a1b72` (shared run-evidence sidecar).

## Changed paths

- `skills/task-implementation-flow/task-maintainability-review/SKILL.md`
- `skills/task-implementation-flow/task-maintainability-review/evals/evals.json`
- `skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py`
- `skills/task-implementation-flow/task-review-discovery/SKILL.md`
- `skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md`
- `skills/task-implementation-flow/task-acceptance-review/SKILL.md`
- `skills/task-implementation-flow/task-verification-designer/SKILL.md`
- `skills/task-implementation-flow/task-verification-designer/evals/evals.json`
- `skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py`
- `tests/test_task_maintainability_review.py`
- `tests/test_task_flow_guides.py`
- `tests/test_task_review_discovery.py`
- `tests/test_task_acceptance_review.py`
- `tests/test_task_preparation_contracts.py`

Inspected and unchanged, with reason: root `README.md`, `skills/README.md`,
and `skills/task-implementation-flow/README.md` already state the corrected
route/currentness semantics (asserted by the passing composition and
flow-guide checks), so no README claim became stale;
`scripts/install_development_skills.py` declarations are unchanged and the
corrected packages project through them (passing installer module exercised
disposable committed targets). The active `.agents/` installation, official
plans/task-map, `tests/fixtures/review-composition/tasks/index.json`, prior task/review/composition
history, and pre-existing untracked `.DS_Store` junk files are untouched.

## Correction map

- **I-01 / AC-01 / V-01:** the maintainability `Correction loop` now names
  the first outstanding stage and the complete ordered remainder — applicable
  `task-contract-registry-updater` synchronization when a registry stage
  applies, then fresh `task-review-discovery` evidence, then the separate
  `task-acceptance-review` decision — states that naming a route does not
  execute it, keeps only required-and-outstanding stages, cannot drop
  applicable registry work, and cannot invent an absent registry stage; the
  post-acceptance correction paragraph re-enters only conditional stages
  whose reviewed scope the correction affected.
- **I-02 / AC-02 / V-02, V-03:** the `Independence` section now follows actual
  affected reviewed scope and current evidence — affected scope owes a fresh
  review, demonstrably unaffected scope with applicable current proof retains
  that evidence, and stale/missing/inapplicable proof never completes a stage.
  The blanket "Every production correction invalidates the previous
  maintainability verdict" sentence is removed. Existing tests-only and
  reference-only route conditions in the flow guide and acceptance skill are
  preserved and asserted unchanged.
- **I-03 / AC-03 / V-04:** the producer contract now requires a stable
  finding ID (example `MNT-01`) independent of display order; the Output and
  `SELF_CHECK_ONLY` forms carry IDs plus a current disposition; genuine stops
  retain IDs with full evidence and no finding cap; prior reports stay
  unchanged, resolved IDs are never recycled, and new findings receive unused
  identities. The fixture gained a `correction-round` scenario staging a prior
  durable report with `MNT-B1`–`MNT-B4`, a correction that applies only
  MNT-B2's smallest correction direction, and identity-continuity facts; new
  eval case 4 is the corresponding T-005 role call.
- **I-04 / AC-04 / V-05–V-08:** discovery's final handoff and the durable
  report template now carry the applicable packaged preparation references
  (verification revision, readiness/preflight, decision context) for
  complete, clean guided reports as well as explicitly partial ones, while
  unpackaged direct edits hand off supplied conversational context; guided
  acceptance inputs and decision-workflow step 1 now identify and read those
  references. Existing revision-recovery/old-readiness, preflight-only
  contextual-disposition, and compact direct-entry rules were already
  present and are asserted unchanged.
- **I-05 / AC-05 / V-09:** the verification designer permits deriving
  task-local scenarios for an executable integration leaf's own explicit
  composition ACs from supplied producer outputs at stated consumer
  boundaries, while refusing composite parents (route to the
  dependency-ready executable leaf), invented sibling requirements and
  system-wide strategy ownership, and unavailable inputs/oracles (route to
  owner/preflight/task design; never fabricate a report or claim readiness).
  Packaged preparation remains mandatory for that leaf. The fixture gained an
  `integration-leaf` scenario and eval case 9 is the corresponding T-005 role
  call.

## Verification evidence

All commands ran from the repository root.

1. **Fail-first rejection (old bytes, pre-edit):** focused unittest run of the
   changed/new checks — FAILED (8 assertion failures rejecting the old
   shortcut/blanket-invalidation/identity-less output/omitted references/
   blanket refusal; 2 staging errors for the not-yet-existing fixture
   scenarios). Structural contract evidence that the new checks reject the
   old instructions.
2. **Focused checks (post-edit):** the same 11 changed/new test methods — OK.
3. **Owning modules:**
   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest
   test_task_maintainability_review test_task_review_discovery
   test_task_acceptance_review test_task_preparation_contracts
   test_task_flow_guides test_review_composition
   test_install_development_skills` — Ran 118 tests, OK (~3.0 s; recorded
   through the run-evidence sidecar; preflight baseline was 110 tests).
4. `git diff --check` — clean; changed paths are exactly the 14 files above.

Real fixture/Git observations inside those runs: the `correction-round`
workspace is a real disposable Git repo whose corrected `pricing.py` was
observed at the import boundary (`fee(100) -> 2.0`, `surcharge(100, 10) ->
1.5`, no `billing.db` created, seeded sqlite rates ignored) while the
MNT-B1 divergence still reproduces (`99.0` vs `103.50`); the
`integration-leaf` and `preparation-routes`-family scenarios stage real
committed Git workspaces; the installer module projected the corrected
packages onto disposable committed targets.

Evidence limits: skill-text assertions are structural contract checks;
staged reports (prior maintainability report, oracle, facts) are supplied
fixture inputs, not actual role outputs. No maintainability/discovery/
acceptance/verification-designer role call was executed and no role runner
was added — those are T-005 boundaries.

## T-005 qualification inputs

- **Exact setup:**
  `EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py <four-blockers|genuine-stop|correction-round>` and
  `EVAL_WORK_ROOT=<disposable> python3 skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py integration-leaf`.
- **Role calls:** `task-maintainability-review` eval case 4 (correction-round
  identity continuity) and `task-verification-designer` eval case 9
  (integration-leaf permission and refusals); discovery eval case 11 and
  the acceptance guided cases supply prepared verification/preflight context
  for observing preparation-reference handoff and consumption.
- **Intended producers/consumers:** maintainability review produces stable
  finding IDs and the conditional-remainder handoff; the correction
  implementer and fresh maintainability review consume the prior report and
  correction facts; discovery/acceptance consume the preparation references;
  the verification designer consumes the INT-9 brief plus producer outputs
  and produces the leaf's composition scenarios.
- **Expected contrasts:** three survivors keep IDs despite reorder; MNT-B2
  keeps its ID with a corrected disposition; a new finding takes an unused
  identity (next: MNT-B5); prior report bytes unchanged; next durable report
  is `maintainability-02.md`; registry work appears exactly when applicable
  and naming never executes a stage; complete clean handoffs still carry
  preparation references; the integration leaf's own composition ACs are
  designed while the composite parent/sibling/unavailable-oracle contrasts
  stay refused.
- **Unrun boundaries:** all actual role compliance, durable-report writing,
  and routing behavior.

## Actual contract impact

- added/changed/removed durable cross-task surface: **none**; no
  `docs/contracts` registry exists and none was created (per brief).
- Executable contract declarations changed: none (skill instructions,
  templates, eval expectations, and task-local fixture setup only).

## Next route

First outstanding owner: a **fresh `task-maintainability-review`** of these
corrected bytes. Complete ordered remainder: (architecture gate — no
canonical deterministic architecture command is declared in this repository;
registry synchronization — no registry exists, so the stage is absent, not
skipped) → fresh independent `task-review-discovery` evidence → the separate
fresh `task-acceptance-review` decision. Naming this route does not execute
it; the implementer invocation ends here.