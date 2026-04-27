---
name: extract-pattern
description: Formalize reusable pattern from recent work. Use when non-obvious, repeated, proven technique should become focused local pattern or skill.
---

# Extract Pattern

Extract reusable pattern only when proven, non-obvious, likely to help again.

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
- technique that solved real problem cleanly
- guardrail that prevented recurrence
- structure worth teaching again

### 2. Decide the right home

Choose one:

- existing skill ref
- new focused skill
- command or agent doc if procedural

No duplicate ideas across multiple places.

### 3. Write it small

Target ~30-80 lines, one pattern per doc.

Use this shape:

```text
# Pattern Name

## When to Use

## Pattern

## Guardrails
```

Add examples only when they materially improve clarity.

### 4. Confirm before canonizing

No pattern → repo guidance until user validates worth keeping.

## Constraints

- focused
- prefer smallest natural home
- avoid "learned" clutter no one uses

## Related

- `commands/docs.md`
