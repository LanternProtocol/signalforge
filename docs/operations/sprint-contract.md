# Sprint Contract

A SignalForge sprint is eligible for selection only when it is measurable.

## Required fields

Each sprint in `config/sprints.json` must define an identifier, repository name, title, priority, status, area, labels, completion tests, documentation targets, and definition of done.

## Completion tests

Every sprint must include at least one completion test.

Automated tests must define a command. Manual tests must define the required evidence.

## Definition of done

A sprint is done only when its completion tests have passed or their required evidence is recorded, documentation has been updated or reviewed, CI and review gates are satisfied, and the default branch is current after completion.
