---
name: textual
description: Textual patterns for building and testing terminal UIs in Python.
  Covers app structure, widgets, layout, styling, bindings, focus, screens, and
  headless testing with `run_test()` and the Pilot API.
---

# Textual

Use when work is primarily Textual TUI, terminal workflow, or tests for Textual widgets and screens.

## Boundary

Use for:

- Textual app structure and widget composition
- layout and `.tcss` styling
- bindings, actions, focus, interactive behavior
- screens, dialogs, menus, drawers, navigation flows
- headless functional testing with `run_test()`

Pair with:

- `python` for general Python conventions, typing, project workflow
- `rich` when renderables, terminal formatting, or console UX matter outside TUI
- `quality` when interaction regressions or state bugs need stronger tests

## Reference Map

- `references/app-structure.md` -- app shape, widgets, reactivity, messages, screens, state boundaries
- `references/widgets.md` -- common widgets, tables, forms, containers, custom widget guidance
- `references/widget-development.md` -- custom widget patterns: base class selection, composition, lifecycle, advanced compositions
- `references/layout-and-styling.md` -- `.tcss`, containers, layout, spacing, ids, classes, visual structure, themes, colors
- `references/reactive-programming.md` -- reactive attrs, watchers, computed props, valid, complex state, `recompose`
- `references/interactivity.md` -- bindings, actions, focus, mouse and keyboard handling, interaction patterns
- `references/testing.md` -- headless tests, full Pilot API, resize, animations, workers, assert patterns for complex widgets

## Assets

- `assets/app.py` -- small Textual app with bindings, dialog-like screen, stable selectors for tests
- `assets/app.tcss` -- matching `.tcss` file for example app
- `assets/test_app.py` -- headless functional tests using `run_test()`

## What Stays Here

Keep this file focused on defaults and guardrails.

- keep here: app design defaults, testing stance, review cues
- move to refs: widget catalogs, long examples, styling details, specific test recipes
- use assets for copyable app and test skeletons over growing giant code blocks in refs

## Core Defaults

- widgets small, responsibility-driven
- styling in `.tcss`, not large inline CSS strings
- semantic ids/classes so tests and styles have stable targets
- reactive state only for values that genuinely affect UI
- watchers small, explicit; heavy logic out of `watch_*` methods
- prefer `action_*` + `BINDINGS` for keyboard behavior
- messages/events explicit; no smuggling state through globals
- screens or focused containers for dialog-like flows, not one giant app class
- stable widget ids/classes so styling, querying, tests align
- prefer built-in widgets/messages before inventing custom abstractions
- test interactions headlessly with `run_test()` over only checking impl details
- always call `super().__init__(name=name, id=id, classes=classes)` in custom widget `__init__`
- replace list/dict entirely to trigger watchers -- `.append()` won't fire `watch_*`
- frozen dataclasses for immutable reactive data points

## Quick Start

```python
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label


class DemoApp(App):
    CSS_PATH = "app.tcss"
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Hello, Textual!", id="status")
        yield Footer()


if __name__ == "__main__":
    DemoApp().run()
```

## Testing Defaults

- use `async with app.run_test() as pilot:` for functional tests
- call `await pilot.pause()` after interactions that queue updates
- use `await pilot.wait_for_animation()` when animation timing matters
- use `await pilot.wait_for_scheduled_animations()` for all scheduled animations
- use `await pilot.app.workers.wait_for_complete()` for worker-driven flows
- assert both user-visible state and underlying app state when useful
- configure pytest with `asyncio_mode = "auto"` -- avoids `@pytest.mark.asyncio` on every test
- use `pilot.app.query_one("#id", WidgetType)` for typed querying
- test different terminal sizes with `run_test(size=(w, h))`

For deeper patterns, load `references/testing.md`.

## Reactive Defaults

- declare type: `attr: reactive[Type] = reactive(default)`
- use `init=False` when initializing in `__init__`; omit when reactive sets default
- use `recompose=True` when attribute change should rebuild child widget tree
- use `layout=True` when attribute change affects size/position
- watcher signature: `watch_attr(self, old: T, new: T) -> None`
- computed: use `@property` for derived values; update via watcher when dependency changes
- for valid: constrain in `watch_*`, revert or clamp value there

For full patterns, load `references/reactive-programming.md`.

## Widget Development Defaults

- extend `Static` for display-only content; extend `Container`/`Vertical`/`Horizontal` for composition
- put `DEFAULT_CSS` on class for self-contained defaults
- use keyword-only args (after `*`) for `id`, `name`, `classes`
- always pass `name`, `id`, `classes` to `super().__init__()`
- store config in `_prefixed` instance vars; never in class vars that aren't `ClassVar`
- custom messages: define as nested class; use `post_message()` from child, handle in parent
- messages flow UP -- parents handle, children emit; attributes flow DOWN -- parents set child attrs

For deep patterns, load `references/widget-development.md`.

- do not bury most of app in one monolithic `App` class
- do not rely on fragile widget order when ids or classes can make tests stable
- do not mix layout, styling, and interaction logic into same method
- do not overuse reactivity for one-off imperative updates
- do not make keyboard shortcuts undocumented or inconsistent with visible UI
- do not write Textual tests that only assert internal methods were called

## Review Focus

- widget boundaries clear, reusable
- layout and styling targets stable
- bindings and actions discoverable, consistent
- dialogs, menus, drawers have sensible focus and close behavior
- tests cover real interaction flows, not only internal state
