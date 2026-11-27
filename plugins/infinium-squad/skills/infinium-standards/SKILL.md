---
name: infinium-standards
description: Infinium's company-wide engineering standards (Security Guide, Architecture Guide, Coding Standards, Testing Standards, Git and PR Workflow). Load whenever designing, writing, reviewing, testing or shipping code at Infinium, or when asked what Infinium's policy is.
---

# Infinium Engineering Standards

These are the shared rules every Infinium squad agent follows. Read the guide that matches the task before acting, and cite the section you rely on (for example "Security Guide §4.2") in reviews and plans.

| Guide | Read it when |
|---|---|
| [Security Guide](standards/security-guide.md) | Handling auth, secrets, user input, personal data, dependencies, or any review |
| [Architecture Guide](standards/architecture-guide.md) | Designing a system or feature, adding a service, choosing technology, writing an ADR |
| [Coding Standards](standards/coding-standards.md) | Writing or reviewing any code |
| [Testing Standards](standards/testing-standards.md) | Writing tests, deciding coverage, fixing flaky tests |
| [Git and PR Workflow](standards/git-and-pr-workflow.md) | Branching, committing, opening or reviewing a PR, releasing |

## Precedence

1. A project's own `CLAUDE.md` or `docs/standards/` may tighten these rules. It may only loosen them with a written, approved exception (Security Guide §11).
2. Where a guide has a `TODO(infinium)` placeholder, the company has not yet filled it in. Apply the default written next to it, and mention in your output that the policy is unconfirmed.
3. Never invent Infinium policy. If a guide is silent, say so and use widely accepted industry practice (OWASP, the Twelve-Factor App, the language's official style guide).
