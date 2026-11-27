---
description: Run an Infinium code review of the current changes before opening a PR
argument-hint: [path or branch, defaults to current branch changes]
---

Use the `code-reviewer` agent to review the following.

Scope: $ARGUMENTS
(If no scope is given above, review the current branch's changes against the default branch, including uncommitted changes.)

If the changes touch authentication, user input, personal data, secrets, dependencies or infrastructure, also run the `security-reviewer` agent in parallel. Combine the results into one prioritised list with a final verdict.
