# Frontend JavaScript/TypeScript Security Spec (Vanilla Browser JS/TS)

## Constraints

- MUST NOT output/log/hard-code/commit secrets. Frontend code is observable by end users.
- "Public" keys (publishable analytics keys) MUST be scoped accordingly.
- MUST NOT "fix" security by disabling protections (weakening CSP, removing origin checks, switching to `innerHTML`, etc.).
- MUST provide evidence-based findings (file paths, snippets, config values).
- If security headers might be set by server/edge/CDN, report as "not visible here; verify at runtime/edge config." Note: `<meta http-equiv>` only supports a subset of headers.

## Audit finding format

Rule ID | Severity | Location (file+function+line) | Evidence (snippet) | Impact | Fix (minimal diff) | Mitigation | False positive notes

## Audit order

1. HTML entrypoints, script/style includes, CSP delivery (header vs meta)
2. DOM XSS sinks (`innerHTML`, `document.write`, `insertAdjacentHTML`, event-handler attrs) and their data sources
3. Navigation/redirect handling (`window.location*`, link targets, `javascript:` URLs)
4. Cross-origin communication (`postMessage`, iframe sandboxing)
5. Storage of sensitive data (localStorage/sessionStorage)
6. Third-party scripts, tag managers, CDNs, SRI, CSP
7. DOM clobbering gadgets (`window`/`document` named properties)

## Untrusted input sources

- URL-derived: `location.href`, `.search`, `.hash`, `document.baseURI`, `URLSearchParams`
- DOM content: user-controlled markup (comments, profiles, CMS, markdown-to-HTML)
- `postMessage` `event.data` and `event.origin`
- Browser storage: `localStorage`, `sessionStorage`, IndexedDB (attacker-influenceable via XSS)
- Network responses (may contain stored attacker content)

## Dangerous sinks

- HTML parsing: `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write/writeln`
- Code execution: `eval`, `new Function`, `setTimeout("...")`, `setInterval("...")`
- Navigation: `javascript:` URLs via `Location.href`/`window.location`/link `href`
- Event handler attrs from strings: `setAttribute("onclick", "...")`

---

## Production baseline

### CSP baseline (SHOULD; MUST for high-risk apps)

- Prefer HTTP header delivery. MAY use `<meta http-equiv="Content-Security-Policy">` if headers unavailable.
- Meta CSP limitations: must appear before governed scripts; `report-uri`, `frame-ancestors`, `sandbox` NOT supported in meta; report-only not available via meta.
- Avoid `unsafe-inline` and `unsafe-eval`. Prefer nonce/hash-based script policies.
- Consider Trusted Types enforcement.

### Third-party scripts (SHOULD)

- Treat as equivalent privilege to first-party JS.
- Use SRI for CDN-hosted scripts/styles.

### Cross-window communication (SHOULD)

- Restrict `postMessage` to explicit origins; validate origin and message shape.

---

## Rules

### JS-XSS-001: No untrusted HTML via `innerHTML` and friends (Critical/Medium)

- `innerHTML`, `outerHTML`, `insertAdjacentHTML` are dangerous sinks.
- MUST use `textContent` for text, `createElement`/`appendChild`/`setAttribute` for DOM.
- If HTML insertion required: sanitize with allowlist-based sanitizer, enforce Trusted Types.
- Detect: `.innerHTML`, `.outerHTML`, `insertAdjacentHTML(`. Trace origin of inserted string.

### JS-XSS-002: No `document.write`/`writeln` (Critical/Medium)

- MUST avoid in production code.
- If legacy unavoidable: ensure no untrusted input reaches it, enforce Trusted Types.
- Detect: `document.write(`, `document.writeln(`.
- Fix: Replace with `createElement`/`appendChild`/`textContent`.

### JS-XSS-003: No string-to-code execution (Critical/Medium)

- MUST NOT pass untrusted data to `eval()`, `new Function(...)`, `setTimeout("...")`/`setInterval("...")`.
- SHOULD avoid these APIs entirely. MUST NOT add `unsafe-eval` to CSP as a fix.
- Fix: structured data + explicit handlers; `JSON.parse` instead of `eval` for JSON.

### JS-XSS-004: No event handler attributes from strings (High)

- MUST NOT use `setAttribute("on...", string)` with untrusted data.
- SHOULD use `addEventListener` with function references.
- Detect: `.setAttribute("on`, `.onclick =`, `.onmouseover =` etc.

### JS-URL-001: Sanitize URLs before navigation (Low; High if fully attacker-controlled)

NOTE: High false-positive rate. Only flag if URL is fully attacker-controlled.

- MUST prevent `javascript:` URLs. Only allow `http:`/`https:`.
- Applies to: `window.location`, `location.href`, `.assign()`, `.replace()`.
- SHOULD validate: same-origin relative paths or strict origin allowlist.
- Fix: `new URL(value, location.origin)` then check `url.protocol` and `url.origin`.
- Some apps intentionally support external redirects (SSO, payments) -- those MUST be allowlisted.

### JS-URL-002: Sanitize URLs in DOM attributes (`href`, `src`, etc.) (Low/High)

NOTE: High false-positive rate. Only flag if URL is fully attacker-controlled.

- MUST prevent `javascript:`/active schemes in `a.href`, `img.src`, `script.src`, `iframe.src`, `form.action`, `link.href`.
- Never pass user-provided values into `<script src>`.
- Fix: `new URL(...)` + protocol allowlist.
- Detect: `.href =`, `.src =`, `.action =`, `setAttribute("href"`, `setAttribute("src"`.

### JS-CSP-001: Use CSP; meta delivery allowed (Medium/High)

NOTE: `script-src` is the most important directive; others can be excluded for dev ease.

- SHOULD deploy CSP. MAY use meta delivery.
- Meta: place early; cannot use `report-uri`, `frame-ancestors`, `sandbox`.
- MUST NOT add `unsafe-inline` or `unsafe-eval` without explicit reviewed justification.
- Detect: `<meta http-equiv="Content-Security-Policy"`, server/edge CSP configs.

### JS-CSP-002: Strict CSP (nonces/hashes) (Medium)

- SHOULD design code to work under strict CSP: no inline scripts/handlers, no eval.
- Allow scripts via nonce or hash.
- Detect: inline `<script>` blocks, `onclick="..."`, CSP with `unsafe-inline`/`unsafe-eval`.

### JS-TT-001: Trusted Types (Low)

- SHOULD consider `require-trusted-types-for 'script'` to reject raw strings at DOM sinks.
- Use `trusted-types` directive to restrict policy creation.
- Policy code must be small, heavily reviewed.
- Trusted Types is not universal -- targets DOM injection sinks only.
- Detect: `trustedTypes.createPolicy(` and inspect implementations.

### JS-MSG-001: `postMessage` origin validation (Medium/High)

- Sending: MUST set explicit `targetOrigin` (not `*`).
- Receiving: MUST validate `event.origin` exactly (no substring matching), validate `event.data` schema, treat as data only (never `innerHTML`).
- SHOULD validate `event.source` when applicable.

```javascript
// Fix pattern
const ALLOWED = new Set(["https://app.example.com"]);
// or: new Set([window.location.origin])
window.addEventListener("message", (e) => {
  if (!ALLOWED.has(e.origin)) return;
  // validate e.data schema, reject unknown fields
});
// Send: otherWindow.postMessage(payload, "https://app.example.com");
```

- Detect: `postMessage(` with `"*"`, `addEventListener("message"` without origin check.

### JS-STORAGE-001: Web Storage is not safe for secrets (Low)

- MUST NOT store session IDs or sensitive secrets in `localStorage`/`sessionStorage` (single XSS exfiltrates all).
- MUST treat storage values as untrusted input.
- SHOULD use `HttpOnly` cookies for session identifiers.
- Detect: `localStorage.setItem/getItem`, `sessionStorage.*` with keys named `token`, `jwt`, `session`, `auth`, `refresh`.

### JS-SUPPLY-001: Third-party JS supply-chain risk (Low)

- Third-party JS has full first-party privilege.
- SHOULD minimize, self-host/mirror, use strict CSP allowlists, use SRI.
- Detect: `<script src="https://...">` without `integrity=`, tag manager snippets, dynamic script injection (`createElement("script")`).

### JS-SRI-001: Subresource Integrity (Low)

- SHOULD use SRI (`integrity="sha384-..."`) for third-party scripts/styles.
- Pin versions; avoid "latest" URLs.
- Detect: `<script src="https://` and `<link href="https://` without `integrity=`.

### FS-DOMC-001: DOM clobbering (Medium/High/Critical)

- MUST NOT rely on `window.someName`/`document.someName` lookups that can be clobbered by injected HTML elements with matching `id`/`name`.
- Dangerous pattern: `let x = window.redirectTo || "/safe"; location.assign(x);` -- attacker injects `<a id="redirectTo" href="javascript:...">`.
- SHOULD use explicit variable declarations, local scope, `getElementById`.
- Detect: `window.<name> || ...` fallback patterns, `location.assign/replace` with `window`/`document` property sources, dynamic script creation with `.src` from non-local variable.
- Fix: module-scoped constants, not `window`/`document`; validate URLs with protocol/origin allowlists.

---

## Scanning grep patterns

| Category       | Patterns                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| DOM XSS sinks  | `.innerHTML`, `.outerHTML`, `insertAdjacentHTML(`, `document.write(`, `document.writeln(`               |
| Navigation/URL | `window.location`, `location.href`, `.assign`, `.replace`, `javascript:`                                |
| Code execution | `eval(`, `new Function`, `setTimeout("`, `setInterval("`                                                |
| Event handlers | `.setAttribute("on`, `.onclick =`, `.onload =`                                                          |
| postMessage    | `postMessage(` with `"*"`, `addEventListener("message"` without origin check                            |
| Storage        | `localStorage.setItem/getItem`, `sessionStorage.*`, keys: `token`, `jwt`, `session`, `auth`             |
| CSP            | `Content-Security-Policy`, `<meta http-equiv="Content-Security-Policy"`, `unsafe-inline`, `unsafe-eval` |
| Third-party    | `<script src="https://...">` without `integrity=`, tag managers, `createElement("script")`              |
| DOM clobbering | `window.<name> \|\| ...`, `document.<name> \|\| ...`, `location.assign` with window props               |

Confirm for each: data origin, sink type, protective controls present.

---

## Sources

- [W3C CSP Level 2](https://www.w3.org/TR/CSP2/) | [MDN CSP Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) | [MDN meta http-equiv](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/http-equiv) | [MDN frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors)
- [OWASP DOM XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html) | [MDN innerHTML](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML) | [MDN insertAdjacentHTML](https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML) | [MDN document.write](https://developer.mozilla.org/en-US/docs/Web/API/Document/write)
- [MDN javascript: URLs](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Schemes/javascript)
- [W3C Trusted Types](https://www.w3.org/TR/trusted-types/) | [MDN require-trusted-types-for](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for) | [MDN trusted-types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/trusted-types)
- [MDN postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) | [OWASP HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)
- [OWASP Third Party JS](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html) | [MDN SRI](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity) | [W3C SRI](https://www.w3.org/TR/sri-2/)
- [OWASP DOM Clobbering](https://cheatsheetseries.owasp.org/cheatsheets/DOM_Clobbering_Prevention_Cheat_Sheet.html)
