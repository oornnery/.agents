---
name: commit
description: Analyze staged and unstaged changes, group them into small logical commits with precise conventional commit messages. Use when the user asks to commit, save progress, or create commits from current changes. Never use `git add .`, never amend unless asked.
---

# Commit

Create small, focused commits from the current working tree changes. Each
commit should represent one logical unit of change.

Safety rules are in `rules/git.md` — they apply automatically.

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

## Beyond the Commit

After committing, the next steps depend on what you shipped.

### Push and Create PR

```bash
# Push branch to remote
git push -u origin feat/my-feature

# Create PR targeting dev (or main for hotfixes)
gh pr create --base dev --title "feat(scope): description" --body "$(cat <<'EOF'
## Summary
- What this PR does and why

## Test Plan
- [ ] Unit tests pass
- [ ] Manual testing done
EOF
)"

# Create draft PR for early feedback
gh pr create --draft --title "WIP: feat(scope): description"
```

PR checklist:

- Title follows Conventional Commits format
- Description explains WHY, not just WHAT
- No secrets or credentials in diff
- Tests pass, lint clean
- No unrelated changes

### Tagging

Use annotated tags for releases. Lightweight tags for temporary markers.

```bash
# Annotated tag (for releases)
git tag -a v1.2.0 -m "feat: add user search and dashboard filters"
git push origin v1.2.0

# Tag from a specific commit
git tag -a v1.2.1 -m "fix: token refresh race condition" abc1234
git push origin v1.2.1

# List tags
git tag -l "v1.*"

# Delete a tag (local + remote)
git tag -d v1.2.0-rc.1
git push origin --delete v1.2.0-rc.1
```

Tag naming:

- Release: `v1.2.0` (semver)
- Pre-release: `v1.3.0-rc.1`, `v1.3.0-beta.1`
- Never tag unverified code — run validation first

### GitHub Release

Create a release after tagging. This often triggers CI pipelines for
publishing and container builds.

```bash
# Auto-generate release notes from commits since last tag
gh release create v1.2.0 --generate-notes

# Release with custom notes
gh release create v1.2.0 --title "v1.2.0" --notes "$(cat <<'EOF'
## Highlights
- User search with full-text support
- Dashboard date range filters

## Bug Fixes
- Fixed token refresh race condition (#42)

## Breaking Changes
- Removed deprecated `/api/v1/search` endpoint
EOF
)"

# Pre-release
gh release create v1.3.0-rc.1 --prerelease --generate-notes

# Upload build artifacts to release
gh release upload v1.2.0 dist/*.whl dist/*.tar.gz

# View and list releases
gh release view v1.2.0
gh release list
```

### Package Publishing

```bash
# Build Python package
uv build

# Publish to PyPI (triggered by tag in CI, or manual)
uv publish --token $PYPI_TOKEN

# Publish to test PyPI first
uv publish --index-url https://test.pypi.org/legacy/ --token $TEST_PYPI_TOKEN
```

### Container Build and Push

```bash
# Build container
docker build -t myapp:latest .

# Tag for GitHub Container Registry
docker tag myapp:latest ghcr.io/user/myapp:v1.2.0

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push
docker push ghcr.io/user/myapp:v1.2.0
```

In CI (GitHub Actions), container builds are usually triggered by tags.
See `skills/cicd/SKILL.md` for full workflow definitions.

### Full Release Workflow

```bash
# 1. Validate on dev
git checkout dev && git pull
uv run ruff format --check . && uv run ruff check . && uv run pytest -v

# 2. Create release PR: dev → main
gh pr create --base main --head dev --title "chore: release v1.2.0"

# 3. After PR is merged, tag main
git checkout main && git pull
git tag -a v1.2.0 -m "release: v1.2.0"
git push origin v1.2.0

# 4. Create GitHub release (triggers CI publish + container)
gh release create v1.2.0 --generate-notes

# 5. Back-merge main into dev
git checkout dev
git merge main
git push origin dev
```

## Related

- `rules/git.md` — safety rules (always-on).
- `skills/git/SKILL.md` — branching, PRs, rebase, worktrees.
- `skills/cicd/SKILL.md` — GitHub Actions, container builds, publishing.
- `skills/graphite/SKILL.md` — stacked PRs for large features.
