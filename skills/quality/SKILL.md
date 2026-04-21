---
name: quality
description: Quality guidance for test-driven development and root cause analysis. Load when preventing regressions, shaping behavior through tests, or diagnosing failures systematically.
---

# Quality

Use this skill when reliability is the main concern: either preventing defects
before they ship or understanding why something broke.

## Pick the Mode

| Situation                               | Read                                          |
| --------------------------------------- | --------------------------------------------- |
| write tests before code, drive design   | `references/tdd.md`                           |
| incident analysis or recurring failures | `references/rca.md`                           |
| a fix already failed once               | `references/rca.md`, then `references/tdd.md` |

## Shared Rules

- make failures explicit instead of masking them
- do not guess when evidence can be gathered
- small verified steps beat broad speculative changes
- always close the loop with a guardrail, usually a regression test or clearer boundary

## Workflow

1. decide whether the work is preventive or investigative
2. load only the matching reference
3. work in small verified steps
4. close the loop with a regression test or clearer guardrail
