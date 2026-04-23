---
name: refactor
description: Behavior-preserving structural improvement. Use when the user asks to refactor, simplify, or improve maintainability without changing public behavior.
---

# Refactor

Refactor: improve structure, readability, maintainability. Preserve external behavior.

## Process

### 1. Understand the current structure

Inspect:

- architecture, layout
- recent git history, momentum
- duplication, coupling, readability problems
- validations protecting behavior

Load relevant skills:

- `skills/arch/SKILL.md` for structure, layering, boundaries
- `skills/python/SKILL.md` for impl patterns
- `skills/quality/SKILL.md` for regression guards
- `skills/security/SKILL.md` if change touches sensitive code paths

### 2. Choose narrow refactor target

One maintainability problem at a time:

- duplicated logic
- unclear module boundaries
- high coupling
- poor naming in recently changed code
- deeply nested or hard-to-scan flow
- mixed responsibilities in one class/function

### 3. Refactor in small steps

- one logical change at a time
- validate after each meaningful step
- preserve public behavior unless explicitly asked
- keep style churn out of diff

### 4. Report clearly

Summarize:

- what improved
- what intentionally left alone
- what validated
- remaining risks or follow-up ideas

## Constraints

- preserve external behavior
- no sneaked feature work
- don't rewrite stable code just because old
- don't mix broad renames with structural changes unless required
- if correctness or security bug found requiring behavioral change, stop and surface separately -- don't fold into refactor

## Related

- `commands/review.md`
- `commands/verify.md`