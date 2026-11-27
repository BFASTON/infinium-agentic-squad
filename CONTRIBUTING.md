# Contributing to the Infinium Agentic Squad

Thanks for helping improve the squad. Every change here affects every developer who has the plugin installed, so changes go through PR review.

## Ground rules

1. **Never add secrets or confidential details.** No credentials, internal hostnames, IP ranges, customer names or confidential policy text. Use a `TODO(infinium): ...` placeholder instead.
2. **One speciality per agent.** Improve an existing agent before adding a new one. A new agent needs a clear, non-overlapping job and a `description` that tells Claude exactly when to use it.
3. **Standards are owned.** Changes to the Security Guide need approval from the security owner; changes to the Architecture Guide from the architecture owner (see each guide's header). Keep section numbers stable, because agents cite them; add new sections at the end of a chapter.
4. **Agents reference standards, they don't copy them.** Put rules in `skills/infinium-standards/standards/` and point to them from agents, so there's one source of truth.
5. **Community tools are pinned and registered.** Any third-party skill or plugin must be listed in the [Community Tools Register](plugins/infinium-squad/skills/infinium-standards/standards/community-tools.md) and, if it's in the marketplace, pinned to a full commit `sha` (the validator enforces this). Vendor files into `plugins/infinium-extras/` only when the licence allows it and they contain no executable code; keep the upstream licence beside them and record the commit in `plugins/infinium-extras/THIRD_PARTY_NOTICES.md`. Anything that runs code, stores session data or uses the network needs the security owner's approval.
6. **Test it.** Install your branch locally and try the agent or command on a real task before opening the PR.

## Trying a change locally

```bash
git clone https://github.com/BFASTON/infinium-agentic-squad
cd infinium-agentic-squad
python3 scripts/validate.py
```

Then in Claude Code:

```
/plugin marketplace add ./path/to/infinium-agentic-squad
/plugin install infinium-squad@infinium
```

After editing files, run `/plugin marketplace update infinium` and restart Claude Code to pick up changes.

## File formats

- **Agents** (`plugins/infinium-squad/agents/*.md`): YAML frontmatter with `name`, `description`, optional `tools` (comma-separated; omit to inherit all tools) and `model` (`inherit`, `sonnet`, `opus` or `haiku`), then the system prompt.
- **Commands** (`plugins/infinium-squad/commands/*.md`): frontmatter with `description` and optional `argument-hint`; `$ARGUMENTS` is replaced by what the user types.
- **Versioning**: bump `version` in both `plugins/infinium-squad/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` for any user-visible change, following semantic versioning.

## Commit and PR conventions

Follow the [Git and PR Workflow](plugins/infinium-squad/skills/infinium-standards/standards/git-and-pr-workflow.md): Conventional Commits, small PRs, squash merge.
