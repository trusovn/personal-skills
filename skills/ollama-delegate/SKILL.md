---
name: ollama-delegate
description: Delegate a bounded repository analysis or review task to an Ollama-hosted cloud model through the local Ollama HTTP server. Use when a second model should independently inspect a repository using a selected personal skill, especially for reviews, challenge passes, or comparative analysis. The delegated agent is read-only in this version.
compatibility: Requires Python 3, access to the configured Ollama HTTP endpoint, and an Ollama model available through that server.
---

# Ollama Delegate

Use the shared `ollama_delegate.py` runtime to give a bounded task and a complete selected skill package to a separate Ollama-backed model. The delegated agent gets read-only repository tools (`list_files`, `search_text`, `read_file`) and should inspect evidence for itself rather than relying only on a preassembled diff.

## Resolve the runtime from the active installation

Keep skill and shared runtime from the same installation root.

- Source repository skill: use `scripts/ollama_delegate.py` and `scripts/ollama-models.json`.
- Project-local `.agents/skills/ollama-delegate`: use sibling `.agents/scripts/ollama_delegate.py` and `.agents/scripts/ollama-models.json`.
- Do not mix a project-local skill with user-global or source-repository runtime files.

The endpoint defaults to the value in `ollama-models.json`. `OLLAMA_BASE_URL` overrides it, which is useful when a sandbox must reach an Ollama daemon outside the sandbox.

## Normal invocation

Run from the target repository root:

```bash
python3 .agents/scripts/ollama_delegate.py run \
  --model glm-flash \
  --skill senior-code-review \
  "Review the current change for material correctness and maintainability problems."
```

In the source repository, use `scripts/ollama_delegate.py` instead.

Useful discovery commands:

```bash
python3 .agents/scripts/ollama_delegate.py models
python3 .agents/scripts/ollama_delegate.py skills
```

Use `--repo PATH` when the target repository is not the current directory. Use `--max-turns` only when the task clearly needs a different bound.

## Delegation contract

Before invoking:

1. Choose one bounded task.
2. Choose the skill whose instructions the delegated model should follow.
3. Prefer a model alias from the local JSON rather than embedding a provider model name in workflow instructions.
4. Make sure the target repository and requested scope are accessible from the delegated runtime.

The runtime packages the selected skill's `SKILL.md` and skill-owned text references into the system context. It also tells the model that repository instructions outrank the skill. The model can then inspect the repository itself with read-only tools.

Treat the result as another agent's evidence or review, not as automatically authoritative. The caller remains responsible for reconciling conflicts, checking important findings, and applying any workflow verdict rules.

## Model catalog maintenance

`ollama-models.json` is intentionally local configuration, not a permanent catalog. Ollama cloud model names, availability, and recommended variants change over time.

When a requested model is missing, stale, or no longer available:

1. Check the **current official Ollama model/cloud catalog** first when web access is available. Do not assume the checked-in JSON is current.
2. Use `ollama list` only to inspect models currently known to the local Ollama installation. It is **not** an exhaustive list of all cloud models available from Ollama.
3. For a newly selected Ollama Cloud model, use the exact cloud model identifier published by Ollama, normally a name with the `:cloud` variant.
4. If the local Ollama installation must fetch/register that model before use, it is acceptable to stop and ask the user to run the one-time command:
   ```bash
   ollama pull <model>:cloud
   ```
   Then retry after the user confirms it completed.
5. Add or update a concise alias entry in the adjacent `ollama-models.json`. Keep provider-specific names there rather than spreading them through skills.
6. Validate with:
   ```bash
   python3 .agents/scripts/ollama_delegate.py models
   ```
   and then run a small bounded delegation before relying on the new entry.

Do not silently substitute a different model family when an alias becomes stale. Surface the mismatch and update the configuration deliberately.

## Configuration

The checked-in JSON contains:

- `endpoint`: default Ollama HTTP endpoint;
- `default_model`: optional default alias;
- `models`: alias map;
- per alias:
  - `model`: exact Ollama model identifier;
  - `think`: optional Ollama reasoning value;
  - `context_length`: optional request context;
  - `temperature`, `top_p`, `seed`: optional decoding controls;
  - `max_tokens`: optional output cap;
  - `timeout_seconds`: optional request timeout.

Keep the configuration provider-specific and small. Do not add benchmark artifact digests, residency policy, repetitions, ranking data, or OpenRouter/OpenAI-provider settings to this tool.

## Failure handling

- Connection failure: report the endpoint and let the caller/user fix sandbox or daemon access.
- Unknown alias: list configured aliases and update the JSON only after confirming the current Ollama identifier.
- Missing skill: list installed skill IDs; do not fall back across installation roots.
- Tool/path denial: report it as a bounded read limitation.
- Model asks for edits or shell execution: do not grant them in this version.
- Timeout/max turns: return the partial failure explicitly; do not present it as a completed independent review.
