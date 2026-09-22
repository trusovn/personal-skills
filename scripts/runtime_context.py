#!/usr/bin/env python3
"""Load and validate provider-neutral external agent runtime identity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Mapping


SCHEMA_PATH = Path(__file__).with_name("runtime-context.schema.v1.json")
SCHEMA_VERSION = 1
CONTEXT_FIELDS = (
    "schema_version",
    "runner",
    "provider",
    "model",
    "variant",
    "effort",
    "session_id",
    "identity_source",
)
IDENTITY_FIELDS = (
    "runner",
    "provider",
    "model",
    "variant",
    "effort",
    "session_id",
)
IDENTITY_SOURCES = frozenset(
    {"launcher", "runner_api", "runner_event", "adapter", "unavailable"}
)


class RuntimeContextError(ValueError):
    """Raised when supplied runtime context is malformed or unsupported."""


def unavailable_runtime_context() -> dict[str, Any]:
    """Return the canonical non-fatal representation for absent trusted context."""
    return {
        "schema_version": SCHEMA_VERSION,
        "runner": None,
        "provider": None,
        "model": None,
        "variant": None,
        "effort": None,
        "session_id": None,
        "identity_source": "unavailable",
    }


def _load_schema() -> dict[str, Any]:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeContextError(f"Runtime-context schema is missing: {SCHEMA_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeContextError(f"Runtime-context schema is invalid JSON: {exc}") from exc
    if not isinstance(schema, dict):
        raise RuntimeContextError("Runtime-context schema must be a JSON object")
    return schema


def _validate_schema_contract() -> None:
    """Fail if the shipped schema and helper contract drift apart."""
    schema = _load_schema()
    properties = schema.get("properties")
    required = schema.get("required")
    if not isinstance(properties, dict) or set(properties) != set(CONTEXT_FIELDS):
        raise RuntimeContextError("Runtime-context schema properties do not match helper contract")
    if not isinstance(required, list) or set(required) != set(CONTEXT_FIELDS):
        raise RuntimeContextError("Runtime-context schema required fields do not match helper contract")
    version = properties.get("schema_version", {}).get("const")
    if version != SCHEMA_VERSION:
        raise RuntimeContextError(
            f"Runtime-context schema version {version!r} does not match helper version {SCHEMA_VERSION}"
        )
    sources = properties.get("identity_source", {}).get("enum")
    if not isinstance(sources, list) or set(sources) != IDENTITY_SOURCES:
        raise RuntimeContextError("Runtime-context identity_source values do not match helper contract")


def validate_runtime_context(value: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and return a normalized copy of one runtime-context object."""
    _validate_schema_contract()
    if not isinstance(value, Mapping):
        raise RuntimeContextError("Runtime context must be a JSON object")

    keys = set(value)
    expected = set(CONTEXT_FIELDS)
    missing = sorted(expected - keys)
    extra = sorted(keys - expected)
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append(f"missing fields: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected fields: {', '.join(extra)}")
        raise RuntimeContextError("Invalid runtime-context fields (" + "; ".join(details) + ")")

    version = value["schema_version"]
    if isinstance(version, bool) or not isinstance(version, int):
        raise RuntimeContextError("schema_version must be integer 1")
    if version != SCHEMA_VERSION:
        raise RuntimeContextError(
            f"Unsupported runtime-context schema_version {version!r}; expected {SCHEMA_VERSION}"
        )

    normalized: dict[str, Any] = {"schema_version": SCHEMA_VERSION}
    for field in IDENTITY_FIELDS:
        field_value = value[field]
        if field_value is not None:
            if not isinstance(field_value, str) or not field_value.strip():
                raise RuntimeContextError(f"{field} must be a non-empty string or null")
        normalized[field] = field_value

    identity_source = value["identity_source"]
    if not isinstance(identity_source, str) or identity_source not in IDENTITY_SOURCES:
        allowed = ", ".join(sorted(IDENTITY_SOURCES))
        raise RuntimeContextError(
            f"identity_source must be one of: {allowed}; got {identity_source!r}"
        )
    if identity_source == "unavailable" and any(
        normalized[field] is not None for field in IDENTITY_FIELDS
    ):
        raise RuntimeContextError(
            "identity_source 'unavailable' requires all runtime identity values to be null"
        )
    normalized["identity_source"] = identity_source
    return normalized


def load_runtime_context(path: str | Path | None = None) -> dict[str, Any]:
    """Load trusted context from JSON, or return unavailable when no file exists."""
    if path is None:
        return unavailable_runtime_context()

    context_path = Path(path)
    if not context_path.exists():
        return unavailable_runtime_context()
    if not context_path.is_file():
        raise RuntimeContextError(f"Runtime-context path is not a file: {context_path}")

    try:
        value = json.loads(context_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeContextError(f"Invalid runtime-context JSON in {context_path}: {exc}") from exc
    except OSError as exc:
        raise RuntimeContextError(f"Cannot read runtime context {context_path}: {exc}") from exc

    return validate_runtime_context(value)


def _json_dump(value: Mapping[str, Any]) -> None:
    print(json.dumps(dict(value), sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Load or validate normalized external agent runtime context."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate an existing runtime-context JSON file"
    )
    validate_parser.add_argument("file")

    load_parser = subparsers.add_parser(
        "load", help="Load context; missing/omitted file yields identity_source=unavailable"
    )
    load_parser.add_argument("file", nargs="?")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate":
            path = Path(args.file)
            if not path.is_file():
                raise RuntimeContextError(f"Runtime-context file does not exist: {path}")
            context = load_runtime_context(path)
        else:
            context = load_runtime_context(args.file)
    except RuntimeContextError as exc:
        print(json.dumps({"error": str(exc), "valid": False}, sort_keys=True), file=sys.stderr)
        return 2

    _json_dump(context)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
