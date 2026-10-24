# Task Brief: T-001.3 — Expose advisory discovery and prove installed composition

## Outcome

Foundation guidance lets agents find the installed advisory command beside a
repository's existing native checks. A real disposable installation demonstrates
the complete T-001 result: capture, edit, compare, truthful failure handling and
source/index preservation. T-002 can then consume the accepted installed contract.

## Direction trace

- Direction contribution: first useful proof in the plan's Product outcome and
  section 7's separation of advisory measurement from existing hard checks.
- User-observable effect: discoverable installed command and verified local
  operation against a separate repository without the source checkout.
- Why now: closes T-001 before preflight integration in T-002.
- Direction decisions used: plan sections 1–2, 6–7, T-001 and V-001/V-008.
- New direction decisions required: None.

## Authority and scope

- Authority: [parent authority and reviewed identities](../T-001/brief.md#authority-and-scope);
  plan section 10's T-001 foundation guidance and section 11 verification map.
- Repository: `personal-skills`; repository instructions govern source/installation
  separation, test reuse and the independent review route.
- Dependencies: accepted T-001.1 installed runtime/settings/setup and T-001.2
  report/empty-baseline behavior; consume their actual registry records and evidence.
- Allowed changes: source `skills/repo-foundation/`,
  `skills/architecture-guardrails/` including `templates/gates.yaml`; inspect
  `skills/project-bootstrap/` and `skills/foundation-readiness-review/`, changing
  only integration-stale references. Relevant measurement/installer tests,
  installer membership/managed-file checks, `skills/README.md`, `README.md`,
  tool guide and project-map paths may change only for this discovery/composition.
  Final evidence goes in this package's `results.md` and separate review artifacts.
- Out of scope: T-002–T-004 instruction changes and T-005's full implemented
  workflow/reviewer/correction journey or live-agent qualification. Parent
  exclusions apply; do not introduce a checker/runner or registry requirement.
- Read-only context: current foundation guidance, optional gates template, both
  predecessor submissions/reviews and existing reusable installer fixture helpers.
- Assumptions: native check discovery already exists in source guidance; exact
  effective predecessor paths and prepared interpreter are confirmed in preflight.

Use a single discovery pass through a registry/equivalent, then existing agent
instructions, map and native task configuration as needed. Carry command,
scope/policy reference, requiredness and stage owner without copying policy.
Documented commands suffice without a registry. Advisory success cannot waive
a native hard failure, narrow native scope or require a new review stage.
Applicable current aggregate evidence covers its constituents without duplicate
execution just to populate reporting. No new linter/typechecker is selected.

### Expected contract impact

- Materialize ART-007/IF-004 foundation discovery alongside ART-001/IF-001;
  produce T-001's combined ART-006 proof. Preserve INV-001/INV-002/INV-003/
  INV-006/INV-007/INV-009 and native-check ownership.
- Current dependencies: [installation](../../contracts/installation.json),
  [foundation tools](../../contracts/foundation-tools.json), and T-001.1/T-001.2's
  implemented measurement record, resolved through the current contract index.
- Expected delta: discoverable advisory CLI/settings/setup references, with
  native scope/policy/owner preserved, and complete installed proof for T-002.
  Registry stage synchronizes only actual implemented authority/discovery changes.

## Work and acceptance criteria

- **AC-01:** Source repo-foundation and architecture-guardrails explain where
  enabled advisory measurement is discovered, target/default policy and explicit
  setup. The optional gates template remains command discovery; it does not
  duplicate thresholds or become mandatory. Existing native check rules, scope,
  requiredness and declared owners remain clear and unchanged.
- **AC-02:** Inspect bootstrap/readiness guidance for conflicts. Correct only
  integration-stale references; record no-change dispositions when appropriate.
  Synchronize installer selections, managed files, profile guide, focused installer
  coverage and README as applicable. Never refresh the active installation.
- **AC-03:** From an unrelated cwd, run the installed CLI with real pinned
  analyzers on a disposable Git target without source-checkout access/dependency.
  Capture dirty/staged/untracked starting code, make an actual edit including
  added/deleted paths within captured scope, compare, and assert values, source
  identities, native unknown handling and source/real-index preservation.
  Include empty-parent capture -> new file -> valid comparison.
- **AC-04:** Installed proof covers target/default and mixed settings origins,
  malformed target settings, missing tools with target-aware setup instructions,
  old-format baseline rejection, neutral JSON/text labels, successful breaches,
  and fresh report names with overwrite refusal. Reuse predecessor behavioral
  cases; add only missing installed-boundary evidence.
- **AC-05:** Fresh install, refresh and read-only drift detection include all new
  shared files and updated skills while preserving unrelated target bytes,
  policy, environments/reports and AGENTS content. Installation cannot fall back
  to this checkout or user-global helpers.
- **AC-06:** A disposable target with a real existing static check produces a
  hard failure while advisory measurement succeeds. Published evidence keeps
  the results/policy/owners separate. Guidance preserves whole-project scope,
  current aggregate reuse and missing/stale required-proof duties; when no native
  command exists it invents none. This task proves tool composition and prepares
  the discovery handoff; live agent compliance remains unqualified.

### Finite-risk cases

#### R-05 — Discovery weakens native check authority; AC-01–AC-02, AC-06

- Invariant: INV-001/INV-009; native policy, scope and owner survive integration.
- Material cases: existing registry or documented commands only; no applicable
  native command; hard failure alongside metric success; current aggregate
  covering constituents; missing/stale required evidence.
- Oracle/boundary: a real declared native check fails on supplied fixture input
  while installed metrics complete; published references retain both outcomes.
  For instruction-only cases, inspect concrete example handoffs and policy
  references; these are structural evidence, not proof of agent compliance.
- Implementation evidence: reuse existing fixture facilities, identify the
  command's real authority, and record actual input/result. Inspect all four
  named foundation skills and relevant template for conflicting obligations.
- Independent review probe: trace one native obligation through the modified
  discovery guidance, check aggregate coverage/required-proof handling and
  reproduce the mixed hard/advisory result on a fresh disposable target.
- Gate owner/stage: implementer owns local proof; fresh discovery owns independent
  corroboration. No live eval is required or authorized here.

#### R-06 — Installed first proof depends on source or loses target bytes; AC-03–AC-05

- Invariant: INV-002/INV-003/INV-006/INV-007; the complete installed boundary
  preserves provenance, report history, target bytes and real index.
- Material cases: installed baseline -> real edit -> compare; empty parent ->
  added file; captured deleted file; settings/default/invalid cases from R-01;
  format/unknown/collision cases from R-03/R-04; install/refresh/drift from R-02.
- Oracle/boundary: real separate-target CLI and native analyzer output, exact
  index/source/report identities, explicit incompatible/unavailable status,
  and successful installed operation with original source inaccessible.
- Implementation evidence: extend existing measurement/installer cases; use a
  disposable source projection that can be made unavailable after installation,
  rather than alter the actual checkout. Reuse lower-level evidence for semantics;
  prove only missing composition risks again at the installed boundary.
- Independent review probe: run the installed command independently from another
  cwd, inspect all helper/resource paths and repeat one preservation/failure case.
- Gate owner/stage: implementer owns final composition and aggregate gate after
  focused checks pass. Corrections run targeted evidence first; after successful
  correction the final fresh discovery owns any outstanding aggregate rerun.

## Verification

Verification-design recommendation: separate — cross-boundary composition,
native hard/advisory policy and guidance-only evidence require distinct oracles.

Before adding fixtures inspect `tests/test_maintainability.py`,
`tests/test_install_development_skills.py` and `tests/staging_fixture_support.py`.
Derive `verification.md`, then preflight. Run targeted cases, then the measurement
suite with the available pinned interpreter, then the installer suite. Final
composition must use real pinned analyzers; skips do not satisfy AC-03/AC-04.

The implementer runs `python3 tools/verify.py` after focused checks pass, and
the canonical architecture and contract commands before handoff:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
```

Applicable current aggregate evidence may cover these checks when it establishes
the same scope/policy. Report skips, failures and active-profile drift truthfully;
never repair drift by refreshing this invocation. Ask before live/networked or
expensive additional verification. No live model results are claimed.

## Execution and handoff

Status: `ready`
Task kind: `executable`

Guided profile. Brief prepared; execution prerequisites still required.
Readiness route: standalone guided preflight after derived `verification.md`,
then a ready `preflight.md`. Confirm both accepted predecessor outputs, actual
runtime paths, real analyzer availability and disposable isolation mechanism.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / foundation discovery and installed proof
```

### Execution sizing

- Sizing policy: `default@1`, active project-local `references/task-sizing.yaml`.
- Estimate: 15 agent calls; 40 implementation minutes. Confidence: medium.
- Policy result: fits; equality with a policy maximum is permitted.
- The estimate reuses predecessor tests and existing installer fixtures; it does
  not include T-005's full skill-driven review/correction journey or live evals.

### Stops and next action

- Stop for contradictory owner policy, required new registry/runner architecture,
  absent real-tool evidence, or verification that needs unapproved network/budget.
- Next: verification design, preflight, implementation. Publish commands, setup,
  inputs, outputs, skips and limits in `results.md` here. T-002 receives exact
  installed command/resource paths, settings/format contract and current evidence.
- After implementation or correction and applicable maintainability review and
  registry synchronization, immediately hand completed bytes to fresh independent
  `task-review-discovery`; hand its report to a separate `task-acceptance-review`.
  Preserve conditional stage order and stable findings. No parent implementation
  or parent acceptance stage substitutes for this final executable leaf.
