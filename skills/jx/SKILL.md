---
name: jx
description: JX patterns for Jinja-based server-rendered Python apps. Use when building or refactoring `.jinja` components, configuring a `Catalog`, declaring arguments with `{# def #}`, importing child components with `{# import #}`, passing content and named slots, forwarding HTML attributes with `attrs`, managing component CSS or JS assets, organizing component libraries, integrating JX with FastAPI, Flask, or Django, combining with HTMX or Alpine.js, building SVG-based components, migrating from JinjaX, or validating templates with `jx check`.
---

# JX

Official JX skill to write Jinja-based server-rendered components with best
practices, keeping up to date with the JX API.

## Shared `Catalog` Singleton

Create one shared `Catalog` in a dedicated module and import it everywhere.
This preserves parsing cache and avoids rebuilding component state on every
request.

```python
# app/components.py
from jx import Catalog

catalog = Catalog("components", site_name="Example")
```

Do not do this:

```python
# DO NOT DO THIS
@app.get("/")
async def home():
    catalog = Catalog("components")
    return catalog.render("HomePage.jinja")
```

### Constructor Shape

```python
Catalog(
    folder=None,           # optional single component folder (shortcut for add_folder)
    *,
    jinja_env=None,        # existing jinja2.Environment to reuse
    extensions=None,       # extra Jinja extensions list
    filters=None,          # dict of Jinja filters
    tests=None,            # dict of Jinja tests
    auto_reload=True,      # re-process files when mtime changes
    asset_resolver=None,   # callable(url, prefix) -> resolved_url
    **globals,             # keyword arguments become template globals
)
```

Key points:

- `folder` is a single path, not variadic. Use `add_folder()` for extra folders.
- Globals are passed as **keyword arguments**, not as a `globals={}` dict.
- `auto_reload=True` checks file mtimes and recompiles when changed.

Do this:

```python
catalog = Catalog("components", site_name="Example", current_year=2026)
```

instead of this:

```python
# DO NOT DO THIS
catalog = Catalog("components", globals={"site_name": "Example"})
```

### Adding Folders and Packages

```python
catalog.add_folder("shared/ui", prefix="ui")
catalog.add_folder("shared/forms", prefix="form", assets="shared/assets/forms")
```

Register components from an installed Python package (must expose `JX_COMPONENTS`):

```python
catalog.add_package("my_ui_kit", prefix="ui")
```

Register all folders and packages **before** the first render call.

### Core Methods

- `catalog.render(relpath, globals=None, **kwargs)` — render a component and
  return HTML.
- `catalog.render_string(source, globals=None, **kwargs)` — render from a raw
  source string (not cached).
- `catalog.list_components()` — return all registered component relative paths.
- `catalog.get_signature(relpath)` — return required/optional args, slots,
  css, js.
- `catalog.collect_assets(output)` — copy package assets to an output folder.

## Component Files

A JX component is a `.jinja` file with a TitleCased name: `Card.jinja`, `UserTable.jinja`.

Keep metadata comments at the top in this order:

1. `{# css #}`
2. `{# js #}`
3. `{# import #}` (one per imported component)
4. `{# def #}`
5. template body

Minimal example:

```jinja
{# def title #}
<section class="card">
  <h2>{{ title }}</h2>
  {{ content }}
</section>
```

## Arguments with `{# def #}`

Use Python-like parameter syntax. Type hints provide runtime `isinstance()`
validation (base types only).

```jinja
{# def
  title: str,
  subtitle: str = "",
  count: int = 0,
  show_icon: bool = True
#}
```

Only one `{# def #}` block is allowed per component. Never declare `content`
or `attrs` — they are always implicit.

Do this:

```jinja
{# def title #}
```

instead of this:

```jinja
{# DO NOT DO THIS #}
{# def title, content, attrs #}
```

## Imports with `{# import #}`

Every child component used in a template **must** be explicitly imported.
Without an import, the parser raises `TemplateSyntaxError: Unknown component`.

```jinja
{# import "Button.jinja" as Button #}
{# import "icons/CheckIcon.jinja" as CheckIcon #}
{# def title #}
<div>
  <h2>{{ title }}</h2>
  <Button label="OK">
    <CheckIcon />
  </Button>
</div>
```

For prefixed folders, use `@prefix/` syntax:

```jinja
{# import "@ui/Button.jinja" as Button #}
```

Relative imports (starting with `./`) resolve from the current file's directory:

```jinja
{# import "./Sibling.jinja" as Sibling #}
```

Do not use components without importing:

```jinja
{# DO NOT DO THIS — will raise TemplateSyntaxError #}
{# def title #}
<Card title="{{ title }}">
  <Button>OK</Button>
</Card>
```

## Passing Values

Use normal HTML attributes for strings:

```jinja
<Button label="Save" />
```

Use double curly braces for non-string values (expressions):

```jinja
<Counter count={{ items | length }} />
<UserCard user={{ current_user }} />
<Chart data={{ [10, 20, 30] }} />
```

Boolean shorthand without a value passes `True`:

```jinja
<Modal open />
```

**Important**: JX does **not** support Vue-like `:attr` colon syntax. That syntax
is commented out in the parser.

Do this:

```jinja
<Counter count={{ items | length }} />
```

instead of this:

```jinja
{# DO NOT DO THIS — colon syntax is not supported #}
<Counter :count="items | length" />
```

## `content` Slot

Every component has an implicit `content` variable containing the rendered HTML
passed between opening and closing tags.

```jinja
{# def title #}
<article class="card">
  <h3>{{ title }}</h3>
  {% if content %}
    <div class="card-body">{{ content }}</div>
  {% endif %}
</article>
```

- `content` is always available (empty string for self-closing tags).
- `content` is rendered in the caller's context first.
- Do not escape `content` again — it is already `Markup`.

## Named Slots and Fills

For components that need multiple content regions, use named slots instead of
extra parameters.

### Defining Slots in a Component

```jinja
{# def title #}
<article class="card">
  <header>{% slot header %}<h3>{{ title }}</h3>{% endslot %}</header>
  <div class="card-body">{{ content }}</div>
  <footer>{% slot footer %}{% endslot %}</footer>
</article>
```

### Filling Slots from the Caller

```jinja
{# import "Card.jinja" as Card #}
<Card title="Welcome">
  {% fill header %}<h2 class="custom">Custom Header</h2>{% endfill %}
  {% fill footer %}<button>Close</button>{% endfill %}
  <p>This is the default content.</p>
</Card>
```

If a fill is not provided, the slot renders its default content. The remaining
body (outside `{% fill %}` blocks) becomes the `content` variable.

## `attrs` Passthrough

Attributes not claimed by `{# def #}` are collected in the implicit `attrs`
object. This keeps components flexible without declaring every HTML, HTMX, and
Alpine attribute up front.

```jinja
{# def variant="primary" #}
<button {{ attrs.render(type="button", class="btn btn-" + variant) }}>
  {{ content }}
</button>
```

Caller:

```jinja
{# import "Button.jinja" as Button #}
<Button variant="danger" id="del-btn" hx-delete="/item/1" class="shadow">
  Delete
</Button>
```

### `attrs` Methods

- `attrs.render(**defaults)` — render all passthrough attrs as HTML string.
  For `class`, defaults are appended (not replaced).
- `attrs.set(**kwargs)` — force values. `False` removes. Class values are
  appended.
- `attrs.setdefault(**kwargs)` — only set values not already present.
- `attrs.get(name, default=None)` — return a single attribute value.
- `attrs.add_class(*values)` / `attrs.prepend_class(*values)` /
  `attrs.remove_class(*names)` — manipulate CSS classes.
- `attrs.classes` — property: all classes as space-separated string.
- `attrs.as_dict` — property: all attributes as a sorted dict.

Python-style underscores in kwargs are converted to dashes (`aria_label` →
`aria-label`). Attributes starting with `_` are silently ignored.

## CSS and JS Assets

Declare assets at the top of the component:

```jinja
{# css "/static/components/card.css" #}
{# js "/static/components/card.js" #}
{# def title #}
<section class="card">{{ title }}</section>
```

Render them from the layout using the `assets` global (injected by `catalog.render()`):

```jinja
<head>
  {{ assets.render() }}
</head>
```

Available helpers: `assets.render()`, `assets.render_css()`, `assets.render_js()`,
`assets.collect_css()`, `assets.collect_js()`.

CSS is emitted before JS. JS is `<script type="module">` by default. Repeated
declarations are deduplicated. Assets from imported children are collected
recursively.

Do this:

```jinja
{{ assets.render() }}
```

instead of this:

```jinja
{# DO NOT DO THIS — catalog is not available in templates #}
{{ catalog.render_assets() }}
```

## Jinja Environment

By default, JX creates a `jinja2.Environment` with `autoescape=True`,
`StrictUndefined`, and the `jinja2.ext.do` extension. Reuse an existing
framework environment when you want shared globals and filters:

```python
from flask import Flask
from jx import Catalog

app = Flask(__name__)
catalog = Catalog("components", jinja_env=app.jinja_env)
```

Or configure via constructor hooks:

```python
catalog = Catalog(
    "components",
    filters={"initials": lambda name: "".join(p[0] for p in name.split())},
    tests={"admin": lambda user: getattr(user, "role", None) == "admin"},
    extensions=["jinja2.ext.loopcontrols"],
    current_year=2026,
)
```

## Common Mistakes to Avoid

- **Missing imports**: every `<Component />` tag needs a `{# import #}`.
- **String expressions**: use `data={{ [1,2,3] }}`, not `data="[1,2,3]"`.
- **Colon syntax**: use `count={{ expr }}`, not `:count="expr"`.
- **Escaping content**: use `{{ content }}`, not `{{ content | e }}`.
- **Globals as dict**: use `Catalog("c", key=val)`, not `Catalog("c", globals={...})`.
- **Assets in templates**: use `{{ assets.render() }}`, not
  `{{ catalog.render_assets() }}`.
- **Catalog per request**: create one singleton, not a new `Catalog()` per handler.
- **Adding folders late**: register all folders before the first `render()` call.
- **Hardcoded colors**: never use raw hex or Tailwind palette names (`blue-500`,
  `#7c7cff`) in components — always use semantic tokens (`accent`, `success`,
  `warn`, `danger`) so components respond to theme and palette changes.
- **Plain CSS var in Tailwind config**: `var(--accent)` breaks opacity modifiers
  (`bg-accent/10`). Use `rgb(var(--accent-rgb) / <alpha-value>)` instead.
- **Hover only on links**: apply `cursor-pointer` explicitly on `<span>` tags
  that are interactive — browsers do not inherit it from CSS hover rules.

## Validation with `jx check`

The `jx check` command validates all components in a `Catalog`. It takes a
Python import path, not a folder path.

```bash
jx check myapp.components:catalog
jx check path/to/components.py:catalog
jx check myapp.components:catalog --format json
```

See [the migration and tooling reference](references/migration-and-tooling.md)
for testing strategies, CI setup, `jx collect_assets`, and JinjaX migration.

## Integrations

See [the integrations reference](references/integrations.md) for FastAPI,
Flask, Django, HTMX (fragment rendering, 4xx config, URL sync), Alpine.js,
Stimulus (lifecycle controllers), and esbuild build system guidance.

## Organization

See [the organization reference](references/organization-and-patterns.md) for
project structure, prefixed folders, recursive subfolder imports, SVG components,
semantic color tokens with RGB channels, component variant dict pattern, and
status variant templates.
