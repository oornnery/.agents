---
name: markdown
description: Markdown writing and rumdl guidance. Use when creating or
  refactoring README and docs content, enforcing Markdown structure,
  configuring or running rumdl, improving headings, lists, tables, links, and
  code fences, or reviewing documentation quality.
---

# Markdown

Use this skill when the task is primarily about documentation quality,
structure, or Markdown linting.

## Documentation

- Markdown Guide: <https://www.markdownguide.org/>
- CommonMark: <https://spec.commonmark.org/>
- rumdl: <https://rumdl.com/docs/>

## Load These References

| Reference                      | When to load                                 |
| ------------------------------ | -------------------------------------------- |
| `references/best-practices.md` | Writing style, headings, tables, code fences |
| `references/rumdl.md`          | rumdl install, config, commands, validation  |

## Core Workflow

1. Keep prose scannable and structurally consistent before optimizing wording.
2. Prefer short sections, explicit headings, and fenced code blocks with an
   info string.
3. Use `rumdl` to validate the result after editing Markdown-heavy content.

## Rules of Thumb

- Prefer one topic per section.
- Keep heading depth shallow unless the document genuinely needs nesting.
- Use lists for enumerations, not for every paragraph.
- Keep tables for dense comparisons, not long prose.
- Use reference files for detailed policy and keep top-level docs focused.
- When a repo already has a Markdown style, follow it before introducing a new
  structure.
