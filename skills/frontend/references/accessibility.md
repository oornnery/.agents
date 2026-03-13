# Frontend Accessibility

Use this reference to ensure web applications and generic UI components are
accessible to all users, leveraging semantic HTML conventions and robust ARIA
patterns.

## When to Use

- Ensuring the UI meets basic a11y standards (WCAG).
- Creating interactive components (modals, dropdowns, tooltips).
- Providing feedback and error states in forms.
- Managing focus across the application.

## Core Rules

1. Prefer semantic HTML over custom elements (`<button>` instead of `<div onClick>`).
2. Manage focus explicitly when rendering elements conditionally.
3. Keep screen reader announcements explicit, avoiding implicit visual cues.

## Semantic HTML

The browser handles much of accessibility for you if you use the right element.

```tsx
// ❌ Anti-pattern: Missing semantics and keyboard interaction
<div onClick={submit}>Submit</div>

// ✅ Correct: Native semantics, keyboard focus, screen reader description
<button type="submit" onClick={submit}>Submit</button>
```

Always label inputs explicitly:

```tsx
// ❌ Anti-pattern
<input placeholder="Username" />

// ✅ Correct
<label for="username">Username</label>
<input id="username" type="text" />
```

Or visibly hide the label if design dictates:

```tsx
<label for="search" class="sr-only">Search the site</label>
<input id="search" type="search" placeholder="Search..." />
```

## ARIA Attributes

Use WAI-ARIA correctly to communicate structure and state when HTML forms fall
short. Wait until semantic elements are not enough before reaching for ARIA.

- `aria-expanded` on toggle buttons.
- `aria-controls` to link buttons to panels.
- `aria-describedby` for form field hints or validation messages.
- `aria-hidden="true"` on decorative icons to remove them from screen readers.

Example using Basecoat and Tailwind:

```tsx
<button
  aria-expanded={isOpen()}
  aria-controls="menu-dropdown"
  onClick={() => setIsOpen(!isOpen())}
>
  Toggle Menu
</button>

<Show when={isOpen()}>
  <div id="menu-dropdown" role="menu">
    {/* Menu Items */}
  </div>
</Show>
```

## Focus Management

- Use `autofocus` (or focus explicit DOM nodes inside `onMount`) when opening modals.
- Trap focus inside modals so keyboard users cannot navigate behind them.
- Ensure the user's focus returns to the element that triggered the modal when closing.

```tsx
// Using SolidJS ref for focus control
let inputRef: HTMLInputElement | undefined

onMount(() => {
  inputRef?.focus()
})

return <input ref={inputRef} />
```

## Screen Reader Announcements

Use an `aria-live` region (`role="status"` or `role="alert"`) for dynamic updates
like form errors or toast messages.

```tsx
// Tailwind utility class usually named .sr-only
<div aria-live="polite" class="sr-only">
  {message()}
</div>
```

## Forms and Validation

Forms must explicitly link validation errors to inputs so screen reader users
know what to fix.

```tsx
<div>
  <label for="email">Email</label>
  <input
    id="email"
    type="email"
    aria-invalid={hasError()}
    aria-describedby={hasError() ? "email-error" : undefined}
  />
  <Show when={hasError()}>
    <span id="email-error" role="alert" class="text-error">{error()}</span>
  </Show>
</div>
```

## Rules of Thumb

- Check color contrast ratio (preferably 4.5:1).
- Use tools like `eslint-plugin-jsx-a11y` to catch basic errors automatically.
- Do not disable outlines or focus borders (`outline-none`) unless you replace
  them with a custom visual focus state (`focus-visible:ring`).
