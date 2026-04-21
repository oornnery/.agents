# skills

My custom skills and agent knowledge base for AI coding assistants. This repo
is organized around a base `AGENTS` variant, stack and project variants,
workflow commands, specialized agents, local skills, and a lockfile for
upstream installed skills.

## Install In A Project

Add this repo as a submodule at `.agents`:

```bash
git submodule add https://github.com/oornnery/skills .agents
git submodule update --init --recursive
git submodule update --remote
```

## Structure

- **`templates/project/variants/AGENTS.base.md`** -- generic base instructions
  for projects
- **`agents/`** -- specialized personas for Python, design, architecture, and security
- **`commands/`** -- workflow entrypoints such as `onboard`, `plan`, `debug`, `review`, `verify`, and `build-fix`
- **`skills/`** -- local domain skills loaded on demand
- **`skills-lock.json`** -- upstream skill lockfile for external skills installed into the repo
- **`hooks/`** -- automation hooks for RTK rewrite, safety gates, autofix, and lifecycle helpers
- **`templates/`** -- project bootstrap files organized by project, stack, CI, and local settings profiles

Use `templates/project/variants/AGENTS.base.md` as the generic base, then layer
the relevant `AGENTS.*.md` variant for the project shape or stack.

## Template Layout

- **`templates/project/`** -- root project files such as `.env.example`, `.gitignore`, and project instruction variants
- **`templates/project/variants/`** -- project-level `AGENTS.*.md` base and
  overlay variants
- **`templates/stack/python/`** -- Python stack scaffolding such as `pyproject.toml`, `ruff.toml`, `ty.toml`, `Dockerfile`, and lint configs
- **`templates/ci/github/`** -- GitHub Actions workflow templates
- **`templates/settings/`** -- local Claude settings profiles such as `local.python.json`, `local.fullstack.json`, `local.hooks.json`, `local.default.json`, `local.custom-model.json`, `local.glm.json`, and `local.ollama.json`

## Commands Quick Ref

| Command           | What it does                                                                   |
| ----------------- | ------------------------------------------------------------------------------ |
| `onboard`         | detect stack, verify toolchain, find validation entrypoints, and map the repo  |
| `plan`            | produce an implementation plan with phases, files, risks, and testing strategy |
| `debug`           | reproduce a failure, isolate the boundary, and confirm the root cause          |
| `review`          | review changed code for correctness, security, maintainability, and risk       |
| `verify`          | run adversarial verification with baseline validation and edge-case probes     |
| `build-fix`       | fix broken lint, types, tests, docs, or CI incrementally with minimal diffs    |
| `docs`            | sync README, commands, agents, skills, and other docs from source of truth     |
| `refactor`        | improve structure without changing behavior                                    |
| `checkpoint`      | record a known-good or known-yellow state with metadata                        |
| `extract-pattern` | turn a proven, non-obvious pattern into a focused reusable document            |
| `commit`          | stage safely, check for sensitive files, and prepare a clean commit            |

## Agents

The repo currently ships these local agents:

- `python-engineer`
- `design-engineer`
- `architect-engineer`
- `security-engineer`

## Local Skills

The repo currently ships these local skills:

- `arch`
- `building-agents`
- `cicd`
- `design`
- `docs`
- `git`
- `hooks`
- `htmx`
- `httpx`
- `jinja2`
- `polars`
- `python`
- `quality`
- `rich`
- `rtk`
- `security`
- `skill-builder`
- `sqlmodel`
- `textual`

## Locked Upstream Skills

`skills-lock.json` records upstream skills that should be reinstalled alongside
the local `skills/` directory. The current lockfile includes:

- `building-pydantic-ai-agents`
- `cicd-expert`
- `fastapi`
- `htmx-expert`
- `httpx`
- `jx-components`
- `solid`
- `solidjs-patterns`
- `tailwind-design-system`
- `textual-builder`
- `textual-testing`

To reinstall the locked upstream skills:

```bash
npx skills experimental_install
```

## Add A Skill From This Repo

You can add one of this repo's local skills directly using the full URL to its
`SKILL.md` file.

Examples:

```bash
npx skills add "https://raw.githubusercontent.com/oornnery/skills/master/skills/python/SKILL.md" -y
npx skills add "https://raw.githubusercontent.com/oornnery/skills/master/skills/security/SKILL.md" -y
npx skills add "https://raw.githubusercontent.com/oornnery/skills/master/skills/arch/SKILL.md" -y
```

Replace the skill path with any folder under `skills/`, for example:

- `skills/design/SKILL.md`
- `skills/docs/SKILL.md`
- `skills/git/SKILL.md`
- `skills/hooks/SKILL.md`
- `skills/htmx/SKILL.md`
- `skills/httpx/SKILL.md`
- `skills/jinja2/SKILL.md`
- `skills/polars/SKILL.md`
- `skills/skill-builder/SKILL.md`
- `skills/textual/SKILL.md`

If your installed `npx skills` prefers repo-aware installation, use the repo
URL plus `--skill`:

```bash
npx skills add "https://github.com/oornnery/skills" --skill python -y
npx skills add "https://github.com/oornnery/skills" --skill security -y
```

## RTK Integration

RTK (Rust Token Killer) auto-rewrites CLI commands for major token savings.
Install it globally with:

```bash
rtk init -g
```

## Acknowledgments

- The FastAPI skill is based on the official
  [FastAPI agents skill](https://github.com/fastapi/fastapi/tree/master/fastapi/.agents/skills).
- Output token efficiency rules inspired by
  [drona23/claude-token-efficient](https://github.com/drona23/claude-token-efficient).
- Agent prompt research from
  [Leonxlnx/agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research).
- Agent orchestration patterns from
  [WorldFlowAI/everything-claude-code](https://github.com/WorldFlowAI/everything-claude-code).
- Production-ready plugin architecture from
  [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code).
- [wshobson/agents](https://github.com/wshobson/agents)
