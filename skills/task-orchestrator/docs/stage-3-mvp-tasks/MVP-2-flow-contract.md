# Task Brief: `MVP-2` — Freeze the configurable flow contract

Status: `ready`

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 35 tool calls / 90 minutes / 90k context
```

## Readiness route

`implementer self-preflight`

Before changing files, estimate the work against the 35-tool-call and
90-minute pilot boundary. Keep this as one task when the contract, validation,
and cursor work fit. If they do not, stop and return it for the map's approved
split into:

1. flow contract, examples, envelopes, and validation; and
2. persisted cursor and existing-controller integration.

Both resulting tasks would have to be independently accepted before `MVP-3A`
could be actualized.

## Outcome

Persist one versioned, closed MVP flow as controller-owned authority, validate
its profiles and revisions before actor launch, and maintain a coherent current
step and bounded correction cycle without adding any new actor adapter or
workflow execution loop.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [Stage 3 MVP task-actualization map](../stage-3-mvp-task-actualization-map.md), `MVP-2` row and boundary adjustment; [Stage 3 MVP rebaseline](../stage-3-mvp-rebaseline.md), “Configurable workflow model,” “MVP-2,” Gate 1, deferred work, and stop/replan conditions |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Dependencies | `S3-08` foundation accepted; see [S3-08 result](../history/stage-3-tasks/S3-08-result.md). No new prerequisite task. |
| Allowed changes | `skills/task-orchestrator/scripts/controller_state.py`; `skills/task-orchestrator/scripts/controller.py` only for flow persistence, validation, cursor wiring, safe-boundary revision, and pre-launch enforcement; `skills/task-orchestrator/assets/run-policy.schema.json`; existing examples that must adopt the new contract; the smallest new flow, handoff, outcome, and profile schema/example files under `skills/task-orchestrator/assets/`; `skills/task-orchestrator/tests/test_controller_state.py`; `skills/task-orchestrator/tests/test_controller.py`; `skills/task-orchestrator/tests/test_retrieval_surface.py` only when needed to validate new current examples; and `skills/task-orchestrator/docs/stage-3-mvp-tasks/MVP-2-result.md` |
| Read-only context | [Architecture map](../../references/architecture-map.md); `skills/task-orchestrator/docs/controller-contract.md`; `skills/task-orchestrator/docs/stage-3-retrieval-surface-follow-up.md`; accepted S3-01–S3-08 results; owning source and tests named above |
| Out of scope | Concrete preflight or semantic-review actor selection; actor launch adapters; recovery, stop, resume, correction execution, fresh-session routing, semantic-review execution, acceptance, dependency release, automatic advance, plan preparation, skill/operator-guide rewrites, commit or tracker behavior, migration of pre-MVP run directories, arbitrary step kinds, plugins, a general workflow engine, and unrelated source or test reorganization |
| Assumptions / unresolved decisions | No material design decision is open. The implementation may choose the smallest JSON layout and the smallest explicit controller-owned flow-revision surface. Whether the initial flow is embedded in the run policy or digest-referenced from it is an implementation choice, provided there is one canonical authority, immutable history, and exact digest validation. |

The current retrieval documentation remains transitional. Do not update
`SKILL.md`, the operator guide, or the architecture map to advertise a runnable
profile flow before the later public runner and actors exist.

## Work and acceptance criteria

Required work:

1. Define one strict, versioned flow contract for the closed MVP phase order:
   optional `preflight`, required `implement`, optional `verify`, optional
   `semantic_review`, and required terminal `accept`. `correction` and
   `advance` are named controller/runner transitions, not freely orderable
   profile steps. S3-08 mechanical inspection of records, repository identity,
   and allowed scope remains always on; omitting `verify` disables configured
   test-command execution, not that controller inspection.
2. Represent the selected profile as immutable run authority. Bind the exact
   initial flow bytes or canonical content to the run and validate the same
   authority on every existing public path that could otherwise launch or
   inspect an actor. Do not create two mutable sources of flow truth.
3. Supply data-defined `fast local`, default `reviewed`, and `strong local`
   profiles. A custom profile may omit supported optional steps or change a
   supported level without a production-code edit, but it may not introduce a
   step kind, jump, mode, actor authority, or phase ordering outside this
   contract. Persist role and level configuration, not a concrete preflight or
   review transport/adapter. Cover preflight `light`/`standard`/`strong`,
   verification `targeted`/`targeted plus repository gate`, and semantic review
   `standard`/`strong`; optional-step omission is the canonical `off` behavior.
4. Apply the frozen actor-level mapping in the contract:
   `light -> gpt-5.6-sol/low`, `standard -> gpt-5.6-sol/medium`, and
   `strong -> gpt-5.6-sol/high`. Semantic review supports only `standard` and
   `strong`. The implementation-session reuse threshold is exactly 50% and is
   not profile-configurable.
5. Persist the profile's finite correction limit and its stop/escalation
   routes. Preserve the current routes for `blocked`, `failed`,
   `needs_input`, and unexpected changes, and cover `inconclusive`, exhausted
   correction cycles, permission expansion, and plan/architecture questions.
   Ordinary task-local `changes_requested` may authorize the correction
   transition only when the profile allows it and the next cycle remains
   within the persisted limit.
6. Define strict, versioned compact handoff and step-outcome envelopes for
   later adapters. Outcomes must be attributable to the run, selected task,
   flow revision, step, correction cycle, and actor role; use run-relative
   artifact references for durable evidence and raw transcripts. The envelopes
   may report outcomes and findings but cannot change the task range, selected
   task, flow, permissions, correction limit, or stop policy. Freeze one
   canonical spelling for the rebaseline's normal result families:

   - preflight: `ready`, `blocked`, `needs_input`;
   - implementation: `complete`, `needs_input`, `failed`;
   - verification: `mechanically_eligible`, `findings`;
   - semantic review: `ACCEPT`, `CHANGES_REQUESTED`, `INCONCLUSIVE`; and
   - acceptance: `task_accepted`.

   Do not invent the MVP-4 finding identity/status model in this task; the
   envelope may carry a versioned payload/reference slot without defining that
   later model.
7. Add controller-owned cursor state. With no selected task, the current step
   is null and the correction cycle is zero. Selecting a task sets the first
   enabled step and cycle zero. Existing commands may advance the cursor only
   across behavior they already own. In particular:

   - `run-next` may launch the existing implementation worker only when the
     validated current step is `implement`;
   - after implementation, `inspect` always performs the accepted S3-08
     mechanical boundary; it executes configured test commands only when
     `verify` is enabled, records verification as omitted by policy otherwise,
     and advances the cursor only after the applicable inspection/verification
     outcome is durably recorded; and
   - a pending preflight, semantic-review, correction, accept, or advance
     action with no owning MVP adapter must remain pending and must not be
     silently skipped, treated as passed, or replaced with an implementation
     launch.
8. Make cursor and correction updates exact, pure controller transitions. A
   forward step follows the persisted ordered flow. A
   `changes_requested -> correction -> fresh semantic_review` lifecycle
   increments the cycle exactly once when correction begins and cannot exceed
   the limit. Unsupported rewinds, caller-written counters, and cursor changes
   that disagree with the selected task or flow revision fail without
   mutation.
9. Permit flow revision only through an explicit operator action while the run
   is at a safe task boundary: `ready`, with no selected task, active attempt,
   or active operation. Publish a new immutable revision and atomically point
   controller state at it; preserve prior revision bytes. Reject revision
   during every ownership-bearing or terminal state, reject in-place rewrite,
   and reject any purported flow change carried by actor output or handoff.
10. Add focused behavior tests before implementation, then record exact
    commands, results, chosen serialization, revision publication sequence,
    cursor lifecycle, and residual risks in
    `docs/stage-3-mvp-tasks/MVP-2-result.md`.

- **AC-01:** The three required profiles and a custom supported profile pass
  runtime validation from real JSON inputs. `reviewed` is the default; the
  fast profile omits preflight and semantic review, and the strong profile
  resolves the strong preflight, verification, and review selections. Changing
  optional-step presence or a supported level is a data change, not a
  production-code change.
- **AC-02:** Runtime validation rejects a missing or duplicate required step,
  every duplicate actor step, invalid phase order, unsupported step or mode,
  semantic-review `light`, acceptance side effects other than `off`, a
  non-finite/negative/wrong-type correction limit, an unbounded backward route,
  a configurable context threshold, and any actor mapping that contradicts the
  frozen model/reasoning mapping.
- **AC-03:** Invalid, stale, tampered, or digest-mismatched flow authority fails
  before worker preflight or launch and leaves the run directory, ledger, flow
  revisions, and repository unchanged. Defensive validation prevents direct
  `run-next` or `inspect` use from bypassing initialization checks.
- **AC-04:** Initial flow authority and every explicit revision are immutable
  and digest-bound. A revision succeeds only at the exact safe boundary,
  preserves the prior record, changes no task/scope/permission authority, and
  becomes the sole current revision in one controller-owned state update.
  Repeating the same requested revision is a byte-identical no-op with no new
  revision or ledger write, never an in-place rewrite or ambiguous partial
  state.
- **AC-05:** Cursor state is coherent with the selected task and current flow.
  Task selection establishes the first enabled step at cycle zero; the first
  authorized correction increments to cycle one; fresh re-review retains that
  cycle; the next authorized correction increments exactly once again; and the
  configured limit routes to the persisted stop/escalation action without
  another correction.
- **AC-06:** Existing implementation and mechanical-inspection commands cannot
  skip a pending optional actor or acceptance step. A valid profile whose next
  step has no adapter produces a clear, unchanged pending/stop result with zero
  wrong-actor launches. With `verify` omitted, `inspect` still performs every
  S3-08 mechanical check, runs zero configured test commands, and records
  omission by policy rather than a pass.
- **AC-07:** The handoff and outcome validators accept each supported
  step-specific normal result, reject a result invalid for that step, require
  exact subject/cursor identity and safe artifact references, distinguish
  `omitted by policy` from passed or not-run behavior, and reject embedded
  authority changes or raw-transcript copying.
- **AC-08:** Accepted S3-01–S3-08 safety behavior and useful tests remain
  passing. Existing closure evidence is still mechanical eligibility;
  MVP-2 does not claim semantic review, acceptance, recovery, correction
  execution, or an end-to-end workflow runner.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| A profile can express only the closed MVP phase order. | `preflight` absent/light/standard/strong; required `implement`; `verify` absent/targeted/targeted-plus-repository-gate; `semantic_review` absent/standard/strong; one terminal side-effect-free `accept`; duplicates, reordered phases, unknown steps/modes. | Runtime validation of real JSON followed by public initialization; invalid input creates no runnable actor state. | Fail-first valid-profile test plus exhaustive table-driven validator cases and public-init denials. | Construct a custom supported profile and one adversarial profile with a valid-looking unknown/reordered step; corroborate zero launch. | Implementer owns focused validator/init evidence; fresh reviewer owns the adversarial probe. |
| Every backward route is bounded and policy-owned. | Correction disabled; finite limit zero; first correction; fresh re-review; next correction; exact exhaustion; wrong-type/negative/unbounded limit; stop versus escalate. | Pure transition oracle plus persisted ledger bytes at the controller state boundary. | Table-driven lifecycle test carrying the first legitimate change and next real occurrence through the exact limit. | Attempt a caller-supplied cycle jump and one correction beyond the limit; compare persisted bytes before/after. | Implementer owns transition coverage; fresh reviewer owns mutation-denial corroboration. |
| Flow authority never changes from an actor or during owned work. | Initial flow; explicit same/different revision at `ready`; running, awaiting-inspection, resumable, finalizing, and stopped denial; in-place tamper; actor/handoff-proposed flow. | Public controller revision boundary, immutable revision bytes, current digest reference, and zero worker calls. | Safe-boundary revision integration test and denial tests for every non-safe state and source. | Tamper an old revision and try a coherent ledger/reference rewrite before `run-next`; require fail-closed behavior. | Implementer owns publication/replay cases; fresh reviewer owns coherent-tamper probe. |
| The cursor describes the only profile step that existing commands may perform, while mandatory mechanical inspection is never disabled. | No selected task/null; selection/first enabled step; implementation; verify enabled/omitted; pending preflight/review/accept; task-boundary reset; cycle zero/one/next/exhausted. | Persisted ledger plus fake-worker/executor markers at `run-next`/`inspect`; wrong actor is never invoked, and verify omission suppresses commands but not S3-08 inspection. | Pure cursor tests and public integration tests for fast, verify-off, and reviewed/strong pending-step cases. | Start from a coherent-looking cursor/flow mismatch, then a verify-off run; prove zero wrong-adapter calls and complete mechanical inspection. | Implementer owns cursor and existing-command cases; fresh reviewer owns mismatch and verify-off probes. |
| Frozen actor selection and session threshold cannot drift by profile. | Light/standard/strong mappings; review excludes light; exactly 50%; omitted, 49.9%, 50%, 50.1%, null/unavailable as envelope values for later routing. | Runtime-resolved contract values and strict validators; no adapter launch is needed for this task. | Exact mapping/threshold cases that reject alternative model, reasoning, or threshold authority. | Supply semantically equivalent but non-canonical threshold/mapping encodings and verify rejection or one documented canonicalization. | Implementer owns the mapping matrix; fresh reviewer checks alternate encodings. |
| Structured records carry evidence, not authority. | Every supported step outcome; wrong-step outcome; run/task/flow/step/cycle/role mismatch; safe run-relative reference; traversal/absolute path; transcript reference versus copied transcript; omitted versus passed. | Runtime envelope validator operating on real JSON fixtures and exact subject identity. | Positive fixture per step and focused negative identity/path/authority cases. | Change one identity link and add a flow/permission field coherently; require rejection without state mutation. | Implementer owns fixture/validator evidence; fresh reviewer owns coherent authority-injection probe. |

## Verification

Run one command at a time. Install or repair no dependency unless a targeted
command proves one is missing.

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | A real reviewed-profile JSON fixture is accepted, persisted as exact authority, and initializes a null cursor; before implementation the current v1 validator must reject the new contract for the intended reason. | Add and run the focused method, for example: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_versioned_workflow_profiles_and_cursor` |
| Targeted | Pure profile, envelope, revision, cursor, and correction-cycle validation, including the first correction and next occurrence. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` |
| Targeted public boundary | Real JSON initialization/revision and fake-worker-marker cases prove invalid or pending flows cannot mutate state or launch the wrong actor. | Run the new focused `ControllerIntegrationTest` methods by exact name, then `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` |
| Owning suite | Current examples exercise runtime validation, not schema syntax alone; source-owned state and controller regressions pass. | If changed, run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_retrieval_surface.py`, after the two owning suites above pass. |
| Broader gate | All preserved controller, Git, transport, verification, and retrieval behavior remains passing. This aggregate gate is run once on the completed bytes by the fresh acceptance reviewer. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` |
| Diff hygiene | No whitespace errors or accidental edits outside the scoped implementation and result file. | `git diff --check` |

No live model, external network, sandbox smoke test, or MVP-3+ synthetic flow
is authorized by this task. JSON Schema or syntax checks may supplement the
runtime tests but cannot replace them.

## Stops and handoff

- Stop before implementation and return for the authorized two-way split if
  self-preflight estimates more than 35 tool calls or 90 minutes.
- Stop for ambiguous authority, overlap with user-owned changes in the allowed
  files, unsafe permission needs, a new shared module/framework, a new actor
  surface, or any requirement for arbitrary steps or a general workflow
  language.
- Stop and replan if the accepted S3-08 mechanical boundary cannot coexist
  with a truthful persisted cursor without redesigning its evidence contract.
- Treat the metadata budget as a checkpoint, preserve pre-existing user work,
  and do not update the governing rebaseline or task-actualization map.
- Next action: guided implementation after implementer self-preflight.
- Required follow-on: immediately after implementation or correction, hand
  the completed bytes to a fresh independent acceptance reviewer.
