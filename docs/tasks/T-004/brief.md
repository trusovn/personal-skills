# Task Brief: T-004 — Add independent measurement and review decisions

## Outcome

A fresh maintainability reviewer compares the actual submitted code against the
task's original baseline, checks the implementer's affected-function attribution,
and records a disposition for each required design rationale. The review carries
current native-check evidence into the existing downstream route. A justified
threshold breach can receive `ACCEPT`; a request for correction needs a concrete
maintenance problem or an applicable hard-rule violation.

This task changes source workflow guidance and prepares executable review evals.
It enables T-005's complete installed handoff and correction proof. Local fixture
checks establish the states they exercise; they do not prove agent compliance.

## Authority and scope

- Authority: [project plan, T-004](../../project-plan.md#t-004--add-independent-measurement-and-review-decisions),
  sections 1–7, FLOW-002/FLOW-003 and V-004–V-008;
  [task-map entry T-004](../../task-map.json). The
  [independent plan review](../../project-plan-review.md) accepted the plan.
- Repository: `personal-skills`. Repository instructions, the
  [project map](../../project-map.md) and [development guide](../../development.md)
  govern ownership and verification.
- Dependency: T-003's accepted implementer comparison, rationale and correction
  handoff, recorded in [acceptance-01.md](../T-003/reviews/acceptance-01.md).
  Consume the original-baseline and native-obligation fields supplied through
  T-002 and the portable format-5 runtime from T-001. Historical acceptance
  establishes the dependency's source/preparation result, not current execution
  readiness, live agent compliance or installed end-to-end qualification.
- Allowed changes: source `skills/task-implementation-flow/task-maintainability-review/`,
  including its inputs, protocol, report form, correction instructions and eval
  definitions/setup. Change `task-review-discovery/`, `task-acceptance-review/`
  and `skills/task-implementation-flow/README.md` only where needed to consume
  this review evidence and preserve existing routing. Reuse owning test/fixture
  coverage; extend it only for distinct missing evidence at this boundary.
  Synchronize affected contract records at the designated registry-updater stage.
- Inspect `scripts/install_development_skills.py`, `DEVELOPMENT_SKILL_SOURCES`,
  `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`, focused installer tests and
  README installation instructions in the same change. Synchronize entries made
  stale, while preserving the installer's narrow ownership boundary. No new
  profile membership or runtime dependency is inherently required.
- Out of scope: runtime/analyzer redesign, new static tools or attribution
  analyzers, a new runner/registry/evidence store, new stages, controller changes,
  full functional review, T-005's complete installed journey, mandatory live evals
  and active-installation refresh. Keep results beside the plan; do not update
  plan documents to track completion.
- Read-only context: source maintainability guidance, its existing
  `evals/evals.json` and `evals/files/setup_fixture.py`; source implementer
  submission/correction contracts; existing discovery/acceptance entry and
  correction fixtures; the [measurement guide](../../../scripts/measure-maintainability.md);
  `tests/test_maintainability.py` and `tests/test_install_development_skills.py`.
  Source skills are development specifications, separate from active installed
  instructions. Use disposable installations to verify changed distribution.

Plan sections 1 and 5 govern proportionality and supersede the older requirement
to defend every increase. Preserve provisional advisory targets of 10/50/5,
session independence, naming and ownership guidance, significant test/eval/harness
review, and abstraction-cost calibration. Measurement warnings alone do not make
an optional review stage required. Cleanup remains local, authorized and verifiable.

### Expected contract impact

- Materialize independent reviewer disposition (`CAP-004`, `ART-005`) and the
  reviewer/downstream side of `IF-003`; produce reviewer-owned `ART-003`, task
  evidence (`ART-006`) and current native-check references (`ART-008`). Consume
  `ART-001`/`ART-002`/`ART-004` and native policy (`ART-007`, `CAP-005`, `IF-004`);
  preserve `INV-001`–`INV-005` and `INV-007`–`INV-009` across FLOW-002/FLOW-003.
- Available dependencies: [implementer feedback](../../contracts/implementer-feedback.json)
  owns submission/rationale and correction references;
  [measurement](../../contracts/measurement.json) owns the runtime, baseline,
  standalone producer and native-policy discovery;
  [installation](../../contracts/installation.json) owns managed projection;
  [runtime evidence](../../contracts/runtime-evidence.json) owns optional capture.
- Expected durable delta: current numbered maintainability reports provide a
  fresh comparison, complete rationale dispositions, native-check evidence and
  the applicable outstanding route. Registry synchronization records the actual
  source guidance and proof limits; it must not claim live agent qualification.

## Work and acceptance criteria

**AC-01 — Independently compare the submitted bytes**

Extend review inputs and protocol to consume the exact original baseline,
implementer comparison, rationale and native-obligation handoff. A fresh reviewer
invokes its own comparison through the active installation's runtime on current
changed/added/deleted Python paths within captured coverage, including relevant
test/eval/fixture/harness assets. Reusing the implementer's report alone is not
independent comparison. Preserve same-session `SELF_CHECK_ONLY` and the existing
read-only boundary except authorized report writes.

Check logical project, source applicability, tool/settings/check compatibility,
coverage and current submitted-byte identity. Use fresh named report paths;
preserve source/index, original baseline and prior report pairs. Isolated review
receives exact JSON/text transfer paths; ignored reports do not travel with
commits. No implicit setup, cross-installation fallback or baseline recapture
after editing is allowed. Missing, stale, incomplete, incompatible or uncovered
evidence is explicit. Attempt recoverable current measurement and record any
before-state gap. Docs-only/unsupported scope is N/A. Advisory absence blocks
only under explicit indispensable-evidence authority, with owner and recovery
named; it never supplies clean or complete comparison evidence.

**AC-02 — Assess affected responsibilities and proportionate rationale**

Apply every condition in plan section 5. Verify affected-function attribution
from the diff and local context: file membership, line movement and formatting
alone do not make untouched siblings affected. Assess renamed/moved/extracted
responsibilities with their helpers; unknown counts or unmatched symbols remain
unknown rather than zero or invented deltas.

Growth at or below target is information only. Explicitly dispose of rationale
for new/newly crossed breaches, worsening breaches and materially edited legacy
hotspots retained above target even when equal or improved. The rationale names
report, function, metric, known before/after, cohesion and a plausible alternative's
cost; related metrics may share one explanation. Recover missing required
rationale. Useful bounded cleanup is considered, without mandatory threshold
compliance or blocking unchanged legacy debt.

Record agreement or a concrete counterargument with future maintenance cost
and the smallest reasonable correction. A bare threshold cannot cause
`CHANGES_REQUESTED`; smaller metrics cannot excuse worse ownership, names,
navigation, hidden arguments or speculative abstractions. Preserve the existing
semantic review and hard-architecture rules and separate functional ownership.

**AC-03 — Preserve native policy and consume current check evidence**

Add compact existing-check evidence to review inputs/protocol/output. Retain
each command's governed scope, policy, requiredness and stage owner, plus checked
bytes, result and producer/stage. Validate current coverage; keep required
architecture-gate run/validation under existing authority. Consume applicable
lint/typecheck evidence and recover missing/stale required proof through its
owner or an authorized focused run, without duplicating general functional review.

Preserve whole-project scope. Reuse current aggregate evidence only when its
constituent coverage, scope, policy and checked bytes are established; do not
repeat constituents merely to populate report sections. Do not invent commands
or require a registry where documented commands suffice; record none when absent.
Native hard failures, missing required proof and advisory metrics have separate
dispositions. A required native failure remains visible when measurement succeeds
or is N/A; success in metrics cannot waive it. Contradictory policy returns to
its authority owner. Optional run-evidence wrapping does not require a second
execution or replace missing measurement/native evidence.

**AC-04 — Carry a complete review result outside the warning cap**

Extend the existing numbered report with compact measurement status and exact
baseline/current report references, scope/byte identities, and all relevant
rationale dispositions. Retain native-check evidence and any owed proof/owner.
Required dispositions and gaps remain outside the optional `WARNINGS` list's
three-item cap; neither that cap nor an early decisive finding can truncate them.
Preserve every confirmed blocker and stable finding identity.

`ACCEPT` can retain justified breaches when required evidence and existing review
conditions are satisfied. Missing mandatory proof follows existing incomplete-review
rules; it cannot disappear under a successful metric result or verdict label.
Keep `ACCEPT`, `CHANGES_REQUESTED`, `INCONCLUSIVE` and measurement execution
outcomes distinct. The maintainability verdict applies to reviewed bytes and
does not certify functional acceptance.

**AC-05 — Preserve correction continuity and the conditional downstream route**

Corrections keep the original baseline and historical reports, use fresh
comparisons and update rationale/native evidence for affected current bytes.
Changed scope stales affected reports/verdicts. Retain surviving and resolved
finding IDs without recycling them, and preserve complete coverage ledgers and
separate evidence/correction/decision ownership.

Downstream discovery and acceptance consume applicable maintainability evidence
without repeating general review. Name the first outstanding stage and complete
ordered remainder: applicable registry synchronization, fresh discovery, then
separate acceptance, under the existing submission route. Re-enter only conditional
stages affected by corrections; current evidence can retain an unaffected stage.
Do not invent registry/review stages or execute downstream work as a reviewer.
Unexpected scope expansion needs authorized resolution and exact preserved
pre-edit evidence, or an explicit gap; it never permits relabeling edited code
as the original baseline.

**AC-06 — Prepare decisive review and routing evals**

Inspect and reuse existing maintainability entry, independence, report-path,
multi-finding, test/harness, correction and genuine-stop cases before adding
coverage. Extend downstream route fixtures only where needed for the new handoff.
Supply actual inputs, tools, report-write permissions and oracles for T-004's
V-004–V-008 obligations: fresh versus stale comparison, original-baseline
corrections, below-target growth, justified breaches, touched versus untouched
legacy hotspots, misleading extraction, missing/incompatible evidence, required
native failure beside successful metrics, current aggregate reuse and stale-proof
recovery. Exercise complete dispositions beyond three optional warnings.

Preserve distinct existing scenarios and fixture boundaries. Prepared evals grade
actual artifacts/diff, rationale, evidence and route, rather than keywords alone.
Deterministic setup/tool checks report only exercised behavior. Do not claim live
agent results without separately authorized execution and independent grading.

## Evidence boundaries

Verification-design recommendation: **separate — independent comparison, complete
dispositions, correction freshness and native/advisory policy require distinct
success, failure and recovery scenarios.** Derived `verification.md` owns the
detailed scenario matrix, fixtures, observations, reuse and stage/gate allocation.

The portable pinned CLI, accepted implementer handoff, disposable installer/Git
fixtures and existing review eval setup provide believed-existing observation
mechanisms. Preflight confirms availability and authorized paths. A missing
indispensable capability returns to its owner; it does not authorize a new shared
harness here.

Start with changed fixture/targeted checks and owning measurement coverage,
then installer coverage when affected. Run canonical architecture and contract
checks before handoff; use `python3 tools/verify.py` for cross-cutting implementation
after focused checks pass. Report skips, failures and active-profile drift without
refreshing this session's installation. Live model execution needs separate
runtime/budget approval; unrun agent behavior remains unqualified.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Profile: `guided`
Brief revision: `1`

The brief is prepared; execution prerequisites remain. Next, use
`task-verification-designer` to create `verification.md`, then standalone guided
`task-preflight` to create a current ready `preflight.md` before implementation.
This brief does not certify present readiness or require high-assurance execution
merely because the source workflow supports it.

Use the [shared submission route](../../../.agents/skills/README.md#submission-route),
with separate fresh discovery and acceptance for `review: immediate`. T-005
consumes the reviewer/report contract for the complete installed composition proof.
Stop for material authority/scope changes, unresolved ownership overlap or missing
indispensable capability; carry the exact gap, owner and recovery action forward.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 20 tool calls / 55 minutes / focused context
```

### Execution sizing

- Policy: active `default`, version 1, from the installed designer's
  `references/task-sizing.yaml`.
- Estimate: 20 agent calls; 55 implementation minutes; confidence: medium.
  Includes focused discovery, reviewer protocol/report/correction changes,
  fixture updates, minimal downstream guidance and implementation verification;
  excludes separate preparation, reviews and registry synchronization.
- Policy result: `override_cannot_split_safely`.
- `decomposition_override: cannot_split_safely` — exceeds the 15-call and
  40-minute limits. Considered separating reviewer comparison from disposition
  and downstream handoff. Those parts share the same review inputs, report,
  correction protocol and existing correction/route fixtures; a split would
  require revising and reverifying an intermediate incomplete review contract.
  The downstream changes are limited consumers of that contract. One owner avoids
  repeated contract negotiation. The active policy permits this override.
  Residual risk is the number of finite evidence cases; treat the estimate as a
  soft checkpoint and return material scope growth to design.
