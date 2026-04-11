---
globs: "**"
---

# Performance

Model selection and agent cost conventions.

## Model Selection

Choose the cheapest model that handles the task:

1. **haiku** -- documentation, simple renames, formatting (3x cheaper than sonnet)
2. **sonnet** -- default for implementation, review, debugging
3. **opus** -- only for deep reasoning, architecture, ambiguous specs

## Agent Efficiency

- Keep agent definitions lean (<60 lines). Knowledge belongs in skills.
- Prefer Grep/Glob over Bash for search (structured results, less noise).
- Read only the relevant section of large files (use offset/limit).
