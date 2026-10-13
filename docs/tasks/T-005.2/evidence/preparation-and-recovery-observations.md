# T-005.2 preparation and readiness-recovery observations

Maps every verification scenario of `docs/tasks/T-005.2/verification.md`
(revision 1) to current evidence. Three evidence levels are kept separate
everywhere: **observed** (this invocation's raw local staging/probe results),
**structural** (current green owner-test modules over the fixture oracles),
and **unrun** (role-call boundaries owned by the coordinator; never presented
as observed output). Raw commands/identities: `run-log.md`.

## V-01 — Actual packaged preparation reaches implementation in order

**Observed (the actual chain, this package).** The T-005.2 package itself is
the minimal executable package whose preparation chain was actually exercised
across three separate coordinator invocations:

1. a separate `task-verification-designer` call produced
   `docs/tasks/T-005.2/verification.md` — actual producer bytes, SHA-256
   `85f58c81…4431b`, revision 1, whose `Source brief:` declaration resolves
   to this package's `brief.md` (SHA-256 `794247bc…91c77`, re-verified
   byte-for-byte);
2. a separate `task-preflight` call consumed those exact designer bytes and
   produced `docs/tasks/T-005.2/preflight.md` — Status `ready`, binding the
   same brief SHA-256, verification revision 1, authority
   (`docs/project-plan.md` sections 8/10–11, parent P-01–P-07) and scope;
   the preflight itself records the designer→preflight link as "this call";
3. this separate `bounded-task-implementer` call (the consumer) re-verified
   all three artifact hashes, HEAD and status before the first edit
   (`run-log.md`), and only then began implementation. Implementation did not
   precede derived verification or ready preflight; each handoff resolves to
   the actual preceding producer's bytes, not a filename or a staged expected
   answer.

**Retained proof level (F-01 correction):** artifact existence/identity only —
the three artifact hashes were re-verified before entry, and discovery's
DISC-02 confirmed the preparation bytes existed before implementation. The raw
outputs of the three separate invocations and this invocation's
consumer-read transcript were not retained; full role-chain provenance
remains an explicit evidence gap, not an observed pass.

**Staged variants (role behavior unrun).**
- Compact documentation package: `preparation-routes` stages `PKG-1` (ready
  executable brief whose outcome is a compact documentation update) and
  `entry-cases` stages the `DOCS` package — `brief.md` + `verification.md`
  but **no** `preflight.md` — plus `requests/relabel.md`, which attempts to
  relabel the documentation package as a conversational direct request. The
  entry rule (packaged preparation cannot be bypassed by relabeling; missing
  readiness refuses entry without repository edits) is control bytes only
  here: the implementer-side refusal is unrun.
- Minimal executable package fixture inputs: `queue-defect` stages the QR-12
  workspace including the untracked staged `docs/tasks/QR-12/preflight.md`
  placeholder packet (supplied history) that the T-005.1 handoff manifest
  names for replacement by actual designer/preflight raw outputs. Those role
  calls were not launched; the reproducible setup and current identities are
  retained (`run-log.md`, `unrun-role-boundaries.md`).

## V-02 — Invalid verification cannot borrow green evidence or artifact ownership

Staged controls (designer + preflight fixtures; all exit 0, identities in
`run-log.md`):

- `coverage-closure`: `COV-VALID` (V-01/V-02 cover both ACs incl. the
  ROW-TIMESTAMP finite-risk row with exact-timestamp oracle) vs
  `COV-OMITTED` (V-01 title evidence green while AC-02/ROW-TIMESTAMP are
  omitted — the omitted AC stays a gap despite other green evidence),
  `COV-UNSUPPORTED` (V-99 "encrypt every export" — an unsupported scenario
  cannot add a requirement), `COV-WEAK` (V-02 checks only that an export
  file exists — a weak oracle cannot prove the required exact-timestamp
  result).
- `verification-conflicts`: `CONFLICT-MISSING` (no `Source brief:`
  declaration), `CONFLICT-MALFORMED`, `CONFLICT-DUPLICATE` (two declarations),
  `CONFLICT-FOREIGN` (declaration resolves to `OTHER`'s brief), vs
  `CONFLICT-VALID` (valid same-package control clears ownership only;
  coverage/current-readiness obligations still apply). Existing
  verification contents are preserved in each staged package.
- `readiness-cases`: `MISSING` (verification.md absent — missing or foreign
  verification cannot satisfy packaged readiness), `FOREIGN` (declaration
  rewritten to `tasks/VALID/brief.md`), `OMITTED` (V-02 truncated), in
  addition to the V-03 entries below.

Current structural evidence: owner modules
`tests/test_task_preparation_contracts.py`, `tests/test_task_preflight.py`,
`tests/test_bounded_task_implementer.py` (green — preflight ran them at
`3eba17c`; renewed green at completion, see `results.md`). Designer/preflight
role assessment over these controls: **unrun** with owner (coordinator;
per-call role owners per the T-005.1 inventory).

## V-03 — Missing prerequisites differ from task-owned future proof

Staged (`readiness-cases`): `VALID` — the absent future test
`tests/test_future.py` is explicitly task-owned, its necessary setup,
capability (stdlib unittest), authority and permissions are available, and an
available baseline (`tests/test_existing.py`) exists: the case may be ready
with planned proof and the absent test is never reported as executed or
passing; contrasted with `CAPABILITY` (indispensable `tools/secure_clock.py`
absent, outside allowed scope, no supported equivalent, "do not create it" —
blocks with the prerequisite owner), `DEPENDENCY` (approved enterprise time
SDK not installed, installation prohibited — dependency owner), and
`PERMISSION` (production clock service; network prohibited — permission
owner must authorize). Negative inputs are preserved; no prerequisite was
created to turn an invalid case green.

Inherited T-005.2-owned controls (staged; structural owner evidence current):
`scheduler-missing` (INV-CASE-05 — `SCH-09` package whose decisive scheduler
capability is absent; missing decisive capability blocks with its
prerequisite owner), `queue-ready` (INV-CASE-19 — `QR-12` package with
verification; material standalone value resolved from dirty ownership,
dependencies and command facts), `api-overlap` (INV-CASE-20 — `API-31`
package with `MM src/auth/session.py`: ownership overlap is separated within
authority or blocks before implementation), `queue-guided` (INV-CASE-21 — a
guided direct request stays inline without durable paperwork).

Role assessment over these controls: **unrun** (coordinator-launched
`task-preflight` calls).

## V-04 — Compact and integration routes retain their authority boundaries

Staged: `preparation-routes` (PKG-1 compact documentation package; `PARENT`
composite `decomposed` → routes to its executable leaf, never implemented;
`BLOCKED` `blocked_design` → its decision owner; `LEGACY.md` direct legacy
brief → package normalization); `entry-cases` (`NOVERIF` missing verification;
`NOPREP` missing readiness; `BLOCKED` blocked readiness; `STALE` brief
revision 2 vs preflight's recorded revision 1; `FOREIGN` verification
declaring another brief; `REVMISMATCH` verification revision 2 vs preflight
revision 1; `WRONGSCOPE` preflight naming `W-32`'s brief; `COMPOSITE`
decomposed parent with `index.json` registering dependency-ready leaf `T-C1`
(and `T-C2` depending on it); `BLOCKEDDESIGN` verification Status `blocked`;
`API-31.md` legacy direct brief outside any package; `DOCS` + `relabel`/`direct`
requests; unpackaged direct request keeps compact inline readiness);
`queue-guided` (direct-edit control). `requests/direct.md` (readiness-cases)
is the unpackaged small conversational direct request — inline readiness
permitted, no durable paperwork required.

`integration-leaf` (IFQ-02 / INT-FLOW-001 I-05): the executable integration
leaf `INT-9`'s own ACs specify the supplied producer output
(`docs/producer-outputs/export-handoff.json`) consumed exactly once at the
settlement consumer boundary; the contrasts file keeps outside authority:
sibling requirement `INT-10` (export retention — must not be invented or
owned), system-wide export-to-archive strategy, and an unavailable decisive
settlement oracle (reported to its owner, never fabricated). The composite
`INT-PARENT` is staged beside it. Integration-leaf permission does not
authorize composite-parent implementation or invented sibling requirements.

INV-CASE-22 (legacy direct brief refused and routed to `task-brief-designer`)
is a prompt-only eval with no single fixture scenario declared in the T-005.1
inventory; its structural evidence is the current green owner module
(`tests/test_task_preflight.py`), and the implementer-side legacy-brief
control `docs/tasks/API-31.md` is staged in `entry-cases`. Role behavior:
**unrun**.

Role assessment over these controls: **unrun** (coordinator-launched
designer/preflight/implementer calls).

## V-05 — Recovery preserves IDs and rejects obsolete readiness twice

Staged designer-side coverage gap: `coverage-revision` — `REV-1`'s brief has
AC-01 (export a report) + AC-02 (preserve the source timestamp), while its
verification revision 1 covers only AC-01 and its preflight is ready at
verification revision 1 with "Evidence: V-01 passed" (green evidence for the
covered AC does not close the uncovered AC-02).

Staged recovery bytes (`revision-recovery`; INV-CASE-23 / CCR-07 / REV-01):
- `FEASIBLE` and `UNAVAILABLE` verification moved to **revision 2** with
  the original V-01/V-02 IDs and scenario bytes retained, an explicit
  recorded reason ("omitted expiry=now+1 boundary is justified by AC-01;
  retain V-01/V-02") and the new justified coverage V-03
  (expires_at=101, now=100 must return true) — regenerable deterministically
  from the fixture; the claimed verbatim capture was **not** retained
  (discovery-01 F-01; corrected).
- The revision-1 `preflight.md` (Status ready, "Verification revision: 1")
  remains staged unchanged beside the revision-2 verification: the
  affected obsolete readiness, i.e. the wrong-ready contrast that must be
  rejected for its obsolete revision both **before** focused recovery and
  **again after** current revised proof exists (a later green proof cannot
  rescue it).
- `verification-v1.md` copies are preserved as history (prior artifacts
  remain available; recovery does not discard history).
- `UNAVAILABLE` variant: the revised V-03 oracle requires the absent
  indispensable `tools/secure_clock.py`, outside allowed scope — recovery
  stays blocked with reason and prerequisite owner instead of becoming ready.

**Structural (regenerable; F-01 correction):** the staged bytes preserve the
ID/reason/history chain — independently regenerated and hashed by discovery
DISC-02; the claimed verbatim capture was not retained. The actual T-005.2
package chain (V-01) demonstrates the governing order discipline on a real
package at artifact level only: current readiness precedes implementation, and
this implementer call consumed the current revision-1 references.
**Unrun:** the actual recovery role chain over these staged inputs — designer
revision call, focused preflight producing readiness for revision 2, current
revised-proof implementer submission, and the separate new acceptance
decision consuming current evidence. Old-readiness rejection behavior:
structural owner evidence current (`tests/test_task_preflight.py`,
`tests/test_review_composition.py` REV-01); role behavior unrun.

## V-06 — Requirement changes and material staleness retain distinct owners

Staged, each as a real Git before/after boundary (identities in
`run-log.md`):

- `revision-recovery/transitions/requirement`: proposed AC-03 (retention
  export) appended to the CURRENT brief, explicitly not approved by the
  cited authority — a changed requirement returns to the task
  design/decision owner; it is not settled through a verification revision
  (contrast: the `FEASIBLE` coverage repair under unchanged authority takes
  focused preflight, V-05).
- `expected-implementation` / `expected-report`: task-owned in-scope
  implementation effects and task-local report text — expected authorized
  effects alone do not restart task design or force broad rediscovery.
- `authority` / `prerequisite` / `ownership` / `permission` / `capability`:
  material fact changes (operating envelope superseded, prerequisite SDK
  removed, inseparable user ownership without merge permission, permission
  revoked, supported helper removed) — each forces readiness reconsideration
  with the actual reason and owner rather than silently reusing approval.
- `freshness-change` (INV-CASE-24): **observed locally** — identical
  short-status text (`MM src/auth/session.py`) and identical index blob
  coexist with changed non-artifact worktree bytes (worktree SHA-256
  `cfd8bf6d…` → `8fe8c530…`): equal Git status text does not prove
  freshness; changed identities preserve user work and force
  reconsideration (`run-log.md` probe 1).
- `coverage-revision`'s `changed-requirement.md` ("AC-02 now requires an
  approved retention decision") — the changed-requirement contrast kept as
  an alternative before/after input; transition inputs are preserved, not
  applied or reset.

Routing assessments over these states: **unrun** (role calls); staged
before/after states and their distinct owners are retained exactly.