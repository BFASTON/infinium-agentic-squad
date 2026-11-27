# Infinium Git and PR Workflow

> Version 0.1.

## 1. Branching

1. Trunk-based development: `main` is always releasable and protected.
2. Short-lived branches (ideally under 2 days) named `type/short-description`, optionally with a ticket key: `feat/PROJ-123-invoice-export`.
3. Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `ci`, `build`.
4. Use feature flags for work that can't be finished in a short branch.

## 2. Commits

1. Follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): summary` in the imperative, under 72 characters.
2. Body explains *why*; reference the ticket. Mark breaking changes with `!` and a `BREAKING CHANGE:` footer.
3. Each commit should build. Squash fix-up noise before merging.
4. Never commit secrets, generated build output, or large binaries.
5. Commits made with AI assistance may include a `Co-Authored-By:` trailer. `TODO(infinium): confirm attribution policy.`

## 3. Pull requests

1. Keep PRs small and focused: aim for under ~400 changed lines of non-generated code.
2. Use the repo's PR template. A good description covers: what and why, how it was tested, risks and rollback, screenshots for UI.
3. Open as draft early for feedback; mark ready when CI is green and you've self-reviewed.
4. Run `/review` and, for anything touching auth, data or infrastructure, `/security-review` before requesting human review.
5. Required to merge:
   - CI green (build, lint, types, tests, secret scan, dependency scan)
   - At least one approving review from someone other than the author `TODO(infinium): two for production-critical repos?`
   - CODEOWNERS approval where applicable
   - All review threads resolved
6. Merge method: squash merge by default, so `main` has one Conventional Commit per PR.
7. Never force-push to `main` or to someone else's branch.

## 4. Reviewing

1. Review within one working day.
2. Look for correctness, security, tests, readability, and fit with the Architecture Guide, in that order.
3. Label comments: `blocking:`, `suggestion:`, `nit:`, `question:`.
4. Be kind and specific; critique code, not people. Approve when it's good enough, not perfect.
5. AI-generated code gets the same scrutiny as human code (Security Guide §12.5).

## 5. Releases

1. Releases are automated from `main` by the pipeline, with semantic versioning for libraries and APIs.
2. Every release can be rolled back, and the rollback has been practised.
3. Changelogs are generated from Conventional Commits.
4. Production deploys follow `TODO(infinium): change management process (approvals, freeze windows)`.
