# CLAUDE.md

<!-- Infinium project template. Copy to your repo root, fill in every section, delete these comments. -->

This project uses the **Infinium Agentic Squad** plugin. All agents follow the Infinium engineering standards (`infinium-standards` skill). The rules below add project-specific context and may tighten, but not loosen, those standards.

## Project

- **What it is:** <!-- one or two sentences -->
- **Owner team:** <!-- team name; see CODEOWNERS -->
- **Data classification:** <!-- C-level of the most sensitive data this project handles, e.g. C3 (Internal). See Security Guide §2 -->
- **Architecture notes:** <!-- link to docs/adr/ and any diagrams -->

## Stack

- Language(s) and versions: <!-- e.g. TypeScript 5, Node 22 -->
- Frameworks: <!-- e.g. NestJS, React 19 -->
- Data stores: <!-- e.g. PostgreSQL 16 -->
- Hosting / infra: <!-- e.g. containers on Kubernetes, Terraform in infra/ -->

## Commands

```bash
# install
# run locally
# format check
# lint
# type check
# unit tests
# integration tests
```

## Layout

<!-- Key directories and what lives where. -->

## Project rules

<!-- Anything stricter or more specific than the Infinium standards, e.g.:
- All money values are integer minor units (cents); never floats.
- Every new endpoint needs an entry in openapi.yaml.
- Do not touch generated code in src/generated/.
-->

## Escalation

Agents resolve problems themselves and ask a human only when the Escalation Policy says one is genuinely needed. Bugs with an unclear cause go to `on-call-engineer` (or `/oncall`).

- **Human contact for this project:** <!-- who answers the squad's questions -->
- **Extra things that always need a human here:** <!-- e.g. any change under billing/, any schema migration -->
- **Phone alerts:** each developer sets `INFINIUM_NOTIFY` and their ntfy or Pushover variables in their own environment (see the user guide). Never commit them here.

## Never

- Commit secrets or read `.env` files (use `.env.example` for variable names).
- Run migrations, deploys or destructive commands against shared or production environments without asking.
- Skip or weaken tests or security checks to make CI pass.
