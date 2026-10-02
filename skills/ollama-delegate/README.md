# Ollama Delegate — operator setup

This README covers one-time/local operator setup for `ollama-delegate`. The agent-facing behavior and delegation contract live in `SKILL.md`.

## Default local setup

The runtime reads its default endpoint and model aliases from the adjacent shared configuration installed as:

```text
.agents/scripts/ollama-models.json
```

By default, Ollama is expected on:

```text
http://127.0.0.1:11434
```

A normal project-local invocation is:

```bash
python3 .agents/scripts/ollama_delegate.py run \
  --model glm-flash \
  --skill senior-code-review \
  "Review the current change for material correctness and maintainability problems."
```

## Sandbox or container reaching host Ollama

If the agent runs inside a sandbox/container, `127.0.0.1` may point to the sandbox itself rather than the host machine running Ollama. Override the endpoint for that invocation:

```bash
OLLAMA_BASE_URL=http://<sandbox-visible-host>:11434 \
python3 .agents/scripts/ollama_delegate.py run \
  --model glm-flash \
  --skill senior-code-review \
  "Review the current change for material correctness and maintainability problems."
```

Replace `<sandbox-visible-host>` with the host/address that the sandbox is allowed to reach. The runtime does not manage sandbox networking; it only uses the endpoint supplied through `OLLAMA_BASE_URL`.

## Cloud-model authentication

Ollama Cloud inference may require the local Ollama installation to be signed in. If authentication is missing, run once on the host:

```bash
ollama signin
```

Then retry the delegation.

## Adding or refreshing a cloud model

The checked-in aliases in `ollama-models.json` are intentionally small and may become stale as Ollama's cloud catalog changes.

1. Check the current official Ollama model/cloud catalog.
2. Use the exact published cloud model identifier, normally with a `:cloud` variant.
3. If Ollama requires the model to be fetched/registered locally, run once:

```bash
ollama pull <exact-cloud-model-id>
```

4. Add or update a concise alias in `.agents/scripts/ollama-models.json` (or `scripts/ollama-models.json` in the source repository).
5. Verify the configured aliases:

```bash
python3 .agents/scripts/ollama_delegate.py models
```

6. Run a small bounded delegation before relying on the new model for a larger task.

`ollama ls` shows models currently known to the local Ollama installation. It is useful for local verification, but it is not the authoritative list of all cloud models currently offered by Ollama.

## Useful discovery

```bash
python3 .agents/scripts/ollama_delegate.py models
python3 .agents/scripts/ollama_delegate.py skills
```

Use `--repo PATH` when the repository to inspect is not the current working directory.
