# Jinja2 Context

## Context Depends on the Host

The available globals, helpers, and objects vary by framework or host app.

Common patterns:

- page templates receive a page or view model
- email templates receive a document-like object plus helper functions
- fragment templates receive only the data needed for that swap target

## Keep Context Explicit

Prefer clear names such as:

- `user`
- `items`
- `errors`
- `form`
- `page`

Avoid large ambiguous context blobs when a smaller explicit surface would do.

## Formatting Helpers

If the host app provides formatting helpers for:

- dates
- currency
- translated strings
- localized numbers

prefer those helpers over ad hoc formatting in templates.

## Translation

Use the host translation helper for user-facing strings when one exists.

Keep translatable text stable and readable.

## Partial Context

For partials:

- pass only what the fragment needs
- keep the fragment self-explanatory
- keep ids and classes stable if htmx or Alpine depends on them

## Python Boundary

Move work back to Python when:

- data needs extra fetching
- formatting logic becomes non-trivial
- permissions or business rules decide whether content may appear
- the template would otherwise perform repeated expensive lookups
