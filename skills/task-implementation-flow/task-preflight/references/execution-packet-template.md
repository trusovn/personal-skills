# Task Preflight: `<TASK-ID>` — `<brief title>`

Status: `ready | blocked`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | `<brief or request and status>` |
| Repository | `<absolute root>` |
| Dependencies / entry criteria | `<confirmed state or blocker>` |
| Allowed scope | `<paths or bounded area>` |
| User-work ownership | `<clean, separable paths, or overlap>` |
| Permission limits | `<network/dependency/commit/destructive/slow-check policy>` |
| Profile | `guided | high-assurance` |
| Standalone preflight value | `<marginal/material and routine basis or exact uncertainty resolved>` |
| Source brief / revision | `<package brief.md and supplied revision/reference; request for direct work>` |
| Verification / Verification revision | `<package verification.md and current revision; N/A for direct work>` |
| Current applicability | `<current facts; expected effects; affected material changes/revision and decision>` |

## Decision context

Link relevant task/project direction, architecture and current/planned contracts.
Record intended use/operating envelope, failure consequences, relevant priorities,
required consumers, credible maintenance/planned changes, mitigations and unknowns.
Reassess relevant recorded known issues; no file means no recorded deferrals.
State ordinary assumptions without routine questions. Use current authority first
for serious-delay/costly-later uncertainty; retain any unresolved decision, owner
and focused question. Do not invent policy or waive required proof.

## Acceptance evidence and commands

| AC / scenario / risk | Authority relationship | Setup / decisive boundary / oracle | Exact command / cwd | Feasibility: dependencies / permissions / ownership | Baseline result / gap |
|---|---|---|---|---|---|
| `<IDs; account for every material row>` | `<brief/cited authority>` | `<required inputs and decisive observation>` | `<command or feasible planned future-test command>` | `<conclusions and evidence; blocker/owner if absent>` | `<passed baseline, intended fail-first, not run, or blocker; readiness is not future behavior proof>` |

For guided packages, these compact sections are required at `preflight.md` beside
`brief.md`, even for routine work. Direct requests may use inline readiness.
No digest ledger, tracker, schema, instrumentation or separate context artifact
is required by package presence alone. Missing/foreign verification, omitted
ACs, unsupported scenarios or weak oracles prevent ready. Future task-owned tests
may be absent with feasible in-scope setup; unavailable indispensable capabilities
block and belong to their prerequisite owner.

A reasoned coverage revision retains IDs, supersedes affected old readiness and
needs focused current preflight bound to the new revision. Reuse unchanged facts.
Material authority/prerequisite/ownership/permission/capability changes need
reconsideration; expected implementation/report effects alone do not force full
rediscovery. Requirement changes return to task design. None of these guided
rules relax the high-assurance addendum below.

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| `<none, warning, or blocker>` | `<non-blocking limit or why implementation cannot begin>` | `<person/stage>` | `<action>` |

For `ready`, state the implementation stops and the next exact action. For
`blocked`, state that implementation must not begin.

---

## High-assurance packet addendum

Include every section below only for a high-assurance packet.

### Artifact identity and inputs

| Field | Value |
|---|---|
| Task ID | `<stable ID>` |
| Producing stage | `task-preflight` |
| Created at | `<ISO-8601 timestamp with timezone>` |
| Durable packet path | `<task-package>/preflight.md` |
| Task brief | `<exact path and lowercase SHA-256>` |
| Verification design | `<required package verification.md, revision and lowercase SHA-256>` |
| Primary authority | `<path>#<section> and digest>` |
| Dependency source | `<path, digest, and state>` |
| Instructions | `<applicable paths and digests>` |
| Run policy | `<identifier, paths, and digests>` |
| Environment fingerprints | `<values/digests or N/A>` |

### Repository baseline and dirty ownership

| Field | Value |
|---|---|
| `HEAD` | `<commit SHA or unborn>` |
| Pre-write `git status --short` | `<verbatim snapshot or clean>` |
| Post-write `git status --short` | `<verbatim snapshot including only the attributed packet delta>` |
| Packet artifact delta | `<new or modified <task-package>/preflight.md>` |
| Final non-packet baseline recapture | `<unchanged or exact blocker>` |
| Incidental artifacts | `<paths/disposition or none>` |

| Status entry / path | Index SHA-256 or state | Worktree SHA-256 or state | Ownership | Task overlap | Evidence / disposition |
|---|---|---|---|---|---|
| `<verbatim status and path>` | `<sha256, absent, deleted, or not_applicable>` | `<sha256, absent, deleted, or not_applicable>` | `<user/task/tool/UNKNOWN>` | `yes | no` | `<source/route>` |

Preserve separate index and worktree identities for staged/unstaged
combinations, renames, and deletions even when short-status text is unchanged.

### Exact command records

| ID | Class / cost | Exact command | Working directory / environment | Purpose / ACs | Expected signal | Run? / result | Authorization |
|---|---|---|---|---|---|---|---|
| `CMD-01` | `<targeted; cheap/local>` | `<no placeholders>` | `<cwd and variables>` | `<behavior>` | `<observable oracle>` | `<yes/no; exit and signal>` | `<allowed or approval need>` |

### Helper and capability inventory

| Capability | Exact path / interface | Existence evidence | Authorized and usable? | Disposition |
|---|---|---|---|---|
| `<fixture/helper/runner/oracle>` | `<path/interface>` | `<inspection evidence>` | `yes | no` | `<use or blocker/owner>` |

### Implementer contract

Before the first edit, the implementer must recalculate the recorded brief,
verification-design (when present), Git, dirty-path, dependency, instruction,
policy, and environment identities. It must also match the recorded post-write
status and confirm that the packet artifact is the only delta from the
pre-write baseline.
It may change only allowed paths, must preserve pre-existing work, run exact
commands progressively, and produce the supplied structured result. Any
unexplained freshness mismatch routes to fresh preflight.
