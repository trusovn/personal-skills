# Task Brief: T-002.3 — Revise approved inputs safely and prove the controller guards

## Outcome

Let an explicitly authorized owner revision replace task inputs at a safe
boundary. Atomically change their identity and the state version, require fresh
preflight and invalidate affected evidence. Prove the combined T-002 controller
contract locally so T-003 can connect sbx actors without guessing its interface.

## Direction trace

- Direction contribution: changed task authority cannot reuse evidence for old work.
- User-observable effect: status explains the revision, retained correction count
  and fresh evidence needed before work can continue.
- Why now: this closes IF-001 after policy and reservations exist; T-003 needs
  their composed contract.
- Decisions used: [plan](../../local-harness-orchestration-plan.md), ART-001 revision,
  IF-001 and FLOW-003; [parent](../T-002/brief.md), including approved shared repair budget.
- New direction decisions required: None.

Status: `ready`
Task kind: `executable`
Brief revision: 1
Profile: `guided`; predecessor acceptance and readiness still pending.

```yaml
agent_tier: strong
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / 60k context
```

## Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Estimate: 15 agent calls, 40 implementation minutes, medium
confidence. Intended profile: `strong/medium`. Policy result: `fits`;
triggered limits: none; decomposition override: none. Existing immutable-flow
publication and lock fixtures provide the local pattern; excludes separate review.

## Authority and scope

- Authority: [parent](../T-002/brief.md), P-01..06;
  [plan](../../local-harness-orchestration-plan.md), IF-001, ART-001/002/004,
  INV-001/002/003/005/008 and FLOW-001/003.
- Dependencies: accepted T-002.1 and T-002.2 and their implemented contract notes.
- Consumes: frozen authority, status, reservations and their existing ledger.
  Produces: authorized revision through IF-001 and final composed T-002 handoff.
- Allowed changes: controller/state scripts, affected schemas and owning
  state/controller tests/fixtures under `skills/task-orchestrator/`; implementation
  reports here; final `../T-002/controller-contract.md` successor reference.
- Excludes: live adapter, production preflight/collection/acceptance admission,
  completion gate/publication, crash-recovery service, automatic commits,
  tracker migration, official plan edits and active-install changes.

## Work and acceptance criteria

- **AC-01 — Authorized revision:** accept an explicit owner-authorized material
  input/policy revision only against the current expected version, with no
  reserved/running/unknown operation and a task that is not completed. Bind
  authority/provenance to the requested change; acknowledgement or actor prose
  is insufficient. Atomically publish the new ART-001 identity and increment
  the ART-002 state version, preserving previous input/operation/evidence history
  and the correction count. Revalidate revised inputs against mandatory policy;
  authority cannot make an invalid payload pass validation.
- **AC-02 — Invalidation:** admitted revision clears readiness and invalidates
  affected candidate, check, collection and acceptance eligibility. No old
  input-bound evidence becomes current by changing a pointer. Fresh preflight
  is required before implementation. Historical record contents remain intact;
  T-003..005 own admission of new runtime/semantic evidence.
- **AC-03 — Safe refusals/publication:** unauthorized, acknowledgement-only,
  stale-version, malformed, reserved/running/unknown-operation and completed-task
  requests preserve authoritative state/version, policy, count and task files.
  During an interrupted publication, readers see coherent old or new authority,
  or a precise conservative stop, never mixed eligible identities. Replay cannot
  publish the same revision twice or reset budget/history. This requires local
  publication safety, not an automatic recovery service.
- **AC-04 — Composed proof:** through public controller operations on disposable
  repository/run files, freeze inputs, reserve preflight, exercise readiness
  guards, reserve cycle-zero implementation and shared corrections, reload,
  revise safely, reject stale evidence and require fresh preflight. Prove a
  fourth correction cannot be authorized after revision, legacy routes cannot
  bypass required stages, and no operation declares completion while actual
  successor evidence is missing. Test-only setup may supply not-yet-implemented
  terminal/readiness/check/review records; label this boundary explicitly.
- **AC-05 — Successor handoff:** publish `../T-002/controller-contract.md` with
  actual callable names/payloads, schemas, state/version and operation rules,
  policy/input identities, revision authority, counting/replay rules, refusal
  examples, exact local verification results and T-003/004/005 ownership seams.
  Include required re-preflight after environment repair. Identify unrun sbx/model
  proof; do not claim runtime provenance or first useful proof completion.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R1: revision is authorized and safe | Authorized idle/noncompleted; unauthorized/acknowledgement-only; stale version; reserved/running/unknown; completed; malformed policy | Public revision result plus authoritative/file byte comparisons; only valid revision changes identity/version | Focused real-file revision cases | Attempt revision after third correction and during unknown operation | Implementer targeted/owning; fresh discovery corroborates |
| R2: old evidence never follows new authority | Current readiness/candidate/check/collection/acceptance references; changed brief, verification or policy; retained history/count | Current eligibility cleared; old contents preserved; new implementation blocked pending fresh preflight | Seed explicit historical fixtures; execute real revision and status/reserve | Try old readiness/evidence references after revision and reload | Implementer targeted/owning; fresh discovery corroborates |
| R3: publication/replay stays coherent | Before publication; after revision content exists but before authoritative pointer; after authoritative publication before response; replay/reload | Coherent old/new identity/version or conservative stop; no duplicate revision or budget reset | Reuse fault-boundary publication fixtures | Independently retry interrupted revision and inspect eligibility/history | Implementer targeted/owning; fresh discovery owns combined aggregate gate |

## Expected contract impact

Complete IF-001 by extending the same ART-001/002 controller authority boundary.
Consolidate T-002.1/002.2 notes into the final parent contract without replacing
their evidence. No current contract registry exists; if one is introduced by
other authorized work, route synchronization to its owning installed workflow.
Do not claim ART-006/009 semantic admission or IF-004 completion is implemented.

## Verification and readiness

Verification reasoning: **separate** — atomic publication, evidence invalidation
and the composed lifecycle need distinct observable oracles. Use
[verification.md](verification.md) revision 1. Readiness route: **standalone
guided preflight** after accepted predecessors; confirm their exact interfaces,
current authority and fixture reuse. This package supplies no ready preflight.

Implementer runs focused revision/composition tests, then the owning state and
controller modules. Fresh independent discovery owns the final broader gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
```

Keep correction implementation on the targeted/owning gates while failures
remain. The final reviewer decides aggregate execution after they pass and
reports any environment limitation. No live/networked check is authorized here.

## Stops and handoff

Stop for changed authority, material predecessor mismatch, owner-work overlap,
permission expansion or a publication oracle requiring new shared infrastructure.
Use existing lock/atomic storage patterns. Preserve installations and old runs.

Next: accepted predecessors, ready standalone preflight, implementation, then
applicable required architecture/maintainability/registry stages, fresh independent
`task-review-discovery` and a separate `task-acceptance-review` decision immediately
after implementation/correction. The parent closes only after all leaves pass
their required routes. Then hand the actual controller contract to T-003;
do not launch actors as part of this leaf.
