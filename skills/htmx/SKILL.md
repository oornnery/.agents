---
name: htmx
description: htmx patterns for server-rendered applications. Covers hypermedia
  interactions, fragment responses, attributes, swap strategies, validation,
  OOB updates, and server-side patterns for Python apps using templates.
---

# htmx

Use this skill when the work is primarily htmx interactions, fragment
responses, or server-rendered HTML flows.

## Boundary

Use this skill for:

- `hx-*` attributes and interaction design
- fragment-oriented endpoints
- form validation and partial updates
- polling, infinite scroll, modal, and inline-edit flows
- OOB updates and HX response headers

Pair with:

- `design` when surface contracts and UI flows need cleanup
- `python` when request handlers, templates, and backend code are Python
- `security` when CSRF, auth, untrusted HTML, or unsafe headers are involved

## Reference Map

- `references/attributes.md` -- request, trigger, target, swap, history, sync,
  and indicator patterns
- `references/server-patterns.md` -- fragment endpoints, validation responses,
  OOB updates, HX headers, and template organization

## Assets

- `assets/search.html` -- a simple active-search surface using stable targets
- `assets/form.jinja` -- a server-rendered form fragment with validation and
  request-state feedback

## What Stays Here

Keep this file focused on the mental model and defaults.

- keep here: hypermedia-first rules, fragment boundaries, validation stance,
  and review cues
- move to refs: long attribute tables, detailed endpoint patterns, and deeper
  examples
- use assets for copyable template fragments when they are more useful than
  another inline snippet

## Core Defaults

- respond with HTML fragments for htmx surfaces; do not force JSON where HTML
  is the real contract
- let one route return a full page for normal requests and a fragment for
  `HX-Request` when that keeps the UI flow simple
- keep `hx-target` stable and boring; prefer ids or clear local selectors
- use `hx-swap` deliberately; default to `innerHTML`, use `outerHTML` only when
  replacing the full component boundary is clearer
- use `422` for validation fragments when the form is well-formed but invalid
- use OOB updates only when one action truly needs to refresh multiple surfaces
- keep Alpine for local UI state and htmx for server round-trips; do not make
  the page fight itself
- escape server-rendered content by default and include CSRF protection where
  relevant

## Fragment-Oriented Server Pattern

```python
from fastapi import Request


def is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request") == "true"
```

A common pattern:

- full page for direct navigation
- fragment for htmx requests
- shared template partials for repeated surfaces

## Validation Pattern

- validate on the server
- re-render the form or field fragment with errors
- keep field names and target ids stable
- return status codes that help debugging and review, not only happy-path HTML

For attribute details, load `references/attributes.md`.
For server patterns, load `references/server-patterns.md`.

## Guardrails

- do not return giant page-sized fragments for tiny interactions
- do not hide important navigation or state changes behind surprising swaps
- do not push every interaction into OOB updates
- do not trust inline JSON in `hx-headers` or `hx-vals` if the values come from
  untrusted sources
- do not mix complex client-side state management into a flow that should stay
  hypermedia-driven
- do not forget non-htmx fallback behavior for important navigation or form
  actions

## Review Focus

- check whether the response contract is HTML-first and stable
- check whether target and swap boundaries are clear
- check whether form validation returns useful fragment updates
- check whether history behavior is intentional
- check whether auth, CSRF, and escaping are handled safely
- check whether htmx is solving the interaction instead of recreating a client
  framework piecemeal
