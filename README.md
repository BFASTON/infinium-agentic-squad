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
| `frontend-engineer` | UI, components, design systems, accessibility, responsive layout, web performance |
| `python-specialist` | Idiomatic, typed Python: packaging, async, pytest, Python performance |
| `rust-specialist` | Idiomatic Rust: ownership, error handling, async, `unsafe` review, Cargo, performance |
| `sql-specialist` | Writing, reviewing and tuning SQL in any dialect, query plans and indexes |
| `data-engineer` | Schemas, migrations, pipelines, data quality |
| `qa-engineer` | Test strategy, writing tests, reproducing bugs, fixing flaky tests |
| `devops-engineer` | CI/CD, Docker, infrastructure as code, observability |
| `security-reviewer` | Threat models and security reviews (read-only) |
| `code-reviewer` | Correctness and standards review before a PR (read-only) |
| `simplifier` | Flags over-engineering and needless complexity, and proposes (or applies) simpler code |
| `tech-writer` | READMEs, runbooks, API docs, release notes |
| `on-call-engineer` | When a bug, failing build or incident has an unclear cause: triages severity, finds the root cause, fixes it with a regression test and gets it reviewed |

Claude picks the right agent automatically from your request, or you can ask for one by name: *"Use the architect to design a notifications service."*

### The challenger team

A second, independent team whose job is to check the first team's work and build a competing solution, so you can compare two genuinely different answers instead of trusting one.

| Agent | What it does |
|---|---|
| `challenger-lead` | Builds an alternative solution from the task brief alone, deliberately exploring a different approach |
| `challenger-validator` | Independently verifies a solution against the acceptance criteria and tries to break it (read-only) |
| `challenger-critic` | Gives the other team's solution the toughest fair critique, compared with the alternative (read-only) |
| `squad-judge` | Neutral judge: compares both solutions blind on a rubric and gives a verdict (read-only) |

How it stays independent:

- **Separate context.** The challenger team gets only a frozen task brief. It never sees the primary squad's plan, reasoning or code while it builds, and the primary squad isn't told a challenger exists.
- **Separate code.** Each team builds in its own git worktree and branch, from the same base commit.
- **Swap testers.** Each solution is validated by the *other* team's tester (`challenger-validator` checks the squad's work, `qa-engineer` checks the challenger's).
- **Critique only finished work.** Teams see each other's diff and report only after both have committed, then critique each other and get one chance to respond.
- **Blind judging.** The judge sees "Solution 1" and "Solution 2" in random order, with team names removed.

Run it with `/compete` for a new task or `/challenge` for work that's already done. Nothing is merged or pushed; you get a verdict (adopt one, combine named parts of both, or neither), a comparison table and both branches to look at. A run costs roughly two to three times a normal one, so save it for decisions that are high-stakes, hard to reverse, or have several credible approaches. The full procedure is in the [`challenge-protocol` skill](plugins/infinium-squad/skills/challenge-protocol/SKILL.md).

### Slash commands

| Command | What it does |
|---|---|
| `/squad <task>` | Hand a whole task to the squad lead |
| `/design <feature>` | Architect designs it and drafts an ADR if needed |
| `/adr <title>` | Create a new Architecture Decision Record |
| `/review [scope]` | Code review of your current changes |
| `/security-review [scope]` | Security review of your current changes |
| `/ship-check` | Lint, types, tests, both reviews and a PR description: ready or not |
| `/simplify-check [scope] [--apply]` | Find over-engineering in your changes; `--apply` makes the simplifications |
| `/compete <task>` | Squad and challenger team both build it, validate and critique each other, judge picks |
| `/challenge [what it was for]` | Challenger team validates existing work, builds an alternative, judge compares |
| `/oncall <error or symptom>` | On-call engineer triages, investigates to root cause, fixes and reviews |

(If another plugin or a built-in uses the same command name, use the namespaced form, e.g. `/infinium-squad:review`.)

### Company standards

Every agent loads these before working and cites them in its output. The **Agent Instructions** tell agents how to behave, which guide to use and when to hand over; the **Escalation Policy** says when a human is genuinely needed. They live in [`plugins/infinium-squad/skills/infinium-standards/standards/`](plugins/infinium-squad/skills/infinium-standards/standards/):

- [Agent Instructions](plugins/infinium-squad/skills/infinium-standards/standards/agent-instructions.md)
- [Escalation Policy](plugins/infinium-squad/skills/infinium-standards/standards/escalation-policy.md)
- [Security Guide](plugins/infinium-squad/skills/infinium-standards/standards/security-guide.md)
- [Architecture Guide](plugins/infinium-squad/skills/infinium-standards/standards/architecture-guide.md)
- [Coding Standards](plugins/infinium-squad/skills/infinium-standards/standards/coding-standards.md)
- [Testing Standards](plugins/infinium-squad/skills/infinium-standards/standards/testing-standards.md)
- [Git and PR Workflow](plugins/infinium-squad/skills/infinium-standards/standards/git-and-pr-workflow.md)
- [Community Tools Register](plugins/infinium-squad/skills/infinium-standards/standards/community-tools.md)

### Guardrails

A `PreToolUse` hook stops agents reading or writing common secrets files (`.env`, `*.pem`, `*.key`, cloud credentials, Terraform state). `.env.example` style templates are still allowed.

### Autonomy and phone alerts

Agents resolve problems themselves and only ask you when the [Escalation Policy](plugins/infinium-squad/skills/infinium-standards/standards/escalation-policy.md) says a human is genuinely needed (production or irreversible actions, credentials, goal-changing ambiguity, policy decisions, serious security findings, or being truly stuck). They ask in chat. If you set a few environment variables, a `Notification` hook also pushes an alert to your phone through [ntfy](https://ntfy.sh) or [Pushover](https://pushover.net) whenever Claude is waiting for you. Setup: [user guide](docs/USER_GUIDE.md#getting-a-phone-notification-when-the-squad-needs-you). Nothing is sent unless you configure it, and pushes never include code or data.

### Community skills and plugins

The `infinium` marketplace also offers reviewed community tools, all **opt-in** and pinned. See the [Community Tools Register](plugins/infinium-squad/skills/infinium-standards/standards/community-tools.md) for each tool's licence, what it runs, stores and sends, and the guardrails to follow.

| Tool | How to get it | Status |
|---|---|---|
| napkin (curated per-repo runbook) | `/plugin install infinium-extras@infinium` | Opt-in, vendored (MIT) |
| Ponytail (simplest-solution mode) | `/plugin install ponytail@infinium` | Opt-in, pinned to v5.3.3 |
| Graphify (code knowledge graph) | `uv tool install graphifyy==0.9.121` | Opt-in, code-only by default |
| claude-mem (session memory) | Upstream marketplace, with guardrails | Restricted: Internal (C3) work only, telemetry off |
| awesome-design-md | Reference only | `DESIGN.md` examples |
| Agent Skills spec | Enforced by `scripts/validate.py` | Adopted |
| OmniRoute | | Not approved |

## Install

You need Claude Code installed and signed in, and Python 3 on your `PATH` (for the guardrail hook).

In Claude Code, run:

```
/plugin marketplace add BFASTON/infinium-agentic-squad
/plugin install infinium-squad@infinium
```

Restart Claude Code if prompted, then check with `/agents` (you should see the nineteen squad and challenger agents) and `/help` (the commands above).

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
/compete Add rate limiting to the public API
/challenge Replace the nightly invoice sync with change data capture
```

Or just talk to Claude normally. It will hand work to specialists when it fits, and run the code and security reviewers before you open a PR.

## Repository layout

```
.claude-plugin/marketplace.json        Marketplace catalogue (what /plugin marketplace add reads)
plugins/infinium-squad/
  .claude-plugin/plugin.json           Plugin manifest
  agents/                              The squad and challenger team agents
  commands/                            Slash commands
  skills/infinium-standards/           Company standards, loaded by every agent
  skills/challenge-protocol/           How /compete and /challenge run the two teams
  hooks/                               Secret-file guardrail and opt-in phone notifications
plugins/infinium-extras/               Opt-in community skills vendored with their licences (napkin)
templates/CLAUDE.md                    Starter CLAUDE.md for project repos
scripts/validate.py                    Checks manifests, frontmatter and agent/skill references
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
