# Git Worktrees

Worktrees = multiple branch checkouts in separate dirs, shared `.git` database. Use when switching branches disrupts active work or creates stash churn.

## When to use

- hotfix mid-feature
- PR review in isolation
- verification without leaving current branch
- parallel agent work with separate trees
- comparing two implementations side by side

## Core commands

```bash
# existing branch
git worktree add ../hotfix-tree hotfix/critical-bug

# new branch
git worktree add -b feat/new-feature ../feature-tree

# detached verification tree
git worktree add --detach ../verify-tree origin/feat/some-feature

# inspect and clean up
git worktree list
git worktree remove ../hotfix-tree
git worktree prune
```

## Patterns

### Hotfix during feature work

```bash
git worktree add -b hotfix/login-fix ../my-app-hotfix main
cd ../my-app-hotfix
# fix, validate, commit
cd -
git worktree remove ../my-app-hotfix
```

### Isolated review or verification

```bash
git worktree add --detach ../my-app-verify origin/feat/some-feature
cd ../my-app-verify
uv run pytest -v
uv run ruff check .
cd -
git worktree remove ../my-app-verify
```

### Parallel agent work

Use worktree when two agents need different branches or review/verification must stay isolated from impl tree.

## Caveats

- all worktrees share same `.git` directory
- branch checked out in one worktree cannot be checked out in another
- detached HEAD worktrees useful for read-only verification
- always remove worktrees when done
- never remove worktree with uncommitted changes without warning

If worktree goes stale, run:

```bash
git worktree prune
```

## Directory convention

Keep temporary worktrees adjacent to main repo:

```text
projects/
├── my-app/
├── my-app-hotfix/
├── my-app-review-42/
└── my-app-verify/
```

Use short, intention-revealing names so cleanup is obvious.

## Related

- `skills/git/SKILL.md` -- broader git workflow guidance
- `commands/verify.md` -- isolated verification flow
