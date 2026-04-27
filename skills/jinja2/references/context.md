# Jinja2 Context

## Context Depends on the Host

Available globals/helpers/objects vary by framework or host app.

Common patterns:

- page templates receive page or view model
- email templates receive document-like object plus helpers
- fragment templates receive only data needed for that swap target

## Keep Context Explicit

Prefer clear names:

- `user`
- `items`
- `errors`
- `form`
- `page`

Avoid large ambiguous context blobs when smaller explicit surface suffices.

## Formatting Helpers

If host provides formatting helpers for:

- dates
- currency
- translated strings
- localized numbers

prefer those over ad hoc formatting in templates.

## Translation

Use host translation helper for user-facing strings when available.

Keep translatable text stable and readable.

## Partial Context

For partials:

- pass only what fragment needs
- keep fragment self-explanatory
- keep ids and classes stable if htmx or Alpine depends on them

## Python Boundary

Move work back to Python when:

- data needs extra fetching
- formatting logic becomes non-trivial
- permissions or business rules decide whether content may appear
- template would otherwise perform repeated expensive lookups
