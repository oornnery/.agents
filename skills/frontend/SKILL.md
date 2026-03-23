---
name: frontend
description: Frontend bootstrap and UI tooling guidance. Use when setting up
  JavaScript or TypeScript tooling, ESLint or Prettier, Tailwind CSS, Basecoat
  UI, semantic theme tokens, or editor-friendly frontend defaults for new
  projects.
---

# Frontend

Official frontend skill for bootstrapping and maintaining editor-friendly UI
stacks with clear conventions.

Treat the Tailwind and Basecoat setup here as a recommended baseline for new
projects, not a mandatory repo-wide standard.

## Documentation

- Solid: <https://docs.solidjs.com/>
- SolidStart: <https://docs.solidjs.com/solid-start/getting-started>
- TypeScript: <https://www.typescriptlang.org/docs/>
- TypeScript Language Server: <https://github.com/typescript-language-server/typescript-language-server>
- ESLint: <https://eslint.org/docs/latest/>
- Prettier: <https://prettier.io/docs/>
- Tailwind CSS: <https://tailwindcss.com/docs>
- Tailwind Editor Setup: <https://tailwindcss.com/docs/editor-setup>
- Basecoat UI: <https://basecoatui.com/installation>

## Submodules

| Submodule                     | When to load                                                 |
| ----------------------------- | ------------------------------------------------------------ |
| `references/solid.md`         | SolidJS setup, components, signals, router, state, resources |
| `references/solid-islands.md` | Solid islands with Jinja2 and JX                             |
| `references/solidstart.md`    | SolidStart app structure, file routes, meta                  |
| `references/tailwind.md`      | Tailwind setup and semantic token baseline                   |
| `references/basecoat.md`      | Basecoat CSS, theming, JS imports, macros                    |
| `references/testing.md`       | Vitest, testing components, Solid Testing Library            |
| `references/vite-tooling.md`  | Vite config, path aliases, code splitting                    |
| `references/accessibility.md` | Semantic HTML, WAI-ARIA, forms, screen readers               |
| `../markdown/SKILL.md`        | Docs, README updates, rumdl validation                       |

---

## Default Approach

When bootstrapping a frontend:

1. Set up JavaScript and TypeScript tooling first.
2. Pick the application runtime layer: plain Solid or SolidStart.
3. Add formatting and linting before adding UI libraries.
4. Add Tailwind only if utility CSS and token-based theming are desired.
5. Add Basecoat when you want prebuilt primitives without depending on React.
6. Validate the toolchain before expanding the UI surface area.

This order keeps failures easy to isolate. Editor tooling, linting, CSS
pipeline, and UI primitives should not be introduced all at once unless the
project is brand new.

---

## Solid Stack Guide

Use Solid when you want a fine-grained reactive UI layer with explicit control
over rendering and state. Use SolidStart when you also want the official app
framework, file-based routing, server rendering, and full-stack conventions.

Load `references/solid.md` for:

- core SolidJS setup;
- component and signal patterns;
- router setup with `@solidjs/router`;
- route definitions, links, params, and lazy route loading.

Load `references/solidstart.md` for:

- SolidStart project bootstrap;
- app file layout such as `src/routes` and `app.tsx`;
- file-based route conventions;
- `@solidjs/meta` setup for page titles and SEO metadata.

Load `references/solid-islands-jinja.md` for:

- progressive enhancement in Jinja2 or JX pages;
- islands-style hydration for isolated interactive widgets;
- mount-point conventions between server-rendered HTML and Solid;
- boundaries and caveats when mixing Solid islands with non-hydrating content.

### Quick Guidance

- Choose plain Solid for widget-style apps, embedded interfaces, or cases where
  you want to control routing explicitly.
- Choose SolidStart for full applications with route-based pages and SSR or
  hybrid rendering needs.
- In SolidStart, prefer file routes over hand-built router trees unless you
  have a specific reason not to.
- For Jinja2 or JX pages, prefer Solid as isolated islands mounted into
  server-rendered HTML instead of forcing the whole page into a SPA model.

---

## Tooling First

Install the language and editor tools before adding framework-specific code:

- `typescript` for compiler and project typing.
- `typescript-language-server` for editor support.
- `eslint` for code quality and basic JS rules.
- `prettier` for formatting.
- `@tailwindcss/language-server` when the project uses Tailwind classes.

Do this:

```bash
npm install -g typescript
npm install -g typescript-language-server
npm install -g @tailwindcss/language-server
npm install -g eslint
npm install -g prettier
```

instead of skipping straight to CSS libraries without a stable lint and format
baseline.

### Config Shape

- Keep `eslint.config.js` minimal unless the project already requires a layered
  preset structure.
- Keep `prettier.config.js` small and predictable.
- Prefer one formatter and one linter path instead of overlapping tools with
  competing rewrites.

Recommended defaults:

### `eslint.config.js`

```js
import js from '@eslint/js'

export default [js.configs.recommended]
```

### `prettier.config.js`

```js
export default {
  semi: false,
  singleQuote: true,
  trailingComma: 'es5',
  printWidth: 100,
}
```

---

## Tailwind as a Token Layer

Load `references/tailwind.md` when the project needs utility CSS plus semantic
theme tokens.

Use Tailwind as a design-system layer, not just a bag of arbitrary classes:

- Prefer semantic CSS variables such as `--background`, `--foreground`, and
  `--primary`.
- Map those variables into Tailwind theme colors.
- Keep `content` globs aligned with the actual app layout.
- Add plugins only when the project will use them.

Do this:

```js
colors: {
  background: 'hsl(var(--background))',
  foreground: 'hsl(var(--foreground))',
}
```

instead of scattering hard-coded color values across templates and components.

### Recommended Uses

- Utility-driven application shells.
- Design tokens shared across templates and components.
- Server-rendered templates that still benefit from a consistent utility layer.

### Anti-Patterns

- Do not introduce Tailwind if the project already has a stable CSS system that
  would be duplicated by it.
- Do not mix semantic tokens and raw palette values randomly in the same layer.
- Do not add plugin packages that are never used.

---

## Basecoat for Non-React Primitives

Load `references/basecoat.md` when the project wants shadcn-style primitives
without a React dependency.

Basecoat fits well when:

- the project is server-rendered;
- you want consistent UI primitives but not a client-heavy component runtime;
- Jinja or Nunjucks macros are a better fit than framework components.

Use Basecoat as an extra layer on top of Tailwind, not as a reason to abandon
semantic theming.

### Integration Guidance

- Import Basecoat after Tailwind in the main stylesheet.
- Keep theme tokens in a dedicated file when the project benefits from clearer
  separation.
- Add Basecoat JavaScript only for the specific interactive pieces you use.
- For template-heavy apps, prefer the documented CLI macro flow over copying
  markup manually.

Do this:

```css
@import 'tailwindcss';
@import 'basecoat-css';
@import './theme.css';
```

instead of mixing Basecoat assets into unrelated CSS files without a clear load
order.

---

## Project Structure

Prefer structure that makes the content globs and asset ownership obvious.

Common layout:

```text
frontend/
components/
templates/
docs/
```

Match the existing repository shape before introducing new directories. The
recommended Tailwind config assumes those paths because they work well for mixed
frontend and server-rendered projects.

---

## Validation

Validate the frontend setup in layers:

```bash
typescript-language-server --version
eslint --version
prettier --version
```

Then validate the project-specific config and docs:

```bash
uvx rumdl check .
```

Use `../markdown/SKILL.md` when the task includes README changes, docs updates,
or Markdown lint failures.

---

## Rules of Thumb

- Prefer SolidStart for full apps and plain Solid for smaller routed shells or
  embedded UI.
- For Jinja2 and JX projects, keep Solid limited to interactive islands with
  stable mount points and server-owned outer markup.
- Keep route ownership obvious, either via SolidStart file routes or a single
  explicit router tree.
- Put metadata near the route that owns it, and keep shared SEO defaults at the
  app root.
- Keep frontend setup explicit and easy to recreate.
- Prefer semantic color tokens over raw color utility sprawl.
- Prefer stable defaults over clever config layering.
- Match the existing project structure before adding new frontend conventions.
- If the project is server-rendered, consider Basecoat macros before inventing
  a custom component layer.
- Use references for detailed config snippets; keep this file focused on
  decision-making and workflow.
