# Organization and Patterns

This reference groups project structure, naming, reusable UI patterns, and SVG
component patterns.

## Project Structure

Choose a structure that matches the project size.

### Flat Structure for Small Projects

```text
components/
  Alert.jinja
  Button.jinja
  Card.jinja
  Layout.jinja
```

Usage (every component must be imported):

```jinja
{# import "Layout.jinja" as Layout #}
{# import "Card.jinja" as Card #}
<Layout title="Home">
  <Card title="Welcome">
    <p>Hello</p>
  </Card>
</Layout>
```

### Nested Structure for Medium Projects

```text
components/
  layout/
    Layout.jinja
    Header.jinja
  ui/
    Button.jinja
    Card.jinja
  forms/
    Input.jinja
    FormGroup.jinja
  pages/
    HomePage.jinja
```

Import using folder-relative paths:

```jinja
{# import "layout/Layout.jinja" as Layout #}
{# import "ui/Card.jinja" as Card #}
{# import "forms/Input.jinja" as Input #}
<Layout title="Home">
  <Card title="Welcome">
    <Input name="search" />
  </Card>
</Layout>
```

### Prefixed Folders for Larger Apps

```python
catalog = Catalog("components")
catalog.add_folder("shared/ui", prefix="ui")
catalog.add_folder("shared/forms", prefix="form")
catalog.add_folder("features/auth", prefix="auth")
catalog.add_folder("features/dashboard", prefix="dash")
```

Import using `@prefix/` paths:

```jinja
{# import "@auth/LoginForm.jinja" as LoginForm #}
{# import "@dash/StatsGrid.jinja" as StatsGrid #}
<LoginForm />
<StatsGrid data={{ stats }} />
```

### Subfolders within a Prefixed Folder

`add_folder` registers files **recursively**. Subfolders become part of the import
path relative to the registered root. For example, with `add_folder("ui", prefix="ui")`:

```text
ui/
  layout/
    row.jinja        → @ui/layout/row.jinja
    stack.jinja      → @ui/layout/stack.jinja
  nav/
    navbar.jinja     → @ui/nav/navbar.jinja
    breadcrumb.jinja → @ui/nav/breadcrumb.jinja
  form/
    button.jinja     → @ui/form/button.jinja
    input.jinja      → @ui/form/input.jinja
  card/
    card.jinja       → @ui/card/card.jinja
  tag.jinja          → @ui/tag.jinja
```

Import with the full subfolder path:

```jinja
{# import "@ui/form/button.jinja" as Button #}
{# import "@ui/layout/row.jinja" as Row #}
{# import "@ui/card/card.jinja" as Card #}
```

This is the pattern used in this project. Primitives and atoms with no logical
grouping stay at the prefix root (`@ui/tag.jinja`, `@ui/icon.jinja`).

## Imports

All component usage requires explicit imports via `{# import #}`. There is no
auto-discovery at the template level.

```jinja
{# import "Button.jinja" as Button #}
{# def message #}
<div>{{ message }}</div>
<Button>OK</Button>
```

For aliased names, use dot notation if desired:

```jinja
{# import "@ui/Button.jinja" as ui.Button #}
<ui.Button label="Save" />
```

### Third-Party Packages

Register component packages with `add_package`:

```python
catalog.add_package("my_ui_kit", prefix="ui")
```

The package must expose `JX_COMPONENTS` (and optionally `JX_ASSETS`).
Components are then imported with the `@prefix/` path.

## Common UI Patterns

### Layout Shell

Centralize the document shell and asset output in one layout.

```jinja
{# import "Header.jinja" as Header #}
{# import "Footer.jinja" as Footer #}
{# def title #}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  {{ assets.render() }}
</head>
<body>
  <Header />
  <main>{{ content }}</main>
  <Footer />
</body>
</html>
```

### Layout with Named Slots

Use slots for layouts with multiple insertion regions:

```jinja
{# def title #}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  {{ assets.render() }}
  {% slot head_extra %}{% endslot %}
</head>
<body>
  {% slot sidebar %}{% endslot %}
  <main>{{ content }}</main>
</body>
</html>
```

Caller:

```jinja
{# import "Layout.jinja" as Layout #}
<Layout title="Dashboard">
  {% fill sidebar %}
    <nav>...</nav>
  {% endfill %}
  {% fill head_extra %}
    <link rel="stylesheet" href="/extra.css">
  {% endfill %}
  <h1>Dashboard Content</h1>
</Layout>
```

### Form Wrapper

Let HTMX and validation-related attributes flow through `attrs`.

```jinja
{# def action, method="post" #}
<form action="{{ action }}" method="{{ method }}" {{ attrs.render() }}>
  {{ content }}
</form>
```

### Reusable List or Table Leaf

Break repeated markup into a leaf component instead of building the whole page
inline.

```jinja
{# def user #}
<tr id="user-{{ user.id }}">
  <td>{{ user.name }}</td>
  <td>{{ user.email }}</td>
</tr>
```

### HTMX Action Button

```jinja
{# def label, variant="primary" #}
<button {{ attrs.render(class="btn btn-" + variant, type="button") }}>
  {{ label }}
</button>
```

This pattern works well because `hx-*` attributes pass through automatically.

## SVG Component Patterns

JX is a strong fit for SVG because SVG markup is verbose, repetitive, and often
needs dynamic size, color, and accessibility attributes.

### Basic Icon Component

```jinja
{# def size="24", color="currentColor", label="" #}
<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{{ size }}"
  height="{{ size }}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{{ color }}"
  {% if label %}
    role="img"
    aria-label="{{ label }}"
  {% else %}
    aria-hidden="true"
    focusable="false"
  {% endif %}
  {{ attrs.render() }}
>
  {{ content }}
</svg>
```

Usage:

```jinja
{# import "Icon.jinja" as Icon #}
<Icon label="Warning">
  <circle cx="12" cy="12" r="10" />
</Icon>
```

### Logo and Illustration Components

Use separate components for app branding and empty states so pages do not carry
large SVG blobs inline.

### Spinner and Progress Indicators

SVG is a good fit for loading and progress components because it scales cleanly
and can animate with CSS or SVG animation primitives.

## Semantic Color Tokens with Tailwind Opacity Modifiers

Use RGB channel CSS variables so Tailwind's opacity modifier syntax (`/10`,
`/20`, etc.) works on semantic tokens. Define the channel var alongside the
hex var in `tokens.css`:

```css
:root[data-theme="dark"] {
  --accent: #7c7cff;
  --accent-rgb: 124 124 255;       /* space-separated, no commas */

  --warn: #f59e0b;
  --warn-rgb: 245 158 11;

  --danger: #ef4444;
  --danger-rgb: 239 68 68;

  --accent-2: #22c55e;             /* success / positive */
  --accent-2-rgb: 34 197 94;
}
```

Wire them in `tailwind.config.cjs` using the `<alpha-value>` placeholder:

```js
colors: {
  accent:   'rgb(var(--accent-rgb) / <alpha-value>)',
  warn:     'rgb(var(--warn-rgb) / <alpha-value>)',
  danger:   'rgb(var(--danger-rgb) / <alpha-value>)',
  success:  'rgb(var(--accent-2-rgb) / <alpha-value>)',
}
```

Do **not** use plain `var(--accent)` for colors that need opacity modifiers —
Tailwind cannot inject `<alpha-value>` into a plain CSS variable reference.

Usage in templates:

```jinja
{# Border that respects the active palette #}
<div class="border border-accent/20 hover:border-accent/40">...</div>

{# Status badge using semantic tokens #}
<span class="bg-success/10 text-success border border-success/20">OK</span>
<span class="bg-danger/10 text-danger border border-danger/20">Error</span>
<span class="bg-warn/10 text-warn border border-warn/20">Warning</span>
```

### Palette-aware colors

Theme is controlled via two attributes on `<html>`:

- `data-theme` — `dark` or `light`
- `data-palette` — e.g. `default`, `ocean`, `rose`, `forest`

Palette overrides redefine the full `--accent-rgb`, `--accent`, surface, and
border tokens. Palette rules in `tokens.css` must come **after** the
`data-theme` block in the cascade — specificity is equal (`0,1,1`) so order
wins.

```css
/* ✅ correct — palette block is after data-theme block */
:root[data-theme="dark"] { --accent-rgb: 124 124 255; }
:root[data-palette="rose"] { --accent-rgb: 225 29 72; }

/* ❌ wrong — palette block before data-theme, gets overridden */
:root[data-palette="rose"] { --accent-rgb: 225 29 72; }
:root[data-theme="dark"] { --accent-rgb: 124 124 255; }
```

Every visual accent use (borders, dots, badges, timeline markers) must
reference `--accent-rgb` or `--accent`. Reserve `--interactive` for text link
hover colors only.

## Component Variant Pattern

Define all variants as a Jinja dict, resolve the active variant by key, then
compose the final class string. This keeps all variant styles in one place and
avoids scattered conditionals.

```jinja
{#def variant="default", size="default" #}

{% set variants = {
    "default":   "bg-surface/50 border border-accent/20",
    "outlined":  "bg-transparent border-2 border-accent/30",
    "ghost":     "bg-surface-2/30",
    "glass":     "bg-surface/30 backdrop-blur-md border border-accent/20",
} %}
{% set sizes = {
    "sm":      "p-3 sm:p-4",
    "default": "p-4 sm:p-6",
    "lg":      "p-6 sm:p-8",
} %}
{% set hover = "hover:border-accent/40 hover:bg-surface-2/60" %}
{% set cls = "rounded-lg transition-all duration-200 " ~ variants[variant] ~ " " ~ sizes[size] ~ " " ~ hover %}

<div class="{{ cls }}" {{ attrs.render() }}>{{ content }}</div>
```

Rules:

- Dict keys match the `variant` parameter values exactly.
- Hover and focus classes are composed separately, not baked into each variant.
- Status variants (`success`, `warning`, `danger`) use semantic tokens:
  `bg-success/10 text-success border border-success/20`.
- `transition-all duration-200` (or `transition-colors`) goes on the base
  class, not per-variant, so it always applies.
- When a component renders as `<a>` or `<button>` (clickable), pass
  `cursor-pointer` explicitly — browsers don't always inherit it.

### Status variant template

```jinja
{% set variants = {
    "default":   "bg-surface-2 text-foreground/70 border border-accent/15",
    "accent":    "bg-accent/10 text-accent border border-accent/20",
    "success":   "bg-success/10 text-success border border-success/20",
    "warning":   "bg-warn/10 text-warn border border-warn/20",
    "danger":    "bg-danger/10 text-danger border border-danger/20",
    "outline":   "bg-transparent text-foreground/60 border border-accent/15",
} %}
{% set hover = "hover:text-accent hover:border-accent/50 hover:bg-surface-2/80" %}
{% set cls = "inline-flex items-center font-medium rounded-full transition-colors "
             ~ variants[variant] ~ " " ~ sizes[size] %}

{% if href %}
<a href="{{ href }}" class="{{ cls }} {{ hover }}" {{ attrs.render() }}>{{ text or content }}</a>
{% else %}
<span class="{{ cls }} cursor-pointer {{ hover }}" {{ attrs.render() }}>{{ text or content }}</span>
{% endif %}
```

### Form component variant template

```jinja
{% set variants = {
    "default": "bg-surface border border-accent/15 focus:ring-accent/30 focus:border-accent",
    "filled":  "bg-surface-2 border border-transparent focus:ring-accent/30 focus:border-accent",
    "outline": "bg-transparent border-2 border-accent/20 focus:ring-accent/30 focus:border-accent",
} %}
{% set err_cls = "border-danger/50 focus:border-danger focus:ring-danger/30" if error else "" %}
{% set cls = base ~ " " ~ variants[variant] ~ " " ~ sizes[size] ~ " " ~ err_cls %}
```

## Best Practices

- Group by domain for medium and large apps.
- Use prefixes to avoid naming collisions across folders.
- Keep shared primitives in `ui/`, forms in `form/`, layout in `layout/`.
- Co-locate CSS and JS files next to the component that owns them.
- Always import every component explicitly; there is no auto-discovery.
- Keep SVG accessible: decorative icons should be hidden from screen readers;
  informative SVGs should have labels.
- All color values in components must use semantic tokens (`accent`, `success`,
  `warn`, `danger`) — never hardcode hex or Tailwind color names like
  `blue-500`.
- Borders that should follow the active palette use `border-accent/N`.
- Hover that includes a background fill uses `hover:bg-surface-2/80`;
  hover that only shifts text/border uses `hover:text-accent hover:border-accent/50`.
