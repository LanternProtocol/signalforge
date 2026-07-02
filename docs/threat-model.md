# Threat Model

This is the initial SignalForge threat model. It is intentionally broad and should be refined as protocol semantics and implementation details mature.

## Assets to protect

- Signal integrity.
- Source identity and source context.
- Evidence integrity and custody.
- Provenance records.
- Verification results.
- Audit trails.
- Trust decisions and downstream actions.
- Build, dependency, and release chain.

## Adversary capabilities to consider

- Submit forged or manipulated signals.
- Replay old but valid-looking signals.
- Delay, suppress, or reorder signal delivery.
- Spoof source identity, location, timing, or metadata.
- Poison evidence or provenance records.
- Exploit schema ambiguity or parser differences.
- Abuse degraded-mode behavior.
- Introduce malicious dependencies or CI/CD changes.
- Create misleading documentation, examples, or test vectors.

## Initial threat categories

### Spoofing

False source identity, false origin metadata, false sensor context, or false actor attribution.

### Tampering

Modification of signal payloads, evidence, provenance, verification results, or audit logs.

### Replay and staleness

Reuse of previously valid signals in a new context or after expiration.

### Ambiguity exploitation

Abuse of undefined fields, conflicting semantics, parser disagreement, optional metadata, or silent defaults.

### Provenance forgery

Fabrication or alteration of lineage, custody, transformations, or supporting evidence.

### Degraded-mode abuse

Forcing the system into fallback behavior that relaxes validation or trust requirements.

### Supply-chain compromise

Malicious or vulnerable dependencies, build steps, CI workflows, release artifacts, or maintainer credentials.

## Required design posture

- Unverified data must remain distinguishable from verified data.
- Missing provenance must not silently become acceptable provenance.
- Confidence and uncertainty should be explicit.
- Replay, freshness, and context should be considered before trust decisions.
- Security-sensitive code paths should be owned and reviewed deliberately.
- Test vectors should include adversarial and malformed cases, not only happy paths.

## Open questions

- What metadata is mandatory for each signal class?
- What expiration, freshness, or replay protections are required?
- What verification failures are hard failures versus warning states?
- How should conflicting evidence be represented?
- How should emergency-condition behavior differ from normal operation?