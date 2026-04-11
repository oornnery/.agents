---
name: gh-fix-ci
description: Debug and fix failing GitHub PR checks using gh CLI -- inspect logs,
  summarize failures, draft fix plan. Load when CI is failing, PR checks are red,
  or GitHub Actions need debugging.
---

# Fix CI

Debug failing GitHub PR checks via `gh` CLI.

## Workflow

1. **Resolve PR**: `gh pr view --json number,url`
2. **Inspect checks**: `gh pr checks <pr>`
3. **Get logs**: `gh run view <run_id> --log-failed`
4. **Analyze** (see table below)
5. **Summarize**: failing check, log snippet, root cause
6. **Fix**: propose plan, implement after approval
7. **Verify**: run local validation, then `gh pr checks`
8. **Re-run**: `gh run rerun <run_id> --failed`

## Common Failures

| Symptom                  | Cause          | Fix                         |
| ------------------------ | -------------- | --------------------------- |
| `ruff check` fails       | Lint errors    | `uv run ruff check . --fix` |
| `ruff format` fails      | Formatting     | `uv run ruff format .`      |
| `ty check` fails         | Type errors    | Fix annotations             |
| `pytest` fails           | Test failure   | Read traceback, fix code    |
| `uv sync --frozen` fails | Lockfile drift | `uv lock` and commit        |
| Module not found         | Missing dep    | `uv add <pkg>`              |

## Scope

- Only GitHub Actions checks -- external providers: report URL only
- If workflow YAML is broken, inspect `.github/workflows/`

## Related

- `skills/cicd/SKILL.md` -- CI/CD workflows and Actions patterns
- `templates/ci.yml` -- CI validation workflow template
