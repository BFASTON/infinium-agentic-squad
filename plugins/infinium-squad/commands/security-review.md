---
description: Run an Infinium security review of the current changes (or a given path)
argument-hint: [path or branch, defaults to current branch changes]
---

Use the `security-reviewer` agent to review the following against the Infinium Security Guide.

Scope: $ARGUMENTS
(If no scope is given above, review the current branch's changes against the default branch, including uncommitted changes.)

Report verified findings by severity with file:line, exploit scenario, fix and guide reference, and finish with a Block / Fix before merge / OK to merge verdict.
