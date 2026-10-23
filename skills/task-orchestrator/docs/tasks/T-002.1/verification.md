# Verification Design: T-002.1 — Freeze the approved one-task policy

Source brief: brief.md
Source brief revision: 1
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

This is verification design, not executed evidence or a ready preflight.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | Real frozen-input files, not hash-field presence alone |
| AC-02, R1 | V-02 | Required roles/stages and single-task authority |
| AC-03, R2 | V-01, V-03 | Approved policy and reliable-context boundary |
| AC-04, R2 | V-04, V-05 | Preserved old runs and exact successor contract |

## Verification scenarios

### V-01 — Source edits cannot silently revise frozen authority

- **Covers:** AC-01, AC-03, R2.
- **Intent:** reject freezing only mutable source paths or policy defaults.
- **Given:** a disposable repository with actual brief and verification files,
  scope/check requirements, approved policy and one selected task.
- **When:** initialize a run, capture its authority, change source brief,
  verification and policy content separately, then reopen the run.
- **Then:** the approved frozen content/identity remains unchanged or a precise
  drift refusal stops use; new source bytes cannot become approved implicitly.
  The original frozen records remain present and unchanged.
- **Oracle / boundary:** real initialization/loading and before/after contents
  of input/run files. Validation or digest format alone is insufficient.
- **Variants:** each input family; more than one selected task is rejected.

### V-02 — A weak profile cannot remove a required role

- **Covers:** AC-02, R1.
- **Intent:** reject the old optional-profile shortcut and combined reviewer role.
- **Given:** otherwise valid new-policy inputs and the required stage sequence.
- **When:** validate/init with each required stage removed, roles merged,
  stages reordered or an actor result presented as completion authority.
- **Then:** each invalid request is refused without adopting the weaker policy;
  a valid representation retains independent collection, separate acceptance
  and a controller-owned completion gate. No actor claim completes the task.
- **Oracle / boundary:** runtime validator plus public initialization and real
  authoritative/task-file comparison for refusal. Schema checks supplement this.
- **Variants:** preflight/checks/collection/acceptance omissions; wrong role/order;
  a weaker optional profile. No Cartesian product is required.

### V-03 — Approved mapping and correction-session rules are explicit

- **Covers:** AC-03, R2.
- **Intent:** reject stale models, altered budgets and treating unknown context as free capacity.
- **Given:** an approved current-policy run and inputs for each reasoning level.
- **When:** resolve frozen policy and correction-session eligibility using known
  occupancy within the reuse rule, its threshold boundary, above it, unknown
  occupancy and terminal token totals without occupancy.
- **Then:** mapping is exactly `gpt-6.1-sol` low/medium/high; eligibility follows
  the existing reliable-occupancy rule/0.5 threshold; unknown or totals-only
  information selects a fresh session. Policy explicitly records sbx/YOLO
  authorization, shared three-correction limit including repair, and chat intervention.
- **Oracle / boundary:** runtime policy resolution and persisted policy, checked
  against schemas/current examples. This does not prove adapter launch flags or
  model availability; T-003 owns applying the resolved policy.
- **Variants:** wrong model/effort, changed limit, missing execution authorization
  and mandatory-stage omission must fail validation rather than silently default.

### V-04 — Old frozen runs are refused without migration

- **Covers:** AC-04, R2.
- **Intent:** reject reinterpreting old frozen policy under new constants.
- **Given:** a real frozen old-format/model/profile run fixture and its file bytes.
- **When:** request continuation through an applicable public controller path.
- **Then:** incompatible continuation stops with a reason and new-run action;
  policy, history, task files and state remain unchanged. An ordinary read must
  not rewrite the run or pretend its policy is current.
- **Oracle / boundary:** controller response and byte comparison of persisted
  fixture files; actor launch is never needed.
- **Variants:** old model mapping and old profile lacking the mandatory sequence.

### V-05 — The published contract matches executable declarations

- **Covers:** AC-04.
- **Intent:** prevent a successor from consuming proposed names as implemented APIs.
- **Given:** completed implementation and its package `controller-contract.md`.
- **When:** compare its field/role/version/compatibility examples with actual
  declarations and focused behavioral results.
- **Then:** supported operations and missing stages are explicit; examples match
  implemented interfaces. No sbx execution or active-install refresh is claimed.
- **Oracle / boundary:** source/declaration review plus reproducible local evidence;
  this document check does not substitute for V-01..04 behavior.
- **Variants:** none.

## Implementation handoff

Preserve these IDs and all material coverage. Use existing fixture helpers and
the brief's targeted-first commands. Demonstrate that a focused case rejects
old/faulty behavior where feasible. Test layout and helper design remain with
the implementer. A changed oracle routes to task design; current executability
routes to standalone preflight. Fresh independent discovery and separate
acceptance follow implementation as specified in the brief.
