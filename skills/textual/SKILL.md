---
name: textual
description: Textual patterns for building and testing terminal UIs in Python.
  Covers app structure, widgets, layout, styling, bindings, focus, screens, and
  headless testing with `run_test()` and the Pilot API.
---

# Textual

Use this skill when the work is primarily a Textual TUI, a terminal workflow,
or tests for Textual widgets and screens.

## Boundary

Use this skill for:

- Textual app structure and widget composition
- layout and `.tcss` styling
- bindings, actions, focus, and interactive behavior
- screens, dialogs, menus, drawers, and navigation flows
- headless functional testing with `run_test()`

Pair with:

- `python` for general Python conventions, typing, and project workflow
- `rich` when renderables, terminal formatting, or console UX matter outside
  the TUI itself
- `quality` when interaction regressions or state bugs need stronger tests

## Reference Map

- `references/app-structure.md` -- app shape, widgets, reactivity, messages,
  screens, and state boundaries
- `references/widgets.md` -- common widgets, tables, forms, containers, and
  custom widget guidance
- `references/layout-and-styling.md` -- `.tcss`, containers, layout, spacing,
  ids, classes, and visual structure
- `references/interactivity.md` -- bindings, actions, focus, mouse and
  keyboard handling, and common interaction patterns
- `references/testing.md` -- headless tests, Pilot API, resize, animations,
  workers, and assert patterns for complex widgets

## Assets

- `assets/app.py` -- a small Textual app with bindings, a dialog-like screen,
  and stable selectors for tests
- `assets/app.tcss` -- the matching `.tcss` file for the example app
- `assets/test_app.py` -- headless functional tests using `run_test()`

## What Stays Here

Keep this file focused on defaults and guardrails.

- keep here: app design defaults, testing stance, and review cues
- move to refs: widget catalogs, long examples, styling details, and specific
  test recipes
- use assets for copyable app and test skeletons instead of growing giant code
  blocks in the refs

## Core Defaults

- keep widgets small and responsibility-driven
- keep styling in `.tcss` instead of large inline CSS strings
- use semantic ids and classes so tests and styles have stable targets
- use reactive state only for values that genuinely affect the UI
- keep watchers small and explicit; move heavy logic out of `watch_*` methods
- prefer `action_*` plus `BINDINGS` for keyboard behavior
- keep messages and events explicit instead of smuggling state through globals
- use screens or focused containers for dialog-like flows rather than one giant
  app class
- use stable widget ids and classes so styling, querying, and tests align
- prefer built-in widgets and messages before inventing a custom abstraction
- test interactions headlessly with `run_test()` instead of only checking
  implementation details

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
- use `await pilot.app.workers.wait_for_complete()` for worker-driven flows
- assert both user-visible state and underlying app state when useful

For deeper patterns, load `references/testing.md`.

## Guardrails

- do not bury most of the app in one monolithic `App` class
- do not rely on fragile widget order when ids or classes can make tests stable
- do not mix layout, styling, and interaction logic into the same method
- do not overuse reactivity for one-off imperative updates
- do not make keyboard shortcuts undocumented or inconsistent with visible UI
- do not write Textual tests that only assert internal methods were called

## Review Focus

- check whether widget boundaries are clear and reusable
- check whether layout and styling targets are stable
- check whether bindings and actions are discoverable and consistent
- check whether dialogs, menus, and drawers have sensible focus and close
  behavior
- check whether tests cover real interaction flows, not only internal state
