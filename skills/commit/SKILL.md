---
name: commit
description: Analyze staged and unstaged changes, group them into small logical commits with precise conventional commit messages. Use when the user asks to commit, save progress, or create commits from current changes. Never use `git add .`, never amend unless asked, never sign as Claude Code.
---

# Commit

Create small, focused commits from the current working tree changes. Each
commit should represent one logical unit of change.

## Process

### 1. Assess the Working Tree

Run these in parallel:

```bash
git status
git diff --stat
git diff --stat --cached
git log --oneline -5
```

Understand what changed, what is staged, and the recent commit style.

### 2. Group Changes into Logical Units

Analyze the diff and split changes into the smallest meaningful groups:

- One commit per feature, fix, refactor, or doc change.
- Separate unrelated file changes into distinct commits.
- If a single file contains changes for two purposes, stage hunks
  selectively with `git add -p`.

### 3. Stage Files Explicitly

**Never use `git add .` or `git add -A`.** Always stage files by name:

```bash
git add path/to/file1.py path/to/file2.py
```

Before staging, check that no sensitive files are included (`.env`,
credentials, secrets, tokens). Warn the user if any are detected.

### 4. Write the Commit Message

Use Conventional Commits format:

```text
type(scope): concise imperative description

Optional body explaining WHY, not WHAT.
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`,
`style`, `ci`, `build`.

**Rules:**

- Subject line max 72 characters, imperative mood ("add", not "added").
- Scope is optional but recommended (module, component, or area).
- Body only when the WHY is not obvious from the subject.
- Reference issues when applicable: `Closes #123`.

### 5. Create the Commit

Use the system-configured git identity. **Never** append
`Co-Authored-By: Claude` or any AI signature. The commit must use the
author already configured in `git config user.name` and
`git config user.email` — do not override them.

```bash
git commit -m "$(cat <<'EOF'
type(scope): description

Optional body.
EOF
)"
```

### 6. Verify

After each commit, run `git status` to confirm success and check
remaining uncommitted changes. Repeat from step 2 until the working tree
is clean or only intentionally untracked files remain.

## Safety Rules

- **Never** `git add .`, `git add -A`, or `git add --all`.
- **Never** `git commit --amend` unless the user explicitly asks.
- **Never** `git push` unless the user explicitly asks.
- **Never** `git reset --hard`, `git checkout .`, or `git clean`.
- **Never** sign commits as Claude Code or any AI identity.
- **Never** use `--no-verify` to skip pre-commit hooks.
- If a pre-commit hook fails, fix the issue and create a **new** commit.
- Skip files that look like secrets (`.env`, `*.pem`, `credentials.*`).

## Examples

Good commit messages:

```text
fix(auth): handle expired tokens in refresh flow
docs(jx): align skill with upstream JX 0.10 API
refactor(api): extract validation into shared middleware
feat(dashboard): add date range filter to analytics
test(models): cover edge cases in user serialization
chore: update dependencies to latest compatible versions
```

Bad commit messages:

```text
update files                    <- too vague
fix bug                         <- which bug?
WIP                             <- not a meaningful unit
changes                         <- says nothing
refactor everything             <- too broad for one commit
```
