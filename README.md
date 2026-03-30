# .agents

Agent knowledge base for AI coding assistants. Organized into rules,
commands, and skills for on-demand loading.

## Usage

Add as a git submodule pointing to `.claude/`:

```bash
git submodule add <repo-url> .claude
git submodule update --init
```

Propagate updates across all projects:

```bash
git submodule update --remote
```

## Structure

```text
.agents/
├── CLAUDE.md                  # Entrypoint — stack, commands, skills index
├── AGENTS.md -> CLAUDE.md     # Codex/Copilot compatibility
├── rules/                     # Always-on conventions (auto-loaded)
│   ├── python.md              # Python style and conventions
│   ├── git.md                 # Git safety rules
│   └── documentation.md       # Markdown and docs standards
├── commands/                  # Procedural workflows (invoke on task)
│   ├── commit.md              # Logical commits with conventional messages
│   ├── refactor.md            # Code audit and refactoring
│   ├── review.md              # Structured code review
│   ├── debug.md               # Systematic debugging
│   ├── setup.md               # Project onboarding
│   └── plan.md                # SDD, SPEC.md, ARCH.md, mermaid diagrams
├── skills/                    # Domain knowledge (load on demand)
│   ├── python/                # Python conventions, async, architecture
│   ├── fastapi/               # FastAPI APIs, dependencies, streaming
│   ├── frontend/              # JS/TS, Tailwind, Basecoat, Solid
│   ├── jx/                    # Jinja server-rendered components
│   ├── markdown/              # Markdown writing, rumdl config
│   ├── rtk/                   # RTK token optimization
│   ├── pydantic/              # Data validation, serialization
│   ├── httpx/                 # HTTP client patterns
│   ├── testing/               # Testing strategy, pytest, coverage
│   ├── rich/                  # Console output, tables, progress
│   ├── typer/                 # CLI applications
│   ├── uv/                    # Package management, dev toolchain
│   ├── git/                   # Git workflows, branching, PRs
│   └── cicd/                  # CI/CD, releases, tags, containers
├── hooks/                     # Versionable hook templates
│   └── rtk-rewrite.sh         # RTK command rewriting hook
└── templates/                 # Project bootstrap templates
    ├── CLAUDE.project.md      # Template for project CLAUDE.md
    ├── pyproject.toml         # Python project config (ruff, pytest, ty, taskipy)
    ├── .pre-commit-config.yaml# Pre-commit hooks (ruff, trailing whitespace)
    ├── .rumdl.toml            # Markdown lint config
    ├── .gitignore             # Python + fullstack gitignore
    ├── .env.example           # Environment variables template
    ├── Dockerfile             # Python app container with uv
    ├── ci.yml                 # GitHub Actions validation workflow
    ├── publish.yml            # GitHub Actions PyPI publish on tag
    ├── settings.python.json   # Python project permissions
    └── settings.fullstack.json# Fullstack project permissions
```

## Concepts

### Rules

Files in `rules/` are always-on conventions. Claude Code loads them
automatically based on file globs. They apply without being explicitly
invoked.

### Commands

Files in `commands/` are procedural workflows. They define step-by-step
processes for tasks like committing, reviewing, debugging, or planning.
Invoke them when performing that specific task.

### Skills

Files in `skills/` are domain knowledge modules. Each has a `SKILL.md`
entrypoint and optional `references/` submodules. Load only what you
need for the current task to save tokens.

## RTK Integration

RTK (Rust Token Killer) is used as default for all command execution.
The hook in `hooks/rtk-rewrite.sh` automatically rewrites commands for
60-90% token savings. Install globally:

```bash
rtk init -g
```

## Acknowledgments

The FastAPI skill is based on the official
[FastAPI agents skill](https://github.com/fastapi/fastapi/tree/master/fastapi/.agents/skills)
maintained by the FastAPI project.
