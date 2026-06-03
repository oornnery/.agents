---
name: state
description: Update lightweight project state files. Use after planning, implementation, verification, or handoff work that changes SPEC.md, DESIGN.md, TODO.md, .spec/, or .mem/.
---

# State

Keep project state current with verified facts and explicit next steps.

## Skills

- `skills/project-state/SKILL.md` -- always
- `skills/verification/SKILL.md` -- when updating validation status
- `skills/docs/SKILL.md` -- when editing top-level docs
- `skills/security/SKILL.md` -- when recording trust-boundary or security decisions

## Process

### 1. Read current state

Inspect existing files if present:

```bash
ls SPEC.md DESIGN.md TODO.md .spec/state.md .spec/checks.md .spec/handoff.md .mem/hot.md .mem/decisions.md .mem/open-loops.md 2>/dev/null
```

### 2. Classify the update

- Scope or requirement changed -> `SPEC.md` and `.spec/state.md`
- Architecture, API, UI, or product decision changed -> `DESIGN.md` and `.mem/decisions.md`
- Work remains -> `TODO.md`, `.spec/handoff.md`, `.mem/open-loops.md`
- Validation ran -> `.spec/checks.md` and `.spec/state.md`
- Stable cross-session fact emerged -> `.mem/hot.md`

### 3. Update only what changed

Write concise, dated entries. Use `UNKNOWN` for unresolved facts.

Do not store:

- secrets or credentials
- private data
- raw transcripts
- large command output
- speculative guesses

### 4. Validate docs

Run Markdown validation if configured:

```bash
uv run rumdl check SPEC.md DESIGN.md TODO.md .spec .mem
```

## Output

Report:

- files updated
- facts or decisions recorded
- next steps now visible
- validation command and result

## Constraints

- no automatic memory writes without inspecting current state
- no duplicate decisions across multiple files
- no changing code during state-only work
