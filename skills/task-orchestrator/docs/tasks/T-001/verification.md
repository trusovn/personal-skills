# Verification Design: T-001 — Local runtime support

Source brief: brief.md
Source brief revision: SHA-256 3eaa6df3972c254764c1b92992a52dfdbc832f637abb8c89826ea56a994462c2
Verification revision: 1
Authority: derived from brief.md and its cited direction, plan and map
Status: ready

## Coverage summary

| AC / risk | Scenarios |
|---|---|
| AC-01 | V-01 |
| AC-02 / R1 | V-02 |
| AC-03 / R2 | V-03 |
| AC-04 / R3 | V-04, V-05 |
| AC-05 | V-06 |

## Verification scenarios

### V-01 — Select a callable, versioned bridge
Covers: AC-01.
Intent: Reject treating interactive coordinator tools as Python APIs.
Given: installed runtime help, existing adapter and transport tests.
When: inspect callable entry points and perform offline CLI help probes.
Then: report one versioned selection or an exact missing capability; distinguish
existing calls from proposed IF-001/002/004 operations.
Oracle / boundary: local executable output and source, with official documentation
only for claims not settled locally. Help proves parsing, never a successful launch.
Variants: native coordinator delegation versus controller-callable subprocess.

### V-02 — Preserve identity through uncertain recovery
Covers: AC-02, R1.
Intent: Reject duplicate launch and actor-authored provenance.
Given: existing transport fixtures and real process/filesystem wrapper boundary.
When: run focused persistence/resume, live-process refusal and missing-result cases;
trace the spawn-to-receipt crash window against source.
Then: report first/duplicate launch, live/terminal/unknown, missing receipt and
replacement-coordinator semantics; unsupported idempotency stays blocked.
Oracle / boundary: persisted wrapper artifacts and subprocess outcomes; fake runtime
IDs qualify wrapper parsing only. Exact missing real-runtime proof must be stated.
Variants: first launch; same key; live; terminal; unknown; missing launch receipt;
replacement coordinator.

### V-03 — Establish actual permissions and frozen policy
Covers: AC-03, R2.
Intent: Reject claiming sandbox enforcement from argv or prompt wording.
Given: installed runtime interface, policy constants/schema and protected-root layout.
When: inspect enforcement options and context measurement source; use bounded offline
boundary probes only where feasible without expanding permissions.
Then: identify allowed implementation writes, denied reviewer/protected writes,
model/reasoning mappings and exact 0.5 reuse threshold. Missing denial proof or a
reliable context numerator/denominator is unverified, never zero or supported.
Oracle / boundary: actual runtime denial/allow observation for enforcement claims;
source/configuration is labeled separately and unavailable proof is a valid limitation.
Variants: allowed task write; read-only review; run/controller/skill denial; unknown usage.

### V-04 — Commit without losing owner work or duplicating effects
Covers: AC-04, R3.
Intent: Reject broad staging and crash-driven duplicate commits.
Given: disposable Git repository with accepted files plus unrelated staged and
unstaged owner work; no real project commit.
When: inspect or probe an exact-path local commit mechanism and crash recovery.
Then: specify durable intent/receipt, parent/tree identity, index preservation,
reconciliation before retry and blocked unknown commit. A proposed mechanism cannot
be described as implemented finalization.
Oracle / boundary: Git objects, HEAD and index/worktree content in a disposable repo;
missing integrated crash proof is explicit.
Variants: before commit; after commit before receipt; unavailable/unknown commit;
unrelated staged and unstaged content, including mixed task-path staging.

### V-05 — Never invent notification success
Covers: AC-04, R3.
Intent: Reject durable local status as proof that the owner was notified.
Given: no authorization for a real owner notification.
When: inspect callable notification mechanisms and their result boundaries.
Then: specify delivery success/failure/unknown and smallest required proof; keep
real delivery pending and prevent dependency release on uncertain completion.
Oracle / boundary: documented observable delivery status; no actual message is sent.
Variants: success; explicit failure; unknown/unavailable delivery.

### V-06 — Trace every limitation to consumers
Covers: AC-05.
Intent: Reject treating an accepted investigation as harness qualification.
Given: V-01..05 observations and all AC/risk rows.
When: inspect the completed report and reproduction evidence.
Then: every required capability has a disposition/evidence level; Q-001/Q-002,
T-002..006 effects and smallest owner actions are explicit.
Oracle / boundary: report-to-source/probe trace; fresh independent discovery and
separate acceptance remain required after implementation handoff.
Variants: supported; unsupported; unverified.

## Implementation handoff

This design adds no requirements. Preserve scenario IDs. Use existing test fixtures
before adding any. The report may truthfully complete with capability blockers.
No live model launch, network smoke test or notification is authorized. Official
documentation retrieval is permitted by the brief. No production or plan edits.
