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
