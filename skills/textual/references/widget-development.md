# Textual Widget Development

## Choose Base Class

| base                                    | when                                         |
| --------------------------------------- | -------------------------------------------- |
| `Static`                                | display-only, renders string/Rich renderable |
| `Container` / `Vertical` / `Horizontal` | composition -- holds child widgets           |
| `Widget`                                | fully custom rendering + composition         |
| built-in (`Button`, `Input`, etc.)      | use first, before custom                     |

## Minimal Custom Widget

```python
from textual.app import ComposeResult
from textual.widgets import Static

class StatusCard(Static):
    DEFAULT_CSS = """
    StatusCard {
        height: auto;
        border: solid $primary;
        padding: 1;
    }
    """
    def __init__(self, label: str, *, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name=name, id=id, classes=classes)  # always pass through
        self._label = label
    def render(self) -> str:
        return self._label
```

Rules:

- keyword-only args after `*` for `name`, `id`, `classes`
- always pass `name`, `id`, `classes` to `super().__init__()`
- store config in `_prefixed` instance vars

## Composition Widget

```python
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button, Label

class UserCard(Vertical):
    DEFAULT_CSS = """
    UserCard {
        height: auto;
        border: solid $primary;
        padding: 1;
    }
    UserCard .header {
        background: $boost;
        text-style: bold;
    }
    UserCard .controls {
        height: 3;
        border-top: solid $primary;
    }
    """
    def __init__(self, name: str, email: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._name = name
        self._email = email
    def compose(self) -> ComposeResult:
        yield Static(self._name, classes="header")
        yield Label(self._email, id="email")
        with Horizontal(classes="controls"):
            yield Button("Edit", id="btn-edit")
            yield Button("Delete", id="btn-delete", variant="error")
```

## Widget Lifecycle

```python
class MyWidget(Widget):
    def on_mount(self) -> None:
        """Widget is mounted and ready. Query children here."""
        self.query_one("#title").update("Loaded")
    def on_unmount(self) -> None:
        """Widget being removed. Clean up resources."""
        pass
    def on_show(self) -> None:
        """Widget became visible."""
        pass
    def on_hide(self) -> None:
        """Widget became hidden."""
        pass
```

Use `on_mount` to query children (exist then). Not `__init__`.

## Messages (communication pattern)

Follow: **attributes down, messages up**.

```python
# Child emits
class SearchBox(Widget):
    class Submitted(Message):
        def __init__(self, query: str) -> None:
            super().__init__()
            self.query = query
    def action_submit(self) -> None:
        self.post_message(self.Submitted(self.query_one(Input).value))

# Parent handles
class MyApp(App):
    def on_search_box_submitted(self, message: SearchBox.Submitted) -> None:
        self.run_query(message.query)
```

Handler naming: `on_{widget_class}_{message_class}` (snake_case).

## Dynamic Composition

Mount/remove widgets after initial compose:

```python
# Add
await self.mount(Label("new item", classes="item"))

# Remove
await self.query_one("#old-item").remove()

# Replace contents
await self.query(".item").remove()
for item in new_items:
    await self.mount(Label(item, classes="item"))
```

Use `recompose=True` on reactive attr to auto-call `compose()` on change.

## Advanced: Dashboard Pattern

```python
class DashboardWidget(Vertical):
    DEFAULT_CSS = """
    DashboardWidget { height: 100%; border: solid $primary; }
    DashboardWidget .stats-grid { height: auto; grid-size: 3; grid-gutter: 1; padding: 1; }
    DashboardWidget .stat-card { height: 5; border: solid $accent; padding: 1; }
    DashboardWidget .chart-section { height: 1fr; border-top: solid $primary; }
    DashboardWidget .controls { height: 3; background: $surface; border-top: solid $primary; }
    """
    def compose(self) -> ComposeResult:
        yield Static(self._title, classes="header")
        with Grid(classes="stats-grid"):
            yield Static("Users: 0", classes="stat-card", id="stat-users")
            yield Static("Orders: 0", classes="stat-card", id="stat-orders")
            yield Static("Revenue: $0", classes="stat-card", id="stat-revenue")
        with Vertical(classes="chart-section"):
            yield DataTable(id="activity-table")
        with Horizontal(classes="controls"):
            yield Button("Refresh", id="btn-refresh", variant="primary")
            yield Button("Export", id="btn-export")
    async def on_mount(self) -> None:
        table = self.query_one("#activity-table", DataTable)
        table.add_column("Time", width=20)
        table.add_column("User", width=20)
        table.add_column("Action", width=40)
    def update_stats(self, users: int, orders: int, revenue: float) -> None:
        self.query_one("#stat-users", Static).update(f"Users: {users}")
        self.query_one("#stat-orders", Static).update(f"Orders: {orders}")
        self.query_one("#stat-revenue", Static).update(f"Revenue: ${revenue:.2f}")
```

## ClassVar vs Instance Var

```python
from typing import ClassVar

class MyWidget(Static):
    # Class-level constant -- shared across all instances
    BORDER_COLOR: ClassVar[str] = "$primary"
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        # Instance-level state -- unique per instance
        self._state: dict[str, str] = {}
```

## Testing Custom Widgets

```python
async def test_user_card() -> None:
    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield UserCard("Alice", "alice@example.com", id="card")
    async with TestApp().run_test() as pilot:
        card = pilot.app.query_one("#card", UserCard)
        assert card._name == "Alice"
        await pilot.click("#btn-edit")
        await pilot.pause()
        # assert expected behavior
```
