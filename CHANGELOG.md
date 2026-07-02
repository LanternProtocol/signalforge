# Changelog

All notable changes to SignalForge will be documented in this file.

This project is in early formation and has not published a stable release.

## Unreleased

### Added

- Repository governance baseline.
- Initial security, contribution, roadmap, architecture, protocol overview, and threat-model documentation.
- ADR-0002 selecting JSON Schema 2020-12 plus Pydantic v2 as the initial schema representation.
- Machine-readable Signal Envelope JSON Schema.
- Python package scaffold and Pydantic models.
- Provisional canonical payload hashing helpers.
- Validation harness for schema, Pydantic, and payload-hash semantic checks.
- Test vectors for valid, missing-provenance, stale, replay, origin-conflict, conflicting-evidence, hash-mismatch, and degraded-mode envelopes.
- RFC-0002 for canonical payload hashing, timestamp handling, and replay/freshness semantics.
- Apache-2.0 code license, CC-BY-4.0 documentation notice, and trademark reservation NOTICE.
- Repository-admin checklist for main-branch rulesets and GitHub security controls.

### Changed

- Expanded README from placeholder to project baseline.
- Updated README with schema, validation, and license guidance.
- Updated CI to run repository checks, Ruff, the vector validation harness, and pytest.
- Updated Dependabot configuration for Python dependency monitoring.
- Switched code license posture from MIT to Apache-2.0.

### Security

- Added security reporting policy and initial security-sensitive contribution expectations.
- Added file-backed support for CodeQL, Dependabot, CI validation, and CODEOWNERS.
