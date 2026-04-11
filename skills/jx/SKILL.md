---
name: jx
description: JX patterns for Jinja-based server-rendered components -- Catalog, {# def #}, {# import #}, slots, attrs, CSS/JS assets. Load when building .jinja components or integrating JX with FastAPI/Flask/Django.
---

# JX

JX 0.10 skill for Jinja-based server-rendered components. For client-side
interactivity beyond HTML sprinkles, use Solid islands
(`../frontend/references/solid-islands.md`).

## Core Principles

1. **Native HTML first.** Prefer built-in elements and APIs before JavaScript:
   - `<dialog>` + `.showModal()` for modals — close via
     `<form method="dialog">`, Escape key dismisses by default.
   - Popover API (`popover` + `popovertarget`) for dropdowns, tooltips, and
     all floating/overlay UI — renders in the top layer, escapes
     `overflow: hidden`.
   - `<details>` for accordions — use the `name` attribute for exclusive
     groups.
   - Native `<form>` validation — `required`, `pattern`, `type="email"`, etc.

2. **Tailwind v4 for styling.** Utility classes directly in markup. Tailwind
   v4 uses a CSS-first config model (no `tailwind.config.js`).

3. **Vanilla JS as ES modules.** When JavaScript is unavoidable, write it as a
   small ES module declared via `{#js component.js #}`. Keep scripts minimal,
   focused, and progressively enhancing.

4. **Framework-agnostic.** No `url_for`, `csrf_token()`, or other
   framework-specific helpers. Accept URLs and tokens as props.

5. **Components are fragments.** Never output `<!DOCTYPE>`, `<html>`, `<head>`,
   or `<body>`. Components are rendered inside an existing page.

## When to Use JavaScript

| Interaction                 | Solution                                                         |
| --------------------------- | ---------------------------------------------------------------- |
| Modal dialog                | `<dialog>` + `.showModal()` — close via `<form method="dialog">` |
| Backdrop dismiss            | `closedby="any"` on `<dialog>`                                   |
| Dropdown menu               | Popover API (`popover` + `popovertarget`)                        |
| Tooltip                     | Popover API with `popover="hint"`                                |
| Floating listbox / combobox | Popover API (`popover="manual"`) + JS for filtering              |
| Show/hide panel             | `<details>` or Popover API                                       |
| Form validation             | Native `required`, `pattern`, `type` attrs                       |
| Cancel bypassing validation | `formmethod="dialog"` + `formnovalidate` on the button           |
| Tabs                        | `<details name="...">` for accordion-style, or JS for true tabs  |
| Clipboard copy              | JS (`navigator.clipboard`)                                       |
| Dynamic list filtering      | JS                                                               |
| Keyboard shortcuts          | JS                                                               |
| Complex animations          | CSS `@starting-style` + transitions                              |

When writing JS: declare via `{#js component.js #}`, write as an ES module
(`type="module"` is the JX default), use event delegation on `document` where
possible, keep it small — one focused behavior per file.

## Shared `Catalog` Singleton

Create one shared `Catalog` singleton and import it everywhere. Never
create a new `Catalog()` per request.

```python
# app/components.py
from jx import Catalog

catalog = Catalog("components", site_name="Example", current_year=2026)
```

### Constructor

- `folder` is a single path. Use `add_folder()` for extra folders.
- Globals are **keyword arguments**, not `globals={}` dict.
- `jinja_env=` reuses an existing Jinja environment.
- `auto_reload=True` checks file mtimes.

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

A JX component is a `.jinja` file. Use `snake_case` filenames, with a
`CamelCased` root CSS class and `kebab-cased` utility classes:

```html+jinja title="tab_group.jinja"
<div {{ attrs.render(class="TabGroup") }}>
  <select class="tab-group-control">
  {{ content }}
</div>
```

For components that need JS, output a companion `.js` file declared via
`{#js ... #}`:

```text
components/
  button.jinja
  card.jinja
  modal.jinja
  modal.js          <- companion JS when needed
  forms/
    input.jinja
    select.jinja
```

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

Only one `{# def #}` block per component. Never declare `content`
or `attrs` -- they are always implicit.

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

## Passing Values

- String: `<Button label="Save" />`
- Expression: `<Counter count={{ items | length }} />`
- Boolean: `<Modal open />` (passes `True`)
- JX does **not** support Vue-like `:attr` colon syntax.

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

Put all attributes inside `attrs.render()` -- do not scatter as bare HTML.
Use `{% set %}` for complex values before the render call.

## CSS and JS Assets

Declare assets at the top of the component:

```jinja
{# css "/static/components/card.css" #}
{# js "/static/components/card.js" #}
{# def title #}
<section class="card">{{ title }}</section>
```

Render in layout with `{{ assets.render() }}` (CSS + JS) or separately
with `{{ assets.render_css() }}` / `{{ assets.render_js() }}`. Assets
deduplicate automatically. JS is `<script type="module">` by default.

Use `assets.render_js(module=False)` for IIFE bundles.

### External JS

JX does not bundle asset URLs. Use CDN `<script>` tags, local static via
`{#js #}`, or esbuild/Vite output. Use `asset_resolver` callback on `Catalog`
to transform URLs at render time.

See [integrations reference](references/integrations.md) for build tool configs.

## Animations

Use a shared `transitions.css` (`{#css transitions.css #}`) for `<dialog>` and
popover enter/exit animations via `@starting-style` and `allow-discrete`.
Patterns: default dialog (fade+scale), `slide-from-left`, `slide-from-right`.

## Jinja Environment

Default: `autoescape=True`, `StrictUndefined`, `jinja2.ext.do`. Pass
`jinja_env=` to reuse a framework environment. Add `filters={}`, `tests={}`,
`extensions=[]` via constructor.

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
- **Typed params with quotes**: when a `{# def #}` declares a typed param like
  `rows: int = 4`, the caller must pass `rows=5` (no quotes), not `rows="5"`.
  Quoted values are strings and will raise `InvalidPropType` at runtime.
- **Params that accept mixed types**: if a param can receive both `str` and
  `int` (e.g., a form `value`), omit the type hint to skip validation:
  `{# def value="" #}` instead of `{# def value: str = "" #}`.
- **Hardcoded colors**: never use raw hex or Tailwind palette names (`blue-500`,
  `#7c7cff`) in components — always use semantic tokens (`accent`, `success`,
  `warn`, `danger`) so components respond to theme and palette changes.
- **Plain CSS var in Tailwind config**: `var(--accent)` breaks opacity modifiers
  (`bg-accent/10`). Use `rgb(var(--accent-rgb) / <alpha-value>)` instead.
- **Hover only on links**: apply `cursor-pointer` explicitly on `<span>` tags
  that are interactive — browsers do not inherit it from CSS hover rules.

## Color Mode

Before generating components, confirm which color mode the user wants:

- **Light only** (default) — no `dark:` prefixes needed.
- **Dark only** — dark backgrounds, light text; no `dark:` prefixes needed.
- **Both** — light as base, add `dark:` variants for all color-bearing
  utilities: backgrounds, text, borders, rings, placeholders, shadows, and
  hover/focus state colors.

If unspecified, default to **light only**. When generating both modes, apply
`dark:` variants to every color-dependent utility.

## Checklist Before Output

1. Props have sensible defaults — only truly required data lacks a default.
2. `attrs.render()` is on the root element with default classes.
3. Accessibility — correct ARIA attributes, keyboard navigability, labels,
   `focus-visible` styles.
4. No framework-specific helpers — no `url_for`, `csrf_token()`.
5. Native HTML first — no JS for interactions the browser handles natively.
6. Tailwind classes only — no custom CSS unless declared via `{#css #}`.
7. No page shell — no `<!DOCTYPE>`, `<html>`, `<head>`, or `<body>`.
8. Color mode matches the user's preference.

## Test Files

Only generate test files when explicitly asked. Create one `test_<name>.jinja`
per **top-level** component (not internal sub-components). Each test file
should:

- Import the component with a relative path.
- Pass realistic data exercising all features: required props, optional props
  with non-default values, slots, edge cases.
- Be self-contained — renderable with `catalog.render("test_<name>.jinja")`
  without external context.
- Include inline test data directly in the template.

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

## Component Patterns

See [the patterns reference](references/patterns.md) for production-ready
component examples: Button, Modal (`<dialog>`), Dropdown (Popover API), Form
Input, Data Table, and Sidebar Layout.

## Organization

See [the organization reference](references/organization-and-patterns.md) for
project structure, prefixed folders, recursive subfolder imports, SVG components,
semantic color tokens with RGB channels, component variant dict pattern, and
status variant templates.
