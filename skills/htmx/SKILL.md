---
name: htmx
description: htmx patterns for server-rendered applications. Covers hypermedia
  interactions, fragment responses, attributes, swap strategies, validation,
  OOB updates, and server-side patterns for Python apps using templates.
---

# htmx

Use skill when work primarily htmx interactions, fragment responses, or server-rendered HTML flows.

## Boundary

Use for:

- `hx-*` attributes and interaction design
- fragment-oriented endpoints
- form valid and partial updates
- polling, infinite scroll, modal, and inline-edit flows
- OOB updates and HX response headers

Pair with:

- `design` when surface contracts and UI flows need cleanup
- `python` when request handlers, templates, and backend code are Python
- `security` when CSRF, auth, untrusted HTML, or unsafe headers involved

## Reference Map

- `references/attributes.md` -- request, trigger, target, swap, history, sync, indicator patterns
- `references/server-patterns.md` -- fragment endpoints, valid responses, OOB updates, HX headers, template organization

## Assets

- `assets/search.html` -- simple active-search surface using stable targets
- `assets/form.jinja` -- server-rendered form fragment with valid and request-state feedback

## What Stays Here

Keep focused on mental model and defaults.

- keep here: hypermedia-first rules, fragment boundaries, valid stance, review cues
- move to refs: long attribute tables, detailed endpoint patterns, deeper examples
- use assets for copyable template fragments when more useful than another inline snippet

## Core Defaults

- respond with HTML fragments for htmx surfaces; do not force JSON where HTML is real contract
- let one route return full page for normal requests and fragment for `HX-Request` when that keeps UI flow simple
- keep `hx-target` stable and boring; prefer ids or clear local selectors
- use `hx-swap` deliberately; default `innerHTML`, use `outerHTML` only when replacing full component boundary is clearer
- use `422` for valid fragments when form well-formed but invalid
- use OOB updates only when one action truly needs to refresh multiple surfaces
- keep Alpine for local UI state, htmx for server round-trips; do not make page fight itself
- escape server-rendered content by default; include CSRF protection where relevant

## Fragment-Oriented Server Pattern

```python
from fastapi import Request


def is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request") == "true"
```

Common pattern:

- full page for direct navigation
- fragment for htmx requests
- shared template partials for repeated surfaces

## Validation Pattern

- validate on server
- re-render form or field fragment with errors
- keep field names and target ids stable
- return status codes that help debugging and review, not only happy-path HTML

For attribute details, load `references/attributes.md`.
For server patterns, load `references/server-patterns.md`.

## Guardrails

- do not return giant page-sized fragments for tiny interactions
- do not hide important navigation or state changes behind surprising swaps
- do not push every interaction into OOB updates
- do not trust inline JSON in `hx-headers` or `hx-vals` if values come from untrusted sources
- do not mix complex client-side state management into flow that should stay hypermedia-driven
- do not forget non-htmx fallback behavior for important navigation or form actions

## Review Focus

- check response contract HTML-first and stable
- check target and swap boundaries clear
- check form valid returns useful fragment updates
- check history behavior intentional
- check auth, CSRF, and escaping handled safely
- check htmx solving interaction over recreating client framework piecemeal
