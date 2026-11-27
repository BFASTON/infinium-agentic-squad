# Infinium Architecture Guide

> Version 0.1. Owner: `TODO(infinium): architecture group / forum name`.

## 1. Principles

1. **Simple first.** Choose the simplest design that meets today's known requirements, with a clear path to the next step. A well-structured modular monolith beats premature microservices.
2. **Clear boundaries.** Organise by business capability (domain), not by technical layer. Each module or service owns its data.
3. **Explicit contracts.** Modules talk through documented interfaces (APIs, events, schemas). No reaching into another module's database or internals.
4. **Stateless compute.** Keep state in managed data stores so instances can be replaced and scaled.
5. **Design for failure.** Every network call can fail, be slow, or be repeated.
6. **Observable by default.** If you can't see it in logs, metrics and traces, it isn't production-ready.
7. **Secure by design.** Every design is checked against the [Security Guide](security-guide.md).
8. **Reversible decisions fast, irreversible decisions carefully.** Spend design effort where change is expensive (data models, public APIs, vendor lock-in).

## 2. Architecture Decision Records (ADRs)

Write an ADR for any decision that is costly to reverse: new service, new data store, new language or framework, new third-party platform, public API shape, cross-team contract.

- Location: `docs/adr/NNNN-short-title.md` in the owning repo.
- Format: Context, Decision, Options considered, Consequences, Status (Proposed, Accepted, Superseded by NNNN).
- An ADR is reviewed in a PR like code. `TODO(infinium): which decisions need architecture forum sign-off.`

Use `/design` to have the architect agent draft one.

## 3. Approved technology

`TODO(infinium): fill in the approved stack ("tech radar"). Until then, agents should prefer what the repository already uses and flag new technology as needing an ADR.`

| Area | Adopt | Trial | Hold |
|---|---|---|---|
| Languages | `TODO` | `TODO` | `TODO` |
| Frontend | `TODO` | `TODO` | `TODO` |
| Data stores | `TODO` | `TODO` | `TODO` |
| Messaging | `TODO` | `TODO` | `TODO` |
| Cloud / hosting | `TODO` | `TODO` | `TODO` |
| CI/CD | `TODO` | `TODO` | `TODO` |
| Observability | `TODO` | `TODO` | `TODO` |

## 4. Service and module design

1. One clear owner (team) per service. Record it in the repo README and `CODEOWNERS`.
2. Layering inside a service: interface (HTTP/CLI/consumer) → application (use cases) → domain (business rules) → infrastructure (DB, external APIs). Dependencies point inward; domain code does not import framework or infrastructure code.
3. Configuration comes from the environment (Twelve-Factor). The same artefact runs in every environment.
4. Health endpoints: liveness and readiness, separate from business endpoints.
5. Every service has a README covering purpose, how to run locally, how to test, how to deploy, and its runbook.

## 5. APIs

1. Default to REST over HTTPS with JSON, described by an OpenAPI spec kept in the repo. Use gRPC or GraphQL only with an ADR.
2. Resource-oriented URLs, plural nouns, standard HTTP verbs and status codes.
3. Version public APIs (`/v1/...` or a header). Never make a breaking change to a published version; add a new one and deprecate with notice.
4. Paginate every list endpoint. Bound every request (size, time).
5. Consistent error body, e.g. RFC 9457 Problem Details: `type`, `title`, `status`, `detail`, `instance`, plus a correlation ID.
6. Unsafe operations that may be retried (payments, orders) accept an idempotency key.
7. Use ISO 8601 UTC timestamps and explicit units in field names (`timeout_ms`).

## 6. Events and async work

1. Use events for facts that other domains react to (`OrderPlaced`), commands/queues for work to be done.
2. Events have a versioned schema stored in the repo or a schema registry.
3. Consumers are idempotent and tolerate out-of-order and duplicate delivery.
4. Use the outbox pattern (or equivalent) when a DB write and an event publish must both happen.
5. Every queue has a dead-letter queue, an alert on it, and a documented replay process.

## 7. Data

1. Each service owns its schema. Other services get data through APIs or events, not shared tables.
2. Schema changes go through versioned migrations in the repo, applied by the pipeline, never by hand.
3. Migrations are backward compatible with the currently running version (expand → migrate → contract).
4. Choose the store by access pattern; relational is the default. Document why if not.
5. Back-ups are automated and restores are tested on a schedule. `TODO(infinium): RPO/RTO targets per tier.`
6. Classify data per Security Guide §2 at design time.

## 8. Resilience and performance

1. Set timeouts on every outbound call. No infinite waits.
2. Retry only idempotent operations, with exponential backoff and jitter, and a cap.
3. Use circuit breakers or bulkheads around unreliable dependencies.
4. Degrade gracefully: decide what the user sees when a dependency is down.
5. Define SLOs for user-facing services (availability, latency) and alert on error-budget burn. `TODO(infinium): default SLO tiers.`
6. Cache deliberately: state the TTL, the invalidation rule and what happens on a stale read.

## 9. Observability

1. Structured JSON logs with timestamp, level, service, environment, correlation/trace ID.
2. Metrics: at least request rate, error rate and latency (RED) per endpoint, plus saturation for resources.
3. Distributed tracing with OpenTelemetry across service boundaries.
4. Every alert is actionable and links to a runbook. `TODO(infinium): observability platform and on-call tooling.`

## 10. Design review checklist

Before building anything that needs an ADR, confirm:

- [ ] Problem, users and non-functional requirements (scale, latency, availability, data class) are written down
- [ ] At least two options were considered, with trade-offs
- [ ] Boundaries and data ownership are clear
- [ ] API/event contracts are drafted
- [ ] Failure modes and how the system degrades are listed
- [ ] Security review against the Security Guide is done (threat model for anything handling Confidential data or above)
- [ ] Observability, deployment and rollback plan exist
- [ ] Cost estimate and owner are recorded
