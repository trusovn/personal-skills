# Synthetic fixture authority

Use project-local skills and sibling shared helpers. All stages are sequential and launched by code; never spawn agents. All actors use gpt-5.6-terra with medium reasoning. Implementer may change only catalog.py and tests/test_catalog.py. Independent maintainability review is required before registry update and acceptance. Architecture command: `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_architecture.py`. Registry commands: `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_contracts.py --root . --write-index` and the same without --write-index. These are cheap local checks, authorized. Source, tests, and executable contracts are owned by implementation. Registry updater owns docs/contracts/** and stale README.md claims. Read authority.md and run-policy.json for stage artifact permissions. Do not edit authority, policy, dependencies, skills, tools, or plans. No network, package installation, destructive actions, or actor commits.

<!-- personal-skills:development-install:begin -->
## Skill installation resolution

This block is managed by the `personal-skills` development-profile installer.
Rerun the installer to update it; keep repository-specific instructions outside
these markers.

- When work in the current repository uses a named skill and a matching project-local copy exists under `.agents/skills/`, resolve and read that project-local copy before considering user-global skill paths. Do not probe or switch to a user-global copy after a matching project-local skill has been selected for the invocation.
- Resolve shared tooling from the same installation root as the active skill. For a project-local `.agents/skills/` installation, use only the sibling `.agents/scripts/`; do not mix project-local skills with user-global helpers or vice versa.
- If optional shared tooling is missing or unavailable, follow the active skill's documented fallback behavior. Do not silently replace it with tooling from another installation root.
<!-- personal-skills:development-install:end -->
