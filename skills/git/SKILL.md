---
name: git
description: Git safety, staging, commit workflow, branching, pull requests, rebase, bisect, tagging, and worktrees. Load when working with branches, commits, PRs, or recovering from tricky git situations.
---

# Git

Use this skill when the main problem is a git workflow problem rather than a
code problem.

## Boundary

Use this skill for:

- safe staging and commit flow
- branch and PR workflow
- rebasing and syncing feature branches
- bisecting regressions
- stashing and worktrees
- tags and release-oriented git operations

Pair with:

- `skills/cicd/SKILL.md` for GitHub Actions CI and release automation
- `skills/quality/SKILL.md` when bisecting or isolating regressions
- `skills/docs/SKILL.md` when the deliverable is release notes or changelog content

## Core safety rules

- stage files by name, not `git add .` or `git add -A`
- do not amend unless explicitly asked
- do not push unless explicitly asked
- do not skip hooks with `--no-verify`
- do not use destructive resets or cleanup commands casually
- do not delete a dirty worktree without warning

## Common workflow

1. inspect the working tree
2. group changes into logical units
3. stage explicitly by file or hunk
4. commit with a precise conventional message
5. verify what remains uncommitted

Use `commands/commit.md` when the task is specifically about preparing
commits from the current tree.

## Branching and PR workflow

Prefer short-lived feature branches and reviewable PRs.

PR checklist:

- title is a conventional commit style summary
- description explains the WHY
- validation passes for the changed surface
- no secrets or unrelated changes are included

Draft PRs are appropriate for early feedback on incomplete work.

## Rebase vs merge

| Scenario                  | Preferred action      |
| ------------------------- | --------------------- |
| update a feature branch   | `git rebase`          |
| merge a completed PR      | squash merge          |
| preserve explicit history | merge commit          |
| isolate a regression      | `git bisect`          |

### Rebase pattern

```bash
git checkout feat/my-feature
git fetch origin
git rebase origin/main
```

If conflicts appear, resolve them carefully and continue. Force-push only when
explicitly asked and only with `--force-with-lease`.

## Bisect

Use `git bisect` when a regression has a known good point:

```bash
git bisect start
git bisect bad
git bisect good <commit>
```

Then test each candidate commit until git identifies the first bad commit.

Automated form:

```bash
git bisect start HEAD <good-commit>
git bisect run uv run pytest tests/path/to/test_file.py -v
git bisect reset
```

## Stash

Stash only when you truly need to park work temporarily:

```bash
git stash
git stash -m "description"
git stash list
git stash pop
```

Prefer worktrees over repeated stashing when you need parallel work.

## Tags and release flow

Use annotated tags for releases:

```bash
git tag -a v1.2.0 -m "release 1.2.0"
```

Create tags only after validation passes and only when release intent is clear.

## Worktrees

Use worktrees for:

- hotfixes while feature work is in progress
- isolated PR review
- verification without switching branches
- parallel agent work

Read `references/worktree.md` for the full worktree guide.

## Useful commands

```bash
git status
git diff --stat
git log --oneline -10
git show <commit>
git blame path/to/file.py
git branch -a
git worktree list
```

## Related

- `commands/commit.md` -- prepare clean commits from the current tree
- `commands/debug.md` -- investigate regressions before using `git bisect`
- `references/worktree.md` -- worktree patterns and caveats
