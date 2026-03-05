# Typer Reference

CLI development with Typer including command structure, typed options/arguments, async execution, and testing.

## Documentation

- Typer Docs: <https://typer.tiangolo.com/>
- Typer Tutorial: <https://typer.tiangolo.com/tutorial/>
- Testing CLIs: <https://typer.tiangolo.com/tutorial/testing/>

## Install

```bash
uv add typer rich
```

## CLI Layout Pattern

```python
import typer

app = typer.Typer(help="Project CLI")
users = typer.Typer(help="User operations")
app.add_typer(users, name="users")
```

## Command Pattern

```python
from pathlib import Path
import typer


@users.command("import")
def import_users(
    file: Path = typer.Argument(..., exists=True, readable=True),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate without writing"),
) -> None:
    if dry_run:
        typer.echo(f"Validated file: {file}")
        raise typer.Exit(code=0)
    typer.echo(f"Imported users from: {file}")
```

## Validation and Exit Codes

```python
@app.command()
def run(env: str = typer.Option("dev")) -> None:
    if env not in {"dev", "staging", "prod"}:
        typer.echo("Invalid env", err=True)
        raise typer.Exit(code=2)
    typer.echo(f"Running in {env}")
```

## Async Integration Pattern

```python
import asyncio
import typer


@app.command()
def sync_users() -> None:
    asyncio.run(_sync_users())


async def _sync_users() -> None:
    ...
```

## Rich Integration

Pair Typer with Rich for styled output:

```python
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command()
def list_users() -> None:
    table = Table(title="Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Status", style="green")
    table.add_row("1", "Alice", "active")
    table.add_row("2", "Bob", "inactive")
    console.print(table)
```

## Callbacks and Global Options

```python
@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    if verbose:
        configure_logging(logging.DEBUG)
```

## Testing Pattern

```python
from typer.testing import CliRunner

runner = CliRunner()


def test_run_default() -> None:
    result = runner.invoke(app, ["run"])
    assert result.exit_code == 0
    assert "Running in dev" in result.stdout


def test_run_invalid_env() -> None:
    result = runner.invoke(app, ["run", "--env", "unknown"])
    assert result.exit_code == 2
    assert "Invalid env" in result.stdout
```

## Guardrails

- Keep commands thin — delegate business logic to services.
- Use type hints for all command params.
- Return stable exit codes for automation (`0` success, `1` error, `2` usage).
- Avoid printing secrets in stdout/stderr.
- Use `err=True` for error messages to write to stderr.
