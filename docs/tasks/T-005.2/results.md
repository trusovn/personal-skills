# Implementation results: T-005.2 — Exercise preparation and readiness recovery

Implemented: READY_FOR_REVIEW (brief metadata `review: immediate`). No
independent review has accepted these bytes; this file records the
implementer's submission evidence only.

- Preflight/context reference: `docs/tasks/T-005.2/brief.md` (SHA-256
  `794247bc2477968d6394ce6bdbb9798ab6c06b96ed4d28ab7383da68ab391c77`),
  `docs/tasks/T-005.2/verification.md` revision 1 (SHA-256
  `85f58c81d53fc6629baaf3eb663a5b3031d48f4b63982630e51fa7b77cd4431b`),
  `docs/tasks/T-005.2/preflight.md` (ready; SHA-256
  `f7d367539891d51d1d07b428fc9953b4e10ad726446c74ad5d1af1b8b647b04d`). All
  three hashes were re-verified against the preflight's recorded bindings
  before the first edit; the only repository delta since the preflight's
  HEAD `3eba17c` was the coordinator's commit `9127e59` ("5.2 docs") adding
  this package's own `verification.md`/`preflight.md` — the expected
  preparation report effect, so the recorded readiness stayed applicable.
- Evidence run (project-local sidecar `scripts/run_evidence.py`; availability
  green, no prior open run): `run-20261013T143605Z-d20d1908061f` (begin at
  entry, finish `completed` at invocation end).

## Changed paths

- `docs/tasks/T-005.2/results.md` — this submission record.
- `docs/tasks/T-005.2/evidence/run-log.md` — raw staging/probe record: 16
  staging commands with exit codes, per-root Git identities (HEAD + dirty
  state), the eight revision-recovery transition boundaries, entry-cases
  conditional-evidence states, the observed freshness probe, and a
  correction-annotated record of the staged control-byte capture gap
  (discovery-01 F-01: the capture was not retained — see
  `evidence/correction-discovery-01.md`).
- `docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md` —
  every verification scenario V-01–V-06 mapped to observed/structural/unrun
  evidence.
- `docs/tasks/T-005.2/evidence/unrun-role-boundaries.md` — AC-04/V-07
  discipline and the complete unrun role-call ledger with reproducible
  setup, reason and owner.

Inspected and unchanged, with reason: every other path. No missing
task-local case adapter was needed — all nine preflight-named staged
controls and every inherited T-005.2-owned case dispatch in committed
fixture scripts. No source skill, active `.agents/` installation, installer
declaration, protected history, `docs/tasks/index.json`, plan/master
document, or user-owned byte (including the three pre-existing untracked
`.DS_Store` files) was touched; `git diff --check` is clean.

## Deliverables

- **Actual packaged-preparation chain evidence (AC-01):** the coordinator
  exercised this package's full designer → preflight → implementer chain as
  three separate invocations; each handoff resolves to the actual preceding
  producer's bytes (hashes above), and implementation began only after
  derived verification and ready preflight existed and were consumed.
  **Retained proof level (F-01 correction):** artifact existence/identity —
  the three hashes were re-verified before entry. The raw outputs of the
  three separate invocations and the implementer's consumer-read transcript
  were not retained, so full role-chain provenance remains an explicit
  evidence gap (discovery-01 F-01), not an observed pass.
- **Staged refusal/direct-edit/validity/readiness controls (AC-02):** all
  named controls staged fresh in disposable workspaces with identities
  recorded, mapped to current structural owner evidence or explicit unrun
  role boundaries.
- **Revision-recovery staged chain with retained IDs (AC-03):** revision-2
  verification bytes retaining V-01/V-02 and the recorded reason, the
  revision-1 ready preflight kept as the obsolete-readiness wrong-ready
  contrast, revision-1 history preserved, the changed-requirement contrast
  kept distinct, and eight real Git before/after staleness boundaries.
- **Auditable raw-call/unrun-boundary records (AC-04):** evidence-run
  sidecar, per-staging identities, the retained freshness-probe values, and
  the complete unrun ledger — the staged control bytes were **not** retained
  (F-01 gap, corrected below); no staged readiness is presented as an
  observed role output.

## Exact commands and results

All from the repository root. Observation statuses are kept separate from
expected fixture verdicts.

| ID | Exact command | Result |
|---|---|---|
| A | `python3 scripts/run_evidence.py --repo . availability`; `python3 scripts/run_evidence.py --repo . active` | `available: true` (installation root = this repository; workflow fingerprint recorded as workflow-identity evidence only); `active: null` — no open run to recover |
| B | `python3 scripts/run_evidence.py --repo . begin --task-id T-005.2 --task-brief docs/tasks/T-005.2/brief.md` | run `run-20261013T143605Z-d20d1908061f` begun before the first implementation edit |
| S | 16 stagings `EVAL_WORK_ROOT=/tmp/opencode/t0052/<scenario> python3 <fixture> <scenario>` — `preparation-routes`, `coverage-revision`, `coverage-closure`, `verification-conflicts`, `integration-leaf` (designer fixture); `readiness-cases`, `revision-recovery`, `freshness-change`, `scheduler-missing`, `queue-ready`, `api-overlap`, `queue-guided` (preflight fixture); `entry-cases` (implementer fixture); `queue-defect`, `discovery-prepared-ledger`, `authored-production-self-check` (discovery fixture) | all 16 exit 0; per-root HEAD + dirty-state identities in `evidence/run-log.md` (fresh identities per staging, recorded per preflight warning 3) |
| P1 | freshness equal-status probe over `freshness-change/api` (staged baseline JSON vs current `git status --short`, `git show :src/auth/session.py | sha256sum`, worktree file sha256) | **observed pass**: status text identical (`MM src/auth/session.py`), index blob identical (`0eeb7613…d3c8`), worktree bytes changed (`cfd8bf6d…324c` → `8fe8c530…b273`) — equal short status does not prove freshness |
| P2 | staged control-byte capture (FEASIBLE/UNAVAILABLE revision-2 verification, FEASIBLE revision-1 ready preflight, REV-1 verification/preflight/changed-requirement, QR-12 staged preflight placeholder) | **corrected gap (discovery-01 F-01)** — the claimed verbatim capture was not retained: both `/tmp/opencode/t0052*` raw roots were removed and the full control bytes are absent from the retained evidence files; the sidecar manifest's `checks: []` records no captured evidence. The historical capture cannot be recovered; the claim is downgraded to an explicit evidence gap. The fixtures regenerate the same bytes deterministically (verified by discovery DISC-02 regeneration) |
| M1 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py` | 13 tests OK |
| M2 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preflight.py` | 7 tests OK |
| M3 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py` | 15 tests OK |
| C | `git diff --check`; `git status --short` | diff-check clean; status shows only the pre-existing `.DS_Store` user files plus this package's new `results.md`/`evidence/` |

M1–M3 ran as a current confirmation at completion: this task changed no
source/test bytes (the preflight already ran the same three modules green
at `3eba17c`), so no test-evidence renewal was required; the focused
staging/probes above are the primary new evidence.

## AC and scenario evidence

Implementation evidence, not independent acceptance. Every scenario of
`docs/tasks/T-005.2/verification.md` (revision 1) is accounted for.

| AC / scenario | Evidence (command, setup/oracle, result) |
|---|---|
| AC-01 / V-01 | **Corrected (F-01) — artifact-level evidence only, no observed pass for the chain.** Separate designer call → `verification.md` (rev 1, `Source brief:` resolves to the brief at SHA `794247bc…`) → separate preflight call → ready `preflight.md` bound to the same brief/revision/authority/scope → this separate implementer call re-verified all three hashes + HEAD + status before the first edit (A/B; `run-log.md`). Retained: artifact existence/identity (V-01-A). Not retained: raw outputs of the three separate invocations and the consumer-read transcript — full role-chain provenance is an explicit gap. Variants staged: compact documentation packages `PKG-1` (preparation-routes) and `DOCS` (entry-cases; verification without preflight + `requests/relabel.md` bypass attempt — same entry rule, refusal role behavior unrun) and the QR-12 minimal-package inputs with the untracked staged preflight placeholder (unrun ledger rows 1, 5). Role boundaries unrun |
| AC-02 / V-02 | Staged `coverage-closure` (COV-VALID vs COV-OMITTED — omitted AC-02/ROW-TIMESTAMP stays a gap despite green title evidence; COV-UNSUPPORTED — V-99 cannot add a requirement; COV-WEAK — file-exists oracle cannot prove the exact-timestamp result), `verification-conflicts` (MISSING/MALFORMED/DUPLICATE/FOREIGN vs VALID; artifact bytes preserved), `readiness-cases` (MISSING/FOREIGN/OMITTED). Structural: M1–M3 green. Designer/preflight role assessment **unrun** (ledger 5) |
| AC-02 / V-03 | Staged `readiness-cases`: VALID — absent task-owned future test `tests/test_future.py` with available setup/capability/permission may be ready with planned proof, never reported as run; vs CAPABILITY/DEPENDENCY/PERMISSION — indispensable unavailable prerequisites block with the concrete gap and owner. Inherited controls staged: `scheduler-missing` (INV-CASE-05), `queue-ready` (19), `api-overlap` (20: `MM src/auth/session.py` ownership overlap), `queue-guided` (21: guided direct request stays inline). Structural: M1–M2 green. Role assessment **unrun** |
| AC-01, AC-02 / V-04 | Staged `preparation-routes` (composite `PARENT` → executable leaf; `BLOCKED` blocked design → decision owner; `LEGACY.md` → package normalization), `entry-cases` (NOVERIF, NOPREP, BLOCKED, STALE, FOREIGN, REVMISMATCH, WRONGSCOPE, COMPOSITE + `index.json` registering dependency-ready leaf T-C1, BLOCKEDDESIGN, `API-31.md` legacy direct brief, DOCS + relabel/direct requests), `integration-leaf` (IFQ-02: INT-9 leaf's own composition ACs from the supplied `export-handoff.json` producer output at the settlement consumer boundary; sibling INT-10, system-wide strategy and the unavailable oracle stay outside authority; composite INT-PARENT not implementable). INV-CASE-22 (prompt-only) mapped to structural evidence (M2) plus the staged implementer-side `API-31.md` control. Role behavior **unrun** (ledger 2, 5) |
| AC-01, AC-03 / V-05 | Staged `coverage-revision` (REV-1: rev-1 verification covers only AC-01 while the brief carries AC-01+AC-02; ready rev-1 preflight with "V-01 passed" — green covered evidence does not close the uncovered AC) and `revision-recovery` (rev-2 verification bytes retaining V-01/V-02 + recorded reason + new justified V-03, regenerable deterministically from the fixture — claimed verbatim capture not retained, F-01; rev-1 ready preflight kept unchanged as the obsolete-readiness wrong-ready contrast, to be rejected for the obsolete revision both before and after focused recovery; `verification-v1.md` history preserved; UNAVAILABLE variant stays blocked on the absent indispensable `tools/secure_clock.py`). Structural: M2 green (incl. REV-01 semantics in `tests/test_review_composition.py`, green at the preflight run). Actual recovery role chain (designer revision → focused preflight → revised proof → separate new decision) **unrun** (ledger 3, 4); the T-005.2 package chain (artifact-level, F-01 provenance gap) demonstrates the governing order discipline on a real package |
| AC-02, AC-03 / V-06 | Eight real Git before/after boundaries staged (requirement: unapproved proposed AC-03 returns to task design, not a coverage repair; expected-implementation/expected-report: expected authorized effects alone do not stale readiness; authority/prerequisite/ownership/permission/capability: material changes force reconsideration with actual reason and owner) + **observed** freshness probe P1 (INV-CASE-24: identical status text and index blob with changed non-artifact worktree bytes) + `changed-requirement.md` contrast preserved unapplied. Routing role behavior **unrun** (ledger 4, 5) |
| AC-04 / V-07 | **Corrected (F-01) — no observed pass for raw retention.** Retained: evidence-run sidecar (`run-20261013T143605Z-d20d1908061f`, begin/finish recorded), per-staging Git identities, the freshness-probe values (P1), observation statuses separate from expected fixture verdicts, permissions/limits visible, complete unrun ledger with reproducible setup/reason/owner, no staged readiness relabeled as an observed role output, protected state verified before/after (C). **Not retained:** the staged control bytes claimed as captured before grading — raw capture roots removed, manifest `checks: []`; explicit evidence gap (F-01). |

Finite-risk rows: P-01 / INV-001/002/003 → V-01, V-02, V-03, V-04, V-07;
P-02 / INV-003/005/008 → V-05, V-06, V-07 (above). The brief's reviewer
probes are answerable from these bytes: one readiness reference traced to
the bytes actually read by implementation (this invocation read and
re-verified brief/verification/preflight bytes before editing); refusal
controls staged and inspectable with their identities retained.

## Preserved inherited identities (mapped, none dropped)

- **INV-CASE-05, 19, 20, 21** — staged (`scheduler-missing`, `queue-ready`,
  `api-overlap`, `queue-guided`) with current identities; structural owner
  evidence green; role assessment unrun.
- **INV-CASE-22** — prompt-only per the T-005.1 inventory (no single fixture
  scenario declared); structural evidence + staged implementer-side
  `API-31.md` control; role behavior unrun.
- **INV-CASE-23 + CCR-07 + REV-01** — staged recovery bytes + wrong-ready
  contrast retained; recovery role chain unrun.
- **INV-CASE-24** — staged and locally observed (equal-status changed-byte
  probe).
- **COMP-05** — both scenarios (`discovery-prepared-ledger`,
  `authored-production-self-check`) staged with identities; discovery-side
  role behavior unrun; prepared-ledger input supplies the I-04
  preparation-reference parity that T-005.3's role calls consume via IFQ-03.
- **IFQ-02 / INT-FLOW-001 I-05** — `integration-leaf` staged; designer role
  call unrun.
- **INT-FLOW-001 I-04** — covered by this package's artifact-level
  preparation-reference chain (the discovery/acceptance consumers' actual
  preparation references are the real package bytes recorded above; raw
  consumer-read records not retained — F-01) plus
  the staged prepared-ledger control.

## Filesystem/Git proof versus unrun behavior

Everything run here is local staging/CLI/test/byte-comparison proof in
disposable workspaces and over this repository's own bytes. No role call
over staged fixtures, live/network/model-budget eval, durable reviewer
report, or acceptance decision was run or claimed; behavioral
qualification of the staged controls remains incomplete with the owners in
`evidence/unrun-role-boundaries.md`. The designer→preflight→implementer
chain for this package is coordinator-launched artifact evidence (hashes
re-verified by this invocation), not retained role-call raw output (F-01).
Disposable `/tmp/opencode/t0052*` workspaces were removed; the receipts
retained the staging identities and probe-1 values but not the staged
control bytes — correction recorded in `evidence/correction-discovery-01.md`.

Actual contract impact:
- added/changed/removed durable cross-task surface: none (task-local
  evidence and results only; ART-001/002/003/004 preparation interfaces and
  all stable refs preserved; case-local ART-012 evidence inputs added; no
  `docs/contracts` registry exists and none was created).
- Executable contract declarations changed: none.

## Local decisions (reversible, task-local)

- Treated this package's own designer→preflight→implementer chain as the
  minimal-executable-package variant of V-01 (it is the only package whose
  preparation role calls the coordinator actually launched); staged
  PKG-1/DOCS/QR-12 controls supply the compact-package and fixture-input
  variants for the unrun boundaries.
- Staged the four inherited preflight scenarios and COMP-05's two discovery
  scenarios beyond the nine named controls so every preserved inherited
  identity maps to current evidence rather than an inherited pointer.
- Reused T-005.1's retained `queue-defect` public-probe receipt instead of
  rerunning the QR-12 CLI probe (parent rule 1: no ceremony reruns);
  staged `queue-defect` fresh only to record the QR-12 placeholder bytes and
  current identities for the unrun-call setup.
- No task-local case adapter was created: all controls dispatch in
  committed fixture scripts.
- Budget note: the brief's soft sizing (15 calls / 40 minutes / 50k
  context) was passed; a progress summary was stated at the checkpoint and
  work continued while the task remained bounded and within authority, per
  the soft-checkpoint rule. No hard limit, authority expansion, or
  slow/networked/privileged check was involved.

## Remaining obligations and carried warnings

- Owed dependency acceptance dispositions (T-001.4, T-002.4, T-003.4,
  T-004.1–.3, INT-FLOW-001, TEST-STAB-001.1/.2) — owners: coordinator +
  fresh `task-acceptance-review` per package, before T-005.6's ART-012
  audit; carried forward from the preflight and T-005.1 acceptance-01.
- All role calls over staged controls (`unrun-role-boundaries.md` rows
  1–7) — owner: coordinator; behavioral qualification stays incomplete by
  authority, never inferred as passing.
- T-005.5 consumes this leaf's reviewed revision-recovery evidence;
  T-005.6 audits it in the ART-012 report.

## Review handoff

Per `review: immediate`, implementation checks are complete and this
invocation ends here as READY_FOR_REVIEW, without a review verdict.
Conditional-stage judgment for the route: no canonical deterministic
architecture command is declared in this repository (no architecture gate
to run; none invented); the maintainability stage does not apply to this
submission's bytes (documentation/evidence receipts only — no test, fixture,
harness or production code bytes changed; fresh reviewers may challenge
this judgment); no `docs/contracts` registry exists (the registry stage is
absent, not skipped).

Next owners, in order: fresh independent `task-review-discovery` evidence
over these bytes, then its report to a separate fresh
`task-acceptance-review` decision. Naming this route does not execute it;
the implementer invocation ends without a self-issued verdict.