# SIDE-003 results

Source instruction costs fell. All 26 descriptions total **14,448 → 9,119 characters** (−5,329; 36.9%); the unchanged 20-skill profile totals **10,809 → 6,920** (−3,889; 36.0%). Five packages have useful conditional extraction. Other assessed packages retain their existing layout. Local source and disposable distribution checks pass within the limits below. Live routing, model compliance and session/billing savings remain **pending**.

The owner replaced formal workflow chains with direct implementation and independent native review. Earlier leaf completions and the .7 closing correction are recorded in [rollout results](rollout-results.md). Independent native GPT-6.1 Sol / medium closing review completed with APPROVE and no findings; it independently checked accounting, composed routes, disposable resolution and sentinels, drift classification and raw test evidence. The pilot experiment framing and rollback machinery were discarded; Git history is the revert path. This closing validation made no provider calls and did no dependency provisioning, active installation refresh or installer/profile changes. Earlier authorized Ollama independent reviews in .8/.9 remain recorded in rollout results; no live behavioral, routing or session eval qualification is claimed.

## Source accounting

Counts use normalized description characters and UTF-8 file/body bytes from the [frozen baseline](baseline.md), recomputed with `python3 tools/baseline_measure.py` into temporary output. These are source descriptions, not a measurement of the host-rendered catalog, token use, observed reads or bills. Bodies start immediately after frontmatter. Extracted reference bytes are excluded from the entry totals and charged when applicable in route accounting.

| Scope | Description characters | Entry file bytes | Entry body bytes |
|---|---:|---:|---:|
| All 26 | 14,448 → 9,119 | 404,992 → 369,732 | 388,640 → 358,767 |
| Profile 20 | 10,809 → 6,920 | 332,433 → 315,322 | 320,123 → 306,934 |

Descriptions were compressed in .2–.6; `task-contract-registry-updater` was already compact and stays unchanged. Description histories and preserved trigger boundaries are in [description results](description-results.md). Entry file changes below combine description and body changes; no-op means no body restructuring in the named leaf.

| Skill | Description characters before → after | Entry bytes before → after | Body decision |
|---|---:|---:|---|
| ai-flow-foundation | 580 → 300 | 8,634 → 8,351 | Description only; body unchanged |
| architecture-guardrails | 533 → 341 | 17,306 → 17,113 | No-op (.16) |
| ask-user-questions | 720 → 351 | 5,345 → 4,956 | Description only; body unchanged |
| foundation-readiness-review | 445 → 291 | 9,196 → 9,041 | No-op (.16) |
| idea-brief | 620 → 393 | 8,097 → 7,870 | No-op (.17) |
| idea-challenger | 797 → 448 | 6,735 → 6,381 | Description only; body unchanged |
| idea-investigator | 548 → 324 | 10,937 → 10,713 | Description only; body unchanged |
| ollama-delegate | 339 → 260 | 6,124 → 6,045 | Description only; body unchanged |
| project-bootstrap | 659 → 311 | 11,663 → 11,308 | Description only; body unchanged |
| project-delivery-plan | 687 → 302 | 17,935 → 17,550 | No-op (.15) |
| project-direction | 573 → 392 | 7,936 → 7,749 | No-op (.16) |
| project-plan-verification | 649 → 307 | 14,058 → 13,716 | No-op (.16) |
| repo-foundation | 563 → 300 | 22,269 → 20,634 | Move registry mechanics to existing reference (.14) |
| senior-code-review | 638 → 426 | 9,387 → 9,175 | No-op (.17) |
| session-handoff | 515 → 271 | 8,307 → 8,063 | Description only; body unchanged |
| skill-creator | 319 → 203 | 34,440 → 17,640 | Extract behavioral eval, optimization and platform routes (.13) |
| bounded-task-implementer | 515 → 365 | 41,936 → 33,861 | Extract evidence, strict and correction routes (.7) |
| task-acceptance-review | 599 → 483 | 32,281 → 32,165 | Withdraw .8 candidate; no-op |
| task-brief-designer | 571 → 331 | 26,051 → 23,559 | Extract decomposition, exceptional output and strict fields (.9) |
| task-contract-registry-updater | 279 → 279 | 6,998 → 6,998 | Description only; body unchanged |
| task-maintainability-review | 640 → 413 | 21,497 → 21,254 | No-op (.11) |
| task-preflight | 453 → 326 | 22,142 → 20,374 | Extract strict procedure/template fields (.10) |
| task-review-discovery | 494 → 374 | 16,195 → 16,077 | No-op (.17) |
| task-verification-designer | 487 → 366 | 15,620 → 15,499 | No-op (.17) |
| task-orchestrator | 635 → 480 | 7,005 → 6,850 | No-op (.17) |
| testing-discipline | 590 → 482 | 16,898 → 16,790 | No-op (.12) |

## Cumulative route accounting

The following are unique-file static estimates, not traces. They include the baseline route’s repository instructions, applicable references/templates, and invoked sibling entries. **Controlled** holds unrelated frozen file weights fixed and applies only the owning extraction. **Invocation** uses the leaf’s actual pre-edit dependency weights on both sides. Thus sibling/description savings are not credited again to the extraction. These overlapping scenarios must not be summed into a session-saving claim. The recorded leaf before/after figures are preserved rather than relabeled as a fresh observed session.

| Route | Frozen → controlled after | Leaf invocation before → after | Final composed bytes |
|---|---:|---:|---:|
| implementer-direct-guided | 75,212 → 68,720 | 74,956 → 68,612 | 68,612 |
| implementer-packaged-guided | 83,469 → 76,977 | 83,213 → 76,869 | 74,253 |
| implementer-high-assurance | 83,469 → 80,850 | 83,213 → 80,742 | 78,126 |
| implementer-correction | 83,469 → 82,450 | 83,213 → 82,342 | 79,726 |
| implementer-evidence-available | 75,212 → 68,720 | 74,956 → 68,612 | 68,612 |
| implementer-evidence-unavailable | 75,212 → 67,137 | 74,956 → 67,029 | 67,029 |
| acceptance-guided | 48,659 → 48,659 | 48,543 → 48,543 | 48,543 |
| acceptance-high-assurance | 63,721 → 63,721 | 63,605 → 63,605 | 63,605 |
| acceptance-tests-only-reproducer | 51,591 → 51,591 | 51,475 → 51,475 | 51,475 |
| brief-ordinary | 57,560 → 51,686 | 57,320 → 51,446 | 51,446 |
| brief-immediate-review | 71,716 → 65,842 | 71,476 → 65,602 | 65,602 |
| brief-high-assurance | 57,560 → 53,289 | 57,320 → 53,049 | 53,049 |
| preflight-ordinary | 46,777 → 42,520 | 46,650 → 42,393 | 42,393 |
| preflight-high-assurance | 46,777 → 48,489 | 46,650 → 48,362 | 48,362 |
| maintainability-ordinary | 37,875 → 37,875 | 37,632 → 37,632 | 37,632 |
| maintainability-test-assets | 67,983 → 67,983 | 67,632 → 67,632 | 67,632 |
| testing-ordinary | 33,276 → 33,276 | 33,168 → 33,168 | 33,168 |
| testing-specialized-strategy | 46,486 → 46,486 | 46,378 → 46,378 | 46,378 |
| creator-ordinary | 50,818 → 34,134 | 50,702 → 34,018 | 34,018 |
| creator-eval-schemas | 63,814 → 56,819 | 63,698 → 56,703 | 56,703 |
| creator-grade-analyze | 83,239 → 76,244 | 83,123 → 76,128 | 76,128 |
| creator-blind-comparison | 68,481 → 51,797 | 68,365 → 51,681 | 51,681 |
| creator-description-optimization | 57,876 → 46,602 | 57,760 → 46,486 | 46,486 |
| repo-ordinary | 38,647 → 37,278 | 38,381 → 37,012 | 37,012 |
| repo-contract-registry | 46,313 → 46,999 | 46,047 → 46,733 | 46,733 |
| repo-python-guardrails | 65,952 → 64,583 | 65,493 → 64,124 | 64,124 |
| delivery-ordinary | 43,354 → 43,354 | 42,969 → 42,969 | 42,969 |
| delivery-model-dependent | 43,354 → 43,354 | 42,969 → 42,969 | 42,969 |
| guardrails-ordinary | 40,103 → 40,103 | 39,910 → 39,910 | 39,910 |
| guardrails-python | 43,683 → 43,683 | 43,490 → 43,490 | 43,490 |
| guardrails-javascript-typescript | 45,623 → 45,623 | 45,430 → 45,430 | 45,430 |
| guardrails-java | 42,911 → 42,911 | 42,718 → 42,718 | 42,718 |
| guardrails-dotnet | 42,787 → 42,787 | 42,594 → 42,594 | 42,594 |
| guardrails-command-registry | 45,134 → 45,134 | 44,941 → 44,941 | 44,941 |
| readiness-ordinary | 32,367 → 32,367 | 32,212 → 32,212 | 32,212 |
| readiness-model-product | 32,367 → 32,367 | 32,212 → 32,212 | 32,212 |
| direction-ordinary | 28,079 → 28,079 | 27,892 → 27,892 | 27,892 |
| direction-delta | 28,079 → 28,079 | 27,892 → 27,892 | 27,892 |
| plan-review-ordinary | 32,785 → 32,785 | 32,443 → 32,443 | 32,443 |
| plan-review-model-product | 32,785 → 32,785 | 32,443 → 32,443 | 32,443 |
| idea-ordinary | 27,787 → 27,787 | 27,560 → 27,560 | 27,560 |
| idea-custom-format | 27,787 → 27,787 | 27,560 → 27,560 | 27,560 |
| senior-review-ordinary | 32,164 → 32,164 | 31,952 → 31,952 | 31,952 |
| senior-review-security | 32,164 → 32,164 | 31,952 → 31,952 | 31,952 |
| discovery-ordinary | 32,573 → 32,573 | 32,455 → 32,455 | 32,455 |
| discovery-durable | 42,580 → 42,580 | 42,462 → 42,462 | 42,462 |
| verification-ordinary | 37,386 → 37,386 | 37,265 → 37,265 | 37,265 |
| verification-lifecycle | 37,386 → 37,386 | 37,265 → 37,265 | 37,265 |
| orchestrator-ordinary | 28,644 → 28,644 | 28,489 → 28,489 | 28,489 |
| orchestrator-modify | 30,079 → 30,079 | 29,924 → 29,924 | 29,924 |
| orchestrator-plan-future | 104,289 → 104,289 | 104,134 → 104,134 | 104,134 |
| orchestrator-prepare-inputs | 37,605 → 37,605 | 37,450 → 37,450 | 37,450 |

Final composed bytes use the current source snapshot with each route’s explicit unique file list and applicable new references (`final-routes.json`; `final_routes.py`). For example, implementer packaged guidance now costs 74,253 bytes, strict input 78,126 and correction 79,726: each includes the shorter current preflight template. The template forwards to preflight strict fields **before assembling a packet**; these implementer scenarios consume an already-ready packet, so they do not load that producer-only reference. A scenario also producing strict readiness must add it. Reference links are conditional instructions, not recursive startup loading. Other final differences include description compression; they are not credited to body extraction twice.

Additional measured branches from the leaves:

| Branch | Frozen → controlled after | Invocation before → after |
|---|---:|---:|
| Brief decomposition | 57,560 → 56,471 | 57,320 → 56,231 |
| Strict brief decomposition | 57,560 → 58,074 | 57,320 → 57,834 |
| Early direction/blocked brief | Not in frozen route set | 42,189 → 41,996 |
| Implementer strict correction with evidence, all three references | 83,469 → 86,323 | 83,213 → 86,215 |
| Creator ordinary on Claude.ai/Cowork | Not in frozen route set | 50,702 → 38,606 |
| Creator entry plus all three extracted procedures | Entry/reference closure only | 34,324 → 37,327 |

Useful ordinary invocation reductions are implementer 6,344 bytes with evidence (7,927 without), brief designer 5,874, packaged preflight 4,257, creator 16,684 and repo foundation 1,369. Direct inline preflight omits its template: 38,393 → 36,752. These are route-specific gains, not additive global savings.

Growth remains visible: strict preflight +1,712, strict brief decomposition +514, repo registry +686, implementer combined branch +3,002 and creator all-procedure closure +3,003 bytes. Required content plus navigation costs remain on these branches. Implementer available-evidence body closure falls 41,369 → 35,025 (15.3%; 19.2% without evidence), missing the earlier 40–60% default target. Acceptance’s rejected .8 layout grew applicable context and was withdrawn; its candidate costs are not promoted as final results.

No-op decisions preserve useful always-needed instructions and existing conditional resources. In particular, .11/.12/.15/.16/.17 did not add loading/stop scaffolding merely to satisfy superseded wording. Their unchanged timing and missing/unreadable-reference qualifications remain recorded in rollout results; this closing check proves readable paths, not that uniform explicit stop wording or agent compliance was added.

## Local verification and distribution

Raw artifacts are under `/tmp/side003-sequential/18/`: the task-start `baseline/`, `manifest.json`, original index/status/diff captures, command logs, `validate_distribution.py`, `reference-resolution.json`, `enrich_evidence.py`, `authority-closure.json`, `active-drift.json` and `cost-summary.json`. Existing .1–.17 records were read without replacement. The .18 snapshot predates the authorized .7 correction to `tests/test_run_evidence.py` and its rollout note; that separate correction is retained at `/tmp/side003-sequential/7-closing/`. This leaf writes only this results file.

| Check | Observed result |
|---|---|
| Focused installer first: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` | 36 tests PASS; no skips (`installer-suite.log`). |
| Real canonical install, then `--check /tmp/side003-sequential/18/disposable` | PASS in a disposable Git repo; profile remains 20. Whole-package equality: 211 files across profile 20 plus three full nonprofile copies (skill-creator, idea-brief, task-orchestrator). |
| `python3 /tmp/side003-sequential/18/validate_distribution.py` | PASS: 49 recorded resources with explicit route/base inventory; 135 nested Markdown edges; 93 files actually read, including cross-package paths and anchor checks. Entry-relative code paths and document-relative links use their stated bases. |
| Ownership sentinels | Unmanaged skill entry, extra skill file, script and AGENTS prefix all survive with exact bytes. A first malformed scratch sentinel lacked frontmatter and was rejected; it was corrected before successful installation. |
| Controlled faults, same resolver | Renamed required `run-evidence.md` in disposable target fails resolution; restored afterward. Invalid preflight handoff anchor also fails. Required real handoff, orchestrator and installed guide anchors resolve. Placeholder artifact links are bound explicitly to the installed guide, not treated as source paths. |
| `python3 tools/verify.py` | Initial 7 checks: three suite constituents PASS (3, 13, 4 tests); orchestrator fails under host sandbox (3 failures/13 errors); root fails on one moved-entry assertion (309 tests, 31 skips); registry PASS; active drift reported separately below. Raw failures retained in `aggregate.log`. |
| Affected root constituent rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v` | After owning .7 correction: 309 tests OK, 31 skips (`root-corrected.log`). The correction preserves all seven assertions and follows the required linked evidence closure; independent native review approved. |
| Failed orchestrator constituent rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py' -v` | Approved host escalation: 207 tests PASS, no skips (`orchestrator-escalated.log`). Supported-host sandbox denial was a failure, not drift or a skip. |
| Architecture: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Latest exact canonical run: 4 PASS (`7-closing/architecture.log`); source policy unchanged afterward. |
| `python3 tools/check_contracts.py --root .` | PASS: 7 subsystems / 22 indexed plan refs (aggregate and latest `7-closing/contracts.log`). Actual measurement authorities resolve: .7 measurement/native duties remain inline, .10 strict packet authority is declared, .14/.16 native authorities remain inline. No further registry/index write needed. |

Across the five current suite constituents, **536 tests ran with 31 skips**; all executed tests pass after the correction and host escalation. Successful unaffected constituents were reused. The skips are 30 cases requiring real pinned Radon/Ruff and one requiring real pinned dependencies; those analyzer integrations remain unqualified. No tools were provisioned to remove skips. Syntax/reference/contract checks establish structure and distribution, not behavioral equivalence of model-driven workflows.

## Deliberately stale active installation

The aggregate’s exact read-only `python3 scripts/install_development_skills.py --check .` compared 106 managed paths and returned exit 1: **39 differences, 28 changed and 11 missing**. Every changed installed file byte-matches an earlier source commit; `active-drift.json` records source/installed hashes, byte counts, historical matches and every exact path. This is observed managed drift in the deliberately unrefreshed installation. The fresh disposable `--check` passes; no refresh was used to hide drift.

SIDE-003-related differences include the compressed entry descriptions; implementer’s three extracted references; brief-designer decomposition, exceptional-output and strict resources plus changed template/test; preflight strict resource and changed template; repo-foundation’s registry reference. Other observed stale inputs precede this work: `.agents/scripts/ollama-models.json`, implementer measurement eval README/JSON/setup/helpers and preflight eval JSON/setup. Their historical match demonstrates stale content, not that SIDE-003 changed them. In particular, the user’s model alias/config settings were not edited here.

The exact 11 missing paths, relative to `.agents/skills/`, are:

- `task-implementation-flow/bounded-task-implementer/evals/README.md`, `evals/files/check_measurement_fixture.py`, `evals/files/measurement_cases.json`, `evals/files/measurement_fixture.py` (the latter three under the same implementer package).
- `task-implementation-flow/bounded-task-implementer/references/{correction-protocol,high-assurance,run-evidence}.md`.
- `task-implementation-flow/task-brief-designer/references/{decomposition,exceptional-output,high-assurance}.md`.
- `task-implementation-flow/task-preflight/references/high-assurance.md`.

Changed paths are the 19 profile entries other than task-contract-registry-updater, plus `.agents/scripts/ollama-models.json`; repo-foundation registry reference; implementer eval JSON/setup; brief-designer template/package test; preflight eval JSON/setup/template. The exact inventory and hashes remain in the temporary JSON. No unrelated source/suite failure is classified as drift.

## Qualification still owed

Catalog-only implicit, explicit, negative and nearest-neighbor routing evals; traced model workflow/critical-gate cases; paired fresh-session reads and usage with repetitions; tokenizer/rendered-host catalog accounting; and billing/session savings remain pending separately approved live budget. Local passing fixtures and reference walks do not qualify those outcomes. No pilot benchmark apparatus or rollback system was built. Closing review is complete. No findings remain in the authorized local scope; the qualification limits above remain.
