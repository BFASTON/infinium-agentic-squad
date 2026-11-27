# Infinium Agentic Squad

A shared team of specialist [Claude Code](https://code.claude.com/docs) agents, plus Infinium's company-wide engineering standards, packaged as a Claude Code plugin. Install it once and every developer at Infinium works with the same squad, following the same Security Guide, Architecture Guide and coding standards.

**New here?** Read the [Staff User Guide](docs/USER_GUIDE.md): getting a Claude licence, installing the squad, using the agents and commands, and pushing code to Infinium's Azure DevOps repos.

## What you get

### The squad

| Agent | What it does |
|---|---|
| `squad-lead` | Plans multi-step work and delegates to the right specialists, then gates it through review |
| `architect` | System and feature design, trade-offs, API/event contracts, ADRs |
| `backend-engineer` | APIs, services, business logic, integrations |
| `frontend-engineer` | UI, components, accessibility, client performance |
| `data-engineer` | Schemas, migrations, queries, pipelines, data quality |
| `qa-engineer` | Test strategy, writing tests, reproducing bugs, fixing flaky tests |
| `devops-engineer` | CI/CD, Docker, infrastructure as code, observability |
| `security-reviewer` | Threat models and security reviews (read-only) |
| `code-reviewer` | Correctness and standards review before a PR (read-only) |
| `tech-writer` | READMEs, runbooks, API docs, release notes |

Claude picks the right agent automatically from your request, or you can ask for one by name: *"Use the architect to design a notifications service."*

### Slash commands

| Command | What it does |
|---|---|
| `/squad <task>` | Hand a whole task to the squad lead |
| `/design <feature>` | Architect designs it and drafts an ADR if needed |
| `/adr <title>` | Create a new Architecture Decision Record |
| `/review [scope]` | Code review of your current changes |
| `/security-review [scope]` | Security review of your current changes |
| `/ship-check` | Lint, types, tests, both reviews and a PR description: ready or not |

(If another plugin uses the same command name, use the namespaced form, e.g. `/infinium-squad:review`.)

### Company standards

Every agent loads these before working and cites them in its output. They live in [`plugins/infinium-squad/skills/infinium-standards/standards/`](plugins/infinium-squad/skills/infinium-standards/standards/):

- [Security Guide](plugins/infinium-squad/skills/infinium-standards/standards/security-guide.md)
- [Architecture Guide](plugins/infinium-squad/skills/infinium-standards/standards/architecture-guide.md)
- [Coding Standards](plugins/infinium-squad/skills/infinium-standards/standards/coding-standards.md)
- [Testing Standards](plugins/infinium-squad/skills/infinium-standards/standards/testing-standards.md)
- [Git and PR Workflow](plugins/infinium-squad/skills/infinium-standards/standards/git-and-pr-workflow.md)

### Guardrails

A `PreToolUse` hook stops agents reading or writing common secrets files (`.env`, `*.pem`, `*.key`, cloud credentials, Terraform state). `.env.example` style templates are still allowed.

## Install

You need Claude Code installed and signed in, and Python 3 on your `PATH` (for the guardrail hook).

In Claude Code, run:

```
/plugin marketplace add BFASTON/infinium-agentic-squad
/plugin install infinium-squad@infinium
```

Restart Claude Code if prompted, then check with `/agents` (you should see the ten squad agents) and `/help` (the commands above).

### Install for a whole repository

To have the squad offered automatically to everyone who opens a project, add this to the project's `.claude/settings.json` and commit it:

```json
{
  "extraKnownMarketplaces": {
    "infinium": {
      "source": { "source": "github", "repo": "BFASTON/infinium-agentic-squad" }
    }
  },
  "enabledPlugins": {
    "infinium-squad@infinium": true
  }
}
```

Then copy [`templates/CLAUDE.md`](templates/CLAUDE.md) into the project root and fill it in, so the squad knows the project's stack, commands and any stricter local rules.

### Update

```
/plugin marketplace update infinium
```

## Using the squad

```text
/squad Add CSV export to the invoices page, with an API endpoint and tests
/design Move order notifications to an event-driven model
/review
/ship-check
```

Or just talk to Claude normally. It will hand work to specialists when it fits, and run the code and security reviewers before you open a PR.

## Repository layout

```
.claude-plugin/marketplace.json        Marketplace catalogue (what /plugin marketplace add reads)
plugins/infinium-squad/
  .claude-plugin/plugin.json           Plugin manifest
  agents/                              The ten squad agents
  commands/                            Slash commands
  skills/infinium-standards/           Company standards, loaded by every agent
  hooks/                               Secret-file guardrail
templates/CLAUDE.md                    Starter CLAUDE.md for project repos
scripts/validate.py                    Checks manifests and agent/command frontmatter
.github/workflows/                     CI: validation and secret scanning
```

## Filling in Infinium-specific policy

This repo is designed to be shareable, so it contains **no secrets and no confidential company details**. Wherever company-specific policy is needed there is a `TODO(infinium): ...` placeholder with a sensible default next to it. Agents apply the default and flag that the policy is unconfirmed.

To list every placeholder:

```bash
grep -rn "TODO(infinium)" plugins/ templates/
```

Before filling one in, check that the information is safe to publish at this repo's visibility. Internal hostnames, customer names, network ranges, and anything classified Confidential or above should stay out (see the Security Guide §2).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: open a PR, keep agents focused on one speciality, change standards through review with the owning team, and run `python3 scripts/validate.py` before pushing.

To report a security issue with this repo, see [SECURITY.md](SECURITY.md).
