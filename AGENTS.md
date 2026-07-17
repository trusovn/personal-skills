## Verification evidence

- Do not treat schema, syntax, or configuration checks as behavioral verification. Any test or eval that claims a successful outcome must supply the inputs and setup needed to exercise that outcome.

- When creating session handoff, do not edit the previous existing file, if there's one. Delete the old one and create a new one. 

## Working on a specific named task (from official plan docs)

- When finishing a task, do not update existing plan documents - write your results next to them either per task or in a dedicated file, if already present.
- Use a soft stop around 25–35 tool calls or 80–100k current-context input. If the task reaches that boundary, stop with a structured handoff instead of continuing.
