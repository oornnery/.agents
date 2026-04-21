# Jinja2 Safety

## Escaping

Default to escaped output.

```jinja
{{ user_input }}
```

This should stay escaped unless the HTML is trusted.

## Safe

Use `safe` only for trusted HTML:

```jinja
{{ trusted_html | safe }}
```

Never use it on raw user input.

## Undefined and Defaults

Use `default` or explicit checks when a value may be missing:

```jinja
{{ title | default('Untitled') }}
{% if user is defined %}
```

This keeps missing context behavior readable.

## N+1 and Repeated Calls

If the host exposes functions or queries in templates, avoid calling them inside
loops in ways that trigger repeated work.

Bad pattern:

- fetch one related object per row in a large loop

Better:

- precompute data in Python
- pass a render-ready structure into the template

## Heavy Logic

Keep heavy logic out of templates:

- permission rules
- expensive calculations
- complex branching trees
- fallback fetch behavior

Templates should render a prepared view model, not assemble one from scratch.

## Review Focus

- check whether escaping is still the default
- check whether `safe` is justified
- check whether undefined handling is graceful
- check whether loops hide extra host calls or expensive work
