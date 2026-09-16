# Personal Skills

This repository is the canonical editable source for general-purpose personal
agent skills used by the Local Workbench.
## Layout

```text
skills/
└── <skill-name>/
    ├── SKILL.md
    └── <skill-owned references, scripts, fixtures, or evals>
```

Each direct child of `skills/` is a complete skill package. Its `SKILL.md`
frontmatter `name` is the identifier used by workbench profiles and installers.
Keep files used only by one skill inside that skill's directory.

Current source skills:
- `architecture-guardrails`
- `ask-user-questions`
- `ai-flow-foundation`
- `bounded-task-implementer`
- `foundation-readiness-review`
- `idea-brief`
- `idea-challenger`
- `idea-investigator`
- `project-direction`
- `project-bootstrap`
- `repo-foundation`
- `senior-code-review`
- `session-handoff`
- `skill-creator`
- `task-acceptance-review`
- `task-brief-designer`
- `task-maintainability-review`
- `task-preflight`
- `task-orchestrator`
- `testing-discipline`
## How the skills fit together

These skills are a toolkit, not one mandatory pipeline. Start at the point that
matches the state of the work and use only the stages that reduce meaningful
uncertainty or risk.
### From an idea to a usable project foundation
```text
raw idea
  -> idea-challenger        optional pressure test
  -> idea-investigator      optional evidence-backed investigation
  -> idea-brief             portable early planning seed
  -> project-direction      owner-editable goals, priorities, and boundaries
  -> project-bootstrap      project charter and minimum foundation plan
  -> ai-flow-foundation     only when AI participates in the data/process flow
  -> repo-foundation        materialize the approved repository foundation
       -> architecture-guardrails when maintainability guardrails are planned
  -> foundation-readiness-review
```
Not every project needs every idea stage. Enter at `project-direction` when the
desired experience and tradeoffs need clarification, or at `project-bootstrap`
when the objective and repository scaffold are already clear. Run
`ai-flow-foundation` before foundation materialization for AI-bearing projects
so provider, validation, deterministic-test, retry, and side-effect boundaries
are part of the materialization handoff.

`project-bootstrap` decides whether maintainability/architecture guardrails are
needed; `repo-foundation` owns their repository placement and integration. When
that capability is `ADD` or `REPAIR`, use `architecture-guardrails` to establish
the smallest useful deterministic architecture gate without redesigning the
product architecture.

`foundation-readiness-review` checks the resulting repository from a fresh
operator's perspective and recommends the cheapest safe delivery route. Its
`SDD_*` routes refer to an optional external or project-provided SDD workflow;
this repository does not currently provide those SDD skills. When no SDD
workflow is available, use the bounded personal flow or ask the project owner
how planning should proceed.
### Implementing a bounded change

The normal human-driven path is deliberately lightweight:

```text
clear request or task brief
  -> task-brief-designer       when the implementation contract has gaps
  -> task-preflight            when readiness needs an independent check
  -> bounded-task-implementer  implementation and progressive verification
  -> architecture gate + task-maintainability-review
                               when repo policy requires maintainability review
  -> task-acceptance-review    fresh independent functional review when risk requires it
```
For small, unambiguous work, go directly to `bounded-task-implementer`; it
performs a compact self-preflight. When the repo declares a required
maintainability gate, run that gate and a fresh `task-maintainability-review`
before functional acceptance. Use `testing-discipline` alongside implementation
or review when behavioral evidence, test design, or QA risk is material. Use
`senior-code-review` for general diff/PR review when the stricter focused review
contracts are not needed.

The detailed guided, maintainability-gated, and high-assurance variants are
documented in
[`skills/task-implementation-flow/README.md`](skills/task-implementation-flow/README.md).
### Task orchestrator status

`task-orchestrator` is an experimental, incomplete high-assurance execution
path, not the default way to run the skills above. Its controller currently
supports `init`, `run-next`, and `inspect` for an already approved manifest and
run policy. It does **not** yet provide plan-to-manifest preparation, semantic
review/correction loops, safe stop and recovery, atomic acceptance with
dependency release/advance, or an unattended end-to-end runner.
Use it only when its current controller contract is specifically needed and
the required manifest/policy inputs already exist. Otherwise run the bounded
flow directly under human coordination.
### Supporting skills

- `ask-user-questions` supplies a consistent clarification protocol when a
  consequential decision cannot safely be inferred.
- `session-handoff` preserves verified context between sessions or agents.
- `skill-creator` creates, validates, and evaluates skills in this source repo.

Installed copies under `~/.agents/skills`, `~/.codex/skills`, or a project are
distribution targets. Edit here, validate here, and redistribute from here.
