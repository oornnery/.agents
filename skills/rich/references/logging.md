# Rich Logging

## RichHandler

Use `RichHandler` when logs are part of the interactive CLI experience.

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

Rich tracebacks are useful for:

- local developer tools
- operator-facing CLIs
- internal automation

Keep production-safe error messaging separate from verbose tracebacks when the
audience is not purely technical.

## stderr

Send actionable failures to stderr:

- missing config
- invalid input
- failed external commands

Keep stdout clean when output might be piped.

## Guardrails

- do not treat Rich as a replacement for good log structure
- do not hide important failure details behind too much styling
