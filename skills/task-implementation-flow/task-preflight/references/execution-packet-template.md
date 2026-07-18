# Task Preflight Packet: `<TASK-ID>` — `<brief title>`

## 1. Identity and status

| Field | Value |
|---|---|
| Task ID | `<stable ID>` |
| Artifact status | `ready \| blocked` |
| Producing stage | `task-preflight` |
| Created at | `<ISO-8601 timestamp with timezone>` |
| Repository root | `<absolute path>` |
| Durable packet path | `<absolute path outside repository, or proved ignored/status-neutral path>` |
| Task brief | `<exact path>` |

`ready` means the packet is fresh and executable under the recorded policy.
`blocked` means implementation must not begin.

## 2. Authoritative inputs and digests

Use lowercase SHA-256 digests of file bytes.

| Input | Identifier or path | Digest / value | Confirmed fact or decision |
|---|---|---|---|
| Task brief | `<exact path>` | `<sha256>` | `Status is ready_for_preflight and bytes stayed unchanged: yes \| no` |
| Primary authority | `<path>#<section>` | `<sha256>` | `<decision used>` |
| Dependency source | `<tracker/result path>` | `<sha256>` | `<dependency status>` |
| Repository instruction | `<applicable path>` | `<sha256>` | `<constraint applied>` |
| Run policy | `<identifier and path>` | `<sha256>` | `<permission/commit/verification/stop decision>` |
| Environment fingerprint | `<tool/env source or N/A>` | `<version/value/digest>` | `<why executability depends on it>` |

## 3. Repository baseline and dirty-path ownership

| Field | Value |
|---|---|
| `HEAD` | `<commit SHA \| unborn>` |
| Exact `git status --short` | `<verbatim snapshot, or clean>` |
| Baseline recaptured after packet write | `<unchanged \| changed with exact evidence>` |
| Packet-path neutrality | `<outside repository \| ignored and status-neutral before/after write \| unsafe>` |
| Incidental check artifacts | `<paths and disposition, or none>` |

| Status entry / path | Index blob SHA-256 or state | Worktree SHA-256 or state | Ownership | Task overlap | Evidence / disposition |
|---|---|---|---|---|---|
| `<verbatim status entry and path>` | `<sha256 \| absent \| deleted \| not_applicable>` | `<sha256 \| absent \| deleted \| not_applicable>` | `<user/task/tool/UNKNOWN>` | `yes \| no` | `<source and required route>` |

For renames, staged/unstaged combinations, and deletions, preserve the exact Git
status entry and record every involved path or explicit missing state. For an
`MM` path, record different index and worktree digests even when the short
status text remains unchanged.

## 4. Entry criteria and dependency evidence

| Criterion | Required state | Observed evidence | Result | Owner if failed |
|---|---|---|---|---|
| `<brief status/dependency/baseline condition>` | `<required value>` | `<path, tracker state, or command result>` | `pass \| fail \| gap` | `<stage/person>` |

## 5. Confirmed scope and prohibited paths

| Item | Confirmed contract and evidence |
|---|---|
| Allowed paths | `<exact paths and ownership evidence>` |
| Read-only context | `<exact paths>` |
| Prohibited paths/work | `<adjacent paths or decisions>` |
| Pre-existing user work | `<paths and required preservation behavior>` |
| Missing or wider scope request | `<none, or route to task-brief-designer>` |

## 6. AC execution plan

| AC | Invariant and oracle | Positive evidence | Negative / unchanged evidence | Real entry point and boundary | Repeated / recovery path | Exact command reference | Executable? |
|---|---|---|---|---|---|---|---|
| `<AC-ID>` | `<observable result and independent oracle>` | `<scenario>` | `<scenario>` | `<public workflow plus process/filesystem/database/etc.>` | `<first + legitimate state change + next occurrence, or N/A with reason>` | `<command ID>` | `yes \| no — evidence` |

## 7. Legacy-assumption findings

| Entry point / search | Exact relevant location | Finding | Implementation follow-through | Brief defect? |
|---|---|---|---|---|
| `<path and term/trace>` | `<path:line or no relevant match>` | `<confirmed fact>` | `<bounded instruction>` | `no \| yes — route` |

`N/A — <task-specific reason>` only when the brief establishes that no changed
workflow or lifecycle can reach a legacy assumption.

## 8. Verification helpers and exact commands

### Helper and oracle inventory

| Capability | Exact path / interface | Existence evidence | Authorized and usable? | Disposition |
|---|---|---|---|---|
| `<fixture/helper/runner/oracle>` | `<path and callable interface>` | `<inspection evidence>` | `yes \| no` | `<use \| blocked and owner>` |

### Commands

| ID | Class / cost | Exact copy-pasteable command | Working directory | Required environment | Purpose / ACs | Expected signal | Run? | Result | Broader authorization required? |
|---|---|---|---|---|---|---|---|---|---|
| `CMD-01` | `targeted; cheap/local` | `<exact command with no placeholders>` | `<absolute path>` | `<variables/tools/fixtures or none>` | `<behavior and AC IDs>` | `<exit/output/state oracle>` | `yes \| no` | `<exit code and concise evidence>` | `no \| yes — exact policy need` |

Do not mark the packet `ready` while a targeted command remains a family,
placeholder, guessed syntax, or unauthorized required operation.

## 9. Permission and commit envelope

| Action | Policy decision | Evidence / limit |
|---|---|---|
| Repository writes | `<allowed paths only after freshness check \| prohibited>` | `<policy source>` |
| Dependency changes / install | `<allowed \| prohibited \| approval required>` | `<exact limit>` |
| Network / live services | `<allowed \| prohibited \| approval required>` | `<exact limit>` |
| Privileged / destructive action | `<allowed \| prohibited \| approval required>` | `<exact limit>` |
| Slow / flaky verification | `<allowed \| prohibited \| approval required>` | `<exact limit>` |
| Commit / push | `<allowed \| prohibited \| approval required>` | `<exact identity/path limit>` |
| Stop / budget policy | `<checkpoint and two-strike or supplied rule>` | `<policy identifier>` |

## 10. Risks, gaps, and stop conditions

| Risk or gap | Evidence | Effect on verdict | Owning stage / person | Smallest next action |
|---|---|---|---|---|
| `<condition or none>` | `<path, digest, status, or command result>` | `<blocks \| authorized residual gap>` | `<owner>` | `<bounded action>` |

- Stop before the first edit if any recorded digest, `HEAD`, Git status entry,
  index state/digest, worktree state/digest, dependency source, instruction
  source, run-policy source, or required environment fingerprint changed
  without explanation.
- Stop on dirty overlap, scope widening, missing authority/helper/oracle,
  undeclared infrastructure, or an unapproved required check.
- Route contract defects to `task-brief-designer`; route stale/current-state
  failures through a fresh `task-preflight`.

## 11. Implementer instructions and required result format

For `ready` only:

1. Re-read the listed instructions and compare every freshness value, including
   each dirty path's separate index and worktree state/digest, before the first
   edit. Route any unexplained change back to `task-preflight`.
2. Change only the confirmed allowed paths and preserve all pre-existing user
   work. Do not create undeclared shared infrastructure or widen scope.
3. Establish the highest-risk fail-first evidence from the AC plan, implement
   the minimum task, then run exact targeted commands before broader commands.
4. Follow the permission, commit, checkpoint, two-strike, and stop envelope.
5. Write the result to `<required durable result path>` using
   `<worker-result schema path or supplied output contract>`. Report exact files
   changed, AC evidence, every command and truthful outcome, local decisions,
   questions, residual risks, status, and exact next action. Submission is not
   acceptance.

For `blocked`:

`Implementation must not begin. Route to <owner> to <smallest next action>, then run a fresh task-preflight.`
