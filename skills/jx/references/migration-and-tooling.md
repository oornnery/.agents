# Migration and Tooling

This reference groups the JinjaX-to-JX migration path, testing strategies,
`jx check` validation, and `jx collect_assets`.

## Migration from JinjaX

The main migration is in Python setup, not in component templates.

### Install

```bash
# before
pip install jinjax

# after
pip install jx
```

### Imports

```python
# before
from jinjax import Catalog

# after
from jx import Catalog
```

### Catalog Creation

```python
# before
catalog = jinjax.Catalog(globals={"site_name": "Example"})
catalog.add_folder("components")

# after
catalog = Catalog("components", site_name="Example")
```

### Key Differences

| JinjaX                                     | JX                                        |
| ------------------------------------------ | ----------------------------------------- |
| `Catalog(globals={...})`                   | `Catalog("folder", **globals)`            |
| `catalog.add_module(mod, prefix=...)`      | `catalog.add_package("name", prefix=...)` |
| `catalog.get_middleware(app)`              | Removed — serve assets externally         |
| `root_url="/static/..."` constructor param | Removed — not needed                      |
| `{{ catalog.render_assets() }}`            | `{{ assets.render() }}`                   |
| `:attr="expr"`                             | `attr={{ expr }}`                         |

### What Stays the Same

- `{# def #}` argument declarations
- `{# css #}` and `{# js #}` metadata
- `{{ attrs.render() }}`
- `{{ content }}`
- TitleCased component filenames
- Component tag syntax like `<Card />`

### New Features in JX

- Named slots: `{% slot name %}` / `{% fill name %}`
- `render_string()`, `get_signature()`, `list_components()`, `collect_assets()`
- `asset_resolver` callback for custom asset URL transformation
- Runtime type validation with `{# def #}` type annotations
- Thread-safe component registry

### Common Migration Steps

1. Replace package: `jinjax` → `jx`.
2. Update imports to `from jx import Catalog`.
3. Move first folder path into the constructor.
4. Convert `globals={...}` to keyword arguments.
5. Remove `root_url` from the constructor.
6. Remove `get_middleware()` calls; serve assets externally.
7. Replace `catalog.render_assets()` with `{{ assets.render() }}`.
8. Replace `:attr="expr"` with `attr={{ expr }}`.
9. Replace `add_module(mod, prefix=...)` with `add_package("name", prefix=...)`.
10. Run `jx check` and app tests.

## Component Tests

The most reliable baseline is to render components and assert on the produced
HTML.

```python
import pytest
from jx import Catalog


@pytest.fixture
def catalog():
    return Catalog("components")


def test_button_renders_label(catalog):
    html = catalog.render("Button.jinja", label="Save")
    assert "Save" in html


def test_missing_required_argument_raises(catalog):
    with pytest.raises(Exception):
        catalog.render("Button.jinja")
```

### Structured HTML Assertions

When whitespace or attribute ordering may vary, parse the HTML and assert on
structure:

```python
from bs4 import BeautifulSoup


def test_nav_marks_current_page(catalog):
    html = catalog.render("Nav.jinja", items=[{"label": "Home", "href": "/"}], current_path="/")
    soup = BeautifulSoup(html, "html.parser")
    assert soup.find("a")["aria-current"] == "page"
```

### Route Tests

Test the framework route when behavior depends on request headers or
integration glue:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text
```

Best practice: test full pages and reusable leaf components separately.

## `jx check`

Validates all components registered in a `Catalog` instance. Takes a Python
import path, not a folder path.

```bash
jx check myapp.components:catalog
jx check path/to/components.py:catalog
jx check myapp.components:catalog --format json
```

### What It Validates

- All imports resolve to registered components.
- Component tags used in templates match an imported name.
- `{# def #}` syntax parses correctly.
- Template syntax (unclosed tags, unmatched braces).
- Suggests similar names for typos via fuzzy matching.

It performs static analysis only. It does not prove the rendered HTML is
correct for your real runtime data.

### JSON Output

The `--format json` output includes `checked` (number of components) and
`errors` (list of objects with `file`, `line`, `message`, `suggestion`,
`abs_path`).

## `jx collect_assets`

Copies all registered package assets to an output folder:

```bash
jx collect_assets myapp.components:catalog static/vendor
```

Files from each prefix are placed in `<output>/<prefix>/`.

## CI and Pre-Commit

Minimal GitHub Actions step:

```yaml
- run: pip install jx
- run: jx check myapp.components:catalog --format json
```

Minimal pre-commit hook:

```yaml
- id: jx-check
  name: JX Component Check
  entry: jx check myapp.components:catalog
  language: system
  pass_filenames: false
```
