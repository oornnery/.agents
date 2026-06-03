---
name: build-fix
description: Fix failing validation incrementally with the smallest safe diff. Use when lint, typing, tests, Markdown checks, or CI workflow validation is broken.
---

# Build Fix

Fix broken valid one surface at time. Minimal safe diffs, fast feedback per fix.

## Skills to use

- `skills/verification/SKILL.md` for gate ordering and result reporting
- `skills/python/SKILL.md` for `ruff`, `ty`, `pytest`, Python runtime issues
- `skills/docs/SKILL.md` for `rumdl`, doc breakage
- `skills/cicd/SKILL.md` for GitHub Actions workflow failures
- `skills/security/SKILL.md` when fix touches auth, secrets, trust boundaries, unsafe input

## Process

### 1. Identify the first real failure

Capture exact command and error output. Do not fix from memory or summary alone.

Python repos, use this order:

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

If project exposes task aliases, prefer them.

### 2. Pick the smallest relevant surface

Classify failure before editing:

- formatting
- lint
- markdown
- types
- tests
- CI workflow

Load only matching skill.

### 3. Fix one error group at a time

Prefer this order:

1. formatting
2. lint
3. markdown
4. types
5. tests

Within check, fix one file or one tightly related error group at time.

### 4. Re-run the same failing check after each fix

Do not jump to full suite after every tiny change. Confirm immediate failure gone first, then move to next surface.

### 5. Stop when the problem is no longer a build fix

Escalate over forcing when:

- fix requires dependency install or lockfile changes
- fix requires architectural redesign
- same error survives multiple focused attempts
- change would alter intended behavior over restoring valid

## Output

Report:

- exact command(s) used
- files changed
- failures fixed
- failures remaining
- whether full valid was re-run

## Constraints

- prefer minimal diffs over cleanup
- do not mix bug fixes with opportunistic refactors
- do not suppress failing checks to look green
- do not claim success without rerunning relevant command
