---
name: setup
description: Project onboarding and environment verification. Use when setting up a new project, verifying the dev environment, or bootstrapping the .agents submodule.
---

# Setup

Verify the development environment and onboard a project with the
`.agents` submodule.

## Process

### 1. Detect Project Type

Check what kind of project this is:

```bash
ls pyproject.toml package.json Cargo.toml go.mod 2>/dev/null
```

| File              | Stack          |
| ----------------- | -------------- |
| `pyproject.toml`  | Python (uv)    |
| `package.json`    | Node.js        |
| Both              | Fullstack      |

### 2. Verify Toolchain

#### Python Projects

```bash
uv --version
ruff --version
ty --version
python --version
```

If any tool is missing, install it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install ruff
uv tool install ty
```

#### Frontend Projects

```bash
node --version
npm --version  # or bun --version
```

### 3. Verify RTK

RTK should be installed globally for token optimization:

```bash
rtk --version
rtk gain
```

If not installed:

```bash
brew install rtk-ai/tap/rtk  # macOS
cargo install rtk             # or from source
```

Initialize the global hook:

```bash
rtk init -g
```

Verify the hook is active:

```bash
rtk hook-audit
```

### 4. Install Dependencies

```bash
# Python
uv sync

# Node.js
npm install  # or bun install
```

### 5. Run Validation

Run the project's validation suite to confirm everything works:

```bash
# Python
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

### 6. Suggest Skills

Based on the project structure, recommend which skills to load:

| Detected                    | Suggested Skill        |
| --------------------------- | ---------------------- |
| FastAPI in dependencies     | `fastapi/SKILL.md`     |
| Jinja templates present     | `jx/SKILL.md`          |
| `package.json` present      | `frontend/SKILL.md`    |
| CLI app (typer/click)       | `typer/SKILL.md`       |
| Tests present               | `testing/SKILL.md`     |
| HTTP client usage           | `httpx/SKILL.md`       |
| Pydantic models             | `pydantic/SKILL.md`    |

### 7. Submodule Setup (New Projects)

If the `.agents` submodule is not yet configured:

```bash
git submodule add <repo-url> .claude
git submodule update --init
```

Copy project templates:

```bash
cp .claude/templates/CLAUDE.project.md CLAUDE.md
cp .claude/templates/pyproject.toml pyproject.toml
cp .claude/templates/.rumdl.toml .rumdl.toml
cp .claude/templates/.pre-commit-config.yaml .pre-commit-config.yaml
cp .claude/templates/.gitignore .gitignore
cp .claude/templates/.env.example .env.example
cp .claude/templates/settings.python.json .claude/settings.local.json
```

For CI/CD workflows:

```bash
mkdir -p .github/workflows
cp .claude/templates/ci.yml .github/workflows/ci.yml
cp .claude/templates/publish.yml .github/workflows/publish.yml
```

For containerized projects:

```bash
cp .claude/templates/Dockerfile Dockerfile
```

Edit `CLAUDE.md` and `pyproject.toml` to match the project, then commit.

## Report

After setup, summarize:

- Project type detected.
- Toolchain status (what was installed, what was already present).
- RTK status.
- Validation results.
- Suggested skills for this project.
