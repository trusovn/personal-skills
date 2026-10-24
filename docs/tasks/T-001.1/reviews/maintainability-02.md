VERDICT: ACCEPT
ARCHITECTURE_GATE: PASS

BLOCKERS: NONE

WARNINGS: NONE

REVIEWED:
- Independent reviewer session: this session authored none of the reviewed production, test, fixture or harness bytes. The only repository write is this new report.
- Baseline: HEAD `ab9bac8ea13be3ef325750cfc0b00930f5906539`. This is correction re-entry after maintainability-01.md and discovery-01.md's F-01. F-01 is a functional discovery identity, not a maintainability blocker; its functional disposition remains for fresh discovery and separate acceptance.
- Changed implementation scope for re-entry: scripts/maintainability.py and tests/test_maintainability.py. Compared both against the pre-correction snapshot; both snapshot hashes equal maintainability-01.md's reviewed identities. The complete correction is validate_policy(), its call inside settings(), and test_invalid_policy_settings_fail_before_measurement().
- Unaffected scope: launcher, environment helper, shipped defaults/pins, installer and installer tests, README, skill guide, measurement guide and project map match the prior report hashes exactly. Their prior maintainability evidence remains applicable. docs/development.md has subsequent registry documentation changes; inspected as policy/context. Contract records and other task packages are separate worktree context, not implementation attributed to this correction.
- Architecture command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — exit 0; 4 tests; no skips.
- Additional verification: `python3 tools/check_contracts.py --root .` — exit 0; 6 subsystems, 7 indexed plan refs. This is structural verification only. Behavioral suites were reviewed, not rerun; producer results are not independent behavioral acceptance.
- Policy/boundary sources: AGENTS.md; docs/project-map.md; docs/development.md; tests/test_architecture.py; docs/contracts/index.json; docs/contracts/measurement.json; docs/tasks/T-001.1/brief.md, implementation.md, reviews/maintainability-01.md and reviews/discovery-01.md; project-local task-maintainability-review and testing-discipline skills. No separate machine gate registry was found in the applicable paths.

Semantic review:
- Traced settings resolution through validation, default-check selection, build_report, discovery, analyzer dispatch and error translation. Both target and shipped policy enter the same validation owner before their fields affect scanning. The validator is deterministic, has no I/O or mutation, and keeps field-specific diagnostics; settings adds the effective path and preserves the cause. Existing repeated parsing/check selection predates this correction and is not a new material design regression.
- Reviewed the installed CLI regression and its existing fixture collaborators. The test reuses installed_launcher(), launch() and snapshot_tree(); the invalid-source sentinel establishes the exclusion control. Each table row reconstructs policy from the same original defaults, so rows do not inherit previous policy mutations. Field/value subtests and path/field diagnostics identify failures. Complete disposable-tree snapshots express the preservation contract. Test text replacement is bounded to the shipped flat TOML fixture and does not introduce a second production policy authority or harness abstraction.
- No introduced or materially worsened cohesion, coupling, hidden-state, change-locality, testability, diagnostic or abstraction-cost blocker was confirmed. This verdict does not establish functional conformance or close F-01.

First outstanding stage and complete ordered remainder:
1. task-contract-registry-updater: reconcile current correction and discovery references with the existing measurement/installation records. Initial registry materialization exists; the correction submission explicitly leaves current wording/references to this stage. No new CLI field, managed resource or dependency was added by the correction.
2. Fresh independent task-review-discovery for corrected bytes, carrying the complete existing ledger and F-01.
3. Separate task-acceptance-review decision.

No downstream stage was executed or delegated. Corrected reviewed bytes invalidate this verdict for their affected scope.

Reviewed-byte identities (SHA-256; unchanged identities carry forward prior evidence):
```text
caa1d0e31fcc04130dd55347f7dc48943a232939156d9fd631f688a0e2fd8b2b  scripts/measure_maintainability.py
54525f713a8865b1a1f26be6c966ffbc5a6c44171ae0727556dbe458c583b9eb  scripts/maintainability_env.py
ef736038b84c35f258f8a1284d1fd9d700de8e2963a0549bd877f8a319b95997  scripts/maintainability.py
f258d0e5a0dc070fc9ec33aa0dc000b1959fba9eebdd5cc20e1cb00178a654fb  scripts/maintainability-default.toml
a95813db8c5666acfbeae7e1734e7f1a16ad674d1798cc710853e0d3bbb2754b  scripts/maintainability-ruff-default.toml
79dbf22b5bc1bc8c10f5746610e937d4f592ebfb3bfc6123d1428cae5e344d44  scripts/maintainability-requirements.txt
a614b7bc21a84f27df588ec150e1c5ccfadd229b562aa3bd967e1e9026a159da  scripts/install_development_skills.py
f37e329e8a5930f015cc25512e01efc7e140817f9b7d270479c1cb53bfdbd5de  tests/test_maintainability.py
a73ea29dbbe97e8070c56247b7e36e2a1147f31e8e12c1a13c688b48aa454f55  tests/test_install_development_skills.py
0c559568b1ec9cf336961222c0855b9b19ce10ddceefb89fac226524b39981de  README.md
bc8930ae9b081c4bf7f030003ebbc7fbe71ae41e54cc27ddce69aa21548eee8d  skills/README.md
5dae8e41784b2157fbf91f89d317c5c5ddeb0c432f78551529aadad3d1d38789  scripts/measure-maintainability.md
e68fb53a19376c37820c1781b474c4972a8b7020b0238d102923ceebd44f4648  docs/project-map.md
246a3e85d87b1fcc2f2f3ff270128d4f0bc1d6940de5dea575e3e3da9827702e  docs/development.md
```

Exact Git status before report creation (`git status --porcelain=v1 --untracked-files=all`):
```text
 M README.md
 M docs/contracts/index.json
 M docs/contracts/installation.json
 M docs/development.md
 M docs/project-map.md
 M scripts/install_development_skills.py
 M scripts/measure-maintainability.md
 M scripts/measure_maintainability.py
 M skills/README.md
 M tests/test_install_development_skills.py
 M tests/test_maintainability.py
 D tools/maintainability.py
 D tools/maintainability_env.py
?? docs/contracts/measurement.json
?? docs/tasks/T-001.1/brief.md
?? docs/tasks/T-001.1/implementation.md
?? docs/tasks/T-001.1/preflight.md
?? docs/tasks/T-001.1/reviews/discovery-01.md
?? docs/tasks/T-001.1/reviews/maintainability-01.md
?? docs/tasks/T-001.1/verification.md
?? docs/tasks/T-001.2/brief.md
?? docs/tasks/T-001.3/brief.md
?? docs/tasks/T-001/brief.md
?? docs/tasks/index.json
?? scripts/maintainability-default.toml
?? scripts/maintainability-requirements.txt
?? scripts/maintainability-ruff-default.toml
?? scripts/maintainability.py
?? scripts/maintainability_env.py
```

Exact Git status after report creation (same command; verified against this recorded value):
```text
 M README.md
 M docs/contracts/index.json
 M docs/contracts/installation.json
 M docs/development.md
 M docs/project-map.md
 M scripts/install_development_skills.py
 M scripts/measure-maintainability.md
 M scripts/measure_maintainability.py
 M skills/README.md
 M tests/test_install_development_skills.py
 M tests/test_maintainability.py
 D tools/maintainability.py
 D tools/maintainability_env.py
?? docs/contracts/measurement.json
?? docs/tasks/T-001.1/brief.md
?? docs/tasks/T-001.1/implementation.md
?? docs/tasks/T-001.1/preflight.md
?? docs/tasks/T-001.1/reviews/discovery-01.md
?? docs/tasks/T-001.1/reviews/maintainability-01.md
?? docs/tasks/T-001.1/reviews/maintainability-02.md
?? docs/tasks/T-001.1/verification.md
?? docs/tasks/T-001.2/brief.md
?? docs/tasks/T-001.3/brief.md
?? docs/tasks/T-001/brief.md
?? docs/tasks/index.json
?? scripts/maintainability-default.toml
?? scripts/maintainability-requirements.txt
?? scripts/maintainability-ruff-default.toml
?? scripts/maintainability.py
?? scripts/maintainability_env.py
```

Only the new report entry was added. This report does not review itself.
