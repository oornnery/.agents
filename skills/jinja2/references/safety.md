# Jinja2 Safety

## Escaping

Default to escaped output.

```jinja
{{ user_input }}
```

Keep escaped unless HTML trusted.

## Safe

Use `safe` only for trusted HTML:

```jinja
{{ trusted_html | safe }}
```

Never on raw user input.

## Undefined and Defaults

Use `default` or explicit checks when value may be missing:

```jinja
{{ title | default('Untitled') }}
{% if user is defined %}
```

Keeps missing context behavior readable.

## N+1 and Repeated Calls

Avoid calling host functions/queries inside loops -- triggers repeated work.

Bad pattern:

- fetch one related object per row in large loop

Better:

- precompute data in Python
- pass render-ready structure into template

## Heavy Logic

Keep heavy logic out of templates:

- permission rules
- expensive calculations
- complex branching trees
- fallback fetch behavior

Templates render prepared view model, not assemble one from scratch.

## Review Focus

- check escaping still default
- check `safe` justified
- check undefined handling graceful
- check loops hide no extra host calls or expensive work
