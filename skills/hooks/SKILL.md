---
name: hooks
description: Hook design and maintenance for local automation. Use when creating, renaming, wiring, reviewing, or debugging hooks, hook matchers, JSON payload handling, lifecycle reminders, autofix behavior, or safety gates.
---

# Hooks

Use this skill when working on local hook automation, hook wiring, or hook
policies. Keep hooks small, predictable, and easy to smoke test.

## Boundary

This skill covers:

- hook scripts in `hooks/*.sh`
- hook wiring in `templates/settings/local.hooks.json`
- local hook behavior such as reminders, gates, autofix, and lifecycle helpers

This skill does not replace:

- `skills/security/SKILL.md` for actual threat modeling or secret handling
- `skills/docs/SKILL.md` for broader documentation structure
- `skills/rtk/SKILL.md` for RTK behavior itself

## Current hook surfaces

- `hooks/autofix.sh` for file-type-aware formatting helpers
- `hooks/git-safety-gate.sh` for unsafe git command blocking
- `hooks/session-context.sh` for session-start context
- `hooks/compact-state.sh` and `hooks/compact-reminder.sh` for compaction lifecycle
- `hooks/stop-reminders.sh` for end-of-session reminders
- `hooks/rtk-rewrite.sh` for RTK integration
- `hooks/desktop-notify.sh` for local notifications

## Assets

Use these when a full hook example is more useful than isolated snippets.

- `assets/project/hooks/git-safety-gate.sh` -- a focused blocker hook
- `assets/project/hooks/session-context.sh` -- a JSON-emitting reminder hook
- `assets/project/templates/settings/local.hooks.json` -- the matching local
  settings wiring

## Principles

- choose the smallest hook that enforces the behavior
- keep blocker hooks for truly unsafe or policy-critical actions
- use reminder hooks for guidance, not annoyance
- emit structured JSON safely; prefer `jq` over hand-built JSON strings
- keep stderr messages short, direct, and actionable
- make hooks idempotent when possible
- fail closed only when the risk of continuing is higher than the interruption
- fail open for convenience helpers when the fallback is still safe

## Workflow

### 1. Define the event and intent

Decide:

- which event should trigger the hook
- whether it is a blocker, reminder, formatter, or state helper
- what the minimal matcher should be

### 2. Keep the script focused

Each hook should do one job:

- inspect input
- decide
- print a short message
- exit clearly

Do not hide broad automation inside a safety gate.

### 3. Wire it once

Reflect the behavior in `templates/settings/local.hooks.json` with:

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

Then smoke test the changed hook with the smallest reproducible input.

## Guardrails

- do not use destructive git operations in hooks
- do not silently swallow important failures
- do not turn a reminder into a blocker without a concrete safety reason
- do not duplicate the same policy in multiple hooks unless the events differ
- do not add network-dependent behavior to routine local hooks
