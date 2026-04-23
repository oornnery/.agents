# Textual Layout and Styling

## Styling Defaults

- keep styles in `.tcss`
- use ids for unique surfaces, classes for reusable states
- avoid deeply nested containers; prefer grid or horizontal/vertical when clear

## Common Layout Choices

### Vertical

```css
Screen {
    layout: vertical;
}
```

### Horizontal

```css
#toolbar {
    layout: horizontal;
}
```

### Grid

```css
#content {
    layout: grid;
    grid-size: 2 2;
    grid-columns: 1fr 2fr;
    grid-rows: auto 1fr;
}
```

Use grid when screen has genuine regions. Don't force grid for simple stacks.

## Sizing and Spacing

Use explicit spacing for predictable structure:

```css
.panel {
    padding: 1 2;
    margin: 1;
    border: round $accent;
}
```

Prefer stable container widths/heights for key panels:

- sidebars
- drawers
- status bars
- dialogs

## Semantic Selectors

Prefer selectors like:

- `#sidebar`
- `#status-bar`
- `.action`
- `.selected`
- `.danger`

Avoid selectors reflecting accidental structure over meaning.

## Pseudo-classes

Use hover/focus states intentionally:

```css
Button:hover {
    background: $accent;
}

Button:focus {
    border: round $accent;
}
```

Matters for usability and tests needing visible interaction state.

## Dialog and Drawer Layout

For dialogs:

- center surface
- clear primary action
- sensible focus landing

For drawers/side panels:

- visually distinct open/closed states
- clear dismissal behavior
- stable content area when possible

## Guardrails

- don't over-style every widget individually; use classes
- don't hide important layout in inline styles
- don't let ids/classes drift between code, styles, tests