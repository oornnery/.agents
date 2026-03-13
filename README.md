# .agents

Agent knowledge base for AI coding assistants. Skill-based architecture
with on-demand loading.

## Structure

```bash
 .
├──  AGENTS.md -> CLAUDE.md
├──  CLAUDE.md
├── 󰂺 README.md
└──  skills
    ├──  frontend
    │   ├──  references
    │   │   ├──  basecoat.md
    │   │   ├──  solid-islands-jinja.md
    │   │   ├──  solid.md
    │   │   ├──  solidstart.md
    │   │   ├──  tailwind.md
    │   └──  SKILL.md
    ├──  fastapi
    │   ├──  references
    │   │   ├──  dependencies.md
    │   │   ├──  other-tools.md
    │   │   └──  streaming.md
    │   └──  SKILL.md
    ├──  jx
    │   ├──  references
    │   │   ├──  integrations.md
    │   │   ├──  migration-and-tooling.md
    │   │   └──  organization-and-patterns.md
    │   └──  SKILL.md
    ├──  markdown
    │   ├──  references
    │   │   ├──  best-practices.md
    │   │   └──  rumdl.md
    │   └──  SKILL.md
    └──  python
        ├──  references
        │   ├──  httpx.md
        │   ├──  pydantic.md
        │   ├──  pytest.md
        │   ├──  rich.md
        │   ├──  typer.md
        │   └──  uv.md
        └──  SKILL.md

```

## How It Works

1. **CLAUDE.md** is the entrypoint — agents read it for stack, commands, and conventions.
2. **Skills** are loaded on demand when working in a specific domain.
3. Each skill has a **SKILL.md** (entrypoint) and **references/** (detailed submodules).
4. References are loaded only when needed — not all at once.

## Active Skills

| Skill    | Description                                            |
| -------- | ------------------------------------------------------ |
| python   | Python conventions, async, type hints, uv toolchain    |
| fastapi  | FastAPI APIs, Annotated style, DI, streaming           |
| jx       | Jinja server-rendered components (JX)                  |
| frontend | Frontend bootstrap, JS/TS tooling, Tailwind, Basecoat  |
| markdown | Markdown writing, structure, rumdl configuration       |

## Acknowledgments

The FastAPI skill is based on the official
[FastAPI agents skill](https://github.com/fastapi/fastapi/tree/master/fastapi/.agents/skills)
maintained by the FastAPI project.
