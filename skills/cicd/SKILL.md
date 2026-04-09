---
name: cicd
description: CI/CD workflows — dev branch strategy, tagging, releases, container builds, GitHub Actions. Load when setting up pipelines, publishing packages, or managing releases.
---

# CI/CD

CI/CD workflows, release management, and container builds using GitHub
Actions and the `gh` CLI.

## Documentation

- GitHub Actions: <https://docs.github.com/en/actions>
- GitHub CLI: <https://cli.github.com/manual/>
- Docker: <https://docs.docker.com/>

## Branch Strategy

### Dev Branch Workflow

Never work directly on `main`/`master`. Always create a `dev` branch:

```bash
# Start from main
git checkout main
git pull origin main

# Create dev branch
git checkout -b dev

# Work, commit, push
git push -u origin dev

# When ready, merge dev into main via PR
gh pr create --base main --title "chore: merge dev into main" --body "..."
```

### Feature Branches from Dev

For specific features, branch from `dev`:

```bash
git checkout dev
git checkout -b feat/my-feature

# Work, commit, push
git push -u origin feat/my-feature
gh pr create --base dev --title "feat(scope): description"
```

### Flow

```text
main (protected, deployable)
  └── dev (integration branch)
       ├── feat/user-auth
       ├── fix/token-refresh
       └── feat/dashboard
```

## Tagging and Releases

### Semantic Versioning

```text
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes (backwards compatible)
  │     └──────── New features (backwards compatible)
  └────────────── Breaking changes
```

### Creating Tags

```bash
# Create annotated tag
git tag -a v1.2.0 -m "feat: add user search and dashboard filters"

# Push tag
git push origin v1.2.0

# Push all tags
git push origin --tags
```

### Creating GitHub Releases

```bash
# Create release from tag
gh release create v1.2.0 --title "v1.2.0" --generate-notes

# Create release with custom notes
gh release create v1.2.0 --title "v1.2.0" --notes "$(cat <<'EOF'
## What's New
- User search functionality
- Dashboard date range filters

## Bug Fixes
- Fixed token refresh on expired sessions
EOF
)"

# Create pre-release
gh release create v1.3.0-rc.1 --prerelease --title "v1.3.0-rc.1"

# Upload assets to release
gh release upload v1.2.0 dist/*.whl dist/*.tar.gz
```

### List and View Releases

```bash
gh release list
gh release view v1.2.0
```

## Package Publishing

### Python (uv + PyPI)

```bash
# Build
uv build

# Publish to PyPI
uv publish --token $PYPI_TOKEN

# Publish to test PyPI
uv publish --index-url https://test.pypi.org/legacy/ --token $TEST_PYPI_TOKEN
```

### GitHub Actions Workflow (Python Package)

```yaml
name: Publish
on:
  push:
    tags: ["v*"]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv build
      - run: uv publish
        env:
          UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

## Container Builds

### Dockerfile (Python + uv)

```dockerfile
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ src/

CMD ["uv", "run", "python", "-m", "myapp"]
```

### Build and Push

```bash
# Build
docker build -t myapp:latest .

# Tag for registry
docker tag myapp:latest ghcr.io/user/myapp:v1.2.0

# Push to GitHub Container Registry
docker push ghcr.io/user/myapp:v1.2.0
```

### GitHub Actions Workflow (Container)

```yaml
name: Container
on:
  push:
    tags: ["v*"]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
```

## GitHub Actions Patterns

### Validation Workflow

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main, dev]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync --frozen
      - run: uv run ruff format --check .
      - run: uv run ruff check .
      - run: uvx rumdl check .
      - run: uv run ty check
      - run: uv run pytest -v --cov=src
```

### Matrix Testing

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with:
          python-version: ${{ matrix.python-version }}
      - run: uv sync --frozen
      - run: uv run pytest -v
```

## Release Workflow (Full)

```bash
# 1. Ensure dev is up to date
git checkout dev
git pull origin dev

# 2. Merge dev into main
gh pr create --base main --head dev --title "chore: release v1.2.0"
gh pr merge --squash

# 3. Tag the release on main
git checkout main
git pull origin main
git tag -a v1.2.0 -m "release: v1.2.0"
git push origin v1.2.0

# 4. GitHub Release (triggers CI publish)
gh release create v1.2.0 --generate-notes

# 5. Back to dev
git checkout dev
git merge main
git push origin dev
```

## GitHub CLI (`gh`) Reference

The `gh` CLI is the primary interface for GitHub operations. Use it
instead of the web UI whenever possible.

### Pull Requests

```bash
# Create PR
gh pr create --base dev --title "feat(scope): description" --body "..."

# Create draft PR
gh pr create --draft --title "WIP: feat(scope): description"

# List open PRs
gh pr list

# View PR details
gh pr view 42
gh pr view 42 --json title,state,reviews,checks

# View PR diff
gh pr diff 42

# Check PR status (CI checks)
gh pr checks 42

# Review a PR
gh pr review 42 --approve
gh pr review 42 --request-changes --body "Please fix..."
gh pr review 42 --comment --body "Looks good overall"

# Merge PR
gh pr merge 42 --squash
gh pr merge 42 --rebase
gh pr merge 42 --merge

# Close PR without merging
gh pr close 42

# Reopen PR
gh pr reopen 42

# Read PR comments
gh api repos/{owner}/{repo}/pulls/42/comments
```

### Issues

```bash
# Create issue
gh issue create --title "Bug: login fails on expired token" --body "..."
gh issue create --label bug,urgent --assignee @me

# List issues
gh issue list
gh issue list --label bug
gh issue list --assignee @me
gh issue list --state closed

# View issue
gh issue view 123

# Close issue
gh issue close 123 --reason completed
gh issue close 123 --reason "not planned"

# Reopen issue
gh issue reopen 123

# Add comment
gh issue comment 123 --body "Fixed in #42"

# Transfer issue to another repo
gh issue transfer 123 owner/other-repo

# Pin issue
gh issue pin 123
```

### Workflows and Actions

```bash
# List workflow runs
gh run list
gh run list --workflow ci.yml
gh run list --status failure

# View a specific run
gh run view 12345

# Watch a running workflow
gh run watch 12345

# Re-run a failed workflow
gh run rerun 12345
gh run rerun 12345 --failed  # only failed jobs

# Download artifacts from a run
gh run download 12345

# Trigger a workflow manually (workflow_dispatch)
gh workflow run deploy.yml --ref main
gh workflow run deploy.yml -f environment=staging

# List workflows
gh workflow list

# View workflow definition
gh workflow view ci.yml

# Disable/enable a workflow
gh workflow disable ci.yml
gh workflow enable ci.yml
```

### Releases (Extended)

```bash
# Create release with auto-generated notes
gh release create v1.2.0 --generate-notes

# Create release from specific target
gh release create v1.2.0 --target main --generate-notes

# Edit existing release
gh release edit v1.2.0 --notes "Updated notes"

# Delete release (keeps the tag)
gh release delete v1.2.0

# Download release assets
gh release download v1.2.0
gh release download v1.2.0 --pattern "*.whl"
```

### Repository

```bash
# Clone
gh repo clone owner/repo

# Fork
gh repo fork owner/repo

# Create repo
gh repo create my-project --public --clone

# View repo info
gh repo view
gh repo view owner/repo --json name,description,stars

# Set repo topics
gh repo edit --add-topic python,fastapi,api

# Set default branch
gh repo edit --default-branch main

# Enable/disable features
gh repo edit --enable-wiki=false
gh repo edit --enable-issues=true
```

### Gists

```bash
# Create gist
gh gist create file.py --desc "Utility function"

# Create secret gist
gh gist create file.py --desc "Private snippet" --public=false

# List gists
gh gist list

# View gist
gh gist view abc123

# Edit gist
gh gist edit abc123
```

### GitHub API (Direct)

For operations not covered by `gh` subcommands:

```bash
# Get repo info
gh api repos/owner/repo

# List PR review comments
gh api repos/owner/repo/pulls/42/comments

# Get workflow runs
gh api repos/owner/repo/actions/runs --jq '.workflow_runs[:5]'

# Create a label
gh api repos/owner/repo/labels -f name="priority:high" -f color="d93f0b"

# GraphQL query
gh api graphql -f query='{ viewer { login } }'
```

### Environment and Auth

```bash
# Login
gh auth login

# Check auth status
gh auth status

# Switch between accounts
gh auth switch

# Set default repo for commands
gh repo set-default owner/repo
```

## Related

- `git/SKILL.md` — branching, PRs, conventional commits.
- `commands/commit.md` — commit workflow, tags, releases, publishing.
- `skills/documentation/SKILL.md` — GitHub Wiki, Pages, issue templates.
- `uv/SKILL.md` — package building and publishing.
