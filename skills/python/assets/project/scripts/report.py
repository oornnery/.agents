#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "rich",
# ]
# ///

from __future__ import annotations

from rich.console import Console
from rich.table import Table

console = Console()


def main() -> None:
    table = Table(title='daily report')
    table.add_column('task')
    table.add_column('status')
    table.add_row('lint', 'ok')
    table.add_row('tests', 'ok')
    console.print(table)


if __name__ == '__main__':
    main()
