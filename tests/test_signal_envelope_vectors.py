from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.validate_vectors import validate_vector
from signalforge.envelope import SignalEnvelope

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "signal-envelope.schema.json"
VECTOR_DIR = REPO_ROOT / "tests" / "vectors"


def test_vectors_match_schema_and_semantic_expectations() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    vector_paths = sorted(VECTOR_DIR.glob("*.json"))
    assert vector_paths, "expected at least one vector"

    failures: dict[str, list[str]] = {}
    for path in vector_paths:
        ok, errors = validate_vector(path, validator)
        if not ok:
            failures[path.name] = errors

    assert not failures


def test_schema_accepts_valid_minimal_envelope() -> None:
    vector_path = VECTOR_DIR / "valid-minimal-envelope.json"
    vector = json.loads(vector_path.read_text(encoding="utf-8"))
    envelope = vector["envelope"]

    SignalEnvelope.model_validate(envelope)
