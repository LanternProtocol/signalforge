# Architecture

This document captures the initial architecture posture for SignalForge. It will evolve as the project moves from protocol framing into implementation.

## Architectural goals

- Keep protocol semantics separate from implementation convenience.
- Keep evidence, provenance, verification, and decisions distinguishable.
- Make adversarial assumptions visible in docs and tests.
- Prefer deterministic validation behavior where possible.
- Avoid hidden trust upgrades caused by missing metadata or implicit defaults.

## Initial repository layers

```text
signalforge
├─ docs/                  # Protocol, architecture, threat model, ADRs
├─ .github/               # Repository automation and ownership
├─ src/                   # Future implementation
└─ tests/                 # Future tests, fixtures, and adversarial cases
```

## Expected implementation boundaries

Future code should separate:

- **Parsing** — accepts and validates input formats.
- **Normalization** — converts inputs into internal signal structures.
- **Provenance capture** — records origin, custody, transformations, and context.
- **Verification** — evaluates integrity, freshness, consistency, and trust assumptions.
- **Decision support** — produces outputs without hiding uncertainty or evidence gaps.
- **Audit output** — exposes enough information to reproduce or challenge decisions.

## Non-goals for early versions

- Production deployment.
- Stable protocol guarantee.
- Broad integration surface.
- Automatic trust decisions without explainability.
- Silent fallback from verified to unverified data.

## Architecture decision records

Use `docs/decisions/` for decisions that affect protocol behavior, security posture, data model, repository structure, or long-term maintainability.