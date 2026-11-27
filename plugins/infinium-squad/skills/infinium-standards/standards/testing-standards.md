# Infinium Testing Standards

> Version 0.1.

## 1. Principles

1. **Tests are part of the change.** New behaviour ships with tests; bug fixes ship with a test that failed before the fix.
2. **Test behaviour, not implementation.** Assert on outputs and observable effects, not private internals, so refactors don't break tests.
3. **Fast, isolated, deterministic.** Unit tests run in milliseconds, need no network, and pass in any order. Control time, randomness and IDs.
4. **The testing pyramid.** Many unit tests, fewer integration tests, a small number of end-to-end tests on critical journeys.
5. **A flaky test is a broken test.** Fix it or quarantine it with an owner and a ticket within one working day. Never just add retries.

## 2. Levels

| Level | Scope | Dependencies | Runs |
|---|---|---|---|
| Unit | One function/class/module | All external deps faked | Every commit |
| Integration | Service + its real DB/queue/cache | Real deps in containers (e.g. Testcontainers) | Every PR |
| Contract | API/event between two services | Consumer-driven contracts or schema checks | Every PR |
| End-to-end | Critical user journeys | Deployed environment | Before release / nightly |
| Non-functional | Performance, load, security (DAST), accessibility | As needed | Before major releases, scheduled |

## 3. Coverage

1. Coverage is a signal, not a goal. Default floor: **80% line coverage on changed code**, enforced in CI. `TODO(infinium): confirm threshold.`
2. Critical logic (money, permissions, data integrity) needs branch coverage and edge-case tests regardless of the number.
3. Never write assertion-free tests to inflate coverage.

## 4. Writing good tests

1. Structure: Arrange, Act, Assert. One behaviour per test.
2. Names describe the behaviour: `returns_404_when_invoice_belongs_to_another_customer`.
3. Use builders/factories for test data; keep each test's relevant data visible in the test.
4. Mock at the boundary you own (your repository or client interface), not deep inside third-party libraries.
5. Include unhappy paths: invalid input, unauthorised caller, dependency timeout, empty and maximum sizes.
6. Security-relevant tests: authorisation (including other tenants' data), input validation, and that secrets don't appear in logs.
7. Test data must be synthetic. Never copy production personal data into tests or fixtures (Security Guide §9.5).

## 5. CI

1. All tests required for merge run in CI on every PR.
2. Agents and developers must never skip, delete or weaken a test to make CI pass without the reviewer explicitly agreeing in the PR.
3. Test reports and coverage are published as CI artefacts.
