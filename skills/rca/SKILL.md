---
name: rca
description: Root Cause Analysis methodology — 5 Whys, Fishbone, Fault Tree, postmortem templates. Load when investigating production incidents, recurring bugs, or systematic failures.
---

# Root Cause Analysis

Systematic techniques for finding the true cause of problems, not just
the symptoms.

> _"If you don't find the root cause, you'll fix the symptom and the
> problem will come back."_

## When to Use RCA

- Production incident or outage
- Recurring bug that keeps being "fixed"
- Flaky tests with no clear cause
- Performance degradation over time
- Customer-reported issues that are hard to reproduce

## Techniques

### 5 Whys

Ask "why" repeatedly until you reach the root cause. Usually 3-5 levels.

```text
Problem: Users cannot log in

Why? → The auth service returns 500
Why? → The database connection pool is exhausted
Why? → Connections are not being released after queries
Why? → The ORM session is not properly closed in error paths
Why? → The error handler catches exceptions but skips session cleanup

Root cause: Missing session cleanup in error handling middleware
```

**Rules:**

- Each "why" must be supported by evidence (logs, metrics, code)
- Do not stop at the first plausible answer — verify it
- If you branch into multiple causes, follow each one
- Avoid blame — focus on systems and processes, not people

### Fishbone Diagram (Ishikawa)

Categorize potential causes:

```text
         Methods    Machines    Materials
            \          |          /
             \         |         /
              ╲        |        ╱
               ╲       |       ╱
                ──── PROBLEM ────
               ╱       |       ╲
              ╱        |        ╲
             /         |         \
            /          |          \
      People     Environment    Measurement
```

Categories for software:

- **Code** — logic errors, race conditions, missing validation
- **Infrastructure** — server capacity, network, DNS, certificates
- **Configuration** — environment variables, feature flags, secrets
- **Dependencies** — library updates, API changes, service outages
- **Process** — missing review, skipped tests, incomplete deployment
- **Data** — corrupt records, unexpected input, schema drift

### Fault Tree Analysis

Work backward from the failure through logical gates:

```text
                    [Login Fails]
                    /           \
                 OR               OR
                /                   \
    [Auth Service Down]    [Token Validation Fails]
         |                    /              \
        AND                 OR                OR
       /    \              /                    \
  [DB Down] [No Retry]  [Clock Skew]    [Secret Rotated]
```

Use when the failure has multiple possible paths.

## Investigation Workflow

### 1. Reproduce

- **Can you reproduce it?** If not, gather more data first.
- Create a minimal reproduction case.
- Note: exact steps, environment, timing, frequency.

### 2. Isolate

- **When did it start?** Check deploy history, config changes, dependency
  updates. Use `git bisect` if tied to a code change.
- **Where does it happen?** Specific endpoint, service, environment?
- **Who is affected?** All users, specific cohort, specific region?

### 3. Build Timeline

```text
14:00 — Deploy v2.3.1 to production
14:05 — First error alerts from monitoring
14:08 — Error rate spikes to 15%
14:12 — Team identifies auth service as source
14:15 — Rollback to v2.3.0
14:16 — Error rate returns to baseline
14:30 — Root cause identified: missing DB connection cleanup
```

### 4. Find Root Cause

Apply 5 Whys or Fishbone to narrow down. Verify with:

- Logs and metrics (not assumptions)
- Code review of the specific change
- Reproducing the fix in staging

### 5. Fix and Verify

- Fix the root cause, not just the symptom
- Add a regression test
- Verify the fix resolves the original issue
- Check for similar patterns elsewhere in the codebase

## Postmortem Template

```markdown
# Postmortem: [Incident Title]

## Date

YYYY-MM-DD

## Duration

Start time → Resolution time (total duration)

## Impact

- Number of affected users
- Services impacted
- Revenue/SLA impact (if applicable)

## Summary

One paragraph describing what happened.

## Timeline

- HH:MM — Event description
- HH:MM — Event description

## Root Cause

What actually caused the incident (from 5 Whys or Fishbone).

## Resolution

What was done to resolve the incident.

## Action Items

- [ ] Fix: [description] — owner — due date
- [ ] Prevent: [description] — owner — due date
- [ ] Detect: [description] — owner — due date

## Lessons Learned

What went well, what could be improved.
```

### Action Item Categories

- **Fix** — address the immediate root cause
- **Prevent** — systemic changes to prevent recurrence (better tests,
  validation, monitoring)
- **Detect** — improve detection to catch similar issues earlier (alerts,
  health checks, dashboards)

## Common Root Cause Patterns

| Symptom                      | Common Root Causes                                  |
| ---------------------------- | --------------------------------------------------- |
| Intermittent failures        | Race condition, resource exhaustion, clock skew     |
| Slow degradation             | Memory leak, connection pool exhaustion, log growth |
| Works locally, fails in prod | Environment difference, missing config, DNS         |
| Regression after deploy      | Untested edge case, migration issue, config change  |
| Flaky tests                  | Shared state, time dependency, port conflicts       |

## Related

- `commands/debug.md` — systematic debugging workflow
- `skills/testing/SKILL.md` — test failure triage
- `skills/architecture/SKILL.md` — architecture patterns that prevent issues
