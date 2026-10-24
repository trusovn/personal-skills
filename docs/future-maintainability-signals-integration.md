## Proposed changes to `measure_maintainability.py`

Goal: Run a deterministic maintainability check immediately after `bounded-task-implementer`, independently of the implementing agent. Produce evidence for `task-maintainability-review`, without making arbitrary complexity thresholds automatic acceptance failures.

Based on `t-o-new-flow-2` (`f17b93a`), I would make the following changes.

| Priority | Change                        | Required behavior                                                                                                                                                              |
| -------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| P0       | Trusted baseline              | Capture exact source state before implementation, through the controller/preflight infrastructure, not the implementer. Store outside worker-writable scope.                   |
| P0       | Post-implementation execution | Controller/verifier runs the tool against the actual submitted files. Implementer cannot declare its own results authoritative.                                                |
| P0       | Separate outcomes             | Distinguish `PASS`, `WARNINGS`, `FAIL`, and `INCOMPLETE`. Complexity increases are warnings requiring review, not automatic failures.                                          |
| P0       | Portable comparisons          | Remove absolute checkout path from compatibility identity. Compare measurements across different sandbox directories with matching policies, versions, and scopes.             |
| P1       | Basic correctness linting     | Add selected Ruff `F` and `B` rules for objective defects. These can produce hard failures, unlike complexity heuristics.                                                      |
| P1       | Compact reports               | Produce concise machine-readable findings: changed symbol, metric, before/after, location, severity, evidence identity. Store full source snapshots separately.                |
| P1       | Improve change attribution    | Preserve conservative handling of renamed/extracted functions, but avoid treating every unmatched function as a design regression. Classify uncertainty separately.            |
| P1       | Reduce noisy metrics          | Keep Radon complexity and statement count advisory. Make parameter count optional or drop it if calibration shows low value.                                                   |
| P2       | Dependency boundary checks    | Support invoking a repository-native architecture checker (e.g. Import Linter), with specific forbidden imports and cycle rules. Don't implement a custom dependency analyzer. |
| P2       | Type/contract checks          | Incorporate existing type checking and schema/contract validation commands when a target repository supports them.                                                             |

## Expected workflow

Pre-implementation

Capture trusted baseline (no LLM judgment)

bounded-task-implementer

Implement changes; submit candidate

Deterministic check

Independent tooling

Run analyzers, compare baseline, produce findings

task-maintainability-review

Interpret advisory findings and architecture impact

Existing discovery / acceptance

Consume evidence without repeating the same review

The baseline capture doesn't need a separate LLM stage. It should be a cheap controller operation before the implementation worker starts. If the baseline is unavailable, the checker must report comparison evidence as incomplete rather than reconstruct an unreliable "before" state.

## Recommended decision semantics

| Finding                                             | Outcome                              |
| --------------------------------------------------- | ------------------------------------ |
| Complexity 6 → 8                                    | Warning, available for review        |
| Complexity 12 → 13                                  | Warning, potentially higher priority |
| New function complexity 15                          | Warning                              |
| Existing complexity 20 → 20                         | No new finding                       |
| Function renamed/extracted                          | Unmatched; review if relevant        |
| Undefined name or other selected correctness defect | Fail                                 |
| Forbidden dependency                                | Fail                                 |
| Analyzer unavailable or baseline incompatible       | Incomplete                           |
| All required checks completed, no findings          | Pass                                 |

The tool should not ask agents to refactor merely to improve metrics. It should report objective facts; the independent reviewer decides whether the design needs correction.

## What I would explicitly defer

I would not introduce cognitive-complexity scoring, CRAP scores, generic duplication detection, custom cross-language analyzers, or a comprehensive maintainability index yet.

I also wouldn't force all checks into `measure_maintainability.py` itself. Keep it as a narrow measurement/comparison implementation, while the deterministic stage invokes repo-native lint, architecture, and contract commands as appropriate.

### One additional requirement: test the checker

Before making this a standard step, extend `test_maintainability.py` to verify cross-sandbox comparisons, unavailable/stale baseline behavior, correct severity classification, intentional function extraction, and enforcement failures. Existing tests already cover many measurement scenarios.

Bottom line: Keep most of your current implementation. The essential work is making the baseline trustworthy, the checker independently executable, the reports portable and compact, and the outcomes suitable for automated routing.

That creates a useful deterministic stage without turning it into another expensive semantic reviewer or an incentive for agents to game code-complexity metrics.