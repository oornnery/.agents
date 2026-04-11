---
name: tdd
description: Test-Driven Development workflow. Use when implementing a new feature or fixing a bug where tests should drive the implementation.
---

# TDD

Implement features using the Red/Green/Refactor cycle. Tests come first.

## Agent Routing

For enforcement, invoke `agents/tdd-guide.md` (model: sonnet). The agent
ensures the cycle is followed and tests are written before code.

## Workflow

### 1. Define the Interface

Before writing any code, define:

- Function signature (name, params, return type)
- Expected behavior for happy path
- Edge cases and error conditions
- Where it fits in the existing architecture

### 2. RED -- Write Failing Test

```bash
# Create test file if needed
# Write test describing ONE behavior
uv run pytest tests/unit/test_<module>.py::test_<name> -x -v
# Confirm: test FAILS for the expected reason
```

Naming: `test_given_<precondition>_when_<action>_then_<expected>`

### 3. GREEN -- Minimal Implementation

Write the simplest code that makes the test pass. No optimization,
no elegance -- just green.

```bash
uv run pytest tests/unit/test_<module>.py::test_<name> -x -v
# Confirm: test PASSES
```

### 4. REFACTOR -- Clean Up

Improve structure without changing behavior:

- Extract helpers if duplicated
- Improve naming
- Simplify logic

```bash
uv run pytest -v  # Full suite stays GREEN
```

### 5. Repeat

Next behavior -> next test -> next implementation. Each cycle: minutes.

### 6. Verify Coverage

```bash
uv run pytest --cov=src --cov-report=term-missing -v
# Target: >80% branch coverage on new code
```

## What to Test

- Business logic and domain rules
- Edge cases: empty, None, boundaries, max values
- Error paths: invalid input, missing data, exceptions
- Integration points: API contracts, database queries

## Constraints

- Never write production code without a failing test first.
- One behavior per test. One assertion per concept.
- If a test is hard to write, the design needs improvement.
- Reference `skills/tdd/SKILL.md` for methodology details.
