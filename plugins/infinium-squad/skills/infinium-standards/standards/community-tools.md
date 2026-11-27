# Infinium Community Tools Register

> Version 0.1. Reviewed 2026-11-27. Owner: `TODO(infinium): name the owner who approves community tools.`

Community skills and plugins are third-party code and instructions running with a developer's access to Infinium source. This register says which ones the squad supports, at which pinned version, and with what guardrails. Anything not listed here is not supported.

## 1. Rules for every community tool

1. **Pin, don't float.** Plugins listed in the `infinium` marketplace are pinned to a reviewed commit. Upgrading means a PR that bumps the pin after re-reviewing the diff.
2. **Reference before vendoring.** Prefer pointing at the upstream project. Copy files into this repository only when the licence allows it, the files contain no executable code, and we record the upstream commit and keep the licence beside them.
3. **Opt-in.** Nothing here installs with `infinium-squad`. Each developer, or each project's `.claude/settings.json`, chooses to enable it.
4. **Data classification applies.** A tool that stores or transmits prompts, code or tool output is cleared only for the classes stated below (Security Guide §2). Until the full C-level scale is confirmed, "Internal" means C3.
5. **Infinium standards win.** If a community skill's instructions conflict with the Infinium standards or [Agent Instructions](agent-instructions.md), follow Infinium's.

## 2. Register

| Tool | Upstream (pinned) | What it is | Licence | Status |
|---|---|---|---|---|
| Agent Skills spec | [agentskills/agentskills](https://github.com/agentskills/agentskills/tree/83021e2be457a9b6679148719c1f6074f0ad975e) | Open standard for the `SKILL.md` format | Apache-2.0 (code), docs licence in repo | **Adopted.** Our validator enforces it (§3.1) |
| napkin | [blader/napkin](https://github.com/blader/napkin/tree/27fa60a895de4383b26a539136bc983155cb979c) | Instruction-only skill: a curated per-repo runbook at `.claude/napkin.md` | MIT | **Opt-in, vendored** in `infinium-extras` (§3.2) |
| Ponytail | [DietrichGebert/ponytail v5.3.3](https://github.com/DietrichGebert/ponytail/tree/7801d061243d7b753bad0e0b3c057cd250b11755) | Plugin: "simplest solution that works" mode, skills and hooks | MIT | **Opt-in, pinned** external plugin `ponytail@infinium` (§3.3) |
| awesome-design-md | [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md/tree/fcc70284932276d085f01ef9f83edde90b1258cb) | Collection of 80+ example `DESIGN.md` files | MIT | **Reference only** (§3.4) |
| Graphify | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify/tree/0f22ae762e3e3d0b689fc7ad2b8192740628413b) (PyPI `graphifyy`) | CLI and skill that builds a code knowledge graph | MIT and Apache-2.0 | **Opt-in, install pinned yourself** (§3.5) |
| claude-mem | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/tree/ad682a38da4cdbd2076451f595adc7db512a626c) | Plugin with hooks, a local worker and database that records sessions as memory | Apache-2.0 | **Restricted opt-in**, Internal (C3) work only (§3.6) |
| OmniRoute | [cheaper-inference/OmniRoute](https://github.com/cheaper-inference/OmniRoute/tree/c71f0065a7efe9230ec23b96a12253b050c4d7ad) | Self-hosted AI gateway that routes prompts across ~400 third-party model providers and free tiers | MIT | **Not approved** (§3.7) |

## 3. Notes and guardrails

### 3.1 Agent Skills spec

The squad's skills follow the [Agent Skills specification](https://agentskills.io/specification): `name` of 1 to 64 lowercase letters, digits and single hyphens matching its folder, and a `description` of at most 1,024 characters. `scripts/validate.py` checks every skill in this repository against those rules, with no dependency on the upstream `skills-ref` tool.

### 3.2 napkin

- One Markdown file, no code. Vendored at the pinned commit with its MIT licence in `plugins/infinium-extras/skills/napkin/`, plus an Infinium addendum at the end of the skill.
- It writes `.claude/napkin.md` in each repository it is used in. Treat that file like code: review it before committing, and never let it hold secrets, customer data or anything above the repository's classification.
- Install: `/plugin install infinium-extras@infinium`.

### 3.3 Ponytail

- Overlaps with our `simplifier` agent; use one or the other on a task, not both, to avoid conflicting advice.
- Runs Node.js hooks on session start, subagent start and every prompt, and adds a status-bar module.
- By default it writes a per-task ledger (cost, turns, tokens) to `~/.config/ponytail/band/`. Turn the **Task board** option off if you don't want local usage records. Leave **Webhook URL** empty: a webhook would send task names and usage off your machine, which needs approval.
- Install: `/plugin install ponytail@infinium` (pinned to v5.3.3).

### 3.4 awesome-design-md

- Example `DESIGN.md` files describing well-known companies' visual systems, for AI agents to build UI from. Documentation only.
- Use it to learn the format and to write Infinium's or a client's own `DESIGN.md`. Don't ship UI that copies another company's brand; `frontend-engineer` builds to the project's own design system.
- Not vendored: link to the pinned commit instead, so we don't redistribute other companies' brand descriptions.

### 3.5 Graphify

- A Python CLI (`graphifyy` on PyPI, with two y's; the single-y name is a different package). It is not a Claude Code plugin, so it can't be pinned in our marketplace. Install it pinned: `uv tool install graphifyy==0.9.121`, then `graphify install` to add its skill.
- Code is parsed locally with tree-sitter and nothing leaves your machine. Docs, PDFs and images are sent to an LLM for a semantic pass, and headless runs pick whichever provider API key is set in your environment, including providers outside Infinium's approved list (for example Moonshot, which routes to servers in China).
- Guardrails: set `GRAPHIFY_BACKEND=none` (code-only graph) unless the provider is approved for the repository's classification. Don't commit `graphify-out/` without checking it, and don't connect the hosted MCP service for Infinium code without approval.

### 3.6 claude-mem

claude-mem records what happens in your sessions (prompts, tool use and output, and screenshots) and replays a summary into later sessions. That is useful, and it is also a copy of everything you worked on.

- **Storage:** SQLite and a Chroma vector index under `~/.claude-mem/` on your machine, plus screenshots under `~/.claude-mem/media-v1/`. Unencrypted unless your disk is.
- **Processing:** a local worker uses Claude to compress observations, under your own Claude account.
- **Network:** anonymous usage analytics are **on by default**. Cloud Sync and TeamBrain upload memory to cmem.ai and are opt-in. The `cmem-pro` plugin in the same marketplace streams tool use to cmem.ai and is **not approved**.
- **Clearance:** Internal (C3) work only. Not for repositories holding Confidential or Restricted data (customer data, credentials, payment, health or ID data) until the full C-level scale is confirmed and the tool is reviewed for higher classes.
- **Required settings:** run `npx claude-mem telemetry disable` straight after install; leave Cloud Sync, TeamBrain and image upload off; wrap anything sensitive in `<private>` tags; delete `~/.claude-mem/` when you leave a project that has a higher classification.
- **Install:** it is not in the `infinium` marketplace, because its name is reserved and its upstream marketplace cannot be pinned. If you accept the guardrails above: `/plugin marketplace add thedotmack/claude-mem`, then `/plugin install claude-mem@thedotmack`, then check the installed version against the pinned commit above.

### 3.7 OmniRoute (not approved)

OmniRoute is a gateway you run yourself that sends prompts, and therefore code, to whichever of roughly 400 third-party providers its routing picks, including pooled free tiers. It is not approved for Infinium work because:

- prompts and code would go to providers that are not vetted for Infinium data, and many free tiers allow training on inputs;
- pooling free tiers across accounts can breach those providers' terms;
- it stores many provider credentials in one service, which is a concentrated secret risk;
- it is a large, fast-moving codebase (several releases a week) with a broad attack surface.

If Infinium needs a model gateway, propose one through the architecture process (Architecture Guide) with an approved provider list.

## 4. Adding or upgrading a tool

1. Open a PR that adds a row here with upstream, pinned commit, licence, maintenance status, what it executes, what it stores and what it sends over the network.
2. For a plugin, add it to `.claude-plugin/marketplace.json` with a `sha` pin. The validator rejects unpinned external plugins.
3. Vendor files only when §1.2 allows it, with the upstream licence and commit beside them.
4. The security owner approves anything that runs code, stores session data or uses the network.
