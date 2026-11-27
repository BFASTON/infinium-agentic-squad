# Infinium Agentic Squad: Staff User Guide

This guide is for everyone at Infinium who writes, reviews or ships code with Claude Code. It covers:

1. [What the squad is](#1-what-the-squad-is)
2. [Getting a Claude licence for Claude Code](#2-getting-a-claude-licence-for-claude-code)
3. [Installing Claude Code and signing in](#3-installing-claude-code-and-signing-in)
4. [Getting access to the squad and installing it](#4-getting-access-to-the-squad-and-installing-it)
5. [Using the agents and commands](#5-using-the-agents-and-commands)
6. [Connecting a project to Azure DevOps and pushing code](#6-connecting-a-project-to-azure-devops-and-pushing-code)
7. [Rules of the road](#7-rules-of-the-road)
8. [Troubleshooting and getting help](#8-troubleshooting-and-getting-help)

Anything marked `TODO(infinium)` is an internal detail still to be confirmed. Ask your team lead until it is filled in.

---

## 1. What the squad is

The Infinium Agentic Squad is a **Claude Code plugin** that gives every developer the same team of specialist AI agents, all working to Infinium's own engineering standards. Install it once and Claude Code knows how Infinium designs, builds, tests, secures and reviews software.

### What was built

| Part | What it gives you |
|---|---|
| **14 specialist agents** | Squad lead, architect, backend, frontend, Python, Rust, SQL, data, QA, DevOps, security reviewer, code reviewer, simplifier and tech writer |
| **Challenger team** | 3 challenger agents and a neutral judge that independently check the squad's work, build a competing solution and compare the two |
| **9 slash commands** | `/squad`, `/design`, `/adr`, `/review`, `/security-review`, `/ship-check`, `/simplify-check`, `/compete`, `/challenge` |
| **Infinium standards** | Security Guide, Architecture Guide, Coding Standards, Testing Standards, Git and PR Workflow. Every agent loads these before it works and cites them in its output |
| **Secret-file guardrail** | A hook that stops agents reading or writing `.env` files, private keys, cloud credentials and Terraform state |
| **Project template** | A starter `CLAUDE.md` that tells the squad about a project's stack, commands and local rules |
| **CI checks** | Manifest validation and secret scanning on every change to the squad itself |

The standards also set Infinium-wide defaults such as using **Azure Key Vault** for secrets and the **C-level data classification** scheme (for example C3 = Internal). See the [Security Guide](../plugins/infinium-squad/skills/infinium-standards/standards/security-guide.md).

The squad is distributed from the GitHub repository `BFASTON/infinium-agentic-squad`. `TODO(infinium): update this location if the repo moves to an Infinium organisation.`

---

## 2. Getting a Claude licence for Claude Code

Claude Code needs a paid Claude account. The free claude.ai plan does not include Claude Code. At Infinium we use a **business plan** (Claude Team or Claude Enterprise), so your licence is a **seat** in Infinium's Claude organisation, paid for centrally. Do not buy a personal Pro or Max plan for company work, and do not share a seat: each seat belongs to one named person.

### For staff: how to get a seat

1. Ask for a seat through `TODO(infinium): request route, e.g. IT service desk form or ticket queue`.
   Include your name, work email, team, and whether you expect heavy daily use (this decides the seat type, see below).
2. Your request is approved by `TODO(infinium): approver, e.g. line manager plus Engineering/IT budget owner`.
3. You receive an email invitation to Infinium's Claude organisation. Accept it **with your Infinium work email**.
   `TODO(infinium): if SSO is enabled, note "sign in with Microsoft/Entra SSO" here.`
4. Install Claude Code and sign in (section 3).

### Seat types

Claude Team plans have two seat types:

| Seat | What it includes |
|---|---|
| **Standard** | Claude on the web, desktop and mobile, plus Claude Code, with standard usage limits |
| **Premium** | Everything in Standard, with higher usage limits |

Anthropic's current help article says Standard seats include Claude Code access. Older (2025) announcements said Claude Code came with Premium seats, so check the current terms when buying. If you regularly hit usage limits, ask for a Premium seat or for extra usage to be enabled on your account. `TODO(infinium): Infinium's default seat type for engineers.`

### For Claude admins: buying and assigning seats

Only **Owners / Primary Owners** can buy seats and see billing. **Admins and above** can assign seat types. In claude.ai:

- **Buy seats:** Organization settings > Organization and access > **Total seats: Manage** > **Add or change seats** > `+` next to Standard or Premium > **Next** > confirm > **Confirm & purchase**. New seats are prorated and charged straight away.
- **Invite people:** add members from the admin dashboard (Organization settings > Members). Pending invitations count toward the seat limit.
- **Change a seat type:** Organization settings > Members > **Tier** dropdown > Standard or Premium. If the plan has no Premium seats yet, buy one first. Upgrades are prorated and charged immediately; downgrades take effect at renewal.
- **Free a seat:** set the member to **No seat assigned**. Removing seats lowers the bill only from the next renewal; there are no prorated refunds.
- **SSO and provisioning:** Team includes SSO; Enterprise adds domain capture, role-based permissions and the Compliance API. Users created by JIT/SCIM provisioning get the highest available seat type unless group mappings say otherwise.
- **Keep Claude Code on the company account:** use managed settings to set `forceLoginMethod` to `"claudeai"` and `forceLoginOrgUUID` to Infinium's organisation ID (shown in claude.ai admin settings under Organization). Claude Code then refuses logins to any other organisation.

Sources (checked November 2026): [Purchase and manage seats on Team plans](https://support.claude.com/en/articles/12004354-how-to-purchase-and-manage-premium-seats), [Claude Code authentication](https://code.claude.com/docs/en/authentication), [Claude Code on Team and Enterprise](https://www.anthropic.com/news/claude-code-on-team-and-enterprise). Prices are on [claude.com/pricing](https://claude.com/pricing). These pages change, so check them before quoting terms.

---

## 3. Installing Claude Code and signing in

1. **Install Claude Code** using the command for your system from the official [setup page](https://code.claude.com/docs/en/setup). Package-manager options include Homebrew on macOS (`brew install --cask claude-code`) and WinGet on Windows (`winget install Anthropic.ClaudeCode`). You need macOS 13+, Windows 10 1809+ or a recent Linux, and 4 GB+ RAM. On Windows, install [Git for Windows](https://git-scm.com/download/win) too: Claude Code uses it, and it includes Git Credential Manager (section 6).
   `TODO(infinium): note if IT deploys Claude Code through Intune/Company Portal instead.`
2. **Check it:** `claude --version`. If anything looks wrong, run `claude doctor`.
3. **Sign in:** run `claude` in a terminal. A browser window opens. Choose to log in with your **Claude account (claude.ai)** and use the Infinium work account you were invited with. Do not choose Console / API key unless you have been told to.
   - If the browser does not open, press `c` to copy the login URL and paste it into a browser.
   - On WSL, SSH or containers you may be shown a code to paste back into the terminal.
4. Use `/login` to switch account or renew a login, and `/logout` to sign out.

If you have `ANTHROPIC_API_KEY` set in your shell from earlier experiments, Claude Code will use it instead of your seat. Run `unset ANTHROPIC_API_KEY` (and remove it from your shell profile) so usage goes through Infinium's plan.

---

## 4. Getting access to the squad and installing it

### Access

You need read access to the squad's GitHub repository.
`TODO(infinium): while the repo is in a personal account it must be shared with you; once it moves to an Infinium GitHub org, access will come through org membership. Say how to request it.`

You also need **Python 3** on your `PATH`, because the secret-file guardrail is a small Python script.

### Install for yourself

In Claude Code run:

```
/plugin marketplace add BFASTON/infinium-agentic-squad
/plugin install infinium-squad@infinium
```

Restart Claude Code if asked, then check:

- `/agents` lists the eighteen squad and challenger agents
- `/help` lists the squad commands

### Install for a whole project

So everyone who opens a project gets the squad automatically, add this to the project's `.claude/settings.json` and commit it:

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

Then copy [`templates/CLAUDE.md`](../templates/CLAUDE.md) into the project root and fill it in (stack, commands, data classification, project rules). The better this file, the better the squad's work.

### Keep it up to date

```
/plugin marketplace update infinium
```

---

## 5. Using the agents and commands

### Just ask

You can talk to Claude normally. It picks a specialist when the task fits, and runs the code and security reviewers before you open a PR. You can also name one:

> Use the architect to design a notifications service.
> Ask the qa-engineer to write a failing test that reproduces this bug.

### The agents

| Agent | Use it for |
|---|---|
| `squad-lead` | Multi-step work across several areas. Plans, delegates to specialists and integrates the results |
| `architect` | System and feature design, trade-offs, API/event contracts, ADRs |
| `backend-engineer` | APIs, services, business logic, integrations |
| `frontend-engineer` | UI, components, design systems, accessibility, responsive layout, web performance |
| `python-specialist` | Python code: typing, packaging, async, pytest, performance |
| `rust-specialist` | Rust code: ownership, error handling, async, `unsafe` review, Cargo, performance |
| `sql-specialist` | Writing, reviewing and tuning SQL queries in any dialect |
| `data-engineer` | Schemas, migrations, pipelines, data quality |
| `qa-engineer` | Test strategy, writing tests, reproducing bugs, flaky tests |
| `devops-engineer` | CI/CD, Docker, infrastructure as code, observability |
| `security-reviewer` | Threat models and security reviews. Read-only: reports, never edits |
| `code-reviewer` | Correctness and standards review. Read-only |
| `simplifier` | Spots over-engineering and needless complexity and suggests simpler code. Only edits when you ask |
| `tech-writer` | READMEs, runbooks, API docs, release notes |

### The commands

| Command | What it does | Example |
|---|---|---|
| `/squad <task>` | Hands a whole task to the squad lead | `/squad Add CSV export to the invoices page, with an API endpoint and tests` |
| `/design <feature>` | Architect designs it and drafts an ADR if needed | `/design Move order notifications to an event-driven model` |
| `/adr <title>` | Creates a new Architecture Decision Record | `/adr Use Azure Service Bus for order events` |
| `/review [scope]` | Code review of your current changes | `/review` |
| `/security-review [scope]` | Security review of your current changes | `/security-review src/auth` |
| `/ship-check` | Lint, types, tests, both reviews and a PR description: tells you if you are ready to ship | `/ship-check` |
| `/simplify-check [scope] [--apply]` | Finds over-engineering in your changes; `--apply` makes the simplifications | `/simplify-check --apply` |
| `/compete <task>` | The squad and the challenger team both build it, test and critique each other, and a judge picks | `/compete Add rate limiting to the public API` |
| `/challenge [what it was for]` | The challenger team tests work that's already done, builds an alternative, and a judge compares | `/challenge Replace the nightly invoice sync with change data capture` |

If another plugin or a built-in command uses the same name, use the namespaced form, for example `/infinium-squad:review`.

### Getting a second opinion: the challenger team

For decisions that are high-stakes, hard to undo, or have several sensible approaches, you can have a second, independent team solve the same problem and compare the answers.

- `/compete <task>`: the squad and the challenger team each build a solution.
- `/challenge`: the challenger team takes on work you've already done on your branch. Tell it in one line what the change was for.

The challenger team only ever gets the task description, never the squad's plan or code, and each team works in its own git worktree. Each solution is tested by the other team's tester, each team critiques the other's finished work, and a neutral judge compares them without knowing which team built which. You get a verdict (use one, combine named parts of both, or neither), a comparison table and both branches.

Nothing is merged or pushed for you. A run costs roughly two to three times a normal one, so use it when the decision is worth it. When you're done, remove the extra worktrees with `git worktree remove <path>`.

### A typical day

1. Start a feature: `/design ...` for anything non-trivial, then `/squad ...` or ask a specific engineer agent.
2. While working: ask the `qa-engineer` for tests as you go.
3. Before a PR: run `/ship-check`. Fix what it flags. For a big or risky change, `/challenge` it first.
4. Push to Azure DevOps and open a PR (section 6). A human still reviews and approves every PR.

You stay responsible for what you commit. Read the diff before you accept it.

---

## 6. Connecting a project to Azure DevOps and pushing code

Infinium's internal code lives in **Azure Repos** (Azure DevOps). These steps connect a local project to an Azure Repos Git repository and push your work.

`TODO(infinium): Azure DevOps organisation URL, e.g. https://dev.azure.com/<org>, and which project new repos belong in.`
`TODO(infinium): who creates new repositories, and how to request one.`

### 6.1 One-time setup: authentication

Use **Git Credential Manager (GCM) with Microsoft Entra ID** sign-in. It uses your normal Infinium Microsoft login with MFA and caches a short-lived token, so you do not handle passwords or tokens yourself.

1. **Install GCM.**
   - Windows: install [Git for Windows](https://git-scm.com/download/win) and keep **Git Credential Manager** ticked in the installer.
   - macOS: `brew install --cask git-credential-manager`
   - Linux: follow the [GCM install guide](https://github.com/git-ecosystem/git-credential-manager/blob/main/docs/install.md).
2. **Make Entra ID tokens the default** for Azure Repos:

   ```bash
   git config --global credential.azreposCredentialType oauth
   ```

3. Set your name and work email for commits:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@infinium.example"   # TODO(infinium): real email domain
   ```

The first time you fetch or push, a Microsoft sign-in window appears. Sign in with your Infinium account and complete MFA. After that Git does not prompt again until the token expires.

**SSH** keys are a supported alternative if you prefer them ([Azure Repos SSH guide](https://learn.microsoft.com/azure/devops/repos/git/use-ssh-keys-to-authenticate)).

**Personal access tokens (PATs)** are a last resort, for example a tool that cannot use GCM. If you must use one: give it the narrowest scope (**Code: Read & write**), the shortest expiry, store it only in GCM or your OS keychain, and **never** put it in a remote URL, a script, a `.env` file, a commit or a chat with Claude. `TODO(infinium): confirm whether PATs are allowed at all.`

### 6.2 Get the repository URL

In Azure DevOps open **Repos > Files**, choose the repository, click **Clone** and copy the **HTTPS** URL. It looks like:

```
https://dev.azure.com/<organisation>/<project>/_git/<repository>
```

### 6.3 Connect and push

**A. The Azure repo already exists and has code:** just clone it.

```bash
git clone https://dev.azure.com/<organisation>/<project>/_git/<repository>
cd <repository>
```

**B. You have a local project and an empty Azure repo:**

```bash
cd my-project
git init -b main            # skip if it's already a Git repo
git add --all
git commit -m "chore: initial commit"
git remote add origin https://dev.azure.com/<organisation>/<project>/_git/<repository>
git push -u origin main
```

**C. The project currently points somewhere else** (for example GitHub) and is moving to Azure Repos:

```bash
git remote -v                                  # see current remotes
git remote rename origin github                # keep the old one, or: git remote remove origin
git remote add origin https://dev.azure.com/<organisation>/<project>/_git/<repository>
git push -u origin --all
git push origin --tags
```

Check which remote is which with `git remote -v` before pushing. Never push Infinium code to a personal or public remote.

### 6.4 Day-to-day: branches and pull requests

`main` is protected by **branch policies** in Azure Repos, so you cannot push to it directly. Work like this (see also the [Git and PR Workflow](../plugins/infinium-squad/skills/infinium-standards/standards/git-and-pr-workflow.md) standard):

```bash
git switch -c feat/invoice-csv-export
# ...work with the squad, then:
/ship-check                                   # in Claude Code
git push -u origin feat/invoice-csv-export
```

Then open a pull request:

- In the browser: Azure DevOps shows a **Create a pull request** banner after the push, or go to **Repos > Pull requests > New pull request**.
- From the terminal (optional, needs the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) with the `azure-devops` extension):

  ```bash
  az repos pr create --source-branch feat/invoice-csv-export --target-branch main \
    --title "feat: CSV export for invoices" --description "..."
  ```

Paste the PR description that `/ship-check` wrote. Branch policies then require the checks below before you can complete (merge) the PR. `TODO(infinium): actual policy, e.g. minimum reviewers, linked work item, build validation pipeline, comment resolution, squash merge.`

- at least one reviewer approval
- a linked Azure Boards work item
- the build validation pipeline passing
- all comments resolved

Claude can prepare commits and PR descriptions, but a person must review and approve every PR.

### 6.5 No secrets, ever

- Never commit credentials, connection strings, keys, certificates or `.env` files. Use `.env.example` with variable names only.
- Store secrets in **Azure Key Vault** and read them at runtime (Security Guide §3). Pipelines should use service connections or variable groups linked to Key Vault, never secret values in YAML.
- The squad's hook blocks agents from opening common secret files, but it does not scan what *you* commit. Check `git diff --staged` before committing. `TODO(infinium): name the secret-scanning tool used on Azure Repos, e.g. GitHub Advanced Security for Azure DevOps.`
- If a secret is committed, even on a branch that was never merged: **rotate it straight away** and report it to `TODO(infinium): security contact`. Deleting the commit is not enough.

Sources: [Use Git Credential Manager to authenticate to Azure Repos](https://learn.microsoft.com/azure/devops/repos/git/set-up-credential-managers), [Authentication with Azure Repos](https://learn.microsoft.com/azure/devops/repos/git/auth-overview), [Share your code with Git from the command line](https://learn.microsoft.com/azure/devops/repos/git/share-your-code-in-git-cmdline).

---

## 7. Rules of the road

- **Company account only.** Use your Infinium Claude seat for company work, never a personal account or API key.
- **Mind the data classification.** Don't paste data above what your project's classification allows into prompts. `TODO(infinium): which C-levels may be used with Claude, per the AI usage policy.`
- **You own the output.** Read every diff, run the tests, and get human review. Agents can be confidently wrong.
- **No production changes without a human.** Agents must ask before migrations, deploys or destructive commands against shared environments.
- **Improve the squad.** If an agent gives poor advice or a standard is unclear, open a PR on the squad repo (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

---

## 8. Troubleshooting and getting help

| Problem | Try |
|---|---|
| `claude` asks for an API key or bills the wrong account | `unset ANTHROPIC_API_KEY`, then `/login` with your Claude (claude.ai) work account |
| "Your login expires in N days" | Run `/login` |
| Login refused for your organisation | You may be signed in to a personal account. `/logout`, then sign in with your Infinium email |
| Hitting usage limits often | Ask for a Premium seat or extra usage (section 2) |
| `/plugin marketplace add` fails | Check you have access to the GitHub repo (section 4) and are signed in to GitHub |
| Squad agents missing from `/agents` | `/plugin marketplace update infinium`, then restart Claude Code |
| Guardrail hook errors | Make sure `python3` is on your `PATH` |
| `git push` asks for a password | GCM isn't installed or configured. Repeat section 6.1. Never type your Microsoft password into a Git prompt |
| `TF402455: Pushes to this branch are not permitted` | `main` is protected. Push a feature branch and open a PR |

Help: `TODO(infinium): support channel, e.g. #claude-code Teams channel, and squad maintainers.`
