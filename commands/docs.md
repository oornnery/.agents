---
name: docs
description: Update and align documentation with the current system state. Use for README, docs pages, ADRs, changelogs, docstrings, skill docs, command docs, and agent docs.
---

# Docs

Update docs to match current code, workflow, repo structure. Optimize clarity, scanability, low drift.

## Scope

- `README.md`
- docs pages, ADRs
- changelogs
- docstrings (when requested)
- local `SKILL.md`
- local `commands/*.md`, `agents/*.md`

## Skills

- `skills/docs/SKILL.md` — always
- `skills/python/SKILL.md` — docstrings, Python usage
- `skills/arch/SKILL.md` — ADR, SDD
- `skills/design/SKILL.md` — API, UI docs
- `skills/cicd/SKILL.md` — CI docs
- `skills/hooks/SKILL.md` — hook docs, settings wiring, lifecycle

## Source of truth

Doc from real implementation, not memory:

- `pyproject.toml`, `uv.lock`, task aliases — install, validation, tooling
- `.env.example`, typed settings, config loaders — configuration
- `.github/workflows/*.yml` — CI
- `hooks/*.sh`, `templates/settings/local.hooks.json` — hook behavior, wiring
- local `skills/*/SKILL.md`, `commands/*.md`, `agents/*.md` — operating docs

## Process

1. inspect target doc, identify source of truth
2. update only docs derived from that source
3. keep examples specific, copy-pasteable, repo-aligned
4. remove stale paths, names, commands, references
5. flag obsolete docs for removal when no source matches
6. run Markdown validation after editing

## Constraints

- no code logic changes during doc-only work
- focused edits over broad rewrites
- top-level docs concise; move detail into focused pages
- no invented behavior code doesn't implement

## Related

- `skills/docs/SKILL.md`
- `skills/hooks/SKILL.md`
- `commands/review.md`
- `commands/commit.md`