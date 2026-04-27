# skills

Custom skills and agent knowledge base. Use as `.agents` submodule; layer base instructions, variants, commands, skills, hooks, and upstream lockfile.

## Install

```bash
git submodule add https://github.com/oornnery/skills .agents
git submodule update --init --recursive
git submodule update --remote
```

## Layout

| Path                                        | Purpose                                               |
| ------------------------------------------- | ----------------------------------------------------- |
| `templates/project/variants/AGENTS.base.md` | generic base agent instructions                       |
| `templates/project/variants/AGENTS.*.md`    | project/stack overlays                                |
| `commands/`                                 | workflow entrypoints                                  |
| `agents/`                                   | Python/design/architecture/security personas          |
| `skills/`                                   | local domain skills, loaded on demand                 |
| `hooks/`                                    | RTK rewrite, safety gates, autofix, lifecycle helpers |
| `templates/`                                | project, stack, CI, and settings templates            |
| `skills-lock.json`                          | upstream skill reinstall lockfile                     |

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

`arch`, `building-agents`, `cicd`, `design`, `docs`, `git`, `hooks`, `htmx`, `httpx`, `jinja2`, `polars`, `python`, `quality`, `rich`, `rtk`, `security`, `skill-builder`, `sqlmodel`, `textual`.

Install local skill:

```bash
npx skills add "https://raw.githubusercontent.com/oornnery/skills/master/skills/python/SKILL.md" -y
npx skills add "https://github.com/oornnery/skills" --skill python -y
```

Swap `python` for any folder under `skills/`.

## Upstream Skills

`skills-lock.json` includes Cavekit/Caveman, FastAPI, htmx, HTTPX, JX, SOLID, Tailwind, Textual, SQLModel, CI/CD, and related expert skills.

Reinstall locked skills:

```bash
npx skills experimental_install
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
