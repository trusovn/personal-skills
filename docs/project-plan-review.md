# Project Plan Review

Verdict: `ACCEPT`
Review date/session: `2026-10-24 / fresh delegated reviewer /root/plan_review`

## Reviewed bytes

- `docs/project-plan.md` SHA-256: `9856d3ccfffcd56b4faed20dcf6ea4b49d87c4553292a5ed996cb4e784ca0df7`
- `docs/task-map.json` SHA-256: `952f094d08ad03c5f5dfe18674fdbd710e8851fc8eaff1bdddc6facec2a5c954`
- Repository revision: `c3a70dc9be38f106dc19857265300ca4d825a19a`.
- Both planning artifacts and the previous review file were untracked at entry. Other existing work included changes to the advisory proposal, delivery-plan template and source artifact checker, plus untracked experiment reports and checker tests. This review preserves that work and replaces only this report.
- Exit observation: the final status shows existing documentation staged, this report as `AM`, and the source template/checker changes absent from status. Another actor changed index/worktree state during review; this reviewer ran no staging or cleanup command. Both reviewed planning digests remained unchanged.
- Independence: this reviewer did not author the planning artifacts or implementation. The parent supplied the review request and protocol, without planner explanations or a proposed verdict.
- Active workflow: project-local `.agents/skills/project-plan-verification/SKILL.md`, its bundled checker and report template. Source skill files are development specifications, not substituted active instructions.

## Authoritative sources reviewed

- User-supplied repository instructions; `docs/project-map.md`; `docs/development.md`.
- `docs/advisory-code-maintainability-signals.md` and `docs/future-maintainability-signals-integration.md`, read as historical proposals subject to the explicit direction delta in plan section 1.
- `scripts/measure-maintainability.md`; `docs/maintainability-tool-highlights-change.md`; `docs/ruff-zero-collection-update.md`.
- `docs/contracts/index.json`, `installation.json` and `runtime-evidence.json`; the current installer and measurement launcher, adapter and environment helper; existing measurement and installer test coverage.
- Source foundation guidance in `project-bootstrap`, `repo-foundation` and `architecture-guardrails`; source task-flow README and relevant preflight, implementer, maintainability, discovery and acceptance contracts. These establish current behavior and intended edit boundaries, not availability of future behavior.

The preceding owner conversation is not separately available in this reviewer context. The plan explicitly persists its accepted policy delta; no separate upstream direction document is referenced for that delta. This review uses that recorded direction and checks it against the available historical and repository authorities. It does not independently authenticate the conversation. A project charter, AI foundation and readiness report are absent; this integration route explicitly does not require a new bootstrap. No new model-provider runtime is being designed.

## Independent reconstruction

### Product outcome

The existing experiment can measure real Python snapshots but is tied to this source checkout and is absent from the installed development profile. The intended product is a portable measurement capability used within the existing bounded-task workflow: preserve the actual starting code, give implementers useful comparisons, and let a separate reviewer judge design consequences. It must preserve the target repository's existing hard-check obligations.

### Required capabilities / critical journeys

- Install complete runtime, pinned dependencies and defaults into a separate target without taking ownership of target settings or unrelated files.
- Capture dirty, staged and untracked starting source before editing; pass a stable named report through packaged or direct entry.
- Compare affected production and test/harness code, including added and deleted paths, without treating native missing counts as zero.
- Obtain proportionate implementation reasoning and a fresh reviewer comparison of submitted bytes; transfer ignored reports to isolated clones explicitly.
- Correct code while retaining the original baseline and historical reports; stale affected review/check evidence and re-enter only the existing required stages.
- Discover native check scope, policy and owner; consume current applicable evidence or recover missing proof without duplicating aggregate checks solely for reporting.

### Explicit non-goals / constraints

- No new analyzers, generic runner, review stage, controller integration, automatic refactoring or mandatory live evals.
- Advisory targets remain provisional 10/50/5. The recorded direction makes below-target growth informational and requires reasoning for retained breaches and affected legacy hotspots.
- Native hard rules retain their policy. Metrics cannot waive them or broaden optional review applicability.
- Source/index preservation, explicit authorized setup, installation-local dependencies and no active-installation refresh remain required.
- Colocated hashes are provenance, not protection from a malicious writer. Existing high-assurance protection remains external authority.

## Structural checks

- Bundled verifier: `PASS` — `python3 .agents/skills/project-plan-verification/scripts/verify_plan_artifacts.py docs/project-plan.md docs/task-map.json`.
- Reference integrity: `PASS` for the checker's artifact/ID checks and the reviewed semantic handoffs.
- Task dependency graph: `PASS` — serial `T-001 -> T-002 -> T-003 -> T-004 -> T-005`, without cycles.
- Repository architecture check: `PASS` — 4 tests, no skips, using `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`.
- Contract registry check: `PASS` — 5 subsystems, 0 indexed plan references, using `python3 tools/check_contracts.py --root .`.

These checks do not establish future measurement behavior or agent compliance. No analyzer setup, live provider check, agent eval or aggregate implementation suite was run for this report-only review.

## Coverage summary

| Area | Result | Notes |
|---|---|---|
| Scope fidelity | PASS | Available proposals establish the measurement/review need; section 1 identifies the changed response policy and rejects the older new-stage/correctness-runner scope. |
| End-to-end flow completeness | PASS | FLOW-001 ends in demonstrated installed capability or explicit unavailability; FLOW-002 reaches current conditional handoff; FLOW-003 retains the original baseline through recovery or leaves an owned evidence gap. |
| Artifact producer/consumer closure | PASS | ART-001..ART-008 have named producers, authorities and consumers. Ignored report transfer and pre-existing native policy are explicit. |
| State/lifecycle semantics | PASS | Original capture, fresh comparisons, historical preservation, incompatible/partial results, overwrite refusal, stale verdicts and affected-stage correction are distinct. |
| Interface contracts | PASS | IF-001..IF-004 settle CLI/settings/setup, capture handoff, reviewer authority and native-check ownership sufficiently for sequential tasks. |
| Cross-task invariants | PASS | INV-001..INV-009 assign advisory authority, provenance, compatibility, freshness, attribution, installation preservation, conditional routes and native policy to tasks and evidence. |
| Capability/task coverage | PASS | CAP-001..CAP-005 have flows and completion boundaries; every task has a concrete producer/consumer role. See task trace below. |
| Dependency/order composition | PASS | Shared CLI/runtime contracts precede capture, capture precedes implementer consumption, submission precedes reviewer consumption, and final integration follows all producers. |
| Verification coverage | PASS | V-001..V-008 include real installed analyzers, dirty/index preservation, repeated correction, native hard failure/recovery and prepared independently graded agent cases. Unrun agent behavior remains unqualified. |
| Planning abstraction | PASS | Cross-task behavior is settled; internal decomposition, filenames and compact field layout remain delegated. No implementation-local algorithm or class design is required to close a handoff. |

### Critical flow trace

- **FLOW-001:** installer produces ART-001 within its narrow managed boundary; target settings override corresponding defaults, invalid present settings fail, and dependency pins remain installation-owned. Explicit setup owns provisioning in the selected target. The installed CLI runs from an unrelated cwd with source-tree access unnecessary. Missing tools produce actionable unavailable capability rather than implicit installation or global fallback. V-001/V-002 own the decisive real-boundary proof.
- **FLOW-002:** preflight or self-preflight consumes installed capability and native policy, captures actual before bytes and hands off path/scope/origin/identity. The implementer validates applicability, edits within coverage, compares affected added/deleted files and records required rationale and native evidence. The independent reviewer repeats comparison on submitted bytes, checks attribution and rationale, and consumes or recovers required check evidence. Current disposition reaches only the outstanding conditional route. Unsupported/advisory absence is explicit; required native proof remains owed. V-003/V-005/V-006/V-007/V-008 cover the material alternatives.
- **FLOW-003:** corrections invalidate affected proof, preserve ART-002 and history, generate new comparisons/rationale, reconcile stable finding IDs and obtain a fresh affected-stage decision. Report transfer, scope expansion, exact pre-edit remeasurement, native unknowns and unrecoverable evidence have explicit rules. V-004 tests two actual edits against the same baseline; V-006/V-008 cover capability and required-proof recovery.

### Task and invariant placement

| Task | Required contribution and handoff | Evidence / invariant coverage |
|---|---|---|
| T-001 | Owns ART-001/IF-001; completes portable installation, target settings/setup and minimal native-check discovery guidance before later consumers exist. Synchronizes installer and implemented registry contracts through their existing owners. | V-001/V-002/V-003/V-008; INV-001/002/003/006/007/009. |
| T-002 | Produces ART-002/IF-002 and compact IF-004 references using T-001. Preserves readiness profiles and distinguishes stale before state, optional absence and indispensable evidence failure. | V-003/V-006/V-008; INV-002/003/007/009. |
| T-003 | Consumes capture; owns ART-004 and implementer IF-003, including direct capture, current native evidence and original-baseline correction. | V-003/V-004/V-005/V-007/V-008; INV-001/002/003/005/007/008/009. |
| T-004 | Owns ART-005 and reviewer/downstream IF-003. Repeats comparison independently, preserves complete dispositions and current native evidence, and hands off without duplicating functional review. | V-004/V-005/V-006/V-007/V-008; INV-001/003/004/005/008/009. |
| T-005 | Consumes all prior interfaces in an installed repeated-edit journey, including actual hard-check failure and recovery. Publishes ART-006 and prepared agent evals with qualification limits. | All flows, interfaces, capabilities and INV-001..INV-009; deterministic composition is separate from live behavioral qualification. |

Stable ART/IF/INV identities and the preserved CLI provide downstream contract-discovery anchors. Exact future implementation paths are not required; registry synchronization follows implemented authorities rather than registering intended capability now.

## Findings

None. No confirmed BLOCKER, MAJOR or MINOR plan defect was identified.

## Producer/consumer exceptions checked

- ART-006 is legitimate historical evidence consumed by task reviewers and the owner; it need not mutate current state.
- Prior ART-002..ART-005 and ART-008 reports remain historical after supersession; only applicable evidence can authorize the next handoff.
- ART-007 originates with the target repository's existing authority. Tasks discover and preserve it; they do not need to create a linter or registry where none exists.
- Analyzer dependencies originate from installation-owned pins and explicitly authorized setup. The target owns settings and environments, while the installer owns only its declared managed files.
- Protected high-assurance anchors and native stage ownership may pre-exist outside these tasks; the plan neither claims to implement them nor weakens their requirements.

## Open system questions

None blocking downstream task planning. Agent-behavior qualification remains an explicitly budgeted later evidence choice, not a claim supplied by this verdict. Native analyzer skips cannot satisfy the plan's real-tool acceptance criteria.

## Verdict rationale

The plan settles the coordination contracts needed for the five tasks to compose. It includes failure, stale-state and correction paths, preserves repository authority and review independence, and assigns decisive verification without treating schemas or scripted composition as agent behavior. Available evidence reveals no material omission or contradiction. This verdict applies only to the digests above and does not accept any implementation.

## Next action

Feed the verified plan and task map into downstream task planning, starting with T-001. Prepare its executable brief, required verification design and current readiness before implementation. Any material change to the reviewed planning artifacts requires fresh plan verification.
