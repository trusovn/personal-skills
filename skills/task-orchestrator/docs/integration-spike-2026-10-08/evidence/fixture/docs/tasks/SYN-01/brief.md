# Task Brief: `SYN-01` — Add prefix selection to `catalog.select_names`

Status: `ready_for_preflight`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: milestone
budget: 8 tool calls / 20 minutes / focused task context
```

## Execution sizing

- Sizing policy: `default@1`
- Estimated agent calls: `8`
- Estimated implementation duration: `20 minutes`
- Estimate confidence: `high`
- Policy result: `fits`
- Triggered limits: `none`
- Decomposition override: `none`

## Readiness route

`high-assurance preflight`

## Verification-design recommendation

`separate — mandated by the integration experiment; the finite default, empty-prefix, no-match, empty-input, ordering, duplicate, and non-mutation cases need an explicit oracle map.`

## Outcome

`catalog.select_names(names, prefix="")` returns, without mutating `names`, the input names that start with the case-sensitive string prefix, preserving input order and duplicates.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | `authority.md` — “Approved synthetic task SYN-01” |
| Repository root | `/private/tmp/task-flow-spike-2026-10-08` |
| Dependencies | None (`dependencies.json`: `SYN-01` has no dependencies) |
| Allowed changes | `catalog.py` and `tests/test_catalog.py` only |
| Read-only context | `authority.md`, `run-policy.json`, `docs/contracts/catalog.json`, `docs/contracts/index.json`, `README.md`, and existing tests |
| Out of scope | Invalid input types; changes outside the two implementation paths; contract-registry and README edits; network, dependency installation, commits, plans, and additional behavior |
| Assumptions / unresolved decisions | None. The current registry identifies `select_names` as a durable public function; preflight must confirm the current declaration and test command paths. |

## Work and acceptance criteria

Required work:

1. Change `catalog.select_names` to accept `prefix=""` and select names using a case-sensitive prefix match.
2. Extend `tests/test_catalog.py` with focused public-API tests for the approved selection and preservation behaviors.

- **AC-01:** Calling `select_names(names, prefix)` returns only entries whose values start with `prefix`, with case-sensitive matching, original order, and duplicates preserved.
- **AC-02:** Calling `select_names(names)` or `select_names(names, "")` returns all input names; the input list remains unchanged.
- **AC-03:** Empty input and a prefix with no matches each return `[]`.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| Selection preserves only prefix matches and their original sequence | matching and nonmatching names interleaved; repeated matching names; case-only mismatch | Public `select_names(names, prefix)` result equals the ordered expected list | Add focused regression tests in `tests/test_catalog.py`; run the targeted command | Independently invoke the public function with an interleaved, duplicated, case-variant list | Implementer: targeted test; acceptance reviewer: public-API corroboration |
| Default selection does not alter caller data | omitted prefix and explicit empty prefix; duplicate input values; empty list | Returned list equals expected values and the original input list is unchanged after each call | Add focused default/empty-prefix and non-mutation assertions | Check returned value and original input after public calls | Implementer: targeted test; acceptance reviewer: public-API corroboration |
| Empty outcomes remain valid lists | empty input; nonempty input with no matches | Public call returns `[]` | Add focused empty-input and no-match assertions | Invoke both boundary cases independently | Implementer: targeted test; acceptance reviewer: public-API corroboration |

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first / regression | Before the implementation change, new focused tests must reject the current one-argument/all-names behavior for a nonempty prefix; the assertion oracle is the ordered filtered result. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_catalog -v` |
| Targeted | Exercise the public function for case-sensitive prefix filtering, order, duplicates, omitted and empty prefixes, non-matches, empty input, and non-mutation. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_catalog -v` |
| Owning suite | Run the repository’s owning test suite after the targeted test passes. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` |
| Broader gate | No broader test suite is required by authority. Run architecture validation as a cheap local structural gate; it does not prove API behavior. | `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_architecture.py` |

## Stops and handoff

- Stop for ambiguous authority, overlap with pre-existing user work, unsafe permission needs, material scope expansion, or a missing decisive verification capability.
- Treat the metadata budget as a checkpoint unless explicitly declared hard.
- Preserve pre-existing user work.
- Next action: high-assurance preflight.
- Required ordered follow-on after a successful preflight: separate verification design; implementation limited to `catalog.py` and `tests/test_catalog.py`; independent maintainability review; contract-registry update; then fresh independent acceptance review. The registry updater, not the implementer, owns `docs/contracts/**` and stale `README.md` usage.

---

## High-assurance addendum

### Artifact identity

| Field | Value |
|---|---|
| Task ID | `SYN-01` |
| Producing stage | `task-brief-designer` |
| Created at | `2026-10-08T18:09:10+01:00` |
| Primary authority | `authority.md#Approved synthetic task SYN-01` |
| Known policy | `run-policy.json#synthetic-flow-spike-v1` |

### Knowledge ledger

| Kind | Path or statement | Relevance / owner |
|---|---|---|
| Confirmed fact | `authority.md` specifies the exact signature, behavior, implementation paths, tests, and no broader suite. | Bounds implementation and verification. |
| Confirmed fact | `dependencies.json` declares no dependencies for `SYN-01`. | Preflight has no upstream task prerequisite. |
| Confirmed fact | `docs/contracts/catalog.json` records `select_names`, owned by `catalog.py`, and its input-unchanged invariant. | Registry updater must synchronize the durable API record after implementation. |
| Frozen decision | `run-policy.json` fixes high-assurance artifacts, prohibits network/dependency installation/actor commits, and assigns registry paths to the updater. | All downstream stages must respect these ownership and policy limits. |
| Assumption | The supplied unittest and architecture commands resolve in the current repository. | High-assurance preflight confirms command syntax and availability. |
| Unresolved item | None. | N/A. |

### AC execution matrix

| AC | Production invariant | Positive evidence | Negative evidence | Real entry point / boundary | Repeated or recovery path | Verification dependency |
|---|---|---|---|---|---|---|
| AC-01 | Only case-sensitive prefix matches are returned, in order with duplicates. | Interleaved matching input returns ordered matching values. | Case-only mismatch and nonmatching values are absent. | Public `catalog.select_names(names, prefix)` call. | N/A: pure selection with no state. | Existing unittest runner; task-local tests. |
| AC-02 | Empty/omitted prefix returns all values without mutating the caller list. | Omitted and explicit empty prefix each return all values. | Original list differs after call. | Public `catalog.select_names` call and caller-owned input list. | N/A: pure selection with no state. | Existing unittest runner; task-local tests. |
| AC-03 | Empty input and no-match selection return an empty list. | Each boundary call equals `[]`. | Any retained value or non-list result fails. | Public `catalog.select_names` call. | N/A: pure selection with no state. | Existing unittest runner; task-local tests. |

### Legacy-assumption and risk checks

| Area / search | Risk | Required evidence or follow-through |
|---|---|---|
| `catalog.py:select_names` signature and existing default test | Existing one-argument implementation or test expectations conceal missing prefix behavior. | Preflight and implementation inspect the declaration and add a nonempty-prefix regression. |
| `docs/contracts/catalog.json` and `README.md` | Durable API documentation remains stale after the signature/behavior change. | Registry updater synchronizes the catalog record and stale README usage, then runs both registry commands. |

| Risk | Impact / escalation trigger | Evidence and residual gap |
|---|---|---|
| Case-insensitive or substring matching | Public API returns unauthorized names. | Focused case-variant and non-prefix tests; no residual gap after passing targeted test. |
| Returning/mutating caller list incorrectly | Breaks the durable non-mutation invariant. | Focused input-unchanged assertion; no residual gap after passing targeted test. |
| Registry validation treated as behavior proof | Stale or structurally valid metadata masks faulty API behavior. | API behavior is proven only by unittest and independent public-call review; registry commands remain structural evidence only. |

### Verification-capability inventory

| Needed capability | Disposition | Owner / path | Preflight confirmation |
|---|---|---|---|
| Public API behavior oracle | task-local | `tests/test_catalog.py` | Confirm tests can import `catalog.select_names` and assert ordered results. |
| Python unittest runner | believed existing | `python3 -m unittest` | Confirm supplied targeted and owning commands execute. |
| Architecture gate | believed existing | `tools/check_architecture.py` | Confirm command executes and allowed paths remain enforceable. |
| Registry structural validator | believed existing | `tools/check_contracts.py` | Confirm both supplied commands and updater ownership; do not use as behavior oracle. |

### High-assurance handoffs

- Preflight must confirm exact paths, empty dependencies, ownership, permission envelope, supplied command syntax, public-API oracles, and freshness evidence for this brief.
- The verification-design stage must create `docs/tasks/SYN-01/verification.md` as the separate, mandated pass and keep its test design within the approved behavior.
- Implementation may change only `catalog.py` and `tests/test_catalog.py`, must record required commands truthfully, and must produce the supplied structured result.
- Independent maintainability review is required before registry update and acceptance. The registry updater then owns `docs/contracts/catalog.json`, `docs/contracts/index.json`, and stale `README.md` usage, and runs `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_contracts.py --root . --write-index` followed by `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_contracts.py --root .`.
- Independent acceptance must reconstruct the scoped diff, corroborate every AC at the public API boundary, and issue a fresh verdict after every correction.

## Expected contract impact

- Plan refs: none — no plan applies.
- Current contract dependencies: `catalog.select_names -> docs/contracts/catalog.json`.
- Expected durable delta: change the public function signature and selection behavior; preserve the input-unchanged invariant; later synchronize the catalog contract record and stale README usage.
