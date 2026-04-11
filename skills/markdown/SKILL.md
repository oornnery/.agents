---
name: markdown
description: Markdown writing, rumdl configuration, and documentation best practices. Use when creating or refactoring docs, enforcing structure, or running rumdl.
---

# Markdown

## Core Workflow

1. Keep prose scannable and structurally consistent.
2. Prefer short sections, explicit headings, and fenced code blocks.
3. Run `rumdl` after editing Markdown-heavy content.

## Headings

- Start with a single `#` title.
- Increase heading depth one level at a time.
- Keep headings short and descriptive.
- Avoid empty sections and one-off headings with a single sentence under them.
- Prefer h2/h3, avoid h4+ unless the document genuinely needs deep nesting.

## Paragraphs and Lists

- Prefer short paragraphs over dense walls of text.
- Use bullets for enumerations, commands, and checklists.
- Keep bullet phrasing parallel where possible.
- Avoid deeply nested lists unless hierarchy is essential.

## Code Blocks

- Always fence multi-line code blocks.
- Add an info string such as `bash`, `python`, `toml`, `js`, or `html`.
- Keep examples minimal but executable-looking.
- Prefer one command per line in shell examples.

## Links and References

- Use descriptive link text.
- Link the first meaningful mention of a tool or spec when it helps orientation.
- Avoid dumping raw URLs in the middle of prose unless the URL itself matters.

## Tables

- Use tables for compact comparisons or matrices.
- Keep cell text short.
- Prefer bullets or sections when explanations are longer than a phrase.

## Readability

- Keep documents scannable.
- Prefer explicit names over shorthand.
- Avoid decorative formatting that does not add structure.
- When editing an existing doc, preserve local style unless it blocks
  readability or lint compliance.

## Rumdl

### Install

```bash
uv tool install rumdl
```

### Common Commands

```bash
uv run rumdl check .
uv run rumdl check --fix .
uv run rumdl fmt .
uv run rumdl init
```

### Recommended `.rumdl.toml`

```toml
[global]
disable = ["MD013", "MD033"]
exclude = ["node_modules", "dist", "build", "target"]
respect_gitignore = true

[MD003]
style = "atx"

[MD007]
indent = 4

[MD060]
enabled = true
style = "aligned"
```

### Usage Notes

- Use `check` in CI and validation flows.
- Use `check --fix` when the repo accepts automatic Markdown rewrites.
- Use `fmt` when you want formatting without applying other lint fixes.
- Keep config close to the repo root unless the project already centralizes it
  elsewhere.

## Rules of Thumb

- Follow existing repo Markdown style before introducing new structure.
- Use reference files for detailed policy; keep top-level docs focused.

## Related

- `skills/documentation/SKILL.md` -- README structure, ADRs, changelogs
- `rules/documentation.md` -- always-on Markdown conventions
