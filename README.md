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

- `ask-user-questions`
- `idea-brief`
- `idea-challenger`
- `idea-investigator`
- `repo-foundation`
- `senior-code-review`
- `session-handoff`
- `skill-creator`
- `testing-discipline`

Installed copies under `~/.agents/skills`, `~/.codex/skills`, or a project are
distribution targets. Edit here, validate here, and redistribute from here.
