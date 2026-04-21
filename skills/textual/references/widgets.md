# Textual Widgets

## Common Display Widgets

Use:

- `Label` or `Static` for visible text
- `Placeholder` for quick layout prototyping
- `Header` and `Footer` for common app shell structure

Keep displayed state easy to query and update.

## Input Widgets

Common choices:

- `Input` for single-line text
- `TextArea` for multi-line editing
- `Button` for explicit actions
- `Switch` for boolean toggles
- `Select`, `OptionList`, or list-like widgets when the interaction fits them

Use widget-specific messages instead of guessing internal state changes.

## Data Widgets

Use `DataTable` when:

- the surface is genuinely tabular
- keyboard navigation matters
- selection or sorting behavior should be explicit

Keep table ids and column setup stable if tests depend on them.

## Containers

Common containers:

- `Container`
- `Horizontal`
- `Vertical`
- `Grid`

Choose the container that matches the layout directly instead of piling on
extra wrappers.

## Custom Widgets

Create a custom widget when:

- markup repeats
- behavior belongs together
- the widget owns a small local state boundary

Good custom widgets:

- focused filter panel
- form section
- status card
- menu surface

Bad custom widgets:

- giant wrapper around half the app
- thin alias over one built-in widget with no real behavior

## Widget Messages

Prefer widget messages and events for coordination:

- `Button.Pressed`
- `Input.Changed`
- `Input.Submitted`
- widget-specific selection or change messages

This keeps interaction logic closer to the widget boundary and easier to test.
