---
name: quality
description: Quality guidance for TDD and root cause analysis. Load when preventing regressions, shaping behavior through tests, or diagnosing failures.
---

# Quality

Use skill when reliability = main concern: prevent defects before ship or understand why something broke.

Use `skills/verification/SKILL.md` for selecting and reporting format, lint,
type/LSP, test, build, and security gates. This skill is for test strategy,
regression thinking, and root cause analysis.

## Pick the Mode

| Situation                               | Read                                          |
| --------------------------------------- | --------------------------------------------- |
| write tests before code, drive design   | `references/tdd.md`                           |
| incident analysis or recurring failures | `references/rca.md`                           |
| fix already failed once                 | `references/rca.md`, then `references/tdd.md` |

## Shared Rules

- make failures explicit, don't mask them
- don't guess when evidence can be gathered
- small verified steps beat broad speculative changes
- always close loop with guardrail -- regression test or clearer boundary

## Workflow

1. decide: preventive or investigative
2. load only matching reference
3. work in small verified steps
4. close loop with regression test or clearer guardrail
