---
name: onboard
description: Project onboarding and environment verification. Use when starting work in a repo, checking the local toolchain, or mapping validation entrypoints before editing.
---

# Onboard

Onboard project before changes. Goal: understand stack, toolchain, validation, repo shape with minimum reading.

## Process

### 1. Detect the project type

Check stack markers:

```bash
ls pyproject.toml package.json Cargo.toml go.mod 2>/dev/null
```

Interpretation:

- `pyproject.toml` -> Python project, usually `uv`
- `package.json` -> frontend or Node project
- both -> fullstack

### 2. Verify the matching toolchain

Check only tools relevant to detected stack.

Python:

```bash
uv --version
ruff --version
ty --version
python --version
```

Frontend:

```bash
node --version
npm --version
```

RTK, when relevant:

```bash
rtk --version
rtk hook-audit
```

### 3. Install dependencies with the native tool

Prefer stack-native command:

```bash
uv sync
npm install
```

Do not activate virtual environments manually. Use `uv run ...` for Python commands.

### 4. Find validation entrypoints

Check in this order:

1. task aliases in `pyproject.toml`
2. direct `uv run` commands
3. repo docs or scripts
4. CI configuration if needed

For Python repos, default validation order:

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

### 5. Map the project before editing

Identify:

- repo layout and main packages
- architecture style in use
- how configuration is loaded
- where tests live and how they are grouped
- recent momentum from `git log --oneline -10`

### 6. Suggest the right local skills

Recommend only what fits the repo:

- `skills/python/SKILL.md` for Python code and tooling
- `skills/design/SKILL.md` for API, UI, or BFF work
- `skills/arch/SKILL.md` for layering, DDD, or SDD
- `skills/quality/SKILL.md` for TDD or RCA
- `skills/security/SKILL.md` for trust boundaries or audits
- `skills/docs/SKILL.md` for README, ADRs, or changelogs
- `skills/cicd/SKILL.md` for GitHub Actions CI
- `skills/sqlmodel/SKILL.md` for SQLModel or Alembic
- `skills/rich/SKILL.md` for terminal UX
- `skills/rtk/SKILL.md` for output rewriting and hook troubleshooting
- `skills/building-agents/SKILL.md` for agent runtime work

## Output

Summarize:

- project type detected
- toolchain status
- dependency install status
- validation entrypoints found
- repo layout and architecture notes
- suggested local skills

## Constraints

- inspect before editing
- prefer targeted search over broad shell noise
- do not install unrelated tools or dependencies
- report missing tools plainly instead of guessing