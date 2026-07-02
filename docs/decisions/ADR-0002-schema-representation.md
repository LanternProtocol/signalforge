# ADR-0002: Initial schema representation

## Status

Accepted

## Context

RFC-0001 defines the minimum viable Signal Envelope. The project now needs a machine-readable representation that can validate examples, drive implementation, and remain understandable to protocol reviewers.

SignalForge also needs a Python-native model because the early validation harness and reference implementation are expected to be Python-based.

## Decision

SignalForge will use a dual representation for the initial Signal Envelope:

1. **JSON Schema 2020-12** as the protocol-facing, language-neutral schema.
2. **Pydantic v2 models** as the Python implementation-facing validation and developer ergonomics layer.

The JSON Schema will live under `schemas/` and is the canonical machine-readable contract for serialized envelopes.

The Pydantic models will live under `src/signalforge/` and must remain aligned with the JSON Schema.

## Rationale

JSON Schema is appropriate for the initial protocol representation because it is language-neutral, reviewable, widely supported, and easy to use with JSON test vectors.

Pydantic is appropriate for the initial Python implementation because it provides type-aware models, structured validation, useful errors, and a clean path from schema examples to implementation code.

Using both avoids prematurely binding Lantern Protocol to Python while still giving SignalForge a practical reference implementation path.

## Consequences

- The JSON Schema is the primary cross-language artifact.
- Pydantic models must not introduce hidden semantics that are absent from the schema or RFCs.
- Test vectors must validate against the JSON Schema.
- Python tests should also instantiate the Pydantic models to catch implementation drift.
- Semantic checks that cannot be fully represented in JSON Schema, such as canonical payload-hash verification, should be implemented in the validation harness and documented in RFC follow-up work.

## Deferred decisions

- Whether future protocol releases should also provide Protocol Buffers, Avro, or OpenAPI artifacts.
- Whether canonical payload hashing should use JSON Canonicalization Scheme, a custom canonical JSON profile, or another representation.
- Whether schema publication should be versioned by URI, release tag, or package artifact.

## Related

- RFC-0001: Minimum Viable Signal Envelope
- RFC-0002: Canonical payload hashing, timestamps, and replay/freshness semantics