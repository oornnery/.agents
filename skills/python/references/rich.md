# Rich Reference

Console output, formatting, tables, progress bars, tracebacks, and logging integration with Rich.

## Documentation

- Rich Docs: <https://rich.readthedocs.io/en/stable/>
- Console API: <https://rich.readthedocs.io/en/stable/console.html>
- Tables: <https://rich.readthedocs.io/en/stable/tables.html>
- Progress: <https://rich.readthedocs.io/en/stable/progress.html>
- Logging Handler: <https://rich.readthedocs.io/en/stable/logging.html>
- Markup: <https://rich.readthedocs.io/en/stable/markup.html>
- Tracebacks: <https://rich.readthedocs.io/en/stable/traceback.html>

## Install

```bash
uv add rich
```

## Console Basics

```python
from rich.console import Console

console = Console()

console.print("Hello, [bold magenta]World[/bold magenta]!")
console.print("[green]Success[/green] — operation completed.")
console.print("[red bold]Error:[/red bold] something went wrong.", style="red")
```

### Print with Markup

```python
console.print("[bold]Name:[/bold] Alice")
console.print("[dim]Processing...[/dim]")
console.print("[link=https://example.com]Click here[/link]")
```

### Stderr Output

```python
err_console = Console(stderr=True)
err_console.print("[red]Error: file not found[/red]")
```

## Tables

```python
from rich.table import Table

table = Table(title="Deployments")
table.add_column("Service", style="cyan", no_wrap=True)
table.add_column("Version", style="magenta")
table.add_column("Status", justify="center")

table.add_row("api", "2.1.0", "[green]healthy[/green]")
table.add_row("worker", "2.0.9", "[yellow]degraded[/yellow]")
table.add_row("scheduler", "2.1.0", "[red]down[/red]")

console.print(table)
```

## Progress Bars

### Simple Iteration

```python
from rich.progress import track

for item in track(items, description="Processing..."):
    process(item)
```

### Advanced Progress

```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("[cyan]Downloading...", total=100)
    while not progress.finished:
        progress.update(task, advance=1)
```

### Multiple Tasks

```python
with Progress() as progress:
    download = progress.add_task("[green]Downloading", total=1000)
    extract = progress.add_task("[blue]Extracting", total=500)

    # Update independently
    progress.update(download, advance=10)
    progress.update(extract, advance=5)
```

## Panels and Layout

```python
from rich.panel import Panel

console.print(Panel("Application started", title="Status", border_style="green"))
```

```python
from rich.columns import Columns

items = [Panel(f"Item {i}", expand=True) for i in range(6)]
console.print(Columns(items))
```

## Trees

```python
from rich.tree import Tree

tree = Tree("[bold]Project")
src = tree.add("[blue]src/")
src.add("main.py")
src.add("utils.py")
tree.add("[blue]tests/")
console.print(tree)
```

## Logging with RichHandler

```python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)

logger = logging.getLogger(__name__)
logger.info("Server started on port %d", 8000)
logger.warning("Cache miss for key: %s", "user:42")
```

## Rich Tracebacks

Install globally for all uncaught exceptions:

```python
from rich.traceback import install

install(show_locals=True)
```

Or use in logging only via `RichHandler(rich_tracebacks=True)`.

## Inspect Objects

```python
from rich import inspect

inspect(some_object, methods=True)
```

## Status Spinner

```python
with console.status("[bold green]Working on it...") as status:
    do_work()
    status.update("[bold blue]Almost done...")
    do_more_work()
```

## Prompt and Confirm

```python
from rich.prompt import Prompt, Confirm

name = Prompt.ask("Enter your name", default="World")
proceed = Confirm.ask("Do you want to continue?")
```

## Guardrails

- Use `Console` for user-facing output, `logging` for operational logs.
- Never use `print()` — always use `console.print()` for styled output.
- Use `stderr=True` for error consoles to keep stdout clean for piping.
- Prefer markup strings over manual ANSI codes.
