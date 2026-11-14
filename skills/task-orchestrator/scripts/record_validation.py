"""Small shared record-shape, scalar and relative-path predicates.

No record families, workflow decisions, persistence or sibling dependencies."""

from __future__ import annotations

import re
from typing import Any



def validate_exact_object(value: Any, required: tuple[str, ...], field: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    missing = set(required) - set(value)
    if missing:
        raise ValueError(f"{field} is missing: {', '.join(sorted(missing))}")
    unknown = set(value) - set(required)
    if unknown:
        raise ValueError(f"{field} contains unknown fields: {', '.join(sorted(unknown))}")


def validate_sha256(value: Any, field: str) -> None:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError(f"{field} must be a lowercase SHA-256 digest")


def validate_str(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")


def validate_str_array(value: Any, field: str, *, allow_empty: bool = False) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    if not allow_empty and len(value) < 1:
        raise ValueError(f"{field} must have at least one item")
    for item in value:
        validate_str(item, f"{field} item")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} items must be unique")


def validate_bool(value: Any, field: str) -> None:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be a boolean")


def validate_run_relative_reference(value: Any, field: str) -> None:
    validate_str(value, field)
    if value.startswith("/") or "\\" in value:
        raise ValueError(f"{field} must be a run-relative artifact path")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError(f"{field} contains an invalid path segment")


def is_valid_repo_relative_path(path_str: str) -> bool:
    if not path_str:
        return False
    return not any(part in {"", ".", ".."} for part in path_str.split("/"))
