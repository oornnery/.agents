---
name: docs
description: Update and align documentation with the current system state. Use for README, docs pages, ADRs, changelogs, docstrings, skill docs, command docs, and agent docs.
---

# Docs

Update documentation so it matches the current code, workflow, and repo
structure. Optimize for clarity, scanability, and low drift.

## Scope

Use this command for:

- `README.md`
- docs pages and ADRs
- changelog entries
- docstrings when requested
- local `SKILL.md` files
- local `commands/*.md` and `agents/*.md`

## Skills to use

- `skills/docs/SKILL.md` always
- `skills/python/SKILL.md` for docstrings and Python usage docs
- `skills/arch/SKILL.md` for ADR or SDD updates
- `skills/design/SKILL.md` for API or UI docs
- `skills/cicd/SKILL.md` for CI docs
- `skills/hooks/SKILL.md` for hook docs, settings wiring, and lifecycle notes

## Source of truth

Document from the real implementation surface, not from memory.

Common sources:

- `pyproject.toml`, `uv.lock`, and task aliases for install, validation, and tooling docs
- `.env.example`, typed settings, and config loaders for configuration docs
- `.github/workflows/*.yml` or local workflow configs for CI docs
- `hooks/*.sh` and `templates/settings/local.hooks.json` for hook behavior and wiring docs
- local `skills/*/SKILL.md`, `commands/*.md`, and `agents/*.md` for this repo's operating docs

## Process

1. inspect the requested doc target and identify its source of truth
2. update only the document(s) derived from that source
3. keep examples specific, copy-pasteable, and aligned with the repo
4. remove stale paths, names, commands, and references
5. flag obsolete docs for removal when they no longer match any source of truth
6. run Markdown validation after editing

## Constraints

- do not change code logic while doing doc-only work
- prefer focused edits over broad rewrites
- keep top-level docs concise and move detail into focused pages when needed
- do not invent behavior that the code does not implement

## Related

- `skills/docs/SKILL.md`
- `skills/hooks/SKILL.md`
- `commands/review.md`
- `commands/commit.md`
