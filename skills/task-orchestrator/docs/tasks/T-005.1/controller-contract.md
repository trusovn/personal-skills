# T-005.1 controller contract: separate acceptance and recovery

Submission contract for T-005.2. Independent review is still owed; the
implementation report owns evidence and qualification limits. This extends the
[T-004 contract](../T-004/controller-contract.md), preserving its candidate,
check, collection, reservation and transport contracts. It implements ART-009,
the IF-003 acceptance slice and candidate-bound ART-002 decision status.

## Public operations

From the repository root, with an external run directory and a currently passed
candidate/check/independent-collection history:

```sh
python3 skills/task-orchestrator/scripts/controller.py status --run-dir RUN
python3 skills/task-orchestrator/scripts/controller.py reserve --run-dir RUN \
  --expected-version VERSION --task-id TASK --stage acceptance \
  --role acceptance_reviewer --operation-key UNIQUE_KEY
# Save exactly the returned assignment object as assignment.json.
python3 skills/task-orchestrator/scripts/controller.py launch --run-dir RUN \
  --request assignment.json --codex-bin CODEX --timeout-seconds 300
python3 skills/task-orchestrator/scripts/controller.py observe --run-dir RUN \
  --operation-id operation-NNN
```

Equivalent callables in `scripts/controller.py`:

- `reserve_operation(run_dir, *, expected_version, task_id, stage, role,
  operation_key, reason="initial")`;
- `launch_operation(run_dir, assignment, *, codex_bin="codex", timeout_seconds=300)`;
- `observe_operation(run_dir, operation_id)`; and
- `status_run(run_dir)`.

Use `Path` run directories. Only the existing observe → `_admit_actor_outcome`
→ `_publish_actor_outcome` path admits acceptance. No additional actor-output
admission API exists. `run-next` remains a refusal/reporting stub.

The assignment envelope is unchanged: run/task/operation/key/stage/role/reason,
input/policy/flow hashes and flow revision, candidate hash, correction count,
write/repair booleans, session policy and frozen actor model/reasoning. Exact JSON
value types matter. Acceptance has `can_change_files=false`, `can_repair=false`,
and always launches a fresh session. Its actor comes from the frozen acceptance
flow step, preserving `gpt-6.1-sol` low/medium/high mapping. The legacy nullable
`session_policy` field remains null for non-correction assignments; it does not
authorize session reuse.

## Authority and evidence supplied to the reviewer

The prompt includes the exact assignment, frozen brief and verification, scope,
checks, policy/flow and `collection_context`. For acceptance that context contains
`run_dir`, current candidate, checks, collection, exact evidence path/digest map,
retained findings/dispositions/history, required conditional stages and their
receipts, known-issue history, the default `docs/known-issues.md` contents/hash
when present, and runtime limits. A declared nondefault tracker is discoverable
through task/repository authority; this slice adds no tracker format or writer.

The assignment prohibits implementation/correction edits, collection takeover,
tracker writes, commits, policy changes and task selection. This is an assignment
boundary under approved sbx/YOLO assumptions, not enforced filesystem isolation.
The prompt preserves contextual disposition policy, missing-proof ownership,
impact versus likelihood, bounded deferral conditions and mixed-condition
precedence. Scripted reviewer responses cannot qualify live semantic judgment.

Optional task-manifest `required_reviews` enumerates `maintainability` and/or
`registry`. Preparation must enumerate applicable conditional stages from the
human-reviewed workflow; the controller does not infer natural-language stage
requirements. The field is frozen in initial/revised inputs and cannot be
removed by actor claims or weaker result profiles. Discovery and acceptance
remain unconditional stages. Existing manifests without the field use `[]`.

Each conditional stage's existing independent owner supplies
`reviews/<candidate_sha256>/<stage>.json` in the external run directory with
exact fields:

```text
stage, status, candidate_sha256, inputs_sha256, policy_sha256, flow_sha256,
session_id, rationale, evidence
```

`status` must be `passed`; identities must match current authority; `session_id`
is nonempty and independent of product producers. `evidence` is a nonempty map
of run-relative artifact paths to SHA-256 hashes; referenced JSON, Markdown or
other bytes must exist and match. These are trusted coordinator-supplied stage
receipts, not a newly implemented conditional-role launcher or provider/session
attestation. Acceptance cannot reuse their session. Their exact bytes/digests
are supplied to acceptance and rechecked at admission and eligibility reads.

## Actor result and decision

`assets/actor-result.schema.json` extends the existing envelope with `decision`
only for acceptance. Runtime validation requires exact keys:

```text
assignment, session_id, status, summary, readiness, decision
```

`readiness=null`, `status=complete`, and explicit `session_id` equal to the
adapter-observed thread are required. Terminal adapter proof, successful process
outcome, exact assignment/configuration and current authority remain mandatory.
Acceptance cannot reuse any prior actor session, including invalid prior
acceptance, implementation, correction or collector sessions.

The exact decision fields are:

```text
action: accept | correct | missing_evidence | blocker
rationale: nonempty string
evidence: exact collection_context.evidence map (run-relative path -> SHA-256)
dispositions: array of finding dispositions
unfinished: array of {owner: verify | semantic_review | intervene,
                      reason: nonempty string, evidence: nonempty string array}
```

Every retained finding needs one disposition with its stable `id`; omissions
and duplicate/unknown IDs refuse admission. Exact disposition fields:

```text
id, kind, rationale, evidence, requirement_violation, material_risk,
correction_authorized, trigger, consequence, boundary, impact, likelihood,
mitigation, compatible_consumers, follow_up, reassess_when
```

`kind` is `blocking`, `known_issue`, `observation`, `resolved`, `missing_evidence`
or `blocker`. Evidence is a nonempty string array; the three flags are booleans;
other fields are nonempty strings. Flags encode supported reviewer judgments,
not an automatic defect classifier. The reviewer must ground them in supplied
requirements, exposure and retained evidence. Known issues cannot waive a
requirement violation or material risk; observations/resolutions cannot erase
either. A preference without a requirement violation or material risk cannot
authorize correction. Known issues retain compatible consumers, follow-up and
reassessment conditions, plus acceptance operation/session/candidate provenance.

An unchanged approved disposition is retained verbatim. Changed relevant
finding evidence or exposure reopens it with a reason and prior disposition;
collection history and original decision files remain. Candidate changes alone
do not reopen an otherwise unchanged approved issue. Collection omission never
removes a finding. This slice does not record approved issues in a tracker.

## Retained paths, digests and current eligibility

- `acceptance-inputs/<operation>.json`: immutable launch context snapshot.
- `actors/<operation>/result.json`: raw actor claims, diagnostic after admission.
- `actors/<operation>/result.state.json`: exclusive adapter terminal receipt.
- `decisions/<operation>.json`: admitted assignment, observation, decision,
  retained finding dispositions/history, `next_actions`, `correction_request`.
- `ledger.evidence.acceptance`: status, input/candidate hashes, operation ID,
  decision `path` and SHA-256 of the exact decision file bytes.
- `ledger.outstanding_findings`: current stable IDs, dispositions and history.

Checks now retain result-file SHA-256 in `ledger.evidence.verify`. Collection
records additionally bind independent rerun bytes through `rerun_sha256`.
Eligibility reads validate candidate bytes/workspace (HEAD, index, tracked,
visible untracked and explicit ignored inputs), frozen source-document identity,
check/result/execution/log bytes, collection and independent rerun identity/logs,
conditional receipts and their proof, decision bytes and known-issue context.
Drift before reservation, launch or terminal admission cannot become eligibility.
Irrelevant ignored generated output retains inherited exclusion behavior.

Authorized input revisions additionally capture each document's
`source_sha256` at revision admission: reviewed frozen content may differ from
its source, while subsequent unauthorized source drift still invalidates it.
Revisions invalidate old readiness/candidate/evidence without resetting the shared
correction count. Historical producer assignments cannot rebind to revised inputs.
Older runs without the new check/rerun digests need fresh verify/collection
operations; there is no silent hash backfill or reinterpretation of raw history.

`status_run` exposes `acceptance_decision`, `completion_eligible`, current
`evidence`, `outstanding_findings`, `next_actions`, blockers and intervention
history. `completion_eligible=true` means a current separate `accept` exists,
required proof remains valid, and no actor is active. `completion_eligible` in
`next_actions` is a consumer signal, not a callable command. This neither marks
the task completed nor writes known issues, commits or releases dependencies.

## Recovery, budget and replay

| Supported decision | Durable route and effect |
|---|---|
| `correct` with an authorized confirmed blocker | Sets `correction_request=review_findings`; reservation, not the decision, charges one shared correction. Other unfinished evidence and blockers remain in the decision. |
| `missing_evidence` without an eligible blocker | Requests `reserve:verify` and/or `reserve:semantic_review`, or `intervene`, according to unfinished owners; zero correction charge. |
| `blocker`, including prevented correction or missing authority/capability | `intervene`, retained decision and opened active-chat intervention; no implementation/repair authority. |
| `accept` | Current eligibility only; unresolved blockers, missing proof or unfinished required rows forbid it. |

An authorized blocker takes precedence over separate unfinished evidence. A
`correct` proposal without an eligible blocker refuses. Environment repair keeps
its inherited explicit upstream authority and invalidates readiness; fresh
preflight is required afterward. Chat acknowledgement alone grants no authority.
Initial work is cycle zero, followed by at most three shared check/review/repair
corrections. At the limit valid acceptance is still possible; a fourth correction
refuses `corrections_exhausted` with preserved work/evidence and intervention.

Same-key exact reservation and same-config launch replay never charge or launch
again. Conflicting keys/configuration, stale versions and invalid roles refuse
without authoritative mutation. Unknown/live ownership blocks successors even
when result bytes exist. No automatic recovery is added. After publication,
observation returns the retained operation without rereading changed raw output.
An interrupted decision-file publication can admit the same terminal result once
on reload; an intent without terminal proof remains unknown. Later evidence-only
operations supersede the old decision and require fresh acceptance, preserving
all old files/history. Historical admission replay does not restore current
eligibility after drift.

## T-005.2 consumer seam and remaining work

Consume the current `status_run` view and decision path/digest. In a future
completion transaction, hold the existing `RunCommandLock`, reload authority,
require no active/unknown operation and use `_current_acceptance(run_dir, ledger)`
plus `_acceptance_context` to recheck the exact candidate/evidence and accepted
decision. A previously cached true status is not completion authority. The
completion owner must separately validate scope, required effects, any approved
known-issue recording and receipts immediately before publication.

T-005.2 still owns coordinator recording, recording idempotency/validation,
completion publication and the fully composed completion proof. Automatic
commits, dependency release and automatic task advancement remain absent.
T-006 owns real sbx/provider/model and semantic-review qualification. The local
suite uses real disposable Git/filesystem/processes with scripted role responses.
It cannot establish those live properties or tamper resistance against an actor
with full access to controller-owned records.
