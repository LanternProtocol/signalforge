# Security Policy

SignalForge is security-sensitive by design. Treat issues involving trust decisions, provenance, evidence integrity, spoofing, replay, downgrade behavior, secrets, dependencies, build systems, and deployment paths as potentially security-relevant.

## Reporting security issues

Do not open a public issue for active vulnerabilities, exploit details, secrets, or sensitive operational findings.

Use GitHub private vulnerability reporting or a private maintainer channel when available.

## Include in reports

- Affected commit, branch, release, or component.
- Description of the vulnerability or failure mode.
- Preconditions and attacker capabilities.
- Reproduction steps or proof-of-concept, if safe to share.
- Impact on confidentiality, integrity, availability, provenance, evidence validity, or trust decisions.
- Suggested mitigation, if known.

## In-scope examples

- Evidence or provenance forgery.
- Replay, spoofing, downgrade, or ambiguity attacks.
- Unsafe parsing or schema validation behavior.
- Authentication, authorization, or secret-handling failures.
- CI/CD, dependency, or release-chain weaknesses.
- Behavior that causes unsafe trust decisions under degraded or adversarial conditions.

## Researcher conduct

Do not perform destructive testing, unauthorized access, persistence, lateral movement, data exfiltration, or denial-of-service testing.