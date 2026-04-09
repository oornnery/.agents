# Git Worktrees

Worktrees let you check out multiple branches simultaneously in separate
directories, sharing the same `.git` database. This enables parallel work
without stashing or switching branches.

## When to Use Worktrees

- **Hotfix while mid-feature**: work on a fix without losing feature context
- **Code review**: check out the PR branch in a separate tree while keeping
  your work intact
- **Agent isolation**: run agents in their own worktree so changes do not
  conflict with the main tree
- **Parallel CI-like tasks**: run tests on one branch while developing on another
- **Comparing implementations**: have two approaches side by side

## Core Commands

```bash
# Create a worktree for an existing branch
git worktree add ../hotfix-tree hotfix/critical-bug

# Create a worktree with a new branch
git worktree add -b feat/new-feature ../feature-tree

# Create a worktree from a specific commit/tag
git worktree add ../release-tree v2.1.0

# List all worktrees
git worktree list

# Remove a worktree (after merging/completing work)
git worktree remove ../hotfix-tree

# Clean up stale worktree references
git worktree prune
```

## Patterns

### Worktree per PR Review

```bash
# Reviewer checks out PR branch in a separate tree
git worktree add ../review-pr-42 origin/feat/user-auth
cd ../review-pr-42
uv run pytest -v
# When done:
cd -
git worktree remove ../review-pr-42
```

### Worktree for Hotfix During Feature Work

```bash
# Currently working on feat/dashboard
git worktree add -b hotfix/login-fix ../hotfix main
cd ../hotfix
# fix, commit, push, create PR
cd -
git worktree remove ../hotfix
```

### Temporary Worktree for Verification

```bash
# Verify a branch without switching
git worktree add --detach ../verify-tree origin/feat/some-feature
cd ../verify-tree
uv run pytest -v && uv run ruff check .
cd -
git worktree remove ../verify-tree
```

## Claude Code Integration

Claude Code supports worktree isolation for sub-agents:

```text
Agent({
  description: "Verify feature implementation",
  isolation: "worktree",
  prompt: "Run tests and verify the implementation..."
})
```

When `isolation: "worktree"` is set:

- The agent works on an isolated copy of the repo
- Changes made by the agent do not affect the main tree
- If the agent makes no changes, the worktree is automatically cleaned up
- If changes exist, the worktree path and branch are returned in the result

## Important Caveats

- **Shared refs**: all worktrees share the same `.git` directory. A branch
  checked out in one worktree cannot be checked out in another.
- **Lock files**: if a worktree is on a network drive or external storage,
  use `git worktree lock` to prevent accidental pruning.
- **HEAD state**: a worktree can be in detached HEAD state (useful for
  read-only verification).
- **Cleanup**: always remove worktrees when done. Stale worktrees waste
  disk space and can cause confusing branch lock errors.
- **Submodules**: worktrees share submodule state. Run `git submodule update`
  in new worktrees if submodules are used.

## Directory Convention

Keep worktrees adjacent to the main repo:

```text
projects/
├── my-app/              # main worktree
├── my-app-hotfix/       # temporary worktree
├── my-app-review-42/    # review worktree
└── my-app-verify/       # verification worktree
```

## Related

- `skills/git/SKILL.md` — branching, PRs, rebase, bisect
- `rules/git.md` — worktree safety rules
