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

## pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"   # no @pytest.mark.asyncio on each test
testpaths = ["tests"]
```

## Testing Rules

- keep tests `async def`
- interact through Pilot API where possible
- assert visible state, not only internals
- pause after interactions that queue updates
- wait for workers or animations when timing matters

## Complete Pilot API

### Mouse

```python
await pilot.click("#save")
await pilot.click(Button)               # by type
await pilot.click(offset=(40, 12))      # absolute coords
await pilot.click("#item", shift=True)
await pilot.click("#item", times=2)     # double-click
await pilot.double_click("#item")
await pilot.triple_click("#item")
await pilot.hover("#menu-item")
await pilot.mouse_down("#draggable")
await pilot.hover("#drop-target")
await pilot.mouse_up("#drop-target")
```

### Keyboard

```python
await pilot.press("enter")
await pilot.press("tab", "enter", "escape", "backspace")
await pilot.press("up", "down", "left", "right")
await pilot.press("ctrl+s", "ctrl+shift+p", "shift+tab")
await pilot.press(*"hello world")       # type a string
```

### Timing

```python
await pilot.pause()           # drain message queue
await pilot.pause(0.5)        # + extra 0.5s delay

await pilot.wait_for_animation()
await pilot.wait_for_scheduled_animations()
```

### App Control

```python
await pilot.exit(result={"status": "ok"})
await pilot.resize_terminal(120, 40)
await pilot.pause()   # propagate resize events
```

### Workers

```python
await pilot.app.workers.wait_for_complete()
```

## Querying

```python
button = pilot.app.query_one("#save")
button = pilot.app.query_one("#save", Button)  # typed
items = list(pilot.app.query(".menu-item"))
first = pilot.app.query(Button).first()
```

Use stable ids/classes so tests don't depend on incidental structure.

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

input_widget = pilot.app.query_one("#name", Input)
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
async with MyApp().run_test(size=(80, 24)) as pilot:
    assert pilot.app.size == (80, 24)
    await pilot.resize_terminal(120, 40)
    await pilot.pause()
    assert pilot.app.size == (120, 40)
```

### Responsive Layout (different sizes)

```python
async with app.run_test(size=(40, 20)) as pilot:
    assert not pilot.app.query_one("#sidebar").is_visible

async with app.run_test(size=(120, 40)) as pilot:
    assert pilot.app.query_one("#sidebar").is_visible
```

## Complex Control Pitfalls

| pitfall                       | fix                                           |
| ----------------------------- | --------------------------------------------- |
| assertion fails before update | `await pilot.pause()`                         |
| worker result not available   | `await pilot.app.workers.wait_for_complete()` |
| animation state varies        | `await pilot.wait_for_animation()`            |
| missing `async def`           | all test functions must be `async def`        |
| missing `await`               | all pilot methods are async                   |

assert pilot.app.size.width == 100

```text

### Widget Messages and Visible State

Prefer assertions showing user-facing result:

```python
status = pilot.app.query_one('#status', Label)
assert status.renderable == 'Saved'
```

Use internal state assertions only as supplement when they clarify ownership or workflow.

## Patterns for Complex Controls

### Dialogs and Screens

Test:

- open action
- visible dialog content
- focus lands inside dialog when expected
- `escape` or cancel closes it
- result or dismiss path updates parent screen correctly

### Menus and Drawers

Test:

- open/close transitions
- focused item after open
- arrow-key navigation
- click outside or `escape` when supported
- selected action updates visible state
- drawer width or visibility state when layout changes

### Sliders and Value Controls

Test:

- initial value
- keyboard change
- mouse or click change if supported
- visible label or status text stays in sync with underlying value

These patterns are the right place to extend later with concrete slider, dialog, and drawer asserts.

## Common Pitfalls

| Pitfall                            | Fix                        |
| ---------------------------------- | -------------------------- |
| assertion runs too early           | add `await pilot.pause()`  |
| worker-driven state missing        | wait for worker completion |
| animation-dependent state is flaky | wait for animation         |
| selectors are brittle              | add stable ids or classes  |
| test only checks internals         | assert visible state too   |

## Guardrails

- don't overuse sleep-like delays when `pause()`, worker waits, or animation waits suffice
- don't test Textual internals instead of your app behavior
- don't rely on random widget order when stable selectors can exist
