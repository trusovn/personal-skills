---
name: architecture-guardrails
description: >
  Use when a repository needs new or repaired deterministic architecture/maintainability guardrails:
  dependency-direction rules, forbidden imports, cycle/boundary checks, a canonical architecture
  command, legacy no-regression baselines, or a short agent-facing maintainability contract. Usually
  invoked during repo-foundation materialization or an explicit foundation change. Encode existing or
  deliberately chosen invariants; do not redesign product architecture or turn heuristic
  size/complexity metrics into universal hard failures.
---
# Architecture Guardrails

Establish the **smallest trustworthy executable maintainability boundary** for a repository.

The goal is not to prove that the architecture is good. The goal is to make a few important,
low-ambiguity architecture regressions mechanically difficult to introduce, and to give a focused
maintainability reviewer compact evidence for the semantic questions machines cannot decide reliably.

## Core contract

Optimize for:

- **cohesion** — changed modules keep a clear responsibility
- **low coupling** — components know only what they need
- **explicit dependencies** — important collaborators and boundaries are visible
- **localized change** — normal feature variation stays near the owning subsystem
- **testability** — important logic can be verified without unnecessary external infrastructure
- **proportionate abstraction** — introduce a layer/interface only for a concrete boundary, variation,
  dependency inversion, or test seam

Do not use these words as a substitute for executable repo-specific rules.

## Ownership boundary

This skill owns:

- identifying architecture invariants suitable for deterministic enforcement
- separating hard failures from advisory maintainability signals
- selecting the lightest repo/ecosystem-native enforcement mechanism
- clean vs no-regression/baseline semantics
- proving that representative hard rules can actually fail
- defining the canonical architecture-check capability and reviewer handoff evidence

`repo-foundation` owns:

- where configs/tests/wrappers live in this repository
- how the canonical command is exposed
- repo-local agent instructions and architecture/project maps
- CI integration and command discoverability
- avoiding duplicate sources of truth

Do not create or move product architecture merely to make an enforcement tool convenient.

## Inputs

Read, when present:

- root/scoped `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`
- `docs/foundation-plan.md` and `docs/project-charter.md`
- project/architecture maps and accepted ADRs
- module/package docs that state boundaries
- package/build/task-runner configuration
- existing lint/static-analysis/architecture tooling
- CI configuration
- current git status/diff

If the task came from `repo-foundation`, stay inside the authorized foundation scope.

## Outputs

Materialize or repair only what is useful for the target repo:

1. **Canonical architecture command** using the repo's existing command surface, for example:
   - `npm run check:architecture`
   - `make architecture-check`
   - `just architecture-check`
   - a Gradle/Maven architecture-test target
   - a filtered `dotnet test` architecture target

2. **Native architecture policy/tests** in the ecosystem-appropriate place.

3. **Optional compact gate registry** such as `.quality/gates.yaml` when automated/cheap agents would
   otherwise have to rediscover commands. Reuse an existing machine-readable command registry when one
   already exists.

4. **Explicit baseline/exceptions** only when existing debt prevents clean enforcement.

5. **Short repo-local implementation contract**, routed through `repo-foundation` into the existing
   agent instructions rather than duplicated across tasks.

6. **Verification evidence**, including a passing current-tree run and representative hard-failure
   sentinel evidence when safely feasible.

## Protocol

### 1. Discover architecture reality before rules

Identify only boundaries supported by current authority or clearly established code structure.

For each candidate invariant record:

- evidence path / authority
- what dependency or boundary behavior is allowed
- what concrete regression would be prohibited
- whether the rule can be checked deterministically with low ambiguity
- whether current code already violates it

Do **not** infer that a repo must use domain/application/infrastructure layers merely because that is a
familiar architecture. Do not create interfaces, folders, or modules just to give the checker something
to enforce.

If the repository has no meaningful stable boundary yet, prefer documentation plus semantic review or
`DEFER` over invented deterministic policy.

### 2. Classify repository enforcement mode

Use one of these conceptual modes; map to native tooling as appropriate.

#### `CLEAN`

Use when the intended hard invariants already hold across the governed scope.

- current violations: zero
- any future hard violation: fail
- no baseline is needed

#### `NO_REGRESSION`

Use when legitimate existing debt would make immediate clean enforcement disproportionate.

- capture only the known existing violations necessary to activate the rule
- unchanged existing debt: tolerated and visible
- removed debt: stays removed
- new or expanded hard violations: fail
- baseline refresh is **not** a feature-work fix

A baseline is a temporary compatibility boundary, not evidence that the violation is acceptable.

If the native tool has first-class known-violation/baseline support, prefer it. Otherwise use exact
native exclusions or a small repo-owned comparison wrapper. Avoid wildcard exceptions that suppress
future violations you have not observed.

See `references/enforcement-model.md`.

### 3. Split hard rules from advisory signals

#### Hard deterministic rule

Make a rule blocking only when all are true:

1. the invariant is authoritative or an explicit foundation decision;
2. violation has a concrete maintainability/architecture consequence;
3. the checker can detect it deterministically with acceptably low false positives;
4. the repo can explain what a developer should do when it fails.

Common candidates, **only when applicable**:

- forbidden dependency direction between declared layers/modules
- production code importing test-only/private implementation areas
- prohibited cross-domain/package dependency
- direct access to a protected internal module from outside its public boundary
- dependency cycles in a scope where cycles are explicitly prohibited

#### Advisory signal

Use warnings or reviewer evidence for ambiguous smells such as:

- large file/function growth
- cyclomatic/cognitive complexity
- dependency fan-out
- generic `utils` / `helpers` / `manager` accumulation
- broad constructor/service dependency surface
- growing conditional dispatch
- duplicated business/domain rules
- suspected god module / mixed responsibilities

Do not turn a heuristic threshold into a hard design verdict merely because a tool supports `max-lines`
or `complexity`. The semantic reviewer decides whether the signal corresponds to a concrete regression.

Implementation agents MUST NOT treat advisory architecture warnings as required changes unless a bounded
architecture-review step explicitly promotes them to blocking findings.

### 4. Choose the lightest enforcement mechanism

Preference order:

1. existing repo-native architecture/static rules that already express the invariant
2. existing linter/compiler/test framework with a precise rule
3. small ecosystem architecture tool
4. small repo-owned check only when existing tools cannot express the important invariant cheaply

Do not build a general dependency analyzer inside the repo.

Read the matching reference only when relevant:

- JavaScript / TypeScript: `references/javascript-typescript.md`
- Python: `references/python.md`
- Java: `references/java.md`
- .NET: `references/dotnet.md`

For mixed/monorepos, use the fewest mechanisms that cover real boundaries. A root command may compose
package-native checks without forcing every package onto one tool.

### 5. Expose one stable repo command

Cheap implementation/review agents should need to remember **one command**, not tool syntax.

Fit the command into the existing task runner/package/build convention. Do not introduce Make/Just/npm
only for this gate if the repo already has a different command surface.

The direct architecture command must remain runnable even if the repo's aggregate `verify`/`check`
command also includes it.

Document:

- canonical command
- governed scope
- policy/config/test path
- mode: `CLEAN` / `NO_REGRESSION` or equivalent native wording
- baseline/exception path when present

### 6. Add compact machine-readable discovery only when useful

If automated or low-capability agents benefit and no equivalent registry exists, merge a small
`.quality/gates.yaml` using `templates/gates.yaml` as a shape guide.

This registry is **command discovery**, not the architecture policy language. Keep dependency rules in
the native config/tests. When guardrails are being installed specifically to support low-capability
implementation agents, default the semantic review entry to `task-maintainability-review` and mark it required; disable
that stage only by an explicit repo decision.

Do not create the file for a tiny repo merely for ceremony.

### 7. Persist the short implementation contract

Route this compact contract through `repo-foundation` into the repo's existing agent instructions:

```text
Maintainability:
- Keep each changed module focused on one clear responsibility.
- Keep changes local to the owning subsystem; avoid unrelated edits.
- Keep dependencies explicit and narrow; business logic should not reach through unrelated infrastructure or global state.
- Keep important logic testable without external I/O where practical.
- Prefer existing patterns; add abstraction only for a concrete boundary, variation, or test seam.
- Before handoff, run <canonical architecture command>. Fix hard failures. Leave advisory warnings for the architecture-review stage.
```

Adapt vocabulary to the actual repo. Detailed policy belongs in executable rules, architecture docs, and `task-maintainability-review`.

### 8. Handle legacy baselines safely

When `NO_REGRESSION` is required:

1. run the intended hard rules without suppression and record the exact existing violations;
2. inspect them enough to confirm they are real pre-existing debt, not bad configuration;
3. encode the narrowest native baseline/exceptions;
4. add a **non-mutating baseline-freshness check** to the canonical command. It must fail when an
   exception/baseline entry no longer matches a present violation; it may inspect or generate a
   temporary candidate, but it must not rewrite the tracked baseline;
5. rerun and require success;
6. prove this regression sequence in a safe fixture/worktree: baseline one exact forbidden edge;
   remove that edge and verify freshness fails because the baseline must shrink; make the reviewed
   shrink; then reintroduce the same edge and verify the ordinary gate fails;
7. prove a **new** representative violation still fails;
8. document where the baseline lives and who/what is allowed to update it.

Run freshness before the normal ignored-known-violations check. Otherwise an ignored entry can keep
masking the exact edge after it was removed and later reintroduced. Treat a required baseline shrink
as a focused, reviewed architecture change, never as an automatic side effect of feature verification.

Never:

- auto-regenerate a baseline as part of the ordinary architecture command
- allow a feature agent to make the gate green by widening an ignore pattern
- treat baseline growth as routine maintenance

A baseline change is itself an architecture/foundation change and should receive focused review.

### 9. Prove the gate can fail

A green current-tree run is necessary but insufficient.

For at least one representative high-value hard rule, prove the checker rejects a prohibited case when
safe and proportionate. Preferred methods:

1. tool/config unit fixture already provided by the repo;
2. disposable temporary fixture outside production paths;
3. disposable branch/worktree or controlled temporary source mutation with exact restoration.

Never risk unrelated dirty/user work merely to create a sentinel.

Record:

- rule exercised
- expected failure
- observed non-zero/failing result
- cleanup/restoration evidence
- final clean architecture-gate result
- final git status/diff showing only intended foundation changes

If sentinel proof is unsafe or technically disproportionate, state `NOT_PROVEN` and why; do not fake
evidence.

### 10. Integrate CI without creating a second policy

When CI is part of the authorized foundation:

- CI invokes the same canonical repo command used locally
- do not re-express dependency rules in CI YAML
- keep architecture failure output actionable
- do not make advisory warnings fail CI unless the project explicitly promotes that signal to a hard invariant

### 11. Handoff to readiness/task flow

Report a compact contract another agent can consume:

```text
ARCHITECTURE_GATE
command: <canonical command>
mode: CLEAN | NO_REGRESSION
policy: <native config/test paths>
baseline: <path or NONE>
hard_rules: <short IDs/names>
advisory_signals: <sources or NONE>
sentinel: PASS | NOT_PROVEN (<reason>)
agent_contract: <path containing the short contract>
```

Do not require future implementation agents to reread this entire skill.

## Tool references

These are starting points, not mandatory dependencies:

- JavaScript / TypeScript: dependency-cruiser or already-installed ESLint boundary rules
- Python: Import Linter or existing equivalent import policy
- Java: ArchUnit architecture tests
- .NET: ArchUnitNET architecture tests

Use current repo-compatible versions; do not pin a version merely because this skill names the tool.
Initiate pros and cons discussion with the user if there are material tradeoffs for the tool candidates.

## Definition of Done

- Hard rules encode real current/decided architecture invariants, not generic architecture fashion.
- One canonical architecture command is discoverable and runs successfully on the intended current tree.
- Hard failures and advisory signals are clearly separated.
- Existing debt uses explicit no-regression handling when clean enforcement would require unrelated refactoring.
- The canonical no-regression command includes a non-mutating baseline-freshness check, so a fixed
  exact violation cannot return under its old exception.
- Baseline/exception widening cannot happen silently inside normal feature verification.
- A representative hard failure has been proven to fail when safely feasible, with restoration evidence.
- The repo-local implementation-agent contract stays short.
- CI, when used, invokes the same canonical command rather than duplicating policy.
- The gate is ready to provide evidence to `task-maintainability-review`.

## Anti-patterns

- Adding Clean Architecture/layers to a repo that did not choose them.
- Failing every file over an arbitrary line count.
- Requiring an interface for every class or an abstraction for every dependency.
- Splitting a god file mechanically into equally coupled mini-files to satisfy metrics.
- Adding a large custom analyzer when a small native rule works.
- Treating warnings as architecture verdicts.
- Baseline-everything / wildcard ignore rules.
- Auto-refreshing known violations on every run.
- A gate that only proves syntax/lint style while claiming architecture coverage.
- A gate that has never been shown capable of rejecting a prohibited case.
- Duplicating the same policy in config, CI, AGENTS, and architecture docs.
