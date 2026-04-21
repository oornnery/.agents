# Textual Testing

## Core Pattern

Use `run_test()` for functional tests.

```python
async def test_status_updates() -> None:
    app = MyApp()

    async with app.run_test() as pilot:
        await pilot.press("enter")
        await pilot.pause()

        status = pilot.app.query_one("#status")
        assert status.renderable == "Done"
```

## Testing Rules

- keep tests `async def`
- interact through the Pilot API when possible
- assert visible state, not only internal implementation
- pause after interactions that queue updates
- wait for workers or animations when timing matters

## Common Pilot Actions

```python
await pilot.click("#save")
await pilot.hover("#menu-item")
await pilot.double_click("#save")
await pilot.mouse_down("#drag-handle")
await pilot.mouse_up("#drop-target")
await pilot.press("tab", "enter", "escape")
await pilot.resize_terminal(120, 40)
await pilot.pause()
await pilot.wait_for_animation()
await pilot.wait_for_scheduled_animations()
await pilot.app.workers.wait_for_complete()
```

Use the smallest interaction that proves the behavior.

## Querying

```python
button = pilot.app.query_one("#save")
items = list(pilot.app.query(".menu-item"))
```

Use stable ids and classes so tests do not depend on incidental structure.

Query by type when that improves clarity:

```python
button = pilot.app.query_one('#save', Button)
```

## Assert Patterns

### Simple Widget State

```python
label = pilot.app.query_one("#status")
assert label.renderable == "Saved"
```

### Input State

```python
await pilot.click("#name")
await pilot.press(*"alice")
await pilot.pause()

input_widget = pilot.app.query_one("#name")
assert input_widget.value == "alice"
```

### Binding Behavior

```python
await pilot.press("ctrl+s")
await pilot.pause()
assert pilot.app.saved is True
```

### Worker Completion

```python
pilot.app.fetch_data()
await pilot.app.workers.wait_for_complete()
assert pilot.app.data is not None
```

### Resize

```python
await pilot.resize_terminal(100, 30)
await pilot.pause()
assert pilot.app.size.width == 100
```

### Widget Messages and Visible State

Prefer assertions that show the user-facing result:

```python
status = pilot.app.query_one('#status', Label)
assert status.renderable == 'Saved'
```

Use internal state assertions only as a supplement when they clarify ownership
or workflow.

## Patterns for Complex Controls

### Dialogs and Screens

Test:

- open action
- visible dialog content
- focus lands inside the dialog when expected
- `escape` or cancel closes it
- result or dismiss path updates the parent screen correctly

### Menus and Drawers

Test:

- open and close transitions
- focused item after open
- arrow-key navigation
- click outside or `escape` when supported
- selected action updates visible state
- drawer width or visibility state when the layout changes

### Sliders and Value Controls

Test:

- initial value
- keyboard change
- mouse or click change if supported
- visible label or status text stays in sync with the underlying value

These patterns are the right place to extend later with concrete slider,
dialog, and drawer asserts.

## Common Pitfalls

| Pitfall                            | Fix                        |
| ---------------------------------- | -------------------------- |
| assertion runs too early           | add `await pilot.pause()`  |
| worker-driven state missing        | wait for worker completion |
| animation-dependent state is flaky | wait for animation         |
| selectors are brittle              | add stable ids or classes  |
| test only checks internals         | assert visible state too   |

## Guardrails

- do not overuse sleep-like delays when `pause()`, worker waits, or animation
  waits are enough
- do not test Textual internals instead of your app behavior
- do not rely on random widget order when stable selectors can exist
