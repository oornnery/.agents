---
name: rich
description: Console output with Rich -- formatting, tables, progress bars, tracebacks, logging. Load when building CLI output or styled console apps.
---

# Rich

Styled console output. See [Rich docs](https://rich.readthedocs.io/en/stable/).

```bash
uv add rich
```

## Guardrails

- Use `Console` for user-facing output, `logging` for operational logs.
- Never use `print()` -- always use `console.print()` for styled output.
- Use `stderr=True` for error consoles to keep stdout clean for piping.
- Prefer markup strings over manual ANSI codes.
- Use `RichHandler(rich_tracebacks=True)` for logging integration.
- Use `track()` for simple progress, `Progress()` for multi-task.
