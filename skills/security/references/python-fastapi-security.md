# FastAPI (Python) Web Security Spec (FastAPI 0.128.x, Python 3.x) ([PyPI][1])

Security spec for FastAPI code generation and auditing. Normative
requirements (MUST/SHOULD/MAY) plus audit rules (bad patterns, detection,
remediation). Covers Starlette + Pydantic layers where they affect security.

---

## Safety constraints (MUST FOLLOW)

* MUST NOT output, log, or commit secrets.
* MUST NOT "fix" security by disabling protections (weakening auth,
  `allow_origins=["*"]` with credentials, disabling TLS verification).
* MUST provide evidence-based findings: file paths, snippets, config values.
* If a protection might exist in infra, report as "not visible in app code;
  verify at runtime/config".
* CORS is not auth; it only affects browsers.
* CSRF applies only when browser auto-attaches credentials (cookies); not
  relevant for purely header-token APIs. ([OWASP][2])

---

## Audit finding format

For each issue: Rule ID, Severity (Critical/High/Medium/Low), Location
(file + function + lines), Evidence (snippet), Impact, Fix (minimal diff),
Mitigation (defense-in-depth), False positive notes.

---

## Production baseline

* No `debug=True`, `--reload`, or auto-reload in production. ([PyPI][4])
* `TrustedHostMiddleware` or equivalent. ([PyPI][5])
* CORS disabled unless needed; if enabled, strict + least-privilege. ([OWASP][6])
* Auth enforced via dependencies (no missed routes). ([FastAPI][7])
* Cookie flags secure + CSRF addressed if cookies used. ([OWASP][8])
* Request/multipart size limits at edge + app. ([advisory][9])
* Starlette/python-multipart patched (multiple DoS/traversal CVEs). ([advisory][10])

---

## Rules

### FASTAPI-DEPLOY-001: No auto-reload in production

Severity: High

* MUST NOT run `--reload` / `reload=True` in production.
* Detect: search `--reload`, `reload=True`, `watchfiles`, `fastapi dev` in
  Dockerfiles, Procfiles, systemd units.

### FASTAPI-DEPLOY-002: Debug mode off in production

Severity: Critical

* `FastAPI(debug=True)` / Starlette `debug=True` exposes internals. ([PyPI][5])
* Detect: `debug=True`, `DEBUG = True`, env flags mapped to debug.
* Fix: generic error responses to clients; log details internally.

### FASTAPI-OPENAPI-001: Docs disabled/protected in production

Severity: Medium-High

* SHOULD disable `/docs`, `/redoc`, `/openapi.json` for public-facing prod.
* If enabled, MUST protect with auth or network allowlist.
* Fix: `docs_url=None, redoc_url=None, openapi_url=None` or restrict at edge.

---

### FASTAPI-AUTH-001: Auth via dependencies, consistently enforced

Severity: High

* MUST implement auth as `Depends()`/`Security()` dependency, not ad-hoc
  checks inside handlers. ([FastAPI][7])
* Default deny for privileged routers; explicitly mark public routes.
* Detect: endpoints missing `Depends()`; `if user is None: raise` inside
  handlers instead of dependencies.

### FASTAPI-AUTH-002: No secrets in URLs

Severity: High

* Use `Authorization: Bearer` header, not `?token=` / `?api_key=`. ([FastAPI][11])
* Detect: param names `token`, `api_key`, `key`, `secret`, `password`.

### FASTAPI-AUTH-003: Password storage

Severity: Critical

* MUST use Argon2id or bcrypt. Never plaintext, never fast hashes (SHA256).
* Detect: `hashlib.md5/sha1/sha256` on passwords; password fields in
  response models.

### FASTAPI-AUTH-004: JWT validation

Severity: High

* MUST validate signature + enforce algorithm allowlist.
* MUST validate `exp`; validate `iss`/`aud` in multi-service setups. ([FastAPI][12])
* MUST NOT put secrets in JWT payloads (readable by client).
* Detect: `jwt.decode(..., options={"verify_signature": False})`,
  `alg=none`, missing exp validation.

### FASTAPI-AUTHZ-001: Object + property-level authorization

Severity: High

* MUST check ownership/ACL per-object when accessing by user-controlled ID. ([OWASP][13])
* MUST use dedicated response models excluding internal fields.
* Detect: `GET /users/{id}` without authz check; response models with
  roles/permissions/billing/password fields.

---

### FASTAPI-SESS-001: Secure cookie attributes (production + TLS)

Severity: High

* MUST: `Secure` (prod only -- use `SESSION_COOKIE_SECURE` toggle for
  dev/test), `HttpOnly`, `SameSite=Lax` (or `Strict`). ([OWASP][8])
* Starlette `SessionMiddleware`: set `https_only=True` in prod,
  appropriate `same_site`. ([PyPI][5])
* Detect: `SessionMiddleware(` params, `set_cookie(` flags.

### FASTAPI-SESS-002: No secrets in signed session cookies

Severity: High

* Signed != encrypted. Store only opaque IDs; sensitive state server-side.
* Detect: `request.session[...] =` storing tokens/PII.

### FASTAPI-CSRF-001: CSRF for cookie-authenticated state changes

Severity: High

Only applies to cookie-based auth. If auth is via `Authorization` header,
CSRF is not applicable. ([FastAPI][11])

* MUST protect POST/PUT/PATCH/DELETE with CSRF tokens when cookie auth.
* Detect: cookie-auth state-changing endpoints without CSRF validation;
  GET used for state changes.

---

### FASTAPI-VALID-001: Schema-driven validation; prevent mass assignment

Severity: Medium

* MUST use Pydantic models for bodies, not `dict`/`Any`. ([OWASP][14])
* SHOULD reject unexpected fields on write endpoints.
* Detect: `await request.json()` + `Model(**payload)` or `db.update(**payload)`
  with unfiltered input; models accepting extra fields.

### FASTAPI-RESP-001: Prevent excessive data exposure

Severity: Medium

* MUST define response models with only intended fields. ([FastAPI][15])
* Use separate models: create-input, db/internal, public-output.
* Detect: returning ORM objects without `response_model`; response
  containing `password_hash`, `is_admin`, internal fields.

---

### FASTAPI-XSS-001: XSS in HTML responses

Severity: High (if serving HTML)

* MUST use auto-escaping templates. Never mark untrusted content safe.
* Deploy CSP for user content pages. ([OWASP][16])
* Note: pure JSON APIs -- XSS is client concern, but error/docs pages may
  render HTML.

### FASTAPI-SSTI-001: Server-Side Template Injection

Severity: Critical

* MUST NOT render templates containing user-controlled syntax. ([OWASP][17])
* Detect: `Environment.from_string`, `Template(...)` with user/DB input.
* Fix: simple string substitution; if needed, Jinja sandbox. ([Jinja][18])

---

### FASTAPI-HEADERS-001: Security headers

Severity: Medium

* SHOULD set: `X-Content-Type-Options: nosniff`, clickjacking protection
  (if HTML), `Referrer-Policy`, `Permissions-Policy`.
* If not in app code, flag as "verify at edge". ([OWASP][6])

### FASTAPI-CORS-001: CORS least-privilege

Severity: Medium-High

* Disabled if not needed. If needed: explicit origin allowlist.
* MUST NOT `allow_origins=["*"]` + `allow_credentials=True`.
* Detect: `CORSMiddleware` config, `allow_origin_regex=".*"`.

### FASTAPI-HOST-001: Host header validation

Severity: Low

* SHOULD use `TrustedHostMiddleware` in production. ([PyPI][5])
* MUST NOT trust `Host` for security decisions (password reset links,
  callback URLs) without validation.
* Detect: `request.url`, `request.base_url` used to build external URLs.

### FASTAPI-PROXY-001: Reverse proxy trust

Severity: High

* MUST configure forwarded-header trust correctly behind proxy.
* MUST restrict `forwarded_allow_ips` to known proxy IPs. ([PyPI][4])
* Detect: `--proxy-headers`, `--forwarded-allow-ips`; security use of
  `request.client.host`, `request.headers["x-forwarded-for"]`.

---

### FASTAPI-LIMITS-001: Request/multipart size limits

Severity: Low

* Enforce at edge + app. Historical multipart DoS vectors. ([advisory][9])
* Detect: file upload endpoints, `multipart/form-data` without limits.

### FASTAPI-FILES-001: Path traversal / unsafe static files

Severity: High

* MUST NOT pass user-controlled paths to `FileResponse`. ([advisory][10])
* Keep Starlette updated (path traversal CVE in StaticFiles < 0.27.0).
* MUST NOT serve user uploads as active content (HTML/JS/SVG) inline.
* Detect: `FileResponse(`, `StaticFiles(`, `open(` in routes with
  untrusted path input.
* Fix: opaque file IDs mapped to server-side paths; serve as attachment.

### FASTAPI-FILES-002: Range-header DoS

Severity: Low

* Keep Starlette patched (FileResponse Range DoS fixed 0.49.1). ([advisory][19])
* Detect: `FileResponse`/`StaticFiles` with affected Starlette versions.

### FASTAPI-UPLOAD-001: File upload safety

Severity: Medium

* Size limits (app + edge), type allowlist (content check, not just ext),
  server-generated filenames, serve active formats as attachment. ([OWASP][20])
* Detect: upload handlers, direct exposure of upload directories.

---

### FASTAPI-INJECT-001: SQL injection

Severity: High

* Parameterized queries or ORM only. No f-string SQL. ([OWASP][21])
* Detect: SQL keywords in Python strings near `.execute(...)`.

### FASTAPI-INJECT-002: OS command injection

Severity: Critical-High

* Avoid shell commands with untrusted input. If subprocess needed:
  args as list, no `shell=True`, strict allowlists. ([OWASP][22])
* Detect: `os.system`, `subprocess`, `Popen`, `shell=True`.

### FASTAPI-SSRF-001: SSRF in outbound HTTP

Severity: Medium-High (cloud/VPC)

* Validate/restrict destinations for user-influenced URL fetches.
* Block localhost/private IPs/metadata endpoints; restrict to http/https.
* Detect: `httpx`/`requests`/`urllib`/`aiohttp` with URLs from
  request/DB; endpoints named `fetch`, `preview`, `proxy`, `webhook`. ([OWASP][23])

### FASTAPI-REDIRECT-001: Open redirects

Severity: Low

* Validate redirect targets from untrusted input (`next`, `redirect`,
  `return_to`). Prefer same-site relative paths or domain allowlist. ([OWASP][24])
* Detect: `RedirectResponse(` with user-controlled target.

### FASTAPI-WS-001: WebSocket auth and cross-site protection

Severity: Medium-High

* MUST authenticate WebSocket connections for non-public channels. ([OWASP][25])
* Validate Origin for browser clients; rate limit messages/connections.
* Detect: `@app.websocket` / `websocket_endpoint` without auth;
  query-string tokens without rotation.

### FASTAPI-SUPPLY-001: Dependency patch hygiene

Severity: Low

* Pin and update: FastAPI, Starlette, Uvicorn, Pydantic, python-multipart,
  auth/JWT libs. Treat file serving + multipart deps as security-sensitive.

Historical CVEs:

* StaticFiles path traversal -- fixed 0.27.0 ([advisory][10])
* Multipart DoS -- fixed 0.40.0 ([advisory][9])
* FileResponse Range DoS -- fixed 0.49.1 ([advisory][19])

---

## Scanning heuristics

| Category          | Grep patterns                                                                   |
| ----------------- | ------------------------------------------------------------------------------- |
| Dev/debug         | `--reload`, `reload=True`, `debug=True`, `FastAPI(debug=True)`                  |
| Docs exposure     | `/docs`, `/redoc`, `/openapi.json`, `docs_url=`, `openapi_url=`                 |
| Auth gaps         | Endpoints missing `Depends()`/`Security()`; `token=`, `api_key=` in query       |
| Session/CSRF      | `SessionMiddleware(`, `https_only`, `same_site`; cookie-auth POST without CSRF  |
| Mass assignment   | `await request.json()` + direct DB writes; models accepting extras              |
| Data exposure     | ORM objects returned without `response_model`; password/role fields in response |
| CORS              | `CORSMiddleware` + `allow_origins=["*"]`, `allow_credentials=True`              |
| Files             | `FileResponse(` + user path; `StaticFiles(` exposing uploads                    |
| Multipart         | No size/field constraints; outdated Starlette/python-multipart                  |
| SQL injection     | SQL f-strings near `.execute(...)`                                              |
| Command injection | `subprocess.*`, `shell=True`, `os.system`                                       |
| SSRF              | `httpx.get/post`, `requests.*` with URL from request/DB                         |
| Redirects         | `RedirectResponse(next)` unvalidated                                            |
| WebSockets        | `@app.websocket` without auth/origin checks                                     |

For each finding, confirm: data origin (untrusted?), sink type, protective
controls present, dependency versions vs vulnerable ranges.

---

## Sources

[1]: https://pypi.org/project/fastapi/ "https://pypi.org/project/fastapi/"
[2]: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html"
[4]: https://pypi.org/project/uvicorn/ "https://pypi.org/project/uvicorn/"
[5]: https://pypi.org/project/starlette/ "https://pypi.org/project/starlette/"
[6]: https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html?utm_source=chatgpt.com "HTTP Security Response Headers Cheat Sheet"
[7]: https://fastapi.tiangolo.com/reference/dependencies/ "Dependencies - FastAPI"
[8]: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html"
[9]: https://advisories.gitlab.com/pkg/pypi/starlette/CVE-2024-47874/ "Starlette DoS via multipart/form-data"
[10]: https://advisories.gitlab.com/pkg/pypi/starlette/CVE-2023-29159/ "Starlette Path Traversal in StaticFiles"
[11]: https://fastapi.tiangolo.com/tutorial/security/first-steps/?utm_source=chatgpt.com "Security - First Steps - FastAPI"
[12]: https://fastapi.tiangolo.com/tutorial/response-model/ "https://fastapi.tiangolo.com/tutorial/response-model/"
[13]: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ "https://owasp.org/API-Security/editions/2023/en/0x11-t10/"
[14]: https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html "https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html"
[15]: https://fastapi.tiangolo.com/tutorial/extra-models/ "https://fastapi.tiangolo.com/tutorial/extra-models/"
[16]: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"
[17]: https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server_Side_Template_Injection?utm_source=chatgpt.com "Testing for Server Side Template Injection"
[18]: https://jinja.palletsprojects.com/en/stable/sandbox/?utm_source=chatgpt.com "Sandbox — Jinja Documentation (3.1.x)"
[19]: https://advisories.gitlab.com/pkg/pypi/starlette/CVE-2025-62727/ "Starlette vulnerable to O(n^2) DoS via Range header merging in ``starlette.responses.FileResponse`` | GitLab Advisory Database"
[20]: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html"
[21]: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
[22]: https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html "https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html"
[23]: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html "https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html"
[24]: https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html?utm_source=chatgpt.com "Unvalidated Redirects and Forwards Cheat Sheet"
[25]: https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html?utm_source=chatgpt.com "WebSocket Security - OWASP Cheat Sheet Series"
