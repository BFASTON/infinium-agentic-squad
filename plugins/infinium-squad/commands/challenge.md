---
description: Send the challenger team after existing work - independently validate it, build a competing alternative, and judge the two
argument-hint: [what the change was for] (defaults to the current branch's changes)
---

Load the `challenge-protocol` skill and run its `/challenge` variant, as referee in this main session.

The existing solution is the current branch's changes against the default branch (or the branch or PR named below). Frame the task brief from the description below, the PR description, linked issue or commit subjects, **not from the code**. If there is nothing to go on but the diff, ask me for one sentence on what the change was for.

- The `challenger-lead` agent builds an alternative from the merge base in its own worktree, without ever being shown the existing branch.
- The `challenger-validator` agent validates the existing work; the `qa-engineer` agent validates the alternative. Run the `simplifier` agent on both, and the `security-reviewer` agent where relevant.
- Cross-critique with the `challenger-critic` agent (on the existing work) and the `squad-lead` agent (on the alternative), allow one round of responses, then have the `squad-judge` agent compare the two blind.

Finish with the verdict, a comparison table, the branches to look at and the recommended next step. Do not merge, push or delete anything.

What the change was for: $ARGUMENTS
