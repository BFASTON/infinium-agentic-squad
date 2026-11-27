---
description: Check the current branch is ready to ship against Infinium's Definition of Done
---

Check whether the current branch is ready to open or merge a PR, against Infinium's Definition of Done (Coding Standards §7) and Git and PR Workflow §3.

1. Run the project's formatter check, linter, type checker and test suite (find the commands in the README, package scripts, Makefile or CI config). Report pass/fail with the failing output.
2. In parallel, run the `code-reviewer` and `security-reviewer` agents on the branch's changes.
3. Check that docs, API specs, migrations and the changelog were updated where behaviour changed, and that no secrets or debug code were added.
4. Check commit messages follow Conventional Commits and the branch name follows `type/short-description`.
5. Draft a PR description: what and why, how it was tested, risks and rollback.

Finish with a checklist of each item as done or not done, and a clear Ready / Not ready verdict.
