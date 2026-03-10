# Integrations

This reference groups framework integration and browser interaction patterns:
FastAPI, Flask, Django, HTMX, and Alpine.js.

## FastAPI

FastAPI is a strong default pairing because route handlers can fetch data and
return rendered HTML directly.

Minimal setup:

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jx import Catalog

app = FastAPI()
catalog = Catalog("components", site_name="My App")


@app.get("/", response_class=HTMLResponse)
async def home():
    return catalog.render("pages/HomePage.jinja")
```

Recommended app structure:

```python
# app/components.py
from jx import Catalog

catalog = Catalog("components", site_name="Example")
```

```python
# app/routes/pages.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.components import catalog

router = APIRouter()


@router.get("/users", response_class=HTMLResponse)
async def users_page():
    users = await fetch_users()
    return catalog.render("pages/UsersPage.jinja", users=users)
```

Best practice: keep data fetching in Python and keep JX focused on rendering.

### Static Files for Component Assets

JX does not include middleware for serving component assets. Use FastAPI's
`StaticFiles` mount or a reverse proxy (nginx, Caddy) to serve CSS and JS
files from the component directories:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

For package assets, use `catalog.collect_assets("static/vendor")` at build
time and serve the output folder.

## Flask

Reuse Flask's Jinja environment when you want its filters and globals.

```python
from flask import Flask
from jx import Catalog

app = Flask(__name__)
catalog = Catalog("components", jinja_env=app.jinja_env)


@app.route("/")
def home():
    return catalog.render("HomePage.jinja")
```

Serve component assets through Flask's static file handling or a dedicated
static files library.

## Django

Create the catalog once in a dedicated module and return the rendered HTML
inside `HttpResponse`.

```python
# project/jx_catalog.py
from jx import Catalog

catalog = Catalog("templates/components")
```

```python
# app/views.py
from django.http import HttpResponse

from project.jx_catalog import catalog


def home(request):
    return HttpResponse(catalog.render("HomePage.jinja", user=request.user))
```

Best practice: keep the singleton outside the view function, just like in
FastAPI and Flask.

## HTMX

JX and HTMX pair well because both center on server-rendered HTML.

### Fragment rendering pattern

Centralize rendering helpers so routes stay thin:

```python
from typing import Any
from fastapi import Request
from fastapi.responses import HTMLResponse


def is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request") == "true"


def render_page(page: PageRenderData, *, status_code: int = 200) -> HTMLResponse:
    html = render_template(page.template, **page.context.model_dump())
    return HTMLResponse(content=html, status_code=status_code)


def render_fragment(template: str, *, status_code: int = 200, **ctx: Any) -> HTMLResponse:
    html = render_template(template, **ctx)
    return HTMLResponse(content=html, status_code=status_code)
```

Route that serves both full pages and htmx fragments:

```python
@router.get("/users", response_class=HTMLResponse)
async def user_list(request: Request):
    users = await fetch_users()
    if is_htmx(request):
        return render_fragment("@features/UserList.jinja", users=users)
    page = build_users_page(users)
    return render_page(page)
```

### Response handling for 4xx/5xx

By default htmx does NOT swap on error responses. Enable it in JS so
inline validation errors display correctly:

```javascript
import htmx from "htmx.org";

window.htmx = htmx;
htmx.config.responseHandling = [
    { code: "204", swap: false },
    { code: ".*", swap: true },
];
```

### URL sync with hx-push-url

Use `hx-push-url="true"` for in-page navigation that should update the
browser URL (e.g. tag filters, pagination):

```jinja
<Tag
    href="/blog/tags/python"
    hx-get="/blog/tags/python"
    hx-target="#tag-posts"
    hx-swap="outerHTML"
    hx-push-url="true"
/>
```

### Fragment scope

When swapping, the `hx-target` element is replaced. Make sure **all** UI
that needs updating is inside the target. For example, if tag pills AND
posts need to update together, wrap them in the same target container.

### HTMX-friendly component

JX's `attrs` passthrough lets htmx attributes flow naturally:

```jinja
{# def label #}
<button {{ attrs.render(class="btn") }}>
  {{ label }}
</button>
```

Caller:

```jinja
{# import "ActionButton.jinja" as ActionButton #}
<ActionButton
  label="Load More"
  hx-get="/api/items?page=2"
  hx-target="#item-list"
  hx-swap="beforeend"
/>
```

Best practice: render the smallest HTML fragment needed for each swap.

## Alpine.js

Use Alpine.js as progressive enhancement for local UI state: toggles, dropdowns,
modals, tabs, validation, or toasts. Keep the core render on the server.

Include Alpine with `defer`:

```jinja
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

Dropdown example:

```jinja
{# def label #}
<div x-data="{{ { open: false } }}" @click.outside="open = false" {{ attrs.render() }}>
  <button @click="open = !open" :aria-expanded="open">{{ label }}</button>
  <div x-show="open" x-transition>
    {{ content }}
  </div>
</div>
```

Because `x-*`, `@*`, and hyphenated attributes pass through `attrs`, Alpine
can sit naturally on top of JX components.

Use Alpine for:

- dropdowns and accordions;
- modal open/close state;
- tabs and local selection state;
- lightweight form validation;
- toast stores and minor client-side feedback.

Best practice: use Alpine for UI state, HTMX for server round-trips, and JX for
the HTML source of truth.

## Stimulus

Stimulus provides lifecycle-bound controllers for complex client behavior
that benefits from connect/disconnect hooks (e.g. scroll tracking, observer
patterns). It complements Alpine (simple state) and htmx (server fragments).

Register controllers in the JS entry point:

```javascript
import { Application } from "@hotwired/stimulus";
import TocController from "./controllers/toc-controller.js";

const app = Application.start();
app.register("toc", TocController);
```

Attach to JX templates via `data-controller`:

```jinja
<div data-controller="toc">
  {{ content }}
</div>
```

Use Stimulus when you need:

- `connect()`/`disconnect()` lifecycle (event listener cleanup)
- Target tracking across DOM mutations
- Complex scroll, intersection, or resize observers
- Behavior that should auto-bind/unbind when elements enter/leave the DOM

Use Alpine instead for simple toggles, local state, and reactive bindings.

## JS Build System (esbuild)

Bundle Alpine, Stimulus, htmx, and custom JS into a single IIFE with esbuild:

```javascript
// esbuild.config.mjs
import esbuild from "esbuild";

await esbuild.build({
    entryPoints: ["app/static/js/src/main.js"],
    bundle: true,
    minify: true,
    format: "iife",
    target: "es2018",
    outfile: "app/static/js/main.js",
});
```

The entry point registers all frameworks:

```javascript
import Alpine from "@alpinejs/csp";
import { Application } from "@hotwired/stimulus";
import htmx from "htmx.org";

// Alpine data factories
Alpine.data("navbar", navbar);
Alpine.data("palette", palette);
window.Alpine = Alpine;
Alpine.start();

// htmx
window.htmx = htmx;

// Stimulus controllers
const stimulusApp = Application.start();
stimulusApp.register("toc", TocController);
```

Use the CSP-safe Alpine build (`@alpinejs/csp`) to avoid inline `eval()`.

## Combined Stack Rules

- Keep SEO- and content-critical rendering on the server with JX.
- Use HTMX for partial requests and DOM swaps.
- Use Alpine for interaction that does not need a server trip.
- Use Stimulus for lifecycle-bound controllers with cleanup needs.
- Keep components flexible by routing HTMX and Alpine attributes through `attrs`.
- Bundle all JS with esbuild into a single IIFE — no module loader needed.
- Serve component assets via your framework's static files or a reverse proxy;
  JX does not include built-in asset-serving middleware.
