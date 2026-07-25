# Task Brief: `SC-EVAL-01` — add a Codex behavioral eval runner MVP

Status: `ready`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 25-35 tool calls / one implementation session / 60k context
```

## Readiness route

`implementer self-preflight`

## Outcome

Add one small Codex-only runner to `skill-creator` that can launch selected
artifact-producing skill evals, with an optional baseline, from structured
`evals.json` setup metadata and leave enough evidence for a later agent to
inspect the run.

The `task-brief-designer` eval set is the pilot. The runner launches evals; it
does not decide whether semantic expectations pass.

## Why this MVP

Recent `task-preflight` and `task-brief-designer` work repeatedly had to
reconstruct the same sequence manually: stage a fixture outside the read-only
`/work` root, invoke `codex exec`, preserve the generated repository, and run
the same case against an older skill when discrimination mattered. Static JSON,
syntax, and fixture checks could not establish skill behavior, while manual
Codex runs found material defects.

The repository already owns eval schemas, grading guidance, aggregation, and a
viewer under `skills/skill-creator/`. The missing boundary is a discoverable
Codex executor. Keep that executor with `skill-creator`; keep scenario-specific
fixtures and expectations with each evaluated skill.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | This brief, derived from the user's 2026-07-23 request and the current repository's repeated eval-launch failures |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Owning skill | `skills/skill-creator/` |
| Pilot skill | `skills/task-implementation-flow/task-brief-designer/` |
| Allowed changes | `skills/skill-creator/SKILL.md`; `skills/skill-creator/references/schemas.md`; new `skills/skill-creator/scripts/run_behavior_evals.py`; new tests under `skills/skill-creator/tests/`; `skills/task-implementation-flow/task-brief-designer/evals/evals.json` |
| Read-only context | Existing `skill-creator` scripts, grader/viewer contracts, the pilot fixture script, and `skills/skill-creator/docs/codex-behavioral-eval-runner-future-work.md` |
| Out of scope | Migrating other skills, automated semantic grading, benchmark/viewer integration, parallel execution, repetitions or variance analysis, resume/retry orchestration, multi-provider support, full Codex transcripts, token/timing metrics, skill hashing, CI integration, and changes to task-implementation-flow skill behavior |
| Dependencies | Local `python3`, `git`, and `codex` commands; live Codex execution remains approval-gated |

Preserve unrelated work. Do not change installed or active skill copies outside
the canonical repository paths.

## MVP command and behavior

Expose one documented command shaped like:

```bash
python3 skills/skill-creator/scripts/run_behavior_evals.py \
  skills/task-implementation-flow/task-brief-designer \
  --ids 1,4,5 \
  --baseline-skill <optional-path> \
  --output-dir <optional-path>
```

Required CLI behavior:

- The positional path is the current skill under test.
- `--ids` selects comma-separated eval IDs; omission runs all defined evals.
- `--baseline-skill` is optional. When supplied, run the same selected evals
  against that skill in separate fresh workspaces.
- `--output-dir` is optional. Without it, create a unique directory under the
  system temporary directory and print its absolute path.
- Optional `--model` and `--reasoning` values may be forwarded to `codex exec`.
  When omitted, use the user's configured Codex defaults.
- Run sequentially. Continue after an individual eval failure, summarize all
  results, and exit nonzero when any requested run failed to launch or
  complete.

Do not add provider abstraction, concurrency, automatic retries, or a general
workflow engine.

## Structured eval setup

Extend the existing eval schema with an optional `execution` object:

```json
{
  "id": 1,
  "prompt": "The user task only; no fixture-launch instruction.",
  "execution": {
    "setup": {
      "command": [
        "python3",
        "evals/files/setup_fixture.py",
        "queue-runner"
      ],
      "cwd": ".",
      "env": {
        "EVAL_WORK_ROOT": "{run_root}/work"
      }
    },
    "workspace": "{run_root}/work/queue-runner"
  }
}
```

Contract:

- `command` is an argument array, not a shell string.
- `cwd` is relative to the positional/current skill directory and defaults to
  `.`.
- `env` permits literal values plus the single `{run_root}` placeholder.
- `workspace` is required when `setup` is present and must resolve inside
  `{run_root}`.
- Without `execution`, use a fresh empty workspace and allow Codex to run
  without requiring an existing Git repository.
- Reject unknown placeholders, paths escaping the run directory, missing
  commands, and setup commands that exit nonzero before invoking Codex.
- Setup is harness behavior. Remove setup commands and `/work` paths from the
  pilot's user-facing prompts rather than parsing or rewriting prompt prose.

Do not create a larger fixture DSL.

## Run isolation and evidence

For every eval/configuration pair:

1. Create a fresh run directory.
2. Load eval metadata and run setup from the positional/current skill for both
   current and baseline configurations.
3. Run the declared setup with `{run_root}` resolved.
4. Invoke a fresh, ephemeral `codex exec` process in the resolved workspace.
5. Instruct Codex to read either the current or requested baseline `SKILL.md`
   and then execute the eval's task prompt. Keep that skill path outside the
   writable eval workspace.
6. Preserve the workspace after completion.

Keep the evidence bundle small:

```text
<output-dir>/
  current/eval-<id>/
    work/                  # staged repo and generated artifacts
    effective-prompt.txt
    final-response.txt
    result.json
    stderr.txt             # only when non-empty
  baseline/eval-<id>/      # only when requested
    ...
```

`result.json` needs only:

- eval ID and configuration (`current` or `baseline`);
- requested model/reasoning values, or `null` when defaults were used;
- setup and Codex exit codes;
- resolved workspace path;
- Git status paths after the run when the workspace is a Git repository; and
- a short error string when setup or Codex failed.

The effective prompt, final response, preserved workspace, and exit result are
enough for MVP inspection. Do not add a full JSONL transcript, timing/token
capture, source hashes, automatic patch files, or grading output.

## `skill-creator` workflow update

Update `skills/skill-creator/SKILL.md` narrowly:

- Distinguish trigger-description evaluation (`scripts/run_eval.py`) from
  behavioral execution (`scripts/run_behavior_evals.py`).
- Use the new runner for Codex-backed artifact evals with structured execution
  metadata.
- Show the command before a live/model-backed run and obtain approval when the
  run is not already authorized.
- State that a successful process exit is execution evidence, not an
  expectation grade or acceptance verdict.
- Keep existing grader, aggregation, viewer, and human-review guidance. Do not
  claim the MVP automatically produces their complete workspace contract.

## Pilot migration

Update all five `task-brief-designer` eval entries:

- Keep their task intent, expected outputs, and expectations unchanged.
- Move fixture setup out of prompts for evals 1, 2, 4, and 5 into `execution`.
- Use the fixture directories currently produced by `setup_fixture.py`:
  `queue-runner`, `verification-runner`, `api`, and `evidence-flow`.
- Leave eval 3 without setup so it runs in a fresh empty workspace.
- Do not change `setup_fixture.py` or task-brief-designer skill instructions in
  this task.

## Work and acceptance criteria

Required work:

1. Document the optional execution schema.
2. Implement the Codex-only sequential runner and minimal result bundle.
3. Add focused tests using a fake `codex` executable; unit tests must not call
   a live model.
4. Migrate the five pilot eval definitions.
5. Make the runner discoverable from `skill-creator/SKILL.md`.

- **AC-01 — one command launches a real eval.** Given the pilot skill and a
  selected configured eval, the runner stages its fixture under a writable
  unique run root and invokes Codex in the declared workspace without relying
  on `/work`.
- **AC-02 — prompts remain task prompts.** Setup is executed by the harness;
  the effective Codex prompt contains the eval task unchanged inside only the
  minimal instruction to load the selected skill.
- **AC-03 — runs are isolated.** Current and optional baseline runs use
  separate workspaces, use the same current eval/setup definition, and neither
  modifies either skill source or the user's repository worktree.
- **AC-04 — evidence is inspectable but minimal.** Each completed run preserves
  the effective prompt, final response, result metadata, and workspace.
  Non-empty stderr is retained. Deferred evidence is not generated.
- **AC-05 — failures are truthful.** Invalid metadata, failed setup, missing
  Codex, and nonzero Codex exits produce a failed run/result and a nonzero
  aggregate exit without being described as behavioral success.
- **AC-06 — baseline is symmetric.** When requested, the baseline receives the
  same eval prompt and setup contract in a fresh workspace; only the skill
  path supplied to Codex differs.
- **AC-07 — pilot coverage is complete.** All five pilot evals parse under the
  revised schema; the four fixture-backed cases resolve to their existing
  staged repos and the blocked-design case uses an empty workspace.
- **AC-08 — workflow ownership is clear.** `skill-creator` owns and documents
  the runner; the pilot skill owns only its eval definitions and fixtures.
- **AC-09 — execution is not grading.** The runner and documentation do not
  convert exit code zero into passed semantic expectations.

## Verification

Run one command at a time, narrowest first.

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Schema structure | Pilot eval JSON parses after setup metadata is separated from prompts | `python3 -m json.tool skills/task-implementation-flow/task-brief-designer/evals/evals.json` |
| Runner syntax | The new runner parses without executing Codex or writing bytecode | `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('skills/skill-creator/scripts/run_behavior_evals.py').read_text())"` |
| Targeted runner tests | Fake Codex proves setup substitution, empty-workspace behavior, isolation, baseline symmetry, evidence files, and aggregate failure exit | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/skill-creator/tests -p 'test_*.py'` |
| Skill validation | Updated skill metadata and instructions remain valid | `python3 skills/skill-creator/scripts/quick_validate.py skills/skill-creator` |
| Real Codex smoke | One fixture-backed pilot eval produces its expected task artifact inside only the disposable workspace | Run the new CLI for one selected eval after obtaining approval for live/model execution |
| Scope and hygiene | Only allowed files changed and no whitespace errors exist | `git diff --check` plus a scoped `git status --short` |

Schema parsing, fake-process tests, or a successful fixture setup do not prove
the real Codex boundary. Conversely, the smoke run proves invocation and
workspace behavior, not that every semantic expectation passes.

## Stops and handoff

- Stop for overlap with unrelated user changes in an allowed file, a required
  change outside the allowed paths, or a Codex CLI incompatibility that would
  materially alter the interface.
- Ask before the live Codex smoke unless that exact class of model-backed check
  is already authorized.
- Do not expand into deferred work to make the runner look complete.
- Next action: guided implementation.
- Required follow-on: immediately after implementation or correction, hand the
  completed bytes to a fresh independent acceptance reviewer.
