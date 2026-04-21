---
name: jinja2
description: Jinja2 template patterns for Python applications. Covers syntax,
  inheritance, includes, macros, filters, loops, whitespace control, template
  context, escaping, and safe server-rendered HTML design.
---

# Jinja2

Use this skill when the work is primarily Jinja2 templates, server-rendered
HTML, email templates, partials, or template macros.

## Boundary

Use this skill for:

- Jinja2 syntax and control flow
- template inheritance, includes, and macros
- page, partial, email, and component-like templates
- host-provided globals, formatting helpers, and context rules
- escaping, `safe`, and template safety boundaries

Pair with:

- `python` when template context comes from Python handlers or controllers
- `htmx` when templates are returned as fragment responses
- `design` when template structure and UI boundaries need cleanup
- `security` when escaping, trusted HTML, or untrusted context is involved

## Reference Map

- `references/syntax.md` -- expressions, conditionals, loops, filters, tests,
  `set`, comments, and whitespace control
- `references/templates.md` -- inheritance, blocks, includes, imports, macros,
  call blocks, and partial organization
- `references/context.md` -- host-provided globals, formatting helpers,
  translation, and context boundaries
- `references/safety.md` -- escaping, `safe`, undefined handling, N+1 risks,
  and template review guidance

## Assets

- `assets/main.py` -- a small FastAPI entrypoint wiring templates and static
- `assets/templates/base.jinja` -- shared page shell
- `assets/templates/page/projects.jinja` -- a full page that composes partials
- `assets/templates/partials/project_list.jinja` -- a reusable list fragment
- `assets/templates/components/badge.jinja` -- small reusable template helpers
- `assets/static/app.css` -- minimal static styling for the example app

## What Stays Here

Keep this file focused on defaults and guardrails.

- keep here: syntax stance, structure defaults, and safety cues
- move to refs: long syntax catalogs, inheritance patterns, and host-context
  details
- use assets for copyable template skeletons and macro examples

## Core Defaults

- keep templates focused on presentation, not business logic
- use inheritance, includes, and macros to avoid repeated markup
- keep loops and conditionals readable; move heavy branching into Python
- use host formatting helpers for dates, currency, and localized values when
  the host app provides them
- keep ids, classes, and partial boundaries stable when templates power htmx or
  interactive surfaces
- default to escaped output; use `safe` only for trusted HTML
- give templates explicit empty states instead of silent blank sections

## Template Structure Rules

- use a base template for shared page shell when the app has full pages
- use partials for repeated fragments or htmx swap targets
- use macros for small repeated structures, not giant hidden sub-apps
- keep context names boring and explicit
- keep template files close to the surface they render

For deeper structure patterns, load `references/templates.md`.

## Guardrails

- do not run database queries or expensive calls from inside loops when the host
  allows such access
- do not bury important formatting logic in ad hoc inline expressions
- do not use `safe` on user input or unknown HTML
- do not let templates become the place where permissions or business rules are
  decided
- do not over-nest inheritance and includes until tracing output becomes hard

## Review Focus

- check whether the template uses clear blocks, partials, or macros
- check whether formatting and translation are handled consistently
- check whether escaping is safe and intentional
- check whether the context contract is explicit enough for the host app
- check whether heavy computation or N+1-style access should move back to
  Python
