---
name: challenge-protocol
description: How to run Infinium's two-team challenge, where the primary squad and an independent challenger team solve the same task, validate and critique each other, and a neutral judge picks the winner. Load when running /compete or /challenge, or when asked to get a competing or independent alternative solution.
---

# Challenge protocol

Two teams solve one task. **Team A** is the primary squad (`squad-lead` and its specialists). **Team B** is the challenger team (`challenger-lead`, `challenger-validator`, `challenger-critic`). The **judge** (`squad-judge`) belongs to neither. You, the main session, are the **referee**: you run the phases below, carry information between them, and enforce isolation. Do the orchestration yourself in the main session; don't hand it to a subagent, because subagents may not be able to start other subagents.

## Why isolation matters

The value of a second team is a second, *uncorrelated* opinion. If Team B sees Team A's plan, reasoning or code before it has built its own solution, it anchors on it and the comparison is worthless. So:

- **Context isolation.** Each agent starts with a fresh context. Give Team B only the frozen brief, never Team A's plan, transcript, summary or code, and vice versa. Don't tell Team A a challenger exists.
- **Filesystem isolation.** Each team builds in its own git worktree on its own branch, from the same base commit.
- **Information is released in one direction, at one time.** Teams see each other's *finished output* (diff and report) only in the critique phase, after both have committed. Reasoning transcripts are never shared.
- **Blind judging.** The judge sees the two solutions as "Solution 1" and "Solution 2" in random order, with team names removed from everything you pass it.

## Phase 0: Frame

1. Write the **frozen brief**: goal, acceptance criteria (testable), constraints, out of scope, and the base commit. Write it from the user's request (and, for `/challenge`, from the PR description, linked issue or commit subjects), **never from the existing solution's code**. Where something is ambiguous, leave it ambiguous rather than resolving it with knowledge of one team's work.
2. Pick a short kebab-case `<slug>` for the task.
3. Tell the user, in two lines, the brief and that a challenge run costs roughly two to three times a normal run. Then proceed; don't wait unless the brief is too vague to build from.
4. If the working tree has uncommitted changes that the run depends on, stop and ask the user to commit or stash them, because worktrees are created from commits.

## Phase 1: Build (independently, in parallel)

Create one worktree per team that needs to build, both from the base commit. Prefer the Agent tool's worktree isolation and record the path and branch it returns. If that isn't available, create them yourself:

```bash
git worktree add ../<repo>-<slug>-a -b compete/<slug>-a <base>   # Team A (compete only)
git worktree add ../<repo>-<slug>-b -b compete/<slug>-b <base>   # Team B
```

Start both builds in the same turn so they run in parallel:

- **Team A**: the `squad-lead` agent with the brief and its worktree path. Brief it exactly as `/squad` would, and ask it to commit its work on its branch.
- **Team B**: the `challenger-lead` agent with the brief, its worktree path and base commit, and nothing else.

Wait for both to finish. If either fails to produce a committed solution, report that and stop rather than judging a half-built entry.

## Phase 2: Validate and review (in parallel)

Each solution is validated by the *other* team's tester, with only the brief and the solution:

- Team A's solution: `challenger-validator`
- Team B's solution: `qa-engineer` (ask it to verify the solution against the brief's acceptance criteria and try to break it, without editing the solution's code)

Also run `simplifier` on each solution (review only), and `security-reviewer` on each if the task touches auth, user input, personal data, secrets, dependencies or infrastructure.

## Phase 3: Cross-critique (in parallel)

Now, and only now, each team sees the other's finished output: the diff against the base commit (`git diff <base>..compete/<slug>-x`) and that team's report.

- **Team B critiques A**: `challenger-critic` with the brief, Team A's diff and report, Team A's validation report, and Team B's own diff and report.
- **Team A critiques B**: `squad-lead` with the brief, Team B's diff and report, Team B's validation report, and Team A's own diff and report. Ask it for a fair, evidence-based critique in the same shape as the `challenger-critic` output (steelman, then `fatal:`/`major:`/`minor:`/`question:` findings, then a head-to-head comparison).

## Phase 4: Respond (one round, in parallel)

Give each lead the critique and validation report of its *own* solution and ask for a short response: concede, or dispute with evidence. No code changes in this round, so the judge compares what was actually built. (The winning team fixes its accepted defects after the verdict.)

## Phase 5: Judge

Randomly assign the two solutions to "Solution 1" and "Solution 2". Strip team names and agent names from every document. Give `squad-judge` the brief, both solutions' worktree paths and diffs, and for each: its report, validation report, simplicity review, security findings, the critique it received and its response.

## Phase 6: Report to the user

Lead with the verdict, mapped back to team names. Then: a short comparison table, the strongest point each side made and whether the judge upheld it, the branches and worktree paths, and the recommended next step (for example "open a PR from `compete/<slug>-b`, after fixing the two defects the validator found").

Never merge, push, open a PR or delete a branch or worktree without the user asking. Tell them how to clean up: `git worktree remove <path>` and `git branch -D <branch>`.

## `/challenge`: challenging work that already exists

When Team A's solution already exists (the current branch, or a branch or PR the user names), skip Team A's build:

- Team A's solution is that branch as it stands. Its base is the merge base with the default branch.
- Frame the brief from the user's words, the PR description, linked issue or commit subjects, not from the diff. If there is nothing but the diff, ask the user for one sentence on what the change was for.
- Team B builds from the merge base in `challenge/<slug>-b`, without ever being shown the existing branch.
- Team A's report for the critique and judging phases is the PR description or a factual summary of the diff you write *after* Team B has committed.
- Then run Phases 2 to 6 as above. In Phase 3 and 4, `squad-lead` speaks for Team A.
