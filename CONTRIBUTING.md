# Contributing to SignalForge

SignalForge changes should be small, reviewable, and explicit about protocol and security impact.

## Before coding

Open or reference an issue when the change affects:

- Protocol behavior or semantics.
- Evidence, provenance, verification, or auditability.
- Threat boundaries or adversarial assumptions.
- Build, dependency, release, or deployment behavior.

## Pull requests

Each pull request should include:

1. Summary of the change.
2. Motivation.
3. Validation performed.
4. Protocol impact.
5. Security impact.
6. Documentation impact.

## Review expectations

Maintainers may block changes that lack tests, omit threat-model considerations, weaken auditability, introduce ambiguous semantics, or combine unrelated work into a single pull request.

## Documentation-first areas

For protocol, trust, provenance, and verification behavior, update documentation and/or ADRs alongside code.