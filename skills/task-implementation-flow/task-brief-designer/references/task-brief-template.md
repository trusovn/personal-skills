# Task Brief: `<TASK-ID>` — `<imperative title>`

Status: `ready | ready_for_preflight | blocked_design`

```yaml
agent_tier: mechanical | standard | strong
reasoning: low | medium | high
review: mechanical | milestone | immediate
budget: <tool calls> / <time> / <context>
```

## Outcome

`<One testable sentence describing the approved result.>`

## Authority and scope

| Item | Contract |
|---|---|
| Authority | `<user request, issue, plan/spec path and section, or other source>` |
| Repository root | `<absolute path or working repository>` |
| Dependencies | `<IDs/states or none>` |
| Allowed changes | `<exact paths when known, otherwise bounded area for focused discovery>` |
| Read-only context | `<closest authority, precedent, or owning tests>` |
| Out of scope | `<adjacent work, permissions, or prohibited actions>` |
| Assumptions / unresolved decisions | `<none, UNKNOWN facts for discovery, or blocking decision and owner>` |

For an existing adequate brief, preserve its equivalent sections instead of
rewriting them into this table.

## Work and acceptance criteria

Required work:

1. `<Small implementation outcome.>`
2. `<Small implementation outcome.>`

- **AC-01:** `<Observable positive behavior or invariant.>`
- **AC-02:** `<Most credible negative, failure, or unchanged-state behavior.>`
- **AC-03:** `<Lifecycle, compatibility, or boundary behavior when relevant.>`

Omit AC-03 when it adds no distinct protection. Add more ACs only for distinct
approved outcomes.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first / regression | `<how the test rejects missing or faulty behavior, or why infeasible>` | `<exact command or focused discovery owner>` |
| Targeted | `<lowest reliable behavior and boundary>` | `<exact command or focused discovery owner>` |
| Owning suite | `<nearby regression coverage>` | `<command or N/A with reason>` |
| Broader gate | `<blast radius covered>` | `<command, approval required, or N/A with reason>` |

For repeated, resumed, retried, recovered, paginated, or migrated behavior,
include the first occurrence, its legitimate state change, and the next real
occurrence. Pure state simulation is insufficient when public wiring is the
risk.

## Stops and handoff

- Stop for ambiguous authority, user-work overlap, unsafe permission needs,
  material scope expansion, or a missing decisive verification capability.
- Treat the metadata budget as a checkpoint unless explicitly declared hard.
- Preserve pre-existing user work.
- Next action: `<guided implementation | high-assurance preflight | decision owner>`.

---

## High-assurance addendum

Include this addendum only when status is `ready_for_preflight` or when a
specific risk requires durable evidence. Do not add it to routine guided tasks.

### Artifact identity

| Field | Value |
|---|---|
| Task ID | `<stable ID>` |
| Producing stage | `task-brief-designer` |
| Created at | `<ISO-8601 timestamp with timezone>` |
| Primary authority | `<path>#<exact section>` |
| Known policy | `<identifier/path or UNKNOWN for preflight>` |

### Knowledge ledger

| Kind | Path or statement | Relevance / owner |
|---|---|---|
| Confirmed fact | `<fact and source>` | `<effect on task>` |
| Frozen decision | `<authority-entitled decision>` | `<source>` |
| Assumption | `<provisional fact>` | `<how preflight confirms it>` |
| Unresolved item | `<none or blocker>` | `<owner and smallest next action>` |

### AC execution matrix

| AC | Production invariant | Positive evidence | Negative evidence | Real entry point / boundary | Repeated or recovery path | Verification dependency |
|---|---|---|---|---|---|---|
| AC-01 | `<invariant>` | `<scenario/oracle>` | `<scenario/oracle>` | `<public workflow and boundary>` | `<first + state change + next, or N/A with reason>` | `<existing, task-local, prerequisite, or gap>` |

### Legacy-assumption and risk checks

| Area / search | Risk | Required evidence or follow-through |
|---|---|---|
| `<entry point, guard, literal, identifier, path, or baseline assumption>` | `<credible stale assumption>` | `<focused search/test>` |

| Risk | Impact / escalation trigger | Evidence and residual gap |
|---|---|---|
| `<credible failure>` | `<consequence>` | `<test level, real boundary, gap or none>` |

### Verification-capability inventory

| Needed capability | Disposition | Owner / path | Preflight confirmation |
|---|---|---|---|
| `<fixture/helper/runner/oracle>` | `task-local | prerequisite task | believed existing | blocked` | `<path or task>` | `<exact existence/interface question>` |

### High-assurance handoffs

- Preflight must confirm exact paths, dependencies, ownership, permission
  envelope, command syntax, decisive oracles, and required freshness evidence.
- Implementation may change only confirmed scope, must record every required
  command truthfully, and must produce the supplied structured result.
- Independent review must reconstruct the scoped diff, corroborate every AC at
  the required boundary, and issue a fresh verdict after every correction.
