# GitHub Repository Controls

This document records repository-admin controls recommended for `LanternProtocol/signalforge`.

Some controls are GitHub settings rather than repository files. They must be configured by a repository or organization administrator in GitHub.

## Branch protection or ruleset for `main`

Recommended controls:

- Require pull request before merging.
- Require at least one approval.
- Dismiss stale approvals when new commits are pushed.
- Require conversation resolution before merge.
- Require status checks to pass before merge.
- Require the `CI / Repository baseline` check.
- Require the `CI / Python validation` check.
- Require signed commits when compatible with maintainer workflow.
- Block force pushes.
- Block branch deletion.
- Restrict bypass permissions to emergency maintainers only.

## Security controls

Recommended repository security settings:

- Enable Dependabot alerts.
- Enable Dependabot security updates.
- Enable secret scanning.
- Enable push protection.
- Enable private vulnerability reporting.
- Enable code scanning alerts.
- Keep default GitHub Actions workflow permissions read-only where possible.

## File-backed controls already present

The repository includes these file-backed controls:

- `.github/CODEOWNERS`
- `.github/dependabot.yml`
- `.github/workflows/ci.yml`
- `.github/workflows/codeql.yml`
- `SECURITY.md`
- `NOTICE`
- `LICENSE`

## Verification checklist

After configuring repository settings, verify:

- Direct pushes to `main` are blocked.
- Pull requests without passing checks cannot merge.
- Pull requests with unresolved conversations cannot merge.
- Dependabot can open dependency update pull requests.
- Private vulnerability reporting is visible from the repository Security tab.
