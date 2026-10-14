# Issues for separate fixes

Each item separates observed behavior from source-contract inspection. These
are integration findings, not grades of actor reasoning. All seven live stages
completed; see `README.md` and the preserved evidence for the proof limits.

## FLOW-01 — Structured stage outcomes are incomplete

- Evidence: `bounded-task-implementer` supports a caller-supplied JSON schema.
  Preflight uses a Markdown packet; maintainability uses uppercase text labels;
  acceptance uses a Markdown report; registry update uses text statuses. Brief
  readiness, verification recommendation, scope, and sizing are human-readable.
- Impact: code must interpret several prose layouts to extract readiness,
  findings, authority defects, coverage, and correction ownership. A status regex
  does not validate the whole handoff. Fail-closed parsing can stop valid work;
  permissive parsing can advance incomplete evidence.
- Owner: implementation-flow contracts plus the orchestration adapter.
- Bounded fix: define versioned, typed per-stage sidecars or envelopes under one
  common invocation identity. Preserve canonical human reports. Include explicit
  no-output/blocked outcomes; do not require an AI coordinator to infer them.
- Acceptance: valid examples for all seven stages validate; missing task/stage
  identity, wrong artifact, unknown outcome, conflicting verdict, missing blocker
  owner, and omitted required coverage reject. Code routes representative blocked
  and correction outcomes without reading prose.

## FLOW-02 — Immediate-review handoff conflicts with required stage order

- Evidence: implementer `Machine-contracted invocation` requires `next_action`
  to route to a fresh acceptance reviewer for immediate review. Its provenance
  and ordinary output sections use the same direct route. The flow README and
  registry boundary require architecture, maintainability, registry update, then
  acceptance when applicable.
- Impact: obeying the implementer's next action can bypass required stages;
  obeying the flow means overriding an otherwise valid actor handoff.
- Owner: implementer handoff contract and flow transition contract.
- Bounded fix: distinguish submission endpoint from controller-selected next
  stage. Represent required pending obligations explicitly, or route to a
  controller handoff that cannot be mistaken for permission to skip them.
- Acceptance: immediate-review tasks with and without maintainability/registry
  obligations produce compatible results. No valid result directs code to
  functional acceptance before its prerequisites.

## FLOW-03 — Conditional flow rules have no code-readable authority

- Evidence: README prose owns required standalone orchestrated preflight,
  optional verification, conditional maintainability and registry stages, and
  different correction routes. The older orchestrator's closed stage list is
  `preflight -> implement -> verify -> semantic_review -> accept`.
- Impact: a new executor must reproduce the flow policy in code. Updating the
  skills can silently leave stage selection or invalidation stale.
- Owner: flow package; executor consumes its supported contract version.
- Bounded fix: publish a small flow manifest for supported stages, prerequisites,
  applicability facts, allowed effects, outcomes, correction routes, and
  invalidation. Keep semantic judgment inside each skill.
- Acceptance: deterministic tests select the complete route, justified omissions,
  and both correction routes. Unknown contract versions and contradictory repo
  requirements stop. A flow-rule change requires a compatibility test change.

## FLOW-04 — Freshness/effect records need one machine representation

- Evidence: preflight's packet template requires exact SHA-256 identities and
  before/after short status in Markdown. Implementer recalculates every recorded
  value. Acceptance compares the original baseline with current implementation,
  runtime artifacts, and reports. Review artifacts add authorized status deltas.
- Impact: code cannot robustly distinguish legitimate lifecycle effects from
  stale evidence by parsing loosely formatted snapshots. Default short status
  can collapse new files into one untracked directory entry.
- Owner: flow evidence contract and shared deterministic capture helper.
- Bounded fix: specify canonical identity records for HEAD, index/worktree,
  absent/deleted paths, authority inputs, command evidence, and exact authorized
  artifact writes. Keep stage-start identity separate from original task baseline.
- Acceptance: same-status byte edits and index-only edits invalidate evidence;
  creation of the one allocated packet/report succeeds; extra files reject;
  legitimate implementation and registry effects do not falsely invalidate
  downstream review. Include an untracked package with no placeholder files.

## FLOW-05 — Correction findings do not provide typed ownership

- Evidence: acceptance prose distinguishes implementation defects, reference-only
  defects, authority/design problems, and current-state blockers. Registry
  `BLOCKED` names one of implementation/planning/repo-foundation, while acceptance
  and preflight express the next route in prose. The implementation correction
  contract requires a complete ledger and finding IDs.
- Impact: deterministically choosing the right loop requires classified defects,
  affected byte classes, and complete continuation payloads. A free-text route
  cannot safely drive retries or retain a maintainability verdict.
- Owner: review/preflight/updater result contracts.
- Bounded fix: add bounded owner/reason enums, affected path classes, finding IDs,
  complete coverage rows, and required next inputs. Validate actual file effects
  before using the classification.
- Acceptance: production findings re-enter gates and fresh reviews; reference-only
  findings re-enter updater and fresh acceptance; a mislabeled production effect
  cannot retain maintainability approval; authority mismatches never auto-correct.

## FLOW-06 — Workflow digest is not a retained runnable flow version

- Evidence: `scripts/workflow_version.py:fingerprint_workflow` hashes files inside
  one skill directory. Shared helpers are separate installer inputs. The flow
  consists of seven skills, their references, external schemas, and adapter rules.
- Impact: a digest can identify changed content but cannot reproduce an old run
  after installation refresh; one skill digest is not the identity of all stages.
- Owner: flow distribution and orchestrator run-version contract.
- Bounded fix: add a retained bundle manifest covering all required skill,
  reference, helper, schema, policy, and adapter dependencies. Explicitly separate
  content identity from protocol compatibility. Preserve existing fingerprint
  semantics unless a separate compatibility decision changes them.
- Acceptance: start a run, replace installed skills/helpers, and resume using
  retained original bytes. Missing retained inputs cause a specific stop. New runs
  adopt only a qualified version.

## SETUP-01 — Development installer fails in an unborn Git repository

- Observed: canonical installer returned `workflow_unavailable`, caused by
  `fatal: ambiguous argument 'HEAD'`, immediately after `git init`. Adding an
  initial empty commit allowed installation to complete.
- Reproduction: initialize a new temporary Git repository, then invoke
  `python3 scripts/install_development_skills.py <root>` before its first commit.
- Impact: a valid new Git repository cannot install the profile at bootstrap.
  This is a setup defect, not an implementation-stage failure.
- Owner: installer/run-evidence workflow availability integration.
- Bounded fix: represent unborn HEAD explicitly or document and enforce a first
  commit prerequisite before attempting installation. Keep installer ownership
  limits intact.
- Acceptance: focused installer behavior test on a genuine unborn repository;
  verify the selected disposition and no unintended edits. Syntax checking alone
  is insufficient.

## SETUP-02 — Selected project-local copies lag source without a qualification signal

- Observed: this repository's installed implementer and acceptance `SKILL.md`
  differed from their source; the other five matched. Implementer lacked newer
  helper availability/skip-once instructions; acceptance lacked explicit valid
  and invalid validator-instance probes. The experiment avoided this drift with
  a fresh canonical installation of the requested source into the fixture.
- Impact: a test launched in the maintenance repository can exercise older
  instructions while appearing to test current source. Installation precedence
  makes silent source substitution incorrect.
- Owner: installation qualification/refresh procedure, not actor reasoning.
- Bounded fix: expose source-vs-installed identity and an explicit refresh/check
  command for maintainers. Do not automatically upgrade active runs.
- Acceptance: an intentionally stale installed copy is reported before launch;
  an explicit refresh synchronizes the profile and helpers; pinned active runs
  retain their earlier bundle.

## LIVE-01 — Durable review evidence is not fully replayable by itself

- Observed: `maintainability-01.md` contains `ACCEPT`, architecture evidence, and
  reviewed paths, but its exact pre/post Git snapshots are only available in the
  command transcript and controller ledger. Acceptance's REV-01 command is
  `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY' ... PY`, which omits the actual probe
  body. Its CR-01 validator evidence covers a valid registry; the deliberate
  invalid-instance probe was supplied by the separate post-run audit.
- Authority: maintainability's durable-report instructions require exact status
  records; the acceptance template requires exact reproducible command records;
  source acceptance instructions require valid/invalid evidence for a material
  executable-validator boundary. The compact maintainability output example has
  no dedicated fields for those status records.
- Impact: code cannot regard an `ACCEPT` label as complete high-assurance evidence.
  Artifact consumption alone loses replay inputs. The experiment succeeded at
  its smoke gates, but those gates did not enforce every prose requirement.
- Owner: review evidence contracts and the deterministic admission validator.
- Bounded fix: add explicit durable snapshot/session/byte-identity fields and
  references to complete executable probe files or exact argv/stdin records.
  Model validator cases as explicit valid/invalid evidence when applicable. Let
  controller-captured evidence satisfy named fields; avoid copying full logs
  into every report. This can follow FLOW-01 and FLOW-04 without changing the
  reviewer rubric.
- Acceptance: a report with a placeholder command, missing required snapshot,
  missing applicable invalid-instance probe, or an unavailable evidence reference
  does not advance. A report referencing complete controller evidence validates
  and replays locally. Judge evidence completeness, not reasoning style.

## TELEMETRY-01 — Shared instrumentation was not exercised by this flow run

- Observed on follow-up audit: all seven transports emitted usage and session
  events, and the driver retained model/effort argv and file/command evidence.
  No stage invoked `run_evidence.py`. The fixture's Git-local run-evidence
  storage exists from installer availability probes but contains no run files.
  The launcher supplied no canonical runtime-context JSON file. See
  `evidence/telemetry-audit.json`.
- Impact: the happy path does not qualify canonical begin/finish manifests,
  runtime-context ingestion, retained Git tree snapshots, check timing, or
  recovery. Driver evidence cannot be presented as successful operation of the
  shared collector. This is missing integration/qualification coverage, not a
  demonstrated defect in the collector; the skill documents instrumentation
  primarily for ordinary guided use, and this experiment used high-assurance.
- Owner: launcher instrumentation adapter and flow instrumentation policy.
- Bounded fix: decide and encode collector applicability for each profile/stage.
  Supply trusted runtime-context metadata through its existing contract. Bind
  transport usage/session records to canonical run identity. Define one lifecycle
  owner so actor and controller cannot create duplicate active runs. Preserve
  documented optional-skip behavior where collection is optional.
- Acceptance: a simple task with explicit instrumentation policy produces a real
  begin/finish manifest with the correct task, workflow, session, model/effort,
  retained repository boundaries, and captured command duration/output. Exercise
  optional unavailable behavior, mandatory unavailable blocking, and recovery of
  an interrupted open run. Merely installing helpers or probing availability
  does not count as lifecycle evidence.
