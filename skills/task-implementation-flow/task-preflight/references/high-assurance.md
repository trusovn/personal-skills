# High-assurance preflight

Read before validating or acting on high-assurance inputs or strict packets.
Apply the entry's package prerequisites, guided coverage/feasibility/context,
starting-evidence/native-obligation rules, stop routes and evidence integrity.
This procedure does not replace those shared obligations.

## High-assurance workflow

1. Read the complete brief, required packaged task-local verification design,
   cited authority, applicable instructions, dependency source, and run policy.
   Confirm status `ready_for_preflight`. Treat verification design as derived
   guidance under the brief rather than independent requirements authority.
   Apply the same complete coverage, feasibility and context checks as guided
   packages; feasible absent future tests never waive required capabilities or
   the exact freshness checks below.
2. Resolve the durable packet path first. It must be the executable task
   package's `preflight.md`. A different path is a contract error: return
   blocked content without writing it and route package normalization or a
   corrected invocation to the owner.
3. Capture before checks:
   - brief bytes and lowercase SHA-256;
   - applicable verification-design path and lowercase SHA-256, or explicit
     `none`;
   - `HEAD` or `unborn` and exact `git status --short`;
   - separate index-blob and worktree digests/states for every pre-existing
     dirty path, including absent/deleted/not-applicable states;
   - dependency, instruction, and run-policy source digests; and
   - task-specific environment/tool fingerprints when executability depends on
     them.
4. Confirm dependencies, exact allowed paths, dirty ownership, permissions,
   commit policy, public entry points, helpers, fixtures, oracles, and legacy
   assumptions named by the brief. An absent required capability is a blocker,
   not new implementation scope.
5. Resolve every required targeted and broader command as copy-pasteable text
   with working directory, environment, purpose, expected signal, cost,
   authorization, whether it ran, and truthful result. When verification design
   applies, map its scenario IDs to those commands/oracles and leave any blocked
   or not-yet-executable scenario visible rather than silently dropping it.
6. Run only authorized cheap local baselines, narrowest first. Record incidental
   artifacts and do not claim a clean baseline until their disposition is
   explicit.
7. Recapture all freshness values before and after packet creation. Record both
   exact status snapshots and attribute the new/modified `preflight.md` entry.
   Any change beyond that one packet artifact, or any changed non-packet
   identity, blocks readiness. The packet need not be ignored or status-neutral.
8. Write exactly one packet using
   [execution-packet-template.md](execution-packet-template.md).

## Packet fields

Use these fields in addition to every shared section of
[execution-packet-template.md](execution-packet-template.md), before writing the
single canonical packet. Include every section below only for a high-assurance
packet.

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
