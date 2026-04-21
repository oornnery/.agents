---
name: extract-pattern
description: Formalize a reusable pattern from recent work. Use when a non-obvious, repeated, proven technique should become a focused local pattern or skill.
---

# Extract Pattern

Extract a reusable pattern only when it is proven, non-obvious, and likely to
help again.

## Keep only patterns that are

- reusable
- non-obvious
- proven in practice

Skip:

- trivial fixes
- one-off hacks
- speculative ideas

## Process

### 1. Review the recent work

Look for:

- repeated decisions
- a technique that solved a real problem cleanly
- a guardrail that prevented recurrence
- a structure worth teaching again

### 2. Decide the right home

Choose one:

- existing skill ref
- new focused skill
- command or agent doc if it is really procedural

Do not duplicate the same idea in multiple places.

### 3. Write it small

Target roughly 30-80 lines and keep one pattern per document.

Use this shape:

```text
# Pattern Name

## When to Use

## Pattern

## Guardrails
```

Add examples only when they materially improve clarity.

### 4. Confirm before canonizing

Do not turn a pattern into repo guidance until the user has validated that it
is worth keeping.

## Constraints

- keep it focused
- prefer the smallest natural home
- avoid creating "learned" clutter that no one will use

## Related

- `commands/docs.md`
