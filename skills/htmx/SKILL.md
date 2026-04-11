---
name: htmx
description: HTMX 2.x patterns -- hx-* attributes, AJAX, OOB swaps, SSE, triggers,
  loading indicators, hypermedia-driven apps. Load when writing htmx attributes,
  server-side HTML fragments, or integrating htmx with JX/FastAPI.
---

# HTMX

Target: htmx 2.x. Servers respond with HTML fragments, not JSON.

## Core Philosophy

htmx extends HTML to handle AJAX, CSS transitions, WebSockets, and SSE
directly from attributes. The server controls application state; the
browser renders HTML.

## Core Attributes

| Attribute   | Purpose              | Default Trigger      |
| ----------- | -------------------- | -------------------- |
| `hx-get`    | Issue GET request    | click                |
| `hx-post`   | Issue POST request   | click (form: submit) |
| `hx-put`    | Issue PUT request    | click                |
| `hx-patch`  | Issue PATCH request  | click                |
| `hx-delete` | Issue DELETE request | click                |

## Key Attributes

- `hx-target` -- where to place response (`this`, `closest <sel>`,
  `next <sel>`, `find <sel>`)
- `hx-swap` -- how to insert (`innerHTML`, `outerHTML`, `beforeend`,
  `afterend`, `delete`, `none`). Modifiers: `swap:Xms`, `settle:Xms`,
  `scroll:top`, `transition:true`
- `hx-trigger` -- when to fire (`click`, `input changed delay:300ms`,
  `load`, `revealed`, `every 5s`, `from:<selector>`)
- `hx-boost` -- progressive enhancement: converts links/forms to AJAX
- `hx-indicator` -- show element during request (`.htmx-indicator` class)
- `hx-disabled-elt` -- disable elements during request
- `hx-confirm` -- confirmation dialog before request
- `hx-sync` -- coordinate requests (`abort`, `drop`, `replace`, `queue`)
- `hx-push-url` -- push URL to browser history
- `hx-select` -- select subset of response to swap
- `hx-include` -- include additional element values
- `hx-vals` -- add extra values to request (JSON)
- `hx-headers` -- add custom headers (JSON)
- `hx-preserve` -- keep element unchanged during swaps (needs stable `id`)

## Common Patterns

### Active Search

```html
<input type="search" name="q"
  hx-get="/search"
  hx-trigger="input changed delay:300ms, search"
  hx-target="#results"
  hx-sync="this:abort" />
```

### Out-of-Band Updates

Server response updates multiple elements simultaneously:

```html
<div id="main-content">Updated content</div>
<div id="notification" hx-swap-oob="true">New notification!</div>
<span id="counter" hx-swap-oob="true">42</span>
```

### Loading Indicator

```html
<button hx-get="/data" hx-indicator="#spinner" hx-disabled-elt="this">
  Load <span id="spinner" class="htmx-indicator">...</span>
</button>
```

### Infinite Scroll

```html
<div hx-get="/items?page=2" hx-trigger="revealed" hx-swap="afterend">
  Loading...
</div>
```

## Template Organization

Serve full page for direct navigation, partial fragment for AJAX:

```python
if request.headers.get("HX-Request"):
    return render_template("_partial.html")
else:
    return render_template("full_page.html")
```

Convention: prefix partials with `_` (`_search_results.html`).

## Server Response Headers

| Header                  | Purpose                    |
| ----------------------- | -------------------------- |
| `HX-Redirect`           | Full page redirect         |
| `HX-Push-Url`           | Push URL to history        |
| `HX-Reswap`             | Override hx-swap value     |
| `HX-Retarget`           | Override hx-target value   |
| `HX-Trigger`            | Trigger client-side events |
| `HX-Trigger-After-Swap` | Trigger after swap         |

## Security

- Escape all user content server-side (prevent XSS)
- Include CSRF tokens: `<body hx-headers='{"X-CSRF-Token": "{{ csrf_token }}"}'>`
- `htmx.config.selfRequestsOnly = true` (restrict request origins)
- `htmx.config.allowScriptTags = false` (disable script processing)
- Use `hx-disable` on untrusted content

## Events (htmx 2.x syntax)

```html
<button hx-get="/data"
  hx-on::before-request="console.log('Starting...')"
  hx-on::after-swap="console.log('Done!')">
  Load
</button>
```

Note: `hx-on:click` for DOM events, `hx-on::after-swap` for htmx events
(double colon).

## Extensions

Loaded as separate packages in htmx 2.x: `idiomorph` (morph swaps),
`sse` (Server-Sent Events), `ws` (WebSockets), `head-support`,
`response-targets` (target by HTTP status), `preload`.

## Guardrails

- Always use `hx-sync="this:abort"` on search/typeahead inputs
- Use `input changed` not `keyup changed` (catches paste, autofill)
- Keep element IDs stable for CSS transitions and OOB swaps
- Use `hx-boost` for progressive enhancement before adding attributes
- Forms: only named inputs are included in requests
- Use `hx-on:` syntax (not `hx-on="..."`) in htmx 2.x

## Related

- `skills/jx/SKILL.md` -- Jinja server-rendered components (pair with htmx)
- `skills/frontend/SKILL.md` -- Tailwind, Solid for client-heavy UIs
