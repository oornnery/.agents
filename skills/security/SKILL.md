---
name: security
description: Security review, threat modeling, and best-practices audit. Load when
  performing security reviews, writing secure code, threat modeling, or auditing
  vulnerabilities. Supports Python (FastAPI, Django, Flask), JS/TS, Go.
---

# Security

Security review and threat modeling. Load framework-specific references
from `references/` based on the detected stack.

## Operating Modes

1. **Generation** (default) -- write secure-by-default code.
2. **Passive review** (always on) -- notice violations in touched code.
3. **Active audit** (explicit request) -- systematic scan with report.

## Audit Workflow

1. Identify languages and frameworks in the project
2. Load relevant references from `references/`
3. Scan using the OWASP checklist below
4. Output findings in structured format

## OWASP Checklist (Python)

### Injection (Critical)

- SQL: raw string queries, f-string in SQL, missing parameterization
- Command: `subprocess` with `shell=True`, `os.system`, unsanitized args
- Path traversal: user input in file paths without validation
- Template: Jinja2 with `| safe` on user data

### Authentication and Authorization

- Missing auth checks on protected routes
- Permission bypass (checking auth but not authorization)
- Session/token mishandling (hardcoded secrets, weak algorithms)
- Default credentials or admin backdoors

### Data Exposure

- Secrets in code: API keys, passwords, tokens (grep for patterns)
- Sensitive data in logs or error responses
- Missing `.env` / credential rotation
- Overly permissive CORS

### Input Validation

- Missing Pydantic models at API boundaries
- `strict=False` where `strict=True` is needed
- Missing `extra="forbid"` allowing injection of unexpected fields
- Unbounded input (no max length, no pagination limits)

### Dependencies

- Known CVEs in pinned versions
- Unpinned dependencies allowing supply chain attacks

## Finding Format

```text
- Rule ID: SEC-XXX
- Severity: Critical / High / Medium / Low
- Location: file:line
- Evidence: code snippet
- Impact: what could go wrong
- Fix: minimal safe change
```

## Threat Modeling Workflow

1. **Scope** -- components, data stores, external integrations
2. **Boundaries** -- trust boundaries with protocol/auth/encryption
3. **Assets** -- credentials, PII, integrity-critical state
4. **Threats** -- abuse paths (exfiltration, escalation, DoS)
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

- `commands/review.md` -- code review (Agent 4: Security Reviewer)
