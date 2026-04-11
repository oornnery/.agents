---
name: typer
description: CLI development with Typer -- commands, typed options, async, testing. Load when building CLI applications.
---

# Typer

CLI development with Typer. See [Typer docs](https://typer.tiangolo.com/).

```bash
uv add typer rich
```

## Patterns

- One `Typer()` app, subcommands via `app.add_typer()`.
- `typer.Argument()` for positional, `typer.Option()` for flags.
- `asyncio.run()` wrapper for async commands.
- Pair with Rich for styled output.
- Test with `typer.testing.CliRunner`.

## Guardrails

- Keep commands thin -- delegate business logic to services.
- Use type hints for all command params.
- Return stable exit codes for automation (`0` success, `1` error, `2` usage).
- Avoid printing secrets in stdout/stderr.
- Use `err=True` for error messages to write to stderr.
