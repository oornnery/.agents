# Textual Layout and Styling

## Styling Defaults

- keep styles in `.tcss`
- use ids for unique surfaces and classes for reusable states
- keep layout readable; avoid deeply nested containers when one clear grid or
  horizontal/vertical container would do

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

Use grid when the screen genuinely has regions. Do not force grid for simple
stacks.

## Sizing and Spacing

Use explicit spacing to make structure predictable:

```css
.panel {
    padding: 1 2;
    margin: 1;
    border: round $accent;
}
```

Prefer stable container widths and heights for key panels like:

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

Avoid selectors that reflect accidental structure rather than meaning.

## Pseudo-classes

Use hover and focus states intentionally:

```css
Button:hover {
    background: $accent;
}

Button:focus {
    border: round $accent;
}
```

This matters for usability and for tests that need visible interaction state.

## Dialog and Drawer Layout

For dialogs:

- center the surface
- keep a clear primary action
- ensure focus lands somewhere sensible

For drawers or side panels:

- keep open and closed states visually distinct
- make dismissal behavior clear
- keep the content area stable when possible

## Guardrails

- do not over-style every widget individually when a class can carry the rule
- do not make important layout behavior depend on hidden inline styles
- do not let ids and classes drift between code, styles, and tests
