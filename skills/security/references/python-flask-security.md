# Flask Security Spec (Flask 3.1.x, Python 3.x)

## Constraints

- MUST NOT output/log/commit secrets.
- MUST NOT "fix" security by disabling protections.
- MUST provide evidence-based findings (file paths, snippets, config values).
- If protection might exist at infra level, report as "not visible in app code; verify at runtime/config".

## Audit finding format

Rule ID | Severity | Location (file+function+line) | Evidence (snippet) | Impact | Fix (minimal diff) | Mitigation | False positive notes

## Audit order

1. Entrypoints / deploy scripts / Dockerfiles
2. Config and env handling
3. Auth + sessions + cookies
4. CSRF on state-changing routes
5. Templates: XSS/SSTI
6. File handling + path traversal
7. Injection (SQL, command, deserialization)
8. Outbound requests (SSRF)
9. Redirects
10. CORS + security headers

## Untrusted input sources

`request.args`, `.form`, `.values`, `.get_json()`, `.json`, `.data`, `.headers`, `.cookies`, URL path params, external systems, persisted user content.

## Production baseline config

| Setting                     | Value                                         |
| --------------------------- | --------------------------------------------- |
| `SECRET_KEY`                | Strong random, not committed                  |
| `SESSION_COOKIE_SECURE`     | `True` (prod/HTTPS only; conditional for dev) |
| `SESSION_COOKIE_HTTPONLY`   | `True`                                        |
| `SESSION_COOKIE_SAMESITE`   | `'Lax'` or `'Strict'`                         |
| `TRUSTED_HOSTS`             | Set in production                             |
| Security headers (CSP etc.) | Set in app or at edge                         |

---

## Rules

### FLASK-DEPLOY-001: No dev server in production (High)

- MUST run behind production WSGI server (gunicorn, etc.).
- Detect: `app.run(`, `flask run`, `--debug`, `FLASK_DEBUG` in deploy scripts/Dockerfiles/Procfiles.
- Only flag if clearly used as production entrypoint.

### FLASK-DEPLOY-002: Debug mode disabled in production (Critical)

- Interactive debugger = remote code execution if exposed.
- Detect: `debug=True`, `FLASK_DEBUG=1`, `app.debug = True`, `TRAP_HTTP_EXCEPTIONS`.
- Only flag if clearly production context.

### FLASK-CONFIG-001: SECRET_KEY (High/Critical)

- MUST be strong random, loaded from secret manager/env var.
- MUST NOT be hard-coded or committed.
- MAY use `SECRET_KEY_FALLBACKS` for rotation.
- Detect: `SECRET_KEY =`, `app.secret_key =`, `.env` committed, `print(config)`.

### FLASK-SESS-001: Session cookie attributes (Medium)

- `SESSION_COOKIE_SECURE=True` in prod (conditional for dev HTTP).
- `SESSION_COOKIE_HTTPONLY=True`.
- `SESSION_COOKIE_SAMESITE='Lax'` (or `'Strict'`).
- `SESSION_COOKIE_DOMAIN=None` unless subdomain cookies needed.
- SameSite is defense-in-depth, not a CSRF replacement.
- Detect: `app.config.update(...)`, `set_cookie(..., secure=..., httponly=..., samesite=...)`.

### FLASK-SESS-002: Session lifetime and fixation (Medium)

- SHOULD bound `PERMANENT_SESSION_LIFETIME`.
- SHOULD clear session on login/privilege change.
- MUST NOT store secrets in default cookie sessions (signed, not encrypted).
- Detect: `session[...] =` with sensitive values, missing session clear on login.

### FLASK-CSRF-001: CSRF protection (High)

- If cookies used for auth: MUST protect all state-changing endpoints (POST/PUT/PATCH/DELETE).
- If auth is via Authorization header/bearer token only: no CSRF risk.
- Minimum alternative: require custom header + `SESSION_COOKIE_SAMESITE=lax`.
- MUST NOT use GET for state-changing actions.
- Detect: POST/PUT/PATCH/DELETE routes without CSRF checks; absence of Flask-WTF/CSRF middleware.

### FLASK-XSS-001: Template XSS (High)

- MUST rely on Jinja auto-escaping.
- MUST NOT use `Markup(...)` or `|safe` on untrusted data.
- MUST quote HTML attributes: `value="{{ x }}"` not `value={{ x }}`.
- MUST NOT serve uploaded HTML inline (use `Content-Disposition: attachment`). Only relevant for document uploads, not images.
- SHOULD deploy CSP.
- Detect: `Markup(`, `|safe`, unquoted attributes in templates, file-serving routes without `as_attachment=True`.

### FLASK-SSTI-001: Server-Side Template Injection (Critical)

- MUST NOT render user-controlled template syntax.
- `render_template_string` and `Environment.from_string(...).render(...)` are dangerous with untrusted input.
- MUST NOT use `.format()` on user-controlled strings.
- Detect: `render_template_string`, `from_string`, `.render(` with dynamic strings.
- Fix: use `string.Template` or `str.replace` instead.

### FLASK-HEADERS-001: Security headers (Medium)

- SHOULD set: CSP, `X-Content-Type-Options: nosniff`, clickjacking protection (`X-Frame-Options` / CSP `frame-ancestors`).
- May be set via proxy/CDN -- check for evidence.
- Detect: `after_request` hooks, Flask-Talisman, reverse proxy config.

### FLASK-LIMITS-001: Request size limits (Low/Medium)

- SHOULD set `MAX_CONTENT_LENGTH`, `MAX_FORM_MEMORY_SIZE`, `MAX_FORM_PARTS`.
- Enforce at reverse proxy level too.

### FLASK-HOST-001: Host header validation (Low)

- MUST set `TRUSTED_HOSTS` in production. MUST NOT rely on `SERVER_NAME` for this.
- Detect: `url_for(..., _external=True)` without host validation.

### FLASK-PROXY-001: Reverse proxy trust (Medium/High)

- MUST configure `ProxyFix` with correct hop counts. MUST NOT blindly trust `X-Forwarded-*`.
- Detect: `ProxyFix` settings, `request.remote_addr`/`.scheme`/`.host` in security logic.

### FLASK-PATH-001: Path traversal (High)

- MUST NOT pass user-controlled paths to `send_file` or `open`.
- MUST use `send_from_directory`, `safe_join` (from `werkzeug.security`), `secure_filename`.
- SHOULD use `safe_join` over `os.path.join` for any path with untrusted components.
- Detect: `send_file(`, `open(`, `os.path.join(`, `pathlib.Path(...)` in file routes.

### FLASK-UPLOAD-001: File uploads (High)

- MUST enforce size limits, validate type via allowlist + content check (not just extension).
- MUST store outside executable/static roots.
- SHOULD generate server-side filenames (random IDs).
- MUST serve active formats as download attachment.
- Detect: `request.files[...]` handlers, `secure_filename` usage.

### FLASK-INJECT-001: SQL injection (High)

- MUST use parameterized queries or ORM.
- Detect: `SELECT`/`INSERT`/`UPDATE`/`DELETE` strings with f-strings/`%` formatting into `.execute(...)`.

### FLASK-INJECT-002: OS command injection (Critical/High)

- MUST avoid shell commands with untrusted input. Prefer pure Python libraries.
- If subprocess necessary: args as list, no `shell=True`, strict allowlists.
- Arguments can be processed as flags even with `shell=False` -- use `--` separator.
- Detect: `os.system`, `subprocess`, `Popen`, `shell=True`.

### FLASK-SSRF-001: SSRF (Medium)

- Most important in LAN/multi-service deployments.
- MUST validate/allowlist outbound URL destinations.
- SHOULD block localhost, private IPs, cloud metadata endpoints.
- MUST allow only `http:`/`https:` protocols.
- Detect: `requests.get/post`, `httpx`, `urllib`, `aiohttp` with untrusted URL sources.

### FLASK-REDIRECT-001: Open redirects (Low)

- MUST validate redirect targets from untrusted input (`next`, `redirect`, `return_to`).
- SHOULD allow only relative paths or allowlisted domains.
- Detect: `redirect(` with `request.args.get(...)`.

### FLASK-HTTP-001: HTTP method safety (Medium)

- MUST NOT change state via GET. MUST NOT put secrets in URLs.
- Detect: GET routes that mutate state; URL params named `token`, `key`, `secret`, `password`.

### FLASK-CORS-001: CORS (Medium/High)

- If not needed, keep disabled.
- MUST allowlist origins (not reflect arbitrary). MUST NOT combine broad origins with credentials.
- Detect: `flask_cors.CORS(`, `Access-Control-Allow-Origin`, `supports_credentials=True` with wildcards.

### FLASK-SUPPLY-001: Dependency hygiene (Low)

- Pin and update Flask, Werkzeug, Jinja2, itsdangerous.
- Note: Werkzeug `safe_join` Windows device-name edge cases (CVE-2025-66221).

---

## Scanning grep patterns

| Category  | Patterns                                                                  |
| --------- | ------------------------------------------------------------------------- |
| Dev/debug | `app.run(`, `flask run`, `--debug`, `DEBUG=True`, `FLASK_DEBUG`           |
| Secrets   | `SECRET_KEY`, `secret_key`, `.env` committed                              |
| Sessions  | `SESSION_COOKIE_SECURE/HTTPONLY/SAMESITE`, `session[...] =`               |
| CSRF      | POST/PUT/PATCH/DELETE without CSRF in cookie-auth apps                    |
| XSS/SSTI  | `Markup(`, `\|safe`, unquoted attrs, `render_template_string`             |
| Files     | `send_file(` + user path, `open(` + user path, `os.path.join` + untrusted |
| Injection | SQL strings + `.execute(...)`, `subprocess.*`, `shell=True`, `os.system`  |
| SSRF      | `requests.get/post`, `httpx` with URL from request/DB                     |
| Redirect  | `redirect(request.args.get("next"))`                                      |
| CORS      | `flask_cors.CORS` permissive configs, wildcard + credentials              |

Confirm for each: data origin, sink type, protective controls present.

---

## Sources

- Flask: [Deploying](https://flask.palletsprojects.com/en/stable/deploying/) | [Debugging](https://flask.palletsprojects.com/en/stable/debugging/) | [Config](https://flask.palletsprojects.com/en/stable/config/) | [Security](https://flask.palletsprojects.com/en/stable/web-security/) | [Proxy Fix](https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/) | [Sessions API](https://flask.palletsprojects.com/en/stable/api/#sessions)
- Werkzeug: [Utilities](https://werkzeug.palletsprojects.com/en/stable/utils/) | [CVE-2025-66221](https://github.com/advisories/GHSA-hgf8-39gv-g3f2)
- Jinja: [Sandbox](https://jinja.palletsprojects.com/en/stable/sandbox/)
- OWASP Cheat Sheets: [Session](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | [XSS](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | [SQLi](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | [OS Cmd Injection](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html) | [SSRF](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | [File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | [Redirects](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html) | [Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
- [OWASP SSTI Testing](https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server_Side_Template_Injection) | [PortSwigger SSTI](https://portswigger.net/web-security/server-side-template-injection)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
