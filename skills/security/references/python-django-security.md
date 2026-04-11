# Django Security Spec (Django 6.0.x, Python 3.x)

## Constraints

- MUST NOT output/log/commit secrets (`SECRET_KEY`, `SECRET_KEY_FALLBACKS`, DB passwords, session cookies).
- MUST NOT "fix" security by disabling protections (removing `CsrfViewMiddleware`, `@csrf_exempt` everywhere, `ALLOWED_HOSTS=['*']`, disabling auto-escaping).
- MUST provide evidence-based audit findings: file paths, snippets, config values.
- If a protection might exist in infrastructure (proxy, WAF, CDN), report as "not visible in app code; verify at runtime/edge config".
- MUST prefer Django built-ins (middleware, auth, forms, ORM) over custom security logic. ([ref][1])

## Operating Modes

**Generation** (default): follow all MUST/SHOULD rules; prefer safe-by-default Django APIs; avoid introducing risky sinks (dynamic template rendering, unsafe redirects, shell exec, raw SQL formatting, SSRF-capable fetchers).

**Passive review** (always on while editing): notice violations in touched/nearby code; mention with brief fix.

**Active audit** (explicit scan): systematically search codebase; output structured findings.

## Untrusted Input (treat as attacker-controlled)

- `request.GET`, `request.POST`, `request.FILES`, `request.body`, `request.data` (DRF)
- URL path parameters (`<int:id>`, `<slug:...>`)
- `request.headers` / `request.META` (including `HTTP_HOST`, `HTTP_X_FORWARDED_*`)
- `request.COOKIES`
- External systems (webhooks, third-party APIs, message queues)
- Persisted user content (DB rows, cached content, file uploads)

## Audit Finding Format

Rule ID | Severity | Location (file:line) | Evidence (snippet) | Impact | Fix (minimal diff) | Mitigation | False-positive notes

Audit order: deployment entrypoints > settings > middleware > authn/authz > CSRF > templates/XSS > file handling > injection > SSRF > redirects/CORS/headers > dependencies.

---

## Production Baseline

### Settings Management

- Load `SECRET_KEY` and DB passwords from env/secret manager, never hardcode. ([ref][1])
- Separate dev/prod settings; prod defaults must fail closed.

### Minimum Requirements

| Setting/Rule            | Requirement                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `DEBUG`                 | `False` in prod ([ref][1])                                            |
| `SECRET_KEY`            | Strong random, secret, not in source control ([ref][1])               |
| `SECRET_KEY_FALLBACKS`  | Remove old keys after rotation window ([ref][1])                      |
| `ALLOWED_HOSTS`         | Explicit domains, no `['*']` ([ref][1])                               |
| `CSRF_COOKIE_SECURE`    | `True` when TLS enabled ([ref][1])                                    |
| `SESSION_COOKIE_SECURE` | `True` when TLS enabled ([ref][1])                                    |
| Entrypoint              | Production WSGI/ASGI server, not `manage.py runserver` ([ref][1])     |
| Uploads                 | Untrusted; never executable; `MEDIA_ROOT` != `STATIC_ROOT` ([ref][1]) |

---

## Rules

### DJANGO-DEPLOY-001: No dev server in production (High)

- MUST NOT deploy `manage.py runserver` as production entrypoint.
- MUST use production WSGI/ASGI server (gunicorn, uvicorn, daphne, etc.). ([ref][1])
- `runserver` is fine for local development; only flag if used as production entrypoint.
- **Detect**: `manage.py runserver` or `runserver 0.0.0.0` in Dockerfile CMD/ENTRYPOINT, Procfile, systemd units, Helm charts, `--insecure` flag.

### DJANGO-DEPLOY-002: `DEBUG=False` in production (High)

- `DEBUG=True` leaks source excerpts, local variables, settings, and installed apps. ([ref][1])
- MUST set `DEBUG=False` in prod; use safe logging/monitoring for errors.
- **Detect**: `DEBUG = True`, `DEBUG=os.environ.get(..., True)` (unsafe default), prod settings importing dev defaults.

### DJANGO-CONFIG-001: `SECRET_KEY` management (High/Critical)

- MUST NOT commit to source control, print, or log.
- MUST load from env or secret store (not hardcoded). ([ref][1])
- MUST NOT reuse across environments.
- Rotate via `SECRET_KEY_FALLBACKS`: set new key, keep old in fallbacks temporarily, remove after rotation window. ([ref][1])
- **Detect**: `SECRET_KEY =` with literal string in repo, `SECRET_KEY_FALLBACKS` with long-expired keys, `print(settings.SECRET_KEY)`, committed `.env` files.

### DJANGO-HOST-001: Strict `ALLOWED_HOSTS` (Medium)

- MUST set to expected domains in production. ([ref][1])
- `['*']` requires your own Host validation to prevent CSRF/cache-poisoning/poisoned email links. ([ref][2])
- `[]` with `DEBUG=False` prevents the site from running.
- SHOULD configure fronting web server to reject unknown hosts (defense-in-depth). ([ref][1])
- **Detect**: `ALLOWED_HOSTS = ['*']` or env expanding to `*`; check platform env overrides.
- **Fix**: `ALLOWED_HOSTS = ['example.com', 'www.example.com']` for prod; keep dev hosts separate.

### DJANGO-HTTPS-001: Secure cookie transport under TLS (High)

Only when TLS is enabled:

| Setting                 | Value                                    |
| ----------------------- | ---------------------------------------- |
| `CSRF_COOKIE_SECURE`    | `True`                                   |
| `SESSION_COOKIE_SECURE` | `True`                                   |
| `SECURE_SSL_REDIRECT`   | `True` (with correct proxy config)       |
| `SECURE_HSTS_SECONDS`   | Start low, validate, increase ([ref][3]) |

- **Detect**: `*_SECURE=False` in prod HTTPS settings.

### DJANGO-PROXY-001: `SECURE_PROXY_SSL_HEADER` (Medium)

- Set ONLY if proxy strips inbound spoofed headers. Misconfig compromises security. ([ref][3])
- Infinite redirect loops after `SECURE_SSL_REDIRECT=True` = wrong HTTPS detection.
- **Detect**: `SECURE_PROXY_SSL_HEADER` set without proxy header-stripping guarantee.

### DJANGO-SESS-001: Session cookie attributes (Medium)

| Setting                   | Requirement                         |
| ------------------------- | ----------------------------------- |
| `SESSION_COOKIE_SECURE`   | `True` (prod HTTPS)                 |
| `SESSION_COOKIE_HTTPONLY` | `True` (Django default)             |
| `SESSION_COOKIE_SAMESITE` | `Lax` (Django default)              |
| `SESSION_COOKIE_DOMAIN`   | Avoid unless cross-subdomain needed |

- Do NOT set `Secure` in local dev over HTTP; use conditional config.

### DJANGO-SESS-002: CSRF cookie settings (Medium)

- `CSRF_COOKIE_SECURE=True` when HTTPS.
- `CSRF_COOKIE_HTTPONLY=True` only if frontend reads token from DOM, not cookie.
- **Detect**: `CSRF_COOKIE_HTTPONLY=True` + JS reading `csrftoken` cookie = broken AJAX CSRF.

---

### DJANGO-CSRF-001: CSRF protection (High)

- MUST keep `CsrfViewMiddleware` enabled and ordered before views assuming CSRF handled. ([ref][4])
- MUST include `{% csrf_token %}` in POST forms; MUST NOT include in forms POSTing to external URLs (leaks token). ([ref][4])
- AJAX: send token via `X-CSRFToken` header. ([ref][4])
- `@csrf_exempt` only when necessary; replace with alternative control (e.g., webhook signing).
- Cached views needing CSRF: apply `@csrf_protect`. ([ref][4])
- Under HTTPS, CSRF middleware also checks Referer for same-origin. ([ref][2])

**Insecure patterns**:

- Missing `CsrfViewMiddleware` in `MIDDLEWARE`
- `@csrf_exempt` on authenticated views
- GET for state-changing actions

**Detect**: grep `csrf_exempt`, `csrf_protect`, `ensure_csrf_cookie`; enumerate non-GET URL patterns.

---

### DJANGO-XSS-001: Template XSS (High)

- MUST rely on Django auto-escaping (on by default). ([ref][2])
- MUST NOT use `{% autoescape off %}` on untrusted content. ([ref][5])
- MUST NOT use `mark_safe()` or `|safe` on user data.
- MUST quote HTML attributes; unquoted attrs bypass escaping. ([ref][2])
- Use `format_html()` over manual HTML concatenation. ([ref][6])

**Insecure patterns**:

```django
{% autoescape off %}{{ user_input }}{% endautoescape %}
{{ user_input|safe }}
<style class={{ var }}>  {# unquoted attr #}
```

```python
mark_safe(request.GET["q"])
HttpResponse(user_html_value)
```

**Detect**: grep templates for `|safe`, `autoescape off`, `safeseq`; grep Python for `mark_safe`, `SafeString`, HTML concat with request/DB values.

### DJANGO-TEMPLATE-001: No untrusted template source (High/Critical)

- MUST NOT render templates where source string comes from untrusted input.
- Can leak context data, bypass escaping, create XSS.

**Insecure patterns**:

```python
Template(request.GET["tmpl"]).render(Context({...}))
# User templates from DB rendered with app context
```

**Detect**: grep `Template(`, `Engine.from_string`, `.render(Context(` with non-constant strings.
**Fix**: use `string.Template` or explicit placeholders; if user templates required, isolate heavily.

---

### DJANGO-SQL-001: SQL injection (High)

- MUST use ORM/querysets for normal DB access. ([ref][2])
- Raw SQL (`raw()`, `cursor.execute()`, `extra()`, `RawSQL`): MUST use `params=`, MUST NOT string-interpolate. ([ref][7])
- MUST NOT quote `%s` placeholders (documented as unsafe). ([ref][8])

**Insecure patterns**:

```python
cursor.execute(f"SELECT ... WHERE id={request.GET['id']}")
Model.objects.raw("... %s" % user_input)
extra(where=[f"headline='{q}'"])
# Quoted placeholder: WHERE othercol = '%s'
```

**Detect**: grep `.raw(`, `.extra(`, `RawSQL(`, `cursor.execute(`, SQL keywords in Python strings.

### DJANGO-CMD-001: OS command injection (Critical/High)

- MUST pass subprocess args as list, not shell string.
- MUST NOT use `shell=True` with attacker-influenced content.
- Prefer pure-Python libraries.

**Detect**: grep `os.system`, `subprocess`, `Popen`, `shell=True`; trace request/DB inputs.

---

### DJANGO-UPLOAD-001: File upload safety (High)

- All uploads untrusted; never serve as executable. ([ref][1])
- Enforce size limits at web server level. ([ref][2])
- Validate types with allowlists + content checks (not extension only).
- Store outside app code and static roots.
- Serve from separate domain to reduce same-origin impact. ([ref][2])
- Polyglot risk: valid PNG header + HTML content may be served as HTML. ([ref][2])

**Detect**: grep `request.FILES`, `FileField`, `ImageField`; inspect `MEDIA_URL`/`MEDIA_ROOT`; check web server media config.
**Fix**: force `Content-Disposition: attachment` for risky types; separate domain for user content.

### DJANGO-PATH-001: Path traversal (High)

- MUST NOT use user input as filesystem path.
- `MEDIA_ROOT` and `STATIC_ROOT` must be distinct. ([ref][3])
- Use server-side IDs mapped to known files.

**Detect**: grep `open(`, `Path(`, `os.path.join(` with request values; check `MEDIA_ROOT`/`STATIC_ROOT` equality.

### DJANGO-REDIRECT-001: Open redirects (Medium/High)

- MUST validate redirect targets from untrusted input (`next`, `return_to`).
- Use `django.utils.http.url_has_allowed_host_and_scheme()`.
- Default to safe internal path on validation failure.

**Detect**: grep `redirect(` + trace target origin; grep params named `next`, `return_to`, `redirect`, `url`.

---

### DJANGO-HEADERS-001: Security headers (Medium/High)

`SecurityMiddleware` settings (defaults shown):

| Setting                             | Default       | Purpose         |
| ----------------------------------- | ------------- | --------------- |
| `SECURE_CONTENT_TYPE_NOSNIFF`       | `True`        | nosniff         |
| `SECURE_REFERRER_POLICY`            | `same-origin` | Referrer-Policy |
| `SECURE_CROSS_ORIGIN_OPENER_POLICY` | `same-origin` | COOP            |

- Enable `XFrameOptionsMiddleware` unless third-party framing required. ([ref][2])
- Headers may be set at edge; if not in app code, flag "verify at edge".

**Detect**: inspect `MIDDLEWARE` for `SecurityMiddleware`, `XFrameOptionsMiddleware`; grep per-view disabling.

### DJANGO-CSP-001: Content Security Policy (Medium/High)

- CSP `script-src` is the most critical directive.
- MUST NOT exclude routes from CSP (unprotected page undermines protected pages). ([ref][2])
- Start with `SECURE_CSP_REPORT_ONLY`, then enforce. ([ref][3])
- Avoid `unsafe-inline` without justification.

**Detect**: grep `SECURE_CSP`, `SECURE_CSP_REPORT_ONLY`; inspect proxy/CDN for CSP headers.

---

### DJANGO-AUTH-001: Password storage (High)

- MUST use Django's built-in password hashing (`user.set_password()`); never plaintext or reversible encryption.
- SHOULD prefer modern hashers (Argon2, bcrypt, scrypt) and keep `PASSWORD_HASHERS` updated. ([ref][3])
- SHOULD configure `AUTH_PASSWORD_VALIDATORS` for production password policy (default is empty). ([ref][3])

**Insecure patterns**:

- Custom password storage or manual hashing bypassing Django auth.
- Plaintext passwords in DB fields.
- No password validators on consumer-facing apps.

**Detect**: grep `.set_password(` vs manual hashing; inspect `PASSWORD_HASHERS`, `AUTH_PASSWORD_VALIDATORS`.
**Fix**: use Django auth model APIs; enable validators appropriate to risk profile.

### DJANGO-AUTHZ-001: Authorization (High)

- MUST enforce authorization on every privileged action (view, modify, admin operations).
- MUST NOT rely on UI-only restrictions (hiding buttons) without server-side checks.
- SHOULD use Django permissions/groups and per-object authorization patterns.
- `is_authenticated` alone is insufficient; check object-level access.

**Insecure patterns**:

- Views assuming "logged in" implies "authorized".
- Missing authorization on update/delete endpoints.

**Detect**: enumerate state-changing views; verify ownership/permission checks; look for only `is_authenticated` or `is_staff` without object-level checks.
**Fix**: add explicit permission checks and tests for unauthorized access.

### DJANGO-ADMIN-001: Admin hardening (High)

- MUST protect admin with strong auth and HTTPS-only transport. ([ref][1])
- SHOULD restrict exposure: IP allowlist, VPN, SSO, or additional auth controls.
- SHOULD audit admin extensions and third-party apps for XSS/CSRF.

**Insecure patterns**:

- Admin exposed to internet with weak auth or over HTTP.

**Detect**: grep `admin.site.urls` in urlpatterns; check deployment IP restrictions and auth gateways.
**Fix**: add network controls, enforce HTTPS, consider changing admin URL path.

### DJANGO-LOG-001: Logging safety (Medium/High)

- MUST NOT log secrets (`SECRET_KEY`, session cookies, auth headers, password reset tokens).
- MUST configure production logging deliberately; review before deployment. ([ref][1])
- `DEBUG=False` prevents exceptions rendering with sensitive context.

**Insecure patterns**:

- Logging full request headers or cookies in production.
- `print(settings.__dict__)` or `logging.info(request.META)`.

**Detect**: inspect `LOGGING` config; grep `print(settings`, `logging.info(request.META)`; search for middleware logging request headers/cookies.
**Fix**: redact sensitive values; log IDs not secrets; use structured logging.

### DJANGO-SUPPLY-001: Dependency hygiene (Medium/High)

- SHOULD pin and regularly update Django + security-critical deps.
- MUST respond to Django security releases promptly.

**Detect**: check `requirements.txt`/lockfiles/build images; compare Django version against [downloads page][9].
**Fix**: upgrade to patched versions; add regression tests for previously vulnerable patterns.

---

## Scanning Quick Reference

| Category      | Grep patterns                                                                |
| ------------- | ---------------------------------------------------------------------------- |
| Dev server    | `manage.py runserver`, `runserver 0.0.0.0`, `--insecure`                     |
| Debug/secrets | `DEBUG = True`, `SECRET_KEY =`, `SECRET_KEY_FALLBACKS`                       |
| Hosts         | `ALLOWED_HOSTS = ['*']`                                                      |
| HTTPS/proxy   | `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SECURE_PROXY_SSL_HEADER`      |
| Cookies       | `SESSION_COOKIE_*`, `CSRF_COOKIE_*`                                          |
| CSRF bypass   | `csrf_exempt`, missing `CsrfViewMiddleware`, POST without `{% csrf_token %}` |
| XSS           | `\|safe`, `autoescape off`, `mark_safe(`, HTML concat                        |
| SQLi          | `.raw(`, `.extra(`, `RawSQL(`, `cursor.execute(` + formatted strings         |
| Uploads       | `request.FILES`, `MEDIA_ROOT`, `MEDIA_URL`, `MEDIA_ROOT == STATIC_ROOT`      |
| Redirects     | `redirect(request.GET.get("next"))`, missing allowlist                       |
| Headers/CSP   | missing `SecurityMiddleware`, missing `SECURE_CSP`                           |

For each finding, confirm: data origin (untrusted?) > sink type > protective controls present > headers set in-app vs edge.

---

## Sources

[1]: https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/ "Deployment checklist"
[2]: https://docs.djangoproject.com/en/6.0/topics/security/ "Security in Django"
[3]: https://docs.djangoproject.com/en/6.0/ref/settings/ "Settings reference"
[4]: https://docs.djangoproject.com/en/6.0/howto/csrf/ "CSRF protection"
[5]: https://docs.djangoproject.com/en/6.0/ref/templates/builtins/ "Template built-ins"
[6]: https://docs.djangoproject.com/en/6.0/ref/utils/ "Utilities reference"
[7]: https://docs.djangoproject.com/en/6.0/topics/db/sql/ "Raw SQL queries"
[8]: https://docs.djangoproject.com/en/6.0/ref/models/querysets/ "QuerySet API reference"
[9]: https://www.djangoproject.com/download/ "Django downloads"
