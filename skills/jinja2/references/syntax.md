# Jinja2 Syntax

## Output and Comments

Use:

```jinja
{{ value }}
```

for output and:

```jinja
{# comment #}
```

for comments.

## Conditionals

```jinja
{% if user %}
  Hello {{ user.name }}
{% elif guest_name %}
  Hello {{ guest_name }}
{% else %}
  Hello
{% endif %}
```

Keep conditionals readable. Move business-heavy logic to Python.

## Loops

```jinja
{% for item in items %}
  {{ loop.index }}. {{ item.name }}
{% else %}
  No items
{% endfor %}
```

Useful loop values:

- `loop.index`
- `loop.first`
- `loop.last`
- `loop.length`

## Set

```jinja
{% set total = items | length %}
{% set title = page_title | default('Untitled') %}
```

Use `set` for small presentational values, not complex computation.

## Filters

Common filters:

- `default`
- `length`
- `join`
- `truncate`
- `replace`
- `trim`
- `safe`

Example:

```jinja
{{ name | default('Unknown') }}
{{ tags | join(', ') }}
```

## Tests

Use tests for clearer intent:

```jinja
{% if value is none %}
{% if user is defined %}
{% if items is sequence %}
```

## Whitespace Control

Use whitespace trimming when needed:

```jinja
{%- if compact -%}
...
{%- endif -%}
```

Use deliberately. Overuse hurts readability.

## Guardrails

- do not turn template expressions into a second programming language
- do not hide fragile string-building logic in nested filters
- do not use `safe` casually