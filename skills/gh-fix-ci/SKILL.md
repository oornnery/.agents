---
name: gh-fix-ci
description: Debug and fix failing GitHub PR checks using gh CLI -- inspect logs,
  summarize failures, draft fix plan. Load when CI is failing, PR checks are red,
  or GitHub Actions need debugging.
---

# Fix CI

Debug failing GitHub PR checks using the `gh` CLI. Inspect logs,
summarize failures, propose fixes.

## Prerequisites

```bash
gh auth status    # confirm repo + workflow scopes
```

## Workflow

### 1. Resolve the PR

```bash
# Current branch PR
gh pr view --json number,url

# Or specific PR
gh pr view 42 --json number,url
```

### 2. Inspect Failing Checks

```bash
gh pr checks <pr>
```

### 3. Get Failure Logs

```bash
# Find run ID from checks output, then:
gh run view <run_id> --json name,conclusion,status,url
gh run view <run_id> --log-failed
```

If logs say "in progress", fetch job logs directly:

```bash
gh api "/repos/{owner}/{repo}/actions/jobs/{job_id}/logs"
```

### 4. Analyze Failure

Common patterns:

| Symptom                  | Likely Cause           | Fix                          |
| ------------------------ | ---------------------- | ---------------------------- |
| `ruff check` fails       | Lint errors            | `uv run ruff check . --fix`  |
| `ruff format` fails      | Formatting             | `uv run ruff format .`       |
| `ty check` fails         | Type errors            | Fix type annotations         |
| `pytest` fails           | Test failure           | Read traceback, fix code     |
| `uv sync --frozen` fails | Lockfile drift         | `uv lock` and commit         |
| Permission denied        | Missing workflow scope | Check `permissions:` in YAML |
| Module not found         | Missing dependency     | `uv add <pkg>`               |

### 5. Summarize for User

Provide:

- Failing check name and run URL
- Concise log snippet showing the error
- Root cause assessment

### 6. Propose Fix

Draft a fix plan. Implement only after user approval.

### 7. Verify

After fixing:

```bash
# Run local validation
uv run ruff format --check . && uv run ruff check . && uv run ty check && uv run pytest -v

# Re-check PR after push
gh pr checks <pr>
```

### 8. Re-run Failed Jobs

```bash
gh run rerun <run_id> --failed
```

## Scoping

- Only debug GitHub Actions checks
- External providers (Buildkite, CircleCI): report the details URL only
- If the workflow YAML itself is broken, inspect `.github/workflows/`

## Related

- `skills/cicd/SKILL.md` -- CI/CD workflows and GitHub Actions patterns
- `templates/ci.yml` -- CI validation workflow template
- `commands/debug.md` -- systematic debugging workflow
