---
description: Safety and production protection rules — applies to all actions
globs: "**"
---

# Safety and Production Protection

## Reversibility Assessment

Before any action, evaluate:

- **Reversibility** — can this be undone easily?
- **Blast radius** — does this affect shared systems or other people?
- **Scope match** — does the action match what was actually requested?

## Confirmation Required

These actions always require explicit user confirmation:

- **Destructive operations**: deleting files/branches, dropping tables, `rm -rf`,
  overwriting uncommitted changes
- **Hard-to-reverse operations**: force push, `git reset --hard`, amending
  published commits, removing dependencies
- **Actions visible to others**: pushing code, creating/closing PRs or issues,
  sending messages, posting to external services
- **Production-affecting actions**: deployments, database migrations on prod,
  modifying infrastructure or permissions

## Standing Rules

- Approving an action once does **not** mean approval in all contexts
- Never skip hooks (`--no-verify`), bypass signing, or force push without
  explicit request
- Prioritize immediate correction of failing tests — test suite integrity
  is non-negotiable
- When encountering unexpected state (unfamiliar files, branches, configs),
  investigate before deleting or overwriting — it may be in-progress work
- Resolve merge conflicts rather than discarding changes
- If a lock file exists, investigate what holds it rather than deleting it

## Error Handling

- Diagnose root causes before switching tactics
- Do not retry the identical failing action blindly
- Do not use destructive actions as shortcuts to remove obstacles
- Read the error, check assumptions, try a focused fix first
