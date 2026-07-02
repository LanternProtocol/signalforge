# RFC-0001: Minimum Viable Signal Envelope

## Status

Draft

## Tracking issue

- #2

## Summary

This RFC defines the first minimum viable Signal Envelope for SignalForge.

The envelope is the canonical wrapper around a signal payload. It separates the observed data from source context, provenance, verification state, adversarial-resilience metadata, and audit references.

The goal is not to finalize the full Lantern Protocol specification. The goal is to prevent early implementation work from creating implicit, undocumented semantics.

## Motivation

SignalForge needs a stable conceptual unit for representing signals under adversarial, degraded, or ambiguous conditions.

A minimum viable envelope should make these questions answerable:

- What was observed?
- Who or what claims to have produced it?
- Where, when, and how was it observed?
- What transformations or custody events affected it?
- What evidence supports or challenges it?
- What verification was performed?
- What remains unknown, missing, stale, ambiguous, or conflicting?
- What downstream decisions relied on it?

## Design principles

1. **Separate payload from trust.** The payload is not inherently trusted because it exists inside an envelope.
2. **Represent uncertainty explicitly.** Unknown, missing, unverifiable, stale, and conflicting states must not collapse into a generic null.
3. **Preserve auditability.** A reviewer should be able to reconstruct what was known, claimed, verified, and decided.
4. **Avoid silent trust upgrades.** Missing provenance or verification must not be interpreted as acceptable provenance or verification.
5. **Support degraded operation without hiding degradation.** Degraded-mode behavior must be visible in the envelope.
6. **Keep the first version implementation-neutral.** This RFC describes fields and semantics before choosing a final schema technology.

## Proposed envelope shape

The initial envelope should contain the following top-level sections:

```json
{
  "envelope_id": "string",
  "schema_version": "string",
  "created_at": "RFC3339 timestamp",
  "signal": {},
  "source": {},
  "provenance": {},
  "verification": {},
  "resilience": {},
  "audit": {}
}
```

## Mandatory top-level fields

| Field | Required | Purpose |
|---|---:|---|
| `envelope_id` | Yes | Unique identifier for this envelope instance. |
| `schema_version` | Yes | Envelope schema version. |
| `created_at` | Yes | Time the envelope was created. |
| `signal` | Yes | Raw or normalized signal content and payload metadata. |
| `source` | Yes | Claimed and observed source context. |
| `provenance` | Yes | Lineage, custody, transformation, and evidence references. |
| `verification` | Yes | Current verification state and supporting details. |
| `resilience` | Yes | Replay, freshness, spoofing, ambiguity, and degraded-mode indicators. |
| `audit` | Yes | Traceability and downstream decision references. |

## Section: `signal`

The `signal` section describes the observed or submitted data without granting trust to it.

### Candidate fields

| Field | Required | Purpose |
|---|---:|---|
| `signal_type` | Yes | Type or class of signal. |
| `payload` | Yes | Raw or normalized payload. |
| `payload_hash` | Recommended | Hash of payload bytes or canonical representation. |
| `payload_encoding` | Recommended | Encoding or serialization format. |
| `observed_at` | Recommended | Time the signal was observed or collected. |
| `declared_at` | Optional | Time claimed by the source, if present. |

### Notes

`observed_at` and `declared_at` are intentionally separate. A claimed timestamp from the source should not be treated as equivalent to an observer timestamp.

## Section: `source`

The `source` section captures claimed and observed origin context.

### Candidate fields

| Field | Required | Purpose |
|---|---:|---|
| `source_id` | Recommended | Identifier for the source, if known. |
| `source_type` | Yes | Human, device, service, sensor, system, feed, or other source type. |
| `claimed_origin` | Optional | Origin claimed by the signal or source. |
| `observed_origin` | Optional | Origin observed by collection infrastructure. |
| `collection_context` | Recommended | How, where, or under what conditions the signal was collected. |

### Notes

When `claimed_origin` and `observed_origin` conflict, the envelope should preserve both and set a corresponding ambiguity or spoofing indicator.

## Section: `provenance`

The `provenance` section records lineage and custody information.

### Candidate fields

| Field | Required | Purpose |
|---|---:|---|
| `provenance_chain` | Recommended | Ordered lineage records. |
| `custody_events` | Optional | Handling, transfer, or custody changes. |
| `transformations` | Optional | Normalization, enrichment, redaction, or conversion steps. |
| `evidence_refs` | Recommended | References to supporting or challenging evidence. |
| `provenance_state` | Yes | `complete`, `partial`, `missing`, `conflicting`, or `unknown`. |

### Notes

`provenance_state` is required even when the chain is unavailable. Missing provenance must be explicit.

## Section: `verification`

The `verification` section describes what has and has not been verified.

### Candidate fields

| Field | Required | Purpose |
|---|---:|---|
| `verification_state` | Yes | Current state of verification. |
| `verification_methods` | Recommended | Methods applied, such as signature check, hash match, source validation, freshness check, or cross-source corroboration. |
| `verified_at` | Optional | Time verification was completed. |
| `verifier_id` | Optional | Actor or system that performed verification. |
| `failure_reasons` | Optional | Structured explanation of failed checks. |
| `confidence` | Optional | Confidence representation, deferred until scoring semantics are defined. |

### Initial verification states

- `unverified`
- `verified`
- `partially_verified`
- `failed`
- `conflicting`
- `unknown`

### Notes

The default state should be `unverified`, not `verified` or `unknown`.

## Section: `resilience`

The `resilience` section makes adversarial and degraded-condition indicators visible.

### Candidate fields

| Field | Required | Purpose |
|---|---:|---|
| `freshness_status` | Yes | Fresh, stale, expired, unknown, or not applicable. |
| `replay_status` | Yes | No replay evidence, suspected replay, confirmed replay, unknown, or not applicable. |
| `spoofing_indicators` | Optional | Structured indicators of source, origin, timing, or metadata spoofing. |
| `ambiguity_flags` | Optional | Parser, schema, semantic, source, or evidence ambiguity. |
| `degraded_mode_flags` | Optional | Any degraded operational conditions that affected collection or verification. |

### Notes

The envelope should not hide degraded mode. A signal accepted during degraded conditions may still be useful, but that status must remain visible downstream.

## Section: `audit`

The `audit` section links envelopes to downstream review and decision context.

### Candidate fields

| Field | Required | Purpose |
|---|---:|---|
| `trace_id` | Recommended | Cross-system trace identifier. |
| `decision_refs` | Optional | Decisions, alerts, classifications, or actions that used this envelope. |
| `audit_notes` | Optional | Human or system-readable notes. |
| `created_by` | Optional | Envelope creator, if available. |

## Required handling semantics

### Missing values

Missing values must be represented explicitly when the missing value affects trust, provenance, verification, freshness, or auditability.

### Unknown values

Unknown means the value is not currently known. Unknown is not the same as missing, failed, or not applicable.

### Conflicting values

Conflicting values should preserve each conflicting claim and indicate the conflict in `verification` or `resilience`.

### Not applicable values

Not applicable should be used only when a field does not apply to the signal class, not when the implementation failed to collect the value.

## Initial test-vector scenarios

The first implementation should include at least these scenarios:

1. **Valid minimal envelope** — required sections and required fields are present.
2. **Missing provenance** — envelope is accepted as structurally valid but marked with `provenance_state: missing` and `verification_state: unverified`.
3. **Stale signal** — signal is structurally valid but marked stale or expired.
4. **Replay suspected** — signal appears to repeat a prior payload or identifier in a suspicious context.
5. **Claimed/observed origin conflict** — source claims one origin while collection context indicates another.
6. **Conflicting evidence** — evidence references disagree and verification state becomes `conflicting`.
7. **Malformed payload hash** — payload hash does not match canonical payload representation.
8. **Degraded-mode collection** — envelope remains usable but carries degraded-mode flags.

## Open decisions

- Choose initial schema technology: JSON Schema, Pydantic, Protocol Buffers, or another representation.
- Define canonical hashing rules for payloads.
- Define envelope ID generation rules.
- Define timestamp precision and clock-skew handling.
- Define confidence representation or explicitly defer it.
- Define rules for versioning and migration.

## Proposed acceptance criteria

This RFC is ready to move from Draft to Accepted when:

- Required top-level fields are confirmed.
- Required fields per section are confirmed.
- Initial verification states are confirmed.
- Missing, unknown, conflicting, and not-applicable semantics are accepted.
- Initial test-vector scenarios are accepted.
- ADR-0002 records the selected schema representation.

## Follow-up work

- Add ADR-0002 for schema representation.
- Add initial schema file.
- Add initial validation fixtures.
- Add tests for the test-vector scenarios.
- Update `docs/threat-model.md` with any new threats discovered during RFC review.