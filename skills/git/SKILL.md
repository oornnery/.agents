---
name: git
description: Git workflows, branching strategies, PR workflow, rebase vs merge, bisect. Load when working with branches, PRs, or complex git operations.
---

# Git Workflows

Git workflow knowledge. For commit conventions and safety rules, see
`commands/commit.md` and `rules/git.md`.

## Branching Strategy

### Dev Branch (Preferred)

Never work directly on `main`/`master`. Always use a `dev` branch:

- `main`/`master` is always deployable and protected.
- `dev` is the integration branch — all work happens here or from here.
- Feature branches branch from `dev`, merge back to `dev`.
- When ready to release, merge `dev` into `main` via PR.

```text
main (protected, deployable)
  └── dev (integration branch)
       ├── feat/user-auth
       ├── fix/token-refresh
       └── feat/dashboard
```

```bash
# Start from main
git checkout main && git pull origin main

# Create dev branch (once)
git checkout -b dev
git push -u origin dev

# Feature branches from dev
git checkout dev
git checkout -b feat/add-user-search
# work, commit, push
gh pr create --base dev --title "feat(users): add search" --body "..."

# Release: merge dev into main
gh pr create --base main --head dev --title "chore: release v1.2.0"
```

### Trunk-Based (Alternative)

- Main branch is always deployable.
- Short-lived feature branches (1-3 days max).
- Merge via squash or rebase for clean history.
- Feature flags for incomplete work, not long-lived branches.

### Feature Branch

- Use when trunk-based isn't feasible (large features, team coordination).
- Keep branches up to date with `git rebase dev`.
- Merge back via PR with review.

## PR Workflow

### Creating PRs

```bash
git push -u origin feat/my-feature
gh pr create --title "feat(scope): description" --body "..."
```

### Draft PRs

Use drafts for work-in-progress that needs early feedback:

```bash
gh pr create --draft --title "WIP: feat(scope): description"
```

### PR Checklist

- Title follows Conventional Commits format.
- Description explains WHY, not just WHAT.
- Tests pass (`uv run pytest -v`).
- Lint and type checks pass.
- No secrets or credentials committed.
- No unrelated changes included.

## Rebase Vs Merge

| Scenario                  | Use                |
| ------------------------- | ------------------ |
| Updating feature branch   | `git rebase`       |
| Merging PR into main      | Squash merge       |
| Preserving branch history | Merge commit       |
| Cleaning up local commits | Interactive rebase |

### Rebase (Preferred for Feature Branches)

```bash
git checkout feat/my-feature
git fetch origin
git rebase origin/main
# Resolve conflicts if any, then:
git push --force-with-lease
```

### Squash Merge (Preferred for PRs)

One clean commit on main per PR. Use GitHub's squash merge button or:

```bash
gh pr merge <number> --squash
```

## Bisect

Find the commit that introduced a regression:

```bash
git bisect start
git bisect bad              # current commit is broken
git bisect good <commit>    # this commit was working

# Git checks out a middle commit. Test it, then:
git bisect good  # or git bisect bad

# Repeat until git identifies the first bad commit
git bisect reset  # when done
```

### Automated Bisect

```bash
git bisect start HEAD <good-commit>
git bisect run uv run pytest tests/test_specific.py -v
git bisect reset
```

## Stashing

```bash
git stash                    # save working changes
git stash -m "description"   # with a message
git stash list               # see all stashes
git stash pop                # apply and remove latest
git stash apply stash@{2}    # apply specific stash
git stash drop stash@{0}     # remove specific stash
```

## Conventional Commits

```text
type(scope): description

Types: feat, fix, refactor, docs, test, chore, perf, style, ci, build
```

| Type       | When                                |
| ---------- | ----------------------------------- |
| `feat`     | New feature or capability           |
| `fix`      | Bug fix                             |
| `refactor` | Code change that doesn't fix/add    |
| `docs`     | Documentation only                  |
| `test`     | Adding or fixing tests              |
| `chore`    | Maintenance (deps, config, tooling) |
| `perf`     | Performance improvement             |
| `ci`       | CI/CD changes                       |
| `build`    | Build system changes                |

## Useful Commands

```bash
# See what changed between branches
git log main..HEAD --oneline
git diff main...HEAD --stat

# Find who changed a line
git blame path/to/file.py

# Show a specific commit
git show <commit>

# List branches
git branch -a

# Clean up merged branches
git branch --merged main | grep -v main | xargs git branch -d
```

## Worktrees

Worktrees let you check out multiple branches simultaneously in separate
directories, sharing the same `.git` database. Use them for parallel work
without stashing or losing context.

### Quick Reference

```bash
git worktree add ../hotfix-tree hotfix/critical-bug   # existing branch
git worktree add -b feat/new ../feature-tree           # new branch
git worktree list                                       # show all
git worktree remove ../hotfix-tree                     # cleanup
git worktree prune                                      # remove stale refs
```

### When to Use

- Hotfix while mid-feature
- PR review in isolation
- Agent isolation (Claude Code `isolation: "worktree"`)
- Verification without switching branches

See `references/worktree.md` for full patterns and Claude Code integration.

## Related

- `commands/commit.md` — commit workflow and message format.
- `rules/git.md` — safety rules (always-on).
- `references/worktree.md` — detailed worktree guide.
