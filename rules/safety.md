---
description: Safety and production protection rules -- applies to all actions
globs: "**"
---

# Safety

## Before Any Action

Evaluate: reversibility, blast radius, scope match with request.

## Confirmation Required

- **Destructive**: deleting files/branches, dropping tables, `rm -rf`
- **Hard-to-reverse**: force push, amending published commits, removing deps
- **Visible to others**: pushing code, creating/closing PRs/issues, sending messages
- **Production-affecting**: deployments, migrations on prod, infra changes

## Standing Rules

- Approval once does **not** mean approval in all contexts
- Prioritize immediate correction of failing tests
- Investigate unexpected state before deleting -- it may be in-progress work
- Resolve merge conflicts rather than discarding changes
- Diagnose root causes before switching tactics -- do not retry blindly
