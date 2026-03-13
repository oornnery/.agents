# SolidJS and Router

Use this reference when building a frontend with `solid-js` and explicit router
setup.

## When to Use

- Single-page applications built directly on Solid.
- Embedded UI or dashboard surfaces that do not need a full app framework.
- Projects that want explicit control over routing with `@solidjs/router`.

## Bootstrap

Create a Solid app with the official starter flow:

```bash
npm create solid@latest
```

Pick the basic Solid template when you do not need SolidStart.

## Core Patterns

Solid uses fine-grained reactivity. Prefer signals and derived expressions over
manual state synchronization.

```tsx
import { createSignal, Show } from 'solid-js'

export default function Counter() {
  const [count, setCount] = createSignal(0)

  return (
    <section>
      <button onClick={() => setCount(count() + 1)}>Increment</button>
      <Show when={count() > 0}>
        <p>Count: {count()}</p>
      </Show>
    </section>
  )
}
```

## Router Setup

Install the router when the app has multiple screens:

```bash
npm install @solidjs/router
```

Minimal setup:

```tsx
import { Route, Router } from '@solidjs/router'
import { render } from 'solid-js/web'

import HomePage from './pages/HomePage'
import SettingsPage from './pages/SettingsPage'

render(
  () => (
    <Router>
      <Route path="/" component={HomePage} />
      <Route path="/settings" component={SettingsPage} />
    </Router>
  ),
  document.getElementById('root')!
)
```

## Routes

Use explicit route trees for plain Solid apps.

- Use `Route` for route definitions.
- Use `A` for internal navigation links.
- Use `useParams` for dynamic path segments.
- Use `lazy` to split route components.

```tsx
import { A, Route, Router, useParams } from '@solidjs/router'
import { lazy } from 'solid-js'

const UserPage = lazy(() => import('./pages/UserPage'))

function UserDetails() {
  const params = useParams()
  return <h1>User {params.id}</h1>
}
```

## Rules of Thumb

- Keep route definitions centralized in plain Solid apps.
- Use `lazy` for page-level code splitting.
- Prefer route params and loader boundaries over ad hoc URL parsing.
- Keep reactive reads inside Solid expressions instead of copying signal values
  into intermediate mutable state.

## Advanced State and Reativity

When state grows complex or requires nested object tracking, upgrade from
`createSignal` to `createStore`.

```tsx
import { createStore } from 'solid-js/store'

function UserSettings() {
  const [user, setUser] = createStore({ name: 'Alice', theme: 'dark' })

  // Update specific fields without spreading the whole object
  const toggleTheme = () => {
    setUser('theme', (t) => (t === 'dark' ? 'light' : 'dark'))
  }
}
```

### Context and Dependency Injection

Avoid prop-drilling by providing state via Context. Best practice is to export
a strongly typed hook to consume it.

```tsx
import { createContext, useContext, JSX } from 'solid-js'

const ThemeContext = createContext<() => string>()

export function ThemeProvider(props: { children: JSX.Element }) {
  const [theme] = createSignal('light')
  return (
    <ThemeContext.Provider value={theme}>
      {props.children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider')
  return ctx
}
```

### Derived State and Side Effects

Use `createMemo` for expensive derived calculations that only need updating when
their dependencies change. Use `createEffect` to synchronize external systems
with Solid state.

```tsx
import { createSignal, createMemo, createEffect } from 'solid-js'

const [firstName, setFirstName] = createSignal('Jane')
const [lastName, setLastName] = createSignal('Doe')

// Recomputes only when firstName or lastName changes
const fullName = createMemo(() => `${firstName()} ${lastName()}`)

createEffect(() => {
  // Automatically tracks reads of fullName() and runs when it changes
  document.title = `Profile: ${fullName()}`
})
```

## Data Fetching

Use `createResource` for querying APIs and bounding loading/error states cleanly
to Suspense and ErrorBoundary components.

```tsx
import { createSignal, createResource, Suspense, ErrorBoundary } from 'solid-js'

async function fetchUser(id: number) {
  const response = await fetch(`/api/users/${id}`)
  if (!response.ok) throw new Error('Failed to fetch user')
  return response.json()
}

function Profile() {
  const [userId, setUserId] = createSignal(1)
  // Re-fetches automatically when userId changes
  const [user, { mutate, refetch }] = createResource(userId, fetchUser)

  return (
    <ErrorBoundary fallback={(err) => <div>Error: {err.message}</div>}>
      <Suspense fallback={<div>Loading...</div>}>
        <section>
          <h1>{user()?.name}</h1>
          <button onClick={() => setUserId(2)}>Load User 2</button>
        </section>
      </Suspense>
    </ErrorBoundary>
  )
}
```
