---
name: graphite
description: Graphite CLI for stacked PRs — create, manage, and submit PR stacks. Load when working with stacked branches, incremental code review, or the Graphite CLI tool.
---

# Graphite — Stacked PRs

Graphite manages **stacked pull requests** — a series of dependent PRs
that build on each other, enabling incremental review of large features.

## When to Use Stacked PRs

- Feature requires 500+ lines of changes
- Feature has natural layers (model → service → API → frontend)
- Multiple reviewers need to review different parts
- You want fast incremental feedback instead of one large PR

## When NOT to Use

- Small, self-contained changes (< 300 lines)
- Changes with no natural decomposition
- Hotfixes that need to merge immediately

## Setup

```bash
# Install Graphite CLI
brew install withgraphite/tap/graphite
# or
npm install -g @withgraphite/graphite-cli

# Authenticate with GitHub
gt auth --token <github-pat>

# Initialize in a repo
gt init
```

## Core Workflow

### 1. Create a Stack

```bash
# Start from main/dev
gt checkout main

# Create first PR in the stack (data layer)
gt create -m "feat(users): add user model and migrations"
# ... make changes, commit ...

# Create second PR (stacked on first)
gt create -m "feat(users): add user service and repository"
# ... make changes, commit ...

# Create third PR (stacked on second)
gt create -m "feat(users): add user API endpoints"
# ... make changes, commit ...
```

### 2. Submit the Stack

```bash
# Push all branches and create PRs
gt submit

# Submit with draft PRs
gt submit --draft
```

Each PR's base branch is the previous PR in the stack. GitHub shows only
the diff for that specific layer.

### 3. Update After Review

```bash
# Make changes to any PR in the stack
gt checkout feat/users-model
# ... fix review comments ...
git add -p && git commit -m "fix: address review feedback"

# Restack — rebase all dependent branches
gt restack

# Re-submit updated stack
gt submit
```

### 4. Merge the Stack

Merge from bottom to top:

```bash
# Merge the first PR (base of the stack)
gt merge

# This automatically rebases the next PR onto main
# Repeat for each PR in the stack
gt merge
gt merge
```

## Key Commands

```bash
gt create -m "message"   # Create a new branch in the stack
gt submit                 # Push all and create/update PRs
gt restack                # Rebase the stack after changes
gt merge                  # Merge the bottom PR
gt checkout <branch>      # Switch to a branch in the stack
gt log                    # Visualize the stack
gt info                   # Show current branch info
gt sync                   # Sync with remote (fetch + restack)
gt branch delete          # Clean up merged branches
```

## Stack Visualization

```bash
$ gt log
  feat/users-api (3/3)
  │ feat(users): add user API endpoints
  │
  feat/users-service (2/3)
  │ feat(users): add user service and repository
  │
  feat/users-model (1/3)
  │ feat(users): add user model and migrations
  │
  main
```

## Best Practices

- **Small PRs**: each PR should be 100-400 lines of diff
- **Self-contained**: each PR should be independently reviewable
- **Descriptive titles**: use Conventional Commits format
- **Bottom-up order**: data → logic → API → UI
- **Review order**: reviewers should start from the bottom
- **Quick merges**: merge approved PRs promptly to reduce restack conflicts

## Handling Conflicts

```bash
# After a conflict during restack
gt restack
# If conflicts appear:
# 1. Resolve conflicts in the file
# 2. git add <resolved-files>
# 3. git rebase --continue
# 4. gt restack (to continue restacking the rest)
```

## Integration with CI

Each PR in a stack runs CI independently. Configure GitHub branch
protection to require status checks. The stack merges cleanly because
each PR is rebased on its parent.

## Related

- `skills/git/SKILL.md` — branching strategies, PR workflow
- `rules/git.md` — git safety rules
- `commands/commit.md` — commit message conventions
