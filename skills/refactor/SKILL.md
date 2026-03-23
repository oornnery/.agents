---
name: refactor
description: Deep audit and refactoring of the project or a specific area. Analyzes code for clean code principles, SOLID, security, readability, maintainability, and consistency. Use when the user asks to refactor, audit, clean up, improve code quality, or review architecture.
---

# Refactor

Perform a thorough audit and refactoring pass on the project (or a specific
area if the user provides a scope). The goal is to improve readability,
maintainability, and security without changing external behavior.

## Process

### Phase 1: Understand the Project

Before changing anything, build a mental model:

1. Read `CLAUDE.md` and any skill files relevant to the stack.
2. Scan the project structure — understand modules, layers, and boundaries.
3. Read recent git history (`git log --oneline -20`) to understand momentum.
4. Identify the architecture in use (layered, hexagonal, MVC, etc.).

### Phase 2: Audit

Launch parallel review agents focused on different concerns:

#### Agent 1: Clean Code and Readability

- **Naming** — functions, variables, classes, and modules have clear,
  intention-revealing names. No abbreviations, no single-letter vars outside
  tight loops.
- **Function size** — functions longer than 30 lines likely do too much.
  Extract sub-functions with descriptive names.
- **Parameter count** — more than 3-4 parameters suggests a missing
  abstraction (dataclass, config object, builder).
- **Comments** — delete comments that restate the code. Keep only WHY
  comments (hidden constraints, workarounds, non-obvious invariants).
- **Dead code** — remove unused imports, functions, variables, and
  unreachable branches.
- **Magic values** — replace literals with named constants or enums.

#### Agent 2: Architecture and SOLID

Apply whichever principles fit the project's paradigm:

- **Single Responsibility** — each module, class, and function has one
  reason to change.
- **Open/Closed** — extend behavior through composition or polymorphism,
  not by editing existing code paths.
- **Liskov Substitution** — subtypes must be substitutable for their base
  types without breaking callers.
- **Interface Segregation** — no client should depend on methods it does
  not use. Prefer small, focused protocols/interfaces.
- **Dependency Inversion** — high-level modules depend on abstractions,
  not concrete implementations. IO at edges only.

Also check:

- **Layer violations** — does a domain/service module import from the
  HTTP layer? Does a template import from the database layer?
- **Circular imports** — detect and break cycles.
- **God objects** — classes or modules that accumulate unrelated
  responsibilities.
- **Coupling** — modules that know too much about each other's internals.
- **DRY** — near-duplicate code that should be unified. But avoid
  premature abstraction — three instances is the threshold.

#### Agent 3: Security and Robustness

- **Input validation** — all external input (HTTP params, file uploads,
  environment variables, CLI args) is validated at the boundary.
- **SQL injection** — parameterized queries only, never f-string SQL.
- **XSS** — output escaping in templates. JX's `autoescape=True` covers
  Jinja, but check `| safe` and `Markup()` usage.
- **Path traversal** — user-supplied paths are resolved and confined.
- **Secret management** — no hardcoded secrets, tokens, or API keys.
  Check `.env` files are gitignored.
- **Dependency vulnerabilities** — flag known-vulnerable packages.
- **Error handling** — sensitive information not leaked in error messages
  or stack traces. Catch specific exceptions, not bare `except:`.
- **Authentication/authorization** — verify checks exist on protected
  routes and are not bypassable.
- **CSRF/CORS** — verify configuration if the project serves a web API.

### Phase 3: Prioritize

After the audit completes, consolidate findings and rank by impact:

1. **Security** issues — fix immediately.
2. **Correctness** bugs — fix immediately.
3. **Maintainability** wins with low risk — refactor.
4. **Readability** improvements — refactor.
5. **Nice-to-have** cleanups — refactor if trivial, otherwise note for later.

Skip findings that are false positives or not worth the churn. Do not argue
with findings — skip or fix.

### Phase 4: Refactor

Apply changes incrementally:

- One logical change at a time. Do not mix a rename with a structural refactor.
- After each change, run the project's validation suite (lint, type check,
  tests) before moving to the next change.
- If tests fail, fix the regression before continuing.
- Preserve all existing public APIs unless explicitly asked to break them.

### Phase 5: Report

Briefly summarize:

- What was found (grouped by category).
- What was fixed.
- What was intentionally skipped and why.
- Any recommendations that require user input or are out of scope.

## What NOT to Do

- **Do not change behavior.** Refactoring preserves external behavior.
  If a behavior change is needed, flag it and let the user decide.
- **Do not over-engineer.** Do not add abstractions "just in case."
  Three similar lines are better than a premature framework.
- **Do not add dependencies.** Do not introduce new libraries unless the
  user approves.
- **Do not rewrite from scratch.** Improve incrementally. A rewrite is a
  separate decision.
- **Do not touch generated files.** Lock files, migration files, and
  auto-generated code are off-limits unless broken.
- **Do not add comments** explaining what the code does — make the code
  self-explanatory instead.

## Stack-Specific Guidance

Load the relevant project skills before auditing:

- **Python**: `python/SKILL.md` — naming, typing, async, pathlib, logging.
- **FastAPI**: `fastapi/SKILL.md` — dependency injection, Annotated style.
- **JX**: `jx/SKILL.md` — component conventions, attrs, assets.
- **Frontend**: `frontend/SKILL.md` — Tailwind, Solid, accessibility.

Follow whichever conventions the project already uses. When conventions
conflict, prefer the project's established pattern over theoretical ideals.
Consistency within the codebase beats "correctness" in isolation.
