"""Canonical payload helper functions.

These helpers are provisional until RFC-0002 is accepted. They intentionally use a small,
deterministic JSON profile: UTF-8, sorted object keys, and no insignificant whitespace.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_payload_bytes(payload: Any) -> bytes:
    """Return deterministic JSON bytes for a payload."""

    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def sha256_payload_hash(payload: Any) -> str:
    """Return the SignalForge provisional sha256 payload hash string."""

    return f"sha256:{hashlib.sha256(canonical_payload_bytes(payload)).hexdigest()}"
