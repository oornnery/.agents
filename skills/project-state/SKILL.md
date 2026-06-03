---
name: project-state
description: Manage lightweight project state files such as SPEC.md, DESIGN.md, TODO.md, .spec/, and .mem/. Use when starting multi-step work, planning features, recording decisions, updating next steps, preserving cross-session context, or preparing handoff notes.
---

# Project State

Use this skill to keep durable project context current without bloating `AGENTS.md`.

## Files

Top-level docs:

- `SPEC.md` -- user goal, scope, requirements, success criteria, validation plan
- `DESIGN.md` -- architecture, UX/API decisions, product/design constraints
- `TODO.md` -- active task list, next steps, blocked items, done items

Operational state:

- `.spec/state.md` -- current objective, done, next steps, validation, open questions
- `.spec/checks.md` -- known validation commands and latest meaningful results
- `.spec/handoff.md` -- concise handoff for the next agent/session

Memory:

- `.mem/hot.md` -- stable high-value facts, max 80 lines
- `.mem/decisions.md` -- accepted decisions with date, reason, impact
- `.mem/open-loops.md` -- unresolved questions, blockers, follow-ups

## When to Create

Create or update these files when work is multi-step, spans sessions, changes product/architecture/design direction, or leaves meaningful next steps.

Do not create state files for trivial one-file fixes unless the repo already uses them.

## Workflow

1. At session start, read existing `SPEC.md`, `DESIGN.md`, `TODO.md`, `.spec/state.md`, and `.mem/hot.md` if present.
2. Before implementation, record success criteria in `SPEC.md` or `.spec/state.md` when scope is non-trivial.
3. During work, update `.spec/state.md` with done/next/validation only after facts are verified.
4. After decisions, append durable choices to `.mem/decisions.md` or `DESIGN.md`.
5. Before stopping, update `TODO.md`, `.spec/handoff.md`, and `.mem/open-loops.md` when work remains.

## Rules

- Keep `AGENTS.md` stable; put project-specific state in these files.
- Keep `.mem/hot.md` short and factual. No transcripts, guesses, secrets, credentials, tokens, or private user data.
- Write dates as `YYYY-MM-DD`.
- Mark uncertainty as `UNKNOWN` or an explicit open question.
- Do not store tool output unless it is a concise validation result or reproducible command.
- Prefer updating existing state over creating duplicate docs.
- If a state file is stale or contradicted by code, update it or report the drift.

## Minimal State Shape

`.spec/state.md`:

```markdown
# Project State

## Current Objective

## Done

## Next Steps

## Validation

## Open Questions
```

`.mem/hot.md`:

```markdown
# Hot Memory

- [YYYY-MM-DD] Stable fact, decision, or preference.
```

## Handoff Shape

Use this before ending multi-step work:

```markdown
# Handoff

## Current State

## Completed

## Remaining

## Validation

## Risks
```
