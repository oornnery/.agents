# .agents

Agent knowledge base for AI coding assistants. Organized into rules,
commands, and skills for on-demand loading.

## Usage

Add as a git submodule pointing to `.claude/`:

```bash
git submodule add https://github.com/oornnery/.agents .claude
git submodule update --init
```

Propagate updates across all projects:

```bash
git submodule update --remote
```

## Structure

```text
.agents/
├── CLAUDE.md                   # Entrypoint — stack, commands, skills index
├── rules/                      # Always-on conventions (auto-loaded)
│   ├── python.md               # Python style, anti-gold-plating, comments
│   ├── git.md                  # Git safety, production protection, worktrees
│   ├── documentation.md        # Markdown and docs standards
│   └── safety.md               # Reversibility, blast radius, production safety
├── commands/                   # Procedural workflows (invoke on task)
│   ├── commit.md               # Commits, tags, PRs, releases, publishing
│   ├── refactor.md             # Code audit, SOLID, 3-agent simplify pass
│   ├── review.md               # Code review with 4 specialized agents
│   ├── verify.md               # Adversarial verification — try to break it
│   ├── debug.md                # Systematic debugging
│   ├── setup.md                # Project onboarding
│   └── plan.md                 # SDD, SPEC, ARCH, DDD, ADRs, mermaid
├── skills/                     # Domain knowledge (load on demand)
│   ├── python/                 # Python conventions, async, architecture
│   ├── fastapi/                # FastAPI APIs, dependencies, streaming
│   ├── api-design/             # REST, OpenAPI, BFF, pagination, errors
│   ├── frontend/               # JS/TS, Tailwind, Basecoat, Solid
│   ├── design-system/          # Design tokens, Figma workflow, a11y
│   ├── jx/                     # Jinja server-rendered components
│   ├── pydantic/               # Data validation, serialization
│   ├── httpx/                  # HTTP client patterns
│   ├── testing/                # Test pyramid, pytest, coverage, BDD
│   ├── tdd/                    # TDD cycle, red-green-refactor, test-first
│   ├── architecture/           # DDD, Clean Architecture, SOLID, patterns
│   ├── rca/                    # Root cause analysis, 5 Whys, postmortems
│   ├── git/                    # Git workflows, branching, PRs, worktrees
│   ├── graphite/               # Stacked PRs, incremental review
│   ├── cicd/                   # CI/CD, releases, containers, gh CLI
│   ├── documentation/          # ADRs, changelogs, Wiki, Pages, docstrings
│   ├── markdown/               # Markdown writing, rumdl config
│   ├── rtk/                    # RTK token optimization
│   ├── rich/                   # Console output, tables, progress
│   ├── typer/                  # CLI applications
│   ├── uv/                     # Package management, dev toolchain
│   └── building-agents/        # Building tool-using LLM agents
├── hooks/                      # Versionable hook templates
│   └── rtk-rewrite.sh          # RTK command rewriting hook
└── templates/                  # Project bootstrap templates
    ├── CLAUDE.project.md       # Template for project CLAUDE.md
    ├── CLAUDE.fullstack.md     # Template for fullstack projects
    ├── pyproject.toml          # Python project config (ruff, pytest, ty)
    ├── .pre-commit-config.yaml # Pre-commit hooks (ruff, trailing whitespace)
    ├── .rumdl.toml             # Markdown lint config
    ├── .gitignore              # Python + fullstack gitignore
    ├── .env.example            # Environment variables template
    ├── Dockerfile              # Python app container with uv
    ├── ci.yml                  # GitHub Actions validation workflow
    ├── publish.yml             # GitHub Actions PyPI publish on tag
    ├── settings.python.json    # Python project permissions
    └── settings.fullstack.json # Fullstack project permissions
```

## Concepts

### Rules

Files in `rules/` are always-on conventions. Claude Code loads them
automatically based on file globs. They apply without being explicitly
invoked.

| Rule               | Scope                                          |
| ------------------ | ---------------------------------------------- |
| `python.md`        | Python style, anti-gold-plating, comments      |
| `git.md`           | Git safety, production protection, worktrees   |
| `documentation.md` | Markdown and documentation standards           |
| `safety.md`        | Reversibility, blast radius, production safety |

### Commands

Files in `commands/` are procedural workflows. They define step-by-step
processes for tasks like committing, reviewing, debugging, or planning.
Invoke them when performing that specific task.

| Command       | Purpose                                          |
| ------------- | ------------------------------------------------ |
| `commit.md`   | Commits, tags, PRs, releases, publishing         |
| `refactor.md` | Code audit, SOLID, 3-agent simplify pass         |
| `review.md`   | Code review with 4 specialized reviewer agents   |
| `verify.md`   | Adversarial verification — try to break the code |
| `debug.md`    | Systematic debugging workflow                    |
| `setup.md`    | Project onboarding and environment verification  |
| `plan.md`     | SDD, SPEC, ARCH, DDD, ADRs, mermaid diagrams     |

### Skills

Files in `skills/` are domain knowledge modules. Each has a `SKILL.md`
entrypoint and optional `references/` submodules. Load only what you
need for the current task to save tokens.

| Skill              | Domain                                          |
| ------------------ | ----------------------------------------------- |
| `python/`          | Python conventions, async, architecture         |
| `fastapi/`         | FastAPI APIs, dependencies, streaming           |
| `api-design/`      | REST, OpenAPI, BFF, pagination, error handling  |
| `frontend/`        | JS/TS tooling, Tailwind, Basecoat, Solid        |
| `design-system/`   | Design tokens, Figma workflow, theming, a11y    |
| `jx/`              | Jinja server-rendered components                |
| `pydantic/`        | Data validation, serialization, settings        |
| `httpx/`           | HTTP client patterns (sync/async)               |
| `testing/`         | Test pyramid, pytest, coverage, mocking, BDD    |
| `tdd/`             | TDD cycle, red-green-refactor, test-first       |
| `architecture/`    | DDD, Clean Architecture, SOLID, design patterns |
| `rca/`             | Root cause analysis, 5 Whys, postmortems        |
| `git/`             | Git workflows, branching, PRs, worktrees        |
| `graphite/`        | Stacked PRs, incremental review                 |
| `cicd/`            | CI/CD, releases, containers, gh CLI reference   |
| `documentation/`   | ADRs, changelogs, Wiki, Pages, docstrings       |
| `markdown/`        | Markdown writing, structure, rumdl lint         |
| `rtk/`             | RTK setup, custom filters, token optimization   |
| `rich/`            | Console output, tables, progress bars           |
| `typer/`           | CLI applications                                |
| `uv/`              | Package management, dev toolchain               |
| `building-agents/` | Building tool-using LLM agents, ReAct loop      |

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
