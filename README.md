# .agents

Agent knowledge base for AI coding assistants. Organized into rules,
commands, and skills for on-demand loading.

## Usage

```bash
git submodule add https://github.com/oornnery/.agents .claude
git submodule update --init
git submodule update --remote   # propagate updates
```

## Structure

- **`CLAUDE.md`** -- entrypoint with stack, commands, and skills index.
- **`rules/`** -- always-on conventions, auto-loaded by file globs.
- **`commands/`** -- procedural workflows invoked per task.
- **`skills/`** -- domain knowledge modules loaded on demand.
- **`hooks/`** -- versionable hook templates (RTK rewrite).
- **`templates/`** -- project bootstrap files.

See `CLAUDE.md` for the full index of rules, commands, and skills.

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
