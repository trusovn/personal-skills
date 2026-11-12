# T-004 controller contract for T-005

T-004.2 implementation handoff, READY_FOR_REVIEW. This consolidates the accepted
[T-004.1 producer interface](../T-004.1/controller-contract.md) with collection
admission. Independent review and acceptance remain separate. T-005 must not infer
acceptance or completion from this document or a passed collection.

## Public operations and sequence

Import `scripts/controller.py`; paths are `pathlib.Path`, payloads are JSON values.
Initialization, frozen input revisions, reservation accounting and observed actor
transport retain [T-002](../T-002/controller-contract.md) and
[T-003](../T-003/controller-contract.md).

| Callable | Meaning |
|---|---|
| `inspect_candidate(run_dir, operation_id)` | Inspect the latest admitted complete terminal implementation/correction; publish current scope-checked candidate. Returns passed, blocked or refused. |
| `check_candidate(run_dir, assignment, *, timeout_seconds)` | Execute the exact active reserved verify assignment once. Return passed, failed, not_run, stale, blocked or refused with retained records. Ordinary verify reservation and replay retain T-004.1 semantics. |
| `check_collection(run_dir, assignment, *, timeout_seconds)` | While the exact launched collector owns the active operation and an adapter-observed session exists, run one new full frozen check plan. This is a collector-owned subordinate command, never a second actor reservation. |
| `reserve_operation(...)` | Reserve semantic_review/review_collector after current passed checks, or acceptance/acceptance_reviewer after current passed collection. Evidence-only verify/recollection is permitted without charging corrections. |
| `launch_operation(...)`, `observe_operation(...)` | Launch a fresh collector through the existing bridge; terminal observation is the sole collection admission/publication path. Acceptance transport remains raw only. |
| `status_run(run_dir)` | Expose current candidate/check/collection evidence, findings, history, count, ownership, blockers and next actions without admitting anything. |

CLI forms:

```sh
python3 <skill>/scripts/controller.py inspect-candidate --run-dir RUN --operation-id PRODUCER
python3 <skill>/scripts/controller.py check-candidate --run-dir RUN --request VERIFY_ASSIGNMENT.json --timeout-seconds 30
python3 <skill>/scripts/controller.py reserve --run-dir RUN --expected-version VERSION --task-id TASK --stage semantic_review --role review_collector --operation-key UNIQUE
python3 <skill>/scripts/controller.py launch --run-dir RUN --request COLLECTOR_ASSIGNMENT.json --timeout-seconds 300
python3 <skill>/scripts/controller.py check-collection --run-dir RUN --request COLLECTOR_ASSIGNMENT.json --timeout-seconds 30
python3 <skill>/scripts/controller.py observe --run-dir RUN --operation-id COLLECTOR
```

`check-collection` is called by the collector after its session is observed. Save
only the returned assignment object in the request file. Positive finite timeout
is mandatory. Producer CLI exit 0 covers passed, failed and stale evidence;
blocked/not_run/refused exit 1. This is command delivery, not acceptance.

## Assignments, result schema and admission

Assignments retain the exact T-002 fields and recursive JSON types. Collection
assignments have stage semantic_review, role review_collector, can_change_files
false, no repair authority and the current candidate/input/policy/flow identities.
Prompts include frozen brief/verification/scope/checks, policy, current candidate
and controller-produced check evidence, prior findings/dispositions/history,
requirements/behavior/code-quality coverage, project-local installed-skill
resolution rules and the separate maintainability/registry/discovery/acceptance
route. Frozen task and repository instructions determine stage applicability.
Missing mandatory capability must be reported blocked; source instructions do not
establish installation. These instructions and capability attestations do not
prove semantic review quality or enforce filesystem isolation.

`assets/actor-result.schema.json` adds collection only to semantic_review results.
Other actors retain assignment, session_id, status, summary and readiness. The
collector must echo its exact assignment and explicit adapter-observed session_id,
use status complete/blocked/failed/needs_input, readiness null, and supply:

```json
{
  "coverage": {
    "requirements": {"status": "passed", "evidence": "requirement inspection evidence"},
    "behavior": {"status": "passed", "evidence": "behavior inspection evidence"},
    "code_quality": {"status": "passed", "evidence": "quality and applicable review capability evidence"}
  },
  "gaps": [],
  "findings": [],
  "rerun_path": "collection-checks/operation-NNN.rerun.json"
}
```

Coverage status is passed, blocked or not_run. Gaps are explicit nonempty strings;
findings is an explicit array. Each finding has exactly id, evidence (nonempty
string array), requirement, context and exposure (nonempty strings). Duplicate IDs,
missing fields, invented provenance, acceptance decisions and disposition/deferral
authority are rejected. No collector creates an ART-009 decision or tracker entry.

Admission requires actual successful terminal adapter observation, exact assignment,
current input/policy/flow/candidate and current Git/filesystem identity. Collector
sessions matching any implementation or correction session fail independence.
The owned rerun must match collector operation, session, candidate and inputs;
controller command record and stdout/stderr digests are revalidated. A copied
implementer pass or replayed ordinary verifier executes nothing new and cannot
cover collection. Actual failed checks override a claimed pass. Complete current
coverage enables a separate acceptance reservation even when findings remain;
that reviewer decides their significance and dispositions.

## Retained artifacts and replay

Existing candidates/<sha256>.json, checks/<operation>.json, check intents,
verification execution records and per-command logs retain T-004.1 binding.
Collection adds:

- `collection-checks/<collector>.rerun.intent.json`: exclusive rerun identity,
  assignment, observed session, candidate, frozen plan/setup and timeout;
- `collection-checks/<collector>.rerun.json`: command result and execution digest;
- `verification/<collector>.rerun.turn-001.execution.json` and command logs:
  distinct command identity and actual controller-run check outcomes;
- `collections/<collector>.json`: admitted assignment, adapter observation,
  explicit report, truthful status and blocker;
- ART-002 `evidence.semantic_review`: current identity, artifact path/digest,
  disposition and blocker; `outstanding_findings`: durable finding history.

A collector has one complete-plan rerun. Exact rerun replay while its collector
still owns the active slot validates retained execution/log bytes and launches
nothing. Changed assignment/timeout/session refuses. After terminal admission,
observe replays the admitted outcome without rereading a replaced raw claim or
changing version/findings/count. A new evidence attempt uses a fresh collector
operation, session, rerun identity and logs; old evidence remains historical.

Rerun intent without completed execution proof is unresolved ownership. Neither
collector terminal receipt nor process absence authorizes another actor in that
case. Observation retains unknown operation, blocked coverage, exact blocker,
intervention and evidence location. Reload can consume known complete receipts,
or conservatively stop; it never relaunches an uncertain command. Command locking
serializes reruns against other mutations. There is no automatic repair/recovery
service or power-loss qualification.

Relevant tracked/untracked/explicitly evaluated ignored/config/index/HEAD changes
make candidate/check/collection stale, including changes during collection.
Owner-authorized input/policy/flow revisions invalidate prior bound evidence and
readiness while retaining history/count. Repointing old report paths/digests cannot
restore eligibility. Irrelevant ignored generated output retains inherited handling.
Invalid API requests preserve authoritative ledger/version/count and task bytes;
diagnostic files and operational failures may retain evidence/interventions.

## Findings, correction and status routing

Repeated finding IDs preserve one current finding and append snapshots containing
operation, candidate, evidence/context/exposure and prior disposition. Findings
absent from a later report remain retained; omission does not resolve them.
Upstream-approved dispositions survive unchanged evidence/exposure. New relevant
evidence or changed exposure reopens with a reason and previous disposition,
without granting repair/deferral authority. Observations alone never authorize
review_findings corrections.

Initial implementation is cycle zero. An actual failed ordinary or independent
required check grants check_failed; reserve correction/implementer with that exact
reason, then launch a fresh correction actor. Each reservation charges exactly
one of three shared cycles; replay/observe/reload/check/recollection do not charge.
Unknown occupancy selects fresh. Correct the actual code, inspect the latest
terminal correction, rerun required checks and launch a fresh collector. Relevant
edits invalidate current coverage while retaining old candidates/logs/findings.
Environment repair consumes the same budget, invalidates readiness and requires
fresh public preflight. Review-driven correction authority remains T-005-owned.
Revision cannot reset the budget or grant a second cycle zero. Fourth correction
refuses corrections_exhausted; retain partial work/evidence and use the existing
record_intervention active-chat path for the precise owner action. Acknowledgement
is not new authority.

Status distinguishes failed product checks (bounded correction), missing report
or not_run/gapped evidence (fresh collection/reruns), stale work (new inspection,
checks and collection), blocked review capability (inspect report/active-chat
intervention), and infrastructure/unknown rerun terminality (inspect intent/logs,
resolve ownership and obtain repair authority). Failed infrastructure cannot
become a product pass or an authorized repair through prose.

## T-005 extension seam and proof limits

Extend `observe_operation` → `_admit_actor_outcome(run_dir, ledger, operation,
observed, result)` → `_publish_actor_outcome` for ART-009 admission. Acceptance
already receives exact frozen assignment through raw `actors/<operation>/result.json`
and adapter `result.state.json`, with observed session/configuration/terminality
retained under operation.transport.outcome. It currently admits no semantic
acceptance, correction decision, completion, commit, tracker write or dependency
release. T-005 must validate current collection and acceptance identity, separate
decision authority and missing-evidence/correction routing before adding them.
Generic ledger mutation is not an admission bypass.

Exact local commands, scenario/subrow coverage, raw evidence paths, original
measurement pair and results are in [T-004.2 implementation-report](../T-004.2/implementation-report.md).
Local evidence uses real disposable Git/filesystem/subprocess checks and scripted
actors controlling role responses/edits. It proves local controller wiring and
observed sessions, not actual sbx containment, provider/model identity or semantic
review quality. No live/model/network check ran. Historical unsupported Linux
legacy sandbox boundaries remain unqualified. T-006 owns the approved live pilot.
