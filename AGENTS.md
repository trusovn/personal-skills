## Verification evidence

- Do not treat schema, syntax, or configuration checks as behavioral verification. Any test or eval that claims a successful outcome must supply the inputs and setup needed to exercise that outcome.

- When creating session handoff, do not edit the previous existing file, if there's one. Delete the old one and create a new one. 

## Skill installation resolution

- When work in the current repository uses a named skill and a matching project-local copy exists under `.agents/skills/`, resolve and read that project-local copy before considering user-global skill paths. Do not probe or switch to a user-global copy after a matching project-local skill has been selected for the invocation.
- Resolve shared tooling from the same installation root as the active skill. For a project-local `.agents/skills/` installation, use only the sibling `.agents/scripts/`; do not mix project-local skills with user-global helpers or vice versa.
- If optional shared tooling is missing or unavailable, follow the active skill's documented fallback behavior. Do not silently replace it with tooling from another installation root.

## Working on a specific named task (from official plan docs)

- When finishing a task, do not update existing plan documents - write your results next to them either per task or in a dedicated file, if already present.
- Use a soft stop around 25–35 tool calls or 80–100k current-context input. If the task reaches that boundary, stop with a structured handoff instead of continuing.