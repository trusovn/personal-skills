# Task Brief: T-003 — Give implementers proportionate feedback

## Outcome

Implementation agents use one original code baseline, compare their final changes,
and explain retained complexity where a design decision needs review. Packaged
tasks consume T-002's handoff; direct tasks capture the same evidence during
self-preflight. Submissions carry current measurement and required native-check
evidence so T-004 can add independent comparison and design judgment. For example,
growth from complexity 6 to 8 under a target of 10 needs no individual defense.

This task changes source workflow guidance and prepares executable eval inputs.
It does not establish that an agent followed the guidance. T-005 owns the full
installed handoff and correction proof.

## Authority and scope

- Authority: [project plan, T-003](../../project-plan.md#t-003--give-implementers-proportionate-feedback),
  sections 1–7, FLOW-002/FLOW-003 and V-003/V-004/V-005/V-007/V-008;
  [task-map entry T-003](../../task-map.json). The
  [independent plan review](../../project-plan-review.md) accepted the plan.
- Repository: `personal-skills`; repository instructions, the
  [project map](../../project-map.md) and [development guide](../../development.md)
  govern ownership and verification.
- Dependency: T-002's accepted standalone preflight producer and native-obligation
  handoff, recorded in [acceptance-01.md](../T-002/reviews/acceptance-01.md).
  Consume the current source preflight's
  [starting-evidence fields](../../../skills/task-implementation-flow/task-preflight/references/execution-packet-template.md#starting-evidence-and-native-obligations-both-profiles)
  and the portable format-5 runtime from T-001. Preflight confirms current
  applicability; historical acceptance is not current readiness or agent qualification.
- Allowed changes: source `skills/task-implementation-flow/bounded-task-implementer/`,
  including its inline submission/correction formats, eval definitions and fixture
  setup; `skills/task-implementation-flow/README.md`; and current advisory entry
  points such as `scripts/measure-maintainability.md` and relevant README links.
  Add only the policy precedence/reference changes needed in superseded proposals.
  Extend existing owning measurement/installer coverage only for distinct missing
  evidence at this boundary. Update affected contract records at the designated
  registry-updater stage.
- Inspect `scripts/install_development_skills.py`, its profile guide, shared-file
  list, focused tests and README installation instructions in the same change.
  Synchronize only entries made stale; this task does not inherently add a runtime
  dependency or change profile membership.
- Out of scope: runtime/analyzer redesign, a new checker or evidence store, new
  stages, controller changes, T-004 reviewer protocol, T-005's complete installed
  journey, mandatory live evals and active-installation refresh. Do not rewrite
  historical experiment results or update the plan to track completion.
- Read-only context: current source implementer entry, freshness, optional evidence
  and correction rules; source preflight's accepted producer; the
  [measurement guide](../../../scripts/measure-maintainability.md);
  `tests/test_maintainability.py`, `tests/test_install_development_skills.py`, and
  existing implementer eval cases/setup. Source skills are development specifications,
  distinct from this session's installed skills.

Plan section 1 supersedes the old requirement to defend every increase. Preserve
the provisional advisory targets of 10/50/5 and existing semantic review duties.
Do not split cohesive code, hide arguments, tune exclusions or expand cleanup
scope merely to improve numbers. Native hard rules keep their policy and owner.

### Expected contract impact

- Materialize implementer feedback (`CAP-003`, `ART-004`, implementer side of
  `IF-003`), direct self-preflight's `ART-002`/`IF-002`, and current comparison,
  task evidence and native-check references (`ART-003`, `ART-006`, `ART-008`).
  Consume `ART-001`/`IF-001` and `ART-007`/`IF-004`; preserve `INV-001`,
  `INV-002`, `INV-003`, `INV-005`, `INV-007`, `INV-008` and `INV-009` across
  FLOW-002 and FLOW-003.
- Available dependencies: [measurement](../../contracts/measurement.json)
  owns the runtime, baseline facts and standalone producer guidance;
  [installation](../../contracts/installation.json) owns managed projection;
  [runtime evidence](../../contracts/runtime-evidence.json) supplies optional
  instrumentation without requiring a new lifecycle.
- Expected delta: existing initial and correction submissions give T-004 the
  original baseline, current report, proportionate rationale and native obligations.
  Registry synchronization describes implemented guidance and its proof limits,
  without claiming independent reviewer integration or live compliance is complete.

## Work and acceptance criteria

**AC-01 — Establish starting evidence before either entry path edits code**

Packaged guided and high-assurance entry validate the supplied baseline's project,
captured inventory/source hashes, effective tools/settings/checks and governed
folder coverage before the first implementation edit. Preserve the existing
profile-specific readiness and exact high-assurance freshness rules. A material
starting-state mismatch routes to focused preflight reconsideration, not silent
replacement capture or broad rediscovery by the implementer.

Conversational direct execution uses self-preflight to attempt the same capture
contract before editing supported, authorized Python scope. Capture actual
worktree bytes, including relevant dirty/staged/untracked code, without changing
source or the real index. Include relevant production, test, eval, fixture and
harness folders under existing exclusions/asset groups. Existing empty parent
folders can cover future Python files. Use the installation-local runtime and
fresh JSON/text paths; never provision tools implicitly. Direct work needs no
new task package or formal identity solely for measurement.

**AC-02 — Compare the final affected scope and report coverage honestly**

Before submission, compare final changed, added and deleted Python paths within
captured coverage, including relevant test/harness assets. Determine affected
functions from actual behavioral, structural or responsibility changes using
the diff and local context. File membership, line movement or formatting alone
does not make an untouched sibling affected. Assess extracted responsibilities
together with their helpers; do not build a change-attribution analyzer.

Reference exact original JSON/text paths, current comparison paths, coverage and
measurement status in existing submission formats. Missing native counts and
unmatched symbols remain unknown; explain rename/move/extraction relationships
without invented deltas. Docs-only/unsupported work records N/A. Missing, partial,
stale, incompatible or uncovered evidence is explicit and cannot claim a clean
or complete comparison. Attempt current measurement when recoverable before
evidence is absent, recording the before-state gap. Advisory absence blocks only
when explicit authority makes that evidence indispensable, with owner/recovery
named; other required checks retain their failure policy.

**AC-03 — Give retained breaches proportionate reasoning**

Apply every condition in plan section 5. Growth at or below the target is
information only. Explain new or newly crossed breaches, worsening existing
breaches, and retention of materially edited legacy hotspots even when equal
or improved. Consider useful local cleanup without requiring target compliance.
Untouched legacy hotspots remain context only; smaller numbers do not excuse
worse ownership, names or navigation.

Required rationale identifies report, function, metric, known before/after,
why the decisions belong together and the cost of a plausible alternative.
Group related metrics when one explanation suffices. Recover missing required
rationale; do not turn a bare threshold into an automatic rejection or a
per-increase defense below target. Preserve existing naming, ownership,
test/harness and abstraction guidance.

**AC-04 — Preserve the baseline and route corrections for current bytes**

Corrections retain the original baseline and prior reports and create new named
comparisons and applicable rationale. Changed bytes stale affected evidence and
verdicts. Preserve existing complete coverage ledgers, stable finding/scenario
IDs, separate owners and affected-stage ordering; successful implementation
measurement is not independent review.

Unexpected scope expansion requires authorized scope resolution and exact
preserved pre-edit evidence for added coverage, or an explicit unrecoverable gap.
Never relabel edited code as the original baseline. For isolated consumers,
identify the exact JSON/text files and receiving paths to transfer; ignored
reports do not travel with commits. A report collision requires a fresh path,
not deletion or replacement. The next task captures its own actual starting code.

**AC-05 — Keep required native evidence and optional instrumentation distinct**

Consume the handed-off native-check inventory; direct self-preflight discovers
the same command, scope, policy, requiredness and existing owner fields. Documented
commands suffice without a registry. Record none when no check exists; invent
no lint/typecheck command. Preserve whole-project scope and execute required
applicable checks under existing ownership.

Carry current `ART-008` evidence beside the metrics reference, including command,
governed scope/policy, checked-byte identity, result and producer/stage. Reuse
aggregate evidence only with established constituent coverage, scope, policy
and current bytes. Do not rerun constituents solely for reporting. Missing/stale
required evidence remains owed to its real owner. Successful metrics cannot mask
a required static-check failure, including when Python measurement is N/A.

Preserve optional run-evidence availability, skip-once and strict-contract rules.
Wrapping an actual comparison is permitted when appropriate; no duplicate run
or new evidence lifecycle is required. Measurement availability and optional
instrumentation availability remain separate facts.

**AC-06 — Prepare decisive evals and align current policy entry points**

Reuse/update existing implementer entry and correction fixtures before adding
cases. Supply inputs, tools, authorized report-write paths and oracles needed for
the T-003 portions of V-003/V-004/V-005/V-007/V-008, including both entry paths,
original-baseline corrections, below-target growth, retained/legacy breaches,
affected versus untouched siblings, missing evidence and native failure/reuse.
Preserve distinct existing entry, freshness, provenance and correction cases.

The source flow README and current advisory entry points lead to plan section 5's
policy. Mark or link superseded proposal policy clearly where needed without
rewriting historical experiment evidence. Keep conditional review applicability:
measurement warnings alone do not require an otherwise optional review stage.
Deterministic fixture/tool checks prove only their exercised boundary. Prepared
agent evals grade actual artifacts, diff, rationale and retained obligations;
syntax, keywords or setup exit status alone do not qualify agent behavior.

## Evidence boundaries

Verification-design recommendation: **separate — two entry paths, affected-function
attribution, correction continuity and native/advisory evidence policies require
distinct scenarios.** Derived `verification.md` owns the detailed matrix, setup,
oracles, evidence reuse and gate allocation under AC-01–AC-06.

The existing pinned CLI, preflight handoff and disposable Git/installer fixtures
provide the believed-existing observation mechanisms. Preflight confirms their
current availability and authorized paths. A missing indispensable mechanism
returns to its owner; it does not authorize building a shared harness here.

Start with changed fixture/targeted checks and the owning measurement suite,
then installer coverage when affected. Run canonical architecture and contract
checks before handoff; use `python3 tools/verify.py` for a cross-cutting
implementation after focused checks pass. Report skips, failures and active-profile
drift. Never refresh this invocation's installation. Live model execution requires
separate runtime/budget approval; unrun agent behavior remains unqualified.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Profile: `guided`
Brief revision: `1`

The brief is prepared; execution prerequisites remain. Next, use
`task-verification-designer` to create `verification.md`, then standalone guided
`task-preflight` to create a current ready `preflight.md` before implementation.
This brief does not certify present readiness or require high-assurance execution
merely because the source skill supports it.

Use the [shared submission route](../../../.agents/skills/README.md#submission-route),
with separate fresh discovery and acceptance for `review: immediate`. T-004
consumes the resulting implementer contract; T-005 owns full installed composition.
Stop for unresolved ownership overlap, material authority/scope changes or missing
indispensable capability. Carry any evidence gap and its owner into the handoff.

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
  Includes focused discovery, instructions/inline formats, fixture updates,
  policy entry points and implementation verification; excludes separate
  preparation, reviews and registry synchronization.
- Policy result: `override_cannot_split_safely`.
- `decomposition_override: cannot_split_safely` — exceeds the 15-call and
  40-minute limits. Considered splitting baseline entry from feedback/corrections.
  Both would edit the same implementer instructions, inline submission formats
  and entry/correction fixture setup, while the second would need to revise and
  reverify the first's evidence fields. Keeping one owner avoids an intermediate
  incomplete submission contract and repeated fixture negotiation. The active
  policy permits this override. Residual risk is the breadth of finite eval cases;
  use the estimate as a soft checkpoint and return material scope growth to design.
