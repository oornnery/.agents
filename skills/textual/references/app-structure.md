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

Use `compose()` for structure, `on_mount()` for startup actions needing mounted widgets.

## Lifecycle

- `compose()` for initial structure
- `on_mount()` for startup work needing mounted widgets
- `mount()` for dynamic widget insertion

Keep lifecycle responsibilities clear. Avoid drifting startup code into one giant setup block.

## Widget Boundaries

Prefer:

- one widget per meaningful concern
- reusable child widgets for repeated UI pieces
- focused containers owning local state

Avoid:

- one giant `App` with all behavior
- hidden coupling via direct deep queries

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
- open/closed state
- filter text

Bad fits:

- large service objects
- opaque mutable blobs
- state not affecting UI

## Messages and Events

Use messages when child widgets communicate upward cleanly.

- child emits message
- parent screen/app handles it
- state + side effects stay in right owner

Scales better than reaching into unrelated widgets directly. Use built-in widget messages for smaller interactions before inventing custom event plumbing.

## Screens and Dialogs

Use screens when interaction has own lifecycle:

- dialog or confirm flow
- settings page
- wizard step
- modal picker

Keep screen responsibilities explicit:

- entry
- exit
- result or dismissal path

## State Ownership

- widget owns local view state
- screen owns screen-level workflow
- app owns global navigation, services, long-lived coordination

## Querying Widgets

Use ids and classes as stable boundaries:

```python
status = self.query_one("#status")
button = self.query_one("#save", Button)
buttons = self.query(".action")
```

Don't depend on incidental widget ordering when a clearer selector exists.