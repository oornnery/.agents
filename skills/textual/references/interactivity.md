# Textual Interactivity

## Bindings and Actions

Define keyboard behavior with `BINDINGS` and `action_*`.

```python
from textual.app import App


class MyApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+s", "save", "Save"),
    ]
    def action_save(self) -> None:
        self.notify("Saved")
```

Keep bindings:

- predictable
- discoverable
- aligned with visible UI behavior

If action availability changes with state, refresh bindings deliberately or use reactive state that updates them cleanly.

## Focus Rules

Focus behavior is part of UX, not afterthought.

Check:

- where focus starts
- how focus moves with `tab` and arrow keys
- whether dialogs and menus keep focus inside active surface when needed
- whether `escape` closes right surface

## Mouse and Keyboard Events

Use direct event handlers when bindings aren't right abstraction:

- clicks on custom widgets
- hover states
- drag-like interactions
- fine-grained key handling inside focused widgets

Keep event handlers small, delegate real work outward.

For focused widgets, prefer widget-specific handlers over one giant global `on_key`.

## Common Interaction Patterns

### Form Submit

- focus first field on open
- submit with enter when appropriate
- show valid near field or form summary
- keep status feedback visible

### Dialog

- open with clear action
- close with `escape`
- return focus to invoking control where possible
- keep confirm and cancel paths explicit

### Menu or Drawer

- keep open state visible
- support keyboard navigation
- support explicit close action and escape
- avoid trapping user in hidden state

### Slider or Value Control

- reflect value changes visibly
- support keyboard adjustment
- keep labels and units clear
- keep tests focused on displayed value and underlying state owner

## Notifications and Feedback

Use notifications or status areas for:

- save success
- failure feedback
- background work completion

Do not rely only on hidden state changes user cannot see.

## Guardrails

- do not scatter related bindings across many owners without clear priority
- do not let one action mutate far-away widgets directly when messages or state ownership would be cleaner
- do not make keyboard and mouse behavior disagree on same control
