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

Use a full page for normal navigation and a smaller component for HTMX:

```python
from fastapi import Request


def is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request") == "true"


@router.get("/users/list", response_class=HTMLResponse)
async def user_list(request: Request):
    users = await fetch_users()
    template = "UserList.jinja" if is_htmx(request) else "pages/UsersPage.jinja"
    return catalog.render(template, users=users)
```

HTMX-friendly button component:

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

## Combined Stack Rules

- Keep SEO- and content-critical rendering on the server with JX.
- Use HTMX for partial requests and DOM swaps.
- Use Alpine for interaction that does not need a server trip.
- Keep components flexible by routing HTMX and Alpine attributes through `attrs`.
- Serve component assets via your framework's static files or a reverse proxy; JX does not include built-in asset-serving middleware.
