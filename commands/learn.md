---
name: learn
description: Extract reusable patterns from the current session into a skill. Use after completing significant work where a repeatable pattern emerged.
---

# Learn

Extract reusable patterns from the current session and save them as
skills for future conversations.

## Process

### 1. Review Session Work

Look at what was accomplished:

- Files created or modified
- Problems solved and how
- Patterns that emerged
- Techniques that worked well

### 2. Identify Extractable Patterns

A pattern is worth extracting if it is:

- **Reusable** -- applies beyond this specific case
- **Non-obvious** -- not something the agent would do by default
- **Proven** -- actually worked in practice (not theoretical)

Skip: trivial fixes, one-time configurations, project-specific hacks.

### 3. Draft the Skill

Create `skills/learned/<pattern-name>/SKILL.md` following the format:

```markdown
---
name: <pattern-name>
description: <one-line description of when to use>
---

# <Pattern Name>

## When to Use

[Context that triggers this pattern]

## Pattern

[The technique, with code examples]

## Guardrails

[What to watch out for, common mistakes]
```

### 4. Confirm with User

Present the draft and ask:

- Is this pattern correct and complete?
- Should anything be added or removed?
- Is the naming clear?

### 5. Save

Write the skill file. Update `CLAUDE.md` skills table if it belongs
in a named category (otherwise it stays in `learned/`).

## Constraints

- One pattern per skill file. Keep it focused.
- Target 30-80 lines. Lean and scannable.
- Include working code examples, not just descriptions.
- Do not extract patterns the user hasn't validated.
