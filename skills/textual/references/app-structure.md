# Textual App Structure

## Basic Shape

```python
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class MyApp(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
```

Use `compose()` for structure and `on_mount()` for startup actions that need
mounted widgets.

## Lifecycle

Common lifecycle points:

- `compose()` for initial structure
- `on_mount()` for startup work that needs mounted widgets
- `mount()` for dynamic widget insertion

Keep lifecycle responsibilities clear so startup code does not drift into one
giant setup block.

## Widget Boundaries

Prefer:

- one widget per meaningful concern
- reusable child widgets for repeated UI pieces
- focused containers that own local state

Avoid:

- one giant `App` with all behavior
- hidden coupling through direct deep queries everywhere

## Reactive State

Use reactive attributes for UI-relevant state.

```python
from textual.reactive import reactive


class Counter(Widget):
    count = reactive(0)

    def watch_count(self, value: int) -> None:
        self.query_one("#value").update(str(value))
```

Good fits:

- selected item
- current page
- open or closed state
- filter text

Bad fits:

- large service objects
- opaque mutable blobs
- state that does not affect the UI

## Messages and Events

Use messages when child widgets need to communicate upward cleanly.

- child widget emits a message
- parent screen or app handles it
- state and side effects stay in the right owner

This scales better than reaching into unrelated widgets directly.

For smaller built-in interactions, use widget messages directly before inventing
custom event plumbing.

## Screens and Dialogs

Use screens when the interaction has its own lifecycle:

- dialog or confirm flow
- settings page
- wizard step
- modal picker

Keep screen responsibilities explicit:

- entry
- exit
- result or dismissal path

## State Ownership

A simple rule:

- widget owns local view state
- screen owns screen-level workflow
- app owns global navigation, services, and long-lived coordination

## Querying Widgets

Use ids and classes as stable boundaries:

```python
status = self.query_one("#status")
button = self.query_one("#save", Button)
buttons = self.query(".action")
```

Do not make code depend on incidental widget ordering if a clearer selector can
exist.
