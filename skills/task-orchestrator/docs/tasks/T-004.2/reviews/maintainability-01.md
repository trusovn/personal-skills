# T-004.2 maintainability review 01

Verdict: **ACCEPT**. Fresh independent review of the submitted implementation;
no concrete introduced or materially worsened maintainability regression found.
No material finding IDs or unresolved maintainability warnings. This verdict is
not functional acceptance and grants no ART-009/completion authority.

## Provenance and reviewed bytes

Reviewer: fresh `/root/maintainability_01` session; authored no production,
schema, instruction, test, fixture or harness bytes under review. Executed the
project-local `.agents/skills/task-implementation-flow/task-maintainability-review/SKILL.md`,
its required `references/measurement-review.md`, and relevant project-local
`testing-discipline`; no source substitution or installation refresh.

Authority read: repository AGENTS.md, project-map/development, current contract
index and task-orchestrator record, architecture-map, T-004.2 brief/preflight/
verification and READY_FOR_REVIEW implementation report. Reviewed the actual
HEAD-to-worktree diff in controller.py, controller_state.py, actor-result schema,
test_actor_operations.py, SKILL.md and the new parent T-004/controller-contract.md.
The reference-only operator-guide correction is included as context. Existing
staged verification.md, preparation preflight.md, and unrelated untracked
.DS_Store files are not implementation authored by this task. README,
architecture-map and registry explanatory synchronization belongs to the next
registry stage, not a blocker here.

Frozen SHA-256 identity (paths relative to `skills/task-orchestrator/`):

| Asset | SHA-256 |
|---|---|
| scripts/controller.py | `508c8a81c755c8d0195ac882d2072e2e7c378e9478920b74088308f610fcdf79` |
| scripts/controller_state.py | `58cc1d2b61bb97e9c594303f57f57da7a2b8074a599c0e750b9d6610fbd20226` |
| tests/test_actor_operations.py | `47fd170d8e6939655fd426151a79f168ad3a54960ac2ac53a1c19d7d6643ff53` |
| assets/actor-result.schema.json | `9e51376d8b8e98767866ca0f88c977fcbba7c29c197da532132d06a23af99725` |
| SKILL.md | `399bbe8b3e59a7e7d4aaad3c64a48eea0dbf6a4ff321cc592c89360ffc919336` |
| docs/tasks/T-004/controller-contract.md | `8aa7b9103748f8cdb3b440a2249426168bff777eb3d451e9dd650dcf7120936e` |
| references/operator-guide.md | `a70c2232ed005cd1058a2a4500a410905fa230fb56120ed0ef5ce34da7b6bc57` |

The diagnostic directory is
`.quality/reports/T-004.2-maintainability-01-20261112/`.
`before.json` records exact initial Git status, real index hash and the above
asset identities; `after.json` records the final comparison. Only this new report
and new reviewer diagnostics were written. The report does not review itself.

## Original B, author I and independent R

All pairs are present locally at the original receiving repository
`/Users/mtrusov/work/skill-sources/personal-skills`; there was no transfer.
Both siblings were checked absent before creating R. No original or prior
comparison was overwritten.

- B JSON: `.quality/reports/T-004.2-preflight-20261112T165634690085Z/starting.json`
- B text: `.quality/reports/T-004.2-preflight-20261112T165634690085Z/starting.txt`
- I JSON: `.quality/reports/T-004.2-implementation-20261112/comparison-05.json`
- I text: `.quality/reports/T-004.2-implementation-20261112/comparison-05.txt`
- R JSON: `.quality/reports/T-004.2-maintainability-01-20261112/comparison-R.json`
- R text: `.quality/reports/T-004.2-maintainability-01-20261112/comparison-R.txt`

Reviewer command, from repository root (already prepared pinned interpreter;
no setup/install/download):

```sh
.quality/envs/Linux-aarch64-cpython-3.14.4-79dbf22b5bc1/bin/python .agents/scripts/measure_maintainability.py compare skills/task-orchestrator/scripts/controller.py skills/task-orchestrator/scripts/controller_state.py skills/task-orchestrator/tests/test_actor_operations.py --root . --baseline .quality/reports/T-004.2-preflight-20261112T165634690085Z/starting.json --output .quality/reports/T-004.2-maintainability-01-20261112/comparison-R.json
```

R: exit 0, complete, full_profile=true, comparison=compared; complexity 221
records and Ruff 376 records. Same CPython 3.14.4, Radon 6.0.1, Ruff 0.14.2,
checks, zero-limit Ruff collection, effective target settings and adapter hash
`c24932c841189b72725b50c86f20a2814c50a7a8903921a2ceb8b167b0f285df`
as B and I. Targets are advisory 10 complexity / 50 statements / 5 arguments.
Policy SHA-256 `f258d0e5a0dc070fc9ec33aa0dc000b1959fba9eebdd5cc20e1cb00178a654fb`;
Ruff configuration SHA-256 `a95813db8c5666acfbeae7e1734e7f1a16ad674d1798cc710853e0d3bbb2754b`.

Project identity is not inferred from the absolute path: repository HEAD is
`9afc120029ed85e10e56d4ac2fcce926db129d01`; all 12 B source snapshots hash to
their recorded hashes and exactly match the corresponding preserved HEAD blobs.
B originally covered scripts/tests/evals folders, including the existing empty
evals Python parent. All three actually changed Python files are covered; no
Python additions, deletions or module extraction require supplemental baseline.
Current files exactly match I and R hashes and the final submission manifest.
B correctly differs for edited files. New symbols have unknown before counts.
The old raw-review test was replaced with real collection plus retained fresh
raw-acceptance behavior; this is explicit scenario replacement, not a numeric
cross-symbol match. Untouched neighboring hotspots are not attributed to T-004.2.
Documentation/JSON schema have no Python metric; reviewed semantically instead.

## Required rationale dispositions

Every row below references the independently corroborated B-to-R values, which
also match I05. Each disposition agrees with the author's retained-structure
rationale after reading the changed responsibility and immediate collaborators.

| Affected responsibility / metric, B → R | Independent disposition, cohesion and bounded alternative cost |
|---|---|
| `check_collection`, CC unknown → 18 | Retain. One locked, collector-owned execution transaction makes exact-assignment/session validation, exclusive replay/intent, execution and post-workspace inspection visible in order. Context/artifact responsibilities already have narrow helpers. Extracting replay versus execute would pass the same authority tuple and obscure the no-relaunch boundary; it would not remove a separate reason to change. |
| `_admit_collection`, CC unknown → 25 | Retain. Identity/independence, current rerun disposition and coverage precedence jointly determine one admitted evidence result. Shape validation and finding merge are separately owned. A status-policy helper is plausible, but presently separates precedence from the evidence that determines it and adds navigation without a second consumer. Publication stays under the existing locked admission path. |
| `_reservation_options`, CC 25 → 29 | Retain. Ordered prerequisite and occupancy guards define the coordinator's next action in one owner; collection adds the adjacent prerequisite before acceptance. A transition table would still require guard ordering and exceptional exhaustion/readiness rules. Keeping those rules visible costs less than reconstructing table callbacks. |
| `status_run`, CC 15 → 21 | Retain. One read-only projection applies candidate and collection freshness while preserving occupied/exhausted precedence. Collection artifact validation is extracted. A further projection helper would mostly move cloning and precedence branches while splitting the status owner. |
| `reserve_operation`, CC 32 → 33 | Retain. The added current-collection guard belongs to the existing atomic acceptance-reservation prerequisites. It reuses `_validate_current_collection`; extracting a second reservation path would duplicate request/replay/accounting policy. |
| `reserve_operation`, arguments 7 → 7 | Retain the materially edited existing breach. Explicit public reservation inputs remain the established interface and preserve authority visibility. A request object solely to reduce the count changes that API and hides rather than simplifies the protocol. |
| `launch_operation`, CC 12 → 13 | Retain. Collector context is selected at the same controller-owned authority/launch boundary; its construction is already a helper. Moving it into transport couples generic process ownership to candidate/check semantics. Another dispatcher adds little beyond this one stage test. |
| `_admit_actor_outcome`, CC 10 → 11 | Retain. The one semantic stage dispatch preserves the single admission owner and delegates all collection detail. A registry for one additional branch adds indirection and a registration owner without localizing another concrete variation. |
| `observe_operation`, CC 15 → 18 | Retain. Unresolved subordinate reruns must gate terminal admission at the same observed-ownership boundary. Detection/path ownership is extracted. A second observer would duplicate liveness, locking and idempotent publication rules. |
| `ActorOperationsTest.test_collection_v07_files_configuration_index_head_and_repointing`, CC unknown → 11 | Retain. Finite named variants keep decisive real Git/filesystem mutations adjacent to a shared stale-evidence oracle. Isolated cases retain separate roots. Callback dispatch factories would obscure each mutation and add a single-consumer fixture layer. |
| `build_parser`, statements 53 → 53 | Retain the materially edited existing breach. One extra command name uses the existing producer-registration loop and shared CLI handler. A parser module split would add ownership/navigation without simplifying this bounded registration change. |

No other actually affected above-target native metric exists. Growth through or
at the targets is informational. Equal numbers on untouched hotspot siblings do
not create cleanup duties. New helpers retain explicit dependencies and no
metrics-only extraction was introduced. Missing native counts remain unknown.

## Semantic maintainability review

The representative collection path remains easy to locate: reserve/launch adds
frozen context; `check_collection` executes through the existing verification
runner; observe delegates to one collection admission; publication records
findings/evidence and clears the actor slot. State validation owns report shape;
controller owns candidate/session authority, rerun identity and publication;
transport remains generic. Pure finding reconciliation and shape validation are
independent of provider I/O. No new sibling dependency or test/runtime edge was
introduced.

Controller-owned `.rerun` path derivation has one helper. Repeated checks at
launch, execution, admission and later freshness queries are legitimate different
observation boundaries. The ordinary verifier and collector share the planning/
execution seam while retaining different reservation/publication semantics. Their
small repeated policy preparation is not sufficient evidence of an introduced
material coordination regression. Failure branches retain operation identity,
execution/log paths and underlying causes; unresolved terminality has a distinct
blocker rather than silent retry. Names and units communicate the new behavior.

Significant test architecture was reviewed, including generated actor script,
producer setup wrapper, independent-case cleanup and process-interruption hooks.
Tests extend the existing fixture owner rather than introduce a parallel harness.
Setup wrappers still call real initialization; actors control responses/edits and
invoke public production reruns. The new tests observe durable evidence,
execution counters, product bytes, findings/history, refusal and replay, rather
than reconstruct admission with a second algorithm. Isolated roots and bounded
polling/file events keep concurrency scenarios understandable. The explicit
future-ART-009 disposition fixture remains marked; real failed-check correction
starts from actual production admission. The old collection-raw-claim scenario
is replaced because that boundary is now implemented; fresh acceptance-session,
raw-claim and no-completion assertions remain in its successor test. Full
functional adequacy and finite scenario acceptance belong to discovery.

The declarative actor schema repeats the three fixed coverage shapes but keeps
one closed collection envelope aligned with the runtime validator. Introducing a
schema abstraction solely for those three declarations is not a material design
improvement. SKILL, operator guide and parent handoff expose the actual single
admission seam and distinguish collection from future semantic acceptance.

## Native evidence and limits

No separate command registry is present/required; AGENTS.md and development.md
are the command authority. Exact commands below are from repository root.
Reviewer-owned architecture evidence is current for the complete governed scope,
not merely the three measured Python files. `architecture-identity.json` records
the checker/policy and every runtime file in its canonical discovery scope.

| Native command | Governed scope / policy and owner | Evidence / current disposition |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Entire root scripts/tools and all skill runtime scripts; mandatory CLEAN, no baseline; maintainability reviewer before handoff | Reviewer executed, exit 0, 4 pass/no skips; diagnostic `architecture.log`. Import scope and frozen bytes unchanged through report. No hard violation. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py` | Owning actor/process/lifecycle suite; implementation then discovery | Author `actors-submission.log`: 50 pass/no skips against final submitted Python; I05/final manifest/current hashes match. Not rerun merely to duplicate the functional owner's proof. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_state.py` | Owning state suite; implementation then discovery | Author `state-final.log`: 45 pass/no skips; state bytes unchanged. Discovery validates functional sufficiency. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | Whole orchestrator; mandatory after targeted success; implementation then discovery | Author `orchestrator-final.log`: 264 tests, 6 failures/7 errors/20 skips; not green qualification. `baseline-failures.log` reproduces the same 13 cases on preserved unmodified HEAD, whose B source identity was independently verified. Same runtime; final test-input refinements were later covered by the final actor suite. No claim that the earlier whole-suite test-byte inventory equals the final one. |
| `python3 tools/check_contracts.py --root .` | Whole registry structural check; registry-updater then discovery | Author `contracts-pre-registry.log`: 8 subsystems/35 refs. Structure only; changed collection contract/reference synchronization is still owed in its designated next stage. |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py` | Whole repository aggregate for cross-cutting change; implementation then discovery | Author `aggregate-final.log`: 7 checks, 1 failed, same orchestrator boundary; 32 root skips plus 20 orchestrator skips. Profile constituent matched 112 managed paths. This is retained failure/skip evidence, not a successful aggregate or final-byte full behavioral qualification. |

Author log paths in the table are under
`.quality/reports/T-004.2-implementation-20261112/`; exact commands and checked-byte
limits are retained here rather than converting an aggregate into a pass. No new
functional test run, live/provider qualification or permission expansion occurred.
Baseline Linux/macOS sandbox failures and skipped containment/analyzer scenarios
remain visible for discovery/acceptance; no architecture exception is inferred.
The mandatory maintainability architecture proof and all required metric/rationale
obligations are complete. The broader functional qualification limits are owned by
discovery/acceptance, not silently cleared by this verdict.

## Outstanding route

First outstanding stage: designated `task-contract-registry-updater` (root owns
collection/ART-002/ART-006/IF-003 and discovery-reference synchronization, then
explicit index regeneration). Next: fresh independent `task-review-discovery`
for these submitted bytes and retained native limitations; then separate
`task-acceptance-review`. T-005 remains downstream after this task's acceptance.
No downstream stage was executed, delegated or awaited by this reviewer.

If runtime, significant test/harness, schema or other reviewed implementation
bytes change, this verdict is stale for affected scope and must re-enter the
required architecture/fresh maintainability duties before the remaining route.
Reference/registry-only synchronization has its own stage and does not invalidate
unchanged runtime/test evidence.
