# SolidStart and Meta

Use this reference when building a full Solid application with SolidStart.

## When to Use

- Multi-page applications using the official Solid app framework.
- Projects that benefit from file-based routing.
- Apps that need SSR, route-level rendering control, or page metadata.

## Bootstrap

Create a SolidStart app with the official starter:

```bash
npm create solid@latest
```

Choose a SolidStart template when the app should use file routes and the
official framework structure.

## App Structure

Common layout:

```text
src/
  routes/
  app.tsx
  entry-client.tsx
  entry-server.tsx
```

- `src/routes` owns file-based pages and nested route layout.
- `app.tsx` defines the shared app shell.
- entry files wire the client and server runtime.

## File Routes

SolidStart uses file-based routing from `src/routes`.

Typical examples:

- `src/routes/index.tsx` -> `/`
- `src/routes/about.tsx` -> `/about`
- `src/routes/blog/[slug].tsx` -> `/blog/:slug`

Prefer file routes for page ownership and discoverability.

## App Shell

Minimal `app.tsx` shape:

```tsx
import { MetaProvider, Title } from '@solidjs/meta'
import { Router } from '@solidjs/router'
import { FileRoutes } from '@solidjs/start/router'

export default function App() {
  return (
    <Router
      root={(props) => (
        <MetaProvider>
          <Title>My App</Title>
          {props.children}
        </MetaProvider>
      )}
    >
      <FileRoutes />
    </Router>
  )
}
```

## `@solidjs/meta`

Use `@solidjs/meta` for titles and route-level metadata.

Install it when it is not already present:

```bash
npm install @solidjs/meta
```

Typical route usage:

```tsx
import { Meta, Title } from '@solidjs/meta'

export default function AboutPage() {
  return (
    <>
      <Title>About</Title>
      <Meta name="description" content="About this application" />
      <main>About page</main>
    </>
  )
}
```

## Rules of Thumb

- Put shared metadata defaults in `app.tsx`.
- Put route-specific `Title` and `Meta` close to the page that owns them.
- Prefer file routes over manually declared route trees in SolidStart apps.
- Keep route modules page-focused and move reusable UI into separate
  components.
