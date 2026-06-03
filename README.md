# agents

Personal agents kit for Claude Code, OpenAI Codex, and OpenCode.

Use this repo as a `.agents` submodule to share the same project templates, local skills,
workflow commands, role agents, hooks, and setup expectations across coding agents.

The goal is a small always-loaded base plus focused skills loaded on demand.

## Full Setup

Install as a project submodule:

```bash
git submodule add https://github.com/oornnery/agents .agents
git submodule update --init --recursive
git submodule update --remote
```

Set the agent targets used by the skills installer:

```bash
SKILL_AGENT_FLAGS=(-a opencode -a codex -a claude-code)
```

Install a local skill from this repo:

```bash
npx skills add "https://github.com/oornnery/agents" --skill python "${SKILL_AGENT_FLAGS[@]}" -y
```

Install the core local skills:

```bash
for skill in python python-web typescript-web docs quality security git hooks rtk; do
  npx skills add "https://github.com/oornnery/agents" --skill "$skill" "${SKILL_AGENT_FLAGS[@]}" -y
done
```

Install optional local skills when needed:

```bash
for skill in arch design building-agents cicd httpx sqlmodel rich polars textual skill-builder; do
  npx skills add "https://github.com/oornnery/agents" --skill "$skill" "${SKILL_AGENT_FLAGS[@]}" -y
done
```

Reinstall upstream skills pinned by `skills-lock.json`:

```bash
npx skills experimental_install
```

The skills CLI writes generated skill copies to `.agents/skills/` and updates
`skills-lock.json`. Keep `.agents/` local unless you intentionally want to vendor
generated installs.

Install active upstream packs manually when not using the lockfile:

```bash
npx skills add JuliusBrussee/caveman "${SKILL_AGENT_FLAGS[@]}" -y
npx skills add JuliusBrussee/cavekit "${SKILL_AGENT_FLAGS[@]}" -y
npx skills add pydantic/skills "${SKILL_AGENT_FLAGS[@]}" -y
npx skills add fastapi/fastapi "${SKILL_AGENT_FLAGS[@]}" -y
```

Optional Claude plugin installs:

```bash
claude plugin install security-guidance@claude-plugins-official
claude plugin install frontend-design@claude-plugins-official
claude plugin install pydantic-ai@claude-plugins-official
claude plugin marketplace add JuliusBrussee/cavekit
claude plugin install ck@cavekit-marketplace
claude plugin marketplace add pbakaus/impeccable
claude plugin install impeccable@impeccable
claude plugin marketplace add tjboudreaux/cc-thinking-skills
claude plugin install thinking-skills@thinking-skills-marketplace
# claude-mem: install through its configured marketplace or project-specific instructions
```

Refresh optional upstream packs now pinned in the lockfile:

```bash
npx skills add pbakaus/impeccable "${SKILL_AGENT_FLAGS[@]}" -y
npx skills add aaron-he-zhu/seo-geo-claude-skills "${SKILL_AGENT_FLAGS[@]}" -y
npx skills add Nutlope/hallmark "${SKILL_AGENT_FLAGS[@]}" -y
npx skills add tjboudreaux/cc-thinking-skills "${SKILL_AGENT_FLAGS[@]}" -y
```

Install memory tooling when using persistent cross-session memory:

```bash
npm install -g cavemem
cavemem install
cavemem status
```

`JuliusBrussee/cavemem` and `JuliusBrussee/pitchr` are not listed as `npx skills add`
commands here because the skills CLI does not currently find a valid `SKILL.md` in
those repos. Treat them as manual tools until they expose installable skills.

## OpenCode Setup

OpenCode can use this repo through the same layered model:

- `AGENTS.md` / `templates/project/variants/AGENTS.*.md` for always-loaded project rules
- `.agents/skills/` for local skills
- `.agents/commands/` for reusable workflows
- `.agents/agents/` for focused role agents
- `.agents/hooks/` for local automation references

Recommended project wiring:

```bash
mkdir -p .opencode
cp .agents/templates/project/variants/AGENTS.base.md AGENTS.md
```

Then add the relevant stack overlay into the project `AGENTS.md`:

```md
@.agents/templates/project/variants/AGENTS.python.md
@.agents/templates/project/variants/AGENTS.fastapi.md
@.agents/templates/project/variants/AGENTS.tsjs.md
```

Use OpenCode-specific config in your dotfiles when you want global agents, commands,
plugins, and permissions. This repo provides the reusable content; it does not own
machine-local OpenCode config.

## Layout

| Path                                        | Purpose                                    |
| ------------------------------------------- | ------------------------------------------ |
| `templates/project/variants/AGENTS.base.md` | generic base agent instructions            |
| `templates/project/variants/AGENTS.*.md`    | project/stack overlays                     |
| `skills/`                                   | local skills loaded on demand              |
| `commands/`                                 | workflow entrypoints                       |
| `agents/`                                   | focused role agents                        |
| `hooks/`                                    | RTK, safety, autofix, lifecycle helpers    |
| `templates/`                                | project, stack, CI, and settings templates |
| `skills-lock.json`                          | active upstream skill reinstall lockfile   |

## Active Layers

### AGENTS Templates

Use the smallest stack overlay that fits the project:

- `AGENTS.base.md`: behavior contract shared by all stacks
- `AGENTS.python.md`: Python apps, packages, CLIs, scripts, services
- `AGENTS.fastapi.md`: Python web/API, FastAPI, SSR, HTMX/Jinja flows
- `AGENTS.tsjs.md`: TypeScript/JavaScript, Vite, React, React Router, Hono
- `AGENTS.cli.md`: terminal applications
- `AGENTS.library.md`: public/internal package APIs
- `AGENTS.script.md`: standalone scripts
- `AGENTS.harness.md`: agent harnesses and tool runtimes
- `RTK.md`: project RTK usage note

### Local Skills

Core:

`python`, `python-web`, `typescript-web`, `docs`, `quality`, `security`, `git`, `hooks`, `rtk`.

Optional:

`arch`, `design`, `building-agents`, `cicd`, `httpx`, `sqlmodel`, `rich`, `polars`, `textual`, `skill-builder`.

`python-web` owns normal FastAPI/Jinja2/HTMX guidance. Standalone `jinja2` and `htmx`
skills are retained as deeper references, not promoted as default setup.

### Commands

Core workflows:

`onboard`, `plan`, `build-fix`, `debug`, `review`, `verify`, `commit`, `compress`.

Optional workflows:

`docs`, `refactor`.

### Agents

Primary role agents:

- `python-engineer`
- `python-web-engineer`
- `typescript-web-engineer`

Focused subagent:

- `security-engineer`

Architecture and design are skills, not separate default agents. Load `arch` or `design`
when that lens is needed.

## Upstream Lockfile

`skills-lock.json` tracks upstream skills installed through the skills CLI so they
can be restored consistently:

- `JuliusBrussee/caveman`
- `JuliusBrussee/cavekit`
- `pydantic/skills`
- `fastapi/fastapi`
- `pbakaus/impeccable`
- `aaron-he-zhu/seo-geo-claude-skills`
- `Nutlope/hallmark`
- `tjboudreaux/cc-thinking-skills`

Do not hand-edit hashes. Add new upstream skills through the skills CLI and commit the
generated lockfile change.

Claude plugins are documented separately because plugin install state does not belong
in the skills lockfile.

`JuliusBrussee/cavemem` and `JuliusBrussee/pitchr` are optional manual tools, not
lockfile entries, until the skills CLI can install them as skills.

## Memory and Session Continuity

Use memory tooling as an optional layer, not as always-loaded instructions.

- `cavemem`: local persistent memory CLI; install with `npm install -g cavemem`
- `claude-mem`: Claude plugin path for persistent memory
- OpenCode memory plugins: keep in dotfiles or machine-local config, not in this repo
- Repo memory: keep durable project facts in docs or `AGENTS.md`, not only in chat memory

Memory rule: record stable preferences, project decisions, and validated facts; do not
store secrets, unverified guesses, or noisy session transcripts.

## External Pack Roles

| Pack                                      | Use when                                      | Default status |
| ----------------------------------------- | --------------------------------------------- | -------------- |
| `JuliusBrussee/caveman`                   | terse/token-efficient interaction modes       | locked         |
| `JuliusBrussee/cavekit`                   | spec/build/check/backprop workflow            | locked         |
| `rtk`                                     | shell output compression                      | local skill    |
| `JuliusBrussee/cavemem`                   | persistent memory CLI                         | manual tool    |
| `JuliusBrussee/pitchr`                    | pitch, offer, positioning                     | manual tool    |
| `pbakaus/impeccable`                      | frontend design critique and polish           | locked         |
| `pydantic/skills`                         | Pydantic, Pydantic AI, Logfire guidance       | locked         |
| `aaron-he-zhu/seo-geo-claude-skills`      | SEO/GEO content, audits, memory-management    | locked         |
| `Nutlope/hallmark`                        | UI generation/design critique                 | locked         |
| `tjboudreaux/cc-thinking-skills`          | hard reasoning, planning, debugging strategy  | locked         |
| `fastapi/fastapi`                         | FastAPI guidance                              | locked         |

Claude plugin equivalents:

| Plugin                                      | Use when                                |
| ------------------------------------------- | --------------------------------------- |
| `security-guidance@claude-plugins-official` | secure implementation/review            |
| `frontend-design@claude-plugins-official`   | frontend UI implementation and critique |
| `pydantic-ai@claude-plugins-official`       | Pydantic AI work                        |
| `impeccable@impeccable`                     | UI polish through Impeccable            |
| `ck@cavekit-marketplace`                    | Cavekit commands/plugin workflow        |
| `thinking-skills@thinking-skills-marketplace` | reasoning frameworks                  |
| `claude-mem`                                | persistent Claude memory                |

## Token and Context Rules

- Keep always-loaded files short.
- Move stack depth into skills and focused references.
- Keep README operational; do not turn it into a catalog of every installed thing.
- Prefer `AGENTS.base.md` plus one stack overlay over many broad instructions.
- Use RTK for noisy terminal output when available.
- Use `commands/compress.md` when reducing AGENTS, skill, memory, or preference files.

## RTK

Install and initialize:

```bash
rtk init -g
```

Project note:

```md
@.agents/templates/project/variants/RTK.md
```

Guidance lives in `skills/rtk/SKILL.md`.

## Maintenance Rules

- README lists active setup only.
- Skills contain reusable knowledge.
- Commands encode repeatable workflows.
- Agents encode role/persona routing.
- Templates are copied or referenced by projects.
- Lockfile pins upstream skills only.

## Acknowledgments

Influences include FastAPI official agent guidance, Caveman/Cavekit, RTK, token-efficient
agent instruction research, and practical multi-agent coding workflows.
