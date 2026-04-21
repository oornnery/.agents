# Git Worktrees

Worktrees let you check out multiple branches at once in separate directories
while sharing the same `.git` database. Use them when switching branches would
interrupt active work or create unnecessary stash churn.

## When to use

- hotfix while mid-feature
- PR review in isolation
- verification without leaving the current branch
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

Use a worktree when two agents need to operate on different branches or when a
review/verification pass should stay isolated from the implementation tree.

## Caveats

- all worktrees share the same `.git` directory
- a branch checked out in one worktree cannot be checked out in another
- detached HEAD worktrees are useful for read-only verification
- always remove worktrees when done
- never remove a worktree with uncommitted changes without warning

If a worktree goes stale, run:

```bash
git worktree prune
```

## Directory convention

Keep temporary worktrees adjacent to the main repo:

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
