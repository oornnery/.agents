# .agents

Agent knowledge base for AI coding assistants. Skill-based architecture
with on-demand loading.

## Structure

```text
.agents/
├── CLAUDE.md           # Project instructions (entrypoint for agents)
├── AGENTS.md           # Symlink → CLAUDE.md
├── .rumdl.toml         # Markdown lint/format config
├── .gitignore
└── skills/
    ├── python/         # Core Python skill
    │   ├── SKILL.md
    │   └── references/
    │       ├── httpx.md
    │       ├── pydantic.md
    │       ├── pytest.md
    │       ├── rich.md
    │       ├── typer.md
    │       └── uv.md
    ├── fastapi/        # FastAPI skill
    │   ├── SKILL.md
    │   └── references/
    │       ├── dependencies.md
    │       ├── streaming.md
    │       └── other-tools.md
    └── jx/             # JX (Jinja components) skill
        ├── SKILL.md
        └── references/
            ├── integrations.md
            ├── migration-and-tooling.md
            └── organization-and-patterns.md
```

## How It Works

1. **CLAUDE.md** is the entrypoint — agents read it for stack, commands, and conventions.
2. **Skills** are loaded on demand when working in a specific domain.
3. Each skill has a **SKILL.md** (entrypoint) and **references/** (detailed submodules).
4. References are loaded only when needed — not all at once.

## Active Skills

| Skill    | Description                                         |
| -------- | --------------------------------------------------- |
| python   | Python conventions, async, type hints, uv toolchain |
| fastapi  | FastAPI APIs, Annotated style, DI, streaming        |
| jx       | Jinja server-rendered components (JX)               |

## Acknowledgments

The FastAPI skill is based on the official
[FastAPI agents skill](https://github.com/fastapi/fastapi/tree/master/fastapi/.agents/skills)
maintained by the FastAPI project.
