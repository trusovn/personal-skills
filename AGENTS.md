## Verification evidence

- Do not treat schema, syntax, or configuration checks as behavioral verification. Any test or eval that claims a successful outcome must supply the inputs and setup needed to exercise that outcome.

## Session handoff

- When creating a session handoff, delete the previous handoff file if one exists, then create a new file. Do not edit the previous file.

## Test and eval maintenance

- Before adding tests, evals, or fixtures, inspect relevant existing coverage and setup. Use `testing-discipline` as the authority for test design and maintenance.
- Prefer updating, reusing, or consolidating existing cases and fixture helpers over appending cases or copying setup infrastructure. Add coverage for distinct behavioral evidence that is missing.
- Before removing obsolete or redundant tests or evals, identify the remaining coverage and preserve distinct scenarios, failure modes, and boundary evidence. Keep this maintenance within the task's scope.

## Development-profile installer maintenance

- `scripts/install_development_skills.py` is the canonical installer for the predefined project-local development profile. When changing, renaming, moving, adding, or removing a skill that belongs in that profile, or when changing a shared runtime dependency required by those installed skills, inspect the installer in the same change.
- Keep `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`, focused installer tests, and README installation documentation synchronized. Do not assume that editing a source skill or shared script automatically updates the installation profile.
- Preserve the installer's narrow ownership boundary: it may replace only the profile-selected skill directories, the explicitly managed profile guide, the explicitly managed shared script files, and its marked block in target `AGENTS.md`. Do not broaden it into a generic package manager unless a separate task explicitly requires that.

## Working on a specific named task (from official plan docs)

- When finishing a task, do not update existing plan documents - write your results next to them either per task or in a dedicated file, if already present.

## Working on skill source in this repository

This repository contains editable skill source. Source presence does not mean a skill is installed, available, or active. Follow the installer-managed resolution rules below when selecting an installation.

When following a named-skill workflow:

- Resolve the actual available skill installation for this session.
- Do not request an unavailable skill merely because it is referenced by source documentation or the target project plan.
- Do not silently substitute newer source instructions for an older installed skill.
- Do not refresh the active installation during an ongoing agent run.

For development of skills not yet installed:

- Treat source instructions as development specifications.
- Where independent review is required, use an explicitly authorized fresh source-guided reviewer if the named skill is unavailable.
- Clearly distinguish source-guided review from installed-skill execution and behavioral qualification.
- If the required review cannot be performed, report the missing capability and next action; never invent a completed review.

Do not omit an independent review merely because the named skill is unavailable, and do not combine separate discovery and acceptance decisions when the applicable task contract requires separation.

## Development routing and maintainability

- Read `docs/project-map.md` for source/test ownership and `docs/development.md`
  for setup, test tiers, and command scope.
- Discover implemented reusable contracts through `docs/contracts/index.json`,
  then the subsystem record and its code/schema/test authorities. Plans describe
  intended work, not implemented capability. Update affected subsystem records
  and regenerate the index when current contracts change; in the bounded task
  flow, use its designated registry-updater stage.
- Run the owning focused suite first. For cross-cutting changes run
  `python3 tools/verify.py`; report skips and failures without treating them as
  successful behavioral qualification. Live or expensive checks still require
  the applicable approval.
- Keep modules focused and changes local to their owner. Keep dependencies
  explicit, reuse existing patterns, and keep deterministic logic testable
  without provider I/O. Add abstractions only for concrete boundaries or consumers.
- Before handoff, run the canonical architecture check:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`.
  Fix hard failures. `tests/test_architecture.py` owns CLEAN policy; there is no
  debt baseline. Advisory analyzer signals do not require unrelated cleanup.
- Check contracts with `python3 tools/check_contracts.py --root .`;
  regenerate only with the explicit `--write-index` command. Repository-only
  foundation tools are not development-profile runtime dependencies.

<!-- personal-skills:development-install:begin -->
## Skill installation resolution

This block is managed by the `personal-skills` development-profile installer.
Rerun the installer to update it; keep repository-specific instructions outside
these markers.

- When work in the current repository uses a named skill and a matching project-local copy exists under `.agents/skills/`, resolve and read that project-local copy before considering user-global skill paths. Do not probe or switch to a user-global copy after a matching project-local skill has been selected for the invocation.
- Resolve shared tooling from the same installation root as the active skill. For a project-local `.agents/skills/` installation, use only the sibling `.agents/scripts/`; do not mix project-local skills with user-global helpers or vice versa.
- If optional shared tooling is missing or unavailable, follow the active skill's documented fallback behavior. Do not silently replace it with tooling from another installation root.
<!-- personal-skills:development-install:end -->
