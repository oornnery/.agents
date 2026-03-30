---
name: review
description: Structured code review of staged changes, a diff, or a pull request. Use when the user asks to review code, check a PR, or give feedback on changes.
---

# Review

Perform a structured code review. The goal is to produce actionable
feedback — not to rewrite the code yourself.

## Process

### 1. Understand the Scope

Determine what to review:

- **Staged changes**: `git diff --cached`
- **Working tree**: `git diff`
- **PR**: `gh pr diff <number>` or `gh pr view <number>`
- **Specific commits**: `git diff <base>...<head>`

Read the diff and understand the intent of the change.

### 2. Check Against Conventions

Load the project's `CLAUDE.md` and relevant skills. Verify:

- Naming follows project conventions.
- Code style matches existing patterns.
- New dependencies are justified.
- Public APIs are typed.
- Tests cover the new behavior.

### 3. Check for Issues

#### Correctness

- Edge cases handled (empty inputs, nulls, boundaries).
- Error paths tested and meaningful.
- Race conditions in concurrent code.

#### Security

- Input validation at boundaries.
- No hardcoded secrets or credentials.
- SQL injection, XSS, path traversal checks.
- Sensitive data not leaked in logs or errors.

#### Performance

- No N+1 queries or unbounded loops.
- Large data processed lazily (generators, streaming).
- Caching used where appropriate.

#### Maintainability

- Functions are focused (single responsibility).
- No dead code or commented-out blocks.
- Magic values replaced with named constants.
- Comments explain WHY, not WHAT.

### 4. Produce Feedback

Structure your review as:

```text
## Summary
One-line verdict: approve / request changes / comment only.

## Findings
### [Category] Finding title
- **File**: path/to/file.py:42
- **Severity**: critical / warning / suggestion / nitpick
- **Description**: What the issue is and why it matters.
- **Suggestion**: How to fix it (if applicable).

## What Looks Good
Brief note on well-done aspects (positive feedback matters).
```

### Severity Guide

| Level      | Meaning                                        |
| ---------- | ---------------------------------------------- |
| critical   | Must fix before merge — bug, security, crash   |
| warning    | Should fix — correctness risk, maintainability |
| suggestion | Nice to have — readability, consistency        |
| nitpick    | Trivial — style preference, minor cleanup      |

## What NOT to Do

- **Do not make changes yourself.** Review produces feedback, not code.
- **Do not nitpick style** that the linter already handles.
- **Do not block on personal preference** — if it works and is consistent, approve.
- **Do not review generated files** (lock files, migrations, vendor).
