# Jinja2 Templates

## Inheritance

Use `extends` and blocks for full-page layouts:

```jinja
{% extends 'base.jinja' %}

{% block title %}Projects{% endblock %}

{% block content %}
  <h1>Projects</h1>
{% endblock %}
```

This keeps shared shell markup in one place.

## Includes

Use includes for repeated fragments:

```jinja
{% include 'partials/_row.jinja' %}
```

Good fits:

- tables
- cards
- alerts
- form fragments

## Imports and Macros

Use imports and macros for reusable markup helpers:

```jinja
{% from 'macros/forms.jinja' import field_error %}
{{ field_error(errors.name) }}
```

Use macros when:

- the markup is small and repeated
- it needs a stable call contract
- it helps avoid repeating label, hint, or error markup

## Call Blocks

Use `call` when a macro should wrap caller content:

```jinja
{% call panel('Settings') %}
  <p>Body content</p>
{% endcall %}
```

## Page vs Partial

Keep a clear difference:

- page templates own full-page content
- partials own swap targets, components, or sections
- email templates optimize for email rendering constraints

## File Organization

A simple pattern:

```text
templates/
  base.jinja
  users/
    page.jinja
    partials/
      _table.jinja
      _row.jinja
  macros/
    forms.jinja
```

## Guardrails

- do not chain too many include layers for simple markup
- do not make macros responsible for opaque global state
- do not treat partials like controllers; context should arrive ready enough to
  render
