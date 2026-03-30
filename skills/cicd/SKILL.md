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

## Related

- `git/SKILL.md` — branching, PRs, conventional commits.
- `commands/commit.md` — commit workflow.
- `uv/SKILL.md` — package building and publishing.
