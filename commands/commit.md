---
name: commit
description: Prepare a clean, reviewable commit from the current working tree. Use when the user wants to save progress with focused commits and precise conventional commit messages.
---

# Commit

Create small, coherent commits from the current working tree. Keep staging
explicit and safe.

## Safety rules

- never use `git add .` or `git add -A`
- never amend unless explicitly asked
- never push unless explicitly asked
- never skip hooks with `--no-verify`
- never include secrets or credential-like files

For broader git workflow guidance, use `skills/git/SKILL.md`.

## Process

### 1. Assess the working tree

Check:

```bash
git status
git diff --stat
git diff --stat --cached
git log --oneline -5
```

### 2. Group changes into logical units

- one commit per coherent feature, fix, refactor, docs change, or test change
- separate unrelated edits
- if needed, stage hunks with `git add -p`

### 3. Stage by name

Stage files explicitly. Warn if sensitive files appear in the diff:

- `.env`
- `*.pem`
- `credentials.*`

### 4. Write the commit message

Use Conventional Commits:

```text
type(scope): concise imperative description
```

Common types:

- `feat`
- `fix`
- `refactor`
- `docs`
- `test`
- `chore`
- `perf`
- `ci`
- `build`

Rules:

- subject under 72 characters
- imperative mood
- add a body only when the WHY is not obvious
- use the configured git identity
- do not add AI signatures or co-author lines unless explicitly requested

### 5. Commit and verify

After each commit:

```bash
git status
```

Confirm what remains uncommitted before creating another commit.

## Output

Report:

- logical commit groups proposed or created
- final commit message(s)
- anything intentionally left unstaged
- any blocked or risky files that were skipped

## Constraints

- do not mix unrelated edits in one commit
- do not hide failing hooks
- do not override git author config
- do not assume a clean tree without checking
