---
name: design-system
description: Design system patterns — design tokens, component documentation, Figma-to-code workflow, theming, accessibility. Load when building or documenting a frontend design system.
---

# Design System

Patterns for building and documenting a consistent frontend design system.

## Design Tokens

Tokens are the atomic values of a design system. Define them as CSS custom
properties for maximum flexibility.

### Token Categories

```css
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-secondary: #64748b;
  --color-success: #16a34a;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-bg: #ffffff;
  --color-bg-subtle: #f8fafc;
  --color-text: #0f172a;
  --color-text-muted: #64748b;
  --color-border: #e2e8f0;

  /* Spacing (4px base unit) */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;

  /* Borders */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px rgb(0 0 0 / 0.1);
}
```

### Dark Mode

Override tokens with a dark theme:

```css
[data-theme="dark"] {
  --color-bg: #0f172a;
  --color-bg-subtle: #1e293b;
  --color-text: #f1f5f9;
  --color-text-muted: #94a3b8;
  --color-border: #334155;
}
```

Toggle via JavaScript:

```javascript
document.documentElement.dataset.theme =
  document.documentElement.dataset.theme === "dark" ? "light" : "dark";
```

## Component States

Every interactive component must define these states:

| State    | Visual Change                   | Trigger              |
| -------- | ------------------------------- | -------------------- |
| Default  | Base appearance                 | No interaction       |
| Hover    | Subtle highlight, cursor change | Mouse hover          |
| Focus    | Visible ring/outline            | Keyboard focus       |
| Active   | Pressed/depressed appearance    | Click/tap            |
| Disabled | Muted, no pointer events        | `disabled` attribute |
| Loading  | Spinner or skeleton             | Async operation      |
| Error    | Red border/text, error message  | Validation failure   |

```css
.btn {
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-4);
}
.btn:hover { background: var(--color-primary-hover); }
.btn:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
.btn:active { transform: scale(0.98); }
.btn:disabled { opacity: 0.5; pointer-events: none; }
```

## Component Documentation

Each component should have:

### Props Table

| Prop       | Type                                  | Default     | Description         |
| ---------- | ------------------------------------- | ----------- | ------------------- |
| `variant`  | `"primary" \| "secondary" \| "ghost"` | `"primary"` | Visual style        |
| `size`     | `"sm" \| "md" \| "lg"`                | `"md"`      | Button size         |
| `disabled` | `boolean`                             | `false`     | Disable interaction |
| `loading`  | `boolean`                             | `false`     | Show loading state  |

### Variants

```text
[Primary]  [Secondary]  [Ghost]  [Danger]
```

### Examples

Show usage in context:

```html
<!-- Basic -->
<Button variant="primary">Save</Button>

<!-- With icon -->
<Button variant="secondary"><Icon name="edit" /> Edit</Button>

<!-- Loading state -->
<Button loading>Saving...</Button>
```

## Figma to Code Workflow

### From Figma Design to Implementation

1. **Extract tokens** — colors, spacing, typography from Figma styles
2. **Map components** — Figma components → code components (1:1 mapping)
3. **Define props** — Figma variants → component props
4. **Implement states** — hover, focus, active, disabled
5. **Test accessibility** — contrast ratios, keyboard navigation

### Naming Convention

Keep Figma names aligned with code names:

| Figma                    | Code                                   |
| ------------------------ | -------------------------------------- |
| Button / Primary / Large | `<Button variant="primary" size="lg">` |
| Card / Elevated          | `<Card elevation="raised">`            |
| Input / Error / Filled   | `<Input state="error" filled>`         |

## Accessibility (WCAG 2.1 AA)

### Requirements

- **Color contrast**: 4.5:1 for normal text, 3:1 for large text
- **Focus indicators**: visible focus ring on all interactive elements
- **Keyboard navigation**: all interactive elements reachable via Tab
- **Screen readers**: semantic HTML, ARIA labels where needed
- **Motion**: respect `prefers-reduced-motion`

### Checklist

- [ ] All images have `alt` text (or `alt=""` for decorative)
- [ ] Form inputs have associated `<label>` elements
- [ ] Error messages are announced to screen readers (`role="alert"`)
- [ ] Color is not the only indicator of state (add icons or text)
- [ ] Interactive elements have min 44x44px touch target
- [ ] Focus order follows visual layout
- [ ] Modal traps focus within the dialog

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Responsive Breakpoints

```css
/* Mobile first */
--breakpoint-sm: 640px;   /* Small tablets */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Laptops */
--breakpoint-xl: 1280px;  /* Desktops */
```

With Tailwind: `sm:`, `md:`, `lg:`, `xl:` prefixes.

## Component Inventory

Track all components and their status:

| Component | Status      | Variants | A11y    | Tests |
| --------- | ----------- | -------- | ------- | ----- |
| Button    | Done        | 4        | Pass    | Yes   |
| Input     | Done        | 3        | Pass    | Yes   |
| Select    | In progress | 2        | Pending | No    |
| Modal     | Planned     | -        | -       | -     |
| Toast     | Planned     | -        | -       | -     |

## Related

- `skills/frontend/SKILL.md` — frontend tooling, Solid, Tailwind
- `skills/jx/SKILL.md` — Jinja component patterns
- `skills/frontend/references/accessibility.md` — detailed a11y guide
- `skills/frontend/references/tailwind.md` — Tailwind patterns
