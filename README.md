# skills

My custom skills and agent knowledge base for AI coding assistants. Organized into rules,
commands, agents, and skills for on-demand loading.

## Usage

```bash
git submodule add https://github.com/oornnery/skills .claude
git submodule update --init
git submodule update --remote   # propagate updates
```

## Structure

- **`CLAUDE.md`** -- entrypoint with stack, agents, commands, and skills index.
- **`rules/`** -- always-on conventions, auto-loaded by file globs.
- **`agents/`** -- specialized personas with constrained tools and model selection.
- **`commands/`** -- procedural workflows invoked per task.
- **`skills/`** -- domain knowledge modules loaded on demand.
- **`hooks/`** -- automation hooks (RTK rewrite, safety gate, autofix, lifecycle).
- **`templates/`** -- project bootstrap files.

See `CLAUDE.md` for the full index of rules, agents, commands, and skills.

## RTK Integration

RTK (Rust Token Killer) auto-rewrites CLI commands for 60-90% token
savings. Install: `rtk init -g`.

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
