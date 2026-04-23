---
name: rich
description: Terminal UX with Rich -- console setup, tables, panels, progress, logging, tracebacks, live updates. Load when building polished CLI output.
---

# Rich

Use when CLI needs better structure, readability, feedback.

## Boundary

Use for terminal presentation and interaction design.

- pair with `python` when implementing CLI in Python
- keep logging policy, validation, domain behavior outside this skill
- use for how output rendered, not what system means

## Reference Map

- `references/console.md` -- console setup, panels, tables, rules, markup, output boundaries
- `references/progress.md` -- status, progress bars, live updates, final summaries
- `references/logging.md` -- `RichHandler`, tracebacks, stderr, failure presentation

## Assets

- `assets/main.py` -- runnable CLI example with table, status, progress, error output

## Output Boundaries

- use `Console` for user-facing output
- use `logging` for operational events
- keep stdout clean when output may be piped or parsed
- send human-readable errors to console configured with `stderr=True`
- do not mix `print()` with Rich output

## Console Setup

```python
from rich.console import Console

console = Console()
error_console = Console(stderr=True)
```

Keep near CLI entrypoint, not scattered ad hoc console instances.

## Common Primitives

### Tables

Use `Table` for compact comparison, status, inventory output.

- keep column names short
- align numbers and durations consistently
- avoid overly wide tables that wrap unpredictably

### Panels and Rules

Use `Panel` and `Rule` to separate sections only when it improves scanning.

- prefer one or two strong separators over heavy framing everywhere
- do not turn every message into a panel

### Status and Progress

- use `track()` for single simple loop
- use `Progress()` when multiple tasks or richer status needed
- keep task labels short and specific
- progress should describe meaningful work, not every tiny function call

### Syntax and JSON

- use `Syntax` when showing code snippets
- use `JSON` when pretty-printing structured payloads for humans
- avoid syntax highlighting for machine-oriented logs or giant payload dumps

## Logging and Tracebacks

Use `RichHandler` when logs part of interactive CLI experience.

```python
from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
```

- keep log messages concise
- prefer structured fields in logs; use Rich for rendering, not hiding detail
- enable rich tracebacks for local CLI tools and developer workflows

## Live Output

Use `Live` when screen should update in place:

- dashboards
- job runners
- multi-step setup flows
- streaming status views

Prefer `Live` only when evolving state matters. Static output usually easier to debug and copy.

## Markup Guardrails

- prefer Rich markup over raw ANSI escapes
- escape or disable markup for untrusted user content
- keep styles purposeful; too much color hurts readability
- use color to signal meaning, not decoration

## Good CLI Defaults

- success output short and calm
- failures explicit and actionable
- progress output transient when possible
- final summaries compact
- important identifiers copyable without stripping decorations