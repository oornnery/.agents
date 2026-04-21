#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "rich",
# ]
# ///

from __future__ import annotations

import logging
import time

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress
from rich.rule import Rule
from rich.table import Table

console = Console()
error_console = Console(stderr=True)


def setup_logging() -> None:
    logging.basicConfig(
        level='INFO',
        format='%(message)s',
        handlers=[RichHandler(rich_tracebacks=True)],
    )


def render_summary() -> None:
    table = Table(title='Deploy Summary')
    table.add_column('Service')
    table.add_column('Status')
    table.add_column('Duration', justify='right')

    table.add_row('api', '[green]ok[/green]', '12s')
    table.add_row('worker', '[yellow]warning[/yellow]', '18s')
    table.add_row('cron', '[green]ok[/green]', '9s')
    console.print(table)


def main() -> None:
    setup_logging()
    logging.info('starting demo run')

    console.print(Panel('Running deployment checks', title='rich demo'))
    console.print(Rule('tasks'))

    with console.status('Preparing environment...'):
        time.sleep(0.1)

    with Progress() as progress:
        task = progress.add_task('Deploying', total=3)
        for _ in range(3):
            time.sleep(0.1)
            progress.advance(task)

    render_summary()
    error_console.print('[bold red]warning:[/bold red] one service needs review')


if __name__ == '__main__':
    main()
