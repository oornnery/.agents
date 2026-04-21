---
name: refactor
description: Behavior-preserving structural improvement. Use when the user asks to refactor, simplify, or improve maintainability without changing public behavior.
---

# Refactor

Refactor to improve structure, readability, or maintainability while preserving
external behavior.

## Process

### 1. Understand the current structure

Inspect:

- architecture and layout
- recent git history and momentum
- duplication, coupling, and readability problems
- validations that protect behavior

Load only the relevant skills:

- `skills/arch/SKILL.md` for structure, layering, and boundaries
- `skills/python/SKILL.md` for implementation patterns
- `skills/quality/SKILL.md` for regression guards
- `skills/security/SKILL.md` if the change touches sensitive code paths

### 2. Choose a narrow refactor target

Focus on one maintainability problem at a time, for example:

- duplicated logic
- unclear module boundaries
- high coupling
- poor naming in recently changed code
- deeply nested or hard-to-scan flow
- responsibilities mixed in one class or function

### 3. Refactor in small steps

- make one logical change at a time
- validate after each meaningful step
- preserve public behavior unless explicitly asked otherwise
- keep style churn out of the diff

### 4. Report clearly

Summarize:

- what was improved
- what was intentionally left alone
- what was validated
- any remaining risks or follow-up ideas

## Constraints

- preserve external behavior
- do not sneak in feature work
- do not rewrite stable code just because it looks old
- do not mix broad renames with structural changes unless required
- if you uncover a correctness or security bug that requires behavioral change,
  stop and surface it separately instead of folding it into the refactor

## Related

- `commands/review.md`
- `commands/verify.md`
