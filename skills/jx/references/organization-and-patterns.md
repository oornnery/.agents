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

## Best Practices

- Group by domain for medium and large apps.
- Use prefixes to avoid naming collisions across folders.
- Keep shared primitives in `ui/`, forms in `forms/`, layout in `layout/`.
- Co-locate CSS and JS files next to the component that owns them.
- Always import every component explicitly; there is no auto-discovery.
- Keep SVG accessible: decorative icons should be hidden from screen readers; informative SVGs should have labels.
