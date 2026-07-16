# Execution Brief: `<ID>` — `<imperative title>`

| Field | Value |
|---|---|
| Status / owner | `draft \| ready \| blocked \| complete` / `<agent or person>` |
| Dependencies | `<IDs or none>` |
| Execution | `mechanical \| standard \| strong` agent; `low \| medium \| high` reasoning |
| Review | `mechanical \| milestone \| immediate` |

## Outcome

`<One testable sentence describing the result, not the implementation process.>`

## Authority and boundary

| Item | Contract |
|---|---|
| Entry criteria | `<passing baseline>`; `<required predecessor or capability>`; no overlapping user changes |
| Read only | `<authoritative section>`; `<closest precedent>`; `<owning test>` |
| Frozen decisions | `<decision>`; `<invariant>`; unresolved design decisions: `none` |
| Allowed paths | `<exact repository-relative path>`; `<exact repository-relative path>` |
| Out of scope | `<adjacent work>`; `<unauthorized network, dependency, commit, or destructive action>` |

If entry is false or a design decision remains, stop without editing. Do not
load future briefs, full transcripts, or unrelated planning docs.

## Work and acceptance

Required behavior:

1. `<Small implementation action.>`
2. `<Small implementation action.>`

- **AC-01:** `<Positive behavior with an observable result.>`
- **AC-02:** `<Negative or failure behavior with an observable result.>`
- **AC-03:** `<Compatibility, persistence, or unchanged-behavior requirement.>`

## Verification

Targeted check first:

```text
<single cheapest command that proves the task>
```

Broader check after it passes:

```text
<owning suite or repository gate, or N/A with reason>
```

## Budget, stop, and handoff

Pilot budget: `35 tool calls | 100,000 final input-context tokens | 90 minutes`.

Stop when the budget is reached, scope/authority must expand, verification is
ambiguous, or user changes overlap. Do not start adjacent work.

Report only changed files, AC evidence, commands/results, deviations or new
decisions, residual risks, and the exact next action.

The maintainer records token-efficiency results separately using
[execution-brief-pilot-measurement.md](execution-brief-pilot-measurement.md).
