# Task Preflight: `SYN-01` — Add prefix selection to `catalog.select_names`

Status: `ready`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Task / authority | `docs/tasks/SYN-01/brief.md` is `ready_for_preflight`; `authority.md#Approved synthetic task SYN-01` defines the signature, behavior, scope, and required stage order. |
| Repository | `/private/tmp/task-flow-spike-2026-10-08` |
| Dependencies / entry criteria | `dependencies.json` maps `SYN-01` to `[]`; no upstream dependency or installation is required. |
| Allowed scope | Implementation may change only `catalog.py` and `tests/test_catalog.py`. This preflight writes only this authorized packet. Registry and README paths remain updater-owned. |
| User-work ownership | Clean pre-write worktree. No user-owned dirty path overlaps the implementation scope. |
| Permission limits | Network, dependency installation, destructive actions, and actor commits are prohibited. Cheap local checks are authorized. The registry write command is updater-owned and was not run. |
| Profile | `high-assurance` |

## Acceptance evidence and commands

| AC / risk | Observable oracle and boundary | Exact command | Baseline result / gap |
|---|---|---|---|
| AC-01 / V-01 | Public `catalog.select_names(names, prefix)` equals the exact ordered list of case-sensitive prefix matches, retaining matching duplicates and excluding case-only/non-prefix values. | `cd /private/tmp/task-flow-spike-2026-10-08 && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_catalog -v` | Baseline passed 1 existing test. The focused nonempty-prefix oracle is absent and must be added fail-first before implementation. |
| AC-02 / V-02 | Public calls with omitted and explicit empty prefix each equal all input values; caller list remains unchanged. | `cd /private/tmp/task-flow-spike-2026-10-08 && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_catalog -v` | Baseline passed; existing test partially proves omitted-default and non-mutation only. Explicit empty-prefix coverage is required. |
| AC-03 / V-03 | Public calls for empty input and no-match prefix each equal `[]`. | `cd /private/tmp/task-flow-spike-2026-10-08 && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_catalog -v` | Baseline passed; both boundary oracles are absent and must be added. |
| Owning suite | Repository test discovery passes after targeted tests pass. | `cd /private/tmp/task-flow-spike-2026-10-08 && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | Passed: 1 test, exit 0. |
| Structural scope gate | `catalog.py` contains no imports. This is structural only, not API behavior proof. | `cd /private/tmp/task-flow-spike-2026-10-08 && PYTHONDONTWRITEBYTECODE=1 python3 tools/check_architecture.py` | Passed: `Architecture gate passed`, exit 0. |

## Warnings, blockers, and next action

| Condition | Effect | Owner | Smallest next action |
|---|---|---|---|
| Focused regression coverage does not yet exist for V-01 through V-03. | Warning only; this is the intended implementation delta, not a preflight blocker. | Implementer | Add the finite public-API tests, observe the nonempty-prefix assertion fail against the old signature/behavior, then implement the smallest change. |
| `docs/contracts/catalog.json`, `docs/contracts/index.json`, and `README.md` will become stale after the public API delta. | Warning only; implementer must not edit these updater-owned paths. | Registry updater | Synchronize them after independent maintainability review, then run the two registry commands. |

Implementation stops: stop and return to fresh preflight if any recorded input identity changes other than this packet, scope expands beyond `catalog.py` and `tests/test_catalog.py`, a required command no longer runs, or an unexplained dirty overlap appears. Do not edit registry or README files, use network/install dependencies, commit, or start downstream stages.

Next exact action: the separate verification-design stage has already produced `docs/tasks/SYN-01/verification.md`; hand off to implementation limited to `catalog.py` and `tests/test_catalog.py` under this packet.

---

## High-assurance packet addendum

### Artifact identity and inputs

| Field | Value |
|---|---|
| Task ID | `SYN-01` |
| Producing stage | `task-preflight` |
| Created at | `2026-10-08T18:12:31+01:00` |
| Durable packet path | `docs/tasks/SYN-01/preflight.md` |
| Task brief | `docs/tasks/SYN-01/brief.md`; SHA-256 `83cd92efeb30639a5475430aba4477150a84b133b98525752b6df488a3ffeee9` |
| Verification design | `docs/tasks/SYN-01/verification.md`; source declaration resolves to `docs/tasks/SYN-01/brief.md`; SHA-256 `e8f4727604fded0551956f4cae661cd9d1d36ae3b9ff595aadbda2672d0caa1a` |
| Primary authority | `authority.md#Approved synthetic task SYN-01`; SHA-256 `4fc7349de4fdcd14ca1b2795307f0bbea1e7620884e5ef988e331417a62c5df3` |
| Dependency source | `dependencies.json`; SHA-256 `e51cca7a311dfb4b19dfbb483d04f09e19529d180ee7aec53427185e1c4818d8`; `SYN-01: []` |
| Instructions | `AGENTS.md`; SHA-256 `57fd2c7dd428e2ba3672d1dee9a9726f933cd51b1a5f66da290f6eb90ff654b9` |
| Run policy | `run-policy.json` (`synthetic-flow-spike-v1`); SHA-256 `82ad4578dce7ca9468a90276a1e29100417fb559c5d6eb38333c937d049baa20` |
| Environment fingerprints | `python3 --version`: `Python 3.14.6`; `catalog.py` SHA-256 `52051cde0f03ca5ba49ef3782a36cdce578328536e4f4dcbff630d52cda10a73`; `tests/test_catalog.py` SHA-256 `0325d1231ad4f23f63fc385bbc3351bf2e82e080f6947189a08fbbb0b319f400`; architecture tool SHA-256 `cd468098acf799dbca5be2724a3924e25725ec77f5d2441ba1f05ff5a198250d`; registry tool SHA-256 `00f38e439f5347804a1c78646ecf9bf8b9fba805cfbb88075226b447d987b928` |

### Repository baseline and dirty ownership

| Field | Value |
|---|---|
| `HEAD` | `8805b776d7da0a92f6206f5c2c33003b0888a7cf` |
| Pre-write `git status --short` | `clean` |
| Post-write `git status --short` | `?? docs/tasks/SYN-01/preflight.md` |
| Packet artifact delta | New `docs/tasks/SYN-01/preflight.md`. |
| Final non-packet baseline recapture | Unchanged: all recorded non-packet source, test, registry, README, tool, authority, dependency, instruction, policy, brief, and verification-design SHA-256 identities match the pre-write capture. |
| Incidental artifacts | None observed. `PYTHONDONTWRITEBYTECODE=1` prevented bytecode output; checks did not create files. |

No pre-existing dirty paths existed, so no index/worktree dirty-path identity rows apply.

### Exact command records

| ID | Class / cost | Exact command | Working directory / environment | Purpose / ACs | Expected signal | Run? / result | Authorization |
|---|---|---|---|---|---|---|---|
| CMD-01 | targeted; cheap/local | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_catalog -v` | `/private/tmp/task-flow-spike-2026-10-08`; `PYTHONDONTWRITEBYTECODE=1` | V-01, V-02, V-03 / AC-01, AC-02, AC-03 | Focused public-API assertions pass; prior to implementation, only the legacy default test passes. | Yes; exit 0, 1 legacy test passed. | Authorized cheap local check. |
| CMD-02 | owning suite; cheap/local | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | `/private/tmp/task-flow-spike-2026-10-08`; `PYTHONDONTWRITEBYTECODE=1` | Verify the owning test suite after CMD-01. | All discovered tests pass. | Yes; exit 0, 1 test passed. | Authorized cheap local check. |
| CMD-03 | structural; cheap/local | `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_architecture.py` | `/private/tmp/task-flow-spike-2026-10-08`; `PYTHONDONTWRITEBYTECODE=1` | Enforce the dependency-free `catalog.py` architecture condition. | `Architecture gate passed`. | Yes; exit 0. | Authorized cheap local check. |
| CMD-04 | registry validation; cheap/local | `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_contracts.py --root .` | `/private/tmp/task-flow-spike-2026-10-08`; `PYTHONDONTWRITEBYTECODE=1` | Confirm current registry-validator capability; structural only. | `contract registry OK`. | Yes; exit 0, 1 subsystem and 0 plan refs. | Authorized cheap local check. |
| CMD-05 | registry update plus validation; cheap/local but writes | `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_contracts.py --root . --write-index` | `/private/tmp/task-flow-spike-2026-10-08`; `PYTHONDONTWRITEBYTECODE=1` | Later updater deterministically refreshes `docs/contracts/index.json`. | Exit 0 after writing canonical index. | Not run: updater-owned write command, outside preflight permission envelope. Syntax/interface inspected in `tools/check_contracts.py`. | Reserved for registry updater by authority and policy. |

### Helper and capability inventory

| Capability | Exact path / interface | Existence evidence | Authorized and usable? | Disposition |
|---|---|---|---|---|
| Public API boundary | `catalog.select_names` in `catalog.py` | Current declaration exists as `select_names(names)` and returns `list(names)`. | Yes | Implementer changes it only within approved scope. |
| Focused unittest runner | `python3 -m unittest tests.test_catalog -v` | CMD-01 executed successfully on Python 3.14.6. | Yes | Add V-01 through V-03 to `tests/test_catalog.py`. |
| Owning test discovery | `python3 -m unittest discover -s tests -v` | CMD-02 executed successfully. | Yes | Run after targeted tests pass. |
| Architecture validator | `tools/check_architecture.py` | Exists; CMD-03 passed. | Yes | Structural regression gate only. |
| Contract registry validator | `tools/check_contracts.py` | Exists; CMD-04 passed; source exposes `--write-index`. | Read-only validation: yes. Write-index: later updater only. | Do not treat as behavior proof. |
| Contract/README legacy-assumption target | `docs/contracts/catalog.json`, `docs/contracts/index.json`, `README.md` | Current declarations document the old one-argument/all-names API. | Read-only for implementation; update is authorized only to registry updater. | Preserve for later registry synchronization. |

### Implementer contract

Before the first edit, the implementer must recalculate the recorded brief, verification-design, Git, dirty-path, dependency, instruction, policy, and environment identities. It must also match the recorded post-write status and confirm that the packet artifact is the only delta from the pre-write baseline.

It may change only `catalog.py` and `tests/test_catalog.py`, must preserve pre-existing work, run CMD-01 before and after the minimal implementation change, then CMD-02 and CMD-03 progressively, and produce the supplied structured result. Any unexplained freshness mismatch routes to fresh preflight.
