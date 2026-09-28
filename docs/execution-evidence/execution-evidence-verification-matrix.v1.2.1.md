# Execution Evidence v2 — Verification Matrix

**Design-pack version:** 1.2.1  
**Evidence schema target:** 2  
**Status:** Contract-closure checklist  
**Authority:** non-authoritative execution aid subordinate to the v1.2.1 design pack.

This matrix maps approved requirements to focused verification. It does not add evidence categories, architecture, or implementation scope.

## Verification principles

- Prefer deterministic unit/integration tests over broad workflow tests when they prove the same invariant.
- Do not add production instrumentation solely to make a test easier.
- Reuse `workflow_version.py`, `runtime_context.py`, and the existing Git snapshot mechanism rather than duplicating them.
- Missing optional values stay unavailable; tests must not encourage guessing/backfill.

## Storage and identity

| ID | Requirement | Expected verification |
|---|---|---|
| S-01 | Evidence root outside worktree | resolves under `<git-dir>/personal-skills/evidence/v2/` |
| S-02 | Blob deduplication | identical bytes produce one content ref |
| S-03 | Blob identity is content-based | different bytes produce different refs regardless of filename |
| S-04 | Immutable conflict rejected | same logical ID + different payload fails |
| S-05 | Identical immutable write reusable | same ID/payload is idempotent |
| S-06 | Atomic writes | no partial visible record |
| S-07 | Path-independent identity | equivalent inputs under different absolute roots yield same logical ID |
| S-08 | ProjectSnapshot identity deterministic | same explicit manifest yields same ID |
| S-09 | TaskRevision identity covers semantic revision | changing planning/estimate/relation/identity-bearing provenance changes ID |
| S-10 | TaskRevision not keyed only by brief bytes | same brief + changed semantic planning content yields new ID |
| S-11 | TaskRevision can exist without attempt | produced/unexecuted revision persists |
| S-12 | Association immutable | conflicting rewrite rejected |
| S-13 | Collector identity present | schema version + deterministic collector fingerprint |
| S-14 | Knowledge-status distinctions survive | unknown != zero/false/not-applicable |
| S-15 | Canonical serialization stable | key-order/insignificant JSON formatting does not perturb equivalent identity payloads |
| S-16 | Omitted vs null not silently collapsed | distinction remains unless constructor explicitly normalizes field |

## ExecutionAttempt lifecycle

| ID | Requirement | Expected verification |
|---|---|---|
| A-01 | PRE-RUN freezes at begin | later PRE-RUN mutation rejected |
| A-02 | Active attempt may grow execution facts | checks/execution updates append while PRE-RUN stays fixed |
| A-03 | Finish records POST-RUN and finalizes | complete record becomes immutable |
| A-04 | Recovery is factual | uncertain interval is not invented |
| A-05 | Finalized attempt cannot mutate | update/append rejected |
| A-06 | Checks remain inline | no separate check namespace/model required |
| A-07 | Check command runs once | wrapper records one actual execution |
| A-08 | Optional telemetry accepted | caller-supplied mapping can be stored |
| A-09 | Telemetry absent is valid | ordinary attempt still valid |
| A-10 | Optional conditions accepted | supplied PRE-RUN mapping retained |
| A-11 | Conditions absent is valid | ordinary attempt still valid |

## Existing authoritative mechanisms

| ID | Requirement | Expected verification |
|---|---|---|
| I-01 | Workflow identity reused | attempt value matches canonical workflow-version result |
| I-02 | Trusted runtime identity reused | runtime context is canonical actual identity |
| I-03 | No self-report fallback | absent trusted context remains unavailable |
| I-04 | PRE-RUN repository state reconstructable | dirty/untracked fixture captured with existing Git snapshot mechanism |
| I-05 | POST-RUN repository state reconstructable | add/change/delete fixture captured with same mechanism |
| I-06 | Derived patch metrics not mandatory | raw state sufficient; no required collection-time metrics |

## Task and profile semantics

| ID | Requirement | Expected verification |
|---|---|---|
| T-01 | Direct task is first-class | exact direct request produces valid attempt |
| T-02 | Direct task needs no fake formal artifacts | no manufactured task ID/brief/project plan |
| T-03 | Formal task references TaskRevision | no duplicate embedding of formal artifacts |
| T-04 | Planning and execution ProjectSnapshot roles distinct | independent refs preserved |
| T-05 | Planner recommendation distinct | preserved on TaskRevision |
| T-06 | Intended launch profile distinct | preserved on attempt PRE-RUN |
| T-07 | Actual runtime distinct | trusted runtime value preserved separately |
| T-08 | Assignment provenance optional/factual | supplied retained; absent remains unknown |
| T-09 | Retry/correction relationships do not collapse attempts | linked attempts remain separate records |

## Planner/decomposition integration

| ID | Requirement | Expected verification |
|---|---|---|
| P-01 | Explicit relevant project artifacts may become ProjectSnapshot | capture/reuse succeeds |
| P-02 | Formal task artifacts may become TaskRevision | capture/reuse succeeds |
| P-03 | Already-produced planner context survives | supplied fields retained with provenance |
| P-04 | Missing planner fields stay missing | no inference/backfill |
| P-05 | Planner estimates remain predictions | persisted with producer provenance |
| P-06 | Composite parent survives without execution | parent revision persists with no attempt |
| P-07 | Child relationships preserved | decomposition links survive |
| P-08 | Evidence failure non-fatal to planning | valid brief still produced |
| P-09 | No second parser/LLM | static review confirms explicit known values only |

## bounded-task-implementer integration

| ID | Requirement | Expected verification |
|---|---|---|
| B-01 | Standalone guided task can begin evidence before edits | direct fixture succeeds |
| B-02 | Formal task reuses TaskRevision | revision referenced |
| B-03 | Begin precedes implementation edits | ordering proven |
| B-04 | Known conditions may be passed | retained when available |
| B-05 | Missing conditions/telemetry harmless | task proceeds |
| B-06 | Deterministic command not duplicated | one execution |
| B-07 | Normal completion finalizes attempt | factual closure + POST-RUN |
| B-08 | Interruption/failure factual | correct closure without invented success |
| B-09 | Missing evidence tooling non-fatal | ordinary task semantics remain valid |
| B-10 | Broken evidence tooling non-fatal | task continues; no fake evidence |
| B-11 | Attempt ID retained for review handoff | reliable ID passed when review follows |

## Acceptance association

| ID | Requirement | Expected verification |
|---|---|---|
| R-01 | Reliable attempt ID creates `acceptance_review` Association | immutable association written |
| R-02 | Durable report content-addressed when present | artifact ref retained |
| R-03 | Factual verdict/status preserved | no synthetic success score |
| R-04 | Reviewer provenance preserved | producer context retained |
| R-05 | Missing attempt ID is not guessed | review works; no association |
| R-06 | Association does not mutate finalized attempt | attempt bytes unchanged |
| R-07 | Existing independent-review semantics preserved | regression coverage remains green |
| R-08 | Maintainability review unchanged | no integration in this scope |

## Installation and portability

| ID | Requirement | Expected verification |
|---|---|---|
| X-01 | Approved tool set works under `.agents/scripts/` | project-local fixture succeeds |
| X-02 | `.agents/` may be ignored | ignored installation still works |
| X-03 | Evidence remains outside worktree | records under Git metadata root |
| X-04 | Direct task needs no planning files | valid installed attempt |
| X-05 | Missing optional evidence tooling non-fatal | skill remains executable |
| X-06 | Workflow/runtime helpers remain shared authorities | no duplicate implementations |
| X-07 | Fresh-agent docs sufficient | clean-context installation/discovery works |

## Regression / scope protection

| ID | Requirement | Expected verification |
|---|---|---|
| G-01 | `test_workflow_version.py` green | PASS |
| G-02 | `test_runtime_context.py` green | PASS |
| G-03 | migrated `test_run_evidence.py` green | PASS |
| G-04 | new evidence-store tests green | PASS |
| G-05 | new evidence-record tests green | PASS |
| G-06 | affected planner/implementer/acceptance evals green | PASS |
| G-07 | legacy v1 evidence untouched | no migration/deletion |
| G-08 | no mandatory runner telemetry instrumentation | static review PASS |
| G-09 | no adapter framework | static review PASS |
| G-10 | no collection-time feature/scoring system | static review PASS |
| G-11 | no task-orchestrator implementation change | diff review PASS |
| G-12 | no maintainability-review integration | diff review PASS |
| G-13 | standard-library-only default retained | any new third-party runtime dependency requires explicit separate justification |
| G-14 | CLI-level single-active-worktree behavior not leaked into storage abstraction | `EvidenceStore` addresses attempts by ID and has no global active-attempt invariant |

## Minimal end-to-end closure scenarios

1. **Standalone direct task** — direct request → begin → one check → repo change → finish; no formal artifacts manufactured.
2. **Formal planned task** — ProjectSnapshot → TaskRevision → ExecutionAttempt; planning/intended/actual profile roles remain separate.
3. **Decomposition without parent execution** — decomposed parent + child revisions; execute one child; parent remains visible without attempt.
4. **Acceptance association** — finalized attempt → independent acceptance review → immutable association; attempt unchanged.
5. **Best-effort degradation** — ordinary guided task with evidence tooling absent/broken still remains a valid implementation workflow.

## Closure rule

Execution Evidence v2 is complete when every current-scope matrix row is PASS or legitimately not applicable under the approved design, and durable evidence can answer the design pack's PRE-RUN, EXECUTION, POST-RUN, provenance, relationship, decomposition, and collector-semantics questions without transient agent memory.

Do not block closure on S3, remote sync, legacy migration, dataset export, patch metrics, feature extraction, similarity/embeddings/RAG/ML, routing, runner telemetry scraping, maintainability-review integration, or task-orchestrator implementation redesign.
