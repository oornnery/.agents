# Rich Progress

## Status

Use `console.status()` for short-lived feedback around one operation:

```python
with console.status('Loading data...'):
    ...
```

## Track

Use `track()` for a single simple loop:

```python
from rich.progress import track

for item in track(items, description='Processing'):
    ...
```

## Progress

Use `Progress()` when:

- there are multiple tasks
- you want richer updates
- totals matter

Keep task descriptions short and meaningful.

## Live

Use `Live` when the current state should update in place:

- dashboards
- queues
- long-running orchestration

Prefer static output unless live state materially improves the UX.
