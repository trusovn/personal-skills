# Codex behavioral eval runner: possible future work

This document records ideas intentionally excluded from
`SC-EVAL-01`. It is not implementation authority and does not expand the MVP
brief.

The MVP succeeds when agents developing `task-implementation-flow` skills have
one discoverable command that stages portable fixtures and launches selected
evals against Codex with inspectable outputs.

## Evidence from initial use

The MVP has now been used for current-skill and baseline comparisons across
multiple `task-implementation-flow` skills. It successfully exposed prompt
leakage, invalid fixture oracles, missing output-contract fields, premature
broad gates, and runtime portability problems that static checks did not find.

The same use also exposed avoidable cost and evidence-quality gaps:

- interrupted or targeted follow-up work could not safely resume into an
  existing suite;
- agents repeated model-backed runs or fragmented one review across many output
  directories;
- missing baseline runs could still be summarized as proof that old behavior
  was rejected;
- undeclared `python` versus `python3` assumptions caused false blockers,
  inconsistent substitutions, and external `PATH` shims;
- source identity, effective model configuration, duration, and cost had to be
  reconstructed manually;
- buffered progress caused repeated empty polling while sequential suites ran;
  and
- semantic grading remained manual and did not produce the existing
  benchmark/viewer contract.

Use this evidence to prioritize freshness, invalid-run prevention, selective
reuse, and durable grading before adding more execution throughput.

## Near-term plan

Implement the near-term work as bounded follow-on tasks. Keep execution,
grading, and acceptance as separate responsibilities.

### 1. `SC-EVAL-02`: reliable, freshness-aware execution

#### Add a read-only eval doctor

Provide a preflight mode that performs no model-backed invocation. It should
validate selected evals, structured execution metadata, setup, resolved
workspaces, declared outputs, current and baseline skill paths, and output
directory state.

Flag:

- setup commands embedded in user prompts;
- absolute `/work` assumptions;
- unknown placeholders or paths escaping the run directory;
- unavailable declared runtime commands;
- current and baseline skills that are byte-identical;
- missing declared outputs or expectations that cannot be inspected from
  preserved evidence; and
- likely prompt-answer leakage.

Treat prompt-leakage and assertion-quality findings as warnings for human
judgment, not automatic failures. Prefer explicit runtime requirements over
parsing commands from prompt prose. Fixture setup must make required commands
portable; do not rely on session-local `PATH` shims.

#### Add a suite manifest, resume, and selective reruns

Persist one suite manifest with:

- selected eval IDs and configurations;
- current skill, baseline skill, eval-definition, and relevant fixture/setup
  digests;
- requested model and reasoning configuration plus effective values when they
  are observable;
- runner and Codex versions;
- per-eval/configuration state such as `pending`, `running`, `completed`,
  `failed`, `graded`, or `stale`; and
- start time, end time, and duration.

Support resuming a suite, rerunning only failed or explicitly selected rows,
and safely adding untouched rows to the same suite. Reuse a result only when
its complete freshness key still matches. Mark results stale when relevant
skill, eval, fixture, model, reasoning, or runner identity changes. Never
silently overwrite unknown or stale evidence.

#### Make comparison requirements explicit

Allow an eval or suite to declare that prior-behavior comparison is required.
When required, demand a baseline skill or an explicit recorded reason for
omitting it. A summary must not claim that old behavior was rejected without
matching baseline evidence.

Run baselines only for evals whose acceptance claims require comparison. This
preserves discrimination evidence without paying for unrelated baseline rows.

#### Capture cheap reproducibility evidence

Record source/configuration digests, Git identity when available, duration, and
output size without requiring another model call. Capture token usage when the
executor exposes it reliably. Keep full event transcripts and generated patch
files optional.

Flush suite and per-eval progress immediately, including elapsed time. This
does not reduce model tokens, but it avoids empty polling and makes long
sequential runs operable.

### 2. `SC-EVAL-03`: deterministic-first grading and review

Translate behavioral-runner results into the existing grader, benchmark
aggregator, and eval-viewer workspace contract.

Grade in this order:

1. deterministic checks for files, exact fields, Git paths, command ordering,
   hashes, and unchanged-state evidence;
2. one grouped semantic grading pass per eval only for expectations that
   genuinely require judgment; and
3. human or fresh acceptance review for consequential release decisions.

Produce durable `grading.json` evidence with the required `text`, `passed`, and
`evidence` fields, then support `aggregate_benchmark.py` and
`eval-viewer/generate_review.py` without manual directory reconstruction.
Never convert executor success or a model's self-claim into a passing grade.

### 3. `SC-EVAL-04`: small controlled concurrency

Add bounded parallel execution only after manifests, freshness checks,
resumability, and progress reporting are stable. Keep sequential execution as
the default and begin with a small explicit worker limit. Preserve isolated
workspaces, deterministic result paths, readable progress, approval behavior,
and aggregate failure reporting.

Concurrency reduces wall-clock time, not model-token cost. Do not use it to
mask invalid fixtures, weak expectations, or missing comparison evidence.

## Deferred work

### Migrate the remaining eval definitions

`bounded-task-implementer` and `task-acceptance-review` now use structured
execution metadata. `task-preflight` remains to be migrated; do it after
`SC-EVAL-02` so its evals inherit doctor, freshness, and resume behavior.
Continue to migrate incrementally rather than through a bulk schema rewrite.

### Add repetitions and variance reporting

Support multiple runs per configuration and feed their results into
`aggregate_benchmark.py` only when a narrow decision is sensitive to stochastic
variance. Keep one run as the default. Repetitions multiply model cost and do
not repair prompt leakage, invalid fixtures, or missing baselines.

### Capture expensive diagnostics on demand

Consider optional Codex JSONL events, fuller transcripts, generated patches,
and detailed environment metadata when a concrete debugging case needs them.
Do not make them mandatory suite output.

### Consider provider adapters

If the same behavioral workflow is needed for another agent runtime, extract a
small executor boundary after the second real provider exists. Do not design a
provider framework in advance.

### Promote the runner to repository-level tooling if ownership changes

Keep the runner under `skills/skill-creator/scripts/`. If it later serves CI or
non-skill workflows, consider moving testable CLI code to a repository
`tools/skill-eval/` package while leaving `skill-creator` as a consumer.

## Explicitly not a goal

The runner should not become an autonomous acceptance system. Skill behavior
can be subjective, fixtures can be incomplete, and model graders can ratify
the same misunderstanding as the executor. The durable division should remain:

- the runner executes and preserves evidence;
- deterministic checks establish objective facts;
- graders assess declared expectations; and
- a human or fresh acceptance reviewer owns consequential release decisions.
