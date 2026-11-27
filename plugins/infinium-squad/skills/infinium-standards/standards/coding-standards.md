# Infinium Coding Standards

> Version 0.1. Applies to all languages unless a language section says otherwise.

## 1. General

1. **Readable over clever.** Code is read far more than it is written. Optimise for the next person.
2. **Consistency wins.** Follow the existing conventions of the repo you are in, even if you'd choose differently.
3. **Small units.** Functions do one thing. Prefer functions under ~40 lines and files under ~400 lines; split when they grow.
4. **Names say what, not how.** `unpaid_invoices`, not `list2`. Booleans read as questions: `is_active`, `has_access`.
5. **No dead code.** Delete it; git remembers. No commented-out blocks.
6. **Comments explain why.** The code says what. Document public APIs with the language's doc-comment format.
7. **Fail loudly.** Don't swallow errors. Catch only what you can handle, and add context when re-raising.
8. **No magic values.** Name constants. Keep configuration out of code.
9. **Pure where possible.** Keep side effects (I/O, time, randomness) at the edges so logic is easy to test.
10. **Formatting and linting are automated** and enforced in CI. Don't argue about style in review; fix the config.

## 2. Error handling

1. Use the language's idiomatic mechanism (exceptions, `Result`, error returns) consistently within a codebase.
2. Distinguish expected failures (validation, not found) from unexpected ones (bugs, outages).
3. Never expose internal error details to end users (Security Guide §7.4).
4. Log an error once, at the boundary where it is handled, with context. Don't log-and-rethrow at every layer.

## 3. Dependencies

1. Adding a dependency is a design decision: check maintenance, licence, size and security (Security Guide §8).
2. Wrap third-party SDKs behind your own interface when they are central to the domain, so they can be replaced and mocked.

## 4. Language defaults

`TODO(infinium): confirm or replace these defaults.`

| Language | Style / formatter | Linter | Types |
|---|---|---|---|
| TypeScript / JavaScript | Prettier | ESLint (typescript-eslint) | `strict: true`; no `any` without a comment |
| Python | Black or Ruff format, PEP 8 | Ruff | Type hints on public functions; mypy or pyright in CI |
| Java / Kotlin | Google Java Style / ktlint | Checkstyle / detekt | Null-safety annotations / Kotlin nullability |
| C# | .NET conventions, `dotnet format` | Roslyn analysers | Nullable reference types enabled |
| Go | `gofmt` | `golangci-lint` | — |
| Terraform | `terraform fmt` | `tflint`, `checkov` or `tfsec` | — |
| SQL | Lowercase keywords or uppercase, but consistent per repo | `sqlfluff` | — |

## 5. Frontend

1. Accessibility is a requirement: meet WCAG 2.2 AA. Semantic HTML first, ARIA only when needed, keyboard operable, visible focus, sufficient contrast.
2. Components are small, typed and stateless where possible; keep server state in a data-fetching layer, not ad-hoc in components.
3. Watch bundle size and Core Web Vitals; lazy-load heavy routes.
4. No secrets in frontend code. Anything shipped to the browser is public.
5. Internationalisation-ready: no hard-coded user-facing strings where the product is or will be localised.

## 6. Backend

1. Validate input at the boundary (Security Guide §5) and convert to domain types early.
2. Keep transactions short; never call external services inside a DB transaction.
3. Make handlers idempotent where retries can happen.
4. Use dependency injection (constructor parameters) rather than global singletons, so code is testable.

## 7. Definition of done

A change is done when:

- [ ] It meets the acceptance criteria
- [ ] Tests are written and passing (Testing Standards)
- [ ] Lint, format, type check and security scans pass
- [ ] Docs, README, OpenAPI spec, runbook or ADR are updated if behaviour changed
- [ ] It has been reviewed and approved (Git and PR Workflow)
- [ ] It is observable (logs/metrics for new paths) and can be rolled back
