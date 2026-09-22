# Runtime context contract

`runtime_context.py` is the provider-neutral boundary between launcher-specific metadata and future evidence consumers. Launcher adapters may emit one JSON object matching `runtime-context.schema.v1.json`; consumers load that object without runner-specific logic.

The contract contains only `schema_version`, `runner`, `provider`, `model`, `variant`, `effort`, `session_id`, and `identity_source`. Unknown identity values are `null`. If no trusted context file exists, `load_runtime_context(...)` returns the canonical object with all identity values `null` and `identity_source: "unavailable"`; absence is not an execution failure.

## Trust boundary

Canonical values must come from externally observable launcher/runtime information such as launcher configuration, runner API/session metadata, runner event streams, or a trusted adapter that normalizes those sources. LLM prose or model self-identification is not a valid source. Do not guess missing values.

`identity_source` describes the trusted source category and is one of `launcher`, `runner_api`, `runner_event`, `adapter`, or `unavailable`.

## Producer shape

A future launcher-specific adapter writes JSON like:

```json
{
  "schema_version": 1,
  "runner": "codex",
  "provider": "openai",
  "model": "gpt-5.6-sol",
  "variant": null,
  "effort": "medium",
  "session_id": "thread-123",
  "identity_source": "launcher"
}
```

The generic helper does not discover Codex, OpenCode, Ollama, or provider metadata itself.

## Consumer API

```python
from scripts.runtime_context import load_runtime_context

context = load_runtime_context("runtime-context.json")
```

A missing path returns the canonical unavailable context. A present but malformed or unsupported file raises `RuntimeContextError`; invalid evidence is not silently downgraded to unavailable.

## CLI

```bash
python3 scripts/runtime_context.py validate runtime-context.json
python3 scripts/runtime_context.py load runtime-context.json
python3 scripts/runtime_context.py load
```

Successful commands print normalized JSON. Validation errors are machine-readable JSON on stderr and exit with status 2.

If this shared tooling is copied into another repository, copy `runtime_context.py` together with `runtime-context.schema.v1.json`. It is an explicit shared runtime dependency, not a skill-owned file.
