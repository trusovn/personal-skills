# Verification Design: SYN-01 — Add prefix selection to `catalog.select_names`

Source brief: docs/tasks/SYN-01/brief.md
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | One interleaved public call proves prefix-only selection, case sensitivity, order, and duplicate preservation. |
| AC-02 | V-02 | Omitted and explicit empty prefixes both return all values without changing the caller list. |
| AC-03 | V-03 | Both required empty-result boundaries return an empty list. |

## Verification scenarios

### V-01 — Prefix selection retains only ordered case-sensitive matches

Covers: AC-01; Selection preserves only prefix matches and their original sequence

Intent: Reject all-names behavior, substring matching, case-insensitive
matching, reordering, or duplicate collapse.

Given:
- a list with interleaved matching and nonmatching values, repeated matching
  values, and a value differing only by case

When:
- `catalog.select_names(names, prefix)` is called with a nonempty prefix

Then:
- the result contains only values beginning with that exact case-sensitive
  prefix, in their original order, including each matching duplicate
- nonmatching values and case-only mismatches are absent

Oracle / boundary:
- compare the returned value of the public `catalog.select_names` call with
  the exact ordered expected list

Variants:
- interleaved matching/nonmatching values; repeated matching values; a
  case-only mismatch

### V-02 — Default prefixes preserve all caller values without mutation

Covers: AC-02; Default selection does not alter caller data

Intent: Reject a default that filters values, an explicit empty prefix that
differs from the omitted default, or mutation of the caller-owned list.

Given:
- a nonempty list containing duplicate values

When:
- `catalog.select_names(names)` and `catalog.select_names(names, "")` are
  called

Then:
- each result equals all input values in their original order
- the original input list remains unchanged after each call

Oracle / boundary:
- compare each public-call result and the caller-owned list with their expected
  values

Variants:
- omitted prefix; explicit empty prefix; duplicate input values

### V-03 — Empty-result boundaries return empty lists

Covers: AC-03; Empty outcomes remain valid lists

Intent: Reject retained values, a non-list result, or a special-case failure at
either required empty boundary.

Given:
- an empty input list
- a nonempty input list whose values do not start with a selected prefix

When:
- `catalog.select_names` is called for each boundary condition

Then:
- each call returns `[]`

Oracle / boundary:
- compare each returned value at the public `catalog.select_names` boundary
  with `[]`

Variants:
- empty input; nonempty input with no matches

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios.
- Concrete test structure, framework usage, helpers, and file placement remain
  implementation choices unless already fixed by repository authority.
- If implementation discovery shows that a scenario cannot be exercised at its
  stated boundary, route the conflict back to task design/preflight rather than
  silently weakening the oracle.
