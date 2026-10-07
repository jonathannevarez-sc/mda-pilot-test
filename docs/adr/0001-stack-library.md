# 0001. Stack for library work

Date: 2026-10-07

Status: Accepted. The signed-in person confirmed build_setup for story 1402.

## Decision

This repo is a library project. A Python package with tests. Standard library only.

| | |
|---|---|
| Language | python |
| Framework | none |
| Runtime | none |
| Test | `python3 -m unittest discover -s tests` |
| Build | none |
| Template | none |

## Layout

- <package>/: the module the story changes
- tests/: unittest tests

## Consequences

- Every story in this repo follows `.mda/repo.json`. The build agent reads it before it writes code.
- A new package needs an ADR.
- The agent never deploys. The company pipeline builds, scans, and deploys.
- Changing the stack needs a new ADR and an edit to `.mda/repo.json`.
