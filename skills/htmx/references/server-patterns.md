# htmx Server Patterns

## Full Page vs Fragment

Important routes support both:

- full page for direct navigation
- fragment for `HX-Request`

```python
from fastapi import Request


def is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request") == "true"
```

This keeps:

- refresh and deep links working
- server rendering as source of truth
- partial UI flows easy to reason about

## Template Organization

Simple pattern:

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

Use full-page templates for navigation, smaller partials for swaps.

## Form Validation

Invalid input:

- return form fragment again
- preserve entered values
- show field or form errors
- use `422` when request shape valid but content invalid

Makes valid:

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

Use sparingly and intentionally. Prefer template-driven flows first.

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

Use field-level valid when it genuinely helps form flow.

```html
<input
  name="email"
  hx-post="/users/validate-email"
  hx-trigger="blur changed"
  hx-target="next .validation"
>
<span class="validation"></span>
```

Keep server response small and specific.

## Error Handling

Use status codes matching failure:

- `200` successful fragment refresh
- `201` created resources when distinction matters
- `204` actions with no swap body
- `401` and `403` auth boundaries
- `404` missing resources
- `409` state conflicts
- `422` semantic valid failures

Keep error fragments readable. Do not leak stack traces or sensitive details into HTML responses.

## Security Rules

- escape template output by default
- include CSRF tokens for state-changing requests
- validate permissions on fragment endpoints same as full routes
- do not trust hidden fields as authorization signals
- do not assume htmx requests safer than any other request

## Review Focus

- check full-page and fragment behaviors stay consistent
- check partials map to stable UI boundaries
- check headers and OOB updates intentional, not incidental
- check valid and auth responses remain understandable when requested asynchronously
