# Task Brief: `W2.3` — Complete attempt and association records

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: strong
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / 36k context
```

## Execution sizing

- Sizing policy: `default@1`
- Estimated agent calls: `15`
- Estimated implementation duration: `40 minutes`
- Estimate confidence: `medium`
- Policy result: `fits`
- Triggered limits: `none`
- Decomposition override: `none`

The estimate covers implementation-agent work only. It excludes prior-leaf
acceptance and the fresh independent review required after this leaf.

## Readiness route

`implementer self-preflight`

Confirm W2.2 was accepted and run
`python3 -m unittest tests/test_evidence_records.py -v` plus
`python3 -m unittest tests/test_evidence_store.py -v` before editing. Stop
rather than folding a predecessor correction into W2.3.

## Verification-design recommendation

`separate — mutually exclusive direct/formal task input, distinct planning /
intended / actual profile roles, optional nested conditions and telemetry,
attempt relations, generic association semantics, and collector-fingerprint
change/stability cases permit multiple schema-valid but contract-wrong designs`

This is advisory. If skipped, every finite case and oracle below remains an
implementation obligation in `tests/test_evidence_records.py`.

## Outcome

A programmatic caller can construct and validate complete schema-v2
`ExecutionAttempt` and immutable `Association` records, with inline optional
conditions/telemetry/checks, distinct task/profile/relationship semantics, and
deterministic collector identity; all four W2 record concepts compose through
W1 without skill integration or physical-path knowledge.

## Direction trace

- Direction contribution: Complete the approved four-record raw-evidence model
  and collector-semantics envelope used by later lifecycle and review producers.
- User-observable effect: No direct workflow effect; enables W3 to create a
  complete v2 attempt and W6 to attach acceptance evidence without mutating the
  attempt.
- Why now: Accepted W2.1/W2.2 provide project/task inputs; W2.3 is the approved
  integration closure before `run_evidence.py` migration.
- Direction decisions used: collection contract §§1–3, 4.3–4.5, 5.3, 6–10 and
  11.2/11.4–11.7/11.9/11.11–11.14; architecture §§8–13 and 15–22; repo
  integration §§4–5 and 20; implementation-plan Task 1 exit criteria;
  work-breakdown W2; verification refs S-12–S-16, A-06/A-08–A-11,
  T-04–T-09.
- New direction decisions required: `None`

## Authority and scope

| Item | Contract |
|---|---|
| Authority | The v1.2.1 four-document authority chain, refined by W0/W2 and the verification matrix. |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Dependencies | Accepted W2.2, including all W2.1/W2.2 module/schema/test behavior; accepted W1 attempt/association namespaces. |
| Consumes | Direct-input blob ref or TaskRevision ref; optional execution ProjectSnapshot ref; caller-supplied PRE-RUN/execution/POST-RUN facts; related-attempt links; association inputs; explicit collector-semantic files/config bytes. |
| Produces | ExecutionAttempt and Association constructor/validation behavior, deterministic collector fingerprint helper/input contract, final four-record v2 schema, and full integrated W2 behavioral suite in the same three files. |
| Allowed changes | Only `scripts/evidence_records.py`, `scripts/execution-evidence.schema.v2.json`, and `tests/test_evidence_records.py`. |
| Read-only context | Design pack; accepted W2.1/W2.2 artifacts/reviews; W1 store/tests; existing workflow/runtime helpers only to preserve distinct reference shapes, not to integrate them. |
| Out of scope | Running lifecycle transitions; PRE-RUN capture timing; appending checks; finish/recovery behavior; `run_evidence.py`; discovering runtime/workflow/repository facts; executing commands; runner adapters; skill/review integration; synthetic grading. Those belong to W3+. |
| Assumptions / unresolved decisions | Exact constructor names and compact validation structure are bounded implementation choices. W2 constructs/validates factual record states; W3 owns lifecycle sequencing and freezing at the real producer boundary. No unresolved product or architecture decision blocks W2.3. |

## Work and acceptance criteria

Required work:

1. Extend the module/schema with ExecutionAttempt construction/validation for
   the approved PRE-RUN, EXECUTION, POST-RUN, evidence, optional-inline, and
   related-attempt sections without implementing the lifecycle runner.
2. Add generic immutable Association construction/validation and W1 persistence
   support without acceptance-specific policy or mutation of attempt records.
3. Add deterministic collector fingerprint support over explicit semantic
   inputs, separate from workflow identity and independent of absolute paths.
4. Complete the single v2 schema and integrated tests for all four record
   concepts, preserving accepted W2.1/W2.2 behavior.

- **AC-01:** A valid attempt contains exactly one task input mode—direct input
  ref or TaskRevision ref—while independently preserving an optional execution
  ProjectSnapshot ref and the planning snapshot already held by TaskRevision.
- **AC-02:** PRE-RUN, EXECUTION, and POST-RUN remain distinct sections.
  Conditions live only as an optional PRE-RUN object, telemetry and checks only
  inline under EXECUTION, and absent optional sections remain valid without
  guessed/default observations.
- **AC-03:** Planner-recommended profile (TaskRevision), intended execution
  profile (attempt PRE-RUN), and trusted actual runtime identity (attempt
  PRE-RUN) remain separately representable and are never overwritten or
  collapsed by validation.
- **AC-04:** Attempt relationships preserve separate attempt IDs and the
  approved relation meanings (`retry_of`, `correction_of`, `continuation_of`,
  `profile_replay_of`, `calibration_of`) without collapsing attempts; task
  parent/child relations remain on TaskRevision.
- **AC-05:** Association preserves type, attempt ref, producer/provenance,
  optional durable artifact ref, factual outcome/status, and collection time;
  it persists immutably through W1 and does not alter the referenced attempt.
- **AC-06:** Collector metadata contains schema version `2` and a deterministic
  fingerprint that is stable for the same explicitly selected semantic inputs,
  changes when any such bytes/config change, ignores input ordering and
  absolute locations, and remains distinct from workflow identity.
- **AC-07:** Invalid mixed/missing task input, misplaced standalone models,
  malformed relation/association refs, unsupported knowledge status/schema
  version, and invalid nested optional sections are rejected without a false
  persisted record.
- **AC-08:** The completed schema exposes only the four first-class records;
  conditions, telemetry, checks, and collector identity remain nested
  definitions/fields rather than top-level models or namespaces.
- **AC-09:** A real W1-backed integration can create/reuse ProjectSnapshot and
  TaskRevision records, construct a valid attempt and association, persist the
  attempt/association through the correct W1 operations, and retrieve all
  linked records without knowing physical storage paths or importing skills.
- **AC-10:** Only the three scoped W2 files change; all W2 and W1 tests pass
  using the standard library, with no W3 producer/lifecycle behavior added.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| Attempt task and snapshot roles do not collapse | direct ref only; TaskRevision ref only; both refs invalid; neither invalid; planning snapshot on revision vs execution snapshot on attempt | Public constructors/schema plus linked W1 record readback | Focused cases cover all input modes and distinct snapshot values | Build a formal attempt whose planning/execution snapshot refs differ and inspect both | Implementer owns targeted suite; fresh reviewer owns probe |
| Optional inline evidence remains optional and correctly located | conditions present/absent; telemetry present/absent; checks present/empty; unknown vs zero/false/not_applicable | Constructed record and final schema validation | Matrix checks exact nesting and preserved values without new top-level records | Supply false/zero telemetry and omit conditions; verify neither is lost or invented | Implementer owns targeted suite; fresh reviewer owns probe |
| Profile and relation semantics remain distinct | planner recommendation; intended launch; actual runtime; five approved attempt relation types; task parent/child relation excluded from attempt | Full linked record graph through public API | Tests use deliberately different profile values and each attempt relation, then inspect graph | Probe one correction link and confirm TaskRevision parent/child data is unchanged | Implementer owns targeted suite; fresh reviewer owns probe |
| Association is append-only evidence beside an attempt | with/without durable artifact; factual status; producer/provenance; collection time; conflicting same ID | W1 association namespace plus byte-for-byte attempt readback | Persist association variants; conflict rejects; attempt bytes/value unchanged | Attach an acceptance-shaped generic association and compare attempt before/after | Implementer owns targeted suite; fresh reviewer owns probe |
| Collector fingerprint identifies collector semantics, not location | same inputs reordered/relocated; one file changed; one config changed; workflow identity changed alone | Public fingerprint helper output | Focused stability/change tests over explicit temp files/bytes | Relocate identical inputs, then alter one byte | Implementer owns targeted suite; fresh reviewer owns probe |

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first / regression | New attempt/association/fingerprint and integrated graph cases fail before production changes because W2.3 behavior is absent. | `python3 -m unittest tests/test_evidence_records.py -v` |
| Targeted | Full four-record identity, validation, sparse optionality, relation, association, fingerprint, and real W1-backed integration cases pass. | `python3 -m unittest tests/test_evidence_records.py -v` |
| Owning suite | W1 lifecycle/namespace/immutability behavior remains compatible with completed records. | `python3 -m unittest tests/test_evidence_store.py -v` |
| Broader gate | Final W2 implementer runs the existing run-evidence suite to prove the untouched v1 producer remains green; the fresh reviewer owns aggregate rerun of all three suites after any correction is clean. | `python3 -m unittest tests/test_run_evidence.py -v` |

The final fresh reviewer should run the aggregate gate once on final bytes:

```bash
python3 -m unittest tests/test_evidence_records.py tests/test_evidence_store.py tests/test_run_evidence.py -v
```

## Expected contract impact

- Plan refs: architecture §§8–13/15–22; repo integration §§4–5;
  implementation-plan Task 1 exit criteria; work-breakdown W2;
  S-12–S-16, A-06/A-08–A-11, and T-04–T-09 — `materialize`;
  accepted W2.1/W2.2 refs — `preserve`.
- Current contract dependencies: no `docs/contracts/` registry exists; consume
  accepted W2.1/W2.2 module/schema behavior and W1's attempt/association
  persistence operations.
- Expected durable delta: complete schema-v2 four-record construction and
  validation contract, generic association boundary, attempt/profile/relation
  representation, and deterministic collector identity consumed by W3–W6.

## Stops and handoff

- Stop if W2.2 is not accepted/green, predecessor APIs require material
  redesign, user work overlaps scoped files, a third-party dependency appears
  necessary, or implementation pressure crosses into W3 lifecycle/producer
  orchestration or a new top-level model.
- Treat the budget as a checkpoint; preserve all pre-existing work and leave
  authority/master-plan/index documents unchanged.
- Next action: guided implementation after implementer self-preflight (with the
  optional focused verification-design pass recommended above).
- Required follow-on: immediately after implementation or correction, hand
  the completed bytes to a fresh independent acceptance reviewer. That final
  reviewer owns the aggregate three-suite gate on final bytes.
