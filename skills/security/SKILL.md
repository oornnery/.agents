---
name: security
description: Security review, threat modeling, and secure-by-default guidance.
  Load when writing code with security in mind, reviewing changes for
  vulnerabilities, auditing risk, or producing a threat model.
---

# Security

App security guidance. Framework- and language-agnostic. Principles and review patterns across APIs, backends, frontends, workers, CLIs, and external integrations.

## Boundary

Security reasoning, review order, threat modeling, and risk prioritization.

- pair with `python` for secure Python code
- pair with `design` for risk in API shape, BFF boundaries, or UI trust
- pair with `quality` for RCA or regression guards after fix

Not for framework-specific secure coding notes.

## Assets

Use these when deliverable should look like real security work product.

- `assets/threat-model.md` -- filled threat model template
- `assets/audit-report.md` -- compact review findings report
- `assets/findings.md` -- small findings list in expected evidence format

## Operating Modes

1. **Generation** (default) -- write secure-by-default code.
2. **Passive review** (always on) -- notice violations in touched code.
3. **Active audit** (explicit request) -- systematic scan with report.
4. **Threat modeling** (explicit request) -- map assets, trust boundaries,
   abuse paths, and mitigations before or alongside impl.

## Audit Workflow

1. Define scope: entry points, data stores, external services, privileged
   ops, and sensitive user flows.
2. Identify assets: credentials, secrets, personal data, money movement,
   integrity-critical state, admin actions, and internal systems access.
3. Map trust boundaries: browser to server, public to private network,
   service to service, user to admin, tenant to tenant, and app to third party.
4. Treat all external input as attacker-controlled until validated.
5. Review system using checklist below, prioritizing auth,
   authorization, data exposure, and injection first.
6. Record concrete findings with evidence, impact, and minimal safe fix.

## Core Principles

- Default deny. Require explicit allow rules for access, origins, methods,
  fields, actions, and integrations.
- Validate at boundaries. Parse, validate, normalize, and constrain external
  input before business logic uses it.
- Least privilege. Grant minimum permissions needed for users, services,
  tokens, files, queries, and background jobs.
- Defense in depth. Assume one control may fail; keep independent layers.
- Minimize exposure. Return only needed data, log only needed data, and expose
  only endpoints and capabilities system truly needs.
- Keep secrets out of code, logs, URLs, client storage, and error messages.
- Prefer safe defaults in prod. Debug features, test shortcuts, and broad
  trust should be opt-in only for local dev.
- Security is systemic. Stored data, queue messages, database content, and
  third-party responses can all be attacker-controlled.

## Untrusted Input Sources

- Request paths, query params, headers, cookies, bodies, and uploaded files
- Webhooks, queue messages, scheduled job payloads, and CLI arguments
- Env variables and config from outside repo
- Database content that originated from users or external systems
- Third-party API responses, redirects, and downloaded files
- Browser storage, URL fragments, cross-window messages, and DOM content

## Review Order

1. Authentication and authorization
2. Secrets, session handling, and data exposure
3. Valid, output encoding, and injection
4. File handling, redirects, and outbound network access
5. Browser, cross-origin, and client-side trust boundaries
6. Availability, abuse resistance, and resource exhaustion
7. Logging, monitoring, dependency hygiene, and operational hardening

## Security Checklist

### Production Baseline

- Dev servers, hot reload, debug endpoints, and verbose error pages are off
  or protected in prod.
- Admin, docs, internal tooling, and operational endpoints are protected or
  disabled when not needed.
- Host, origin, proxy, and deployment trust are explicitly configured rather
  than inferred from arbitrary headers.
- TLS expectations are clear at edge, and transport security assumptions
  match actual deployment topology.
- Dependencies are pinned or otherwise controlled, patched regularly, and
  sourced from trusted registries or internal mirrors.

### Authentication and Authorization

- Authentication is enforced consistently on all protected ops.
- Authorization is checked per action and per object, not only at route entry.
- Privileged fields, admin actions, and cross-tenant access paths have
  explicit checks.
- Tokens, sessions, and API keys are validated correctly, rotated when needed,
  and scoped to minimum required privileges.
- Passwords and other credentials are never stored or compared in plaintext.
- Secrets are not placed in URLs, hidden form fields, client-readable storage,
  or source control.
- State-changing actions using ambient credentials have replay and CSRF
  protections where applicable.

### Validation and Data Exposure

- External input is schema-driven, validated, normalized, and bounded.
- Unexpected fields, unsafe enum values, and malformed state transitions are
  rejected over ignored.
- Length, size, count, pagination, and rate limits exist where input could
  grow without bound.
- Responses return minimum needed fields and avoid leaking internal state,
  secrets, stack traces, or sensitive identifiers.
- Error messages are useful but do not expose credentials, tokens, queries,
  file paths, internal topology, or exploitable details.

### Injection and Code Execution

- Queries, commands, templates, and interpreters never receive attacker input
  through string concatenation or equivalent unsafe composition.
- Dynamic code execution and unsafe deserialization are avoided unless there is
  compelling, isolated, and tightly controlled reason.
- Output is encoded or escaped for target sink so untrusted content cannot
  become executable code, markup, templates, or policy directives.
- Untrusted template sources, HTML fragments, selectors, expressions, or
  config snippets are treated as code execution risk.
- File paths derived from input are normalized and confined to approved roots.

### Files, URLs, and External Calls

- Uploads are validated by size, type, extension, and storage location before
  further processing.
- Downloaded or generated files are served from safe locations with correct
  content-type and disposition handling.
- Outbound requests guard against SSRF with protocol restrictions, destination
  valid, timeouts, and network allowlists where appropriate.
- Redirect targets are validated so attackers cannot bounce users to
  arbitrary destinations.
- Archive extraction, image processing, and document parsing consider zip
  bombs, parser exploits, and unsafe metadata.

### Browser and Cross-Origin Concerns

- Untrusted data is not inserted into executable browser sinks such as raw HTML,
  script contexts, event handlers, or dynamic navigation targets.
- Cross-origin access is least-privilege: only required origins, methods,
  headers, and credentials are allowed.
- Browser-delivered policies such as CSP and related headers are used when
  app serves HTML or script-capable content.
- Cross-window and real-time messaging validate origin, peer, and message type.
- Client-side storage is treated as readable by user and often by injected
  code; do not store high-value secrets there.

### Availability and Abuse Resistance

- Request, body, upload, query, and fan-out limits exist for expensive paths.
- Expensive ops have timeouts, pagination, batching, or backpressure.
- Idempotency and replay handling exist where duplicate submissions are risky.
- Rate limits or quota controls exist for brute-force, spam, scraping, and
  resource exhaustion paths.
- Background work, file parsing, and external calls cannot be used to create
  unbounded compute, storage, or network amplification.

### Logging, Monitoring, and Supply Chain

- Logs omit secrets, credentials, session material, highly sensitive payloads,
  and raw attacker-controlled blobs unless strictly necessary.
- Security-relevant events are observable: auth failures, permission denials,
  suspicious input, administrative changes, and abnormal outbound traffic.
- Audit trails exist for privileged and integrity-critical actions.
- Dependencies, containers, base images, and build tooling are reviewed for
  provenance, patch level, and known vulnerabilities.
- Third-party integrations are scoped narrowly and reviewed as part of
  trust boundary, not assumed safe because they are popular.

## Finding Format

```text
- Rule ID: SEC-XXX
- Severity: Critical / High / Medium / Low
- Location: file:line
- Evidence: code or configuration evidence
- Impact: what could go wrong
- Fix: minimal safe change
```

## Threat Modeling Workflow

1. **Scope** -- components, actors, external integrations, sensitive flows.
2. **Assets** -- credentials, money movement, PII, internal systems access,
   integrity-critical records, admin actions.
3. **Entry points** -- UI, API, webhooks, files, jobs, CLI, support tooling.
4. **Trust boundaries** -- where identity, origin, or privilege changes.
5. **Threats** -- abuse paths such as exfiltration, escalation, tampering,
   replay, impersonation, and DoS.
6. **Controls** -- existing mitigations and their assumptions.
7. **Residual risk** -- what remains exploitable or fragile.
8. **Mitigations** -- concrete recommendations tied to specific locations.

Output: `<repo-name>-threat-model.md`

## Risk Prioritization

- **Critical**: unauthenticated code execution, auth bypass, cross-tenant
  access, key theft, or destructive integrity compromise
- **High**: sensitive data exposure, SSRF to internal systems, unsafe file
  handling, command execution, significant privilege escalation
- **Medium**: targeted DoS, open redirect with realistic abuse path,
  limited-scope authorization gaps, unsafe defaults with real exposure
- **Low**: low-sensitivity leaks, defense-in-depth gaps, unlikely-precondition
  issues, observability gaps without direct exploitability
