---
description: Git safety rules — applies whenever running git commands
globs: "**"
---

# Git Safety

- **Never** `git add .`, `git add -A`, or `git add --all` — stage files by name
- **Never** `git commit --amend` unless the user explicitly asks
- **Never** `git push` unless the user explicitly asks
- **Never** `git reset --hard`, `git checkout .`, or `git clean`
- **Never** use `--no-verify` to skip pre-commit hooks
- If a pre-commit hook fails, fix the issue and create a **new** commit
- Skip files that look like secrets (`.env`, `*.pem`, `credentials.*`)
- Use Conventional Commits format: `type(scope): description`
- All CLI commands should go through RTK for token optimization (handled by hook)

## Production Protection

- **Never** alter production data directly
- **Never** commit or push directly to `main`/`master` — always use a PR
- **Never** modify third-party APIs or external services without explicit user supervision
- **Never** deploy without passing the full validation suite

## Worktrees

- Use `git worktree` for parallel work (e.g., hotfix while mid-feature)
- Temporary worktrees must be cleaned up after completion (`git worktree remove`)
- **Never** delete a worktree with uncommitted changes without warning the user
- Prefer worktree isolation for review and verification tasks
