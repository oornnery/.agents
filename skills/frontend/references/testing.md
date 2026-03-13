# Frontend Testing

Use this reference for testing frontend code, primarily focusing on Vitest and
Solid Testing Library.

## When to Use

- Setting up test runners for Solid or SolidStart applications.
- Writing unit and integration tests for UI components.
- Mocking API calls and asserting reactive state changes.

## Vitest Setup

Vitest is the recommended test runner for Vite-based projects.

```bash
npm install -D vitest @solidjs/testing-library jsdom @testing-library/jest-dom
```

Configure `vitest.config.ts`:

```ts
import { defineConfig } from 'vitest/config'
import solidPlugin from 'vite-plugin-solid'

export default defineConfig({
  plugins: [solidPlugin()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./setupVitest.ts'],
    isolate: false,
  },
})
```

Create `setupVitest.ts` for DOM assertions:

```ts
import '@testing-library/jest-dom'
```

## Testing Components

Use `@solidjs/testing-library` to render and interact with components.

```tsx
import { render, screen, fireEvent } from '@solidjs/testing-library'
import Counter from './Counter'

describe('Counter Component', () => {
  it('increments value', async () => {
    render(() => <Counter />)
    const button = screen.getByRole('button', { name: /increment/i })

    expect(screen.getByText('Count: 0')).toBeInTheDocument()

    await fireEvent.click(button)

    expect(screen.getByText('Count: 1')).toBeInTheDocument()
  })
})
```

## Testing Asynchronous Behavior

Solid Testing Library provides utilities like `findBy*` and `waitFor` to handle
asynchronous state updates and data fetching.

```tsx
import { render, screen, waitFor } from '@solidjs/testing-library'
import { UserProfile } from './UserProfile'

describe('UserProfile', () => {
  it('loads and displays user data', async () => {
    // Assuming API is mocked
    render(() => <UserProfile id={1} />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
    })
  })
})
```

## Rules of Thumb

- Test behavior, not implementation details.
- Use `screen.getByRole` or `screen.getByText` instead of querying by test IDs
  or DOM structure when possible.
- Use `fireEvent` to simulate user interactions.
- Remember to clean up DOM after each test (done automatically by the library).
