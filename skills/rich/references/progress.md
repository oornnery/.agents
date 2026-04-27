# Rich Progress

## Status

Use `console.status()` for short-lived feedback around one op:

```python
with console.status('Loading data...'):
    ...
```

## Track

Use `track()` for single simple loop:

```python
from rich.progress import track

for item in track(items, description='Processing'):
    ...
```

## Progress

Use `Progress()` when:

- multiple tasks
- richer updates needed
- totals matter

Keep task descriptions short, meaningful.

## Live

Use `Live` when current state updates in place:

- dashboards
- queues
- long-running orchestration

Prefer static output unless live state materially improves UX.
