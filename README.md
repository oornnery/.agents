# agents

Personal agents kit. Use as `.agents` submodule to share the same commands, skills, hooks, templates, and tool expectations across Claude Code, Codex, and OpenCode.

This repo reflects the tools I actually use. The goal is a small base with optional stack skills, not a huge always-loaded catalog.

## Install

```bash
git submodule add https://github.com/oornnery/agents .agents
git submodule update --init --recursive
git submodule update --remote
```

## Layout

| Path                                        | Purpose                                                |
| ------------------------------------------- | ------------------------------------------------------ |
| `templates/project/variants/AGENTS.base.md` | generic base agent instructions                        |
| `templates/project/variants/AGENTS.*.md`    | project/stack overlays                                 |
| `commands/`                                 | workflow entrypoints                                   |
| `agents/`                                   | focused personas for Python, design, arch, security    |
| `skills/`                                   | local skills, loaded on demand                         |
| `hooks/`                                    | RTK rewrite, safety gates, autofix, lifecycle helpers  |
| `templates/`                                | project, stack, CI, and settings templates             |
| `skills-lock.json`                          | upstream skill reinstall lockfile                      |

## Current Setup

### Agent CLIs

These are the coding tools this repo is meant to support:

- **Claude Code**: primary Claude CLI and Claude plugin target.
- **OpenAI Codex**: Codex CLI and Codex skill/plugin target.
- **OpenCode**: alternate terminal agent and skill target.

External skills should be installed for all active agents when possible. The matching environment variable used by my setup scripts is:

```bash
SKILL_AGENTS=opencode,codex,claude-code
```

### Workflow Layer

| Tool       | Role                                                              |
| ---------- | ----------------------------------------------------------------- |
| RTK        | compress and rewrite noisy terminal output before it hits context |
| Caveman    | terse interaction and compression style                           |
| Cavekit    | spec/build/check/backprop workflow                                |
| Claude-Mem | persistent memory across Claude/OpenCode/Codex sessions           |

### External Skills and Plugins

| Source / Plugin                              | Role                                    | Target                 |
| -------------------------------------------- | --------------------------------------- | ---------------------- |
| `JuliusBrussee/caveman`                      | caveman modes and compact commit/review | skills                 |
| `JuliusBrussee/cavekit`                      | spec/build/check/backprop               | skills + Claude plugin |
| `pbakaus/impeccable`                         | frontend/design critique and polish     | skills + Claude plugin |
| `pydantic/skills`                            | Pydantic, Pydantic AI, Logfire guidance | skills + Claude plugin |
| `microsoft/skills --skill fastapi-router-py` | FastAPI router guidance                 | skills                 |
| `aaron-he-zhu/seo-geo-claude-skills`         | SEO/GEO research, content, audits       | skills + Claude plugin |
| `Nutlope/hallmark`                           | anti-AI-slop UI design and critique     | skills                 |
| `tjboudreaux/cc-thinking-skills`             | mental models for hard decisions        | Claude plugin          |
| `security-guidance@claude-plugins-official`  | secure implementation and review        | Claude plugin          |
| `frontend-design@claude-plugins-official`    | frontend design guidance                | Claude plugin          |
| `pydantic-ai@claude-plugins-official`        | Pydantic AI guidance                    | Claude plugin          |

`skills-lock.json` pins upstream skills reinstalled through the skills CLI. Claude plugins are documented here because their install state lives in Claude's plugin system, not in the skills lockfile. Do not hand-edit lockfile hashes; keep generated entries only.

## Commands

| Command           | Purpose                                                     |
| ----------------- | ----------------------------------------------------------- |
| `onboard`         | detect stack, verify tools, find validation, map repo       |
| `plan`            | implementation plan                                         |
| `debug`           | reproduce failure, isolate boundary, prove root cause       |
| `review`          | read-only code review                                       |
| `verify`          | adversarial validation                                      |
| `build-fix`       | fix lint/types/tests/docs/CI incrementally                  |
| `docs`            | sync docs from source of truth                              |
| `refactor`        | behavior-preserving structure improvement                   |
| `compress`        | engine-agnostic structural prompt/document compression      |
| `checkpoint`      | record known-good/known-yellow state                        |
| `extract-pattern` | capture reusable proven pattern                             |
| `commit`          | safe staging + conventional commit prep                     |

## Local Skills

Core skills:

`python`, `docs`, `quality`, `security`, `git`, `hooks`, `rtk`.

Design and architecture:

`arch`, `design`.

Optional stack/library skills:

`building-agents`, `cicd`, `htmx`, `httpx`, `jinja2`, `polars`, `python-web`, `rich`, `skill-builder`, `sqlmodel`, `textual`, `typescript-web`.

FastAPI, Pydantic, Stow, and similar focused libraries can come from upstream skills or local skills depending on the project. They should be loaded only when the repo actually uses that stack.

Install local skill:

```bash
npx skills add "https://raw.githubusercontent.com/oornnery/agents/master/skills/python/SKILL.md" -y
npx skills add "https://github.com/oornnery/agents" --skill python -y
```

Swap `python` for any folder under `skills/`.

## Upstream Skills

`skills-lock.json` includes Cavekit/Caveman and selected upstream stack skills. It should stay focused on external skills I actively install or want to reinstall consistently.

Reinstall locked skills:

```bash
npx skills experimental_install
```

Common manual installs:

```bash
npx skills add JuliusBrussee/caveman -a opencode,codex,claude-code
npx skills add JuliusBrussee/cavekit -a opencode,codex,claude-code
npx skills add pbakaus/impeccable -a opencode,codex,claude-code
npx skills add pydantic/skills -a opencode,codex,claude-code
npx skills add microsoft/skills --skill fastapi-router-py -a opencode,codex,claude-code
npx skills add aaron-he-zhu/seo-geo-claude-skills -a opencode,codex,claude-code
npx skills add nutlope/hallmark -a opencode,codex,claude-code
npx skills add tjboudreaux/cc-thinking-skills -a opencode,codex,claude-code
```

Claude plugin installs:

```bash
claude plugin install security-guidance@claude-plugins-official
claude plugin install frontend-design@claude-plugins-official
claude plugin install pydantic-ai@claude-plugins-official
claude plugin marketplace add pbakaus/impeccable
claude plugin install impeccable@impeccable
claude plugin marketplace add JuliusBrussee/cavekit
claude plugin install ck@cavekit-marketplace
claude plugin marketplace add aaron-he-zhu/seo-geo-claude-skills
claude plugin marketplace add tjboudreaux/cc-thinking-skills
claude plugin install thinking-skills@thinking-skills-marketplace
```

### When to Use External Packs

- **SEO/GEO**: use only for marketing, search visibility, content planning, technical SEO audits, and `/aaron:*` workflows.
- **Hallmark**: use for UI generation, design critique, redesign, or studying a screenshot/site; do not load it for routine backend work.
- **Thinking skills**: use when the task explicitly benefits from a reasoning framework, such as architecture decisions, debugging strategy, planning, pre-mortems, or red-team review.

For `tjboudreaux/cc-thinking-skills`, Claude plugin install is the primary path. The `npx skills add` command is listed as a skills-host attempt only; if unsupported, keep it plugin-only.

## Python Base

Default Python stack:

- Python 3.12+
- `uv`
- `ruff`
- `ty`
- `pyright`
- `pytest`
- `rumdl`
- `taskipy`
- `pre-commit`
- `bandit`

Default validation:

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pyright
uv run pytest -v
```

Bandit is explicit security review:

```bash
uv run task sec
```

## Token Optimization Stack

Goal: reduce waste across whole agent loop without reducing prompt effectiveness.

| Layer                | Rule                                                                                   |
| -------------------- | -------------------------------------------------------------------------------------- |
| Terminal output      | RTK rewrites noisy commands before context                                             |
| Base instructions    | keep startup docs terse; move detail into variants/skills                              |
| Skill loading        | narrow triggers; metadata first, refs on demand                                        |
| Session continuity   | hooks/memory recover context after compaction                                          |
| Backend/tool context | prefer `--json`, semantic exit codes, structured errors; MCP for live state            |
| Retrieval            | graph/symbol/semantic search optional, not default stack                               |
| Measurement          | token audits over guessing                                                             |
| Prompt effectiveness | preserve task intent, priority, triggers, constraints, examples needed for correctness |

### RTK

Shell-compression layer:

```bash
rtk init -g
```

Guidance: `skills/rtk/SKILL.md`.

### Caveman/Cavekit

Installed upstream ecosystem:

- Caveman: terse output mode without changing reasoning depth
- Caveman-compress: input-file compression inspiration; local `commands/compress.md` is engine-agnostic replacement
- Caveman-commit/review: terse commit and PR feedback
- Cavekit: spec/build/check/backprop workflow

Reinstall:

```bash
npx skills add JuliusBrussee/caveman
npx skills add JuliusBrussee/cavekit
```

### Cavemem

Persistent local memory for session continuity:

```bash
npm install -g cavemem
cavemem install
cavemem search "<q>"
cavemem viewer
cavemem status
```

## Compression Doctrine

- Compress structurally: delete duplication, merge repeated examples, move detail to refs.
- Keep prompt power: preserve triggers, invariants, priority order, MUST/NEVER/ALWAYS force.
- Optimize always-loaded files first.
- Use progressive disclosure: base -> skill metadata -> focused refs/assets.
- Measure with tokenizer when possible.

## Acknowledgments

Influences: FastAPI official agents skill, `drona23/claude-token-efficient`, `Leonxlnx/agentic-ai-prompt-research`, `WorldFlowAI/everything-claude-code`, `affaan-m/everything-claude-code`, `wshobson/agents`, JuliusBrussee Caveman/Cavekit.
