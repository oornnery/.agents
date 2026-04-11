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

## Specialized Review Agents

For thorough reviews, launch up to 4 agents in parallel, each focused on
a specific concern. Consolidate findings into a single report.

**Model recommendation:** use `model: "sonnet"` for each agent — the tasks
are focused and well-scoped. Upgrade to `model: "opus"` only if the diff
involves complex security logic or deep architectural changes.

### Agent 1: Code Quality Reviewer

Focus: clean code, readability, and project conventions.

- **Naming** — clear, intention-revealing names. No abbreviations.
- **Function size** — functions over 30 lines likely do too much.
- **Complexity** — cyclomatic complexity, deep nesting, long parameter lists.
- **Dead code** — unused imports, functions, variables, unreachable branches.
- **Magic values** — replace literals with named constants or enums.
- **Consistency** — follows established project patterns and conventions.
- **DRY** — near-duplicate code that should be unified (3+ instances).

### Agent 2: Performance Reviewer

Focus: efficiency and resource usage.

- **N+1 queries** — database calls inside loops.
- **Unbounded operations** — loops, queries, or reads without limits.
- **Lazy loading** — large data should use generators or streaming.
- **Caching** — repeated expensive computations that could be cached.
- **Async** — blocking calls in async code, missing `await`.
- **Memory** — large objects held longer than needed, connection leaks.
- **Indexing** — database queries on unindexed columns.

### Agent 3: Test Coverage Reviewer

Focus: test adequacy for the changed code.

- **Coverage** — are new/changed code paths tested?
- **Edge cases** — empty inputs, boundaries, error paths tested?
- **Behavior vs implementation** — tests verify behavior, not internals?
- **BDD** — do tests clearly describe the expected behavior?
- **Flakiness** — tests depend on order, time, or external state?
- **Missing tests** — untested error handlers, validators, auth checks?

### Agent 4: Security Reviewer

Focus: security vulnerabilities and data protection.

- **Input validation** — all external input validated at boundaries.
- **Injection** — SQL injection, XSS, command injection, path traversal.
- **Authentication** — auth checks on all protected routes.
- **Authorization** — proper permission checks, not just auth.
- **Secrets** — no hardcoded credentials, tokens, or API keys.
- **Error leaking** — sensitive data not exposed in error messages or logs.
- **Dependencies** — known vulnerabilities in added/updated packages.
- **CORS/CSRF** — proper configuration for web APIs.

### Consolidated Output

Merge findings from all agents into a single report sorted by severity:

```text
## Summary
[approve | request changes | comment only]

## Critical (must fix)
...

## Warnings (should fix)
...

## Suggestions (nice to have)
...

## What Looks Good
...
```

## Constraints

- Review produces feedback, not code -- do not make changes.
- Do not nitpick style the linter handles.
- Do not review generated files (lock files, migrations, vendor).

## Related

- `commands/verify.md` — adversarial verification (run the code, not just read it).
- `commands/refactor.md` — apply review findings via refactoring.
