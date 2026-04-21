# htmx Server Patterns

## Full Page vs Fragment

For important routes, let the server support both:

- full page for direct navigation
- fragment for `HX-Request`

```python
from fastapi import Request


def is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request") == "true"
```

This keeps:

- refresh and deep links working
- server rendering as the source of truth
- partial UI flows easy to reason about

## Template Organization

A simple pattern:

```text
templates/
  users/
    page.jinja
    partials/
      _table.jinja
      _row.jinja
      _form.jinja
      _errors.jinja
```

Use full-page templates for navigation and smaller partials for swaps.

## Form Validation

For invalid input:

- return the form fragment again
- preserve entered values
- show field or form errors
- use `422` when the request shape is valid but the content is not

This makes validation:

- inspectable in tests
- easier to reason about in logs
- less magical than hidden client-side rules

## Response Headers

Useful HX headers:

- `HX-Redirect`
- `HX-Location`
- `HX-Push-Url`
- `HX-Replace-Url`
- `HX-Trigger`
- `HX-Trigger-After-Swap`
- `HX-Retarget`
- `HX-Reswap`

Use them sparingly and intentionally. Prefer template-driven flows first.

## OOB Update Pattern

Good fit:

- create one row and also update count or flash area

```html
<tr id="user-{{ user.id }}">
  ...
</tr>

<div id="flash" hx-swap-oob="true">User created</div>
<span id="user-count" hx-swap-oob="true">{{ total }}</span>
```

Bad fit:

- turning every response into many unrelated UI updates

## Inline Field Validation

Use field-level validation when it genuinely helps the form flow.

```html
<input
  name="email"
  hx-post="/users/validate-email"
  hx-trigger="blur changed"
  hx-target="next .validation"
>
<span class="validation"></span>
```

Keep the server response small and specific.

## Error Handling

Use status codes that match the failure:

- `200` for successful fragment refresh
- `201` for created resources when the distinction matters
- `204` for actions with no swap body
- `401` and `403` for auth boundaries
- `404` for missing resources
- `409` for state conflicts
- `422` for semantic validation failures

Keep error fragments readable. Do not leak stack traces or sensitive details
into HTML responses.

## Security Rules

- escape template output by default
- include CSRF tokens for state-changing requests
- validate permissions on fragment endpoints the same way you would for full
  routes
- do not trust hidden fields as authorization signals
- do not assume htmx requests are safer than any other request

## Review Focus

- check whether full-page and fragment behaviors stay consistent
- check whether partials map to stable UI boundaries
- check whether headers and OOB updates are intentional, not incidental
- check whether validation and auth responses remain understandable when
  requested asynchronously
