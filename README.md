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

## Token Optimization Stack

This repo treats token efficiency as a systems problem, not a single-tool
problem. The goal is to reduce waste across the whole agent loop: shell output,
always-loaded instructions, skill loading, session recovery, code retrieval,
and noisy backend/tool responses.

### What Changed In This Repo

The main repo changes follow a few rules:

- keep always-loaded files small and topic-focused
- move detail into specialized skills and references instead of bloating base
  instructions
- prefer narrow skills with progressive disclosure over broad catch-all skills
- use hooks and persistent memory to recover context instead of re-explaining it
- prefer structured CLI output and explicit error context over noisy tool dumps

That is why the repo now leans harder on short `AGENTS.*` variants, scoped
`SKILL.md` files, compressed instruction files, and memory/hooks that preserve
useful state across sessions.

### Design Principles

| Layer                    | Repo approach                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| Terminal output          | use RTK to rewrite noisy commands before they hit context                                              |
| Base instructions        | keep `AGENTS.base` and startup docs terse; push details into variants and skills                       |
| Skill loading            | keep triggers narrow so most skills stay metadata-only until needed                                    |
| Session continuity       | use hooks plus persistent memory so compaction does not force a full re-brief                          |
| Backend and tool context | prefer CLI `--json`, semantic exit codes, and structured errors; use MCP for live state, not doc dumps |
| Retrieval                | treat graph, symbol, and semantic search as optional layers, not defaults to stack blindly             |
| Measurement              | leave room for token audits and compaction checks instead of guessing                                  |

### RTK

RTK is the shell-compression layer. It auto-rewrites CLI commands so high-noise
output is compact before it reaches the model.

```bash
rtk init -g
```

Guidance in `skills/rtk/SKILL.md`.

### Caveman Ecosystem (JuliusBrussee)

This repo uses Caveman as the prompt/output discipline layer. The useful part is
that it is composable: response compression, input-file compression, terse
commit/review flows, and spec-driven execution all work independently.

#### Caveman — output compression

Use at session start when you want terse answers without changing the actual
reasoning depth. It reduces output tokens while keeping the technical content.

| Trigger                      | Effect                             |
| ---------------------------- | ---------------------------------- |
| `/caveman` or "caveman mode" | activates terse output for session |
| "less tokens please"         | same                               |
| `/caveman ultra`             | maximum compression                |

Install: already in `.agents/skills/caveman/` via `npx skills add JuliusBrussee/caveman`.

#### Caveman-compress — input file compression

Use on always-loaded files that cost tokens every session. The repo strategy is
to compress startup-heavy files and keep human-readable backups next to them.

```bash
cd .agents/skills/caveman-compress && python3 -m scripts <filepath>
```

Trigger: `/caveman:compress <filepath>` or "compress memory file".

#### Caveman-commit — terse commit messages

Keeps commit subjects short and reason-first.

Trigger: `/caveman-commit` or "write a commit message".

#### Caveman-review — terse code review

Keeps review comments compact and actionable.

Trigger: `/caveman-review` or "review this PR".

### Cavekit — spec-driven workflow

This is the repo's execution discipline layer: write a spec, build against it,
and backprop failures into the spec instead of letting process drift.

| Command      | What it does                                              |
| ------------ | --------------------------------------------------------- |
| `/ck:spec`   | create or amend SPEC.md                                   |
| `/ck:build`  | plan → execute → auto-backprop failures into SPEC.md      |
| `/ck:check`  | read-only drift report between code and SPEC.md           |

Install: already in `.agents/skills/` via `npx skills add JuliusBrussee/cavekit`.

### Cavemem — persistent cross-session memory

This is the continuity layer. It stores compact session memory locally so the
agent can recover relevant prior decisions without restating everything in the
next session.

```bash
npm install -g cavemem
cavemem install         # wires hooks into Claude Code
cavemem search "<q>"    # query past context
cavemem viewer          # browse at localhost:37777
cavemem status          # check health
```

MCP tools available to agents: `search`, `timeline`, `get_observations`, `list_sessions`. Memory accumulates at session boundaries — no manual steps. `<private>...</private>` stripped at write.

Settings: `~/.cavemem/settings.json`.

### Ideas Adapted Into The Repo

Not everything was installed directly. Several projects shaped how the repo was
refined:

- `InsForge/InsForge`: backend context engineering; keep static knowledge in
  skills, use CLI for structured actions, reserve MCP for live state
- `mksglu/context-mode`: compaction recovery and session-state ideas adapted
  into hook and harness patterns
- `drona23/claude-token-efficient`: terse defaults, less repetition, smaller
  startup instructions
- `nadimtuhin/claude-token-optimizer`: topic-based docs and smaller
  always-loaded core files
- `alexgreensh/token-optimizer`: token audits, compaction checkpoints, and
  measurement as future work
- `tirth8205/code-review-graph`, `Mibayy/token-savior`, and
  `zilliztech/claude-context`: retrieval should be layered and piloted, not all
  enabled by default

### Recommended Workflow

1. Use RTK for shell noise.
2. Start sessions with `/caveman` when terse output is enough.
3. Compress expensive always-loaded files with `caveman-compress`.
4. Use Cavekit for spec/build/check loops instead of free-form drift.
5. Let Cavemem carry session memory through hooks.

### Reinstall Caveman Skills

```bash
npx skills add JuliusBrussee/caveman     # caveman, caveman-compress, caveman-commit, caveman-review, compress, caveman-help
npx skills add JuliusBrussee/cavekit     # spec, build, check, backprop, caveman
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
