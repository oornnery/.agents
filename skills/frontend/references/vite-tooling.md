# Vite Tooling and Optimizations

Use this reference when configuring build tools, environment variables, aliases,
and optimizing bundles in Vite-based applications.

## When to Use

- Initializing Vite configuration for SolidJS or SolidStart projects.
- Migrating from Webpack or Create React App to Vite conventions.
- Setting up path aliases (`~/*`, `@/*`).
- Optimizing code splitting and asset processing.

## Base Configuration

SolidJS projects typically use `vite-plugin-solid`.
SolidStart apps use `@solidjs/start/config`.

```typescript
// vite.config.ts for Plain Solid
import { defineConfig } from 'vite'
import solidPlugin from 'vite-plugin-solid'

export default defineConfig({
  plugins: [solidPlugin()],
  server: {
    port: 3000,
  },
  build: {
    target: 'esnext',
  },
})
```

## Path Aliases

Simplify imports by configuring path aliases in both `vite.config.ts` and
`tsconfig.json`.

**vite.config.ts:**

```typescript
import { resolve } from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '~': resolve(__dirname, './src'),
    },
  },
})
```

**tsconfig.json:**

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "~/*": ["src/*"]
    }
  }
}
```

## Environment Variables

Vite exposes environment variables on `import.meta.env` and require the
`VITE_` prefix to be available to client-side code.

```env
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My Application
```

Use them in code safely:

```typescript
const apiUrl = import.meta.env.VITE_API_URL
```

To get TypeScript support for custom environment variables, add an `env.d.ts` file:

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_TITLE: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

## Optimization and Code Splitting

- Route components should be lazy-loaded using `lazy` from Solid.
- Shared vendor chunks can be managed using Rollup's `manualChunks` configuration
  inside the `build` options.

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          solid: ['solid-js', '@solidjs/router'],
        },
      },
    },
  },
})
```

## Proxy Server for Development

When developing against an API that does not support CORS natively, use Vite's
dev server proxy to forward requests.

```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

This ensures that requests to `/api/*` are forwarded transparently to the backend
(e.g., a FastAPI application).
