# Personal Skills

This repository is the canonical editable source for general-purpose personal
agent skills used by the Local Workbench.
## Layout

```text
skills/
├── README.md
├── <skill-name>/
│   ├── SKILL.md
│   └── <skill-owned references, scripts, fixtures, or evals>
└── task-implementation-flow/
    ├── README.md
    └── <flow-skill>/
        ├── SKILL.md
        └── <skill-owned references, scripts, fixtures, or evals>
```

Each directory containing a `SKILL.md` is the complete skill-owned package. Its
frontmatter `name` is the identifier used by workbench profiles and installers.
Keep files used only by one skill inside that skill's directory. Shared
repository-level runtime tooling is separate: when a skill or flow explicitly
names a shared script/schema as a dependency, that dependency must also be
installed or copied.

Current source skills:
- `architecture-guardrails`
- `ask-user-questions`
- `ai-flow-foundation`
- `bounded-task-implementer`
- `foundation-readiness-review`
- `idea-brief`
- `idea-challenger`
- `idea-investigator`
- `ollama-delegate`
- `project-delivery-plan`
- `project-direction`
- `project-bootstrap`
- `project-plan-verification`
- `repo-foundation`
- `senior-code-review`
- `session-handoff`
- `skill-creator`
- `task-acceptance-review`
- `task-brief-designer`
- `task-contract-registry-updater`
- `task-maintainability-review`
- `task-preflight`
- `task-verification-designer`
- `task-orchestrator`
- `testing-discipline`

## Installation and shared integrations

### Preferred development-profile installation

For a local Git repository that should receive the normal development skill set,
including this source repository, use the canonical installer rather than
manually copying individual skills and shared helpers:

```bash
python3 /path/to/personal-skills/scripts/install_development_skills.py \
  /path/to/target-repo
```

The predefined development profile (`development`) starts at repository-stage
project direction and installs the foundation and delivery-planning skills,
the seven task-implementation-flow skills, `senior-code-review`,
`ollama-delegate`, `testing-discipline`, and `session-handoff`. Pre-repository
idea work (`ask-user-questions`, `idea-challenger`, `idea-investigator`, and
`idea-brief`), the specialist `skill-creator`, and the explicitly invoked
`task-orchestrator` remain separate installs. The profile also installs the
shared workflow/runtime/evidence files required by the current bounded
implementation integration plus the Ollama delegation runtime and its local
model-alias configuration.

The installer:

- locates source skills and shared helpers relative to its own script path;
- copies complete selected skill packages into `.agents/skills/` while preserving
  their source-relative nested layout;
- copies `skills/README.md` to `.agents/skills/README.md` as the concise usage,
  input, output, and call-order guide for the installed profile;
- replaces only those selected skill directories on rerun, so stale files inside
  a managed package are removed without deleting unrelated local skills;
- updates only the explicitly managed shared files under `.agents/scripts/`;
- preserves existing target `AGENTS.md` content and adds/updates one marked
  project-local skill-resolution block;
- validates the staged evidence/runtime installation before replacing managed
  targets and runs the installed `run_evidence.py ... availability` check again
  after replacement;
- supports using the source repository as the target because all selected files
  are staged before managed destinations are replaced; and
- is safe to rerun as the normal update mechanism for this profile.

To refresh the project-local installation in this source repository itself, run:

```bash
python3 scripts/install_development_skills.py .
```

**Maintenance contract for future skill changes:**
`scripts/install_development_skills.py` is part of the distribution surface.
Any change that renames, moves, adds, or removes a skill that belongs in the
`development` profile, or changes shared runtime files required by those skills,
must inspect and, when needed, update `DEVELOPMENT_SKILL_SOURCES`,
`PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`,
`tests/test_install_development_skills.py`, and this installation documentation
in the same change. Root `AGENTS.md` repeats this rule so an agent working on
future skill updates sees it before finishing.

### Manual/project-specific installation

This source repository keeps editable skills under `skills/` and shared tooling
under `scripts/`. For a project-local manual installation, use the project's
`.agents/` namespace rather than adding agent infrastructure to the
application's own top-level directories:

```text
project/
└── .agents/
    ├── skills/
    │   └── <selected skills>
    └── scripts/
        └── <shared tooling required by those skills>
```

A skill-owned directory is the complete package only for files owned by that
skill. Shared scripts/schemas explicitly named by the skill or flow are separate
runtime dependencies and must be copied when that integration is wanted.

Current shared integrations:

| Capability | Project-local files | Required? |
| --- | --- | --- |
| Workflow fingerprinting | `.agents/scripts/workflow_version.py` | Only when workflow identity/fingerprinting is wanted |
| Generic runtime identity | `.agents/scripts/runtime_context.py`, `.agents/scripts/runtime-context.schema.v1.json` | Only when trusted runtime identity is supplied/consumed |
| Bounded-run evidence | `.agents/scripts/run_evidence.py` plus the workflow-version and runtime-context files above | Optional in ordinary guided use; may be made mandatory by an explicit repository/user/machine contract |
| Ollama cloud delegation | `.agents/skills/ollama-delegate/`, `.agents/scripts/ollama_delegate.py`, `.agents/scripts/ollama-models.json` | Only when a bounded task should be delegated to an Ollama-backed model through the configured local daemon |

`workflow_version.py` supports both this source repository layout
(`skills/` + `scripts/`) and the project-local installation layout
(`.agents/skills/` + `.agents/scripts/`). Shared tooling is resolved from the
same installation root as the active skills tree: `scripts/` beside `skills/`
in this source repository, or `.agents/scripts/` beside `.agents/skills/` in a
project-local installation. Task skills should refer to that canonical shared
tooling convention rather than hardcode repository-root script paths.

`ollama-delegate` follows the same installation-root rule. Its adjacent
`ollama-models.json` is intentionally a small, editable provider-specific alias
file rather than a permanent catalog. The skill documents how an agent should
check the current official Ollama cloud catalog, distinguish it from locally
known models, request a one-time `ollama pull <model>:cloud` from the user when
needed, and update the JSON deliberately rather than silently substituting a
model.

An unchanged copied skill keeps the same fingerprint because absolute
filesystem location is not part of the fingerprint. For source-repository
skills, Git-aware tracked/non-ignored-untracked discovery remains authoritative.
For an explicit project-local installed skills tree, package files are read from
the installed skill directory itself using the same skill-owned exclusions, so
an application repository may ignore `.agents/` without erasing workflow
identity.

`bounded-task-implementer` remains usable without the run-evidence integration.
Missing optional shared tooling must not accidentally turn a normal standalone
bounded task into a formal/orchestrated workflow.

See `scripts/runtime-context.md` for the runtime identity contract and
`scripts/run-evidence.md` for evidence lifecycle, snapshot, recovery, and
deterministic-check semantics.

## Workflow version fingerprints

Every directory containing a `SKILL.md` is versionable through one canonical
deterministic tool:

```bash
python3 scripts/workflow_version.py bounded-task-implementer
```

The tool prints JSON with the skill ID, a SHA-256 fingerprint, the current Git
commit, current branch (or `null` for detached HEAD), repository dirty state,
and workflow dirty state. For source-repository skills, the fingerprint is derived from the current contents
and relative paths of tracked plus non-ignored untracked files inside that skill
directory. For an explicit installed skills tree beside the active shared scripts,
the same fingerprint framing reads the installed package files directly instead
of applying the target application's Git ignore policy. Both modes exclude obvious
transient files such as `__pycache__`, `*.pyc`, `.DS_Store`, and `node_modules`, plus
root-level development-only `evals/` and `tests/` directories.

This fingerprint answers "what workflow definition is present?" and is kept
separate from repository provenance. `repository_commit` and
`repository_branch` identify the checked-out Git state, while
`repository_dirty` and `workflow_dirty` show whether the repository or this
workflow differs from committed state. Unrelated repository changes therefore
do not change a skill fingerprint. There are no manually incremented per-skill
versions.

Fingerprint semantics are a compatibility contract. Changes to input
selection/exclusion, path normalization, canonical ordering, hash framing, or
the hash algorithm can redefine fingerprints even when skill contents have not
changed. Do not change those semantics silently; treat such a change as an
explicit compatibility/versioning decision.

The mechanism intentionally versions only the skill-owned package in this
iteration. Do not add ad-hoc external dependency rules to individual skills;
extend the canonical tool later if a concrete shared runtime dependency makes
that necessary.

## Shared agent runtime context

External agent runtime identity uses a small provider-neutral contract in
`scripts/runtime-context.schema.v1.json` with loading/validation support in
`scripts/runtime_context.py`. Launcher-specific adapters may later normalize
trusted launcher/session metadata into that contract; consumers do not need
Codex-, OpenCode-, Ollama-, or provider-specific branches.

Runtime identity is optional. Missing trusted context normalizes to
`identity_source: "unavailable"` with unknown fields left `null`; LLM
self-identification is never canonical identity. See
`scripts/runtime-context.md` for the trust boundary, API, and CLI.

## Optional bounded-run evidence

`scripts/run_evidence.py` can capture raw begin/finish facts around
`bounded-task-implementer` invocations without changing the normal guided
workflow contract. It records Git-local run state, immutable begin/finish
worktree snapshot identities, canonical workflow fingerprint, optional runtime
context, optional task association, and raw deterministic-check execution
facts. It does not generate diffs, change statistics, scores, or acceptance
verdicts.

Evidence storage lives under the worktree's Git metadata and does not require a
`.gitignore` change. In ordinary guided use, instrumentation is best-effort:
missing or failed evidence tooling does not make an otherwise valid bounded
implementation fail. A repository/user/machine contract may opt into stricter
requirements separately.

Parallel multi-agent execution against one worktree is not supported by this
iteration of run evidence. Concurrent run claiming and its coordination must be
implemented separately before multi-agent use is treated as supported.

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
  -> ai-flow-foundation     only when the product/runtime calls a model in its data/process flow
  -> repo-foundation        materialize the approved repository foundation
       -> architecture-guardrails when maintainability guardrails are planned
  -> foundation-readiness-review
  -> project-delivery-plan  when multi-task delivery needs a shared flow and handoff plan
  -> project-plan-verification  fresh-agent check before task planning
```
Not every project needs every idea stage. Enter at `project-direction` when the
desired experience and tradeoffs need clarification, or at `project-bootstrap`
when the objective and repository scaffold are already clear. Run
`ai-flow-foundation` before foundation materialization only when the product
or runtime itself has model-dependent behavior, so provider, validation,
deterministic-test, retry, and side-effect boundaries are part of the
materialization handoff. Coding-agent development or maintenance alone does not
trigger it; `repo-foundation` owns agent-legible repository setup for every
project.

`project-bootstrap` decides whether maintainability/architecture guardrails are
needed; `repo-foundation` owns their repository placement and integration. When
that capability is `ADD` or `REPAIR`, use `architecture-guardrails` to establish
the smallest useful deterministic architecture gate without redesigning the
product architecture.

`foundation-readiness-review` checks the resulting repository from a fresh
operator's perspective and recommends the cheapest safe delivery route. For
deeper SDD planning, go to the separate SDD repository.

`project-delivery-plan` is the lightweight default bridge from a ready
foundation to multi-task delivery when full SDD is unnecessary. It makes
end-to-end data/process/state flow, interfaces, artifacts, invariants, and task
handoffs explicit without pre-solving task-local implementation. Run
`project-plan-verification` with a fresh agent before implementation to
independently check scope, producer/consumer closure, interface/state
consistency, task coverage, and dependency composition. Use full SDD instead
when foundation readiness or project risk requires deeper specification
artifacts.
### Implementing a bounded change

The normal human-driven path is deliberately lightweight:

```text
clear request or task brief
  -> task-brief-designer       when the implementation contract has gaps
  -> task-verification-designer
                               when task-local verification semantics are non-obvious
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
contracts are not needed. Use `ollama-delegate` when a separate Ollama-backed
model should independently inspect the repository under one of the installed
skill contracts; its V1 repository tools are intentionally read-only.

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
- `ollama-delegate` runs a bounded second-model repository inspection through a
  configured Ollama daemon without granting write or shell tools.
- `session-handoff` preserves verified context between sessions or agents.
- `skill-creator` creates, validates, and evaluates skills in this source repo.

Edit skills in this source repository, validate them here, and redistribute
using the installation conventions defined above.


<!-- contract-registry-flow:root-readme:begin -->
## Implemented-contract discovery in the delivery flow

For projects that enable machine-readable contract discovery, the end-to-end flow distinguishes intended and implemented system state:

```text
project-bootstrap
  -> ai-flow-foundation (when the product/runtime calls a model)
  -> repo-foundation
  -> foundation-readiness-review
  -> project-delivery-plan
  -> project-plan-verification
  -> task brief
  -> bounded implementation
  -> deterministic architecture validation
  -> maintainability review
  -> contract-registry synchronization
  -> acceptance review
```

Planning artifacts (`project-plan.md`, `task-map.json`, task briefs) may describe future contracts. `docs/contracts/*.json` describes reusable contracts that are currently implemented. Stable plan IDs connect the two when a planned contract materializes. Executable declarations and code/tests remain the underlying authority.
<!-- contract-registry-flow:root-readme:end -->