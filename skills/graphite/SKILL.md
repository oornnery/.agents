---
name: graphite
description: Graphite CLI for stacked PRs -- create, manage, and submit PR stacks. Load when working with stacked branches, incremental code review, or the Graphite CLI tool.
---

# Graphite -- Stacked PRs

Manages stacked pull requests for incremental review of large features.

## When to Use

- Feature requires 500+ lines with natural layers (model -> service -> API)
- Multiple reviewers for different parts
- Want fast incremental feedback

Skip for: small changes (<300 lines), no natural decomposition, hotfixes.

## Core Workflow

```bash
# Create stack from main/dev
gt create -m "feat(users): add user model"
# ... work, commit ...
gt create -m "feat(users): add user service"    # stacked on first
gt create -m "feat(users): add user API"         # stacked on second

# Push all and create PRs
gt submit

# After review feedback
gt checkout feat/users-model
# ... fix comments, commit ...
gt restack && gt submit

# Merge bottom-up
gt merge    # repeat for each PR
```

## Key Commands

```bash
gt create -m "message"   # New branch in stack
gt submit                # Push all, create/update PRs
gt restack               # Rebase stack after changes
gt merge                 # Merge bottom PR
gt log                   # Visualize stack
gt sync                  # Fetch + restack
gt branch delete         # Clean merged branches
```

## Best Practices

- Each PR: 100-400 lines, independently reviewable
- Bottom-up order: data -> logic -> API -> UI
- Merge approved PRs promptly to reduce restack conflicts
- Use Conventional Commits for titles

## Related

- `skills/git/SKILL.md` -- branching, PR workflow
- `commands/commit.md` -- commit conventions
