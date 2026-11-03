# SIDE-003 loading-cost baseline

Baseline recorded from HEAD `2007ca53ef92e94b76719f70ebe6e87c6baa9b6b` and the current working tree. Source skill bytes match that commit. The user updated `AGENTS.md` before the resumed run; its current bytes and hash are included. Preparation artifacts and the baseline outputs do not change skill bytes.

Run from the repository root:

```sh
python3 tools/baseline_measure.py
```

This read-only command prints the complete JSON record to stdout. Its static route definitions and command-prerequisites data come from [baseline-measurements.json](baseline-measurements.json); numeric inventories, hashes, totals, route sums and graph edges are recomputed from current files. The script reads the installer constant through Python AST, without executing the installer. No installation is refreshed.

To save a refreshed record, first redirect to a separate temporary file, then replace the record after checking it. Do not redirect onto the input record. Explicit list measurement is also available:

```sh
python3 tools/baseline_measure.py --sum AGENTS.md skills/testing-discipline/SKILL.md
```

## Counting basis and limits

All counts are UTF-8 bytes or normalized description characters. No tokenizer was used; there is no token or billing estimate. Body bytes begin immediately after the closing `---`, including its following newline and whitespace. Description characters are the whitespace-normalized scalar only; the current plain, folded `>` and folded `>-` forms are supported.

Routes are **static unique-file estimates**, not observed execution traces. Each explicit scenario lists entry files, applicable references/templates, invoked sibling skill entries and their applicable references, package instruction documents, and repository instructions. Every route includes `AGENTS.md`, `docs/project-map.md` and `docs/development.md` because the repository instructions require those reads. Task-specific project authorities, task briefs, verification/preflight records, runtime scripts, command output and model output are outside this source-instruction estimate. They must be measured in a future observed session, together with repeated reads.

Rendered catalog visibility, host wrapping/truncation/omission and session usage are unobservable from this repo-only command. Source presence does not establish installation or activation.

## Source inventory and plan comparison

All 26 rows agree exactly with the plan table measured at `aa94e28eaf170b68b30300b3f7cb183943698076`. There are no per-file or total deltas. The recording commit differs; source skill bytes and counting results remain unchanged. Per-file SHA-256 values and profile membership are in the machine record.

| Scope | Skills | File bytes | Body bytes | Description characters |
|---|---:|---:|---:|---:|
| All source | 26 | 404,992 | 388,640 | 14,448 |
| Development profile | 20 | 332,433 | 320,123 | 10,809 |

| Skill | Profile | File bytes | Body bytes | Description characters |
|---|---|---:|---:|---:|
| ai-flow-foundation | yes | 8,634 | 7,994 | 580 |
| architecture-guardrails | yes | 17,306 | 16,708 | 533 |
| ask-user-questions | no | 5,345 | 4,559 | 720 |
| foundation-readiness-review | yes | 9,196 | 8,684 | 445 |
| idea-brief | no | 8,097 | 7,439 | 620 |
| idea-challenger | no | 6,735 | 5,890 | 797 |
| idea-investigator | no | 10,937 | 10,344 | 548 |
| ollama-delegate | yes | 6,124 | 5,610 | 339 |
| project-bootstrap | yes | 11,663 | 10,941 | 659 |
| project-delivery-plan | yes | 17,935 | 17,199 | 687 |
| project-direction | yes | 7,936 | 7,299 | 573 |
| project-plan-verification | yes | 14,058 | 13,356 | 649 |
| repo-foundation | yes | 22,269 | 21,649 | 563 |
| senior-code-review | yes | 9,387 | 8,584 | 638 |
| session-handoff | yes | 8,307 | 7,578 | 515 |
| skill-creator | no | 34,440 | 34,080 | 319 |
| bounded-task-implementer | yes | 41,936 | 41,369 | 515 |
| task-acceptance-review | yes | 32,281 | 31,632 | 599 |
| task-brief-designer | yes | 26,051 | 25,433 | 571 |
| task-contract-registry-updater | yes | 6,998 | 6,661 | 279 |
| task-maintainability-review | yes | 21,497 | 20,786 | 640 |
| task-preflight | yes | 22,142 | 21,647 | 453 |
| task-review-discovery | yes | 16,195 | 15,652 | 494 |
| task-verification-designer | yes | 15,620 | 15,079 | 487 |
| task-orchestrator | no | 7,005 | 6,205 | 635 |
| testing-discipline | yes | 16,898 | 16,262 | 590 |

Current `AGENTS.md`: 6,452 bytes; SHA-256 `c53da175135a5e451d06c2f3406c254c1bff15efda76126a462671738b497a17`.

## File table, read graph and route inventories

The machine record is authoritative for the per-file table: **75 files**, including all 26 entries, all 28 owned `references/` files, templates, route-applicable agent instructions/assets/module docs, and repository instructions. Each row gives `path`, `file_bytes` and `sha256`.

Its `read_graph` contains **103 edges**. `package_reference` edges enumerate every package-owned reference without claiming it is always read. `literal_link` edges record resolvable Markdown destinations and inline-code paths among the inventory files, including cross-package references. Edges describe possible reads; route conditions determine loading. No runtime loader or recursive loading policy was added.

The `routes` array gives all 52 scenario IDs, conditions, authority sections, explicit unique file lists and recomputed `file_bytes` sums. It covers all named pilot route families and ordinary/conditional paths for SIDE-003.9–.17, including .10. Some conditional routes have the same cost because the current branch procedure is inline. Background or unlinked resources are not silently made mandatory. In particular, the plan-verification checklist is inventoried but its entry does not require reading it.

The pilot summaries below are cumulative instruction bytes. Entry-only costs are the corresponding rows above.

| Scenario ID | Unique files | Cumulative file bytes |
|---|---:|---:|
| implementer-direct-guided | 5 | 75,212 |
| implementer-packaged-guided | 6 | 83,469 |
| implementer-high-assurance | 6 | 83,469 |
| implementer-correction | 6 | 83,469 |
| implementer-evidence-available | 5 | 75,212 |
| implementer-evidence-unavailable | 5 | 75,212 |
| acceptance-guided | 4 | 48,659 |
| acceptance-high-assurance | 5 | 63,721 |
| acceptance-tests-only-reproducer | 5 | 51,591 |

Available/unavailable evidence routes have equal instruction cost: their helper availability changes execution, while the lifecycle procedure remains in the current entry file. Executed helper code is not charged as an instruction read. Guided acceptance uses its inline output format; the report template is loaded on the separate high-assurance route. The tests-only reproducer is loaded only on its explicitly authorized post-verdict route.

## Command prerequisites

The machine record maps **every source skill** to its focused local suites, package eval files, fixture setup scripts and live-eval invocation when applicable. It records actual `tools/verify.py` discovery roots: `tests/`, project-plan-verification tests, skill-creator tests, task-brief-designer tests and task-orchestrator tests. The first of those skill-local roots is present even though the prose development guide omits it from its current-root summary.

Local prerequisites are Python 3, Git, temporary files, local subprocesses and disposable Git repositories. Structural checks and installer checks do not qualify agent behavior. Some packages have no dedicated local suite; that gap is explicit. Optional frontmatter validation requires PyYAML. Analyzer evidence requires an already prepared pinned environment. Real containment cases require macOS and permission to run `/usr/bin/sandbox-exec`; unsupported-host skips and execution denial remain distinct.

Package eval execution needs its selected metadata/setup, supported Codex/provider configuration, separate live-execution approval and grading of actual effects. The recorded live commands are recipes, not completed eval evidence. No live behavioral qualification or aggregate gate ran for this leaf. SIDE-003.18 owns aggregate verification.

## Implementation verification

| Scenario | Evidence and result |
|---|---|
| V-01 | Two executions of `python3 tools/baseline_measure.py`, captured at `/tmp/side0031-run1.json` and `/tmp/side0031-run2.json`, are byte-identical and match the saved record (`cmp`, exit 0). |
| V-02 | All 26 file/body/description rows match the plan; totals match 404,992 / 388,640. Installer subset and plan profile membership agree. |
| V-02b | Independent raw delimiter split and folded-line join for `ask-user-questions`: 5,345 file bytes, 4,559 body bytes, 720 description characters; SHA-256 `34a5d62b9c5cd9d6b16db91dfb96f989a35688e690d1324a45db4b6d70ccc5a2`. All four equal the recorded row. |
| V-03 | Each of 52 explicit route lists passed through the real `--sum` CLI; every sorted file list and sum reproduced. Conditions were checked against the named current source sections, separately from arithmetic. |
| V-04 | Inventory covers 26 entries, the exact 20-profile subset, all 28 references, 75 instruction files, graph links, 52 routes, recording commit and 26 prerequisites entries. All named suite/eval/setup paths exist. |
| V-05 | Record explicitly labels bytes, characters and static unique-file estimates; tokenizer/rendered catalog/session telemetry remain unobserved. |
| V-06 | Each source skill SHA-256 matches `git show HEAD:<path>`; `git diff HEAD --name-only -- skills scripts tests` is empty. Only task outputs/preparation and the user-owned AGENTS update are dirty. |
| V-07 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`: 4 tests, OK, no skips. Executed once through installed run-evidence capture. |

`python3 tools/check_contracts.py --root .` passed: 7 subsystems, 22 indexed plan references. No current cross-task contract changed; no registry regeneration was needed.

Targeted raw evidence: `/tmp/side0031-targeted.log`; architecture: `/tmp/side0031-architecture.log`; contracts: `/tmp/side0031-contracts.log`. To repeat the full route-sum check:

```sh
python3 - <<'PY'
import json, subprocess
from pathlib import Path
r = json.loads(Path('docs/tasks/SIDE-003/baseline-measurements.json').read_text())
for route in r['routes']:
    got = json.loads(subprocess.check_output(['python3', 'tools/baseline_measure.py', '--sum', *route['files']]))
    assert got['file_bytes'] == route['file_bytes']
    assert got['files'] == route['files']
print('All route sums reproduce.')
PY
```

Advisory code evidence used the installed helper and existing pinned environment, without setup: original `/tmp/side0031-code-before.json` and `.txt`, then `/tmp/side0031-code-after.json` and `.txt`. The new script has two complexity signals above the provisional target 10: `read_graph` 11 and `measure` 16. Both are bounded inventory transformations: link/path filtering and explicit table assembly. Extracting one-use predicates or table comprehensions would add indirection without a new consumer or boundary; retain the short functions. Other collected argument/statement counts are within targets. New symbols have no numeric before value or delta. These are advisory observations, not behavioral or acceptance evidence.

## Submission

Implemented: `READY_FOR_REVIEW`. Preparation: [verification revision 1](../SIDE-003.1/verification.md) and [ready preflight with focused resumption refresh](../SIDE-003.1/preflight.md). No skill, shared-runtime, installer or test bytes changed. No tests or fixtures were added.

Deliverables: `tools/baseline_measure.py`, this record and `baseline-measurements.json`. Actual cross-task contract impact: none. Executable contract declarations changed: none.

Next: fresh independent `task-review-discovery` evidence, followed by a separate fresh `task-acceptance-review` decision. The architecture gate is complete; this repository does not require a separate maintainability stage for this bounded utility, and no contract-registry stage applies. No independent verdict is claimed here.
