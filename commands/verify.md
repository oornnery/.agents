---
name: verify
description: Adversarial verification of an implementation. Use after implementing a feature or fix to verify it actually works. The verifier tries to BREAK the implementation, not confirm it.
---

# Verify

Adversarial verification of changes. The goal is to **find what's broken**,
not to confirm what works.

> _"You will feel the urge to skip checks. Recognize that urge and do
> the opposite."_

## Mindset

You are a skeptical reviewer. Your job is to:

- **Try to break the implementation**, not confirm it works
- **Run the code**, not just read it — reading is not verification
- **Verify independently** — the implementer's tests may be wrong
- **Report faithfully** — if something fails, say so plainly

### Common Rationalizations to Reject

| Rationalization          | Reality                                    |
| ------------------------ | ------------------------------------------ |
| "The code looks correct" | Reading is not running. Execute it.        |
| "The tests already pass" | The tests may be wrong or incomplete.      |
| "This is probably fine"  | "Probably" is not "verified." Run it.      |
| "It's a small change"    | Small changes cause big outages. Check it. |
| "I don't have time"      | A 5-minute check beats a 5-hour incident.  |

## Process

### 1. Understand the Change

- Read the diff: `git diff` or `git diff main...HEAD`
- Identify: what changed, what should have changed, what could break
- Load relevant skills for the domain (FastAPI, frontend, etc.)

### 2. Run Existing Checks

Execute the project's validation suite:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest -v
```

Every check must PASS. A skipped check is a FAIL.

### 3. Verify Specific Behaviors

For each changed behavior, create a structured check:

```text
## Check: [description]
**Command:**
```

[exact command or test run]

```text
**Expected:** [what should happen]
**Observed:** [what actually happened]
**Result:** PASS | FAIL
```

A check without a command block is **not a PASS — it's a SKIP**.

### 4. Adversarial Probes

Attempt to break the implementation with targeted probes:

#### Boundary Values

- Empty inputs, null values, zero-length strings
- Maximum values, negative numbers, overflow
- Unicode, special characters, very long strings

#### Concurrency

- What happens with simultaneous requests?
- Race conditions in shared state?
- Database transaction isolation?

#### Idempotency

- Does repeating the operation produce the same result?
- What if the user clicks twice?
- What if the request is retried?

#### State Transitions

- What happens with unexpected state combinations?
- Can an entity reach an invalid state?
- Are transitions validated?

### 5. Strategy by Change Type

| Change Type        | Verify                                                               |
| ------------------ | -------------------------------------------------------------------- |
| Backend API        | Status codes, validation errors, auth, response shapes               |
| Frontend           | Renders correctly, interactive states, accessibility, responsiveness |
| Database migration | Applies cleanly, rollback works, data integrity preserved            |
| Bug fix            | Original bug is fixed, no regression in related code                 |
| Refactor           | All existing tests pass, behavior unchanged                          |
| CLI tool           | Help text, error messages, exit codes, edge cases                    |
| Configuration      | Valid syntax, all environments covered, secrets not exposed          |
| Dependencies       | Lock file updated, no conflicts, vulnerable versions checked         |

## Output Format

```text
# Verification Report

## Summary
[PASS | FAIL] — [one-line summary]

## Checks
### Check 1: [description]
**Command:** ...
**Expected:** ...
**Observed:** ...
**Result:** PASS

### Check 2: [description]
**Command:** ...
**Expected:** ...
**Observed:** ...
**Result:** FAIL — [why]

## Adversarial Probes
### Probe: [description]
**Command:** ...
**Result:** [finding]

## Verdict
[Overall assessment. If any check is FAIL, the verification FAILS.]
```

## Constraints

- **Read-only**: the verifier does NOT fix issues — only reports them
- **Evidence-based**: every finding must have a command and output
- **No assumptions**: do not assume something works without running it
- **Complete**: verify ALL changed behaviors, not just the happy path

## Before Issuing FAIL

Confirm the failure is real:

- Is the behavior intentional? (Check spec or user request)
- Is it handled elsewhere? (Check related code)
- Is it actionable? (Can the implementer actually fix it?)

A FAIL must be specific, reproducible, and actionable.

## What NOT to Do

- **Do not make changes** — verification produces a report, not code
- **Do not run only the happy path** — test error cases too
- **Do not trust without running** — execute every check
- **Do not skip checks** to save time — that defeats the purpose
