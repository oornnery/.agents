---
name: jinja2
description: Jinja2 template patterns for Python. Syntax, inheritance, includes, macros, filters, loops, whitespace, context, escaping, safe server-rendered HTML.
---

# Jinja2

Use when work primarily Jinja2 templates, server-rendered HTML, email templates, partials, or template macros.

## Boundary

Use for:

- Jinja2 syntax and control flow
- template inheritance, includes, macros
- page, partial, email, component-like templates
- host-provided globals, formatting helpers, context rules
- escaping, `safe`, template safety boundaries

Pair with:

- `python` when template context from Python handlers/controllers
- `htmx` when templates returned as fragment responses
- `design` when template structure/UI boundaries need cleanup
- `security` when escaping, trusted HTML, untrusted context involved

## Reference Map

- `references/syntax.md` -- expressions, conditionals, loops, filters, tests, `set`, comments, whitespace control
- `references/templates.md` -- inheritance, blocks, includes, imports, macros, call blocks, partial organization
- `references/context.md` -- host-provided globals, formatting helpers, translation, context boundaries
- `references/safety.md` -- escaping, `safe`, undefined handling, N+1 risks, template review guidance

## Assets

- `assets/main.py` -- small FastAPI entrypoint wiring templates and static
- `assets/templates/base.jinja` -- shared page shell
- `assets/templates/page/projects.jinja` -- full page composing partials
- `assets/templates/partials/project_list.jinja` -- reusable list fragment
- `assets/templates/components/badge.jinja` -- small reusable template helpers
- `assets/static/app.css` -- minimal static styling for example app

## What Stays Here

Keep this file focused on defaults and guardrails.

- keep here: syntax stance, structure defaults, safety cues
- move to refs: long syntax catalogs, inheritance patterns, host-context details
- use assets for copyable template skeletons and macro examples

## Core Defaults

- keep templates focused on presentation, not business logic
- use inheritance, includes, macros to avoid repeated markup
- keep loops/conditionals readable; move heavy branching into Python
- use host formatting helpers for dates, currency, localized values when host provides them
- keep ids, classes, partial boundaries stable when templates power htmx or interactive surfaces
- default to escaped output; use `safe` only for trusted HTML
- give templates explicit empty states over silent blank sections

## Template Structure Rules

- use base template for shared page shell when app has full pages
- use partials for repeated fragments or htmx swap targets
- use macros for small repeated structures, not giant hidden sub-apps
- keep context names boring and explicit
- keep template files close to surface they render

For deeper structure patterns, load `references/templates.md`.

## Guardrails

- do not run DB queries or expensive calls from inside loops when host allows such access
- do not bury important formatting logic in ad hoc inline expressions
- do not use `safe` on user input or unknown HTML
- do not let templates become where permissions or business rules decided
- do not over-nest inheritance and includes until tracing output hard

## Review Focus

- check template uses clear blocks, partials, or macros
- check formatting and translation handled consistently
- check escaping safe and intentional
- check context contract explicit enough for host app
- check heavy computation or N+1-style access should move back to Python
