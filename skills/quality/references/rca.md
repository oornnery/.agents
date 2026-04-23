# RCA

Use RCA when problem recurs, failure unclear, or quick fix already failed once.

## When to Use

- production incident or outage
- recurring bug that keeps being "fixed"
- flaky test with no clear cause
- performance degradation over time

## Investigation Workflow

1. reproduce problem with evidence
2. isolate where and when it starts
3. build short timeline
4. choose simplest RCA technique that fits
5. verify root cause against logs, code, config, or data
6. fix cause, add guardrail, check nearby variants

## 5 Whys

Use when failure looks like one causal chain, not many branches.

Rules:

- every answer backed by evidence
- avoid vague endpoints like "human error"
- stop when next "why" becomes speculative

Template:

```markdown
1. Why did [symptom] happen?
2. Why did that happen?
3. Why did that happen?
4. Why was that possible?
5. Why was the system set up that way?
```

## Fishbone

Use when several cause categories plausible, need broad sweep before narrowing down.

Common categories:

- Code
- Infrastructure
- Configuration
- Dependencies
- Process
- Data

## Fault Tree

Use when failure depends on multiple conditions or several distinct paths to same outage.

Core idea:

- **AND** = multiple conditions must be true
- **OR** = any one of several conditions can trigger failure

## Postmortem

Capture:

- date, duration, impact
- summary
- timeline
- root cause
- resolution
- action items
- lessons learned

Action items include owner and due date.

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
- fix root cause, not just visible symptom
- add regression coverage after fix