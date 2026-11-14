"""Canonical JSON text and UTF-8 text digests for retained record identities.

Standard library only; record shape, policy and publication belong elsewhere."""

from __future__ import annotations

import hashlib
import json
from typing import Any



def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()
