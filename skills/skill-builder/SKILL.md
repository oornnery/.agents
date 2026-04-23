---
name: skill-builder
description: Create or refactor local skills with clear triggers and low
  context overhead. Use when adding a new skill, reorganizing a skill into
  references, reducing duplication between skills, or improving skill quality
  and taxonomy.
---

# Skill Builder

Use when creating or refactoring local skills. Optimize for clear triggering, progressive disclosure, minimal duplication.

## Boundary

Covers:

- creating new local skill under `skills/`
- restructuring large skill into `references/`
- tightening metadata, taxonomy, trigger descriptions
- removing redundancy between `SKILL.md` and detailed references

## Principles

- prefer extending existing skill or ref over creating new skill
- keep `SKILL.md` lean and procedural
- move detailed examples, variants, deep reference material into `references/`
- write descriptions around trigger conditions, not vague topics
- avoid duplicating repo-wide rules already covered elsewhere
- one skill = one clear domain or workflow

## Workflow

### 1. Choose the smallest natural home

Prefer this order:

1. existing ref inside existing skill
2. existing skill with clearer `SKILL.md`
3. new skill only when gap is real and recurring

### 2. Write strong metadata

Frontmatter should make triggering obvious:

- what skill is for
- when it should be used
- what requests activate it

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

Do not repeat same content across:

- `SKILL.md` and `references/`
- sibling skills
- commands or agents unless their mandate truly differs

### 5. Validate the skill

Check:

- name is short and understandable
- description is specific enough to trigger correctly
- refs linked clearly from `SKILL.md`
- skill matches current repo taxonomy

Run:

```bash
uv run rumdl check skills/*/SKILL.md skills/*/references/*.md
```

## Guardrails

- do not create README or changelog files inside a skill
- do not make `SKILL.md` a dumping ground for all related knowledge
- do not create nested reference chains when one level is enough
- do not split skill into refs unless split improves selection and context use