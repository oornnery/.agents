---
name: review
description: Structured read-only review of a diff, staged changes, or a pull request. Use when the user asks for feedback, risk analysis, or a code review.
---

# Review

Structured code review. Output feedback, not code.

## Scope inputs

Review one of:

- staged diff: `git diff --cached`
- working tree: `git diff`
- PR diff: `gh pr diff`
- commit range: `git diff A...B`

## Process

### 1. Understand the change

Read diff. Identify:

- what changed
- expected new behavior
- nearby regression risk

### 2. Load only the relevant lenses

Use matching local skills:

- `skills/python/SKILL.md` for Python correctness and conventions
- `skills/design/SKILL.md` for API, UI, or BFF contract changes
- `skills/arch/SKILL.md` for layering or responsibility issues
- `skills/quality/SKILL.md` for missing tests or RCA concerns
- `skills/security/SKILL.md` for auth, trust boundaries, injection, or secrets
- `skills/cicd/SKILL.md` for GitHub Actions workflow changes
- `skills/docs/SKILL.md` for Markdown and documentation work

### 3. Review by concern

- correctness: edge cases, error paths, race conditions
- security: validation, auth, secrets, injection, data exposure
- performance: N+1s, unbounded loops, blocking in async, wasteful queries
- maintainability: SRP, dead code, magic values, unclear comments
- convention adherence: naming, style, project patterns

### 4. Report findings by severity

Use this shape:

```text
## Summary
[approve | request changes | comment only]

## Critical

## Warnings

## Suggestions

## What Looks Good
```

Severity guide:

| Level      | Meaning                                         |
| ---------- | ----------------------------------------------- |
| critical   | must fix before merge -- bug, security, crash   |
| warning    | should fix -- correctness risk, maintainability |
| suggestion | nice to have -- readability, consistency        |
| nitpick    | trivial and usually skip-worthy                 |

Each finding include:

- file and location
- evidence
- impact
- minimal safe fix

## Constraints

- review only; do not edit code
- skip nitpicks already enforced by tooling
- skip generated files when possible
- focus on actionable findings

## Optional routing

For dedicated security pass, hand off to `agents/security-engineer.md` when that agent exists.