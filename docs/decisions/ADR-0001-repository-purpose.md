# ADR-0001: Repository purpose

## Status

Accepted

## Context

SignalForge is the first implementation workspace for Lantern Protocol concepts. The repository needs a clear boundary before implementation work begins so that protocol design, security assumptions, and implementation details do not collapse into undocumented code.

## Decision

SignalForge will serve as the early reference workspace for:

- Protocol framing and vocabulary.
- Threat modeling.
- Evidence and provenance handling patterns.
- Verification behavior experiments.
- Implementation scaffolding and validation.

SignalForge is not yet a stable protocol specification or production deployment target.

## Consequences

- Protocol-impacting work should be documented before or alongside code.
- Security and adversarial-resilience considerations are part of normal review, not optional hardening.
- The repository may contain experiments, but experiments must be labeled and should not be confused with stable behavior.
- Future repositories may split specification, reference implementation, integrations, and deployment assets once boundaries are mature.