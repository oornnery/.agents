---
name: skill-builder
description: Create or refactor local skills with clear triggers and low
  context overhead. Use when adding a new skill, reorganizing a skill into
  references, reducing duplication between skills, or improving skill quality
  and taxonomy.
---

# Skill Builder

Use this skill when creating or refactoring a local skill. Optimize for clear
triggering, progressive disclosure, and minimal duplication with existing
skills, commands, agents, and repo guidance.

## Boundary

This skill covers:

- creating a new local skill under `skills/`
- restructuring a large skill into `references/`
- tightening metadata, taxonomy, and trigger descriptions
- removing redundancy between `SKILL.md` and detailed references

## Principles

- prefer extending an existing skill or ref before creating a new skill
- keep `SKILL.md` lean and procedural
- move detailed examples, variants, and deep reference material into
  `references/`
- write descriptions around trigger conditions, not vague topics
- avoid duplicating repo-wide rules that already belong elsewhere
- keep one skill responsible for one clear domain or workflow

## Workflow

### 1. Choose the smallest natural home

Prefer this order:

1. existing ref inside an existing skill
2. existing skill with a clearer `SKILL.md`
3. new skill only when the gap is real and recurring

### 2. Write strong metadata

Frontmatter should make triggering obvious:

- what the skill is for
- when it should be used
- what kinds of requests should activate it

### 3. Keep `SKILL.md` to the essentials

Put in `SKILL.md`:

- purpose
- boundary
- workflow
- selection guidance for refs
- guardrails

Move to `references/`:

- long examples
- variant-specific guidance
- framework-specific details
- large checklists or catalogs

### 4. Avoid duplication

Do not repeat the same content across:

- `SKILL.md` and `references/`
- sibling skills
- commands or agents unless their mandate truly differs

### 5. Validate the skill

Check:

- the name is short and understandable
- the description is specific enough to trigger correctly
- refs are linked clearly from `SKILL.md`
- the skill matches the current repo taxonomy

Run:

```bash
uv run rumdl check skills/*/SKILL.md skills/*/references/*.md
```

## Guardrails

- do not create README or changelog files inside a skill
- do not make `SKILL.md` a dumping ground for all related knowledge
- do not create nested reference chains when one level is enough
- do not split a skill into refs unless the split improves selection and
  context use
