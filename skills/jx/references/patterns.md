# Component Patterns

Ready-made patterns for common UI components. Each pattern uses platform
features first (native `<dialog>`, Popover API, HTML validation) and layers
JX for composition. Colors shown are illustrative -- swap for semantic tokens
(`accent`, `danger`, `success`, `warn`) in real projects.

## Buttons

Renders as `<a>` when `href` is provided, `<button>` otherwise. A variants
dict keeps all color schemes in one place. `attrs.render()` merges caller
classes with defaults so extra Tailwind or HTMX attributes pass through.

```html+jinja
{#def
  label="",
  variant="primary",
  size="md",
  href=""
#}

{% set base = "Button inline-flex items-center justify-center font-medium rounded-lg transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-current disabled:opacity-50 disabled:pointer-events-none cursor-pointer" %}

{% set variants = {
  "primary": "bg-indigo-600 text-white hover:bg-indigo-700",
  "secondary": "bg-gray-100 text-gray-800 hover:bg-gray-200",
  "danger": "bg-red-600 text-white hover:bg-red-700",
  "ghost": "text-gray-700 hover:bg-gray-100",
  "outline": "border border-gray-300 text-gray-700 hover:bg-gray-50",
} %}

{% if href %}
  <a href="{{ href }}" {{ attrs.render(class=base ~ " " ~ variants[variant]) }}>
    {{ label if label else content }}
  </a>
{% else %}
  <button {{ attrs.render(class=base ~ " " ~ variants[variant], type="button") }}>
    {{ label if label else content }}
  </button>
{% endif %}
```

Key decisions:

- **Variant dict** -- all visual variants live in a single dict. Add new
  variants by adding a key; no extra conditionals needed. See the variant
  pattern in `organization-and-patterns.md` for the general rule.
- **`cursor-pointer`** on base -- browsers do not always inherit it,
  especially on `<a>` tags styled as buttons.
- **`type="button"` default** -- prevents accidental form submission when the
  button is inside a `<form>`. Callers can override via `attrs` when they need
  `type="submit"`.
- **`label` or `content`** -- simple text goes in `label`; rich markup goes
  between the opening and closing tags and lands in `content`.

## Modals

Uses the native `<dialog>` element. No JavaScript is needed for the close
button -- `<form method="dialog">` with a submit button closes the dialog
natively. `closedby="any"` allows closing via Escape key and backdrop click.

```html+jinja
{#css transitions.css #}
{#def id, title="" #}

<dialog id="{{ id }}" closedby="any"
  {{ attrs.render(class="Dialog bg-white rounded-xl shadow-xl max-w-lg w-full p-0") }}
>
  <div class="flex items-center justify-between p-4 border-b border-gray-200">
    {% slot header %}
      {% if title %}<h2 class="text-lg font-semibold text-gray-900">{{ title }}</h2>{% endif %}
    {% endslot %}
    <form method="dialog">
      <button type="submit" class="p-1 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 cursor-pointer" aria-label="Close" autofocus>
        <svg class="size-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
        </svg>
      </button>
    </form>
  </div>
  <div class="p-4">{{ content }}</div>
  {% slot footer %}{% endslot %}
</dialog>
```

Key decisions:

- **`closedby="any"`** -- enables Escape and light-dismiss (backdrop click)
  without writing any JavaScript.
- **`<form method="dialog">`** -- the close button lives inside a dialog-method
  form. Clicking submit closes the dialog natively. Zero JS.
- **`autofocus` on the close button** -- when the dialog opens, focus lands on
  the close button for keyboard accessibility.
- **`{#css transitions.css #}`** -- declares a shared CSS asset for open/close
  animations. JX deduplicates it across components.
- **Cancel buttons inside forms** -- when a modal wraps a real form and you need
  a cancel button that closes without submitting, add `formmethod="dialog"` and
  `formnovalidate` to the cancel button:

```html+jinja
<form action="/save" method="post">
  <input name="title" required />
  <button type="submit">Save</button>
  <button type="submit" formmethod="dialog" formnovalidate>Cancel</button>
</form>
```

  `formmethod="dialog"` overrides the form's action and closes the dialog.
  `formnovalidate` prevents required-field errors on cancel.

## Dropdowns

Uses the Popover API (`popover` attribute + `popovertarget`). The browser
handles show/hide, light-dismiss, and top-layer stacking -- no JS needed for
basic menus.

```html+jinja
{#def id, label="Menu" #}

<div {{ attrs.render(class="Dropdown relative inline-block") }}>
  <button popovertarget="{{ id }}" class="inline-flex items-center gap-1.5 px-3 py-2 text-sm font-medium rounded-lg border border-gray-300 hover:bg-gray-50 cursor-pointer">
    {{ label }}
    <svg class="size-4" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
    </svg>
  </button>
  <div id="{{ id }}" popover class="m-0 absolute top-full left-0 mt-1 min-w-48 bg-white rounded-lg shadow-lg ring-1 ring-gray-200 p-1">
    {{ content }}
  </div>
</div>
```

Key decisions:

- **`popover` (auto mode)** -- the default `popover` attribute is equivalent to
  `popover="auto"`. It light-dismisses on outside click and closes other
  auto-popovers, which is the correct behavior for menus.
- **`popover="manual"`** -- use manual mode for JS-controlled scenarios like a
  combobox or autocomplete where you need to show/hide the popover
  programmatically via `showPopover()` / `hidePopover()` without
  light-dismiss interference.
- **Top-layer rendering** -- popover content renders in the top layer, so it
  escapes `overflow: hidden` containers. The `m-0 absolute` positioning is
  relative to the wrapper `<div>` for visual alignment.

## Form Inputs

Lean on native HTML validation first (`required`, `pattern`, `type`). The
component handles error-state styling and label rendering.
`attrs.setdefault(id=name)` ensures there is always an `id` for the
`<label>` `for` attribute, but callers can override it.

```html+jinja
{#def name, label="", type="text", required=false, error="" #}

{% do attrs.setdefault(id=name) %}

<div class="space-y-1.5">
  {% if label %}
    <label for="{{ attrs.get('id', name) }}" class="block text-sm font-medium text-gray-700">
      {{ label }}
      {% if required %}<span class="text-red-500">*</span>{% endif %}
    </label>
  {% endif %}
  <input {{ attrs.render(
    type=type, name=name, required=required,
    class="block w-full rounded-lg border px-3 py-2 text-sm shadow-sm focus:outline-2 focus:outline-indigo-500 " ~
      ("border-red-300 text-red-900 placeholder:text-red-300" if error else "border-gray-300 text-gray-900 placeholder:text-gray-400")
  ) }} />
  {% if error %}<p class="text-sm text-red-600">{{ error }}</p>{% endif %}
</div>
```

Key decisions:

- **`attrs.setdefault(id=name)`** -- sets `id` only when the caller has not
  already passed one. This keeps the `<label for>` wired up without forcing a
  specific ID.
- **Native validation first** -- `required`, `pattern`, `type="email"`, and
  other HTML validation attributes pass through `attrs`. Use them before
  reaching for JS validation.
- **Error state styling** -- the ternary in the `class` string swaps border and
  text colors when `error` is truthy. The error message renders below the input
  only when present.
- **Caller passthrough** -- attributes like `placeholder`, `pattern`,
  `minlength`, `maxlength`, `hx-validate`, and `autocomplete` all flow through
  `attrs.render()` without needing to be declared in `{# def #}`.

## Data Tables

Headers and rows are passed as lists. Optional `striped` and `hoverable`
flags control visual treatment. For complex cell content, use slot-based
markup instead of the simple list-of-lists approach.

```html+jinja
{#def headers=[], rows=[], striped=true, hoverable=true #}

<div {{ attrs.render(class="overflow-x-auto rounded-lg border border-gray-200") }}>
  <table class="min-w-full divide-y divide-gray-200 text-sm">
    {% if headers %}
      <thead class="bg-gray-50">
        <tr>
          {% for header in headers %}<th class="px-4 py-3 text-left font-semibold text-gray-700">{{ header }}</th>{% endfor %}
        </tr>
      </thead>
    {% endif %}
    <tbody class="divide-y divide-gray-100">
      {% for row in rows %}
        <tr class="{{ 'bg-gray-50/50' if striped and loop.index is odd else '' }} {{ 'hover:bg-gray-50' if hoverable else '' }}">
          {% for cell in row %}<td class="px-4 py-3 text-gray-600">{{ cell }}</td>{% endfor %}
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
```

Key decisions:

- **Simple data path** -- `headers` is a flat list of strings; `rows` is a list
  of lists. This covers the majority of data tables.
- **Slot-based markup for complex cells** -- when cells need links, badges,
  or action buttons, skip the `rows` prop and use `content` with raw `<tr>`
  / `<td>` markup instead. Import the table component and fill the body
  slot directly:

```html+jinja
{# import "DataTable.jinja" as DataTable #}
{# import "Badge.jinja" as Badge #}

<DataTable headers={{ ["Name", "Status", "Actions"] }}>
  {% for user in users %}
    <tr>
      <td class="px-4 py-3">{{ user.name }}</td>
      <td class="px-4 py-3"><Badge variant={{ user.status }}>{{ user.status }}</Badge></td>
      <td class="px-4 py-3"><a href="/users/{{ user.id }}">Edit</a></td>
    </tr>
  {% endfor %}
</DataTable>
```

- **Striping uses `loop.index`** -- Jinja's `loop.index` is 1-based, so odd
  rows get the alternating background.
- **`overflow-x-auto`** on the wrapper -- ensures wide tables scroll
  horizontally on small screens without breaking layout.

## Sidebar Layout

Responsive pattern: a persistent sidebar on desktop, a `<dialog>` drawer on
mobile. The mobile drawer slides in from the left using a CSS transition
class and closes via native `<form method="dialog">`.

```html+jinja
{#import "./sidebar_nav.jinja" as SidebarNav #}
{#css transitions.css #}
{#def title="", nav_items=[], current="" #}

<div {{ attrs.render(class="lg:flex min-h-screen") }}>
  <header class="sticky top-0 z-30 flex items-center justify-between bg-white border-b border-gray-200 px-4 py-3 lg:hidden">
    <span class="text-lg font-semibold text-gray-900">{{ title }}</span>
    <button type="button" onclick="document.getElementById('mobile-nav').showModal()" class="p-2 rounded-lg text-gray-600 hover:bg-gray-100 cursor-pointer" aria-label="Open menu">
      <svg class="size-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
      </svg>
    </button>
  </header>
  <dialog id="mobile-nav" closedby="any" class="slide-from-left fixed inset-0 z-40 m-0 h-full w-72 max-h-full max-w-full bg-white p-0 shadow-xl lg:hidden">
    <div class="flex items-center justify-between p-4 border-b border-gray-200">
      <span class="text-lg font-semibold text-gray-900">{{ title }}</span>
      <form method="dialog">
        <button type="submit" class="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 cursor-pointer" aria-label="Close menu">
          <svg class="size-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
      </form>
    </div>
    <nav class="flex-1 overflow-y-auto p-4">
      <SidebarNav items={{ nav_items }} current={{ current }} />
    </nav>
  </dialog>
  <aside class="hidden lg:flex lg:flex-col lg:w-64 lg:shrink-0 bg-white border-r border-gray-200">
    <div class="flex items-center h-16 px-6 border-b border-gray-200">
      <span class="text-lg font-semibold text-gray-900">{{ title }}</span>
    </div>
    <nav class="flex-1 overflow-y-auto p-4">
      <SidebarNav items={{ nav_items }} current={{ current }} />
    </nav>
    {% slot sidebar_footer %}{% endslot %}
  </aside>
  <main class="flex-1 min-w-0 p-6 lg:p-8">{{ content }}</main>
</div>
```

Key decisions:

- **Desktop sidebar** -- `hidden lg:flex` shows the `<aside>` only at `lg` and
  above. The sidebar has a fixed width (`lg:w-64`) and `lg:shrink-0` to prevent
  flex compression.
- **Mobile drawer** -- uses `<dialog>` with `showModal()` for a full modal
  overlay. The `slide-from-left` CSS class (from `transitions.css`) animates the
  drawer entrance.
- **`closedby="any"`** -- allows closing the mobile drawer with Escape or
  backdrop click, matching user expectations for drawers.
- **`<form method="dialog">`** -- the close button uses the same zero-JS
  pattern as the modal component.
- **Shared nav component** -- `SidebarNav` is imported once and used in both
  the mobile drawer and the desktop sidebar. This avoids duplicating navigation
  markup.
- **`{% slot sidebar_footer %}`** -- optional slot at the bottom of the desktop
  sidebar for user profile, settings link, or version info.
