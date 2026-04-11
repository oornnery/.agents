---
name: htmx
description: HTMX 2.x patterns -- hx-* attributes, AJAX, OOB swaps, SSE, triggers,
  loading indicators, hypermedia-driven apps. Load when writing htmx attributes,
  server-side HTML fragments, or integrating htmx with JX/FastAPI.
---

# HTMX

Target: htmx 2.x. Servers respond with HTML fragments, not JSON.

## Key Attributes

- `hx-get/post/put/patch/delete` -- issue HTTP request (default trigger: click)
- `hx-target` -- where to place response (`this`, `closest <sel>`, `find <sel>`)
- `hx-swap` -- how to insert (`innerHTML`, `outerHTML`, `beforeend`, `afterend`,
  `delete`, `none`). Modifiers: `swap:Xms`, `scroll:top`, `transition:true`
- `hx-trigger` -- when to fire (`click`, `input changed delay:300ms`, `load`,
  `revealed`, `every 5s`, `from:<selector>`)
- `hx-boost` -- progressive enhancement: converts links/forms to AJAX
- `hx-indicator` -- show element during request (`.htmx-indicator` class)
- `hx-sync` -- coordinate requests (`abort`, `drop`, `replace`, `queue`)
- `hx-push-url` -- push URL to browser history
- `hx-select` -- select subset of response to swap
- `hx-preserve` -- keep element unchanged during swaps (needs stable `id`)
- `hx-confirm` -- confirmation dialog before request
- `hx-vals/hx-headers` -- add extra values/headers (JSON format)

## Patterns

### Active Search

```html
<input type="search" name="q"
  hx-get="/search"
  hx-trigger="input changed delay:300ms, search"
  hx-target="#results"
  hx-sync="this:abort" />
```

### Out-of-Band Updates

```html
<!-- Main response swapped into hx-target -->
<div id="main-content">Updated</div>
<!-- OOB: swapped by matching id -->
<span id="counter" hx-swap-oob="true">42</span>
```

### Infinite Scroll

```html
<div hx-get="/items?page=2" hx-trigger="revealed" hx-swap="afterend">...</div>
```

## Template Organization

Full page for direct navigation, partial for AJAX:

```python
if request.headers.get("HX-Request"):
    return render_template("_partial.html")  # prefix _ for partials
else:
    return render_template("full_page.html")
```

## Response Headers

`HX-Redirect`, `HX-Push-Url`, `HX-Reswap`, `HX-Retarget`, `HX-Trigger`,
`HX-Trigger-After-Swap`.

## Security

- Escape all user content server-side
- CSRF: `<body hx-headers='{"X-CSRF-Token": "{{ csrf_token }}"}'>`
- `htmx.config.selfRequestsOnly = true`
- `htmx.config.allowScriptTags = false`

## Events (2.x syntax)

`hx-on:click` for DOM events, `hx-on::after-swap` for htmx events (double colon).

## Guardrails

- Use `hx-sync="this:abort"` on search/typeahead inputs
- Use `input changed` not `keyup changed` (catches paste, autofill)
- Keep element IDs stable for CSS transitions and OOB swaps
- Use `hx-boost` for progressive enhancement before adding attributes
- Only named inputs are included in requests
- Extensions are separate packages in 2.x: `idiomorph`, `sse`, `ws`,
  `head-support`, `response-targets`, `preload`

## Related

- `skills/jx/SKILL.md` -- Jinja server-rendered components (pair with htmx)
