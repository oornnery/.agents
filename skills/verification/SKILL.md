---
name: verification
description: Discover and run project validation gates: format, lint, typecheck, LSP diagnostics, tests, build, static security checks, dependency audits, and RTK output handling. Use before claiming work is complete, when fixing broken checks, or when setting up a validation plan.
---

# Verification

Use this skill to prove changes with the strongest practical checks the repo already supports.

## Discovery Order

1. Read task aliases: `package.json`, `pyproject.toml`, `justfile`, `Taskfile.yml`, `Makefile`, CI workflows.
2. Prefer repo-defined aggregate commands such as `task check`, `pnpm check`, `make test`, or CI-equivalent scripts.
3. If no aggregate exists, run the narrowest direct command that proves the changed surface.
4. Broaden by blast radius: format -> lint -> type/LSP -> tests -> build -> security.

Do not install new validation tools just because they are listed here.

## Python Gates

Use configured tools only:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pyright
uv run pytest -v
uv run task sec
uv run bandit -r src
uv run pip-audit
```

Prefer `uv run task check` or another repo alias when it maps to the same gates.

## TS/JS Gates

Use the repo package manager:

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm build
pnpm exec playwright test
pnpm audit --prod
```

Use `npm`, `yarn`, or `bun` only when their lockfile owns the repo.

## LSP and Static Diagnostics

Use LSP diagnostics when the environment exposes them. Treat them as another signal, not a replacement for command-line checks.

Record:

- which files were checked
- diagnostic source
- severity
- whether the issue is pre-existing or introduced

## Security Checks

Run static security checks when code touches auth, permissions, secrets, file handling, templates, webhooks, subprocesses, external URLs, SQL, deserialization, dependency changes, or production config.

Security checks may include:

- repo security task such as `task sec`
- Bandit, pip-audit, Semgrep, npm/pnpm audit, cargo audit
- manual review using `skills/security/SKILL.md`

Do not hide findings inside generic "lint passed" wording. Triage them separately.

## RTK

Use RTK for noisy output when available:

```bash
rtk <command>
rtk proxy <command>
rtk gain
```

Use raw commands when full unfiltered output is needed for diagnosis.

## Result Format

Report checks as facts:

```text
Command: ...
Result: PASS | FAIL | SKIPPED
Reason: ...
Risk: ...
```

Never say validation passed if a required check was skipped, unavailable, or failed.
