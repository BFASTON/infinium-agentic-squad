---
description: Run two independent teams on one task, have them validate and critique each other, and get a judged verdict
argument-hint: <what you want built or fixed>
---

Load the `challenge-protocol` skill and run the full protocol on the task below, as referee in this main session.

- Team A is the `squad-lead` agent; Team B is the `challenger-lead` agent. They build in separate git worktrees from the same base commit, in parallel, and Team B never sees Team A's plan, reasoning or code until both have committed.
- Validate each solution with the other team's tester (`challenger-validator` for Team A, `qa-engineer` for Team B), run the `simplifier` agent on both, and the `security-reviewer` agent where relevant.
- Cross-critique with the `challenger-critic` agent (on Team A) and the `squad-lead` agent (on Team B), allow one round of responses, then have the `squad-judge` agent compare the two blind.

Finish with the verdict, a comparison table, the branches to look at and the recommended next step. Do not merge, push or delete anything.

Task: $ARGUMENTS
