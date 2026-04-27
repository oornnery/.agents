# Textual Reactive Programming

## Declaration

```python
from textual.reactive import reactive

class MyWidget(Static):
    # Basic
    count: reactive[int] = reactive(0)
    # init=False: caller initializes in __init__
    status: reactive[str] = reactive("idle", init=False)
    # recompose=True: rebuilds compose() when changed
    items: reactive[list[str]] = reactive(list, recompose=True)
    # layout=True: triggers relayout when changed
    visible_rows: reactive[int] = reactive(10, layout=True)
```

**Options:**

| param            | effect                      |
| ---------------- | --------------------------- |
| `init=False`     | must set in `__init__`      |
| `recompose=True` | calls `compose()` on change |
| `layout=True`    | triggers layout pass        |
| `bindings=True`  | refreshes footer bindings   |

Always declare with type: `attr: reactive[Type]`.

## Watchers

Auto-called after value change, before next render:

```python
def watch_status(self, old_value: str, new_value: str) -> None:
    # side effects, cascading updates, validation
    self.refresh()  # usually not needed -- reactive triggers it
```

Rules:

- signature: `watch_{attr}(self, old: T, new: T) -> None`
- called BEFORE re-render
- revert/clamp here for valid
- use for side effects or cascading reactive updates

## Mutation Rule

Replace object -- mutations on lists/dicts don't fire watchers:

```python
# CORRECT: triggers watch_items
self.items = self.items + [new_item]

# WRONG: won't trigger watch_items
self.items.append(new_item)
```

Same for dicts: `self.data = {**self.data, "key": val}`.

## Computed Properties

Derived from multiple reactive attrs:

```python
first_name: reactive[str] = reactive("John", init=False)
last_name: reactive[str] = reactive("Doe", init=False)

@property
def full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"

def watch_first_name(self, old: str, new: str) -> None:
    self.refresh()

def watch_last_name(self, old: str, new: str) -> None:
    self.refresh()
```

`@property` for simple derivation. Secondary reactive + watcher chain for complex derived state.

## Validation Pattern

```python
value: reactive[int] = reactive(0)

def watch_value(self, old: int, new: int) -> None:
    if new < 0:
        self.value = 0  # clamp to min
    elif new > 100:
        self.value = 100  # clamp to max
```

## Complex State

Group related attrs; use immutable data:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class DataPoint:
    value: float
    timestamp: str

class StatsWidget(Static):
    data: reactive[list[DataPoint]] = reactive(list, init=False)
    total: reactive[float] = reactive(0.0)
    loading: reactive[bool] = reactive(False)
    error: reactive[str | None] = reactive(None)
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.data = []
    def watch_data(self, old: list[DataPoint], new: list[DataPoint]) -> None:
        self.total = sum(p.value for p in new)
        self.error = None
    async def load(self) -> None:
        self.loading = True
        try:
            # fetch...
            self.data = [DataPoint(1.0, "2024-01-01")]
        except Exception as e:
            self.error = str(e)
        finally:
            self.loading = False
```

**Pattern:** `loading -> fetch -> data -> watch_data computes totals -> render`.

## Async Workers + Reactive

```python
from textual import work

class WorkerWidget(Widget):
    result: reactive[str | None] = reactive(None)
    @work
    async def fetch(self) -> None:
        data = await some_async_call()
        self.result = data  # triggers watcher safely from worker thread
    def on_mount(self) -> None:
        self.fetch()
```

`@work` for async ops that set reactive state -- thread-safe.

## Bindings Refresh

```python
class MyApp(App):
    page: reactive[int] = reactive(0, bindings=True)
    def check_action(self, action: str, parameters: tuple) -> bool | None:
        if action == "next" and self.page == MAX:
            return None  # dims footer binding
        return True
```

`bindings=True` re-evaluates `check_action` whenever `page` changes.
