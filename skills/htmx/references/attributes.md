# htmx Attributes

## Request Attributes

| Attribute   | Purpose        | Example                |
| ----------- | -------------- | ---------------------- |
| `hx-get`    | GET request    | `hx-get="/users"`      |
| `hx-post`   | POST request   | `hx-post="/users"`     |
| `hx-put`    | PUT request    | `hx-put="/users/1"`    |
| `hx-patch`  | PATCH request  | `hx-patch="/users/1"`  |
| `hx-delete` | DELETE request | `hx-delete="/users/1"` |

Prefer noun-based URLs, normal HTTP semantics.

## Trigger Patterns

Use `hx-trigger` to control when requests fire.

Common patterns:

```html
<input
  hx-get="/search"
  hx-trigger="keyup changed delay:300ms"
  hx-target="#results"
>
```

```html
<div
  hx-get="/items?page=2"
  hx-trigger="revealed"
  hx-swap="afterend"
>
  Loading more...
</div>
```

Useful modifiers:

- `changed`
- `delay:300ms`
- `throttle:500ms`
- `once`
- `from:<selector>`
- `target:<selector>`
- `queue:first|last|all|none`

## Target Rules

Use `hx-target` to pick smallest stable surface to update.

Prefer:

- `#results`
- `#form-errors`
- `closest tr`
- `this`

Avoid fragile selectors dependent on incidental DOM structure.

## Swap Rules

Default `innerHTML` unless another boundary clearer.

Common values:

- `innerHTML`
- `outerHTML`
- `beforebegin`
- `afterbegin`
- `beforeend`
- `afterend`
- `delete`
- `none`

Common modifiers:

- `swap:200ms`
- `settle:200ms`
- `scroll:top`
- `show:top`

## History and Navigation

Use history only when interaction should behave like navigation.

- `hx-push-url="true"` when new state deserves history entry
- `hx-replace-url="true"` when state should not grow history

Good fits:

- filter state worth sharing
- pagination
- detail panels that function like navigation

Bad fits:

- transient validation
- one-off loading spinners
- tiny inline component state

## Indicators and Disabled State

Use `hx-indicator` and `hx-disabled-elt` so request state visible.

```html
<form
  hx-post="/users"
  hx-target="#user-form"
  hx-disabled-elt="find button"
  hx-indicator="#saving"
>
  ...
</form>
<div id="saving" class="htmx-indicator">Saving...</div>
```

## Synchronization

Use `hx-sync` when multiple requests can fight each other.

Common patterns:

- `closest form:abort`
- `this:drop`
- `this:replace`
- `this:queue last`

Matters for:

- autosave
- validation plus submit
- repeated clicks on same action

## OOB Updates

Use out-of-band swaps only when one server action should update more than one surface.

```html
<div id="notification" hx-swap-oob="true">Saved</div>
```

Keep them explicit, sparse.

## Guardrails

- do not stack many `hx-*` concerns on one element if interaction becomes unreadable
- do not use `outerHTML` on unstable component roots without checking focus and event implications
- do not poll when event-driven updates or user-triggered refresh would be enough