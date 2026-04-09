---
name: documentation
description: Documentation patterns — ADRs, changelogs, README structure, docstrings, auto-generation, Mermaid diagrams. Load when writing or organizing project documentation.
---

# Documentation

Standards and patterns for project documentation.

> _"Documentation is a love letter to your future self."_

## README Structure

```markdown
# Project Name

Brief description (1-2 sentences).

## Features

- Feature 1
- Feature 2

## Quick Start

Installation and first run in < 5 commands.

## Usage

Key use cases with code examples.

## API Reference

(Link to auto-generated docs or inline summary)

## Configuration

Environment variables and settings.

## Development

Setup, testing, and contributing guide.

## License

License type and link.
```

**Rules:**

- Quick Start must work in under 5 commands — copy-paste ready
- Usage examples must be runnable, not pseudocode
- Keep the README focused — link to detailed docs for deep dives

## Architecture Decision Records (ADRs)

Document decisions that affect the system's structure.

### Template

```markdown
# ADR-{number}: {Title}

## Status

Proposed | Accepted | Deprecated | Superseded by ADR-{n}

## Context

What problem are we facing? What forces are at play?

## Decision

What did we decide and why?

## Consequences

What are the trade-offs? What becomes easier? Harder?
```

### Workflow

1. Create ADR when making a significant architecture decision
2. Number sequentially: `ADR-001`, `ADR-002`, etc.
3. Store in `docs/adr/` or in ARCH.md for smaller projects
4. Never delete — mark as deprecated or superseded
5. Review ADRs during onboarding

### When to Write an ADR

- Choosing a database, framework, or major library
- Deciding on architecture pattern (monolith vs microservices)
- Changing API versioning strategy
- Introducing a new deployment pattern
- Any decision you'd need to explain in 6 months

## Changelogs

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

## [Unreleased]

### Added

- New user search endpoint with full-text search

### Changed

- Updated pagination to cursor-based for large collections

### Fixed

- Token refresh race condition under concurrent requests

## [1.2.0] - 2025-03-15

### Added

- OAuth2 authentication flow
- Rate limiting middleware

### Deprecated

- Basic auth (will be removed in 2.0.0)
```

**Categories:** Added, Changed, Deprecated, Removed, Fixed, Security.

**Rules:**

- Write entries as you work, not at release time
- Each entry describes the user-facing change, not the implementation
- Link to PRs or issues where relevant

## Docstrings

### Google Style (Preferred for Python)

```python
def create_user(name: str, email: str, role: str = "member") -> User:
    """Create a new user account and send a welcome email.

    Args:
        name: Full name of the user.
        email: Email address (must be unique).
        role: User role. Defaults to "member".

    Returns:
        The newly created User entity.

    Raises:
        DuplicateEmailError: If the email is already registered.
        ValidationError: If name or email is empty.
    """
```

### When to Write Docstrings

- **Always**: public functions and classes in libraries/packages
- **Usually**: complex business logic, non-obvious algorithms
- **Skip**: private methods, trivial wrappers, test functions
- **Never**: to explain WHAT the code does — make the code self-explanatory

### Module-Level Docstrings

```python
"""User authentication and session management.

This module handles OAuth2 flows, token generation, and session
lifecycle. It does NOT handle authorization (see auth/permissions.py).
"""
```

## Auto-Generated Documentation

### MkDocs (Recommended for Python Projects)

```yaml
# mkdocs.yml
site_name: My Project
theme:
  name: material
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
nav:
  - Home: index.md
  - API Reference: api/
  - Architecture: arch.md
  - ADRs: adr/
```

### Sphinx (For Larger/Library Projects)

Use when: building a public library, need cross-references, existing
Sphinx infrastructure.

### OpenAPI / FastAPI

FastAPI generates OpenAPI docs automatically at `/docs` (Swagger UI)
and `/redoc`. Enhance with:

- Detailed docstrings on route functions
- `response_model` for all endpoints
- `responses={}` for error status codes
- `tags=[]` for grouping in the docs UI

## Mermaid Diagrams

Use Mermaid for all visual documentation. Renders in GitHub, MkDocs,
and most Markdown viewers.

### When to Use Each Type

| Diagram               | When                                       |
| --------------------- | ------------------------------------------ |
| `graph` / `flowchart` | System architecture, data flow, user flows |
| `sequenceDiagram`     | API interactions, request/response flows   |
| `erDiagram`           | Database schema, entity relationships      |
| `classDiagram`        | Domain models, class hierarchies           |
| `stateDiagram`        | State machines, workflow states            |
| `gantt`               | Project timelines, release planning        |

### Tips

- Keep diagrams small and focused — one concept per diagram
- Use `subgraph` to group related components
- Label edges with the action or data being passed
- Update diagrams when the architecture changes

## Release Notes

```markdown
# Release v1.3.0

## Highlights

One paragraph summarizing the most important changes.

## New Features

- **User search** — full-text search across name and email fields
- **CSV export** — export user lists as CSV files

## Improvements

- Pagination now uses cursor-based approach for better performance
- Error messages include field-level details

## Bug Fixes

- Fixed token refresh race condition (#142)
- Fixed timezone handling in scheduled tasks (#138)

## Breaking Changes

- Removed `GET /api/v1/users/search` — use query params on `GET /api/v2/users`
- `created_at` field now returns UTC timestamps (was local time)

## Migration Guide

Steps to upgrade from v1.2.x to v1.3.0.
```

## GitHub Wiki

GitHub Wikis provide a separate git-backed documentation space alongside
the main repository. Useful for user-facing docs, guides, and knowledge
bases that don't belong in the code tree.

### When to Use Wiki vs In-Repo Docs

| Use Wiki                           | Use In-Repo (`docs/`)            |
| ---------------------------------- | -------------------------------- |
| User guides and tutorials          | API reference (auto-generated)   |
| Onboarding and setup instructions  | ADRs (tied to code decisions)    |
| FAQ and troubleshooting            | CHANGELOG (tied to releases)     |
| External contributor documentation | Configuration reference          |
| Meeting notes and decisions        | Architecture docs (near code)    |

### Wiki Structure

```text
Home.md                    # Landing page (auto-linked from repo sidebar)
Getting-Started.md         # Installation and first run
Architecture-Overview.md   # High-level system design
API-Guide.md               # How to use the API
Deployment-Guide.md        # How to deploy
Troubleshooting.md         # Common issues and fixes
_Sidebar.md                # Custom sidebar navigation
_Footer.md                 # Custom footer for all pages
```

### Managing Wiki via Git

The wiki is a separate git repository:

```bash
# Clone the wiki repo
git clone https://github.com/user/repo.wiki.git

# Edit, commit, push like normal
cd repo.wiki
# ... edit files ...
git add -A && git commit -m "docs: update getting started guide"
git push origin master
```

### Wiki with `gh` CLI

```bash
# There is no direct gh wiki command, but you can:
# 1. Clone via git (above)
# 2. Link to wiki pages in issues/PRs
# 3. Reference wiki in README: [Guide](../../wiki/Getting-Started)
```

### Tips

- Use `_Sidebar.md` to create persistent navigation across all pages
- Use `_Footer.md` for links back to the repo, issue tracker, etc.
- Keep page names hyphenated (`Getting-Started.md`) — GitHub converts
  spaces to hyphens in URLs
- Images go in a wiki `images/` folder or use GitHub-hosted URLs
- Wiki search is built-in — no extra setup needed

## GitHub Pages

For public-facing documentation sites, GitHub Pages hosts static sites
from a branch or `docs/` folder.

### Setup with MkDocs

```bash
# Install MkDocs with Material theme
uv add --dev mkdocs-material mkdocstrings[python]

# Create docs structure
mkdocs new .

# Serve locally
uv run mkdocs serve

# Deploy to GitHub Pages
uv run mkdocs gh-deploy
```

### GitHub Actions for Pages

```yaml
name: Docs
on:
  push:
    branches: [main]
    paths: ["docs/**", "mkdocs.yml"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync --frozen
      - run: uv run mkdocs gh-deploy --force
```

### When to Use Pages vs Wiki

- **Pages**: polished public docs, API reference, project website
- **Wiki**: internal knowledge base, quick guides, collaborative editing

## GitHub Discussions and Issues as Documentation

Use GitHub features as living documentation:

- **Discussions (Q&A category)**: searchable knowledge base of answered
  questions — pin important ones
- **Issue templates**: standardize bug reports and feature requests with
  required fields
- **PR templates**: ensure every PR has context (summary, test plan)
- **Labels**: categorize issues for discoverability (`bug`, `docs`,
  `good first issue`)

### Issue Template Example

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report a bug
labels: [bug]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: What happened?
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
```

### PR Template Example

```markdown
<!-- .github/pull_request_template.md -->
## Summary

What this PR does and why.

## Test Plan

- [ ] Unit tests pass
- [ ] Manual testing done
- [ ] No breaking changes (or documented)

## Related Issues

Closes #
```

## Related

- `skills/markdown/SKILL.md` — Markdown writing and structure
- `commands/plan.md` — SPEC.md, ARCH.md, SDD.md templates
- `commands/commit.md` — tags, PRs, releases, publishing workflow
- `skills/architecture/SKILL.md` — ADR patterns and architecture docs
- `skills/cicd/SKILL.md` — GitHub Actions, container builds, publishing
