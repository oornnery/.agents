---
name: design-system
description: Design system patterns -- design tokens, component documentation, Figma-to-code workflow, theming, accessibility. Load when building or documenting a frontend design system.
---

# Design System

Patterns for building a consistent frontend design system.

## Design Tokens

Define as CSS custom properties (4px base unit):

```css
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-bg: #ffffff;
  --color-text: #0f172a;
  --color-border: #e2e8f0;

  /* Spacing */
  --space-1: 0.25rem;  --space-2: 0.5rem;
  --space-4: 1rem;     --space-8: 2rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Borders and Shadows */
  --radius-md: 0.375rem;
  --shadow-md: 0 4px 6px rgb(0 0 0 / 0.1);
}
```

### Dark Mode

Override tokens with `[data-theme="dark"]` selector.

## Component States

Every interactive component must define: Default, Hover, Focus,
Active, Disabled, Loading, Error.

## Component Documentation

Each component needs: Props table, Variants, Usage examples.

## Figma to Code

1. Extract tokens from Figma styles
2. Map Figma components to code components (1:1)
3. Map Figma variants to component props
4. Implement all interaction states
5. Test accessibility

## Accessibility (WCAG 2.1 AA)

- Contrast: >=4.5:1 normal text, >=3:1 large text
- Visible focus ring on all interactive elements
- Keyboard navigation via Tab for all interactive elements
- Semantic HTML, ARIA labels where needed
- Respect `prefers-reduced-motion`
- Min 44x44px touch targets
- Color is not the only state indicator

## Responsive Breakpoints

`sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px` (mobile first).

## Related

- `skills/frontend/SKILL.md` -- frontend tooling, Solid, Tailwind
- `skills/frontend/references/accessibility.md` -- detailed a11y guide
