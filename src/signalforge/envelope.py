"""Pydantic models for the SignalForge Signal Envelope."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

SourceType = Literal["human", "device", "service", "sensor", "system", "feed", "other"]
ProvenanceState = Literal["complete", "partial", "missing", "conflicting", "unknown"]
VerificationState = Literal[
    "unverified", "verified", "partially_verified", "failed", "conflicting", "unknown"
]
FreshnessStatus = Literal["fresh", "stale", "expired", "unknown", "not_applicable"]
ReplayStatus = Literal[
    "no_replay_evidence", "suspected_replay", "confirmed_replay", "unknown", "not_applicable"
]
SCHEMA_VERSION_PATTERN = r"^v[0-9]+(\.[0-9]+){0,2}(-[A-Za-z0-9.-]+)?$"


class StrictModel(BaseModel):
    """Base model that rejects unexpected fields."""

    model_config = ConfigDict(extra="forbid")


class SignalSection(StrictModel):
    signal_type: str = Field(min_length=1)
    payload: Any
    payload_hash: str | None = Field(default=None, pattern=r"^sha256:[a-f0-9]{64}$")
    payload_encoding: str | None = Field(default=None, min_length=1)
    observed_at: datetime | None = None
    declared_at: datetime | None = None


class SourceSection(StrictModel):
    source_type: SourceType
    source_id: str | None = Field(default=None, min_length=1)
    claimed_origin: str | None = None
    observed_origin: str | None = None
    collection_context: dict[str, Any] | None = None


class ProvenanceSection(StrictModel):
    provenance_state: ProvenanceState
    provenance_chain: list[dict[str, Any]] | None = None
    custody_events: list[dict[str, Any]] | None = None
    transformations: list[dict[str, Any]] | None = None
    evidence_refs: list[str] | None = None


class VerificationSection(StrictModel):
    verification_state: VerificationState
    verification_methods: list[str] | None = None
    verified_at: datetime | None = None
    verifier_id: str | None = Field(default=None, min_length=1)
    failure_reasons: list[str] | None = None
    confidence: float | str | dict[str, Any] | None = None


class ResilienceSection(StrictModel):
    freshness_status: FreshnessStatus
    replay_status: ReplayStatus
    spoofing_indicators: list[str] | None = None
    ambiguity_flags: list[str] | None = None
    degraded_mode_flags: list[str] | None = None


class AuditSection(StrictModel):
    trace_id: str | None = Field(default=None, min_length=1)
    decision_refs: list[str] | None = None
    audit_notes: str | list[Any] | dict[str, Any] | None = None
    created_by: str | None = Field(default=None, min_length=1)


class SignalEnvelope(StrictModel):
    envelope_id: str = Field(min_length=1)
    schema_version: str = Field(pattern=SCHEMA_VERSION_PATTERN)
    created_at: datetime
    expires_at: datetime | None = None
    signal: SignalSection
    source: SourceSection
    provenance: ProvenanceSection
    verification: VerificationSection
    resilience: ResilienceSection
    audit: AuditSection
