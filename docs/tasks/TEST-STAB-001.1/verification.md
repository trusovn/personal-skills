# Verification Design: TEST-STAB-001.1 — Assign clear test owners without changing evidence

Source brief: docs/tasks/TEST-STAB-001.1/brief.md
Source brief revision: SHA-256 `73471a7e4fdad30a72ee010b9936906f95227bec4a38f8267024efaaa568c100`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

The brief, its parent, root `AGENTS.md`, and the active project-local
`testing-discipline` govern this design. T-001/T-002 contracts, the cited plan
sections, and T-002.4 composition evidence supply preservation context. This
file specifies evidence for relocation only. It does not verify new role
behavior or close sibling tasks.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 — Ownership | V-01 | All ten permitted ownership rows, including mixed designer tests and three distinct fixture responsibilities. |
| AC-02 — Preservation | V-02, V-03 | Collection bijection plus unchanged assertions, scenario inputs, and actual boundary outcomes. |
| AC-03 — Execution | V-04 | Focused, isolated, and mapped aggregate runs; no import-order or cwd dependency. |
| AC-04 — Independence | V-05, V-06 | Copied/installed package execution and unchanged real installer ownership. |
| AC-05 — Scope | V-03, V-07 | Unchanged contracts and fixture semantics; retained parity guard and truthful evidence labels. |
| Ownership table — all ten rows | V-01, V-02, V-04 | Each responsibility has the required owner and runnable selector without duplication. |
| COMP-01–05 | V-02, V-03, V-07 | Preserve every existing composition record and its baseline assertions/probes; no new cross-task closure claim. |
| INV-CASE-01–24 | V-02, V-03, V-07 | Preserve each inherited case, its scenario selection and signal; registration is distinguished from executed probes. |

The brief has no separate finite-risk table. The final three rows map its finite
ownership and preservation inventories. FLOW-001/002/003, INV-001–011 and
ART-009 are preservation constraints, not instructions to qualify all planned
flow behavior in this leaf.

## Verification scenarios

### V-01 — Each responsibility has its specified owner

Covers: AC-01; ownership table — all ten rows

Intent: Reject cosmetic splitting that retains mixed owners, duplicates
cross-stage assertions, or leaves source-checkout dependencies in package tests.

Given:
- The brief's permitted ownership table and the original two modules are
  available, including each test's resource and guide dependencies.

When:
- Inspect the relocated tests, remaining designer suite, and `tests/README.md`.

Then:
- Designer-local tests cover only their own package and resolve it from their
  file location. Preflight, implementer, preparation, acceptance, discovery,
  senior-review, flow-guide, and composition checks have the repository owners
  named in the brief.
- Export/consumer, uncertainty/mixed-context, and known-issue/repeated-review
  fixture responsibilities have three separate repository modules, with their
  chosen names recorded in the evidence map.
- Both specifically identified mixed designer tests move to repository
  preparation/guide ownership. Genuine cross-stage assertions stay together.
- Each module has one stated purpose; the navigation guide records owner,
  purpose, fixture dependency, and focused/aggregate commands.
- Any emptied original module is removed; no forwarding test class remains.

Oracle / boundary:
- Compare actual test dependencies and locations with all ten ownership rows,
  the navigation guide, and the V-02 executed collection map. File size or
  class names alone cannot establish ownership.

Variants:
- All ten ownership rows; the two mixed designer tests explicitly named in the
  brief; each of the three fixture domains.

### V-02 — Baseline evidence maps once to executed post-move evidence

Covers: AC-02; ownership table — all ten rows; COMP-01–05; INV-CASE-01–24

Intent: Reject a green result obtained by dropping a test, discovering it twice,
or retaining its method while losing an input or assertion.

Given:
- Before test edits, the brief's three sequential baseline commands pass.
- Actual `unittest` collection identifies the original tests. The baseline
  inventory also records scenario selections, subtest distinctions, and
  boundary probes rather than relying on historical or AST method counts.

When:
- Collect and execute the mapped post-move union plus the remaining designer
  suite; compare that evidence with the baseline and new leaf `results.md` map.

Then:
- Each original test maps to exactly one collected post-move test, including
  every original scenario/subtest distinction and boundary probe.
- Assertions, supplied inputs, and expected failure signals are unchanged;
  only imports, paths, and class organization needed for relocation differ.
- No added skip, duplicate discovery, decisive-boundary mock, or relaxed
  expected failure accounts for success. Setup/assertion consolidation is
  deferred to .2.
- The new evidence map identifies old and new owners/selectors and reconciles
  collected totals with actual run results.

Oracle / boundary:
- A bijection between actual collected test identities, supported by the
  assertion/input comparison and executed scenario/subtest evidence. Equal
  counts, AST counts, or a passing aggregate without the map are insufficient.

Variants:
- Every baseline test and its scenario/subtest inputs in both original modules;
  every existing COMP-01–05 and INV-CASE-01–24 assertion.

### V-03 — Relocated fixtures retain contrasting boundary signals

Covers: AC-02, AC-05; COMP-01–05; INV-CASE-01–24

Intent: Reject preserved text or registrations that conceal a lost subprocess,
weakened negative control, or changed Git/filesystem observation.

Given:
- Existing fixture programs and eval inputs remain unchanged.
- The V-02 baseline records which tests actually invoke fixtures or public
  probes and which only inspect text, metadata, or registration.

When:
- Run the mapped tests with their original setup and scenario inputs, exercising
  each originally crossed process, filesystem, validator, and Git boundary.

Then:
- Actual fixture outcomes match the baseline, including destructive/mitigated
  export state, consumer-contract contrasts, uncertainty and mixed-context
  inputs, and known-issue/repeated-review facts.
- The late-omission validator accepts the valid case in both fixtures. The
  clean fixture rejects boolean revision, older active attempt, and a second
  running task with exit 2. The fail fixture accepts boolean revision with
  exit 0 while still rejecting the other two invalid cases with exit 2.
- Existing index/worktree distinctions, discovery scenario/role checks, and
  composition/inherited-case assertions retain their original signals.

Oracle / boundary:
- Compare real probe exit results, generated records, persisted file contents,
  and Git observations with their unchanged baseline expectations. Preserve
  the full mapped evidence set; the validator contrast above does not replace
  other probes. Metadata/text assertions retain their narrower evidence label.

Variants:
- All baseline fixture scenarios and public probes, including both
  late-omission variants and all four validator inputs per variant.

### V-04 — Documented selectors work independently and as the mapped union

Covers: AC-03; ownership table — all ten rows

Intent: Reject tests that pass only after another module has modified import
state, selected the source root, or initialized shared mutable state.

Given:
- V-01 records every owner, including the three chosen fixture-module names.
- The navigation guide supplies focused commands and an aggregate covering the
  exact mapped union plus the remaining designer suite.

When:
- Run each owning module alone in a fresh invocation through its documented
  selector. Exercise supported invocation from an unrelated working directory
  with explicit paths or documented configuration, without a previous test's
  cwd/import/state setup.
- After focused checks pass, run the documented mapped union plus remaining
  designer suite, then the existing installer suite, sequentially.

Then:
- All mapped tests pass both alone and in the union, with collection matching
  V-02 and no order-dependent imports or results.
- Documented commands resolve actual owners and require no inherited cwd or
  mutable state from another test. Required cwd/configuration is explicit.
- Results record commands, collected totals, and actual pass/fail outcomes.

Oracle / boundary:
- Fresh Python/unittest process results and their collected test identities;
  documentation inspection alone cannot prove command executability.

Variants:
- Every owning module alone; documented focused selectors and aggregate;
  unrelated starting cwd with explicit invocation configuration.

### V-05 — Copied or installed packages execute without repository helpers

Covers: AC-04

Intent: Reject package tests or eval setup programs that import successfully
only because the source checkout or a repository-test helper is available.

Given:
- A disposable copy or committed-target installation contains the remaining
  designer package and the discovery/acceptance eval packages.
- Package invocations have no source-tree or repository-test-helper fallback;
  fixture work roots are disposable and explicitly supplied.

When:
- Run the entire remaining designer-local suite from that package.
- Invoke each discovery/acceptance setup scenario used by the mapped baseline
  through the copied/installed package's own setup entry point.

Then:
- The designer suite collects its complete expected inventory and passes using
  only its own package resources.
- Discovery and acceptance setups execute independently, with no repository
  helper dependency, and stage the same scenario inputs and decisive fixture
  facts checked by the mapped baseline.

Oracle / boundary:
- Actual Python processes using the disposable package paths, collected
  designer tests, and generated workspace facts. Installer byte projection or
  successful import alone does not prove these executions.

Variants:
- Remaining designer suite; discovery setup; acceptance setup. Use the existing
  baseline scenario selections, without new eval cases or agent calls.

### V-06 — Installation selection and unmanaged preservation stay intact

Covers: AC-04

Intent: Reject relocation that changes shipped package selection or installer
ownership, even if repository tests pass.

Given:
- Existing committed disposable installer fixtures contain their established
  managed and unmanaged files and pre-existing `AGENTS.md` text.

When:
- Run the unchanged installer suite after the mapped tests pass, including
  initial installation and rerun with its existing stale-managed contrasts.

Then:
- The selected skills, guide, shared scripts, package byte projection, and
  managed `AGENTS.md` block retain their existing expected behavior.
- Existing unmanaged skills, helpers, target files, and surrounding agent text
  remain preserved; stale managed files are handled as before.
- The installer and active `.agents/` installation are not changed by this leaf.

Oracle / boundary:
- Existing real installer process and disposable Git/filesystem assertions,
  plus scoped source/active-installation comparison. This proves installation
  projection and ownership, not role compliance.

Variants:
- The unchanged installer suite's initial-installation, rerun, and preservation
  cases; no unfinished T-004 unborn/drift behavior.

### V-07 — Scope and evidence labels remain truthful

Covers: AC-05; COMP-01–05; INV-CASE-01–24

Intent: Reject a relocation that silently changes contracts, removes the parity
guard, or reports constructed qualification inputs as observed role behavior.

Given:
- The pre-edit sources and existing T-002.4 composition records are available
  for comparison, alongside the new navigation guide and leaf evidence map.

When:
- Inspect the scoped diff and the labels attached to relocated tests and results.

Then:
- Changes stay within the brief's allowed test/support/documentation/evidence
  surfaces. Source guidance, eval programs/JSON, input meaning, expected
  verdicts, policy allow/deny values, COMP-01–05, INV-CASE-01–24, installer,
  shared scripts, plans, historical artifacts, and active `.agents/` stay
  unchanged.
- The inherited source-parity guard retains its assertions and collection;
  its evidence is labeled structural protection, not behavioral equivalence.
- Text checks, fixture runtime, installation projection, and unrun role behavior
  remain distinct. T-005 unrun labels remain intact; no actual role compliance
  or installed-flow qualification is claimed from local tests.

Oracle / boundary:
- Pre/post file and assertion comparison, actual V-02 collection of the parity
  guard, and inspection of guide/results evidence labels against unchanged
  composition metadata. This is scope/structural evidence, not agent behavior.

Variants:
- All five composition records, all 24 inherited cases, and every existing
  T-005 unrun boundary.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. `ready` here means design complete, not ready implementation entry
  or accepted implementation.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Obtain the required standalone preflight. It confirms accepted T-002.4 and
  current applicability, resolves exact post-move selectors and the three
  permitted fixture names, and confirms the disposable copied-package check.
- Implement the smallest test/support/doc relocation that satisfies the brief
  and exercises these scenarios. No fabricated red regression is required;
  preserve the passing baseline and its assertion/boundary evidence.
- Concrete test structure, framework usage, helpers, and file placement remain
  implementation choices except where the brief fixes ownership. Reuse the
  existing committed installer fixtures; do not refresh active `.agents/`.
- If a scenario cannot be exercised at its stated boundary, route the conflict
  to task design/preflight rather than weakening its oracle. Stop on a red
  baseline, ambiguous ownership, or the other brief-defined stop conditions.
- Use only the brief-authorized local gates. Do not expand to whole-repository,
  live-network, T-005 agent/model-budget checks, or sibling integration work.
- After implementation, follow the brief's applicable conditional stages,
  fresh independent discovery, and separate fresh acceptance decision.
