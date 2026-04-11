---
name: documentation
description: Documentation patterns -- ADRs, changelogs, README structure, docstrings, auto-generation, Mermaid diagrams. Load when writing or organizing project documentation.
---

# Documentation

Standards and patterns for project documentation.

## README Structure

```markdown
# Project Name -- Brief description (1-2 sentences)

## Features

## Quick Start -- Installation and first run in < 5 commands

## Usage -- Key use cases with runnable code examples

## API Reference -- Link to auto-generated docs

## Configuration -- Environment variables and settings

## Development -- Setup, testing, contributing

## License
```

Quick Start must be copy-paste ready. Usage examples must be runnable.

## Architecture Decision Records (ADRs)

```markdown
# ADR-{number}: {Title}

## Status -- Proposed | Accepted | Deprecated | Superseded by ADR-{n}

## Context -- What problem are we facing?

## Decision -- What did we decide and why?

## Consequences -- Trade-offs. What becomes easier? Harder?
```

- Create when choosing databases, frameworks, architecture patterns, API versioning.
- Number sequentially. Store in `docs/adr/`. Never delete -- mark deprecated.

## Changelogs

Follow [Keep a Changelog](https://keepachangelog.com/):
Categories: Added, Changed, Deprecated, Removed, Fixed, Security.
Write entries as you work, describing user-facing changes.

## Docstrings

Google style. Document non-obvious behavior, not what the signature says.

- **Always**: public functions/classes in libraries
- **Usually**: complex business logic, non-obvious algorithms
- **Skip**: private methods, trivial wrappers, test functions

## Auto-Generated Docs

- **MkDocs** (recommended): `mkdocs-material` + `mkdocstrings`
- **Sphinx**: for larger libraries with cross-references
- **FastAPI**: auto-generates OpenAPI at `/docs` and `/redoc`

## Mermaid Diagrams

| Type              | When                                     |
| ----------------- | ---------------------------------------- |
| `flowchart`       | System architecture, data flow           |
| `sequenceDiagram` | API interactions, request/response flows |
| `erDiagram`       | Database schema, entity relationships    |
| `classDiagram`    | Domain models, class hierarchies         |
| `stateDiagram`    | State machines, workflow states          |

Keep diagrams small and focused. Update when architecture changes.

## GitHub Wiki

Separate git-backed docs for user guides, FAQ, onboarding.
Clone: `git clone https://github.com/user/repo.wiki.git`
Use `_Sidebar.md` for navigation, hyphenated page names.

## GitHub Pages

For public-facing doc sites. Use MkDocs + `mkdocs gh-deploy`.

## Related

- `skills/markdown/SKILL.md` -- Markdown writing and structure
- `commands/plan.md` -- SPEC.md, ARCH.md templates
