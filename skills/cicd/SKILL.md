---
name: cicd
description: CI/CD workflows -- dev branch strategy, tagging, releases, container builds, GitHub Actions. Load when setting up pipelines, publishing packages, or managing releases.
---

# CI/CD

CI/CD workflows, release management, and container builds.

## Branch Strategy

```text
main (protected, deployable)
  └── dev (integration branch)
       ├── feat/user-auth
       ├── fix/token-refresh
       └── feat/dashboard
```

- Never work directly on `main`/`master`.
- Feature branches from `dev`, merge back via PR.
- Release: merge `dev` into `main` via PR, then tag.

## Tagging and Releases

Semantic versioning: `MAJOR.MINOR.PATCH`.

```bash
git tag -a v1.2.0 -m "feat: add user search"
git push origin v1.2.0
gh release create v1.2.0 --generate-notes
```

## Package Publishing

```bash
uv build
uv publish --token $PYPI_TOKEN
```

See `templates/publish.yml` for the GitHub Actions workflow.

## Container Builds

```bash
docker build -t myapp:latest .
docker tag myapp:latest ghcr.io/user/myapp:v1.2.0
docker push ghcr.io/user/myapp:v1.2.0
```

See `templates/Dockerfile` for the Python + uv Dockerfile template.

## GitHub Actions

See `templates/ci.yml` for the validation workflow and
`templates/publish.yml` for the publish-on-tag workflow.

### Matrix Testing

```yaml
jobs:
  test:
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
# 1. Validate on dev
git checkout dev && git pull

# 2. Merge dev into main via PR
gh pr create --base main --head dev --title "chore: release v1.2.0"
gh pr merge --squash

# 3. Tag on main
git checkout main && git pull
git tag -a v1.2.0 -m "release: v1.2.0"
git push origin v1.2.0

# 4. Create release (triggers CI publish)
gh release create v1.2.0 --generate-notes

# 5. Back-merge into dev
git checkout dev && git merge main && git push origin dev
```

## Related

- `commands/commit.md` -- commit workflow, tags, releases, publishing
- `skills/git/SKILL.md` -- branching, PRs, conventional commits
- `templates/ci.yml` -- CI validation workflow
- `templates/publish.yml` -- PyPI publish workflow
- `templates/Dockerfile` -- Python container template
