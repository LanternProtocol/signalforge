# Sprint Contract

A SignalForge sprint is eligible for selection only when it is measurable.

## Required sprint fields

Each sprint in `config/sprints.json` must define an identifier, repository name, title, priority, status, area, labels, completion tests, documentation targets, and definition of done.

## Completion tests

Every sprint must include at least one completion test.

Supported test types are automated test, documentation review, manual file check, manual GitHub setting check, and manual issue check.

Automated tests must define a command. Manual tests must define the required evidence.

## Definition of done

A sprint is done only when its completion tests have passed or their required evidence is recorded, its documentation targets have been updated or reviewed, CI and review gates are satisfied, and the default branch is confirmed current after completion.

## Selection command

Use the sprint selector to view the next sprint set:

```bash
python scripts/next_sprints.py --run-id 20260703T0000Z --output markdown
```

The generated label format is `run:RUNID:REPO-SLUG:SPRINT-ID`.
