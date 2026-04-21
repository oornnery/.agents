---
name: cicd
description: GitHub Actions CI guidance for validation gates, workflow permissions, matrices, caching, path filters, artifacts, and workflow verification. Load when designing, reviewing, or troubleshooting GitHub CI.
---

# GitHub Actions CI

Use this skill for GitHub Actions CI only.

This local skill focuses on pull request and push validation, required checks,
workflow safety, caching, matrices, artifacts, and workflow verification. It is
not the place for GitLab CI, Jenkins, ArgoCD, or broader deployment topology.

## Boundary

Use this skill for:

- GitHub Actions workflow shape
- branch and event triggers for CI
- job dependencies and validation gates
- permissions, secrets, and trust boundaries inside GitHub Actions
- caching, matrices, artifacts, and CI performance
- workflow verification with `actionlint`, `act`, and GitHub tooling

Pair with:

- `python` when the CI is mainly `uv`, `ruff`, `ty`, `rumdl`, and `pytest`
- `quality` when deciding what test depth or verification gates should block merges
- `security` when hardening secrets, provenance, or supply-chain controls

Out of scope here:

- GitLab CI and Jenkins
- runtime deployment architecture
- Kubernetes rollout strategy
- release and deployment workflows that are not part of CI

## Assets

- `assets/project/.github/workflows/ci.yml` -- a repo-shaped GitHub Actions CI
  workflow aligned with the local Python toolchain
- `assets/project/pyproject.toml` -- the matching project config used by the CI
  workflow
- `assets/project/src/myapp/main.py` -- a tiny Python entrypoint that gives the
  CI something real to lint and test
- `assets/project/tests/test_main.py` -- a matching test module for the example
  project

## Core Principles

- fail fast: run cheap, high-signal checks early
- least privilege: declare explicit workflow permissions
- reproducible builds: use lockfiles, pinned tools, and deterministic install commands
- parallel by default: independent checks should not wait on each other
- short feedback loops: optimize for PR feedback first
- auditable automation: make triggers, artifacts, and required checks easy to understand

## GitHub CI Workflow

1. choose the trigger surface: `pull_request`, `push`, or both
2. set explicit `permissions`
3. run lint, type, markdown, and test gates before build jobs
4. keep independent jobs parallel and aggregate only when needed
5. upload only the artifacts needed for later jobs or debugging
6. verify the workflow itself with CI-specific tooling

## Trigger Strategy

Default CI triggers:

```yaml
on:
  pull_request:
  push:
    branches: [main, dev]
```

Rules:

- use `pull_request` for merge-gating checks
- use `push` for protected branches that must stay green
- add `workflow_dispatch` only for manual CI workflows that need operator input
- avoid running expensive jobs on every branch unless they are truly required

For noisy repos, add concurrency control:

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Permissions

Always declare explicit permissions at the workflow level and only widen them
per job when required.

```yaml
permissions:
  contents: read
```

Examples of job-scoped widening:

- `security-events: write` for SARIF upload jobs
- `id-token: write` for OIDC-backed verification or cloud-authenticated jobs
- `pull-requests: write` only when the workflow must comment on PRs

Avoid:

- implicit default permissions
- broad write access for all jobs
- exposing secrets to jobs that only lint or test

## Default Python CI

This matches the repo's current Python stack and the local CI template.

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main, dev]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync --frozen
      - run: uv run ruff format --check .
      - run: uv run ruff check .
      - run: uvx rumdl check .
      - run: uv run ty check
      - run: uv run pytest -v
```

Use `templates/ci/github/ci.yml` as the repo-aligned starting point when scaffolding a
new workflow.

## Validation Gates

Preferred order for Python repos:

1. format check
2. lint
3. markdown lint
4. type check
5. test suite

Rules:

- keep build or artifact-producing jobs downstream of validation gates
- do not hide required failures behind `continue-on-error`
- use required status checks in branch protection for the real blocking jobs
- if one stage is flaky, fix the flake; do not downgrade the gate casually

## Parallelization and Job Shape

Independent checks should run in parallel:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
  typecheck:
    runs-on: ubuntu-latest
  test:
    runs-on: ubuntu-latest
  build:
    needs: [lint, typecheck, test]
    runs-on: ubuntu-latest
```

Use one combined `validate` job when:

- setup cost dominates
- the repo is small
- simpler branch protection matters more than per-check isolation

Split jobs when:

- checks are slow enough to benefit from parallelism
- failures should be easier to localize
- different runners, permissions, or artifacts are needed

## Matrix Builds

Use a matrix only when compatibility is part of the contract.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
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

Rules:

- keep matrix axes small and meaningful
- use `fail-fast: false` only when collecting full compatibility data is valuable
- do not add OS or Python-version matrices that the project does not actually support

## Path Filters

Path filters reduce wasted CI in monorepos or split repos.

Simple trigger filtering:

```yaml
on:
  pull_request:
    paths:
      - "src/**"
      - "tests/**"
      - "pyproject.toml"
      - "uv.lock"
```

Conditional job execution is better when different areas need different jobs.

Use path filters when:

- frontend and backend change independently
- docs-only changes should skip heavy test jobs
- package or service boundaries are already clear in the repo

## Caching

Cache only what materially improves CI time and stays reproducible.

Good candidates:

- dependency downloads keyed by lockfiles
- build caches such as `.pytest_cache` only when proven helpful
- Docker layers for image-building jobs

Rules:

- key caches from lockfiles or precise inputs
- prefer setup actions with built-in cache support when the repo already uses them
- avoid caching the entire virtual environment unless it is proven stable
- treat stale caches as a correctness risk, not only a performance detail

## Artifacts and Outputs

Upload only what later jobs or humans actually need.

Good artifacts:

- coverage reports
- test results
- built packages or wheels
- logs or debug bundles for failing workflows

Rules:

- never upload the entire workspace
- keep retention short by default
- use artifacts to pass validated outputs forward, not as a backup of everything
- prefer job outputs for small metadata and artifacts for actual files

## Secrets and Trust Boundaries

- secrets should not be available to jobs that do not need them
- avoid exposing secrets to `pull_request` jobs from forks
- prefer OIDC over long-lived static credentials when privileged jobs need identity
- keep privileged jobs off unreviewed branches
- pin third-party actions deliberately and review them like dependencies

Examples:

- CI lint/test workflow: usually `contents: read` only
- SARIF upload workflow: add `security-events: write`
- OIDC-backed privileged job: add `id-token: write` only to that job

## Workflow Verification

Validate the workflow itself before relying on it.

```bash
actionlint
act -n
gh workflow run ci.yml
gh run list --workflow ci.yml
```

Use this verification loop:

1. lint workflow syntax with `actionlint`
2. dry-run locally with `act` when the workflow is compatible
3. run the workflow in GitHub when repo context matters
4. inspect required permissions, artifact flow, and status checks

## Anti-Patterns

- no explicit `permissions`
- secrets available in fork PR jobs
- serializing independent lint, type, and test jobs
- `continue-on-error` on required gates
- no job timeouts
- uploading the whole workspace as an artifact
- caching unstable directories without lockfile-based keys
- one giant workflow mixing unprivileged validation with privileged jobs at the same trust level

## CI Checklist

- explicit triggers for `pull_request` and protected branch `push`
- explicit `permissions`
- deterministic install command such as `uv sync --frozen`
- format, lint, markdown, type, and test gates defined
- timeouts on long-running jobs
- matrices only when compatibility requires them
- path filters where they save real time
- artifacts limited to useful outputs
- workflow validated with `actionlint`
- branch protection wired to the real required checks
