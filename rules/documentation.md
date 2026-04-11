---
description: Documentation standards — applies to Markdown files
globs: "**/*.md"
---

# Documentation Standards

- Scannable structure — use headings, short paragraphs, bullet lists
- One topic per section, shallow heading depth (prefer h2/h3, avoid h4+)
- Fenced code blocks with language tags for all code examples
- Tables for structured reference data
- Keep lines readable — no hard wraps, let the editor handle it
- Run `uv run rumdl check . --fix` before committing Markdown (or `uvx rumdl check . --fix` for non-Python projects)
- Use `docs/` directory for project documentation beyond README
- Use GitHub wiki as git submodule for user-facing docs when applicable
- Structure docs as: `docs/getting-started.md`, `docs/api.md`, `docs/architecture.md`
- Keep README.md focused — link to `docs/` for detailed content
