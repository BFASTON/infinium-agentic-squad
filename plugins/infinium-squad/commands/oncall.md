---
description: Hand a bug, failing build or incident with an unclear cause to the on-call engineer to triage, find the root cause, fix and review
argument-hint: <the error, failing test, symptom or log excerpt>
---

Use the `on-call-engineer` agent to triage and investigate the following problem. It should classify severity, reproduce the failure, find the root cause with evidence, make the minimal fix with a regression test when it is in scope, have `code-reviewer` review the fix, and finish with its incident note. It should escalate to me only when the Escalation Policy requires it.

Problem: $ARGUMENTS
