# Architecture enforcement model

Use this reference when deciding **what may block mechanically**, what should be
only reviewer evidence, and how existing debt can coexist with a no-regression
gate.

## 1. Three evidence classes

### HARD

A deterministic violation of an explicit invariant.

Examples when grounded by the repo:

- `domain -> infrastructure` is forbidden
- production modules must not import test modules
- feature package A must not reach into feature package B's private internals
- a declared plugin/package set must remain independent
- cycles are prohibited inside a named package set

A HARD violation may make the architecture command non-zero and may directly
produce `CHANGES_REQUESTED`.

### SIGNAL

A machine-detected fact that may correlate with maintainability problems but is
not itself a semantic verdict.

Examples:

- file grew from 320 to 570 lines
- function complexity rose from 8 to 17
- module fan-out rose from 6 to 14
- a new generic `helpers` module appeared
- a conditional dispatcher gained another behavior branch

Signals should normally be warnings/report data. `task-maintainability-review`
uses them to decide whether the current change introduced a concrete problem.

### EXISTING_DEBT

A hard-rule violation that predates activation of the rule and has been
explicitly accepted **only for no-regression migration purposes**.

Existing debt is not a warning and not an endorsement. It is a bounded exception
that must not grow silently.

## 2. When a rule is safe to make HARD

Require all of these:

1. **Authority** — the boundary is documented, established by an accepted
   architecture decision, or explicitly authorized during foundation work.
2. **Consequence** — violating it creates a concrete ownership/coupling/testability
   problem rather than merely offending a preferred style.
3. **Determinism** — the checker can identify violations consistently with low
   false positives.
4. **Actionability** — failure output tells a future developer where the illegal
   edge is and what boundary should be used instead.

If any criterion is weak, keep the check advisory or leave it to semantic review.

## 3. Clean and no-regression semantics

### CLEAN

```text
current governed violations = 0
new governed violation       = FAIL
```

### NO_REGRESSION

```text
known existing violations    = tolerated by exact baseline
removed violation            = baseline should shrink
same unchanged violation     = tolerated / visible
new violation                = FAIL
expanded violation           = FAIL
baseline expansion           = explicit architecture change, never automatic
```

Prefer native tool baselines/known-violation facilities when they provide these
semantics **and a non-mutating freshness failure for stale entries**. The
canonical command runs freshness before the normal ignored-violation check:

```text
freshness: stale baseline/exception identity = FAIL; tracked baseline unchanged
normal:    known current identity = tolerated; unknown identity = FAIL
```

For a file baseline, generate a shrink-only candidate in a temporary path and
fail if it differs from the tracked file. For native exact exceptions, configure
the tool to error on unmatched exceptions. Otherwise store stable exact
violation identities (rule + source + target, or the closest reliable
equivalent) and compare them in a small wrapper.

Do not baseline unstable line numbers if source/target dependency identity is
available.

## 4. Baseline review rules

A baseline entry should answer:

- which hard rule is being excepted?
- what exact edge/entity is pre-existing?
- why is cleanup intentionally out of current scope?
- how will a removed violation stay removed?

Exercise this regression scenario before accepting `NO_REGRESSION`: baseline an
exact edge; remove it and observe the freshness failure; apply the reviewed
baseline shrink; reintroduce the edge and observe the ordinary gate failure.

Reject patterns such as:

```text
ignore everything under legacy/**
ignore all domain -> infrastructure imports
regenerate baseline before validation
```

unless a deliberate architecture decision explicitly accepts that entire scope.
Broad exceptions are policy, not bookkeeping.

## 5. Failure sentinel

A current green run proves only that the current tree does not trigger the
configured rule. It does not prove the rule is wired correctly.

For at least one important rule, create a safe disposable violation and observe:

```text
expected: architecture command exits non-zero and names the violated rule/edge
observed: same
cleanup: disposable change removed
final: architecture command green again
```

Prefer a fixture or isolated worktree. Never overwrite unrelated dirty user work.

## 6. Semantic review packet

Do not force a cheap reviewer to rediscover the whole repository. Supply or let
it cheaply derive:

```text
TASK
  short task/request summary

CHANGED_PRODUCTION_FILES
  changed source paths

ARCHITECTURE_GATE
  canonical command
  pass/fail
  hard violations
  warnings/signals

POLICY
  relevant architecture-map/ADR/rule paths
  clean vs no-regression mode
  baseline changes, if any

DIFF
  current change plus immediate neighbors only when needed
```

Optional useful derived facts:

- new dependency edges
- dependency fan-out delta
- file/function complexity delta
- newly duplicated business rule
- new generic helper/manager module

These facts are evidence, not a home-grown scoring model.

## 7. Reviewer decision boundary

A maintainability blocker should be:

```text
concrete introduced/worsened design problem
    + evidence in current diff / immediate dependency context
    + plausible maintenance cost or breakage risk
    + smallest reasonable correction direction
```

Do not block because:

- another design is prettier
- a file crosses a generic size threshold
- a class does not have an interface
- a known untouched legacy smell exists
- the reviewer can imagine a hypothetical future requirement with no evidence

## 8. Promotion/demotion of rules

A SIGNAL may become HARD later only after the project establishes a concrete
invariant and the automated check demonstrates acceptably low false positives.

A HARD rule that repeatedly needs broad exceptions is evidence to revisit either:

- the architecture decision, or
- the check's precision.

Do not keep widening exceptions until the rule becomes decorative.
