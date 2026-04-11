---
name: rca
description: Root Cause Analysis methodology -- 5 Whys, Fishbone, Fault Tree, postmortem templates. Load when investigating production incidents, recurring bugs, or systematic failures.
---

# Root Cause Analysis

Systematic techniques for finding the true cause of problems.

## When to Use

- Production incident or outage
- Recurring bug that keeps being "fixed"
- Flaky tests with no clear cause
- Performance degradation over time

## Techniques

### 5 Whys

Ask "why" repeatedly (3-5 levels) until you reach the root cause.
Each answer must be supported by evidence (logs, metrics, code).
Avoid blame -- focus on systems and processes.

### Fishbone (Ishikawa)

Categorize potential causes: **Code**, **Infrastructure**,
**Configuration**, **Dependencies**, **Process**, **Data**.

### Fault Tree

Work backward from failure through logical gates (AND/OR).
Use when the failure has multiple possible paths.

## Investigation Workflow

1. **Reproduce** -- create minimal repro, note steps/environment/timing.
2. **Isolate** -- when did it start? Where? Who is affected? Use `git bisect`.
3. **Build timeline** -- deploy times, error spikes, rollbacks.
4. **Find root cause** -- apply 5 Whys or Fishbone, verify with logs/code.
5. **Fix and verify** -- fix root cause, add regression test, check for similar patterns.

## Postmortem Template

```markdown
# Postmortem: [Title]

## Date / Duration / Impact

## Summary -- one paragraph

## Timeline -- HH:MM events

## Root Cause -- from 5 Whys or Fishbone

## Resolution -- what was done

## Action Items

- [ ] Fix: [description] -- owner -- due date
- [ ] Prevent: [description] -- owner -- due date
- [ ] Detect: [description] -- owner -- due date

## Lessons Learned
```

## Common Patterns

| Symptom                   | Common Root Causes                              |
| ------------------------- | ----------------------------------------------- |
| Intermittent failures     | Race condition, resource exhaustion, clock skew |
| Slow degradation          | Memory leak, connection pool, log growth        |
| Works locally, fails prod | Env difference, missing config, DNS             |
| Regression after deploy   | Untested edge case, migration, config change    |
| Flaky tests               | Shared state, time dependency, port conflicts   |

## Related

- `commands/debug.md` -- systematic debugging workflow
