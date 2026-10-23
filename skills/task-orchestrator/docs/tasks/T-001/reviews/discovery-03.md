# Task Review Discovery Report: T-001 — Capability follow-up

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, project-local installation |
| Coverage completeness | partial for capability qualification; delegation failure independently reproduced; other external/configuration boundaries remain blocked |
| Discovery iteration | 3, fresh independent follow-up to discovery-02 and acceptance-01 |
| Created at | 2026-10-22T20:35:13.388275+00:00 |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report | `skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-03.md` |
| Task brief | `../brief.md` |
| Verification / preparation | `../verification.md` revision 1; `../preflight.md`, including Decision context |
| Current submission | Five new task-local producer artifacts listed in section 7; existing ART-008 v1.0 and accepted investigation preserved |

This report publishes evidence only. It gives no acceptance verdict, approved
deferral or advancement. It applies only to the identified bytes. It does not
review or authenticate itself. The separate acceptance decision must distinguish
acceptance of a truthful investigation from readiness to implement T-002.

## 1. Discovery provenance

This fresh review session authored none of the reviewed artifacts or production
bytes. It performed static inspection and one authorized non-billable local
fake-provider inventory probe. Its sole repository write is this report. No
live actor/model qualification, external notification, production change,
installation refresh, plan update or T-002 implementation occurred.

Active instructions: `.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`
and its `references/discovery-report-template.md`. No global copy was used.
The current user authorized two separate review sessions; this is the first.
That authorization does not renew live model/actor probe permissions.

Current reviewed HEAD: `784a30c1e0d68c9e038945a1ec0db4d396cb5685`. Full worktree SHA-256 identities and
separate index entries are recorded in section 7. The five submitted files
remain untracked, with no index blobs. The old investigation's authority,
production source and preparation hashes still match discovery-02. Existing
review artifacts are historical evidence, not independent proof of new claims.

## 2. Confirmed finding

### F-01 [suggested P1] Selected disable configuration still advertises delegation

| Field | Evidence |
|---|---|
| Location | `skills/task-orchestrator/docs/tasks/T-001/probe_tool_inventory.py:17` and `:59`; launch flags at `:66`; request inventory extraction at `:84` |
| Trigger | Run the saved local fixture with all listed disabled features, including `multi_agent`, `multi_agent_v2`, and `multi_agent_v2_dynamic_tools`, while retaining the required code-mode host |
| Observed behavior | Both real CLI requests carry namespace `collaboration` with `followup_task`, `interrupt_agent`, `list_agents`, `send_message`, `spawn_agent`, `wait_agent`; the router also executes the requested nested inventory expression |
| Consequence | The required unavailable-delegation inventory is not established. The selected configuration cannot qualify actors for the intended local shell/native-patch-only launch contract |
| Evidence | Independent DISC-01: fixture exit 1; CLI exit 0; two requests; `inventory_observed=true`, `delegation_exposed=true`, `isolation_gate_passed=false` |
| Affected AC / invariant | AC-03/R2, AC-05/V-06; explicit owner-required isolation of unused write/delegation surfaces before successor readiness |
| Credible sibling surface | Both implementation and read-only reviewer profiles must exclude delegation; inherited plugin/MCP/connector/browser tools and startup hooks share the isolation requirement and cannot be cleared by this read-only empty fixture |
| Smallest corrective direction | Establish a supported control or runtime version that removes unused direct and deferred capabilities while retaining tested local execution; then qualify effective tool assembly and inherited startup configuration for both actor profiles. Preserve fail-closed handling |

This is a corroborated capability failure already disclosed by the producer,
not a claim that the evidence report hides a defect. No delegation call was
made. Exposure violates the required inventory condition; execution success,
privilege inheritance or actual ability to write through delegation was not
proved and is not asserted.

## 3. Completeness ledger

Stable V-01..06 and R1-trace/R2-level/R3-assume identities continue from
previous discovery. Their old investigation passes remain historical. New
suffixed rows separate missing capability evidence from honest documentation.
`pass` on a documentary row does not qualify the described runtime capability.

| Row ID | AC / explicit cases | Setup / oracle | Submitted evidence | Independent current evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01; controller-callable CLI vs coordinator tools; one selected bridge | Trace ART-008, plan and current worker; callable subprocess must be distinguished from interactive collaboration | CLI 0.163.0 through Python retained; fake provider is a probe only | Static trace of ART-008 selection, worker Popen and fixture override; no second backend implemented | pass for selection/disposition; no live provider parity inferred |
| V-01-model | AC-01/03; gpt-6.1-sol at low/medium/high | Three real completions with exact message, observed thread, no tools; do not infer reasoning quality from trivial prompt | Follow-up records 3 thread IDs, usage and successful completions; probe_model.py checks exit/turn/message/items | Current source matches requested model/efforts and stated prompt; raw historical event captures are not persisted in this packet; no new billable checks authorized | blocked for independent behavioral re-observation; capability owner supplies retained events or obtains explicit live authorization if further corroboration is required |
| V-02 / R1 | AC-02; first/same-key launch, live/terminal/unknown, missing receipt, replacement coordinator | Wrapper source and proposed contract; unknown must block relaunch | No new recovery support claim; accepted ART-008 retains downstream owners | Static source confirms starting before Popen, PID after spawn, existing-path refusal, live/ambiguous PID rejection; follow-up does not claim atomic launch | pass for unchanged honest contract; no new recovery qualification |
| V-03 | AC-03/R2; allowed implementation task writes, denied review/protected writes, unknown occupancy | Actual shell/native patch boundary required; context unknown must never become zero | 96 offline operations, 64 actor shell observations, native patch allow/deny details; owner fresh-session fallback | Static trace of CHILD/setup/parent assertions and actor flags; absent patch alone cannot prove attempted patch. Follow-up explicitly requires stderr diagnostics | pass for correct evidence limits and owner-decision handoff; actor qualification is split below |
| V-03-filesystem | AC-03/R2; create/modify/rename/delete, task/run/controller/skills/.git/.agents and symlinks | Real explicit permission profile with parent bytes/entries oracle | Prior 96 observations reported; source provides disposable controls and assertions | Source inspected; no offline permission rerun within this session's allowed probe scope; no persisted raw output independently inspected | blocked for current independent boundary observation; capability owner retains prior evidence, reviewers must not relabel it current proof |
| V-03-native | AC-03/R2; implementation task native create allowed, protected create denied; review both denied | Real actor patch and router rejection diagnostics plus parent filesystem | Prior two actor sessions and diagnostics summarized; helper checks task bytes/protected absence | Static trace confirms successful shell operation count and parent patch oracle; helper does not independently require each rejected patch attempt. No retained raw stderr/events available in packet | blocked for independent attempt/denial corroboration; producer raw diagnostics or separately authorized actor evidence needed; native modify/delete remains outside prior claim |
| V-03-context | AC-03; known vs unknown occupancy; frozen low/medium/high policy | Owner-approved fresh correction session when reliable occupancy unavailable; no unknown=0 | Explicit owner decision, no reliable meter claimed | Follow-up states fallback and threshold restriction; production constants/schema still old mapping, intentionally unchanged in this proof task | pass for bounded decision/contract; successor must synchronize all policy consumers before use, without mixing an active frozen run |
| V-03-tools-delegation | AC-03/R2; unused delegation unavailable with local execution retained | Real request additional_tools and executed nested inventory, empty fixture, read-only role | Producer reports delegation exposed despite disable flags | DISC-01 independently reproduces exposed collaboration namespace | fail; F-01; capability owner must resolve runtime control |
| V-03-tools-inherited | AC-03/R2; plugin/MCP/connectors/browser/computer use and inherited user/project/managed configuration | Disposable configured sentinels and effective direct/deferred inventories for both roles | Empty fixture shows no connector/browser/plugin action tool; expressly excludes inherited configuration | No hostile sentinel configured; HOME remains inherited; model-visible inventory cannot observe all hook side effects | blocked; capability owner must establish supported controls and sentinel proof, not filesystem or empty-catalog inference |
| V-03-tools-hooks | AC-03/R2; startup hooks unavailable, including configuration autoload | Explicitly configured harmless sentinel plus launch observation, both roles | `hooks=false`; no hook sentinel exercised | Static trace confirms flag only; no startup side-effect observation | blocked; capability owner owns hook isolation proof |
| V-03-tools-parity | AC-03/R2; same selected policy in implementation and review; actual provider compatibility | Both effective actor profiles and selected provider must retain qualified exclusions | Fixture uses only read-only sandbox and synthetic Responses service; producer explicitly excludes parity | DISC-01 observes CLI request/router only; fixture response usage is synthetic | blocked; capability owner owns profile/provider parity; further billable actor sessions need new authorization |
| V-04 / R3 | AC-04; exact-path commit, owner staged/unstaged preservation, before/after crash, unknown/unavailable commit | Existing disposable Git evidence and proposed durable intent/receipt; real finalization belongs to T-005 | No change to accepted primitive evidence or limits | ART-008 remains unchanged; no new implementation or stronger crash claim | pass for unchanged support/disposition; integrated qualification remains T-005 |
| V-05 / R3 | AC-04; relay success/failure/unknown; acknowledgement vs resolution; replacement/replay | Active coordinator chat only; persisted intervention precedes relay; owner reply grants only explicit authority | Follow-up gives six-step protocol; T-003/006 integration and proof outstanding | Static contract trace: unconfirmed relay unknown, seen not permission, silence never success, duplicate acknowledgement not repeated application | pass for explicit selected support contract; no end-to-end notification proof claimed |
| V-06 | AC-05; supported/unsupported/unverified; Q-001/002 and T-002..006 impacts | Cross-row documentary reconciliation; producer must not release successor | Both supplements explicitly retain T-002 blocker and no production/install changes | All five files are task-local; policy/model/context/intervention decisions recorded; delegation failure and remaining gaps explicit | pass for honest disposition; qualification ledger remains partial |
| R1-trace | R1; same key and spawn-without-receipt; actor cannot author provenance | Worker source versus ART-008 proposed receipts | Unchanged accepted contract | Current worker trace at :244–253, :353, :431–439; no atomic operation service added | pass for trace; T-002/003 own implementation and real recovery |
| R2-level | R2; actual selected boundary vs flags/fake argv; sibling external write surfaces | Evidence levels must not be substituted | Supplements separate filesystem, actor, inventory and inherited-config gaps | DISC-01 confirms local router call but not live service; external exposure detected independently of successful CLI exit | pass for evidence-level honesty; F-01 and blocked child rows persist |
| R3-assume | R3; integrated commit/notification success cannot be inferred | Unknown commit/delivery blocks dependency release | No new Git claim; chat protocol explicitly says no delivery/pilot test | Current documents keep unresolved integration at T-003/005/006; no messages sent | pass for unchanged limitations and revised chat contract |

## 4. Adversarial state and evidence checks

- Direct and deferred inventories were both considered. Request tools are in
  `input` items of type `additional_tools`; the executed `functions.exec`
  expression yields the nested `ALL_TOOLS`. A top-level `tools=null` or absent
  JSONL tool-call event is not a no-tools oracle.
- The fake service intentionally returns the inventory call despite the prompt
  asking for no tools. The real router executes it. Prompt compliance therefore
  supplies no isolation enforcement evidence.
- Both first and follow-up requests carry the same collaboration tools. The
  second request includes actual nested output, rather than a model-authored
  inventory assertion.
- No write/delegation call or configured hostile startup surface was exercised.
  No claim is made about successful delegation, all native-patch variants,
  hard links, configuration autoload, credential isolation, live provider parity
  or integrated process recovery.
- The probe's `isolation_gate_passed` boolean checks observation and delegation
  absence only. Even a future zero exit would not alone close the other required
  surface rows. Current exit 1 establishes a specific failure.

## 5. Independent probes and command results

All commands ran from the repository root. Read-only source reads and Git
identity commands are listed by purpose; DISC-01 is the sole behavioral probe.

| ID | Exact command / boundary | Result / signal | Side effects / gap |
|---|---|---|---|
| DISC-01 | `python3 -B skills/task-orchestrator/docs/tasks/T-001/probe_tool_inventory.py`, approved outside enclosing sandbox for loopback bind | exit 1 in 0.525s; CLI exit 0; 2 requests; inventory observed; delegation exposed; gate false | Disposable CODEX_HOME/workspace; local fake Responses only; credential-like environment keys removed; HOME retained; server shut down/joined, subprocess returned, temporary fixture removed |
| DISC-02 | `pgrep -af 't001-tools-\|probe_tool_inventory.py\|codex.*t001-tools'` | sandbox attempt exit 3, sysmond process-list unavailable; approved outside-sandbox retry exit 1 with no matches | No named fixture CLI/server process remains; no child actor was launched; subprocess stdout/stderr pipes reached EOF; server-thread assertion passed. No process-group ownership/recovery claim |
| DISC-03 | `git rev-parse HEAD`; `git status --short`; `git log -3 --oneline`; `git diff --cached --name-status`; `git ls-files --stage <reviewed paths>`; Python SHA-256 snapshot of reviewed files and `.git/index` | Section 7 records current separate HEAD/index/worktree identities | Read only; unrelated external Git activity preserved and excluded |
| DISC-04 | `nl -ba skills/task-orchestrator/docs/tasks/T-001/probe_tool_inventory.py`; `cat` of current five submitted artifacts, brief, verification, preflight, ART-008, acceptance-01, discovery-02; `rg -n` and `sed -n` of cited plan, map, worker, policy/schema sections | Current source and report traces support the ledger and F-01 | Static evidence only; not schema validation or behavioral qualification |
| NOT-RUN-01 | `probe_model.py low\|medium\|high`; `probe_permissions.py --actor-role implementation\|review` | not run; five prior authorized live sessions exhausted; current authorization covers review sessions only | Capability owner supplies raw retained evidence or obtains new exact live authorization if needed |
| NOT-RUN-02 | `probe_permissions.py` offline mode | not run; current delegated scope permits rerunning only saved inventory fixture; prior filesystem outcome remains producer-attributed | Capability owner / next authorized evidence pass |
| NOT-RUN-03 | Inherited MCP/plugin/connector/browser/computer-use and hook sentinel probes, both roles/provider parity | not run; no qualified control/fixture available in submission; delegation gate already fails | Capability owner establishes bounded control and fixture; live qualification requires separate permission |

Independent runtime fixture thread:
`01a1654f-60ef-7302-8651-18dacf6f4a38`. Synthetic service reported zero usage;
that is not billing telemetry or model availability evidence. Nested output:
`apply_patch`, `clock__curr_time`, `exec_command`,
`list_mcp_resource_templates`, `list_mcp_resources`, `read_mcp_resource`,
`view_image`, `write_stdin`. Generic MCP resource methods are exposed; no
configured external server action was invoked or qualified.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Gate / exact command | Capability-readiness aggregate: `not run`; no shell aggregate command added |
| Status | not run |
| Owner / stage | This fresh independent discovery, iteration 3 |
| Reason | Decisive targeted failure DISC-01/F-01 suppresses a success aggregate. Other required capability rows remain blocked for concrete non-gate reasons. A broad suite cannot remove exposed delegation |
| Current evidence | V-03-tools-delegation fails; blocked child rows in section 3; documentary disposition inspection is complete but is not a passed qualification gate |

The historical investigation reconciliation in discovery-02 and acceptance-01
is not copied as a current capability gate. It does not waive downstream or
conditional proof duties.

## 7. Scope and baseline comparison

The five submitted task-local paths are in scope. Six unrelated modifications
under `skills/idea-brief/` and `skills/project-delivery-plan/` existed on entry.
During this review an external actor staged the three idea-brief files, then
committed all six files as `784a30c` (`[IB][PDP] Plans content wording simplification`).
This session did not stage, reset, overwrite or commit anything. Initial HEAD
was `bb906f69dc29d7914bad2991391e65f4abbf2521`; the task and governing hashes
below are unchanged across this unrelated drift. The unrelated files are
excluded from reviewed scope. No overlap with the five task artifacts exists.

Exact pre-publication status:

```text
?? skills/task-orchestrator/docs/tasks/T-001/capability-follow-up.md
?? skills/task-orchestrator/docs/tasks/T-001/probe_model.py
?? skills/task-orchestrator/docs/tasks/T-001/probe_permissions.py
?? skills/task-orchestrator/docs/tasks/T-001/probe_tool_inventory.py
?? skills/task-orchestrator/docs/tasks/T-001/tool-isolation-evidence.md
```

Pre-publication `.git/index` SHA-256: `5720a2aec73d64b4571a405ccaf2363696a9af0c8f497013e04d5fa8b1e6bb83`.
Tracked reviewed artifacts have separate index blobs listed below. No submitted
untracked artifact has an index blob. Production, old accepted artifacts,
preparation, plans and existing tests have no task-owned diff.

### Reviewed worktree SHA-256 identities

| Path | SHA-256 |
|---|---|
| `skills/task-orchestrator/docs/tasks/T-001/capability-follow-up.md` | `40d9a98c4b2a1190a64c27c9d8891a321d305ce53063effc01e60e1cb55b60c5` |
| `skills/task-orchestrator/docs/tasks/T-001/probe_model.py` | `f44a09e97a63d7219ed69639d0cfdf8ac4cea4385197ed1a7c518ee27976e545` |
| `skills/task-orchestrator/docs/tasks/T-001/probe_permissions.py` | `c3358f0657d0e41a9ae7234092daea3aee3d5b0b6c3bce8c3166e67e0948673f` |
| `skills/task-orchestrator/docs/tasks/T-001/probe_tool_inventory.py` | `1c4a710c65cabf850913edf68c195fe50af6c8e68b95cb1b2cc45b84b347a1f3` |
| `skills/task-orchestrator/docs/tasks/T-001/tool-isolation-evidence.md` | `852d2e839e70ed9206b16f1ba6d2347891102f51797e6d3dec801df0a2771534` |
| `skills/task-orchestrator/docs/tasks/T-001/brief.md` | `3eaa6df3972c254764c1b92992a52dfdbc832f637abb8c89826ea56a994462c2` |
| `skills/task-orchestrator/docs/tasks/T-001/verification.md` | `1c7091c9651a85323a5b8acbe7ca3409eee15e307769ab5b53997fa7ff5ef483` |
| `skills/task-orchestrator/docs/tasks/T-001/preflight.md` | `99fbd591aee2b9dc7610c110d216376c44137ce4223b85ff9706569e86ab2e1e` |
| `skills/task-orchestrator/docs/tasks/T-001/harness-contract.md` | `3187faae4080b072e76b3304a872f5d2913468e2484d23569494d607a79f51ab` |
| `skills/task-orchestrator/docs/tasks/T-001/probe_local.py` | `aef89b60af9fc6fee8938006d4c48fa7402d1d5bee9f8eaaf214dd69d53c4a27` |
| `skills/task-orchestrator/docs/tasks/T-001/reviews/acceptance-01.md` | `630f4fab04982955a63584c11491f3125564c375946ad204ba44fbb565f51f24` |
| `skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-01.md` | `2d18cf671a6054a0b2ff221379d6eac885fd65b1184cee67b0fd5df0ae46b869` |
| `skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-02.md` | `edca62a20071c25e1b623db27c2454bded83c4ade9687b0e04af8be1a25816d9` |
| `skills/task-orchestrator/docs/direction-local-harness.md` | `0d17e2787866e1f4872705d6df2ec18e6289e15b97c42cf5e94b6196b3e17f2e` |
| `skills/task-orchestrator/docs/local-harness-orchestration-plan.md` | `98fab11ed34846bbe7c0596ea293be5908b763573ac8b0b988f3f4f5441452fd` |
| `skills/task-orchestrator/docs/local-harness-task-map.json` | `7e6a0a379c360c373934cfa88ee03dcdf32175aae4cc8ac1286cb7a73f9ad440` |
| `skills/task-orchestrator/docs/project-plan-review.md` | `9bc7cfeab8f956c7607cd1b915ed8c24613196b68e7b476474809d396ec4c8f0` |
| `skills/task-orchestrator/scripts/codex_worker.py` | `001a2f5fbf78a0532d342f71e9f8467f1d35073f0133868503d6bb15e70f3ba2` |
| `skills/task-orchestrator/scripts/controller_state.py` | `b3ebc6c5244982b33cacf563b70d46c01336c4a476e46940d75ee595dca2bb02` |
| `skills/task-orchestrator/scripts/controller_git.py` | `49f8685c5a33850250f70587f111d84fba40c33412e9ad11c1590ab13a42c905` |
| `skills/task-orchestrator/assets/flow-profile.schema.json` | `6c3c0f3e1c3ab05203a02b4c57adcaa81a6cf83ce0a73e3725b76ebc28f621d5` |
| `skills/task-orchestrator/assets/worker-result.schema.json` | `32effc1988202bb7b16280169c4914b7300d6632d22ac805827b517675fec9ac` |
| `skills/task-orchestrator/tests/test_codex_worker.py` | `30dabec6e379918c4f20bd00778997628c7363a16aecccbcc725606a50b7fdcd` |

### Reviewed index entries

```text
100644 8a331640e0fe5b21679fc619e22bbd62245dbb0e 0	skills/task-orchestrator/assets/flow-profile.schema.json
100644 b0c6f2120fe38c7232cdc8a9a20a4c42b06020e4 0	skills/task-orchestrator/assets/worker-result.schema.json
100644 8a290783469207e07105631356d0c43d3ef0f2d5 0	skills/task-orchestrator/docs/direction-local-harness.md
100644 0165cf0470b0a94d7aaf98868b14b5b7a874be71 0	skills/task-orchestrator/docs/local-harness-orchestration-plan.md
100644 e405d7a51cef029b6dc00c822420ab31d8fdd379 0	skills/task-orchestrator/docs/local-harness-task-map.json
100644 12e87a274db82c5eb0f4feba6eb6b637d97316c3 0	skills/task-orchestrator/docs/project-plan-review.md
100644 33828a15b1bfbe5250bf6df91d4d7aff75dc955a 0	skills/task-orchestrator/docs/tasks/T-001/brief.md
100644 a121951cc55e17dc2259f16e0729c52348e8f6a9 0	skills/task-orchestrator/docs/tasks/T-001/harness-contract.md
100644 6913e5d3cdf69512ac248db04fa1e93edf20ea23 0	skills/task-orchestrator/docs/tasks/T-001/preflight.md
100644 1a6e3c852abe2a0d2d1db239a8f73ed4c945e784 0	skills/task-orchestrator/docs/tasks/T-001/probe_local.py
100644 c3266bb9211806dc154774b8dd524028c2b25cc2 0	skills/task-orchestrator/docs/tasks/T-001/reviews/acceptance-01.md
100644 99b0383cb8ef2284e8dff594e816ba7849322165 0	skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-01.md
100644 74f097f28ea88239b6d6ae2e624a7b34ea29233a 0	skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-02.md
100644 18b16e9295fc15119668239cde47c46cb2fa8a6c 0	skills/task-orchestrator/docs/tasks/T-001/verification.md
100644 db8cafd5f044a008c0fd6ba570d30d84cb79beb9 0	skills/task-orchestrator/scripts/codex_worker.py
100644 8d6c3a0dacce0ce80767143315e2004e68cd7bbc 0	skills/task-orchestrator/scripts/controller_git.py
100644 03a233e9c0f581c0ff60665f89942589a7623481 0	skills/task-orchestrator/scripts/controller_state.py
100644 0b43d717cefc31623604271e204c6c2dfb338d0f 0	skills/task-orchestrator/tests/test_codex_worker.py
```

## 8. Questions, blocked work and residual risk

| Type / rows | Evidence or exact gap | Owner / next action |
|---|---|---|
| failure / V-03-tools-delegation | Current config exposes collaboration despite disabling all three named flags | Capability owner establishes supported runtime control/build; do not bypass isolation |
| blocked / V-03-tools-inherited, V-03-tools-hooks | Empty configuration and feature flags do not prove inherited external capabilities/hooks unavailable; HOME/global skill discovery persists | Capability owner qualifies explicit controls with harmless configured sentinels, both profiles |
| blocked / V-03-tools-parity | Read-only fake-provider fixture does not establish implementation role or live provider parity | Capability owner provides parity evidence within separately authorized scope |
| blocked / V-01-model, V-03-filesystem, V-03-native | Prior live/offline outcomes are producer summaries; their raw events/diagnostics are not retained in this packet; no current independent rerun authorized here | Acceptance must admit only stated evidence level; capability owner supplies retained captures or seeks bounded additional qualification if necessary |
| downstream / V-02, V-04, V-05 | Reservation/lifecycle provenance, finalization crash/index proof and chat integration/pilot remain planned, with no stronger new claims | T-002/003, T-005, T-003/006 respectively; no implementation occurs in this review |
| policy handoff / V-03-context | Owner-selected model/fresh-context/chat contract differs from old production policy | Successor synchronizes consumers and tests before use at a safe policy boundary; no active-install refresh here |

No request for external communication or a new live model session is made by
this report. Official links in producer reports were treated as cited background,
not independently re-fetched authority for current runtime behavior. The decisive
negative finding rests on the current local boundary observation.

## 9. Coverage completeness and next route

Coverage is partial for runtime capability qualification. Every material row is
listed, with one independently reproduced failure and concrete blocked rows.
The producer evidence correctly records these limitations; it does not complete
isolation or authorize T-002 implementation.

Next: separate fresh `task-acceptance-review` session consumes this report,
the five current artifact bytes/hashes, brief, verification revision 1,
preflight Decision context, ART-008, acceptance-01 and prior discovery context.
That session owns the readiness decision, without rerunning or taking ownership
of the suppressed discovery aggregate. It must receive F-01 and all six
blocked rows, plus unchanged downstream capability ownership.

## 10. Discovery continuation

- Iteration / current byte identity: 3; HEAD `784a30c1e0d68c9e038945a1ec0db4d396cb5685`; five submitted SHA-256 values in section 7; no production authorship by this session.
- Coverage rows: V-01 pass (selection/disposition only); V-01-model blocked (raw historical captures absent, no new live authority); V-02/R1 pass (unchanged contract only); V-03 pass (honest evidence limits); V-03-filesystem blocked (no current independent run); V-03-native blocked (raw attempt/denial diagnostics absent); V-03-context pass (owner decision contract); V-03-tools-delegation fail; V-03-tools-inherited blocked; V-03-tools-hooks blocked; V-03-tools-parity blocked; V-04/R3 pass (unchanged limitations); V-05/R3 pass (chat contract only); V-06 pass (honest disposition); R1-trace pass; R2-level pass; R3-assume pass.
- Finding IDs: F-01, suggested P1, delegation remains exposed.
- Finding/scenario continuity: old V/R investigation passes are historical; new producer model/permission claims remain producer-attributed. Current independent DISC-01 corroborates the inventory failure. Capability owner owns correction and missing evidence; user owns runtime/policy scope and new billable permissions; T-002/003, T-004, T-005, T-006 retain respective integration proof. Siblings: both actor roles, direct/deferred external tool assembly and non-model-visible startup hooks. No approved deferral or advancement is recorded.
- Preparation/context: brief SHA-256 `3eaa6df3972c254764c1b92992a52dfdbc832f637abb8c89826ea56a994462c2`; verification revision 1; ready preflight with Decision context; ART-008 v1.0; acceptance-01 distinguishes investigation from readiness; owner model/fresh-context/chat decisions and two-review authorization in current conversation.
- Reviewer regression: `python3 -B skills/task-orchestrator/docs/tasks/T-001/probe_tool_inventory.py` (loopback bind permission); current failure is expected evidence, not a passing isolation test. No test file added.
- Aggregate gate: not run, owned by this independent discovery; suppressed after decisive DISC-01/F-01; all blocked rows retain concrete owners.
- Next: the separately authorized fresh task-acceptance-review session decides current T-002 readiness from this packet; no T-002 implementation.

## Post-publication scope verification

Exact status after writing this report:

```text
?? skills/task-orchestrator/docs/tasks/T-001/capability-follow-up.md
?? skills/task-orchestrator/docs/tasks/T-001/probe_model.py
?? skills/task-orchestrator/docs/tasks/T-001/probe_permissions.py
?? skills/task-orchestrator/docs/tasks/T-001/probe_tool_inventory.py
?? skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-03.md
?? skills/task-orchestrator/docs/tasks/T-001/tool-isolation-evidence.md
```

Only the new discovery-03.md entry differs from the pre-publication status.
HEAD, index SHA-256 and all reviewed worktree hashes remained unchanged.
These checks establish publication scope, not report authenticity or runtime qualification.
