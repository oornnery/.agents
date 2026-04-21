# Rich Console

## Console Setup

Use one console for normal output and one for errors when needed.

```python
from rich.console import Console

console = Console()
error_console = Console(stderr=True)
```

Keep console ownership near the CLI entrypoint.

## Tables

Use tables for:

- compact status views
- summaries
- item inventories
- result comparisons

Keep:

- headers short
- numeric columns aligned
- widths under control

## Panels and Rules

Use `Panel` and `Rule` to separate important sections.

Do not wrap every message in a panel. Use framing only where scanning improves.

## JSON and Syntax

Use:

- `JSON` for human-readable payloads
- `Syntax` for code or config examples

Avoid these for machine-oriented output that should stay easy to parse or copy.

## Markup

Prefer Rich markup over raw ANSI escapes.

Escape or disable markup if the content is untrusted.
