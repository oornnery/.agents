---
description: Git safety rules -- applies whenever running git commands
globs: "**"
---

# Git Safety

- **Never** `git add .` or `git add -A` -- stage files by name
- **Never** `git commit --amend` unless explicitly asked
- **Never** `git push` unless explicitly asked
- **Never** `git reset --hard`, `git checkout .`, or `git clean`
- **Never** skip hooks (`--no-verify`)
- If a hook fails, fix the issue and create a **new** commit
- Skip files that look like secrets (`.env`, `*.pem`, `credentials.*`)
- Use Conventional Commits: `type(scope): description`

## Production Protection

- Never commit or push directly to `main`/`master` -- use a PR
- Never deploy without passing the full validation suite

## Worktrees

- Use `git worktree` for parallel work; clean up after completion
- Never delete a worktree with uncommitted changes without warning
