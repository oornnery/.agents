---
name: hooks
description: Hook design and maintenance for local automation. Use when creating, renaming, wiring, reviewing, or debugging hooks, hook matchers, JSON payload handling, lifecycle reminders, autofix behavior, or safety gates.
---

# Hooks

Use skill for local hook automation, wiring, policies. Hooks small, predictable, easy smoke test.

## Boundary

Covers:

- hook scripts in `hooks/*.sh`
- hook wiring in `templates/settings/local.hooks.json`
- local hook behavior: reminders, gates, autofix, lifecycle helpers
- portability across Claude Code, Codex, and OpenCode when their hook systems can call shell scripts

Not replace:

- `skills/security/SKILL.md` for threat modeling or secret handling
- `skills/docs/SKILL.md` for broader docs structure
- `skills/rtk/SKILL.md` for RTK behavior itself

## Current hook surfaces

- `hooks/autofix.sh` for file-type-aware formatting helpers
- `hooks/git-safety-gate.sh` for unsafe git command blocking
- `hooks/session-context.sh` for session-start context
- `hooks/project-state-reminder.sh` for SPEC/DESIGN/TODO/.spec/.mem reminders
- `hooks/compact-state.sh` and `hooks/compact-reminder.sh` for compaction lifecycle
- `hooks/stop-reminders.sh` for end-of-session reminders
- `hooks/rtk-rewrite.sh` for RTK integration
- `hooks/desktop-notify.sh` for local notifications

## Assets

Use when full hook example beats isolated snippets.

- `assets/project/hooks/git-safety-gate.sh` -- focused blocker hook
- `assets/project/hooks/session-context.sh` -- JSON-emitting reminder hook
- `assets/project/templates/settings/local.hooks.json` -- matching local settings wiring

## Principles

- smallest hook enforcing behavior
- blocker hooks for truly unsafe or policy-critical actions
- reminder hooks for guidance, not annoyance
- structured JSON; prefer `jq` over hand-built JSON strings
- stderr messages short, direct, actionable
- idempotent where possible
- fail closed only when continuing risk > interruption
- fail open for convenience helpers when fallback safe

## Workflow

### 1. Define the event and intent

Decide:

- which event triggers hook
- blocker, reminder, formatter, or state helper
- minimal matcher

### 2. Keep the script focused

Each hook one job:

- inspect input
- decide
- print short message
- exit clearly

No broad automation hidden inside safety gate.

### 3. Wire it once

Reflect in `templates/settings/local.hooks.json` for Claude Code-style wiring, or
the equivalent local hook config for Codex/OpenCode:

- accurate matcher
- short description
- correct command path

### 4. Validate the right layer

Validate scripts:

```bash
bash -n hooks/*.sh
```

Validate settings wiring:

```bash
jq empty templates/settings/local.hooks.json
```

Smoke test changed hook with smallest reproducible input.

## Guardrails

- no destructive git ops in hooks
- no silently swallowing important failures
- no turning reminder into blocker without concrete safety reason
- no duplicating same policy in multiple hooks unless events differ
- no network-dependent behavior in routine local hooks
- no automatic memory writes from hooks; hooks may remind, agents update state explicitly
