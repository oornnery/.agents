---
name: security
description: Security review, threat modeling, and best-practices audit. Load when
  performing security reviews, writing secure code, threat modeling, or auditing
  vulnerabilities. Supports Python (FastAPI, Django, Flask), JS/TS, Go.
---

# Security

Security review and threat modeling for web applications. Based on
OpenAI's curated security skills and OWASP guidelines.

## Operating Modes

1. **Generation** (default) -- write secure-by-default code following
   best practices for the detected language/framework.
2. **Passive review** (always on while editing) -- notice violations
   in touched/nearby code, mention with brief fix.
3. **Active audit** (explicit request) -- systematic scan, structured
   findings report.

## Audit Workflow

1. Identify languages and frameworks in the project
2. Load relevant references from `references/`
3. Scan in order: entrypoints -> config -> auth -> input validation ->
   templates/XSS -> file handling -> injection -> SSRF -> WebSockets
4. Output findings in structured format (see below)

## Finding Format

```text
- Rule ID: SEC-XXX
- Severity: Critical / High / Medium / Low
- Location: file:line
- Evidence: code snippet
- Impact: what could go wrong
- Fix: minimal safe change
```

## Security Checklist (Language-Agnostic)

### Authentication and Authorization

- Auth enforced consistently via dependencies (no forgotten routes)
- Passwords hashed with bcrypt/scrypt/argon2 -- never MD5/SHA
- JWT: validate signature, expiry, issuer, audience
- Session tokens: cryptographically random, HttpOnly, Secure, SameSite

### Input Validation

- Validate ALL external input at boundaries (Pydantic models)
- Parameterized queries only -- never format SQL strings
- Never `eval()`, `exec()`, `__import__()` with user input
- File uploads: validate type, size, sanitize filename, store outside webroot

### Output and Templates

- Escape all user content in templates (autoescape=True)
- Content-Type headers set correctly
- No sensitive data in error messages or logs

### Configuration

- No debug mode in production
- CORS: strict, least-privilege (never `allow_origins=["*"]` with credentials)
- TrustedHostMiddleware enabled
- CSRF protection for cookie-based auth
- Request size limits set

### Dependencies

- Keep dependencies patched (especially Starlette, python-multipart)
- Pin versions in lockfile

## Threat Modeling

For threat modeling, follow this workflow:

1. **Scope** -- identify components, data stores, external integrations
2. **Boundaries** -- map trust boundaries with protocol/auth/encryption
3. **Assets** -- credentials, PII, integrity-critical state
4. **Threats** -- enumerate as abuse paths (exfiltration, escalation, DoS)
5. **Prioritize** -- likelihood x impact, adjusted for existing controls
6. **Validate** -- confirm assumptions with user before final report
7. **Mitigate** -- concrete recommendations tied to specific locations

Output: `<repo-name>-threat-model.md`

## Risk Prioritization

- **High**: pre-auth RCE, auth bypass, cross-tenant access, key theft
- **Medium**: targeted DoS, partial data exposure, rate-limit bypass
- **Low**: low-sensitivity info leaks, unlikely-precondition issues

## References

- `references/python-fastapi-security.md` -- FastAPI security rules
- `references/python-django-security.md` -- Django security rules
- `references/python-flask-security.md` -- Flask security rules
- `references/javascript-frontend-security.md` -- Frontend XSS/CSP

## Related

- `rules/safety.md` -- operational safety rules
- `rules/python.md` -- input validation at boundaries
- `commands/review.md` -- code review (Agent 4: Security Reviewer)
