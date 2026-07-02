# RFC-0002: Canonical Payload Hashing, Timestamps, and Replay/Freshness Semantics

## Status

Draft

## Summary

This RFC defines the next protocol decision area after RFC-0001: how SignalForge should canonicalize payloads for hashing, represent timestamps, and reason about replay and freshness.

RFC-0001 introduced `payload_hash`, `observed_at`, `declared_at`, `created_at`, `expires_at`, `freshness_status`, and `replay_status`. RFC-0002 narrows the semantics of those fields so implementations can validate envelopes consistently.

## Motivation

A Signal Envelope can only support auditability and adversarial-resilience if different implementations can reproduce the same integrity checks and interpret time-related metadata consistently.

Without canonicalization rules, two systems can compute different hashes for the same logical payload.

Without timestamp rules, stale or replayed data can look fresh.

Without replay/freshness semantics, degraded-mode systems may silently accept unsafe inputs.

## Goals

- Define a provisional canonical payload representation.
- Define the format and meaning of envelope timestamps.
- Define how freshness should be evaluated.
- Define how replay suspicion should be represented.
- Identify which rules belong in schema validation versus semantic validation.
- Provide test-vector requirements for hash, timestamp, freshness, and replay behavior.

## Non-goals

- Final cryptographic signing design.
- Final distributed replay-cache design.
- Final confidence scoring model.
- Final sensor-specific freshness policies.
- Final transport protocol.

## Proposed canonical payload hashing profile

Until superseded, SignalForge should use the following provisional payload canonicalization profile:

1. Encode payloads as JSON.
2. Sort object keys lexicographically.
3. Use UTF-8 encoding.
4. Use no insignificant whitespace.
5. Preserve JSON value types.
6. Hash the canonical byte sequence with SHA-256.
7. Represent hashes as lowercase strings using the prefix `sha256:` followed by 64 lowercase hexadecimal characters.

Example representation:

```text
sha256:<64 lowercase hex characters>
```

The current validation harness implements this provisional profile. It is intentionally minimal and should be reviewed before being treated as a stable protocol requirement.

## Timestamp fields

### `created_at`

Time the envelope was created. This is not necessarily the time the signal was observed.

### `observed_at`

Time the signal was observed or collected by the observer or collection infrastructure.

### `declared_at`

Time claimed by the source or payload. This value may be false, missing, or manipulated.

### `verified_at`

Time verification was performed.

### `expires_at`

Time after which the envelope or signal should no longer be treated as fresh without additional verification.

## Timestamp format

All timestamps should use RFC3339-compatible UTC timestamps when possible.

Recommended profile:

- UTC preferred.
- Include timezone offset or `Z`.
- Avoid naive timestamps.
- Preserve source-provided timestamps separately from observer timestamps.
- Do not overwrite source timestamps during normalization.

## Freshness semantics

Initial `freshness_status` values:

- `fresh` — within applicable freshness policy.
- `stale` — outside the desired freshness window but not necessarily expired.
- `expired` — beyond explicit expiration or policy cutoff.
- `unknown` — insufficient information to determine freshness.
- `not_applicable` — freshness does not apply to the signal class.

Freshness should be based on observed time, declared time, envelope creation time, expiration, and signal-class policy.

Declared source time alone should not be sufficient to mark a signal fresh.

## Replay semantics

Initial `replay_status` values:

- `no_replay_evidence` — no replay indicators were found.
- `suspected_replay` — replay is plausible based on duplicate identifiers, duplicate payload hash, reused nonce, stale timestamp, or unexpected context.
- `confirmed_replay` — replay is established by policy or evidence.
- `unknown` — insufficient data to evaluate replay.
- `not_applicable` — replay analysis does not apply to the signal class.

Replay checks may consider:

- `envelope_id`
- `payload_hash`
- source identifiers
- observed time
- declared time
- prior envelopes
- evidence references
- collection context
- source-specific freshness rules

## Schema versus semantic validation

JSON Schema should validate structure, required fields, enum values, timestamp shape, and hash string format.

Semantic validation should validate:

- Whether `payload_hash` actually matches the canonical payload.
- Whether `expires_at` is consistent with freshness status.
- Whether replay indicators are consistent with replay status.
- Whether declared timestamps conflict with observed timestamps.
- Whether degraded-mode flags require lower confidence or partial verification.

## Test-vector requirements

The test suite should include cases for:

1. Payload hash matches canonical payload.
2. Payload hash mismatch.
3. Fresh signal.
4. Stale signal.
5. Expired signal.
6. Declared time conflicts with observed time.
7. Duplicate payload hash in a new context.
8. Replay status is unknown because required historical context is absent.

## Open questions

- Should SignalForge adopt an existing JSON canonicalization standard instead of the provisional profile?
- How should non-JSON payloads be canonicalized?
- What clock-skew tolerance should be allowed?
- Should replay status require a persistent replay index?
- Should `payload_hash` hash the raw payload bytes, normalized payload, or both?
- Should freshness policies be embedded in the envelope or referenced externally?

## Acceptance criteria

This RFC can move from Draft to Accepted when:

- Canonical payload hashing rules are confirmed or replaced.
- Timestamp rules are confirmed.
- Freshness status semantics are confirmed.
- Replay status semantics are confirmed.
- Test-vector requirements are implemented.
- ADR-0003 records any final canonicalization decision if it differs from this draft.

## Related

- RFC-0001: Minimum Viable Signal Envelope
- ADR-0002: Initial schema representation
- `schemas/signal-envelope.schema.json`
- `scripts/validate_vectors.py`
