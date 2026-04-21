---
name: rich
description: Terminal UX with Rich -- console setup, tables, panels, progress, logging, tracebacks, and live updates. Load when building polished CLI output.
---

# Rich

Use this skill when the CLI needs better structure, readability, or feedback.

## Boundary

Use this skill for terminal presentation and interaction design.

- pair with `python` when implementing the CLI in Python
- keep logging policy, validation, and domain behavior outside this skill
- use this skill for how output is rendered, not for what the system means

## Reference Map

- `references/console.md` -- console setup, panels, tables, rules, markup, and
  output boundaries
- `references/progress.md` -- status, progress bars, live updates, and final
  summaries
- `references/logging.md` -- `RichHandler`, tracebacks, stderr, and failure
  presentation

## Assets

- `assets/main.py` -- a runnable CLI example with table, status, progress, and
  error output

## Output Boundaries

- use `Console` for user-facing output
- use `logging` for operational events
- keep stdout clean when output may be piped or parsed
- send human-readable errors to a console configured with `stderr=True`
- do not mix `print()` with Rich output

## Console Setup

```python
from rich.console import Console

console = Console()
error_console = Console(stderr=True)
```

Keep these near the CLI entrypoint instead of scattering ad hoc console
instances everywhere.

## Common Primitives

### Tables

Use `Table` for compact comparison, status, and inventory output.

- keep column names short
- align numbers and durations consistently
- avoid overly wide tables that wrap unpredictably

### Panels and Rules

Use `Panel` and `Rule` to separate sections only when that improves scanning.

- prefer one or two strong separators over heavy framing everywhere
- do not turn every message into a panel

### Status and Progress

- use `track()` for a single simple loop
- use `Progress()` when multiple tasks or richer status are needed
- keep task labels short and specific
- progress should describe meaningful work, not every tiny function call

### Syntax and JSON

- use `Syntax` when showing code snippets
- use `JSON` when pretty-printing structured payloads for humans
- avoid syntax highlighting for machine-oriented logs or giant payload dumps

## Logging and Tracebacks

Use `RichHandler` when logs are part of the interactive CLI experience.

```python
from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
```

- keep log messages concise
- prefer structured fields in logs; use Rich for rendering, not for hiding detail
- enable rich tracebacks for local CLI tools and developer workflows

## Live Output

Use `Live` when the screen should update in place:

- dashboards
- job runners
- multi-step setup flows
- streaming status views

Prefer `Live` only when the evolving state matters. Static output is usually
easier to debug and copy.

## Markup Guardrails

- prefer Rich markup over raw ANSI escapes
- escape or disable markup for untrusted user content
- keep styles purposeful; too much color hurts readability
- use color to signal meaning, not decoration

## Good CLI Defaults

- success output is short and calm
- failures are explicit and actionable
- progress output is transient when possible
- final summaries are compact
- important identifiers can be copied without stripping decorations
