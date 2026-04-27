# Textual Widgets

## Common Display Widgets

Use:

- `Label` or `Static` for visible text
- `Placeholder` for quick layout prototyping
- `Header` and `Footer` for app shell structure

Keep displayed state queryable, updatable.

## Input Widgets

Common choices:

- `Input` for single-line text
- `TextArea` for multi-line editing
- `Button` for explicit actions
- `Switch` for boolean toggles
- `Select`, `OptionList`, or list-like widgets when interaction fits

Use widget-specific messages over guessing internal state changes.

## Data Widgets

Use `DataTable` when:

- surface is genuinely tabular
- keyboard navigation matters
- selection or sorting should be explicit

```python
table = self.query_one("#my-table", DataTable)
table.add_column("Name", width=20)
table.add_column("Value", width=10)
table.add_row("Alice", "42")
```

Keep table ids and column setup stable if tests depend on them.

## Containers

| container             | layout                                      |
| --------------------- | ------------------------------------------- |
| `Vertical`            | children stacked top to bottom              |
| `Horizontal`          | children side by side                       |
| `Grid`                | grid layout with `grid-size`, `grid-gutter` |
| `Container`           | generic, layout via CSS                     |
| `ScrollableContainer` | container with overflow scroll              |

Choose container matching layout directly, not piling extra wrappers.

Context manager syntax for nesting:

```python
with Horizontal(classes="controls"):
    yield Button("Save", id="btn-save")
    yield Button("Cancel", id="btn-cancel")
```

## Custom Widgets

Create custom widget when:

- markup repeats
- behavior belongs together
- widget owns small local state boundary

Good custom widgets:

- focused filter panel
- form section
- status card
- menu surface

Bad custom widgets:

- giant wrapper around half app
- thin alias over one built-in widget with no real behavior

See `references/widget-development.md` for detailed patterns.

## Widget Messages

Prefer widget messages and events for coordination:

- `Button.Pressed`
- `Input.Changed`
- `Input.Submitted`
- widget-specific selection or change messages

Keeps interaction logic near widget boundary, easier to test.

## Widget Variants

`Button` and other widgets accept `variant`:

```python
Button("Save", variant="primary")
Button("Delete", variant="error")
Button("Info", variant="default")
```

Built-in variants: `default`, `primary`, `success`, `warning`, `error`.

## Updating Widget Content

```python
# Static/Label -- call update()
self.query_one("#status", Static).update("Done")

# Input -- set .value directly
self.query_one("#name", Input).value = "Alice"

# DataTable -- use table methods
table = self.query_one("#tbl", DataTable)
table.add_row("col1", "col2")
table.clear()
```
