# Project Plan — Post-project documentation cleanup

Status: `READY_FOR_PLAN_VERIFICATION`  
Plan version: `2026-10-14 / cleanup-v1`

## 1. Planning authority

### Product outcome

Free the completed delivery paths in `docs/` for the next cycle. Preserve original
documents, evidence and repository context in a fixed Git archive that a fresh
checkout can recover. Keep pending work visible and existing skill/test behavior
intact. This is repository maintenance, not a new product or documentation system.

### Authoritative inputs

- [Owner-approved idea brief](../documentation-consolidation.brief.md).
- Owner decision in this session: put this planning package in
  `ideas/documentation-consolidation/`; preserve the original docs for archival.
- Root `AGENTS.md`: surgical changes, truthful evidence, installation ownership,
  separate task results, and project-local installed-skill resolution.
- Root `README.md`: source/package/shared-tool ownership and installer boundaries.
- `tests/README.md` and `tests/test_review_composition.py`: existing evidence owners,
  commands and concrete consumers of retirement candidates.
- `docs/future-work/FEATURE-MAP.md`: future selection authority, not proof that old
  delivery work is complete.
- The active project-local delivery-plan and testing-discipline skills. The
  idea-challenger check narrows this to cleanup and exposes preservation risks.

The existing source, installer and local unittest setup are the maintenance
foundation. No charter or foundation-readiness review was supplied for this
cleanup; this plan claims neither. No AI runtime, new framework, architecture gate
or foundation change is needed. This plan does not certify historical completion.

### Settled decisions

Preserve `docs/project-plan.md` and `docs/task-map.json` throughout planning. IDs in
this package are local to **cleanup-v1**; they do not replace the old plan's IDs.
Archive the original repository state before retirement, dependency migration or
any later history rewrite. Pin historical references to the archive commit SHA;
the tag is fixed by convention and must resolve to that SHA.

Retirement targets only completed material within `docs/tasks/`, plus the old
`docs/project-plan.md` and `docs/task-map.json`. Preserve original verdicts and
qualification limits. Keep the active future-work catalog. Actual archive
publication needs an explicit execution decision. No rebase, squash, branch
deletion or force push is part of this plan.

## 2. Scope

### In scope

- Discover exact preservation/deletion scope, completion evidence, pending
  obligations, uncommitted assets and live consumers.
- Preserve the intended originals and full repository context under an unused,
  fixed archive tag; verify publication and recovery from the chosen destination.
- Copy necessary executable inputs to existing owned locations, then repair their
  consumers without weakening tests or changing skill semantics.
- Remove approved completed files only after preservation and dependency gates.
- Repair active references and leave a short archive pointer in existing
  navigation. Record tag, exact commit, recovery route and historical limits.
- Prove recovery and the usability of the cleaned tree with local evidence.

### Non-goals

No wiki, new documentation lifecycle system, workflow redesign, skill readability
refactor, planning-path policy change, historical report rewrite, gap closure,
broad document cleanup, installation refresh, or merge-history operation.
`docs/project-plan-review.md`, future-work notes (including `stale/`) and unrelated
docs stay active; only necessary reference repairs are in scope. The full snapshot
preserves them without authorizing their removal.

## 3. Actors and capabilities

The owner resolves preservation/disposition ambiguity and authorizes Git side
effects. The cleanup implementer audits, preserves, migrates and retires. Test
owners retain the observable oracles. A future agent/maintainer recovers history.
No concurrent writer may change approved inputs during a destructive step.

| ID | Actor / capability | Outcome | Critical flows |
|---|---|---|---|
| CAP-001 | Owner and implementer establish retirement eligibility | Exact scoped manifest and visible pending obligations | FLOW-001 |
| CAP-002 | Implementer preserves and exposes original history | Verified fixed archive, reachable beyond the current clone | FLOW-002, FLOW-004 |
| CAP-003 | Implementer retains executable dependencies | Consumers run without retired active-tree inputs | FLOW-003 |
| CAP-004 | Maintainers use a clean delivery workspace | Approved paths freed; backlog and history remain usable | FLOW-003, FLOW-004 |

## 4. Artifact and state catalog

The machine-readable catalog in [task-map.json](task-map.json) carries the same IDs.
Implementation evidence belongs next to this package, outside retirement targets;
these two files are the only artifacts created during planning.

| ID | Artifact/state | Kind | Source of truth / owner | Produced by | Consumed by | Lifecycle / invalidation |
|---|---|---|---|---|---|---|
| ART-001 | Original delivery corpus and repository context | persisted | Original files/Git; historical authors retain verdict authority | Existing delivery work | Audit, archive, migration, future retrieval | Existing -> captured history; originals remain unchanged until approved deletion. A changed byte invalidates affected scope/evidence. |
| ART-002 | Preservation, eligibility and consumer manifest | derived | Implementer records facts; owner settles ambiguous inclusion/disposition | T-001 | T-002 through T-005 | Durable scoped evidence: paths, bytes/hashes/modes, Git state, consumers, pending work, exclusions and reasons. Revalidate on material drift. |
| ART-003 | Archive identity and recovery receipt | audit | Fixed tag plus exact commit in selected Git destination; implementer records observed proof | T-002 | T-003 through T-005; later history-cleaning owner | Prepared -> local verified -> published/recoverable; local-only or mismatched refs block retirement. Never move an existing archive tag. |
| ART-004 | Retained executable inputs and consumer mapping | persisted | Existing test/skill/shared-tool owner at new owned paths | T-003, copied from ART-001 | Active tests, scripts, fixture staging, integration checks | Copied -> consumers rebound -> behavior checked. Historical originals remain archive truth; retained inputs follow their active owner's maintenance. |
| ART-005 | Active backlog, navigation and archive pointer | persisted | Existing future-work catalog/navigation; cleanup only repairs necessary context | Existing maintainers; T-004 repairs | Owner and future agents | Kept active; each pending obligation retains evidence/disposition/next owner. Historical links use ART-003, not reused live paths. |
| ART-006 | Cleaned active repository tree | persisted | Git candidate tree under the approved deletion/repair scope | T-003 migrates; T-004 retires | T-005, future delivery cycle | Original -> dependencies retained -> retirement candidate -> verified, or rejected/restored. New work can reuse freed paths after completion. |
| ART-007 | Migration, retirement and recovery evidence | audit | Observed checks tied to source/archive/candidate revisions and inputs | T-003 through T-005 | Subsequent tasks, independent reviewers, owner | Durable factual results; distinguish structural, actual local behavior and unrun agent qualification. Changed tested bytes stale affected claims. |

## 5. Lifecycle/state models

```text
UNAUDITED -> ELIGIBLE -> ARCHIVE_RECOVERABLE -> DEPENDENCIES_READY
     |           |              |                    |
     +-> BLOCKED +-> BLOCKED    +-> BLOCKED           +-> BLOCKED
DEPENDENCIES_READY -> RETIRED_CANDIDATE -> VERIFIED
                              |-> REJECTED -> scoped repair/restoration -> recheck
```

T-001 owns eligibility. T-002 owns archive identity/recoverability. T-003 owns
dependency readiness, T-004 the retirement candidate, and T-005 observed closure.
A failed/missing check never advances state. Independent review/acceptance, if
required by the executable task contract, remains separate from these observations.

Unfinished work blocks its retirement until the owner explicitly retains it or
records a disposition and sufficient active context/next owner. A historical
qualification gap may remain open; archiving it does not qualify behavior.

No multi-file transaction service is introduced. A partially applied retirement is
an unaccepted candidate: record the diff, finish or restore only approved changes,
and recheck. Revalidate relevant worktree bytes, scope, archive SHA and consumers
before each state transition. Serialize destructive work; concurrent drift stops
that step. Resume from verified current facts. Publication failure leaves the
originals intact. Retrying a matching existing tag is read-only; a tag conflict
needs a new owner-approved name, never a forced replacement.

Cancellation preserves receipts and originals. Restore retired paths from the
recorded SHA only after checking for newer work at those paths; never overwrite a
new delivery cycle. Consumer migrations may stay if still valid; undo reference
repairs as needed to keep the restored tree coherent.

## 6. Cross-task invariants

| ID | Invariant | Applies to artifacts/flows/interfaces | Intended verification |
|---|---|---|---|
| INV-001 | Every retired byte/path/mode is present in the original-context archive before removal; intended uncommitted assets are explicitly included or retirement blocks. | ART-001/002/003; FLOW-001/002/003; IF-001/002/004 | Scoped manifest vs archive tree/blob comparison; unresolved inclusion blocks deletion. |
| INV-002 | Archive tag resolves to the recorded exact commit in the chosen destination and a fresh retrieval; no move, overwrite or dependence on development-branch survival. | ART-003/005; FLOW-002/004; IF-002/005 | Fetch the named ref into a disposable repository and compare peeled commit and recovered bytes. |
| INV-003 | Active consumers have complete owned inputs and retain scenarios, setup, provenance distinctions and decisive oracles; no test is dropped/weakened merely to allow deletion. | ART-004/006/007; FLOW-003; IF-003/004 | Existing targeted baseline/post-migration checks plus real fixture staging; record unrun semantic qualification. |
| INV-004 | Pending work and historical limits remain visible without rewriting old verdicts or treating archive/structural success as behavioral qualification. | ART-001/002/005/007; FLOW-001/003/004; IF-001/004/005 | Reconcile discovered obligations with active context/next owner and immutable original evidence. |
| INV-005 | Active historical references resolve against the recorded archive commit; future reuse of live paths cannot silently change their meaning. | ART-003/005/006; FLOW-003/004; IF-004/005 | Classify references and resolve representative archived file/fragment targets using recovered content. |
| INV-006 | Scope, permission and freshness gates precede side effects; remove only eligible named targets, preserve unrelated work, and block on drift/failure. | ART-002/003/006/007; all flows and interfaces | Review scoped diff and current manifest; controlled failure cases retain originals and report a blocker. |

## 7. System interface map

| ID | Boundary / purpose | Owner / producer | Consumer | Inputs | Outputs | Important success + rejection semantics |
|---|---|---|---|---|---|---|
| IF-001 | Repository facts -> approved retirement scope | Audit implementer; owner resolves ambiguity | Archive/migration/retirement tasks | ART-001, ART-005 | ART-002 | Exact per-path inclusion, current identity, eligibility, consumers and obligation disposition. No inferred completion from commit labels. Unresolved ownership/inclusion blocks affected retirement. |
| IF-002 | Approved preservation set -> Git archive destination | Archive implementer under owner execution decision | Cleanup tasks, future retriever | ART-001, ART-002 | ART-003 | Commit includes intended originals in repository context before migrations; publish unused fixed tag, record peeled SHA and successful fresh recovery. Worktree status alone is insufficient; ignored/untracked intended inputs need explicit handling. Reject conflicts, omissions and unauthorized destination/push. |
| IF-003 | Historical executable input -> owned active input | Test/fixture/tool owner via migration implementer | Existing tests/scripts/staging consumers | ART-001, ART-002, ART-003 | ART-004, ART-006, ART-007 | Preserve input meaning, isolation, held-back oracles and assertion power; migrate all necessary path carriers. No runtime Git/network dependency. If behavior redesign is needed, block and split work. |
| IF-004 | Recoverable archive + ready consumers -> active-tree retirement | Cleanup implementer | Owner, future agents, final checks | ART-002, ART-003, ART-004, ART-005, ART-006, ART-007 | ART-005, ART-006, ART-007 | Delete only approved paths, repair active links, keep pending obligations, record pointer. Recheck evidence/freshness first; missing archive/dependency proof or unexpected diff blocks advancement. Interrupted edits remain a candidate. |
| IF-005 | Active archive pointer -> historical retrieval | Existing navigation and Git archive | Maintainer in disposable/fresh checkout | ART-002, ART-003, ART-005, ART-006 | ART-007 | Retrieve exact old files by recorded SHA/ref and verify bytes/context after retirement without relying on the original local clone. Failure is an incomplete cleanup, not a successful archive. |

The manifest/receipt formats are DELEGATED to owning tasks; the facts above are
fixed. Publication/recovery must record actual commands, destination and results.
Tag naming, remote choice and execution authorization remain owner decisions.
Use existing paths/ownership; a new module/tooling boundary requires separate
foundation placement work. Never refresh the active `.agents/` installation.

## 8. End-to-end data/process/state flows

### FLOW-001 — Establish safe scope

**Trigger:** owner selects documentation cleanup.  
**Terminal outcome:** current evidence-backed scope or an explicit blocker.

| Step | Actor | Action | Reads | Writes | Interface | Transition | Invariants / failures |
|---|---|---|---|---|---|---|---|
| S01 | Implementer | Inventory targets and intended dirty/untracked/ignored evidence, completion and consumers; inspect current coverage before changing it. | ART-001, ART-005 | ART-002 | IF-001 | UNAUDITED -> assessed | INV-001/003/004/006; unresolved facts remain unknown. |
| S02 | Owner + implementer | Resolve ambiguous preservation, active obligations and archive destination; freeze scoped facts and narrow commands. | ART-001, ART-002, ART-005 | ART-002 | IF-001 | assessed -> ELIGIBLE or BLOCKED | INV-001/004/006; no deletion while unresolved. |

### FLOW-002 — Preserve originals before changing dependencies

**Trigger:** eligible scope and explicit archive execution decision.  
**Terminal outcome:** recoverable original-context archive or intact originals and blocker.

| Step | Actor | Action | Reads | Writes | Interface | Transition | Invariants / failures |
|---|---|---|---|---|---|---|---|
| S01 | Implementer | Revalidate scope; capture intended original bytes in a full repository commit before cleanup, create unused archive tag and compare manifest to Git objects. | ART-001, ART-002 | ART-003 | IF-002 | ELIGIBLE -> local verified | INV-001/002/006; do not blindly commit unrelated dirty files. |
| S02 | Implementer | Publish to selected destination; fresh-fetch ref and verify exact commit/files/context; record receipt. | ART-001, ART-002, ART-003 | ART-003 | IF-002 | local verified -> ARCHIVE_RECOVERABLE | INV-001/002/006; failed publication/recovery leaves retirement blocked. |

### FLOW-003 — Retain dependencies, then retire documentation

**Trigger:** recoverable archive and current consumer manifest.  
**Terminal outcome:** cleaned candidate with preserved behavior and usable active navigation.

| Step | Actor | Action | Reads | Writes | Interface | Transition | Invariants / failures |
|---|---|---|---|---|---|---|---|
| S01 | Implementer/test owner | Establish targeted baseline, copy complete required inputs to existing owned locations, rebind consumers and stage real fixtures; compare scenarios/oracles and recheck. | ART-001, ART-002, ART-003, ART-006 | ART-004, ART-006, ART-007 | IF-003 | ARCHIVE_RECOVERABLE -> DEPENDENCIES_READY | INV-003/006; failed baseline or substantial redesign blocks retirement. |
| S02 | Implementer | Revalidate gates; delete eligible targets, repair current links/backlog context and add short fixed-SHA archive pointer in existing navigation. | ART-002/003/004/005/006/007 | ART-005, ART-006, ART-007 | IF-004 | DEPENDENCIES_READY -> RETIRED_CANDIDATE | INV-001/002/003/004/005/006; unexpected drift/scope blocks. |
| S03 | Implementer | Inspect deletion/repair diff, classify remaining historical vs live references and run affected local checks from cleaned tree without restored docs. | ART-002, ART-003, ART-004, ART-005, ART-006 | ART-007 | IF-004 | candidate -> locally checked or REJECTED | INV-003/004/005/006; preserve failure and next owner, no weakened assertions. |

### FLOW-004 — Recover history and close cleanup

**Trigger:** locally checked retirement candidate.  
**Terminal outcome:** evidence of cleaned-tree usability and exact historical recovery,
or a specific failed obligation/repair route.

| Step | Actor | Action | Reads | Writes | Interface | Transition | Invariants / failures |
|---|---|---|---|---|---|---|---|
| S01 | Fresh-checkout maintainer | Follow pointer, retrieve chosen published tag/SHA into disposable checkout; recover every retired path and verify manifest, original reviews and repository context. | ART-002, ART-003, ART-005, ART-006 | ART-007 | IF-005 | locally checked -> recovery checked | INV-001/002/004/005/006; local original objects must not mask missing remote archive. |
| S02 | Implementer | Reconcile recovery, pending work, archive identity, affected-test results and exact final diff; report remaining historical gaps. | ART-002/003/004/005/006/007 | ART-007 | IF-004, IF-005 | recovery checked -> VERIFIED or REJECTED | INV-001/002/003/004/005/006; archive/test gaps cannot be silently waived. |

## 9. Capability-to-flow coverage

| Capability | Flows | Artifacts | Interfaces | Invariants | Observable completion |
|---|---|---|---|---|---|
| CAP-001 | FLOW-001 | ART-001/002/005 | IF-001 | INV-001/004/006 | Explicit current eligibility and owner dispositions |
| CAP-002 | FLOW-002/004 | ART-001/002/003/005/007 | IF-002/005 | INV-001/002/004/005/006 | Fresh retrieval matches original manifest |
| CAP-003 | FLOW-003 | ART-001/002/003/004/006/007 | IF-003/004 | INV-003/006 | Existing consumers run with docs absent |
| CAP-004 | FLOW-003/004 | ART-002/003/004/005/006/007 | IF-004/005 | INV-001 through INV-006 | Approved paths freed, pending work visible, history recoverable |

Producer/consumer closure: ART-001 and the initial ART-005/006 are existing
repository sources; T-001 produces ART-002, T-002 produces ART-003, T-003 owns
ART-004 and changes ART-006, T-004 changes ART-005/006, and T-003/004/005 produce
ART-007. Historical originals have an explicit audit purpose. Each transition
has an owning task, prerequisite and failure destination above.

## 10. Implementation task map

The authoritative machine-readable map is [task-map.json](task-map.json).

| Task | Outcome | Depends on | Flow placement | Consumes | Produces/changes | Interfaces | Invariants | Integration boundary |
|---|---|---|---|---|---|---|---|---|
| T-001 Audit preservation and retirement eligibility | Scoped facts, pending-work disposition and test selection | — | FLOW-001 S01–02 | ART-001/005 | ART-002 | IF-001 | INV-001/003/004/006 | Every candidate has preservation, consumer and eligibility facts or a named blocker |
| T-002 Preserve and verify original-context archive | Published fixed tag/SHA with fresh-recovery receipt | T-001 | FLOW-002 S01–02 | ART-001/002 | ART-003 | IF-002 | INV-001/002/006 | Intended originals match recoverable Git objects before migration/deletion |
| T-003 Retain live executable dependencies | Owned inputs and unchanged decisive checks | T-001, T-002 | FLOW-003 S01 | ART-001/002/003/006 | ART-004/006/007 | IF-003 | INV-003/006 | All discovered consumers work without retirement paths |
| T-004 Retire completed docs and repair active navigation | Clean candidate, usable backlog and immutable historical links | T-001, T-002, T-003 | FLOW-003 S02–03 | ART-002/003/004/005/006/007 | ART-005/006/007 | IF-004 | INV-001 through INV-006 | Scoped removal passes preservation, dependency, navigation and local-check gates |
| T-005 Prove final recovery and cleanup closure | Revision-bound recovery and final integration evidence | T-002, T-003, T-004 | FLOW-004 S01–02 | ART-002/003/004/005/006/007 | ART-007 | IF-004/005 | INV-001 through INV-006 | Fresh retrieval and cleaned-tree behavior pass; unresolved historical gaps stay explicit |

### Task-planning handoff notes

- T-001 is read-only discovery. Review statuses and actual evidence, not just task
  index or commit summaries. The future catalog mentions remaining work; that is
  a reason to inspect, not a current completion verdict. Resolve Q-001–Q-003.
- T-002 needs owner-selected tag/destination and explicit execution authorization.
  Snapshot originals first. The currently untracked `ideas/` content needs an
  explicit preservation decision along with other discovered relevant assets.
- T-003 must retain existing coverage before relocation. Known consumers include
  composition JSON, historical result prose, fixtures/inventories, task index and
  old task map. Preserve structural-vs-behavioral-vs-unrun distinctions. Copy the
  complete dependency closure needed by the consumers; do not clone the whole
  documentation system. Substantial redesign becomes separately authorized work.
  Synchronize installer surfaces only if a managed package/shared input changes;
  do not refresh the active installation during this run.
- T-004 may repair references outside the retirement scope, including the old
  plan review, only as necessary. A remaining historical mention is not itself a
  live dependency. This new package stays outside the retired paths.
- T-005 checks actual retrieval after retirement. No proof of rebase/branch
  deletion is claimed. The tag's independent reachability supports later owner
  history decisions; no history operation is needed to test that property.

## 11. System verification map

This is intended implementation evidence, **not checks run during planning**.

| Flow / invariant / interface | Risk | Intended evidence/oracle and setup | Owner |
|---|---|---|---|
| FLOW-001; INV-001/004/006; IF-001 | Missing dirty assets or active obligations | Inventory tracked, staged, unstaged, untracked and relevant ignored files; reconcile each deletion with original bytes and completion/disposition evidence. Explicitly unresolved cases block deletion. | T-001 |
| FLOW-002; INV-001/002/006; IF-002 | Archive misses bytes or exists only locally | Compare complete preservation manifest to committed tree, blobs and modes; fresh-fetch selected destination/tag with no original-clone object fallback, compare peeled SHA and recovered content. A mismatched/missing ref fails. | T-002 |
| FLOW-003 S01; INV-003; IF-003 | Relocation changes setup/assertions or leaks evaluator inputs | Run existing focused tests before/after and stage affected real fixture scenarios. Preserve case IDs, verdict provenance, consumer-visible inputs, held-back keys and negative controls. Run with retired paths absent in a disposable candidate tree; no fetching historical docs to satisfy tests. | T-003 |
| FLOW-003 S02–03; INV-004/005/006; IF-004 | Broken links, hidden work, accidental extra deletions | Classify active references, resolve archive targets/representative fragments, reconcile pending-work context and review exact diff. Exercise missing archive, stale manifest and live-dependency blockers through a disposable operation/check procedure; original files must remain when a prerequisite fails. | T-004 |
| FLOW-004; INV-001/002/004/005; IF-005 | Fresh user cannot recover the original evidence | Follow final navigation in fresh/disposable context; retrieve every retired file, compare manifest and review contents, inspect original repository context. Test a missing/wrong ref as a failed recovery, not a silent fallback. | T-005 |
| FLOW-003/004; INV-003/006; IF-003/004 | Passing syntax checks hide broken behavior | Repeat affected targeted local behavioral/staging checks on final candidate. Structural assertions retain their narrower evidence label. Report unchanged historical agent-qualification gaps; no live model eval is implied. | T-003/004/005 |

Start with the known focused selector from `tests/README.md`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py
```

T-001 must identify further consumers and the narrow relevant selectors before
edits. Reuse existing coverage/helpers/negative controls. Do not add tests that
only restate new paths. Run installer tests if installed assets/projection change;
broader suites only for a demonstrated wider impact. Commands run one at a time,
dependencies ready first. Ask before slow/live-network/budget-consuming checks
unless that exact class is already authorized. Remote publication/recovery is a
later authorized operation, not part of this planning invocation.

## 12. Risks, assumptions, and delegated choices

### Blocking/open execution questions

- Q-001: What exact files and relevant uncommitted/ignored assets must the archive
  include? T-001 supplies facts; owner resolves ambiguity. Blocks T-002 onward.
- Q-002: Which unused archive tag, destination, publication authorization and
  existing navigation location should be used? Owner decides from T-001 context.
  Blocks publication/retirement/recovery, not read-only discovery.
- Q-003: Which candidates are genuinely completed, and how should remaining
  obligations be retained/disposed? T-001 audits; owner confirms ambiguous cases.
  Blocks affected retirement, never authorizes closing qualification gaps.

These are explicit discovery/owner gates, not silently delegated system decisions.
They do not block independent review of this gated plan. No cleanup may claim
completion until they are resolved and the gates are proved.

### Risks and stated assumptions

- The brief's “future-tasks” is interpreted as the current `docs/future-work/`
  catalog and notes, kept active without renaming. Verify during T-001.
- Completion is unproved. The catalog still mentions remaining T-003/T-004/T-005
  work; current evidence may permit retirement or require retained obligations.
- Concrete test consumers make dependency migration necessary; exact closure and
  size are unknown until T-001. Block/split if migration changes semantics.
- A tag stores committed objects only. Relevant dirty/ignored evidence can be
  omitted unless the manifest and snapshot comparison expose the omission.
- Git-backed external/LFS/submodule content, if discovered, needs demonstrated
  recoverability; ordinary tag success is insufficient. Resolve before retirement.
- The archive is fixed by convention, not by a new enforcement service. The
  recorded SHA detects later tag drift; failures must be reported.
- Reference-only repairs can still affect structural tests; scoped checks and
  truthful evidence labels are required. Cleanup does not prove agent compliance.

### Intentionally delegated task-local choices

- DELEGATED: compact audit/receipt format and exact result filenames beside this
  package; preserve required identity, bytes, commands, dispositions and outcomes.
- DELEGATED: use existing skill-owned/test-owned fixture locations and local
  helpers under current repository rules; exact paths may be chosen by the owner
  task without changing inputs/oracles/distribution semantics.
- DELEGATED: choose a small existing-nav paragraph and exact pinned-link syntax
  once the owner chooses location/destination; include tag, SHA, recovery route
  and original qualification limits without duplicating historical reports.
- DELEGATED: exact local Git inspection/recovery commands and targeted selectors;
  real committed-object comparison and fresh retrieval are fixed obligations.

## 13. Plan-verification handoff

Review [project-plan.md](project-plan.md), [task-map.json](task-map.json), the
owner-approved brief, repository rules, existing test ownership and current
original docs together. Original documents remain untouched by this plan.

Run `project-plan-verification` in a **fresh/separate agent**. Reconstruct scope,
producer/consumer closure, archive-before-migration ordering, active-obligation
gates and failure/recovery semantics independently. Do not treat structural JSON
validation as semantic review, behavioral preservation or archival completion.

Status: `READY_FOR_PLAN_VERIFICATION`.
