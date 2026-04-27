# Rich Logging

## RichHandler

Use `RichHandler` when logs part of interactive CLI experience.

```python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level='INFO',
    format='%(message)s',
    handlers=[RichHandler(rich_tracebacks=True)],
)
```

## Tracebacks

Rich tracebacks useful for:

- local developer tools
- operator-facing CLIs
- internal automation

Keep prod-safe error messaging separate from verbose tracebacks when audience not purely technical.

## stderr

Send actionable failures to stderr:

- missing config
- invalid input
- failed external commands

Keep stdout clean when output might be piped.

## Guardrails

- do not treat Rich as replacement for good log structure
- do not hide important failure details behind too much styling
