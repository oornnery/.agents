# RCA

Use RCA when the problem keeps recurring, the failure is unclear, or a quick
fix already failed once.

## When to Use

- production incident or outage
- recurring bug that keeps being "fixed"
- flaky test with no clear cause
- performance degradation over time

## Investigation Workflow

1. reproduce the problem with evidence
2. isolate where and when it starts
3. build a short timeline
4. choose the simplest RCA technique that fits
5. verify the root cause against logs, code, config, or data
6. fix the cause, add a guardrail, and check for nearby variants

## 5 Whys

Use when the failure looks like one causal chain rather than many branches.

Rules:

- every answer must be backed by evidence
- avoid vague endpoints such as "human error"
- stop when the next "why" would become speculative

Template:

```markdown
1. Why did [symptom] happen?
2. Why did that happen?
3. Why did that happen?
4. Why was that possible?
5. Why was the system set up that way?
```

## Fishbone

Use when several categories of causes are plausible and you need a broad sweep
before narrowing down.

Common categories:

- Code
- Infrastructure
- Configuration
- Dependencies
- Process
- Data

## Fault Tree

Use when the failure may depend on multiple conditions or several distinct
paths to the same outage.

Core idea:

- **AND** = multiple conditions must be true
- **OR** = any one of several conditions can trigger the failure

## Postmortem

Capture:

- date, duration, impact
- summary
- timeline
- root cause
- resolution
- action items
- lessons learned

Action items should include owner and due date.

## Common Patterns

| Symptom                   | Common Root Causes                              |
| ------------------------- | ----------------------------------------------- |
| intermittent failures     | race condition, resource exhaustion, clock skew |
| slow degradation          | memory leak, connection pool, log growth        |
| works locally, fails prod | env difference, missing config, DNS             |
| regression after deploy   | untested edge case, migration, config change    |
| flaky tests               | shared state, time dependency, port conflicts   |

## Rules

- evidence beats intuition
- avoid blame; analyze systems and decisions
- fix root cause, not only the visible symptom
- add regression coverage after the fix
