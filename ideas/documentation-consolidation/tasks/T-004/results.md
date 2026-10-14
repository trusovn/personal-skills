# T-004 — retire completed docs and repair navigation

State: RETIRED_CANDIDATE, locally checked. Prerequisites: owner-approved Q-001/Q-003
scope/disposition, T-002 published/recovered `0ad1706cecc6f7d115e510762bf74c58d732cb6a`,
and T-003 retained-input checks.

Removed exactly the 182 manifest-approved tracked paths under docs/tasks/ plus
docs/project-plan.md and docs/task-map.json. No other deletion appears in the
Git diff. Ignored Finder metadata remains excluded and untouched. All 15
future-work files and docs/project-plan-review.md remain active.

README contains the fixed tag, full SHA, original-doc link, fresh retrieval
commands and brief incomplete-qualification note. Historical navigation,
retained report references and future-work pointers now resolve to the fixed
SHA. Current delivery cautions in FEATURE-MAP and the system-verification concept
were updated to the owner disposition; detailed original verdicts stay unchanged
in the archive. Templates and synthetic fixture docs/tasks paths remain their
existing conventions. Cleanup planning/audit path mentions are historical
inventory/authority, not live original-file consumers.

The same inline checked retirement procedure was exercised on disposable state
and applied to the actual tree. guard-evidence.json records missing archive,
stale original bytes, missing retained input and unmigrated consumer cases; each
blocked before deletion and left all 182 originals present. Valid prerequisites
retired the exact set. No reusable cleanup service or tooling was added.

Reference reconciliation: 106 fixed-SHA archived file links have
recoverable targets; original relative/mutable links and unqualified path
citations are absent from the repaired navigation. Archived heading fragments
were checked against recovered text. Detailed link targets and final recovery
are recorded by T-005.

Final local owner checks pass: 142 tests in 9 sequential focused selectors.
Test assertions/oracles were preserved; a pure Markdown whitespace repair does
not change the tested runtime. No installation refresh, branch commit, rebase,
squash, branch deletion or force push occurred.
