# T-003 — retain live executable inputs

State: DEPENDENCIES_READY. Archive prerequisite: T-002 freshly recovered
`0ad1706cecc6f7d115e510762bf74c58d732cb6a` with all original paths/bytes/modes verified.

Copied exactly 13 inputs into tests/fixtures/review-composition/, preserving
original case IDs, historical evidence levels, scenarios, held-back oracles and
assertions. input-mapping.json gives every old/new path. Consumer constants and
embedded pointers now use the owned inputs. setup_consumer.py computes ROOT via
parents[5] at its new depth; staging behavior is unchanged. No skill-owned input
or shared runtime changed. Installer declarations were inspected and have no
retired-doc input; no installation refresh or profile change is needed.

Actual local checks (same focused command in all three trees):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py
```

- Original tree baseline: 22 tests, PASS (3.775 s).
- Migrated current tree: 22 tests, PASS (4.323 s).
- Disposable copy with all 182 originals removed and no original Git directory:
  22 tests, PASS (4.183 s), /tmp/documentation-cleanup-candidate-zjo6uppq.

The checks stage real fixture inputs, verify all handoff manifests, reject
degraded inventories/manifests, and verify evaluator-answer exclusion from the
route-consumer worktree, index, objects, refs and history. There is no runtime
Git/network fallback for retired documentation. Structural checks remain
structural; fixture staging is actual local behavior; installed-agent
qualification and historical raw-session recovery remain unrun.

Next: pin historical references, validate retirement guards, retire approved
paths, and run affected owner selectors on the final tree (T-004/T-005).
