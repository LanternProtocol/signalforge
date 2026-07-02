#!/usr/bin/env python3
"""Validate SignalForge test vectors against schema and Pydantic models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from pydantic import ValidationError

from signalforge.canonical import sha256_payload_hash
from signalforge.envelope import SignalEnvelope

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = REPO_ROOT / "schemas" / "signal-envelope.schema.json"
DEFAULT_VECTOR_DIR = REPO_ROOT / "tests" / "vectors"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_vector(path: Path, validator: Draft202012Validator) -> tuple[bool, list[str]]:
    vector = load_json(path)
    envelope = vector["envelope"]
    expected = vector.get("expected", {})
    expected_schema_valid = expected.get("schema_valid", True)
    expected_semantic_valid = expected.get("semantic_valid", expected_schema_valid)

    errors: list[str] = []
    schema_errors = sorted(validator.iter_errors(envelope), key=lambda error: error.path)
    schema_valid = not schema_errors

    if schema_valid != expected_schema_valid:
        errors.append(
            f"schema expectation mismatch: expected {expected_schema_valid}, got {schema_valid}"
        )
        for error in schema_errors:
            errors.append(f"schema error at {'/'.join(map(str, error.path))}: {error.message}")

    pydantic_valid = True
    try:
        SignalEnvelope.model_validate(envelope)
    except ValidationError as exc:
        pydantic_valid = False
        if expected_schema_valid:
            errors.append(f"pydantic validation failed unexpectedly: {exc}")

    semantic_errors: list[str] = []
    payload_hash = envelope.get("signal", {}).get("payload_hash")
    if payload_hash:
        actual_hash = sha256_payload_hash(envelope["signal"].get("payload"))
        if payload_hash != actual_hash:
            semantic_errors.append(
                f"payload_hash mismatch: expected {actual_hash}, envelope has {payload_hash}"
            )

    semantic_valid = schema_valid and pydantic_valid and not semantic_errors
    if semantic_valid != expected_semantic_valid:
        errors.append(
            f"semantic expectation mismatch: expected {expected_semantic_valid}, got {semantic_valid}"
        )
        errors.extend(semantic_errors)

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--vectors", type=Path, default=DEFAULT_VECTOR_DIR)
    args = parser.parse_args()

    schema = load_json(args.schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    vector_paths = sorted(args.vectors.glob("*.json"))
    if not vector_paths:
        raise SystemExit(f"No vector files found in {args.vectors}")

    failures: dict[str, list[str]] = {}
    for path in vector_paths:
        ok, errors = validate_vector(path, validator)
        if not ok:
            failures[path.name] = errors

    if failures:
        for name, errors in failures.items():
            print(f"FAIL {name}")
            for error in errors:
                print(f"  - {error}")
        return 1

    print(f"Validated {len(vector_paths)} vector(s) against {args.schema}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
