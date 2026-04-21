---
name: build-fix
description: Fix failing validation incrementally with the smallest safe diff. Use when lint, typing, tests, Markdown checks, or CI workflow validation is broken.
---

# Build Fix

Fix broken validation one failing surface at a time. Optimize for minimal,
safe changes and fast feedback after each fix.

## Skills to use

- `skills/python/SKILL.md` for `ruff`, `ty`, `pytest`, and Python runtime issues
- `skills/docs/SKILL.md` for `rumdl` and documentation breakage
- `skills/cicd/SKILL.md` for GitHub Actions workflow failures
- `skills/security/SKILL.md` when the failing fix touches auth, secrets, trust boundaries, or unsafe input

## Process

### 1. Identify the first real failure

Capture the exact command and error output. Do not fix from memory or from a
summary alone.

For Python repos, use this order:

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

If the project exposes task aliases, prefer them.

### 2. Pick the smallest relevant surface

Classify the failure before editing:

- formatting
- lint
- markdown
- types
- tests
- CI workflow

Load only the skill that matches the failing surface.

### 3. Fix one error group at a time

Prefer this order:

1. formatting
2. lint
3. markdown
4. types
5. tests

Within a check, fix one file or one tightly related error group at a time.

### 4. Re-run the same failing check after each fix

Do not jump to the full suite after every tiny change. Confirm the immediate
failure is gone first, then move to the next failing surface.

### 5. Stop when the problem is no longer a build fix

Escalate instead of forcing it when:

- the fix requires dependency installation or lockfile changes
- the fix requires architectural redesign
- the same error survives multiple focused attempts
- the change would alter intended behavior instead of restoring validation

## Output

Report:

- exact command(s) used
- files changed
- failures fixed
- failures remaining
- whether full validation was re-run

## Constraints

- prefer minimal diffs over cleanup
- do not mix bug fixes with opportunistic refactors
- do not suppress failing checks to look green
- do not claim success without rerunning the relevant command
