---
description: Check the current changes for over-engineering and needless complexity, and optionally simplify them
argument-hint: [path or branch] [--apply]
---

Use the `simplifier` agent on the following.

Scope: $ARGUMENTS
(If no path or branch is given above, review the current branch's changes against the default branch, including uncommitted changes.)

Report a verdict (Lean / Some fat / Over-engineered) and findings ranked by payoff. Only if `--apply` appears in the scope above, apply the `simplify:` findings one at a time, running the project's formatter, linter, type checker and tests after each and reverting any step that breaks them. Never change behaviour or delete tests.
