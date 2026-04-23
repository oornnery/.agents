---
name: docs
description: Documentation patterns for Markdown structure, README shape, ADRs, changelogs, diagrams, docstrings, and rumdl. Load when writing, refactoring, or validating docs.
---

# Docs

Use this skill when improving project documentation, not only writing prose.

## Boundary

Use this skill for document structure, readability, docs workflows, ADRs,
changelogs, and Markdown quality.

- pair with `python` when doc work is mainly docstrings or Python usage docs
- pair with `arch` when document is an ADR or SDD about boundaries and rollout
- pair with `design` when documenting API contracts or UI decisions

This skill shapes the documentation artifact itself, not replaces domain-specific
guidance of the other skills.

## Core Workflow

1. keep document easy to scan
2. prefer explicit headings over long uninterrupted text
3. keep examples copyable and runnable-looking
4. run `rumdl` after editing Markdown-heavy content

## README Structure

```markdown
# Project Name -- Brief description (1-2 sentences)

## Features

## Quick Start -- Installation and first run in < 5 commands

## Usage -- Key use cases with runnable examples

## Configuration -- Environment variables and settings

## Development -- Setup, testing, contributing

## License
```

Quick Start must be copy-paste ready. Usage examples runnable or close enough
to paste with minimal edits.

## ADRs

Use ADRs for meaningful technical decisions.

```markdown
# ADR-{number}: {Title}

## Status -- Proposed | Accepted | Deprecated | Superseded

## Context

## Decision

## Consequences
```

- create for major architecture, storage, integration, or versioning choices
- number sequentially
- deprecate or supersede old ADRs instead of deleting

## Changelogs

Follow [Keep a Changelog](https://keepachangelog.com/):

- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

Write entries as work happens; do not reconstruct whole release from memory later.

## Markdown Structure

### Headings

- start with one `#` title
- increase heading depth one level at a time
- keep headings short and descriptive
- avoid empty sections and one-line stub headings

### Paragraphs and Lists

- prefer short paragraphs over dense walls of text
- use bullets for enumerations, commands, and checklists
- keep bullet phrasing parallel when possible
- avoid deep nesting unless hierarchy essential

### Code Blocks

- always fence multi-line code
- add info string such as `bash`, `python`, `toml`, or `json`
- keep examples minimal but realistic
- prefer one command per line in shell examples

### Links and Tables

- use descriptive link text
- use tables only when matrix genuinely compact
- prefer sections or bullets when explanations longer than a phrase

### Readability

- prefer explicit names over shorthand
- preserve local style unless it harms readability or lint compliance
- delete duplicated guidance instead of maintaining two versions

## Docstrings

Document non-obvious behavior, invariants, constraints, and side effects.
Do not restate the signature.

- always: public library APIs
- usually: complex business logic or tricky algorithms
- skip: trivial wrappers, obvious private helpers, most tests

## Mermaid

| Type              | When                                     |
| ----------------- | ---------------------------------------- |
| `flowchart`       | system architecture and data flow        |
| `sequenceDiagram` | request/response or async interaction    |
| `erDiagram`       | schema and entity relationships          |
| `classDiagram`    | domain models and responsibilities       |
| `stateDiagram`    | workflows and explicit state transitions |

Keep diagrams small, focused, and close to the part of the system they explain.

## Auto-Generated Docs

- use MkDocs for lightweight doc sites
- use Sphinx when cross-references and API-heavy docs dominate
- keep generated API docs supplemental; top-level docs still need narrative guidance

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

## Rules of Thumb

- keep top-level docs focused; move detail to focused docs when needed
- document decisions, not just usage
- examples beat abstract explanation
- if doc is hard to scan, it will not get used