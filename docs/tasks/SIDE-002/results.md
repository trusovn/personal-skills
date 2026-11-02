# SIDE-002 implementation evidence

Implemented: READY_FOR_REVIEW. Authority: [brief.md](brief.md), unchanged SHA-256
`f92313465887e2aa977056f54991bdb76bcf28e2771c42fe2a4e8eb8f6debdb5`.
Entry: [preflight.md](preflight.md), guided ready, and [verification.md](verification.md)
revision 1. This is an implementation handoff, not an acceptance decision.

## Deliverables and contract impact

Brief guidance and template now retain requirements in titled ACs or precise
authority. Risk notes are optional. Verification guidance owns detailed cases,
observations, implementation evidence, independent corroboration and gate
allocation even without risk rows. The shipped profile guide supplies the precise
submission-route anchor; the source flow README points to that authority; execution metadata stays together. Split and
high-assurance forms preserve authority, ownership, sizing and audit boundaries.

Actual contract impact: changed document-output responsibilities of
`task-brief-designer` and `task-verification-designer`; added the shared
`skills/README.md#submission-route` reference. No runtime, schema, sizing threshold,
review policy or registered executable authority changed. Executable contract
declarations changed: none. Registry synchronization is left to its separate
owner; expected registered-record delta is none.

Existing finite-risk eval 5 retains all artifact families, publication prefixes,
orphan states and EVD-12 evidence responsibilities without requiring six fields
in a brief. The queue and direction evals use the same content boundary.
The existing lifecycle fixture now tests derivation without ROW IDs; other
revision/closure fixtures retain supplied-risk-ID traceability. Two focused
structural tests protect the boundary and discriminating fixture inputs.

Inspected installer membership/constants, recursive package copy, focused tests,
profile guide and README installation contract. Both skills and all changed
resources are already copied recursively. No profile member or shared dependency
changed; the managed profile guide now carries the
route. Focused installed-profile coverage resolves its reference after a real
disposable installation; no installer ownership expansion is necessary. No active
installation, existing task artifact, plan or review history was rewritten.

## Scenario evidence

[Worked pairs and requirement/consumer maps](worked-examples.md) are illustrative,
source-guided document reviews. They are not executed skill evals, hypothetical
runtime tests or model qualification. No live/model budget was approved.

| Verification ID | Implementation evidence and limits |
|---|---|
| V-01 | API-5 pair: result/consumer opening; titled independent ACs; no risk section; nonblank control and empty/whitespace refusal with stored-name preservation. |
| V-02 | EVD-12 pair: exact five families, four publications, five prefixes and four orphans map to ACs and V-01a–e/V-02a–e/V-03a–d. Public pre-effect observer, byte reuse, first/change/next, distinct review probes and final-reviewer aggregate ownership remain explicit. Observer feasibility is not claimed. |
| V-03 | Consumer map traces authority/scope/ACs, cases, revision, implementation evidence and separate discovery/acceptance. Shared route retains preparation and conditional/correction order. Source consumers do not require fixed risk headings; no consumer edit was needed. SIDE-001 case presentation and singular per-artifact source metadata remain. |
| V-04a | TASK-40 composite and all three child/verification pairs retain requirement ownership, acyclic dependencies, independent sizing and final FLOW-40 closure. Undefined source contract fields are exposed, not invented; these hypothetical leaves are not certified implementation-ready. |
| V-04b | S3-04 pair retains public command, durable running state, reload and second selection, running exclusion/empty behavior, exact fixture provenance, provisional knowledge and precise freshness/machine references. No packet/schema was supplied or invented. |
| V-05 | API-5 permits derived cases without R rows. RET-8 contrast returns needs_brief_revision to the product owner, preserving the existing marker and absent/unchanged verification artifact; no deletion rule is invented. Existing ambiguity eval/refusal coverage remains. |
| V-06 | Source/template/completion/eval consistency, targeted checks, installer and aggregate evidence below. Existing artifact hash and final diff checked; installed drift remains visible. |

## Verification record

All commands run at repository root. Structural assertions do not establish
model compliance. The controlled pre-change probe imports the new structural
test against HEAD's old brief-designer package and obtains exactly the intended
missing-optional-risk assertion; log `/tmp/side002-prechange-sensitivity.log`.

- C1: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py` — 16 tests passed, repeated after source edits.
- C2: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p 'test_*.py'` — 3 tests passed; aggregate rechecks final bytes.
- C3: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` — 36 tests passed on frozen source; `/tmp/side002-installer.log`. An earlier run had 14 cascading snapshot differences because implementation edited managed source during that run; discarded as concurrent-source evidence and rerun sequentially.
- C4: `python3 tools/verify.py` — 7 checks, 3 failed on pre-correction bytes; `/tmp/side002-aggregate.log`. Containment: 207 orchestrator tests, 3 failures/13 errors due to unavailable sandbox mechanism/EPERM. Root suite: 307 tests, 1 stale inline-route assertion failure and 31 skips; that assertion is corrected below. Contract check passed (6 subsystems, 12 refs). Installed-profile drift was reported, including pre-existing and changed managed source; installation was not refreshed. No corrected aggregate or successful host execution is claimed.
- C5/C6: architecture final correction check recorded below; contracts passed in the aggregate, with no registry bytes changed. Final discovery owns corrected aggregate and host containment proof.
- `git diff --check` — passed. Brief SHA-256 matches readiness and verification.

## Remaining route

Separate maintainability review → contract-registry updater (check actual impact;
expected no registered delta) → fresh independent task-review-discovery → separate
task-acceptance-review. The coordinator starts each separate role. Corrections
re-enter affected conditional stages before fresh discovery and decision.

## MNT-01 correction pre-edit coverage map

Preceding verdict: CHANGES_REQUESTED, [maintainability-01.md](reviews/maintainability-01.md).
Broken invariant: a mandatory shared reference must resolve within the same
installed profile; a source-only README cannot supply omitted route authority.

| Row | Prior reviewer status | Planned implementation evidence / navigation | Next owner |
|---|---|---|---|
| MNT-01 | fail, confirmed | Move canonical route to shipped skills/README.md; resolve source/template references through a disposable installed profile; preserve preparation/conditional/correction order. | Fresh maintainability reviewer; prior fail unchanged |
| V-01 | unchecked by functional reviewer | Existing API-5 pair is navigation only; no changed behavior in this correction. | Fresh discovery |
| V-02 | unchecked by functional reviewer | EVD-12 pair remains navigation; verify its shared route resolves to shipped authority. | Fresh discovery |
| V-03 | unchecked by functional reviewer | Installed link regression and corrected stale flow-guide test; complete ordered route in shipped guide. | Fresh discovery |
| V-04a | unchecked by functional reviewer | TASK-40 parent/children remain navigation; update shared reference only. | Fresh discovery |
| V-04b | unchecked by functional reviewer | S3-04 pair remains navigation; update shared reference only, retain exact freshness rules. | Fresh discovery |
| V-05 | unchecked by functional reviewer | Existing ambiguity contrast remains navigation only. | Fresh discovery |
| V-06 | unchecked by functional reviewer | Focused installed-profile regression, preparation/guide/installer suites; preserve drift and sandbox failures. | Fresh discovery |

Correction gate owner: implementation runs targeted/owning suites and required
architecture; final discovery owns corrected aggregate. Original sandbox
aggregate: 7 checks, 3 failed (containment EPERM, stale inline-route assertion,
installed drift), 31 root-suite skips. Contracts passed. Host escalation waited
for approval and was interrupted after 373.8 seconds; no host log or result exists.
No denial was bypassed and no installed files were refreshed.

## Correction submission

Implemented: READY_FOR_REVIEW

- Authority: `docs/tasks/SIDE-002/brief.md`; preflight/context: `docs/tasks/SIDE-002/preflight.md`, `docs/tasks/SIDE-002/verification.md` revision 1.
- Preceding verdict: CHANGES_REQUESTED, `docs/tasks/SIDE-002/reviews/maintainability-01.md`; complete finding: MNT-01, mandatory route authority was absent from installed distribution. The complete pre-edit ledger above retains MNT-01 fail and V-01–V-06 unchecked; no reviewer row status is changed by this implementation.
- Correction: canonical shared route now lives in already-shipped `skills/README.md#submission-route`. Designer resolves `../../README.md`; template resolves the same active-installation guide; flow README references the canonical owner. Worked pairs and source guards use the shipped owner.
- Influenced siblings: generated briefs, source flow guide, profile guide, disposable installed designer/template access, and all worked-pair route references. No runtime or installer ownership expansion.
- Attempts/discarded hypotheses: no host aggregate result; escalation was pending then interrupted. Initial installer run was invalidated by concurrent source edits and rerun on frozen source. No other discarded correction approach or hidden partial patch.
- Current scoped diff: two authoring skills/instructions/template/evals, lifecycle fixture, shipped/source guides, preparation/flow/installer tests, worked examples and this task result. Pre-existing staged brief remains byte-identical. Reviewer report remains untouched.
- MNT-01 implementation evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k test_installs_profile_preserves_agents_text_and_final_availability` — first failed because the installed route targeted the absent flow README (`/tmp/side002-mnt01-red.log`), then passed after correction (`/tmp/side002-mnt01-green.log`). Real disposable installation, resolved reference and target anchor are checked. Prior reviewer fail remains pending fresh review.
- Owning suites, corrected source: preparation-contract 16 tests, flow-guide 14 tests, brief-designer package 3 tests, full installer 36 tests all passed. Installer log: `/tmp/side002-installer-corrected.log`. Commands are the C1/C2/C3 commands above plus `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py`.
- Architecture: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — 4 tests passed on corrected bytes. Final `git diff --check` passed; brief digest still matches entry.
- Broad gate: corrected `python3 tools/verify.py` not run by correction implementer; final fresh discovery owns the justified corrected aggregate and host containment execution. Preserve the original three failed checks and all reported skips; targeted green does not replace them.
- Remaining reviewer coverage: MNT-01 requires fresh maintainability review; all V rows require fresh discovery and separate acceptance. Model compliance remains unqualified; manual worked outputs are source-guided examples only.
- Next: fresh maintainability review → contract-registry updater → fresh independent task-review-discovery → separate task-acceptance-review. No acceptance verdict is issued here.
