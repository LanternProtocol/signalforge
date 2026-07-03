# Technical Review Checklist

Use this checklist after a sprint run or repository update.

## Repository checks

- Confirm the target repository is listed in `config/repositories.json`.
- Confirm the default branch is known.
- Confirm open pull requests are reviewed.
- Confirm open sprint issues have measurable tests.

## Change checks

- Confirm the change has a sprint identifier.
- Confirm documentation targets were reviewed.
- Confirm the definition of done is satisfied.

## Test checks

- Run declared automated tests.
- Confirm manual checks have recorded evidence.
- Confirm CI is green before merge.
- Confirm CodeQL or equivalent code scanning is green when applicable.

## Follow-up checks

- Record defects as issues.
- Record missing tests as issues.
- Record missing documentation as issues.
- Record feature research opportunities as issues when no defects are found.
