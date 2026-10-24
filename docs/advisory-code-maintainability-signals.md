# Advisory: deterministic code maintainability signals

Date: 2026-10-23

This note proposes a shared maintainability feedback flow for repository setup,
task preparation, implementation, and independent review. It is a design note,
not an implementation plan, an acceptance decision, or active skill policy.
A standalone Python tooling experiment is now available through
[`scripts/measure_maintainability.py`](../scripts/measure_maintainability.py).
See the [setup and usage guide](../scripts/measure-maintainability.md) for local
measurements and baseline comparisons. Skill and workflow integration below
remains proposed; the experiment does not activate that policy.

## Purpose

Help agents produce code that a maintainer can locate, understand, test, and
change without learning unrelated implementation details. Give feedback before
and during implementation, rather than relying only on the final reviewer.

Use several explicit signals rather than one combined quality score.
Deterministic measurement does not make its interpretation objective: small
functions can be poorly designed, and necessary validation can contain many
branches.

Owner decisions, 2026-10-23: **new target breaches and every increase in a
selected maintainability metric for existing functions require a response,
including increases within targets.** Prefer an in-scope refactor that avoids
the increase. Retaining it requires concrete evidence that refactoring would
worsen the design or expand substantially beyond the current task. Flag these
tradeoffs for the independent reviewer to decide; an implementer's explanation
does not authorize an exception. A heuristic threshold alone does not reject
code. Existing hard correctness and architecture rules retain their separate
enforcement.

## What exists in this repository

| Existing asset | Actual capability | Missing capability |
|---|---|---|
| [`scripts/run_evidence.py`](../scripts/run_evidence.py), documented in [`scripts/run-evidence.md`](../scripts/run-evidence.md) | Captures implementation begin/finish snapshots; executes one supplied command and stores command, timing, exit status, stdout, and stderr | Does not choose checks, calculate metrics, interpret results, or compare before/after measurements |
| [`architecture-guardrails`](../skills/architecture-guardrails/SKILL.md), its [Python reference](../skills/architecture-guardrails/references/python.md), and [registry template](../skills/architecture-guardrails/templates/gates.yaml) | Defines how a target repository can install deliberate hard rules, baselines, and one discoverable command | Guidance and a template do not create an active gate in this repository |
| [`task-maintainability-review`](../skills/task-implementation-flow/task-maintainability-review/SKILL.md) | Requires semantic review and any applicable architecture gate; treats automated signals as investigation leads | No standard maintainability measurement/report contract shared with preparation and implementation |
| [`verification_runner.py`](../skills/task-orchestrator/scripts/verification_runner.py) | Constructs and executes authorized verification plans for the orchestrator | Does not define maintainability metrics or comparison policy; not a general prerequisite for standalone skills |
| [`check_contracts.py`](../skills/repo-foundation/scripts/check_contracts.py) | Validates the discovery contract registry and local references | Does not assess source-code maintainability |

At the initial inspection, no root `.quality/gates.yaml`, Python lint
configuration, or active shared complexity comparison command was found.
The standalone experiment now owns settings in `.quality/maintainability.toml`
and `.quality/ruff.toml`, with pinned tools in `.quality/requirements.txt`.
It supplies complete Radon comparisons and supplementary Ruff target diagnostics;
below-target statement/argument comparisons remain unavailable. No skill,
development-profile installer, or CI integration is included.
An import-direction checker exists as generated sample code in the
[maintainability eval fixture](../skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py).
It governs that disposable fixture, not this repository. `ruff` and `radon`
were not on the current shell's `PATH`; this does not establish their absence
from every virtual environment.

The existing command wrapper was exercised with:

```sh
PYTHONPATH=tests python3 -B -m unittest test_run_evidence.RunEvidenceTests.test_architecture_check_captures_raw_facts_without_interpretation -v
```

Result: one test passed. It launches a real Python child process, verifies both
output streams and exit status 7, and checks the saved command record. The
installed `.agents/scripts/` helper and its three shared dependencies had the
same bytes as their `scripts/` sources. This proves the tested recording path,
not a working maintainability checker or the complete evidence lifecycle.
The active installation was not refreshed.

## What good code means here

Numbers should help answer concrete maintenance questions:

| Goal | Evidence from the changed code |
|---|---|
| Easy to navigate | The behavior has a clear owner and entry point. Names identify purpose. A related change can be located without tracing unrelated helpers. |
| Easy to understand | Control flow, data shape, side effects, and important assumptions are explicit. A reader can explain the behavior without reconstructing hidden global state. |
| Easy to change | A small same-kind variant belongs near the current owner. It does not require synchronized policy edits across unrelated modules. |
| Easy to verify | Important deterministic logic and test scenarios have practical, repeatable observation boundaries. Tests express the scenario and expected effect clearly. |

During implementation and review, use one plausible maintenance question from
the task, such as adding a sibling validation case. Identify where it belongs,
which collaborators it needs, and what test would protect it. No speculative
feature implementation or fixed file-count limit is required. This is a focused
reading exercise, not proof that every future change will be easy.

Google's [review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
supports examining unnecessary complexity, naming, comments, and test clarity.
It also cautions against speculative generalization and blocking on personal
style preferences.

Research supports restraint in interpreting metrics. A
[2025 study](https://portal.findresearcher.sdu.dk/en/publications/early-career-developers-perceptions-of-code-understandability-a-s/)
with 216 early-career developers inspecting 12 Java classes found only modest
predictive power for cyclomatic and cognitive complexity, and no predictive
power for issue severity. A smaller
[2023 study](https://link.springer.com/article/10.1007/s10664-023-10396-7)
with three students performing maintenance on 32 methods reported prediction
errors around 30%. These studies do not establish Python-specific thresholds.
Our design inference is to use metrics for attention and comparison, then
require concrete semantic evidence for a design blocker.

## CRAP, complexity, and coverage

CRAP combines cyclomatic complexity and test coverage:

```text
CRAP = complexity² × (1 − coverage)³ + complexity
```

Coverage is a fraction from 0 to 1. The formula identifies complex code with
little test execution, but cannot assess assertion quality or design clarity.
For the initial experiment, prefer cyclomatic complexity and report coverage
separately when available. Missing coverage means unknown, not zero.

Coverage collection needs special care here: several tests launch Python child
processes. Parent-process coverage alone can misrepresent execution of scripts.
Coverage is not required for static complexity checks.

## Initial Python checks and target ownership

Start with per-function cyclomatic complexity and a small set of stable Ruff
rules. Radon provides the complete complexity inventory; Ruff contributes
selected lint findings. Avoid two competing cyclomatic-complexity policies:
use Radon for that comparison, or deliberately choose Ruff `C901` instead.
Do not compare scores from different analyzers as if they were equivalent.

Suggested starting targets, still subject to calibration:

| Signal | Proposed target | Initial treatment |
|---|---|---|
| Radon cyclomatic complexity | At most 10 per function | Measure all functions, including those below target; require a response to new breaches and every increase in existing functions |
| Ruff `PLR0915` statement count | At most 50 | Advisory diagnostic requiring a response when new or worsened; 50 is the documented tool default, not a research-derived optimum |
| Ruff `PLR0913` arguments | At most 5, with the tool's documented exemptions | Advisory diagnostic; keep explicit parameters when grouping them would hide the contract |

The [statement](https://docs.astral.sh/ruff/rules/too-many-statements/) and
[argument](https://docs.astral.sh/ruff/rules/too-many-arguments/) limits are
starting conventions. Tool counting rules matter: they are not interchangeable
with physical lines or a custom parameter count. The [Radon metric definition](https://radon.readthedocs.io/en/latest/intro.html)
and [Ruff C901 definition](https://docs.astral.sh/ruff/rules/complex-structure/)
also make the selected implementation part of the measurement identity.

Keep thresholds, rule selection, scope, and exception ownership in repository
policy, not copied into three skills. A possible home is
`.quality/maintainability.toml`, referring to native Ruff configuration for
Ruff-owned settings. Use an existing command registry, or `.quality/gates.yaml`
when useful, only to discover commands. Do not duplicate native rule values in
the registry. These paths are proposals, not files currently in use.

Source Python under `scripts/`, skill scripts, tests, evals, fixture generators,
and harness code belongs in the governed scope. Report implementation and test
assets separately. Exclude installed `.agents/` copies, vendored/generated
copies, and deliberately invalid samples through explicit policy; do not
silently exempt all tests or fixture infrastructure.

Additional checks should earn their cost:

| Signal | Why it may help | Candidate tooling | Treatment |
|---|---|---|---|
| Nesting depth / cognitive complexity | Exposes the context a reader must retain | Ruff/Pylint nesting checks; a separately evaluated cognitive-complexity tool | Later experiment; these are different measures |
| Local variables | Highlights substantial internal state | Selected Ruff/Pylint rules | Add only if useful beyond the initial checks |
| Duplicated code | Finds logic that may need coordinated changes | Pylint `R0801` | Advisory; preserve intentional independence |
| Type consistency | Makes data contracts explicit and detects incompatible uses | mypy | Candidate gate after scoped adoption |
| Dependency boundaries and cycles | Limits coupling and change propagation | Import Linter | Gate only deliberately chosen architecture rules |
| Unused code | Reduces unnecessary concepts and maintenance surface | Ruff; Vulture for broader detection | Confirm dynamic uses before removal |

Ruff [`PLR1702`](https://docs.astral.sh/ruff/rules/too-many-nested-blocks/)
is currently preview-only. Defer it in the initial stable profile; a nesting
experiment should opt into the specific rule and pin the tool version.
[Sonar's cognitive complexity](https://www.sonarsource.com/docs/CognitiveComplexity.pdf)
accounts for nesting as well as flow breaks; raw nesting depth is not an
equivalent implementation. Defer a cognitive-complexity dependency until it
adds useful evidence on representative Python changes.

Tool versions, selected rules, configuration, and exclusions must be explicit
for comparisons to be repeatable. Type-checking results also depend on
annotation coverage and configuration. Radon itself describes its aggregate
Maintainability Index as experimental; do not use it as the quality score.

## Interpreting cyclomatic complexity

A common starting target is at most 10 per function; there is no universal limit.
Radon ranks 1–5 as A, 6–10 as B, 11–20 as C, 21–30 as D, 31–40 as E, and 41+
as F. These ranks are tool guidance, not proof of defects.

Possible review prioritization, without adding more enforcement limits:

- Aim for 10 or less in new functions where practical.
- Review scores of 11–20 and explain why the decisions belong together.
- Above 20, consider simplification or document the reason to retain complexity.
- Above 40, prioritize a focused maintainability review.

These are proposed advisory thresholds, not adopted repository policy. File
averages can hide large hotspots. Do not split functions merely to lower
scores, replace clear arguments with opaque dictionaries, or add weak tests
to improve CRAP.

## New code and existing code

Compare individual functions and rule findings, not repository averages or
totals. One improved function cannot offset a regression elsewhere.

| Current condition | Required handling in the proposed flow |
|---|---|
| New function | Meet the current targets, or supply a bounded justification for each breach. This applies inside old files too. |
| Existing function within targets | Flag every increase in a selected metric. Prefer an in-scope refactor; being below target is not a justification to retain the increase. |
| Existing function already over target | Apply the same no-increase rule against its actual before value. Equal or lower values do not force unrelated cleanup. |
| Untouched legacy hotspot | Retain it as context; do not make it this task's cleanup obligation. |
| Metric unchanged but design worsened | Semantic review can still block on concrete naming, cohesion, coupling, locality, testability, or abstraction evidence. |
| Function moved, renamed, split, or extracted | Show the relationship explicitly. Do not claim old debt disappeared because its identifier changed or grant new helpers an inherited unlimited allowance. |
| Missing or incompatible measurement | Report unknown/incomplete. Do not turn missing evidence into a zero, a pass, or an invented baseline. |

For example, with a complexity target of 10: a new function at 13 needs a
response; existing functions moving from 6 to 8 or from 24 to 26 both require
refactoring consideration and reviewer resolution if the increase remains.
An unchanged value of 24 does not create a numerical regression.

Start with the smallest relevant refactor. Do not follow an expanding chain of
dependent refactors beyond the task's authority merely to reduce a metric.
If the local alternatives add indirection, scatter one responsibility, or
otherwise worsen maintenance, show that consequence. If avoiding the increase
requires a wider change, identify the affected boundary and additional scope.
Carry the unresolved increase and tradeoff to the reviewer for a decision;
scope pressure alone is not an implementer-approved waiver. Preserve the
requested behavior and its verification during any authorized refactor.

A justification identifies the symbol and rule, the before/after values where
available, the bounded refactoring alternatives considered, and the concrete
design harm or scope expansion that prevents a reasonable local correction.
Do not perform a harmful or out-of-scope refactor just to demonstrate the
problem. The independent reviewer accepts a bounded exception or reports an
actionable regression. Confirmed blockers retain the existing stable
`MNT-NN` identities.

A task baseline is an observation of input code, not a permanent permission to
retain debt. Keep it separate from reviewed policy exceptions. Normal checks
must not widen exclusions, rewrite targets, or regenerate accepted debt.
Any durable exception needs a narrow subject, reason, owner, and reconsideration
condition. Later tasks measure the improved current code, so removed debt
does not regain its old allowance.

## One runner and comparable reports

Provide one discoverable repository command with two operations: capture a
baseline, then measure and compare current code. It should run the default
named profile or an explicitly selected subset of check IDs. A shared helper
can support this command; avoid building a general scheduler, plugin framework,
or custom complexity analyzer.

Use existing analyzers. Keep collection/comparison separate from the raw
recording responsibility of `run_evidence.py`. When an implementation evidence
run is already active, its `check` operation can wrap the canonical command
once. Standalone preflight and review must also work without opening an
implementer evidence run.

Each report needs JSON for consumers and a short human summary. Record:

- Report format version, governed roots, exclusions, requested profile/checks,
  and the checks actually completed, failed, skipped, or unavailable.
- `HEAD`, dirty-state context, and identities of the actual analyzed files,
  including relevant untracked files. Preserve the baseline inputs or a
  resolvable snapshot reference. `HEAD` alone is insufficient for dirty work.
- Tool versions, effective native configuration and policy identities, exact
  commands, exit status, raw results, and measurement errors.
- Per-function location and qualified identity, values, target, before/after
  delta, and classification: new, improved, unchanged, worsened, or unmatched.
- Required-response items, implementation explanations, and links to any later
  reviewer dispositions. Keep measurement facts separate from explanations.

Path and qualified function name can identify an unchanged symbol; line number
is a location, not identity. Ambiguous moves, duplicate qualified names, and
split/merge relationships need explicit review rather than guessed matching.
Where a tool supplies only threshold diagnostics, do not invent a full numeric
inventory. The adapter must expose a tested comparable value or state the
comparison limit; equal diagnostic counts do not prove equal severity.
In particular, threshold-only Ruff output cannot prove the no-increase rule
below its limits. Complete enforcement of each selected metric needs values
on both sides of the threshold, from a suitable analyzer or tested adapter.
Until that exists, label those diagnostics as supplementary target checks and
the missing regression comparison as unavailable; do not claim complete policy
coverage. Radon's full complexity inventory supports the initial comparison.

The full selected scope should be measured for the initial small Python
profile; the task diff determines which findings require a response. A later
changed-file optimization must preserve cross-file checks and truthful scope.
The agent may request fewer checks for exploration, but cannot call a partial
run the complete required profile.

Compare only compatible tool/configuration/scope identities. A tool upgrade or
policy change requires deliberate remeasurement, not an apparent improvement.
Detect input changes during scanning, or analyze a stable read-only snapshot.
Concurrent changes must not be attributed to the implementation by inference.
Never reset or stash user work to obtain baseline code.

Use separate outcomes for measurement completeness, hard-rule results, and
advisory response items. A completed run with warnings is different from a
checker failure. Retain results from completed checks if another check fails;
missing required checks cannot produce an overall clean result. The exact CLI,
exit codes, and report schema remain implementation design work.

## Distribution across the workflow

| Owner | Required contribution when the repository adopts this flow |
|---|---|
| `repo-foundation` and `architecture-guardrails` | Establish command placement, governed scope, native configuration, selected profile, thresholds, and exception authority. Keep hard architectural rules distinct from heuristic response items. |
| `task-preflight` | Resolve the command and capture a cheap local baseline before edits; record report location, scope, capability gaps, and current applicability. This establishes input state, not implementation success. |
| `bounded-task-implementer` before edits | Read the baseline hotspots relevant to the task. Reuse it only if the analyzed inputs and policy still match. For direct requests without standalone preflight, capture it during compact self-preflight. |
| `bounded-task-implementer` during work and before handoff | Use focused feedback during editing; run the adopted profile on final code; address each new breach and every selected-metric increase in existing functions. Prefer bounded refactoring; flag retained increases with evidence of design harm or excessive scope for reviewer decision. Supply a brief navigation/readability explanation where the changed design needs one. |
| `task-maintainability-review` | Verify that before/after scope, inputs, tools, and policy are comparable and current; rerun missing or stale required checks when feasible. Inspect every required-response item and review the changed design even when all numbers are green. |

Do not require standalone preflight for direct edits solely to collect metrics.
Expected readiness/report file changes do not stale an unchanged source
baseline. Source, dependency, tool, or policy changes affecting a measurement
do require focused refresh before edits. A baseline captured after the first
implementation edit cannot be labeled the before state; use preserved exact
inputs or report that comparison as unavailable.

An unavailable adopted required check is an evidence gap with an owner. An
optional experimental check can remain unavailable with an explicit warning.
Preserve each skill's existing readiness, independence, and handoff boundaries;
the runner neither accepts its own output nor starts review stages. A
maintainability verdict still does not establish functional correctness.

Changes to the skills should be short consumption instructions linked to one
report/policy contract. Do not repeat the threshold table or tool manuals in
each skill. `AGENTS.md` should name the canonical command and response rule;
repository-native config should define the actual values.

## Smallest useful implementation and proof

The first delivery should support the initial Python profile, exact before/
after reports, required-response items, and the three workflow consumers. Keep
additional languages behind the same concepts: native analyzer, explicit
profile, comparable symbol/rule identity, and separate semantic interpretation.
Do not claim Python thresholds apply to TypeScript, Java, or other ecosystems.

Before implementation, settle the pending policy choices below and calibrate
the proposed targets on stable representative Python inputs. For calibration,
inspect alerts in both production and test/harness code; judge whether they
expose real maintenance costs. Do not choose limits merely to make the current
repository green, and do not refactor the concurrent orchestrator work as part
of tool adoption.

Use existing test infrastructure and fixture helpers where possible. Required
behavioral proof should include:

| Scenario | Observable evidence |
|---|---|
| New code and legacy comparison | Real snippets below, at, and above a target; increases in existing functions that remain below target; unchanged and worsened legacy hotspots; a new function in an existing file; independent improvements cannot cancel a regression |
| Change attribution | Line shifts, moved/renamed and extracted functions, and ambiguous identity retain accurate or explicitly unmatched results |
| Dirty inputs and freshness | Staged, unstaged, and untracked source is represented; stale or concurrently changed input is rejected or marked incomplete; the real index/worktree is preserved |
| Execution and scope | Default and selected checks run; missing tools, analyzer failure, and partial completion remain visible; exclusions do not silently hide code |
| Policy integrity | Changed tool/config/scope prevents false comparison; routine runs do not rewrite policy, exclusions, or accepted exceptions |
| Agent behavior | Preflight records the actual baseline; implementation considers a local refactor for an increase below target; design harm or excessive refactoring scope is flagged for reviewer decision; fresh review rejects unsupported excuses and can identify poor design despite green metrics |

Run actual analyzers against controlled snippets for measurement proof. A
schema check, matching phrase in a skill, or successful fake command alone
cannot prove this flow. Agent evaluations should also include a justified
complex function and a mechanical function split that worsens navigation, so
the flow rewards maintenance quality rather than smaller numbers. Live agent
evals are a separate, budgeted verification choice.

If implementation changes development-profile skills or shared helpers,
inspect [`scripts/install_development_skills.py`](../scripts/install_development_skills.py)
and synchronize `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
`SHARED_SCRIPT_FILES`, focused installer tests, and README installation
documentation as applicable. Preserve the installer's ownership boundary.
Do not refresh the active installation during a running invocation.

## Decisions still to settle

Calibrate the proposed 10/50/5 profile and explicitly decide whether test/harness
code needs any narrow exceptions. Different asset groups remain visible even
if targets are shared. Confirm which metrics have full inventories for the
no-increase comparison and which remain supplementary target checks.

The enforcement decisions are settled: flag every selected-metric increase in
existing functions, prefer bounded refactoring, and leave exceptions for design
harm or excessive scope to independent reviewer judgment. The exact runner
interface, report location, and format belong to the bounded implementation
design after the remaining calibration choices.

## Local experiment

Radon 6.0.1 was installed in a temporary virtual environment outside the
repository. Static analysis used copies of `scripts/*.py` and the staged Python
files under `skills/task-orchestrator/`. Project code was not executed. Methods
returned through multiple Radon paths were deduplicated; class aggregate scores
were excluded from the function summaries.

| Implementation file | Highest function complexity | Functions above 20 |
|---|---:|---:|
| `scripts/install_development_skills.py` | 21 | 1 |
| `scripts/ollama_delegate.py` | 30 | 1 |
| `scripts/run_evidence.py` | 17 | 0 |
| `scripts/runtime_context.py` | 18 | 0 |
| `scripts/workflow_version.py` | 10 | 0 |
| `skills/task-orchestrator/scripts/controller.py` | 91 | 7 |
| `skills/task-orchestrator/scripts/controller_state.py` | 88 | 6 |

Largest observed hotspots included `_load_inspection_authority` (91),
`validate_ledger` (88), `validate_actor_operations` (52), `_legacy_run_next` (51),
`inspect_run` (42), and `validate_command_execution_record` (42). The three staged
controller test files had maximum function scores of 16, 4, and 9 respectively;
test results should remain separate from implementation results.

These are historical snapshot observations. Concurrent work changed the index
during the experiment; the scan used the staged copies captured at its start.
Rerun against the intended revision before acting on these numbers. No full
baseline, functional verification, or independent maintainability verdict was
produced by this experiment.

## References

- [Radon ranks and commands](https://radon.readthedocs.io/en/latest/commandline.html)
- [Cyclomatic complexity limits](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-cyclomatic-complexity?view=visualstudio)
- [Ruff rules](https://docs.astral.sh/ruff/rules/)
- [Cognitive complexity definition](https://www.sonarsource.com/docs/CognitiveComplexity.pdf)
- [mypy and annotation requirements](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [Import Linter contracts](https://import-linter.readthedocs.io/en/stable/)
- [Pylint duplicate-code check](https://pylint.readthedocs.io/en/latest/user_guide/messages/refactor/duplicate-code.html)
- [Vulture limitations](https://github.com/jendrikseipp/vulture)
- [Coverage in child processes](https://coverage.readthedocs.io/en/latest/subprocess.html)
- [crap4py formula and limitations](https://github.com/sebassdc/crap4py)


The main policy is settled. Before implementation, I would resolve three choices and do one small tooling experiment.

1. **Choose the first measurement set.** Complexity, statement count, and argument count are the current candidates. Your strict rule needs actual before/after values—even below thresholds. First prove that the selected tools can supply those values reliably. Threshold-only warnings are insufficient.

2. **Calibrate the targets and scope.** Treat **10/50/5** as provisional. Inspect representative Python functions, tests, and harness code to see whether alerts identify useful maintenance concerns. I recommend including all those asset groups, reporting them separately, and excluding installed/generated copies explicitly.

3. **Define how retained increases reach a decision.** I recommend one required-response entry per affected function/metric: values, bounded refactoring alternatives, concrete design harm or scope expansion, and reviewer disposition. An unresolved entry must remain visible through handoff.

The rest can be routine implementation design:

- One canonical command, with baseline capture and comparison operations.
- Repository-owned configuration; shared tooling installed with the skills.
- JSON results plus a concise human summary.
- Baselines that preserve actual dirty/untracked source inputs.
- Explicit handling of renamed, moved, or split functions and unavailable checks.
- Short integration instructions in preflight, implementer, and maintainability review.

Before coding, turn those decisions into a bounded brief and behavioral verification cases. The important cases are below-target increases, unchanged legacy debt, stale baselines, missing tools, and refactors that lower numbers while worsening navigation.

**My recommended next step:** a small tooling experiment to establish which metrics can be collected completely. That resolves the largest technical uncertainty before committing to a runner design. `.quality/gates.yaml` can follow once there is a real command to register.


========

As a separate issues raised during such refactorings is naming issue. Likely the good place to handle
it is task-maintainability-review. Overall complex names is also a good indication that the design
isn't great.
Here's report from the agent on the issue:
Yes, but **standard linters mainly check naming conventions, not whether a name explains its purpose**. `_ledger_attempt_owners` is a weak name I introduced: it hides both the mapping direction and the validation it performs.

The function builds **attempt ID → task ID**, rejecting duplicate attempt IDs. A clearer version would be:

```python
def _map_attempt_ids_to_task_ids(ledger: dict[str, Any]) -> dict[str, str]:
    """Return the task ID for each attempt ID; reject duplicate attempt IDs."""
```

At the call site:

```python
task_id_by_attempt_id = _map_attempt_ids_to_task_ids(ledger)
```

That communicates more than `attempt_owners = _ledger_attempt_owners(ledger)`.

Available help falls into three groups:

| Approach | What it can assess |
|---|---|
| Ruff naming rules | Capitalization, naming conventions, `self`/`cls`, and similar consistency checks. [Rules](https://docs.astral.sh/ruff/rules/#pep8-naming-n) |
| Pylint naming configuration | Naming patterns and explicitly forbidden names such as `foo` or project-specific ambiguous terms. [Configuration](https://pylint.readthedocs.io/en/latest/user_guide/messages/convention/invalid-name.html), [forbidden names](https://pylint.pycqa.org/en/latest/messages/convention/disallowed-name.html) |
| Focused human or LLM review | Whether names communicate the actual responsibility, mapping direction, domain meaning, and important effects. This requires judgment and can still miss problems. |

For this experiment, I recommend adding a **signature-and-call-site readability check** to semantic review:

- Can the reviewer describe the function’s purpose without opening its body?
- Do collection names identify their contents and mapping direction?
- Does the name or short docstring disclose important rejection behavior?
- Did extraction create helpers whose purpose remains unclear outside the original function?

This is a concrete weakness in the result: the metrics showed smaller functions, but they did not establish clearer names. Adding more naming-style lint rules alone would not catch your example.