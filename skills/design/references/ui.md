# UI

Use when main problem is not styling but keeping interface coherent, scalable, and evolvable.

Rules are framework-agnostic. Examples/impl cues assume Python-friendly stack with server-rendered UI, Jx components, and Tailwind-style tokens.

## When to Use

- creating or evolving design system
- defining tokens, themes, and component primitives
- shaping reusable component APIs
- deciding UI states, accessibility behavior, and responsive rules
- reviewing whether screen or component is consistent with rest of product

## UI Boundary

In scope:

- visual language and token systems
- component architecture and component contracts
- accessibility, states, and interaction patterns
- layout, responsiveness, and motion
- design-to-code handoff and system consistency

Out of scope:

- API route and payload design
- BFF aggregation logic
- domain rules disguised as component behavior

## Design System Layers

Keep system layered so change flows predictably.

```text
brand decisions
  -> semantic tokens
  -> primitive components
  -> composed patterns
  -> screens and flows
```

Rules:

- brand values should not leak directly into every component
- semantic tokens express meaning such as `surface`, `text-muted`, `accent`, `danger`
- primitives solve one UI problem well
- composed patterns combine primitives for product workflows

## Tokens and Themes

### Token Categories

Centralize tokens for:

- color
- spacing
- typography
- radius
- shadow
- border
- motion
- z-index

Use semantic names over raw values:

- good: `surface`, `surface-subtle`, `text`, `text-muted`, `accent`, `danger`
- bad: `blue-500-primary`, `gray-200-card-border`

### Theme Rules

- components should consume tokens, not hardcoded hex values
- separate global tokens from component aliases when that improves clarity
- define light and dark themes intentionally; do not invert colors mechanically
- motion tokens should include both normal and reduced-motion behavior

### Token Hierarchy

```text
raw values
  -> semantic tokens
  -> component-level aliases
```

Example:

```text
oklch(...) -> --color-accent -> button background
```

## Component Architecture

Build from small stable primitives first.

```text
base styles
  -> variants
  -> sizes
  -> states
  -> composition
```

Good primitives:

- button
- input
- textarea
- select
- checkbox
- radio group
- card
- badge
- table shell
- dialog shell

Good compositions:

- search bar
- filter panel
- page header
- empty state
- form section
- data table with toolbar

Rules:

- prefer composition before adding many boolean props
- one primitive should not carry several unrelated product concepts
- if component needs too many flags, split concern

## Component Contract

Each reusable component should answer:

- what problem it solves
- which variants are actual product needs
- which sizes are real and worth maintaining
- which slots, children, or actions it exposes
- which states it must support
- what smallest stable API is

Ask before adding props:

- is this real reusable variant or one-off page customization?
- should this be slot over another prop?
- should this be composition over flag?
- does this change visual appearance, structure, or behavior?

## Variants, Sizes, and Slots

Use small, intentional set.

Good defaults:

- variants: `primary`, `secondary`, `ghost`, `danger`
- sizes: `sm`, `md`, `lg`
- slots: icon, heading, description, actions, footer

Avoid:

- variants that differ only slightly but create long-term maintenance cost
- `is_compact`, `is_small`, `dense`, and `tiny` all existing at once
- component APIs that make composition harder than direct markup

## Required States

Every reusable component should design and document states that matter.

Minimum interactive state set:

- default
- hover
- focus
- active
- disabled

Frequently required product states:

- loading
- empty
- error
- success
- selected
- read-only

Rules:

- if state is not designed, it becomes inconsistent in prod
- loading must preserve layout stability where possible
- empty and error states need real copy, not only icons
- success and error feedback should be adjacent to action or field that caused them

## Accessibility Baseline

- keyboard flow works before visual polish
- focus remains visible
- semantic HTML first; ARIA only when needed
- color is never only signal
- labels, hints, and errors stay associated with right control
- target size and contrast stay usable on dense layouts
- overlays, dialogs, and popovers must preserve escape, dismissal, and focus behavior

Native-first guidance:

- use native buttons, inputs, selects, and forms before custom controls
- use `<dialog>` for true dialogs when stack allows it
- use `<details>` for simple disclosure and accordion behavior
- add custom keyboard behavior only when native behavior is insufficient

## Forms

Forms reveal design debt quickly. Keep them systematic.

Each field should define:

- label
- hint or help text when needed
- valid message
- disabled behavior
- loading or submitting behavior where relevant

Rules:

- required vs optional should be clear without visual clutter
- valid should explain what to fix, not only that something failed
- related controls should group visually and semantically
- long forms need sectioning, progressive disclosure, or both
- destructive actions must not visually resemble primary submit actions

## Data Display

Tables, lists, and dashboards should optimize for scanning first.

Rules:

- typography and spacing should make hierarchy obvious
- numeric data should align predictably
- empty tables and filtered-zero states need explicit copy
- dense data still needs visible focus and hover states
- sorting, filtering, and bulk actions should be discoverable, not hidden in visual noise

For cards, lists, and dashboards:

- keep one dominant action per cluster
- avoid stacking several visual emphasis levels in same region
- use muted surfaces and borders to group info before adding heavier chrome

## Navigation and Overlays

Navigation and overlay patterns should not fight each other.

Rules:

- navigation hierarchy should be obvious from position and emphasis
- drawers, menus, dialogs, and popovers must have clear ownership and dismissal rules
- do not use overlays when in-flow disclosure pattern would be simpler
- nested overlays should be rare and justified

## Responsive Rules

- design mobile intentionally over shrinking desktop layouts
- prefer fluid spacing and container constraints over rigid pixel grids
- test long labels, empty states, dense tables, and valid errors on small screens
- keep overflow behavior explicit; do not let important UI clip by accident
- responsive behavior should preserve task completion, not only layout symmetry

Ask for each breakpoint:

- what becomes hidden?
- what becomes stacked?
- what becomes scrollable?
- what action remains primary?

## Motion

Motion should explain state changes, not decorate them.

Use motion for:

- enter and exit of overlays
- progressive reveal of new content
- feedback after meaningful user action
- orientation when layout changes

Rules:

- keep durations short and purposeful
- preserve reduced-motion support
- do not animate every hover, border, and layout shift by default
- loading indicators should signal progress without becoming visual noise

## Design-to-Code Workflow

1. define tokens first
2. build primitives second
3. compose recurring patterns third
4. test states and accessibility before visual polish
5. document examples and anti-patterns as they appear
6. remove duplicate variants when existing primitive already solves need

Good handoff outputs:

- token names and intent
- component API and slots
- required states
- accessibility notes
- responsive behavior
- examples of correct and incorrect usage

## Python Implementation Cues

When UI is implemented in Python-oriented stack:

- keep templates or components close to semantic HTML
- prefer reusable fragments over page-specific one-offs pretending to be primitives
- let tokens and utility classes express consistency; keep business logic out of component
- if JS is needed, keep it progressively enhanced and narrowly scoped
- for Jx-style component systems, use slots and composition before adding many props

## UI Review Checklist

- tokens are semantic and reused consistently
- primitives solve one UI problem each
- variants and sizes are intentional, not speculative
- required states exist and are visually coherent
- keyboard, focus, and labels work
- mobile behavior is designed, not accidental
- empty, loading, and error states are real
- overlays and menus have clear open and close behavior
- one screen does not invent second design language

## Anti-Patterns

- product-specific components becoming fake primitives
- too many boolean props over clearer composition
- inconsistent spacing and typography between similar screens
- inaccessible custom controls replacing native elements without good reason
- mixing domain logic and visual logic inside component APIs
- adding new variant over fixing underlying primitive
- dark mode implemented as afterthought with broken contrast and state handling
